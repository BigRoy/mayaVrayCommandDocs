import maya.cmds as mc


def addVrayObjectIds(shapes=None):
    """ Add a vray_objectID attribute to selected meshes

    :param shapes: Shapes to apply the attribute to. If shapes is None it will get
                   the shapes related to the current selection.
    """
    if shapes is None:
        shapes = mc.ls(sl=1, s=1, dag=1, lf=1, o=1, long=True)

    if shapes:
        # Can only add objectIds to mesh, nurbsSurface so lets filter it
        shapes = mc.ls(shapes, type=("mesh", "nurbsSurface"))

    if shapes:
        result = mc.promptDialog(title='Object ID value',
                                    message='Object ID:',
                                    button=['OK', 'Cancel'],
                                    defaultButton='OK',
                                    cancelButton='Cancel',
                                    dismissString='Cancel')

        if result == 'OK':
            value = int(mc.promptDialog(query=True, text=True))

            for shape in shapes:
                mc.vray("addAttributesFromGroup", shape, "vray_objectID", 1)
                mc.setAttr("{0}.{1}".format(shape, 'vrayObjectID'), value)


if __name__ == "__main__":
    addVrayObjectIds()