import os, sys; sys.path.insert(1, '../../CJHAcademicPlot'); 

from __cjhAcademicPlotSettings import CJHStylePlot

if __name__ == '__main__':
    csp = CJHStylePlot(path2info_dot_dat=__file__, nrows=6)

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

    csp.plot(list_of_ylabel, list_of_signalNames)

# Obsolete 
if __name__ == '!__main__':
    from __cjhAcademicPlotSettings import *

    df, time, fname = load_dataframe(os.path.dirname(os.path.abspath(__file__)))
    fig, axes_v = plt.subplots(ncols=1, nrows=6, sharex=True, figsize=(8,9), facecolor='w', edgecolor='k'); # modifying dpi would change the size of fonts
    # fig.subplots_adjust(wspace=0.01)

    i =0; ax = axes_v[i]; plot_it(ax, time, 'Speed\n[rpm]', OD([ 
               (r'$\omega^*$',             df["ACM.rpm_cmd"]),
               (r'$\omega$',               df["ACM.rpm"]),
               (r'$\hat\omega$',           df["marino.xOmg*ELEC_RAD_PER_SEC_2_RPM"]),
             ]))      
    i+=1; ax = axes_v[i]; plot_it(ax, time, '$\\alpha$-axis Flux\n[Wb]', OD([ 
               (r'$T_L$',                  df["ACM.psi_Amu"]),
               (r'$\hat T_L$',             df["ohtani.psi_2_real_output[0]"]),
             ]))
    i+=1; ax = axes_v[i]; plot_it(ax, time, 'Torque Current\n[A]', OD([ 
               (r'1',             df["CTRL.I->iDQ_cmd[1]"]),
               # (r'2',             df["ACM.iTs"]),
               (r'3',             df["CTRL.I->iDQ[1]"]),
             ]))
    i+=1; ax = axes_v[i]; plot_it(ax, time, 'Offset Voltage\n[V]', OD([ 
               (r'$\hat u_{\alpha,\mathrm{offset}}$', df["ohtani.correction_integral_term[0]"]),
               (r'$\hat u_{\beta,\mathrm{offset}}$',  df["ohtani.correction_integral_term[1]"]),
             ]))
    i+=1; ax = axes_v[i]; plot_it(ax, time, 'Magn. Current\n[A]', OD([ 
               (r'1',             df["CTRL.I->iDQ_cmd[0]"]),
               # (r'2',             df["ACM.iMs"]),
               (r'3',             df["CTRL.I->iDQ[0]"]),
             ]))
    i+=1; ax = axes_v[i]; plot_it(ax, time, 'Load Torque\n[Nm]', OD([ 
               (r'$T_L$',                  df["ACM.TLoad"]),
               (r'$\hat T_L$',             df["marino.xTL"]),
             ]))

    for ax in axes_v:
        ax.grid(True)
        # ax.axvspan(14, 29, facecolor='r', alpha=0.1)
        ax.set_yticklabels([f'{el:g}' for el in ax.get_yticks()], font) # https://matplotlib.org/3.3.3/api/_as_gen/matplotlib.axes.Axes.set_yticklabels.html

    # axes_v[-1].set_xlim((0,130))
    # axes_v[-1].set_xticks(np.arange(0, 201, 20))
    axes_v[-1].set_xlabel('Time, $t$ [s]', fontdict=font)
    axes_v[-1].set_xticklabels(axes_v[-1].get_xticks(), font)

    # fig.tight_layout() # tight layout is bad if you have too many subplots
    fig.savefig(              f'{fname[:-4]}.pdf', dpi=300, bbox_inches='tight', pad_inches=0)
    os.system('sumatrapdf ' + f'{fname[:-4]}.pdf')
    # plt.show()

