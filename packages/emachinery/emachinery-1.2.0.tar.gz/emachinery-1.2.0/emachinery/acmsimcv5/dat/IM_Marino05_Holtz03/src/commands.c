#include "ACMSim.h"

// 定义特定的测试指令，如快速反转等
void cmd_fast_speed_reversal(double timebase, double instant, double interval, double rpm_cmd){
    if(timebase > instant+2*interval){
        ACM.rpm_cmd = 1*1500 + rpm_cmd;
    }else if(timebase > instant+interval){
        ACM.rpm_cmd = 1*1500 + -rpm_cmd;
    }else if(timebase > instant){
        ACM.rpm_cmd = 1*1500 + rpm_cmd;
    }else{
        ACM.rpm_cmd = 20; // default initial command
    }
}

void commands(REAL *p_rpm_speed_command, REAL *p_amp_current_command){
    #define rpm_speed_command (*p_rpm_speed_command)
    #define amp_current_command (*p_amp_current_command)

    // 位置环 in rad
    #if EXCITATION_TYPE == 0
        REAL position_command = 10*M_PI;
        if(CTRL.timebase>5){
            position_command = -10*M_PI;
        }
        REAL position_error = position_command - ACM.theta_d_accum;
        REAL position_KP = 8;
        REAL rad_speed_command = position_KP*position_error;
        rpm_speed_command = rad_speed_command*ELEC_RAD_PER_SEC_2_RPM;
    #endif

    // 扫频建模
    #if EXCITATION_TYPE == 2
        // REAL amp_current_command;
        sf.time += CL_TS;
        if(sf.time > sf.current_freq_end_time){
            // next frequency
            sf.current_freq += sf.freq_step_size;
            // next end time
            sf.last_current_freq_end_time = sf.current_freq_end_time;
            sf.current_freq_end_time += 1.0/sf.current_freq; // 1.0 Duration for each frequency
        }
        if(sf.current_freq > SWEEP_FREQ_MAX_FREQ){
            rpm_speed_command = 0.0;
            amp_current_command = 0.0;
        }else{
            // # closed-cloop sweep
            rpm_speed_command   = SWEEP_FREQ_VELOCITY_AMPL * sin(2*M_PI*sf.current_freq*(sf.time - sf.last_current_freq_end_time));

            // open-loop sweep
            amp_current_command = SWEEP_FREQ_CURRENT_AMPL * sin(2*M_PI*sf.current_freq*(sf.time - sf.last_current_freq_end_time));
        }
    #endif

    // 转速运动模式 in rpm
    #if EXCITATION_TYPE == 1
        #define RPM1 100
        if(CTRL.timebase<1){ // note 1 sec is not enough for stator flux to reach steady state.
            rpm_speed_command = 0;
        }else if(CTRL.timebase<2){
            rpm_speed_command = RPM1;
        }else if(CTRL.timebase<4){
            rpm_speed_command = -RPM1;
        }else if(CTRL.timebase<6){
            rpm_speed_command = 0;
        }else if(CTRL.timebase<8){
            rpm_speed_command = RPM1;
        }
    #endif
}
