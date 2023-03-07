import numpy as np
from scipy.linalg import svd as svd

def MatRotate(theta, matAppend=None, pivot=None, radians=False):
    """
    Create 3D rotation matrix and rotate grids of points.

    @param  ->
        theta       :   Array containing rotations around x,y,z axes in degrees.
        origin      :   Origin of rotation.
        radians     :   Whether theta is in degrees or radians.

    @return ->
        matOut      :   Full affine rotation matrix.
    """
    pivot = np.zeros(3) if pivot is None else pivot
    matAppend = np.eye(4) if matAppend is None else matAppend

    if radians:
        theta_x, theta_y, theta_z = theta

    else:
        theta_x, theta_y, theta_z = np.radians(theta)

    ox, oy, oz = pivot

    trans1 = np.array([[1, 0, 0, -ox],
                    [0, 1, 0, -oy],
                    [0, 0, 1, -oz],
                    [0, 0, 0, 1]])

    rotX = np.array([[1, 0, 0, 0],
                    [0, np.cos(theta_x), -np.sin(theta_x), 0],
                    [0, np.sin(theta_x), np.cos(theta_x), 0],
                    [0, 0, 0, 1]])

    rotY = np.array([[np.cos(theta_y), 0, np.sin(theta_y), 0],
                    [0, 1, 0, 0],
                    [-np.sin(theta_y), 0, np.cos(theta_y), 0],
                    [0, 0, 0, 1]])

    rotZ = np.array([[np.cos(theta_z), -np.sin(theta_z), 0, 0],
                    [np.sin(theta_z), np.cos(theta_z), 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])

    trans2 = np.array([[1, 0, 0, ox],
                    [0, 1, 0, oy],
                    [0, 0, 1, oz],
                    [0, 0, 0, 1]])
    
    matOut = (trans2 @ (rotZ @ (rotY @ (rotX @ trans1)))) @ matAppend

    return matOut

def MatTranslate(trans, matAppend=None):
    matAppend = np.eye(4) if matAppend is None else matAppend
    xt, yt, zt = trans
    trans = np.array([[1, 0, 0, xt],
                    [0, 1, 0, yt],
                    [0, 0, 1, zt],
                    [0, 0, 0, 1]])

    matOut = trans @ matAppend

    return matOut

def InvertMat(mat):
    R_T = mat[:3, :3].T
    R_Tt = -R_T @ mat[:3, -1]

    matInv = np.eye(4)
    matInv[:3, :3] = R_T
    matInv[:3, -1] = R_Tt

    return matInv

