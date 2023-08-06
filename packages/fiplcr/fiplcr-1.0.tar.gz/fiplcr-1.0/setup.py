import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()
with open('requirements.txt', 'r') as f:
    requirements = f.read().strip('\n').split('\n')

setuptools.setup(
    name='fiplcr',
    version='v1.0',
    author='Natalia Zambrana Prado',
    author_email='natalia.zambrana-prado@ias.u-psud.fr',
    description='Relative FIP bias diagnostics using linear combinations of spectral lines',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://git.ias.u-psud.fr/nzambran/fiplcr',
    packages=setuptools.find_packages(),
    python_requires='>=3.5',
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
    ],
)
