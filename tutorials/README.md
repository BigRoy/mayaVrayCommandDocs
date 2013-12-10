mayaVrayCommandDocs Tutorials
=============================

These tutorials are meant to help anyone getting up to speed to writing some scripts for v-ray for maya.

The easiest way is to start at the beginning and use the [wiki page](https://github.com/BigRoy/mayaVrayCommandDocs/wiki)
as complementary information when working through some functions. For example when you start using
`mc.vray("addAttributesFromGroup", ..)` also have a look at the ["vray addAttributesFromGroup documentation"](https://github.com/BigRoy/mayaVrayCommandDocs/wiki/vray-addAttributesFromGroup).


01. Getting Started
-------------------

This will very quickly introduce you on how to import maya commands into Python and call the mc.vray() command.
Then we hop into adding the `vray_subdivision` attribute to mesh nodes.


02. Deeper into V-ray Attributes
--------------------------------

This chapter will go a tiny bit deeper (but still very basic level) into adding v-ray attributes to only the nodes you
want it to. We will get children shapes from transform and apply the `vray_subdivision` and `vray_nurbscurve_renderable`
attributes. At the end you should have a good grasp on adding any v-ray attribute you need to exactly the object you
want in your maya scene.


Have some ideas?
----------------

We're doing these tutorials on the side so it'll likely evolve a bit slower then someone might want.
If you're looking for something specific or have cool ideas to be added in here give me a heads up at roy@colorbleed.nl.
Then I'll see what I can do. Or you can fork and branching the repository and start building on it. :)