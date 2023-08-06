#!/usr/bin/env python3

# Special thanks to GABRIEL PELOUZE for providing this python object
# The git repository of this class can be found at :
# https://git.pelouze.net/gabriel/roman_numerals.git

# LICENSE
# Copyright (c) 2017 Gabriel Pelouze
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files 
# (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, 
# publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do 
# so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE 
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION 
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from collections import OrderedDict
import numpy as np

def _shift(arr, num, fill_value=np.nan):
    result = np.empty_like(arr)
    if num > 0:
        result[:num] = fill_value
        result[num:] = arr[:-num]
    elif num < 0:
        result[num:] = fill_value
        result[:num] = arr[-num:]
    else:
        result = arr
    return result

class RomanNumeral():

    ''' Digits used to parse from roman. '''
    digits = OrderedDict((
        ('0', 0),
        ('I', 1),
        ('V', 5),
        ('X', 10),
        ('L', 50),
        ('C', 100),
        ('D', 500),
        ('M', 1000),
        ))

    ''' Base of symbols used to convert to roman. '''
    symbols = OrderedDict((
        (1, 'I'),
        (4, 'IV'),
        (5, 'V'),
        (9, 'IX'),
        (10, 'X'),
        (40, 'XL'),
        (50, 'L'),
        (90, 'XC'),
        (100, 'C'),
        (400, 'CD'),
        (500, 'D'),
        (900, 'CM'),
        (1000, 'M'),
        ))

    def __init__(self, num):
        ''' Represent a roman number.
        Parameters
        ==========
        num : int or str
            Either the roman (str), or the arabic (int) representation of the
            number.

        Attributes
        ==========
        roman : str
            The roman representation of the number.
        int : int
            The arabic representation of the number.

        Examples
        ========

        >>> rn = RomanNumeral('MDCXLII')
        >>> rn, rn.roman, rn.int
        (<RomanNumeral MDCXLII (1642)>, 'MDCXLII', 1642)
        >>> rn = RomanNumeral(1954)
        >>> rn, rn.roman, rn.int
        (<RomanNumeral MCMLIV (1954)>, 'MCMLIV', 1954)

        >>> def parse_ion(ion_name):
        ...     atom, ionisation = ion_name.split(' ')
        ...     ionisation = RomanNumeral(ionisation)
        ...     return atom, ionisation.int
        ... parse_ion('Fe XIV')
        ...
        ('Fe', 14)

        '''

        error_msg = "'{}' cannot be interperted as a roman numeral."

        if type(num) is int:
            self.int = num
            self.roman = self._int_to_roman(self.int)

        elif type(num) is str:
            self.roman = num.upper()
            chars = set(self.roman)
            allowed_chars = set(RomanNumeral.digits.keys())
            if not chars.issubset(allowed_chars):
                raise ValueError(error_msg.format(num))
            try:
                # shortcut for parsing single digits, needed by _roman_to_int
                self.int = RomanNumeral.digits[self.roman]
            except KeyError:
                self.int = self._roman_to_int(self.roman)

        else:
            raise ValueError(error_msg.format(type(num)))

    def _roman_to_int(self, roman_string):
        ''' Convert a roman string to an arabic int. '''
        digits = np.array([RomanNumeral(d).int for d in roman_string])
        next_digits = _shift(digits, -1, fill_value=0)

        followed_digits = digits < next_digits
        following_digits = _shift(followed_digits, 1, fill_value=False)

        # count digits that are not followed nor following once
        single_digits = (digits[~(followed_digits | following_digits)])
        # add the difference of followed and following digits
        composed_digits = digits[following_digits] - digits[followed_digits]

        int_value = np.sum(single_digits) + np.sum(composed_digits)

        return int_value

    def _int_to_roman(self, int_value):
        ''' Convert an arabic int to a roman string. '''
        sorted_symbols = sorted(RomanNumeral.symbols.items(), reverse=True)
        roman_string = ''
        r = int_value
        for base_int, base_roman in sorted_symbols:
            q, r = divmod(r, base_int)
            roman_string += q * base_roman
        assert r == 0, 'Converting {} to roman failed.'.format(int_value)

        return roman_string

    def __repr__(self):
        repr_string = '<RomanNumeral {} ({})>'.format(self.roman, self.int)
        return repr_string