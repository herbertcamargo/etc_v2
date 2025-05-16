
# 📦 YouTube Transcription Caching Mechanism (Python + cachetools)

## Overview

This caching system is responsible for **storing original YouTube video transcriptions** (after formatting via our intelligent processing mechanism) into an in-memory cache using Python's `cachetools` library.

## Workflow

1. When a transcription is captured from YouTube, it is **processed and formatted** by our custom logic.
2. Once formatted, it is **saved into the cache**, using the **YouTube video ID** as the unique key.
3. Transcriptions are retrieved **based on video ID**, which is extracted from the video URL (e.g., `/watch?v=hGg3nWp7afg&t=639s` → `hGg3nWp7afg`).

## Implementation Details

- We use `cachetools.LRUCache` with a **maximum memory budget of 100 MB**.
- Each transcription is stored as a string (UTF-8), and average size is estimated to be ~10 KB.
- The cache **does not limit by number of entries**, but instead tracks total memory usage.
- When the 100 MB threshold is reached, the cache automatically **evicts the oldest entries first** (Least Recently Used - LRU policy).
- We **do not preload transcriptions**, even if they are popular. All entries are created **on-demand**.

## Key Characteristics

| Feature                     | Value                              |
|-----------------------------|-------------------------------------|
| Key                         | YouTube video ID (string)          |
| Value                       | Processed transcription (string)   |
| Cache type                  | `cachetools.LRUCache`              |
| Size limit                  | 100 MB total                       |
| Eviction policy             | Oldest (Least Recently Used)       |
| Preloading popular videos   | ❌ Disabled                        |

## Example (to be implemented)

```python
from cachetools import LRUCache
import sys

# Roughly estimate size of each transcription in bytes
def estimate_size(transcription):
    return sys.getsizeof(transcription)

# Initialize cache with size in bytes
cache = LRUCache(maxsize=100 * 1024 * 1024, getsizeof=estimate_size)

def save_transcription(video_id: str, transcription: str):
    cache[video_id] = transcription

def get_transcription(video_id: str):
    return cache.get(video_id)
