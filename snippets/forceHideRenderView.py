import maya.cmds as mc
import maya.utils as mutils


def getRenderSize():
    return mc.getAttr("defaultResolution.width"), mc.getAttr("defaultResolution.height")


def forceHideRenderView(state=None, renderViewWindow="renderViewWindow", renderView="renderView",
                        min_size=(999999, 999999), label="CLICK HERE TO KILL HIDE RENDER VIEW"):
    """ Hides the renderView in a dock control.

    This (force) hides the renderView in a dockControl in the right area of you Main Window.
    By doing that the renderView doesn't pop-up when you use the V-ray Framebuffer, sweet!

    HOW TO DISABLE:
    To disable just run this again with state=None (toggles), or force it by state=False.
    You could also right mouse click on the draggable part of that dockControl area,
    (which is normally the attribute editor / channel box area) and then click on the label:
        "CLICK HERE TO KILL HIDE RENDER VIEW"

    Note:
        This hack might spit out the following errors:
            // Error: line 1: No window found.  //
        Yet as far as I know it's never doing any harm.

        A workaround for that error is depicted here: http://polygonspixelsandpaint.tumblr.com/post/68136553566

        -- warning --
        The code snippet on that website seems to be problematic under Windows, as it resizes the main
        window even with Auto Resize set to False. (tested on Maya 2014 ext 1, Windows 7 64 bit) This function has
        a work-around for that. Though the work-around should work similarly. :)


    :param state: The state to enable/disable the forceHideRenderView functionality.

                  A True value will enable the hiding functionality
                  A False value will disable the hiding functionality.
                  A None value will toggle the hiding functionality.

    :type  state: bool or None

    :param renderViewWindow: The name of the renderView window object to act upon.
                             The maya default renderView window object is called: "renderViewWindow".
                             This is the default value; normally this requires no changes.
    :type  renderViewWindow: str


    :param renderView: The name of the renderView object to act upon.
                       The maya default renderView object is called: "renderView".
                       This is the default value; normally this requires no changes.
    :type  renderViewWindow: str
    
    :param min_size: The minimum size enforced for the controls. Setting this very high avoids the main window being
                     resized when rendering high resolution images. (A workaround for stupid Autodesk UI functionality.)
    :type  min_size: (int, int)
    
    :param label: The label that will show in the dock control right menu as a label.
    :type  label: str

    :rtype: bool
    :return: The resulting state

    """
    UI_OBJ = "rendEditorDC"

    if state is None:
        state = not mc.dockControl(UI_OBJ, q=1, exists=True)

    if mc.dockControl(UI_OBJ, q=1, exists=True):
       mc.deleteUI(UI_OBJ)

    if state:
        # Show the render view so we can parent it to our dock control
        if not mc.window(renderViewWindow, q=1, exists=True):
            mc.RenderViewWindow()

        # Uses either the minimum size or the size of the render settings + 250 (just to be sure)
        size = [max(x, y+250) for x, y in zip(min_size, getRenderSize())]

        def __deleteRenderViewHideDockControl(*args):
            # If it's made visible we hide it and delete it.
            # We use executeDeferred because otherwise we'll get a fatal error. :)
            if mc.dockControl(UI_OBJ, q=1, visible=True):
                mc.dockControl(UI_OBJ, e=1, visible=False)
                mutils.executeDeferred(lambda: mc.deleteUI(UI_OBJ))


        if not mc.dockControl(UI_OBJ, q=1, exists=True):
            lyt = mc.scrollLayout()
            dock = mc.dockControl(UI_OBJ, area="right", content=renderViewWindow,
                           visible=False, epo=True, manage=False, vcc=__deleteRenderViewHideDockControl,
                           label=label)

        # This is the same control the renderWindowPanel.mel script checks for the size .
        # We just need to make it big enough so it doesn't call a resize of the top UI element.
        renderWindowControl = mc.scriptedPanel(renderView, q=True, control=True)
        mc.control(renderWindowControl, e=1, w=size[0], h=size[1], visible=False)

        print "ENABLED HIDE RENDER VIEW"
    else:
        print "DISABLED HIDE RENDER VIEW"


if __name__ == "__main__":
    forceHideRenderView()