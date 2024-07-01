import gmsh
import sys
path = sys.path[0]
print(path)

# Initialize GMSH
gmsh.initialize()
# import a step file called fluid.step
# get the absolute path of the file
gmsh.open(path+"/Reference_Problem_Mesh.step")
volumes = gmsh.model.getEntities(3)
# fragment the volume
gmsh.model.occ.fragment(volumes,[])
gmsh.model.occ.synchronize()
# add physical group for the fluid
gmsh.model.addPhysicalGroup(3, [volumes[0][1]], tag=1, name="Fluid")
# add a physical group for the solid
gmsh.model.addPhysicalGroup(3, [volumes[1][1]], tag=2, name="Plate")
# move the mode to 2.5 in z direction and -5 in x direction
bbox = gmsh.model.getBoundingBox(3, volumes[0][1])
xmin, ymin, zmin, xmax, ymax, zmax = round(bbox[0],3), round(bbox[1],3), round(bbox[2],3), round(bbox[3],3), round(bbox[4],3), round(bbox[5],3)
# Create a new model
model = gmsh.model
model.geo.synchronize()
surfaces = model.getEntities(2)
fluid_walls = []
# get all the surfaces that are in volume 2
fluid_surfaces = gmsh.model.getBoundary([(3, 1)], False, False)
solid_surfaces = gmsh.model.getBoundary([(3, 2)], False, False)
for s in fluid_surfaces:
    bbox = model.getBoundingBox(2, s[1])
    xmins, ymins, zmins, xmaxs, ymaxs, zmaxs = round(bbox[0],3), round(bbox[1],3), round(bbox[2],3), round(bbox[3],3), round(bbox[4],3), round(bbox[5],3)
    # get the inlet surface wch is the left surface
    if xmins == xmin and xmaxs == xmin:
        # add physical group
        model.addPhysicalGroup(2, [s[1]], tag=-1, name="Inlet")

    # get the outlet surface wch is the right surface
    elif xmaxs == xmax and xmins == xmax:
        # add physical group
        model.addPhysicalGroup(2, [s[1]], tag=-1, name="Outlet")
    elif s[1] == 12:
        # add physical group
        model.addPhysicalGroup(2, [s[1]], tag=-1, name="Coupling_Interface")
    else:
        # add physical group if s not in the volume 2
        if s not in solid_surfaces:
            fluid_walls.append(s[1])
# add all the walls to a physical group

# get the surfaces for the lower solid
model.addPhysicalGroup(2, fluid_walls, tag=-1, name="Fluid_Walls")
bbox = gmsh.model.getBoundingBox(3, volumes[1][1])
xmin, ymin, zmin, xmax, ymax, zmax = round(bbox[0],3), round(bbox[1],3), round(bbox[2],3), round(bbox[3],3), round(bbox[4],3), round(bbox[5],3)
solid_walls = []
for s in solid_surfaces:
    bbox = model.getBoundingBox(2, s[1])
    xmins, ymins, zmins, xmaxs, ymaxs, zmaxs = round(bbox[0],3), round(bbox[1],3), round(bbox[2],3), round(bbox[3],3), round(bbox[4],3), round(bbox[5],3)
        
    # get the bottom surface
    if zmins == zmin and zmaxs == zmin:
        # add physical group
        model.addPhysicalGroup(2, [s[1]], tag=-1, name="Plate_Bottom")
    # get the walls
    else:
        if s not in fluid_surfaces:
            solid_walls.append(s[1])  
# add physical group
model.addPhysicalGroup(2, solid_walls, tag=-1, name="Plate_Sides")

# limit the mesh size
gmsh.option.setNumber("Mesh.MeshSizeMax", 0.5)
# Generate the mesh
model.mesh.generate(3)

# Write the mesh to a file
gmsh.write(path+"/Reference_Problem_Mesh.msh")

gmsh.fltk.run()
# Finalize GMSH
gmsh.finalize()
