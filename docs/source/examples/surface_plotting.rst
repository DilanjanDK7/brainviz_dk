Surface Plotting Examples
=========================

This page provides comprehensive examples for surface plotting with BrainViz_DK.

Basic Examples
--------------

Single Hemisphere, Single View
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_nifti

   plot_nifti(
       'activation.nii.gz',
       'lateral_left.png',
       hemi='lh',
       view='lateral',
       colormap='hot',
       dpi=300
   )

Both Hemispheres
~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import generate_four_views

   outputs = generate_four_views(
       'activation.nii.gz',
       'output_dir/',
       hemis=('lh', 'rh'),
       views=('lateral',),
       colormap='hot',
       dpi=600
   )

   # Generates: lateral_lh.png, lateral_rh.png

All Standard Views
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import generate_all_standard_views

   outputs = generate_all_standard_views(
       'activation.nii.gz',
       'output_dir/',
       colormap='hot',
       dpi=600
   )

   # Generates 12 images:
   # lateral_lh.png, lateral_rh.png
   # medial_lh.png, medial_rh.png
   # dorsal_lh.png, dorsal_rh.png
   # ventral_lh.png, ventral_rh.png
   # anterior_lh.png, anterior_rh.png
   # posterior_lh.png, posterior_rh.png

Quality Settings
----------------

Draft Quality (Fast Preview)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_nifti, get_quality_preset

   plot_nifti(
       'brain.nii.gz',
       'draft.png',
       hemi='lh',
       view='lateral',
       **get_quality_preset('draft')
   )

   # Settings: 150 DPI, PNG, fsaverage5, ~2 seconds

Publication Quality
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_nifti, get_quality_preset

   plot_nifti(
       'activation.nii.gz',
       'figure1.svg',
       hemi='lh',
       view='lateral',
       **get_quality_preset('publication')
   )

   # Settings: 600 DPI, SVG (vector), fsaverage, ~10 seconds

Custom Quality
~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_nifti

   plot_nifti(
       'brain.nii.gz',
       'custom.png',
       hemi='lh',
       view='lateral',
       dpi=900,
       figsize=(12, 10),
       mesh='fsaverage6',
       interpolation='cubic'
   )

Surface Types
-------------

Pial Surface (Default)
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   plot_nifti(
       'brain.nii.gz',
       'pial.png',
       hemi='lh',
       view='lateral',
       surface_name='pial'  # Outer cortical surface
   )

Inflated Surface
~~~~~~~~~~~~~~~~

.. code-block:: python

   plot_nifti(
       'brain.nii.gz',
       'inflated.png',
       hemi='lh',
       view='lateral',
       surface_name='inflated'  # Reduces sulcal/gyral complexity
   )

White Matter Surface
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   plot_nifti(
       'brain.nii.gz',
       'white.png',
       hemi='lh',
       view='lateral',
       surface_name='white'  # Inner cortical surface
   )

Colormap Examples
-----------------

Hot Colormap
~~~~~~~~~~~~

.. code-block:: python

   plot_nifti(
       'activation.nii.gz',
       'hot.png',
       hemi='lh',
       view='lateral',
       colormap='hot'  # Classic hot colormap
   )

Coolwarm Colormap
~~~~~~~~~~~~~~~~~

.. code-block:: python

   plot_nifti(
       't_stat.nii.gz',
       'coolwarm.png',
       hemi='lh',
       view='lateral',
       colormap='coolwarm'  # Good for t-statistics
   )

Custom Colormaps
~~~~~~~~~~~~~~~~

.. code-block:: python

   # Viridis (perceptually uniform)
   plot_nifti('brain.nii.gz', 'viridis.png', hemi='lh', view='lateral', colormap='viridis')

   # Plasma
   plot_nifti('brain.nii.gz', 'plasma.png', hemi='lh', view='lateral', colormap='plasma')

   # Red-Blue diverging
   plot_nifti('brain.nii.gz', 'rdbu.png', hemi='lh', view='lateral', colormap='RdBu_r')

Advanced Styling
----------------

Custom Alpha and Darkness
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   plot_nifti(
       'activation.nii.gz',
       'styled.png',
       hemi='lh',
       view='lateral',
       alpha=0.9,  # Overlay transparency (0-1)
       darkness=0.6,  # Background brightness (0-1, lower = brighter)
       colormap='hot'
   )

Custom Radius
~~~~~~~~~~~~~

.. code-block:: python

   plot_nifti(
       'activation.nii.gz',
       'sharp.png',
       hemi='lh',
       view='lateral',
       radius=1.0,  # Smaller = sharper, larger = smoother
       colormap='hot'
   )

With Smoothing
~~~~~~~~~~~~~~

.. code-block:: python

   plot_nifti(
       'noisy_data.nii.gz',
       'smoothed.png',
       hemi='lh',
       view='lateral',
       smooth_fwhm=3.0,  # 3mm FWHM Gaussian smoothing
       colormap='hot'
   )

Batch Processing
----------------

Process Multiple Files
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_nifti, get_quality_preset
   import glob

   preset = get_quality_preset('publication')

   for nifti_file in glob.glob('results/*.nii.gz'):
       basename = os.path.basename(nifti_file).replace('.nii.gz', '')
       output = f'figures/{basename}_lateral_lh.svg'

       plot_nifti(
           nifti_file,
           output,
           hemi='lh',
           view='lateral',
           **preset
       )

       print(f"Processed: {basename}")

Generate All Views for Multiple Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import generate_all_standard_views
   import glob

   for nifti_file in glob.glob('results/*.nii.gz'):
       basename = os.path.basename(nifti_file).replace('.nii.gz', '')
       output_dir = f'figures/{basename}/'

       outputs = generate_all_standard_views(
           nifti_file,
           output_dir,
           colormap='hot',
           dpi=600,
           prefix=basename
       )

       print(f"Generated {len(outputs)} views for {basename}")

Custom View Combinations
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import generate_four_views

   # Custom view set
   custom_views = ('lateral', 'medial', 'dorsal')

   for nifti_file in glob.glob('*.nii.gz'):
       generate_four_views(
           nifti_file,
           'output/',
           hemis=('lh', 'rh'),
           views=custom_views,
           dpi=600
       )

Publication Workflows
---------------------

Single Figure for Paper
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_nifti, get_quality_preset

   # High-quality vector figure
   plot_nifti(
       'main_result.nii.gz',
       'manuscript/figure1_activation.svg',
       hemi='lh',
       view='lateral',
       **get_quality_preset('publication')
   )

Multi-Panel Figure
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import generate_four_views, get_quality_preset

   # Generate 4 views for multi-panel figure
   views = ('lateral', 'medial', 'dorsal', 'ventral')

   outputs = generate_four_views(
       'activation.nii.gz',
       'manuscript/',
       hemis=('lh',),
       views=views,
       prefix='fig1',
       **get_quality_preset('publication')
   )

   # Results in:
   # fig1_lateral_lh.svg
   # fig1_medial_lh.svg
   # fig1_dorsal_lh.svg
   # fig1_ventral_lh.svg

   # Combine in graphics software (Inkscape, Illustrator, etc.)

Supplementary Materials
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import generate_all_standard_views

   # Generate all views for supplementary figures
   subjects = ['sub-01', 'sub-02', 'sub-03']

   for subject in subjects:
       nifti_file = f'results/{subject}_activation.nii.gz'
       output_dir = f'supplementary/{subject}/'

       generate_all_standard_views(
           nifti_file,
           output_dir,
           prefix=subject,
           dpi=300,  # Standard quality for supplementary
           colormap='hot'
       )

Interactive 3D
--------------

Generate Interactive HTML
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_3d_interactive

   view = plot_3d_interactive(
       'activation.nii.gz',
       colormap='hot',
       threshold=2.0
   )

   # Save to HTML file
   view.save_as_html('brain_3d.html')

   # Open in browser to interact

With Custom Threshold
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_3d_interactive

   # Only show strong activations
   view = plot_3d_interactive(
       't_stat.nii.gz',
       colormap='hot',
       threshold=3.0  # Only show t > 3.0
   )

   view.save_as_html('significant_activation.html')

Complete Example Script
-----------------------

Full Analysis Pipeline
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   #!/usr/bin/env python3
   """
   Complete surface visualization pipeline.
   """

   from brainviz_dk import (
       plot_nifti,
       generate_all_standard_views,
       plot_3d_interactive,
       get_quality_preset
   )
   import os

   # Configuration
   INPUT_FILE = 'group_activation.nii.gz'
   OUTPUT_DIR = 'visualizations/'
   os.makedirs(OUTPUT_DIR, exist_ok=True)

   # 1. Quick preview (draft quality)
   print("1. Generating quick preview...")
   plot_nifti(
       INPUT_FILE,
       f'{OUTPUT_DIR}/preview_lateral.png',
       hemi='lh',
       view='lateral',
       **get_quality_preset('draft')
   )

   # 2. High-quality main figure (publication)
   print("2. Generating publication figure...")
   plot_nifti(
       INPUT_FILE,
       f'{OUTPUT_DIR}/figure1_lateral_lh.svg',
       hemi='lh',
       view='lateral',
       **get_quality_preset('publication')
   )

   # 3. All standard views (supplementary)
   print("3. Generating all standard views...")
   outputs = generate_all_standard_views(
       INPUT_FILE,
       f'{OUTPUT_DIR}/all_views/',
       colormap='hot',
       dpi=600
   )
   print(f"   Generated {len(outputs)} views")

   # 4. Interactive 3D
   print("4. Generating interactive 3D...")
   view = plot_3d_interactive(
       INPUT_FILE,
       colormap='hot',
       threshold=2.0
   )
   view.save_as_html(f'{OUTPUT_DIR}/interactive_3d.html')

   print("✓ Pipeline complete!")
   print(f"   Outputs in: {OUTPUT_DIR}")

See Also
--------

- :doc:`volumetric_plotting` - Volumetric visualization examples
- :doc:`../api/plot` - Surface plotting API reference
- :doc:`../quality_presets` - Quality preset details
