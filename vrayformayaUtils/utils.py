import maya.cmds as mc


def getMaterials(nodes=None):
    """ Returns the materials related to nodes

    :param nodes: The nodes to get the related materials from.
                  If nodes is None the current selection will be used.

    :rtype: list
    """
    # Get selected nodes if None provided
    if nodes is None:
        nodes = mc.ls(sl=1)

    # Get materials from list
    materials = mc.ls(nodes, mat=1, long=True)

    # Get materials related to nodes (material from object)
    # And add those materials to the material list we already have
    if nodes:
        nodes_history = mc.listHistory(nodes,f=1)
        if nodes_history:
            nodes_connections = mc.listConnections(nodes_history)
            if nodes_connections:
                connected_materials = mc.ls(nodes_connections, mat=True, long=True)
                if connected_materials:
                    # Use a set so we don't have any duplicates
                    materials = set(materials)
                    materials.update(connected_materials)
                    materials = list(materials)

    return materials


def getShapes(nodes=None,
              filterType=None,
              allDescendents=True,
              fullPath=True):
    """ Returns the shapes related to nodes

    :param nodes: The nodes to get the related shapes from.
                  If nodes is None the current selection will be used.
    :type  nodes: None, str, unicode or tuple

    :param filterType: The filterType can be used to filter the result to only a certain type
                       of nodes.
    :type  filterType: str or tuple

    :param allDescendents: If True it will get all children shapes at any depth.
                           Otherwise it will only get direct children shapes.
    :type  allDescendents: bool

    :param fullPath: If True it will return the result in long names / full paths.
                     Otherwise it should return the shortest unique name.
    :type  fullPath: bool

    :rtype: list
    """

    # Acquire from selection
    if nodes is None:
        if allDescendents:
            shapes = mc.ls(sl=1, s=1, dag=1, lf=1, o=1, long=True, allPaths=True)
        else:
            sel = mc.ls(sl=1)
            shapes = mc.ls(sl=1, s=1, long=True)

            # Note that we can't directly get allDescendents and filter to shapes through listRelatives because it will
            # still stop at the first level because it will not pass through other nodes than shapes. :/
            children = mc.listRelatives(sel,
                                       children=True,
                                       fullPath=True,
                                       allDescendents=allDescendents)
            if children:
                childrenShapes = mc.ls(children, s=True, long=True)
                if childrenShapes:
                    shapes.extend(childrenShapes)

    # Acquire from input nodes
    else:

        # If an emtpy list (or anything that passes through as False) was passed in we return the empty list
        if not nodes:
            return []

        shapes = mc.ls(nodes, s=1, long=True)

        children = mc.listRelatives(nodes,
                                       children=True,
                                       fullPath=True,
                                       allDescendents=allDescendents)
        if children:
            childrenShapes = mc.ls(children, s=True, long=True)
            if childrenShapes:
                shapes.extend(childrenShapes)

    # Return nothing if we have nothing
    if not shapes:
        return []

    # Filter to a certain type (and change to non-long/non-fullPath version if the user requests that).
    elif filterType is not None:
        # Only apply to mesh or nurbsSurface (other shapes can't contain the vray_subdivision attribute)
        shapes = mc.ls(shapes, type=filterType, long=fullPath)

    # Change to non-long/non-fullPath version if the user requests that.
    elif not fullPath:
        shapes = mc.ls(shapes, long=fullPath)

    return shapes