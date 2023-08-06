# import os, sys; sys.path.insert(1, '../../CJHAcademicPlot'); 
# from __cjhAcademicPlotSettings import CJHStylePlot

import emachinery
CJHStylePlot = emachinery.acmsimcv5.CJHAcademicPlot.__cjhAcademicPlotSettings.CJHStylePlot

if __name__ == '__main__':
    csp = CJHStylePlot(path2info_dot_dat=__file__, nrows=6)
    csp.load()
    quit()
'''
# ---- List of Keys:
#      ACM.rpm_cmd
#      marino.xOmg*ELEC_RAD_PER_SEC_2_RPM
#      ACM.rpm
#      CTRL.I->cmd_psi
#      ACM.psi_Dmu
#      marino.psi_Dmu
#      marino.e_psi_Dmu
#      marino.e_psi_Qmu
#      ACM.TLoad
#      marino.xTL
#      ACM.iMs-ACM.psi_Dmu/ACM.Lmu
#      CTRL.I->iDQ_cmd[0]-CTRL.I->cmd_psi/CTRL.motor->Lmu
#      ACM.psi_Bmu
#      clest.psi_2[1]
#      -clest.correction_integral_term[0]
#      htz.u_off[0]
#      htz.u_off_calculated_increment[0]
#      -clest.correction_integral_term[1]
#      htz.u_off[1]
#      htz.u_off_calculated_increment[1]
#      ACM.psi_Amu
#      htz.psi_2[0]
#      htz.psi_2_min[0]
#      htz.psi_2_max[0]
#      ACM.psi_Amu - htz.psi_2[0]
#      ACM.psi_Dmu.1
#      htz.psi_2_ampl
#      0.5*(htz.psi_2_min[0] + htz.psi_2_max[0])
#      htz.Delta_t
#      htz.Delta_t_last
#      htz.sat_max_time[0]
#      htz.sat_min_time[0]
#      htz.extra_limit
'''

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
