#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 21:46:30 2019

@author: john.onwuemeka; Ge Li
"""
import matplotlib.transforms as transforms
from matplotlib.ticker import MaxNLocator, LogLocator
import matplotlib.pyplot as plt
import numpy as np
from ..handlers.save_output import save_output
from ..optimizer.fit_sin_spec import fit_sin_spec
from ..optimizer.fit_sin_spec_pll import fit_sin_spec_pll
from ..optimizer.sinspec_model import sinspec_model
from matplotlib import colors as clors


def colorlist(numspec):
    if numspec < 27:
        colortype = [ 'r', 'y','skyblue','rebeccapurple','peru','sienna',\
                     'indigo','purple','pink','palevioletred','turquoise',\
                     'coral','tomato','lightsteelblue','teal','firebrick',\
                     'orchid','olivedrab','bisque','thistle','orangered',\
                     'darkcyan','wheat','azure','salmon','linen']
    else:
        colors = dict(clors.BASE_COLORS, **clors.CSS4_COLORS)
        hsv_sort = sorted((tuple(clors.rgb_to_hsv(clors.to_rgba(color)[:3])),
                           name)
                for name, color in colors.items())
        colortype = list(set([name for hsv, name in hsv_sort]))
    return colortype

def plot_waveform(self,stn,nsstart,Ptime,Stime,time_win,evtype,axz,wv):

    '''
    This is used to plot waveforms of the event pairs shown in the
    spectral ratio figure.

    Input:
    -------
    stn      --> event waveforms (3-components if available)
    nsstart  --> noise start time (UTC)
    Ptime    --> P-phase arrival time (UTC)
    Stime    --> S-phase arrival time (UTC)
    time_win --> Time window length (seconds)
    evtype   --> event type (main or egf)
    axz      --> figure axes of the spectral ratio plot
    wv       --> wave type (P or S)

    Return:
    --------
    None
    '''

    if axz:
        if wv.upper() == 'S':
            tr = stn.select(component= 'T')[0]
        elif wv.upper() == 'P':
            tr = stn.select(component='Z')[0]
        nsstart = nsstart - tr.stats.starttime
        axz.plot(tr.times(reftime = tr.stats.starttime) , tr.data, "k-",
                 label = tr.stats.channel)
        axz.set_ylabel('Velocity (m/s)',fontsize = 23,fontweight='bold')
        leg = axz.legend(loc=3,fontsize = 18,handlelength=0, handletextpad=0)
        for item in leg.legendHandles:
            item.set_visible(False)
        axz.annotate("", xy=(nsstart, max(tr.data)*0.15),
                     xytext=(time_win+nsstart, max(tr.data)*0.15),
                         arrowprops=dict(arrowstyle="<->",facecolor='k'))
        axz.text(nsstart+(time_win*0.3), 0.65,'Ns',fontsize=20,
                 fontweight='bold',
                 transform=transforms.blended_transform_factory(axz.transData,
                                                                axz.transAxes))
        if Stime and self.wvtype2 == 'S':
            Stimex = Stime - tr.stats.starttime
            axz.text(Stimex - 0.85, max(tr.data)*0.7,'S',fontsize=22,
                     fontweight='bold')
            axz.annotate("", xy=(Stimex - 0.55, max(tr.data)*0.75),
                         xytext=(Stimex - 0.15, max(tr.data)*0.20),
                         arrowprops=dict(arrowstyle="<-",facecolor='k',
                                         connectionstyle="arc3"))
        if Ptime and self.wvtype1 == 'P':
            Ptimex = Ptime - tr.stats.starttime
            axz.text(Ptimex - 0.85, max(tr.data)*0.5,'P',fontsize=22,
                     fontweight='bold')
            axz.annotate("", xy=(Ptimex - 0.55, max(tr.data)*0.55),
                         xytext=(Ptimex - 0.15, max(tr.data)*0.05),
                         arrowprops=dict(arrowstyle="<-",facecolor='k',
                                         connectionstyle="arc3"))
        axz.tick_params(axis='both',which='both',length=5.,labelsize='large')
        axz.get_yaxis().get_major_formatter().set_powerlimits((0, 0))
        for tick in axz.yaxis.get_major_ticks():
            tick.label.set_fontsize(24)
        for tick in axz.xaxis.get_major_ticks():
            tick.label.set_fontsize(24)
        axz.set_xlim([0,max(tr.times(reftime = tr.stats.starttime))])
        axz.yaxis.get_offset_text().set_fontsize(24)
        axz.set_xlabel('Time (s)',fontsize = 26,fontweight='bold')
        if evtype[0] == 'e':
            axz.set_title('%s' % ('Auxiliary event'),fontweight='bold',
                          fontsize=22)
            axz.text(0.2,0.10,tr.stats.station.strip(),fontsize=22,
                     fontweight='bold',transform=axz.transAxes)
        else:
            axz.set_title('%s' % ('Main event'),fontweight='bold',fontsize=22)
            axz.set_title('%s%s' % (evtype.capitalize(),' event'),
                          fontweight='bold',fontsize=22)
        axz.text(0.2,0.10,stn[0].stats.station.strip(),fontsize=22,
                 fontweight='bold',transform=axz.transAxes)
        axz.yaxis.set_major_locator(MaxNLocator(integer=True,nbins=3))
        axz.xaxis.set_major_locator(MaxNLocator(integer=True,nbins=5))
    return None

def make_figures_spec(self,specmain,freqmain,wmfc,wm,wmn,wefc,we,wen,indexx,
                      time_win,mainfile,egffile,wv):

    '''
    Function for creating and organizing the spectra ratio plots.
    All the subplots (axes) are initiated and organized here.
    '''

    from obspy.core import read
    from ..analyzer import get_sig_nois_data
    lste = list(specmain.keys())
    colortype = colorlist(len(lste))
    fig = plt.figure(1,figsize=(16,9),tight_layout=True)
    fig.subplots_adjust(hspace = .2,wspace=0.1)
    ax_spec = plt.subplot2grid((3, 2), (1, 1), rowspan = 2,colspan = 1)
    axx = plt.subplot2grid((3, 2), (1, 0), rowspan = 2)
    colornum = 0
    Ptime,Stime = None,None
    if indexx:
        et1 = egffile[indexx]
        axs = plt.subplot2grid((3, 2), (0, 1))
        st = read(et1)
        if self.S_tt[self.egfev]:
            for i in self.S_tt[self.egfev]:
                if i[1] == st[0].stats.station.strip():
                    Stime = i[0]
        if self.P_tt[self.egfev]:
            for i in self.P_tt[self.egfev]:
                if i[1] == st[0].stats.station.strip():
                    Ptime = i[0]
        origtime = self.evlist[self.egfev][0]
        baz = self.baz['egf']
        if baz < 0:
            baz = baz + 360
        _,_,nsstart,stn,_ = get_sig_nois_data(self,et1,origtime,Ptime,Stime,
                                              time_win,True,None,self.egfev,
                                              baz,'yes')
        trn = stn.select(component='N')
        trn += stn.select(component='E')
        trn.rotate('NE->RT',back_azimuth=baz)
        stn[1] = trn[1]
        plot_waveform(self,stn,nsstart,Ptime,Stime,time_win,'egf',axs,wv)
        et2 = mainfile[indexx]
        if self.S_tt[self.mainev]:
            for i in self.S_tt[self.mainev]:
                if i[1] == st[0].stats.station.strip():
                    Stime = i[0]
        if self.P_tt[self.mainev]:
            for i in self.P_tt[self.mainev]:
                if i[1] == st[0].stats.station.strip():
                    Ptime = i[0]
        origtime = self.evlist[self.mainev][0]
        baz = self.baz['main']
        if baz < 0:
            baz = baz + 360
        _,_,nsstart,stn,_ = get_sig_nois_data(self,et2,origtime,Ptime,Stime,
                                              time_win,True,None,self.mainev,
                                              baz,'yes')
        trn = stn.select(component='N')
        trn += stn.select(component='E')
        trn.rotate('NE->RT',back_azimuth=baz)
        stn[1] = trn[1]
        axs = plt.subplot2grid((3, 2), (0, 0))
        plot_waveform(self,stn,nsstart,Ptime,Stime,time_win,'main',axs,wv)
    for index in range(len(lste)):
        station=lste[index]
        ax_spec.loglog(freqmain[lste[index]],specmain[lste[index]],
                       linewidth = 1,color = colortype[colornum],
                       label = station)
        if lste[index] == indexx:
            if freqmain[indexx][0] == 0:
                x_begin = freqmain[indexx][1]
            else:
                x_begin = freqmain[indexx][0]
            try:
                x_end = self.stationlist[indexx]['pre_filt'][2]
            except:
                x_end = 45.
                pass
            ploting(x1 = wmfc[indexx],y1 = wm[indexx],y12 = wmn[indexx],
                    x2 = wefc[indexx],
                    y2 = we[indexx],y22 = wen[indexx],ax = axx,
                    station = station,color = colortype[colornum],
                    x_begin=x_begin,x_end=x_end,wv=wv)
#            xlim1 = 10**(np.floor(np.log10(x_begin)))
            ax_spec.set_xlim([x_begin,x_end])
        colornum += 1
    return fig,ax_spec

def ploting(x1,y1,y12,x2,y2,y22,ax,station,color,x_begin,x_end,wv):

    '''
    Handles example event pair plot shown on the bottom left of
    the spectral ratio figure. This figures gives an idea of the SNR for the
    example events
    '''

    ax.loglog(x1,y1,linewidth = 3, label =  'Main event',color = color ) # Main event
    ax.loglog(x1,y12,linewidth = 2,ls='--', alpha=0.7,
              label =  'Main event noise',color=color)
    ax.loglog(x2,y2,linewidth = 2, ls='-',label =  'Auxiliary event',
              color='darkgray') #EGFs for single EGF analysis
    ax.loglog(x2,y22,linewidth = 1.5,ls='-.',label =  'Auxiliary event noise',
              color='lightgray')
    ax.text(0.7,0.1,'%s wave' % wv,style = 'normal',weight='bold',size=16,
            transform=ax.transAxes)

    ax.text(0.7,0.9,station,style = 'normal',weight='bold',size=18,
            transform = ax.transAxes)
    ax.set_xlim([x_begin,x_end])
    ax.set_ylim([y22[-1]*0.5,max(y1)*10])
    ax.yaxis.set_major_locator(LogLocator(base=10.0, numticks=5))
    ax.set_xlabel('Frequency (Hz)',fontsize=24,fontweight='bold')
    ax.set_ylabel('Amplitude (nm/Hz)',fontsize=24,fontweight='bold')
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(20)
    ax.get_xaxis().get_major_formatter().labelOnlyBase = True
    ax.get_xaxis().get_minor_formatter().labelOnlyBase = False
    ax.tick_params(axis='x',which='minor',bottom='on')
    ax.tick_params(axis='both',which='both',length=4.0)
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(20)
    ax.legend(loc='lower left',ncol=1,prop={'size':17})
    return None

def specrat_fit_plot(self,freqbin,specratio,mtpl,freqperturb,
                     allresidua1,ax,popt,maxy):

    '''
    Function to create the bottom right figure (axes) of the spectral
    ratio plot. Individual spectral ratios of each station and the
    representative spectral ratio for the event pair is organised and plotted
    by this function.
    '''

    from mpl_toolkits.axes_grid1.inset_locator import inset_axes
    from ..optimizer import specr_model
    mtpl = mtpl
    specratio = np.multiply(specratio,mtpl,dtype=float)
    residua = np.power(np.subtract(specratio,specr_model(freqbin, *popt)),2)
    residua = np.power(np.subtract(specratio,specr_model(freqbin, *popt)),2)
    normresidua = np.sqrt(np.sum(residua)/np.sum(np.power(specratio,2)))
    if popt.any():
        ax.loglog(freqbin,np.divide(specr_model(freqbin, *popt),mtpl),
                  'g--', label='model fit',linewidth = 5)
        ax.text(0.55,0.1,'M$_L$$_($$_1$$_)$ = %s' % self.evlist[self.mainev][1][3],
                style = 'normal',weight='bold',size=14,transform=ax.transAxes)
        ax.text(0.55,0.05,'M$_L$$_($$_2$$_)$ = %s' % self.evlist[self.egfev][1][3],
                style = 'normal',weight='bold',size=14,transform=ax.transAxes)
        ax.text(0.55,0.15,'rms = %.2f' %(normresidua),style = 'normal',
                weight='bold',size=14,transform=ax.transAxes)

        try:
            xbin = np.where(freqbin >= popt[0])[0][0]
            ybin = np.divide(specr_model(freqbin, *popt),mtpl)[xbin]
            ax.text(popt[0]*0.95,ybin*1.25,'f$_c$$_($$_1$$_)$ =  %s' \
                    %(float(round(popt[0],1))),style = 'normal',
                    weight='bold',size=14)
            ax.loglog(popt[0]*1.0,ybin*1.12,marker="v",color='green',
                      markersize=10)
            if self.showfc2.upper() == 'YES':
                xbin2 = np.where(freqbin >= popt[1])[0][0]
                ybin2 = np.divide(specr_model(freqbin, *popt),mtpl)[xbin2]
                ax.text(popt[1]*0.55,ybin2*0.7,'f$_c$$_($$_2$$_)$ =  %s' \
                        %(float(round(popt[1],1))),style = 'normal',
                        weight='bold',size=14)
                ax.loglog(popt[1],ybin2*0.9,marker="^",color='green',
                          markersize=10)
        except:
            pass
        upl = 10**(np.floor(np.log10(maxy*10)))
        upl1 = 10**(np.floor(np.log10(maxy)))
        if upl/upl1 > 20:
           upl = 10**(np.floor(np.log10(maxy*10)))
        ax.set_ylim([min(specratio)*0.15/mtpl,upl*3])#0.025
        ax.get_xaxis().get_major_formatter().labelOnlyBase = True
        ax.get_xaxis().get_minor_formatter().labelOnlyBase = True
        ax.set_xlabel('Frequency (Hz)',fontsize = 24,fontweight='bold')
        ax.set_ylabel('Spectral Ratio',fontsize = 24,fontweight='bold')
        ax.legend(loc='upper left',ncol=1,prop={'size':20})
        ax.tick_params(axis='both',which='both',length=5.)
        for tick in ax.xaxis.get_major_ticks():
             tick.label.set_fontsize(20)
        for tick in ax.yaxis.get_major_ticks():
             tick.label.set_fontsize(20)
        if ax:
            inset_axin = inset_axes(ax,
                                    width="30%",
                                    height="25%",
                                    loc=3,
                                    borderpad=4.8)
            tempx = []; tempy = []
            for h in range(len(freqperturb)):
                if allresidua1[h] < 0.57:
                    tempy.append(allresidua1[h])
                    tempx.append(freqperturb[h])
            index1 = np.where(allresidua1 == min(allresidua1))[0][0]
            y1 = allresidua1[index1]
            x1 = freqperturb[index1]
            inset_axin.semilogx(tempx,tempy,'o',ms=3,mfc = 'blue')
            inset_axin.semilogx(x1,y1,'*',mfc='blue',ms=8,mec='red')
            bb = np.floor(np.log10(min(tempx)))#.round()-1
            inset_axin.set_xlim([(10**bb)*5,max(tempx)*2])
            inset_axin.xaxis.set_major_locator(LogLocator(base=10.0, numticks=3))
            inset_axin.set_ylim([0,0.6])
            inset_axin.set_yticks(np.linspace(0,0.6,endpoint=True,num=4))
            inset_axin.set_xlabel('Corner Frequency (Hz)',fontsize = 13,fontweight='bold')
            inset_axin.set_ylabel('RMS',fontsize = 13,fontweight='bold')
            inset_axin.get_xaxis().get_major_formatter().labelOnlyBase = True
            inset_axin.get_xaxis().get_minor_formatter().labelOnlyBase = True
            inset_axin.tick_params(axis='both',which='both',length=3.5)
            for tick in inset_axin.xaxis.get_major_ticks():
                tick.label.set_fontsize(11)
            for tick in inset_axin.yaxis.get_major_ticks():
                tick.label.set_fontsize(11)
        ax.legend(loc='upper right',ncol=4,prop={'size':11})
    return None

def make_figures_ind(self,wm,wmfc,wmn,trtm,wv):
    '''
    Handler for individual spectra analysis spectral fitting and figure
    creation.

    Input:
    -------
    wm   --> individual signal spectra
    wmfc --> individual signal spectra frequency bins
    wmn  --> individual noise spectra
    trtm --> Travel times of the events contained in wm
    wv   --> wave type (P or S)

    Returns:
    ---------
    It returns None but fits individual spectra and dispatches spectrum
    fitting results.
    '''

    colornum = 0
    fig = plt.figure(figsize=(16,10),tight_layout=True)
    lste = list(wm.keys())
    colortype = colorlist(len(lste))
    n = 1; m = 1
    for index in range(len(lste)):
        station = lste[index]
        fn = wmfc[lste[index]]
        try:
            if self.numworkers <= 1:
                popt_ind,pcov_ind = fit_sin_spec(wm[lste[index]],fn,station,
                                             min(wmfc[lste[index]]),
                                             max(wmfc[lste[index]])*2.5,
                                             trtm[lste[index]],
                                             self.autofit_single_spec,
                                             self.source_model)
            elif self.numworkers > 1:
                popt_ind,pcov_ind = fit_sin_spec_pll(wm[lste[index]],fn,station,
                                             min(wmfc[lste[index]]),
                                             max(wmfc[lste[index]])*2.5,
                                             trtm[lste[index]],
                                             self.source_model,self.numworkers)
        
            axx2 = fig.add_subplot(2,3,n)
            if fn[0] == 0:
                bb = fn[1]
            else:
                bb = fn[0]
    #        bb = np.floor(np.log10(min(fn)))
            x_end = self.stationlist[station]['pre_filt'][2]
            axx2.set_xlim([bb,x_end])
            fig.subplots_adjust(hspace = .2,wspace = 0.0)
            dlim = int(min(len(wmfc[lste[index]]),len(wmn[lste[index]])) - 1)
            axx2.loglog(wmfc[lste[index]][0:dlim],wm[lste[index]][0:dlim],linewidth = 1,color = colortype[colornum],label = 'data')
            axx2.loglog(fn, sinspec_model(fn, *popt_ind), 'k--', label='model fit',
                        linewidth=2)
            axx2.loglog(wmfc[lste[index]][0:dlim],wmn[lste[index]][0:dlim],linewidth = 1,color = 'gray',alpha = 0.6,label = 'noise')
            axx2.get_xaxis().get_major_formatter().labelOnlyBase = True
            axx2.get_xaxis().get_minor_formatter().labelOnlyBase = False
            axx2.tick_params(axis='x',which='minor',bottom='on')
            axx2.tick_params(labelsize='large')
            for tick in axx2.xaxis.get_major_ticks():
                tick.label.set_fontsize(20)
            for tick in axx2.yaxis.get_major_ticks():
                tick.label.set_fontsize(20)
            axx2.set_xlabel('Frequency (Hz)',fontsize=24)
            axx2.set_ylabel('Amplitude (nm/Hz)',fontsize=24)
            axx2.legend(loc='lower left',ncol=1,prop={'size':18})
            axx2.text(0.2, 0.5, station,fontsize=20, horizontalalignment='center',verticalalignment='center', transform=axx2.transAxes)
            lm,hm = axx2.get_ylim()
            axx2.set_ylim([lm,hm*10])
            try:
                xbin = np.where(fn >= popt_ind[1])[0][0]
            except:
                fig.delaxes(fig.axes[len(fig.axes)-1])
                pass
            axx2.text(popt_ind[1]*.8,wm[lste[index]][xbin]*1.8,'f$_c$ =  %s' %(float(round(popt_ind[1],1))),style = 'normal',weight='bold',size=17)
            axx2.loglog(popt_ind[1],wm[lste[index]][xbin]*1.2,marker="v",color='green',markersize=10)
            axx2.yaxis.set_major_locator(LogLocator(base=10.0, numticks=4))
            axx2.text(0.6,0.2,'%s wave' % wv,style = 'normal',weight='bold',size=16,transform=axx2.transAxes)
            colornum += 1
            if pcov_ind[0] is not None:
                save_output(self,None,None, None,popt_ind, pcov_ind,station,wv)
#            popt_ind,pcov_ind = [],[]
            n = len(fig.axes)+1
            if n > 6:
                save_fig(self,fig,'ind', m,wv)
                plt.close()
                fig = plt.figure(figsize=(16,10),tight_layout=True)
                n = 1
                m += 1
        except:
            pass
    try:
        if fig.axes[0]:
            save_fig(self,fig,'ind',m,wv)
            plt.close()
    except:
        pass
    return None


def stf_plot(self,x,y,wv):

    '''
    Designed to handle source time function plots but this option is not
    yet activated, stay tuned!
    '''

#    y = [i*np.sign(i) for i in y]
    fig = plt.figure(figsize=(6,3))
    ax = fig.add_subplot(111)
    ax.plot(x,y,'k',linewidth=1.5)
    ax.set_xlabel('Time (s)',fontsize=20)
    ax.fill_between(x, y, facecolor='gray', alpha=0.5)
    for tick in ax.xaxis.get_major_ticks():tick.label.set_fontsize(18)
    for tick in ax.yaxis.get_major_ticks():tick.label.set_fontsize(18)
    save_fig(self,fig,'stf',None,wv)
    return None


def save_fig(self,fig,figtype,mm,wv):

    '''
    All created figures are saved to by this function. The default dpi
    for each figure is 300.
    '''

    if figtype == 'spec':
        fig.subplots_adjust(hspace = .1,wspace=0.1)
        fig.tight_layout()
        imagefile = self.output_dir+self.mainev+'_'+self.egfev+'_'+wv+'_'+str(mm)+'.pdf'
        fig.savefig(imagefile, format='pdf', dpi=300)
        fig.clf()
    if figtype == 'ind':
        imagefile = self.output_dir+self.mainev+'_sinspec_'+wv+'_'+str(mm)+'.pdf'
        fig.savefig(imagefile, format='pdf', dpi=300)
        fig.clf()
    if figtype == 'stf':
        imagefile = self.output_dir+self.mainev+'_'+self.egfev+'_'+wv+'_STF.pdf'
        fig.savefig(imagefile, format='pdf', dpi=300)
        fig.clf()
    return None
