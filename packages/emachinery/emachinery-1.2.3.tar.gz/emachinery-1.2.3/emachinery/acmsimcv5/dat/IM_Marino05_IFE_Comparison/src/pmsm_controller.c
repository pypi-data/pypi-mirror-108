#include "ACMSim.h"
#if MACHINE_TYPE == 2
void experiment_init(){
    CTRL_init();    // 控制器结构体初始化
    rk4_init();     // 龙格库塔法结构体初始化
    harnefors_init(); // harnefors结构体初始化
    // COMM_init(); // 参数自整定初始化
}


// 初始化函数
void CTRL_init(){

    allocate_CTRL(&CTRL);

    /* Basic quantities */
    CTRL.timebase = 0.0;

    /* Controller quantities */
    // commands
    // CTRL.I->idq_cmd[0] = 0.0;
    // CTRL.I->idq_cmd[1] = 0.0;
    // // error
    // CTRL.omg_ctrl_err = 0.0;
    // CTRL.speed_ctrl_err = 0.0;
    // // feedback
    // CTRL.I->omg_elec = 0.0;
    // CTRL.I->theta_d_elec = 0.0;
    // CTRL.I->iab[0] = 0.0;
    // CTRL.I->iab[1] = 0.0;
    // CTRL.I->idq[0] = 0.0;
    // CTRL.I->idq[1] = 0.0;
    // CTRL.psi_mu_al__fb = 0.0;
    // CTRL.psi_mu_be__fb = 0.0;
    // CTRL.Tem = 0.0;
    // // indirect field oriented control
    CTRL.S->cosT = 1.0;
    CTRL.S->sinT = 0.0;
    // CTRL.S->omega_syn = 0.0;

    /* Machine parameters */
    CTRL.motor->R  = PMSM_RESISTANCE;
    CTRL.motor->KE = PMSM_PERMANENT_MAGNET_FLUX_LINKAGE;
    CTRL.motor->Ld = PMSM_D_AXIS_INDUCTANCE;
    CTRL.motor->Lq = PMSM_Q_AXIS_INDUCTANCE;
    CTRL.motor->npp     = MOTOR_NUMBER_OF_POLE_PAIRS;
    CTRL.motor->npp_inv = 1.0 / CTRL.motor->npp;
    CTRL.motor->Js      = MOTOR_SHAFT_INERTIA * (1.0+LOAD_INERTIA);
    CTRL.motor->Js_inv  = 1.0 / CTRL.motor->Js;

    // PID调谐
    ACMSIMC_PIDTuner();

    // PID regulators
    CTRL.S->iM  = &pid1_iM;
    CTRL.S->iT  = &pid1_iT;
    CTRL.S->pos = &pid1_pos;
    CTRL.S->spd = &pid1_spd;
}


extern int Set_current_loop;
void controller(REAL rpm_speed_command, REAL set_iq_cmd, REAL set_id_cmd){

    // 定义局部变量，减少对CTRL的直接调用
    #define MOTOR  (*CTRL.motor)

    // 
    CTRL.I->cmd_position_rad    = 0.0;  // mechanical
    CTRL.I->cmd_speed_rpm       = rpm_speed_command;     // mechanical


    // 帕克变换
    // Input 2 is feedback: measured current 
    CTRL.S->cosT = cos(CTRL.I->theta_d_elec);
    CTRL.S->sinT = sin(CTRL.I->theta_d_elec);
    CTRL.I->idq[0] = AB2M(CTRL.I->iab[0], CTRL.I->iab[1], CTRL.S->cosT, CTRL.S->sinT);
    CTRL.I->idq[1] = AB2T(CTRL.I->iab[0], CTRL.I->iab[1], CTRL.S->cosT, CTRL.S->sinT);
    pid1_id.Fbk = CTRL.I->idq[0];
    pid1_iq.Fbk = CTRL.I->idq[1];

    // 2. 电气转子位置和电气转子转速反馈
    harnefors_scvm();
    #if SENSORLESS_CONTROL == TRUE
        //（无感）
        CTRL.I->omg_elec     = harnefors.omg_elec;
        CTRL.I->theta_d_elec = harnefors.theta_d;
    #endif

    // 转速环
    static int vc_count = 0;
    if(vc_count++ == SPEED_LOOP_CEILING){
        vc_count = 0;

        pid1_spd.Ref = CTRL.I->cmd_speed_rpm*RPM_2_ELEC_RAD_PER_SEC;
        pid1_spd.Fbk = CTRL.I->omg_elec;
        pid1_spd.calc(&pid1_spd);
        pid1_iq.Ref = pid1_spd.Out;
        CTRL.I->idq_cmd[1] = pid1_iq.Ref;
    }
    // 磁链环
    #if CONTROL_STRATEGY == NULL_D_AXIS_CURRENT_CONTROL
        CTRL.I->cmd_rotor_flux_Wb = 0.0;
        pid1_id.Ref = CTRL.I->cmd_rotor_flux_Wb / MOTOR.Ld;
    #else
        pid1_id.Ref = set_id_cmd;
        printf("CONTROL_STRATEGY Not Implemented: %s", CONTROL_STRATEGY);
        getch();
    #endif
    CTRL.I->idq_cmd[0] = pid1_id.Ref;

    // For luenberger position observer for HFSI
    CTRL.I->Tem     = MOTOR.npp * (MOTOR.KE*CTRL.I->idq[1]     + (MOTOR.Ld-MOTOR.Lq)*CTRL.I->idq[0]    *CTRL.I->idq[1]);
    CTRL.I->Tem_cmd = MOTOR.npp * (MOTOR.KE*CTRL.I->idq_cmd[1] + (MOTOR.Ld-MOTOR.Lq)*CTRL.I->idq_cmd[0]*CTRL.I->idq_cmd[1]);

    // 扫频将覆盖上面产生的励磁、转矩电流指令
    #if SWEEP_FREQ_C2V == TRUE
        pid1_iq.Ref = set_iq_cmd; 
    #endif
    #if SWEEP_FREQ_C2C == TRUE
        pid1_iq.Ref = 0.0;
        pid1_id.Ref = set_iq_cmd;
    #endif 

    // debug
    // Set_current_loop = 1;
    // set_iq_cmd = 1;

    if(Set_current_loop==1)
    {
        pid1_iq.Ref = set_iq_cmd;
    }

    // 电流环
    pid1_id.calc(&pid1_id);
    pid1_iq.calc(&pid1_iq);
    // 解耦
    #if VOLTAGE_CURRENT_DECOUPLING_CIRCUIT == TRUE
        REAL decoupled_d_axis_voltage = pid1_id.Out -             pid1_iq.Fbk*MOTOR.Lq *CTRL.I->omg_elec;
        REAL decoupled_q_axis_voltage = pid1_iq.Out + ( MOTOR.KE + pid1_id.Fbk*MOTOR.Ld)*CTRL.I->omg_elec;
    #else
        REAL decoupled_d_axis_voltage = pid1_id.Out;
        REAL decoupled_q_axis_voltage = pid1_iq.Out;
    #endif

    // 反帕克变换
    CTRL.O->uab_cmd[0] = MT2A(decoupled_d_axis_voltage, decoupled_q_axis_voltage, CTRL.S->cosT, CTRL.S->sinT);
    CTRL.O->uab_cmd[1] = MT2B(decoupled_d_axis_voltage, decoupled_q_axis_voltage, CTRL.S->cosT, CTRL.S->sinT);

    // for harnefors observer
    CTRL.O->udq_cmd[0] = decoupled_d_axis_voltage; //pid1_id.Out;
    CTRL.O->udq_cmd[1] = decoupled_q_axis_voltage; //pid1_iq.Out;
    CTRL.I->idq_cmd[0] = pid1_id.Ref;
    CTRL.I->idq_cmd[1] = pid1_iq.Ref;

    #if PC_SIMULATION
        // for plot
        ACM.rpm_cmd = rpm_speed_command;
        // CTRL.speed_ctrl_err = rpm_speed_command*RPM_2_ELEC_RAD_PER_SEC - CTRL.I->omg_elec;
    #endif
}

#endif
