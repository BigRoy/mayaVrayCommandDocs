"""

    This **gettingStarted** tutorial should allow  you to get up on your feet quickly to work with Chaosgroup's ``vray``
    command in Maya with Python.

    For a very short overview of the tutorials have a look at the README that resides in the tutorials directory.

"""

# To start we need to import the maya commands. Because everyone likes short names it's often imported as ``mc``.
# So let's do that:

import maya.cmds as mc

# This allows us to use Maya's command features in our code.
# For example we can list all mesh shapes in our scene, like:

print mc.ls(type="mesh")

# But hey, you came here to do some v-ray for maya magic.
#
# This is the moment where you make sure the vrayformaya.mll is loaded in your Plug-in Manager.
# You can find it in: Window > Settings/Preferences > Plug-in Manager
# Search for the vrayformaya.mll and make sure the loaded checkbox is checked.
#
# Basically most of the stuff you can do with commands provided from the V-ray for Maya plug-in is done through a
# command called ``vray``. Commands created by plug-ins are available in the maya.cmds namespace.
# In short we can do something like:

mc.vray()

# Note that this doesn't give any errors, but it doesn't do anything either.
# By having a look at the wiki documentation on this repository you'll find what you can provide as arguments:
# https://github.com/BigRoy/mayaVrayCommandDocs/wiki
#
# Many people getting started with v-ray for maya scripting are doing it to help ease the adding of v-ray attributes.
# So let's start there. Adding v-ray attributes is done through the ``vray`` command with the action
# ``addAttributesFromGroup``. More information here:
# https://github.com/BigRoy/mayaVrayCommandDocs/wiki/vray-addAttributesFromGroup
#
# The example on that page shows us:

shapes = mc.ls(sl=1, dag=1, lf=1, s=1)
for shape in shapes:
    mc.vray("addAttributesFromGroup", shape, "vray_subdivision", 1)

# So what does that do?
# First it gets all shapes from the current selection.
# Then we loop over all of these shapes,
# To add a ``vray_subdivision`` attribute to every single on of them.
# EASY!
#
# So the command to add the attributes is basically in the format of:
#
# mc.vray("addAttributesFromGroup", node, attr, state)
#
# Where:
#    `node` is the node to apply the command to. (this should be of the correct type)
#    `attr` is the attribute type/group to create. (some variations can be found in the wiki documentation)
#    `state` is an integer (1 or 0) to either create or remove the attributes. (note: True or False don't work correctly!)
#
# Now let's remove it again by changing the state parameter.

shapes = mc.ls(sl=1, dag=1, lf=1, s=1)
for shape in shapes:
    mc.vray("addAttributesFromGroup", shape, "vray_subdivision", 0)

# This should get you up and running with interpreting the WIKI documentation and writing your own code.
# Play around with creating different types of v-ray attributes.