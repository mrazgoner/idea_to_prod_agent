"""
Tests for Google Drive MCP Server
"""

import json
import tempfile
from pathlib import Path

from ..config.google_drive_config import GoogleDriveConfig, create_config
from ..google_drive_mcp import GoogleDriveMCPServer


def test_default_config():
    """Test default configuration"""
    print("\n[TEST] Default Configuration")
    config = GoogleDriveConfig()
    assert config.mode == "file"
    assert config.name == "google-drive-mcp"
    assert config.version == "1.0.0"
    assert config.enable_logging is True
    print("✓ Default configuration is correct")


def test_custom_config():
    """Test custom configuration"""
    print("\n[TEST] Custom Configuration")
    with tempfile.TemporaryDirectory() as tmpdir:
        config = create_config(
            storage_dir=tmpdir,
            mode="file",
            enable_logging=False,
            log_level="ERROR",
        )
        assert str(config.storage_dir) == tmpdir
        assert config.mode == "file"
        assert config.enable_logging is False
        print("✓ Custom configuration is correct")


def test_config_from_dict():
    """Test creating config from dictionary"""
    print("\n[TEST] Config from Dictionary")
    config_dict = {
        "mode": "file",
        "enable_logging": False,
    }
    config = GoogleDriveConfig.from_dict(config_dict)
    assert config.mode == "file"
    assert config.enable_logging is False
    print("✓ Config from dictionary works")


def test_config_to_dict():
    """Test converting config to dictionary"""
    print("\n[TEST] Config to Dictionary")
    config = GoogleDriveConfig()
    config_dict = config.to_dict()
    assert isinstance(config_dict, dict)
    assert config_dict["mode"] == "file"
    assert config_dict["name"] == "google-drive-mcp"
    print("✓ Config to dictionary conversion works")


def test_server_init():
    """Test server initialization"""
    print("\n[TEST] Server Initialization")
    server = GoogleDriveMCPServer()
    assert server.config is not None
    assert server.logger is not None
    print("✓ Server initialization successful")


def test_get_server_info():
    """Test getting server info"""
    print("\n[TEST] Get Server Info")
    server = GoogleDriveMCPServer()
    info = server.get_server_info()
    assert info["name"] == "google-drive-mcp"
    assert info["version"] == "1.0.0"
    assert info["mode"] == "file"
    print("✓ Server info retrieval works")
    print(f"  Info: {json.dumps(info, default=str, indent=2)}")


def test_get_capabilities():
    """Test getting server capabilities"""
    print("\n[TEST] Get Capabilities")
    server = GoogleDriveMCPServer()
    caps = server.get_capabilities()
    assert "tools" in caps
    assert "modes" in caps
    assert "file_formats" in caps
    assert "md" in caps["file_formats"]
    print("✓ Capabilities retrieval works")
    print(f"  Tools: {caps['tools']}")


def test_save_document():
    """Test saving a document"""
    print("\n[TEST] Save Document")
    with tempfile.TemporaryDirectory() as tmpdir:
        config = create_config(storage_dir=tmpdir, enable_logging=False)
        server = GoogleDriveMCPServer(config=config)
        
        result = server.save_document(
            name="test_doc",
            content="# Test Document\n\nThis is a test.",
            file_format="md",
        )
        
        assert result["status"] == "success"
        assert "file_path" in result
        assert "metadata" in result
        assert Path(result["file_path"]).exists()
        print("✓ Document saved successfully")


def test_read_document():
    """Test reading a document"""
    print("\n[TEST] Read Document")
    with tempfile.TemporaryDirectory() as tmpdir:
        config = create_config(storage_dir=tmpdir, enable_logging=False)
        server = GoogleDriveMCPServer(config=config)
        
        # Save document
        content = "# Test\n\nTest content"
        server.save_document(
            name="test_doc",
            content=content,
            file_format="md",
        )
        
        # Read document
        result = server.read_document(name="test_doc")
        
        assert result["status"] == "success"
        assert result["content"] == content
        assert result["file_name"] == "test_doc.md"
        print("✓ Document read successfully")


def test_create_folder():
    """Test creating folders"""
    print("\n[TEST] Create Folder")
    with tempfile.TemporaryDirectory() as tmpdir:
        config = create_config(storage_dir=tmpdir, enable_logging=False)
        server = GoogleDriveMCPServer(config=config)
        
        result = server.create_folder("documents/2024/january")
        
        assert result["status"] == "success"
        assert Path(result["folder_path"]).exists()
        print("✓ Folder created successfully")


def test_save_with_folder():
    """Test saving document to a folder"""
    print("\n[TEST] Save Document to Folder")
    with tempfile.TemporaryDirectory() as tmpdir:
        config = create_config(storage_dir=tmpdir, enable_logging=False)
        server = GoogleDriveMCPServer(config=config)
        
        result = server.save_document(
            name="test_doc",
            content="Test content",
            folder_path="documents/2024",
            file_format="txt",
        )
        
        assert result["status"] == "success"
        assert "documents" in result["file_path"]
        assert "2024" in result["file_path"]
        print("✓ Document saved to folder successfully")


def test_list_files():
    """Test listing files"""
    print("\n[TEST] List Files")
    with tempfile.TemporaryDirectory() as tmpdir:
        config = create_config(storage_dir=tmpdir, enable_logging=False)
        server = GoogleDriveMCPServer(config=config)
        
        # Save multiple documents
        for i in range(3):
            server.save_document(
                name=f"doc_{i}",
                content=f"Content {i}",
                folder_path="documents",
                file_format="txt",
            )
        
        result = server.list_files(folder_path="documents")
        
        assert result["status"] == "success"
        assert result["file_count"] == 3
        assert len(result["files"]) == 3
        print("✓ Files listed successfully")
        for file_info in result["files"]:
            print(f"    - {file_info['name']}")


def test_list_files_with_format():
    """Test listing files with format filter"""
    print("\n[TEST] List Files with Format Filter")
    with tempfile.TemporaryDirectory() as tmpdir:
        config = create_config(storage_dir=tmpdir, enable_logging=False)
        server = GoogleDriveMCPServer(config=config)
        
        # Save files in different formats
        server.save_document(name="doc1", content="txt content", file_format="txt")
        server.save_document(name="doc2", content="md content", file_format="md")
        server.save_document(name="doc3", content="txt content", file_format="txt")
        
        # List only txt files
        result = server.list_files(file_format="txt")
        
        assert result["status"] == "success"
        assert result["file_count"] == 2
        print("✓ Files listed with format filter successfully")


def test_get_file_metadata():
    """Test getting file metadata"""
    print("\n[TEST] Get File Metadata")
    with tempfile.TemporaryDirectory() as tmpdir:
        config = create_config(storage_dir=tmpdir, enable_logging=False)
        server = GoogleDriveMCPServer(config=config)
        
        server.save_document(
            name="test_doc",
            content="Test content",
            file_format="md",
        )
        
        result = server.get_file_metadata(name="test_doc")
        
        assert result["status"] == "success"
        assert "metadata" in result
        metadata = result["metadata"]
        assert metadata["filename"] == "test_doc.md"
        assert metadata["file_size_bytes"] > 0
        print("✓ File metadata retrieved successfully")
        print(f"    Size: {metadata['file_size_bytes']} bytes")


def test_delete_file():
    """Test deleting a file"""
    print("\n[TEST] Delete File")
    with tempfile.TemporaryDirectory() as tmpdir:
        config = create_config(storage_dir=tmpdir, enable_logging=False)
        server = GoogleDriveMCPServer(config=config)
        
        # Save document
        server.save_document(
            name="test_doc",
            content="Test content",
            file_format="md",
        )
        
        # Delete document
        result = server.delete_file(name="test_doc")
        
        assert result["status"] == "success"
        assert not Path(result["file_path"]).exists()
        print("✓ File deleted successfully")


def test_delete_nonexistent():
    """Test error handling for deleting non-existent file"""
    print("\n[TEST] Delete Non-existent File (Error Handling)")
    with tempfile.TemporaryDirectory() as tmpdir:
        config = create_config(storage_dir=tmpdir, enable_logging=False)
        server = GoogleDriveMCPServer(config=config)
        
        result = server.delete_file(name="nonexistent")
        
        assert result["status"] == "error"
        assert "error" in result
        print("✓ Error handling works for non-existent file")


def test_read_nonexistent():
    """Test error handling for reading non-existent file"""
    print("\n[TEST] Read Non-existent File (Error Handling)")
    with tempfile.TemporaryDirectory() as tmpdir:
        config = create_config(storage_dir=tmpdir, enable_logging=False)
        server = GoogleDriveMCPServer(config=config)
        
        result = server.read_document(name="nonexistent")
        
        assert result["status"] == "error"
        assert "error" in result
        print("✓ Error handling works for non-existent file")


def test_save_empty_content():
    """Test error handling for saving empty content"""
    print("\n[TEST] Save Empty Content (Error Handling)")
    with tempfile.TemporaryDirectory() as tmpdir:
        config = create_config(storage_dir=tmpdir, enable_logging=False)
        server = GoogleDriveMCPServer(config=config)
        
        result = server.save_document(
            name="empty_doc",
            content="",
            file_format="md",
        )
        
        assert result["status"] == "error"
        assert "error" in result
        print("✓ Error handling works for empty content")


def test_multiple_formats():
    """Test saving in multiple formats"""
    print("\n[TEST] Multiple File Formats")
    with tempfile.TemporaryDirectory() as tmpdir:
        config = create_config(storage_dir=tmpdir, enable_logging=False)
        server = GoogleDriveMCPServer(config=config)
        
        formats = ["md", "txt", "json", "html"]
        for fmt in formats:
            result = server.save_document(
                name=f"doc",
                content=f"Content in {fmt}",
                file_format=fmt,
            )
            assert result["status"] == "success", f"Failed to save {fmt}"
        
        print("✓ All file formats saved successfully")
        print(f"  Formats: {formats}")


def test_recursive_list():
    """Test recursive file listing"""
    print("\n[TEST] Recursive File Listing")
    with tempfile.TemporaryDirectory() as tmpdir:
        config = create_config(storage_dir=tmpdir, enable_logging=False)
        server = GoogleDriveMCPServer(config=config)
        
        # Create nested structure
        server.save_document(
            name="doc1",
            content="content",
            folder_path="a/b/c",
            file_format="txt",
        )
        server.save_document(
            name="doc2",
            content="content",
            folder_path="a/b",
            file_format="txt",
        )
        server.save_document(
            name="doc3",
            content="content",
            folder_path="a",
            file_format="txt",
        )
        
        # List recursively
        result = server.list_files(recursive=True)
        
        assert result["status"] == "success"
        assert result["file_count"] == 3
        print("✓ Recursive file listing works")


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print("Google Drive MCP Server - Unit Tests")
    print("="*70)
    
    tests = [
        test_default_config,
        test_custom_config,
        test_config_from_dict,
        test_config_to_dict,
        test_server_init,
        test_get_server_info,
        test_get_capabilities,
        test_save_document,
        test_read_document,
        test_create_folder,
        test_save_with_folder,
        test_list_files,
        test_list_files_with_format,
        test_get_file_metadata,
        test_delete_file,
        test_delete_nonexistent,
        test_read_nonexistent,
        test_save_empty_content,
        test_multiple_formats,
        test_recursive_list,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"✗ FAILED: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*70)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("="*70 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
