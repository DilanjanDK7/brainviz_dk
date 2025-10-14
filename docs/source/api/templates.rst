Template Management API
=======================

.. automodule:: templates
   :members:
   :undoc-members:
   :show-inheritance:

Classes
-------

TemplateManager
~~~~~~~~~~~~~~~

.. autoclass:: templates.TemplateManager
   :members:
   :undoc-members:
   :show-inheritance:

Main manager class for brain templates.

**Example:**

.. code-block:: python

   from brainviz_dk import TemplateManager

   manager = TemplateManager()

   # Get template
   template = manager.get_template('mni152', resolution=2)

   # Get template info
   info = manager.get_template_info('mni152')

Functions
---------

get_template
~~~~~~~~~~~~

.. autofunction:: templates.get_template

Load a brain template by name.

**Example:**

.. code-block:: python

   from brainviz_dk import get_template

   # Load MNI152 template
   template = get_template('mni152', resolution=2)

   # Load brain mask
   mask = get_template('mni152_brain_mask', resolution=2)

   # Load TemplateFlow template (requires installation)
   template = get_template('MNI152NLin2009cAsym', resolution=2)

list_available_templates
~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: templates.list_available_templates

Display all available templates.

**Example:**

.. code-block:: python

   from brainviz_dk import list_available_templates

   list_available_templates()

Available Templates
-------------------

The following templates are available through the TemplateManager:

nilearn Templates
~~~~~~~~~~~~~~~~~

**mni152**
   - Source: nilearn
   - Description: MNI152 T1 template (1mm or 2mm)
   - Resolutions: 1, 2
   - Space: MNI152
   - Status: Always available

**mni152_brain_mask**
   - Source: nilearn
   - Description: MNI152 brain mask
   - Resolutions: 1, 2
   - Space: MNI152
   - Status: Always available

**mni152_gm_mask**
   - Source: nilearn
   - Description: MNI152 gray matter mask
   - Resolutions: 1, 2
   - Space: MNI152
   - Status: Always available

**mni152_wm_mask**
   - Source: nilearn
   - Description: MNI152 white matter mask
   - Resolutions: 1, 2
   - Space: MNI152
   - Status: Always available

**fsaverage**
   - Source: nilearn
   - Description: FreeSurfer average surface templates
   - Resolutions: Multiple
   - Space: FreeSurfer
   - Status: Always available

TemplateFlow Templates
~~~~~~~~~~~~~~~~~~~~~~

**MNI152NLin2009cAsym**
   - Source: TemplateFlow
   - Description: MNI152 nonlinear asymmetric 2009c (fMRIPrep default)
   - Resolutions: 1, 2
   - Space: MNI152NLin2009cAsym
   - Status: Requires ``pip install templateflow``

**MNI152NLin6Asym**
   - Source: TemplateFlow
   - Description: MNI152 nonlinear asymmetric 6th generation
   - Resolutions: 1, 2
   - Space: MNI152NLin6Asym
   - Status: Requires ``pip install templateflow``

Template Information Structure
------------------------------

Each template has the following metadata:

.. code-block:: python

   {
       'source': str,          # 'nilearn' or 'templateflow'
       'description': str,     # Human-readable description
       'resolutions': list,    # Available resolutions [1, 2]
       'space': str,          # Template space name
   }

Examples
--------

Basic Template Loading
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import get_template

   # Load default resolution (2mm)
   template = get_template('mni152')

   # Load specific resolution
   template_1mm = get_template('mni152', resolution=1)
   template_2mm = get_template('mni152', resolution=2)

   # Returns nibabel Nifti1Image
   print(template.shape)
   print(template.affine)

Using with Plotting Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_volumetric_slices

   plot_volumetric_slices(
       'activation.nii.gz',
       'slices.png',
       template='mni152',  # Automatically loaded
       display_mode='ortho',
       dpi=600
   )

Loading TemplateFlow Templates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import get_template

   # First use will download template
   template = get_template('MNI152NLin2009cAsym', resolution=2)

   # Use in plotting
   from brainviz_dk import plot_glass_brain

   plot_glass_brain(
       'activation.nii.gz',
       'glass.png',
       template='MNI152NLin2009cAsym',
       dpi=600
   )

Getting Template Information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import TemplateManager

   manager = TemplateManager()

   # Get info for specific template
   info = manager.get_template_info('mni152')
   print(info)
   # {
   #     'source': 'nilearn',
   #     'description': 'MNI152 T1 template (1mm or 2mm)',
   #     'resolutions': [1, 2],
   #     'space': 'MNI152'
   # }

   # List all templates
   for name in manager.list_templates():
       print(f"{name}: {manager.get_template_info(name)['description']}")

Checking Template Availability
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import TemplateManager

   manager = TemplateManager()

   # Check if template is available
   if manager.is_available('mni152'):
       template = manager.get_template('mni152', resolution=2)

   # Check if TemplateFlow templates are available
   try:
       template = manager.get_template('MNI152NLin2009cAsym', resolution=2)
       print("TemplateFlow template loaded successfully")
   except Exception as e:
       print(f"TemplateFlow not available: {e}")
       print("Install with: pip install templateflow")

Loading Multiple Templates
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import get_template

   # Load T1w template and brain mask
   template = get_template('mni152', resolution=2)
   brain_mask = get_template('mni152_brain_mask', resolution=2)
   gm_mask = get_template('mni152_gm_mask', resolution=2)
   wm_mask = get_template('mni152_wm_mask', resolution=2)

   # Use for masking operations
   import nibabel as nib
   import numpy as np

   # Apply brain mask
   template_data = template.get_fdata()
   mask_data = brain_mask.get_fdata()
   masked_data = template_data * mask_data

Advanced Usage
--------------

Custom Template Cache
~~~~~~~~~~~~~~~~~~~~~

For TemplateFlow templates, set custom cache directory:

.. code-block:: python

   import os

   # Set before importing brainviz_dk
   os.environ['TEMPLATEFLOW_HOME'] = '/path/to/templates'

   from brainviz_dk import get_template

   template = get_template('MNI152NLin2009cAsym', resolution=2)

Direct TemplateFlow Access
~~~~~~~~~~~~~~~~~~~~~~~~~~~

For advanced TemplateFlow usage:

.. code-block:: python

   import templateflow.api as tflow

   # Download specific template variant
   template_path = tflow.get(
       'MNI152NLin2009cAsym',
       resolution=2,
       desc='brain',
       suffix='T1w',
       extension='nii.gz'
   )

   # Load with nibabel
   import nibabel as nib
   template = nib.load(template_path)

Template Comparison
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import get_template
   import numpy as np

   # Load two templates
   mni152 = get_template('mni152', resolution=2)
   icbm = get_template('MNI152NLin2009cAsym', resolution=2)

   # Compare shapes
   print(f"MNI152 shape: {mni152.shape}")
   print(f"ICBM shape: {icbm.shape}")

   # Compare affines
   print(f"MNI152 voxel size: {np.diag(mni152.affine)[:3]}")
   print(f"ICBM voxel size: {np.diag(icbm.affine)[:3]}")

Error Handling
--------------

Template Not Found
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import get_template

   try:
       template = get_template('invalid_template')
   except ValueError as e:
       print(f"Error: {e}")
       # Error: Template 'invalid_template' not found

TemplateFlow Not Installed
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import get_template

   try:
       template = get_template('MNI152NLin2009cAsym')
   except ImportError as e:
       print("TemplateFlow not installed")
       print("Install with: pip install templateflow")

Invalid Resolution
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import get_template

   try:
       template = get_template('mni152', resolution=3)
   except ValueError as e:
       print(f"Error: {e}")
       # Error: Invalid resolution. Available: [1, 2]

See Also
--------

- :doc:`../templates` - Template documentation
- :doc:`volumetric` - Volumetric plotting API
- :doc:`plot` - Surface plotting API
