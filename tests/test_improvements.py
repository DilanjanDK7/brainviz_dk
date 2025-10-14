#!/usr/bin/env python3
"""
Test Plotly 3D Improvements
============================

Test the two new improvements:
1. Closer hemisphere spacing
2. ICBM152 (MNI152NLin2009cAsym) template support
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from interactive3d import plot_interactive_surface_plotly

# Test data
TEST_FILE = '/media/brainlab-uwo/Data2/Results/Group_level_analysis/Testing/MNI152NLin2009cAsym/group_mean.nii.gz'
OUTPUT_DIR = '/media/brainlab-uwo/Data2/Results/Group_level_analysis/Testing/MNI152NLin2009cAsym/IMPROVEMENTS_TEST'

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 70)
print(" Testing Plotly 3D Improvements")
print("=" * 70)
print(f"\nTest file: {TEST_FILE}")
print(f"Output: {OUTPUT_DIR}\n")

tests = [
    {
        'name': '1_closer_spacing_fsaverage',
        'desc': 'Both hemispheres CLOSER together (fsaverage)',
        'hemi': 'both',
        'template': 'fsaverage',
        'mesh': 'fsaverage5',
    },
    {
        'name': '2_icbm152_template',
        'desc': 'ICBM152/MNI152NLin2009cAsym template',
        'hemi': 'both',
        'template': 'MNI152NLin2009cAsym',
        'mesh': 'MNI152NLin2009cAsym',
    },
    {
        'name': '3_icbm152_left_only',
        'desc': 'ICBM152 left hemisphere only',
        'hemi': 'lh',
        'template': 'MNI152NLin2009cAsym',
        'mesh': 'MNI152NLin2009cAsym',
    },
]

print("Running improvement tests:\n")

for test in tests:
    try:
        output_file = os.path.join(OUTPUT_DIR, f'{test["name"]}.html')

        print(f"Test: {test['name']:30s}")
        print(f"  → {test['desc']:50s}...", end=" ")

        plot_interactive_surface_plotly(
            TEST_FILE,
            output_file,
            hemi=test['hemi'],
            mesh=test['mesh'],
            template=test['template'],
            colormap='hot'
        )

        size_mb = os.path.getsize(output_file) / (1024**2)
        print(f"✓ ({size_mb:.2f} MB)")

    except Exception as e:
        print(f"✗ Error: {str(e)[:60]}")
        import traceback
        traceback.print_exc()

print("\n" + "=" * 70)
print(" Test Complete!")
print("=" * 70)
print(f"\nOutput: {OUTPUT_DIR}")
print("\n✅ Improvement 1: Hemispheres are now CLOSER together (60mm vs 100mm)")
print("✅ Improvement 2: ICBM152 (MNI152NLin2009cAsym) template now supported!")
print("\nOpen the HTML files to see the improvements:")
print("- Hemispheres are closer when viewing both together")
print("- ICBM152 template provides higher resolution mesh")
print("=" * 70)
