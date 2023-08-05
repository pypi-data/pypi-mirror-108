variable = {
    "branch" : "probe_MC12TuneV3_ProbNNpi", 
    "data_range" : (0., 1.), 
    "transform_forward" : lambda x : 1.-(1.-x**0.25)**0.5, 
    "transform_backward" : lambda x : (1.-(1.-x)**2)**4, 
    "normalise_bins" : 1000, 
    "normalise_method" : "gauss", 
    "normalise_range" : (-2.5, 2.5), 
    "template_bins" : 200, 
    "template_sigma" : 2., 
    "resample_bins" : 200, 
}
