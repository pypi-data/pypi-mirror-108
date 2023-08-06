import numpy as np
from astropy import units as u

import matplotlib as mlt
import matplotlib.pyplot as plt
mlt.rc('xtick', labelsize=12)
mlt.rc('ytick', labelsize=12)
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
import matplotlib.colors as colors

from fiplcr.specline import Line

class EISData:
    
    def __init__(self, filename):
        ''' 
        This class recovers fitted Hinode/EIS data stored in an .npz file.
        An EISData object is created from a file. Go to the end of this
        docstring to see detailed examples. 
        
        Parameters
        ----------
        filename:
            string, filename is the name (with path) of the file from 
            which you wish to create a EISData object.

        WHAT SHOULD YOUR .NPZ FILE CONTAIN ?
        ------------------------------------
        - data about the observation (see attributes)
        - the date of the observation (see attributes)
        - a list of the lines used that will become a Line object list
        - the radiance map for each line (after fitting and alignment)
        - solar_x and solar_y for the radiance maps

        For an example of the file structure run

        from eis_data_class import EISData
        eis_data = EISData('/your_path/fiplcr/examples/hinode_eis/eis_data_example.npz')

        For an example on how to save your data in this structure see
        save_eis_data_example.py

        Attributes of a EISData object
        ------------------------------
        self.filename   : string
            It contains the path to the directory where the data are 
            stored.

        self.obs_data   : dictionary
            Contains the following information about the observation :
            - slit          : string
                '1"' if the one arcsec slit was used
                '2"' if the two arcsec slit was used
            - alpha_slit    : quantity
                width of the slit in arcsec
            - alpha_y       : quantity
                one spatial CCD pixel (or macro-pixel if the
                data was binned) in height in arcsec
            - exposure_time : quantity array
                exposure time in seconds
        self.obs_date   : integer
            Date of the observation in format yyyymmdd
        
        self.lines      : list of Line objects
            Contains information about every spectral line that is in
            self.lines_list that was found in the observations.
            Attributes of each Line object (after fitting process):
                - ionid         : string
                    String identifying ion 
                    (CHIANTI format e.g. 'fe_11')
                - element       : string
                    Element that emits the spectral line, 
                    e.g. 'Fe', 'O'
                - iondeg        : string
                    Ionization degree
                - cute          : string
                    Pretty string representation of a Line object
                - wvl           : quantity
                    Wavelength at which the spectral line is
                    emitted
                - int_map : quantity numpy array of shape (ny, nx)
                    For each pixel of the observations, integral of 
                    the gaussian fitted on that pixel's spectrum
                - solar_x : quantity numpy array of shape (nx)

                - solar_y : quantity numpy array of shape (ny)
            
        Useful methods
        --------------     
        plot_radiance_map(ionid, wvl)               :


        Creating an EISData object by reading a file :

            eis_data = EISData('/path/eis_l1_20071017_024748_fited_.npz')

        '''

        self.filename = filename
        self.read_file()
        
    def __repr__(self):
        
        return """
        EISData object for observations in file : 
        {} 
  
        Attributes
        ----------
        filename, lines (list of lines in the observation),
        Attributed of each line in lines : 
            'ionid'   : string, ion and ionization degree e.g. 'fe_12'
            'wvl'     : quantity, wavelength of the spectral line
            'int_map' : numpy array of shape (ny, nx), map of the
                radiance of the line

             """.format(self.filename)

    def __getitem__(self, item):
        '''
        Returns a spectral line in self.lines and thus this line can be 
        modified, particularly useful for adding new attributes to each
        spectral lines. If the requested line is not available in the
        self.lines list, it returns None.

        Parameters
        ----------
        item : tuple (ionid, wvl)
              in first position is the ionid for the spectral line
              e.g. 'fe_12'
              in second position is the wavelength which is a float
              float defining the wavelength of the spectral line in
              angstroms
        '''
        line_ionid, line_wvl = item
        desired_line = Line(line_ionid, line_wvl)

        # We look for the requested line in the self.lines list.
        # Here we use the __equal__ function defined in specline
        # module to compare spectral lines.
        for i in range(len(self.lines)):
            if self.lines[i] == desired_line:
                return self.lines[i]

        # If the requested line is not available in the self.lines
        # list, return None
        return None

    def read_file(self):
        '''
        Recovers the fitted data from the file (self.filename).
        Creates a FitsPar object with the same functions (in particular
        the plotting functions) as a new FitsPar object.
        '''
        cfile = np.load(self.filename, allow_pickle=True)
        self.lines = []
        i = 0
        for key in cfile.keys():
            if key=='obs_date':
                # Recovering date of the observation.
                self.obs_date = cfile['obs_date'].item()
            elif key=='obs_data':
                # Recovering data about the observation as a whole such as
                # the opening angle in the y direction, the openng angle 
                # of the slit, which slit was used and an array of the 
                # exposure times during the observation.
                self.obs_data = cfile['obs_data'].item()
            else:
                # Recovering data for each spectral line that was fitted
                # present in this file.
                # This includes the ion, the wavelength, the average 
                # fitted centrum for the fitted gaussian, the integral
                # of the gaussian fitting of the spectral cube for each
                # pixel, the spectral cube, the factor by which one has
                # to multiply the intensity in order to obtain the number
                # of photons that hit the detector, all the gaussian
                # fitting parameters for each pixel of the spectral cube,
                # the wavelength array of the fitted window, solar x and 
                # solar y positions for the window.
                dico = cfile[key][()]
                ionid = dico['ionid']
                wvl = dico['wvl'] * u.Unit(dico['wvl_unit'])
                line = Line(ionid, wvl.to(u.AA).value)
                line.int_map = dico['int_map'] * u.Unit(dico['int_map_unit'])
                line.solar_x = dico['solar_x'] * u.Unit(dico['solar_x_unit'])
                line.solar_y = dico['solar_y'] * u.Unit(dico['solar_y_unit'])
                print('Line for {} line retrieved from file...'.format(line.cute))
                self.lines.append(line)
            i += 1
        cfile.close()


    def plot_radiance_map(self, line_ionid, line_wvl):
        '''
        Plots the integral of the fitted gaussian of a particular spectral line at each
        pixel of the observations.
        
        Parameters
        ----------
        raie : string
            defines the spectral line, for a given ion and a given wavelength write the 
            acronym of the element as it would be found in the periodic table followed by 
            an underscore, its ionization number, another underscore and finally the 
            desired wavelength in angstroms. For example for the 195.119 angstrom iron 
            twelve line, write 'fe_12_195.119'.
        '''
        desired_line = self.__getitem__((line_ionid, line_wvl.value))
        left = desired_line.solar_x[0].value
        right = desired_line.solar_x[-1].value
        bottom = desired_line.solar_y[0].value
        top = desired_line.solar_y[-1].value
        plt.clf()
        plt.rc('text', usetex=True)
        plt.rc('font', family='serif')
        plt.imshow(np.log10(desired_line.int_map.value), origin='lower', extent=(left,right,bottom,top))
        plt.title('Log of the integral of the fitted gaussians for each pixel \n for line {}'.format(desired_line.cute), fontsize = 16)
        plt.xlabel('x (arcsec)', fontsize = 14)
        plt.ylabel('y (arcsec)', fontsize = 14)
        plt.colorbar()
        plt.show()

    def read_density_file(self, density_filename):
        '''
        Add a density map to the EISData object for the relative FIP 
        bias calculation. This allows to use the best possible linear
        combination of lines for each pixel of the observation 
        depending on its density.
        '''

        cfile = np.load(density_filename, allow_pickle=True)
        # Check if at least the dates are the same
        assert self.obs_date == cfile['obs_date']

        self.density_map_solar_x = cfile['solar_x'].item(0) * u.Unit(cfile['solar_x_unit'].item())
        self.density_map_solar_y = cfile['solar_y'].item(0) * u.Unit(cfile['solar_y_unit'].item())
        self.density_map = cfile['density_map'] * u.Unit(cfile['density_map_unit'].item())
        cfile.close()
