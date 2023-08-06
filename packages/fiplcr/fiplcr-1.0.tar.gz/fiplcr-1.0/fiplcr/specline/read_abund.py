#!/usr/bin/env python3

import re
import numpy as np

from fiplcr import config

def read_abund(filename):
    ''' Read chianti .abund files

    Parameters
    ==========
    filename : str
        File to read.

    Returns
    =======
    data : dict
        A dictionnary where the keys are the atom names
        and the values are the abundances.

    '''
    # find first line containing '-1' to discard
    # comments at the end of the file
    with open(config.xuvtop+'/abundance/'+filename+'.abund', 'r') as f:
        lines = f.readlines()
    is_comment_delimiter = [
        bool(re.match('\s*-1\s*\n', line))
        for line in lines]
    first_comment_delimiter = np.where(is_comment_delimiter)[0].min()
    # load data
    data = np.loadtxt(
        config.xuvtop+'/abundance/'+filename+'.abund',
        max_rows=int(first_comment_delimiter),
        dtype=[
            ('index', int),
            ('abundance', float),
            ('element', '<U2')
            ],
        )
    data = dict(zip(
        data['element'],
        data['abundance'],
        ))
    # Note: the dict conversion discards the indexes and the order, and may be
    # removed in order to preserve them.  In this case, access data['index'],
    # data['abundance'] and data['element']
    return data

if __name__ == '__main__':
    a = read_abund('proto_solar_2009_lodders')
    print(a)
