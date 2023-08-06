# %%
try:
    from numba.experimental import jitclass
except:
    from numba import jitclass
from numba import njit, types, vectorize, prange
from numba import int32, float64 # import the types
from pylab import np, plt
plt.style.use('ggplot')


# %%
@jitclass(
    spec=[
        # name plate data
        ('npp',   int32),
        ('npp_inv', float64),
        ('IN',  float64),
        # electrical parameters
        ('R',   float64),
        ('Ld',  float64),
        ('Lq',  float64),
        ('KE',  float64),
        # mechanical parameters
        ('Js',  float64),
        ('Js_inv', float64),
        ('B',   float64),
        # states
        ('NS',    int32),
        ('x',   float64[:]),
        ('Tem', float64),
        # inputs
        ('uab',   float64[:]),
        ('udq',   float64[:]),
        ('TLoad', float64),
        # output
        ('cosT', float64),
        ('sinT', float64),
        ('theta_d', float64),
        ('theta_mech', float64),
        ('omega_elec', float64),
        ('iab', float64[:]),
    ])
class The_AC_Machines:
    def __init__(self):
        # name plate data
        self.npp = 4
        self.npp_inv = 1.0/self.npp
        self.IN = 3 # Arms (line-to-line)
        # electrical parameters
        self.R = 1.1
        self.Ld = 5e-3
        self.Lq = 5e-3
        self.KE = 0.095
        # mechanical parameters
        self.Js = 0.0006168  # kg.m^2
        self.Js_inv = 1.0/self.Js
        self.B  = 0*0.7e-3 # Nm.s
        # states
        self.NS = 5
        self.x = np.zeros(self.NS, dtype=np.float64)
        self.Tem = 0.0
        # inputs
        self.uab = np.zeros(2, dtype=np.float64)
        self.udq = np.zeros(2, dtype=np.float64)
        self.TLoad = 0
        # output
        self.cosT = 0.0
        self.sinT = 0.0
        self.theta_d = 0.0
        self.theta_mech = 0.0
        self.omega_elec = 0.0
        self.iab = np.zeros(2, dtype=np.float64)

@jitclass(
    spec=[
        # constants
        ('CL_TS', float64),
        ('VL_TS', float64),
        # feedback / input
        ('theta_d', float64),
        ('omega_elec', float64),
        ('iab', float64[:]),
        # states
        ('timebase', float64),
        ('cosT', float64),
        ('sinT', float64),
        ('idq', float64[:]),
        # commands
        ('idq_cmd', float64[:]),
        ('udq_cmd', float64[:]),
        ('uab_cmd', float64[:]),
        ('cmd_rpm_speed', float64),
        # MOTOR
            # name plate data
            ('npp',   int32),
            ('IN',  float64),
            # electrical parameters
            ('R',   float64),
            ('Ld',  float64),
            ('Lq',  float64),
            ('KE',  float64),
            # mechanical parameters
            ('Js',  float64),
    ])
class The_Motor_Controller:
    def __init__(self, CL_TS, VL_TS, human):
        # constants
        self.CL_TS = CL_TS
        self.VL_TS = VL_TS
        # feedback / input
        self.theta_d = 0.0
        self.omega_elec = 0.0
        self.iab = np.zeros(2, dtype=np.float64)
        # states
        self.timebase = 0.0
        self.cosT = 0.0
        self.sinT = 0.0
        self.idq = np.zeros(2, dtype=np.float64)
        # commands 
        self.idq_cmd = np.zeros(2, dtype=np.float64)
        self.udq_cmd = np.zeros(2, dtype=np.float64)
        self.uab_cmd = np.zeros(2, dtype=np.float64)
        self.cmd_rpm_speed = 0.0;
        # MOTOR
        self.npp = human.npp
        self.IN  = human.IN
        self.R   = human.R
        self.Ld  = human.Ld
        self.Lq  = human.Lq
        self.KE  = human.KE
        self.Js  = human.Js

@jitclass(
    spec=[
        # feedback / inputs
        ('iab_prev', float64[:]),
        ('iab_curr', float64[:]),
        ('uab_prev', float64[:]),
        # states
        ('cosT', float64),
        ('sinT', float64),
        # outputs
        ('theta_d', float64),
        ('omega_elec', float64),
        # MOTOR
            # name plate data
            ('npp',   int32),
            ('IN',  float64),
            # electrical parameters
            ('R',   float64),
            ('Ld',  float64),
            ('Lq',  float64),
            ('KE',  float64),
            # mechanical parameters
            ('Js',  float64),
    ])
class The_Observer:
    def __init__(self, human):
        # feedback / input
        self.theta_d = 0.0
        self.omega_elec = 0.0
        self.iab = np.zeros(2, dtype=np.float64)
        # states
        self.timebase = 0.0
        self.cosT = 0.0
        self.sinT = 0.0
        self.idq = np.zeros(2, dtype=np.float64)
        # commands 
        self.idq_cmd = np.zeros(2, dtype=np.float64)
        self.udq_cmd = np.zeros(2, dtype=np.float64)
        self.uab_cmd = np.zeros(2, dtype=np.float64)
        self.cmd_rpm_speed = 0.0;
        # MOTOR
        self.npp = human.npp
        self.IN  = human.IN
        self.R   = human.R
        self.Ld  = human.Ld
        self.Lq  = human.Lq
        self.KE  = human.KE
        self.Js  = human.Js


@jitclass(
    spec=[
        ('Kp', float64),
        ('Ki', float64),
        ('Err', float64),
        ('Ref', float64),
        ('Fbk', float64),
        ('Out', float64),
        ('OutLimit', float64),
        ('ErrPrev', float64),
        ('OutPrev', float64),
    ])
class The_PI_Regulator:
    def __init__(self, KP_CODE, KI_CODE, OUTPUT_LIMIT):
        self.Kp = KP_CODE
        self.Ki = KI_CODE
        self.Err      = 0.0
        self.Ref      = 0.0
        self.Fbk      = 0.0
        self.Out      = 0.0
        self.OutLimit = OUTPUT_LIMIT
        self.ErrPrev  = 0.0
        self.OutPrev  = 0.0

@jitclass(
    spec=[
        ('sensorless_position', int32),
        ('sensorless_speed', int32),
        # MOTOR
            # name plate data
            ('npp',   int32),
            ('IN',  float64),
            # electrical parameters
            ('R',   float64),
            ('Ld',  float64),
            ('Lq',  float64),
            ('KE',  float64),
            # mechanical parameters
            ('Js',  float64),
    ])
class The_Human:
    def __init__(self):
        self.sensorless_position = False
        self.sensorless_speed    = False
        # name plate data
        self.npp = 4
        self.IN = 3 # Arms (line-to-line)
        # electrical parameters
        self.R = 1.1
        self.Ld = 5e-3
        self.Lq = 5e-3
        self.KE = 0.095
        # mechanical parameters
        self.Js = 0.0006168  # kg.m^2



@njit(nogil=True)
def MACHINE_DYNAMICS(t, x, ACM, CLARKE_TRANS_TORQUE_GAIN=1.5):
    fx = np.zeros(5)

    # 电磁子系统 (id, iq)
    fx[0] = (ACM.udq[0] - ACM.R * x[0] + x[2]*ACM.Lq*x[1]) / ACM.Ld
    fx[1] = (ACM.udq[1] - ACM.R * x[1] - x[2]*ACM.Ld*x[0] - x[2]*ACM.KE) / ACM.Lq

    # 机械子系统 (omega_r_elec, theta_d_elec, theta_r_mech)
    ACM.Tem = CLARKE_TRANS_TORQUE_GAIN * ACM.npp * \
        (x[1]*ACM.KE + (ACM.Ld - ACM.Lq)*x[0]*x[1]) # 电磁转矩 Tem 计算
    fx[2] = (ACM.Tem - ACM.TLoad - ACM.B * x[2]) * ACM.npp/ACM.Js # elec. angular rotor speed
    fx[3] = x[2]              # elec. angular rotor position(bounded)
    fx[4] = x[2]/ACM.npp  # mech. angular rotor position(accumulated)
    return fx

@njit(nogil=True)
def RK4(t, ACM, hs): # 四阶龙格库塔法
    NS = ACM.NS
    k1, k2, k3, k4 = np.zeros(NS), np.zeros(NS), np.zeros(NS), np.zeros(NS)
    xk, fx = np.zeros(NS), np.zeros(NS)

    if False:
        """ this is about twice slower than loop through the element one by one """ 
        fx = MACHINE_DYNAMICS(t, ACM.x, ACM) # @timer.t,
        k1 = fx * hs
        xk = ACM.x + k1*0.5

        fx = MACHINE_DYNAMICS(t, xk, ACM)  # @timer.t+hs/2.,
        k2 = fx * hs
        xk = ACM.x + k2*0.5

        fx = MACHINE_DYNAMICS(t, xk, ACM)  # @timer.t+hs/2.,
        k3 = fx * hs
        xk = ACM.x + k3

        fx = MACHINE_DYNAMICS(t, xk, ACM)  # timer.t+hs,
        k4 = fx * hs
        ACM.x = ACM.x + (k1 + 2*(k2 + k3) + k4)/6.0
    else:
        for i in range(NS):
            k1[i] = fx[i] * hs
            xk[i] = ACM.x[i] + k1[i]*0.5

        fx = MACHINE_DYNAMICS(t, xk, ACM)  # @timer.t+hs/2.,
        for i in range(NS):
            k2[i] = fx[i] * hs
            xk[i] = ACM.x[i] + k2[i]*0.5

        fx = MACHINE_DYNAMICS(t, xk, ACM)  # @timer.t+hs/2.,
        for i in range(NS):
            k3[i] = fx[i] * hs
            xk[i] = ACM.x[i] + k3[i]

        fx = MACHINE_DYNAMICS(t, xk, ACM)  # timer.t+hs,
        for i in range(NS):
            k4[i] = fx[i] * hs
            ACM.x[i] = ACM.x[i] + (k1[i] + 2*(k2[i] + k3[i]) + k4[i])/6.0
            # derivatives
            # ACM.x_dot[i] = (k1[i] + 2*(k2[i] + k3[i]) + k4[i])/6.0 / hs 

@njit(nogil=True)
def incremental_pi(reg):
    reg.Err = reg.Ref - reg.Fbk
    reg.Out = reg.OutPrev + \
        reg.Kp * (reg.Err - reg.ErrPrev) + \
        reg.Ki * reg.Err
    if reg.Out >    reg.OutLimit:
        reg.Out =   reg.OutLimit
    elif reg.Out < -reg.OutLimit:
        reg.Out =  -reg.OutLimit
    reg.ErrPrev = reg.Err
    reg.OutPrev = reg.Out

@njit(nogil=True)
def FOC(CTRL, reg_id, reg_iq, reg_speed):
    reg_speed.Ref = CTRL.cmd_rpm_speed / 60 * 2*np.pi * CTRL.npp
    reg_speed.Fbk = CTRL.omega_elec
    incremental_pi(reg_speed)

    reg_id.Ref = 0.0
    reg_id.Fbk = CTRL.idq[0]
    incremental_pi(reg_id)
    CTRL.udq_cmd[0] = reg_id.Out

    reg_iq.Ref = reg_speed.Out
    reg_iq.Fbk = CTRL.idq[1]
    incremental_pi(reg_iq)
    CTRL.udq_cmd[1] = reg_iq.Out

    return CTRL.udq_cmd



""" DSP """
@njit(nogil=True)
def DSP(ACM, CTRL, reg_id, reg_iq, reg_speed, human):
    CTRL.timebase += CTRL.CL_TS

    """ Measurment """
    CTRL.iab[0]     = ACM.iab[0] # + offset, scale error , noise
    CTRL.iab[1]     = ACM.iab[1] # + offset, scale error , noise
    if human.sensorless_speed:
        CTRL.omega_elec = ACM.omega_elec # OB.omega_elec
    else:
        CTRL.omega_elec = ACM.omega_elec
    if human.sensorless_position:
        CTRL.theta_d = ACM.theta_d # OB.theta_d
    else:
        CTRL.theta_d = ACM.theta_d
    # do this once per control interrupt
    CTRL.cosT = np.cos(CTRL.theta_d)
    CTRL.sinT = np.sin(CTRL.theta_d)
    # Park transformation
    CTRL.idq[0] = CTRL.iab[0] * CTRL.cosT + CTRL.iab[1] * CTRL.sinT
    CTRL.idq[1] = CTRL.iab[0] *-CTRL.sinT + CTRL.iab[1] * CTRL.cosT

    """ Controller """
    CTRL.udq_cmd = FOC(CTRL, reg_id, reg_iq, reg_speed)
    # Inverse Park transformation
    CTRL.uab_cmd[0] = CTRL.udq_cmd[0] * CTRL.cosT + CTRL.udq_cmd[1] *-CTRL.sinT
    CTRL.uab_cmd[1] = CTRL.udq_cmd[0] * CTRL.sinT + CTRL.udq_cmd[1] * CTRL.cosT

    """ Inverter """
    ACM.uab[0] = CTRL.uab_cmd[0] # + current denpendent distorted voltage
    ACM.uab[1] = CTRL.uab_cmd[1] # + current denpendent distorted voltage

""" MAIN for Real-time simulation """
@njit(nogil=True)
def ACMSimPyIncremental(parameters,
            t0, TIME,
            ACM=None,
            CTRL=None,
            reg_id=None,
            reg_iq=None,
            reg_speed=None,
            human=None,
            ):
    MACHINE_TS = CTRL.CL_TS
    down_sampling_ceiling = int(CTRL.CL_TS / MACHINE_TS); #print('\tdown sample:', down_sampling_ceiling)

    # watch variabels
    machine_times  = np.arange(t0, t0+TIME, MACHINE_TS)
    control_times  = np.arange(t0, t0+TIME, CTRL.CL_TS)
    id = np.zeros_like(control_times)
    iq = np.zeros_like(control_times)
    ia = np.zeros_like(control_times)
    ib = np.zeros_like(control_times)
    speed = np.zeros_like(control_times)

    # Main loop
    # print('\tt0 =', t0)
    jj = 0; watch_index = 0
    for ii in range(len(machine_times)):

        t = machine_times[ii]

        """ Machine Simulation @ MACHINE_TS """
        # Park transformation
        ACM.udq[0] = ACM.uab[0] *  ACM.cosT + ACM.uab[1] * ACM.sinT
        ACM.udq[1] = ACM.uab[0] * -ACM.sinT + ACM.uab[1] * ACM.cosT
        # Numerical Integration (ode4) with 5 states
        RK4(t, ACM, hs=MACHINE_TS)

        """ Machine Simulation Output @ MACHINE_TS """
        # Generate output variables for easy access
        ACM.omega_elec  = ACM.x[2]
        ACM.theta_d     = ACM.x[3]
        ACM.theta_mech  = ACM.x[4]
        # Inverse Park transformation
        ACM.cosT = np.cos(ACM.theta_d)
        ACM.sinT = np.sin(ACM.theta_d)
        ACM.iab[0] = ACM.x[0] * ACM.cosT + ACM.x[1] *-ACM.sinT
        ACM.iab[1] = ACM.x[0] * ACM.sinT + ACM.x[1] * ACM.cosT

        jj += 1
        if jj >= down_sampling_ceiling:
            jj = 0

            """ DSP @ CL_TS """
            DSP(ACM=ACM,
                CTRL=CTRL,
                reg_id=reg_id,
                reg_iq=reg_iq,
                reg_speed=reg_speed,
                human=human)

            """ Console @ CL_TS """
            if t < 1.0:
                CTRL.cmd_rpm_speed = 50
            elif t < 1.5:
                ACM.TLoad = 2
            elif t < 2.0:
                CTRL.cmd_rpm_speed = 200
            elif t < 3.0:
                CTRL.cmd_rpm_speed = -200
            elif t < 4.0:
                CTRL.cmd_rpm_speed = 0
            elif t < 4.5:
                CTRL.cmd_rpm_speed = 2000
            # else: # don't implement else to allow command from IPython console

            """ Watch @ CL_TS """
            id[watch_index] = ACM.x[0]
            iq[watch_index] = ACM.x[1]
            ia[watch_index] = CTRL.iab[0]
            ib[watch_index] = CTRL.iab[1]
            speed[watch_index] = CTRL.omega_elec / (2*np.pi*ACM.npp) * 60
            watch_index += 1

    return control_times, id, iq, ia, ib, speed


# %% Test incremental simulation
if __name__ == '__main__':

    # Simulation Basics
    CL_TS      = 1e-4
    TIME_SLICE = 1.0

    # Human
    human = The_Human()

    # init
    ACM       = The_AC_Machines()
    CTRL      = The_Motor_Controller(CL_TS, 5*CL_TS, human)
    reg_id    = The_PI_Regulator(6.39955, 6.39955*237.845*CTRL.CL_TS, 600)
    reg_iq    = The_PI_Regulator(6.39955, 6.39955*237.845*CTRL.CL_TS, 600)
    reg_speed = The_PI_Regulator(0.0380362, 0.0380362*30.5565*CTRL.VL_TS, 1*1.414*ACM.IN)

    # Global arrays
    global_speed = None

    for ii in range(0, 10):
        """perform animation step"""
        control_times, id, iq, ia, ib, speed, = \
            ACMSimPyIncremental(1,
                        t0=ii*TIME_SLICE, TIME=TIME_SLICE, 
                        ACM=ACM,
                        CTRL=CTRL,
                        reg_id=reg_id,
                        reg_iq=reg_iq,
                        reg_speed=reg_speed,
                        human=human)
        if global_speed is None:
            global_speed = speed
        else:
            global_speed = np.append(global_speed, speed)
        print(len(speed), end='|')
        print(max(speed), end='|')
        print(len(global_speed), end='|')
        print(max(global_speed))

# %%
