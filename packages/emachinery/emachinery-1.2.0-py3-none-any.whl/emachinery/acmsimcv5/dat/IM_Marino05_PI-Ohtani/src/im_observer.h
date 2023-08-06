#ifndef ADD_IM_OBSERVER_H
#define ADD_IM_OBSERVER_H
#if MACHINE_TYPE == 1 || MACHINE_TYPE == 11

/* Macro for External Access Interface */
#define US(X)   rk4.us[X]
#define IS(X)   rk4.is[X]
#define US_C(X) rk4.us_curr[X]
#define IS_C(X) rk4.is_curr[X]
#define US_P(X) rk4.us_prev[X]
#define IS_P(X) rk4.is_prev[X]

struct RK4_DATA{
    REAL us[2];
    REAL is[2];
    REAL us_curr[2];
    REAL is_curr[2];
    REAL us_prev[2];
    REAL is_prev[2];

    // REAL omg_elec;

};
extern struct RK4_DATA rk4;

struct ObserverControl{
    
    REAL k_AP_I;
    REAL k_AP_P;
    REAL k_AP_D;
    REAL k_RP_I;
    REAL k_RP_P;
    REAL k_RP_D;

    REAL xIs[2];    // \psi_\sigma
    REAL xPsiMu[2];       // \psi_\mu
    REAL xOmg;
    REAL xTL; 
    REAL xTL_integral_part_AP; 
    REAL xTL_integral_part_RP; 
    REAL xTem;
    // REAL refined_omg;
    REAL actual_iTs;

    REAL xUps_al[6];     // The alpha component of the filtered regressors
    REAL xUps_be[6];     // The beta component of the filtered regressors
    REAL xTheta[2]; 

    REAL mismatch[3];
    REAL error[2];
    REAL varepsilon_AP;
    REAL varepsilon_RP;

    REAL epsilon_AP; // estimate of varepsilon
    REAL varsigma_AP; // estimate of dot varepsilon
    REAL epsilon_RP; // estimate of varepsilon
    REAL varsigma_RP; // estimate of dot varepsilon
    REAL lambda1;
    REAL lambda2;

    REAL taao_alpha; 
    REAL taao_omg_integralPart; // 纯积分的自适应律就用不到这个
    REAL taao_speed; // 机械速度rpm！再强调一遍，不是电气速度rpm，而是机械速度rpm。

    REAL timebase;
    REAL Ts;

    REAL omega_e;
    REAL Tem;

    REAL taao_flux_cmd;
    int taao_flux_cmd_on;

    REAL cosT;
    REAL sinT;
    REAL theta_M;

    REAL actual_flux[2];
    REAL actual_TL;
    REAL actual_z;

    REAL k_Gopinath;
    REAL k_1minusGopinath_inv;
    REAL xXi[2];
};
extern struct ObserverControl ob;

void rk4_init();
void observer_init();
void simulation_only_flux_estimator();
void observer_marino2005();





/********************************************
/* Collections of VM based Flux Estimators 
/********************************************/

struct Holtz_Variables{
    double emf_stator[2];

    double psi_1[2];
    double psi_2[2];
    double psi_2_prev[2];

    double psi_1_nonSat[2];
    double psi_2_nonSat[2];

    double psi_1_min[2];
    double psi_1_max[2];
    double psi_2_min[2];
    double psi_2_max[2];

    double rs_est;
    double rreq_est;

    double Delta_t;
    double u_off[2];
    double u_off_integral_input[2];
    double gain_off;

    int    flag_pos2negLevelA[2];
    int    flag_pos2negLevelB[2];
    double time_pos2neg[2];
    double time_pos2neg_prev[2];

    int    flag_neg2posLevelA[2];
    int    flag_neg2posLevelB[2];
    double time_neg2pos[2];
    double time_neg2pos_prev[2];

    double psi_aster_max;

    double sat_min_time[2];
    double sat_max_time[2];
    double sat_min_time_reg[2];
    double sat_max_time_reg[2];
    double extra_limit;
    int flag_limit_too_low;

    // double ireq[2];
    double field_speed_est;
    double omg_est;
    double slip_est;
};
extern struct Holtz_Variables htz;

struct Variables_Ohtani1990{
    // D-Q
    REAL psi_DQ1[2];
    REAL psi_DQ2[2];
    REAL psi_DQ2_prev[2];

    // alpha-beta
    REAL psi_1[2];
    REAL psi_2[2];

    REAL psi_2_prev[2];
    REAL psi_2_pprev[2];

    // sum_up_method
        // TOP
        int flag_top2top[2];
        REAL last_time_reaching_top[2];
        REAL Delta_time_top2top[2];
        REAL change_in_psi_2_top[2];
        REAL psi_2_last_top[2];
        REAL u_offset_estimated_by_psi_2_top_change[2];

        // BUTT
        int flag_butt2butt[2];
        REAL last_time_reaching_butt[2];
        REAL Delta_time_butt2butt[2];
        REAL change_in_psi_2_butt[2];
        REAL psi_2_last_butt[2];
        REAL u_offset_estimated_by_psi_2_butt_change[2];

        REAL u_offset[2];
        REAL offset_voltage_compensation[2];

        REAL first_time_enter_top[2];
        REAL first_time_enter_butt[2];

        // 这个没用！
        // REAL top2top_sum[2];
        REAL top2top_count[2];
        // REAL psi_2_offset[2];
        // REAL u_offset_estimated_by_psi_2_sumup[2];

        REAL butt2butt_count[2];

        REAL filtered_compensation[2]; // psi_offset
        REAL filtered_compensation2[2];
        REAL u_offset_estimated_by_top_minus_butt[2];
        REAL u_offset_estimated_by_integration_correction[2];
        REAL u_offset_error[2];

        REAL bool_compensate_psi_offset[2];

        REAL psi_2_real_output[2];

        REAL psi_2_output[2];
        REAL psi_2_output2[2];
        REAL psi_2_output_last_top[2];
        REAL psi_2_output2_last_top[2];
        REAL psi_2_output_last_butt[2];
        REAL psi_2_output2_last_butt[2];

        REAL current_Lissa_move[2];
        REAL last_Lissa_move[2];

    REAL correction_integral_term[2];

    // // zero_crossing_method
    // REAL psi_2_max[2]; // always not equal to zero
    // REAL psi_2_min[2]; // always not equal to zero
    // REAL psi_2_max_temp[2]; // can be reset to zero
    // REAL psi_2_min_temp[2]; // can be reset to zero
    // REAL psi_2_maxmin_difference[2];
    // REAL psi_2_last_zero_level[2];
    // REAL psi_2_last_zero_level_inLoopTheSame[2];
    // REAL psi_2_moved_distance_in_LissajousPlot[2];
    // // REAL offset_voltage[2];

    // REAL flag_Pos_stageA[2];
    // REAL flag_Pos_stageB[2];

    // REAL flag_Neg_stageA[2];
    // REAL flag_Neg_stageB[2];

    // REAL Delta_t_PosMinusNeg[2];
    // REAL Delta_t_NegMinusPos[2];
    // REAL time_Pos[2];
    // REAL time_Neg[2];
};
extern struct Variables_Ohtani1990 ohtani;
void VM_Ohtani1990();


struct Variables_HoltzQuan2002{
    REAL psi_1[2];
    REAL psi_2[2];
};
extern struct Variables_HoltzQuan2002 holtz02;
void VM_HoltzQuan2002();


struct Variables_LascuAndreescus2006{
    REAL psi_1[2];
    REAL psi_2[2];
};
extern struct Variables_LascuAndreescus2006 lascu;
void VM_LascuAndreescus2006();


struct Variables_HuWu1998{
    REAL psi_1[2];
    REAL psi_2[2];
};
extern struct Variables_HuWu1998 huwu;
void VM_HuWu1998();


struct Variables_Stojic2015{
    REAL psi_1[2];
    REAL psi_2[2];
};
extern struct Variables_Stojic2015 stojic;
void VM_Stojic2015();


struct Variables_Harnefors2003_SCVM{
    REAL psi_1[2];
    REAL psi_2[2];
    REAL lambda;
};
extern struct Variables_Harnefors2003_SCVM harnefors;
void VM_Harnefors2003_SCVM();


struct Variables_fluxModulusEstimator{
    REAL psi_DQ2[2];
    REAL psi_DQ1[2];
    REAL temp;
};
extern struct Variables_fluxModulusEstimator fme;


#define VM_HoltzQuan2003 VM_Saturated_ExactOffsetCompensation
void VM_Saturated_ExactOffsetCompensation();
void VM_Saturated_ExactOffsetCompensation_WithAdaptiveLimit();
void VM_Saturated_ExactOffsetCompensation_WithParallelNonSaturatedEstimator();


void stableFME();




#endif
#endif