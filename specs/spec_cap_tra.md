
# YouTube Video Capture and Transcription Service

## Overview

The YouTube Video Capture and Transcription Service is a critical component of the application that enables users to:

1. Search for YouTube videos using keywords
2. Retrieve detailed information about specific videos
3. Extract transcriptions (captions/subtitles) from YouTube videos
4. Cache video details and transcriptions for improved performance


## Core Components

### 1. YouTube API Client

A service class that interacts with the YouTube Data API v3 for searching videos and retrieving video metadata.

```python
class YouTubeClient:
    """
    Client for interacting with YouTube Data API v3.
    Handles authentication, video searching, and metadata retrieval.
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        
    async def build_client(self):
        """Create an authenticated YouTube API client."""
        # Implementation with googleapiclient.discovery in an async-compatible way
        
    async def search_videos(self, query: str, max_results: int = 10) -> list[dict]:
        """
        Search YouTube videos by query term.
        
        Args:
            query: Search keywords
            max_results: Maximum number of results to return (default: 10)
            
        Returns:
            List of video data dictionaries with id, title, thumbnail, etc.
        """
        
    async def get_video_details(self, video_id: str) -> dict:
        """
        Get detailed information about a specific YouTube video.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Dictionary containing video metadata
        """
        
    async def list_captions(self, video_id: str) -> list:
        """
        List available captions for a video.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            List of available caption tracks
        """
```

### 2. Transcript Service

A service responsible for extracting and processing transcripts from YouTube videos.

```python
class TranscriptService:
    """
    Service for retrieving and processing YouTube video transcripts.
    Supports multiple retrieval methods and caching.
    """
    
    def __init__(self, youtube_client: YouTubeClient, cache_enabled: bool = True):
        self.youtube_client = youtube_client
        self.cache_enabled = cache_enabled
        
    async def get_transcript(self, video_id: str, languages: list[str] = None, debug_mode: bool = True) -> tuple[str, list[float]]:
        """
        Get transcript for a YouTube video.
        
        Args:
            video_id: YouTube video ID
            languages: List of language codes to try, in order of preference
            debug_mode: If True, logs detailed debug information
            
        Returns:
            Tuple of (transcript_text, timestamps) where timestamps is a list
            of start times for each word
        """
        
    async def process_transcript_data(self, transcript_data: list) -> tuple[str, list[float]]:
        """
        Process raw transcript data into text and timestamps.
        
        Args:
            transcript_data: Raw transcript data from YouTube API
            
        Returns:
            Tuple of (transcript_text, timestamps)
        """
        
    async def filter_sound_indications(self, line: str) -> bool:
        """
        Filter out lines that only contain sound indications.
        
        Args:
            line: Text line from transcript
            
        Returns:
            True if the line should be filtered (is a sound indication only)
        """
        
    async def check_captions_availability(self, video_id: str) -> bool:
        """
        Directly check if a video has captions available via the YouTube API.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            True if captions are available, False otherwise, None if unknown
        """
```

### 3. Caching Layer

Implements caching for video details and transcripts to improve performance and reduce API calls.

```python
class YouTubeCache:
    """
    Caching service for YouTube data.
    Provides persistent caching for video details and transcripts.
    """
    
    def __init__(self, cache_dir: str = "cache"):
        self.cache_dir = cache_dir
        self.video_details_dir = os.path.join(cache_dir, "video_details")
        self.transcript_dir = os.path.join(cache_dir, "transcripts")
        
    async def get_video_details(self, video_id: str) -> Optional[dict]:
        """Get cached video details if available."""
        
    async def save_video_details(self, video_id: str, data: dict) -> None:
        """Save video details to cache."""
        
    async def get_transcript(self, video_id: str) -> Optional[tuple[str, list[float]]]:
        """Get cached transcript if available."""
        
    async def save_transcript(self, video_id: str, transcript: str, timestamps: list[float]) -> None:
        """Save transcript to cache."""
```

### 4. Debug and Logging Component

Implements debug logging for transcript retrieval processes.

```python
class TranscriptDebugger:
    """
    Debug helper for transcript retrieval.
    Logs and tracks detailed information about transcript retrieval processes.
    """
    
    def __init__(self, debug_enabled: bool = True):
        self.debug_enabled = debug_enabled
        self.debug_info = []
        
    def log(self, message: str) -> None:
        """
        Log a debug message if debug is enabled.
        
        Args:
            message: Debug message to log
        """
        
    def get_log(self) -> list[str]:
        """
        Get all logged debug messages.
        
        Returns:
            List of debug messages
        """
        
    def clear(self) -> None:
        """Clear all logged debug messages."""
```

## API Endpoints

### Video Search and Retrieval

New endpoints to be implemented in the `videos.py` router:

```python
# GET /api/v1/videos/search
@router.get("/search", response_model=List[schemas.VideoSearchResult])
async def search_videos(
    query: str, 
    max_results: int = 10,
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Search for YouTube videos by query term.
    
    Args:
        query: Search keywords
        max_results: Maximum number of results to return
        
    Returns:
        List of video data with id, title, thumbnail, etc.
    """
    
# GET /api/v1/videos/{video_id}
@router.get("/{video_id}", response_model=schemas.VideoDetails)
async def get_video_details(
    video_id: str,
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Get detailed information about a specific YouTube video.
    
    Args:
        video_id: YouTube video ID
        
    Returns:
        Detailed video information
    """
```

### Transcript Retrieval

New endpoint to be implemented in the `videos.py` router:

```python
# GET /api/v1/videos/{video_id}/transcript
@router.get("/{video_id}/transcript", response_model=schemas.VideoTranscript)
async def get_video_transcript(
    video_id: str,
    languages: Optional[List[str]] = Query(None),
    debug_mode: bool = Query(False),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Get transcript for a YouTube video.
    
    Args:
        video_id: YouTube video ID
        languages: List of language codes to try, in order of preference
        debug_mode: If True, includes detailed debug information in response
        
    Returns:
        Transcript text and word timestamps
    """
```

## Data Models

New Pydantic schemas to be added to the schemas directory:

```python
# schemas/video.py

class VideoSearchResult(BaseModel):
    """Schema for YouTube video search results."""
    id: str
    title: str
    thumbnail: str
    channel: str
    published_at: datetime

class VideoDetails(BaseModel):
    """Schema for detailed YouTube video information."""
    video_id: str
    title: str
    channel: str
    description: str
    embed_url: str
    duration: str  # ISO 8601 duration format
    
class VideoTranscript(BaseModel):
    """Schema for YouTube video transcript."""
    video_id: str
    transcript: str
    timestamps: List[float]  # Start time for each word
    debug_info: Optional[List[str]]  # Debug information if debug_mode=True
```

## Implementation Details

### Configuration

Configuration settings to be added to `core/config.py`:

```python
# YouTube API settings
YOUTUBE_API_KEY: str
YOUTUBE_CACHE_ENABLED: bool = True
YOUTUBE_CACHE_DIR: str = "cache"

# Debug settings
TRANSCRIPT_DEBUG_ENABLED: bool = True

# Proxy configuration
PROXY_ENABLED: bool = False
PROXY_HOST: Optional[str] = None
PROXY_PORT: Optional[int] = None
PROXY_USER: Optional[str] = None
PROXY_PASSWORD: Optional[str] = None
```

### Dependencies

New dependencies to be added to `api/dependencies.py`:

```python
def get_youtube_client() -> YouTubeClient:
    """
    Dependency for getting a configured YouTube client.
    
    Returns:
        YouTubeClient instance
    """
    return YouTubeClient(settings.YOUTUBE_API_KEY)
    
def get_transcript_service(
    youtube_client: YouTubeClient = Depends(get_youtube_client)
) -> TranscriptService:
    """
    Dependency for getting a transcript service.
    
    Args:
        youtube_client: YouTube client instance
        
    Returns:
        TranscriptService instance
    """
    return TranscriptService(
        youtube_client=youtube_client,
        cache_enabled=settings.YOUTUBE_CACHE_ENABLED
    )
```

## Transcript Retrieval Strategy

The transcript retrieval implementation should follow a multi-layered approach:

1. **Cache Check**: First check if transcript exists in cache
2. **Direct YouTube API Check**: Check if captions exist using YouTube API
3. **Multi-language Attempt**: Try retrieving transcript in multiple languages (`['', 'en', 'en-US', 'pt', 'pt-BR', 'es']`)
4. **Fallback Messages**: If all attempts fail, return "No closed captions found. Please contact support or try a different video."

### Sound Filtering

Transcripts should be processed to filter out sound indications like `[music]`, `[applause]`, etc., replacing them with line breaks for better readability.

### Debug Mode

The transcript retrieval process should include a debug mode that logs detailed information about each step of the retrieval process. This helps with troubleshooting issues in different environments.

## Error Handling

The service should handle various error scenarios gracefully:

1. YouTube API errors (quotas, service unavailability)
2. Missing transcripts/captions for videos
3. Invalid video IDs
4. Cache read/write errors

Each error should return appropriate HTTP status codes and error messages.

## Proxy Support

For environments requiring proxy support, implement mandatory HTTP proxy for all YouTube API requests:

```python
# Proxy configuration
proxies = {
    'http': f'http://{proxy_user}:{proxy_pass}@{proxy_host}',
    'https': f'http://{proxy_user}:{proxy_pass}@{proxy_host}',
}

# Monkey patch requests Session to force proxy usage
def configure_proxy_for_requests():
    original_request = requests.Session.request
    
    def proxied_request(self, method, url, *args, **kwargs):
        kwargs['proxies'] = proxies
        return original_request(self, method, url, *args, **kwargs)
    
    requests.Session.request = proxied_request
```

This approach ensures all HTTP requests will use the configured proxy.

## Performance Considerations

1. Implement caching for all YouTube API responses
2. Use connection pooling for HTTP requests
3. Properly handle YouTube API quotas and rate limits
4. Use asynchronous programming patterns for all I/O operations
5. Implement appropriate timeouts for all external service calls
6. Store transcripts in cache after successful retrieval

## Testing Strategy

1. Unit tests for each service component
2. Mocked responses for YouTube API calls in tests
3. Integration tests for API endpoints
4. Performance testing for caching behavior
5. Test proxy configuration with dummy proxy server

## Integration with Existing Features

This component will integrate with:

1. User authentication system for API access control
2. Transcription sessions for storing user transcription attempts
3. Subscription service for enforcing user limits on video searches

## Implementation Plan

1. Create service classes for YouTube API client and transcript processing
2. Implement caching layer for performance optimization
3. Add Pydantic schemas for request/response data models
4. Implement API endpoints in the videos router
5. Add unit and integration tests
6. Document API endpoints with Swagger annotations 