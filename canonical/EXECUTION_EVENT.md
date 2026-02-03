# EXECUTION_EVENT

## Purpose
Defines a single immutable execution intent.

## Fields
- event_id: unique immutable id
- intent: semantic purpose (announcement, authority_post, log)
- payload: content object (text, media refs)
- target_platforms: array of platform identifiers
- simultaneity_window: NOW | SCHEDULED
- monetization_hint: FAST_ATTENTION | AUTHORITY | SLOW_ASSET

This file is the execution contract.
