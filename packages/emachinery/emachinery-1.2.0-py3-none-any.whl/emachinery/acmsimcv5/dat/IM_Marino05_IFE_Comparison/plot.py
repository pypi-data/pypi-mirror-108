if __name__ == '__main__':
    import os, sys; sys.path.insert(1, '../../CJHAcademicPlot'); 
    from __cjhAcademicPlotSettings import CJHStylePlot
    csp = CJHStylePlot(path2info_dot_dat=__file__, nrows=7)
    csp.load()
    """ Plot Menu
    Load Torque [Nm]
	Speed [rpm]
	Offset [V]
	Flux Alpha Error [Wb]
	Flux Alpha [Wb]
	Flux Ctrl Error [Wb]
	Speed Ctrl Error [rpm]
	['ACM.TLoad', 'marino.xTL', 'marino.xOmg*ELEC_RAD_PER_SEC_2_RPM', 'ACM.rpm', 'ACM.rpm_cmd', 'watch.offset[0]', 'watch.offset_compensation[0]', 'watch.offset[1]', 'watch.offset_compensation[1]', 'ACM.psi_Amu - watch.psi_2[0]', 'ACM.psi_Amu', 'watch.psi_2[0]', 'marino.e_psi_Dmu', 'marino.e_psi_Qmu', 'ACM.rpm - marino.xOmg*ELEC_RAD_PER_SEC_2_RPM']
	"""


    list_of_ylabel = [    "Load Torque [Nm]",
    "Speed [rpm]",
    "Offset [V]",
    "Flux Alpha Error [Wb]",
    "Flux Alpha [Wb]",
    "Flux Ctrl Error [Wb]",
    "Speed Ctrl Error [rpm]",
    ]

    list_of_signalNames = [
    	######################################
        ( 
			"ACM.TLoad",
			"marino.xTL",
        ),
        	######################################
        ( 
			"marino.xOmg*ELEC_RAD_PER_SEC_2_RPM",
			"ACM.rpm",
			"ACM.rpm_cmd",
        ),
        	######################################
        ( 
			"watch.offset[0]",
			"watch.offset_compensation[0]",
			"watch.offset[1]",
			"watch.offset_compensation[1]",
        ),
        	######################################
        ( 
			"ACM.psi_Amu - watch.psi_2[0]",
        ),
        	######################################
        ( 
			"ACM.psi_Amu",
			"watch.psi_2[0]",
        ),
        	######################################
        ( 
			"marino.e_psi_Dmu",
			"marino.e_psi_Qmu",
        ),
        	######################################
        ( 
			"ACM.rpm - marino.xOmg*ELEC_RAD_PER_SEC_2_RPM",
        ),
        ]

	csp.plot(list_of_ylabel, list_of_signalNames)