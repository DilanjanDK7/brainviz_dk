Volumetric Plotting API
=======================

.. automodule:: volumetric
   :members:
   :undoc-members:
   :show-inheritance:

Main Functions
--------------

plot_volumetric_slices
~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: volumetric.plot_volumetric_slices

Plot orthogonal or single-plane slices.

**Example:**

.. code-block:: python

   from brainviz_dk import plot_volumetric_slices

   plot_volumetric_slices(
       'activation.nii.gz',
       'slices.png',
       template='mni152',
       display_mode='ortho',
       colormap='hot',
       dpi=600
   )

plot_glass_brain
~~~~~~~~~~~~~~~~

.. autofunction:: volumetric.plot_glass_brain

Create transparent 3D glass brain visualization.

**Example:**

.. code-block:: python

   from brainviz_dk import plot_glass_brain

   plot_glass_brain(
       'activation.nii.gz',
       'glass.png',
       display_mode='ortho',
       colormap='hot',
       black_bg=True,
       dpi=600
   )

plot_mosaic
~~~~~~~~~~~

.. autofunction:: volumetric.plot_mosaic

Generate multi-slice mosaic display.

**Example:**

.. code-block:: python

   from brainviz_dk import plot_mosaic

   plot_mosaic(
       'brain.nii.gz',
       'mosaic.png',
       template='mni152',
       display_mode='z',
       n_slices=20,
       colormap='hot',
       dpi=600
   )

plot_roi_overlay
~~~~~~~~~~~~~~~~

.. autofunction:: volumetric.plot_roi_overlay

Plot ROI or parcellation overlay.

**Example:**

.. code-block:: python

   from brainviz_dk import plot_roi_overlay

   plot_roi_overlay(
       'parcellation.nii.gz',
       'roi.png',
       template='mni152',
       display_mode='ortho',
       colormap='tab20',
       dpi=600
   )

Parameters Reference
--------------------

Common Parameters
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Parameter
     - Type
     - Description
   * - nifti_path
     - str
     - Path to input NIfTI file
   * - out_path
     - str
     - Output file path
   * - template
     - str
     - Background template: 'mni152', 'MNI152NLin2009cAsym'
   * - display_mode
     - str
     - Display mode: 'ortho', 'x', 'y', 'z', 'yx', 'xz', 'yz', 'lyrz', 'lr'
   * - cut_coords
     - int/list
     - Number of slices or specific coordinates
   * - colormap
     - str
     - Matplotlib colormap name
   * - threshold
     - float
     - Value threshold for display
   * - vmin
     - float
     - Minimum value for colorbar
   * - vmax
     - float
     - Maximum value for colorbar
   * - symmetric_cbar
     - bool
     - Symmetric colorbar around zero
   * - annotate
     - bool
     - Show coordinate annotations
   * - draw_cross
     - bool
     - Draw crosshair at cut coordinates
   * - black_bg
     - bool
     - Use black background
   * - dpi
     - int
     - Output resolution (default: 300)
   * - figsize
     - tuple
     - Figure size in inches (width, height)
   * - output_format
     - str
     - Output format: 'png', 'svg', 'pdf', 'eps'
   * - title
     - str
     - Plot title

Display Modes
~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Mode
     - Description
   * - ortho
     - Orthogonal 3-plane view (sagittal, coronal, axial)
   * - x
     - Sagittal slices only
   * - y
     - Coronal slices only
   * - z
     - Axial slices only
   * - yx
     - Coronal and axial slices
   * - xz
     - Sagittal and axial slices
   * - yz
     - Coronal and axial slices
   * - lyrz
     - All slices with left/right separation
   * - lr
     - Left and right hemisphere views

Examples
--------

Orthogonal Slices
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_volumetric_slices

   plot_volumetric_slices(
       'activation.nii.gz',
       'ortho.png',
       template='mni152',
       display_mode='ortho',
       colormap='hot',
       threshold=2.0,
       dpi=600
   )

Glass Brain
~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_glass_brain

   plot_glass_brain(
       'activation.nii.gz',
       'glass.png',
       display_mode='ortho',
       colormap='hot',
       black_bg=True,
       threshold=2.3,
       dpi=600
   )

Axial Slices
~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_volumetric_slices

   plot_volumetric_slices(
       'brain.nii.gz',
       'axial.png',
       template='mni152',
       display_mode='z',
       cut_coords=7,
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
       display_mode='z',
       n_slices=20,
       colormap='hot',
       annotate=False,
       dpi=600
   )

Thresholded Statistical Map
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_glass_brain

   plot_glass_brain(
       't_stat.nii.gz',
       'thresholded.png',
       threshold=2.5,  # t > 2.5
       colormap='coolwarm',
       symmetric_cbar=True,
       vmin=-5,
       vmax=5,
       dpi=600
   )

ROI Overlay
~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_roi_overlay

   plot_roi_overlay(
       'atlas.nii.gz',
       'roi.png',
       template='mni152',
       display_mode='ortho',
       colormap='tab20',
       dpi=600
   )

Custom Colormap
~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_glass_brain

   plot_glass_brain(
       'activation.nii.gz',
       'plasma.png',
       colormap='plasma',
       black_bg=True,
       threshold=1.5,
       dpi=600
   )

Sagittal Slices with Annotations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_volumetric_slices

   plot_volumetric_slices(
       'brain.nii.gz',
       'sagittal.png',
       template='mni152',
       display_mode='x',
       cut_coords=5,
       annotate=True,
       draw_cross=True,
       colormap='hot',
       dpi=600
   )

Batch Glass Brain Generation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_glass_brain
   import glob

   for nifti_file in glob.glob('results/*.nii.gz'):
       output = nifti_file.replace('.nii.gz', '_glass.png')
       plot_glass_brain(
           nifti_file,
           output,
           colormap='hot',
           threshold=2.0,
           dpi=600
       )

Advanced Usage
--------------

Specific Slice Coordinates
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_volumetric_slices

   # Specify exact MNI coordinates
   plot_volumetric_slices(
       'activation.nii.gz',
       'custom_coords.png',
       display_mode='z',
       cut_coords=[-20, 0, 20, 40],  # Specific z-coordinates
       colormap='hot',
       dpi=600
   )

Custom Value Range
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_glass_brain

   plot_glass_brain(
       'brain.nii.gz',
       'custom_range.png',
       vmin=0,
       vmax=100,
       threshold=None,  # No threshold
       symmetric_cbar=False,
       colormap='hot',
       dpi=600
   )

Large Figure Size
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_volumetric_slices

   plot_volumetric_slices(
       'brain.nii.gz',
       'large.png',
       display_mode='ortho',
       figsize=(16, 12),
       dpi=600
   )

Colormap Recommendations
------------------------

For Activation Maps
~~~~~~~~~~~~~~~~~~~

- **hot**: Classic hot colormap (good for positive activations)
- **coolwarm**: Diverging colormap (good for t-statistics)
- **plasma**, **viridis**: Perceptually uniform colormaps
- **RdBu_r**: Red-blue diverging (good for correlations)

For Statistical Maps
~~~~~~~~~~~~~~~~~~~~

- **coolwarm**: Symmetric around zero
- **RdBu_r**: Red-blue diverging
- **cold_hot**: Cold-to-hot diverging

For ROI/Parcellations
~~~~~~~~~~~~~~~~~~~~~

- **tab20**: 20 distinct colors
- **Set1**, **Set2**, **Set3**: Qualitative color sets
- **Paired**: Paired categorical colors

See Also
--------

- :doc:`../quickstart` - Quick start guide
- :doc:`plot` - Surface plotting functions
- :doc:`templates` - Template management
