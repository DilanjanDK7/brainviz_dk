#!/usr/bin/env python3
"""
Test Different Dorsal View Configurations
==========================================

Testing to find the best dorsal (top-down) view angle for 3D surface rendering.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from nilearn import plotting, datasets
import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np

# Test data
TEST_FILE = '/media/brainlab-uwo/Data2/Results/Group_level_analysis/Testing/MNI152NLin2009cAsym/group_mean.nii.gz'
OUTPUT_DIR = '/media/brainlab-uwo/Data2/Results/Group_level_analysis/Testing/MNI152NLin2009cAsym/dorsal_test_v2'

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 70)
print(" Testing Dorsal View Configurations")
print("=" * 70)
print(f"\nTest file: {TEST_FILE}")
print(f"Output: {OUTPUT_DIR}\n")

# Load data
img = nib.load(TEST_FILE)
data = np.asanyarray(img.get_fdata())
data = data[np.isfinite(data) & (data > 0)]
threshold = float(np.percentile(data, 10)) if data.size > 0 else 0
vmin = 0.0
vmax = float(np.percentile(data, 99)) if data.size > 0 else 1.0

print(f"Threshold: {threshold:.2f}, vmin: {vmin:.2f}, vmax: {vmax:.2f}\n")

# Get fsaverage
fsaverage = datasets.fetch_surf_fsaverage('fsaverage')

from nilearn import surface

# Test configurations
# Format: (name, description, hemisphere, view_param)
configs = [
    # Standard nilearn views
    ("standard_dorsal_lh", "Standard dorsal left", "left", "dorsal"),
    ("standard_dorsal_rh", "Standard dorsal right", "right", "dorsal"),

    # Custom angles - trying to find true top-down
    # Format: (elevation, azimuth)
    # elevation: 0=horizon, 90=top, -90=bottom
    # azimuth: 0=front, 90=right, 180=back, 270=left

    ("angle_90_0", "Elev=90, Azim=0 (straight down, front)", "left", (90, 0)),
    ("angle_90_180", "Elev=90, Azim=180 (straight down, back)", "left", (90, 180)),
    ("angle_70_0", "Elev=70, Azim=0 (angled, front)", "left", (70, 0)),
    ("angle_80_90", "Elev=80, Azim=90 (angled, side)", "left", (80, 90)),
    ("angle_85_0", "Elev=85, Azim=0 (nearly top, front)", "left", (85, 0)),
]

print("Generating test views:\n")

for name, description, hemi, view_param in configs:
    try:
        output_file = os.path.join(OUTPUT_DIR, f'{name}.png')
        print(f"  {name:25s} - {description:40s}...", end=" ")

        # Project to surface
        surf_mesh = fsaverage.pial_left if hemi == "left" else fsaverage.pial_right
        sulc_map = fsaverage.sulc_left if hemi == "left" else fsaverage.sulc_right

        texture = surface.vol_to_surf(
            img,
            surf_mesh,
            radius=2.0,
            interpolation='linear'
        )

        # Plot
        fig = plotting.plot_surf_stat_map(
            surf_mesh,
            texture,
            bg_map=sulc_map,
            bg_on_data=True,
            hemi=hemi,
            view=view_param,
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
        print(f"✓ ({size_kb:.0f} KB)")

    except Exception as e:
        print(f"✗ {str(e)[:40]}")

print("\n" + "=" * 70)
print(" Test Complete!")
print("=" * 70)
print(f"\nOutput: {OUTPUT_DIR}")
print("\nPlease review the images to see which angle gives you the")
print("dorsal (top-down) view you need.")
print("=" * 70)
