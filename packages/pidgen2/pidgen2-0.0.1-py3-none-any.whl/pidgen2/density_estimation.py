from jax import numpy as np
from jax import jit, lax
import numpy as onp
import functools
import scipy
from scipy.interpolate import RegularGridInterpolator

def filter(data, ranges) : 
  cond = functools.reduce(np.logical_and, [ np.logical_and(data[:,i]>ranges[i][0], data[:,i]<ranges[i][1] ) for i in range(data.shape[1]) ] )
  return data[cond]

def create_normaliser(data, ranges, bins, weights = None) : 
  norm = []
  for i in range(data.shape[1]) : 
    counts, edges = onp.histogram(data[:,i], bins = bins[i], range = ranges[i], weights = weights)
    cum_values = np.concatenate( ( np.array([0.]), np.cumsum(counts*np.diff(edges)) ) )
    cum_values /= cum_values[-1]
    norm += [ (cum_values, edges) ]
  return norm

def create_histograms(data, ranges, bins, weights = None) : 
  norm = []
  for i in range(data.shape[1]) : 
    counts, edges = onp.histogram(data[:,i], bins = bins[i], range = ranges[i], weights = weights)
    norm += [ (counts, edges) ]
  return norm

def reweight(data, norm, max_weights) : 
  weights = np.ones_like(data[:,0])
  for i in range(data.shape[1]) :
    counts, edges = norm[i]
    weights = weights/np.maximum(onp.interp(data[:,i], 0.5*(edges[1:]+edges[:-1]), counts, left = 1., right = 1.)/\
                                   np.amax(counts), 1./max_weights[i])
  return weights

def normalise(data, norm, methods) :
  norm_data = []
  for i in range(data.shape[1]) :
    cum_values, edges = norm[i]
    #dx = edges[1]-edges[0]
    if methods[i] == "flatten" : 
      norm_data += [ onp.interp(data[:,i], edges, cum_values, left = 0., right = 1.) ]
    elif methods[i] == "gauss" : 
      flat = onp.interp(data[:,i], edges, cum_values, left = 0., right = 1.)
      norm_data += [ scipy.special.erfinv( flat*2. - 1. ) ]
    elif methods[i] == "scale" : 
      left = edges[0]
      right = edges[-1]
      norm_data += [ (data[:,i]-left)/(right-left) ]
  return np.stack(norm_data, axis = 1)

def unnormalise(data, norm, methods) : 
  denorm_data = []
  for i in range(data.shape[1]) :
    cum_values, edges = norm[i]
    #dx = edges[1]-edges[0]
    if methods[i] == "flatten" : 
      denorm_data += [ onp.interp(data[:,i], cum_values, edges, left = edges[0], right = edges[-1]) ]
    elif methods[i] == "gauss" : 
      flat = 0.5*(scipy.special.erf( data[:,i] ) + 1.)
      denorm_data += [ onp.interp(flat, cum_values, edges, left = edges[0], right = edges[-1]) ]
    elif methods[i] == "scale" : 
      left = edges[0]
      right = edges[-1]
      norm_data += [ data[:,i]*(right-left)+left ]
  return np.stack(denorm_data, axis = 1)

def resample(counts, edges, data, rnd, range = (-2.5, 2.5), bins = 100) : 
  centres = [ 0.5*(e[:-1]+e[1:]) for e in edges ]
  interp_func = RegularGridInterpolator(centres, counts, bounds_error = False, fill_value = 0.)
  out = []
  for i in np.linspace(range[0], range[1], bins) : 
    arr = np.concatenate([ i*np.ones_like(data[:,0:1]), data], axis = 1)
    out += [ interp_func(arr) ]
  hist = np.stack(out, axis = 1)
  histsum = np.sum(hist, axis = 1, keepdims = True)
  cumsum = np.cumsum(hist, axis = 1)/histsum
  diff = cumsum - rnd[..., np.newaxis]
  ind = np.maximum(1, np.argmax(diff>0., axis = 1)[..., np.newaxis])
  val2 = np.take_along_axis(diff, ind, axis = 1)
  val1 = np.take_along_axis(diff, ind-1, axis = 1)
  return (ind-val2/(val2-val1))/float(bins-1)*(range[1]-range[0]) + range[0], histsum
