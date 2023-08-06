#ifndef ACMCONFIG_H
#define ACMCONFIG_H
/* Consistent with DSP Codes */
// 电机类型（TODO：饱和模型里面用的还是 IM.rr 而不是 IM.rreq）
    #define INDUCTION_MACHINE_CLASSIC_MODEL 1
    #define INDUCTION_MACHINE_FLUX_ONLY_MODEL 11
    #define PM_SYNCHRONOUS_MACHINE 2
#define MACHINE_TYPE 1
	// 电机参数
	#define IM_STAOTR_RESISTANCE        3.04
	#define IM_ROTOR_RESISTANCE         1.6
	#define IM_TOTAL_LEAKAGE_INDUCTANCE 0.0249
	// 磁链给定
	#define IM_MAGNETIZING_INDUCTANCE   0.448
	#define IM_FLUX_COMMAND_DC_PART     0.7105842093440861
	#define IM_FLUX_COMMAND_SINE_PART   0.0
	#define IM_FLUX_COMMAND_SINE_HERZ   10
	// 铭牌值
	#define MOTOR_NUMBER_OF_POLE_PAIRS  2
	#define MOTOR_RATED_CURRENT_RMS     8.8
	#define MOTOR_RATED_POWER_WATT      4000
	#define MOTOR_RATED_SPEED_RPM       1440
	#define MOTOR_SHAFT_INERTIA         0.063
	// 参数误差
		#define MISMATCH_RS               100
		#define MISMATCH_RREQ             100
		#define MISMATCH_LMU              100
		#define MISMATCH_LSIGMA           100

// 指令类型
    #define EXCITATION_POSITION 0
    #define EXCITATION_VELOCITY 1
    #define EXCITATION_SWEEP_FREQUENCY 2
#define EXCITATION_TYPE (1)

// 控制策略
	#define INDIRECT_FOC 1
	#define MARINO_2005_ADAPTIVE_SENSORLESS_CONTROL 2
#define CONTROL_STRATEGY MARINO_2005_ADAPTIVE_SENSORLESS_CONTROL
#define NUMBER_OF_STEPS 320000
#define DOWN_SAMPLE 1
#define SENSORLESS_CONTROL FALSE
#define SENSORLESS_CONTROL_HFSI FALSE
#define VOLTAGE_CURRENT_DECOUPLING_CIRCUIT TRUE
#define SATURATED_MAGNETIC_CIRCUIT FALSE
#define INVERTER_NONLINEARITY FALSE
#define CL_TS          (5e-05)
#define CL_TS_INVERSE  (20000)
#define TS_UPSAMPLING_FREQ_EXE 0.5
#define TS_UPSAMPLING_FREQ_EXE_INVERSE 2

// 调参 (17143), (2700.0)
#define GAMMA_INV_xTL 17142.85714285714
#define LAMBDA_INV_xOmg 2700.0
#define DELTA_INV_alpha (0*1000)
#define xAlpha_LAW_TERM_D 1 // regressor is commanded d-axis rotor current, and error is d-axis flux control error.
#define xAlpha_LAW_TERM_Q 0 // regressor is commanded q-axis stator current, and error is q-axis flux control error.

// 磁链反馈用谁
#define IFE clest
#define FLUX_FEEDBACK_ALPHA         IFE.psi_2[0]
#define FLUX_FEEDBACK_BETA          IFE.psi_2[1]
#define OFFSET_COMPENSATION_ALPHA   IFE.u_offset[0]
#define OFFSET_COMPENSATION_BETA    IFE.u_offset[1]

// 磁链观测系数配置
#define GAIN_OHTANI (5)
// Ohtani 建议取值和转子时间常数相等
#define VM_OHTANI_CORRECTION_GAIN_P (5)
/* B */
#define VM_PROPOSED_PI_CORRECTION_GAIN_P (5)
#define VM_PROPOSED_PI_CORRECTION_GAIN_I (2.5)
/* C */
#define CLOSED_LOOP_ESTIMATOR_GAIN_KP (0.5*50*0.005*5)
#define CLOSED_LOOP_ESTIMATOR_GAIN_KI (0.5*50*0.005*2.5)
#define CLOSED_LOOP_ESTIMATOR_GAIN_KCM (0*0.8)
/* Holtz 2002 */
// default: 20
#define HOLTZ_2002_GAIN_OFFSET 20
/* Harnefors SCVM 2003 */
// default: 2
#define GAIN_HARNEFORS_LAMBDA 2


#define VL_TS          (0.0002)
#define PL_TS VL_TS
#define SPEED_LOOP_CEILING (4)

#define LOAD_INERTIA    0.16
#define LOAD_TORQUE     5
#define VISCOUS_COEFF   0.007

#define CURRENT_KP (610.52)
#define CURRENT_KI (6.42842)
#define CURRENT_KI_CODE (CURRENT_KI*CURRENT_KP*CL_TS)
#define SPEED_KP (3.40446)
#define SPEED_KI (30.5565)
#define SPEED_KI_CODE (SPEED_KI*SPEED_KP*VL_TS)

#define SWEEP_FREQ_MAX_FREQ 200
#define SWEEP_FREQ_INIT_FREQ 2
#define SWEEP_FREQ_VELOCITY_AMPL 500
#define SWEEP_FREQ_CURRENT_AMPL 1
#define SWEEP_FREQ_C2V FALSE
#define SWEEP_FREQ_C2C FALSE

#define DATA_FILE_NAME "../dat/IM_Marino05_IFE_Comparison-205-1000-7-2624.dat"
#endif
