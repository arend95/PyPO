# Standard Python imports
import numbers
import numpy as np
import matplotlib.pyplot as pt
import matplotlib.cm as cm
import time
import psutil
import os
import sys
import json

from scipy.interpolate import griddata

# POPPy-specific modules
from src.POPPy.BindRefl import *
from src.POPPy.BindGPU import *
from src.POPPy.BindCPU import *
from src.POPPy.BindBeam import *
from src.POPPy.Copy import copyGrid
from src.POPPy.MatTransform import *
from src.POPPy.POPPyTypes import *

import src.POPPy.Plotter as plt
import src.POPPy.Efficiencies as effs

class System(object):
    customBeamPath = './custom/beam/'
    customReflPath = './custom/reflector/'

    savePathElem = './save/elements/'

    def __init__(self):
        self.num_ref = 0
        self.num_cam = 0
        self.system = {}

        self.savePathElem = "./save/elements/"

        saveExist = os.path.isdir(self.savePathElem)

        if not saveExist:
            os.makedirs(self.savePathElem)

        self.savePath = './images/'

        existSave = os.path.isdir(self.savePath)

        if not existSave:
            os.makedirs(self.savePath)

    def __str__(self):
        pass

    def setCustomBeamPath(self, path, append=False):
        if append:
            self.customBeamPath += path
        else:
            self.customBeamPath = path

    def setCustomReflPath(self, path, append=False):
        if append:
            self.customReflPath += path
        else:
            self.customReflPath = path

    #### ADD REFLECTOR METHODS
    # Parabola takes as input the reflectordict from now on.
    # Should build correctness test!
    #def addParabola(self, coef, lims_x, lims_y, gridsize, cRot=np.zeros(3), pmode='man', gmode='xy', name="Parabola", axis='a', units='mm', trunc=False, flip=False):
    def addParabola(self, reflDict):
        """
        Function for adding paraboloid reflector to system. If gmode='uv', lims_x should contain the smallest and largest radius and lims_y
        should contain rotation.
        """
        if not "name" in reflDict:
            reflDict["name"] = "Parabola"

        if reflDict["name"] == "Parabola":
            reflDict["name"] = reflDict["name"] + "_{}".format(self.num_ref)

        reflDict["type"] = 0
        reflDict["transf"] = np.eye(4)

        self.system[reflDict["name"]] = copyGrid(reflDict)

        if reflDict["pmode"] == "focus":
            self.system[reflDict["name"]]["coeffs"] = np.zeros(3)

            ve = reflDict["vertex"] # Vertex point position
            f1 = reflDict["focus_1"] # Focal point position

            diff = f1 - ve

            df = np.sqrt(np.dot(diff, diff))
            a = 2 * np.sqrt(df)
            b = a

            orientation = diff / np.sqrt(np.dot(diff, diff))
            offTrans = ve

            # Find rotation in frame of vertex
            rx = np.arccos(1 - np.dot(np.array([1,0,0]), orientation))
            ry = np.arccos(1 - np.dot(np.array([0,1,0]), orientation))
            rz = 0

            offRot = np.array([rx, ry, rz])
            cRot = offTrans

            self.system[reflDict["name"]]["transf"] = MatRotate(offRot, reflDict["transf"], cRot)
            self.system[reflDict["name"]]["transf"] = MatTranslate(offTrans, reflDict["transf"])

            self.system[reflDict["name"]]["coeffs"][0] = a
            self.system[reflDict["name"]]["coeffs"][1] = b
            self.system[reflDict["name"]]["coeffs"][2] = -1

        if reflDict["gmode"] == "xy":
            self.system[reflDict["name"]]["gmode"] = 0

        elif reflDict["gmode"] == "uv":
            # Convert v in degrees to radians
            self.system[reflDict["name"]]["lims_v"] = [self.system[reflDict["name"]]["lims_v"][0],
                                                        self.system[reflDict["name"]]["lims_v"][1]]

            self.system[reflDict["name"]]["gmode"] = 1

        self.num_ref += 1

    def addHyperbola(self, reflDict):

        if not "name" in reflDict:
            reflDict["name"] = "Hyperbola"
        if reflDict["name"] == "Hyperbola":
            reflDict["name"] = reflDict["name"] + "_{}".format(self.num_ref)

        reflDict["type"] = 1
        reflDict["transf"] = np.eye(4)

        self.system[reflDict["name"]] = copyGrid(reflDict)

        if reflDict["pmode"] == "focus":
            self.system[reflDict["name"]]["coeffs"] = np.zeros(3)
            # Calculate a, b, c of hyperbola
            f1 = reflDict["focus_1"] # Focal point 1 position
            f2 = reflDict["focus_2"] # Focal point 2 position
            ecc = reflDict["ecc"] # Eccentricity of hyperbola

            diff = f1 - f2
            c = np.sqrt(np.dot(diff, diff)) / 2
            a = c / ecc
            b = np.sqrt(c**2 - a**2)

            # Convert 2D hyperbola a,b,c to 3D hyperboloid a,b,c
            a3 = b
            b3 = b
            c3 = a

            # Find direction between focii
            orientation = diff / np.sqrt(np.dot(diff, diff))

            # Find offset from center. Use offset as rotation origin for simplicity
            center = (f1 + f2) / 2
            offTrans = center

            # Find rotation in frame of center
            rx = np.arccos(1 - np.dot(np.array([1,0,0]), orientation))
            ry = np.arccos(1 - np.dot(np.array([0,1,0]), orientation))
            rz = 0

            offRot = np.array([rx, ry, rz])
            cRot = offTrans

            self.system[reflDict["name"]]["transf"] = MatRotate(offRot, reflDict["transf"], cRot)
            self.system[reflDict["name"]]["transf"] = MatTranslate(offTrans, reflDict["transf"])

            self.system[reflDict["name"]]["coeffs"][0] = a3
            self.system[reflDict["name"]]["coeffs"][1] = b3
            self.system[reflDict["name"]]["coeffs"][2] = c3

        if reflDict["gmode"] == "xy":
            self.system[reflDict["name"]]["gmode"] = 0

        elif reflDict["gmode"] == "uv":
            self.system[reflDict["name"]]["lims_v"] = [self.system[reflDict["name"]]["lims_v"][0],
                                                        self.system[reflDict["name"]]["lims_v"][1]]

            self.system[reflDict["name"]]["gmode"] = 1

        self.num_ref += 1

    def addEllipse(self, reflDict):
        if not "name" in reflDict:
            reflDict["name"] = "Ellipse"

        if reflDict["name"] == "Ellipse":
            reflDict["name"] = reflDict["name"] + "_{}".format(self.num_ref)

        reflDict["type"] = 2
        reflDict["transf"] = np.eye(4)

        self.system[reflDict["name"]] = copyGrid(reflDict)

        if reflDict["pmode"] == "focus":
            pass

        if reflDict["gmode"] == "xy":
            self.system[reflDict["name"]]["gmode"] = 0

        elif reflDict["gmode"] == "uv":
            self.system[reflDict["name"]]["lims_v"] = [self.system[reflDict["name"]]["lims_v"][0],
                                                        self.system[reflDict["name"]]["lims_v"][1]]

            self.system[reflDict["name"]]["gmode"] = 1

        self.num_ref += 1

    def addPlane(self, reflDict):
        if not "name" in reflDict:
            reflDict["name"] = "Plane"

        if reflDict["name"] == "Plane":
            reflDict["name"] = reflDict["name"] + "_{}".format(self.num_ref)

        reflDict["type"] = 3
        reflDict["transf"] = np.eye(4)

        self.system[reflDict["name"]] = copyGrid(reflDict)
        self.system[reflDict["name"]]["coeffs"] = np.zeros(3)

        self.system[reflDict["name"]]["coeffs"][0] = -1
        self.system[reflDict["name"]]["coeffs"][1] = -1
        self.system[reflDict["name"]]["coeffs"][2] = -1

        if reflDict["gmode"] == "xy":
            self.system[reflDict["name"]]["gmode"] = 0

        elif reflDict["gmode"] == "uv":
            self.system[reflDict["name"]]["gmode"] = 1

        elif reflDict["gmode"] == "AoE":
            # Assume is given in degrees
            # Convert Az and El to radians

            self.system[reflDict["name"]]["lims_Az"] = [self.system[reflDict["name"]]["lims_Az"][0],
                                                        self.system[reflDict["name"]]["lims_Az"][1]]

            self.system[reflDict["name"]]["lims_El"] = [self.system[reflDict["name"]]["lims_El"][0],
                                                        self.system[reflDict["name"]]["lims_El"][1]]

            self.system[reflDict["name"]]["gmode"] = 2

        self.num_ref += 1

    def rotateGrids(self, name, rotation, cRot=np.zeros(3)):
        self.system[name]["transf"] = MatRotate(rotation, self.system[name]["transf"], cRot)

    def translateGrids(self, name, translation):
        self.system[name]["transf"] = MatTranslate(translation, self.system[name]["transf"])

    def generateGrids(self, name):
        grids = generateGrid(self.system[name])
        return grids

    def saveElement(self, name):
        jsonDict = copyGrid(self.system[name])

        for key, value in self.system[name].items():
            if type(value) == np.ndarray:
                jsonDict[key] = value.tolist()

            else:
                jsonDict[key] = value

        with open('./{}{}.json'.format(self.savePathElem, name), 'w') as f:
            json.dump(jsonDict, f)

    def readCustomBeam(self, name_beam, name_source, comp, convert_to_current=True, mode="PMC"):
        rfield = np.loadtxt(self.customBeamPath + "r" + name_beam + ".txt")
        ifield = np.loadtxt(self.customBeamPath + "i" + name_beam + ".txt")

        print(rfield.shape)

        field = rfield + 1j*ifield

        shape = self.system[name_source]["gridsize"]

        fields_c = self._compToFields(comp, field)
        currents_c = calcCurrents(fields_c, self.system[name_source], mode)

        return currents_c, fields_c

    def propagatePO_CPU(self, source_name, target_name, s_currents, k,
                    epsilon=1, t_direction=-1, nThreads=1,
                    mode="JM", precision="double"):

        source = self.system[source_name]
        target = self.system[target_name]

        if precision == "double":
            out = POPPy_CPUd(source, target, s_currents, k, epsilon, t_direction, nThreads, mode)

        return out

    def propagatePO_GPU(self, source_name, target_name, s_currents, k,
                    epsilon=1, t_direction=-1, nThreads=256,
                    mode="JM", precision="single"):

        source = self.system[source_name]
        target = self.system[target_name]

        if precision == "single":
            out = POPPy_GPUf(source, target, s_currents, k, epsilon, t_direction, nThreads, mode)

        return out

    def createFrame(self, argDict):
        frame_in = makeRTframe(argDict)
        return frame_in

    def loadFramePoynt(self, Poynting, name_source):
        grids = generateGrid(self.system[name_source])

        nTot = Poynting.x.shape[0] * Poynting.x.shape[1]
        frame_in = frame(nTot, grids.x.ravel(), grids.y.ravel(), grids.z.ravel(),
                        Poynting.x.ravel(), Poynting.y.ravel(), Poynting.z.ravel())

        return frame_in

    def calcRayLen(self, *args, start=0):
        if isinstance(start, np.ndarray):
            frame0 = args[0]

            out = []
            sumd = np.zeros(len(frame0.x))

            diffx = frame0.x - start[0]
            diffy = frame0.y - start[1]
            diffz = frame0.z - start[2]

            lens = np.sqrt(diffx**2 + diffy**2 + diffz**2)
            out.append(lens)

            sumd += lens

            for i in range(len(args) - 1):
                diffx = args[i+1].x - frame0.x
                diffy = args[i+1].y - frame0.y
                diffz = args[i+1].z - frame0.z

                lens = np.sqrt(diffx**2 + diffy**2 + diffz**2)
                out.append(lens)

                frame0 = args[i+1]
                sumd += lens

            out.append(sumd)

        else:
            frame0 = args[0]

            out = []
            sumd = np.zeros(len(frame0.x))

            for i in range(len(args) - 1):
                diffx = args[i+1].x - frame0.x
                diffy = args[i+1].y - frame0.y
                diffz = args[i+1].z - frame0.z

                lens = np.sqrt(diffx**2 + diffy**2 + diffz**2)
                out.append(lens)

                frame0 = args[i+1]
                sumd += lens

            out.append(sumd)

        return out

    def createGauss(self, gaussDict, name_source):
        gauss_in = makeGauss(gaussDict, self.system[name_source])
        return gauss_in

    def runRayTracer(self, fr_in, name_target, epsilon=1e-10, nThreads=1, t0=100):
        fr_out = RT_CPUd(self.system[name_target], fr_in, epsilon, t0, nThreads)
        return fr_out

    def runRT_GPU(self, fr_in, name_target, epsilon=1e-10, nThreads=256, t0=100):
        fr_out = RT_GPUf(self.system[name_target], fr_in, epsilon, t0, nThreads)
        return fr_out

    def interpFrame(self, fr_in, field, name_target, method="nearest"):
        grids = generateGrid(self.system[name_target])

        points = (fr_in.x, fr_in.y, fr_in.z)

        rfield = np.real(field)
        ifield = np.imag(field)

        grid_interp = (grids.x, grids.y, grids.z)

        rout = griddata(points, rfield, grid_interp, method=method)
        iout = griddata(points, ifield, grid_interp, method=method)

        out = rout.reshape(self.system[name_target]["gridsize"]) + 1j * iout.reshape(self.system[name_target]["gridsize"])

        return out

    def calcSpillover(self, field, name_target, aperDict):
        surfaceObj = self.system[name_target]
        return effs.calcSpillover(field, surfaceObj, aperDict)

    def calcTaper(self, field, name_target, aperDict):
        surfaceObj = self.system[name_target]
        return effs.calcTaper(field, surfaceObj, aperDict)

    def plotBeam2D(self, name_surface, field,
                    vmin=-30, vmax=0, show=True, amp_only=False,
                    save=False, polar=False, interpolation=None,
                    aperDict={"plot":False}, mode='dB', project='xy',
                    units='', name='', titleA="Amp", titleP="Phase"):

        plotObject = self.system[name_surface]

        plt.plotBeam2D(plotObject, field,
                        vmin, vmax, show, amp_only,
                        save, polar, interpolation,
                        aperDict, mode, project,
                        units, name, titleA, titleP, self.savePath)

    def plot3D(self, name_surface, fine=2, cmap=cm.cool,
                returns=False, ax_append=False, norm=False,
                show=True, foc1=False, foc2=False, save=True):

        plotObject = self.system[name_surface]

        plt.plot3D(plotObject, fine, cmap,
                    returns, ax_append, norm,
                    show, foc1, foc2, save, self.savePath)

    def plotSystem(self, fine=2, cmap=cm.cool,
                ax_append=False, norm=False,
                show=True, foc1=False, foc2=False, save=True, ret=False, RTframes=[]):

        figax = plt.plotSystem(self.system, fine, cmap,
                    ax_append, norm,
                    show, foc1, foc2, save, ret, RTframes, self.savePath)

        if ret:
            return figax

    def plotRTframe(self, frame, project="xy"):
        plt.plotRTframe(frame, project, self.savePath)

    def _compToFields(self, comp, field):
        null = np.zeros(field.shape, dtype=complex)

        if comp == "Ex":
            field_c = fields(field, null, null, null, null, null)
        elif comp == "Ey":
            field_c = fields(null, field, null, null, null, null)
        elif comp == "Ez":
            field_c = fields(null, null, field, null, null, null)
        elif comp == "Hx":
            field_c = fields(null, null, null, field, null, null)
        elif comp == "Hy":
            field_c = fields(null, null, null, null, field, null)
        elif comp == "Hz":
            field_c = fields(null, null, null, null, null, field)

        return field_c



if __name__ == "__main__":
    print("System interface for POPPy.")
