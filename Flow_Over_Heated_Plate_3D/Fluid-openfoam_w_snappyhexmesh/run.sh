#!/bin/sh
./Allclean
blockMesh
surfaceFeatureExtract
snappyHexMesh -overwrite
buoyantPimpleFoam
paraFoam
