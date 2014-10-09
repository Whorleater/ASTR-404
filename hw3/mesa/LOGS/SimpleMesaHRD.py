'''
Basis python script to generate an HR diagram using
mesa class to easily import data from star.log files
'''
import matplotlib.pyplot as plt
import mesa as ms

#--------------------------------------------------
#...simplest settings in matplotlib Figures
#...further modifications can be applied in 
#...the matplotlibrc file
#--------------------------------------------------
from matplotlib import rc
rc('font',**{'family':'serif','serif':['Times']})
rc('text', usetex=True)
#-----------------------------------------------------

# define list of log files that are to be used for the
# HR plot
mdlfiles = ['star.log']

#...Plot initializations
lwght = 1.3   # starting line-weight

for fil in mdlfiles:
    # we assume that the log files are stored in the directory
    # where the script runs. Otherwise, replace '.' by the
    # path to the appropriated directory
    logfl = ms.star_log('.',slname=fil)

    lgte   = logfl.get('log_Teff')
    lgl    = logfl.get('log_L')

    plt.plot(lgte, lgl, c='k', lw=lwght)

#...prepare final output, with interted x-axis as usually used
#...when using T_eff scale
plt.xlim(xmin= 4.5,xmax=3.3)      # set a userdefined x-range
plt.ylim(ymin=-1.0,ymax=4.0)      # set a userdefined y-range
   
##plt.title('Conservative ' r'$2.2 M_\odot$')

plt.xlabel(r'$\log T_{\mathrm{\mathrm{eff}}}$')     #labeling the plot
plt.ylabel(r'$\log\,L/L_\odot$')

plt.grid(False)
plt.show()
