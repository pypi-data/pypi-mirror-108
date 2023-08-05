from datasets import converted_run1_pidcalib_datasets_dstar_k as ds_run1
from datasets import legacy_run2_pidcalib_datasets as ds_run2

from itertools import product

common_params = {
    "calib_cache_branches" : ["pt", "eta", "ntr", "sw"], 
    "calib_cache_filename" : "calib_cache.root", 
    "data_ranges" : [ (2.4, 4.4), (2.0, 5.0), (0.7, 3.1) ], 
    "max_weights" : None, 
    "normalise_bins" : [100, 100, 100], 
    "normalise_methods" : ["scale", "scale", "flatten"], 
    "normalise_ranges" : 2*[ (0., 1.) ] + [ (0., 1.) ], 
    "template_bins" : [100, 100, 50], 
    "template_sigma" : [2., 4., 4.], 
}

#"normalise_methods" : ["flatten", "flatten", "flatten"], 
#"normalise_ranges" : 3*[ (0., 1.) ], 
#"normalise_methods" : ["gauss", "gauss", "flatten"], 
#"normalise_ranges" : 2*[ (-2.5, 2.5) ] + [ (0., 1.) ], 

sample_run2 = {
  f"{pol}_{year}" : { 
    "sample" : ds_run2[f"{pol}_{year}"], 
    "branches" : [ 
      "probe_Brunel_PT", 
      "probe_Brunel_ETA", 
      "nTracks_Brunel" if year in ["2017", "2018"] else "nTracks", 
      "probe_sWeight" 
    ], 
    "trees" : ['DSt_KPTuple/DecayTree', 'DSt_KMTuple/DecayTree'], 
    **common_params, 
  } 
  for pol in ["MagUp", "MagDown"] for year in ["2015", "2016", "2017", "2018"]
}

sample_run1 = {
  f"{pol}_{year}" : { 
    "sample" : ds_run1[f"{pol}_{year}"], 
    "branches" : [ 
      "probe_PT", 
      "probe_ETA", 
      "nTracks", 
      "probe_sWeight" 
    ], 
    "trees" : ['DecayTree'], 
    **common_params, 
  } 
  for pol in ["MagUp", "MagDown"] for year in ["2011", "2012"]
}

sample = {**sample_run1, **sample_run2}

