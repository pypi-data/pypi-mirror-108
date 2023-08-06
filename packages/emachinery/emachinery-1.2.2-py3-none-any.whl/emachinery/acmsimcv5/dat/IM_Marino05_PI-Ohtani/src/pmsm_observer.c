#include "ACMSim.h"
#if MACHINE_TYPE == PM_SYNCHRONOUS_MACHINE

void rk4_init(){
    int i;
    for(i=0; i<2; ++i){
        rk4.us[i] = 0;
        rk4.is[i] = 0;
        rk4.us_curr[i] = 0;
        rk4.is_curr[i] = 0;
        rk4.us_prev[i] = 0;
        rk4.is_prev[i] = 0;
        rk4.is_lpf[i]  = 0;
        rk4.is_hpf[i]  = 0;
        rk4.is_bpf[i]  = 0;

        rk4.current_lpf_register[i] = 0;
        rk4.current_hpf_register[i] = 0;
        rk4.current_bpf_register1[i] = 0;
        rk4.current_bpf_register2[i] = 0;
    }

    // EXP.omg_elec = 0.0;
    // EXP.omg_mech = EXP.omg_elec * CTRL.motor->npp_inv;
    // EXP.theta_d = 0.0;
}



void harnefors_init(){
    // harnefors.theta_d = 0.0;
    // harnefors.omg_elec = 0.0;

    harnefors.svf_p0 = SVF_POLE_0_VALUE;
    harnefors.xSVF_curr[0] = 0.0;
    harnefors.xSVF_curr[1] = 0.0;
    harnefors.xSVF_prev[0] = 0.0;
    harnefors.xSVF_prev[1] = 0.0;
    harnefors.is_dq[0] = 0.0;
    harnefors.is_dq[1] = 0.0;
    harnefors.is_dq_curr[0] = 0.0;
    harnefors.is_dq_curr[1] = 0.0;
    harnefors.is_dq_prev[0] = 0.0;
    harnefors.is_dq_prev[1] = 0.0;
    harnefors.pis_dq[0] = 0.0;
    harnefors.pis_dq[1] = 0.0;    
}


void state_variable_filter(double hs){
    // output += SVF_POLE_0 * (input - last_output) * hs;
    // last_output = output;
    // if input == output:
    //     derivative of input = SVF_POLE_0 * (input - last_output)

    /* State Variable Filter for ob.pis[.] Computed by Standalone RK4 */
    double xxsvf1[2];
    double xxsvf2[2];
    double xxsvf3[2];
    double xxsvf4[2];
    double xsvf_temp[2];
    // step 1 @ t
    xxsvf1[0] = SVF_POLE_0 * (IDQ_P(0) - SVF_P(0)) * hs;
    xxsvf1[1] = SVF_POLE_0 * (IDQ_P(1) - SVF_P(1)) * hs;
    // 新的状态变量的增量 = 该状态变量的导数（上一步的状态的值，其他时变的已知量在t时刻的值） * 数值积分的步长；
    xsvf_temp[0] = SVF_P(0) + xxsvf1[0]*0.5;
    xsvf_temp[1] = SVF_P(1) + xxsvf1[1]*0.5;
    // 临时的状态变量 = 上一步的状态变量 + step1增量*0.5；

    // step 2 @ t+hs/2
    IDQ(0) = 0.5*(IDQ_P(0)+IDQ_C(0));
    IDQ(1) = 0.5*(IDQ_P(1)+IDQ_C(1));
    xxsvf2[0] = SVF_POLE_0 * (IDQ(0) - xsvf_temp[0]) * hs;
    xxsvf2[1] = SVF_POLE_0 * (IDQ(1) - xsvf_temp[1]) * hs;
    // 新的状态变量的增量 = 该状态变量的导数（临时的状态变量的值，其他时变的已知量在t+hs/2时刻的值） * 数值积分的步长；
    xsvf_temp[0] = SVF_P(0) + xxsvf2[0]*0.5;
    xsvf_temp[1] = SVF_P(1) + xxsvf2[1]*0.5;
    // 临时的状态变量 = 上一步的状态变量 + step2增量*0.5；

    // step 3 @ t+hs/2
    xxsvf3[0] = SVF_POLE_0 * (IDQ(0) - xsvf_temp[0]) * hs;
    xxsvf3[1] = SVF_POLE_0 * (IDQ(1) - xsvf_temp[1]) * hs;
    // 新的状态变量的增量 = 该状态变量的导数（临时的状态变量的值，其他时变的已知量在t+hs/2时刻的值） * 数值积分的步长；
    xsvf_temp[0] = SVF_P(0) + xxsvf3[0];
    xsvf_temp[1] = SVF_P(1) + xxsvf3[1];
    // 临时的状态变量 = 上一步的状态变量 + step3增量*1.0；

    // step 4 @ t+hs
    xxsvf4[0] = SVF_POLE_0 * (IDQ_C(0) - xsvf_temp[0]) * hs;
    xxsvf4[1] = SVF_POLE_0 * (IDQ_C(1) - xsvf_temp[1]) * hs;
    // 新的状态变量的增量 = 该状态变量的导数（临时的状态变量的值，其他时变的已知量在t时刻的值） * 数值积分的步长；
    SVF_C(0) += (xxsvf1[0] + 2*(xxsvf2[0] + xxsvf3[0]) + xxsvf4[0])*0.166666666666667; // 0
    SVF_C(1) += (xxsvf1[1] + 2*(xxsvf2[1] + xxsvf3[1]) + xxsvf4[1])*0.166666666666667; // 1    
    // 数值积分的结果 = （step1增量+2*step2增量+2*step3增量+step4的增量）/6

    PIDQ(0) = SVF_POLE_0 * (IDQ_C(0) - SVF_C(0));
    PIDQ(1) = SVF_POLE_0 * (IDQ_C(1) - SVF_C(1));
}

// Harnefors 2006
#define LAMBDA 2
void harnefors_scvm(){

    // 这一组参数很适合伺尔沃的400W，也可以用于100W和200W（delta=6.5，VLBW=50Hz）
        // #define CJH_TUNING_A  25 // low voltage servo motor (<48 Vdc)
        // #define CJH_TUNING_B  1  // low voltage servo motor (<48 Vdc)
        // #define CJH_TUNING_C 1
    // 为NTU的伺服调试的参数（delta=3，VLBW=40Hz）
        #define CJH_TUNING_A  1 // low voltage servo motor (<48 Vdc)
        #define CJH_TUNING_B  1  // low voltage servo motor (<48 Vdc)
        #define CJH_TUNING_C 0.2 // [0.2， 0.5]
    // 可调参数壹
    REAL lambda_s = CJH_TUNING_C * LAMBDA * sign(harnefors.omg_elec);
    // 可调参数贰
    REAL alpha_bw_lpf = CJH_TUNING_A*0.1*(1500*RPM_2_ELEC_RAD_PER_SEC) + CJH_TUNING_B*2*LAMBDA*fabs(harnefors.omg_elec);


    // 一阶差分计算DQ电流的导数
    static REAL last_id = 0.0;
    static REAL last_iq = 0.0;
    // #define D_AXIS_CURRENT CTRL.id_cmd
    // #define Q_AXIS_CURRENT CTRL.iq_cmd
    // harnefors.deriv_id = (CTRL.id_cmd - last_id) * CL_TS_INVERSE;
    // harnefors.deriv_iq = (CTRL.iq_cmd - last_iq) * CL_TS_INVERSE;
    // last_id = CTRL.id_cmd;
    // last_iq = CTRL.iq_cmd;
    #define D_AXIS_CURRENT CTRL.I->idq[0]
    #define Q_AXIS_CURRENT CTRL.I->idq[1]
    harnefors.deriv_id = (D_AXIS_CURRENT - last_id) * CL_TS_INVERSE;
    harnefors.deriv_iq = (Q_AXIS_CURRENT - last_iq) * CL_TS_INVERSE;
    last_id = D_AXIS_CURRENT;
    last_iq = Q_AXIS_CURRENT;

    // 用SVF计算DQ电流的导数
    IDQ_C(0) = D_AXIS_CURRENT;
    IDQ_C(1) = Q_AXIS_CURRENT;
    state_variable_filter(CL_TS);
    IDQ_P(0) = IDQ_C(0); // used in SVF 
    IDQ_P(1) = IDQ_C(1); // used in SVF 
    SVF_P(0) = SVF_C(0);
    SVF_P(1) = SVF_C(1);
    #define DERIV_ID PIDQ(0)
    #define DERIV_IQ PIDQ(1)

    #define UD_CMD CTRL.O->udq_cmd[0]
    #define UQ_CMD CTRL.O->udq_cmd[1]
    #define MOTOR  (*CTRL.motor)

    // // 计算反电势（考虑dq电流导数）
    // #define BOOL_COMPENSATE_PIDQ 1
    // REAL d_axis_emf = UD_CMD - MOTOR.R*D_AXIS_CURRENT + harnefors.omg_elec*MOTOR.Lq*Q_AXIS_CURRENT - BOOL_COMPENSATE_PIDQ*MOTOR.Ld*DERIV_ID; // eemf
    // REAL q_axis_emf = UQ_CMD - MOTOR.R*Q_AXIS_CURRENT - harnefors.omg_elec*MOTOR.Ld*D_AXIS_CURRENT - BOOL_COMPENSATE_PIDQ*MOTOR.Lq*DERIV_IQ; // eemf

    // 计算反电势（忽略dq电流导数）
    #define BOOL_COMPENSATE_PIDQ 0
    REAL d_axis_emf = UD_CMD - MOTOR.R*D_AXIS_CURRENT + harnefors.omg_elec*MOTOR.Lq*Q_AXIS_CURRENT - BOOL_COMPENSATE_PIDQ*MOTOR.Ld*DERIV_ID; // eemf
    REAL q_axis_emf = UQ_CMD - MOTOR.R*Q_AXIS_CURRENT - harnefors.omg_elec*MOTOR.Ld*D_AXIS_CURRENT - BOOL_COMPENSATE_PIDQ*MOTOR.Lq*DERIV_IQ; // eemf

    // 数值积分获得转速和转子位置
        // Note it is bad habit to write numerical integration explictly like this. The states on the right may be accencidentally modified on the run.
    #define KE_MISMATCH 1.0 // 0.7
    harnefors.theta_d  += CL_TS * harnefors.omg_elec;
    harnefors.omg_elec += CL_TS * alpha_bw_lpf * ( (q_axis_emf - lambda_s*d_axis_emf)/(MOTOR.KE*KE_MISMATCH+(MOTOR.Ld-MOTOR.Lq)*D_AXIS_CURRENT) - harnefors.omg_elec );

    // 转子位置周期限幅
    while(harnefors.theta_d>M_PI) harnefors.theta_d-=2*M_PI;
    while(harnefors.theta_d<-M_PI) harnefors.theta_d+=2*M_PI;
}

#endif
