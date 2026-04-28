# Google Drive MCP Server (Stub)

A configurable Model Context Protocol (MCP) server for Google Drive operations. This stub implementation currently operates in **file mode**, storing all documents locally on the filesystem instead of syncing with Google Drive.

## Features

- **Configurable**: Easy configuration via code, dictionaries, or environment variables
- **File-Based Storage**: Saves all documents to a local directory
- **Multiple Formats**: Supports md, txt, json, and html file formats
- **Comprehensive Tools**: 6 main operations with full error handling
- **Logging**: Built-in logging with configurable levels
- **Size Controls**: File size and operation limits to prevent abuse

## Installation

The server is part of the `idea_to_prod` package. Import it from:

```python
from idea_to_prod.mcp_servers import GoogleDriveMCPServer, GoogleDriveConfig, create_config
```

## Quick Start

### Basic Usage (with defaults)

```python
from idea_to_prod.mcp_servers import GoogleDriveMCPServer

# Create server with default configuration
server = GoogleDriveMCPServer()

# Save a document
result = server.save_document(
    name="my_document",
    content="# My Document\n\nThis is a test.",
    folder_path="documents",
    file_format="md"
)

# Read the document
result = server.read_document(
    name="my_document",
    folder_path="documents"
)
print(result['content'])
```

### Custom Configuration

```python
from idea_to_prod.mcp_servers import create_config, GoogleDriveMCPServer

# Create custom configuration
config = create_config(
    storage_dir="./my_data",           # Custom storage location
    mode="file",                        # Only mode currently supported
    enable_logging=True,                # Enable logging
    log_level="DEBUG"                   # Log level
)

# Create server with custom config
server = GoogleDriveMCPServer(config=config)
```

## Available Tools

### 1. save_document

Saves a document to local storage.

**Parameters:**
- `name` (str): Document name without extension
- `content` (str): Document content
- `folder_path` (str, optional): Folder path relative to storage_dir
- `file_format` (str): File format - md, txt, json, or html

**Example:**
```python
result = server.save_document(
    name="design_doc",
    content="# High-Level Design\n\nArchitecture overview...",
    folder_path="designs/2024",
    file_format="md"
)
```

**Returns:**
```python
{
    "status": "success",
    "message": "Document 'design_doc' saved successfully",
    "file_path": "/home/user/.idea_to_prod/google_drive/designs/2024/design_doc.md",
    "metadata": {
        "filename": "design_doc.md",
        "file_size_bytes": 1024,
        "file_size_mb": 0.001,
        "created_timestamp": "2024-01-15T10:30:00",
        "modified_timestamp": "2024-01-15T10:30:00",
        "extension": ".md"
    }
}
```

### 2. read_document

Reads a document from local storage.

**Parameters:**
- `name` (str): Document name (with or without extension)
- `folder_path` (str, optional): Folder path relative to storage_dir

**Example:**
```python
result = server.read_document(
    name="design_doc",
    folder_path="designs/2024"
)

if result['status'] == 'success':
    print(result['content'])
```

**Returns:**
```python
{
    "status": "success",
    "file_name": "design_doc.md",
    "content": "# High-Level Design\n\nArchitecture overview...",
    "metadata": { ... }
}
```

### 3. list_files

Lists files in a folder.

**Parameters:**
- `folder_path` (str, optional): Folder path relative to storage_dir
- `recursive` (bool): Whether to list recursively (default: False)
- `file_format` (str, optional): Filter by file format (e.g., "md", "json")

**Example:**
```python
result = server.list_files(
    folder_path="documents",
    recursive=True,
    file_format="md"
)

for file_info in result['files']:
    print(f"{file_info['name']} - {file_info['metadata']['file_size_bytes']} bytes")
```

**Returns:**
```python
{
    "status": "success",
    "folder": "/home/user/.idea_to_prod/google_drive/documents",
    "file_count": 5,
    "files": [
        {
            "name": "doc1.md",
            "relative_path": "doc1.md",
            "metadata": { ... }
        }
    ],
    "truncated": false
}
```

### 4. delete_file

Deletes a file from local storage.

**Parameters:**
- `name` (str): File name (with or without extension)
- `folder_path` (str, optional): Folder path relative to storage_dir

**Example:**
```python
result = server.delete_file(
    name="old_document.md",
    folder_path="documents"
)
```

**Returns:**
```python
{
    "status": "success",
    "message": "File 'old_document.md' deleted successfully",
    "file_path": "/home/user/.idea_to_prod/google_drive/documents/old_document.md"
}
```

### 5. create_folder

Creates a folder in local storage.

**Parameters:**
- `folder_path` (str): Folder path relative to storage_dir

**Example:**
```python
result = server.create_folder(
    folder_path="designs/2024/q1"
)
```

**Returns:**
```python
{
    "status": "success",
    "message": "Folder created successfully",
    "folder_path": "/home/user/.idea_to_prod/google_drive/designs/2024/q1"
}
```

### 6. get_file_metadata

Gets metadata for a file.

**Parameters:**
- `name` (str): File name
- `folder_path` (str, optional): Folder path relative to storage_dir

**Example:**
```python
result = server.get_file_metadata(
    name="design_doc.md",
    folder_path="designs"
)

metadata = result['metadata']
print(f"File size: {metadata['file_size_mb']} MB")
print(f"Created: {metadata['created_timestamp']}")
```

**Returns:**
```python
{
    "status": "success",
    "file_name": "design_doc.md",
    "metadata": {
        "filename": "design_doc.md",
        "file_size_bytes": 2048,
        "file_size_mb": 0.002,
        "created_timestamp": "2024-01-15T10:30:00.123456+00:00",
        "modified_timestamp": "2024-01-15T10:35:00.654321+00:00",
        "extension": ".md",
        "full_path": "/home/user/.idea_to_prod/google_drive/designs/design_doc.md",
        "relative_path": "designs/design_doc.md"
    }
}
```

## Configuration

### Default Configuration

Default storage location: `~/.idea_to_prod/google_drive`

Default settings:
- Mode: `file`
- Logging: `true`
- Log Level: `INFO`
- Max file size: `100 MB`
- Max files per operation: `50`

### Configuration Options

#### Via Code

```python
from idea_to_prod.mcp_servers import GoogleDriveConfig

config = GoogleDriveConfig(
    mode="file",                              # Only 'file' mode supported
    storage_dir="./custom_storage",          # Custom storage directory
    enable_logging=True,                      # Enable logging
    log_level="DEBUG",                        # DEBUG, INFO, WARNING, ERROR, CRITICAL
    google_credentials_path="/path/to/creds", # Future Google Drive integration
    google_project_id="my-project-id",        # Future Google Drive integration
    max_file_size_mb=100,                     # Maximum file size in MB
    max_files_per_operation=50,               # Max files per list operation
)

server = GoogleDriveMCPServer(config=config)
```

#### Via Environment Variables

```bash
# Storage configuration
export GDRIVE_MCP_STORAGE_DIR="/path/to/storage"
export GDRIVE_MCP_MODE="file"

# Logging configuration
export GDRIVE_MCP_LOGGING="true"
export GDRIVE_MCP_LOG_LEVEL="DEBUG"

# Google credentials (for future use)
export GOOGLE_CREDENTIALS_PATH="/path/to/credentials.json"
export GOOGLE_PROJECT_ID="my-project-id"
```

#### Via Dictionary

```python
from idea_to_prod.mcp_servers import GoogleDriveConfig

config_dict = {
    "mode": "file",
    "storage_dir": "./my_storage",
    "enable_logging": True,
    "log_level": "INFO",
}

config = GoogleDriveConfig.from_dict(config_dict)
server = GoogleDriveMCPServer(config=config)
```

### Factory Function

```python
from idea_to_prod.mcp_servers import create_config

config = create_config(
    storage_dir="./documents",
    mode="file",
    enable_logging=True,
    log_level="DEBUG"
)

server = GoogleDriveMCPServer(config=config)
```

## Server Information

### Get Server Info

```python
info = server.get_server_info()
print(info['name'])      # "google-drive-mcp"
print(info['version'])   # "1.0.0"
print(info['mode'])      # "file"
```

### Get Capabilities

```python
caps = server.get_capabilities()
print(caps['tools'])          # List of available tools
print(caps['modes'])          # ["file"]
print(caps['file_formats'])   # ["md", "txt", "json", "html"]
```

## File Formats

The server supports the following file formats:

- **md**: Markdown files
- **txt**: Plain text files
- **json**: JSON files
- **html**: HTML files

## Error Handling

All operations return a status field indicating success or failure:

```python
result = server.save_document(...)

if result['status'] == 'success':
    print("Operation succeeded!")
    print(f"File path: {result['file_path']}")
else:
    print(f"Error: {result['error']}")
    print(f"Message: {result['message']}")
```

## Logging

The server includes built-in logging. Configure it via:

```python
config = GoogleDriveConfig(
    enable_logging=True,
    log_level="DEBUG"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
)

server = GoogleDriveMCPServer(config=config)
# Logs will be printed to console
```

## Usage as part of Idea-To-Prod

This server is used by Agent 1 (High-Level Design) to save design documents:

```python
from idea_to_prod.mcp_servers import GoogleDriveMCPServer

server = GoogleDriveMCPServer()

# Agent 1 generates design and saves it
result = server.save_document(
    name="design_output",
    content=agent_design_output,
    folder_path="agent_outputs/agent_1",
    file_format="md"
)

# Agent 2 can read the design
design = server.read_document(
    name="design_output",
    folder_path="agent_outputs/agent_1"
)
```

## Future Enhancements

This is a stub implementation. Future enhancements may include:

- Real Google Drive integration via Google Drive API
- Support for multiple authentication methods
- Folder sharing and permissions management
- Document version control
- Real-time synchronization
- Integration with additional file services (OneDrive, Dropbox, etc.)

## Limitations

- **File Mode Only**: Currently only operates in file mode (local filesystem)
- **No Real Google Drive Integration**: Does not sync with actual Google Drive
- **Local Only**: All files are stored locally
- **No Authentication**: No actual Google Drive authentication
- **Single Workspace**: No multi-user or workspace support

## Examples

See `example_usage.py` for comprehensive examples demonstrating:

1. Basic usage with default configuration
2. Custom configuration
3. Save and read documents
4. File operations (list, metadata, delete)
5. Multiple file formats
6. Error handling
7. Environment variable configuration

Run examples:
```python
cd src/idea_to_prod/mcp_servers
python example_usage.py
```

## Author

AI For Dev Team

## License

MIT
