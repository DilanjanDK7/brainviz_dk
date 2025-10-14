Contributing
============

We welcome contributions to BrainViz_DK! This guide will help you get started.

Getting Started
---------------

Fork and Clone
~~~~~~~~~~~~~~

1. Fork the repository on GitHub
2. Clone your fork locally:

.. code-block:: bash

   git clone https://github.com/yourusername/brainviz_dk.git
   cd brainviz_dk

Development Setup
~~~~~~~~~~~~~~~~~

Install in development mode with all dependencies:

.. code-block:: bash

   pip install -e ".[dev]"

This installs:

- pytest (testing)
- pytest-cov (coverage)
- sphinx (documentation)
- sphinx_rtd_theme (documentation theme)
- templateflow (optional templates)

Development Workflow
--------------------

1. Create a Branch
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git checkout -b feature/your-feature-name

2. Make Changes
~~~~~~~~~~~~~~~

Edit the code and add tests for new functionality.

3. Run Tests
~~~~~~~~~~~~

.. code-block:: bash

   pytest tests/ -v

Run with coverage:

.. code-block:: bash

   pytest tests/ --cov=brainviz_dk --cov-report=html

4. Build Documentation
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   cd docs
   make html

View documentation:

.. code-block:: bash

   open build/html/index.html  # macOS
   xdg-open build/html/index.html  # Linux

5. Commit Changes
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git add .
   git commit -m "Add: descriptive commit message"

6. Push and Create PR
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git push origin feature/your-feature-name

Then create a Pull Request on GitHub.

Code Style
----------

Python Style
~~~~~~~~~~~~

Follow PEP 8 guidelines:

- 4 spaces for indentation
- 79 characters per line for code
- 72 characters for docstrings
- Use descriptive variable names

Docstring Format
~~~~~~~~~~~~~~~~

Use Google-style docstrings:

.. code-block:: python

   def plot_example(nifti_path, out_path, dpi=300):
       """Plot a brain visualization.

       Args:
           nifti_path (str): Path to input NIfTI file.
           out_path (str): Output file path.
           dpi (int, optional): Output resolution. Defaults to 300.

       Returns:
           str: Path to output file.

       Raises:
           FileNotFoundError: If input file doesn't exist.
           ValueError: If dpi is out of range.

       Example:
           >>> plot_example('brain.nii.gz', 'output.png', dpi=600)
           'output.png'
       """
       pass

Testing
-------

Test Structure
~~~~~~~~~~~~~~

Tests are in the ``tests/`` directory:

.. code-block:: text

   tests/
   ├── test_plot.py          # Surface plotting tests
   ├── test_volumetric.py    # Volumetric plotting tests
   ├── test_templates.py     # Template management tests
   └── conftest.py           # Pytest configuration

Writing Tests
~~~~~~~~~~~~~

Use pytest fixtures and parametrize:

.. code-block:: python

   import pytest
   from brainviz_dk import plot_nifti

   @pytest.fixture
   def sample_nifti(tmp_path):
       """Create a sample NIfTI file."""
       import nibabel as nib
       import numpy as np

       data = np.random.randn(10, 10, 10)
       img = nib.Nifti1Image(data, np.eye(4))
       nifti_path = tmp_path / "sample.nii.gz"
       nib.save(img, nifti_path)
       return str(nifti_path)

   def test_plot_nifti_basic(sample_nifti, tmp_path):
       """Test basic surface plotting."""
       output = tmp_path / "output.png"

       result = plot_nifti(
           sample_nifti,
           str(output),
           hemi='lh',
           view='lateral'
       )

       assert output.exists()
       assert result == str(output)

   @pytest.mark.parametrize("view", ['lateral', 'medial', 'dorsal'])
   def test_plot_multiple_views(sample_nifti, tmp_path, view):
       """Test multiple views."""
       output = tmp_path / f"{view}.png"
       plot_nifti(sample_nifti, str(output), hemi='lh', view=view)
       assert output.exists()

Running Specific Tests
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Run single test file
   pytest tests/test_plot.py -v

   # Run single test
   pytest tests/test_plot.py::test_plot_nifti_basic -v

   # Run tests matching pattern
   pytest tests/ -k "plot" -v

Documentation
-------------

Building Docs
~~~~~~~~~~~~~

.. code-block:: bash

   cd docs
   make html

Documentation uses Sphinx with ReadTheDocs theme.

Adding Documentation
~~~~~~~~~~~~~~~~~~~~

1. Add docstrings to all public functions
2. Create/update RST files in ``docs/source/``
3. Add examples to function docstrings
4. Update API reference if needed

Example Documentation Section
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: rst

   New Feature
   -----------

   Description of the new feature.

   **Example:**

   .. code-block:: python

      from brainviz_dk import new_feature

      result = new_feature('input.nii.gz', param=value)

   **Parameters:**

   - param1 (type): Description
   - param2 (type): Description

   **Returns:**

   - return_value (type): Description

Pull Request Guidelines
-----------------------

Before Submitting
~~~~~~~~~~~~~~~~~

1. ✅ All tests pass
2. ✅ Code follows style guidelines
3. ✅ New features have tests
4. ✅ Documentation is updated
5. ✅ Commit messages are descriptive

PR Description
~~~~~~~~~~~~~~

Include in your PR description:

1. **Purpose**: What does this PR do?
2. **Changes**: What files/functions changed?
3. **Testing**: How was it tested?
4. **Breaking Changes**: Any API changes?

Example:

.. code-block:: text

   ### Purpose
   Add support for custom colormaps in glass brain plots

   ### Changes
   - Modified `plot_glass_brain()` to accept custom colormap parameter
   - Added colormap validation
   - Updated documentation

   ### Testing
   - Added unit tests for colormap validation
   - Tested with 5 different colormaps
   - All existing tests pass

   ### Breaking Changes
   None

Review Process
~~~~~~~~~~~~~~

1. Automated tests run on GitHub Actions
2. Maintainers review code
3. Address feedback
4. Once approved, PR is merged

Types of Contributions
----------------------

Bug Fixes
~~~~~~~~~

Found a bug? Please:

1. Check if it's already reported in Issues
2. Create a new issue with:
   - Description of the bug
   - Steps to reproduce
   - Expected vs. actual behavior
   - System information
3. Submit a PR with fix and test

New Features
~~~~~~~~~~~~

Want to add a feature?

1. Open an issue to discuss the feature
2. Wait for maintainer feedback
3. Implement with tests and documentation
4. Submit PR

Documentation
~~~~~~~~~~~~~

Documentation improvements are always welcome:

- Fix typos
- Add examples
- Clarify explanations
- Add tutorials

Examples
~~~~~~~~

Add example scripts to ``examples/`` directory:

.. code-block:: python

   """
   Example: Generate publication-quality figures
   ============================================

   This example shows how to create high-quality figures.
   """

   from brainviz_dk import plot_nifti, get_quality_preset

   # Generate publication figure
   plot_nifti(
       'activation.nii.gz',
       'figure1.svg',
       hemi='lh',
       view='lateral',
       **get_quality_preset('publication')
   )

Code Review Checklist
---------------------

For Reviewers
~~~~~~~~~~~~~

- [ ] Code is readable and well-documented
- [ ] Tests cover new functionality
- [ ] No breaking changes without discussion
- [ ] Documentation is updated
- [ ] Examples are provided for new features
- [ ] Performance impact is acceptable

For Contributors
~~~~~~~~~~~~~~~~

- [ ] All tests pass locally
- [ ] Documentation builds without errors
- [ ] Code follows project style
- [ ] Commit messages are descriptive
- [ ] PR description is complete

Development Tips
----------------

Debugging Tests
~~~~~~~~~~~~~~~

.. code-block:: bash

   # Run tests with print statements visible
   pytest tests/ -v -s

   # Drop into debugger on failure
   pytest tests/ --pdb

   # Run specific test with debugging
   pytest tests/test_plot.py::test_name -v -s --pdb

Testing with Real Data
~~~~~~~~~~~~~~~~~~~~~~

Use the sample data for testing:

.. code-block:: python

   # Use test data
   SAMPLE_DATA = '/path/to/sample/data.nii.gz'

   def test_with_real_data():
       """Test with actual neuroimaging data."""
       plot_nifti(SAMPLE_DATA, 'output.png', hemi='lh', view='lateral')

Performance Profiling
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import cProfile
   import pstats

   profiler = cProfile.Profile()
   profiler.enable()

   # Your code here
   plot_nifti('brain.nii.gz', 'output.png', hemi='lh', view='lateral')

   profiler.disable()
   stats = pstats.Stats(profiler)
   stats.sort_stats('cumulative')
   stats.print_stats(10)

Questions?
----------

- **General questions**: Open a GitHub Discussion
- **Bug reports**: Open a GitHub Issue
- **Feature requests**: Open a GitHub Issue
- **Security issues**: Email maintainers directly

Thank you for contributing to BrainViz_DK!
