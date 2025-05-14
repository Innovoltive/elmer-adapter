#!/bin/bash

# Script to clean precice-profiling, precice-run folders and OpenFOAM time step folders
# Author: GitHub Copilot
# Date: May 14, 2025

echo "Cleaning preCICE artifacts..."

# Remove precice-profiling folders
echo "Removing precice-profiling folders..."
find . -type d -name "precice-profiling" -exec rm -rf {} \; -prune

# Remove out folder
echo "Removing out folder..."
find . -type d -name "out" -exec rm -rf {} \; -prune

# Remove precice-run folders
echo "Removing precice-run folders..."
find . -type d -name "precice-run" -exec rm -rf {} \; -prune

# Remove OpenFOAM time step folders (folders that start with floating point numbers but not 0)
echo "Removing OpenFOAM time step folders..."
find . -path "*openfoam*" -type d -regextype posix-extended -regex ".*/[0-9]+(\.[0-9]+)?" ! -name "0" -exec rm -rf {} \; -prune

# Show summary
echo "Cleanup completed!"
