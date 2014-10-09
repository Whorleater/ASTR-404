"""
Simple script to generate an interactive gui to inspect history data as 
computed by the MESA code.
 
coder   : a. gautschy 
version : april 2013
"""
import mesa as ms   # this refers to the mesa.py module 
                    # as provided through nugrid
import numpy as np
#----------------------------------
from matplotlib import rc
import matplotlib as mpl
import matplotlib.gridspec as gridspec
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
#--------------------------------------------------
#...AFG-Style settings in matplotlib Figures
#--------------------------------------------------
rc('text', usetex=True)
mpl.rcParams['figure.figsize']  = '10,10'
mpl.rcParams['axes.linewidth']  = 0.5
mpl.rcParams['axes.titlesize']  = 18
mpl.rcParams['axes.labelsize']  = 18
mpl.rcParams['xtick.labelsize'] = 18
mpl.rcParams['ytick.labelsize'] = 18

mpl.rcParams['grid.color']     = '0.8'
mpl.rcParams['grid.linestyle'] = '-'
mpl.rcParams['grid.linewidth'] = 0.3


#----------------------------------------------------------------------
#...Mesa specifics
#----------------------------------------------------------------------
# enter path to history file
mdlfile   = '.'
# name of the history-data file, per default: history.data
hist_name = 'history.data' 


# choose a quantity from the star_dict keys to be used in the long plot:
quantity = "Xc"

# dictionary with the potential 'longplot' quantities
star_dict = {
    'Xsurf':0, 'Ysurf':1, 'Csurf':2, 'Osurf':3,
    'Xc'   :4, 'Yc'   :5, 'Cc'   :6, 'Oc'   :7
            }

len_star_dict = len(star_dict)

# dictionary-associated strings for labeling the plot 
star_strng = [
    '$X_{\mathrm{surf}}$','$Y_{\mathrm{surf}}$','$C_{\mathrm{surf}}$',
    '$O_{\mathrm{surf}}$',
    '$X_{\mathrm{c}}$','$Y_{\mathrm{c}}$','$C_{\mathrm{c}}$',
    '$O_{\mathrm{c}}$'
             ]

lp_title = star_strng[star_dict[quantity]]

nxtickints = 5  # number of x-tick intervals in each plot


#...read data from history fi
logfl = ms.star_log(mdlfile,slname=hist_name)

lgte   = logfl.get('log_Teff')
lgl    = logfl.get('log_L')
lgrhc  = logfl.get('log_center_Rho')
lgtc   = logfl.get('log_center_T')
mod_no = logfl.get('model_number')

nmod = len(mod_no)
lp_alldat = np.zeros((nmod,len_star_dict))


lp_alldat[:,star_dict['Xsurf']] = logfl.get('surface_h1').flatten()
lp_alldat[:,star_dict['Csurf']] = logfl.get('surface_c12').flatten()
lp_alldat[:,star_dict['Osurf']] = logfl.get('surface_o16').flatten()
lp_alldat[:,star_dict['Xc']   ] = logfl.get('center_h1').flatten()
lp_alldat[:,star_dict['Cc']   ] = logfl.get('center_c12').flatten()
lp_alldat[:,star_dict['Oc']   ] = logfl.get('center_o16').flatten()


#...select the quantity to be plotted in the top, long-plot
longplot_y   = lp_alldat[:,star_dict[quantity]]
longplot_anf = longplot_y[0]

lgt_min = min(lgte)
lgt_max = max(lgte)
lgl_min = min(lgl)
lgl_max = max(lgl)

lgrhc_min = min(lgrhc) 
lgrhc_max = max(lgrhc)
lgtc_min  = min(lgtc)
lgtc_max  = max(lgtc) 

xhrdmin = lgt_max + (lgt_max - lgt_min)*0.03
xhrdmax = lgt_min - (lgt_max - lgt_min)*0.03
yhrdmin = lgl_min - (lgl_max - lgl_min)*0.03
yhrdmax = lgl_max + (lgl_max - lgl_min)*0.03

xrhtmin = lgrhc_min - (lgrhc_max - lgrhc_min)*0.03
xrhtmax = lgrhc_max + (lgrhc_max - lgrhc_min)*0.03
yrhtmin = lgtc_min  - (lgtc_max  - lgtc_min)*0.03
yrhtmax = lgtc_max  + (lgtc_max  - lgtc_min)*0.03

mod_anf = mod_no[ 0]
mod_end = mod_no[-1]

xhrd_mod = lgte[0]
yhrd_mod = lgl [0]

xrht_mod = lgrhc[0]
yrht_mod = lgtc [0]

#---------------------------------------------------------
#...define the various subplots with the Mesa history data
#---------------------------------------------------------
gs = gridspec.GridSpec(2, 2, width_ratios =[1,1],
                             height_ratios=[1,3])
# adjust arrangement on canvas
gs.update(left=0.15, bottom=0.15, wspace=0.35, hspace=0.3)  

#..."Longplot": a physical quantity vs. model number
ax1 = plt.subplot(gs[0,:])
plt.grid(True)
glob1,  = plt.plot(mod_no, longplot_y, 'k-', lw=1.5)
glob1a, = plt.plot(mod_anf, longplot_anf, 'ro', ms=7)
plt.axis([mod_anf, mod_end, -0.01, 1.01])
ax1.xaxis.set_major_locator(MaxNLocator(nxtickints))
plt.ylabel(lp_title)
plt.xlabel('Model No')


#...HR Diagram
ax2 = plt.subplot(gs[1,0])
plt.grid(True)
l,  = plt.plot(lgte, lgl, 'k-', lw=1.5)
ll, = plt.plot(xhrd_mod, yhrd_mod, 'ro', ms=7)
plt.axis([xhrdmin, xhrdmax, yhrdmin, yhrdmax])
ax2.xaxis.set_major_locator(MaxNLocator(nxtickints))
plt.title ('HR Diagram')


#...log Rho_c - log T_c
ax3 = plt.subplot(gs[1,1])
plt.grid(True)
lrht,  = plt.plot(lgrhc, lgtc, 'k-', lw=1.5)
llrht, = plt.plot(xrht_mod, yrht_mod, 'ro', ms=7)
plt.axis([xrhtmin, xrhtmax, yrhtmin, yrhtmax])
ax3.xaxis.set_major_locator(MaxNLocator(nxtickints))
plt.title(r'$\log \rho_{\mathrm{c}} - \log T_{\mathrm{c}}$')


#...Slider setup
axcolor = 'lightgoldenrodyellow'
axmodno = plt.axes([0.2, 0.05, 0.7, 0.03], axisbg=axcolor)
smodno  = Slider(axmodno, 'Model No.', mod_anf, mod_end,
                 valinit=mod_anf, valfmt='%i')

def update(val):
    slidemod = int(smodno.val)
    detfun = np.abs(slidemod-mod_no)
    itemindex = list(detfun).index(detfun.min())

    xhrd_mod = lgte[itemindex]
    yhrd_mod = lgl [itemindex]

    xrht_mod = lgrhc[itemindex]
    yrht_mod = lgtc [itemindex]

    ylp_mod  = longplot_y[itemindex]

    #...update the epoch pointer along the track
    ll.set_xdata(xhrd_mod)
    ll.set_ydata(yhrd_mod)

    llrht.set_xdata(xrht_mod)
    llrht.set_ydata(yrht_mod)

    glob1a.set_xdata(slidemod)
    glob1a.set_ydata(ylp_mod)

    plt.draw()
smodno.on_changed(update)


#...Reset button
resetax = plt.axes([0.084, 0.008, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')

def reset(event):
    smodno.reset()
button.on_clicked(reset)


plt.show()



