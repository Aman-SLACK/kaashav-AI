"""
Utility functions for FlowState AI Research Agent.
Handles file operations, logging, and common helper functions.
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def ensure_directory(directory_path: str) -> Path:
    """
    Ensure a directory exists; create it if it doesn't.
    
    Args:
        directory_path: Path to the directory to create/verify.
        
    Returns:
        Path object of the directory.
        
    Raises:
        OSError: If directory creation fails.
    """
    try:
        path = Path(directory_path)
        path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Directory ready: {directory_path}")
        return path
    except OSError as e:
        logger.error(f"Failed to create directory {directory_path}: {e}")
        raise


def save_markdown(content: str, filename: str, directory: str = "research") -> str:
    """
    Save content as a Markdown file in the specified directory.
    
    Args:
        content: Markdown content to save.
        filename: Name of the file (e.g., "ai_trends.md").
        directory: Target directory (default: "research").
        
    Returns:
        Full path to the saved file.
        
    Raises:
        IOError: If file writing fails.
    """
    try:
        # Ensure directory exists
        dir_path = ensure_directory(directory)
        
        # Construct full file path
        file_path = dir_path / filename
        
        # Write content to file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        logger.info(f"Markdown saved: {file_path}")
        return str(file_path)
    
    except IOError as e:
        logger.error(f"Failed to save markdown {filename}: {e}")
        raise


def save_json(data: Dict[str, Any], filename: str, directory: str = "research") -> str:
    """
    Save data as a JSON file in the specified directory.
    
    Args:
        data: Dictionary or JSON-serializable data.
        filename: Name of the file (e.g., "research_data.json").
        directory: Target directory (default: "research").
        
    Returns:
        Full path to the saved file.
        
    Raises:
        IOError: If file writing fails.
        ValueError: If data is not JSON-serializable.
    """
    try:
        # Ensure directory exists
        dir_path = ensure_directory(directory)
        
        # Construct full file path
        file_path = dir_path / filename
        
        # Write JSON with nice formatting
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"JSON saved: {file_path}")
        return str(file_path)
    
    except (IOError, ValueError) as e:
        logger.error(f"Failed to save JSON {filename}: {e}")
        raise


def read_markdown(file_path: str) -> str:
    """
    Read and return content from a Markdown file.
    
    Args:
        file_path: Full path to the markdown file.
        
    Returns:
        File content as a string.
        
    Raises:
        FileNotFoundError: If file doesn't exist.
        IOError: If file reading fails.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        logger.info(f"Markdown read: {file_path}")
        return content
    
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise
    except IOError as e:
        logger.error(f"Failed to read markdown {file_path}: {e}")
        raise


def read_json(file_path: str) -> Dict[str, Any]:
    """
    Read and return data from a JSON file.
    
    Args:
        file_path: Full path to the JSON file.
        
    Returns:
        Parsed JSON data as a dictionary.
        
    Raises:
        FileNotFoundError: If file doesn't exist.
        json.JSONDecodeError: If JSON is invalid.
        IOError: If file reading fails.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        logger.info(f"JSON read: {file_path}")
        return data
    
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {file_path}: {e}")
        raise
    except IOError as e:
        logger.error(f"Failed to read JSON {file_path}: {e}")
        raise


def generate_filename(prefix: str = "content", extension: str = "md") -> str:
    """
    Generate a timestamped filename for automatic content creation.
    
    Args:
        prefix: Prefix for the filename (e.g., "research").
        extension: File extension without dot (default: "md").
        
    Returns:
        Filename with timestamp (e.g., "research_2025_05_30_14_32_45.md").
    """
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    filename = f"{prefix}_{timestamp}.{extension}"
    logger.info(f"Generated filename: {filename}")
    return filename


def list_files(directory: str, extension: Optional[str] = None) -> List[str]:
    """
    List all files in a directory, optionally filtered by extension.
    
    Args:
        directory: Path to the directory.
        extension: Optional file extension to filter (e.g., "md", "json").
        
    Returns:
        List of file paths.
        
    Raises:
        FileNotFoundError: If directory doesn't exist.
    """
    try:
        dir_path = Path(directory)
        
        if not dir_path.exists():
            logger.error(f"Directory not found: {directory}")
            raise FileNotFoundError(f"Directory not found: {directory}")
        
        if extension:
            files = list(dir_path.glob(f"*.{extension}"))
        else:
            files = list(dir_path.glob("*"))
        
        file_paths = [str(f) for f in files if f.is_file()]
        logger.info(f"Found {len(file_paths)} files in {directory}")
        return file_paths
    
    except FileNotFoundError as e:
        logger.error(f"Failed to list files in {directory}: {e}")
        raise


def get_env_var(key: str, default: Optional[str] = None) -> str:
    """
    Safely retrieve environment variables with optional default.
    Use this for all secret/config retrieval to enforce consistency.
    
    Args:
        key: Environment variable name.
        default: Default value if not found (should be None for secrets).
        
    Returns:
        Environment variable value.
        
    Raises:
        ValueError: If required variable is missing (when default is None).
    """
    value = os.getenv(key, default)
    
    if value is None:
        logger.error(f"Required environment variable missing: {key}")
        raise ValueError(f"Environment variable '{key}' is not set.")
    
    logger.debug(f"Environment variable loaded: {key}")
    return value


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename by removing/replacing invalid characters.
    
    Args:
        filename: Original filename.
        
    Returns:
        Sanitized filename safe for filesystem.
    """
    # Replace invalid characters with underscores
    invalid_chars = r'<>:"/\|?*'
    sanitized = filename
    for char in invalid_chars:
        sanitized = sanitized.replace(char, "_")
    
    logger.debug(f"Filename sanitized: {filename} -> {sanitized}")
    return sanitized


if __name__ == "__main__":
    # Test utilities
    print("FlowState AI Utils Module - Ready for import.")
