Quality Presets
===============

BrainViz_DK provides four quality presets optimized for different use cases, from quick previews to high-quality print output.

Overview
--------

Quality presets are pre-configured settings that control:

- **DPI**: Output resolution
- **Format**: File format (PNG, SVG, PDF)
- **Mesh**: Surface mesh resolution (for surface plots)
- **Radius**: Gaussian kernel radius
- **Smoothing**: FWHM smoothing parameter

Available Presets
-----------------

draft
~~~~~

**Fast preview quality** - Ideal for quick visual inspection and iterative development.

**Settings:**

- DPI: 150
- Format: PNG
- Mesh: fsaverage5 (medium resolution)
- Radius: 3.0

**Use Cases:**

- Quick quality checks
- Rapid iteration during analysis
- Draft reports
- Initial parameter testing

**Output Size:** ~200 KB per plot

**Example:**

.. code-block:: python

   from brainviz_dk import plot_nifti, get_quality_preset

   plot_nifti(
       'brain.nii.gz',
       'draft_preview.png',
       hemi='lh',
       view='lateral',
       **get_quality_preset('draft')
   )

.. code-block:: bash

   brainviz_dk --in brain.nii.gz --out preview.png --quality draft

standard
~~~~~~~~

**Standard quality** - Good balance between quality and file size for general use.

**Settings:**

- DPI: 300
- Format: PNG
- Mesh: fsaverage (high resolution)
- Radius: 2.0

**Use Cases:**

- General analysis reports
- Presentations
- Internal documentation
- Lab meetings
- Supplementary materials

**Output Size:** ~400-500 KB per plot

**Example:**

.. code-block:: python

   plot_nifti(
       'brain.nii.gz',
       'standard_plot.png',
       hemi='lh',
       view='lateral',
       **get_quality_preset('standard')
   )

.. code-block:: bash

   brainviz_dk --in brain.nii.gz --out plot.png --quality standard

publication
~~~~~~~~~~~

**High quality for publications** - Vector format with high resolution for journal submissions.

**Settings:**

- DPI: 600
- Format: SVG (vector, infinitely scalable)
- Mesh: fsaverage (high resolution)
- Radius: 1.5
- Interpolation: linear
- Smoothing: None

**Use Cases:**

- Journal publications
- Conference posters
- High-quality figures
- Professional presentations
- Final manuscript figures

**Output Size:** 1-5 MB per plot (PNG), 20-100 MB (SVG)

**Advantages:**

- Infinitely scalable (vector format)
- Sharp text and lines
- Meets journal requirements (typically 300-600 DPI)
- Can be edited in vector graphics software (Inkscape, Adobe Illustrator)

**Example:**

.. code-block:: python

   plot_nifti(
       'brain.nii.gz',
       'figure1.svg',
       hemi='lh',
       view='lateral',
       **get_quality_preset('publication')
   )

.. code-block:: bash

   brainviz_dk --in brain.nii.gz --out figure1.svg --quality publication

print
~~~~~

**Very high quality for print** - Extreme resolution for large format printing.

**Settings:**

- DPI: 1200
- Format: PDF (vector, print-ready)
- Mesh: fsaverage (high resolution)
- Radius: 1.0

**Use Cases:**

- Large format posters (A0, A1)
- High-end printing
- Books and textbooks
- Billboards
- Professional printing services

**Output Size:** 5-15 MB per plot

**Warning:** Large file sizes and longer processing times.

**Example:**

.. code-block:: python

   plot_nifti(
       'brain.nii.gz',
       'poster_figure.pdf',
       hemi='lh',
       view='lateral',
       **get_quality_preset('print')
   )

.. code-block:: bash

   brainviz_dk --in brain.nii.gz --out poster.pdf --quality print

Comparison Table
----------------

+-------------+--------+--------+--------+------------+---------------+
| Preset      | DPI    | Format | Mesh   | File Size  | Processing    |
+=============+========+========+========+============+===============+
| draft       | 150    | PNG    | fsavg5 | ~200 KB    | Fast (~2s)    |
+-------------+--------+--------+--------+------------+---------------+
| standard    | 300    | PNG    | fsavg  | ~450 KB    | Moderate (~5s)|
+-------------+--------+--------+--------+------------+---------------+
| publication | 600    | SVG    | fsavg  | 1-70 MB    | Slow (~10s)   |
+-------------+--------+--------+--------+------------+---------------+
| print       | 1200   | PDF    | fsavg  | 5-15 MB    | Very slow     |
+-------------+--------+--------+--------+------------+---------------+

Using Presets
-------------

Python API
~~~~~~~~~~

**Method 1: Direct preset application**

.. code-block:: python

   from brainviz_dk import plot_nifti, get_quality_preset

   plot_nifti(
       'brain.nii.gz',
       'output.svg',
       hemi='lh',
       view='lateral',
       **get_quality_preset('publication')
   )

**Method 2: Preset with overrides**

.. code-block:: python

   preset = get_quality_preset('publication')
   preset['dpi'] = 1200  # Override DPI
   preset['output_format'] = 'png'  # Override format

   plot_nifti(
       'brain.nii.gz',
       'output.png',
       hemi='lh',
       view='lateral',
       **preset
   )

**Method 3: List all presets**

.. code-block:: python

   from brainviz_dk import list_quality_presets

   list_quality_presets()

Command-Line Interface
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Use preset directly
   brainviz_dk --in brain.nii.gz --out plot.svg --quality publication

   # Override preset settings
   brainviz_dk --in brain.nii.gz --out plot.png \
               --quality publication --dpi 1200 --format png

   # List all presets
   brainviz_dk --list-presets

Custom Quality Settings
-----------------------

You can create custom quality configurations without using presets:

Python API
~~~~~~~~~~

.. code-block:: python

   plot_nifti(
       'brain.nii.gz',
       'custom.png',
       hemi='lh',
       view='lateral',
       dpi=900,
       figsize=(14, 12),
       output_format='png',
       interpolation='cubic',
       smooth_fwhm=2.0,
       mesh='fsaverage6'
   )

Command-Line Interface
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   brainviz_dk --in brain.nii.gz --out custom.png \
               --dpi 900 --figsize 14,12 --format png --mesh fsaverage6

Choosing the Right Preset
--------------------------

Decision Flowchart
~~~~~~~~~~~~~~~~~~

1. **Need quick preview?** → Use **draft**
2. **For general work/presentations?** → Use **standard**
3. **For journal submission?** → Use **publication**
4. **For large format printing?** → Use **print**

By Use Case
~~~~~~~~~~~

**Research Workflow**

- Exploratory analysis: **draft**
- Quality control: **standard**
- Lab meeting: **standard**
- Manuscript preparation: **publication**
- Final submission: **publication**

**Publication Workflow**

- Initial drafts: **standard**
- Manuscript submission: **publication**
- Reviewer revisions: **publication**
- Final publication: **publication**

**Presentation Workflow**

- Internal slides: **standard**
- Conference slides: **standard** or **publication**
- Conference poster: **print**

**Teaching/Outreach**

- Lecture slides: **standard**
- Printed handouts: **publication**
- Textbook figures: **print**

Performance Considerations
--------------------------

Processing Time
~~~~~~~~~~~~~~~

Approximate times for single surface plot (varies by system):

- draft: 1-3 seconds
- standard: 3-7 seconds
- publication: 8-15 seconds
- print: 15-30 seconds

Disk Space
~~~~~~~~~~

For typical analysis with 12 views (all-views mode):

- draft: ~2.5 MB total
- standard: ~5 MB total
- publication: 15-70 MB total (SVG), 20 MB (PNG)
- print: 100+ MB total

Memory Usage
~~~~~~~~~~~~

Peak memory during processing:

- draft: ~500 MB
- standard: ~800 MB
- publication: ~1.2 GB
- print: ~2 GB

Format Recommendations
----------------------

PNG (Raster)
~~~~~~~~~~~~

**Advantages:**

- Small file size
- Universal compatibility
- Fast rendering
- Web-friendly

**Disadvantages:**

- Fixed resolution
- Pixelation when scaled
- Lossy quality

**Best for:** draft, standard presets, web use

SVG (Vector)
~~~~~~~~~~~~

**Advantages:**

- Infinitely scalable
- Editable in vector software
- Sharp at any size
- Text remains selectable

**Disadvantages:**

- Large file size
- Some compatibility issues
- Slower to render

**Best for:** publication preset, journal submissions

PDF (Vector)
~~~~~~~~~~~~

**Advantages:**

- Print-ready
- Widely supported
- Vector quality
- Embeds fonts

**Disadvantages:**

- Large file size
- Less editable than SVG

**Best for:** print preset, poster printing

EPS (Vector)
~~~~~~~~~~~~

**Advantages:**

- Standard in publishing
- High compatibility with LaTeX
- Vector quality

**Disadvantages:**

- Outdated format
- Large file size

**Best for:** LaTeX documents, legacy workflows

Advanced Tips
-------------

Optimizing for Specific Journals
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Check journal requirements and adjust accordingly:

.. code-block:: python

   # Nature journals: 300-600 DPI, RGB, TIFF/EPS
   preset = get_quality_preset('publication')
   preset['dpi'] = 600
   plot_nifti(..., **preset)

   # PLOS: 300 DPI minimum, TIFF preferred
   preset = get_quality_preset('publication')
   preset['dpi'] = 300
   preset['output_format'] = 'png'
   plot_nifti(..., **preset)

Batch Processing with Presets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from brainviz_dk import plot_glass_brain, get_quality_preset
   import glob

   preset = get_quality_preset('publication')

   for nifti in glob.glob('results/*.nii.gz'):
       output = nifti.replace('.nii.gz', '_glass.svg')
       plot_glass_brain(nifti, output, **preset)

See Also
--------

- :doc:`quickstart` - Quick start examples
- :doc:`cli_usage` - CLI documentation
- :doc:`api/plot` - API reference
