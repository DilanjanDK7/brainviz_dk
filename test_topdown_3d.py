#!/usr/bin/env python3
"""
Test Script: 3D Surface Top-Down View
======================================

Test custom elevation/azimuth angles to achieve true top-down 3D surface view.
We'll test different angle combinations to find the best top-down view.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from plot import project_volume_to_surface, _auto_scaling_from_img
import nibabel as nib
from nilearn import plotting
import matplotlib.pyplot as plt

# Test data
TEST_FILE = '/media/brainlab-uwo/Data2/Results/Group_level_analysis/Testing/MNI152NLin2009cAsym/group_mean.nii.gz'
OUTPUT_DIR = '/media/brainlab-uwo/Data2/Results/Group_level_analysis/Testing/MNI152NLin2009cAsym/topdown_3d_test'

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 70)
print(" Testing 3D Surface Top-Down View Angles")
print("=" * 70)
print(f"\nTest file: {TEST_FILE}")
print(f"Output: {OUTPUT_DIR}\n")

# Load and prepare data
img = nib.load(TEST_FILE)
vmin, vmax, threshold = _auto_scaling_from_img(img)

# Test different angle combinations
# Format: (name, elevation, azimuth)
test_angles = [
    ("topdown_90_0", 90, 0),      # Directly from above
    ("topdown_90_90", 90, 90),    # From above, rotated 90°
    ("topdown_90_180", 90, 180),  # From above, rotated 180°
    ("topdown_90_270", 90, 270),  # From above, rotated 270°
    ("topdown_80_0", 80, 0),      # Slightly angled
    ("topdown_85_45", 85, 45),    # Slight angle, rotated
]

print("Testing view angles for both hemispheres:\n")

for hemi in ['lh', 'rh']:
    print(f"\n{hemi.upper()} Hemisphere:")
    print("-" * 40)

    # Project to surface
    surf_mesh, sulc_map, texture = project_volume_to_surface(
        TEST_FILE,
        hemi=hemi,
        mesh='fsaverage',
        surface_name='pial',
    )

    for name, elev, azim in test_angles:
        try:
            output_file = os.path.join(OUTPUT_DIR, f'{name}_{hemi}.png')

            print(f"  Testing {name} (elev={elev}, azim={azim})...", end=" ")

            # Create figure with custom view angle
            fig = plotting.plot_surf_stat_map(
                surf_mesh,
                texture,
                bg_map=sulc_map,
                bg_on_data=True,
                hemi='left' if hemi == 'lh' else 'right',
                view=(elev, azim),  # Custom elevation and azimuth
                cmap='hot',
                colorbar=True,
                darkness=0.8,
                threshold=threshold,
                vmin=vmin,
                vmax=vmax,
                alpha=0.8,
            )

            fig.savefig(output_file, dpi=300, bbox_inches='tight')
            plt.close(fig)

            size_kb = os.path.getsize(output_file) / 1024
            print(f"✓ ({size_kb:.1f} KB)")

        except Exception as e:
            print(f"✗ Error: {str(e)[:50]}")

print("\n" + "=" * 70)
print(" Test Complete!")
print("=" * 70)
print(f"\nOutput directory: {OUTPUT_DIR}")
print("\nReview the images to determine which angle gives the best top-down view.")
print("The topdown_90_* variants should show the brain from directly above.")
print("=" * 70)
