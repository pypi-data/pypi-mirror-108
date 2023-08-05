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

from plotting import plot_distr2d, plot_distr1d, set_lhcb_style, plot_hist2d
from tuples import read_array_filtered, write_array, read_array
import density_estimation as de

import argparse
from contextlib import contextmanager

def get_samples() :
  """
    Import all modules with calibration samples from the "samples" subdir
    and construct the dictionary of all calibration samples
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
    and construct the dictionary of all variables
  """
  import variables
  d = {}
  for i in variables.__all__ : 
    module = __import__("variables." + i)
    c = getattr(getattr(module, i), "variable")
    d[i] = c
  return d

@contextmanager
def plot(name, prefix) : 
  """
    Auxiliary function to simplify matplotlib plotting
    (using "with" statement). Opens the subplot and 
    after yielding saves the figs to .pdf and .png files
  """
  fig, ax = plt.subplots(figsize = (3.5, 2.7) )
  fig.subplots_adjust(bottom=0.18, left = 0.18, right = 0.9, top = 0.9)
  yield fig, ax
  fig.savefig(prefix + name + ".pdf")
  fig.savefig(prefix + name + ".png")

def read_calib_tuple(sample, trees, branches) : 
  datasets = []
  for i in range(sample[1]) : 
    filename = sample[0] % i
    print(f"Reading file ({i}/{sample[1]}) {filename}")
    for tree in trees : 
      try : 
        with uproot.open(filename) as f : 
          t = f[tree]
          a = [t.array(b) for b in branches]
          arr = np.stack(a, axis = 1)

#        with uproot4.open(filename + ":" + tree) as t : 
#          arr = t.arrays(branches, library = "pd")[branches].to_numpy()
#          print (arr.shape)
#          datasets += [ arr ]
      except : 
        print(f"... failed")
        continue
  return np.concatenate(datasets, axis = 0)

def calib_transform(x, variable) :
  transform_forward = variable["transform_forward"]
  arr = [ 
    transform_forward(x[:,0]), 
    np.log10(x[:,1]), 
    x[:,2], 
    np.log10(x[:,3] + onp.random.uniform(size = x.shape[0]) - 0.5 ), 
    x[:,4]
  ]
  return np.stack(arr, axis = 1)

def data_transform(x) :
  arr = [ np.log10(x[:,0]), x[:,1], np.log10(x[:,2]) ]
  return np.stack(arr, axis = 1)

def create_template(variable, config, kernels = None, use_calib_cache = True, interactive_plot = True, prefix = "") : 

  sample = config['sample']
  trees = config['trees']
  calib_branches = [variable["branch"]] + config["branches"]
  ranges = [ variable["data_range"]] + config["data_ranges"]
  calib_cache_filename = config["calib_cache_filename"]
  calib_cache_branches = ["pid"] + config["calib_cache_branches"]
  normalise_bins = [variable["normalise_bins"]] + config["normalise_bins"]
  normalise_methods = [variable["normalise_method"]] + config["normalise_methods"]
  normalise_ranges = [variable["normalise_range"]] + config["normalise_ranges"]
  template_bins = [variable["template_bins"]] + config["template_bins"]
  if kernels : 
    template_sigma = kernels
  else : 
    template_sigma = [variable["template_sigma"]] + config["template_sigma"]
  max_weights = config["max_weights"]

  if use_calib_cache : 
    with uproot4.open(calib_cache_filename + ":tree") as t : 
      raw_data = t.arrays(calib_cache_branches, library = "pd")[calib_cache_branches].to_numpy()
  else :
    raw_data = read_calib_tuple(sample, trees, calib_branches)
    print(raw_data.shape)
    write_array(calib_cache_filename, raw_data, branches = calib_cache_branches)

  print(f"Read {len(raw_data)} events")
  data = calib_transform(raw_data, variable)
  print(f"Transformed data: {data}")

  data = de.filter(data, ranges + [ (-1000., 1000.) ] )

  weights1 = data[:,-1]

  if max_weights : 
    histograms = de.create_histograms(data[:,1:-1], ranges = ranges[1:], bins = normalise_bins[1:], weights = weights1)
    weights2 = de.reweight(data[:,1:-1], histograms, max_weights = max_weights)
    weights = weights1*weights2
  else : 
    weights = weights1

  normaliser = de.create_normaliser(data[:,:-1], ranges = ranges, bins = normalise_bins, weights = weights )
  print(f"Normalizer: {normaliser}")

  norm_data = de.normalise(data[:,:-1], normaliser, normalise_methods)
  print(f"Normalized data: {norm_data}")

  #unnorm_data = de.unnormalise(norm_data, normaliser, normalise_methods)

  counts, edges = onp.histogramdd(norm_data, bins = template_bins, range = normalise_ranges, weights = weights)
  smooth_counts = gaussian_filter(counts, template_sigma)

  set_lhcb_style(size = 12, usetex = False)
  #fig, axes = plt.subplots(nrows = 7, ncols = 6, figsize = (12, 9) )

  labels = [r"PID", r"$p_T$", r"$\eta$", r"$N_{\rm tr}$"]
  names = ["pid", "pt", "eta", "ntr"]

  log = True

  for i in range(len(ranges)) : 
    with plot(f"{names[i]}_transformed", prefix) as (fig, ax) : 
      plot_distr1d(data[:,i], bins = 50, range = ranges[i], ax = ax, label = "Transformed " + labels[i], weights = weights1, title = "Transformed distribution")

  for i in range(len(ranges)) : 
    with plot(f"{names[i]}_weighted", prefix) as (fig, ax) : 
      plot_distr1d(data[:,i], bins = 50, range = ranges[i], ax = ax, label = "Weighted " + labels[i], weights = weights, title = "Weighted distribution")

  for i in range(len(ranges)) : 
    with plot(f"{names[i]}_normalised", prefix) as (fig, ax) : 
      plot_distr1d(norm_data[:,i], bins = 50, range = normalise_ranges[i], ax = ax, label = "Normalised " + labels[i], weights = weights, title = "Normalised distribution")

  for i,j in [ (0,1), (0,2), (1,2), (0,3), (1,3), (2,3) ] : 
    with plot(f"{names[i]}_{names[j]}_data_proj", prefix) as (fig, ax) : 
      plot_distr2d(norm_data[:,i], norm_data[:,j], bins = 2*[50], ranges = (normalise_ranges[i], normalise_ranges[j]), 
             fig = fig, ax = ax, labels = ("Normalised " + labels[i], "Normalised " + labels[j]), weights = weights, cmap = "jet", log = log, 
             title = "Data projection")

  bins = template_bins

  smooth_proj = {
    (0, 1) : [np.sum(smooth_counts, (2,3)), edges[0], edges[1]],
    (0, 2) : [np.sum(smooth_counts, (1,3)), edges[0], edges[2]],
    (1, 2) : [np.sum(smooth_counts, (0,3)), edges[1], edges[2]],
    (0, 3) : [np.sum(smooth_counts, (1,2)), edges[0], edges[3]],
    (1, 3) : [np.sum(smooth_counts, (0,2)), edges[1], edges[3]],
    (2, 3) : [np.sum(smooth_counts, (0,1)), edges[2], edges[3]],
  }

  n1,n2,n3,n4 = [int(n/2) for n in bins]

  data_slices = {
    (0, 1) : [counts[:,:,n3,n4], edges[0], edges[1]], 
    (0, 2) : [counts[:,n2,:,n4], edges[0], edges[2]], 
    (1, 2) : [counts[n1,:,:,n4], edges[1], edges[2]], 
    (0, 3) : [counts[:,n2,n3,:], edges[0], edges[3]], 
    (1, 3) : [counts[n1,:,n3,:], edges[1], edges[3]], 
    (2, 3) : [counts[n1,n2,:,:], edges[2], edges[3]], 
  }

  smooth_slices = {
    (0, 1) : [smooth_counts[:,:,n3,n4], edges[0], edges[1]], 
    (0, 2) : [smooth_counts[:,n2,:,n4], edges[0], edges[2]], 
    (1, 2) : [smooth_counts[n1,:,:,n4], edges[1], edges[2]], 
    (0, 3) : [smooth_counts[:,n2,n3,:], edges[0], edges[3]], 
    (1, 3) : [smooth_counts[n1,:,n3,:], edges[1], edges[3]], 
    (2, 3) : [smooth_counts[n1,n2,:,:], edges[2], edges[3]], 
  }

  for i,j in smooth_proj.keys() : 
    with plot(f"{names[i]}_{names[j]}_smooth_proj", prefix) as (fig, ax) : 
      plot_hist2d(smooth_proj[(i,j)], fig = fig, ax = ax, labels = ("Normalised " + labels[i], "Normalised " + labels[j]), log = log, cmap = "jet", 
                  title = "Smoothed projection")
    with plot(f"{names[i]}_{names[j]}_data_slice", prefix) as (fig, ax) : 
      plot_hist2d(data_slices[(i,j)], fig = fig, ax = ax, labels = ("Normalised " + labels[i], "Normalised " + labels[j]), log = log, cmap = "jet", 
                  title = "Data slice")
    with plot(f"{names[i]}_{names[j]}_smooth_slice", prefix) as (fig, ax) : 
      plot_hist2d(smooth_slices[(i,j)], fig = fig, ax = ax, labels = ("Normalised " + labels[i], "Normalised " + labels[j]), log = log, cmap = "jet", 
                  title = "Smoothed slice")

  #plt.tight_layout(pad=1., w_pad=1., h_pad=0.5)
  if interactive_plot : plt.show()

  return smooth_counts, edges, normaliser

def resample_data(data, variable, config, template, chunk_size = 50000) : 

  counts, edges, normaliser = template

  normalise_methods = [variable["normalise_method"]] + config["normalise_methods"]
  normalise_ranges = [variable["normalise_range"]] + config["normalise_ranges"]
  resample_bins = variable["resample_bins"]
  transform_backward = variable["transform_backward"]

  norm_data = de.normalise(data, normaliser[1:], normalise_methods[1:])

  print(f"norm_data = {norm_data}")

  start_index = 0
  chunk = 0
  resampled_pid_arrs = []
  pid_calib_stats = []
  stop = False
  chunks = (len(norm_data)-1)//chunk_size+1

  while not stop : 
    print(f"Resampling chunk {chunk+1}/{chunks}, index={start_index}/{len(norm_data)}")
    end_index = start_index + chunk_size
    if end_index >= len(norm_data) : 
      end_index = len(norm_data)
      stop = True

    rnd = onp.random.uniform(size = (end_index-start_index, ))
    norm_pid, stats = de.resample(counts, edges, norm_data[start_index:end_index,], 
                          rnd = rnd, range = normalise_ranges[0], 
                          bins = resample_bins)
    unnorm_pid = de.unnormalise(norm_pid, normaliser[0:1], normalise_methods)
    resampled_pid = transform_backward(unnorm_pid)

    resampled_pid_arrs += [ resampled_pid ]
    pid_calib_stats += [ stats ]

    start_index += chunk_size
    chunk += 1

  resampled_pid_arr = np.concatenate(resampled_pid_arrs, axis = 0)
  pid_calib_stat = np.concatenate(pid_calib_stats, axis = 0)
  return resampled_pid_arr, pid_calib_stat

  #output_data = np.concatenate([data[start_index:end_index,:], norm_data[start_index:end_index,:], unnorm_data[:nev,:], 
  #                              norm_pid, unnorm_pid, resampled_pid], axis = 1)
  #write_array("output.root", output_data, branches = 
  #            ["pid", "pt", "eta", "ntr", "sw", 
  #             "normpid", "normpt", "normeta", "normntr", 
  #             "unnormpid", "unnormpt", "unnormeta", "unnormntr", 
  #             "normpidgen", "pidgen", "respidgen"])

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

  use_calib_cache = args.usecache
  control_plot = args.plot
  interactive_plot = args.interactive

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

  template = create_template(variable, config, use_calib_cache, interactive_plot)

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

  data = data_transform(input_data)
  pid_arr, calib_stat = resample_data(data, variable, config, template)

  print(f"data = {data}")
  print(f"pid_arr = {pid_arr}")
  print(f"calib_stat = {calib_stat}")

  write_array(output_tuple, np.concatenate([all_data, pid_arr, calib_stat], axis = 1), 
            branches = branches + [output_branch, stat_branch] )

if __name__ == "__main__" : 
  main()
