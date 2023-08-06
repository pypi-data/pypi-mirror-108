# -*- coding: utf-8 -*-

from astropy import units as u
import numpy as np
import scipy.optimize as op
import scipy.io as sio

import matplotlib as mlt
import matplotlib.pyplot as plt
mlt.rc('xtick', labelsize=18)
mlt.rc('ytick', labelsize=18)
plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{mathrsfs}\usepackage{txfonts}')

from fiplcr.specline import SpecLine
from fiplcr.specline import Line

from fiplcr.config import threshold, regions, density_array
# From config, we will use variables 
# - threshold     : float, minimum number of photons that we accept for a 
#                   spectral line to be included in our calculations
# - regions       : list of strings, different solar regions which we 
#                   calculate typical radiances
# - density_array : array of quantities, density array with which the 
#                   calculations of the contribution functions will be
#                   performed and for which the linear combination 
#                   coefficients will be optimized.


def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)

def vector_objective_function(coeffs, HF, LF, idens):
    ''' 
    Parameters :
    ------------
    coeffs : float array
              coefficients of the linear combination
    HF     : array of SpecLine objects
              array of high FIP elements' spectral lines as defined in
              specline module, each spectral line has the attribute
              normed_cofnt which is the contribution function normalized
              to the median of the maximums of all considerd spectral
              lines
    LF     : array of SpecLine objects
              array of low FIP elements' spectral lines as defined in
              specline module, each spectral line has the attribute
              normed_cofnt which is the contribution function normalized
              to the median of the maximums of all considerd spectral
              lines
    '''

    cl_LF_integrated = np.zeros((len(regions)))
    cl_HF_integrated = np.zeros((len(regions)))

    j = 0
    for region in regions:
        # We sum over the different high FIP spectral lines
        for i in range(0, len(HF)):
            # Coefficient times the scalar product of the normalized contribution function
            # of the spectral lines and the emission measure of a certain region 
            cl_HF_integrated[j] += np.sum(coeffs[i]*HF[i].normed_cofnt[idens] * HF[i].regions[region]['em'].value)

        # We sum over the different high FIP spectral lines
        for i in range(0, len(LF)):
            # Coefficient times the scalar product of the normalized contribution function
            # of the spectral lines and the emission measure of a certain region 
            cl_LF_integrated[j] += np.sum(coeffs[i+len(HF)]*LF[i].normed_cofnt[idens] * LF[i].regions[region]['em'].value)
        j += 1
    # ratio of our pseudo intensities (they contain no abundances)
    return cl_LF_integrated / cl_HF_integrated

def objective_function(coeffs, HF, LF, idens):
    ''' 
    This is the function used to optimize our linear combinations. 

    In the module config.py, a list of regions of interest is stated.
    This function creates two vectors of the size of this list, one for
    the low FIP elements and one for the high FIP elements. Each element
    of the vector is the integrated intensity of a linear combination of
    spectral lines for each chosen region. So let's say we want to
    optimize our linear combination for active regions, quiet sun and 
    coronal holes. The element of the low FIP vector correspondig to the
    active region would contain the sum all the spectral lines of a 
    coefficient (that will be optimized) times the scalar product of the 
    contribution function of the spectral line at the density defined in 
    config.py and the typical emission measure for an active region. The 
    second element of the vector would contain this same integrated
    intensity for the linear combination of low FIP spectral lines but
    using a typical EM for quiet sun, and the third would be the exact 
    same except with a coronal hole EM. For high FIP elements we would 
    have the same three elements.

    We then create a new vector which the element by element ratio of 
    the previous two (so the ratio of the "intensities" for the low FIP
    linear combination and the high FIP linear combination).
    Our objective function is the distance between this vector and a 
    vector of the same size containing only ones.

    The coefficients defining our linear combinations of high FIP and 
    low FIP spectral lines will be adjusted by the minimize function in 
    order for our intensity ratios to be as close as possible to one. 
    It is the norm used as a target function for the minimize 
    function using the Nelder-Mead method. This optimization is made in 
    the self.optimize function of the LinearComb class.
    
    Parameters :
    ------------
    coeffs : float array
              coefficients of the linear combination
    HF     : array of SpecLine objects
              array of high FIP elements' spectral lines as defined in
              specline module, each spectral line has the attribute
              normed_cofnt which is the contribution function normalized
              to the median of the maximums of all considerd spectral
              lines
    LF     : array of SpecLine objects
              array of low FIP elements' spectral lines as defined in
              specline module, each spectral line has the attribute
              normed_cofnt which is the contribution function normalized
              to the median of the maximums of all considerd spectral
              lines
    '''
    
    ratio_of_cl = vector_objective_function(coeffs, HF, LF, idens)
    # Distance between these ratios and a vector of ones that has the same shape as cl
    return np.sqrt(np.sum((ratio_of_cl - np.ones_like(ratio_of_cl))**2))

class LinearComb:

    def __init__(self, lines, verbose=False, plot_bool=False, using_S_as_LF=False):
        '''
        Linear Combination object : 

        Parameters
        ----------
        lines   : list of Line objects, as defined in the specline module. This list contains 
                  all spectral lines we wish to use for the linear combinations. 
                  Line :  Line object, defines a spectral line unambigiously by ion and 
                          wavelength.
                          Example of initialization:
                          mg8_180.5 = Line('mg_8', 180.5)
                          'mg_8' is the ionid which is a string defining the element and the 
                                ionization number
                          180.5 is a float defining the wavelength of the spectral line in 
                                units of angstroms.

        Keyword Parameters
        ------------------        
        dens    : float
            Density at which we want to do the calculations in cm-3.
            Defined in config.py
        verbose : bool
            If True (default), information about the calculation process will be displayed
        
        !!! IMPORTANT !!!

        IF you want to optimize linear combinations for an OBSERVATION, every Line object MUST
        HAVE the ATTRIBUTE rad_to_phot. This factor corresponds to the quantity by which one 
        has to multiply a radiance to obtain a number of photons and it is specific to the
        instrument you wish to use. It should be defined as an astropy quantity and must have 
        a unit equivalent to sr * s**3 kg**-1.
        Spectral lines that have less photons than a certain threshold (variable defined in 
        config.py) will be excluded of this optimization.

        If the Line objects do not have this attribute, all lines will be taken into account 
        for the optimization.

        Examples for 'lines' when we want to include them all (so not an observation):
        ne_et_mg = [Line('ne_8',770.42), Line('ne_8', 780.3), Line('ne_6', 1005.79), Line('ne_6', 1010.29), Line('ne_6', 999.27), \
        Line('mg_9',706.02), Line('mg_9',749.54), Line('mg_8',762.65), Line('mg_8',769.38), Line('mg_8',772.31), Line('mg_8',782.34), \
        Line('mg_8',789.43)]

        To use observations, you can take a look at the example given in example.py in directory
        example/eisfit/ given with the DIAGNOSTICS module. In that example, we use Hinode/EIS 
        observations.

        Attributes :
        ------------
        
        
        
        Useful methods :
        ----------------

        '''

        # The density needs to be in cm**-3 because of how ChiantiPy works
        self.density_array = density_array.to(u.cm**-3)
        self.threshold = threshold
        self.verbose = verbose
        self.plot_bool = plot_bool
        self.using_S_as_LF = using_S_as_LF
        self.lines = lines
        if self.verbose:
            # Prints information about the lines the user wishes to use
            self.print_lines()

    def compute_linear_combinations(self):
        if isinstance(self.lines[0], SpecLine):
            self.ions = self.lines
        else:
            # For each line in lines we calculate its specline object as defined in the
            # specline module. This will add attributes to our lines such as their 
            # contribution funcctions, their coronal and photospheric abundance, typical 
            # radiances in different solar regions...
            self.calculate_speclines(self.lines)
        # If we have an observation (i.e. if the lines entered as input have the attribute
        # rad_to_phot) we will exclude lines that have less photons than a certain 
        # threshold defined in config.py
        if self.obs_bool:
            self.not_enough_photons(self.threshold)

        # After excluding noisy lines, we normalize all remaining contribution functions
        # for the optimization (definition of the attribute normed_cofnt, in this
        # normalization we take into account the photospheric abundance of each element)
        self.normalize()

        # We separate ions in two lists: all low FIP ions will go to self.ionsLF and all
        # high FIP ions will go to self.ionsHF
        self.separate_ions()

        # We optimize the coefficients of our linear combination
        self.optimize()

        # We calculate the contribution function of both linear combinations of spectral 
        # lines
        self.lincomb()
        if self.plot_bool:
            # We plot the contribution functions of both linear combinations
            self.plot_lincomb_all()
    

    def print_lines(self):
        '''
        Prints the spectral lines entered as input.
        '''
        print('The spectral lines you intend to use are :')
        for line in self.lines:
            print('ion : {} {}, wavelength : {}'.format(line.element, line.iondeg, line.wvl)) 
        print(' ')

    def calculate_speclines(self, lines):
        '''
        Calculates specline objects for each spectral line in lines.
        '''
        self.ions = []
        i = 0
        for line in lines:
            ion = SpecLine(line.ionid,line.wvl.to(u.AA).value,verbose=self.verbose)
            if i == 0:
                self.obs_bool = hasattr(line, 'rad_to_phot')
                if self.obs_bool:
                    print('Optimizing linear combinations for an observation.')
                    print('Not all lines might be taken into account.')
                else:
                    print('All lines will be taken into account')
                self.temperature = ion.temperature
            else:
                assert(hasattr(line, 'rad_to_phot')==self.obs_bool)
                assert(np.array_equal(self.temperature, ion.temperature))
            if hasattr(line, 'rad_to_phot'):
                ion.rad_to_phot = line.rad_to_phot
            i += 1
            self.ions += [ion]
        assert(len(lines) == len(self.ions))

    def not_enough_photons(self, seuil):
        '''
        If a spectral line is too noisy, the results will be less accurate.
        The threshold allows to rule out lines that are considered to have
        too few photons.
        '''
        for ion in self.ions:
            ion.typical_radiances()
            i = 0
            photons = 0.0
            for region in regions:
                photons += np.mean(ion.regions[region]['radiance']) * ion.rad_to_phot
                i += 1
            photons /= i
            if photons<seuil:
                self.ions.remove(ion)
                print('The following ion has been removed : {}'.format(ion.cute))
                print('Not enough photons !!')

    def normalize(self):
        """
        Creates an initial set of coefficients necessary to minimize
        the objective function and find the optimal coefficients.
        We normalize using the median of the maximums of all involved
        contribution functions.
        """
        print('Normalizing contribution functions')

        maxs = np.zeros((len(self.ions),len(self.density_array)))
        i = 0
        for line in self.ions:
            maxs[i] = np.amax(line.cofnt, axis=1)
            i += 1
        med = np.median(maxs, axis=0)
        i=0
        for ion in self.ions:
            ion.normed_cofnt = np.zeros(ion.cofnt.shape)
            ion.coeff = np.zeros((len(self.density_array)))
            for j in range(len(self.density_array)):
                ion.normed_cofnt[j] = ion.cofnt[j] / med[j]
                ion.coeff = med[j] / maxs[i,:]
            i+=1

    def separate_ions(self):
        '''
        This function creates two lists of speclines, one of lines that
        are produced by low FIP elements and another one by high FIP elements
        It also creates an initial list of coefficients necessary to minimize
        the objective function and find the optimal coefficients.
        '''

        # This list will contain all spectral lines from low FIP elements
        self.ionsLF = []
        # This list will contain all spectral lines from high FIP elements
        self.ionsHF = []
        # This list will contain the linear combination coefficients for 
        # both preceeding lists
        self.x0 = np.zeros((len(self.density_array), len(self.ions)), dtype='float')

        # Separating ions according to FIP value
        for ion in self.ions:
            if self.using_S_as_LF:
                if ion.FIP.value < 10.5:
                    self.ionsLF += [ion]
                else:
                    self.ionsHF += [ion]
            else:
                if ion.FIP.value < 10.0:
                    self.ionsLF += [ion]
                else:
                    self.ionsHF += [ion]

        # We will now check that there is at least one element in self.ionsLF and self.ionsHF
        if not self.ionsLF:
            raise ValueError("You haven't chosen any low FIP ions, the optimization cannot be done !")
        if not self.ionsHF:
            raise ValueError("You haven't chosen any high FIP ions, the optimization cannot be done !")

        # The following lines are necessary because of how the minimize function works
        i = 0
        for ion in self.ionsHF:
            self.x0[:,i] = ion.coeff
            i += 1
        for ion in self.ionsLF:
            self.x0[:,i] = ion.coeff
            i += 1

    def optimize(self):
        '''
        This function minimizes the objective function in order to find the
        optimal coefficients for the linear combinations of the contribution
        functions of the used spectral lines.
        '''
        print('We are looking for the best linear combination of contribution functions...')
        self.result = np.zeros((len(self.density_array), len(self.ions)), dtype=float)
        self.success = []
        def objective_partial(coeffs, i):
            return objective_function(np.append([1], coeffs), self.ionsHF, self.ionsLF, i)

        for i in range(len(self.density_array)):
            result = op.minimize(objective_partial, self.x0[i][1:]/self.x0[i][0], args=(i), tol=1e-3, method='Nelder-Mead', options={'maxiter':10000, 'maxfev':10000, 'fatol':0.001})
            self.result[i] = np.append([1.], result.x)
            if self.verbose: 
                print('Log10(density) value {}: '.format(np.log10(self.density_array[i].value)))
                print(result)
                print(' ')
                print('Result of the objective function :')
                print(objective_function(self.result[i], self.ionsHF, self.ionsLF, i))
                print('Objective function vector :')
                print(vector_objective_function(self.result[i], self.ionsHF, self.ionsLF, i))
                print(' ')
                self.success.append(result.success)
        self.xHF = self.result[:, 0:len(self.ionsHF)]
        self.xLF = self.result[:, len(self.ionsHF):]

    def lincomb(self):
        '''
        This function calculates the linear combination of contribution
        functions for the low FIP spectral lines and for the high FIP
        spectral lines. They are stored as quantity arrays in the 
        variables self.lincombHF and self.lincombLF. It then plots the two
        of them in a single figure in semi-logarithmic scale.
        '''
        self.lincombHF = {}
        self.lincombLF = {}

        for region in self.ionsLF[0].regions:
            ntemp = len(self.temperature)
            ndens = len(self.density_array)
            t1 = np.zeros((ndens, ntemp)) * self.ionsHF[0].cofnt.unit * self.ionsLF[0].regions[region]['em'].unit
            t2 = np.zeros((ndens, ntemp)) * self.ionsHF[0].cofnt.unit * self.ionsLF[0].regions[region]['em'].unit

            for j in range(ndens):
                for i in range(0, len(self.ionsHF)):
                    t1[j] += self.xHF[j,i] * self.ionsHF[i].cofnt[j] * self.ionsLF[0].regions[region]['em']
                for i in range(0, len(self.ionsLF)):
                    t2[j] += self.xLF[j,i] * self.ionsLF[i].cofnt[j] * self.ionsLF[0].regions[region]['em']
            self.lincombHF[region] = t1
            self.lincombLF[region] = t2

    def plot_cofnts(self, log_dens, fontsize=25):
        '''
        Plots the contribution function of all the lines in both linear combinations at a given density.
        '''
        mlt.rc('xtick', labelsize=fontsize)
        mlt.rc('ytick', labelsize=fontsize)
        plt.rc('text', usetex=True)
        plt.rc('text.latex', preamble=r'\usepackage{mathrsfs}')
        plt.rc('text.latex', preamble=r'\usepackage{txfonts}')
        plt.clf()
        color = cb.fccolorblind(len(L.lines))

        f,  ax1 = plt.subplots(1,1)
        f.set_size_inches(11,12)
        f.set_tight_layout(True)
        
        idens = np.argmin(abs(np.log10(self.ionsLF[0].density.value) - log_dens))
        
        j = 0
        for line in self.ionsHF:
            ax1.loglog(self.temperature.value, line.cofnt[idens].value,'-', color=color[j], alpha=0.75, \
            label=r'{} {} {} $\AA$'.format(line.cute.split(' ')[0], line.cute.split(' ')[1], line.cute.split(' ')[2]), \
            zorder=10, markersize=20, lw=4)
            j += 1
        
        for line in self.ionsLF:
            ax1.loglog(self.temperature.value, line.cofnt[idens].value, color=color[j], alpha=0.75, \
                label=r'{} {} {} $\AA$'.format(line.cute.split(' ')[0], line.cute.split(' ')[1], line.cute.split(' ')[2]), \
                zorder=3, lw=4)
            j += 1
        ax1.set_xlabel(r'Temperature in {}'.format(self.ions[0].temperature.unit.to_string(format='Latex')), fontsize=fontsize)
        ax1.set_ylabel(r'C(n, T) in {}'.format(self.ions[0].cofnt.unit.to_string(format='Latex')), fontsize=fontsize)
        ax1.set_xlim([4.5*10**5, 7*10**6])
        ax1.set_ylim([10**-23,3.5*10**-20])
        f.legend()
        f.show()
        # f.savefig('cofnts.pdf',dpi=250)

    def plot_lincomb(self, idens, region):
        '''
        This function plots the obtained linear combinations of 
        contribution functions for the low FIP spectral lines 
        versus that of the high FIP spectral lines as functions 
        of the log of the temperature.
        '''
        plt.plot(np.log10(self.temperature.value), self.lincombHF[region][idens], color='blueviolet', label='High FIP')
        plt.plot(np.log10(self.temperature.value), self.lincombLF[region][idens], '.', label='Low FIP')
        plt.title('Contribution functions of our high FIP and low FIP linear combinations', fontsize = 16)
        plt.xlabel('log(T)', fontsize = 14)
        plt.ylabel('C(n={},T)'.format(self.density_array[idens]), fontsize = 14)
        plt.legend()
        plt.show()
        plt.clf()

    def plot_lincomb_all(self):
        '''
        This function plots the obtained linear combinations of 
        contribution functions for the low FIP spectral lines 
        versus that of the high FIP spectral lines as functions 
        of the log of the temperature for all densities.
        '''
        cmap = get_cmap(len(self.density_array))
        for idens in range(len(self.density_array)):
            plt.plot(np.log10(self.temperature.value), self.lincombHF[idens], '--', color=cmap(idens), label='HF, {}'.format(np.log10(self.density_array[idens].value)))
            plt.plot(np.log10(self.temperature.value), self.lincombLF[idens], '.', color=cmap(idens), label='LF, {}'.format(np.log10(self.density_array[idens].value)))
        plt.title('Contribution functions of our high FIP and low FIP linear combinations', fontsize = 16)
        plt.xlabel('log(T)', fontsize = 14)
        plt.ylabel('C(n,T)', fontsize = 14)
        plt.legend()
        plt.show()
        plt.clf()
