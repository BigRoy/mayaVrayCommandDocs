import maya.cmds as mc


def autoRenderViewMinimize(state=None, renderView="renderViewWindow"):
    """ Overrides the renderView's restore command so that it directly minimizes again.

    This is especially useful when rendering with V-ray Framebuffer enabled,
    because on rendering it 'pops up' the default maya render view (which is extremely annoying).
    Enabling this autoRenderViewMinimize will directly minimize the render view window when the render starts.

    Default value for state is None. This means the value will depend on user input during the execution of the script.
    If the user holds any of the following keys the autoRenderViewMinimize will be disabled: Shift, Alt, Control.
    This makes it an easy to use shelf button script. :)

    Note: You should leave the render view window open, but minimized. Because Maya's render view code has been hard
          coded this to re-open and resize this is really the only viable way to hide it without breaking stuff.
          Until chaosgroup overrides the functionality - eg. hiding the render view when their renderer (or
          framebufffer) kicks in - this is a neat solution.

    Note: Another way might be to dock the renderView window to your interface and hide it. This way it will not pop up.
          But because Maya (auto-)resizes the top window if the view is too small when pressing the render button in the
          UI it will resize Maya's main window (because that is then the top window.)
          A reference to this method can be found here: http://polygonspixelsandpaint.tumblr.com/post/68136553566

    :param state: The state to set the autoRenderViewMinimize to.

                  A True value will open and minimize the render view and override the minimize/restore state functionality.
                  A False value will make sure the functionality is removed.

                  If None it will default to True,
                  unless during the run of the script the user pressed (hold it to be sure) any of the following keys:
                      - Shift
                      - Alt
                      - Control.

    :type  state: bool or None

    :param renderView: The name of the renderView window object to act upon.

                       The maya default renderView window object is called: "renderViewWindow". This is the default value.
    :type  renderView: str

    :rtype: bool
    :return: The resulting state
    """

    if state is None:
        # If state is None we allow the user to set the state by whether they have pressed a modifier button during execution.
        # If any modifier key is pressed when the script is running then the RenderView minimize override is disabled. (force removed)
        # So to disable the functionality run this script while holding: Shift, Alt and/or Control. Else it will enable
        # the functionality.
        state = not (mc.getModifiers())
    print "Setting the override render view minimize to: {0}".format(state)

    if state:
        if not mc.window(renderView, q=1, exists=True):
            mc.RenderViewWindow() # RuntimeCommand (to force create the renderView)

        renderViewMinimize = lambda: mc.window(renderView, e=True, i=True)
        renderViewMinimize() # Minimize the renderView
        mc.window(renderView, e=True, restoreCommand=renderViewMinimize) # Override the renderView restore command
    else:
        if mc.window(renderView, q=1, exists=True):
           mc.deleteUI(renderView)
           mc.RenderViewWindow()

    return state


if __name__ == "__main__":
    autoRenderViewMinimize()