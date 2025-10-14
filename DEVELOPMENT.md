# BrainViz_DK Development Setup Guide

This guide helps you set up BrainViz_DK for development and testing.

## Quick Start

### 1. Install Dependencies

```bash
# Core dependencies
pip install numpy nibabel nilearn matplotlib

# Optional: Advanced templates
pip install templateflow

# Development dependencies
pip install pytest pytest-cov
```

### 2. Set Up Test Data (Optional)

For running tests, you can either:

**Option A: Use your own test data**
```bash
export BRAINVIZ_TEST_DATA_DIR="/path/to/your/test/data"
```

**Option B: Let BrainViz create sample data**
The test suite will automatically create sample NIfTI files if no test data is found.

### 3. Run Tests

```bash
# Basic functionality test
python tests/test_brainviz.py

# Enhanced features test
python tests/test_brainviz_enhanced.py

# Complete test suite (requires pytest)
pytest tests/test_brainviz_complete.py -v

# All features test
python test_all_features.py
```

## Development Installation

### From Source

```bash
git clone <repository-url>
cd brainviz_dk
pip install -e .
```

### With Development Dependencies

```bash
pip install -e ".[dev,templates]"
```

## Testing Without Test Data

If you don't have neuroimaging test data, the package will:

1. **Create sample data**: Automatically generate small test NIfTI files
2. **Skip data-dependent tests**: Use pytest.skip for tests requiring real data
3. **Provide clear instructions**: Show how to set up test data

## Environment Variables

- `BRAINVIZ_TEST_DATA_DIR`: Path to directory containing test NIfTI files
- `BRAINVIZ_LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

## Common Issues

### Issue: "Module not found: brainviz_dk"

**Solution**: Install in development mode:
```bash
pip install -e .
```

### Issue: "No test data available"

**Solution**: Either set the environment variable or let the package create sample data:
```bash
export BRAINVIZ_TEST_DATA_DIR="/path/to/test/data"
# OR
# The package will create sample data automatically
```

### Issue: "TemplateFlow not available"

**Solution**: Install TemplateFlow for advanced templates:
```bash
pip install templateflow
```

## Project Structure

```
brainviz_dk/
├── plot.py              # Core surface plotting
├── volumetric.py        # Volumetric visualization
├── templates.py         # Template management
├── logging_config.py    # Logging configuration
├── test_config.py       # Test configuration
├── __init__.py          # Package initialization
├── __main__.py          # CLI interface
├── tests/               # Test files
├── examples/            # Usage examples
└── docs/               # Documentation
```

## Contributing

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Run tests**: `pytest tests/ -v`
5. **Submit a pull request**

## CLI Usage

```bash
# List available quality presets
python -m brainviz_dk --list-presets

# List available templates
python -m brainviz_dk --list-templates

# Generate all standard views
python -m brainviz_dk --in brain.nii.gz --out plots/ --all-views

# Generate single view with high quality
python -m brainviz_dk --in brain.nii.gz --out plot.svg --view lateral --quality publication
```

## Python API Usage

```python
from brainviz_dk import plot_nifti, generate_four_views

# Single view
plot_nifti("brain.nii.gz", "output.png", hemi="lh", view="lateral")

# Multiple views
generate_four_views("brain.nii.gz", "output_dir/", 
                   hemis=("lh", "rh"), views=("lateral", "medial"))
```

## Logging

The package uses structured logging. Control verbosity with:

```python
from brainviz_dk.logging_config import setup_logging

# Verbose logging
logger = setup_logging(verbose=True)

# Quiet mode
logger = setup_logging(quiet=True)
```

## Performance Tips

- Use `fsaverage5` for faster rendering during development
- Use `fsaverage` for publication-quality output
- Set `BRAINVIZ_LOG_LEVEL=WARNING` to reduce log output
- Use quality presets for consistent output settings

## Troubleshooting

### Memory Issues
- Use `fsaverage5` instead of `fsaverage`
- Reduce DPI for large batch operations
- Process files individually instead of in batches

### Rendering Issues
- Ensure matplotlib backend is set to 'Agg' for headless operation
- Check that NIfTI files are in MNI space
- Verify template data is downloaded (first run downloads ~200MB)

### Import Issues
- Ensure all dependencies are installed
- Check Python version (3.7+ required)
- Verify package is installed correctly: `python -c "import brainviz_dk; print(brainviz_dk.__version__)"`
