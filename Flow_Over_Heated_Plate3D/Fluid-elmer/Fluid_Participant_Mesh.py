import gmsh
import sys
path = sys.path[0]
print(path)

# Initialize GMSH
gmsh.initialize()
# import a step file called fluid.step
# get the absolute path of the file
gmsh.open(path+"/Fluid_Participant_Mesh.step")
volumes = gmsh.model.getEntities(3)
# fragment the volume
gmsh.model.occ.fragment(volumes,[])
# delete volume 2 which is the solid
gmsh.model.occ.remove([(3,2)], True)
gmsh.model.occ.synchronize()
volume = gmsh.model.getEntities(3)
# add physical group for the fluid
gmsh.model.addPhysicalGroup(3, [volume[0][1]], tag=1, name="Fluid")
# move the mode to 2.5 in z direction and -5 in x direction
bbox = gmsh.model.getBoundingBox(3, volume[0][1])
xmin, ymin, zmin, xmax, ymax, zmax = round(bbox[0],3), round(bbox[1],3), round(bbox[2],3), round(bbox[3],3), round(bbox[4],3), round(bbox[5],3)
# Create a new model
model = gmsh.model
model.geo.synchronize()
surfaces = model.getEntities(2)
walls = []
for s in surfaces:
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
        coupling_interface = s
    else:
        # add physical group
        walls.append(s[1])
# add all the walls to a physical group
model.addPhysicalGroup(2, walls, tag=-1, name="Fluid_Walls")
# add a filed size limit for the coupling inter
dis_f_interface = gmsh.model.mesh.field.add("Distance")
gmsh.model.mesh.field.setNumbers(dis_f_interface, "SurfacesList", [coupling_interface[1]])
gmsh.model.mesh.field.setNumber(dis_f_interface, "Sampling", 100)
lc_min = 0.1
lc_max = 1
dist_min = 0.2
dist_max = 1
th_f_interface = gmsh.model.mesh.field.add("Threshold")
gmsh.model.mesh.field.setNumber(th_f_interface, "InField", dis_f_interface)
gmsh.model.mesh.field.setNumber(th_f_interface, "SizeMin", lc_min)
gmsh.model.mesh.field.setNumber(th_f_interface, "SizeMax", lc_max)
gmsh.model.mesh.field.setNumber(th_f_interface, "DistMin", dist_min)
gmsh.model.mesh.field.setNumber(th_f_interface, "DistMax", dist_max)
gmsh.model.mesh.field.setNumber(th_f_interface, "StopAtDistMax", 1)
gmsh.model.mesh.field.setAsBackgroundMesh(th_f_interface)

# limit the mesh size
gmsh.option.setNumber("Mesh.MeshSizeMax", 0.5)
# Generate the mesh
model.mesh.generate(3)

# Write the mesh to a file
gmsh.write(path+"/Fluid_Participant_Mesh.msh")

gmsh.fltk.run()
# Finalize GMSH
gmsh.finalize()
