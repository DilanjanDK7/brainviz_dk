Installation
============

Requirements
------------

BrainViz_DK requires Python 3.8 or higher.

**Core Dependencies:**

- numpy >= 1.19.0
- nibabel >= 3.0.0
- nilearn >= 0.9.0
- matplotlib >= 3.3.0

**Optional Dependencies:**

- templateflow >= 0.8.0 (for ICBM152NLin2009cAsym templates)

Installation Methods
--------------------

From PyPI (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install brainviz_dk

From Source
~~~~~~~~~~~

To install the latest development version:

.. code-block:: bash

   git clone https://github.com/yourusername/brainviz_dk.git
   cd brainviz_dk
   pip install -e .

Development Installation
~~~~~~~~~~~~~~~~~~~~~~~~

For development work, install with additional dependencies:

.. code-block:: bash

   git clone https://github.com/yourusername/brainviz_dk.git
   cd brainviz_dk
   pip install -e ".[dev]"

This installs testing and documentation dependencies:

- pytest
- pytest-cov
- sphinx
- sphinx_rtd_theme

Optional: TemplateFlow Setup
-----------------------------

For enhanced template support (ICBM152NLin2009cAsym), install TemplateFlow:

.. code-block:: bash

   pip install templateflow

First-time use will automatically download required templates (~200 MB).

Verifying Installation
----------------------

Test your installation:

.. code-block:: bash

   # Check version
   python -c "import brainviz_dk; print(brainviz_dk.__version__)"

   # List available quality presets
   brainviz_dk --list-presets

   # List available templates
   brainviz_dk --list-templates

Expected output:

.. code-block:: text

   Available Quality Presets:

   draft: Fast preview quality
     • DPI: 150
     • Mesh: fsaverage5
     • Format: png

   standard: Standard quality for general use
     • DPI: 300
     • Mesh: fsaverage
     • Format: png

   publication: High quality for publications (vector format)
     • DPI: 600
     • Mesh: fsaverage
     • Format: svg

   print: Very high quality for print (large files)
     • DPI: 1200
     • Mesh: fsaverage
     • Format: pdf

Troubleshooting
---------------

Missing Dependencies
~~~~~~~~~~~~~~~~~~~~

If you encounter import errors, ensure all dependencies are installed:

.. code-block:: bash

   pip install --upgrade numpy nibabel nilearn matplotlib

Template Download Issues
~~~~~~~~~~~~~~~~~~~~~~~~

If TemplateFlow fails to download templates:

.. code-block:: python

   import templateflow.api as tflow

   # Manually trigger download
   template = tflow.get('MNI152NLin2009cAsym', resolution=2)

Set custom cache directory:

.. code-block:: bash

   export TEMPLATEFLOW_HOME=/path/to/templates

Memory Issues
~~~~~~~~~~~~~

For large datasets or high-resolution outputs, you may need to increase available memory:

.. code-block:: bash

   # Limit parallelism
   export OMP_NUM_THREADS=1
   export MKL_NUM_THREADS=1

Platform-Specific Notes
-----------------------

macOS
~~~~~

You may need to install additional system dependencies:

.. code-block:: bash

   brew install freetype libpng

Linux
~~~~~

Install system dependencies:

.. code-block:: bash

   # Ubuntu/Debian
   sudo apt-get install python3-dev libfreetype6-dev libpng-dev

   # CentOS/RHEL
   sudo yum install python3-devel freetype-devel libpng-devel

Windows
~~~~~~~

Windows users should install via Anaconda for best compatibility:

.. code-block:: bash

   conda create -n brainviz python=3.10
   conda activate brainviz
   pip install brainviz_dk

Next Steps
----------

- :doc:`quickstart` - Get started with basic examples
- :doc:`cli_usage` - Learn the command-line interface
- :doc:`api/plot` - Explore the Python API
