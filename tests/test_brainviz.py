#!/usr/bin/env python3
"""
Test script for the brainviz package.
Generates sample plots to verify functionality.
"""

import os
import sys

# Add current directory to path so we can import brainviz
sys.path.insert(0, '/media/brainlab-uwo/Data2/Results/Group_level_analysis/ds002748')

from brainviz_dk import generate_four_views, plot_nifti

def main():
    print("="*60)
    print("Testing BrainViz_DK Package")
    print("="*60)
    
    # Test file
    test_nifti = '/media/brainlab-uwo/Data2/Results/Group_level_analysis/ds002748/qie/whole_brain/MNI152NLin2009cAsym/group_mean.nii.gz'
    output_dir = '/media/brainlab-uwo/Data2/Results/Group_level_analysis/ds002748/Plots_BrainViz_Test'
    
    print(f"\nTest NIfTI: {test_nifti}")
    print(f"Output dir: {output_dir}")
    
    if not os.path.exists(test_nifti):
        print(f"ERROR: Test file not found: {test_nifti}")
        return 1
    
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n" + "="*60)
    print("Test 1: Single view (left hemisphere lateral)")
    print("="*60)
    try:
        out_path = plot_nifti(
            test_nifti,
            os.path.join(output_dir, "test_single_lh_lateral.png"),
            hemi="lh",
            view="lateral",
            colormap="jet",
            mesh="fsaverage",
            surface_name="pial",
        )
        print(f"✓ Success: {out_path}")
    except Exception as e:
        print(f"✗ Failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("\n" + "="*60)
    print("Test 2: Generate all four views (both hemispheres)")
    print("="*60)
    try:
        outputs = generate_four_views(
            test_nifti,
            output_dir,
            hemis=("lh", "rh"),
            views=("lateral", "medial", "dorsal", "ventral"),
            mesh="fsaverage",
            surface_name="pial",
            colormap="jet",
            prefix="qie_group_mean",
        )
        print(f"✓ Generated {len(outputs)} images:")
        for out in outputs:
            print(f"  - {out}")
    except Exception as e:
        print(f"✗ Failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("\n" + "="*60)
    print("Test 3: Different colormap (hot)")
    print("="*60)
    try:
        outputs = generate_four_views(
            test_nifti,
            output_dir,
            hemis=("lh",),  # Just left hemisphere
            views=("lateral", "medial"),
            mesh="fsaverage",
            surface_name="pial",
            colormap="hot",
            prefix="qie_group_mean_hot",
        )
        print(f"✓ Generated {len(outputs)} images with 'hot' colormap")
        for out in outputs:
            print(f"  - {out}")
    except Exception as e:
        print(f"✗ Failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("\n" + "="*60)
    print("Test 4: Different surface (inflated)")
    print("="*60)
    try:
        outputs = generate_four_views(
            test_nifti,
            output_dir,
            hemis=("lh",),
            views=("lateral",),
            mesh="fsaverage",
            surface_name="inflated",
            colormap="jet",
            prefix="qie_group_mean_inflated",
        )
        print(f"✓ Generated {len(outputs)} images with inflated surface")
        for out in outputs:
            print(f"  - {out}")
    except Exception as e:
        print(f"✗ Failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("\n" + "="*60)
    print("ALL TESTS PASSED!")
    print("="*60)
    print(f"\nCheck output directory: {output_dir}")
    
    return 0

if __name__ == "__main__":
    exit(main())

