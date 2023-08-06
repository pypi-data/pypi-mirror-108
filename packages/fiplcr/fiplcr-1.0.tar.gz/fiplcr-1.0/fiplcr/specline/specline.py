# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from astropy import units as u
import numpy as np
from scipy import interpolate
from os.path import isfile

from builtins import range
from scipy.interpolate import interp1d
import os
import warnings

from fiplcr.specline.romannumeral import RomanNumeral as romn
from fiplcr.specline.read_abund import read_abund

from fiplcr.config import directory, temperature_array, density_array, abundname, abund_ph_name, regions
# From config, we will use variables 
# - directory         : string defining where the calculated contribution functions should be stored
# - temperature_array : quantity array, temperatures used in calculations of the contribution functions
# - density_array     : quantity array, densities used in calculations of the contribution functions
# - abundname         : string, name of the coronal abundance file in the CHIANTI database used to
#                       make typical coronal radiance calculations
# - abund_ph_name     : string, name of the photospheric abundance file in the CHIANTI database 
#                       used to make FIP bias 
#                       calculations
# - regions           : list of strings, different solar regions which we calculate typical 
#                       radiances

import matplotlib as mlt
import matplotlib.pyplot as plt
mlt.rc('xtick', labelsize=18)
mlt.rc('ytick', labelsize=18)
plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{mathrsfs}')

try:
    import chianti.core as ch
    import chianti.data as chdata
    version = 'old'
    print('using chianti')
except ImportError :  
    import ChiantiPy.core as ch
    import ChiantiPy.tools.data as chdata
    # from ChiantiPy.tools import util
    version = 'new'
    print('using ChiantiPy')

def readChiantiDEM(file, temp=None, dir=None, integrate=True):

    '''
    Read CHIANTI DEM file to get emission measure in ranges of temperature.

    Parameters
    ----------
    file: string
        CHIANTI DEM file name (without directory or extension), can be 
        'active_region', 'coronal_hole', 'flare_ext', 'quiet_sun',
        'AU_Mic', 'flare', 'prominence' or 'auiet_sun_eis'.
        If variable file is not defined, default is 'active_region'.
    dir: list of strings
        Directories where DEM files are searched. Default is subdirectory
        dem/ of system CHIANTI database directory (XUVTOP system variable)
    temp: array
        Array of desired output temperatures
    integrate: bool
        If True (default), integrate over temperature bins to get EM(T)
        instead of DEM(T)
      
    Return
    ------
    t: numpy array
        Temperatures
    em: numpy array
    Emission measures

    Examples of use :
    -----------------
    No customization whatsoever, use only CHIANTI data
    t, em = readChiantiDEM() 
    Choose an array of temperatures and no integration
    temperature_array = 10. ** np.arange (4.5, 7.1, 0.1)
    em_file = 'flare'
    t, dem = readChiantiDEM(em_file, temp=temperature_array, dir='/usr/local/chianti_data',integrate=False)

    '''

    DemPath = os.environ.get('XUVTOP', '/usr/local/ssw/packages/chianti/dbase') + '/dem/'

    if dir is None: dir = [DemPath]
    elif isinstance (dir, list): pass
    else: dir = [dir]
    if file is None: file = 'active_region'

    for d in dir:
        pfile = d + file + '.dem'
        if not os.path.exists (pfile): continue

    # read DEM file
    data = []
    with open (pfile, 'r') as f:
        for l in f.readlines():
            if l.split() == ['-1']: break
            data.append ([np.float32(ll) for ll in l.split()])
    data = np.array (data)
    logt = data[:, 0]
    logdem = data[:, 1]

    if temp is not None:
        from decimal import Decimal
        logdemt = interp1d (logt, logdem, bounds_error=False, fill_value=Decimal('-Infinity'))
        logt = np.log10 (temp)
        logdem = logdemt (logt)
        if np.any (logdem == Decimal('-Infinity')):
            warnings.warn('0 in interpolated DEM: temperature probably out of range of CHIANTI DEM file')

    if integrate:
        em = np.zeros_like (logdem)
        # integrate DEM on each T interval to get EM(T) 
        for i in range (len (logt)):
            # T interval
            if i != 0: t0 = 10. ** ((logt[i-1] + logt[i]) / 2. )
            else: t0 = 10. ** (logt[i] - (logt[i+1] - logt[i]) / 2.)
            if i != len (logt) - 1: t1 = 10. ** ((logt[i] + logt[i+1]) / 2.)
            else: t1 = 10. ** (logt[i] + (logt[i] - logt[i-1]) / 2.)
            em[i] = 10. ** logdem[i] * (t1 - t0)
        return 10. ** logt * u.K, em / u.cm**5
    else:
        return 10. ** logt * u.K, 10. ** logdem / u.cm**5 / u.K

    raise RuntimeError ('DEM file not found, please check path for CHIANTI database') # DemPath

class Line:
    '''Line defined by ion and wavelength'''
    def __init__(self, ionid, wvl, abundname=abundname, abund_ph_name=abund_ph_name):
        '''
        Initialize Line object
        
        Parameters
        ----------
        ionid: string
            String identifying ion (CHIANTI format, e.g. 'fe_11')

        wvl: float
            Target wavelength (e.g. 180.401) in Angstroms

        Attributes
        ---------- 
        ionid, element, iondeg, wvl, cute
        '''

        self.ionid = ionid
        # Transformation of the ionid (e.g. 'fe_11') into two string
        # variables:
        # self.element looks like 'Fe'
        # self.iondeg is the ionization degree of the ion (e.g. '11')
        
        try:
            self.element, self.iondeg = ionid.split('_')
            self.element = self.element.capitalize()
        except ValueError:
            print("You did not define the ionid properly. For example iron 11 times ionized is identified by 'fe_12'")
            raise Exception('Ion ID Error', 'This ion does not exist in the CHIANTI database', self.ionid)
        # _temp_util_name = util.convertName(ionid)
        # self.Z = _temp_util_name['Z']
        ab = read_abund(abundname)[self.element]
        self.abund = 10.**(ab - 12.)
        ab = read_abund(abund_ph_name)[self.element]
        self.ph_abund = 10.**(ab - 12.)

        self.get_wvl(wvl)
        self.cute = '{} {} {}'.format(self.element, romn(int(self.iondeg)).roman, self.wvl)
        self.string = '{} {} {} {}'.format(self.element, romn(int(self.iondeg)).roman, self.wvl.value, self.wvl.unit.to_string('latex'))

    def __repr__(self):
        '''
        This function returns a printable representation of a Line object.
        '''
        return """ Line object for spectral line {} 
        
        Attributes : ionid, element, iondeg, wvl, cute

                   """.format(self.cute)

    def __copy__(self):
        '''
        Create a new Line object from another Line object.
        '''
        cls = self.__class__
        result = cls.__new__(cls)
        result.ionid = self.ionid
        result.element = self.element
        result.iondeg = self.iondeg
        result.wvl = self.wvl
        result.cute = self.cute
        result.string = self.string
        return result

    def get_wvl(self, wvl):
        '''
        Search for the wavelength in the Chianti database. 
        By defining spectral lines in this way, we will be able
        to determine if spectral lines defined by the user in
        different modules are one and the same.
        
        Parameters
        ----------
        wvl: float
            Target wavelength (e.g. 180.401) in Angstroms
        '''
        if self.ionid in chdata.MasterList:
            wvl_list = np.asarray(chdata.chio.wgfaRead(self.ionid)['wvl'], 'float64')
            nonzed = wvl_list != 0.
            wvl_list = wvl_list[nonzed]
            chlineidx = np.argmin(np.abs (wvl_list - wvl))
            self.wvl = wvl_list[chlineidx] * u.AA
        else:
          raise Exception('Ion ID Error', 'This ion does not exist in the CHIANTI database', self.ionid)

    def __eq__(self, other): 
        return (self.wvl == other.wvl) and (self.ionid == other.ionid)


class SpecLine(Line):

    def __init__(self, ionid, wvl, temp=temperature_array, dens=density_array, abundname=abundname, abund_ph_name=abund_ph_name, save=True, verbose=False):
        '''
        
        Spectral line object :
        
        Parameters
        ----------
        ionid: string
            String identifying ion (CHIANTI format, e.g. 'fe_11')

        wvl: float
            Target wavelength (e.g. 180.401) in Angstroms

        Keyword Parameters
        ------------------
        temp : quantity array
            Array of temperatures (usually in K) with which the calculations are to be made
            
        dens : quantity array
            Array of densities (usually in cm**-3) with which the calculations are to be made

        abundname : str

        abund_ph_name : str
            
        save : bool
            If True (default), the data will be stored in a file, filename is defined as follows :
            '/home/nzambran/contribution_functions/cofnt_{}_{}_{}.npz'.format(self.element.lower
            (), self.iondeg, str(wvl))
        
        verbose : bool
            If True (default), information about the calculation process will be displayed

        N. B. : For plotting purposes, it is best if the numbers in the temperature and density 
        arrays are evenly spaced in logarithmic scale.


        Attributes :
        ------------
        (these will be saved to a file with the save method and recovered from one when 
        creating a SpecLine object if such a file exists)
        
        self.element     : str, element that emits the spectral line, e.g. 'Fe', 'O'

        self.iondeg      : str, ionization degree

        self.density     : quantity array(n), density array used to perform the calculations 
                           in cm^-3

        self.temperature : quantity array(m), temperature array used to perform the calculations 
                           in K
        self.wvl         : quantity, wavelength at which the line is emitted in angstroms

        self.FIP         : quantity, first ionization potential of the atom in eV

        self.lower       : str, lower level of the transition (e.g. '3s2 3p4 3P2.0')

        self.upper       : str, upper level of the transition (e.g. '3s2 3p3 3d 3D3.0')

        self.cofnt       : quantity array(n,m), contribution function of the line, n corresponds 
                           to the size of the density array and m to that of the temperature

        self.abund       : float, abundance used to calculate the radiance, it comes from the 
                           CHIANTI database 

        self.ph_abund    : float, photospheric abundance of the element, comes from the CHIANTI 
                           database

        self.regions     : dict of dict, for each region (in the regions list defined in config.py) 
                           self.regions[region] contains three arrays: 
                                - 't'       : contains the logical conjunction of the temperature 
                                              array that we want to use to perform our 
                                              calculations and the temperature interval available 
                                              in the dem files of the  Chianti database
                                - 'em'      : the emission measure as interpolated from the 
                                              Chianti database and evaluated at the desired 
                                              temperatures. If certain values in this array are 
                                              zero, it means that some temperature values were out 
                                              of range.
                               - 'radiance' : array(n,m), typical radiances for the spectral line  
                                              in different solar regions
        
        Useful methods :
        ----------------
        
        self.plot_cofnt      : plots the contribution function as a function of temperature and
                               density
        
        self.plot_coupe_dens : plots the contribution function at a given density as a function of
                               temperature
        
        self.plot_coupe_temp : plots the contribution function at a given temperature as a 
                               function of density
        
        self.save            : saves the attributes described above in a .npz file, this is done
                               by default

        Examples of use :
        -----------------
        
        Define the following variables in the config.py file available in the fiplcr module :
        - directory         : string defining where the data should be stored
        - temperature_array : quantity array, temperatures used in calculations
        - density_array     : quantity array, densities used in calculations
        - abundname         : string, name of the coronal abundance file in the CHIANTI database 
                              used to make typical coronal radiance calculation
        - abund_ph_name     : string, name of the photospheric abundance file in the CHIANTI  
                              database used to make FIP bias calculations
        - regions           : list of strings, different solar regions which we calculate typical 
                              radiances
        
        Calling example for defining spectral line of iron inozied 11 times at wavelength 195.119 
        angstrom without saving the file:
        fe12_195 = SpecLine('fe_12', 195.119, save=False)

        Calling example for defining spectral line of iron inozied 11 times at wavelength 195.119 
        angstrom, saving file, no information about calculations displayed :
        fe12_195 = SpecLine('fe_12', 195.119, verbose=False)

        '''

        Line.__init__(self, ionid, wvl, abundname, abund_ph_name)
        self.verbose = verbose

        # Definition of temperature and density arrays for calculations
        self.density = dens
        self.temperature = temp
        self.abundname = abundname
        self.abund_ph_name = abund_ph_name
        
        # Definition of directories for saving contribution function data and 
        # contribution function plots
        self.cofnt_dir = os.path.join(directory,'contribution_functions')
        self.cofnt_plots_dir = os.path.join(directory,'contribution_function_plots')
        try:
            # We try to create a directory
            os.makedirs(self.cofnt_dir)
        except OSError:
            # If it doesn't work, it exists already (probably), we will be able to
            # store data in this directory
            pass
        try:
            # We try to create a directory
            os.makedirs(self.cofnt_plots_dir)
        except OSError:
            # If it doesn't work, it exists already (probably), we will be able to
            # store plots in this directory
            pass
        
        # Definition of file names for contribution function data and plots
        self.filename = os.path.join(self.cofnt_dir,'cofnt_{}_{}_{}.npz'.format(self.element.lower(),self.iondeg, str(wvl)))
        self.plot_filename = os.path.join(self.cofnt_plots_dir,'cofnt_{}_{}_{}'.format(self.element.lower(),self.iondeg, str(wvl)))

        # We are going to check first if the file exists already or not by calling
        # the function already_calculated that checks if the file exists and if the
        # existing data was calculated with the same parameters (mainly temperature
        # and density).
        (exists, cfile) = self.already_calculated(wvl)
        if exists:
            # If our test succeeds, we are going to recover the data in
            # order to define our SpecLine object
            self.recover(cfile)
        else:
            # If our test fails, the data has not been calculated yet, we
            # are therefore going to calculate it for the first time.
            # Calculation of the contribution function using the 
            # ChiantiPy ion class and its built-in methods
            self.cofnt(ionid, wvl)
            print(' ')
        # We are going to read the EM data available through CHIANTI 
        # This is used in the linear_combination module
        self.read_em()

            # 3 - Calculation of the typical radiances of the spectral 
            # lines in different solar regions
        if save:
            # If save keyword parameter was set to True, we save the data
            # in a file with file name self.filename in directory
            # self.cofnt_dir
            self.save()

    def __repr__(self):
        '''
        This function returns a printable representation of a SpecLine object.
        '''
        return """
        Specline object for {} {} line at {}

        Attributes : element, iondeg, density, temperature, wvl, FIP, lower, 
                    upper, cofnt, abund, ph_abund, regions : - 't'
                                                            - 'em'
                                                            - 'radiance'
        Methods    : plot_cofnt, plot_coupe_dens, plot_coupe_temp, save
                    (already_calculated, recover, read_em, cofnt, radiance)

             """.format(self.element, self.iondeg, self.wvl)

    def already_calculated(self,wvl):
        '''
        Function that checks weather a contribution function has already 
        been calculated or not. If it is the case, this function will 
        return the tuple (True, cfile) where cfile is the opened existing 
        file.
        Otherwise, it will return the tuple (False, 'nofile').
        
        Parameters
        ----------
        wvl : float
            wavelength of the desired spectral line in angstroms
        '''

        # First, check if a file for this particular line already exists
        if isfile(self.filename):
            # We open the file
            cfile = np.load(self.filename)
            # If a file does exist, we check if the temperature and
            # density arrays with which we want to do the calculation and 
            # those with which the calculations in the existing file were 
            # made are the same.
            if np.array_equal(self.temperature.value, cfile['temperature']) and np.array_equal(self.density.value, cfile['density']):
                print('The contribution function for the {} {}, {} line has already been calculated.'.format(self.element, self.iondeg, str(wvl)))
                return (True, cfile)
            else:
                # If a file does exist but doesn't contain the same
                # temperature and density arrays, the calculation will be 
                # carried out.
                # The pre-existing file will be overwritten
                return (False, 'nofile')
        else:
            # If no file exists, the calculation will be carried out
            return (False, 'nofile')


    def recover(self, cfile):
        '''  
        
        Creates a SpecLine object from data already available in a file.
        Defines the following attributes :

        self.element     : str, element that emits the spectral line, e.g. 'Fe', 'O'

        self.iondeg      : str, ionization degree

        self.density     : quantity array(n), density array used to perform the calculations 
                           in cm^-3

        self.temperature : quantity array(m), temperature array used to perform the calculations 
                           in K
        self.wvl         : quantity, wavelength at which the line is emitted in angstroms

        self.FIP         : quantity, first ionization potential of the atom in eV

        self.lower       : str, lower level of the transition (e.g. '3s2 3p4 3P2.0')

        self.upper       : str, upper level of the transition (e.g. '3s2 3p3 3d 3D3.0')

        self.cofnt       : quantity array(n,m), contribution function of the line, n corresponds 
                           to the size of the density array and m to that of the temperature

        self.regions     : dict of dict, for each region (in the regions list at the beginning of 
                           this code) self.regions[region] contains three arrays: 
                                - 't'       : contains the logical conjunction of the temperature 
                                              array that we want to use to perform our 
                                              calculations and the temperature interval available 
                                              in the dem files of the  Chianti database
                                - 'em'      : the emission measure as interpolated from the 
                                              Chianti database and evaluated at the desired 
                                              temperatures. If certain values in this array are 
                                              zero, it means that some temperature values were out 
                                              of range.
                               - 'radiance' : array(n,m), typical radiances for the spectral line  
                                              in different solar regions

        ''' 

        if self.verbose:
            print('Recovering the data...')
        # Wavelength of the spectral line
        self.wvl = cfile['wvl'] * u.AA
        print('The wavelength found in our data base is {}'.format(self.wvl))
        # First ionization potential of the element
        self.FIP = cfile['FIP'] * u.eV
        # Lower level of the transition
        self.lower = cfile['lower']
        # Upper level of the transition
        self.upper = cfile['upper']
        if self.verbose:
            print('It corresponds to the transition from the level {} to the level {}'.format(self.upper, self.lower))
        # Contribution function
        self.cofnt = cfile['cofnt'] * u.erg * u.cm**3 / u.s / u.sr
        # # Coronal abundance of the ion from CHIANTI database
        # self.abund = cfile['abund']
        # # Photospheric abundance of the ion from CHIANTI database
        # self.ph_abund = cfile['ph_abund']
        if self.verbose:
            print('The typical radiances calculations were made with an abundance for {} {} of {}'.format(self.element, self.iondeg, self.abund))
        print(' ')


    def read_em(self):
        '''  
        Reads the EM data, defines 't' and 'em' in self.regions[region]
        for each region in the regions list.
        '''

        self.regions = dict()
        for region in regions:
            self.regions[region] = dict()
            self.regions[region]['t'], self.regions[region]['em'] = readChiantiDEM(region, temp=self.temperature.value)


    def cofnt(self, ionid, wvl):
        '''
        
        Calculation of the contribution function, does not include
        abundance. We obtain a cofnt that depends on temperature aswell 
        as on density. 
        
        The formula used to calculate the contribution function is :
        C(density,temperature) = ionization equilibrium * emissivity / 
        density
        
        Our definition of the contribution function does NOT include the
        abundance factor.

        ionization equilibrium : dimensionless
        emisivity              : in erg / sr / s
        density                : in cm^-3
        C (cofnt)              : in erg cm^3 / sr / s

        Parameters
        ----------
        ionid: string
            String identifying ion (CHIANTI format, e.g. 'fe_11')

        wvl: float
            Target wavelength (e.g. 180.401) in Angstroms
        '''

        ntemp = len(self.temperature.value)
        ndens = len(self.density.value)

        # Initialization of different variables in their corresponding units
        self.cofnt = np.zeros((ndens, ntemp)) * u.erg * u.cm**3 / u.s / u.sr
        self.emiss = np.zeros((ndens, ntemp)) * u.erg / u.s / u.sr
        self.ioneq = np.zeros((ndens, ntemp))
            
        for i in range(0,ndens):
            # Initialization of an ion object and calculation of emissivity
            if version=='old':
                chion = ch.ion (ionid, temperature=self.temperature.value, eDensity=self.density[i].value, abundanceName=abundname)
                chion.emiss(wvlRange=[wvl-1, wvl+1], allLines=0)
            else:
                chion = ch.ion (ionid, temperature=self.temperature.value, eDensity=self.density[i].value, abundance=abundname)
                chion.emiss(allLines=False)

            # Determination of the index of our spectral line (index used
            # by CHIANTI)
            self.chlineidx = np.argmin(np.abs(chion.Emiss['wvl'] - wvl))
            #print('chlineidx = {}'.format(self.chlineidx))
                
            self.emiss[i] = chion.Emiss["emiss"][self.chlineidx] * u.erg / u.s / u.sr
            # The units of emiss are : erg s^-1 str^-1

            chion.ioneqOne()
            self.ioneq[i] = chion.IoneqOne
            # The ionization equilibrium is dimensionless
                
            if i == 0:
                print('Ion object initialized for {} {} (using the CHIANTI data base)'.format(self.element, self.iondeg))
                print('Calculating contribution function...')
                if self.verbose:
                    print('First iteration of {}'.format(str(ndens)))
                    print('Emissivity calculated for {} {}, {} (using the CHIANTI data base)'.format(self.element, self.iondeg, str(wvl)))
                    print('Ionization equilibrium calculated for {} {} (using the CHIANTI data base)'.format(self.element, self.iondeg))

                self.wvl = chion.Emiss['wvl'][self.chlineidx] * u.AA
                print('The wavelength found in the CHIANTI data base is {}'.format(self.wvl))
                self.upper = chion.Emiss['pretty2'][self.chlineidx]
                self.lower = chion.Emiss['pretty1'][self.chlineidx]
                if self.verbose: 
                    print('It corresponds to the transition from the level {} to the level {}'.format(self.upper, self.lower))
                    print(' ')
                self.FIP = chion.FIP * u.eV
                # self.abund = chion.Abundance
                # self.ph_abund = chdata.Abundance[abund_ph_name]['abundance'][chion.Z-1]
            else:
                if self.verbose:
                    print('Density index {} of {}'.format(str(i+1), str(ndens)))
                
                # We check if all calculations were made for the same spectral line
                assert(self.wvl.value == chion.Emiss['wvl'][self.chlineidx])
                assert(self.upper == chion.Emiss['pretty2'][self.chlineidx])
                assert(self.lower == chion.Emiss['pretty1'][self.chlineidx])
                assert(self.FIP.value == chion.FIP)
            # Calculation of the contribution function, this definition does 
            # NOT include the abundance.
            self.cofnt[i] = self.ioneq[i] * self.emiss[i] / self.density[i]
            # Units of cofnt are : erg s^-1 str^-1 cm^3

    def typical_radiances(self):
        '''
        
        Calculation of typical radiances in different solar regions for 
        the spectral line.

        The formula used to calculate the radiance is :
        R = abundance * contribution function * emission measure

        abundance              : dimensionless
        contribution function  : in erg cm^3 / sr / s 
        emission measure       : in cm^-5
        R (radiance)           : in erg s^-1 str^-1 cm^-2

        '''

        ntemp = len(self.temperature.value)
        ndens = len(self.density.value)
        for region in regions:
            temp_rad = np.zeros((ndens, ntemp)) * u.erg / (u.cm**2 * u.s * u.sr)
            self.regions[region]['radiance'] = np.zeros((ndens)) * u.erg / (u.cm**2 * u.s * u.sr)
            for i in range(0,ndens):
                temp_rad[i] = self.abund * self.cofnt[i] * self.regions[region]['em']
            self.regions[region]['radiance'] = np.sum(temp_rad, axis=1)


    def plot_cofnt(self, save=False):
        '''
        
        2D plot of the contribution function of the line as a function of 
        temperature and density. 

        Keyword parameters
        ------------------
        save : bool, if true, plot will be saved in 

        Example of use :
        ----------------
        If you called your specline fe12_195 and wish to save the plot, 
        write for example :
        
        fe12_195.plot_cofnt(save=True)

        '''
        plt.clf()
        ntemp = len(self.temperature.value)
        ndens = len(self.density.value)
        if ntemp == 1 and ndens == 1:
            print('Only one point in Contribution Function!')
            print('C({:g}{},{:g}{}) = {:g}{}'.format(self.density.value, self.density.unit, self.temperature.value, self.temperature.unit, self.cofnt[0,0].value, self.cofnt[0,0].unit))
            print(' ')
        elif ntemp == 1:
            plt.loglog(self.density.value,self.cofnt[:,0].value)
            plt.xlabel('log(Density), n in {}'.format(self.density.unit.to_string(format='Latex')), fontsize=14)
            plt.ylabel('log(C), C(n,T) in {}'.format(self.cofnt.unit.to_string(format='Latex')), fontsize=14)
            plt.title('Contribution function for the {} line of {} {} at constant T = {:g} K'.format(self.wvl, self.element, self.iondeg, self.temperature.value), fontsize=16)
        elif ndens == 1:
            plt.loglog(self.temperature.value,self.cofnt[0].value)
            plt.xlabel('log(Temperature), T in {}'.format(self.temperature.unit.to_string(format='Latex')), fontsize=14)
            plt.ylabel('log(Contribution Function), Cofnt in {}'.format(self.cofnt.unit.to_string(format='Latex')), fontsize=14)
            plt.title('Contribution function for the {} line of {} {} in {} at constant n = {:g}'.format(self.wvl, self.element, self.iondeg, self.cofnt.unit.to_string(format='Latex'), self.density), fontsize=16)
        else:
            extent = (np.log10(self.temperature[0].value),np.log10(self.temperature[-1].value),np.log10(self.density[0].value),np.log10(self.density[-1].value))
            plt.imshow(np.log10(self.cofnt.value), origin='lower', extent=extent, vmin=-60)
            plt.colorbar()
            plt.xlabel('log(Temperature), T in K', fontsize=14)
            plt.ylabel('log(Density), n in $\\mathrm{cm}^{-3}$', fontsize=14)
            plt.title('Contribution function for the {} line of {} {} \n in {}'.format(self.wvl, self.element, self.iondeg, self.cofnt.unit.to_string(format='Latex')), fontsize=16)
            plt.tight_layout()
        if save:
            plt.savefig(self.plot_filename+'.png')
        else:
            plt.show()


    def plot_coupe_dens(self, idens=0, save=False):
        '''
        
        Plot the contribution function at a given density.

        Keyword Parameters
        ------------------
        idens : int
            Index identifying the density at which the contribution 
            function will be plotted in the self.density array.
            Default value is 0.

        Example of use :
        ----------------
        If you called your specline fe12_195, you wish to save the plot
        and your density array has at least 6 values, write for example :
        
        fe12_195.plot_coupe_dens(idens=5,save=True)

        '''
        plt.clf()
        plt.loglog(self.temperature.value,self.cofnt[idens].value, color='blueviolet')
        plt.xlabel('log(Temperature), T in {}'.format(self.temperature.unit.to_string(format='Latex')), fontsize = 14)
        plt.ylabel('log(C), C(n, T) in {}'.format(self.cofnt.unit.to_string(format='Latex')), fontsize = 14)
        plt.title('Contribution function for the {} line of {} {}  \n at constant n = {:g} {}'.format(self.wvl, self.element, self.iondeg, self.density[idens].value, self.density[idens].unit.to_string(format='Latex')), fontsize = 16)
        plt.tight_layout()
        if save:
            plt.savefig(self.plot_filename+'_coupe_dens_{:g}.png'.format(self.density[idens].value))
        else:
            plt.show()


    def plot_coupe_temp(self, itemp=0, save=False):
        '''
        
        Plot the contribution function at a given temperature.

        Keyword Parameters
        ------------------
            Index identifying the temperature at which the contribution 
            function will be plotted in the self.temperature array.
            Default value is 0.

        Example of use :
        ----------------
        If you called your specline fe12_195, you wish to save the plot
        and your temperature array has at least 6 values, write for 
        example :
        
        fe12_195.plot_coupe_temp(itemp=5,save=True)

        '''

        plt.clf()
        plt.loglog(self.density.value,self.cofnt[:,itemp].value, color='blueviolet')
        plt.xlabel('log(Density), n in {}'.format(self.density.unit.to_string(format='Latex')), fontsize = 14)
        plt.ylabel('log(Contribution Function), C(n, T) in {}'.format(self.cofnt.unit.to_string(format='Latex')), fontsize = 14)
        plt.title('Contribution function for the {} line of {} {} in {} \n at constant T = {:g} K'.format(self.wvl, self.element, self.iondeg, self.cofnt.unit.to_string(format='Latex'), self.temperature[itemp].value), fontsize = 16)
        plt.tight_layout()
        if save:
            plt.savefig(self.plot_filename+'_coupe_temp_{:g}.png'.format(self.temperature[itemp].value))
        else:
            plt.show()


    def save(self):
        '''
        
        Saves a SpecLine object into a .npz file. Use the self.recover 
        function in order to create a SpecLine object from a file.

        Saves the following attributes :

        self.element     : str, element that emits the spectral line, e.g. 'Fe', 'O'

        self.iondeg      : str, ionization degree

        self.density     : quantity array(n), density array used to perform the calculations 
                           in cm^-3

        self.temperature : quantity array(m), temperature array used to perform the calculations 
                           in K
        self.wvl         : quantity, wavelength at which the line is emitted in angstroms

        self.FIP         : quantity, first ionization potential of the atom in eV

        self.lower       : str, lower level of the transition (e.g. '3s2 3p4 3P2.0')

        self.upper       : str, upper level of the transition (e.g. '3s2 3p3 3d 3D3.0')

        self.cofnt       : quantity array(n,m), contribution function of the line, n corresponds 
                           to the size of the density array and m to that of the temperature

        self.abund       : float, abundance used to calculate the radiance, it comes from the 
                           CHIANTI database 

        self.ph_abund    : float, photospheric abundance of the element, comes from the CHIANTI 
                           database

        self.regions     : dict of dict, for each region (in the regions list at the beginning of 
                           this code) self.regions[region] contains three arrays: 
                                - 't'       : contains the logical conjunction of the temperature 
                                              array that we want to use to perform our 
                                              calculations and the temperature interval available 
                                              in the dem files of the  Chianti database
                                - 'em'      : the emission measure as interpolated from the 
                                              Chianti database and evaluated at the desired 
                                              temperatures. If certain values in this array are 
                                              zero, it means that some temperature values were out 
                                              of range.
                               - 'radiance' : array(n,m), typical radiances for the spectral line  
                                              in different solar regions

        '''

        dico = {\
        'temperature' : self.temperature.value, \
        'density': self.density.value, \
        'cofnt': self.cofnt.value, \
        'element' : self.element, \
        'iondeg' : self.iondeg, \
        'wvl' : self.wvl.value, \
        'upper' : self.upper, \
        'lower' : self.lower, \
        'FIP' : self.FIP.value, \
        'abund' : self.abund, \
        'ph_abund' : self.ph_abund, \
        'abundname' : self.abundname, \
        'abund_ph_name' : self.abund_ph_name}

        np.savez(self.filename, **dico)


        #TODO:
        #* blends (à éviter) (à faire à la main?)
        #* "note" combinant intensité typique, absence de blend, qualité de la physique atomique (moins bonne pour Na-like, Li-like)

