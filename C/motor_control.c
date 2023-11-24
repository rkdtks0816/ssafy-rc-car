#include <wiringPiI2C.h>
#include <stdio.h>
#include <unistd.h>

#define I2C_ADDR 0x6F

#define MODE1 0x00
#define MODE2 0x01
#define PRESCALE 0xFE

// PCA9685 PWM 출력 핀
#define PWM0_ON_L 0x06
#define PWM0_ON_H 0x07
#define PWM0_OFF_L 0x08
#define PWM0_OFF_H 0x09

// 적절한 PWM 출력 핀 및 모터 방향을 설정
void setMotor(int motor_fd, int channel, int on, int off) {
    wiringPiI2CWriteReg8(motor_fd, PWM0_ON_L + 4 * channel, on & 0xFF);
    wiringPiI2CWriteReg8(motor_fd, PWM0_ON_H + 4 * channel, on >> 8);
    wiringPiI2CWriteReg8(motor_fd, PWM0_OFF_L + 4 * channel, off & 0xFF);
    wiringPiI2CWriteReg8(motor_fd, PWM0_OFF_H + 4 * channel, off >> 8);
}

// PCA9685 초기화
void initPCA9685(int motor_fd) {
    // PCA9685 초기화
    wiringPiI2CWriteReg8(motor_fd, MODE1, 0x00);
    
    // 모드 2 설정 (출력 순서 및 그 외 설정)
    wiringPiI2CWriteReg8(motor_fd, MODE2, 0x04);
    
    // PWM 주기 설정 (200Hz를 원한다면 값을 조절)
    int prescale_val = 121; // 50Hz에 대한 값
    wiringPiI2CWriteReg8(motor_fd, PRESCALE, prescale_val);
    
    // 모터 정지
    setMotor(motor_fd, 0, 0, 0);
    setMotor(motor_fd, 1, 0, 0);
}

int main(void) {
    int motor_fd;

    if ((motor_fd = wiringPiI2CSetup(I2C_ADDR)) == -1) {
        printf("I2C 초기화 실패\n");
        return 1;
    }

    initPCA9685(motor_fd);

    while (1) {
        // 모터 1을 시계 방향으로 1초간 회전
        setMotor(motor_fd, 11, 0, 4096); // PWM 출력 값을 조절하여 속도를 변경
        setMotor(motor_fd, 12, 4096, 0);

        sleep(1);

        // 모터 1을 반시계 방향으로 1초간 회전
        setMotor(motor_fd, 12, 0, 4096);
        setMotor(motor_fd, 11, 4096, 0);

        sleep(1);

        setMotor(motor_fd, 12, 0, 4096);
        setMotor(motor_fd, 11, 0, 4096);
        sleep(1);
    }

    return 0;
}
