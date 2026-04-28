"""
Google Drive MCP Server Example Usage
Demonstrates how to use the configurable Google Drive MCP Server stub.
"""

import json
from pathlib import Path
from ..config.google_drive_config import GoogleDriveConfig, create_config
from ..google_drive_mcp import GoogleDriveMCPServer


def example_basic_usage():
    """Example: Basic usage with default configuration"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Usage with Default Configuration")
    print("="*70)
    
    # Create server with default config
    server = GoogleDriveMCPServer()
    
    # Get server info
    print("\nServer Info:")
    print(json.dumps(server.get_server_info(), indent=2))
    
    print("\nServer Capabilities:")
    print(json.dumps(server.get_capabilities(), indent=2))


def example_custom_config():
    """Example: Custom configuration"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Custom Configuration")
    print("="*70)
    
    # Create custom config
    custom_config = create_config(
        storage_dir="./my_documents",
        mode="file",
        enable_logging=True,
        log_level="DEBUG",
    )
    
    # Create server with custom config
    server = GoogleDriveMCPServer(config=custom_config)
    print(f"\nServer initialized with custom storage: {custom_config.storage_dir}")


def example_save_and_read():
    """Example: Save and read documents"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Save and Read Documents")
    print("="*70)
    
    server = GoogleDriveMCPServer()
    
    # Save a markdown document
    print("\n1. Saving markdown document...")
    result = server.save_document(
        name="project_design",
        content="""# Project Design Document

## Overview
This is a sample high-level design document for the Idea-To-Prod project.

## Architecture
- Agent 1: High-Level Design
- Agent 2: Detailed Design
- Agent 3: Code Generation
- Agent 4: Test Generation
- Agent 5: Test Execution

## Features
- Multi-agent orchestration
- Automatic code generation
- Comprehensive testing
""",
        folder_path="designs",
        file_format="md",
    )
    print(json.dumps(result, indent=2))
    
    # Save a JSON configuration
    print("\n2. Saving JSON configuration...")
    config_data = {
        "project_name": "Idea-To-Prod",
        "version": "1.0.0",
        "agents": 5,
        "features": ["design", "code_gen", "testing"],
    }
    result = server.save_document(
        name="project_config",
        content=json.dumps(config_data, indent=2),
        folder_path="configs",
        file_format="json",
    )
    print(json.dumps(result, indent=2))
    
    # Read the markdown document
    print("\n3. Reading markdown document...")
    result = server.read_document(
        name="project_design",
        folder_path="designs",
    )
    print(f"Status: {result['status']}")
    print(f"File: {result.get('file_name')}")
    if result['status'] == 'success':
        print(f"Content preview (first 200 chars):")
        print(result['content'][:200] + "...")


def example_file_operations():
    """Example: File listing, metadata, and deletion"""
    print("\n" + "="*70)
    print("EXAMPLE 4: File Operations (List, Metadata, Delete)")
    print("="*70)
    
    server = GoogleDriveMCPServer()
    
    # Create a folder structure
    print("\n1. Creating folder structure...")
    server.create_folder("documents/2024/january")
    print("✓ Folder structure created: documents/2024/january")
    
    # Save multiple documents
    print("\n2. Saving multiple documents...")
    for i in range(3):
        server.save_document(
            name=f"report_{i+1}",
            content=f"This is report number {i+1}",
            folder_path="documents",
            file_format="txt",
        )
    print("✓ 3 documents saved")
    
    # List files
    print("\n3. Listing files in documents folder...")
    result = server.list_files(
        folder_path="documents",
        recursive=False,
        file_format="txt",
    )
    print(f"Found {result['file_count']} files:")
    for file_info in result['files']:
        print(f"  - {file_info['name']} ({file_info['metadata']['file_size_bytes']} bytes)")
    
    # Get metadata for a file
    print("\n4. Getting file metadata...")
    result = server.get_file_metadata(
        name="report_1",
        folder_path="documents",
    )
    print(json.dumps(result['metadata'], indent=2))
    
    # Delete a file
    print("\n5. Deleting a file...")
    result = server.delete_file(
        name="report_3.txt",
        folder_path="documents",
    )
    print(f"Status: {result['status']}")
    print(f"Message: {result['message']}")


def example_multiple_formats():
    """Example: Working with different file formats"""
    print("\n" + "="*70)
    print("EXAMPLE 5: Multiple File Formats")
    print("="*70)
    
    server = GoogleDriveMCPServer()
    
    # Markdown
    print("\n1. Saving Markdown...")
    server.save_document(
        name="readme",
        content="# README\n\nThis is a markdown file.",
        folder_path="formats",
        file_format="md",
    )
    print("✓ Markdown file saved")
    
    # Plain text
    print("\n2. Saving Plain Text...")
    server.save_document(
        name="notes",
        content="These are my notes in plain text format.",
        folder_path="formats",
        file_format="txt",
    )
    print("✓ Text file saved")
    
    # JSON
    print("\n3. Saving JSON...")
    json_data = {
        "name": "Idea-To-Prod",
        "type": "multi-agent",
        "agents": 5,
    }
    server.save_document(
        name="metadata",
        content=json.dumps(json_data, indent=2),
        folder_path="formats",
        file_format="json",
    )
    print("✓ JSON file saved")
    
    # HTML
    print("\n4. Saving HTML...")
    html_content = """
    <html>
        <head><title>Report</title></head>
        <body>
            <h1>Project Report</h1>
            <p>This is an HTML report.</p>
        </body>
    </html>
    """
    server.save_document(
        name="report",
        content=html_content,
        folder_path="formats",
        file_format="html",
    )
    print("✓ HTML file saved")
    
    # List all formats
    print("\n5. Listing all files in formats folder...")
    result = server.list_files(
        folder_path="formats",
        recursive=False,
    )
    print(f"Total files: {result['file_count']}")
    for file_info in result['files']:
        print(f"  - {file_info['name']}")


def example_error_handling():
    """Example: Error handling"""
    print("\n" + "="*70)
    print("EXAMPLE 6: Error Handling")
    print("="*70)
    
    server = GoogleDriveMCPServer()
    
    # Try to read non-existent file
    print("\n1. Reading non-existent file...")
    result = server.read_document(
        name="does_not_exist",
        folder_path="nonexistent_folder",
    )
    print(f"Status: {result['status']}")
    print(f"Error: {result['error']}")
    print(f"Message: {result['message']}")
    
    # Try to save empty document
    print("\n2. Saving empty document...")
    result = server.save_document(
        name="empty_doc",
        content="",  # Empty content
        file_format="md",
    )
    print(f"Status: {result['status']}")
    print(f"Error: {result['error']}")
    print(f"Message: {result['message']}")
    
    # Try to delete non-existent file
    print("\n3. Deleting non-existent file...")
    result = server.delete_file(
        name="ghost_file.txt",
        folder_path="nowhere",
    )
    print(f"Status: {result['status']}")
    print(f"Error: {result['error']}")
    print(f"Message: {result['message']}")


def example_environment_config():
    """Example: Configuration from environment variables"""
    print("\n" + "="*70)
    print("EXAMPLE 7: Environment Variable Configuration")
    print("="*70)
    
    print("\nNote: This example would use environment variables if set:")
    print("  - GDRIVE_MCP_STORAGE_DIR: Custom storage directory")
    print("  - GDRIVE_MCP_MODE: Operation mode (file)")
    print("  - GOOGLE_CREDENTIALS_PATH: Path to Google credentials")
    print("  - GOOGLE_PROJECT_ID: Google project ID")
    print("  - GDRIVE_MCP_LOGGING: Enable/disable logging (true/false)")
    print("  - GDRIVE_MCP_LOG_LEVEL: DEBUG, INFO, WARNING, ERROR, CRITICAL")
    
    print("\nExample environment setup:")
    print("  export GDRIVE_MCP_STORAGE_DIR='/tmp/gdrive_files'")
    print("  export GDRIVE_MCP_LOGGING='true'")
    print("  export GDRIVE_MCP_LOG_LEVEL='DEBUG'")
    
    # Show configuration parsing
    config = GoogleDriveConfig()
    print("\nCurrent configuration:")
    print(f"  Storage Dir: {config.storage_dir}")
    print(f"  Mode: {config.mode}")
    print(f"  Logging: {config.enable_logging}")
    print(f"  Log Level: {config.log_level}")


def main():
    """Run all examples"""
    print("\n" + "="*70)
    print("Google Drive MCP Server - Usage Examples")
    print("="*70)
    
    example_basic_usage()
    example_custom_config()
    example_save_and_read()
    example_file_operations()
    example_multiple_formats()
    example_error_handling()
    example_environment_config()
    
    print("\n" + "="*70)
    print("All examples completed!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
