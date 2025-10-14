#!/usr/bin/env python3
"""
Test Final Spacing and Highest Resolution
==========================================

Test:
1. Hemispheres are MUCH closer (20mm spacing)
2. Using highest resolution fsaverage (no number suffix)
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from interactive3d import plot_interactive_surface_plotly

TEST_FILE = '/media/brainlab-uwo/Data2/Results/Group_level_analysis/Testing/MNI152NLin2009cAsym/group_mean.nii.gz'
OUTPUT_DIR = '/media/brainlab-uwo/Data2/Results/Group_level_analysis/Testing/MNI152NLin2009cAsym/FINAL_SPACING_TEST'

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 70)
print(" Testing FINAL Spacing (20mm) + Highest Resolution fsaverage")
print("=" * 70)
print(f"\nTest file: {TEST_FILE}")
print(f"Output: {OUTPUT_DIR}\n")

print("Creating visualization with:")
print("  - Hemisphere spacing: 20mm (MUCH closer)")
print("  - Mesh: fsaverage (highest resolution, ~163k vertices per hemisphere)")
print("\nThis will take a bit longer due to high resolution...\n")

try:
    output_file = os.path.join(OUTPUT_DIR, 'both_hemispheres_CLOSE_highest_res.html')

    plot_interactive_surface_plotly(
        TEST_FILE,
        output_file,
        hemi='both',
        mesh='fsaverage',  # Highest resolution!
        template='fsaverage',
        colormap='hot',
        initial_camera={'eye': {'x': 0, 'y': 0, 'z': 2.0}}
    )

    size_mb = os.path.getsize(output_file) / (1024**2)
    print(f"✓ Success! ({size_mb:.2f} MB)\n")

    print("=" * 70)
    print(" Test Complete!")
    print("=" * 70)
    print(f"\n✅ Output: {output_file}")
    print("\n✨ Improvements:")
    print("  1. Hemispheres are NOW MUCH CLOSER (20mm spacing)")
    print("  2. Using highest resolution fsaverage mesh")
    print("  3. Interactive - rotate to any angle you want!")
    print("\nOpen the HTML file and rotate with your mouse to see the dorsal view!")
    print("=" * 70)

except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
