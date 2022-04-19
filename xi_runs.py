import numpy as np
from astroML.correlation import two_point
from astroML.correlation import bootstrap_two_point
from matplotlib import pyplot as plt
from astropy.cosmology import WMAP9 as cosmo
from astropy.table import Table

#--
from tools import get_zspace_coords, get_run_name
from configparser import ConfigParser
from astropy.cosmology import FlatLambdaCDM
from sklearn.linear_model import LinearRegression
from scipy.stats import linregress

import mlflow
import sys
import pathlib
from os import path, remove

# %% Load settings

# Set root path
cwd = pathlib.Path().resolve()
root_dir = cwd.parent.parent

# Load config file
config = ConfigParser()
config.read('settings.ini')

# Get settings values
exp_ss = config['experiment']['exp_series']
exp_id = config['experiment']['exp_id_root']
zmin = float(config['sample']['zmin'])
zmax = float(config['sample']['zmax'])
ra_min = float(config['sample']['ra_min'])
ra_max = float(config['sample']['ra_max'])
dec_min = float(config['sample']['dec_min'])
dec_max = float(config['sample']['dec_max'])
r_min = float(config['sample']['r_min'])
r_max = float(config['sample']['r_max'])
nbins = int(config['sample']['nbins'])
H0 = float(config['phys_models']['H0'])
Ωm = float(config['phys_models']['omega_matter'])
Tcmb = float(config['phys_models']['temp_CMB'])
xi_estimator = config['stat_models']['xi_estimator']

# %% read & prepare data
gals = Table.read('DR7-lrg.fits')
rans = Table.read('DR7-lrg-rand.fits')

# %% select data subset
fltr = (gals['z'] > zmin) & (gals['z'] < zmax) & \
       (gals['ra'] > ra_min) & (gals['ra'] < ra_max) & \
       (gals['dec'] > dec_min) & (gals['dec'] < dec_max)
gals = gals[fltr]

fltr = (rans['z'] > zmin) & (rans['z'] < zmax) & \
       (rans['ra'] > ra_min) & (rans['ra'] < ra_max) & \
       (rans['dec'] > dec_min) & (rans['dec'] < dec_max)
rans = rans[fltr]

# %% set models
cosmo = FlatLambdaCDM(H0=H0, Om0=Ωm, Tcmb0=Tcmb)

mlflow.set_experiment(exp_ss)
run_name=get_run_name(exp_id)
run_name = 'FOF_001'
with mlflow.start_run(run_name=run_name) as run:

    # %% compute corr on galaxy catalog
    redshifts = cosmo.comoving_distance(gals['z'].value)
    x, y, z = get_zspace_coords(gals['ra'].value,
                                gals['dec'].value, redshifts)

    redshifts_ran = cosmo.comoving_distance(rans['z'].value)
    xr, yr, zr = get_zspace_coords(rans['ra'].value,
                                   rans['dec'].value, redshifts_ran)

    X = np.array([x, y, z]).transpose()
    R = np.array([xr, yr, zr]).transpose()
    bins = np.linspace(r_min, r_max, nbins)
    xi = two_point(X, bins, method=xi_estimator, data_R=R)

    # %% save results in a data file:
    r = (bins[1:]+bins[:-1])/2
    with open('xi_r.csv', 'w') as f:
        for i in range(len(r)):
            f.write(f'{r[i]:7.3f}, {xi[i]: 9.5f}\n')

    # %% compute metrics

    x = np.log10(r)
    y = np.log10(xi)

    model = linregress(x, y)

    def linea(x, model):
        r = np.log10(x)
        b = model.intercept
        a = model.slope
        y = a*r + b
        yy = 10**y
        return yy

    # %% save results in a plot
    fig = plt.figure(figsize=(9, 5))
    ax = fig.add_subplot()
    ax.set_xscale('log')
    ax.set_yscale('log')
    b = model.intercept
    a = model.slope
    ax.plot([r_min, r_max],
            [linea(r_min, model), linea(r_max, model)],
            color='coral', linestyle='--', linewidth=1)
    ax.plot(r, xi, marker='o', color='cornflowerblue', mfc='white',
            linewidth=2, alpha=0.8)
    ax.set_xlim(3, 110)
    ax.set_xlabel(r'$r$ (h$^{-1}\,Mpc$)')
    ax.set_ylabel(r'$\xi(r)$')
    fig.savefig('xi_r.png')
    plt.close()

    # %% logs
    mlflow.log_param("zmin", zmin)
    mlflow.log_param("zmax", zmax)
    mlflow.log_param("H0", H0)
    mlflow.log_param("omega matter", Ωm)
    mlflow.log_param("Temp CMB", Tcmb)
    mlflow.log_param("estimator", xi_estimator)

    mlflow.log_metric("slope", model.slope)
    mlflow.log_metric("intercept", model.intercept)
    mlflow.log_artifact('xi_r.png')
    mlflow.log_artifact('xi_r.csv')
    mlflow.log_artifact('xi_runs.py')
    mlflow.log_artifact('settings.ini')
