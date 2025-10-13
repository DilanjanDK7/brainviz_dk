.. BrainViz_DK documentation master file

BrainViz_DK Documentation
=========================

**BrainViz_DK** is a comprehensive neuroimaging visualization toolkit that provides high-quality brain plotting capabilities for both surface and volumetric data.

.. image:: https://img.shields.io/badge/python-3.8%2B-blue.svg
   :target: https://www.python.org/downloads/
   :alt: Python Version

.. image:: https://img.shields.io/badge/license-MIT-green.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License

Features
--------

**Surface Plotting**
   - High-resolution cortical surface visualization
   - Multiple viewing angles (lateral, medial, dorsal, ventral, anterior, posterior)
   - fsaverage mesh support (fsaverage, fsaverage5, fsaverage6)
   - Publication-quality output (up to 2400 DPI)
   - Vector formats (SVG, PDF, EPS) for infinite scalability

**Volumetric Rendering**
   - Orthogonal slice views (3-plane visualization)
   - Glass brain visualization (transparent 3D)
   - Mosaic displays (multi-slice views)
   - ROI/parcellation overlays
   - MNI152 template integration

**Quality & Output**
   - Quality presets (draft, standard, publication, print)
   - Multiple output formats (PNG, SVG, PDF, EPS)
   - Configurable DPI (1-2400)
   - Custom figure sizes
   - Colormap support

**Template Management**
   - MNI152 templates (T1w, brain mask, GM/WM masks)
   - TemplateFlow integration (ICBM152NLin2009cAsym)
   - Unified template access system

Quick Start
-----------

Install BrainViz_DK:

.. code-block:: bash

   pip install brainviz_dk

Generate a quick surface plot:

.. code-block:: python

   from brainviz_dk import plot_nifti

   plot_nifti(
       'brain_map.nii.gz',
       'output.png',
       hemi='lh',
       view='lateral',
       quality_preset='publication'
   )

Generate a glass brain visualization:

.. code-block:: python

   from brainviz_dk import plot_glass_brain

   plot_glass_brain(
       'activation_map.nii.gz',
       'glass_brain.png',
       colormap='hot',
       dpi=600
   )

Command-Line Interface
----------------------

BrainViz_DK provides a comprehensive CLI:

.. code-block:: bash

   # Surface plotting with all standard views
   brainviz_dk --in brain.nii.gz --out plots/ --plot-type surface --all-views

   # Volumetric slices
   brainviz_dk --in brain.nii.gz --out slices.png --plot-type volume \
               --display-mode ortho --template mni152

   # Glass brain
   brainviz_dk --in brain.nii.gz --out glass.png --plot-type glass-brain \
               --dpi 600 --colormap hot

   # High-quality publication output
   brainviz_dk --in brain.nii.gz --out plot.svg --plot-type surface \
               --view lateral --hemi left --quality publication

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   installation
   quickstart
   cli_usage
   quality_presets
   templates

.. toctree::
   :maxdepth: 2
   :caption: Examples

   examples/surface_plotting
   examples/volumetric_plotting
   examples/batch_processing
   examples/quality_comparison

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/plot
   api/volumetric
   api/templates

.. toctree::
   :maxdepth: 1
   :caption: Development

   contributing
   changelog

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
