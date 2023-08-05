import uproot
from jax import numpy as np
import numpy as onp
from itertools import product
from timeit import default_timer as timer

import init

def read_array_filtered(tree, branches, selection = None, sel_branches = []) : 
  arrays = []
  for data in tree.pandas.iterate(branches = branches + sel_branches) : 
      if selection : df = data.query(selection)
      else : df = data
      arrays += [ df[list(branches)].to_numpy() ]
  return onp.concatenate(arrays, axis = 0)

def read_array(tree, branches) : 
  a = []
  for b in branches : 
    i = tree.array(b)
    if len(i.shape)==1 : a += [ i ]
    else : a += [ i[:,0] ]
  #a = [ tree.array(b) for b in branches ]
  #print("\n".join([ f"{b} : {i.shape}" for i,b in zip(a, branches)]))
  return np.stack(a, axis = 1)

def write_array(rootfile, array, branches, tree="tree") : 
  """
     Store numpy 2D array in the ROOT file using uproot. 
       rootfile : ROOT file name
       array : numpy array to store. The shape of the array should be (N, V), 
               where N is the number of events in the NTuple, and V is the 
               number of branches
       branches : list of V strings defining branch names
       tree : name of the tree
     All branches are of double precision
  """
  with uproot.recreate(rootfile, compression=uproot.ZLIB(4)) as file :  
    file[tree] = uproot.newtree( { b : "float64" for b in branches } )
    d = { b : array[:,i] for i,b in enumerate(branches) }
    file[tree].extend(d)
