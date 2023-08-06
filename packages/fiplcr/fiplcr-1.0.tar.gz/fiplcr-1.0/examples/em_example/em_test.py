# -*- coding: utf-8 -*-

from astropy import units as u
import numpy as np
import scipy.optimize as op
import scipy.io as sio
from scipy.interpolate import interp1d

import matplotlib as mlt
import matplotlib.pyplot as plt
mlt.rc('xtick', labelsize=18)
mlt.rc('ytick', labelsize=18)
plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{mathrsfs}\usepackage{txfonts}')
import matplotlib.colors as colors

from fiplcr.specline import Line
from fiplcr.linear_combination.linear_comb import LinearComb as lc

em_lines = [Line(ionid,wvl) for (ionid,wvl) in [('s_10',264.2306), ('si_10',258.374), ('si_10',261.056), \
    ('fe_12',195.119),('fe_13',201.126), ('fe_13',202.044), ('fe_14',264.7889), ('fe_14',274.2037)]]

# File containing emission measure data and the temperature array 
# with which the tests will be performed
em_filename_ar = './em_example.npz'

def load_file(filename, L):
    '''
    Reads an .npz file containing an Emissions Measure cube and its corresponding
    temperature cube. We will adapt said Emission Measure to temperature array used
    to compute the contribution functions of the lines we want to do the diagnostic 
    with. If both temperature arrays do not match, the returned EM will be 
    interpolated so that they do.

    Returns :
    ---------
    em      : quantity array, cube of the emission measure. Its unit is cm**-5.
    em_temp : quantity array, should match the temperature array of L, in K.

    Parameters :
    ------------
    filename : str, name of the file containing the EM cube
    L        : LinearComb object, as defined in the linear_comb module.
    '''
    print('Loading EM')
    em_file = np.load(filename, allow_pickle=True)
    em = np.array(em_file['em'], dtype=float)
    em_temp =  em_file['em_temp']
    # If the temperature arrays do not match, we will interpolate the EM
    if em_temp != L.temperature:
        f = interp1d(em_temp, em, axis=0, kind='cubic', fill_value="extrapolate")
        new_em = f(L.temperature.value) * np.array(em_file['em_factor'], dtype = float) * u.cm**-5
        return new_em, L.temperature
    else:
        em = em * np.array(em_file['em_factor'], dtype = float) * u.cm**-5
        return em, em_temp * u.K

def rad_lc(em, coeffs, speclines, idens, abundance='cr', method='linear_combination'):
    '''
    Radiance of a linear combination of spectral lines calculated for a given em cube,
    a given set of spectral lines, at a certain density, with either coronal or 
    photospheric abundances and using either the LCR or the 2LR methods.

    Returns :
    ---------
    cl : quantity array, linear combination of the radiances
    
    Parameters :
    ------------
    em        : float array, emission measure
    coeffs    : float array, coefficients of the linear combination
    speclines : Specline list,  list of some elements' spectral lines as defined in
                specline module
    idens     : int, index on the density array used to calculate the speclines of the 
                density value one wishes to use
    abundance : str, either 'cr' for coronal abundance or 'ph' for photospheric
    method    : str, either 'linear_combination' to use the LCR method or 'line_ratio'
                to use the 2LR method
    
    '''
    cl = 0.0
    for i in range(0, len(speclines)):
        if method=='linear_combination':
            if abundance == 'cr':
                cl += coeffs[idens, i]*speclines[i].abund*np.sum(speclines[i].cofnt[idens]*em)
            elif abundance == 'ph':
                cl += coeffs[idens, i]*speclines[i].ph_abund*np.sum(speclines[i].cofnt[idens]*em)
            else:
                raise ValueError("abundance must be 'cr' for coronal or 'ph' for photospheric")
        if method=='line_ratio':
            if abundance == 'cr':
                cl += coeffs[i]*speclines[i].abund*np.sum(speclines[i].cofnt[idens]*em)
            elif abundance == 'ph':
                cl += coeffs[i]*speclines[i].ph_abund*np.sum(speclines[i].cofnt[idens]*em)
            else:
                raise ValueError("abundance must be 'cr' for coronal or 'ph' for photospheric")
    return cl

def calculate_radiances_from_em(ll, em, idens, method):
    if method == 'linear_combination':
        coeffs_LF = ll.xLF
        coeffs_HF = ll.xHF
    elif method == 'line_ratio':
        coeffs_LF = [1/ll.ionsLF[0].cofnt[idens].value.max()]
        coeffs_HF = [1/ll.ionsHF[0].cofnt[idens].value.max()]
    else: 
        ValueError("method must be 'linear_combination' or 'line_ratio'")
    print('Calculating coronal HF radiance')
    ll.radHFcr = np.apply_along_axis(rad_lc, 0, em, coeffs_HF, ll.ionsHF, idens, abundance='cr', method=method)
    print('Calculating coronal LF radiance')
    ll.radLFcr = np.apply_along_axis(rad_lc, 0, em, coeffs_LF, ll.ionsLF, idens, abundance='cr', method=method)
    print('Calculating photospheric HF radiance')
    ll.radHFph = np.apply_along_axis(rad_lc, 0, em, coeffs_HF, ll.ionsHF, idens, abundance='ph', method=method)
    print('Calculating photospheric LF radiance')
    ll.radLFph = np.apply_along_axis(rad_lc, 0, em, coeffs_LF, ll.ionsLF, idens, abundance='ph', method=method)

def int_over_ph_abund(em, coeffs, speclines, idens, method):
    cl = 0.0 * speclines[0].cofnt[idens].unit * em.unit
    for i in range(0, len(speclines)):
        if method == 'linear_combination':
            cl += coeffs[idens,i]*(speclines[i].abund/speclines[i].ph_abund)*np.sum(speclines[i].cofnt[idens]*em)
        else:
            cl += coeffs[i]*(speclines[i].abund/speclines[i].ph_abund)*np.sum(speclines[i].cofnt[idens]*em)
    return cl

def FIP_from_em(ll, em, idens, method, plot_bool=True):
    if method == 'linear_combination':
        coeffs_LF = ll.xLF
        coeffs_HF = ll.xHF
    elif method == 'line_ratio':
        coeffs_LF = [1/ll.ionsLF[0].cofnt[idens].value.max()]
        coeffs_HF = [1/ll.ionsHF[0].cofnt[idens].value.max()]
    ll.integrated_int_LF_em = np.apply_along_axis(int_over_ph_abund, 0, em, coeffs_LF, ll.ionsLF, idens, method)
    ll.integrated_int_HF_em = np.apply_along_axis(int_over_ph_abund, 0, em, coeffs_HF, ll.ionsHF, idens, method)
    ll.FIP_from_em = ll.integrated_int_LF_em / ll.integrated_int_HF_em
    if plot_bool:
        plot_FIP(ll)

def plot_CHIANTI_ems(L):
    plt.clf()
    color = cb.fccolorblind(3)
    j=0
    for region in regions:
        plt.plot(np.log10(L.temperature.value), np.log10(L.ionsHF[0].regions[region]['em'].value), color=color[j], lw=3, label='{} {}'.format(region.split('_')[0], region.split('_')[1]))
        plt.xlabel('log(Temperature), T in K', fontsize=30)
        plt.ylabel('log(EM (T))', fontsize=30)
        plt.legend(fontsize=30)
        j+=1    
    # plt.show()

def plot_FIP(L, vmin=0.75, vmax=2.25, cmap='magma'):
    plt.clf()
    mlt.rc('xtick', labelsize=22)
    mlt.rc('ytick', labelsize=22)
    fip2 = L.FIP_from_em.value
    fip2_hist = L.FIP_from_em.value[~np.isnan(L.FIP_from_em.value)]
    relative_FIP_bias = (L.ionsLF[0].abund/ L.ionsLF[0].ph_abund)/(L.ionsHF[0].abund/ L.ionsHF[0].ph_abund)
    cm = plt.get_cmap(cmap)
    f,(ax2,ax4) = plt.subplots(2,1)
    f.set_size_inches(5, 10.5)
    f.set_tight_layout(True)
    p2 = ax2.imshow(fip2, origin='lower', vmin=vmin, vmax=vmax, cmap=cm)
    ax2.set_title('FIP bias map', fontsize=24)
    ax2.set_xlabel('X pixel', fontsize=24)
    ax2.set_ylabel('Y pixel', fontsize=24)
    # histogram bins
    bins = np.linspace(vmin, vmax, num=51)
    binc = (bins[:-1] + bins[1:]) / 2  # center
    binw = bins[1:] - bins[:-1]        # width
    h, b = np.histogram(fip2_hist, bins)
    ax4.bar(bins[:-1], h, align='edge', width=binw, color=cm(p2.norm(binc)))
    ax4.set_xlabel('FIP bias', fontsize=24)
    ax4.set_ylabel('N', fontsize=24)
    ax4.axvline(x=relative_FIP_bias, label='relative FIP bias',color='black')
    ax4.legend(fontsize=22)
    # f.show()
    # f.savefig('histo.pdf',dpi=250)

def em_test(lines=[], log_dens=8.3, em_filename=em_filename_ar, method='linear_combination', plot_bool=False, verbose=False, using_S_as_LF=False):
    '''
    Parameters
    lines : can be either a list of Line objects as defined in the 
    specline module or a LinearComb object as defined in the 
    linear_comb module.
    '''

    if isinstance(lines, list):
        if len(lines)==0:
            L = lc(lines=em_lines, verbose=verbose, using_S_as_LF=using_S_as_LF)
            L.compute_linear_combinations()
        else:
            L = lc(lines=lines, verbose=verbose, using_S_as_LF=using_S_as_LF)
            L.compute_linear_combinations()
    elif isinstance(lines, lc):
        if hasattr(lines, 'xLF'):
            L = lines
        else:
            lines.compute_linear_combinations()
            L = lines
    else:
        raise ValueError("Lines is neither a list of Lines nor a LinearComb object")

    L.em, L.em_temp = load_file(em_filename, L)
    idens = np.argmin(abs(np.log10(L.density_array.value)-log_dens))
    print('Using density value : log(n) = {:.2f}'.format(np.log10(L.density_array[idens].value)))

    FIP_from_em(L, L.em, idens, method, plot_bool)

    if plot_bool:
        plot_FIP(L)
        
    print('End of testing')
    return L

if __name__ == '__main__':

    print('Performing tests with a linear combination')
    ll = em_test(plot_bool=True)
    plt.savefig('hist_LCR.pdf')
    
    print('Performing tests using only an Si X line and an S X line')
    lines_2 = [Line(ionid,wvl) for (ionid,wvl) in [('s_10',264.2306), ('si_10',258.374)]]
    ll_2_lines = em_test(lines_2, method='line_ratio', plot_bool=True)
    plt.savefig('hist_2LR.pdf')

