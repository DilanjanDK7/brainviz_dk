Command-Line Interface
======================

BrainViz_DK provides a comprehensive command-line interface for all visualization tasks.

Basic Usage
-----------

.. code-block:: bash

   brainviz_dk --in INPUT.nii.gz --out OUTPUT [OPTIONS]

Main Options
------------

.. option:: --in NIFTI_PATH

   Path to input NIfTI file (.nii or .nii.gz). **Required** for plotting commands.

.. option:: --out OUTPUT_PATH

   Output file or directory path. **Required** for plotting commands.

.. option:: --plot-type {surface,volume,glass-brain,mosaic,roi,3d}

   Type of plot to generate. Default: ``surface``

   - **surface**: Cortical surface projection
   - **volume**: Orthogonal slice views
   - **glass-brain**: Transparent 3D visualization
   - **mosaic**: Multi-slice mosaic display
   - **roi**: ROI/parcellation overlay
   - **3d**: Interactive 3D visualization

Utility Commands
----------------

.. option:: --list-presets

   List available quality presets and exit.

   .. code-block:: bash

      brainviz_dk --list-presets

.. option:: --list-templates

   List available brain templates and exit.

   .. code-block:: bash

      brainviz_dk --list-templates

.. option:: --version

   Show version number and exit.

Surface Plotting Options
------------------------

.. option:: --view {lateral,medial,dorsal,ventral,anterior,posterior}

   View angle for single surface plot.

   .. code-block:: bash

      brainviz_dk --in brain.nii.gz --out plot.png --view lateral --hemi left

.. option:: --views VIEWS

   Comma-separated list of views to generate.

   .. code-block:: bash

      brainviz_dk --in brain.nii.gz --out plots/ --views lateral,medial,dorsal

.. option:: --all-views

   Generate all 6 standard views for each hemisphere (12 plots total).

   .. code-block:: bash

      brainviz_dk --in brain.nii.gz --out plots/ --all-views

.. option:: --hemi {left,right,lh,rh,both}

   Hemisphere(s) to plot. Default: ``both``

.. option:: --surface {pial,inflated,white,sphere}

   Surface type to use. Default: ``pial``

   - **pial**: Outer cortical surface
   - **inflated**: Inflated surface (reduces sulcal/gyral complexity)
   - **white**: White matter surface
   - **sphere**: Spherical surface

.. option:: --mesh {fsaverage,fsaverage5,fsaverage6}

   Surface mesh resolution. Default: ``fsaverage``

   - **fsaverage**: Highest resolution (~150k vertices per hemisphere)
   - **fsaverage5**: Medium resolution (~10k vertices)
   - **fsaverage6**: High resolution (~40k vertices)

Volumetric Plotting Options
----------------------------

.. option:: --template TEMPLATE

   Background brain template. Default: ``mni152``

   Available templates:

   - mni152
   - mni152_brain_mask
   - mni152_gm_mask
   - mni152_wm_mask
   - MNI152NLin2009cAsym (requires templateflow)

.. option:: --display-mode {ortho,x,y,z,yx,xz,yz,lyrz,lr}

   Display mode for volumetric plots. Default: ``ortho``

   - **ortho**: Orthogonal 3-plane view
   - **x**: Sagittal slices
   - **y**: Coronal slices
   - **z**: Axial slices
   - **yx**, **xz**, **yz**: Two-plane combinations
   - **lyrz**: All slices with left/right
   - **lr**: Left and right hemispheres

.. option:: --cut-coords COORDS

   Number of slices or specific coordinates.

   .. code-block:: bash

      # 5 automatically selected slices
      brainviz_dk --in brain.nii.gz --out plot.png --plot-type volume \
                  --display-mode z --cut-coords 5

.. option:: --n-slices N

   Number of slices for mosaic view. Default: ``12``

   .. code-block:: bash

      brainviz_dk --in brain.nii.gz --out mosaic.png --plot-type mosaic \
                  --display-mode z --n-slices 20

Quality & Output Options
------------------------

.. option:: --quality {draft,standard,publication,print}

   Quality preset (overrides dpi, format, mesh settings).

   .. code-block:: bash

      brainviz_dk --in brain.nii.gz --out plot.svg --quality publication

.. option:: --dpi DPI

   Output resolution in DPI. Default: ``300``

   Range: 1-2400 DPI

   .. code-block:: bash

      brainviz_dk --in brain.nii.gz --out high_res.png --dpi 1200

.. option:: --format {png,svg,pdf,eps}

   Output format (auto-detected from filename if not specified).

   .. code-block:: bash

      brainviz_dk --in brain.nii.gz --out plot.svg --format svg

.. option:: --figsize WIDTH,HEIGHT

   Figure size in inches (e.g., '10,8').

   .. code-block:: bash

      brainviz_dk --in brain.nii.gz --out large.png --figsize 12,10

Style Options
-------------

.. option:: --colormap CMAP

   Colormap name. Default: ``hot``

   Common colormaps: hot, jet, coolwarm, viridis, plasma, inferno, RdBu_r, cold_hot

   .. code-block:: bash

      brainviz_dk --in brain.nii.gz --out plot.png --colormap coolwarm

.. option:: --threshold VALUE

   Value threshold for display.

   .. code-block:: bash

      brainviz_dk --in t_map.nii.gz --out thresholded.png --threshold 2.5

.. option:: --black-bg

   Use black background (for volumetric plots).

   .. code-block:: bash

      brainviz_dk --in brain.nii.gz --out dark.png --plot-type glass-brain --black-bg

General Options
---------------

.. option:: --prefix PREFIX

   Filename prefix for batch outputs.

   .. code-block:: bash

      brainviz_dk --in brain.nii.gz --out plots/ --all-views --prefix subject01

.. option:: --verbose, -v

   Verbose output (show detailed progress).

   .. code-block:: bash

      brainviz_dk --in brain.nii.gz --out plot.png --verbose

Complete Examples
-----------------

Surface Plotting
~~~~~~~~~~~~~~~~

**Single View**

.. code-block:: bash

   brainviz_dk --in activation.nii.gz --out lateral_lh.png \
               --plot-type surface --view lateral --hemi left --dpi 600

**Multiple Custom Views**

.. code-block:: bash

   brainviz_dk --in activation.nii.gz --out plots/ \
               --plot-type surface --views lateral,medial,dorsal,ventral \
               --hemi both --dpi 600 --prefix subject01

**All Standard Views**

.. code-block:: bash

   brainviz_dk --in activation.nii.gz --out plots/ \
               --plot-type surface --all-views --quality publication

**High-Resolution Publication Figure**

.. code-block:: bash

   brainviz_dk --in activation.nii.gz --out figure1.svg \
               --plot-type surface --view lateral --hemi left \
               --quality publication --colormap hot

Volumetric Plotting
~~~~~~~~~~~~~~~~~~~

**Orthogonal Slices**

.. code-block:: bash

   brainviz_dk --in brain.nii.gz --out ortho.png \
               --plot-type volume --display-mode ortho \
               --template mni152 --colormap hot --dpi 600

**Glass Brain**

.. code-block:: bash

   brainviz_dk --in activation.nii.gz --out glass.png \
               --plot-type glass-brain --display-mode ortho \
               --colormap hot --black-bg --dpi 600

**Mosaic (Axial Slices)**

.. code-block:: bash

   brainviz_dk --in brain.nii.gz --out mosaic.png \
               --plot-type mosaic --display-mode z --n-slices 20 \
               --colormap hot --dpi 600

**Sagittal Slices**

.. code-block:: bash

   brainviz_dk --in brain.nii.gz --out sagittal.png \
               --plot-type volume --display-mode x --cut-coords 7 \
               --colormap hot --dpi 600

**Coronal Slices**

.. code-block:: bash

   brainviz_dk --in brain.nii.gz --out coronal.png \
               --plot-type volume --display-mode y --cut-coords 7 \
               --colormap hot --dpi 600

3D Interactive
~~~~~~~~~~~~~~

**Save to HTML**

.. code-block:: bash

   brainviz_dk --in activation.nii.gz --out brain_3d.html \
               --plot-type 3d --colormap hot

**Open in Browser**

.. code-block:: bash

   brainviz_dk --in activation.nii.gz --out plots/ \
               --plot-type 3d --colormap hot

ROI Overlay
~~~~~~~~~~~

.. code-block:: bash

   brainviz_dk --in parcellation.nii.gz --out roi.png \
               --plot-type roi --display-mode ortho \
               --template mni152 --dpi 600

Advanced Usage
--------------

Custom Quality Settings
~~~~~~~~~~~~~~~~~~~~~~~

Override individual quality settings:

.. code-block:: bash

   brainviz_dk --in brain.nii.gz --out custom.png \
               --quality publication --dpi 1200 --format png

Thresholded Statistical Map
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   brainviz_dk --in t_stat.nii.gz --out thresholded.png \
               --plot-type glass-brain --threshold 2.3 \
               --colormap coolwarm --dpi 600

Large Custom Figure
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   brainviz_dk --in brain.nii.gz --out large_figure.png \
               --view lateral --hemi left --figsize 16,12 --dpi 600

Batch Processing Script
~~~~~~~~~~~~~~~~~~~~~~~

Create a bash script for batch processing:

.. code-block:: bash

   #!/bin/bash
   # process_all.sh

   for nifti in results/*.nii.gz; do
       basename=$(basename "$nifti" .nii.gz)

       # Generate surface plots
       brainviz_dk --in "$nifti" --out "plots/${basename}_surface.png" \
                   --plot-type surface --view lateral --hemi left \
                   --quality publication

       # Generate glass brain
       brainviz_dk --in "$nifti" --out "plots/${basename}_glass.png" \
                   --plot-type glass-brain --quality publication

       echo "Processed: $basename"
   done

Exit Codes
----------

- **0**: Success
- **1**: Error (missing file, invalid arguments, plotting failure)

Troubleshooting
---------------

**Command Not Found**

If ``brainviz_dk`` command is not found:

.. code-block:: bash

   # Use module syntax
   python -m brainviz_dk --in brain.nii.gz --out plot.png

**Memory Errors**

For large datasets or high DPI:

.. code-block:: bash

   # Reduce DPI
   brainviz_dk --in large_brain.nii.gz --out plot.png --dpi 300

   # Use draft preset
   brainviz_dk --in large_brain.nii.gz --out plot.png --quality draft

**Permission Errors**

Ensure output directory exists and is writable:

.. code-block:: bash

   mkdir -p output_plots
   brainviz_dk --in brain.nii.gz --out output_plots/ --all-views

See Also
--------

- :doc:`quickstart` - Quick start guide
- :doc:`quality_presets` - Quality preset details
- :doc:`templates` - Template information
- :doc:`api/plot` - Python API reference
