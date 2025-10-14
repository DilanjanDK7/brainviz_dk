"""
Test configuration for BrainViz_DK.

This module provides configuration for test data paths and handles
missing test data gracefully.
"""

import os
import tempfile
from pathlib import Path
from typing import Optional


class TestConfig:
    """Configuration for test data and paths."""
    
    def __init__(self):
        """Initialize test configuration."""
        self._test_data_dir = None
        self._temp_dir = None
    
    @property
    def test_data_dir(self) -> Optional[Path]:
        """Get test data directory if available."""
        if self._test_data_dir is None:
            self._test_data_dir = self._find_test_data_dir()
        return self._test_data_dir
    
    @property
    def temp_dir(self) -> Path:
        """Get temporary directory for test outputs."""
        if self._temp_dir is None:
            self._temp_dir = Path(tempfile.mkdtemp(prefix="brainviz_test_"))
        return self._temp_dir
    
    def _find_test_data_dir(self) -> Optional[Path]:
        """Find test data directory from environment or common locations."""
        # Check environment variable first
        env_path = os.getenv('BRAINVIZ_TEST_DATA_DIR')
        if env_path and Path(env_path).exists():
            return Path(env_path)
        
        # Check common test data locations
        common_paths = [
            Path("test_data"),
            Path("tests/test_data"),
            Path("../test_data"),
            Path("../../test_data"),
            Path("/tmp/brainviz_test_data"),
        ]
        
        for path in common_paths:
            if path.exists() and (path / "group_mean.nii.gz").exists():
                return path
        
        return None
    
    def get_test_nifti(self, filename: str = "group_mean.nii.gz") -> Optional[Path]:
        """Get path to test NIfTI file."""
        if self.test_data_dir is None:
            return None
        return self.test_data_dir / filename
    
    def has_test_data(self) -> bool:
        """Check if test data is available."""
        return self.test_data_dir is not None
    
    def create_sample_nifti(self, output_path: Path) -> bool:
        """Create a sample NIfTI file for testing if no test data available."""
        try:
            import numpy as np
            import nibabel as nib
            
            # Create a small sample brain volume
            data = np.random.rand(32, 32, 32) * 0.1
            # Add some structure
            data[10:22, 10:22, 10:22] += 0.5
            
            # Create NIfTI image
            affine = np.eye(4)
            img = nib.Nifti1Image(data, affine)
            
            # Save
            output_path.parent.mkdir(parents=True, exist_ok=True)
            nib.save(img, output_path)
            return True
            
        except ImportError:
            return False
        except Exception:
            return False


# Global test configuration instance
test_config = TestConfig()


def get_test_nifti_path(filename: str = "group_mean.nii.gz") -> Optional[Path]:
    """Get test NIfTI file path, creating sample if needed."""
    nifti_path = test_config.get_test_nifti(filename)
    
    if nifti_path is None:
        # Try to create a sample file
        sample_path = test_config.temp_dir / filename
        if test_config.create_sample_nifti(sample_path):
            return sample_path
    
    return nifti_path


def skip_if_no_test_data():
    """Decorator to skip tests if no test data is available."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not test_config.has_test_data():
                import pytest
                pytest.skip("No test data available. Set BRAINVIZ_TEST_DATA_DIR environment variable.")
            return func(*args, **kwargs)
        return wrapper
    return decorator
