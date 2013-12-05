mayaVrayCommandDocs
===================

Documentation & Code Snippets for Maya's v-ray commands

###See the [Maya V-ray Commands Wiki](https://github.com/BigRoy/mayaVrayCommandDocs/wiki) for documentation.

We're trying to build up documentation for V-ray for Maya's code base. 

First focusing on all the built-in commands that come with a V-ray for Maya installation, like the extremely bad documented `vray` command.

This documentation can be found in this repository's Wiki (see link above).

If you're working extensively with Maya and are scripting a lot for it have a look at the framework/library that we
developed for working with V-ray for Maya:

- [vrayformayaUtils repository on GitHub](https://github.com/BigRoy/vrayformayaUtils/)

The `vrayformayaUtils` could first be found directly in this repository. But since it's growing into a bigger code
library/framework we've decided to seperate it into its own repository.


###Snippets

On the other hand there are the `snippets`. You could consider that the quick stop for finding your script to deal with
a certain repetitive tasks. This is where you should go if you want to get started quickly.

I'll add some more example functions in the repository over time.
With this we hope to share some of the knowledge that we've gained from using V-ray over time and the increasing need we had to improve the efficiency of our workflow.

Getting to a higher level of automatisation is closely related to understanding how to script your way through the basics.
We are trying to help out on that part by sharing small code snippets focused on getting tasks done.
By making this open-source we also hope to learn a lot from others and their ideas on the V-ray for Maya workflow.

*In the snippets section you can find some very useful code to help with fixing the v-ray for maya framebuffer bug.*


###Snippets (Quick Start)

If you don't have a Technical Director in the studio or you're just looking for some quick and dirty scripts to help
you out in your V-ray for Maya workflow this is where you start. Welcome!

Most likely the code snippets are the most interesting thing here if you're looking to get started quickly.
You can find them in the repository in the snippets directory. These are small scripts that don't require
any of the dependencies other than a standard Maya installation with V-ray for Maya.


####[Use the snippets](snippets)

In short, you could copy the raw code of one of the snippets and paste it into the Maya script editor.
Note that all scripts here are written in **Python**, so make sure to run it in a Python tab.


####Get the scripts into your shelve.

You can middle-mouse drag the script from your script editor onto your Maya shelf to create an icon for it. You can
easily label, annotate and customize it by clicking on the small triangle on the shelf at the left of the screen, click
_Shelf Editor..._


###Tutorials

Along the way I'll try to add more and more very simple introductory tutorials to get anyone who wants to delve into
Python scripting for V-ray for Maya.

*The tutorials can be found in the ``tutorials`` directory in the repository.*


###Help the Vray for Maya community

If you have any good documentation, tips or code snippets for Vray for Maya feel free to fork the repository and start adding away.

Note that this is a personal/community project so we can't deliver 24-hour support, but whenever you have some questions feel free to contact me at roy@colorbleed.nl

And if it's really V-ray related (and not to the code provided here) make sure to contact Chaosgroup support.

