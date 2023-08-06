import numpy as np
import astropy.units as u

def save_radiances(filename, lines):
    ''' 
    Saves all arrays contained in the list lines.
            
    The file is saved with extension npz, to open file, use 
    file = np.load(filename.npz)
    Don't forget to file.close()
    '''
    dico = {}
    
    dico['obs_data'] = {}
    dico['obs_data']['slit'] = '2"'
    dico['obs_data']['exposure_time'] = np.ones(180) * 45 * u.s
    dico['obs_data']['alpha_y'] = 1. * u.arcsec
    dico['obs_data']['alpha_slit'] = 2. * u.arcsec

    dico['obs_date'] = 20071017

    for line in lines:
        key = line.ionid + '_' + str(line.wvl.value) 
        dico[key] = {'ionid' : line.ionid, \
        'wvl' : line.wvl.value, 'wvl_unit': line.wvl.unit.to_string(), \
        'int_map' : line.int_map.value, 'int_map_unit':line.int_map.unit.to_string(), \
        'solar_y' : line.solar_y.value, 'solar_y_unit' : line.solar_y.unit, \
        'solar_x' : line.solar_x.value, 'solar_x_unit' : line.solar_x.unit}
    np.savez(filename, **dico)

def save_density_map(filename, obs_date, density_map, solar_x, solar_y):
    '''
    The file is saved with extension npz, to open file, use 
    file = np.load(filename.npz)
    Don't forget to file.close()
    '''
    
    dico = {}
    dico['obs_date'] = obs_date
    dico['density_map'] = density_map.value
    dico['density_map_unit'] = density_map.unit.to_string()
    dico['solar_x'] = solar_x.value
    dico['solar_x_unit'] = solar_x.unit
    dico['solar_y'] = solar_y.value
    dico['solar_y_unit'] = solar_y.unit
    np.savez(filename, **dico)