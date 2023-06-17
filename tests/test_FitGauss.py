import sys
import os
import shutil
import unittest
import numpy as np

from PyPO.System import System
from PyPO.FitGauss import fitGaussAbs, generateGauss

try:
    from . import TestTemplates
except ImportError:
    import TestTemplates
##
# @file
# File containing tests for Gaussian fitting in PyPO.
class Test_FitGauss(unittest.TestCase):
    def setUp(self):
        self.s = TestTemplates.getSystemWithReflectors()
        self.s.setOverride(False) 
    
    def test_fitGauss(self):

        for mode in ["linear", "dB", "log"]:
            popt = self.s.fitGaussAbs(TestTemplates.GPOfield["name"], "Ex", thres=-100, mode=mode, full_output=True, ratio=None)
            self.assertTrue(len(popt) == 6)
            self.assertTrue(f"fitGauss_{TestTemplates.GPOfield['name']}" in self.s.scalarfields)

            popt = self.s.fitGaussAbs(TestTemplates.GPOfield["name"], "Ex", thres=-100, mode=mode, full_output=True, ratio=1)
            self.assertTrue(len(popt) == 6)
            self.assertTrue(f"fitGauss_{TestTemplates.GPOfield['name']}" in self.s.scalarfields)
           
    def test_calcHPBW(self):
        E, H = self.s.calcHPBW(TestTemplates.GPOfield["name"], "Ex")
        self.assertTrue(isinstance(E, float))
        self.assertTrue(isinstance(H, float))

if __name__ == "__main__":
    unittest.main()

