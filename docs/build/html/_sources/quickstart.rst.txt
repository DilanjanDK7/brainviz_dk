Quick Start Guide
=================

This guide will help you get started with BrainViz_DK for common neuroimaging visualization tasks.

Basic Surface Plotting
-----------------------

Single View
~~~~~~~~~~~

Plot a single hemisphere with a specific view:

.. code-block:: python

   from brainviz_dk import plot_nifti

   plot_nifti(
       'my_brain_map.nii.gz',
       'output.png',
       hemi='lh',  # left hemisphere
       view='lateral',
       colormap='hot',
       dpi=300
   )

Multiple Views
~~~~~~~~~~~~~~

Generate multiple standard views:

.. code-block:: python

   from brainviz_dk import generate_four_views

   outputs = generate_four_views(
       'my_brain_map.nii.gz',
       'output_dir/',
       hemis=('lh', 'rh'),  # both hemispheres
       views=('lateral', 'medial', 'dorsal', 'ventral'),
       colormap='hot',
       dpi=600
   )

   print(f"Generated {len(outputs)} plots")

All Standard Views
~~~~~~~~~~~~~~~~~~

Generate all 12 standard neuroimaging views (6 views × 2 hemispheres):

.. code-block:: python

   from brainviz_dk import generate_all_standard_views

   outputs = generate_all_standard_views(
       'my_brain_map.nii.gz',
       'output_dir/',
       mesh='fsaverage',
       colormap='hot',
       dpi=300
   )

Quality Presets
---------------

Use quality presets for common scenarios:

Draft (Fast Preview)
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_nifti, get_quality_preset

   plot_nifti(
       'brain_map.nii.gz',
       'preview.png',
       hemi='lh',
       view='lateral',
       **get_quality_preset('draft')
   )

Publication Quality
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   plot_nifti(
       'brain_map.nii.gz',
       'publication_figure.svg',
       hemi='lh',
       view='lateral',
       **get_quality_preset('publication')
   )

This generates a 600 DPI SVG file with optimal settings for publications.

List Available Presets
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import list_quality_presets

   list_quality_presets()

Volumetric Visualization
-------------------------

Orthogonal Slices
~~~~~~~~~~~~~~~~~

Display 3-plane orthogonal slices:

.. code-block:: python

   from brainviz_dk import plot_volumetric_slices

   plot_volumetric_slices(
       'activation_map.nii.gz',
       'ortho_slices.png',
       template='mni152',
       display_mode='ortho',
       colormap='hot',
       dpi=600
   )

Glass Brain
~~~~~~~~~~~

Create a transparent 3D glass brain visualization:

.. code-block:: python

   from brainviz_dk import plot_glass_brain

   plot_glass_brain(
       'activation_map.nii.gz',
       'glass_brain.png',
       display_mode='ortho',
       colormap='hot',
       black_bg=True,
       dpi=600
   )

Mosaic View
~~~~~~~~~~~

Display multiple slices in a mosaic layout:

.. code-block:: python

   from brainviz_dk import plot_mosaic

   plot_mosaic(
       'brain_map.nii.gz',
       'mosaic.png',
       template='mni152',
       display_mode='z',  # axial slices
       n_slices=20,
       colormap='hot',
       dpi=600
   )

Template Management
-------------------

List Available Templates
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import list_available_templates

   list_available_templates()

Load a Template
~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import get_template

   # Load MNI152 template
   template_img = get_template('mni152', resolution=2)

   # Load brain mask
   mask_img = get_template('mni152_brain_mask', resolution=2)

Command-Line Interface
----------------------

Basic Usage
~~~~~~~~~~~

.. code-block:: bash

   # Single surface plot
   brainviz_dk --in brain.nii.gz --out plot.png \
               --plot-type surface --view lateral --hemi left

   # Multiple views
   brainviz_dk --in brain.nii.gz --out output_dir/ \
               --plot-type surface --views lateral,medial,dorsal

   # All standard views
   brainviz_dk --in brain.nii.gz --out output_dir/ \
               --plot-type surface --all-views

Volumetric Plots
~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Orthogonal slices
   brainviz_dk --in brain.nii.gz --out slices.png \
               --plot-type volume --display-mode ortho

   # Glass brain
   brainviz_dk --in brain.nii.gz --out glass.png \
               --plot-type glass-brain --colormap hot --dpi 600

   # Mosaic
   brainviz_dk --in brain.nii.gz --out mosaic.png \
               --plot-type mosaic --display-mode z --n-slices 20

Quality Control
~~~~~~~~~~~~~~~

.. code-block:: bash

   # Use quality preset
   brainviz_dk --in brain.nii.gz --out plot.svg \
               --plot-type surface --view lateral --hemi left \
               --quality publication

   # Custom high-resolution
   brainviz_dk --in brain.nii.gz --out plot.png \
               --plot-type surface --view lateral --hemi left \
               --dpi 1200 --format png

Utility Commands
~~~~~~~~~~~~~~~~

.. code-block:: bash

   # List quality presets
   brainviz_dk --list-presets

   # List available templates
   brainviz_dk --list-templates

Advanced Examples
-----------------

Custom Figure Size
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   plot_nifti(
       'brain_map.nii.gz',
       'large_plot.png',
       hemi='lh',
       view='lateral',
       figsize=(12, 10),  # 12 inches wide, 10 inches tall
       dpi=600
   )

Threshold and Colormap
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   plot_glass_brain(
       'activation_map.nii.gz',
       'thresholded.png',
       threshold=2.5,  # threshold at z=2.5
       colormap='coolwarm',
       symmetric_cbar=True,
       dpi=600
   )

Batch Processing Multiple Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import glob
   from brainviz_dk import plot_glass_brain

   # Process all NIfTI files in a directory
   nifti_files = glob.glob('results/*.nii.gz')

   for nifti_file in nifti_files:
       output_name = nifti_file.replace('.nii.gz', '_glass.png')
       plot_glass_brain(
           nifti_file,
           output_name,
           colormap='hot',
           dpi=600
       )
       print(f"Processed: {nifti_file}")

ROI Overlay
~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_roi_overlay

   plot_roi_overlay(
       'brain_map.nii.gz',
       'roi_overlay.png',
       template='mni152',
       display_mode='ortho',
       colormap='hot',
       dpi=600
   )

Common Workflows
----------------

Workflow 1: Quality Check
~~~~~~~~~~~~~~~~~~~~~~~~~~

Quick visual inspection of results:

.. code-block:: bash

   # Fast preview
   brainviz_dk --in results.nii.gz --out preview.png \
               --plot-type glass-brain --quality draft

Workflow 2: Publication Figure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

High-quality figure for publication:

.. code-block:: bash

   # Generate high-resolution surface plots
   brainviz_dk --in activation.nii.gz --out figures/ \
               --plot-type surface --all-views --quality publication

   # Generate glass brain for overview
   brainviz_dk --in activation.nii.gz --out glass_brain.svg \
               --plot-type glass-brain --quality publication

Workflow 3: Group Analysis Report
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Generate visualizations for multiple statistical maps:

.. code-block:: python

   from brainviz_dk import plot_glass_brain, plot_volumetric_slices

   maps = ['group_t.nii.gz', 'group_mean.nii.gz', 'group_std.nii.gz']

   for map_file in maps:
       basename = map_file.replace('.nii.gz', '')

       # Glass brain
       plot_glass_brain(
           map_file,
           f'{basename}_glass.png',
           colormap='hot',
           dpi=600
       )

       # Orthogonal slices
       plot_volumetric_slices(
           map_file,
           f'{basename}_slices.png',
           display_mode='ortho',
           colormap='hot',
           dpi=600
       )

Next Steps
----------

- :doc:`cli_usage` - Comprehensive CLI documentation
- :doc:`quality_presets` - Detailed quality preset guide
- :doc:`templates` - Template system documentation
- :doc:`api/plot` - Full API reference
