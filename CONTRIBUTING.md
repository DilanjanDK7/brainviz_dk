# Contributing to BrainViz_DK

Thank you for your interest in contributing to BrainViz_DK! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)

## Code of Conduct

This project follows a simple code of conduct:
- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Git
- Basic knowledge of neuroimaging concepts
- Familiarity with numpy, matplotlib, and nilearn

### Finding Issues to Work On

- Check the [issue tracker](https://github.com/dilanjan/brainviz_dk/issues) for open issues
- Look for issues labeled `good first issue` for beginner-friendly tasks
- Issues labeled `help wanted` are great for contributors

## Development Setup

1. **Fork and Clone**
   ```bash
   # Fork the repository on GitHub
   git clone https://github.com/YOUR-USERNAME/brainviz_dk.git
   cd brainviz_dk
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Development Dependencies**
   ```bash
   pip install -e ".[all,dev]"
   ```

4. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-number-description
   ```

## How to Contribute

### Reporting Bugs

When reporting bugs, please include:
- Python version and operating system
- BrainViz_DK version
- Minimal code to reproduce the issue
- Full error traceback
- Expected vs actual behavior

### Suggesting Enhancements

Enhancement suggestions are welcome! Please:
- Check if the feature has already been requested
- Provide clear use cases
- Explain how it fits with the project goals
- Include example usage if possible

### Contributing Code

1. **Make your changes**
   - Follow the coding standards (see below)
   - Add tests for new functionality
   - Update documentation as needed

2. **Test your changes**
   ```bash
   # Run all tests
   pytest tests/ -v

   # Run with coverage
   pytest tests/ --cov=brainviz_dk --cov-report=html

   # Test specific module
   pytest tests/test_plot.py -v
   ```

3. **Commit your changes**
   ```bash
   git add .
   git commit -m "Brief description of changes"
   ```

   Follow these commit message guidelines:
   - Use present tense ("Add feature" not "Added feature")
   - Use imperative mood ("Move cursor to..." not "Moves cursor to...")
   - First line should be 50 characters or less
   - Reference issues and pull requests when relevant

## Coding Standards

### Python Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters
- Use descriptive variable names

### Docstrings

Use NumPy-style docstrings:

```python
def plot_nifti(nifti_path, output_path, hemi='lh', view='lateral'):
    """
    Plot NIfTI data on cortical surface.

    Parameters
    ----------
    nifti_path : str
        Path to input NIfTI file (.nii or .nii.gz).
    output_path : str
        Path for output image file.
    hemi : {'lh', 'rh'}, optional
        Hemisphere to plot. Default is 'lh'.
    view : str, optional
        View angle. Default is 'lateral'.

    Returns
    -------
    str
        Path to saved output file.

    Examples
    --------
    >>> plot_nifti('brain.nii.gz', 'output.png', hemi='lh', view='lateral')
    'output.png'
    """
    pass
```

### Code Organization

- Keep functions focused and single-purpose
- Use meaningful function and variable names
- Add comments for complex logic
- Organize imports: stdlib, third-party, local

### Type Hints

While not required, type hints are encouraged for new code:

```python
from typing import Optional, Tuple

def get_quality_preset(preset_name: str) -> dict:
    """Return quality preset configuration."""
    pass
```

## Testing

### Writing Tests

- Place tests in the `tests/` directory
- Name test files `test_*.py`
- Name test functions `test_*`
- Use descriptive test names that explain what is being tested

Example:

```python
def test_plot_nifti_creates_output_file():
    """Test that plot_nifti creates an output file."""
    # Test implementation
    pass

def test_plot_nifti_with_invalid_hemisphere_raises_error():
    """Test that invalid hemisphere raises ValueError."""
    # Test implementation
    pass
```

### Test Coverage

- Aim for >80% code coverage
- Test both success and failure cases
- Test edge cases and boundary conditions
- Use fixtures for common test data

## Documentation

### Updating Documentation

- Update docstrings for any changed functions
- Update README.md if adding new features
- Update CHANGELOG.md following [Keep a Changelog](https://keepachangelog.com/) format
- Add examples for new features

### Building Documentation

```bash
cd docs
pip install -r requirements.txt
make html
# Open docs/build/html/index.html
```

## Submitting Changes

### Pull Request Process

1. **Update your branch**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create Pull Request**
   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Select your fork and branch
   - Fill out the PR template

### Pull Request Guidelines

- Link related issues (e.g., "Fixes #123")
- Describe what changes were made and why
- Include screenshots for UI changes
- Ensure all tests pass
- Request review from maintainers

### Review Process

- Maintainers will review your PR
- Address any requested changes
- Once approved, a maintainer will merge your PR
- Your contribution will be included in the next release!

## Development Workflow Example

```bash
# 1. Update your local main branch
git checkout main
git pull upstream main

# 2. Create a feature branch
git checkout -b feature/add-new-colormap

# 3. Make changes and test
# ... edit files ...
pytest tests/ -v

# 4. Commit changes
git add .
git commit -m "Add new colormap option for glass brain plots"

# 5. Push to your fork
git push origin feature/add-new-colormap

# 6. Create pull request on GitHub
```

## Questions?

If you have questions:
- Check existing [documentation](https://brainviz-dk.readthedocs.io/)
- Search [existing issues](https://github.com/dilanjan/brainviz_dk/issues)
- Open a new issue with the `question` label
- Email the maintainer: ddiyabal@uwo.ca

## Recognition

Contributors will be recognized in:
- CHANGELOG.md for each release
- README.md contributors section
- GitHub contributors page

Thank you for contributing to BrainViz_DK!
