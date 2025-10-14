Interactive 3D Module
=====================

.. automodule:: brainviz_dk.interactive3d
   :members:
   :undoc-members:
   :show-inheritance:

Overview
--------

The ``interactive3d`` module provides Plotly-based fully interactive 3D brain surface visualizations.
Unlike static views, these visualizations can be rotated to any angle with mouse controls, making them
perfect for exploring dorsal (top-down) views and other perspectives.

Key Features
------------

- **Full 3D Rotation**: Rotate brain to any angle with mouse drag
- **Perfect Dorsal Views**: Easily achieve top-down perspective impossible with static renders
- **High-Quality Meshes**: Support for fsaverage, fsaverage5, fsaverage6, and ICBM152
- **ICBM152 Template**: MNI152NLin2009cAsym support via TemplateFlow
- **Extremely Close Hemispheres**: Both hemispheres positioned 1mm apart (default)
- **Transparency Support**: Adjustable opacity (0.0-1.0) for depth visualization
- **Standalone HTML**: Output works in any browser without Python
- **Customizable Colormaps**: All matplotlib colormaps supported
- **Interactive Controls**: Zoom, pan, and screenshot capture

Main Function
-------------

plot_interactive_surface_plotly
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: brainviz_dk.interactive3d.plot_interactive_surface_plotly

Examples
--------

Basic Usage
^^^^^^^^^^^

.. code-block:: python

   from brainviz_dk import plot_interactive_surface_plotly

   # Create interactive 3D visualization with both hemispheres
   plot_interactive_surface_plotly(
       'activation.nii.gz',
       'brain_3d.html',
       hemi='both',
       mesh='fsaverage5',
       colormap='hot'
   )
   # Open brain_3d.html in browser and rotate with mouse!

Advanced Usage
^^^^^^^^^^^^^^

.. code-block:: python

   # High-resolution with ICBM152 template
   plot_interactive_surface_plotly(
       'tstat.nii.gz',
       'brain_icbm_3d.html',
       hemi='both',
       mesh='MNI152NLin2009cAsym',
       template='MNI152NLin2009cAsym',
       colormap='coolwarm',
       threshold=2.3,
       vmin=-5,
       vmax=5,
       show_colorbar=True
   )

   # Single hemisphere with transparency
   plot_interactive_surface_plotly(
       'activation.nii.gz',
       'brain_transparent.html',
       hemi='lh',
       mesh='fsaverage5',
       opacity=0.7,  # 30% transparent
       colormap='viridis'
   )

   # Custom camera position for initial view
   plot_interactive_surface_plotly(
       'brain.nii.gz',
       'brain_custom_view.html',
       hemi='both',
       initial_camera={
           'eye': {'x': 0, 'y': 0, 'z': 2.5},  # Start zoomed in from top
           'center': {'x': 0, 'y': 0, 'z': 0},
           'up': {'x': 0, 'y': 1, 'z': 0}
       }
   )

Parameters Guide
----------------

Essential Parameters
^^^^^^^^^^^^^^^^^^^^

- ``nifti_path``: Input NIfTI file path
- ``out_html``: Output HTML file path
- ``hemi``: Hemisphere ('lh', 'rh', or 'both')
- ``mesh``: Mesh resolution ('fsaverage5', 'fsaverage', 'fsaverage6', 'MNI152NLin2009cAsym')
- ``template``: Brain template ('fsaverage' or 'MNI152NLin2009cAsym')

Visualization Control
^^^^^^^^^^^^^^^^^^^^^

- ``colormap``: Matplotlib colormap name (default: 'hot')
- ``threshold``: Minimum value to display (values below are transparent)
- ``vmin/vmax``: Colormap range (auto-computed if None)
- ``opacity``: Mesh transparency (0.0=fully transparent, 1.0=fully opaque)
- ``show_colorbar``: Whether to show colorbar (default: True)

Advanced Options
^^^^^^^^^^^^^^^^

- ``radius``: Sampling radius in mm for volume-to-surface projection (default: 2.0)
- ``interpolation``: 'linear' or 'nearest' for surface projection
- ``surface_name``: Surface type ('pial', 'inflated', 'white', 'sphere')
- ``initial_camera``: Dict specifying initial camera position
- ``title``: Custom plot title (default: filename)

Interactive Controls
--------------------

Once you open the HTML file in a browser:

- **Rotate**: Click and drag with left mouse button
- **Zoom**: Scroll wheel or pinch gesture
- **Pan**: Right-click and drag (or Shift + drag)
- **Reset**: Double-click to reset view
- **Screenshot**: Click camera icon in toolbar
- **Fullscreen**: Click expand icon in toolbar

The visualization is fully self-contained in the HTML file and requires no Python or server.

Performance Notes
-----------------

Mesh Resolution vs File Size
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+-------------------+----------------+------------------+-----------------+
| Mesh              | Vertices/Hemi  | Typical File Size | Best For        |
+===================+================+==================+=================+
| fsaverage5        | ~10k           | 2-4 MB           | General use     |
+-------------------+----------------+------------------+-----------------+
| fsaverage6        | ~40k           | 8-15 MB          | High detail     |
+-------------------+----------------+------------------+-----------------+
| fsaverage         | ~163k          | 30-50 MB         | Maximum quality |
+-------------------+----------------+------------------+-----------------+
| MNI152 (32k)      | ~32k           | 6-12 MB          | ICBM template   |
+-------------------+----------------+------------------+-----------------+

**Recommendation**: Use ``fsaverage5`` for most applications - excellent balance of quality and performance.

Hemisphere Spacing
^^^^^^^^^^^^^^^^^^

The default spacing between left and right hemispheres is **1mm** (extremely close). This provides
optimal visualization while keeping both hemispheres clearly separated. Previous versions used 100mm
spacing which was too far apart.

Template Fallback
^^^^^^^^^^^^^^^^^

When using ``template='MNI152NLin2009cAsym'``, the function will:

1. Try to load ICBM152 surfaces from TemplateFlow (requires ``pip install templateflow``)
2. Fall back gracefully to fsaverage if TemplateFlow is not available
3. Log a warning message about the fallback

Tips and Best Practices
------------------------

For Dorsal (Top-Down) Views
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Simply rotate the brain with your mouse after opening the HTML! The interactive viewer makes it
trivial to achieve perfect dorsal views that were difficult with static rendering.

Alternatively, set an initial camera position:

.. code-block:: python

   plot_interactive_surface_plotly(
       'brain.nii.gz',
       'brain_dorsal.html',
       initial_camera={'eye': {'x': 0, 'y': 0, 'z': 2.0}}  # Start from above
   )

For Statistical Maps
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # T-statistic map with proper thresholding
   plot_interactive_surface_plotly(
       't_stat.nii.gz',
       't_stat_3d.html',
       hemi='both',
       threshold=2.3,  # Only show |t| > 2.3
       vmin=-5,
       vmax=5,
       colormap='coolwarm',
       mesh='fsaverage5'
   )

For Presentations
^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Clean visualization without colorbar
   plot_interactive_surface_plotly(
       'activation.nii.gz',
       'presentation.html',
       hemi='both',
       show_colorbar=False,
       colormap='hot',
       title='Activation Map'
   )

For Transparent Overlays
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Semi-transparent for depth perception
   plot_interactive_surface_plotly(
       'activation.nii.gz',
       'transparent.html',
       hemi='both',
       opacity=0.6,  # 40% transparent
       colormap='plasma'
   )

Troubleshooting
---------------

ImportError: plotly not installed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Install plotly: ``pip install plotly``

TemplateFlow not available
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Install for ICBM152 support: ``pip install templateflow``

The function will automatically fall back to fsaverage if TemplateFlow is not installed.

File size too large
^^^^^^^^^^^^^^^^^^^

Use a lower resolution mesh:

- Change from ``mesh='fsaverage'`` to ``mesh='fsaverage5'``
- Reduces file size from ~40MB to ~4MB with minimal quality loss

See Also
--------

- :doc:`../examples/interactive_3d` - Interactive 3D examples
- :doc:`plot` - Static surface plotting
- :doc:`../cli_usage` - CLI usage with ``--plot-type plotly-3d``
