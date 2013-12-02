import unittest
import maya.cmds as mc
import vrayformayaUtils as vfm

class TestMeshAttributes(unittest.TestCase):
    """
        This is a generic TestCase for most v-ray mesh attributes.
        Note that it doesn't test every single case of changes, but it should capture overall changes of the code.
    """
    def setUp(self):
        self.mesh = mc.polyCube()[0]

    def test_subdivision(self):
        transform = self.mesh
        shapes = mc.listRelatives(transform, children=True, shapes=True)
        vfm.attributes.vray_subdivision(self.mesh, state=True, smartConvert=True)
        for shape in shapes:
            self.assertTrue(mc.objExists("{0}.vraySubdivEnable".format(shape)))

        vfm.attributes.vray_subdivision(self.mesh, state=True, smartConvert=True, vraySubdivEnable=False)
        for shape in shapes:
            self.assertEqual(mc.getAttr("{0}.vraySubdivEnable".format(shape)), False)

        vfm.attributes.vray_subdivision(self.mesh, state=True, smartConvert=True, vraySubdivEnable=True)
        for shape in shapes:
            self.assertEqual(mc.getAttr("{0}.vraySubdivEnable".format(shape)), True)

        vfm.attributes.vray_subdivision(self.mesh, state=False)
        for shape in shapes:
            self.assertFalse(mc.objExists("{0}.vraySubdivEnable".format(shape)))

        # Apply to transform without smart convert (should not work)
        vfm.attributes.vray_subdivision(self.mesh, state=True, smartConvert=False)
        for shape in shapes:
            self.assertFalse(mc.objExists("{0}.vraySubdivEnable".format(shape)))

        for shape in shapes:
            vfm.attributes.vray_subdivision(shape, state=True, smartConvert=False)
            self.assertTrue(mc.objExists("{0}.vraySubdivEnable".format(shape)))
            vfm.attributes.vray_subdivision(shape, state=False, smartConvert=False)
            self.assertFalse(mc.objExists("{0}.vraySubdivEnable".format(shape)))

    def test_vray_subquality(self):
        transform = self.mesh
        shapes = mc.listRelatives(transform, children=True, shapes=True)

        # should run without errors:
        vfm.attributes.vray_subquality(transform, vrayEdgeLength=1, vrayMaxSubdivs=1, vrayOverrideGlobalSubQual=1, vrayViewDep=1)
        vfm.attributes.vray_subquality(transform, vrayEdgeLength=0, vrayMaxSubdivs=0, vrayOverrideGlobalSubQual=0, vrayViewDep=0)

        for shape in shapes:
            self.assertTrue(mc.objExists("{0}.vrayEdgeLength".format(shape)))
            self.assertTrue(mc.objExists("{0}.vrayMaxSubdivs".format(shape)))
            self.assertTrue(mc.objExists("{0}.vrayOverrideGlobalSubQual".format(shape)))
            self.assertTrue(mc.objExists("{0}.vrayViewDep".format(shape)))

        vfm.attributes.vray_subquality(shapes, smartConvert=False, state=False)

        for shape in shapes:
            self.assertFalse(mc.objExists("{0}.vrayEdgeLength".format(shape)))
            self.assertFalse(mc.objExists("{0}.vrayMaxSubdivs".format(shape)))
            self.assertFalse(mc.objExists("{0}.vrayOverrideGlobalSubQual".format(shape)))
            self.assertFalse(mc.objExists("{0}.vrayViewDep".format(shape)))

    def test_vray_user_attributes(self):
        transform = self.mesh
        shapes = mc.listRelatives(transform, children=True, shapes=True)

        value = "Testing this attribute"
        vfm.attributes.vray_user_attributes(transform, vrayUserAttributes=value)

        for shape in shapes:
            self.assertEqual(mc.getAttr("{0}.vrayUserAttributes".format(shape)), value)

        value2 = "Aaaaaaap"
        for shape in shapes:
            self.assertNotEqual(mc.getAttr("{0}.vrayUserAttributes".format(shape)), value2)

        vfm.attributes.vray_user_attributes(transform, vrayUserAttributes=value2)
        for shape in shapes:
            self.assertEqual(mc.getAttr("{0}.vrayUserAttributes".format(shape)), value2)

        vfm.attributes.vray_user_attributes(shapes, state=False)
        for shape in shapes:
            self.assertFalse(mc.objExists("{0}.vrayUserAttributes".format(shape)))

    def test_vray_displacement(self):
        transform = self.mesh
        shapes = mc.listRelatives(transform, children=True, shapes=True)

        vfm.attributes.vray_displacement(transform, vrayDisplacementAmount=10)
        vfm.attributes.vray_displacement(transform, vrayDisplacementShift=5)
        vfm.attributes.vray_displacement(transform, vrayDisplacementType=2, vrayDisplacementUseBounds=True,
                                                    vrayEnableWaterLevel=True, vrayWaterLevel=2.0)

        for shape in shapes:
            self.assertTrue(mc.objExists("{0}.vrayDisplacementNone".format(shape)))

        vfm.attributes.vray_displacement(shapes, state=False)
        for shape in shapes:
            self.assertFalse(mc.objExists("{0}.vrayDisplacementNone".format(shape)))

        vfm.attributes.vray_displacement(shapes, state=0)
        for shape in shapes:
            self.assertFalse(mc.objExists("{0}.vrayDisplacementNone".format(shape)))


    def tearDown(self):
        mc.delete(self.mesh)


#import unittest
#import vrayformayaUtils_tests.attributes_tests as attrTest
#reload(attrTest)
#suite = unittest.TestLoader().loadTestsFromTestCase(attrTest.TestMeshAttributes)
#unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
    unittest.main()