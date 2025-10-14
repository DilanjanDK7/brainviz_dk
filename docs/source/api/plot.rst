Surface Plotting API
====================

.. automodule:: plot
   :members:
   :undoc-members:
   :show-inheritance:

Main Functions
--------------

plot_nifti
~~~~~~~~~~

.. autofunction:: plot.plot_nifti

Generate a single surface plot with full control over all parameters.

**Example:**

.. code-block:: python

   from brainviz_dk import plot_nifti

   plot_nifti(
       'activation.nii.gz',
       'lateral_view.png',
       hemi='lh',
       view='lateral',
       colormap='hot',
       dpi=600,
       figsize=(10, 8)
   )

generate_four_views
~~~~~~~~~~~~~~~~~~~

.. autofunction:: plot.generate_four_views

Generate multiple views for specified hemispheres.

**Example:**

.. code-block:: python

   from brainviz_dk import generate_four_views

   outputs = generate_four_views(
       'activation.nii.gz',
       'output_dir/',
       hemis=('lh', 'rh'),
       views=('lateral', 'medial', 'dorsal', 'ventral'),
       colormap='hot',
       dpi=600
   )

generate_all_standard_views
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: plot.generate_all_standard_views

Generate all 12 standard neuroimaging views (6 views × 2 hemispheres).

**Example:**

.. code-block:: python

   from brainviz_dk import generate_all_standard_views

   outputs = generate_all_standard_views(
       'activation.nii.gz',
       'output_dir/',
       mesh='fsaverage',
       colormap='hot',
       dpi=600
   )

plot_3d_interactive
~~~~~~~~~~~~~~~~~~~

.. autofunction:: plot.plot_3d_interactive

Create interactive 3D visualization.

**Example:**

.. code-block:: python

   from brainviz_dk import plot_3d_interactive

   view = plot_3d_interactive(
       'activation.nii.gz',
       colormap='hot',
       threshold=2.0
   )
   view.save_as_html('brain_3d.html')

Quality Presets
---------------

get_quality_preset
~~~~~~~~~~~~~~~~~~

.. autofunction:: plot.get_quality_preset

Get quality preset configuration dictionary.

**Example:**

.. code-block:: python

   from brainviz_dk import get_quality_preset

   preset = get_quality_preset('publication')
   print(preset)
   # {'dpi': 600, 'output_format': 'svg', 'mesh': 'fsaverage', ...}

list_quality_presets
~~~~~~~~~~~~~~~~~~~~

.. autofunction:: plot.list_quality_presets

Display all available quality presets with descriptions.

**Example:**

.. code-block:: python

   from brainviz_dk import list_quality_presets

   list_quality_presets()

QUALITY_PRESETS
~~~~~~~~~~~~~~~

.. autodata:: plot.QUALITY_PRESETS

Dictionary containing all quality preset configurations.

**Structure:**

.. code-block:: python

   {
       'draft': {
           'dpi': 150,
           'mesh': 'fsaverage5',
           'output_format': 'png',
           'radius': 3.0,
           'description': 'Fast preview quality',
       },
       'standard': { ... },
       'publication': { ... },
       'print': { ... }
   }

Utility Functions
-----------------

project_volume_to_surface
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: plot.project_volume_to_surface

Project volumetric data onto cortical surface.

**Example:**

.. code-block:: python

   from brainviz_dk import project_volume_to_surface

   texture = project_volume_to_surface(
       'activation.nii.gz',
       hemi='lh',
       mesh='fsaverage'
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
     - Path to input NIfTI file (.nii or .nii.gz)
   * - out_path
     - str
     - Output file path
   * - hemi
     - str
     - Hemisphere: 'lh' (left) or 'rh' (right)
   * - view
     - str
     - View angle: 'lateral', 'medial', 'dorsal', 'ventral', 'anterior', 'posterior'
   * - mesh
     - str
     - Surface mesh: 'fsaverage', 'fsaverage5', 'fsaverage6'
   * - surface_name
     - str
     - Surface type: 'pial', 'inflated', 'white', 'sphere'
   * - colormap
     - str
     - Matplotlib colormap name (default: 'jet')
   * - alpha
     - float
     - Overlay transparency (0-1, default: 0.8)
   * - darkness
     - float
     - Background darkness (0-1, default: 0.8)
   * - radius
     - float
     - Gaussian kernel radius (default: 2.0)
   * - dpi
     - int
     - Output resolution (1-2400, default: 300)
   * - figsize
     - tuple
     - Figure size in inches (width, height)
   * - output_format
     - str
     - Output format: 'png', 'svg', 'pdf', 'eps'
   * - interpolation
     - str
     - Interpolation method: 'linear', 'nearest', 'cubic'
   * - smooth_fwhm
     - float
     - FWHM for Gaussian smoothing (mm)
   * - rasterize_data
     - bool
     - Rasterize data layer (reduces SVG size)

View Angles
~~~~~~~~~~~

- **lateral**: Outer side view
- **medial**: Inner side view
- **dorsal**: Top view
- **ventral**: Bottom view
- **anterior**: Front view
- **posterior**: Back view

Surface Types
~~~~~~~~~~~~~

- **pial**: Outer cortical surface (gray matter boundary)
- **inflated**: Inflated surface (reduces sulcal complexity)
- **white**: White matter surface
- **sphere**: Spherical projection

Mesh Resolutions
~~~~~~~~~~~~~~~~

- **fsaverage**: Highest resolution (~150k vertices per hemisphere)
- **fsaverage5**: Medium resolution (~10k vertices, faster)
- **fsaverage6**: High resolution (~40k vertices)

Examples
--------

Basic Surface Plot
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_nifti

   plot_nifti(
       'activation.nii.gz',
       'output.png',
       hemi='lh',
       view='lateral'
   )

High-Resolution Publication Figure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_nifti, get_quality_preset

   plot_nifti(
       'activation.nii.gz',
       'figure1.svg',
       hemi='lh',
       view='lateral',
       **get_quality_preset('publication')
   )

Multiple Views
~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import generate_four_views

   outputs = generate_four_views(
       'activation.nii.gz',
       'figures/',
       hemis=('lh', 'rh'),
       views=('lateral', 'medial'),
       dpi=600,
       prefix='subject01'
   )

Custom Styling
~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_nifti

   plot_nifti(
       'activation.nii.gz',
       'custom.png',
       hemi='lh',
       view='lateral',
       colormap='coolwarm',
       alpha=0.9,
       darkness=0.7,
       radius=1.5,
       dpi=600,
       figsize=(12, 10)
   )

Batch Processing
~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_nifti, get_quality_preset
   import glob

   preset = get_quality_preset('publication')

   for nifti_file in glob.glob('results/*.nii.gz'):
       output = nifti_file.replace('.nii.gz', '_lateral.svg')
       plot_nifti(
           nifti_file,
           output,
           hemi='lh',
           view='lateral',
           **preset
       )

See Also
--------

- :doc:`../quickstart` - Quick start guide
- :doc:`volumetric` - Volumetric plotting functions
- :doc:`templates` - Template management
