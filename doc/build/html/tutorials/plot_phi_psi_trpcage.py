
# coding: utf-8

# # **Aim**
# 
# + download pdb file
# + calculate phi/psi for specific residue
# + show ramachandran plot

# In[1]:

# do some configs to get better plot
get_ipython().magic('matplotlib inline')
get_ipython().magic("config InlineBackend.figure_format = 'retina'")
import matplotlib
matplotlib.rcParams['savefig.dpi'] = 2 * matplotlib.rcParams['savefig.dpi'] # larger image
from matplotlib import pyplot as plt
import numpy as np
import pytraj as pt


# In[2]:

# download trp-cage mini protein
# http://www.rcsb.org/pdb/explore.do?structureId=1l2y

traj = pt.load_pdb_rcsb('1L2Y')
print(traj)
print(set(res.name for res in traj.top.residues))


# In[3]:

# calculate phi/psi for Gly residues
# need to get indcies of Gly residues
indices = [idx for idx, res in enumerate(traj.top.residues) if 'GLY' in res.name]
print('Gly resdiue indices = ', indices)

dataset = pt.multidihedral(traj, 'phi psi', resrange=indices)
print(dataset)


# In[4]:

# take data for 'phi' and flatten to 1D array
phi = np.array([d.values for d in dataset if 'phi' in d.key]).flatten()

# take data for 'psi' and flatten to 1D array
psi = np.array([d.values for d in dataset if 'psi' in d.key]).flatten()

# setup color
colors = np.random.rand(len(psi))

plt.xlim([-180, 180])
plt.ylim([-180, 180])
plt.xlabel('phi')
plt.ylabel('psi')
plt.grid()
plt.scatter(phi, psi, alpha=0.5, c=colors)

