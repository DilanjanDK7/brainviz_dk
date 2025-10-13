"""
BrainViz_DK Command Line Interface.

Provides comprehensive brain visualization from the command line.
"""

import argparse
import os
import sys
from pathlib import Path

from .plot import (
    generate_four_views,
    generate_all_standard_views,
    plot_3d_interactive,
    plot_nifti,
    get_quality_preset,
    list_quality_presets,
)
from .volumetric import (
    plot_volumetric_slices,
    plot_glass_brain,
    plot_mosaic,
    plot_roi_overlay,
)
from .templates import list_available_templates


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="brainviz_dk",
        description="BrainViz_DK: Advanced brain visualization toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:

  SURFACE PLOTTING:
  # All standard views (12 images)
  brainviz_dk --in brain.nii.gz --out plots/ --plot-type surface --all-views

  # Single view with quality preset
  brainviz_dk --in brain.nii.gz --out plot.svg --plot-type surface \\
              --view lateral --hemi left --quality publication

  # High-resolution custom output
  brainviz_dk --in brain.nii.gz --out plot.png --plot-type surface \\
              --view lateral --hemi left --dpi 600 --format png

  VOLUMETRIC PLOTTING:
  # Orthogonal slices
  brainviz_dk --in brain.nii.gz --out slices.png --plot-type volume \\
              --display-mode ortho --template mni152

  # Glass brain
  brainviz_dk --in brain.nii.gz --out glass.png --plot-type glass-brain \\
              --dpi 600 --colormap hot

  # Mosaic view (20 axial slices)
  brainviz_dk --in brain.nii.gz --out mosaic.png --plot-type mosaic \\
              --display-mode z --n-slices 20

  3D INTERACTIVE:
  # Interactive 3D in browser
  brainviz_dk --in brain.nii.gz --out plots/ --plot-type 3d

  # Save to HTML
  brainviz_dk --in brain.nii.gz --out brain.html --plot-type 3d

  UTILITIES:
  # List quality presets
  brainviz_dk --list-presets

  # List available templates
  brainviz_dk --list-templates
        """,
    )

    # === MAIN OPTIONS ===
    main_group = parser.add_argument_group("Main Options")
    main_group.add_argument(
        "--in", dest="nifti_path",
        help="Path to input NIfTI file (.nii or .nii.gz)",
    )
    main_group.add_argument(
        "--out", dest="output_path",
        help="Output file or directory path",
    )
    main_group.add_argument(
        "--plot-type", dest="plot_type",
        choices=["surface", "volume", "glass-brain", "mosaic", "roi", "3d"],
        default="surface",
        help="Type of plot to generate (default: surface)",
    )

    # === UTILITY OPTIONS ===
    utility_group = parser.add_argument_group("Utility Commands")
    utility_group.add_argument(
        "--list-presets", action="store_true",
        help="List available quality presets and exit",
    )
    utility_group.add_argument(
        "--list-templates", action="store_true",
        help="List available brain templates and exit",
    )

    # === SURFACE PLOTTING OPTIONS ===
    surface_group = parser.add_argument_group("Surface Plotting Options")
    surface_group.add_argument(
        "--view", dest="view",
        choices=["lateral", "medial", "dorsal", "ventral", "anterior", "posterior"],
        help="View angle (for single surface plot)",
    )
    surface_group.add_argument(
        "--views", dest="views",
        help="Comma-separated views (e.g., 'lateral,medial')",
    )
    surface_group.add_argument(
        "--all-views", action="store_true",
        help="Generate all 6 standard views per hemisphere",
    )
    surface_group.add_argument(
        "--hemi", dest="hemi",
        choices=["left", "right", "lh", "rh", "both"],
        default="both",
        help="Hemisphere(s) to plot (default: both)",
    )
    surface_group.add_argument(
        "--surface", dest="surface",
        choices=["pial", "inflated", "white", "sphere"],
        default="pial",
        help="Surface type (default: pial)",
    )
    surface_group.add_argument(
        "--mesh", dest="mesh",
        choices=["fsaverage", "fsaverage5", "fsaverage6"],
        default="fsaverage",
        help="Surface mesh resolution (default: fsaverage)",
    )

    # === VOLUMETRIC PLOTTING OPTIONS ===
    volumetric_group = parser.add_argument_group("Volumetric Plotting Options")
    volumetric_group.add_argument(
        "--template", dest="template",
        default="mni152",
        help="Background template (default: mni152)",
    )
    volumetric_group.add_argument(
        "--display-mode", dest="display_mode",
        choices=["ortho", "x", "y", "z", "yx", "xz", "yz", "lyrz", "lr"],
        default="ortho",
        help="Display mode for volumetric plots (default: ortho)",
    )
    volumetric_group.add_argument(
        "--cut-coords", dest="cut_coords",
        type=int,
        help="Number of slices or specific coordinates",
    )
    volumetric_group.add_argument(
        "--n-slices", dest="n_slices",
        type=int,
        default=12,
        help="Number of slices for mosaic view (default: 12)",
    )

    # === QUALITY OPTIONS ===
    quality_group = parser.add_argument_group("Quality & Output Options")
    quality_group.add_argument(
        "--quality", dest="quality_preset",
        choices=["draft", "standard", "publication", "print"],
        help="Quality preset (overrides dpi, format, mesh settings)",
    )
    quality_group.add_argument(
        "--dpi", dest="dpi",
        type=int,
        help="Output resolution in DPI (default: 300)",
    )
    quality_group.add_argument(
        "--format", dest="output_format",
        choices=["png", "svg", "pdf", "eps"],
        help="Output format (auto-detected from filename if not specified)",
    )
    quality_group.add_argument(
        "--figsize", dest="figsize",
        help="Figure size as 'width,height' in inches (e.g., '10,8')",
    )

    # === STYLE OPTIONS ===
    style_group = parser.add_argument_group("Style Options")
    style_group.add_argument(
        "--colormap", dest="colormap",
        default="hot",
        help="Colormap name (default: hot)",
    )
    style_group.add_argument(
        "--threshold", dest="threshold",
        type=float,
        help="Value threshold for display",
    )
    style_group.add_argument(
        "--black-bg", dest="black_bg",
        action="store_true",
        help="Use black background (for volumetric plots)",
    )

    # === GENERAL OPTIONS ===
    general_group = parser.add_argument_group("General Options")
    general_group.add_argument(
        "--prefix", dest="prefix",
        help="Filename prefix for batch outputs",
    )
    general_group.add_argument(
        "--verbose", "-v", action="store_true",
        help="Verbose output",
    )
    general_group.add_argument(
        "--version", action="version",
        version="BrainViz_DK 0.1.0",
    )

    args = parser.parse_args()

    # Handle utility commands
    if args.list_presets:
        list_quality_presets()
        return 0

    if args.list_templates:
        list_available_templates()
        return 0

    # Validate required arguments
    if not args.nifti_path:
        parser.error("--in is required (use --list-presets or --list-templates for utility commands)")

    if not args.output_path:
        parser.error("--out is required")

    # Validate input file exists
    if not os.path.exists(args.nifti_path):
        print(f"❌ Error: Input file not found: {args.nifti_path}", file=sys.stderr)
        return 1

    # Parse quality preset if provided
    plot_kwargs = {}
    if args.quality_preset:
        if args.verbose:
            print(f"Using quality preset: {args.quality_preset}")
        plot_kwargs.update(get_quality_preset(args.quality_preset))

    # Override with explicit arguments
    if args.dpi:
        plot_kwargs['dpi'] = args.dpi
    if args.output_format:
        plot_kwargs['output_format'] = args.output_format
    if args.figsize:
        try:
            w, h = map(float, args.figsize.split(','))
            plot_kwargs['figsize'] = (w, h)
        except ValueError:
            print(f"❌ Error: Invalid figsize format. Use 'width,height' (e.g., '10,8')", file=sys.stderr)
            return 1
    if args.threshold:
        plot_kwargs['threshold'] = args.threshold

    # Ensure output directory exists (for batch modes)
    out_path = Path(args.output_path)
    if args.plot_type in ["surface"] and (args.all_views or args.views):
        os.makedirs(args.output_path, exist_ok=True)
    elif out_path.suffix == '':
        os.makedirs(args.output_path, exist_ok=True)
    else:
        os.makedirs(out_path.parent, exist_ok=True)

    # === EXECUTE PLOTTING ===
    try:
        if args.plot_type == "surface":
            exit_code = handle_surface_plotting(args, plot_kwargs)
        elif args.plot_type == "volume":
            exit_code = handle_volumetric_plotting(args, plot_kwargs)
        elif args.plot_type == "glass-brain":
            exit_code = handle_glass_brain(args, plot_kwargs)
        elif args.plot_type == "mosaic":
            exit_code = handle_mosaic(args, plot_kwargs)
        elif args.plot_type == "roi":
            exit_code = handle_roi_overlay(args, plot_kwargs)
        elif args.plot_type == "3d":
            exit_code = handle_3d_interactive(args, plot_kwargs)
        else:
            print(f"❌ Unknown plot type: {args.plot_type}", file=sys.stderr)
            exit_code = 1

        return exit_code

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def handle_surface_plotting(args, plot_kwargs):
    """Handle surface plotting commands."""
    # Map hemisphere arguments
    hemis_map = {
        "both": ("lh", "rh"),
        "lh": ("lh",),
        "rh": ("rh",),
        "left": ("lh",),
        "right": ("rh",),
    }
    hemis = hemis_map[args.hemi]

    # Determine what to plot
    if args.all_views:
        # Generate all standard views
        if args.verbose:
            print("Generating all standard neuroimaging views...")

        outputs = generate_all_standard_views(
            args.nifti_path,
            args.output_path,
            mesh=args.mesh,
            surface_name=args.surface,
            colormap=args.colormap,
            prefix=args.prefix,
            **plot_kwargs,
        )

        print(f"✓ Generated {len(outputs)} views:")
        for out in outputs:
            print(f"  • {out}")

    elif args.views:
        # Generate custom views
        views = tuple(v.strip() for v in args.views.split(",") if v.strip())
        if args.verbose:
            print(f"Generating views: {', '.join(views)}")

        outputs = generate_four_views(
            args.nifti_path,
            args.output_path,
            hemis=hemis,
            views=views,
            mesh=args.mesh,
            surface_name=args.surface,
            colormap=args.colormap,
            prefix=args.prefix,
            **plot_kwargs,
        )

        print(f"✓ Generated {len(outputs)} plots:")
        for out in outputs:
            print(f"  • {out}")

    elif args.view:
        # Single view plot
        if args.verbose:
            print(f"Generating single view: {args.view} ({args.hemi})")

        # For single view, need to specify hemisphere
        if args.hemi == "both":
            print("⚠️  Warning: Using --view with --hemi both. Defaulting to left hemisphere.")
            hemi = "lh"
        else:
            hemi = "lh" if args.hemi in ("lh", "left") else "rh"

        output = plot_nifti(
            args.nifti_path,
            args.output_path,
            hemi=hemi,
            view=args.view,
            mesh=args.mesh,
            surface_name=args.surface,
            colormap=args.colormap,
            **plot_kwargs,
        )

        print(f"✓ Generated: {output}")

    else:
        # Default: generate standard 4 views
        if args.verbose:
            print("Generating default views (lateral, medial, dorsal, ventral)...")

        outputs = generate_four_views(
            args.nifti_path,
            args.output_path,
            hemis=hemis,
            views=("lateral", "medial", "dorsal", "ventral"),
            mesh=args.mesh,
            surface_name=args.surface,
            colormap=args.colormap,
            prefix=args.prefix,
            **plot_kwargs,
        )

        print(f"✓ Generated {len(outputs)} plots:")
        for out in outputs:
            print(f"  • {out}")

    return 0


def handle_volumetric_plotting(args, plot_kwargs):
    """Handle volumetric slice plotting."""
    if args.verbose:
        print(f"Generating volumetric slices (mode: {args.display_mode})...")

    output = plot_volumetric_slices(
        args.nifti_path,
        args.output_path,
        template=args.template,
        display_mode=args.display_mode,
        cut_coords=args.cut_coords,
        colormap=args.colormap,
        black_bg=args.black_bg,
        **plot_kwargs,
    )

    print(f"✓ Generated: {output}")
    return 0


def handle_glass_brain(args, plot_kwargs):
    """Handle glass brain plotting."""
    if args.verbose:
        print(f"Generating glass brain (mode: {args.display_mode})...")

    output = plot_glass_brain(
        args.nifti_path,
        args.output_path,
        display_mode=args.display_mode,
        colormap=args.colormap,
        black_bg=args.black_bg,
        **plot_kwargs,
    )

    print(f"✓ Generated: {output}")
    return 0


def handle_mosaic(args, plot_kwargs):
    """Handle mosaic plotting."""
    if args.verbose:
        print(f"Generating mosaic view ({args.n_slices} slices)...")

    output = plot_mosaic(
        args.nifti_path,
        args.output_path,
        template=args.template,
        display_mode=args.display_mode,
        n_slices=args.n_slices,
        colormap=args.colormap,
        black_bg=args.black_bg,
        **plot_kwargs,
    )

    print(f"✓ Generated: {output}")
    return 0


def handle_roi_overlay(args, plot_kwargs):
    """Handle ROI overlay plotting."""
    if args.verbose:
        print(f"Generating ROI overlay...")

    output = plot_roi_overlay(
        args.nifti_path,
        args.output_path,
        template=args.template,
        display_mode=args.display_mode,
        cut_coords=args.cut_coords,
        colormap=args.colormap,
        black_bg=args.black_bg,
        **plot_kwargs,
    )

    print(f"✓ Generated: {output}")
    return 0


def handle_3d_interactive(args, plot_kwargs):
    """Handle 3D interactive plotting."""
    if args.verbose:
        print("Generating interactive 3D plot...")

    view = plot_3d_interactive(
        args.nifti_path,
        colormap=args.colormap,
        threshold=args.threshold,
    )

    # Check if output is HTML file or directory
    out_path = Path(args.output_path)
    if out_path.suffix in ['.html', '.htm']:
        # Save to specific HTML file
        view.save_as_html(str(out_path))
        print(f"✓ Saved interactive 3D HTML: {out_path}")
    else:
        # Save to directory
        html_file = out_path / "brain_3d.html"
        view.save_as_html(str(html_file))
        print(f"✓ Saved interactive 3D HTML: {html_file}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
