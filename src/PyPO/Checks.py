import numpy as np
import os
import ctypes
import pathlib

nThreads_cpu = os.cpu_count()

from src.PyPO.PyPOTypes import *
from src.PyPO.CustomLogger import CustomLogger

PO_modelist = ["JM", "EH", "JMEH", "EHP", "FF", "scalar"]

clog_mgr = CustomLogger(os.path.basename(__file__))
clog = clog_mgr.getCustomLogger()

##
# @file
# File containing all commonly used checks for PyPO user input.

##
# Check if the CUDA dynamically linked libraries exist.
# Checks the paths for Windows, Linux and Mac OS.
def has_CUDA():
    has = False

    win_cuda = os.path.exists(pathlib.Path(__file__).parents[2]/"out/build/Debug/pypogpu.dll")    
    nix_cuda = os.path.exists(pathlib.Path(__file__).parents[2]/"out/build/libpypogpu.so")
    mac_cuda = os.path.exists(pathlib.Path(__file__).parents[2]/"out/build/libpypogpu.dylib")

    has = win_cuda or nix_cuda or mac_cuda

    return has

##
# Check if a specified element is in the system dictionary.
#
# @param name Name of element.
# @param elements The system dictionary containing all elements.
# @param errStr Error string for appending error messages.
# @param extern Whether this function is called from System or from here.
#
# @returns errStr The error string with any new entries appended.
def check_elemSystem(name, elements, errStr="", extern=False):
    if name not in elements:
        errStr += errMsg_noelem(name)

    if extern:
        if errStr:
            errList = errStr.split("\n")[:-1]

            for err in errList:
                clog.error(err)
            raise ElemNameError()
    
    else:
        return errStr

##
# Check if a specified field is in the fields dictionary.
#
# @param name Name of field.
# @param fields The fields dictionary containing all fields.
# @param errStr Error string for appending error messages.
# @param extern Whether this function is called from System or from here.
#
# @returns errStr The error string with any new entries appended.
def check_fieldSystem(name, fields, errStr="", extern=False):
    if name not in fields:
        errStr += errMsg_nofield(name)

    if extern:
        if errStr:
            errList = errStr.split("\n")[:-1]

            for err in errList:
                clog.error(err)
            raise FieldNameError()
    
    else:
        return errStr

##
# Check if a specified current is in the currents dictionary.
#
# @param name Name of current.
# @param currents The currents dictionary containing all currents.
# @param errStr Error string for appending error messages.
# @param extern Whether this function is called from System or from here.
#
# @returns errStr The error string with any new entries appended.
def check_currentSystem(name, currents, errStr="", extern=False):
    if name not in currents:
        errStr += errMsg_nocurrent(name)

    if extern:
        if errStr:
            errList = errStr.split("\n")[:-1]

            for err in errList:
                clog.error(err)
            raise CurrentNameError()
    
    else:
        return errStr

##
# Check if a specified scalarfield is in the scalarfields dictionary.
#
# @param name Name of scalarfield.
# @param scalarfields The scalarfields dictionary containing all scalarfields.
# @param errStr Error string for appending error messages.
# @param extern Whether this function is called from System or from here.
#
# @returns errStr The error string with any new entries appended.
def check_scalarfieldSystem(name, scalarfields, errStr="", extern=False):
    if name not in scalarfields:
        errStr += errMsg_noscalarfield(name)

    if extern:
        if errStr:
            errList = errStr.split("\n")[:-1]

            for err in errList:
                clog.error(err)
            raise ScalarFieldNameError()
    
    else:
        return errStr

##
# Check if a specified frame is in the frames dictionary.
#
# @param name Name of frame.
# @param frames The frames dictionary containing all frames.
# @param errStr Error string for appending error messages.
# @param extern Whether this function is called from System or from here.
#
# @returns errStr The error string with any new entries appended.
def check_frameSystem(name, frames, errStr="", extern=False):
    if name not in frames:
        errStr += errMsg_noframe(name)

    if extern:
        if errStr:
            errList = errStr.split("\n")[:-1]

            for err in errList:
                clog.error(err)
            raise FrameNameError()
    
    else:
        return errStr

##
# Check if a specified group is in the groups dictionary.
#
# @param name Name of group.
# @param groups The groups dictionary containing all groups.
# @param errStr Error string for appending error messages.
# @param extern Whether this function is called from System or from here.
#
# @returns errStr The error string with any new entries appended.
def check_groupSystem(name, groups, errStr="", extern=False):
    if name not in groups:
        errStr += errMsg_nogroup(name)

    if extern:
        if errStr:
            errList = errStr.split("\n")[:-1]

            for err in errList:
                clog.error(err)
            raise GroupNameError()
    
    else:
        return errStr

##
# Input reflector error. Raised when an error is encountered in an input reflector dictionary.
class InputReflError(Exception):
    pass

##
# Input ray-trace error. Raised when an error is encountered in an input ray-trace dictionary.
class InputRTError(Exception):
    pass

##
# Propagate ray-trace error. Raised when an error is encountered in a ray-trace propagation dictionary.
class RunRTError(Exception):
    pass

##
# Input physical optics error. Raised when an error is encountered in an input PO beam dictionary.
class InputPOError(Exception):
    pass

##
# Propagate physical optics error. Raised when an error is encountered in a physical optics propagation dictionary.
class RunPOError(Exception):
    pass

##
# Element name error. Raised when specified element cannot be found in the system dictionary. 
class ElemNameError(Exception):
    pass

##
# Field name error. Raised when specified field cannot be found in the fields dictionary. 
class FieldNameError(Exception):
    pass

##
# Current name error. Raised when specified current cannot be found in the currents dictionary. 
class CurrentNameError(Exception):
    pass

##
# Frame name error. Raised when specified frame cannot be found in the frames dictionary. 
class FrameNameError(Exception):
    pass

##
# Scalarfield name error. Raised when specified scalarfield cannot be found in the scalarfields dictionary. 
class ScalarFieldNameError(Exception):
    pass

##
# Group name error. Raised when specified group cannot be found in the groups dictionary. 
class GroupNameError(Exception):
    pass

##
# Error message when a frame, field or current already occurs in the System.
#
# @param elemName Name of object already in use.
#
# @returns errStr The errorstring.
def errMsg_name(elemName):
    return f"Name \"{elemName}\" already in use. Choose different name.\n"

##
# Error message when a mandatory field has not been filled in a dictionary.
#
# @param fieldName Name of field in dictionary that is not filled.
# @param elemName Name of dictionary where error occured. 
#
# @returns errStr The errorstring.
def errMsg_field(fieldName, elemName):
    return f"Missing field \"{fieldName}\", element {elemName}.\n"

##
# Error message when a field has not been filled has been filled with an incorrect type.
#
# @param fieldName Name of field in dictionary that is incorrectly filled.
# @param inpType Type of given input.
# @param elemName Name of dictionary where error occured. 
# @param fieldType Expected type of input.
#
# @returns errStr The errorstring.
def errMsg_type(fieldName, inpType, elemName, fieldType):
    return f"Wrong type {inpType} in field \"{fieldName}\", element {elemName}. Expected {fieldType}.\n"

##
# Error message when a field has an unknown option.
#
# @param fieldName Name of field in dictionary.
# @param option Given option.
# @param elemName Name of dictionary where error occured. 
# @param args Expected options.
#
# @returns errStr The errorstring.
def errMsg_option(fieldName, option, elemName, args):
    if len(args) == 2:
        return f"Unknown option \"{option}\" in field \"{fieldName}\", element {elemName}. Expected \"{args[0]}\" or \"{args[1]}\".\n"

    elif len(args) == 3:
        return f"Unknown option \"{option}\" in field \"{fieldName}\", element {elemName}. Expected \"{args[0]}\", \"{args[1]}\" or \"{args[2]}\".\n"

##
# Error message when a field has an incorrect shape.
#
# @param fieldName Name of field in dictionary.
# @param shape Shape of input.
# @param elemName Name of dictionary where error occured.
# @param shapeExpect Expected input shape for field.
#
# @returns errStr The errorstring.
def errMsg_shape(fieldName, shape, elemName, shapeExpect):
    return f"Incorrect input shape of {shape} for field \"{fieldName}\", element {elemName}. Expected {shapeExpect}.\n"

##
# Error message when a wrong input value is encountered.
#
# @param fieldName Name of field where incorrect value is encountered.
# @param value Input value.
# @param Name of dictionary where error occured.
#
# @returns errStr The errorstring.
def errMsg_value(fieldName, value, elemName):
    return f"Incorrect value {value} encountered in field \"{fieldName}\", element {elemName}.\n"

##
# Error message when a reflector element is not present in System..
#
# @param elemName Name of element.
#
# @returns errStr The errorstring.
def errMsg_noelem(elemName):
    return f"Element {elemName} not in system.\n"

##
# Error message when a frame object is not present in System..
#
# @param frameName Name of frame.
#
# @returns errStr The errorstring.
def errMsg_noframe(frameName):
    return f"Frame {frameName} not in system.\n"

##
# Error message when a field object is not present in System..
#
# @param fieldName Name of field.
#
# @returns errStr The errorstring.
def errMsg_nofield(fieldName):
    return f"Field {fieldName} not in system.\n"

##
# Error message when a current object is not present in System..
#
# @param currentName Name of current.
#
# @returns errStr The errorstring.
def errMsg_nocurrent(currentName):
    return f"Current {currentName} not in system.\n"

##
# Error message when a scalarfield object is not present in System..
#
# @param scalarfieldName Name of scalarfield.
#
# @returns errStr The errorstring.
def errMsg_noscalarfield(scalarfieldName):
    return f"Scalar field {scalarfieldName} not in system.\n"

##
# Error message when a group is not present in System..
#
# @param groupName Name of group.
#
# @returns errStr The errorstring.
def errMsg_nogroup(groupName):
    return f"Group {groupName} not in system.\n"

## 
# Check if an input array has correct shape.
#
# @param fieldName Name of field containing array.
# @param elemDict Dictionary containing field.
# @param shape Expected shape of input array.
#
# @returns errStr The errorstring.
def block_ndarray(fieldName, elemDict, shape):
    _errStr = ""
    if not isinstance(elemDict[fieldName], np.ndarray):
        _errStr += errMsg_type(fieldName, type(elemDict[fieldName]), elemDict["name"], np.ndarray)

    elif not elemDict[fieldName].shape == shape:
        _errStr += errMsg_shape(fieldName, elemDict[fieldName].shape, elemDict["name"], f"{shape}")
    
    return _errStr

##
# Check element input dictionary.
#
# Checks the input dictionary for errors. Raises exceptions when encountered.
#
# @param elemName Name of element, string.
# @param nameList List of names in system dictionary.
# @param num_ref Number of reflectors in System.
def check_ElemDict(elemDict, nameList, num_ref):
    
    errStr = ""
   
    elemDict["transf"] = np.eye(4)
   
    if not "pos" in elemDict:
        elemDict["pos"] = np.zeros(3)

    else:
        errStr += block_ndarray("pos", elemDict, (3,))

    if not "ori" in elemDict:
        elemDict["ori"] = np.array([0,0,1])
    
    else:
        errStr += block_ndarray("ori", elemDict, (3,))

    if not "flip" in elemDict:
        elemDict["flip"] = False

    else:
        if not isinstance(elemDict["flip"], bool):
            clog.warning("Invalid option {elemDict['flip']} for flip. Defaulting to False.")

    if elemDict["type"] == 0:
        if not "name" in elemDict:
            elemDict["name"] = "Parabola"
        
        if "pmode" in elemDict:
            if elemDict["pmode"] == "focus":
                if "vertex" in elemDict:
                    errStr += block_ndarray("vertex", elemDict, (3,))
                else:
                    errStr += errMsg_field("vertex", elemDict["name"])

                if "focus_1" in elemDict:
                    errStr += block_ndarray("focus_1", elemDict, (3,))
                else:
                    errStr += errMsg_field("focus_1", elemDict["name"])

            elif elemDict["pmode"] == "manual":
                if "coeffs" in elemDict:
                    errStr += block_ndarray("coeffs", elemDict, (2,))

                else:
                    errStr += errMsg_field("coeffs", elemDict["name"])

            else:
                args = ["focus", "manual"]
                errStr += errMsg_option("pmode", elemDict["pmode"], elemDict["name"], args=args)

        else:
            errStr += errMsg_field("pmode", elemDict["name"])

    elif elemDict["type"] == 1 or elemDict["type"] == 2:
        if elemDict["type"] == 1:
            
            if not "name" in elemDict:
                elemDict["name"] = "Hyperbola"
        
        else:
            if not "name" in elemDict:
                elemDict["name"] = "Ellipse"

        if "pmode" in elemDict:
            if elemDict["pmode"] == "focus":
                if "focus_1" in elemDict:
                    errStr += block_ndarray("focus_1", elemDict, (3,))
                else:
                    errStr += errMsg_field("focus_1", elemDict["name"])

                if "focus_2" in elemDict:
                    errStr += block_ndarray("focus_2", elemDict, (3,))
                else:
                    errStr += errMsg_field("focus_2", elemDict["name"])
                
                if "ecc" in elemDict:
                    if not ((isinstance(elemDict["ecc"], float) or isinstance(elemDict["ecc"], int))):
                        errStr += errMsg_type("ecc", type(elemDict["ecc"]), elemDict["name"], [float, int])

                    elif elemDict["type"] == 1:
                        if elemDict["ecc"] <= 1:
                            errStr += errMsg_value("ecc", elemDict["ecc"], elemDict["name"])

                    elif elemDict["type"] == 2:
                        if elemDict["ecc"] < 0 or elemDict["ecc"] >= 1:
                            errStr += errMsg_value("ecc", elemDict["ecc"], elemDict["name"])
                
                else:
                    errStr += errMsg_field("ecc", elemDict["name"])
            
            elif elemDict["pmode"] == "manual":
                if "coeffs" in elemDict:
                    errStr += block_ndarray("coeffs", elemDict, (3,))
                else:
                    errStr += errMsg_field("coeffs", elemDict["name"])

            else:
                args = ["focus", "manual"]
                errStr += errMsg_option("pmode", elemDict["pmode"], elemDict["name"], args=args)

    elif elemDict["type"] == 3:
        if not "name" in elemDict:
            elemDict["name"] = "plane"

    if "gmode" in elemDict:
        if elemDict["gmode"] == "xy" or elemDict["gmode"] == 0:
            if "lims_x" in elemDict:
                errStr += block_ndarray("lims_x", elemDict, (2,))
            else:
                errStr += errMsg_field("lims_x", elemDict["name"])

            if "lims_y" in elemDict:
                errStr += block_ndarray("lims_y", elemDict, (2,))
            else:
                errStr += errMsg_field("lims_y", elemDict["name"])

        elif elemDict["gmode"] == "uv" or elemDict["gmode"] == 1:
            if not "gcenter" in elemDict:
                elemDict["gcenter"] = np.zeros(2)
           
            if not "ecc_uv" in elemDict:
                elemDict["ecc_uv"] = 0

            if not "rot_uv" in elemDict:
                elemDict["rot_uv"] = 0

            if "lims_u" in elemDict:
                errStr += block_ndarray("lims_u", elemDict, (2,))

                if elemDict["lims_u"][0] < 0:
                    errStr += errMsg_value("lims_u", elemDict["lims_u"][0], elemDict["name"])

                if elemDict["lims_u"][1] < 0:
                    errStr += errMsg_value("lims_u", elemDict["lims_u"][1], elemDict["name"])
            else:
                errStr += errMsg_field("lims_u", elemDict["name"])

            if "lims_v" in elemDict:
                errStr += block_ndarray("lims_v", elemDict, (2,))

                if elemDict["lims_v"][0] < 0:
                    errStr += errMsg_value("lims_v", elemDict["lims_v"][0], elemDict["name"])
 
                if elemDict["lims_v"][1] > 360:
                    errStr += errMsg_value("lims_v", elemDict["lims_v"][1], elemDict["name"])
            else:
                errStr += errMsg_field("lims_v", elemDict["name"])

            if "ecc_uv" in elemDict:
                if not ((isinstance(elemDict["ecc_uv"], float) or isinstance(elemDict["ecc_uv"], int))):
                    errStr += errMsg_type("ecc_uv", type(elemDict["ecc_uv"]), elemDict["name"], [float, int])

                if elemDict["ecc_uv"] < 0 or elemDict["ecc_uv"] > 1:
                    errStr += errMsg_value("ecc_uv", elemDict["ecc_uv"], elemDict["name"])

            if "rot_uv" in elemDict:
                if not ((isinstance(elemDict["rot_uv"], float) or isinstance(elemDict["rot_uv"], int))):
                    errStr += errMsg_type("rot_uv", type(elemDict["rot_uv"]), elemDict["name"], [float, int])
        
            if "gcenter" in elemDict:
                errStr += block_ndarray("gcenter", elemDict, (2,))

        elif elemDict["gmode"] == "AoE" or elemDict["gmode"] == 2:
            if "lims_Az" in elemDict:
                errStr += block_ndarray("lims_Az", elemDict, (2,))
            else:
                errStr += errMsg_field("lims_Az", elemDict["name"])

            if "lims_El" in elemDict:
                errStr += block_ndarray("lims_El", elemDict, (2,))
            else:
                errStr += errMsg_field("lims_El", elemDict["name"])
    
        else:
            args = ["xy", "uv", "AoE (plane only)"]
            errStr += errMsg_option("gmode", elemDict["gmode"], elemDict["name"], args=args)

    else:
        errStr += errMsg_field("gmode", elemDict["name"])

    if "gridsize" in elemDict:
        errStr += block_ndarray("gridsize", elemDict, (2,))

        if not (isinstance(elemDict["gridsize"][0], np.int64) or isinstance(elemDict["gridsize"][0], np.int32)):
            errStr += errMsg_type("gridsize[0]", type(elemDict["gridsize"][0]), elemDict["name"], [np.int64, np.int32])

        if not (isinstance(elemDict["gridsize"][1], np.int64) or isinstance(elemDict["gridsize"][1], np.int32)):
            errStr += errMsg_type("gridsize[1]", type(elemDict["gridsize"][1]), elemDict["name"], [np.int64, np.int32])
    
    if elemDict["name"] in nameList:
        elemDict["name"] = elemDict["name"] + "_{}".format(num_ref)

    if errStr:
        errList = errStr.split("\n")[:-1]

        for err in errList:
            clog.error(err)
        raise InputReflError()
    
    else:
        return 0

##
# Check a tubular input frame dictionary.
#
# @param TubeRTDict A TubeRTDict object.
# @param namelist List containing names of frames in System.
#
# @see TubeRTDict
def check_TubeRTDict(TubeRTDict, nameList):
    errStr = ""
    
    if TubeRTDict["name"] in nameList:
        errStr += errMsg_name(TubeRTDict["name"])

    if "nRays" in TubeRTDict:
        if not isinstance(TubeRTDict["nRays"], int):
            errStr += errMsg_type("nRays", type(TubeRTDict["nRays"]), "TubeRTDict", int)

    else:
        errStr += errMsg_field("nRays", "TubeRTDict")

    if "nRing" in TubeRTDict:
        if not isinstance(TubeRTDict["nRing"], int):
            errStr += errMsg_type("nRing", type(TubeRTDict["nRays"]), "TubeRTDict", int)

    else:
        errStr += errMsg_field("nRays", "TubeRTDict")


    if "angx0" in TubeRTDict:
        if not ((isinstance(TubeRTDict["angx0"], float) or isinstance(TubeRTDict["angx0"], int))):
            errStr += errMsg_type("angx0", type(TubeRTDict["angx0"]), "TubeRTDict", [float, int])

    else:
        errStr += errMsg_field("angx0", "TubeRTDict")


    if "angy0" in TubeRTDict:
        if not ((isinstance(TubeRTDict["angy0"], float) or isinstance(TubeRTDict["angy0"], int))):
            errStr += errMsg_type("angy0", type(TubeRTDict["angy0"]), "TubeRTDict", [float, int])

    else:
        errStr += errMsg_field("angy0", "TubeRTDict")


    if "x0" in TubeRTDict:
        if not ((isinstance(TubeRTDict["x0"], float) or isinstance(TubeRTDict["x0"], int))):
            errStr += errMsg_type("x0", type(TubeRTDict["x0"]), "TubeRTDict", [float, int])
        
        elif TubeRTDict["x0"] < 0:
            clog.warning(f"Encountered negative value {TubeRTDict['x0']} in field 'x0' in TubeRTDict {TubeRTDict['name']}. Changing sign.")
            TubeRTDict["x0"] *= -1

    else:
        errStr += errMsg_field("x0", "TubeRTDict")


    if "y0" in TubeRTDict:
        if not ((isinstance(TubeRTDict["y0"], float) or isinstance(TubeRTDict["y0"], int))):
            errStr += errMsg_type("y0", type(TubeRTDict["y0"]), "TubeRTDict", [float, int])
        
        elif TubeRTDict["y0"] < 0:
            clog.warning(f"Encountered negative value {TubeRTDict['y0']} in field 'y0' in TubeRTDict {TubeRTDict['name']}. Changing sign.")
            TubeRTDict["y0"] *= -1

    else:
        errStr += errMsg_field("y0", "TubeRTDict")

    if errStr:
        errList = errStr.split("\n")[:-1]

        for err in errList:
            clog.error(err)
        raise InputRTError()

##
# Check a Gaussian input frame dictionary.
#
# @param GRTDict A GRTDict object.
# @param namelist List containing names of frames in System.
#
# @see GRTDict
def check_GRTDict(GRTDict, nameList):
    errStr = ""
    
    if GRTDict["name"] in nameList:
        errStr += errMsg_name(GRTDict["name"])

    if "nRays" in GRTDict:
        if not isinstance(GRTDict["nRays"], int):
            errStr += errMsg_type("nRays", type(GRTDict["nRays"]), "GRTDict", int)

    else:
        errStr += errMsg_field("nRays", "GRTDict")

    if "lam" in GRTDict:
        if GRTDict["lam"] == 0 + 0j:
            clog.info(f"Never heard of a complex-valued wavelength of zero, but good try... Therefore changing wavelength now to 'lam' equals {np.pi:.42f}!")
            GRTDict["lam"] = np.pi

        if not isinstance(GRTDict["lam"], float):
            errStr += errMsg_type("lam", type(GRTDict["lam"]), "GRTDict", float)
        
        elif GRTDict["lam"] < 0:
            clog.warning(f"Encountered negative value {GRTDict['lam']} in field 'lam' in GRTDict {GRTDict['name']}. Changing sign.")
            GRTDict["lam"] *= -1

    else:
        errStr += errMsg_field("lam", "GRTDict")

    if "x0" in GRTDict:
        if not ((isinstance(GRTDict["x0"], float) or isinstance(GRTDict["x0"], int))):
            errStr += errMsg_type("x0", type(GRTDict["x0"]), "GRTDict", [float, int])

        elif GRTDict["x0"] < 0:
            clog.warning(f"Encountered negative value {GRTDict['x0']} in field 'x0' in GRTDict {GRTDict['name']}. Changing sign.")
            GRTDict["x0"] *= -1

    else:
        errStr += errMsg_field("x0", "GRTDict")


    if "y0" in GRTDict:
        if not ((isinstance(GRTDict["y0"], float) or isinstance(GRTDict["y0"], int))):
            errStr += errMsg_type("y0", type(GRTDict["y0"]), "GRTDict", [float, int])
        
        elif GRTDict["y0"] < 0:
            clog.warning(f"Encountered negative value {GRTDict['y0']} in field 'y0' in GRTDict {GRTDict['name']}. Changing sign.")
            GRTDict["y0"] *= -1

    else:
        errStr += errMsg_field("y0", "GRTDict")

    if "n" in GRTDict:
        if not ((isinstance(GRTDict["n"], float) or isinstance(GRTDict["n"], int))):
            errStr += errMsg_type("n", type(GRTDict["n"]), "GRTDict", [float, int])

    if errStr:
        errList = errStr.split("\n")[:-1]

        for err in errList:
            clog.error(err)
        raise InputRTError()

##
# Check a ray-trace propagation input dictionary.
#
# @param runRTDict A runRTDict.
# @param elements List containing names of surfaces in System.
# @param frames List containing names of frames in System.
def check_runRTDict(runRTDict, elements, frames):
    errStr = ""
   
    cuda = has_CUDA()
    errStr = check_frameSystem(runRTDict["fr_in"], frames, errStr)
    errStr = check_elemSystem(runRTDict["t_name"], elements, errStr)

    if "tol" not in runRTDict:
        runRTDict["tol"] = 1e-3

    elif "tol" in runRTDict:
        if runRTDict["tol"] < 0:
            clog.warning("Negative tolerances are not allowed. Changing sign.")
            runRTDict["tol"] *= -1


    if "t0" not in runRTDict:
        runRTDict["t0"] = 1

    if "device" not in runRTDict:
        runRTDict["device"] = "CPU"
    
    if "device" in runRTDict:
        if runRTDict["device"] != "CPU" and runRTDict["device"] != "GPU":
            clog.warning(f"Device {runRTDict['device']} unknown. Defaulting to CPU.")
            runRTDict["device"] = "CPU"

        if runRTDict["device"] == "GPU" and not cuda:
            clog.warning(f"No PyPO CUDA libraries found. Defaulting to CPU.")
            runRTDict["device"] = "CPU"

        if runRTDict["device"] == "CPU":
            if "nThreads" in runRTDict:
                if runRTDict["nThreads"] > nThreads_cpu:
                    clog.warning(f"Insufficient CPU threads available, automatically reducing threadcount.")
                    runRTDict["nThreads"] = nThreads_cpu

            else:
                runRTDict["nThreads"] = nThreads_cpu

        elif runRTDict["device"] == "GPU":
            if "nThreads" not in runRTDict:
                runRTDict["nThreads"] = 256


    if errStr:
        errList = errStr.split("\n")[:-1]

        for err in errList:
            clog.error(err)
        raise RunRTError()

##
# Check a point source input beam dictionary.
#
# @param PSDict A PSDict object.
# @param namelist List containing names of fields in System.
#
# @see PSDict
def check_PSDict(PSDict, nameList):
    errStr = ""
    
    if PSDict["name"] in nameList:
        errStr += errMsg_name(PSDict["name"])

    if "lam" in PSDict:
        if PSDict["lam"] == 0 + 0j:
            clog.info(f"Never heard of a complex-valued wavelength of zero, but good try... Therefore changing wavelength now to 'lam' equals {np.pi:.42f}!")
            PSDict["lam"] = np.pi

        if not ((isinstance(PSDict["lam"], float) or isinstance(PSDict["lam"], int))):
            errStr += errMsg_type("lam", type(PSDict["lam"]), "PSDict", [float, int])
        
        elif PSDict["lam"] < 0:
            clog.warning(f"Encountered negative value {PSDict['lam']} in field 'lam' in PSDict {PSDict['name']}. Changing sign.")
            PSDict["lam"] *= -1

    else:
        errStr += errMsg_field("lam", "PSDict")

    if "phase" in PSDict:
        if not ((isinstance(PSDict["phase"], float) or isinstance(PSDict["phase"], int))):
            errStr += errMsg_type("phase", type(PSDict["phase"]), "PSDict", [float, int])

    else:
        PSDict["phase"] = 0

    if "pol" in PSDict:
        errStr += block_ndarray("pol", PSDict, (3,))

    else:
        PSDict["pol"] = np.array([1, 0, 0])

    if "E0" in PSDict:
        if not ((isinstance(PSDict["E0"], float) or isinstance(PSDict["E0"], int))):
            errStr += errMsg_type("E0", type(PSDict["E0"]), "PSDict", [float, int])

    else:
        PSDict["E0"] = 1

    if errStr:
        errList = errStr.split("\n")[:-1]

        for err in errList:
            clog.error(err)
        raise InputPOError()

##
# Check a Gaussian input beam dictionary.
#
# @param GPODict A GPODict object.
# @param namelist List containing names of fields in System.
#
# @see GPODict
def check_GPODict(GPODict, nameList):
    errStr = ""
    
    if GPODict["name"] in nameList:
        errStr += errMsg_name(GPODict["name"])

    if "lam" in GPODict:
        if GPODict["lam"] == 0 + 0j:
            clog.info(f"Never heard of a complex-valued wavelength of zero, but good try... Therefore changing wavelength now to 'lam' equals {np.pi:.42f}!")
            GPODict["lam"] = np.pi

        if not ((isinstance(GPODict["lam"], float) or isinstance(GPODict["lam"], int))):
            errStr += errMsg_type("lam", type(GPODict["lam"]), "GPODict", [float, int])
        
        elif GPODict["lam"] < 0:
            clog.warning(f"Encountered negative value {GPODict['lam']} in field 'lam' in GPODict {GPODict['name']}. Changing sign.")
            GPODict["lam"] *= -1

    else:
        errStr += errMsg_field("lam", "GPODict")

    if "w0x" in GPODict:
        if not ((isinstance(GPODict["w0x"], float) or isinstance(GPODict["w0x"], int))):
            errStr += errMsg_type("w0x", type(GPODict["w0x"]), "GPODict", [float, int])

        elif GPODict["w0x"] < 0:
            clog.warning(f"Encountered negative value {GPODict['w0x']} in field 'w0x' in GPODict {GPODict['name']}. Changing sign.")
            GPODict["w0x"] *= -1

    else:
        errStr += errMsg_field("w0x", "GPODict")


    if "w0y" in GPODict:
        if not ((isinstance(GPODict["w0y"], float) or isinstance(GPODict["w0y"], int))):
            errStr += errMsg_type("w0y", type(GPODict["w0y"]), "GPODict", [float, int])
        
        elif GPODict["w0y"] < 0:
            clog.warning(f"Encountered negative value {GPODict['w0y']} in field 'w0y' in GPODict {GPODict['name']}. Changing sign.")
            GPODict["w0y"] *= -1

    else:
        errStr += errMsg_field("w0y", "GPODict")

    if "n" in GPODict:
        if not ((isinstance(GPODict["n"], float) or isinstance(GPODict["n"], int))):
            errStr += errMsg_type("n", type(GPODict["n"]), "GPODict", [float, int])

        elif GPODict["n"] < 1 and GPODict >= 0:
            clog.warning("Refractive indices smaller than unity are not allowed. Changing to 1.")

    else:
        GPODict["n"] = 1

    if "dxyz" in GPODict:
        if not ((isinstance(GPODict["dxyz"], float) or isinstance(GPODict["dxyz"], int))):
            errStr += errMsg_type("dxyz", type(GPODict["dxyz"]), "GPODict", [float, int])

    else:
        GPODict["dxyz"] = 0

    if "pol" in GPODict:
        errStr += block_ndarray("pol", GPODict, (3,))

    else:
        GPODict["pol"] = np.array([1, 0, 0])

    if "E0" in GPODict:
        if not ((isinstance(GPODict["E0"], float) or isinstance(GPODict["E0"], int))):
            errStr += errMsg_type("E0", type(GPODict["E0"]), "GPODict", [float, int])

    else:
        GPODict["E0"] = 1

    if errStr:
        errList = errStr.split("\n")[:-1]

        for err in errList:
            clog.error(err)
        raise InputPOError()

##
# Check a physical optics propagation input dictionary.
#
# @param runPODict A runPODict.
# @param elements List containing names of surfaces in System.
# @param currents List containing names of currents in System.
# @param scalarfields List containing names of scalarfields in System.
def check_runPODict(runPODict, elements, currents, scalarfields):
    errStr = ""

    cuda = has_CUDA()
    
    if not "exp" in runPODict:
        runPODict["exp"] = "fwd"

    if "mode" not in runPODict:
        errStr += f"Please provide propagation mode.\n"
    
    else:
        if runPODict["mode"] not in PO_modelist:
            errStr += f"{runPODict['mode']} is not a valid propagation mode.\n"

        if "s_current" in runPODict:
            errStr = check_currentSystem(runPODict["s_current"], currents, errStr)
        
        if "s_scalarfield" in runPODict:
            errStr = check_frameSystem(runPODict["s_scalarfield"], scalarfields, errStr)
    
    errStr = check_elemSystem(runPODict["t_name"], elements, errStr)
   
    if "epsilon" not in runPODict:
        runPODict["epsilon"] = 1

    if "device" not in runPODict:
        runPODict["device"] = "CPU"

    if "device" in runPODict:
        if runPODict["device"] != "CPU" and runPODict["device"] != "GPU":
            clog.warning(f"Device {runPODict['device']} unknown. Defaulting to CPU.")
            runPODict["device"] = "CPU"

        if runPODict["device"] == "GPU" and not cuda:
            clog.warning(f"No PyPO CUDA libraries found. Defaulting to CPU.")
            runPODict["device"] = "CPU"

        if runPODict["device"] == "CPU":
            
            if "nThreads" in runPODict:
                if runPODict["nThreads"] > nThreads_cpu:
                    clog.warning(f"Insufficient CPU threads available, automatically reducing threadcount.")
                    runPODict["nThreads"] = nThreads_cpu

            else:
                runPODict["nThreads"] = nThreads_cpu

        elif runPODict["device"] == "GPU":
            if "nThreads" not in runPODict:
                runPODict["nThreads"] = 256


    if errStr:
        errList = errStr.split("\n")[:-1]
        for err in errList:
            clog.error(err)
        raise RunPOError()

##
# CHeck if aperture dictionary is valid.
def check_aperDict(aperDict):
    errStr = ""

    if "plot" in aperDict:
        if not isinstance(aperDict["plot"], bool):
            errStr += errMsg_type("plot", type(aperDict["plot"]), "aperDict", bool)

    else:
        aperDict["plot"] = True

    if "center" in aperDict:
        errStr += block_ndarray("center", aperDict, (2,))

    else:
        aperDict["center"] = np.zeros(2)

    if not "outer" in aperDict:
        errStr += errMsg_field("outer", "aperDict")
    
    if not "inner" in aperDict:
        errStr += errMsg_field("inner", "aperDict")

##
# Check if ellipsoid limits are valid points.
# If not, reduces limits to acceptable values.
#
# @param ellipsoid A reflDict containing description of ellipsoid surface.
def check_ellipseLimits(ellipsoid):
    buff = 1000
    idx_lim = 0

    if ellipsoid["coeffs"][1] < ellipsoid["coeffs"][0]:
        idx_lim = 1

    if ellipsoid["gmode"] == 0:
        if np.absolute(ellipsoid["lims_x"][0]) > ellipsoid["coeffs"][idx_lim]:
            clog.warning(f"Lower x-limit of {ellipsoid['lims_x'][0]:.3f} incompatible with ellipsoid {ellipsoid['name']}. Changing to {ellipsoid['coeffs'][idx_lim]}.")
            ellipsoid["lims_x"][0] = ellipsoid["coeffs"][idx_lim] + ellipsoid["coeffs"][0] / buff
        
        if np.absolute(ellipsoid["lims_x"][1]) > ellipsoid["coeffs"][idx_lim]:
            clog.warning(f"Upper x-limit of {ellipsoid['lims_x'][1]:.3f} incompatible with ellipsoid {ellipsoid['name']}. Changing to {ellipsoid['coeffs'][idx_lim]}.")
            ellipsoid["lims_x"][1] = ellipsoid["coeffs"][idx_lim] - ellipsoid["lims_x"][1] / buff
        
        if np.absolute(ellipsoid["lims_y"][0]) > ellipsoid["coeffs"][idx_lim]:
            clog.warning(f"Lower y-limit of {ellipsoid['lims_y'][0]:.3f} incompatible with ellipsoid {ellipsoid['name']}. Changing to {ellipsoid['coeffs'][idx_lim]}.")
            ellipsoid["lims_y"][0] = ellipsoid["coeffs"][idx_lim] + ellipsoid["lims_y"][0] / buff
        
        if np.absolute(ellipsoid["lims_y"][1]) > ellipsoid["coeffs"][idx_lim]:
            clog.warning(f"Upper y-limit of {ellipsoid['lims_y'][1]:.3f} incompatible with ellipsoid {ellipsoid['name']}. Changing to {ellipsoid['coeffs'][idx_lim]}.")
            ellipsoid["lims_y"][1] = ellipsoid["coeffs"][idx_lim] - ellipsoid["lims_y"][1] / buff

    elif ellipsoid["gmode"] == 1:
        if np.absolute(ellipsoid["lims_u"][0]) > ellipsoid["coeffs"][idx_lim]:
            clog.warning(f"Lower u-limit of {ellipsoid['lims_u'][0]:.3f} incompatible with ellipsoid {ellipsoid['name']}. Changing to {ellipsoid['coeffs'][idx_lim]}.")
            ellipsoid["lims_u"][0] = ellipsoid["coeffs"][idx_lim] - ellipsoid["lims_u"][0] / buff
 
        if np.absolute(ellipsoid["lims_u"][1]) > ellipsoid["coeffs"][idx_lim]:
            clog.warning(f"Upper u-limit of {ellipsoid['lims_u'][1]:.3f} incompatible with ellipsoid {ellipsoid['name']}. Changing to {ellipsoid['coeffs'][idx_lim]}.")
            ellipsoid["lims_u"][1] = ellipsoid["coeffs"][idx_lim] - ellipsoid["lims_u"][1] / buff

