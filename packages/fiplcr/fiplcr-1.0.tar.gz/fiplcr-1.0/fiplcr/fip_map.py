import numpy as np
from astropy import constants as const
from astropy import units as u
import matplotlib.pyplot as plt

import matplotlib as mlt
import matplotlib.pyplot as plt
mlt.rc('xtick', labelsize=18)
mlt.rc('ytick', labelsize=18)
plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{mathrsfs}')

from fiplcr.config import density_array

def find_dens_idx(densn):
    '''
    This function finds the index of the closest to a density value
    in the density_array with which we compute the contribution 
    functions.
    We will use the vectorized version of this function in order to
    derive a relative FIP bias map using the observations provided
    bu the user. This density value will correspond to each of the
    values in the density map provided by the usor and the density 
    map should come from the same observations one wants to use to
    compute a relative FIP bias map.
    The density_array is defined in config.py in the fiplcr module.
    densn : float, density of a pixel in cm**-3
    '''
    if np.isnan(densn):
        return -1
    else:
        return np.argmin(abs(density_array.value - densn))

# Vectorized version of the find_dens_idx function
# Should be applied to a density map retrieved from observations and
# that has the same shape as the int_map for every ion in ll.ionsLF
# and ll.ionsHF. 
vfinddens = np.vectorize(find_dens_idx)

def coeff_for_dens(ll, idx_dens_map):
    '''
    Defines a coeff_map of the same shape of the int_map for 
    every ion in ll.ionsLF and ll.ionsHF. It relates a coefficient
    that relates pixel by pixel to the density map calculated when 
    reading the simulation data. In this manner, in each pixel we
    apply a density-dependent LCR FIP bias diagnostic.
    ll           : LinearComb object, as defined in the 
                   fiplcr.linear_combination module
    idx_dens_map : array, same shape as the int_map for every ion,
                   map of indexes of the closest density in the
                   density_array (defined in config.py, used to 
                   compute contribution functions) to the density 
                   values of the density map (provided by the user).
                   Obtained through the command
                   vfinddens((density_map.to(u.cm**-3)).value)
    '''
    # We will define a coefficient 2D array for every ion in each
    # of the ion lists (ll.ions LF and ll.ionsHF)
    for i in range(len(ll.ionsLF)):
        # Defining the shape of the coeff_map
        nx, ny = ll.ionsLF[i].int_map.shape
        # New attribute to the ion object ll.ionsLF[i]
        ll.ionsLF[i].coeff_map = np.zeros((nx,ny))
        for j in range(nx):
            for k in range(ny):
                # What to do when there is a np.nan in this pixel of
                # the density map provided by the user
                if idx_dens_map[j,k] == -1 :
                    ll.ionsLF[i].coeff_map[j,k] = np.nan
                # If a density value is defined, we withdraw the 
                # coefficient optimized for this specific line and for
                # this density value
                else:
                    ll.ionsLF[i].coeff_map[j,k] = ll.xLF[idx_dens_map[j,k], i]
    for i in range(len(ll.ionsHF)):
        ll.ionsHF[i].coeff_map = np.zeros(ll.ionsHF[i].int_map.shape)
        for j in range(nx):
            for k in range(ny):
                # What to do when there is a np.nan in this pixel of
                # the density map provided by the user
                if idx_dens_map[j,k] == -1 :
                    ll.ionsHF[i].coeff_map[j,k] = np.nan
                # If a density value is defined, we withdraw the 
                # coefficient optimized for this specific line and for
                # this density value
                else:
                    ll.ionsHF[i].coeff_map[j,k] = ll.xHF[idx_dens_map[j,k], i]

def calculate_FIP_map(ll):
    '''
    Calculates the FIP bias map for a LinearComb object. Must have 
    applied all previous functions before applying this one.
    ll : LinearComb object, as defined in the fiplcr.linear_combination
         module
    '''
    # Defining new attributes FIP_map which will contain the relative FIP
    # bias map; lc_LF which will contain the linear combination of spectral
    # line's intensities of the set of lines from low FIP elements and lc_HF
    # which is the same quantity but for the set of lines from high FIP elements.
    ll.FIP_map = np.zeros(ll.ionsLF[0].int_map.shape)
    ll.lc_LF = np.zeros(ll.ionsLF[0].int_map.shape) * ll.ionsLF[0].int_map.unit
    ll.lc_HF = np.zeros(ll.ionsLF[0].int_map.shape) * ll.ionsLF[0].int_map.unit

    # Computation of lc_LF
    for i in range(len(ll.ionsLF)):
        ll.lc_LF += ll.ionsLF[i].coeff_map / ll.ionsLF[i].ph_abund * ll.ionsLF[i].int_map
    # Computation of lc_HF
    for i in range(len(ll.ionsHF)):
        ll.lc_HF += ll.ionsHF[i].coeff_map / ll.ionsHF[i].ph_abund * ll.ionsHF[i].int_map
    # The relative FIP bias map is then simply the ratio of these two quantities
    ll.FIP_map = ll.lc_LF / ll.lc_HF

def plot_FIP_map(FIP_map):
    """
    Plotting function.

    Parameters
    ----------
    FIP_map  : numpy array, contains a FIP bias map
    extent   : tuple, contains (left x value, right x value, bottom y value, top y value)
    """
    plt.imshow(FIP_map.si.value, origin='lower', vmin=0, vmax=3)
    plt.colorbar()
    plt.show()


def fip_map(ll, density_map):
    '''
    This function allows the user to plot a FIP bias map from two linear combinations 
    of 2D integrated intensity maps of spectral lines, one of lines of low FIP elements 
    and another one of lines of high FIP elements. The result is a 2D numpy array 
    containing the resulting FIP bias map.

    Parameters
    ----------
    ll          : LinearComb object, as defined in the fiplcr.linear_combination module
    density_map : numply array of quantity, defines either a constant density to be used throughout 
                  all calculations or a density map, it has to be of the same shape as 
                  all radiance maps and we will use the best linear combination for the 
                  density value in each pixel. Should be in cm**-3
    '''

    idx_dens_map = vfinddens((density_map.to(u.cm**-3)).value)
    coeff_for_dens(ll, idx_dens_map)
    calculate_FIP_map(ll)
    plot_FIP_map(ll.FIP_map)