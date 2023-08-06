#ifndef PMSM_CONTROLLER_H
#define PMSM_CONTROLLER_H
#if MACHINE_TYPE == 2

typedef struct {
    // commands
    REAL cmd_position_rad;  // mechanical
    REAL cmd_speed_rpm;     // mechanical
    REAL cmd_rotor_flux_Wb;
    REAL idq_cmd[2];
    REAL Tem_cmd;
    // feedback
    REAL omg_elec;
    REAL theta_d_elec;
    REAL iab[2];
    REAL idq[2];
    REAL psi_mu[2];
    REAL Tem;
} st_controller_inputs;
typedef struct {
    // field oriented control
    REAL cosT;
    REAL sinT;
    REAL omega_syn;
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
    REAL Js;
    REAL Js_inv;    
} st_pmsm_parameters;
typedef struct {
    // voltage commands
    REAL uab_cmd[2];
    REAL udq_cmd[2];
} st_controller_outputs;
struct ControllerForExperiment{

    /* Basic quantities */
    REAL timebase;

    /* Machine parameters */
    st_pmsm_parameters *motor;

    /* Controller parameters */
    // dead time

    /* Black Box Model */
    st_controller_inputs  *I;
    st_controller_states  *S;
    st_controller_outputs *O;
};
extern struct ControllerForExperiment CTRL;

void experiment_init();
void CTRL_init();
void controller(REAL rpm_speed_command, REAL set_iq_cmd, REAL set_id_cmd);
void allocate_CTRL(struct ControllerForExperiment *CTRL);

// void control(REAL speed_cmd, REAL speed_cmd_dot);

void cmd_fast_speed_reversal(REAL timebase, REAL instant, REAL interval, REAL rpm_cmd);
void cmd_slow_speed_reversal(REAL timebase, REAL instant, REAL interval, REAL rpm_cmd);

#endif
#endif
