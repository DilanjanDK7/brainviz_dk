import argparse
import os
from .plot import generate_four_views, generate_all_standard_views, plot_3d_interactive


def main():
    p = argparse.ArgumentParser(
        description="BrainViz: Lightweight 3D brain plotting (no MNE)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate all standard views (lateral, medial, dorsal, ventral, anterior, posterior)
  python -m brainviz --in map.nii.gz --out ./plots --all-views
  
  # Generate custom views
  python -m brainviz --in map.nii.gz --out ./plots --views lateral,medial
  
  # Generate 3D interactive HTML
  python -m brainviz --in map.nii.gz --out ./plots --3d --html plot.html
  
  # Different colormap and surface
  python -m brainviz --in map.nii.gz --out ./plots --colormap hot --surface inflated
        """
    )
    
    # Required arguments
    p.add_argument("--in", dest="nifti_path", required=True, 
                   help="Path to NIfTI .nii or .nii.gz")
    p.add_argument("--out", dest="out_dir", required=True, 
                   help="Output directory for PNGs (or HTML with --html)")
    
    # View options
    view_group = p.add_mutually_exclusive_group()
    view_group.add_argument("--all-views", action="store_true",
                           help="Generate all standard neuroimaging views (lateral, medial, dorsal, ventral, anterior, posterior)")
    view_group.add_argument("--views", default="lateral,medial,dorsal,ventral",
                           help="Comma-separated list of views (default: lateral,medial,dorsal,ventral)")
    
    # 3D options
    p.add_argument("--3d", dest="interactive_3d", action="store_true",
                   help="Generate interactive 3D plot (opens in browser)")
    p.add_argument("--html", dest="html_output", default=None,
                   help="Save interactive 3D plot to HTML file (requires --3d)")
    
    # Style options
    p.add_argument("--colormap", default="jet", 
                   help="Matplotlib colormap (default: jet)")
    p.add_argument("--mesh", default="fsaverage", 
                   choices=["fsaverage", "fsaverage5"], 
                   help="Surface mesh resolution (default: fsaverage)")
    p.add_argument("--surface", default="pial", 
                   choices=["pial", "inflated", "white", "sphere"], 
                   help="Surface type (default: pial)")
    
    # Hemisphere options
    p.add_argument("--hemi", default="both", 
                   choices=["both", "lh", "rh", "left", "right"], 
                   help="Hemispheres to render (default: both)")
    
    # Output options
    p.add_argument("--prefix", default=None, 
                   help="Filename prefix for output files")
    p.add_argument("--verbose", "-v", action="store_true",
                   help="Verbose output")
    
    args = p.parse_args()

    # Ensure output directory exists
    os.makedirs(args.out_dir, exist_ok=True)
    
    # Handle 3D interactive plotting
    if args.interactive_3d:
        if args.verbose:
            print(f"Generating interactive 3D plot...")
        
        view = plot_3d_interactive(
            args.nifti_path,
            colormap=args.colormap,
        )
        
        if args.html_output:
            html_path = os.path.join(args.out_dir, args.html_output)
            view.save_as_html(html_path)
            print(f"✓ Saved interactive 3D HTML: {html_path}")
        else:
            print("Opening interactive 3D plot in browser...")
            view.open_in_browser()
        return
    
    # Handle static plotting
    hemis_map = {
        "both": ("lh", "rh"),
        "lh": ("lh",),
        "rh": ("rh",),
        "left": ("lh",),
        "right": ("rh",),
    }
    hemis = hemis_map[args.hemi]
    
    if args.all_views:
        if args.verbose:
            print("Generating all standard neuroimaging views...")
        outputs = generate_all_standard_views(
            args.nifti_path,
            args.out_dir,
            mesh=args.mesh,
            surface_name=args.surface,
            colormap=args.colormap,
            prefix=args.prefix,
        )
    else:
        views = tuple(v.strip() for v in args.views.split(",") if v.strip())
        if args.verbose:
            print(f"Generating views: {', '.join(views)}")
        outputs = generate_four_views(
            args.nifti_path,
            args.out_dir,
            hemis=hemis,
            views=views,
            mesh=args.mesh,
            surface_name=args.surface,
            colormap=args.colormap,
            prefix=args.prefix,
        )
    
    print(f"✓ Generated {len(outputs)} plots:")
    for out in outputs:
        print(f"  {out}")


if __name__ == "__main__":
    main()



