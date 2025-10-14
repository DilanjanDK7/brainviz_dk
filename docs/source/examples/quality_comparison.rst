Quality Comparison Examples
===========================

Visual comparisons and practical examples of different quality settings in BrainViz_DK.

Quality Preset Overview
-----------------------

Generate All Quality Levels
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_nifti, get_quality_preset

   nifti_file = 'activation.nii.gz'
   presets = ['draft', 'standard', 'publication', 'print']

   for preset_name in presets:
       preset = get_quality_preset(preset_name)
       extension = preset['output_format']

       output = f'quality_comparison/{preset_name}.{extension}'

       plot_nifti(
           nifti_file,
           output,
           hemi='lh',
           view='lateral',
           **preset
       )

       # Get file size
       import os
       size_mb = os.path.getsize(output) / (1024 * 1024)

       print(f"{preset_name:12s}: {size_mb:6.2f} MB")

Draft vs Standard vs Publication
---------------------------------

Side-by-Side Comparison
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_nifti, get_quality_preset
   import time

   nifti_file = 'activation.nii.gz'

   # Draft
   print("Draft quality...")
   start = time.time()
   plot_nifti(
       nifti_file,
       'comparison/draft.png',
       hemi='lh',
       view='lateral',
       **get_quality_preset('draft')
   )
   draft_time = time.time() - start

   # Standard
   print("Standard quality...")
   start = time.time()
   plot_nifti(
       nifti_file,
       'comparison/standard.png',
       hemi='lh',
       view='lateral',
       **get_quality_preset('standard')
   )
   standard_time = time.time() - start

   # Publication
   print("Publication quality...")
   start = time.time()
   plot_nifti(
       nifti_file,
       'comparison/publication.svg',
       hemi='lh',
       view='lateral',
       **get_quality_preset('publication')
   )
   publication_time = time.time() - start

   # Summary
   print("\nProcessing Time Comparison:")
   print(f"  Draft:       {draft_time:.2f}s")
   print(f"  Standard:    {standard_time:.2f}s")
   print(f"  Publication: {publication_time:.2f}s")

DPI Comparison
--------------

Different DPI Settings
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_nifti

   nifti_file = 'activation.nii.gz'
   dpi_values = [150, 300, 600, 1200, 2400]

   for dpi in dpi_values:
       output = f'dpi_comparison/brain_{dpi}dpi.png'

       plot_nifti(
           nifti_file,
           output,
           hemi='lh',
           view='lateral',
           dpi=dpi
       )

       import os
       size_mb = os.path.getsize(output) / (1024 * 1024)

       print(f"{dpi:4d} DPI: {size_mb:6.2f} MB")

DPI Impact on File Size
~~~~~~~~~~~~~~~~~~~~~~~~

Expected file sizes for typical surface plot:

.. code-block:: text

   DPI      File Size   Quality      Processing Time
   -------- ----------- ------------ ----------------
   150      ~200 KB     Preview      ~2 seconds
   300      ~450 KB     Standard     ~5 seconds
   600      1.8 MB      High         ~10 seconds
   1200     5-7 MB      Very High    ~20 seconds
   2400     15-20 MB    Extreme      ~40 seconds

Mesh Resolution Comparison
---------------------------

fsaverage5 vs fsaverage
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_nifti

   nifti_file = 'activation.nii.gz'
   meshes = ['fsaverage5', 'fsaverage6', 'fsaverage']

   for mesh in meshes:
       output = f'mesh_comparison/{mesh}.png'

       plot_nifti(
           nifti_file,
           output,
           hemi='lh',
           view='lateral',
           mesh=mesh,
           dpi=600
       )

       print(f"✓ Generated {mesh}")

Mesh Characteristics:

.. code-block:: text

   Mesh         Vertices    File Size   Speed     Detail
   ------------ ----------- ----------- --------- ----------
   fsaverage5   ~10k        ~400 KB     Fast      Medium
   fsaverage6   ~40k        ~1.5 MB     Medium    High
   fsaverage    ~150k       ~5 MB       Slow      Very High

Format Comparison
-----------------

PNG vs SVG vs PDF
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_nifti

   nifti_file = 'activation.nii.gz'
   formats = ['png', 'svg', 'pdf', 'eps']

   for fmt in formats:
       output = f'format_comparison/brain.{fmt}'

       plot_nifti(
           nifti_file,
           output,
           hemi='lh',
           view='lateral',
           dpi=600,
           output_format=fmt
       )

       import os
       size_mb = os.path.getsize(output) / (1024 * 1024)

       print(f"{fmt.upper():4s}: {size_mb:6.2f} MB")

Format Characteristics:

.. code-block:: text

   Format   Type     Size      Scalable   Editable   Best For
   -------- -------- --------- ---------- ---------- -------------------
   PNG      Raster   ~2 MB     No         No         Web, presentations
   SVG      Vector   20-70 MB  Yes        Yes        Publications, editing
   PDF      Vector   ~5 MB     Yes        Limited    Print, LaTeX
   EPS      Vector   ~10 MB    Yes        Limited    LaTeX, legacy

Use Case Scenarios
------------------

Scenario 1: Quick Quality Check
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal:** Fast preview of results

**Solution:**

.. code-block:: python

   from brainviz_dk import plot_nifti, get_quality_preset

   plot_nifti(
       'activation.nii.gz',
       'quick_check.png',
       hemi='lh',
       view='lateral',
       **get_quality_preset('draft')
   )

**Result:** ~2 seconds, 200 KB file

Scenario 2: Lab Meeting Presentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal:** Good quality for slides

**Solution:**

.. code-block:: python

   from brainviz_dk import plot_nifti, get_quality_preset

   plot_nifti(
       'activation.nii.gz',
       'presentation_slide.png',
       hemi='lh',
       view='lateral',
       **get_quality_preset('standard')
   )

**Result:** ~5 seconds, 450 KB file, good for PowerPoint/Keynote

Scenario 3: Journal Manuscript
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal:** High-quality vector figure

**Solution:**

.. code-block:: python

   from brainviz_dk import plot_nifti, get_quality_preset

   plot_nifti(
       'activation.nii.gz',
       'manuscript_figure1.svg',
       hemi='lh',
       view='lateral',
       **get_quality_preset('publication')
   )

**Result:** ~10 seconds, 70 MB SVG (or 2 MB PNG at 600 DPI)

Scenario 4: Conference Poster
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Goal:** Very high quality for large format

**Solution:**

.. code-block:: python

   from brainviz_dk import plot_nifti, get_quality_preset

   # Get publication preset and boost DPI
   preset = get_quality_preset('print')

   plot_nifti(
       'activation.nii.gz',
       'poster_figure.pdf',
       hemi='lh',
       view='lateral',
       **preset
   )

**Result:** ~20 seconds, 5-10 MB PDF, suitable for A0 poster printing

Custom Quality Configurations
------------------------------

Optimized for Web
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_nifti

   plot_nifti(
       'activation.nii.gz',
       'web_optimized.png',
       hemi='lh',
       view='lateral',
       dpi=150,  # Low DPI for web
       mesh='fsaverage5',  # Faster rendering
       figsize=(8, 6),  # Standard web size
       output_format='png'
   )

Optimized for Print
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_nifti

   plot_nifti(
       'activation.nii.gz',
       'print_optimized.pdf',
       hemi='lh',
       view='lateral',
       dpi=1200,  # High DPI for print
       mesh='fsaverage',  # Maximum detail
       figsize=(10, 8),  # Print dimensions
       output_format='pdf',
       interpolation='cubic'  # Smooth interpolation
   )

Balanced Quality/Speed
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_nifti

   plot_nifti(
       'activation.nii.gz',
       'balanced.png',
       hemi='lh',
       view='lateral',
       dpi=450,  # Between standard and publication
       mesh='fsaverage6',  # Good detail, reasonable speed
       figsize=(10, 8),
       output_format='png'
   )

Quality Metrics
---------------

Complete Quality Benchmark
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   #!/usr/bin/env python3
   """
   Comprehensive quality comparison benchmark.
   """

   from brainviz_dk import plot_nifti, get_quality_preset
   import time
   import os

   nifti_file = 'activation.nii.gz'
   output_dir = 'quality_benchmark/'
   os.makedirs(output_dir, exist_ok=True)

   print("=" * 70)
   print(" BrainViz_DK Quality Benchmark")
   print("=" * 70)
   print()

   configurations = [
       ('draft', get_quality_preset('draft')),
       ('standard', get_quality_preset('standard')),
       ('publication', get_quality_preset('publication')),
       ('print', get_quality_preset('print')),
   ]

   results = []

   for name, preset in configurations:
       extension = preset['output_format']
       output = f'{output_dir}/{name}.{extension}'

       print(f"Testing: {name:12s}", end=" ")

       # Time the operation
       start = time.time()
       plot_nifti(
           nifti_file,
           output,
           hemi='lh',
           view='lateral',
           **preset
       )
       duration = time.time() - start

       # Get file size
       size_mb = os.path.getsize(output) / (1024 * 1024)

       results.append({
           'preset': name,
           'time': duration,
           'size': size_mb,
           'dpi': preset['dpi'],
           'format': extension
       })

       print(f"[{duration:5.2f}s, {size_mb:6.2f} MB]")

   # Print summary table
   print("\n" + "=" * 70)
   print(" Summary")
   print("=" * 70)
   print(f"{'Preset':<12} {'DPI':<6} {'Format':<6} {'Time':>8} {'Size':>10}")
   print("-" * 70)

   for r in results:
       print(f"{r['preset']:<12} {r['dpi']:<6} {r['format']:<6} "
             f"{r['time']:>7.2f}s {r['size']:>9.2f} MB")

   print("=" * 70)

Example Output:

.. code-block:: text

   ======================================================================
    BrainViz_DK Quality Benchmark
   ======================================================================

   Testing: draft        [  2.34s,   0.19 MB]
   Testing: standard     [  5.12s,   0.45 MB]
   Testing: publication  [ 10.87s,  68.23 MB]
   Testing: print        [ 22.45s,   8.91 MB]

   ======================================================================
    Summary
   ======================================================================
   Preset       DPI    Format    Time       Size
   ----------------------------------------------------------------------
   draft        150    png        2.34s      0.19 MB
   standard     300    png        5.12s      0.45 MB
   publication  600    svg       10.87s     68.23 MB
   print        1200   pdf       22.45s      8.91 MB
   ======================================================================

Decision Guide
--------------

Choose Quality Based on Need:

.. code-block:: text

   Use Case                  → Recommended Preset
   ------------------------- → --------------------
   Quick preview             → draft
   Exploratory analysis      → draft
   Lab meeting               → standard
   Conference slides         → standard
   Manuscript submission     → publication
   Journal revision          → publication
   Conference poster (A0)    → print
   Textbook figure           → print
   Web/blog post             → draft or standard
   Supplementary materials   → standard

Trade-offs Summary
------------------

.. code-block:: text

   Higher DPI:
   ✓ Sharper images
   ✓ Better for print
   ✓ More detail visible
   ✗ Larger file sizes
   ✗ Slower processing
   ✗ More memory needed

   Vector Formats (SVG/PDF):
   ✓ Infinitely scalable
   ✓ Editable in graphics software
   ✓ Sharp text and lines
   ✗ Very large file sizes
   ✗ Some compatibility issues
   ✗ Slower to render

   High Mesh Resolution:
   ✓ More anatomical detail
   ✓ Smoother surfaces
   ✗ Slower processing
   ✗ Larger files
   ✗ More memory usage

See Also
--------

- :doc:`../quality_presets` - Detailed quality preset documentation
- :doc:`surface_plotting` - Surface plotting examples
- :doc:`../quickstart` - Quick start guide
