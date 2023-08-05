from datasets import legacy_run2_pidcalib_datasets as ds
from itertools import product

def trees(year) : 
  return [ ("Lam0" + ("LL" if year in ["2017", "2018"] else "") + \
            f"_{i}{j}Tuple/DecayTuple") for i, j in product(["", "HPT_", "VHPT_"], ["P", "Pbar"]) ]

sample = {
  f"{pol}_{year}" : { 
    "sample" : ds[f"{pol}_{year}"], 
    "branches" : [ 
      "probe_Brunel_PT", 
      "probe_Brunel_ETA", 
      "nTracks_Brunel" if year in ["2017", "2018"] else "nTracks", 
      "probe_sWeight" 
    ], 
    "trees" : trees(year), 
    "calib_cache_branches" : ["pt", "eta", "ntr", "sw"], 
    "calib_cache_filename" : "calib_cache.root", 
    "data_ranges" : [ (2.4, 4.4), (2.0, 5.0), (0.7, 3.1) ], 
    "max_weights" : (40., 1., 1.), 
    "normalise_bins" : [100, 100, 100], 
    "normalise_methods" : ["flatten", "flatten", "flatten"], 
    "normalise_ranges" : 3*[ (0., 1.) ], 
    "template_bins" : [100, 100, 50], 
    "template_sigma" : [5., 5., 5.], 
  } 
  for pol in ["MagUp", "MagDown"] for year in ["2015", "2016", "2017", "2018"]
}
