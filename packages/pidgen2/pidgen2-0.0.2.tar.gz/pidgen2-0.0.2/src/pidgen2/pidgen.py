##############################################################################
# (c) Copyright 2021 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################

import sys
import argparse

from jax import numpy as np
import uproot3 as uproot

from tuples import write_array, read_array
from resampling import read_calib_tuple, calib_transform, data_transform, create_template, resample_data

def get_samples() :
  """
  Import all modules with calibration samples from the "samples" subdir
  and construct the dictionary of all calibration samples

  Returns: 
      Dictionary of all samples loaded from "samples/" subdirectory
  """
  import samples
  d = {}
  for i in samples.__all__ : 
    module = __import__("samples." + i)
    s = getattr(getattr(module, i), "sample")
    d[i] = s
  return d

def get_variables() : 
  """
  Import all modules with variables description from the "variables" subdir
  and construct the dictionary of all variables. 

  Returns: 
      Dictionary of all variables loaded from "variables/" subdirectory
  """
  import variables
  d = {}
  for i in variables.__all__ : 
    module = __import__("variables." + i)
    c = getattr(getattr(module, i), "variable")
    d[i] = c
  return d

def main() : 

  parser = argparse.ArgumentParser(description = "PIDGen", 
                                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)

  parser.add_argument('--seed', type=int, default = 1, 
                      help="Initial random seed")
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
  parser.add_argument('--branches', type=str, default = "pt:eta:ntr", 
                      help="Input branches for Pt,Eta,Ntracks variables in the form Pt:Eta:Ntrack")
  parser.add_argument('--pidgen', type=str, default = "pidgen", 
                      help="Resampled PID branch")
  parser.add_argument('--stat', type=str, default = "pidstat", 
                      help="PID calibration statistics branch")
  parser.add_argument('--output', type=str, default = None, 
                      help="Output ROOT file")
  parser.add_argument('--outtree', type=str, default = "tree", 
                      help="Output TTree")
  parser.add_argument('--start', type=int, default = 0, 
                      help="Start event")
  parser.add_argument('--stop', type=int, default = -1, 
                      help="Stop event")
  parser.add_argument('--usecache', default = False, action = "store_const", const = True, 
                      help='Use calibration cache')
  parser.add_argument('--plot', default = False, action = "store_const", const = True, 
                      help='Produce control plots')
  parser.add_argument('--interactive', default = False, action = "store_const", const = True, 
                      help='Show interactive control plots')
  parser.add_argument('--kernels', type=str, default = None, help='Kernel widths (e.g. --kernels="2,3,3,4")')

  args = parser.parse_args()

  if len(sys.argv)<2 : 
    parser.print_help()
    raise SystemExit

  kernels = args.kernels
  if kernels : kernels = eval(kernels)

  input_tuple = args.input
  input_tree = args.intree
  input_branches = args.branches.split(":")
  start_event = args.start
  stop_event = args.stop

  output_tuple = args.output
  output_branch = args.pidgen
  stat_branch = args.stat

  sample_name = args.sample
  dataset_name = args.dataset
  variable_name = args.variable

  config = get_samples()[sample_name][dataset_name]
  variable = get_variables()[variable_name]

  print(config)
  print(variable)

  template = create_template(variable, config, use_calib_cache = args.usecache, interactive_plots = args.interactive, control_plots = args.plot)

  f = uproot.open(input_tuple)
  t = f[input_tree]
  branches = t.keys()
  print (f"branches: {branches}")
  input_data = read_array(t, input_branches)
  if stop_event > len(input_data) : stop_event = len(input_data)
  else : input_data = input_data[start_event:stop_event]
  print (f"input_data shape: {input_data.shape}")
  all_data = read_array(t, branches)[start_event:stop_event]
  print (f"all_data shape: {all_data.shape}")

  data = data_transform(input_data, config)
  pid_arr, calib_stat = resample_data(data, config, variable, template)

  print(f"data = {data}")
  print(f"pid_arr = {pid_arr}")
  print(f"calib_stat = {calib_stat}")

  write_array(output_tuple, np.concatenate([all_data, pid_arr, calib_stat], axis = 1), 
            branches = branches + [output_branch, stat_branch] )

if __name__ == "__main__" : 
  main()
