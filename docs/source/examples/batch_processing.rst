Batch Processing Examples
=========================

Examples for processing multiple brain images efficiently with BrainViz_DK.

Basic Batch Processing
----------------------

Process Multiple NIfTI Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_nifti, get_quality_preset
   import glob
   import os

   # Get all NIfTI files
   nifti_files = glob.glob('results/*.nii.gz')
   preset = get_quality_preset('publication')

   for nifti_file in nifti_files:
       basename = os.path.basename(nifti_file).replace('.nii.gz', '')
       output = f'figures/{basename}_lateral.svg'

       plot_nifti(
           nifti_file,
           output,
           hemi='lh',
           view='lateral',
           **preset
       )

       print(f"✓ Processed: {basename}")

Multiple Subjects
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_glass_brain

   subjects = ['sub-01', 'sub-02', 'sub-03', 'sub-04', 'sub-05']

   for subject in subjects:
       nifti_file = f'data/{subject}/activation.nii.gz'
       output = f'figures/{subject}_glass_brain.png'

       plot_glass_brain(
           nifti_file,
           output,
           colormap='hot',
           threshold=2.3,
           dpi=600
       )

       print(f"✓ {subject} complete")

Multiple Views Per Subject
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import generate_all_standard_views

   subjects = glob.glob('data/sub-*')

   for subject_dir in subjects:
       subject = os.path.basename(subject_dir)
       nifti_file = f'{subject_dir}/activation.nii.gz'
       output_dir = f'figures/{subject}/'

       outputs = generate_all_standard_views(
           nifti_file,
           output_dir,
           prefix=subject,
           colormap='hot',
           dpi=600
       )

       print(f"✓ {subject}: {len(outputs)} views generated")

Advanced Batch Processing
--------------------------

With Progress Tracking
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_nifti, get_quality_preset
   import glob
   from tqdm import tqdm  # pip install tqdm

   nifti_files = glob.glob('results/*.nii.gz')
   preset = get_quality_preset('publication')

   for nifti_file in tqdm(nifti_files, desc="Processing"):
       basename = os.path.basename(nifti_file).replace('.nii.gz', '')
       output = f'figures/{basename}.svg'

       plot_nifti(
           nifti_file,
           output,
           hemi='lh',
           view='lateral',
           **preset
       )

Parallel Processing
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_glass_brain
   from concurrent.futures import ProcessPoolExecutor
   import glob

   def process_file(nifti_file):
       """Process a single file."""
       basename = os.path.basename(nifti_file).replace('.nii.gz', '')
       output = f'figures/{basename}_glass.png'

       plot_glass_brain(
           nifti_file,
           output,
           colormap='hot',
           threshold=2.0,
           dpi=600
       )

       return basename

   # Get all files
   nifti_files = glob.glob('results/*.nii.gz')

   # Process in parallel
   with ProcessPoolExecutor(max_workers=4) as executor:
       results = list(executor.map(process_file, nifti_files))

   print(f"✓ Processed {len(results)} files in parallel")

With Error Handling
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_nifti
   import glob
   import logging

   # Setup logging
   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger(__name__)

   nifti_files = glob.glob('results/*.nii.gz')
   successful = 0
   failed = []

   for nifti_file in nifti_files:
       try:
           basename = os.path.basename(nifti_file).replace('.nii.gz', '')
           output = f'figures/{basename}.png'

           plot_nifti(
               nifti_file,
               output,
               hemi='lh',
               view='lateral',
               dpi=600
           )

           successful += 1
           logger.info(f"✓ {basename}")

       except Exception as e:
           failed.append((nifti_file, str(e)))
           logger.error(f"✗ {basename}: {e}")

   # Summary
   print(f"\nSummary:")
   print(f"  Successful: {successful}")
   print(f"  Failed: {len(failed)}")

   if failed:
       print("\nFailed files:")
       for file, error in failed:
           print(f"  - {file}: {error}")

Multiple Contrasts
------------------

Process Different Statistical Maps
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_glass_brain, plot_volumetric_slices

   subjects = ['sub-01', 'sub-02', 'sub-03']
   contrasts = ['faces_vs_houses', 'tools_vs_animals', 'words_vs_nonwords']

   for subject in subjects:
       for contrast in contrasts:
           nifti_file = f'results/{subject}/{contrast}_tstat.nii.gz'

           # Glass brain
           plot_glass_brain(
               nifti_file,
               f'figures/{subject}_{contrast}_glass.png',
               colormap='hot',
               threshold=2.3,
               dpi=600
           )

           # Slices
           plot_volumetric_slices(
               nifti_file,
               f'figures/{subject}_{contrast}_slices.png',
               display_mode='ortho',
               colormap='hot',
               dpi=600
           )

           print(f"✓ {subject} - {contrast}")

Group-Level Analysis
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import (
       plot_glass_brain,
       plot_volumetric_slices,
       plot_mosaic,
       generate_all_standard_views
   )

   # Group-level maps
   group_maps = {
       'group_mean': 'Mean activation',
       'group_tstat': 'T-statistic',
       'group_std': 'Standard deviation',
       'group_p_unc': 'Uncorrected p-values'
   }

   for map_name, description in group_maps.items():
       nifti_file = f'group_results/{map_name}.nii.gz'

       print(f"\nProcessing: {description}")

       # Glass brain
       plot_glass_brain(
           nifti_file,
           f'figures/group/{map_name}_glass.png',
           colormap='hot',
           dpi=600
       )

       # Orthogonal slices
       plot_volumetric_slices(
           nifti_file,
           f'figures/group/{map_name}_slices.png',
           display_mode='ortho',
           colormap='hot',
           dpi=600
       )

       # Surface (all views)
       generate_all_standard_views(
           nifti_file,
           f'figures/group/{map_name}_surface/',
           prefix=map_name,
           colormap='hot',
           dpi=600
       )

       print(f"  ✓ {description} complete")

Quality Workflows
-----------------

Draft → Standard → Publication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_nifti, get_quality_preset

   nifti_file = 'activation.nii.gz'
   qualities = ['draft', 'standard', 'publication']

   for quality in qualities:
       preset = get_quality_preset(quality)
       extension = preset['output_format']

       output = f'figures/activation_{quality}.{extension}'

       plot_nifti(
           nifti_file,
           output,
           hemi='lh',
           view='lateral',
           **preset
       )

       print(f"✓ Generated {quality} version")

Multi-Format Export
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_nifti

   nifti_file = 'activation.nii.gz'
   formats = ['png', 'svg', 'pdf', 'eps']

   for fmt in formats:
       output = f'figures/activation.{fmt}'

       plot_nifti(
           nifti_file,
           output,
           hemi='lh',
           view='lateral',
           dpi=600,
           output_format=fmt
       )

       print(f"✓ Exported {fmt.upper()}")

Complete Batch Pipeline
------------------------

Full Analysis Script
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   #!/usr/bin/env python3
   """
   Complete batch processing pipeline for fMRI group analysis.
   """

   from brainviz_dk import (
       plot_glass_brain,
       plot_volumetric_slices,
       plot_mosaic,
       generate_all_standard_views,
       get_quality_preset
   )
   import glob
   import os
   from datetime import datetime

   # Configuration
   DATA_DIR = 'group_results/'
   OUTPUT_DIR = f'visualizations_{datetime.now().strftime("%Y%m%d_%H%M%S")}/'
   os.makedirs(OUTPUT_DIR, exist_ok=True)

   print("="* 70)
   print(" BrainViz_DK Batch Processing Pipeline")
   print("=" * 70)
   print(f"\nInput: {DATA_DIR}")
   print(f"Output: {OUTPUT_DIR}")
   print()

   # Get all NIfTI files
   nifti_files = glob.glob(f'{DATA_DIR}/*.nii.gz')
   total_files = len(nifti_files)

   print(f"Found {total_files} files to process\n")

   preset = get_quality_preset('publication')
   processed = 0

   for idx, nifti_file in enumerate(nifti_files, 1):
       basename = os.path.basename(nifti_file).replace('.nii.gz', '')

       print(f"[{idx}/{total_files}] Processing: {basename}")

       # Create output directory for this file
       file_output_dir = f'{OUTPUT_DIR}/{basename}/'
       os.makedirs(file_output_dir, exist_ok=True)

       try:
           # 1. Glass brain
           print("  → Glass brain...", end=" ")
           plot_glass_brain(
               nifti_file,
               f'{file_output_dir}/glass_brain.svg',
               **preset
           )
           print("✓")

           # 2. Orthogonal slices
           print("  → Orthogonal slices...", end=" ")
           plot_volumetric_slices(
               nifti_file,
               f'{file_output_dir}/ortho_slices.svg',
               display_mode='ortho',
               **preset
           )
           print("✓")

           # 3. Axial mosaic
           print("  → Axial mosaic...", end=" ")
           plot_mosaic(
               nifti_file,
               f'{file_output_dir}/mosaic_axial.svg',
               display_mode='z',
               n_slices=20,
               **preset
           )
           print("✓")

           # 4. Surface visualizations
           print("  → Surface views...", end=" ")
           outputs = generate_all_standard_views(
               nifti_file,
               f'{file_output_dir}/surface/',
               prefix=basename,
               **preset
           )
           print(f"✓ ({len(outputs)} views)")

           processed += 1

       except Exception as e:
           print(f"✗ Error: {e}")
           continue

   # Summary
   print("\n" + "=" * 70)
   print(" Summary")
   print("=" * 70)
   print(f"Total files: {total_files}")
   print(f"Processed successfully: {processed}")
   print(f"Failed: {total_files - processed}")
   print(f"\nOutput directory: {OUTPUT_DIR}")
   print("=" * 70)

Configuration File Approach
---------------------------

Using Config File
~~~~~~~~~~~~~~~~~

Create ``config.yaml``:

.. code-block:: yaml

   # Batch processing configuration

   input_dir: "results/"
   output_dir: "visualizations/"

   subjects:
     - sub-01
     - sub-02
     - sub-03

   contrasts:
     - faces_vs_houses
     - tools_vs_animals

   plot_types:
     - glass_brain
     - slices
     - surface

   quality: publication

   colormap: hot
   threshold: 2.3
   dpi: 600

Process with config:

.. code-block:: python

   import yaml
   from brainviz_dk import (
       plot_glass_brain,
       plot_volumetric_slices,
       generate_all_standard_views,
       get_quality_preset
   )

   # Load config
   with open('config.yaml', 'r') as f:
       config = yaml.safe_load(f)

   preset = get_quality_preset(config['quality'])

   for subject in config['subjects']:
       for contrast in config['contrasts']:
           nifti_file = f"{config['input_dir']}/{subject}/{contrast}.nii.gz"
           output_base = f"{config['output_dir']}/{subject}_{contrast}"

           if 'glass_brain' in config['plot_types']:
               plot_glass_brain(
                   nifti_file,
                   f'{output_base}_glass.svg',
                   threshold=config['threshold'],
                   colormap=config['colormap'],
                   **preset
               )

           if 'slices' in config['plot_types']:
               plot_volumetric_slices(
                   nifti_file,
                   f'{output_base}_slices.svg',
                   display_mode='ortho',
                   colormap=config['colormap'],
                   **preset
               )

           if 'surface' in config['plot_types']:
               generate_all_standard_views(
                   nifti_file,
                   f'{config['output_dir']}/{subject}_{contrast}_surface/',
                   colormap=config['colormap'],
                   **preset
               )

           print(f"✓ {subject} - {contrast}")

Performance Tips
----------------

Memory-Efficient Batch Processing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import gc
   from brainviz_dk import plot_nifti

   nifti_files = glob.glob('results/*.nii.gz')

   for nifti_file in nifti_files:
       # Process file
       plot_nifti(nifti_file, 'output.png', hemi='lh', view='lateral')

       # Force garbage collection after each file
       gc.collect()

Optimize for Speed
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_nifti, get_quality_preset

   # Use draft quality for speed
   preset = get_quality_preset('draft')

   for nifti_file in glob.glob('results/*.nii.gz'):
       plot_nifti(
           nifti_file,
           f'figures/{basename}.png',
           hemi='lh',
           view='lateral',
           **preset  # Fast processing with fsaverage5
       )

See Also
--------

- :doc:`surface_plotting` - Surface plotting examples
- :doc:`volumetric_plotting` - Volumetric plotting examples
- :doc:`../api/plot` - Surface plotting API
- :doc:`../api/volumetric` - Volumetric plotting API
