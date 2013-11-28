import maya.cmds as mc
from vrayformayaUtils.utils import getShapes, getMaterials


def vray_subdivision(shapes=None,
                     state=1,
                     smartConvert=True,
                     allDescendents=True,
                     vraySubdivEnable=None,
                     vraySubdivUVs=None,
                     vrayPreserveMapBorders=None,
                     vrayStaticSubdiv=None,
                     vrayClassicalCatmark=None):
    """ Add/change the subdivision attribute to selected meshes

    :param shapes: Shapes to apply the attribute to. If shapes is None it will get
                   the shapes related to the current selection.
    :param state: If state is True it will add the subdivision attribute, else it will remove it.
    """
    validTypes = ("mesh", "nurbsSurface")

    if smartConvert or shapes is None:
        shapes = getShapes(shapes, allDescendents=allDescendents, filterType=validTypes)
    else:
        shapes = mc.ls(shapes, validTypes)

    if not shapes:
        raise RuntimeError("No shapes found to apply the vray_subdivision attribute group changes to.")

    for shape in shapes:
        mc.vray("addAttributesFromGroup", shape, "vray_subdivision", state)

        # Manage the attributes (if not None change it to the set value)
        if state:
            if vraySubdivEnable is not None:
                mc.setAttr("{0}.vraySubdivEnable".format(shape), vraySubdivEnable)
            if vraySubdivUVs is not None:
                mc.setAttr("{0}.vraySubdivUVs".format(shape), vraySubdivUVs)
            if vrayPreserveMapBorders is not None:
                mc.setAttr("{0}.vrayPreserveMapBorders".format(shape), vrayPreserveMapBorders)
            if vrayStaticSubdiv is not None:
                mc.setAttr("{0}.vrayStaticSubdiv".format(shape), vrayStaticSubdiv)
            if vrayClassicalCatmark is not None:
                mc.setAttr("{0}.vrayClassicalCatmark".format(shape), vrayClassicalCatmark)


def vray_material_id(materials=None,
                     state=1,
                     smartConvert=True,
                     vrayMaterialId=None):
    """ Add/change the v-ray material ID attribute to selected meshes

    :param materials: Materials to apply the attribute to. If materials is None it will get
                      the materials related to the current selection.

    :param state: If state is True it will add the subdivision attribute, else it will remove it.
    :type  state: 1 or 0

    :param smartConvert: If True the input materials list will be checked for 'related materials'
                         and those found will be included. Else it will on
                         If no materials provided smartConvert is forced to True and it will get
                         materials related to the current selection.
    :type  smartConvert: bool

    :param vrayMaterialId: The material ID number value.
                           If None it will remain default/unchanged.
    :type  vrayMaterialId: None or int

    """
    if smartConvert or materials is None:
        materials = getMaterials(materials)
    else:
        materials = mc.ls(materials, mat=True)

    if not materials:
        raise RuntimeError("No materials found")

    for mat in materials:
        mc.vray("addAttributesFromGroup", mat, "vray_material_id", 1)
        if vrayMaterialId is not None:
            mc.setAttr("{0}.{1}".format(mat, 'vrayMaterialId'), vrayMaterialId)


# Clean-up the module
del mc, getShapes, getMaterials