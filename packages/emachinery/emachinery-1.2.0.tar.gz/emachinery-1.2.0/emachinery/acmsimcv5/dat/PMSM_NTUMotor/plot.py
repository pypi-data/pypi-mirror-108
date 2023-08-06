if __name__ == '__main__':
    import os, sys; sys.path.insert(1, '../../CJHAcademicPlot'); 
    from __cjhAcademicPlotSettings import CJHStylePlot
    csp = CJHStylePlot(path2info_dot_dat=__file__, nrows=10)
    csp.load()
    """ Plot Menu
    Speed [rpm]
	Position [rad]
	Position error [1]
	No title 0
	No title 1
	No title 2
	No title 3
	No title 4
	No title 5
	No title 6
	['ACM.rpm_cmd', 'CTRL.I->rpm', 'CTRL.I->theta_d_elec', 'huwu.theta_d', 'sin(CTRL.I->theta_d_elec-huwu.theta_d)', 'huwu.x[0]', 'huwu.x[1]', 'huwu.x[2]', 'huwu.inner_product_normalized', 'CTRL.I->idq_cmd[0]', 'CTRL.I->idq[0]', 'CTRL.I->idq_cmd[1]', 'CTRL.I->idq[1]', 'huwu.stator_flux_ampl_limited', 'huwu.active_flux_ampl_limited']
	"""


    list_of_ylabel = [    "Speed [rpm]",
    "Position [rad]",
    "Position error [1]",
    "No title 0",
    "No title 1",
    "No title 2",
    "No title 3",
    "No title 4",
    "No title 5",
    "No title 6",
    ]

    list_of_signalNames = [
    	######################################
        ( 
			"ACM.rpm_cmd",
			"CTRL.I->rpm",
        ),
        	######################################
        ( 
			"CTRL.I->theta_d_elec",
			"huwu.theta_d",
        ),
        	######################################
        ( 
			"sin(CTRL.I->theta_d_elec-huwu.theta_d)",
        ),
        	######################################
        ( 
			"huwu.x[0]",
        ),
        	######################################
        ( 
			"huwu.x[1]",
        ),
        	######################################
        ( 
			"huwu.x[2]",
        ),
        	######################################
        ( 
			"huwu.inner_product_normalized",
        ),
        	######################################
        ( 
			"CTRL.I->idq_cmd[0]",
			"CTRL.I->idq[0]",
        ),
        	######################################
        ( 
			"CTRL.I->idq_cmd[1]",
			"CTRL.I->idq[1]",
        ),
        	######################################
        ( 
			"huwu.stator_flux_ampl_limited",
			"huwu.active_flux_ampl_limited",
        ),
        ]

    csp.plot(list_of_ylabel, list_of_signalNames, index=0)