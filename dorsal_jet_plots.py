#!/usr/bin/env python3
"""
Generate dorsal view plots with Jet color scheme for all NIfTI files.

This script will create dorsal view brain visualizations for all NIfTI files found in
/media/brainlab-uwo/Data2/Results/Group_level_analysis/Testing/MNI152NLin2009cAsym/
using the Jet color scheme.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict

# Add the current directory to Python path to import brainviz_dk
sys.path.insert(0, '/home/brainlab-uwo/PycharmProjects/brainviz_dk')

from brainviz_dk import plot_nifti
from brainviz_dk.logging_config import setup_logging, ProgressLogger


def main():
    """Main function to process all NIfTI files for dorsal views."""
    
    # Set up logging
    logger = setup_logging(verbose=True)
    progress = ProgressLogger(verbose=True)
    
    # Define paths
    input_dir = Path("/media/brainlab-uwo/Data2/Results/Group_level_analysis/Testing/MNI152NLin2009cAsym")
    output_dir = input_dir / "BrainViz_Dorsal_Jet"
    
    print("="*80)
    print("BrainViz_DK - Dorsal View with Jet Color Scheme")
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
    
    # Process each file for dorsal views (both hemispheres)
    results = []
    
    for i, nifti_file in enumerate(nifti_files, 1):
        print(f"\n{'='*60}")
        print(f"[{i}/{len(nifti_files)}] Processing: {nifti_file.name}")
        print(f"{'='*60}")
        
        file_results = process_nifti_file_dorsal(nifti_file, output_dir, progress)
        results.append({
            'file': nifti_file.name,
            'results': file_results
        })
    
    # Print summary
    print(f"\n{'='*80}")
    print("DORSAL VIEW PROCESSING COMPLETE!")
    print(f"{'='*80}")
    
    total_plots = sum(len(r['results']) for r in results)
    print(f"Total dorsal plots generated: {total_plots}")
    print(f"Output directory: {output_dir}")
    
    print(f"\nGenerated dorsal plots:")
    for result in results:
        print(f"\n📊 {result['file']}:")
        for plot_result in result['results']:
            status = "✓" if plot_result['success'] else "✗"
            print(f"  {status} {plot_result['type']}: {plot_result['output']}")
    
    return 0


def process_nifti_file_dorsal(nifti_file: Path, output_dir: Path, progress: ProgressLogger) -> List[Dict]:
    """Process a single NIfTI file and generate dorsal view plots for both hemispheres."""
    
    results = []
    base_name = nifti_file.stem.replace('.nii', '')
    
    # Generate dorsal view for left hemisphere
    try:
        progress.info(f"Generating dorsal view (LH)...")
        output_path = output_dir / f"{base_name}_lh_dorsal.png"
        
        plot_nifti(
            str(nifti_file),
            str(output_path),
            hemi="lh",
            view="dorsal",
            mesh="fsaverage",
            surface_name="pial",
            colormap="jet",
            dpi=300
        )
        
        results.append({
            'type': 'Dorsal (LH)',
            'output': str(output_path),
            'success': True
        })
        progress.success(f"Dorsal LH: {output_path.name}")
        
    except Exception as e:
        results.append({
            'type': 'Dorsal (LH)',
            'output': str(output_path),
            'success': False,
            'error': str(e)
        })
        progress.error(f"Dorsal LH failed: {e}")
    
    # Generate dorsal view for right hemisphere
    try:
        progress.info(f"Generating dorsal view (RH)...")
        output_path = output_dir / f"{base_name}_rh_dorsal.png"
        
        plot_nifti(
            str(nifti_file),
            str(output_path),
            hemi="rh",
            view="dorsal",
            mesh="fsaverage",
            surface_name="pial",
            colormap="jet",
            dpi=300
        )
        
        results.append({
            'type': 'Dorsal (RH)',
            'output': str(output_path),
            'success': True
        })
        progress.success(f"Dorsal RH: {output_path.name}")
        
    except Exception as e:
        results.append({
            'type': 'Dorsal (RH)',
            'output': str(output_path),
            'success': False,
            'error': str(e)
        })
        progress.error(f"Dorsal RH failed: {e}")
    
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
