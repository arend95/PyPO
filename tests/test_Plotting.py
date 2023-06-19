import unittest
import warnings
import sys

from nose2.tools import params

try:
    from . import TestTemplates
except ImportError: 
    import TestTemplates

from numpy import ndarray 
from matplotlib.figure import Figure
from matplotlib.pyplot import Axes, close

from mpl_toolkits.mplot3d.axes3d import Axes3D
from PyPO.System import System

##
# @file
# This file contains tests for the plotting functionalities. It tests whether the plotting functions in the System behave as expected.

class Test_Plotting(unittest.TestCase):
    def setUp(self):
        self.s = TestTemplates.getSystemWithReflectors()
        self.s.setOverride(False)
        self.projects = ["xy", "yx", "xz", "zx", "yz", "zy"]
    
    def test_plotBeamCut(self):
        fig, ax = self.s.plotBeamCut(TestTemplates.GPOfield['name'], 'Ex', center=False, align=False, ret=True)

        self.assertEqual(type(fig), Figure)
        self.assertEqual(type(ax), Axes)

        close('all')

    @params("xy", "yx", "xz", "zx", "yz", "zy")
    def test_plotBeam2D(self, project):
        out_ar = []
        out_ax = []
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            aperDict_plot = self.s.copyObj(TestTemplates.aperDict)
            aperDict_plot["plot"] = True

            out_ax.append(self.s.plotBeam2D(TestTemplates.GPOfield['name'], 'Ex', ret=True, amp_only=True, project=project, aperDict=aperDict_plot))
            out_ax.append(self.s.plotBeam2D(TestTemplates.GPOfield['name'], 'Ex', ret=True, amp_only=True, mode="linear", project=project))
            out_ar.append(self.s.plotBeam2D(TestTemplates.GPOfield['name'], 'Ex', ret=True, project=project, aperDict=TestTemplates.aperDict, contour=TestTemplates.GPOfield['name'], contour_comp="Ex", levels=[0.5, 1]))
            out_ar.append(self.s.plotBeam2D(TestTemplates.GPOfield['name'], 'Ex', ret=True, mode="linear", project=project, contour=TestTemplates.GPOfield['name'], contour_comp="Ex", levels=[0.5, 1]))

        for entry_ax, entry_ar in zip(out_ax, out_ar):
            self.assertEqual(type(entry_ax[0]), Figure)
            self.assertEqual(type(entry_ar[0]), Figure)
            
            self.assertEqual(type(entry_ax[1]), Axes)
            self.assertEqual(type(entry_ar[1]), ndarray)

        close('all')

    @params(*TestTemplates.getAllSurfList())
    def test_plotBeam3D(self, element):
        sys.tracebacklimit = 0
        try:
            fig, ax = self.s.plot3D(element['name'], ret=True, foc1=True, foc2=True, norm=True)

        except KeyError:
            fig, ax = self.s.plot3D(element['name'], ret=True, norm=True)
            
        self.assertEqual(type(fig), Figure)
        self.assertEqual(type(ax), Axes3D)

        close('all')

            
    def test_plotSystem(self):
        fig, ax = self.s.plotSystem(ret=True)

        self.assertEqual(type(fig), Figure)
        self.assertEqual(type(ax), Axes3D)

        emptySys = System(verbose=False)
        figE, axE = emptySys.plotSystem(ret=True)

        self.assertEqual(type(figE), Figure)
        self.assertEqual(type(axE), Axes3D)
        

        close('all')
        
        
    def test_plotGroup(self):
        self.s.groupElements('testGroup', 
                          TestTemplates.paraboloid_man_xy['name'],
                          TestTemplates.hyperboloid_man_uv['name'],
                          TestTemplates.ellipsoid_z_foc_xy['name'],
                          TestTemplates.ellipsoid_x_man_uv['name'],
                          TestTemplates.plane_xy['name'],
                          TestTemplates.plane_AoE['name'],
                          )
        
        fig, ax = self.s.plotGroup('testGroup', ret=True)

        self.assertEqual(type(fig), Figure)
        self.assertEqual(type(ax), Axes3D)

        close('all')
        
        
    @params("xy", "yx", "xz", "zx", "yz", "zy")
    def test_plotRTframe(self, project):
        for frameName in [TestTemplates.TubeRTframe['name'], TestTemplates.GaussRTframe['name']]:
            fig = self.s.plotRTframe(frameName, ret=True, project=project)

            self.assertEqual(type(fig), Figure)

            close('all')        

if __name__ == '__main__':
    import nose2
    nose2.main()
