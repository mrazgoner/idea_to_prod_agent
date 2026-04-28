"""
Google Drive MCP Server Stub
A configurable Model Context Protocol server for Google Drive operations.
Supports both 'file' mode to save documents locally and 'api' mode for real Google Drive integration.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Dict, List
from dataclasses import asdict

from .config.google_drive_config import GoogleDriveConfig, create_config

# Import Google Drive API for real operations
try:
    from google.oauth2 import service_account
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.exceptions import DefaultCredentialsError
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    GOOGLE_DRIVE_AVAILABLE = True
except ImportError:
    GOOGLE_DRIVE_AVAILABLE = False


class GoogleDriveMCPServer:
    """
    MCP Server for Google Drive operations.
    Stub implementation that saves files locally.
    """
    
    def __init__(self, config: Optional[GoogleDriveConfig] = None):
        """
        Initialize Google Drive MCP Server
        
        Args:
            config: GoogleDriveConfig instance. If None, uses default config.
        """
        self.config = config or GoogleDriveConfig()
        self._setup_logging()
        self.logger.info(f"Initializing {self.config.name} v{self.config.version}")
        self.logger.info(f"Mode: {self.config.mode}, Storage: {self.config.storage_dir}")
        
        # Initialize Google Drive API client if in 'api' mode
        self.drive_service = None
        if self.config.mode == "api":
            if not GOOGLE_DRIVE_AVAILABLE:
                raise ImportError("Google Drive API libraries are required for 'api' mode. Install with: pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client")
            
            try:
                self.drive_service = self._init_google_drive_api()
                self.logger.info("Google Drive API client initialized successfully")
            except Exception as e:
                self.logger.error(f"Failed to initialize Google Drive API: {e}")
                raise
    
    def _setup_logging(self):
        """Configure logging based on config settings"""
        self.logger = logging.getLogger(self.config.name)
        
        if self.config.enable_logging:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(self.config.log_level)
        else:
            self.logger.addHandler(logging.NullHandler())
    
    def _init_google_drive_api(self):
        """Initialize Google Drive API service"""
        SCOPES = ['https://www.googleapis.com/auth/drive']
        
        # Try to use service account credentials first
        try:
            import os
            if 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ:
                credentials = service_account.Credentials.from_service_account_file(
                    os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
                    scopes=SCOPES
                )
                return build('drive', 'v3', credentials=credentials)
        except Exception as e:
            self.logger.debug(f"Service account auth failed: {e}")
        
        # Fall back to OAuth2 flow
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json',
                SCOPES
            )
            credentials = flow.run_local_server(port=0)
            return build('drive', 'v3', credentials=credentials)
        except FileNotFoundError:
            raise ValueError(
                "Google Drive API requires credentials.json or GOOGLE_APPLICATION_CREDENTIALS "
                "environment variable for OAuth2 authentication"
            )
        except Exception as e:
            raise ValueError(f"Failed to initialize Google Drive API: {e}")
    
    # =========================================================================
    # Tool: save_document
    # =========================================================================
    
    def save_document(
        self,
        name: str,
        content: str,
        folder_path: Optional[str] = None,
        file_format: str = "md",
    ) -> Dict[str, Any]:
        """
        Save a document to storage (local or Google Drive)
        
        Args:
            name: Document name (without extension)
            content: Document content as string
            folder_path: Optional folder path relative to storage_dir or Google Drive folder ID
            file_format: File format (md, txt, json, html)
        
        Returns:
            Dict with operation result and file metadata
        """
        self.logger.info(f"save_document called: name={name}, format={file_format}")
        
        if self.config.mode == "api":
            return self._api_save_document(name, content, folder_path, file_format)
        else:
            return self._file_save_document(name, content, folder_path, file_format)
    
    def _api_save_document(
        self,
        name: str,
        content: str,
        folder_path: Optional[str] = None,
        file_format: str = "md",
    ) -> Dict[str, Any]:
        """Real Google Drive API implementation for save_document"""
        try:
            from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload
            import io
            
            # Validate inputs
            if not name or not isinstance(name, str):
                raise ValueError("Document name must be a non-empty string")
            
            if not content or not isinstance(content, str):
                raise ValueError("Content must be a non-empty string")
            
            # Check file size
            content_size_mb = len(content.encode('utf-8')) / (1024 * 1024)
            if content_size_mb > self.config.max_file_size_mb:
                raise ValueError(
                    f"Content size {content_size_mb:.2f}MB exceeds limit "
                    f"of {self.config.max_file_size_mb}MB"
                )
            
            # Prepare file metadata
            filename = f"{name}.{file_format}"
            
            # Map file format to MIME type
            mime_types = {
                "md": "text/markdown",
                "txt": "text/plain",
                "json": "application/json",
                "html": "text/html",
            }
            mime_type = mime_types.get(file_format, "text/plain")
            
            # Create file metadata
            file_metadata = {"name": filename}
            
            # Set parent folder if provided
            if folder_path:
                file_metadata["parents"] = [folder_path]
            
            # Upload file
            media = MediaIoBaseUpload(io.BytesIO(content.encode('utf-8')), mimetype=mime_type)
            file = self.drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name, mimeType, createdTime, modifiedTime, fileSize'
            ).execute()
            
            self.logger.info(f"Document saved via Google Drive API: {filename}")
            
            return {
                "status": "success",
                "message": f"Document '{name}' saved successfully to Google Drive",
                "file_id": file.get('id'),
                "file_name": file.get('name'),
                "metadata": {
                    "filename": file.get('name'),
                    "file_size_bytes": file.get('fileSize', len(content.encode('utf-8'))),
                    "file_size_mb": round(file.get('fileSize', len(content.encode('utf-8'))) / (1024 * 1024), 4),
                    "created_timestamp": file.get('createdTime'),
                    "modified_timestamp": file.get('modifiedTime'),
                    "extension": file_format,
                    "mime_type": mime_type,
                },
            }
        except HttpError as e:
            self.logger.error(f"Google Drive API error: {e}")
            return {
                "status": "error",
                "message": f"Google Drive API error: {str(e)}",
                "error": type(e).__name__,
            }
        except Exception as e:
            self.logger.error(f"Error saving document via API: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to save document: {str(e)}",
                "error": type(e).__name__,
            }
    
    def _file_save_document(
        self,
        name: str,
        content: str,
        folder_path: Optional[str] = None,
        file_format: str = "md",
    ) -> Dict[str, Any]:
        """File-based implementation for save_document (local storage)"""
        try:
            # Validate inputs
            if not name or not isinstance(name, str):
                raise ValueError("Document name must be a non-empty string")
            
            if not content or not isinstance(content, str):
                raise ValueError("Content must be a non-empty string")
            
            # Check file size
            content_size_mb = len(content.encode('utf-8')) / (1024 * 1024)
            if content_size_mb > self.config.max_file_size_mb:
                raise ValueError(
                    f"Content size {content_size_mb:.2f}MB exceeds limit "
                    f"of {self.config.max_file_size_mb}MB"
                )
            
            # Construct file path
            target_dir = self.config.storage_dir
            if folder_path:
                target_dir = target_dir / folder_path
                target_dir.mkdir(parents=True, exist_ok=True)
            
            filename = f"{name}.{file_format}"
            file_path = target_dir / filename
            
            # Save file
            file_path.write_text(content, encoding='utf-8')
            
            # Generate metadata
            metadata = self._generate_file_metadata(file_path, filename)
            
            self.logger.info(f"Document saved successfully: {file_path}")
            
            return {
                "status": "success",
                "message": f"Document '{name}' saved successfully",
                "file_path": str(file_path),
                "metadata": metadata,
            }
        
        except Exception as e:
            self.logger.error(f"Error saving document: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to save document: {str(e)}",
                "error": type(e).__name__,
            }
    
    # =========================================================================
    # Tool: read_document
    # =========================================================================
    
    def read_document(
        self,
        name: str,
        folder_path: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Read a document from storage (local or Google Drive)
        
        Args:
            name: Document name (with or without extension)
            folder_path: Optional folder path relative to storage_dir or Google Drive folder ID
        
        Returns:
            Dict with document content and metadata
        """
        self.logger.info(f"read_document called: name={name}")
        
        if self.config.mode == "api":
            return self._api_read_document(name, folder_path)
        else:
            return self._file_read_document(name, folder_path)
    
    def _api_read_document(
        self,
        name: str,
        folder_path: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Real Google Drive API implementation for read_document"""
        try:
            from googleapiclient.http import MediaIoBaseDownload
            import io
            
            # Build query to find the file
            query = f"name='{name}' or name='{name}.md' or name='{name}.txt' or name='{name}.json' or name='{name}.html'"
            if folder_path:
                query += f" and parents='{folder_path}'"
            
            # Search for the file
            results = self.drive_service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name, mimeType, modifiedTime, fileSize)',
                pageSize=1
            ).execute()
            
            files = results.get('files', [])
            if not files:
                return {
                    "status": "error",
                    "message": f"Document not found: {name}",
                    "error": "FileNotFoundError",
                }
            
            file_info = files[0]
            file_id = file_info['id']
            
            # Download file content
            request = self.drive_service.files().get_media(fileId=file_id)
            file_content = io.BytesIO()
            downloader = MediaIoBaseDownload(file_content, request)
            done = False
            while not done:
                _, done = downloader.next_chunk()
            
            content = file_content.getvalue().decode('utf-8')
            
            self.logger.info(f"Document read via Google Drive API: {file_info['name']}")
            
            return {
                "status": "success",
                "file_name": file_info['name'],
                "content": content,
                "metadata": {
                    "filename": file_info['name'],
                    "file_size_bytes": file_info.get('fileSize'),
                    "file_size_mb": round(file_info.get('fileSize', 0) / (1024 * 1024), 4) if file_info.get('fileSize') else 'unknown',
                    "modified_timestamp": file_info.get('modifiedTime'),
                    "mime_type": file_info.get('mimeType'),
                    "file_id": file_id,
                },
            }
        except HttpError as e:
            self.logger.error(f"Google Drive API error: {e}")
            return {
                "status": "error",
                "message": f"Google Drive API error: {str(e)}",
                "error": type(e).__name__,
            }
        except Exception as e:
            self.logger.error(f"Error reading document via API: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to read document: {str(e)}",
                "error": type(e).__name__,
            }
    
    def _file_read_document(
        self,
        name: str,
        folder_path: Optional[str] = None,
    ) -> Dict[str, Any]:
        """File-based implementation for read_document (local storage)"""
        try:
            # Construct file path
            target_dir = self.config.storage_dir
            if folder_path:
                target_dir = target_dir / folder_path
            
            # Handle name with or without extension
            file_path = target_dir / name
            if not file_path.exists():
                # Try with common extensions
                for ext in ['md', 'txt', 'json', 'html']:
                    candidate = target_dir / f"{name}.{ext}"
                    if candidate.exists():
                        file_path = candidate
                        break
            
            if not file_path.exists():
                raise FileNotFoundError(f"Document not found: {name}")
            
            # Read file
            content = file_path.read_text(encoding='utf-8')
            metadata = self._generate_file_metadata(file_path, file_path.name)
            
            self.logger.info(f"Document read successfully: {file_path}")
            
            return {
                "status": "success",
                "file_name": file_path.name,
                "content": content,
                "metadata": metadata,
            }
        
        except Exception as e:
            self.logger.error(f"Error reading document: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to read document: {str(e)}",
                "error": type(e).__name__,
            }
    
    # =========================================================================
    # Tool: list_files
    # =========================================================================
    
    def list_files(
        self,
        folder_path: Optional[str] = None,
        recursive: bool = False,
        file_format: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        List files in a folder
        
        Args:
            folder_path: Optional folder path relative to storage_dir
            recursive: Whether to list recursively
            file_format: Optional file format filter (e.g., 'md', 'txt')
        
        Returns:
            Dict with list of files and metadata
        """
        self.logger.info(f"list_files called: folder={folder_path}, recursive={recursive}")
        
        try:
            target_dir = self.config.storage_dir
            if folder_path:
                target_dir = target_dir / folder_path
            
            if not target_dir.exists():
                raise FileNotFoundError(f"Folder not found: {target_dir}")
            
            # List files
            if recursive:
                pattern = "**/*" if not file_format else f"**/*.{file_format}"
                file_paths = list(target_dir.glob(pattern))
            else:
                pattern = "*" if not file_format else f"*.{file_format}"
                file_paths = list(target_dir.glob(pattern))
            
            # Filter out directories and limit results
            file_paths = [p for p in file_paths if p.is_file()]
            
            if len(file_paths) > self.config.max_files_per_operation:
                file_paths = file_paths[:self.config.max_files_per_operation]
                truncated = True
            else:
                truncated = False
            
            # Generate file list with metadata
            files = []
            for file_path in file_paths:
                metadata = self._generate_file_metadata(file_path, file_path.name)
                files.append({
                    "name": file_path.name,
                    "relative_path": str(file_path.relative_to(self.config.storage_dir)),
                    "metadata": metadata,
                })
            
            self.logger.info(f"Listed {len(files)} files")
            
            return {
                "status": "success",
                "folder": str(target_dir),
                "file_count": len(files),
                "files": files,
                "truncated": truncated,
            }
        
        except Exception as e:
            self.logger.error(f"Error listing files: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to list files: {str(e)}",
                "error": type(e).__name__,
            }
    
    # =========================================================================
    # Tool: delete_file
    # =========================================================================
    
    def delete_file(
        self,
        name: str,
        folder_path: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Delete a file from local storage
        
        Args:
            name: File name (with or without extension)
            folder_path: Optional folder path relative to storage_dir
        
        Returns:
            Dict with operation result
        """
        self.logger.info(f"delete_file called: name={name}")
        
        try:
            target_dir = self.config.storage_dir
            if folder_path:
                target_dir = target_dir / folder_path
            
            # Find file
            file_path = target_dir / name
            if not file_path.exists():
                for ext in ['md', 'txt', 'json', 'html']:
                    candidate = target_dir / f"{name}.{ext}"
                    if candidate.exists():
                        file_path = candidate
                        break
            
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {name}")
            
            # Delete file
            file_path.unlink()
            
            self.logger.info(f"File deleted successfully: {file_path}")
            
            return {
                "status": "success",
                "message": f"File '{name}' deleted successfully",
                "file_path": str(file_path),
            }
        
        except Exception as e:
            self.logger.error(f"Error deleting file: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to delete file: {str(e)}",
                "error": type(e).__name__,
            }
    
    # =========================================================================
    # Tool: create_folder
    # =========================================================================
    
    def create_folder(
        self,
        folder_path: str,
    ) -> Dict[str, Any]:
        """
        Create a folder in local storage
        
        Args:
            folder_path: Folder path relative to storage_dir
        
        Returns:
            Dict with operation result
        """
        self.logger.info(f"create_folder called: folder_path={folder_path}")
        
        try:
            if not folder_path or not isinstance(folder_path, str):
                raise ValueError("Folder path must be a non-empty string")
            
            target_path = self.config.storage_dir / folder_path
            target_path.mkdir(parents=True, exist_ok=True)
            
            self.logger.info(f"Folder created successfully: {target_path}")
            
            return {
                "status": "success",
                "message": f"Folder created successfully",
                "folder_path": str(target_path),
            }
        
        except Exception as e:
            self.logger.error(f"Error creating folder: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to create folder: {str(e)}",
                "error": type(e).__name__,
            }
    
    # =========================================================================
    # Tool: get_file_metadata
    # =========================================================================
    
    def get_file_metadata(
        self,
        name: str,
        folder_path: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get metadata for a file
        
        Args:
            name: File name
            folder_path: Optional folder path relative to storage_dir
        
        Returns:
            Dict with file metadata
        """
        self.logger.info(f"get_file_metadata called: name={name}")
        
        try:
            target_dir = self.config.storage_dir
            if folder_path:
                target_dir = target_dir / folder_path
            
            # Find file
            file_path = target_dir / name
            if not file_path.exists():
                for ext in ['md', 'txt', 'json', 'html']:
                    candidate = target_dir / f"{name}.{ext}"
                    if candidate.exists():
                        file_path = candidate
                        break
            
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {name}")
            
            metadata = self._generate_file_metadata(file_path, file_path.name)
            
            return {
                "status": "success",
                "file_name": file_path.name,
                "metadata": metadata,
            }
        
        except Exception as e:
            self.logger.error(f"Error getting file metadata: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to get file metadata: {str(e)}",
                "error": type(e).__name__,
            }
    
    # =========================================================================
    # Helper Methods
    # =========================================================================
    
    def _generate_file_metadata(self, file_path: Path, filename: str) -> Dict[str, Any]:
        """Generate metadata for a file"""
        stat = file_path.stat()
        return {
            "filename": filename,
            "file_size_bytes": stat.st_size,
            "file_size_mb": round(stat.st_size / (1024 * 1024), 4),
            "created_timestamp": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified_timestamp": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "extension": file_path.suffix,
            "full_path": str(file_path),
            "relative_path": str(file_path.relative_to(self.config.storage_dir)),
        }
    
    # =========================================================================
    # Server Management
    # =========================================================================
    
    def get_server_info(self) -> Dict[str, Any]:
        """Get server information"""
        return {
            "name": self.config.name,
            "version": self.config.version,
            "mode": self.config.mode,
            "storage_dir": str(self.config.storage_dir),
            "enabled_tools": self.config.allowed_tools,
            "config": self.config.to_dict(),
        }
    
    def get_capabilities(self) -> Dict[str, List[str]]:
        """Get server capabilities"""
        return {
            "tools": self.config.allowed_tools,
            "modes": ["file"],  # Only file mode is supported
            "file_formats": ["md", "txt", "json", "html"],
        }
