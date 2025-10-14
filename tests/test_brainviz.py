#!/usr/bin/env python3
"""
Test script for the brainviz package.
Generates sample plots to verify functionality.
"""

import os
import sys

from brainviz_dk import generate_four_views, plot_nifti
from test_config import test_config, get_test_nifti_path

def main():
    print("="*60)
    print("Testing BrainViz_DK Package")
    print("="*60)
    
    # Get test file
    test_nifti = get_test_nifti_path()
    if test_nifti is None:
        print("ERROR: No test data available.")
        print("Please set BRAINVIZ_TEST_DATA_DIR environment variable or place test data in test_data/")
        return 1
    
    output_dir = test_config.temp_dir / "Plots_BrainViz_Test"
    
    print(f"\nTest NIfTI: {test_nifti}")
    print(f"Output dir: {output_dir}")
    
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n" + "="*60)
    print("Test 1: Single view (left hemisphere lateral)")
    print("="*60)
    try:
        out_path = plot_nifti(
            str(test_nifti),
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
            str(test_nifti),
            str(output_dir),
            hemis=("lh", "rh"),
            views=("lateral", "medial", "dorsal", "ventral"),
            mesh="fsaverage",
            surface_name="pial",
            colormap="jet",
            prefix="test_group_mean",
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
            str(test_nifti),
            str(output_dir),
            hemis=("lh",),  # Just left hemisphere
            views=("lateral", "medial"),
            mesh="fsaverage",
            surface_name="pial",
            colormap="hot",
            prefix="test_group_mean_hot",
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
            str(test_nifti),
            str(output_dir),
            hemis=("lh",),
            views=("lateral",),
            mesh="fsaverage",
            surface_name="inflated",
            colormap="jet",
            prefix="test_group_mean_inflated",
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

