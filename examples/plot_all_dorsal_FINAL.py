#!/usr/bin/env python3
"""
Plot ALL Testing Files - True Dorsal (Top-Down) View
=====================================================

Uses glass brain visualization which shows true top-down view.
This is what you need for dorsal/top view debugging.
"""

import os
import glob
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from volumetric import plot_glass_brain

# Configuration
DATA_DIR = '/media/brainlab-uwo/Data2/Results/Group_level_analysis/Testing/MNI152NLin2009cAsym'
OUTPUT_DIR = os.path.join(DATA_DIR, 'DORSAL_FINAL')

print("=" * 70)
print(" TRUE DORSAL (TOP-DOWN) VIEW - Glass Brain")
print("=" * 70)
print(f"\nData: {DATA_DIR}")
print(f"Output: {OUTPUT_DIR}")
print("\nUsing glass brain with display_mode='z' for true top-down view\n")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Get all files
nifti_files = sorted(glob.glob(f'{DATA_DIR}/*.nii.gz'))
print(f"Found {len(nifti_files)} files\n")

successful = 0
failed = []

for idx, nifti_file in enumerate(nifti_files, 1):
    basename = os.path.basename(nifti_file).replace('.nii.gz', '')
    print(f"[{idx}/{len(nifti_files)}] {basename}...", end=" ")

    try:
        output = os.path.join(OUTPUT_DIR, f'{basename}_DORSAL_topdown.png')

        # Glass brain with z-axis = shows brain from above (dorsal view)
        plot_glass_brain(
            nifti_file,
            output,
            display_mode='z',  # z = axial = top-down
            colormap='hot',
            black_bg=False,
            dpi=300
        )

        size_kb = os.path.getsize(output) / 1024
        print(f"✓ ({size_kb:.0f} KB)")
        successful += 1

    except Exception as e:
        print(f"✗ {str(e)[:50]}")
        failed.append((basename, str(e)))

print("\n" + "=" * 70)
print(f" SUCCESS: {successful}/{len(nifti_files)} plots created")
print("=" * 70)

if failed:
    print("\nFailed:")
    for name, err in failed:
        print(f"  - {name}: {err[:50]}")

print(f"\n✓ Output: {OUTPUT_DIR}")
print("\nThese are TRUE TOP-DOWN (DORSAL) views showing the brain from above.")
print("=" * 70)
