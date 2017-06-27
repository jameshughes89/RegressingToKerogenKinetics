'''
Author: James Alexander Hughes
Date: Feb 27, 2017
Version 0.1


Given the model:

H_I = H_I^0 (1-exp(-(T_max/Beta)^Theta)) + C

Where, 
H_I^0 is the initial Hydrogen Index
Beta and Theta are unknown params specific to kerogen kinetics
C is some constant (epsilon)

We allso assume that the squigly brackers are just supposed to be regular parenthesis 


This script will fit T_max to expected H_I value provided in a .csv called "data.csv" where first col is T_max and second is H_I.

'''


import csv
import numpy as np
import scipy
import scipy.optimize


def model(T_max, H_I_naught, Beta, Theta, C):
	'''
	The model we are fitting to from "Marine and Petroleum Geology" by Chen and Jiang
	
	:param T_max: Not exactly sure, but it's the indipendent var
	:param H_I_naught: initial H index
	:param Beta: Some Param #1
	:param Theta: Some Param #2
	:param C: Constant

	:returns: The Model's predicted H_I 
	'''

	return H_I_naught * (1 - np.exp(-1 * ((T_max/Beta)**Theta))) + C
	



# Load the data
data = np.array(list(csv.reader(open('data.csv','r'))))
T_max = np.array(data[1:,0]).astype(np.float)	# get's 0th col and call it T_max (skip first row as this is col header)
H_I = np.array(data[1:,1]).astype(np.float)		# same but for H_I


# This bit does the actual regression

# collection of starting areas 
#estimatedStart = [0,0,0,0]
estimatedStart = [300, 450, -100, 25]		

#estimatedStart = [200, 400, -100, 10]		
# These are from Table 1 in the paper. They all actually result in same set of params
#estimatedStart = [900, 455, -120, 20]
#estimatedStart = [506, 440, -40, 25]
#estimatedStart = [665, 439, -60, 35]
#estimatedStart = [180, 422, -42, 15]

# actual regression here
params, covMat = scipy.optimize.curve_fit(model, T_max, H_I, p0=estimatedStart)		# I had this, but dirched it# , method='trf', bounds=(np.min(T_max), np.max(T_max))

print params

# Does some plotting for sanity checking 

import matplotlib.pylab as plt

#T_max_range = np.arange(np.min(T_max), np.max(T_max), 1)	# switch this with the below line if you want only between the data points provided
T_max_range = np.arange(350, 500, 1)						# switch this with the above line if you want to make the function's line larger
H_I_naught = [model(x, params[0], params[1], params[2], params[3]) for x in T_max_range]



plt.scatter(T_max, H_I)
plt.plot(T_max_range, H_I_naught, color='g', label='Model')
plt.xlabel('T_max')
plt.ylabel('H')



H_I_naught_no_c = [model(x, params[0], params[1], params[2], 0) for x in T_max_range]
plt.plot(T_max_range, H_I_naught_no_c, color='r', label='Model With no Constant (C)')

H_I_naught_high_HI = [model(x, 400, params[1], params[2], params[3]) for x in T_max_range]
plt.plot(T_max_range, H_I_naught_high_HI, color='c', label='Model With Higher H_I^0 (400)')

H_I_naught_low_HI = [model(x, 300, params[1], params[2], params[3]) for x in T_max_range]
plt.plot(T_max_range, H_I_naught_low_HI, color='k', label='Model With Lower H_I^0 (300)')

plt.legend(fontsize=8)
plt.show()

