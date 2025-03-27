import numpy as np
from sktime.libs.vmdpy import VMD

def perform_vmd(signal, alpha, tau, K, DC, init, tol):
    """
    Perform Variational Mode Decomposition on a signal using vmdpy from sktime.

    Parameters:
    signal (array-like): The input signal to decompose.
    alpha (float): The balancing parameter of the data-fidelity constraint.
    tau (float): The noise tolerance.
    K (int): The number of modes to extract.
    DC (bool): True if the first mode is initialized as a DC component.
    init (int): Initialization method (0: all zeros, 1: peak filtering, 2: Wiener filtering).
    tol (float): Tolerance for the convergence criterion.

    Returns:
    u_hat (array-like): The decomposed modes.
    u (array-like): The reconstructed signal.
    omega (array-like): The central frequencies of the modes.
    """
    # Perform VMD
    u_hat, u, omega = VMD(signal, alpha, tau, K, DC, init, tol)
    return u_hat, u, omega
