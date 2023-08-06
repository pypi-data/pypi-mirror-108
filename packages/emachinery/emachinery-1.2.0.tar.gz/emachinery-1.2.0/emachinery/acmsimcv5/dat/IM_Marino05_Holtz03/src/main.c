#include "ACMSim.h"
// 主函数
int main(){
    // 初始化
    Machine_init(); // 仿真电机初始化
    experiment_init();
    // 打印
    print_info();
    // 声明文件，并将变量名写入文件
    FILE *fw; fw = fopen(DATA_FILE_NAME, "w"); write_header_to_file(fw);
    // 主循环
    clock_t begin, end; begin = clock(); int _, dfe_counter=0; // _ for the outer iteration // dfe_counter for down frequency execution （降频执行变量）
    for(_=0;_<NUMBER_OF_STEPS*TS_UPSAMPLING_FREQ_EXE_INVERSE;++_){
        // 负载转矩
        ACM.TLoad = load_model();
        // 每隔 MACHINE_TS 调用电机仿真代码一次
        ACM.timebase += MACHINE_TS; if(machine_simulation()){ printf("main.c: Break the loop.\n"); break;}
        // 降频执行控制器代码（比如电机仿真执行两次或多次，才执行控制器代码一次）
        if(++dfe_counter == TS_UPSAMPLING_FREQ_EXE_INVERSE){
            dfe_counter = 0;
            // DSP中的时间
            CTRL.timebase += CL_TS;
            // 采样，包括DSP中的ADC采样等
            measurement();
            // 写数据到文件
            write_data_to_file(fw);
            // 生成转速指令
            REAL rpm_speed_command, set_iq_cmd;
            commands(&rpm_speed_command, &set_iq_cmd);
            // 根据指令，产生控制输出（电压）
            controller(rpm_speed_command, set_iq_cmd, 0.0);
        }
        // 电压指令CTRL.ual，CTRL.ube通过逆变器，产生实际电压ACM.ual，ACM.ube（变换到dq系下得到ACM.ud，ACM.uq）
        inverter_model();
    }
    end = clock(); printf("The simulation in C costs %g sec.\n", (double)(end - begin)/CLOCKS_PER_SEC);
    fclose(fw);
    // 调用python脚本绘图
    // system("cd .. && python ACMPlot.py"); 
    // getch();
    // system("pause");
    return 0; 
}

void print_info(){
    if(SENSORLESS_CONTROL==TRUE){
        printf("Sensorless using observer.\n");
    }else{
        printf("Sensored control.\n");
    }
    printf("NUMBER_OF_STEPS: %d\n\n", NUMBER_OF_STEPS);
    printf("Speed PID: Kp=%g, Ki=%g, limit=%g Nm\n", pid1_spd.Kp, pid1_spd.Ki/CL_TS, pid1_spd.OutLimit);
    printf("Current PID: Kp=%g, Ki=%g, limit=%g V\n", pid1_id.Kp, pid1_id.Ki/CL_TS, pid1_id.OutLimit);
}
