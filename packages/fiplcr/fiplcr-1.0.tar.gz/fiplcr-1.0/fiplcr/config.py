# -*- coding: utf-8 -*-

import os

import numpy as np
from astropy import units as u

############################################################################

# VARIABLES USED IN FIPLCR AND ITS SUBMODULES

# --------------------------------------------------------------------------
# Path to the CHIANTI database (read from environment variable $XUVTOP)
xuvtop = os.environ.get('XUVTOP', '/usr/local/ssw/packages/chianti/dbase')

# --------------------------------------------------------------------------

############################################################################

# VARIABLES USED IN SPECLINE MODULE 

# --------------------------------------------------------------------------
# Path to the directory where you wish to create or where already exist two 
# folders: one containing the contribution function calculations and another
# containing the plots of the different contribution functions.
directory = '.'

# Temperature array with which the calculations of the contribution 
# functions will be performed

temperature_array = 10. ** np.arange (4.5, 7.55, 0.05) * u.K

# Density array with which the calculations of the contribution functions 
# will be performed.
# Optimal coefficients for the linear combinations will be found for each
# density value in this array.
density_array = 10. ** np.arange (7, 11.1, 0.1) / u.cm**3

# Abundance files from which we will retrieve the coronal and the 
# photospheric abundances of the used elements. 
# They should be stored in your local chianti database folders.
abundname = 'sun_coronal_2012_schmelz_ext'
# abund_ph_name = 'sun_photospheric_2009_asplund'
abund_ph_name = 'sun_photospheric_2007_grevesse'

# Different Solar regions for which we want to calculate typical radiances
# for each line. They are necessary to find an optimal linear combination 
# of spectral lines.
regions = ['quiet_sun', 'active_region', 'coronal_hole']

# --------------------------------------------------------------------------

############################################################################

# VARIABLES USED IN LINEAR COMBINATION MODULE 

# --------------------------------------------------------------------------

# A float determining the minimum number of photons that we accept for a 
# spectral line to be included in our calculations
# NOT fully functionnal yet !!
threshold = 5.0
