# Relative FIP bias diagnostics using linear combinations of spectral lines

The `fiplcr` Python package allows to perform FIP bias maps measurements on the 
solar corona from UV intensity maps. It calculates an optimal linear combination
of the spectral lines in order to obtain an accurate FIP bias map.   
The proof of concept for this module is published in 
[Zambrana Prado & Buchlin, 2019](<https://doi.org/10.1051/0004-6361/201834735> "Measuring relative abundances in the solar corona with optimised linear combinations of spectral lines"). 
In order to apply the Linear Combination Ratio (LCR) method one must follow 
4 steps:  
* Selection of the spectral lines  
* Computation of the contribution functions
* Determination of the optimal linear combinations
* Determination of the relative FIP bias from the observations

The 1st step must be done on a case by case basis taking into account the 
lines available in your observation. We suggest you follow the criteria stated 
in Sec. 3.3.1 of Zambrana Prado & Buchlin, 2019.  
The 2nd step is done by the `specline` module of the `fiplcr` module.  
The 3rd step corresponds to the `linear_combination` module.  
Finally the 4th step can be done using the `fip_map` function.

Do not forget to define all required variables in the `config.py` file in order 
to perform all calculations.

## Installation

`fiplcr` uses [ChiantiPy](https://github.com/chianti-atomic/ChiantiPy) and the
Chianti database.
Before installing `fiplcr`, follow the [ChiantiPy installation
instructions](https://github.com/chianti-atomic/ChiantiPy#installation).
In particular, make sure to set the `$XUVTOP` environment variable in your
`.bashrc`.

You can then install `fiplcr` by running the following commands in your
terminal:

```python
git clone https://git.ias.u-psud.fr/nzambran/fiplcr.git
pip install fiplcr/
```

(If you have limited permission, you can install it locally with `pip install
fiplcr/ --user`.)

The `fiplcr` module is now installed on your system.
You can safely remove the `fiplcr/` repository that was created.


## Quick start examples

### Exploring linear combinations and comparing them to a simple 2-line ratio

In order to check if your linear combinations are suited for relative FIP bias
determination, you can compare their performance to that of a simple two-line 
ratio.  
This can be done following the same method presented in Sec. 4 of
[Zambrana Prado & Buchlin, 2019](<https://doi.org/10.1051/0004-6361/201834735> "Measuring relative abundances in the solar corona with optimised linear combinations of spectral lines").


Using a DEM cube (stored in examples/em_example/em_example.npz) we will synthetize 
radiance maps for the selected spectral lines one wishes to test out. The test 
case consists in using uniform abundances to compute these radiance maps. The 
test is considered successful for a given FIP bias determination method if the 
output relative FIP bias mapis consistent with the input elemental abundance 
maps, both in uniformity and in value.

Putting yourself in the directory `examples/em_example` you can run the em_test.py 
file and you will retrieve two LinearComb objects: 
* The variable `ll`, containing the lines you wish to test out with their 
corresponding synthetic radiance maps and the obtained relative FIP bias map.
* The variable `ll_2_lines`, containing the lines for the simple two-line ratio
with their corresponding synthetic radiance maps and the obtained relative 
FIP bias map.

The test has four main steps, detailed below:
1.  We derive a DEM cube from the AIA observation. This is for the sole purpose 
of producing synthetic radiances, for which we  have  control  over  all  parameters,  
while  the  DEMs  are representative of different real solar regions.
2.  Using CHIANTI for the contribution functions and the derived  DEMs,  we  calculate  
the  synthetic  radiances.  We  assume different uniform abundances for different 
elements.
3.  We determine the optimal linear combination coefficients for the LCR method, and 
the coefficients for the two-line ratio method we are comparing it to.
4.  We use these coefficients to retrieve the FIP bias in each pixel. If the selected 
lines are suitable for FIP bias determination, the retrieved FIP bias map should be 
uniform.


## FULL DESCRIPTION OF EACH MODULE

*Notes:*

If you have trouble using matplotlib and ChiantiPy and you get this kind of 
error:
"RuntimeError: LaTeX was not able to process the following string:"
you will need to install an additional package by running

`sudo apt install dvipng texlive-latex-extra texlive-fonts-recommended`
