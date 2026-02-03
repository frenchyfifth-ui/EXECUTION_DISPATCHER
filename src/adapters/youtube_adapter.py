"""YouTube adapter using the Google API client."""

from __future__ import annotations

import json
import time
from importlib.util import find_spec
from typing import Any, Dict, Iterable, Tuple

from src.adapters.base import BaseAdapter
from src.runtime.results import DispatchResult, ResultStatus


class YouTubeAdapter(BaseAdapter):
    """Dispatches content to YouTube using the YouTube Data API v3."""

    PLATFORM = "YOUTUBE"
    MAX_TEXT_LENGTH = 5000
    REQUIRED_FIELDS = ("client_id", "client_secret", "refresh_token")

    _RETRIABLE_STATUS_CODES: Tuple[int, ...] = (403, 429, 500, 503)
    _MAX_RETRIES = 5

    def dispatch(self, payload: Dict[str, Any]) -> DispatchResult:
        content = payload.get("payload", {})
        if not self.live_mode:
            return self._result(ResultStatus.SUCCESS, "DRY_RUN: YouTube upload skipped.")

        video_file = content.get("video_file")
        if not video_file:
            return self._result(ResultStatus.FAILED, "YouTube dispatch requires video_file.")

        if not self._require_credentials():
            return self._result(
                ResultStatus.FAILED,
                "Missing YouTube credentials. Set YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN.",
            )

        missing = self._missing_packages()
        if missing:
            return self._result(
                ResultStatus.FAILED,
                f"Missing packages for YouTube dispatch: {', '.join(missing)}.",
            )

        try:
            youtube_client = self._build_client()
            request = self._build_upload_request(youtube_client, content)
            response = self._execute_resumable_upload(request)
        except Exception as exc:  # noqa: BLE001 - handled for deterministic result
            return self._result(ResultStatus.FAILED, f"YouTube dispatch failed: {exc}")

        video_id = response.get("id") if isinstance(response, dict) else None
        if not video_id:
            return self._result(ResultStatus.FAILED, "YouTube upload succeeded but returned no video ID.")

        return self._result(ResultStatus.SUCCESS, f"Uploaded video with id={video_id}")

    def _missing_packages(self) -> Iterable[str]:
        required = (
            "googleapiclient",
            "googleapiclient.discovery",
            "googleapiclient.http",
            "google.oauth2.credentials",
            "google.auth.transport.requests",
        )
        missing = [pkg for pkg in required if not find_spec(pkg)]
        return missing

    def _build_client(self):
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build

        credentials = Credentials(
            token=None,
            refresh_token=self.credentials.get("refresh_token"),
            token_uri="https://oauth2.googleapis.com/token",
            client_id=self.credentials.get("client_id"),
            client_secret=self.credentials.get("client_secret"),
            scopes=["https://www.googleapis.com/auth/youtube.upload"],
        )
        credentials.refresh(Request())
        return build("youtube", "v3", credentials=credentials)

    def _build_upload_request(self, youtube_client, content: Dict[str, Any]):
        from googleapiclient.http import MediaFileUpload

        title = content.get("text") or "Execution Dispatcher Upload"
        description = content.get("description") or "Uploaded via EXECUTION_DISPATCHER"
        media_body = MediaFileUpload(
            content["video_file"],
            mimetype=content.get("video_mime_type") or "video/*",
            chunksize=1024 * 1024 * 8,
            resumable=True,
        )
        body = {
            "snippet": {
                "title": title,
                "description": description,
            },
            "status": {
                "privacyStatus": content.get("privacy_status", "unlisted"),
            },
        }
        return youtube_client.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media_body,
        )

    def _execute_resumable_upload(self, request):
        response = None
        error = None
        for attempt in range(self._MAX_RETRIES + 1):
            try:
                status, response = request.next_chunk()
                if response is not None:
                    return response
                if status:
                    self.logger.info("YouTube upload progress: %.2f%%", status.progress() * 100)
                error = None
            except Exception as exc:  # noqa: BLE001
                error = exc
                if self._is_retriable_error(exc) and attempt < self._MAX_RETRIES:
                    time.sleep(self._backoff_seconds(attempt))
                    continue
                raise
        if error:
            raise error
        raise RuntimeError("YouTube upload failed without response.")

    def _is_retriable_error(self, exc: Exception) -> bool:
        status_code = getattr(exc, "status_code", None)
        if status_code is None and hasattr(exc, "resp"):
            status_code = getattr(exc.resp, "status", None)
        if status_code in self._RETRIABLE_STATUS_CODES:
            return True
        error_body = getattr(exc, "content", None)
        if error_body:
            try:
                payload = json.loads(error_body)
                reason = payload.get("error", {}).get("errors", [{}])[0].get("reason")
            except (TypeError, json.JSONDecodeError):
                return False
            return reason in {"quotaExceeded", "userRateLimitExceeded"}
        return False

    def _backoff_seconds(self, attempt: int) -> float:
        return min(2 ** attempt, 32)
