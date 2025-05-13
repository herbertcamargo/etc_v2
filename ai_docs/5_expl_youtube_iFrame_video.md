# YouTube Iframe Integration Guide (v2)

## Overview
This document provides essential guidelines for AI agents to understand and implement YouTube iframe embeds properly in the project. All agents must reference this documentation when handling requests related to YouTube video integration.

## Implementation Specifications

### Standard YouTube Iframe Embed
When embedding YouTube videos, always use the following format:

```html
<iframe 
  width="560" 
  height="315" 
  src="https://www.youtube.com/embed/{VIDEO_ID}" 
  title="YouTube video player" 
  frameborder="0" 
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
  allowfullscreen>
</iframe>
```

Replace `{VIDEO_ID}` with the actual YouTube video ID.

### Extracting Video ID from YouTube URLs
YouTube video IDs can be extracted from various URL formats:
- Standard: `https://www.youtube.com/watch?v={VIDEO_ID}`
- Short: `https://youtu.be/{VIDEO_ID}`
- Embedded: `https://www.youtube.com/embed/{VIDEO_ID}`

When processing user input containing YouTube links, always extract the video ID correctly.

### Responsive Implementation
For responsive designs, wrap the iframe in a container with appropriate styling:

```html
<div class="video-container" style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%;">
  <iframe 
    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"
    src="https://www.youtube.com/embed/{VIDEO_ID}" 
    title="YouTube video player" 
    frameborder="0" 
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
    allowfullscreen>
  </iframe>
</div>
```

### Advanced Parameters
YouTube iframes accept additional parameters:

| Parameter | Example Value | Description |
|-----------|---------------|-------------|
| autoplay  | 0 or 1        | Automatically start playback when loaded |
| loop      | 0 or 1        | Loop the video when it ends |
| start     | seconds       | Start video at specific time (in seconds) |
| end       | seconds       | End video at specific time (in seconds) |
| mute      | 0 or 1        | Start video muted |
| controls  | 0 or 1        | Show/hide player controls |

Example URL with parameters:
```
https://www.youtube.com/embed/{VIDEO_ID}?autoplay=0&start=30&mute=1
```

### Security Considerations
- Always set `loading="lazy"` attribute for improved performance
- YouTube Player API requires JS inclusion only when interactive control is needed
- Use the `youtube-nocookie.com` domain for enhanced privacy:
  ```
  https://www.youtube-nocookie.com/embed/{VIDEO_ID}
  ```

## Implementation in Different Frameworks

### React Component
```jsx
const YouTubeEmbed = ({ videoId, title, startTime = 0, autoplay = false }) => {
  const embedUrl = `https://www.youtube.com/embed/${videoId}?start=${startTime}&autoplay=${autoplay ? 1 : 0}`;
  
  return (
    <div className="video-container">
      <iframe
        src={embedUrl}
        title={title || "YouTube video player"}
        frameBorder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowFullScreen
        loading="lazy"
      />
    </div>
  );
};
```

### Vue Component
```vue
<template>
  <div class="video-container">
    <iframe
      :src="`https://www.youtube.com/embed/${videoId}?start=${startTime}&autoplay=${autoplay ? 1 : 0}`"
      :title="title || 'YouTube video player'"
      frameborder="0"
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
      allowfullscreen
      loading="lazy"
    ></iframe>
  </div>
</template>

<script>
export default {
  props: {
    videoId: {
      type: String,
      required: true
    },
    title: {
      type: String,
      default: 'YouTube video player'
    },
    startTime: {
      type: Number,
      default: 0
    },
    autoplay: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style scoped>
.video-container {
  position: relative;
  padding-bottom: 56.25%;
  height: 0;
  overflow: hidden;
  max-width: 100%;
}
.video-container iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
</style>
```

### Angular Component
```typescript
// youtube-embed.component.ts
import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';

@Component({
  selector: 'app-youtube-embed',
  template: `
    <div class="video-container">
      <iframe
        [src]="safeEmbedUrl"
        [title]="title || 'YouTube video player'"
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen
        loading="lazy"
      ></iframe>
    </div>
  `,
  styles: [`
    .video-container {
      position: relative;
      padding-bottom: 56.25%;
      height: 0;
      overflow: hidden;
      max-width: 100%;
    }
    .video-container iframe {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
    }
  `]
})
export class YouTubeEmbedComponent implements OnChanges {
  @Input() videoId!: string;
  @Input() title: string = 'YouTube video player';
  @Input() startTime: number = 0;
  @Input() autoplay: boolean = false;
  
  safeEmbedUrl!: SafeResourceUrl;
  
  constructor(private sanitizer: DomSanitizer) {}
  
  ngOnChanges(changes: SimpleChanges): void {
    if (changes['videoId'] || changes['startTime'] || changes['autoplay']) {
      this.updateEmbedUrl();
    }
  }
  
  private updateEmbedUrl(): void {
    const embedUrl = `https://www.youtube.com/embed/${this.videoId}?start=${this.startTime}&autoplay=${this.autoplay ? 1 : 0}`;
    this.safeEmbedUrl = this.sanitizer.bypassSecurityTrustResourceUrl(embedUrl);
  }
}
```

### Next.js Implementation
```jsx
// components/YouTubeEmbed.jsx
import React from 'react';

const YouTubeEmbed = ({ videoId, title, startTime = 0, autoplay = false }) => {
  const embedUrl = `https://www.youtube.com/embed/${videoId}?start=${startTime}&autoplay=${autoplay ? 1 : 0}`;
  
  return (
    <div className="video-container">
      <iframe
        src={embedUrl}
        title={title || "YouTube video player"}
        frameBorder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowFullScreen
        loading="lazy"
      />
      <style jsx>{`
        .video-container {
          position: relative;
          padding-bottom: 56.25%;
          height: 0;
          overflow: hidden;
          max-width: 100%;
        }
        .video-container iframe {
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
        }
      `}</style>
    </div>
  );
};

export default YouTubeEmbed;
```

## Utility Functions

### URL Validation and ID Extraction

```javascript
/**
 * Extracts YouTube video ID from various YouTube URL formats
 * @param {string} url - YouTube URL
 * @returns {string|null} - YouTube video ID or null if invalid
 */
function extractYouTubeVideoId(url) {
  if (!url) return null;
  
  // Check if URL is valid YouTube URL
  const validYouTubeUrlRegex = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.*$/;
  if (!validYouTubeUrlRegex.test(url)) return null;
  
  // Extract video ID
  const videoIdRegex = /^.*(?:(?:youtu\.be\/|v\/|vi\/|u\/\w\/|embed\/|shorts\/)|(?:(?:watch)?\?v(?:i)?=|\&v(?:i)?=))([^#\&\?]*).*/;
  const match = url.match(videoIdRegex);
  
  return match && match[1] ? match[1] : null;
}

/**
 * Validates if a string is a valid YouTube video ID
 * @param {string} videoId - YouTube video ID to validate
 * @returns {boolean} - Whether the ID is valid
 */
function isValidYouTubeVideoId(videoId) {
  // YouTube video IDs are 11 characters, case-sensitive
  const videoIdRegex = /^[a-zA-Z0-9_-]{11}$/;
  return videoIdRegex.test(videoId);
}

/**
 * Creates a YouTube embed URL with parameters
 * @param {string} videoId - YouTube video ID
 * @param {Object} options - Parameters for the embed
 * @returns {string} - Formatted YouTube embed URL
 */
function createYouTubeEmbedUrl(videoId, options = {}) {
  if (!videoId || !isValidYouTubeVideoId(videoId)) {
    return null;
  }
  
  const domain = options.enhancedPrivacy ? 'youtube-nocookie.com' : 'youtube.com';
  let embedUrl = `https://www.${domain}/embed/${videoId}`;
  
  // Add parameters if provided
  const params = [];
  
  if (options.autoplay) params.push('autoplay=1');
  if (options.mute) params.push('mute=1');
  if (options.loop) params.push('loop=1');
  if (options.controls === false) params.push('controls=0');
  if (typeof options.start === 'number') params.push(`start=${options.start}`);
  if (typeof options.end === 'number') params.push(`end=${options.end}`);
  if (options.playlist) params.push(`playlist=${options.playlist}`);
  if (options.playlistId) params.push(`list=${options.playlistId}`);
  
  if (params.length > 0) {
    embedUrl += '?' + params.join('&');
  }
  
  return embedUrl;
}
```

### React Hook for YouTube Embed

```jsx
// hooks/useYouTubeEmbed.js
import { useState, useEffect } from 'react';

/**
 * Custom hook for handling YouTube embed functionality
 * @param {string} initialUrl - Initial YouTube URL (can be any format)
 * @returns {Object} Functions and state for YouTube embed
 */
export function useYouTubeEmbed(initialUrl = '') {
  const [videoId, setVideoId] = useState('');
  const [embedUrl, setEmbedUrl] = useState('');
  const [error, setError] = useState(null);
  
  // Extract video ID from URL
  const extractVideoId = (url) => {
    if (!url) {
      setVideoId('');
      setEmbedUrl('');
      setError(null);
      return;
    }
    
    const videoIdRegex = /^.*(?:(?:youtu\.be\/|v\/|vi\/|u\/\w\/|embed\/|shorts\/)|(?:(?:watch)?\?v(?:i)?=|\&v(?:i)?=))([^#\&\?]*).*/;
    const match = url.match(videoIdRegex);
    
    if (match && match[1]) {
      setVideoId(match[1]);
      setEmbedUrl(`https://www.youtube.com/embed/${match[1]}`);
      setError(null);
    } else {
      setVideoId('');
      setEmbedUrl('');
      setError('Invalid YouTube URL');
    }
  };
  
  // Create embed URL with parameters
  const createEmbedUrl = (options = {}) => {
    if (!videoId) return '';
    
    let url = `https://www.youtube.com/embed/${videoId}`;
    const params = [];
    
    if (options.autoplay) params.push('autoplay=1');
    if (options.mute) params.push('mute=1');
    if (options.loop) params.push('loop=1');
    if (options.controls === false) params.push('controls=0');
    if (typeof options.start === 'number') params.push(`start=${options.start}`);
    if (typeof options.end === 'number') params.push(`end=${options.end}`);
    
    if (params.length > 0) {
      url += '?' + params.join('&');
    }
    
    setEmbedUrl(url);
    return url;
  };
  
  useEffect(() => {
    if (initialUrl) {
      extractVideoId(initialUrl);
    }
  }, [initialUrl]);
  
  return {
    videoId,
    embedUrl,
    error,
    extractVideoId,
    createEmbedUrl
  };
}
```

## Error Handling
AI agents should validate YouTube URLs and provide helpful error messages:

1. URL validation regex: `/^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.*$/`
2. Video ID extraction regex: `/^.*(?:(?:youtu\.be\/|v\/|vi\/|u\/\w\/|embed\/|shorts\/)|(?:(?:watch)?\?v(?:i)?=|\&v(?:i)?=))([^#\&\?]*).*/`
3. If extraction fails, recommend the user provide a direct YouTube URL

### Common Error Scenarios and Solutions

| Error | Description | Solution |
|-------|-------------|----------|
| Invalid URL | The provided URL is not a YouTube URL | Request a proper YouTube URL from user |
| Missing Video ID | URL format is correct but ID cannot be extracted | Parse URL with regex or request direct video ID |
| Private Video | Video exists but is set to private | Inform user that video is not publicly accessible |
| Deleted Video | Video ID is valid but video was removed | Suggest user to verify video existence |
| Embedding Disabled | Video owner has disabled embedding | Suggest watching on YouTube directly |
| Autoplay Blocked | Browsers block autoplay with sound | Set `mute=1` with autoplay or inform user of browser limitations |

### Error Handling Code Example

```javascript
/**
 * Comprehensive YouTube embed error handling
 * @param {string} url - YouTube URL to validate and process
 * @returns {Object} Result object with status, message, and data
 */
function processYouTubeUrl(url) {
  // Check if URL is provided
  if (!url) {
    return {
      status: 'error',
      message: 'No URL provided. Please provide a YouTube URL.',
      data: null
    };
  }
  
  // Check if URL is a valid YouTube URL
  const validYouTubeUrlRegex = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be|youtube-nocookie\.com)\/.*$/;
  if (!validYouTubeUrlRegex.test(url)) {
    return {
      status: 'error',
      message: 'Invalid YouTube URL. Please provide a valid YouTube URL.',
      data: null
    };
  }
  
  // Extract video ID
  const videoIdRegex = /^.*(?:(?:youtu\.be\/|v\/|vi\/|u\/\w\/|embed\/|shorts\/)|(?:(?:watch)?\?v(?:i)?=|\&v(?:i)?=))([^#\&\?]*).*/;
  const match = url.match(videoIdRegex);
  
  // Check if video ID extraction was successful
  if (!match || !match[1]) {
    return {
      status: 'error',
      message: 'Could not extract video ID from URL. Please provide a standard YouTube URL.',
      data: null
    };
  }
  
  // Check if video ID has valid format
  const videoId = match[1];
  if (!/^[a-zA-Z0-9_-]{11}$/.test(videoId)) {
    return {
      status: 'error',
      message: 'Invalid video ID format. YouTube IDs should be 11 characters.',
      data: null
    };
  }
  
  // Successfully extracted and validated
  return {
    status: 'success',
    message: 'Successfully extracted video ID.',
    data: {
      videoId: videoId,
      embedUrl: `https://www.youtube.com/embed/${videoId}`,
      thumbnailUrl: `https://img.youtube.com/vi/${videoId}/hqdefault.jpg`
    }
  };
}
```

## Performance Optimization

### Lazy Loading
Always implement lazy loading for performance optimization:

```html
<iframe 
  src="https://www.youtube.com/embed/{VIDEO_ID}" 
  loading="lazy"
  title="YouTube video player" 
  frameborder="0" 
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
  allowfullscreen>
</iframe>
```

### Thumbnail Preview with Click-to-Load
For pages with multiple videos, consider using a thumbnail preview with click-to-load functionality:

```html
<div class="youtube-preview" data-video-id="{VIDEO_ID}">
  <img src="https://img.youtube.com/vi/{VIDEO_ID}/hqdefault.jpg" alt="YouTube video preview">
  <div class="play-button"></div>
</div>
```

```javascript
// JavaScript to handle click-to-load
document.querySelectorAll('.youtube-preview').forEach(preview => {
  preview.addEventListener('click', function() {
    const videoId = this.getAttribute('data-video-id');
    const iframe = document.createElement('iframe');
    iframe.src = `https://www.youtube.com/embed/${videoId}?autoplay=1`;
    iframe.title = "YouTube video player";
    iframe.frameBorder = "0";
    iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
    iframe.allowFullscreen = true;
    
    // Replace preview with iframe
    this.parentNode.replaceChild(iframe, this);
  });
});
```

### Lite YouTube Embed
For maximum performance, consider using the "Lite YouTube Embed" approach:

```html
<!-- Include the lite-youtube-embed library -->
<link rel="stylesheet" href="path/to/lite-youtube-embed.css">
<script defer src="path/to/lite-youtube-embed.js"></script>

<!-- Use the custom element -->
<lite-youtube videoid="{VIDEO_ID}" playlabel="Play: Video Title"></lite-youtube>
```

## Accessibility Considerations

### Proper Attributes
Ensure all YouTube embeds include appropriate accessibility attributes:

```html
<iframe 
  src="https://www.youtube.com/embed/{VIDEO_ID}" 
  title="Video Title - Description" 
  frameborder="0" 
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
  allowfullscreen
  aria-labelledby="video-title"
  loading="lazy">
</iframe>
<p id="video-title" class="sr-only">Detailed description of the video content</p>
```

### Keyboard Navigation
When implementing custom video solutions, ensure keyboard navigation works correctly:

```javascript
// Example for custom video controls
playButton.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' || e.key === ' ') {
    e.preventDefault();
    playButton.click();
  }
});
```

## Integration with Project Architecture
When implementing YouTube embeds in the project:

1. Use the responsive container for all embeds
2. Implement lazy loading for performance optimization
3. For React/Next.js implementations, use the component above
4. For Vue/Angular applications, use the framework-specific components
5. For static HTML pages, use the standard iframe with recommended parameters
6. Add proper error handling for invalid YouTube URLs or IDs
7. Consider accessibility requirements for all implementations

## API Integration Examples

### YouTube Data API Integration
For more advanced functionality, integrate with the YouTube Data API:

```javascript
/**
 * Fetch video details using YouTube Data API
 * @param {string} videoId - YouTube video ID
 * @param {string} apiKey - Your YouTube Data API key
 * @returns {Promise} Promise with video details
 */
async function getVideoDetails(videoId, apiKey) {
  try {
    const response = await fetch(
      `https://www.googleapis.com/youtube/v3/videos?id=${videoId}&key=${apiKey}&part=snippet,contentDetails,statistics`
    );
    
    if (!response.ok) {
      throw new Error('Failed to fetch video details');
    }
    
    const data = await response.json();
    
    if (data.items && data.items.length > 0) {
      return {
        title: data.items[0].snippet.title,
        description: data.items[0].snippet.description,
        publishedAt: data.items[0].snippet.publishedAt,
        duration: data.items[0].contentDetails.duration,
        viewCount: data.items[0].statistics.viewCount,
        likeCount: data.items[0].statistics.likeCount,
        channelTitle: data.items[0].snippet.channelTitle,
        thumbnails: data.items[0].snippet.thumbnails
      };
    }
    
    return null;
  } catch (error) {
    console.error('Error fetching video details:', error);
    return null;
  }
}
```

### Using YouTube Player API
For interactive control of the YouTube player:

```html
<!-- 1. Include the YouTube Player API -->
<script src="https://www.youtube.com/iframe_api"></script>

<!-- 2. Add a container for the player -->
<div id="player"></div>

<script>
// 3. Create and control the player
let player;

function onYouTubeIframeAPIReady() {
  player = new YT.Player('player', {
    height: '315',
    width: '560',
    videoId: '{VIDEO_ID}',
    playerVars: {
      'playsinline': 1,
      'rel': 0,
      'modestbranding': 1
    },
    events: {
      'onReady': onPlayerReady,
      'onStateChange': onPlayerStateChange
    }
  });
}

function onPlayerReady(event) {
  // Player is ready
  console.log('Player is ready');
}

function onPlayerStateChange(event) {
  // Player state has changed
  console.log('Player state:', event.data);
}

// Control functions
function playVideo() {
  player.playVideo();
}

function pauseVideo() {
  player.pauseVideo();
}

function seekTo(seconds) {
  player.seekTo(seconds, true);
}
</script>
```

## Changelog
- v2.0: 
  - Added responsive container implementation
  - Enhanced security considerations
  - Added framework-specific components (React, Vue, Angular, Next.js)
  - Improved error handling with detailed scenarios
  - Added performance optimization techniques
  - Added accessibility considerations
  - Added YouTube Data API and Player API integration examples
  - Added utility functions for URL validation and processing
- v1.0: Initial documentation with basic embed instructions

## Usage in AI Responses
When users request YouTube video implementations, AI agents should:

1. Extract the video ID from the URL if provided
2. Generate the appropriate embed code based on the context
3. Provide implementation options based on the project's framework
4. Reference this documentation for additional parameters if needed
5. Consider performance optimization and accessibility requirements
6. Implement proper error handling for invalid URLs or IDs

### Example Response Template

When generating a response for a YouTube embed request:

```
Here's the YouTube embed implementation for the video you requested:

[Framework]-specific implementation:
[Code block with appropriate implementation]

This implementation includes:
- Responsive container for proper sizing
- Lazy loading for performance optimization
- Accessibility attributes for better user experience
- [Any additional features requested]

You can customize this implementation with:
- Autoplay: Add `?autoplay=1` to the URL
- Start time: Add `?start=[seconds]` to the URL
- [Any other relevant customizations]

Remember to extract the video ID correctly from YouTube URLs using the utility function in our documentation.
```

This documentation should be used as a reference for all AI agents handling YouTube iframe implementation requests.
