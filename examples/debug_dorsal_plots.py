#!/usr/bin/env python3
"""
Debug Script: Plot Dorsal View of All Testing Data
===================================================

This script plots the dorsal (top) view of all NIfTI files in the testing directory
for debugging purposes.

Output: Saves plots to a 'dorsal_debug' subfolder in the testing directory
"""

import os
import glob
import sys
from pathlib import Path

# Add current directory to path to import brainviz_dk
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from plot import plot_nifti, get_quality_preset

# Configuration
DATA_DIR = '/media/brainlab-uwo/Data2/Results/Group_level_analysis/Testing/MNI152NLin2009cAsym'
OUTPUT_DIR = os.path.join(DATA_DIR, 'dorsal_debug')

print("=" * 70)
print(" BrainViz_DK: Dorsal View Debug Script")
print("=" * 70)
print(f"\nData directory: {DATA_DIR}")
print(f"Output directory: {OUTPUT_DIR}")
print()

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Get all NIfTI files
nifti_files = sorted(glob.glob(f'{DATA_DIR}/*.nii.gz'))

if not nifti_files:
    print("❌ No NIfTI files found!")
    sys.exit(1)

print(f"Found {len(nifti_files)} NIfTI files to process\n")

# Use standard quality for debugging (faster than publication)
preset = get_quality_preset('standard')

successful = 0
failed = []

# Process each file
for idx, nifti_file in enumerate(nifti_files, 1):
    basename = os.path.basename(nifti_file).replace('.nii.gz', '')

    print(f"[{idx}/{len(nifti_files)}] {basename}")

    # Plot both hemispheres for dorsal view
    for hemi in ['lh', 'rh']:
        try:
            output_file = os.path.join(OUTPUT_DIR, f'{basename}_dorsal_{hemi}.png')

            print(f"  → Plotting {hemi} dorsal view...", end=" ")

            plot_nifti(
                nifti_file,
                output_file,
                hemi=hemi,
                view='dorsal',  # Top view
                colormap='hot',
                **preset
            )

            # Check file was created
            if os.path.exists(output_file):
                size_kb = os.path.getsize(output_file) / 1024
                print(f"✓ ({size_kb:.1f} KB)")
                successful += 1
            else:
                print("✗ File not created")
                failed.append((basename, hemi, "File not created"))

        except Exception as e:
            print(f"✗ Error: {str(e)[:50]}")
            failed.append((basename, hemi, str(e)))

    print()

# Summary
print("=" * 70)
print(" Summary")
print("=" * 70)
print(f"Total files processed: {len(nifti_files)}")
print(f"Total plots attempted: {len(nifti_files) * 2} (2 hemispheres each)")
print(f"Successful plots: {successful}")
print(f"Failed plots: {len(failed)}")
print()

if failed:
    print("Failed plots:")
    for basename, hemi, error in failed:
        print(f"  - {basename} ({hemi}): {error[:60]}")
    print()

print(f"✓ Output directory: {OUTPUT_DIR}")
print("=" * 70)

# Exit with appropriate code
sys.exit(0 if not failed else 1)
