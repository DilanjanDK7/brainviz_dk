#!/usr/bin/env python3
"""
Test Plotly Interactive 3D Viewer
==================================

Test the new Plotly-based 3D interactive viewer with sample data.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from interactive3d import plot_interactive_surface_plotly

# Test data
TEST_FILE = '/media/brainlab-uwo/Data2/Results/Group_level_analysis/Testing/MNI152NLin2009cAsym/group_mean.nii.gz'
OUTPUT_DIR = '/media/brainlab-uwo/Data2/Results/Group_level_analysis/Testing/MNI152NLin2009cAsym/PLOTLY_3D_TEST'

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 70)
print(" Testing Plotly Interactive 3D Viewer")
print("=" * 70)
print(f"\nTest file: {TEST_FILE}")
print(f"Output: {OUTPUT_DIR}\n")

# Test configurations
tests = [
    {
        'name': 'both_hemispheres',
        'desc': 'Both hemispheres side-by-side',
        'hemi': 'both',
        'camera': None  # Default view
    },
    {
        'name': 'left_hemisphere',
        'desc': 'Left hemisphere only',
        'hemi': 'lh',
        'camera': None
    },
    {
        'name': 'dorsal_view',
        'desc': 'Initial dorsal (top-down) view',
        'hemi': 'both',
        'camera': {'eye': {'x': 0, 'y': 0, 'z': 2.5}}  # Looking from above
    },
]

print("Running tests:\n")

for test in tests:
    try:
        output_file = os.path.join(OUTPUT_DIR, f'{test["name"]}.html')

        print(f"Test: {test['name']:20s} - {test['desc']:40s}...", end=" ")

        plot_interactive_surface_plotly(
            TEST_FILE,
            output_file,
            hemi=test['hemi'],
            mesh='fsaverage5',  # Use fsaverage5 for faster testing
            colormap='hot',
            initial_camera=test['camera']
        )

        size_mb = os.path.getsize(output_file) / (1024**2)
        print(f"✓ ({size_mb:.2f} MB)")

    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()

print("\n" + "=" * 70)
print(" Test Complete!")
print("=" * 70)
print(f"\nOutput: {OUTPUT_DIR}")
print("\nOpen the HTML files in a browser to interact!")
print("- Drag with mouse to rotate")
print("- Scroll to zoom")
print("- Right-click drag to pan")
print("\nYou can rotate to ANY angle, including perfect dorsal view!")
print("=" * 70)
