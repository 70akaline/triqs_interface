from pytriqs.gf.local import *
from pytriqs.operators import *
from pytriqs.applications.impurity_solvers.alps_cthyb import Solver
from pytriqs.archive import HDFArchive
import pytriqs.utility.mpi as mpi

# Parameters
D, V, U = 1.0, 0.2, 4.0
e_f, beta = -U/2.0, 50

# Construct the impurity solver with the inverse temperature
# and the structure of the Green's functions
S = Solver(beta = beta, gf_struct = {'up':[0], 'down':[0]}, n_l = 100)

# Initialize the non-interacting Green's function S.G0_iw
for name, g0 in S.G0_iw: g0 << inverse(iOmega_n - e_f - V**2 * Wilson(D))

# Run the solver. The result will be in S.G
S.solve(h_int = U * n('up',0) * n('down',0), max_time = 60, perform_post_proc = True)

# Save the results in an hdf5 file (only on the master node)
if mpi.is_master_node():
    with HDFArchive("aim_alps_solution.h5",'w') as Results:
        Results["G_tau"] = S.G_tau
        Results["G_iw"] = S.G_iw
        Results["G_l"] = S.G_l
