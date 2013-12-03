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

    Many (if not all) attribute functions come with a smartConvert parameter that is True by default.
    It allows the input list to be interpreted as 'get related objects that can have this attribute'.
    This means you can actually apply a `vray_material_id` to a mesh.
    It will get the related assigned material and applies it to that. Easy right?

    If you don't want this automatic conversion doing anything you can set the smartConvert parameter to False.

        - ##### allowTransform parameter

            Some functions might have an allowTransform parameter. This is used for functions that can be applied to
            both shapes as well as transforms. Setting this parameter to True will interpret transform nodes as actual
            nodes to add the attributes to (instead of trying to do a smartConvert). Note that setting allowTransform
            to True actually forces smartConvert to False.

        - ##### allDescendents parameter

            Attribute functions that are applied to shapes can have an allDescendents parameter. This allows the input
            list to be converted to children and it's children children. This allows a group to be used as input and all
            of it's children shapes in the hierarchy will get the attribute. Note that this is (in the relevant cases)
            True by default. So if you only want to apply to direct children of a transform when using smartConvert
            make sure you set allDescendents to False.


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
    :rtype: int
    """
    if not isinstance(state, int) or isinstance(state, bool):
        try:
            state = int(state)
        except (ValueError, TypeError):
            raise TypeError("state argument must be an int or to int convertable type, not {0}".format(type(state)))
    return state


def _convert_input_shapes(shapes=None, smartConvert=True, allDescendents=True, filterType=None, allowTransform=False):
    """
        Converts a input list for shapes (and possibly transforms) to allow for simple smartConvert implementation.
    """
    # If we allow transforms we will NOT Smart Convert to related shapes.
    # Instead we will get transforms + shapes directly from input list or selection
    if allowTransform:
        smartConvert = False

        # Convert string filterType to tuple so we can add the transform to it. :)
        if isinstance(filterType, basestring):
            filterType = (filterType,)

        filterType = filterType + ("transform",)

    # If None provided as input list use selection
    if shapes is None:
        shapes = mc.ls(sl=1, long=True)

    # Convert to related shapes if smartConvert else get directly from input shapes.
    if smartConvert:
        shapes = getShapes(shapes, allDescendents=allDescendents, filterType=filterType)
    else:
        shapes = mc.ls(shapes, filterType, long=True)

    return shapes


#####################
# mesh, nurbsSurface
#####################

def vray_object_id(shapes=None,
                     state=1,
                     smartConvert=True,
                     allDescendents=True,
                     allowTransform=False,
                     vrayObjectID=None):
    """ Add/change the vray_object_id attribute to selected meshes

    Valid node types: (mesh, nurbsSurface, VRayLightDomeShape, VRayLightRectShape, VRayLightSphereShape, transform)

    The v-ray object ID can be applied to transform nodes as well, that means the transform of a mesh or even a parent
    group. Though the lowest in hierarchy will always override the others, i.e.:

        - Group (=Transform)    (3rd)
            - Transform         (2nd)
                - Shape         (1st)

    By default this function excludes transforms and will force it to actual shapes. If you want to apply to transform
    nodes set the allowTransform parameter to True. Note that this will force smartConvert to False.

    :param shapes: Shapes to apply the attribute to. If shapes is None it will get
                   the shapes related to the current selection.

    :param state: If state is True it will add the attribute, else it will remove it.
    :type  state: 1 or 0

    :param smartConvert: If True it will convert the input smartly to related shape nodes.
    :type  smartConvert: bool

    :param allDescendents: If True it will smartConvert to allDescendent shapes.
                           e.g. this allows you to apply it to a group and all shapes in it will get object ids.
    :type  allDescendents: bool

    :param allowTransform: If True it will interpret transform nodes as actual valid objects.
                           This means it will NOT smartConvert, so when True this will override smartConvert to False.
    :type  allowTransform: bool

    :param vrayObjectID: The object ID number value. If None remains default/unchanged.
    :type  vrayObjectID: None or int
    """
    state = _convert_state(state)

    validTypes = ("mesh",
                  "nurbsSurface",
                  "VRayLightDomeShape",
                  "VRayLightRectShape",
                  "VRayLightSphereShape")
    shapes = _convert_input_shapes(shapes=shapes, smartConvert=smartConvert, allDescendents=allDescendents,
                                   filterType=validTypes, allowTransform=allowTransform)

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
                     allowTransform=False,
                     vrayUserAttributes=None):
    """ Add/change the User Attributes (vray_user_attributes) attribute to input shapes/transforms.

    Valid node types: (mesh, nurbsSurface, transform)

    By default this function excludes transforms and will force it to actual shapes. If you want to apply to transform
    nodes set the allowTransform parameter to True. Note that this will force smartConvert to False.

    :param shapes: Shapes to apply the attribute to. If shapes is None it will get
                   the shapes related to the current selection.

    :param state: If state is True it will add the attribute, else it will remove it.
    :type  state: 1 or 0

    :param smartConvert: If True it will convert the input smartly to related shape nodes.
    :type  smartConvert: bool

    :param allDescendents: If True it will smartConvert to allDescendent shapes.
                           e.g. this allows you to apply it to a group and all shapes in it will get object ids.
    :type  allDescendents: bool

    :param allowTransform: If True it will interpret transform nodes as actual valid objects.
                           This means it will NOT smartConvert, so when True this will override smartConvert to False.
    :type  allowTransform: bool

    :param vrayUserAttributes: The actual user attribute string value. If None it remains default/unchanged.
    :type  vrayUserAttributes: None or str
    """

    state = _convert_state(state)

    validTypes = ("mesh", "nurbsSurface")
    shapes = _convert_input_shapes(shapes=shapes, smartConvert=smartConvert, allDescendents=allDescendents,
                                   filterType=validTypes, allowTransform=allowTransform)

    if not shapes:
        raise RuntimeError("No shapes found to apply the vray_user_attributes attribute group changes to.")

    for shape in shapes:
        mc.vray("addAttributesFromGroup", shape, "vray_user_attributes", state)

        # Manage the attributes (if not None change it to the set value)
        if state:
            if vrayUserAttributes is not None:
                mc.setAttr("{0}.vrayUserAttributes".format(shape), vrayUserAttributes, type="string")


##########
# mesh
##########

def vray_subdivision(shapes=None,
                     state=1,
                     smartConvert=True,
                     allDescendents=True,
                     vraySubdivEnable=None,
                     vraySubdivUVs=None,
                     vrayPreserveMapBorders=None,
                     vrayStaticSubdiv=None,
                     vrayClassicalCatmark=None):
    """ Add/change the Subdivision (vray_subdivision) attribute to input meshes.

    Valid node types: (mesh)

    :param shapes: Shapes to apply the attribute to. If shapes is None it will get
                   the shapes related to the current selection.

    :param state: If state is True it will add the attribute, else it will remove it.
    :type  state: 1 or 0

    :param allDescendents: If True it will smartConvert to allDescendent shapes.
                           e.g. this allows you to apply it to a group and all shapes in it will get object ids.
    :type  allDescendents: bool

    :param vraySubdivEnable: Enable/disable the subdivisions. If None it remains default/unchanged.
    :type  vraySubdivEnable: None or bool

    :param vraySubdivUVs: Enable/disable the smoothing of the UVs. If None it remains default/unchanged.
    :type  vraySubdivUVs: None or bool

    :param vrayPreserveMapBorders: Set the method of preserve map borders.
                                   Enum attribute:
                                       0. None,
                                       1. Internal,
                                       2. All
    :type  vrayPreserveMapBorders: None or int (0-2)

    :param vrayStaticSubdiv: Enable/disable vrayStaticSubdiv. If None it remains default/unchanged.
    :type  vrayStaticSubdiv: None or bool

    :param vrayClassicalCatmark: Enable/disable vrayClassicalCatmark. If None it remains default/unchanged.
    :type  vrayClassicalCatmark: None or bool
    """

    state = _convert_state(state)

    validTypes = ("mesh")
    shapes = _convert_input_shapes(shapes=shapes, smartConvert=smartConvert, allDescendents=allDescendents,
                                   filterType=validTypes)

    if not shapes:
        raise RuntimeError("No meshes found to apply the vray_subdivision attribute group changes to.")

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


def vray_subquality(shapes=None,
                     state=1,
                     smartConvert=True,
                     allDescendents=True,
                     vrayOverrideGlobalSubQual=None,
                     vrayViewDep=None,
                     vrayEdgeLength=None,
                     vrayMaxSubdivs=None):
    """ Add/change the Subdivision and Displacement Quality (vray_subquality) attribute to input meshes

    Valid node types: (mesh)

    :param shapes: Shapes to apply the attribute to. If shapes is None it will get
                   the shapes related to the current selection.

    :param state: If state is True it will add the attribute, else it will remove it.
    :type  state: 1 or 0

    :param allDescendents: If True it will smartConvert to allDescendent shapes.
                           e.g. this allows you to apply it to a group and all shapes in it will get object ids.
    :type  allDescendents: bool

    :param vrayOverrideGlobalSubQual: Enable/disable override global settings. If None it remains default/unchanged.
    :type  vrayOverrideGlobalSubQual: None or bool

    :param vrayViewDep: Enable/disable view dependent. If None it remains default/unchanged.
    :type  vrayViewDep: None or bool

    :param vrayEdgeLength: Set the edge length. If None it remains default/unchanged.
    :type  vrayEdgeLength: None or float

    :param vrayMaxSubdivs: Set the maximum subdivisions. If None it remains default/unchanged.
    :type  vrayMaxSubdivs: None or int
    """

    state = _convert_state(state)

    validTypes = ("mesh")
    shapes = _convert_input_shapes(shapes=shapes, smartConvert=smartConvert, allDescendents=allDescendents,
                                   filterType=validTypes)

    if not shapes:
        raise RuntimeError("No meshes found to apply the vray_subquality attribute group changes to.")

    for shape in shapes:
        mc.vray("addAttributesFromGroup", shape, "vray_subquality", state)

        # Manage the attributes (if not None change it to the set value)
        if state:
            if vrayOverrideGlobalSubQual is not None:
                mc.setAttr("{0}.vrayOverrideGlobalSubQual".format(shape), vrayOverrideGlobalSubQual)
            if vrayViewDep is not None:
                mc.setAttr("{0}.vrayViewDep".format(shape), vrayViewDep)
            if vrayEdgeLength is not None:
                mc.setAttr("{0}.vrayEdgeLength".format(shape), vrayEdgeLength)
            if vrayMaxSubdivs is not None:
                mc.setAttr("{0}.vrayMaxSubdivs".format(shape), vrayMaxSubdivs)


def vray_displacement(shapes=None,
                     state=1,
                     smartConvert=True,
                     allDescendents=True,
                     vrayDisplacementNone=None,
                     vrayDisplacementStatic=None,
                     vrayDisplacementType=None,
                     vrayDisplacementAmount=None,
                     vrayDisplacementShift=None,
                     vrayDisplacementKeepContinuity=None,
                     vrayEnableWaterLevel=None,
                     vrayWaterLevel=None,
                     vray2dDisplacementResolution=None,
                     vray2dDisplacementPrecision=None,
                     vray2dDisplacementTightBounds=None,
                     vray2dDisplacementFilterTexture=None,
                     vray2dDisplacementFilterBlur=None,
                     vrayDisplacementUseBounds=None,
                     vrayDisplacementMinValue=None,
                     vrayDisplacementMaxValue=None):
    """ Add/change the Displacement Control (vray_displacement) attribute to input meshes.

    Valid node types: (mesh)

    :param shapes: Shapes to apply the attribute to. If shapes is None it will get
                   the shapes related to the current selection.

    :param state: If state is True it will add the attribute, else it will remove it.
    :type  state: 1 or 0

    :param allDescendents: If True it will smartConvert to allDescendent shapes.
                           e.g. this allows you to apply it to a group and all shapes in it will get object ids.
    :type  allDescendents: bool

    :param vrayDisplacementNone: Enable/disable override global settings. If None it remains default/unchanged.
    :type  vrayDisplacementNone: None or bool

    :param vrayDisplacementStatic: Enable/disable view dependent. If None it remains default/unchanged.
    :type  vrayDisplacementStatic: None or bool

    :param vrayDisplacementType: Set the displacement type. If None it remains default/unchanged.
                                 Enum attribute:
                                    0. 2D Displacement,
                                    1. Normal Displacement,
                                    2. Vector Displacement,
                                    3. Vector Displacement (absolute),
                                    4. Vector Displacement (object)
    :type  vrayDisplacementType: None or int (0-4)

    :param vrayDisplacementAmount: Set the displacement amount. If None it remains default/unchanged.
    :type  vrayDisplacementAmount: None or int

    :param vrayDisplacementShift: Set the displacement shift. If None it remains default/unchanged.
    :type  vrayDisplacementShift: None or int

    :param vrayDisplacementKeepContinuity: Enable/disable keep continuity. If None it remains default/unchanged.
    :type  vrayDisplacementKeepContinuity: None or bool

    :param vrayEnableWaterLevel: Enable/disable water level. If None it remains default/unchanged.
    :type  vrayEnableWaterLevel: None or bool

    :param vrayWaterLevel: Set the water level. If None it remains default/unchanged.
    :type  vrayWaterLevel: None or float

    :param vray2dDisplacementResolution: Set the texture resolution. If None it remains default/unchanged.
    :type  vray2dDisplacementResolution: None or int

    :param vray2dDisplacementPrecision: Set the texture precision. If None it remains default/unchanged.
    :type  vray2dDisplacementPrecision: None or int

    :param vray2dDisplacementTightBounds: Enable/disable tight bounds. If None it remains default/unchanged.
    :type  vray2dDisplacementTightBounds: None or bool

    :param vray2dDisplacementFilterTexture: Enable/disable filter texture. If None it remains default/unchanged.
    :type  vray2dDisplacementFilterTexture: None or bool

    :param vray2dDisplacementFilterBlur: Set the filter blur amount. If None it remains default/unchanged.
    :type  vray2dDisplacementFilterBlur: None or float

    :param vrayDisplacementUseBounds: Set the displacement bounds. If None it remains default/unchanged.
                                      Enum attribute:
                                         0. Automatic,
                                         1. Explicit
    :type  vrayDisplacementUseBounds: None or int (0-1)

    :param vrayDisplacementMinValue: Set the min value bounds. If None it remains default/unchanged.
    :type  vrayDisplacementMinValue: None or double3

    :param vrayDisplacementMaxValue: Set the min value bounds. If None it remains default/unchanged.
    :type  vrayDisplacementMaxValue: None or double3

    """

    state = _convert_state(state)

    validTypes = ("mesh")
    shapes = _convert_input_shapes(shapes=shapes, smartConvert=smartConvert, allDescendents=allDescendents,
                                   filterType=validTypes)

    if not shapes:
        raise RuntimeError("No meshes found to apply the vray_displacement attribute group changes to.")

    for shape in shapes:
        mc.vray("addAttributesFromGroup", shape, "vray_displacement", state)

        # Manage the attributes (if not None change it to the set value)
        if state:

            if vrayDisplacementNone is not None:
                mc.setAttr("{0}.vrayDisplacementNone".format(shape), vrayDisplacementNone)
            if vrayDisplacementStatic is not None:
                mc.setAttr("{0}.vrayDisplacementStatic".format(shape), vrayDisplacementStatic)
            if vrayDisplacementType is not None:
                mc.setAttr("{0}.vrayDisplacementType".format(shape), vrayDisplacementType)
            if vrayDisplacementAmount is not None:
                mc.setAttr("{0}.vrayDisplacementAmount".format(shape), vrayDisplacementAmount)
            if vrayDisplacementShift is not None:
                mc.setAttr("{0}.vrayDisplacementShift".format(shape), vrayDisplacementShift)
            if vrayDisplacementKeepContinuity is not None:
                mc.setAttr("{0}.vrayDisplacementKeepContinuity".format(shape), vrayDisplacementKeepContinuity)
            if vrayEnableWaterLevel is not None:
                mc.setAttr("{0}.vrayEnableWaterLevel".format(shape), vrayEnableWaterLevel)
            if vrayWaterLevel is not None:
                mc.setAttr("{0}.vrayWaterLevel".format(shape), vrayWaterLevel)
            if vray2dDisplacementResolution is not None:
                mc.setAttr("{0}.vray2dDisplacementResolution".format(shape), vray2dDisplacementResolution)
            if vray2dDisplacementPrecision is not None:
                mc.setAttr("{0}.vray2dDisplacementPrecision".format(shape), vray2dDisplacementPrecision)
            if vray2dDisplacementTightBounds is not None:
                mc.setAttr("{0}.vray2dDisplacementTightBounds".format(shape), vray2dDisplacementTightBounds)
            if vray2dDisplacementFilterTexture is not None:
                mc.setAttr("{0}.vray2dDisplacementFilterTexture".format(shape), vray2dDisplacementFilterTexture)
            if vray2dDisplacementFilterBlur is not None:
                mc.setAttr("{0}.vray2dDisplacementFilterBlur".format(shape), vray2dDisplacementFilterBlur)
            if vrayDisplacementUseBounds is not None:
                mc.setAttr("{0}.vrayDisplacementUseBounds".format(shape), vrayDisplacementUseBounds)
            if vrayDisplacementMinValue is not None:
                mc.setAttr("{0}.vrayDisplacementMinValue".format(shape), vrayDisplacementMinValue)
            if vrayDisplacementMaxValue is not None:
                mc.setAttr("{0}.vrayDisplacementMaxValue".format(shape), vrayDisplacementMaxValue)


def vray_roundedges(shapes=None,
                     state=1,
                     smartConvert=True,
                     allDescendents=True,
                     vrayRoundEdges=None,
                     vrayRoundEdgesRadius=None):
    """ Add/change the Round Edges (vray_roundedges) attribute to input meshes.

    Valid node types: (mesh, shadingEngine)

    :param shapes: Shapes to apply the attribute to. If shapes is None it will get
                   the shapes related to the current selection.

    :param state: If state is True it will add the attribute, else it will remove it.
    :type  state: 1 or 0

    :param allDescendents: If True it will smartConvert to allDescendent shapes.
                           e.g. this allows you to apply it to a group and all shapes in it will get object ids.
    :type  allDescendents: bool

    :param vrayRoundEdges: Enable/disable round edges. If None it remains default/unchanged.
    :type  vrayRoundEdges: None or bool

    :param vrayRoundEdgesRadius: Set the round edges radius. If None it remains default/unchanged.
    :type  vrayRoundEdgesRadius: None or float
    """
    # TODO: Support mode to apply vray_roundedges on shadingEngine instead of material

    state = _convert_state(state)

    validTypes = ("mesh")
    shapes = _convert_input_shapes(shapes=shapes, smartConvert=smartConvert, allDescendents=allDescendents,
                                   filterType=validTypes)

    if not shapes:
        raise RuntimeError("No meshes found to apply the vray_roundedges attribute group changes to.")

    for shape in shapes:
        mc.vray("addAttributesFromGroup", shape, "vray_roundedges", state)

        # Manage the attributes (if not None change it to the set value)
        if state:
            if vrayRoundEdges is not None:
                mc.setAttr("{0}.vrayRoundEdges".format(shape), vrayRoundEdges)
            if vrayRoundEdgesRadius is not None:
                mc.setAttr("{0}.vrayRoundEdgesRadius".format(shape), vrayRoundEdgesRadius)


def vray_fogFadeOut(shapes=None,
                     state=1,
                     smartConvert=True,
                     allDescendents=True,
                     vrayFogFadeOut=None):
    """ Add/change the Subdivision (vray_fogFadeOut) attribute to input meshes.

    Valid node types: (mesh)

    :param shapes: Shapes to apply the attribute to. If shapes is None it will get
                   the shapes related to the current selection.

    :param state: If state is True it will add the attribute, else it will remove it.
    :type  state: 1 or 0

    :param allDescendents: If True it will smartConvert to allDescendent shapes.
                           e.g. this allows you to apply it to a group and all shapes in it will get object ids.
    :type  allDescendents: bool

    :param vrayFogFadeOut: Set the fog fade out radius. If None it remains default/unchanged.
    :type  vrayFogFadeOut: None or float
    """

    state = _convert_state(state)

    validTypes = ("mesh")
    shapes = _convert_input_shapes(shapes=shapes, smartConvert=smartConvert, allDescendents=allDescendents,
                                   filterType=validTypes)

    if not shapes:
        raise RuntimeError("No meshes found to apply the vray_fogFadeOut attribute group changes to.")

    for shape in shapes:
        mc.vray("addAttributesFromGroup", shape, "vray_fogFadeOut", state)

        # Manage the attributes (if not None change it to the set value)
        if state:
            if vrayFogFadeOut is not None:
                mc.setAttr("{0}.vrayFogFadeOut".format(shape), vrayFogFadeOut)


def vray_phoenix_object(shapes=None,
                     state=1,
                     smartConvert=True,
                     allDescendents=True,
                     vrayPhoenixObjVoxels=None):
    """ Add/change the Phoenix Object Properties (vray_phoenix_object) attribute to input meshes.

    Valid node types: (mesh)

    V-ray version: Seen since 2.4+ nightly builds.

    :param shapes: Shapes to apply the attribute to. If shapes is None it will get
                   the shapes related to the current selection.

    :param state: If state is True it will add the attribute, else it will remove it.
    :type  state: 1 or 0

    :param allDescendents: If True it will smartConvert to allDescendent shapes.
                           e.g. this allows you to apply it to a group and all shapes in it will get object ids.
    :type  allDescendents: bool

    :param vrayPhoenixObjVoxels: Set the phoenix object voxels. If None it remains default/unchanged.
                                 Enum attribute:
                                    0. Circumscribed,
                                    1. Center,
                                    2. Inscribed
    :type  vrayPhoenixObjVoxels: None or int (0-2)
    """

    state = _convert_state(state)

    validTypes = ("mesh")
    shapes = _convert_input_shapes(shapes=shapes, smartConvert=smartConvert, allDescendents=allDescendents,
                                   filterType=validTypes)

    if not shapes:
        raise RuntimeError("No meshes found to apply the vray_phoenix_object attribute group changes to.")

    for shape in shapes:
        mc.vray("addAttributesFromGroup", shape, "vray_phoenix_object", state)

        # Manage the attributes (if not None change it to the set value)
        if state:
            if vrayPhoenixObjVoxels is not None:
                mc.setAttr("{0}.vrayPhoenixObjVoxels".format(shape), vrayPhoenixObjVoxels)

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

    Valid node types: (nurbsSurface)

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

    validTypes = ("nurbsSurface")
    shapes = _convert_input_shapes(shapes=shapes, smartConvert=smartConvert, allDescendents=allDescendents,
                                   filterType=validTypes)

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
## nurbsCurve
##############

def vray_nurbscurve_renderable(shapes=None,
                     state=1,
                     smartConvert=True,
                     allDescendents=True,
                     vrayNurbsCurveRenderable=None,
                     vrayNurbsCurveMaterial=None,
                     vrayNurbsCurveTesselation=None,
                     vrayNurbsCurveStartWidth=None,
                     vrayNurbsCurveLockEndWidth=None,
                     vrayNurbsCurveEndWidth=None):
    """ Add/change the vray_nurbscurve_renderable attribute to input nurbsCurves.

    Valid node types: (nurbsCurve)

    :param shapes: Shapes to apply the attribute to. If shapes is None it will get
                   the shapes related to the current selection.

    :param state: If state is True it will add the attribute, else it will remove it.
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

    shapes = _convert_input_shapes(shapes=shapes, smartConvert=smartConvert, allDescendents=allDescendents,
                                   filterType=validTypes)

    if not shapes:
        raise RuntimeError("No shapes found to apply the vray_object_id attribute group changes to.")

    for shape in shapes:
        mc.vray("addAttributesFromGroup", shape, "vray_nurbscurve_renderable", state)

        # Manage the attributes (if not None change it to the set value)
        if state:
            if vrayNurbsCurveRenderable is not None:
                mc.setAttr("{0}.vrayNurbsCurveRenderable".format(shape), vrayNurbsCurveRenderable)

            # TODO: Test if this works, it's likely that this needs to have a connection instead of 'value'
            if vrayNurbsCurveMaterial is not None:
                mc.setAttr("{0}.vrayNurbsCurveMaterial".format(shape), vrayNurbsCurveMaterial)

            if vrayNurbsCurveTesselation is not None:
                mc.setAttr("{0}.vrayNurbsCurveTesselation".format(shape), vrayNurbsCurveTesselation)
            if vrayNurbsCurveStartWidth is not None:
                mc.setAttr("{0}.vrayNurbsCurveStartWidth".format(shape), vrayNurbsCurveStartWidth)
            if vrayNurbsCurveLockEndWidth is not None:
                mc.setAttr("{0}.vrayNurbsCurveLockEndWidth".format(shape), vrayNurbsCurveLockEndWidth)
            if vrayNurbsCurveEndWidth is not None:
                mc.setAttr("{0}.vrayNurbsCurveEndWidth".format(shape), vrayNurbsCurveEndWidth)


##############
## materials
##############

def vray_material_id(materials=None,
                     state=1,
                     smartConvert=True,
                     vrayMaterialId=None):
    """ Add/change the v-ray material ID attribute to input materials.

    Valid node types: (material, shadingEngine)

    :param materials: Materials to apply the attribute to. If materials is None it will get
                      the materials related to the current selection.

    :param state: If state is True it will add the attribute, else it will remove it.
    :type  state: 1 or 0

    :param smartConvert: If True the input materials list will be checked for 'related materials'
                         and those found will be included. Else it will on
                         If no materials provided smartConvert is forced to True and it will get
                         materials related to the current selection.
    :type  smartConvert: bool

    :param vrayMaterialId: The material ID number value. If None it will remain default/unchanged.
    :type  vrayMaterialId: None or int
    """
    # TODO: Support mode to apply material ID on shadingEngine instead of material

    state = _convert_state(state)

    if materials is None:
        materials = mc.ls(sl=1)

    if smartConvert:
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

    Valid node types: (material, shadingEngine)

    :param materials: Materials to apply the attribute to. If materials is None it will get
                      the materials related to the current selection.

    :param state: If state is True it will add the attribute, else it will remove it.
    :type  state: 1 or 0

    :param smartConvert: If True the input materials list will be checked for 'related materials'
                         and those found will be included. Else it will on
                         If no materials provided smartConvert is forced to True and it will get
                         materials related to the current selection.
    :type  smartConvert: bool
    """
    # TODO: Support mode to apply vray_specific_mtl on shadingEngine instead of material
    # TODO: Add change attribute value support
    state = _convert_state(state)

    if materials is None:
        materials = mc.ls(sl=1)

    if smartConvert:
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
                     smartConvert=True,
                     vrayClosedVolume=None):
    """ Add/change the v-ray closed volume shading attribute to input materials.

    Valid node types: (v-ray material)

    :param materials: Materials to apply the attribute to. If materials is None it will get
                      the materials related to the current selection.

    :param state: If state is True it will add the attribute, else it will remove it.
    :type  state: 1 or 0

    :param smartConvert: If True the input materials list will be checked for 'related materials'
                         and those found will be included. Else it will on
                         If no materials provided smartConvert is forced to True and it will get
                         materials related to the current selection.
    :type  smartConvert: bool

    :param vrayClosedVolume: Enable/Disable Closed Volume Shading. If None it remains default/unchanged.
    :type  vrayClosedVolume: bool
    """
    # TODO: Add check if node is a valid v-ray material that can have closed volume shading

    state = _convert_state(state)

    if materials is None:
        materials = mc.ls(sl=1)

    if smartConvert:
        materials = getMaterials(materials)
    else:
        materials = mc.ls(materials, mat=True)


    if not materials:
        raise RuntimeError("No materials found")

    for mat in materials:
        mc.vray("addAttributesFromGroup", mat, "vray_closed_volume", state)

        # Manage the attributes (if not None change it to the set value)
        if state:
            if vrayClosedVolume is not None:
                mc.setAttr("{0}.{1}".format(mat, 'vrayClosedVolume'), vrayClosedVolume)


##############
## camera
##############

def vray_cameraPhysical(shapes=None,
                     state=1,
                     smartConvert=True,
                     allDescendents=True):
    """ Add/change the vray_cameraPhysical attribute to selected meshes

    Valid node types: (camera)

    :param shapes: Shapes to apply the attribute to. If shapes is None it will get
                   the shapes related to the current selection.

    :param state: If state is True it will add the attribute, else it will remove it.
    :type  state: 1 or 0

    :param allDescendents: If True it will smartConvert to allDescendent shapes.
                           e.g. this allows you to apply it to a group and all shapes in it will get object ids.
    :type  allDescendents: bool
    """

    state = _convert_state(state)
    validTypes = ("camera")

    shapes = _convert_input_shapes(shapes=shapes, smartConvert=smartConvert, allDescendents=allDescendents,
                                   filterType=validTypes)

    if not shapes:
        raise RuntimeError("No cameras found to apply the vray_cameraPhysical attribute group changes to.")

    for shape in shapes:
        mc.vray("addAttributesFromGroup", shape, "vray_cameraPhysical", state)


def vray_cameraOverrides(shapes=None,
                     state=1,
                     smartConvert=True,
                     allDescendents=True,
                     vrayCameraOverridesOn=None,
                     vrayCameraType=None,
                     vrayCameraOverrideFOV=None,
                     vrayCameraFOV=None,
                     vrayCameraHeight=None,
                     vrayCameraAutoFit=None,
                     vrayCameraDist=None,
                     vrayCameraCurve=None):
    """ Add/change the vray_cameraOverrides attribute to selected meshes

    Valid node types: (camera)

    :param shapes: Shapes to apply the attribute to. If shapes is None it will get
                   the shapes related to the current selection.

    :param state: If state is True it will add the attribute, else it will remove it.
    :type  state: 1 or 0

    :param allDescendents: If True it will smartConvert to allDescendent shapes.
                           e.g. this allows you to apply it to a group and all shapes in it will get object ids.
    :type  allDescendents: bool
    """

    state = _convert_state(state)
    validTypes = ("camera")

    shapes = _convert_input_shapes(shapes=shapes, smartConvert=smartConvert, allDescendents=allDescendents,
                                   filterType=validTypes)

    if not shapes:
        raise RuntimeError("No cameras found to apply the vray_cameraOverrides attribute group changes to.")

    for shape in shapes:
        mc.vray("addAttributesFromGroup", shape, "vray_cameraOverrides", state)

        # Manage the attributes (if not None change it to the set value)
        if state:
            if vrayCameraOverridesOn is not None:
                mc.setAttr("{0}.vrayCameraOverridesOn".format(shape), vrayCameraOverridesOn)
            if vrayCameraType is not None:
                mc.setAttr("{0}.vrayCameraType".format(shape), vrayCameraType)
            if vrayCameraOverrideFOV is not None:
                mc.setAttr("{0}.vrayCameraOverrideFOV".format(shape), vrayCameraOverrideFOV)
            if vrayCameraFOV is not None:
                mc.setAttr("{0}.vrayCameraFOV".format(shape), vrayCameraFOV)
            if vrayCameraHeight is not None:
                mc.setAttr("{0}.vrayCameraHeight".format(shape), vrayCameraHeight)
            if vrayCameraAutoFit is not None:
                mc.setAttr("{0}.vrayCameraAutoFit".format(shape), vrayCameraAutoFit)
            if vrayCameraDist is not None:
                mc.setAttr("{0}.vrayCameraDist".format(shape), vrayCameraDist)
            if vrayCameraCurve is not None:
                mc.setAttr("{0}.vrayCameraCurve".format(shape), vrayCameraCurve)


def vray_cameraDome(shapes=None,
                     state=1,
                     smartConvert=True,
                     allDescendents=True,
                     vrayCameraDomeOn=None,
                     vrayCameraDomeFlipX=None,
                     vrayCameraDomeFlipY=None,
                     vrayCameraDomeFov=None):
    """ Add/change the vray_cameraDome attribute to selected meshes

    Valid node types: (camera)

    :param shapes: Shapes to apply the attribute to. If shapes is None it will get
                   the shapes related to the current selection.

    :param state: If state is True it will add the attribute, else it will remove it.
    :type  state: 1 or 0

    :param allDescendents: If True it will smartConvert to allDescendent shapes.
                           e.g. this allows you to apply it to a group and all shapes in it will get object ids.
    :type  allDescendents: bool
    """

    state = _convert_state(state)
    validTypes = ("camera")

    shapes = _convert_input_shapes(shapes=shapes, smartConvert=smartConvert, allDescendents=allDescendents,
                                   filterType=validTypes)

    if not shapes:
        raise RuntimeError("No cameras found to apply the vray_cameraDome attribute group changes to.")

    for shape in shapes:
        mc.vray("addAttributesFromGroup", shape, "vray_cameraDome", state)

        # Manage the attributes (if not None change it to the set value)
        if state:
            if vrayCameraDomeOn is not None:
                mc.setAttr("{0}.vrayCameraDomeOn".format(shape), vrayCameraDomeOn)
            if vrayCameraDomeFlipX is not None:
                mc.setAttr("{0}.vrayCameraDomeFlipX".format(shape), vrayCameraDomeFlipX)
            if vrayCameraDomeFlipY is not None:
                mc.setAttr("{0}.vrayCameraDomeFlipY".format(shape), vrayCameraDomeFlipY)
            if vrayCameraDomeFov is not None:
                mc.setAttr("{0}.vrayCameraDomeFov".format(shape), vrayCameraDomeFov)


##############
## lights
## These are seperated per light type like:
## - pointLight, spotLight (vray_pointLight)
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

    :param state: If state is True it will add the attribute, else it will remove it.
    :type  state: 1 or 0

    :param allDescendents: If True it will smartConvert to allDescendent shapes.
                           e.g. this allows you to apply it to a group and all shapes in it will get object ids.
    :type  allDescendents: bool
    """

    state = _convert_state(state)
    validTypes = ("ambientLight")

    shapes = _convert_input_shapes(shapes=shapes, smartConvert=smartConvert, allDescendents=allDescendents,
                                   filterType=validTypes)

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

    :param state: If state is True it will add the attribute, else it will remove it.
    :type  state: 1 or 0

    :param allDescendents: If True it will smartConvert to allDescendent shapes.
                           e.g. this allows you to apply it to a group and all shapes in it will get object ids.
    :type  allDescendents: bool
    """

    state = _convert_state(state)
    validTypes = ("directionalLight")

    shapes = _convert_input_shapes(shapes=shapes, smartConvert=smartConvert, allDescendents=allDescendents,
                                   filterType=validTypes)

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

    :param state: If state is True it will add the attribute, else it will remove it.
    :type  state: 1 or 0

    :param allDescendents: If True it will smartConvert to allDescendent shapes.
                           e.g. this allows you to apply it to a group and all shapes in it will get object ids.
    :type  allDescendents: bool
    """

    state = _convert_state(state)
    validTypes = ("spotLight", "pointLight")

    shapes = _convert_input_shapes(shapes=shapes, smartConvert=smartConvert, allDescendents=allDescendents,
                                   filterType=validTypes)

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

    :param state: If state is True it will add the attribute, else it will remove it.
    :type  state: 1 or 0

    :param allDescendents: If True it will smartConvert to allDescendent shapes.
                           e.g. this allows you to apply it to a group and all shapes in it will get object ids.
    :type  allDescendents: bool
    """

    state = _convert_state(state)
    validTypes = ("areaLight")

    shapes = _convert_input_shapes(shapes=shapes, smartConvert=smartConvert, allDescendents=allDescendents,
                                   filterType=validTypes)

    if not shapes:
        raise RuntimeError("No shapes found to apply the vray_arealight attribute group changes to.")

    for shape in shapes:
        mc.vray("addAttributesFromGroup", shape, "vray_arealight", state)

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


##############
## file
##############
#TODO: Add: Texture input Gamma (vray_file_gamma)
# Input Gamma is allowed on: (File, VRayPTex, Substance nodes, imagePlane)
#TODO: Add: Allow negative colors (vray_file_allow_neg_colors)
# Allow negative colors is allowed on: (File, Substance nodes, imagePlane)
#TODO: Add: Image file list (IFL) (vray_file_ifl)
# Allow negative colors is allowed on: (File)
#TODO: Add: Texture Filter (vray_texture_filter)
# Allow negative colors is allowed on: (File, Substance)


###################
## place2dTexture
###################

def vray_2d_placement_options(nodes=None,
                     state=1,
                     smartConvert=True,
                     vrayUVSetName=None):
    """ Add/change the 2D Placement Options (vray_2d_placement_options) attribute to input place2dTexture nodes.

    Valid node types: (place2dTexture)

    :param nodes: nodes to apply the attribute to. If nodes is None it will get
                  the nodes related to the current selection.

    :param smartConvert: CURRENTLY NO IMPLEMENTATION
    :type  smartConvert: bool

    :param state: If state is True it will add the attribute, else it will remove it.
    :type  state: 1 or 0

    :param vrayUVSetName: Set the UV set name attribute string value. If None it remains default/unchanged.
    :type  vrayUVSetName: None or str
    """

    state = _convert_state(state)
    validTypes = ("place2dTexture")

    if nodes is None:
        nodes = mc.ls(sl=1, long=True)

    if smartConvert:
        # TODO: Implement smart convert
        pass

    nodes = mc.ls(nodes, type=validTypes, long=True)

    if not nodes:
        raise RuntimeError("No place2dTexture found to apply the vray_2d_placement_options attribute changes to.")

    for node in nodes:
        mc.vray("addAttributesFromGroup", node, "vray_2d_placement_options", state)

        # Manage the attributes (if not None change it to the set value)
        if state:
            if vrayUVSetName is not None:
                mc.setAttr("{0}.vrayUVSetName".format(node), vrayUVSetName, type="string")


###################
## samplerInfo
###################

def vray_samplerinfo_extra_tex(nodes=None,
                     state=1,
                     smartConvert=True,
                     vrayNormalObj=None,
                     vrayNormalWorld=None,
                     vrayGNormalWorld=None,
                     vrayPointWorldReferenceX=None,
                     vrayNormalWorldReferenceX=None,
                     vrayRayDepth=None,
                     vrayPathLength=None):
    """ Add/change the Additional outputs (vray_samplerinfo_extra_tex) attribute to input samplerInfo nodes.

    Note that in general setting the attribute values for a samplerInfo node isn't really doing anything useful.
    I've implemented the v-ray attribute parameters anyway, but they should be pretty much useless in this case.

    Valid node types: (samplerInfo)

    :param nodes: nodes to apply the attribute to. If nodes is None it will get
                  the nodes related to the current selection.

    :param smartConvert: CURRENTLY NO IMPLEMENTATION
    :type  smartConvert: bool

    :param state: If state is True it will add the attribute, else it will remove it.
    :type  state: 1 or 0
    """
    # TODO: Implement attribute parameters description

    state = _convert_state(state)
    validTypes = ("samplerInfo")

    if nodes is None:
        nodes = mc.ls(sl=1, long=True)

    if smartConvert:
        # TODO: Implement smart convert
        pass

    nodes = mc.ls(nodes, type=validTypes, long=True)

    if not nodes:
        raise RuntimeError("No samplerInfo found to apply the vray_samplerinfo_extra_tex attribute changes to.")

    for node in nodes:
        mc.vray("addAttributesFromGroup", node, "vray_samplerinfo_extra_tex", state)

        # Manage the attributes (if not None change it to the set value)
        if state:
            if vrayNormalObj is not None:
                mc.setAttr("{0}.vrayNormalObj".format(node), vrayNormalObj)
            if vrayNormalWorld is not None:
                mc.setAttr("{0}.vrayNormalWorld".format(node), vrayNormalWorld)
            if vrayGNormalWorld is not None:
                mc.setAttr("{0}.vrayGNormalWorld".format(node), vrayGNormalWorld)
            if vrayPointWorldReferenceX is not None:
                mc.setAttr("{0}.vrayPointWorldReferenceX".format(node), vrayPointWorldReferenceX)
            if vrayNormalWorldReferenceX is not None:
                mc.setAttr("{0}.vrayNormalWorldReferenceX".format(node), vrayNormalWorldReferenceX)
            if vrayRayDepth is not None:
                mc.setAttr("{0}.vrayRayDepth".format(node), vrayRayDepth)
            if vrayPathLength is not None:
                mc.setAttr("{0}.vrayPathLength".format(node), vrayPathLength)


###################
## transform
###################

def vray_skip_export(transforms=None,
                     state=1,
                     smartConvert=False,
                     vraySkipExport=None):
    """ Add/change the Skip Rendering (vray_skip_export) attribute to input transforms.

    Valid node types: (transform)

    :param transforms: transforms to apply the attribute to. If transforms is None it will get
                       the transforms related to the current selection.

    :param smartConvert: If True it will convert input shapes to parent transforms.
                         Since this is likely unwanted behaviour smartConvert is False by default for this function.
    :type  smartConvert: bool

    :param state: If state is True it will add the attribute, else it will remove it.
    :type  state: 1 or 0
    """
    state = _convert_state(state)
    validTypes = ("transform")

    if transforms is None:
        transforms = mc.ls(sl=1, long=True)

    if smartConvert:
        # Include parent transform of a shape node
        shapes = mc.ls(transforms, s=True, long=True)
        if shapes:
            shapeParents = mc.listRelatives(shapes, fullPath=True, parent=True)
            if shapeParents:
                transforms.extend(shapeParents)

    transforms = mc.ls(transforms, type=validTypes, long=True)

    if not transforms:
        raise RuntimeError("No transforms found to apply the vray_skip_export attribute group changes to.")

    for node in transforms:
        mc.vray("addAttributesFromGroup", node, "vray_skip_export", state)

        # Manage the attributes (if not None change it to the set value)
        if state:
            if vraySkipExport is not None:
                mc.setAttr("{0}.vraySkipExport".format(node), vraySkipExport)