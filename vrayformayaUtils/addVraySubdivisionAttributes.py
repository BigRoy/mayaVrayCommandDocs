import maya.cmds as mc
import maya.mel as mel


def addVraySubdivisionAttribute(shapes=None):
    """ Add a v-ray subdivision attribute to selected meshes

    :param shapes: Shapes to apply the attribute to. If shapes is None it will get
                   the shapes related to the current selection.
    """

    if shapes is None:
        shapes = mc.ls(sl=1, s=1, dag=1, lf=1, o=1, long=True)

    if shapes:
        # Only apply to mesh or nurbsSurface (other shapes can't contain the vray_subdivision attribute)
        shapes = mc.ls(shapes, type=("mesh", "nurbsSurface"))

    if shapes:
        for shape in shapes:
            mc.vray("addAttributesFromGroup", shape, "vray_subdivision", 1)
    else:
        raise RuntimeError("No shapes found to apply the vray_subdivision attribute group to.")