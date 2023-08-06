import numpy as np
import matplotlib as mtp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd
from sklearn.metrics import r2_score
import scipy as sc
import numpy as np
import random
import pandas as pd
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
from scipy.integrate import solve_ivp
from scipy.optimize import minimize, leastsq
import requests
import matplotlib.pyplot as plt
from scipy.misc import electrocardiogram
from scipy.signal import find_peaks

def gaussian(x, height, center, width):
    return height*np.exp(-(x - center)**2/(2*width**2)) 

def n_gaussians(x, h1, c1, w1, h2, c2, w2, h3, c3, w3,h4,c4,w4,h5,c5,w5, offset):
    return (gaussian(x, h1, c1, w1) +
            gaussian(x, h2, c2, w2) +
            gaussian(x, h3, c3, w3) + 
            gaussian(x, h4, c4, w4) + 
            gaussian(x, h5, c5, w5) + offset
            #+ 
            #offset=0 
           )	
def optim(data,params):
    op_params=sc.optimize.curve_fit (n_gaussians, np.linspace(0, data.shape[0]-1, data.shape[0]), data["I"],p0=params,bounds=(0,np.inf))
    return op_params   

def mwave(data,Gaussianln):
    Y1=n_gaussians(np.linspace(0, data.shape[0]-1, data.shape[0]), *Gaussianln)
    return Y1
	