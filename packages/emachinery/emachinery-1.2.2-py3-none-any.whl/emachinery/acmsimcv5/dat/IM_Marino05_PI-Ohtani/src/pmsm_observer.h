#ifndef ADD_PMSM_OBSERVER_H
#define ADD_PMSM_OBSERVER_H
#if MACHINE_TYPE == 2

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

    REAL is_lpf[2];
    REAL is_hpf[2];
    REAL is_bpf[2];

    REAL current_lpf_register[2];
    REAL current_hpf_register[2];
    REAL current_bpf_register1[2];
    REAL current_bpf_register2[2];

    // REAL omg_elec; // omg_elec = npp * omg_mech
    // REAL theta_d;

};
extern struct RK4_DATA rk4;


void rk4_init();
void harnefors_init();

void harnefors_scvm();

#define SVF_POLE_0_VALUE (2000*2*M_PI) /* 定子电阻在高速不准确，就把SVF极点加大！加到3000反而比20000要差。*/
#define SVF_POLE_0 harnefors.svf_p0 
#define SVF_C(X)   harnefors.xSVF_curr[X]
#define SVF_P(X)   harnefors.xSVF_prev[X]
#define IDQ(X)     harnefors.is_dq[X]
#define IDQ_C(X)   harnefors.is_dq_curr[X]
#define IDQ_P(X)   harnefors.is_dq_prev[X]
#define PIDQ(X)    harnefors.pis_dq[X]
struct Harnefors2006{
    REAL theta_d;
    REAL omg_elec;

    REAL deriv_id;
    REAL deriv_iq;

    // SVF for d/q current derivative
    REAL svf_p0;
    REAL xSVF_curr[2];
    REAL xSVF_prev[2];
    REAL is_dq[2];
    REAL is_dq_curr[2];
    REAL is_dq_prev[2];
    REAL pis_dq[2];
};
extern struct Harnefors2006 harnefors;


#endif
#endif
