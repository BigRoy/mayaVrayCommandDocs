import maya.cmds as mc

def vray_subdivision(shapes=None,
                     state=1,
                     vraySubdivEnable=None,
                     vraySubdivUVs=None,
                     vrayPreserveMapBorders=None,
                     vrayStaticSubdiv=None,
                     vrayClassicalCatmark=None):
    """ Add a v-ray subdivision attribute to selected meshes

    :param shapes: Shapes to apply the attribute to. If shapes is None it will get
                   the shapes related to the current selection.
    :param state: If state is True it will add the subdivision attribute, else it will remove it.
    """
    # TODO: Add param descriptions for the attributes

    if shapes is None:
        shapes = mc.ls(sl=1, s=1, dag=1, lf=1, o=1, long=True)

    if shapes:
        # Only apply to mesh or nurbsSurface (other shapes can't contain the vray_subdivision attribute)
        shapes = mc.ls(shapes, type=("mesh", "nurbsSurface"))

    if shapes:
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

    else:
        raise RuntimeError("No shapes found to apply the vray_subdivision attribute group changes to.")