#!/usr/bin/env python3
"""
Batch process NIfTI files in the Testing directory using BrainViz_DK.

This script will generate brain visualizations for all NIfTI files found in
/media/brainlab-uwo/Data2/Results/Group_level_analysis/Testing/MNI152NLin2009cAsym/
"""

import os
import sys
from pathlib import Path
from typing import List, Dict

# Add the current directory to Python path to import brainviz_dk
sys.path.insert(0, '/home/brainlab-uwo/PycharmProjects/brainviz_dk')

from brainviz_dk import (
    plot_nifti,
    generate_four_views,
    generate_all_standard_views,
    plot_3d_interactive,
    plot_volumetric_slices,
    plot_glass_brain,
    plot_mosaic
)
from brainviz_dk.logging_config import setup_logging, ProgressLogger


def main():
    """Main function to process all NIfTI files."""
    
    # Set up logging
    logger = setup_logging(verbose=True)
    progress = ProgressLogger(verbose=True)
    
    # Define paths
    input_dir = Path("/media/brainlab-uwo/Data2/Results/Group_level_analysis/Testing/MNI152NLin2009cAsym")
    output_dir = input_dir / "BrainViz_Plots"
    
    print("="*80)
    print("BrainViz_DK Batch Processing")
    print("="*80)
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")
    
    # Create output directory
    output_dir.mkdir(exist_ok=True)
    
    # Find all NIfTI files
    nifti_files = list(input_dir.glob("*.nii.gz"))
    print(f"\nFound {len(nifti_files)} NIfTI files:")
    for f in nifti_files:
        print(f"  • {f.name}")
    
    if not nifti_files:
        progress.error("No NIfTI files found!")
        return 1
    
    # Process each file
    results = []
    
    for i, nifti_file in enumerate(nifti_files, 1):
        print(f"\n{'='*60}")
        print(f"[{i}/{len(nifti_files)}] Processing: {nifti_file.name}")
        print(f"{'='*60}")
        
        file_results = process_nifti_file(nifti_file, output_dir, progress)
        results.append({
            'file': nifti_file.name,
            'results': file_results
        })
    
    # Print summary
    print(f"\n{'='*80}")
    print("PROCESSING COMPLETE!")
    print(f"{'='*80}")
    
    total_plots = sum(len(r['results']) for r in results)
    print(f"Total plots generated: {total_plots}")
    print(f"Output directory: {output_dir}")
    
    print(f"\nGenerated plots:")
    for result in results:
        print(f"\n📊 {result['file']}:")
        for plot_result in result['results']:
            status = "✓" if plot_result['success'] else "✗"
            print(f"  {status} {plot_result['type']}: {plot_result['output']}")
    
    return 0


def process_nifti_file(nifti_file: Path, output_dir: Path, progress: ProgressLogger) -> List[Dict]:
    """Process a single NIfTI file and generate multiple plot types."""
    
    results = []
    base_name = nifti_file.stem.replace('.nii', '')
    
    # 1. Single surface view (left hemisphere lateral)
    try:
        progress.info(f"Generating single surface view...")
        output_path = output_dir / f"{base_name}_lh_lateral.png"
        
        plot_nifti(
            str(nifti_file),
            str(output_path),
            hemi="lh",
            view="lateral",
            mesh="fsaverage",
            surface_name="pial",
            colormap="jet",
            dpi=300
        )
        
        results.append({
            'type': 'Surface (LH Lateral)',
            'output': str(output_path),
            'success': True
        })
        progress.success(f"Surface plot: {output_path.name}")
        
    except Exception as e:
        results.append({
            'type': 'Surface (LH Lateral)',
            'output': str(output_path),
            'success': False,
            'error': str(e)
        })
        progress.error(f"Surface plot failed: {e}")
    
    # 2. Four standard views (both hemispheres)
    try:
        progress.info(f"Generating four standard views...")
        four_views_dir = output_dir / f"{base_name}_four_views"
        
        outputs = generate_four_views(
            str(nifti_file),
            str(four_views_dir),
            hemis=("lh", "rh"),
            views=("lateral", "medial", "dorsal", "ventral"),
            mesh="fsaverage",
            surface_name="pial",
            colormap="jet",
            prefix=base_name,
            dpi=300
        )
        
        results.append({
            'type': 'Four Views (8 plots)',
            'output': f"{four_views_dir} ({len(outputs)} files)",
            'success': True
        })
        progress.success(f"Four views: {len(outputs)} plots in {four_views_dir.name}")
        
    except Exception as e:
        results.append({
            'type': 'Four Views',
            'output': str(four_views_dir),
            'success': False,
            'error': str(e)
        })
        progress.error(f"Four views failed: {e}")
    
    # 3. All standard views (12 plots)
    try:
        progress.info(f"Generating all standard views...")
        all_views_dir = output_dir / f"{base_name}_all_views"
        
        outputs = generate_all_standard_views(
            str(nifti_file),
            str(all_views_dir),
            mesh="fsaverage",
            surface_name="pial",
            colormap="jet",
            prefix=base_name,
            dpi=300
        )
        
        results.append({
            'type': 'All Standard Views (12 plots)',
            'output': f"{all_views_dir} ({len(outputs)} files)",
            'success': True
        })
        progress.success(f"All views: {len(outputs)} plots in {all_views_dir.name}")
        
    except Exception as e:
        results.append({
            'type': 'All Standard Views',
            'output': str(all_views_dir),
            'success': False,
            'error': str(e)
        })
        progress.error(f"All views failed: {e}")
    
    # 4. Volumetric slices
    try:
        progress.info(f"Generating volumetric slices...")
        output_path = output_dir / f"{base_name}_volumetric_slices.png"
        
        plot_volumetric_slices(
            str(nifti_file),
            str(output_path),
            template="mni152",
            display_mode="ortho",
            colormap="hot",
            dpi=300
        )
        
        results.append({
            'type': 'Volumetric Slices',
            'output': str(output_path),
            'success': True
        })
        progress.success(f"Volumetric slices: {output_path.name}")
        
    except Exception as e:
        results.append({
            'type': 'Volumetric Slices',
            'output': str(output_path),
            'success': False,
            'error': str(e)
        })
        progress.error(f"Volumetric slices failed: {e}")
    
    # 5. Glass brain
    try:
        progress.info(f"Generating glass brain...")
        output_path = output_dir / f"{base_name}_glass_brain.png"
        
        plot_glass_brain(
            str(nifti_file),
            str(output_path),
            display_mode="lyrz",
            colormap="hot",
            dpi=600
        )
        
        results.append({
            'type': 'Glass Brain',
            'output': str(output_path),
            'success': True
        })
        progress.success(f"Glass brain: {output_path.name}")
        
    except Exception as e:
        results.append({
            'type': 'Glass Brain',
            'output': str(output_path),
            'success': False,
            'error': str(e)
        })
        progress.error(f"Glass brain failed: {e}")
    
    # 6. Interactive 3D HTML
    try:
        progress.info(f"Generating interactive 3D plot...")
        html_path = output_dir / f"{base_name}_interactive_3d.html"
        
        view = plot_3d_interactive(
            str(nifti_file),
            colormap="jet",
            title=f"{base_name} - Interactive 3D"
        )
        view.save_as_html(str(html_path))
        
        results.append({
            'type': 'Interactive 3D HTML',
            'output': str(html_path),
            'success': True
        })
        progress.success(f"Interactive 3D: {html_path.name}")
        
    except Exception as e:
        results.append({
            'type': 'Interactive 3D HTML',
            'output': str(html_path),
            'success': False,
            'error': str(e)
        })
        progress.error(f"Interactive 3D failed: {e}")
    
    return results


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Processing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
