#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 18:46:20 2020

@author: Vincent
"""


#def GalaxySpectra2()  
import random
import glob
import numpy as np
import os
from scipy import interpolate
from astropy.table import Table 
from dataphile.graphics.widgets import Slider
from matplotlib import pyplot as plt
from astroML.datasets import fetch_sdss_filter, fetch_vega_spectrum
if "setup_text_plots" not in globals():
    from astroML.plotting import setup_text_plots
import matplotlib.gridspec as gridspec
from matplotlib.widgets import RadioButtons
zlims=0,4
pathf='/Users/Vincent/Nextcloud/LAM/Work/LePhare/lephare_200509/filt/'
colors = ['midnightblue','midnightblue','midnightblue','darkblue','deepskyblue','aquamarine','mediumaquamarine','limegreen','grey','yellow','gold','orange','darkorange','coral','tomato','tomato','red','red','maroon','maroon']
sizes=[3690,3911,4851,6242,7716,8915,9801,10240,12562,16499,21570]
sizes = [0.0234, 0.0795, 0.0456,0.0598,0.1194,0.1539,0.1476,0.0768,0.0797,0.0918,0.1714,0.2895,0.3058,5.3245, 35.6385, 74.9582, 77.7000,105.9688,199.8631]
filts=['galex/FUV.pb','galex/NUV.pb','cfht/CLAUDS/u.pb','cfht/CLAUDS/uS.pb','hsc/gHSC.pb','hsc/rHSC.pb','hsc/iHSC.pb','hsc/zHSC.pb','hsc/yHSC.pb','vista/Y.pb','vista/J.pb','vista/H.pb','vista/K.pb','spitzer/mips_24.pb','herschel/PACS_100.pb','herschel/PACS_160.pb','herschel/SPIRE_PSW.pb','herschel/SPIRE_PMW.pb','herschel/SPIRE_PLW.pb']

fig = plt.figure(figsize=(22,12))
wavelength = np.linspace(0,1e7,int(1e4))
gs = gridspec.GridSpec(2, 1, height_ratios=(1,4))
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1], sharex=ax1)
spec = fetch_vega_spectrum()
lam = spec[0]
spectrum = spec[1] / 2.1 / spec[1].max()
d={'lam':lam,'spectrum':spectrum,'z':0}
spectrumInterp = interpolate.interp1d(np.hstack(([0],spec[0],[1e10])), np.hstack(([0],spec[1],[0])),kind='linear')
New_spectrum = spectrumInterp(wavelength)
l = ax2.plot(lam, spectrum, '-k',label='Vega')
lines = {r'$Ly\alpha$':1216,r'$D_{4000}$':4000,r'$Ly_{Break}$':912,r'$D_{3700}$':3700,r'$H_{\alpha}$':6563,r'$H_{\beta}$':4860.74,r'$H_{\gamma}$':4340.10,
# r'$Ne_5$':3425,r'$O_2$':3727,r'$Fe_7a$':3760,r'$Ne_3$':3869,r'$O_{3a}$':4363,r'$O_{3b}$':4959,r'$O_{3c}$':507,r'$Fe_{7b}$':6087,r'$O_{1c}$':6300,r'$N_{2}$':6583,
r'$O_{1}$':63e4,r'$O_{3}$':88e4,r'$N_{2a}$':122e4,r'$C_{2}$':158e4,r'$N_{2b}$':205e4,
#r'$Na_{1a}$':8190,r'$Na_{1b}$':6157,
r'$H_{\delta}$':4101.20
}
lines_plot={}
lines = {k: v for k, v in sorted(lines.items(), key=lambda item: item[1])}
for i,line in enumerate(lines):  
    if i%2:
        y=1
    else:
        y=1.03
    lines_plot[line] = ax2.plot([lines[line],lines[line]], [y, 0],linewidth=0.9,c='k',linestyle='dotted')#,head_width=0.08, head_length=0.00002)
    lines_plot[line+'_text'] = ax2.text(lines[line],y,line)
text_kwargs = dict(ha='center', va='center', alpha=0.8, fontsize=14)
mags = []
filters = []
rax = plt.axes([0., -0.01, 0.10, 0.15], facecolor='None')
radio = RadioButtons(rax, ('Vega', 'COSMOS', 'Dale','QSO','COUPON','Star'))
redshift_ = Slider(figure=fig, location=[0.1, 0.05, 0.8, 0.03], label='$z$',  bounds=(zlims), init_value=0)#,valfmt="%1.
for edge in 'left', 'right', 'top', 'bottom':
    rax.spines[edge].set_visible(False)       
for i, filt in enumerate(filts):
    print(filt)
    path = os.path.join(pathf,filt)
    a=Table.read(path,format='ascii',data_start=1)
    tab = a[a['col2']/a['col2'].max()>0.01]
    data=[a['col1'],a['col2']/a['col2'].max()]
    ax2.fill_between(data[0],data[1], alpha=0.4,color=colors[i])#,label=labels[i])
    b = np.linspace(data[0].max()+1,1e9,int(1e6))
    FieldInterp = interpolate.interp1d(np.hstack(([0],data[0],[1e10])), np.hstack(([0],data[1],[0])),kind='linear')
    filters.append(FieldInterp(wavelength))
    loc = data[0][np.argmax(data[1])]
    ax2.text(loc, 0.02, filt.split('/')[-1].split('.pb')[0], color=colors[i], **text_kwargs)
    mags.append(ax1.plot(loc,New_spectrum.dot(FieldInterp(wavelength)),'o',c=colors[i],markersize=15))
def update(val):
    for line,line_plot in zip(lines,lines_plot):  
        lines_plot[line][0].set_xdata([(1+val)*lines[line],(1+val)*lines[line]])  
        lines_plot[line+'_text'].set_x((1+val)*lines[line])
    l[0].set_data((1+val)*d['lam'], d['spectrum'])
    FieldInterp = interpolate.interp1d(np.hstack(([0],d['lam'],[1e10])), np.hstack(([0],d['spectrum'],[0])),kind='linear')
    for mag,filter_,size in zip(mags,filters,sizes):
        new_spectrum = FieldInterp(wavelength/(1+val))
        mag[0].set_ydata(FieldInterp(wavelength/(1+val)).dot(filter_)/size  )
    plt.draw()
    d['z']=val
    return 
    
def hzfunc(label):
    print(label)
    if label=='Vega':
        filename='/tmp/Vega.sed'
        spec = fetch_vega_spectrum()
        lam = spec[0]
        spectrum = spec[1] / 2.1 / spec[1].max()
    else:
        if label=='Dale':
            filename=random.choice(glob.glob('/Users/Vincent/Nextcloud/LAM/Work/LePhare/lephare_200509/sed/GAL/DALE/*.sed'))
        if label=='COSMOS':
            filename=random.choice(glob.glob('/Users/Vincent/Nextcloud/LAM/Work/LePhare/lephare_200509/sed/GAL/COSMOS_MODIF/*.sed'))
        if label=='QSO':
            filename = random.choice(glob.glob('/Users/Vincent/Nextcloud/LAM/Work/LePhare/lephare_200509/sed/QSO/SALVATO2015/*.sed'))
        if label=='Star':
            filename = random.choice(glob.glob('/Users/Vincent/Nextcloud/LAM/Work/LePhare/lephare_200509/sed/STAR/PICKLES/*.sed'))
        if label=='COUPON':
            filename = random.choice(glob.glob('/Users/Vincent/Nextcloud/LAM/Work/LePhare/lephare_200509/sed/GAL/COUPON2015/*.out'))
        tab = Table.read(filename,format='ascii')
        lam = tab['col1']
        spectrum = tab['col2'] / 2.1 /  tab['col2'].max()
    d['lam'] =lam
    d['spectrum'] =spectrum
    l[0].set_data((1+d['z'])*lam, spectrum)
    l[0].set_label(os.path.basename(filename).split('.sed')[0].split('.out')[0])
    ax2.legend(loc='upper right')
    FieldInterp = interpolate.interp1d(np.hstack(([0],d['lam'],[1e10])), np.hstack(([0],d['spectrum'],[0])),kind='linear')
    for mag,filter_,size in zip(mags,filters,sizes):
        mag[0].set_ydata(FieldInterp(wavelength/(1+d['z'])).dot(filter_)/size  )
    plt.draw()
    return    
radio.on_clicked(hzfunc)
redshift_.on_changed(update)
#ax1.set_xlim(3000, 24000)
ax2.legend(loc='upper right')
ax2.set_ylim(0, 1.06)
ax1.set_xlim(1e3, 1e7)
ax1.set_xscale('log')
ax1.set_ylim(0,6)
ax1.xaxis.tick_top()
#ax1.set_xticklabels([])
#ax2.set_title('SDSS Filters and Reference Spectrum')
ax2.set_xlabel('Wavelength (Angstroms)')
ax2.set_ylabel('normalized flux / filter transmission')
ax1.set_ylabel('$\Delta mag$')
plt.tight_layout()
fig.subplots_adjust(bottom=0.15)
plt.show()