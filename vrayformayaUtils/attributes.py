"""
    Vray Attributes
    ===============

    The `attributes` module makes managing v-ray attributes an easy practice.

    It provides a convenient way of doing everything that mc.vray("addAttributesFromGroup", ..) does, and more!

    # Features

    ### Selection

    The framework uses the current selection if no nodes are specified in the attribute function.
    For example if you use vray_subdivision() without any arguments it will add the v-ray subdivision attributes
    to the current selection.


    ### Smart Convert input

    Many (if not all) attributes come with a smartConvert parameter that is True by default.
    It allows the input list to be interpreted as 'get related objects that can have this attribute'.
    This means you can actually apply a `vray_material_id` to a mesh.
    It will get the related assigned material and applies it to that. Easy right?

    If you don't want this automatic conversion doing anything you can set the smartConvert parameter to False.


    ### Filters to valid objects

    The functions automatically filter objects that aren't supposed to have the attribute. You can try to add the
    vray_subdivision to a camera shape but it will have no effect. Chaosgroup's implementation of vray and
    `addAttributesGroup` creates the given attribute group even if it's not relevant to the node you supply.
    In short the default vray command doesn't come with error checking; this framework helps by doing just that.


"""
import maya.cmds as mc
from vrayformayaUtils.utils import getShapes, getMaterials


def _convert_state(state):
    """ Convert the user input of state to how v-ray command likes it.

    For module internal use.

    :param state: The state to be converted to 1 or 0
    :return: Converted state
    """
    if not isinstance(state, int) or isinstance(state, bool):
        try:
            state = int(state)
        except (ValueError, TypeError):
            raise TypeError("state argument must be an int or to int convertable type, not {0}".format(type(state)))
    return state


##########
# mesh, nurbsSurface
##########
# TODO: Add vray_subquality, vray_displacement, vray_roundedges, vray_fogFadeOut

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

    Valid node types: (mesh, nurbsSurface)

    :param shapes: Shapes to apply the attribute to. If shapes is None it will get
                   the shapes related to the current selection.

    :param state: If state is True it will add the subdivision attribute, else it will remove it.
    :type  state: 1 or 0

    :param allDescendents: If True it will smartConvert to allDescendent shapes.
                           e.g. this allows you to apply it to a group and all shapes in it will get object ids.
    :type  allDescendents: bool

    :param vraySubdivEnable: Enable/disable the subdivisions. If None it remains default/unchanged.
    :type  vraySubdivEnable: None or bool

    :param vraySubdivUVs: Enable/disable the smoothing of the UVs. If None it remains default/unchanged.
    :type  vraySubdivUVs: None or bool

    :param vrayPreserveMapBorders: Enable/disable the UV borders if smoothing UVs is on.
                                   If None it remains default/unchanged.
    :type  vrayPreserveMapBorders: None or bool

    :param vrayStaticSubdiv: Enable/disable vrayStaticSubdiv. If None it remains default/unchanged.
    :type  vrayStaticSubdiv: None or bool

    :param vrayClassicalCatmark: Enable/disable vrayClassicalCatmark. If None it remains default/unchanged.
    :type  vrayClassicalCatmark: None or bool
    """
    # TODO: Add better explanation for what vrayStaticSubdiv and vrayClassicalCatmark is.

    state = _convert_state(state)
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


def vray_object_id(shapes=None,
                     state=1,
                     smartConvert=True,
                     allDescendents=True,
                     vrayObjectID=None):
    """ Add/change the vray_object_id attribute to selected meshes

    :param shapes: Shapes to apply the attribute to. If shapes is None it will get
                   the shapes related to the current selection.

    :param state: If state is True it will add the vray_object_id attribute, else it will remove it.
    :type  state: 1 or 0

    :param smartConvert: If True it will convert the input smartly to related shape nodes.
    :type  smartConvert: bool

    :param allDescendents: If True it will smartConvert to allDescendent shapes.
                           e.g. this allows you to apply it to a group and all shapes in it will get object ids.
    :type  allDescendents: bool

    :param vrayObjectID: The object ID number value. If None remains default/unchanged.
    :type  vrayObjectID: None or int
    """
    # TODO: Somehow also supported by VRayLightDomeShape, VRayLightRectShape, VRayLightSphereShape so add support?
    # TODO: ^- First check if it does anything useful (if it's not doing anything report bug to Chaosgroup)

    state = _convert_state(state)
    validTypes = ("mesh", "nurbsSurface")

    if smartConvert or shapes is None:
        shapes = getShapes(shapes, allDescendents=allDescendents, filterType=validTypes)
    else:
        shapes = mc.ls(shapes, validTypes)

    if not shapes:
        raise RuntimeError("No shapes found to apply the vray_object_id attribute group changes to.")

    for shape in shapes:
        mc.vray("addAttributesFromGroup", shape, "vray_objectID", state)

        # Manage the attributes (if not None change it to the set value)
        if state:
            if vrayObjectID is not None:
                mc.setAttr("{0}.vrayObjectID".format(shape), vrayObjectID)


def vray_user_attributes(shapes=None,
                     state=1,
                     smartConvert=True,
                     allDescendents=True,
                     vrayUserAttributes=None):
    """ Add/change the vray_user_attributes attribute to input shapes.

    :param shapes: Shapes to apply the attribute to. If shapes is None it will get
                   the shapes related to the current selection.

    :param state: If state is True it will add the vray_object_id attribute, else it will remove it.
    :type  state: 1 or 0

    :param smartConvert: If True it will convert the input smartly to related shape nodes.
    :type  smartConvert: bool

    :param allDescendents: If True it will smartConvert to allDescendent shapes.
                           e.g. this allows you to apply it to a group and all shapes in it will get object ids.
    :type  allDescendents: bool

    :param vrayUserAttributes: The actual user attribute string value. If None it remains default/unchanged.
    :type  vrayUserAttributes: str
    """

    state = _convert_state(state)
    validTypes = ("mesh", "nurbsSurface")

    if smartConvert or shapes is None:
        shapes = getShapes(shapes, allDescendents=allDescendents, filterType=validTypes)
    else:
        shapes = mc.ls(shapes, validTypes)

    if not shapes:
        raise RuntimeError("No shapes found to apply the vray_object_id attribute group changes to.")

    for shape in shapes:
        mc.vray("addAttributesFromGroup", shape, "vray_user_attributes", state)

        # Manage the attributes (if not None change it to the set value)
        if state:
            if vrayUserAttributes is not None:
                mc.setAttr("{0}.vrayUserAttributes".format(shape), vrayUserAttributes, type="string")


##########
# nurbsSurface
##########

def vray_nurbsStaticGeom(shapes=None,
                     state=1,
                     smartConvert=True,
                     allDescendents=True,
                     vrayAsStaticGeom=None,
                     vrayMaxSubdivDepth=None,
                     vrayFlatnessCoef=None):
    """ Add/change the NURBS attributes to input shapes.

    Note: The actual v-ray command for this has a typo: vray_nusrbsStaticGeom
          I've submitted this as an error/bug, it's up to Chaosgroup what they'll do with it.

    :param shapes: Shapes to apply the attribute to. If shapes is None it will get
                   the shapes related to the current selection.

    :param state: If state is True it will add the vray_object_id attribute, else it will remove it.
    :type  state: 1 or 0

    :param smartConvert: If True it will convert the input smartly to related shape nodes.
    :type  smartConvert: bool

    :param allDescendents: If True it will smartConvert to allDescendent shapes.
                           e.g. this allows you to apply it to a group and all shapes in it will get object ids.
    :type  allDescendents: bool

    :param vrayAsStaticGeom: Enable/Disable Generate static geometry. If None it remains default/unchanged.
    :type  vrayAsStaticGeom: bool

    :param vrayMaxSubdivDepth: Max Tesselation Depth. If None it remains default/unchanged.
    :type  vrayMaxSubdivDepth: int

    :param vrayFlatnessCoef: Curvature Threshold. If None it remains default/unchanged.
    :type  vrayFlatnessCoef: float
    """

    state = _convert_state(state)
    validTypes = "nurbsSurface"

    if smartConvert or shapes is None:
        shapes = getShapes(shapes, allDescendents=allDescendents, filterType=validTypes)
    else:
        shapes = mc.ls(shapes, validTypes)

    if not shapes:
        raise RuntimeError("No shapes found to apply the vray_object_id attribute group changes to.")

    for shape in shapes:
        mc.vray("addAttributesFromGroup", shape, "vray_nusrbsStaticGeom", state)

        # Manage the attributes (if not None change it to the set value)
        if state:
            if vrayAsStaticGeom is not None:
                mc.setAttr("{0}.vrayAsStaticGeom".format(shape), vrayAsStaticGeom)
            if vrayMaxSubdivDepth is not None:
                mc.setAttr("{0}.vrayMaxSubdivDepth".format(shape), vrayMaxSubdivDepth)
            if vrayFlatnessCoef is not None:
                mc.setAttr("{0}.vrayFlatnessCoef".format(shape), vrayFlatnessCoef)


##############
## nurbsCurves
##############

def vray_nurbscurve_renderable(shapes=None,
                     state=1,
                     smartConvert=True,
                     allDescendents=True):
    """ Add/change the vray_nurbscurve_renderable attribute to input nurbsCurves.

    :param shapes: Shapes to apply the attribute to. If shapes is None it will get
                   the shapes related to the current selection.

    :param state: If state is True it will add the vray_object_id attribute, else it will remove it.
    :type  state: 1 or 0

    :param smartConvert: If True it will convert the input smartly to related shape nodes.
    :type  smartConvert: bool

    :param allDescendents: If True it will smartConvert to allDescendent shapes.
                           e.g. this allows you to apply it to a group and all shapes in it will get object ids.
    :type  allDescendents: bool
    """
    # TODO: Add change attribute value support

    state = _convert_state(state)
    validTypes = ("nurbsCurve")

    if smartConvert or shapes is None:
        shapes = getShapes(shapes, allDescendents=allDescendents, filterType=validTypes)
    else:
        shapes = mc.ls(shapes, validTypes)

    if not shapes:
        raise RuntimeError("No shapes found to apply the vray_object_id attribute group changes to.")

    for shape in shapes:
        mc.vray("addAttributesFromGroup", shape, "vray_nurbscurve_renderable", state)


##############
## materials
##############

def vray_material_id(materials=None,
                     state=1,
                     smartConvert=True,
                     vrayMaterialId=None):
    """ Add/change the v-ray material ID attribute to input materials.

    :param materials: Materials to apply the attribute to. If materials is None it will get
                      the materials related to the current selection.

    :param state: If state is True it will add the subdivision attribute, else it will remove it.
    :type  state: 1 or 0

    :param smartConvert: If True the input materials list will be checked for 'related materials'
                         and those found will be included. Else it will on
                         If no materials provided smartConvert is forced to True and it will get
                         materials related to the current selection.
    :type  smartConvert: bool

    :param vrayMaterialId: The material ID number value. If None it will remain default/unchanged.
    :type  vrayMaterialId: None or int
    """
    state = _convert_state(state)

    if smartConvert or materials is None:
        materials = getMaterials(materials)
    else:
        materials = mc.ls(materials, mat=True)

    if not materials:
        raise RuntimeError("No materials found")

    for mat in materials:
        mc.vray("addAttributesFromGroup", mat, "vray_material_id", state)

        # Manage the attributes (if not None change it to the set value)
        if state:
            if vrayMaterialId is not None:
                mc.setAttr("{0}.{1}".format(mat, 'vrayMaterialId'), vrayMaterialId)


def vray_specific_mtl(materials=None,
                     state=1,
                     smartConvert=True):
    """ Add/change the v-ray material override attribute to input materials.

    :param materials: Materials to apply the attribute to. If materials is None it will get
                      the materials related to the current selection.

    :param state: If state is True it will add the subdivision attribute, else it will remove it.
    :type  state: 1 or 0

    :param smartConvert: If True the input materials list will be checked for 'related materials'
                         and those found will be included. Else it will on
                         If no materials provided smartConvert is forced to True and it will get
                         materials related to the current selection.
    :type  smartConvert: bool
    """
    # TODO: Add change attribute value support
    state = _convert_state(state)

    if smartConvert or materials is None:
        materials = getMaterials(materials)
    else:
        materials = mc.ls(materials, mat=True)

    if not materials:
        raise RuntimeError("No materials found")

    for mat in materials:
        mc.vray("addAttributesFromGroup", mat, "vray_specific_mtl", state)


##############
## v-ray materials
##############

def vray_closed_volume(materials=None,
                     state=1,
                     smartConvert=True):
    """ Add/change the v-ray closed volume shading attribute to input materials.

    :param materials: Materials to apply the attribute to. If materials is None it will get
                      the materials related to the current selection.

    :param state: If state is True it will add the subdivision attribute, else it will remove it.
    :type  state: 1 or 0

    :param smartConvert: If True the input materials list will be checked for 'related materials'
                         and those found will be included. Else it will on
                         If no materials provided smartConvert is forced to True and it will get
                         materials related to the current selection.
    :type  smartConvert: bool
    """
    # TODO: Add attribute value support
    # TODO: Add check if node is a valid v-ray material that can have closed volume shading

    state = _convert_state(state)

    if smartConvert or materials is None:
        materials = getMaterials(materials)
    else:
        materials = mc.ls(materials, mat=True)


    if not materials:
        raise RuntimeError("No materials found")

    for mat in materials:
        mc.vray("addAttributesFromGroup", mat, "vray_closed_volume", state)


##############
## camera
##############
# TODO: Add camera attributes: vray_cameraDome, vray_cameraOverrides, vray_cameraPhysical

##############
## lights
## These are seperated per light type like:
## - pointLight (vray_pointLight)
## - directionalLight (vray_directlight)
## - ambientLight (vray_light)
## - areaLight (vray_arealight)
##############

def vray_light(shapes=None,
                     state=1,
                     smartConvert=True,
                     allDescendents=True,
                     vrayPhotonSubdivs=None,
                     vrayDiffuseMult=None,
                     vrayCausticSubdivs=None,
                     vrayCausticMult=None,
                     vrayShadowBias=None,
                     vrayCutoffThreshold=None,
                     vrayOverrideMBSamples=None,
                     vrayMBSamples=None):
    """ Add/change the vray_light attribute to selected meshes

    Valid node types: (ambientLight)

    :param shapes: Shapes to apply the attribute to. If shapes is None it will get
                   the shapes related to the current selection.

    :param state: If state is True it will add the subdivision attribute, else it will remove it.
    :type  state: 1 or 0

    :param allDescendents: If True it will smartConvert to allDescendent shapes.
                           e.g. this allows you to apply it to a group and all shapes in it will get object ids.
    :type  allDescendents: bool
    """

    state = _convert_state(state)
    validTypes = ("ambientLight")

    if smartConvert or shapes is None:
        shapes = getShapes(shapes, allDescendents=allDescendents, filterType=validTypes)
    else:
        shapes = mc.ls(shapes, validTypes)

    if not shapes:
        raise RuntimeError("No shapes found to apply the vray_light attribute group changes to.")

    for shape in shapes:
        mc.vray("addAttributesFromGroup", shape, "vray_light", state)

        # Manage the attributes (if not None change it to the set value)
        if state:
            if vrayPhotonSubdivs is not None:
                mc.setAttr("{0}.vrayPhotonSubdivs".format(shape), vrayPhotonSubdivs)
            if vrayDiffuseMult is not None:
                mc.setAttr("{0}.vrayDiffuseMult".format(shape), vrayDiffuseMult)
            if vrayCausticSubdivs is not None:
                mc.setAttr("{0}.vrayCausticSubdivs".format(shape), vrayCausticSubdivs)
            if vrayCausticMult is not None:
                mc.setAttr("{0}.vrayCausticMult".format(shape), vrayCausticMult)
            if vrayShadowBias is not None:
                mc.setAttr("{0}.vrayShadowBias".format(shape), vrayShadowBias)
            if vrayCutoffThreshold is not None:
                mc.setAttr("{0}.vrayCutoffThreshold".format(shape), vrayCutoffThreshold)
            if vrayOverrideMBSamples is not None:
                mc.setAttr("{0}.vrayOverrideMBSamples".format(shape), vrayOverrideMBSamples)
            if vrayMBSamples is not None:
                mc.setAttr("{0}.vrayOverrideMBSamples".format(shape), vrayMBSamples)


def vray_directlight(shapes=None,
                     state=1,
                     smartConvert=True,
                     allDescendents=True,
                     vrayPhotonSubdivs=None,
                     vrayDiffuseMult=None,
                     vrayCausticSubdivs=None,
                     vrayCausticMult=None,
                     vrayShadowBias=None,
                     vrayDiffuseContrib=None,
                     vraySpecularContrib=None,
                     vrayStoreWithIrradianceMap=None,
                     vrayOverrideMBSamples=None,
                     vrayMBSamples=None):
    """ Add/change the vray_directlight attribute to selected meshes

    Valid node types: (directionalLight)

    :param shapes: Shapes to apply the attribute to. If shapes is None it will get
                   the shapes related to the current selection.

    :param state: If state is True it will add the subdivision attribute, else it will remove it.
    :type  state: 1 or 0

    :param allDescendents: If True it will smartConvert to allDescendent shapes.
                           e.g. this allows you to apply it to a group and all shapes in it will get object ids.
    :type  allDescendents: bool
    """

    state = _convert_state(state)
    validTypes = ("directionalLight")

    if smartConvert or shapes is None:
        shapes = getShapes(shapes, allDescendents=allDescendents, filterType=validTypes)
    else:
        shapes = mc.ls(shapes, validTypes)

    if not shapes:
        raise RuntimeError("No shapes found to apply the vray_pointLight attribute group changes to.")

    for shape in shapes:
        mc.vray("addAttributesFromGroup", shape, "vray_directlight", state)

        # Manage the attributes (if not None change it to the set value)
        if state:
            if vrayPhotonSubdivs is not None:
                mc.setAttr("{0}.vrayPhotonSubdivs".format(shape), vrayPhotonSubdivs)
            if vrayDiffuseMult is not None:
                mc.setAttr("{0}.vrayDiffuseMult".format(shape), vrayDiffuseMult)
            if vrayCausticSubdivs is not None:
                mc.setAttr("{0}.vrayCausticSubdivs".format(shape), vrayCausticSubdivs)
            if vrayCausticMult is not None:
                mc.setAttr("{0}.vrayCausticMult".format(shape), vrayCausticMult)
            if vrayShadowBias is not None:
                mc.setAttr("{0}.vrayShadowBias".format(shape), vrayShadowBias)
            if vrayDiffuseContrib is not None:
                mc.setAttr("{0}.vrayDiffuseContrib".format(shape), vrayDiffuseContrib)
            if vraySpecularContrib is not None:
                mc.setAttr("{0}.vraySpecularContrib".format(shape), vraySpecularContrib)
            if vrayStoreWithIrradianceMap is not None:
                mc.setAttr("{0}.vrayStoreWithIrradianceMap".format(shape), vrayStoreWithIrradianceMap)
            if vrayOverrideMBSamples is not None:
                mc.setAttr("{0}.vrayOverrideMBSamples".format(shape), vrayOverrideMBSamples)
            if vrayMBSamples is not None:
                mc.setAttr("{0}.vrayOverrideMBSamples".format(shape), vrayMBSamples)


def vray_pointLight(shapes=None,
                     state=1,
                     smartConvert=True,
                     allDescendents=True,
                     vrayPhotonSubdivs=None,
                     vrayDiffuseMult=None,
                     vrayCausticSubdivs=None,
                     vrayCausticMult=None,
                     vrayCutoffThreshold=None,
                     vrayShadowBias=None,
                     vrayDiffuseContrib=None,
                     vraySpecularContrib=None,
                     vrayStoreWithIrradianceMap=None,
                     vrayOverrideMBSamples=None,
                     vrayMBSamples=None):
    """ Add/change the vray_pointLight attribute to selected meshes

    Valid node types: (spotLight, pointLight)

    :param shapes: Shapes to apply the attribute to. If shapes is None it will get
                   the shapes related to the current selection.

    :param state: If state is True it will add the subdivision attribute, else it will remove it.
    :type  state: 1 or 0

    :param allDescendents: If True it will smartConvert to allDescendent shapes.
                           e.g. this allows you to apply it to a group and all shapes in it will get object ids.
    :type  allDescendents: bool
    """

    state = _convert_state(state)
    validTypes = ("spotLight", "pointLight")

    if smartConvert or shapes is None:
        shapes = getShapes(shapes, allDescendents=allDescendents, filterType=validTypes)
    else:
        shapes = mc.ls(shapes, validTypes)

    if not shapes:
        raise RuntimeError("No shapes found to apply the vray_pointLight attribute group changes to.")

    for shape in shapes:
        mc.vray("addAttributesFromGroup", shape, "vray_pointLight", state)

        # Manage the attributes (if not None change it to the set value)
        if state:
            if vrayPhotonSubdivs is not None:
                mc.setAttr("{0}.vrayPhotonSubdivs".format(shape), vrayPhotonSubdivs)
            if vrayDiffuseMult is not None:
                mc.setAttr("{0}.vrayDiffuseMult".format(shape), vrayDiffuseMult)
            if vrayCausticSubdivs is not None:
                mc.setAttr("{0}.vrayCausticSubdivs".format(shape), vrayCausticSubdivs)
            if vrayCausticMult is not None:
                mc.setAttr("{0}.vrayCausticMult".format(shape), vrayCausticMult)
            if vrayCutoffThreshold is not None:
                mc.setAttr("{0}.vrayCutoffThreshold".format(shape), vrayCutoffThreshold)
            if vrayShadowBias is not None:
                mc.setAttr("{0}.vrayShadowBias".format(shape), vrayShadowBias)
            if vrayDiffuseContrib is not None:
                mc.setAttr("{0}.vrayDiffuseContrib".format(shape), vrayDiffuseContrib)
            if vraySpecularContrib is not None:
                mc.setAttr("{0}.vraySpecularContrib".format(shape), vraySpecularContrib)
            if vrayStoreWithIrradianceMap is not None:
                mc.setAttr("{0}.vrayStoreWithIrradianceMap".format(shape), vrayStoreWithIrradianceMap)
            if vrayOverrideMBSamples is not None:
                mc.setAttr("{0}.vrayOverrideMBSamples".format(shape), vrayOverrideMBSamples)
            if vrayMBSamples is not None:
                mc.setAttr("{0}.vrayOverrideMBSamples".format(shape), vrayMBSamples)


def vray_arealight(shapes=None,
                     state=1,
                     smartConvert=True,
                     allDescendents=True,
                     vrayPhotonSubdivs=None,
                     vrayDiffuseMult=None,
                     vrayCausticSubdivs=None,
                     vrayCausticMult=None,
                     vrayShadowBias=None,
                     vrayCutoffThreshold=None,
                     vrayDiffuseContrib=None,
                     vraySpecularContrib=None,
                     vrayInvisible=None,
                     vrayOverrideMBSamples=None,
                     vrayMBSamples=None):
    """ Add/change the vray_arealight attribute to selected meshes

    Valid node types: (areaLight)

    :param shapes: Shapes to apply the attribute to. If shapes is None it will get
                   the shapes related to the current selection.

    :param state: If state is True it will add the subdivision attribute, else it will remove it.
    :type  state: 1 or 0

    :param allDescendents: If True it will smartConvert to allDescendent shapes.
                           e.g. this allows you to apply it to a group and all shapes in it will get object ids.
    :type  allDescendents: bool
    """

    state = _convert_state(state)
    validTypes = ("areaLight")

    if smartConvert or shapes is None:
        shapes = getShapes(shapes, allDescendents=allDescendents, filterType=validTypes)
    else:
        shapes = mc.ls(shapes, validTypes)

    if not shapes:
        raise RuntimeError("No shapes found to apply the vray_pointLight attribute group changes to.")

    for shape in shapes:
        mc.vray("addAttributesFromGroup", shape, "vray_pointLight", state)

        # Manage the attributes (if not None change it to the set value)
        if state:
            if vrayPhotonSubdivs is not None:
                mc.setAttr("{0}.vrayPhotonSubdivs".format(shape), vrayPhotonSubdivs)
            if vrayDiffuseMult is not None:
                mc.setAttr("{0}.vrayDiffuseMult".format(shape), vrayDiffuseMult)
            if vrayCausticSubdivs is not None:
                mc.setAttr("{0}.vrayCausticSubdivs".format(shape), vrayCausticSubdivs)
            if vrayCausticMult is not None:
                mc.setAttr("{0}.vrayCausticMult".format(shape), vrayCausticMult)
            if vrayShadowBias is not None:
                mc.setAttr("{0}.vrayShadowBias".format(shape), vrayShadowBias)
            if vrayCutoffThreshold is not None:
                mc.setAttr("{0}.vrayCutoffThreshold".format(shape), vrayCutoffThreshold)
            if vrayDiffuseContrib is not None:
                mc.setAttr("{0}.vrayDiffuseContrib".format(shape), vrayDiffuseContrib)
            if vraySpecularContrib is not None:
                mc.setAttr("{0}.vraySpecularContrib".format(shape), vraySpecularContrib)
            if vrayInvisible is not None:
                mc.setAttr("{0}.vrayStoreWithIrradianceMap".format(shape), vrayInvisible)
            if vrayOverrideMBSamples is not None:
                mc.setAttr("{0}.vrayOverrideMBSamples".format(shape), vrayOverrideMBSamples)
            if vrayMBSamples is not None:
                mc.setAttr("{0}.vrayOverrideMBSamples".format(shape), vrayMBSamples)