# Google API Python Client

## Overview

The Google API Python Client is a client library for accessing Google APIs. This document provides essential information for working with the library, including installation, authentication methods, making API requests, and common patterns.

## Installation

Install the library using pip:

```bash
pip install google-api-python-client
```

For additional authentication support:

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2
```

## Authentication

There are several authentication methods available:

### 1. Service Account Authentication (Server-to-Server)

Use when your application runs on a server or in a controlled environment.

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Path to service account key file obtained from Google Cloud Console
SERVICE_ACCOUNT_FILE = 'path/to/service-account-key.json'

# Define the scopes your application needs
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Create credentials
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build the service
service = build('sheets', 'v4', credentials=credentials)
```

### 2. OAuth 2.0 User Authentication (User-to-Server)

Use when your application needs to access user data.

```python
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os
import pickle

# Define the scopes your application needs
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_authenticated_service():
    credentials = None
    
    # Check if we have stored token
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    
    # If no valid credentials available, let user log in
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            credentials = flow.run_local_server(port=0)
        
        # Save the credentials for future use
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)
    
    # Build the service
    service = build('gmail', 'v1', credentials=credentials)
    return service
```

### 3. Application Default Credentials (ADC)

Use when running in Google Cloud environments or with local application defaults.

```python
from google.auth import default
from googleapiclient.discovery import build

# Get default credentials
credentials, project = default(scopes=['https://www.googleapis.com/auth/cloud-platform'])

# Build the service
service = build('storage', 'v1', credentials=credentials)
```

## Making API Requests

### Building a Service

The `build()` function creates a service object for interacting with a specific Google API:

```python
from googleapiclient.discovery import build

# Build a service for Google Drive API v3
drive_service = build('drive', 'v3', credentials=credentials)

# Build a service for Google Sheets API v4
sheets_service = build('sheets', 'v4', credentials=credentials)
```

### Executing Requests

Each API service provides methods that correspond to API endpoints:

```python
# List files in Google Drive
results = drive_service.files().list(
    pageSize=10, 
    fields="nextPageToken, files(id, name)"
).execute()

# Read data from Google Sheets
result = sheets_service.spreadsheets().values().get(
    spreadsheetId='SPREADSHEET_ID',
    range='Sheet1!A1:B10'
).execute()
```

### Handling Pagination

Many Google API methods that return collections support pagination:

```python
def list_all_files(drive_service):
    results = []
    page_token = None
    
    while True:
        response = drive_service.files().list(
            pageSize=100,
            fields="nextPageToken, files(id, name)",
            pageToken=page_token
        ).execute()
        
        results.extend(response.get('files', []))
        page_token = response.get('nextPageToken')
        
        if not page_token:
            break
    
    return results
```

### Working with Media (Upload/Download)

For media operations, use the `MediaFileUpload` and `MediaIoBaseDownload` classes:

```python
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io

# Upload a file to Google Drive
file_metadata = {
    'name': 'sample.jpg',
    'mimeType': 'image/jpeg'
}
media = MediaFileUpload('sample.jpg', mimetype='image/jpeg')
file = drive_service.files().create(
    body=file_metadata,
    media_body=media,
    fields='id'
).execute()

# Download a file from Google Drive
file_id = 'FILE_ID'
request = drive_service.files().get_media(fileId=file_id)
file_handle = io.BytesIO()
downloader = MediaIoBaseDownload(file_handle, request)
done = False
while not done:
    status, done = downloader.next_chunk()
    print(f"Download {int(status.progress() * 100)}%")

# Save the downloaded content
with open('downloaded_file.jpg', 'wb') as f:
    f.write(file_handle.getvalue())
```

## Error Handling

Handle API errors gracefully:

```python
from googleapiclient.errors import HttpError

try:
    # Make API request
    result = service.files().get(fileId='non_existent_id').execute()
except HttpError as error:
    print(f"An error occurred: {error}")
    # Handle specific errors by HTTP status code
    if error.resp.status == 404:
        print("File not found")
    elif error.resp.status == 403:
        print("Permission denied")
```

## Rate Limiting and Quotas

Google APIs have rate limits and quotas. Implement exponential backoff for handling rate-limiting errors:

```python
from googleapiclient.errors import HttpError
import time
import random

def execute_with_backoff(request):
    retries = 0
    max_retries = 5
    
    while True:
        try:
            return request.execute()
        except HttpError as error:
            if error.resp.status in [403, 429, 500, 503]:
                if retries >= max_retries:
                    raise  # Give up after max_retries
                
                # Calculate backoff time: 2^retries + random jitter
                wait_time = (2 ** retries) + random.random()
                print(f"Rate limit hit. Waiting {wait_time} seconds.")
                time.sleep(wait_time)
                retries += 1
            else:
                raise  # Re-raise other errors
```

## Batch Requests

Optimize performance by batching multiple API requests:

```python
from googleapiclient.http import BatchHttpRequest

def callback(request_id, response, exception):
    if exception is not None:
        print(f"Error on {request_id}: {exception}")
    else:
        print(f"Response for {request_id}: {response}")

# Create a batch request
batch = drive_service.new_batch_http_request(callback=callback)

# Add individual requests to the batch
batch.add(drive_service.files().get(fileId='file1_id'), request_id='file1')
batch.add(drive_service.files().get(fileId='file2_id'), request_id='file2')
batch.add(drive_service.files().get(fileId='file3_id'), request_id='file3')

# Execute all requests in a single HTTP request
batch.execute()
```

## Common Google API Services

Here are some frequently used Google APIs and their service names:

| API                   | Service Name | Version | Common Use Cases                      |
|-----------------------|--------------|---------|---------------------------------------|
| Google Drive          | drive        | v3      | File storage and sharing              |
| Google Sheets         | sheets       | v4      | Spreadsheet operations                |
| Gmail                 | gmail        | v1      | Email management                      |
| Google Calendar       | calendar     | v3      | Calendar events and scheduling        |
| Google Docs           | docs         | v1      | Document creation and editing         |
| YouTube               | youtube      | v3      | Video uploads and management          |
| Google Cloud Storage  | storage      | v1      | Object storage                        |
| BigQuery              | bigquery     | v2      | Data analytics                        |

## Discovery Document Caching

The client library caches API discovery documents to improve performance. To control caching behavior:

```python
from googleapiclient.discovery_cache.base import Cache
from googleapiclient.discovery import build

# Disable caching
service = build('drive', 'v3', credentials=credentials, cache_discovery=False)

# Use a custom cache implementation
class MyCache(Cache):
    _CACHE = {}
    
    def get(self, url):
        return self._CACHE.get(url)
    
    def set(self, url, content):
        self._CACHE[url] = content

# Use custom cache
from googleapiclient.discovery_cache import DISCOVERY_DOC_MAX_AGE
service = build('drive', 'v3', credentials=credentials, 
                cache=MyCache(), cache_discovery=True)
```

## Best Practices

1. **Minimize API Calls**: Batch requests when possible and request only the data you need.
2. **Use Appropriate Authentication**: Choose the right authentication method for your use case.
3. **Handle Rate Limits**: Implement exponential backoff for handling rate limits.
4. **Securely Store Credentials**: Never hardcode or commit API keys or credentials to version control.
5. **Error Handling**: Always include robust error handling for API requests.
6. **Resource Cleanup**: Close any open connections or resources when done.
7. **Field Selection**: Use the `fields` parameter to limit response data to only what you need.

## Example: Complete Application

Here's a complete example that lists files in Google Drive and uploads a new file:

```python
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

def main():
    # Authentication
    credentials = Credentials.from_service_account_file(
        'service-account.json',
        scopes=['https://www.googleapis.com/auth/drive']
    )
    
    # Build the Drive API service
    drive_service = build('drive', 'v3', credentials=credentials)
    
    try:
        # List files
        print('Listing files:')
        results = drive_service.files().list(
            pageSize=10, 
            fields="nextPageToken, files(id, name, mimeType)"
        ).execute()
        
        files = results.get('files', [])
        if not files:
            print('No files found.')
        else:
            for file in files:
                print(f"{file['name']} ({file['id']}) - {file['mimeType']}")
        
        # Upload a new file
        print('\nUploading new file:')
        file_metadata = {
            'name': 'Sample Document',
            'mimeType': 'application/vnd.google-apps.document'
        }
        media = MediaFileUpload(
            'sample.txt',
            mimetype='text/plain',
            resumable=True
        )
        file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id,name,webViewLink'
        ).execute()
        
        print(f"Created file: {file['name']} ({file['id']})")
        print(f"View it online: {file.get('webViewLink')}")
        
    except HttpError as error:
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    main()
```

## Resources

- [Official Documentation](https://github.com/googleapis/google-api-python-client/blob/main/docs/README.md)
- [Google API Explorer](https://developers.google.com/apis-explorer)
- [Google Cloud Console](https://console.cloud.google.com/) - For creating projects and credentials
- [Available Google APIs](https://developers.google.com/api-client-library/python/apis/)

## Troubleshooting

### Common Error: "Invalid Grant"
This typically occurs when:
- The OAuth token has expired
- The system clock is incorrect
- The service account or OAuth credentials are revoked

### Common Error: "Access Not Configured"
The API you're trying to use is not enabled for your project. Enable it in the Google Cloud Console.

### Common Error: "Insufficient Permissions"
The authenticated user or service account doesn't have the necessary permissions for the operation.

### Missing Discovery Documents
If you're using a new or updated API, you might need to force bypassing the cache:

```python
service = build('newapi', 'v1', credentials=credentials, cache_discovery=False)
```
