Brain Templates
===============

BrainViz_DK provides unified access to brain templates from multiple sources for volumetric visualization.

Overview
--------

The template system provides:

- **Unified interface** for accessing templates from nilearn and TemplateFlow
- **Multiple resolutions** (1mm, 2mm)
- **Various tissue types** (T1w, brain masks, tissue masks)
- **Automatic downloading** and caching

Available Templates
-------------------

MNI152 (nilearn)
~~~~~~~~~~~~~~~~

**Source:** nilearn built-in templates

**Space:** MNI152

**Resolutions:** 1mm, 2mm

**Templates:**

- **mni152**: MNI152 T1-weighted template
- **mni152_brain_mask**: Brain mask
- **mni152_gm_mask**: Gray matter mask
- **mni152_wm_mask**: White matter mask

**Usage:**

.. code-block:: python

   from brainviz_dk import get_template

   # Load T1w template
   template = get_template('mni152', resolution=2)

   # Load brain mask
   mask = get_template('mni152_brain_mask', resolution=2)

MNI152NLin2009cAsym (TemplateFlow)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Source:** TemplateFlow (requires installation)

**Space:** MNI152NLin2009cAsym

**Resolutions:** 1mm, 2mm

**Description:** MNI152 nonlinear asymmetric 2009c template (fMRIPrep default)

**Installation:**

.. code-block:: bash

   pip install templateflow

**Usage:**

.. code-block:: python

   from brainviz_dk import get_template

   # First use will download template (~200 MB)
   template = get_template('MNI152NLin2009cAsym', resolution=2)

fsaverage (nilearn)
~~~~~~~~~~~~~~~~~~~

**Source:** nilearn

**Description:** FreeSurfer average surface templates

**Resolutions:** fsaverage, fsaverage5, fsaverage6, fsaverage7

**Usage:** Automatically used for surface plotting

.. code-block:: python

   from brainviz_dk import plot_nifti

   plot_nifti(
       'brain.nii.gz',
       'output.png',
       hemi='lh',
       view='lateral',
       mesh='fsaverage'  # Specify mesh resolution
   )

Template Manager
----------------

List Available Templates
~~~~~~~~~~~~~~~~~~~~~~~~

Python API:

.. code-block:: python

   from brainviz_dk import list_available_templates

   list_available_templates()

Command-line:

.. code-block:: bash

   brainviz_dk --list-templates

Output:

.. code-block:: text

   Available Brain Templates:

   mni152 (nilearn)
     Description: MNI152 T1 template (1mm or 2mm)
     Resolutions: 1, 2
     Space: MNI152
     Status: ✅ Available

   MNI152NLin2009cAsym (templateflow)
     Description: MNI152 nonlinear asymmetric 2009c (fMRIPrep default)
     Resolutions: 1, 2
     Space: MNI152NLin2009cAsym
     Status: ⚠️  Requires: pip install templateflow

Loading Templates
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import get_template

   # Load with default resolution (2mm)
   template = get_template('mni152')

   # Load with specific resolution
   template_1mm = get_template('mni152', resolution=1)
   template_2mm = get_template('mni152', resolution=2)

   # Returns nibabel Nifti1Image object
   print(template.shape)  # (197, 233, 189) for 2mm

Using Templates in Plotting
----------------------------

Volumetric Slices
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_volumetric_slices

   plot_volumetric_slices(
       'activation.nii.gz',
       'slices.png',
       template='mni152',  # Specify template
       display_mode='ortho',
       dpi=600
   )

Glass Brain
~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_glass_brain

   plot_glass_brain(
       'activation.nii.gz',
       'glass.png',
       template='mni152',  # Background template
       colormap='hot',
       dpi=600
   )

Mosaic
~~~~~~

.. code-block:: python

   from brainviz_dk import plot_mosaic

   plot_mosaic(
       'brain.nii.gz',
       'mosaic.png',
       template='mni152',
       n_slices=20,
       dpi=600
   )

Command-Line Usage
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Specify template with --template
   brainviz_dk --in brain.nii.gz --out slices.png \
               --plot-type volume --template mni152

   # Glass brain with specific template
   brainviz_dk --in brain.nii.gz --out glass.png \
               --plot-type glass-brain --template MNI152NLin2009cAsym

Template Details
----------------

MNI152 Template
~~~~~~~~~~~~~~~

**Full Name:** Montreal Neurological Institute 152-brain average

**Description:** Average of 152 T1-weighted MRI scans linearly registered to Talairach space

**Characteristics:**

- Standard space for neuroimaging
- Symmetric template
- Multiple resolutions available
- Widely used in FSL, SPM, AFNI

**Dimensions:**

- 1mm: (197, 233, 189)
- 2mm: (99, 117, 95)

**Use Cases:**

- General neuroimaging visualization
- Group-level analysis
- Standard space results
- Cross-study comparisons

MNI152NLin2009cAsym Template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Full Name:** MNI152 Nonlinear Asymmetric 2009c

**Description:** Nonlinear average template with asymmetric characteristics preserved

**Characteristics:**

- Nonlinear registration
- Preserves hemispheric asymmetry
- Default in fMRIPrep
- Higher anatomical detail

**Use Cases:**

- fMRIPrep outputs
- High-precision studies
- Asymmetry analyses
- Modern neuroimaging pipelines

Template Resolution
-------------------

Choosing Resolution
~~~~~~~~~~~~~~~~~~~

**1mm resolution:**

- Higher anatomical detail
- Larger file size (~30 MB)
- Slower processing
- Better for precise localization

**2mm resolution:**

- Faster processing
- Smaller file size (~5 MB)
- Sufficient for most visualizations
- Recommended for publications

Example:

.. code-block:: python

   from brainviz_dk import get_template

   # High detail (slower)
   template_1mm = get_template('mni152', resolution=1)

   # Standard (faster, recommended)
   template_2mm = get_template('mni152', resolution=2)

Impact on Visualization:

.. code-block:: python

   # 2mm resolution (default, recommended)
   plot_volumetric_slices(
       'brain.nii.gz',
       'slices_2mm.png',
       template='mni152',  # Uses 2mm by default
       dpi=600
   )

Advanced Usage
--------------

Custom Template Path
~~~~~~~~~~~~~~~~~~~~

If you have custom templates:

.. code-block:: python

   import nibabel as nib
   from nilearn import plotting

   # Load custom template
   custom_template = nib.load('my_template.nii.gz')

   # Use with nilearn directly
   display = plotting.plot_stat_map(
       'activation.nii.gz',
       bg_img=custom_template,
       display_mode='ortho'
   )
   display.savefig('custom_template_plot.png', dpi=600)

Template Metadata
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import TemplateManager

   manager = TemplateManager()

   # Get template information
   template_info = manager.get_template_info('mni152')

   print(template_info)
   # {
   #     'source': 'nilearn',
   #     'description': 'MNI152 T1 template (1mm or 2mm)',
   #     'resolutions': [1, 2],
   #     'space': 'MNI152'
   # }

TemplateFlow Configuration
--------------------------

Installation
~~~~~~~~~~~~

.. code-block:: bash

   pip install templateflow

Set Custom Cache Directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   export TEMPLATEFLOW_HOME=/path/to/templates

Or in Python:

.. code-block:: python

   import os
   os.environ['TEMPLATEFLOW_HOME'] = '/path/to/templates'

Manual Template Download
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import templateflow.api as tflow

   # Download specific template
   template_path = tflow.get(
       'MNI152NLin2009cAsym',
       resolution=2,
       desc='brain',
       suffix='T1w'
   )

Troubleshooting
---------------

Template Not Found
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Error: Template 'MNI152NLin2009cAsym' not found

   # Solution: Install templateflow
   # pip install templateflow

Template Download Fails
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # If templateflow fails to download:

   # 1. Check internet connection
   # 2. Set custom cache directory with write permissions
   # 3. Manually download and place in cache

   import templateflow.api as tflow
   print(tflow.TF_HOME)  # Check cache location

Memory Issues with High-Resolution Templates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Use 2mm resolution instead of 1mm
   template = get_template('mni152', resolution=2)  # Instead of 1

Template Comparison
-------------------

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 20 30

   * - Template
     - Source
     - Resolution
     - Size
     - Best For
   * - mni152
     - nilearn
     - 1mm, 2mm
     - Built-in
     - General use, FSL/SPM outputs
   * - mni152_brain_mask
     - nilearn
     - 1mm, 2mm
     - Built-in
     - Brain masking
   * - MNI152NLin2009cAsym
     - templateflow
     - 1mm, 2mm
     - ~200 MB
     - fMRIPrep outputs, high precision
   * - fsaverage
     - nilearn
     - Multiple
     - Built-in
     - Surface rendering

Best Practices
--------------

1. **Use default (mni152, 2mm) for most cases**
2. **Install templateflow for fMRIPrep compatibility**
3. **Choose resolution based on speed vs. detail tradeoff**
4. **Check template space matches your data**
5. **Cache templates to avoid repeated downloads**

See Also
--------

- :doc:`quickstart` - Quick start examples
- :doc:`api/volumetric` - Volumetric plotting API
- :doc:`api/templates` - Template manager API
