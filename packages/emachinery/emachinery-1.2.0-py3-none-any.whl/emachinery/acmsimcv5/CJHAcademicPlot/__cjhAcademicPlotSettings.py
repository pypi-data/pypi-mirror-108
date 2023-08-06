from dataclasses import dataclass
from pylab import plt, mpl, np
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset
from collections import OrderedDict as OD
import pandas as pd
import os
mpl.rcParams['legend.fontsize'] = 10
mpl.rcParams['font.family'] = ['serif'] # default is sans-serif
mpl.rcParams['font.serif'] = ['Times New Roman']
font = {'family':'Times New Roman', 'weight':'normal', 'size':10}

# plt.style.use('ggplot') 
# plt.style.use('grayscale') # print plt.style.available # get [u'dark_background', u'bmh', u'grayscale', u'ggplot', u'fivethirtyeight']
mpl.style.use('classic')


######################
# Data
def load_dataframe(path='./', index=0):

    df_list = []
    fname_list = []
    for fname in os.listdir(path):
        if '.dat' in fname and 'info' not in fname and 'pdf' not in fname:
            print('--------------', fname)
            fname_list.append(fname)
            df = pd.read_csv(path+fname, na_values = ['1.#QNAN', '-1#INF00', '-1#IND00'])
            df_list.append(df)

    # index = 0
    df    = df_list[index]
    fname = fname_list[index]
    no_samples = df.shape[0]
    no_traces  = df.shape[1]
    df_info = pd.read_csv(path+"info.dat", na_values = ['1.#QNAN', '-1#INF00', '-1#IND00'])
    time = np.arange(1,no_samples+1,1) * float(df_info['DOWN_SAMPLE']) * float(df_info['CL_TS'])  # sampling frequency is 10e3
    print('---- List of Keys:')
    for key in df.keys():
        print('\t', key)

    return df_list, time, fname

######################
# Plotting
def locallyZoomIn(ax, data_zoomed, ylim=None, loc1=None, loc2=None, y_axis_shrink=None, **kwarg):
    # extent = [-3, 4, -4, 3]

    if(y_axis_shrink!=None):
        temp_tuple = (ylim[0]*y_axis_shrink, ylim[1]*y_axis_shrink)
        ylim = temp_tuple
        for ind, el in enumerate(data_zoomed):
            temp_tuple = (el[0], el[1]*y_axis_shrink)
            data_zoomed[ind] = temp_tuple

    axins = zoomed_inset_axes(ax, **kwarg) # zoom = 
    # axins.plot(Z2, extent=extent, interpolation="nearest", origin="lower")
    for ind, el in enumerate(data_zoomed):
        if ind==1:
            if len(data_zoomed)>1:
                axins.plot(el[0],el[1], 'r-', alpha=0.7, linewidth=0.8) # '--'
            else:
                axins.plot(el[0],el[1], 'k-', alpha=0.7, lw=0.8)
        else:
            # axins.plot(*el, lw=2)
            axins.plot(el[0],el[1], lw=1)

    # sub region of the original image
    # x1, x2, y1, y2 = 1.2*pi, 1.25*pi, -0.78, -0.54
    # axins.set_xlim(x1, x2)
    # axins.set_ylim(y1, y2)

    if ylim!=None:
        axins.set_ylim(ylim)

    plt.xticks(np.arange(  axins.viewLim.intervalx[0],
                        axins.viewLim.intervalx[1],
                        axins.viewLim.width/2), visible=False)
    plt.yticks(np.arange(  axins.viewLim.intervaly[0],
                        axins.viewLim.intervaly[1],
                        axins.viewLim.height/4), visible=False)

    if(y_axis_shrink==None):
        # draw a bbox of the region of the inset axes in the parent axes and
        # connecting lines between the bbox and the inset axes area
        if loc1!=None and loc2!=None:
            mark_inset(ax, axins, loc1=loc1, loc2=loc2, fc="none", ec="0.5")
        else:
            mark_inset(ax, axins, loc1=2, loc2=3, fc="none", ec="0.5")
        plt.draw()
    return axins
def plot_it(ax, time, ylabel, OrDi, bool_legend=False):
    cnt_temp = 0
    for k, v in OrDi.items():
        cnt_temp += 1
        if cnt_temp == 2:
            ax.plot(time, v, 'r-', alpha=0.7, lw=0.8)
        elif cnt_temp == 3:
            print('A thrid trace is plotted in blue')
            ax.plot(time, v, 'b-', alpha=0.7, lw=0.8)
        else:
            ax.plot(time, v, 'k-', alpha=0.7, lw=0.8) # label=k
    if bool_legend:
        # ax.legend(loc='lower right', shadow=True)
        ax.legend(bbox_to_anchor=(1.08,0.5), borderaxespad=0., loc='center', shadow=True)
    ax.set_ylabel(ylabel, fontdict=font)
    # ax.set_xlim(0,35) # shared x
    # ax.set_ylim(0.85,1.45)

@dataclass
class CJHStylePlot():
    path2info_dot_dat: str
    nrows: int
    ncols: int          = 1
    sharex: bool        = True
    figsize: tuple      = (8, 9)
    facecolor: str      = 'w'
    edgecolor: str      = 'k'

    def __post_init__(self):
        # this is a directory   # this is path to a file
        self.dir2info_dot_dat = os.path.dirname(os.path.abspath(self.path2info_dot_dat)) + '/'
        print('path2info_dot_dat:', self.path2info_dot_dat)
        print('dir2info_dot_dat:', self.dir2info_dot_dat)

    def load(self):
        self.df_list, self.time, self.fname = load_dataframe(self.dir2info_dot_dat)
        return self.df_list, self.time, self.fname

    def plot(self, list_of_ylabel, list_of_signalNames, customize_plot=lambda axes_v:None, index=0):
        if self.df_list is None:
            self.load()

        df, time, fname = self.df_list[index], self.time, self.fname
        fig, axes_v = plt.subplots(  ncols=     self.ncols,
                                     nrows=     self.nrows,
                                     sharex=    self.sharex,
                                     figsize=   self.figsize,
                                     facecolor= self.facecolor,
                                     edgecolor= self.edgecolor,
                                   ); # modifying dpi would change the size of fonts
        # fig.subplots_adjust(wspace=0.01)

        for i, ylabel, signalNames in zip(range(self.nrows), list_of_ylabel, list_of_signalNames):
            ax = axes_v[i]
            OrDi = OD()
            for ind, signalName in enumerate(signalNames):
                OrDi[str(ind)] = df[signalName]
            plot_it(ax, time, ylabel, OrDi)

        for ax in axes_v:
            ax.grid(True)
            # ax.axvspan(14, 29, facecolor='r', alpha=0.1)
            ax.set_yticklabels([f'{el:g}' for el in ax.get_yticks()], font) # 为了修改ytick的字体  # https://matplotlib.org/3.3.3/api/_as_gen/matplotlib.axes.Axes.set_yticklabels.html

        # axes_v[-1].set_xlim((0,130))
        # axes_v[-1].set_xticks(np.arange(0, 201, 20))
        axes_v[-1].set_xlabel('Time, $t$ [s]', fontdict=font)
        axes_v[-1].set_xticklabels(axes_v[-1].get_xticks(), font)

        customize_plot(axes_v)

        # print(self.path2info_dot_dat)
        # print(fname[:-4])
        # print(fname)
        # fig.tight_layout() # tight layout is bad if you have too many subplots. Use bbox_inches instead
        path2outputFile = self.dir2info_dot_dat+fname[:-4] + f'-{index+1:03d}'
        fig.savefig(              f'{path2outputFile}.pdf', dpi=300, bbox_inches='tight', pad_inches=0)
        os.system('sumatrapdf ' + f'{path2outputFile}.pdf')
        os.system(f'pdfcrop         {path2outputFile}.pdf \
                                    {path2outputFile}-crop.pdf')
        # plt.show()

if __name__ == '__main__':
    # import emachinery
    # CJHStylePlot = emachinery.acmsimcv5.CJHAcademicPlot.__cjhAcademicPlotSettings.CJHStylePlot
    csp = CJHStylePlot( path2info_dot_dat=r'D:\DrH\Codes\emachineryTestPYPI\emachinery\acmsimcv5\dat\IM_Marino05_PI-Ohtani/info.dat', 
                        nrows=6)

    list_of_ylabel = [
      'Speed\n[rpm]',
      '$\\alpha$-axis Flux\n[Wb]',
      'Torque Current\n[A]',
      'Offset Voltage\n[V]',
      'Magn. Current\n[A]',
      'Load Torque\n[Nm]',
    ]

    list_of_signalNames = [
    ######################################
    ("ACM.rpm_cmd",
    "ACM.rpm",
    "marino.xOmg*ELEC_RAD_PER_SEC_2_RPM",
    ),
    ######################################
    ("ACM.psi_Amu",
    "ohtani.psi_2_real_output[0]",
    ),
    ######################################
    ("CTRL.I->iDQ_cmd[1]",
    # "ACM.iTs",
    "CTRL.I->iDQ[1]",
    ) ,
    ######################################
    ("ohtani.correction_integral_term[0]",
    "ohtani.correction_integral_term[1]",
    ) ,
    ######################################
    ("CTRL.I->iDQ_cmd[0]",
    # "ACM.iMs",
    "CTRL.I->iDQ[0]",
    ) ,
    ######################################
    ("ACM.TLoad",
    "marino.xTL",
    ),
    ]

    def customize_plot(axes_v):
        axes_v[0].set_ylim([-300, 300])
    csp.plot(list_of_ylabel, list_of_signalNames, customize_plot=customize_plot)

