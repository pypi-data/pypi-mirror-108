#include "ACMSim.h"

// 定义顶级结构体（指针的集合）
struct ControllerForExperiment CTRL;
// 定义内存空间（结构体）
st_pmsm_parameters    t_motor={0};
st_controller_inputs  t_I={0};
st_controller_states  t_S={0};
st_controller_outputs t_O={0};
st_pid_regulator      pid1_iM  = st_pid_regulator_DEFAULTS;
st_pid_regulator      pid1_iT  = st_pid_regulator_DEFAULTS;
st_pid_regulator      pid1_pos = st_pid_regulator_DEFAULTS;
st_pid_regulator      pid1_spd = st_pid_regulator_DEFAULTS;
// 初始化顶级结构体指针，指向定义好的内存空间
void allocate_CTRL(struct ControllerForExperiment *p){
    /* My attemp to use calloc with TI's compiler in CCS has failed. */
        // p->motor = calloc(1,sizeof(st_pmsm_parameters));
        // p->I = calloc(1,sizeof(st_controller_inputs));
        // p->S = calloc(1,sizeof(st_controller_states));
        // p->O = calloc(1,sizeof(st_controller_outputs));
    p->motor = &t_motor;
    p->I = &t_I;
    p->S = &t_S;
    p->O = &t_O;

    p->S->iM  = &pid1_iM;
    p->S->iT  = &pid1_iT;
    p->S->pos = &pid1_pos;
    p->S->spd = &pid1_spd;
}


// CCS Debug Window
int Set_current_loop=0;



/* Structs for Algorithm */
#if MACHINE_TYPE == PM_SYNCHRONOUS_MACHINE
    // 游离在顶级之外的算法结构体
    struct RK4_DATA rk4;
    struct Harnefors2006 harnefors={0};
#else
    // 游离在顶级之外的算法结构体
    struct RK4_DATA rk4;
    struct Marino2005 marino={0};

    struct Variables_SimulatedVM                         simvm      ={0};
    struct Variables_Ohtani1992                          ohtani     ={0};
    struct Variables_HuWu1998                            huwu       ={0};
    struct Variables_HoltzQuan2002                       holtz02    ={0};
    struct Variables_Holtz2003                           htz        ={0};
    struct Variables_Harnefors2003_SCVM                  harnefors  ={0};
    struct Variables_LascuAndreescus2006                 lascu      ={0};
    struct Variables_Stojic2015                          stojic     ={0};
    struct Variables_fluxModulusEstimator                fme        ={0};
    struct Variables_ExactCompensationMethod             exact      ={0};
    struct Variables_ProposedxRhoFramePICorrectionMethod picorr     ={0};
    struct Variables_ClosedLoopFluxEstimator             clest      ={0};
#endif
