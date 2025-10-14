Interactive 3D Examples
=======================

This guide demonstrates the Plotly-based interactive 3D visualization capabilities of BrainViz_DK.

Overview
--------

The Plotly 3D viewer provides fully rotatable, high-quality 3D brain surface visualizations that can be
viewed from any angle. This is particularly useful for:

- Achieving perfect **dorsal (top-down) views** impossible with static rendering
- Exploring activation patterns from multiple perspectives
- Creating **presentation-ready** interactive HTML files
- Sharing visualizations that don't require Python

All outputs are standalone HTML files that work in any modern web browser.

Basic Examples
--------------

Simple Interactive Visualization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from brainviz_dk import plot_interactive_surface_plotly

   # Create basic interactive 3D plot
   plot_interactive_surface_plotly(
       'activation.nii.gz',
       'brain_3d.html',
       hemi='both',           # Show both hemispheres
       mesh='fsaverage5',     # Good quality, reasonable file size
       colormap='hot'
   )

   # Open brain_3d.html in your browser
   # Drag with mouse to rotate to any angle!

Left Hemisphere Only
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Single hemisphere for focused visualization
   plot_interactive_surface_plotly(
       'activation.nii.gz',
       'left_hemisphere.html',
       hemi='lh',
       mesh='fsaverage5',
       colormap='viridis'
   )

Advanced Examples
-----------------

High-Quality ICBM152 Template
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Use ICBM152/MNI152NLin2009cAsym template (requires templateflow)
   plot_interactive_surface_plotly(
       'group_tstat.nii.gz',
       'icbm152_3d.html',
       hemi='both',
       mesh='MNI152NLin2009cAsym',
       template='MNI152NLin2009cAsym',
       colormap='coolwarm',
       threshold=2.3,
       vmin=-5,
       vmax=5
   )

Statistical Maps with Thresholding
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # T-statistic map with proper statistical thresholding
   plot_interactive_surface_plotly(
       't_stat.nii.gz',
       't_stat_thresholded.html',
       hemi='both',
       mesh='fsaverage5',
       colormap='coolwarm',
       threshold=2.3,        # Only show |t| > 2.3
       vmin=-5,              # Symmetric colormap
       vmax=5,
       show_colorbar=True
   )

Transparent Overlays
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Semi-transparent for better depth perception
   plot_interactive_surface_plotly(
       'activation.nii.gz',
       'transparent_brain.html',
       hemi='both',
       opacity=0.7,          # 70% opaque (30% transparent)
       colormap='plasma',
       mesh='fsaverage5'
   )

   # Very transparent to see internal structure
   plot_interactive_surface_plotly(
       'activation.nii.gz',
       'very_transparent.html',
       hemi='both',
       opacity=0.4,          # 40% opaque
       colormap='hot'
   )

Custom Initial Camera Position
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Start with dorsal (top-down) view
   plot_interactive_surface_plotly(
       'brain.nii.gz',
       'dorsal_start.html',
       hemi='both',
       initial_camera={
           'eye': {'x': 0, 'y': 0, 'z': 2.0},    # View from above
           'center': {'x': 0, 'y': 0, 'z': 0},
           'up': {'x': 0, 'y': 1, 'z': 0}
       }
   )

   # Start zoomed in from the side
   plot_interactive_surface_plotly(
       'brain.nii.gz',
       'lateral_zoom.html',
       hemi='both',
       initial_camera={
           'eye': {'x': 1.5, 'y': 0, 'z': 0},    # From the side, close up
       }
   )

Presentation-Ready Output
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Clean visualization without colorbar for presentations
   plot_interactive_surface_plotly(
       'activation.nii.gz',
       'presentation.html',
       hemi='both',
       mesh='fsaverage5',
       colormap='hot',
       show_colorbar=False,  # Hide colorbar for cleaner look
       title='Motor Cortex Activation'
   )

Batch Processing
----------------

Process Multiple Files
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   import glob
   import os
   from brainviz_dk import plot_interactive_surface_plotly

   # Process all NIfTI files in a directory
   output_dir = 'interactive_3d_outputs/'
   os.makedirs(output_dir, exist_ok=True)

   for nifti_file in glob.glob('results/*.nii.gz'):
       basename = os.path.basename(nifti_file).replace('.nii.gz', '')

       plot_interactive_surface_plotly(
           nifti_file,
           f'{output_dir}/{basename}_3d.html',
           hemi='both',
           mesh='fsaverage5',
           colormap='hot'
       )

       print(f'✓ Created {basename}_3d.html')

Multiple Colormaps
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Compare different colormaps
   colormaps = ['hot', 'viridis', 'plasma', 'coolwarm']

   for cmap in colormaps:
       plot_interactive_surface_plotly(
           'activation.nii.gz',
           f'brain_{cmap}.html',
           hemi='both',
           colormap=cmap,
           mesh='fsaverage5'
       )

Different Mesh Resolutions
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Compare quality vs file size
   meshes = {
       'fsaverage5': 'Good balance (2-4 MB)',
       'fsaverage6': 'High detail (8-15 MB)',
       'fsaverage': 'Maximum quality (30-50 MB)'
   }

   for mesh, description in meshes.items():
       output_file = f'brain_{mesh}.html'

       plot_interactive_surface_plotly(
           'activation.nii.gz',
           output_file,
           hemi='both',
           mesh=mesh,
           colormap='hot'
       )

       size_mb = os.path.getsize(output_file) / (1024**2)
       print(f'{mesh:15s} ({description}): {size_mb:.2f} MB')

Use Case Examples
-----------------

For fMRI Activation Maps
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Standard fMRI activation visualization
   plot_interactive_surface_plotly(
       'task_activation.nii.gz',
       'fmri_activation_3d.html',
       hemi='both',
       mesh='fsaverage5',
       colormap='hot',
       threshold=3.1,        # Z > 3.1 (p < 0.001)
       vmin=0,
       vmax=8,
       title='Task vs Rest Activation'
   )

For Group Statistical Maps
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Group t-statistic with bidirectional colormap
   plot_interactive_surface_plotly(
       'group_tstat.nii.gz',
       'group_stats_3d.html',
       hemi='both',
       mesh='fsaverage5',
       colormap='coolwarm',
       threshold=2.3,        # Two-tailed t-test threshold
       vmin=-5,
       vmax=5,
       title='Group Analysis (N=30, p<0.05 FWE)'
   )

For Connectivity Maps
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Seed-based connectivity
   plot_interactive_surface_plotly(
       'connectivity_map.nii.gz',
       'connectivity_3d.html',
       hemi='both',
       mesh='fsaverage5',
       colormap='bwr',       # Blue-white-red
       threshold=0.3,        # r > 0.3
       vmin=-1,
       vmax=1,
       title='PCC Seed Connectivity'
   )

For Morphometry (VBM, Cortical Thickness)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Cortical thickness differences
   plot_interactive_surface_plotly(
       'thickness_tstat.nii.gz',
       'thickness_3d.html',
       hemi='both',
       mesh='fsaverage',     # High resolution for anatomical detail
       colormap='RdYlBu_r',  # Red-Yellow-Blue reversed
       threshold=2.0,
       title='Cortical Thickness: Patients > Controls'
   )

Command-Line Usage
------------------

You can also create Plotly 3D visualizations from the command line:

Basic Command
^^^^^^^^^^^^^

.. code-block:: bash

   # Simple interactive 3D
   brainviz_dk --in activation.nii.gz --out brain_3d.html --plot-type plotly-3d

With Custom Options
^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Custom mesh and colormap
   brainviz_dk --in brain.nii.gz --out output.html --plot-type plotly-3d \
               --plotly-mesh fsaverage --colormap viridis

ICBM152 Template
^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Use ICBM152 template
   brainviz_dk --in brain.nii.gz --out icbm_3d.html --plot-type plotly-3d \
               --plotly-template MNI152NLin2009cAsym \
               --plotly-mesh MNI152NLin2009cAsym

With Transparency
^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # 70% opaque (30% transparent)
   brainviz_dk --in activation.nii.gz --out transparent.html --plot-type plotly-3d \
               --opacity 0.7 --colormap plasma

Single Hemisphere
^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Left hemisphere only
   brainviz_dk --in brain.nii.gz --out left_3d.html --plot-type plotly-3d \
               --hemi left

Interactive Controls Guide
---------------------------

Once you open the HTML file in a browser, you can interact with the visualization:

Mouse Controls
^^^^^^^^^^^^^^

- **Rotate**: Click and drag with left mouse button
- **Zoom**: Scroll wheel (or pinch on touchpad)
- **Pan**: Right-click and drag (or Shift + left-click drag)
- **Reset View**: Double-click anywhere

Toolbar Actions
^^^^^^^^^^^^^^^

- **Camera Icon**: Save screenshot as PNG
- **Zoom Icons**: Zoom in/out
- **Pan Icon**: Pan mode
- **Box/Lasso**: Not applicable for 3D mesh (can be ignored)
- **Reset Axes**: Return to initial camera position
- **Expand Icon**: Toggle fullscreen mode

Achieving Perfect Dorsal View
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Open the HTML file in your browser
2. Click and drag to rotate the brain upward
3. Continue rotating until you see the top of the brain straight on
4. Fine-tune with small mouse movements
5. Zoom as needed for perfect framing

Tips: The default 1mm hemisphere spacing makes both hemispheres clearly visible from dorsal view!

Performance Tips
----------------

Optimize File Size
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Use fsaverage5 instead of fsaverage for 10x smaller files
   plot_interactive_surface_plotly(
       'brain.nii.gz',
       'optimized.html',
       mesh='fsaverage5'    # 2-4 MB instead of 30-50 MB
   )

Sharing HTML Files
^^^^^^^^^^^^^^^^^^

The output HTML files are completely self-contained and can be:

- Emailed to collaborators
- Uploaded to websites
- Included in supplementary materials
- Opened on any device with a browser (no Python needed!)

Loading Speed
^^^^^^^^^^^^^

For presentations, pre-load the HTML file before presenting:

1. Open the HTML file a few seconds before showing
2. Wait for the mesh to fully render
3. Then switch to full screen for presentation

Troubleshooting
---------------

HTML file won't open
^^^^^^^^^^^^^^^^^^^^

- Make sure you're using a modern browser (Chrome, Firefox, Safari, Edge)
- Some old browsers don't support WebGL required for 3D rendering

File size too large
^^^^^^^^^^^^^^^^^^^

- Use ``mesh='fsaverage5'`` instead of ``'fsaverage'``
- Consider showing only one hemisphere with ``hemi='lh'``

Mesh appears gray/blank
^^^^^^^^^^^^^^^^^^^^^^^^

- Check that your NIfTI file has data in the correct space
- Try adjusting ``threshold``, ``vmin``, and ``vmax`` parameters
- Verify the data range with ``nibabel`` or ``fslinfo``

Slow rendering
^^^^^^^^^^^^^^

- Use lower resolution mesh (``fsaverage5`` or ``fsaverage6``)
- Close other browser tabs to free up memory
- Try a different browser (Chrome often has best WebGL performance)

See Also
--------

- :doc:`../api/interactive3d` - Full API reference
- :doc:`surface_plotting` - Static surface plotting examples
- :doc:`../cli_usage` - CLI usage guide
- :doc:`quality_comparison` - Quality preset comparisons
