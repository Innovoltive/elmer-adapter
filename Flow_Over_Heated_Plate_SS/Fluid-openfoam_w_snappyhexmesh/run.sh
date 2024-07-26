#!/bin/sh
./Allclean
blockMesh
surfaceFeatureExtract
snappyHexMesh -overwrite
buoyantSimpleFoam
paraFoam
