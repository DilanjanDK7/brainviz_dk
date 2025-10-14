Volumetric Plotting Examples
============================

Comprehensive examples for volumetric brain visualization with BrainViz_DK.

Basic Examples
--------------

Orthogonal Slices (3-Plane View)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_volumetric_slices

   plot_volumetric_slices(
       'activation.nii.gz',
       'ortho_slices.png',
       template='mni152',
       display_mode='ortho',
       colormap='hot',
       dpi=600
   )

Glass Brain
~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_glass_brain

   plot_glass_brain(
       'activation.nii.gz',
       'glass_brain.png',
       display_mode='ortho',
       colormap='hot',
       dpi=600
   )

Mosaic View
~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_mosaic

   plot_mosaic(
       'brain.nii.gz',
       'mosaic.png',
       template='mni152',
       display_mode='z',  # Axial slices
       n_slices=20,
       colormap='hot',
       dpi=600
   )

Display Modes
-------------

Axial Slices
~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_volumetric_slices

   plot_volumetric_slices(
       'brain.nii.gz',
       'axial.png',
       display_mode='z',
       cut_coords=7,  # 7 slices
       colormap='hot',
       dpi=600
   )

Sagittal Slices
~~~~~~~~~~~~~~~

.. code-block:: python

   plot_volumetric_slices(
       'brain.nii.gz',
       'sagittal.png',
       display_mode='x',
       cut_coords=5,
       colormap='hot',
       dpi=600
   )

Coronal Slices
~~~~~~~~~~~~~~

.. code-block:: python

   plot_volumetric_slices(
       'brain.nii.gz',
       'coronal.png',
       display_mode='y',
       cut_coords=7,
       colormap='hot',
       dpi=600
   )

Two-Plane Combinations
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Axial + Sagittal
   plot_volumetric_slices('brain.nii.gz', 'xz.png', display_mode='xz', dpi=600)

   # Axial + Coronal
   plot_volumetric_slices('brain.nii.gz', 'yz.png', display_mode='yz', dpi=600)

   # Coronal + Sagittal
   plot_volumetric_slices('brain.nii.gz', 'yx.png', display_mode='yx', dpi=600)

Glass Brain Variations
----------------------

Standard Glass Brain
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_glass_brain

   plot_glass_brain(
       'activation.nii.gz',
       'glass_standard.png',
       display_mode='ortho',
       colormap='hot',
       dpi=600
   )

Black Background
~~~~~~~~~~~~~~~~

.. code-block:: python

   plot_glass_brain(
       'activation.nii.gz',
       'glass_black.png',
       display_mode='ortho',
       colormap='hot',
       black_bg=True,  # Black background
       dpi=600
   )

Single Plane Glass Brain
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Sagittal only
   plot_glass_brain('brain.nii.gz', 'glass_x.png', display_mode='x', colormap='hot', dpi=600)

   # Coronal only
   plot_glass_brain('brain.nii.gz', 'glass_y.png', display_mode='y', colormap='hot', dpi=600)

   # Axial only
   plot_glass_brain('brain.nii.gz', 'glass_z.png', display_mode='z', colormap='hot', dpi=600)

Left/Right Hemisphere Glass Brain
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   plot_glass_brain(
       'brain.nii.gz',
       'glass_lr.png',
       display_mode='lr',  # Left and right separated
       colormap='hot',
       dpi=600
   )

Mosaic Displays
---------------

Axial Mosaic (20 Slices)
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_mosaic

   plot_mosaic(
       'brain.nii.gz',
       'mosaic_axial.png',
       display_mode='z',
       n_slices=20,
       colormap='hot',
       dpi=600
   )

Sagittal Mosaic
~~~~~~~~~~~~~~~

.. code-block:: python

   plot_mosaic(
       'brain.nii.gz',
       'mosaic_sagittal.png',
       display_mode='x',
       n_slices=15,
       colormap='hot',
       dpi=600
   )

Coronal Mosaic
~~~~~~~~~~~~~~

.. code-block:: python

   plot_mosaic(
       'brain.nii.gz',
       'mosaic_coronal.png',
       display_mode='y',
       n_slices=18,
       colormap='hot',
       dpi=600
   )

Statistical Maps
----------------

T-Statistic Map with Threshold
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_glass_brain

   plot_glass_brain(
       't_stat.nii.gz',
       'tstat_thresholded.png',
       threshold=2.3,  # t > 2.3 (p < 0.05 two-tailed)
       colormap='coolwarm',
       symmetric_cbar=True,  # Symmetric around zero
       vmin=-5,
       vmax=5,
       dpi=600
   )

Positive Activations Only
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   plot_glass_brain(
       'activation.nii.gz',
       'positive_only.png',
       threshold=2.0,  # Only show positive values > 2
       colormap='hot',
       vmin=0,
       vmax=10,
       dpi=600
   )

Correlation Map
~~~~~~~~~~~~~~~

.. code-block:: python

   plot_volumetric_slices(
       'correlation_map.nii.gz',
       'correlation.png',
       display_mode='ortho',
       colormap='RdBu_r',  # Red-Blue diverging
       symmetric_cbar=True,
       vmin=-1,
       vmax=1,
       dpi=600
   )

ROI Visualization
-----------------

ROI Overlay
~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_roi_overlay

   plot_roi_overlay(
       'atlas.nii.gz',
       'roi_overlay.png',
       template='mni152',
       display_mode='ortho',
       colormap='tab20',  # Categorical colormap
       dpi=600
   )

Parcellation Atlas
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   plot_roi_overlay(
       'parcellation.nii.gz',
       'parcellation.png',
       display_mode='ortho',
       colormap='Set3',
       dpi=600
   )

Template Options
----------------

Default MNI152
~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_volumetric_slices

   plot_volumetric_slices(
       'brain.nii.gz',
       'mni152.png',
       template='mni152',  # Default
       display_mode='ortho',
       dpi=600
   )

fMRIPrep Template (ICBM152)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Requires: pip install templateflow

   plot_volumetric_slices(
       'brain.nii.gz',
       'icbm152.png',
       template='MNI152NLin2009cAsym',
       display_mode='ortho',
       dpi=600
   )

Colormaps for Volumetric Data
------------------------------

Hot (Classic)
~~~~~~~~~~~~~

.. code-block:: python

   plot_glass_brain('brain.nii.gz', 'hot.png', colormap='hot', dpi=600)

Coolwarm (Diverging)
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   plot_glass_brain('tstat.nii.gz', 'coolwarm.png', colormap='coolwarm',
                     symmetric_cbar=True, dpi=600)

Viridis (Perceptually Uniform)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   plot_glass_brain('brain.nii.gz', 'viridis.png', colormap='viridis', dpi=600)

Plasma
~~~~~~

.. code-block:: python

   plot_glass_brain('brain.nii.gz', 'plasma.png', colormap='plasma', dpi=600)

Cold-Hot (Diverging)
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   plot_volumetric_slices('tstat.nii.gz', 'cold_hot.png',
                          colormap='cold_hot', symmetric_cbar=True, dpi=600)

Advanced Options
----------------

Custom Slice Coordinates
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_volumetric_slices

   # Specify exact MNI coordinates
   plot_volumetric_slices(
       'activation.nii.gz',
       'custom_coords.png',
       display_mode='z',
       cut_coords=[-30, -10, 10, 30, 50],  # Specific z-coordinates
       colormap='hot',
       dpi=600
   )

Without Annotations
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   plot_volumetric_slices(
       'brain.nii.gz',
       'no_annotations.png',
       display_mode='ortho',
       annotate=False,  # No coordinate labels
       draw_cross=False,  # No crosshair
       colormap='hot',
       dpi=600
   )

Custom Figure Size
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   plot_glass_brain(
       'brain.nii.gz',
       'large_glass.png',
       figsize=(16, 12),  # 16×12 inches
       colormap='hot',
       dpi=600
   )

Custom Title
~~~~~~~~~~~~

.. code-block:: python

   plot_volumetric_slices(
       'brain.nii.gz',
       'titled.png',
       display_mode='ortho',
       title='Group Mean Activation (N=50)',
       colormap='hot',
       dpi=600
   )

Batch Processing
----------------

Process Multiple Files
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_glass_brain, plot_volumetric_slices
   import glob

   for nifti_file in glob.glob('results/*.nii.gz'):
       basename = os.path.basename(nifti_file).replace('.nii.gz', '')

       # Glass brain
       plot_glass_brain(
           nifti_file,
           f'figures/{basename}_glass.png',
           colormap='hot',
           dpi=600
       )

       # Orthogonal slices
       plot_volumetric_slices(
           nifti_file,
           f'figures/{basename}_slices.png',
           display_mode='ortho',
           colormap='hot',
           dpi=600
       )

Multiple Display Modes
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_volumetric_slices

   nifti_file = 'activation.nii.gz'
   display_modes = ['ortho', 'x', 'y', 'z']

   for mode in display_modes:
       plot_volumetric_slices(
           nifti_file,
           f'figures/activation_{mode}.png',
           display_mode=mode,
           colormap='hot',
           dpi=600
       )

Complete Volumetric Pipeline
-----------------------------

.. code-block:: python

   #!/usr/bin/env python3
   """
   Complete volumetric visualization pipeline.
   """

   from brainviz_dk import (
       plot_volumetric_slices,
       plot_glass_brain,
       plot_mosaic,
       plot_roi_overlay
   )
   import os

   # Configuration
   INPUT_FILE = 'group_tstat.nii.gz'
   OUTPUT_DIR = 'volumetric_viz/'
   os.makedirs(OUTPUT_DIR, exist_ok=True)

   print("Volumetric Visualization Pipeline")
   print("=" * 50)

   # 1. Orthogonal slices
   print("\n1. Generating orthogonal slices...")
   plot_volumetric_slices(
       INPUT_FILE,
       f'{OUTPUT_DIR}/01_ortho_slices.png',
       display_mode='ortho',
       colormap='hot',
       threshold=2.3,
       dpi=600
   )

   # 2. Glass brain
   print("2. Generating glass brain...")
   plot_glass_brain(
       INPUT_FILE,
       f'{OUTPUT_DIR}/02_glass_brain.png',
       display_mode='ortho',
       colormap='hot',
       threshold=2.3,
       black_bg=True,
       dpi=600
   )

   # 3. Axial mosaic
   print("3. Generating axial mosaic...")
   plot_mosaic(
       INPUT_FILE,
       f'{OUTPUT_DIR}/03_mosaic_axial.png',
       display_mode='z',
       n_slices=20,
       colormap='hot',
       dpi=600
   )

   # 4. Sagittal slices
   print("4. Generating sagittal slices...")
   plot_volumetric_slices(
       INPUT_FILE,
       f'{OUTPUT_DIR}/04_sagittal.png',
       display_mode='x',
       cut_coords=7,
       colormap='hot',
       dpi=600
   )

   # 5. Coronal slices
   print("5. Generating coronal slices...")
   plot_volumetric_slices(
       INPUT_FILE,
       f'{OUTPUT_DIR}/05_coronal.png',
       display_mode='y',
       cut_coords=7,
       colormap='hot',
       dpi=600
   )

   print("\n" + "=" * 50)
   print("✓ Pipeline complete!")
   print(f"Outputs in: {OUTPUT_DIR}")

See Also
--------

- :doc:`surface_plotting` - Surface visualization examples
- :doc:`../api/volumetric` - Volumetric plotting API reference
- :doc:`../templates` - Template documentation
