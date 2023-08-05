from jax import numpy as np
import numpy as onp
import matplotlib
import matplotlib.pyplot as plt
import uproot
import uproot4
import functools
from scipy.ndimage import gaussian_filter

import sys
sys.path.append("../")

from plotting import plot_distr1d_comparison, set_lhcb_style, plot_hist2d
from tuples import read_array_filtered, write_array, read_array

import argparse
from contextlib import contextmanager

def get_samples() : 
  import samples
  d = {}
  for i in samples.__all__ : 
    module = __import__("samples." + i)
    s = getattr(getattr(module, i), "sample")
    d[i] = s
  return d

def get_variables() : 
  import variables
  d = {}
  for i in variables.__all__ : 
    module = __import__("variables." + i)
    c = getattr(getattr(module, i), "variable")
    d[i] = c
  return d

@contextmanager
def plot(name, prefix) : 
  fig, ax = plt.subplots(figsize = (5.5, 4.0) )
  fig.subplots_adjust(bottom=0.18, left = 0.18, right = 0.85, top = 0.9)
  yield fig, ax
  fig.savefig(prefix + name + ".pdf")
  fig.savefig(prefix + name + ".png")

def main() : 

  parser = argparse.ArgumentParser(description = "PIDGen validation", 
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

  parser.add_argument('--input', type=str, default = None, 
                      help="Input ROOT file")
  parser.add_argument('--intree', type=str, default = None, 
                      help="Input TTree")
  parser.add_argument('--sample', type=str, default = None, 
                      help="Calibration sample name")
  parser.add_argument('--dataset', type=str, default = None, 
                      help="Calibration dataset in the form Polarity_Year, e.g. MagUp_2018")
  parser.add_argument('--variable', type=str, default = None, 
                      help="PID variable to resample")
  parser.add_argument('--weight', type=str, default = None, 
                      help="Weigth branch name")
  parser.add_argument('--branches', type=str, default = "pt:eta:ntr", 
                      help="Input branches for Pt,Eta,Ntracks variables in the form Pt:Eta:Ntrack")
  parser.add_argument('--pidgen', type=str, default = "pidgen", 
                      help="Resampled PID branch")
  parser.add_argument('--piddata', type=str, default = "pid", 
                      help="Original PID branch")
  parser.add_argument('--output', type=str, default = None, 
                      help="Output prefix")

  args = parser.parse_args()

  if len(sys.argv)<2 : 
    parser.print_help()
    raise SystemExit

  input_tuple = args.input
  input_tree = args.intree
  input_branches = args.branches.split(":") + [args.pidgen, args.piddata, args.weight]

  output_tuple = args.output

  sample_name = args.sample
  dataset_name = args.dataset
  variable_name = args.variable

  config = get_samples()[sample_name][dataset_name]
  variable = get_variables()[variable_name]

  print(config)
  print(variable)

  f = uproot.open(input_tuple)
  t = f[input_tree]
  branches = t.keys()
  print (f"branches: {branches}")
  input_data = read_array_filtered(t, input_branches, selection = "pidstat>10", sel_branches = ["pidstat"])
  print (f"input_data shape: {input_data.shape}")

  transform_forward = lambda x: 1.-(1.-x)**0.2

  pidgen_tr = transform_forward(input_data[:,-3])
  piddata_tr = transform_forward(input_data[:,-2])
  sw = input_data[:,-1]
  
  print(sw)

  label = variable_name

  set_lhcb_style(size = 12)

  with plot("", args.output) as (fig, ax) : 
    plot_distr1d_comparison(piddata_tr, pidgen_tr, bins = 100, range = variable["data_range"], ax = ax, 
       label = "Transformed PID", 
       weights = sw, data_weights = sw, 
       title = "Transformed PID", log = False, pull = True, 
       legend = ["Original distribution", "Resampled distribution"], 
       data_alpha = 0.5)

  plt.show()

if __name__ == "__main__" : 
  main()
