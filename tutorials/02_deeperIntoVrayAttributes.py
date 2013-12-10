"""

    This **deeperIntoVrayAttributes** tutorial will help you delve deeper into the
    ``mc.vray("addAttributesFromGroup",..)`` command.

    For a very short overview of the tutorials have a look at the README that resides in the tutorials directory.

"""

# So you've gone through tutorial 01 and want to go a bit further. You can't do much automatisation in Maya with V-ray
# if you don't have a grasp on how to write small scripts for Maya. So let start with some tips.

# 1. The script editor is useful to have a look at what commands maya performs when you do something in Maya.
#
#    For example select something in the viewport and you'll set something like:
#
#       select -r pSphere1 ;
#
#    The commands that maya will spit out in the script editor are in MEL. So there might be some syntax adjustments
#    required to do the same magic in Python, but in general you can use it as a good learning resource.


# 2. If you use the script editor and the command doesn't show up, try turning on "Echo all commands" in the "History"
#    menu in the script editor.
#
#    This will show all mel commands (and sourced script commands) that Maya runs when performing actions. Though note
#    that leaving this on during normal operations Maya might slow down a bit (as it's printing more into the script
#    editor.) Turning this off after using it is a good habit.


# 3. The Python/Mel Command Reference (Help > Python Command Reference)
#
#    The command reference shows a list of all built-in maya commands. They come with a brief explanation and with
#    some examples as well. Useful! :)

# One important command is mc.ls()
# It's essentially a ``list`` command and returns a list of node names. Either from selection, or by name or type.

# To get the current selection:
import maya.cmds as mc
print mc.ls(selection=True)


# Or with the short hand flag for selection (-sl):
import maya.cmds as mc
print mc.ls(sl=True)


# Now let's say we wanted to get all transform nodes in our current selection:
import maya.cmds as mc
print mc.ls(sl=True, type="transform")


# Or only the polygon meshes:
import maya.cmds as mc
print mc.ls(sl=True, type="mesh")


# Play around with the mesh version. You'll see that when you select the object in your viewport (what you might think
# is the mesh) and run this it will return an empty list. Nothing?

# That's because you're essentially selecting the transform node of the object. The transform node is that thing that
# tells maya where it is positioned in the scene. You see this behaviour for all shape nodes, they are parented under
# a transform node. For example a camera is under a transform, or a nurbsSurface, or nurbsCurve.

# This is a KEY thing to remember: The shape node is seperate from the transform. It's literally it's child.

# The transform node itself is essentially a group, to show this let's make a polygon cube.
# Select it in the viewport and press the down arrow on the keyboard.
# This will pickwalk down from that node onto its child node, that is the shape!
# Press delete.
# The shape will be gone, but the transform will still be there. Look at the icon of the node of the transform that is
# still there in the outliner. Looks familiar? It should, because it's exactly the icon of a group (NULL).

# To get the shape from your selected transforms you need to exactly that: Go one down in the hierarchy. Or we could
# say: Get its children.

import maya.cmds as mc
selection = mc.ls(sl=1)
print selection
if selection:
    children = mc.listRelatives(selection, children=True)
    print children


# Let's say we wanted to have all mesh shapes of our currently selected transforms, we can do:
import maya.cmds as mc
selection = mc.ls(sl=1)
print selection
if selection:
    meshes = mc.listRelatives(selection, children=True, type="mesh")
    print meshes


# Or all shapes:
import maya.cmds as mc
selection = mc.ls(sl=1)
print selection
if selection:
    meshes = mc.listRelatives(selection, children=True, shapes=True)
    print meshes

# More information about the ls command and listRelatives command can be found in the Python command reference.
# See point 3 at the start of this tutorial for more information about the Python command reference.
# Play around with mc.ls and mc.listRelatives until you feel somewhat familiar.

# To be continued. :)
# Now you should know the difference between transforms and their children shapes.
# Let's get all transform nodes that end with "*_SMOOTH" and add a subdivision attribute to it's children mesh shapes.

import maya.cmds as mc
# Get all transform nodes that end with _SMOOTH
nodes = mc.ls("*_SMOOTH", type="transform")
if nodes:
    # Get the children shapes of type mesh
    meshes = mc.listRelatives(nodes, children=True, shapes=True, type="mesh")
    # If we found children meshes, then for every mesh shape node add the vray_subdivision attribute.
    if meshes:
        for mesh in meshes:
            mc.vray("addAttributesFromGroup", "vray_subdivision", mesh, 1)

# We can do something similar for all nurbsCurves that we want to make renderable. If we have given a specific suffix
# to the nodes we can easily address them.
# So I've discussed with the team and we went for "_EXTREMELY_RENDERABLE_CURVE" as a suffix on the transform node of
# the nurbsCurves.

# Ah yeah, let's get those transforms!
import maya.cmds as mc
nodes = mc.ls("*_EXTREMELY_RENDERABLE_CURVE", type="transform")
print nodes

# So we play around and test if it is giving us the nodes. Did you try it?
# Then go on and get the children nurbsCurve shape nodes.

if nodes:
    shapes = mc.listRelatives(nodes, children=True, shapes=True, type="nurbsCurve")
    print shapes

    # Still looking good?
    # All we need to do now is add the ``vray_nurbscurve_renderable`` attribute.
    # It's very similar to what we did so far. Easy!

    for shape in shapes:
        mc.vray("addAttributesFromGroup", "vray_nurbscurve_renderable", shape, 1)

# Simple as that!
# To make sure you understand correctly try adding the ``vray_skip_export`` to selected transform nodes.
# Then maybe try adding ``vray_objectID`` attributes to all children shapes of your selection. :)
