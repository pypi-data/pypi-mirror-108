#if MACHINE_TYPE == 1 || MACHINE_TYPE == 11
#ifndef IM_CONTROLLER_H
#define IM_CONTROLLER_H
typedef struct {
    // controller strategy
    int ctrl_strategy;
    int sensorless;
    // position commands
    REAL cmd_position_rad;  // mechanical
    // speed commands
    REAL cmd_speed_rpm;     // mechanical
    REAL cmd_omg_elec;        // electrical
    REAL cmd_deriv_omg_elec;  // electrical
    REAL cmd_dderiv_omg_elec; // electrical
    // flux commands
    REAL cmd_psi_raw;
    REAL cmd_psi;
    REAL cmd_psi_inv;
    REAL cmd_deriv_psi;
    REAL cmd_dderiv_psi;
    REAL cmd_psi_ABmu[2];
    REAL m0;
    REAL m1;
    REAL omega1;
    // current commands
    REAL iDQ_cmd[2];
    REAL Tem_cmd;
    // feedback
    REAL omg_elec;
    REAL iab[2];
    REAL iDQ[2];
    REAL psi_mu[2];
    REAL Tem;
    REAL TLoad;
} st_controller_inputs;
typedef struct {
    // ???
    REAL e_M;
    REAL e_T;
    // field oriented control
    REAL omega_sl;
    REAL omega_syn;
    REAL theta_D_elec;
    REAL cosT;
    REAL sinT;
    // states
    st_pid_regulator *iM;
    st_pid_regulator *iT;
    st_pid_regulator *pos;
    st_pid_regulator *spd;
} st_controller_states;
typedef struct {
    // electrical 
    REAL R;
    REAL KE;
    REAL Ld;
    REAL Lq;
    // mechanical
    REAL npp;
    REAL npp_inv;
    REAL rs;
    REAL rreq;
    REAL Lsigma;
    REAL Lsigma_inv;
    REAL Lmu;
    REAL Lmu_inv;
    REAL alpha;
    REAL alpha_inv;
    REAL Js;
    REAL Js_inv;    
} st_pmsm_parameters;
typedef struct {
    // voltage commands
    REAL uab_cmd[2];
    REAL uDQ_cmd[2];
} st_controller_outputs;
struct ControllerForExperiment{

    /* Basic quantities */
    REAL timebase;

    /* Machine parameters */
    st_pmsm_parameters *motor;

    /* Controller parameters */
    // dead time, etc.

    /* Black Box Model */
    st_controller_inputs  *I;
    st_controller_states  *S;
    st_controller_outputs *O;
};
extern struct ControllerForExperiment CTRL;

// 这个结构体声明的是基本的IFOC中所没有的变量的集合体。
struct Marino2005{
    REAL kz;     // zd, zq
    REAL k_omega; // e_omega
    REAL kappa;  // e_omega
    REAL gamma_inv; // TL
    REAL delta_inv; // alpha
    REAL lambda_inv; // omega

    REAL xTL_Max;
    REAL xAlpha_Max;
    REAL xAlpha_min;

    REAL xRho;
    REAL xTL;
    REAL xAlpha;
    REAL xOmg;

    REAL deriv_xTL;
    REAL deriv_xAlpha;
    REAL deriv_xOmg;

    REAL psi_Dmu;
    REAL psi_Qmu;

    REAL zD;
    REAL zQ;
    REAL e_iDs;
    REAL e_iQs;
    REAL e_psi_Dmu;
    REAL e_psi_Qmu;

    REAL deriv_iD_cmd;
    REAL deriv_iQ_cmd;

    REAL Gamma_D;
    REAL Gamma_Q;

    REAL torque_cmd;
    REAL torque__fb;
};
extern struct Marino2005 marino;

struct Holtz2003{
    REAL emf[2];
    REAL emf_DQ[2];

    REAL psi_1[2];
    REAL psi_2[2];
    REAL psi_D2_ode1_v2;
    REAL psi_Q2_ode1_v2;

    REAL psi_D1_ode1;
    REAL psi_Q1_ode1;
    REAL psi_D2_ode1;
    REAL psi_Q2_ode1;

    REAL psi_D1_ode4;
    REAL psi_Q1_ode4;
    REAL psi_D2_ode4;
    REAL psi_Q2_ode4;

    REAL psi_D2;
    REAL psi_Q2;
};
extern struct Holtz2003 holtz;

void experiment_init();

void CTRL_init();
void control(REAL speed_cmd, REAL speed_cmd_dot);


void cmd_fast_speed_reversal(REAL timebase, REAL instant, REAL interval, REAL rpm_cmd);
void cmd_slow_speed_reversal(REAL timebase, REAL instant, REAL interval, REAL rpm_cmd);


void controller();
void allocate_CTRL(struct ControllerForExperiment *CTRL);

#endif
#endif
