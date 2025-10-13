#!/usr/bin/env python3
"""
Example: Batch process multiple neuroimaging features with BrainViz

This script demonstrates how to use BrainViz to generate plots for
multiple features (ALFF, fALFF, ReHo, etc.) in batch.
"""

import sys
import os

# Add parent directory to path to import brainviz
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brainviz_dk import generate_four_views


def main():
    # Base directory for your data
    base_dir = "/media/brainlab-uwo/Data2/Results/Group_level_analysis/ds002748"
    
    # Define features to process
    features = [
        {
            "name": "ALFF",
            "nifti": f"{base_dir}/alff/whole_brain/MNI152NLin2009cAsym/group_mean.nii.gz",
            "output": f"{base_dir}/Plots_BrainViz_Demo/ALFF/",
        },
        {
            "name": "fALFF",
            "nifti": f"{base_dir}/falff/whole_brain/MNI152NLin2009cAsym/group_mean.nii.gz",
            "output": f"{base_dir}/Plots_BrainViz_Demo/fALFF/",
        },
        {
            "name": "ReHo",
            "nifti": f"{base_dir}/reho/whole_brain/MNI152NLin2009cAsym/group_mean.nii.gz",
            "output": f"{base_dir}/Plots_BrainViz_Demo/ReHo/",
        },
        {
            "name": "Hurst",
            "nifti": f"{base_dir}/hurst/whole_brain/MNI152NLin2009cAsym/group_mean.nii.gz",
            "output": f"{base_dir}/Plots_BrainViz_Demo/Hurst/",
        },
        {
            "name": "Simple_Fourier",
            "nifti": f"{base_dir}/simple_fourier/whole_brain/MNI152NLin2009cAsym/group_mean.nii.gz",
            "output": f"{base_dir}/Plots_BrainViz_Demo/Simple_Fourier/",
        },
        {
            "name": "QIE",
            "nifti": f"{base_dir}/qie/whole_brain/MNI152NLin2009cAsym/group_mean.nii.gz",
            "output": f"{base_dir}/Plots_BrainViz_Demo/QIE/",
        },
    ]
    
    print("="*70)
    print("BrainViz Batch Processing Example")
    print("="*70)
    
    for idx, feature in enumerate(features, 1):
        print(f"\n[{idx}/{len(features)}] Processing {feature['name']}...")
        print(f"  Input:  {feature['nifti']}")
        print(f"  Output: {feature['output']}")
        
        if not os.path.exists(feature['nifti']):
            print(f"  ✗ SKIPPED: File not found")
            continue
        
        try:
            outputs = generate_four_views(
                feature['nifti'],
                feature['output'],
                hemis=("lh", "rh"),
                views=("lateral", "medial", "dorsal", "ventral"),
                mesh="fsaverage",
                surface_name="pial",
                colormap="jet",
                prefix=f"{feature['name'].lower()}_group_mean"
            )
            print(f"  ✓ SUCCESS: Generated {len(outputs)} plots")
            
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*70)
    print("Batch processing complete!")
    print("="*70)


if __name__ == "__main__":
    main()

