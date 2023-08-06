import numpy as np
import astropy.units as u
import matplotlib.pyplot as plt

from fiplcr.linear_combination import LinearComb as lc
from fiplcr.fip_map import fip_map as fm
from fiplcr.specline import Line

from eis_data_class import EISData as eisd

def join_fitspar_lincomb(ff, ll):
    # Counter
    found_lines = 0

    # We check that every line that is either in ll.ionsHF or ll.ionsLF is also available in
    # ff.lines_fip_map so that we can get their integrated intensity for FIP map calculation.
    for line in ll.ionsHF:
        if line in ff.lines:
            found_lines += 1
            ff_line = ff.__getitem__((line.ionid,line.wvl.value))
            line.int_map = ff_line.int_map
            line.solar_x = ff_line.solar_x
            line.solar_y = ff_line.solar_y

    for line in ll.ionsLF:
        if line in ff.lines:
            found_lines += 1
            ff_line = ff.__getitem__((line.ionid,line.wvl.value))
            line.int_map = ff_line.int_map
            line.solar_x = ff_line.solar_x
            line.solar_y = ff_line.solar_y

    # Raising error if not all lines were avialable
    if found_lines!=(len(ll.ionsHF)+len(ll.ionsLF)):
        raise ValueError('We were not able to find all the optimized lines in the observations')

if __name__ == '__main__':

    # Directory containing the HINODE/EIS fitted  data that you wish to use. 
    # This file must be in format .npz, this code does not read FITS files.
    filename = './eis_data_example.npz'
    eis_data = eisd(filename)
    eis_data.read_density_file('./eis_density_example.npz')

    print('Lines defined.')
    print(' ')
    print('Optimizing lines')
    # We use the attribute lines_linear_comb from ff as input for linear_comb and determine an 
    # optimal linear combination of spectral lines from the previously fitted ones
    ll = lc(eis_data.lines)
    ll.compute_linear_combinations()

    join_fitspar_lincomb(eis_data, ll)

    # Calculation of FIP map
    FIP_map = fm(ll, eis_data.density_map)
