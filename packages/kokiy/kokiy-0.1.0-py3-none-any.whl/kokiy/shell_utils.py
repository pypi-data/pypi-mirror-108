"""
Module for cartesian or axi-cylindrical cut plane tools
"""

import numpy as np

from arnica.utils.vector_actions import yz_to_theta
from arnica.utils.cloud2cloud import cloud2cloud

from kokiy import AxiShell
from kokiy import CartShell


# TODO: do we really care with those that misuse import?
__all__ = ["infer_shell_from_xyz", "axishell_create_structured_base",
           "cartshell_create_structured_base",
           "interpolate_solutions_on_shell",
           "shell_geom_type", "shell_repr"]


def infer_shell_from_xyz(mesh_xyz, geom_type, shape, bnd_angles=None):
    """ Build a shell from an AVBP Cut

    :param geom_type: str, either "cart" or "axicyl".
    :param shape: tuple (nu,nv), discretization of the shell
    :param bnd_angles: Boundary angles to keep a fraction of the cuts
    :type bnd_angles: list of 2 floats to limite the range of azimuth
    """

    #mesh = find_mesh_for_sol(paths, prefix)
    # Build shell
    if geom_type == "axicyl":
        shell = axishell_create_structured_base(
            shape[0],
            shape[1],
            mesh_xyz,
            bnd_angles)
    elif geom_type == "cart":
        shell = cartshell_create_structured_base(
            shape[0],
            shape[1],
            mesh_xyz)
    return shell


def axishell_create_structured_base(n_longi, n_azi, mesh, bnd_angles=None):
    """
    *Obtain the base in structured mesh*

    Assumes the mesh is the x_axis rotated extrusion of an (x,r) curve.

    :param n_longi: Number of longitudinal points of the shell
    :type n_longi: int
    :param n_azi: Number of azimuthal points of the shell
    :type n_azi: int
    :param mesh: Array of coordinates of the cut mesh of shape (n, 3)
    :param bnd_angles: Boundary angles to keep a fraction of the cuts
    :type bnd_angles: list of 2 floats

    :returns:
        - **shell** -  An array representing axysymmetric computational shell
    """

    x_vals = mesh[:, 0]
    r_vals = np.sqrt(np.square(mesh[:, 1]) + np.square(mesh[:, 2]))

    corners_idx = [np.argmin(x_vals), np.argmax(x_vals)]
    if corners_idx[0] == corners_idx[1]:
        corners_idx = [np.argmin(r_vals), np.argmax(r_vals)]
    angle_vals = np.rad2deg(yz_to_theta(mesh))
    angle_range = np.max(angle_vals) - np.min(angle_vals)
    angle_min = np.amin(angle_vals)

    if bnd_angles is not None:
        try:
            if bnd_angles[1] - bnd_angles[0] > angle_range:
                raise ValueError
        except ValueError as value_error:
            msg = "Your cuts seem smaller than the range of angles you specified:\n"
            msg += f"{bnd_angles[1]} - {bnd_angles[0]} > {angle_range}\n"
            msg += "Please check the input file."
            raise ValueError(msg) from value_error
        try:
            if bnd_angles[0] < np.amin(angle_vals) or bnd_angles[1] > np.amax(angle_vals):
                raise ValueError
        except ValueError as value_error:
            msg = "The bounds you specified are outside the actual bounds of the cuts.\n"
            msg += "Please check the input file"
            raise ValueError(msg) from value_error
        angle_range = bnd_angles[1] - bnd_angles[0]
        angle_min = bnd_angles[0]

    shell = AxiShell(
        n_azi,
        n_longi,
        angle_range,
        x_vals[corners_idx],
        r_vals[corners_idx],
        angle_min,
    )

    return shell


def cartshell_create_structured_base(n_longi, n_trans, mesh):
    # pylint: disable=invalid-name
    """
    *Obtain the base in structured mesh*

    Assumes the path is square, aligned with y and z, with x = constant.

    :param n_longi: Number of longitudinal points of the shell
    :type n_longi: int
    :param n_trans: Number of transversal points of the shell
    :type n_trans: int
    :param mesh: Array of coordinates of the cut mesh of shape (n, 3)

    :returns:
        - **shell** -  An array representing cartesian computational shell
    """

    x_vals, y_vals, z_vals = mesh.T

    zero = (x_vals.mean(), y_vals.min(), z_vals.min())
    v_max = (x_vals.mean(), y_vals.max(), z_vals.min())
    u_max = (x_vals.mean(), y_vals.min(), z_vals.max())
    shell = CartShell(
        n_trans,
        n_longi,
        zero,
        u_max,
        v_max,
    )

    return shell


# TODO :  Eloi, these two functions are the thing to optimize for you. Here, and in cloud2cloud...

def _shell_interp_on_struct_base(shell, mesh, raw_data):
    """
    *Interpolate unstructured data on a structured grid*

    :param shell: AxiShell or CartShell object
    :param mesh: Array of shape (N,3) containing coordinates of raw_data
    :param raw_data: A numpy structured array gathering the unstructured data

    :returns: **struct_data** -  An array holding the intrepolated structured data
    """

    dim = shell.xyz.shape[-1]
    target_xyz = shell.xyz.reshape(-1, dim)
    raw_data_dict = {key: raw_data[key] for key in raw_data.dtype.names}  # Structured array to dict

    struct_dict = cloud2cloud(mesh, raw_data_dict, target_xyz, stencil=4, power=4)

    struct_data = np.empty(shell.shape, dtype=raw_data.dtype)
    for key in struct_dict:
        struct_data[key] = struct_dict[key].reshape(shell.shape)

    return struct_data


def interpolate_solutions_on_shell(shell, mesh, raw_data):
    """
    *Loads AVBP solutions interpolated on structured mesh.*

    :param shell: A shell
    :param data_dict: | A dict( ) containing data on the format \
                      **data_dict** [*key*] = array(*n_steps*, *n_theta*, *n_r*)
                      with various names "rho", "rhou"...

    :returns:
        - **interpol_data** - A dict( ) containing interpolated data
    """

    # TODO : make this interpolation without the for on times
    # probably inside the cloud to cloud
    n_steps = raw_data.shape[0]
    interpol_data = np.zeros((n_steps, *shell.shape), dtype=raw_data.dtype)
    for step in range(n_steps):
        interpol_data[step] = _shell_interp_on_struct_base(
            shell,
            mesh,
            raw_data[step],
        )

    return interpol_data


def shell_geom_type(shell):
    """Return the shell geom_type"""
    # TODO: really required?
    if isinstance(shell, AxiShell):
        return "axicyl"
    elif isinstance(shell, CartShell):
        return "cart"
    else:
        raise RuntimeError("Shell object must be an AxiShell or a CartShell")


def shell_repr(shell):
    """return a shell description"""
    # TODO: why not to make it a method of shell?
    out = f"""
Shell
-----

shape :{shell.shape}
type : {shell_geom_type(shell)}

"""
    return out
