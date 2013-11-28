import maya.cmds as mc
import os


def vrayFrameBufferFix():
    """ Fixes missing V-ray FrameBuffer

        It happens from time to time that the V-ray frame buffer just disappears and won't pop up.
        In that scenario it's probably the good old V-ray for Maya framebuffer bug striking again.
        When that happens this script will come to the rescue.

        It will save your file as a temporary .ma file, removes the buggy ASCII code of the
        framebuffer, reopens the temp file and internally renames it to your original file.

        Note: It doesn't automatically save it over your original file even though it might
              look like it because it shows the original filename at the top.
              Save your scene when it worked. :)
    """
    current_dir = os.path.dirname(mc.file(query=True, sceneName=True))
    current_name, current_ext = os.path.splitext(mc.file(query=True, sceneName=True))
    fix_file_suffix = "_temp_vrayfb_fix.ma"
    confirm = mc.confirmDialog(title='O RLY?', message='Did you backup your file already?', button=['Yes', 'No'],
                               defaultButton='Yes', cancelButton='No', dismissString='No')

    if confirm == "Yes":
        # Save file
        path_current_file = mc.file(force=True,save=1,options="v=0")

        # Save Ma file to fix it (if it's not yet a fix .ma file
        if path_current_file.endswith(fix_file_suffix):
            raise RuntimeError("You're already working in the _temp_vrayfb_fix file?")

        mc.file(rename="%s%s" % (current_name,fix_file_suffix))
        path_fix_save = mc.file(force=True, save=1, options="v=0", type="mayaAscii")

        # Change .ma file
        fin = open(path_fix_save, "r")
        mafile = fin.readlines()
        fin.close()
        fixed_mafile = []

        remove = 0
        foundEOL = 0
        for line in mafile:
            if 'setAttr ".vfbSA"' in line:
                remove = 1

            if remove == 1:
                if ';' in line:
                    foundEOL = 1
                if 'setAttr' in line and not 'setAttr ".vfbSA"' in line:
                    remove = 0

            if remove == 0:
                fixed_mafile.append(line)

            if foundEOL == 1:
                remove = 0

        fout = open(path_fix_save, "w")
        fout.writelines(fixed_mafile)
        fout.close()
        print path_fix_save

        # Open fixed file
        mc.file(path_fix_save, f=True, options="v=0", typ="mayaAscii", o=1)

        # Rename scene to original (without saving)
        mc.file(rename=path_current_file)

        os.remove(path_fix_save)
        print "Fixed!"


if __name__ == "__main__":
    vrayFrameBufferFix()