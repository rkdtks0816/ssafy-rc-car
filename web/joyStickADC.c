#include "hal_data.h"
#include "RTT/SEGGER_RTT.h"

FSP_CPP_HEADER
void R_BSP_WarmStart(bsp_warm_start_event_t event);
FSP_CPP_FOOTER

void hal_entry(void) {
    /* TODO: add your own code here */
    uint16_t data_x;
    uint16_t data_y;

    SEGGER_RTT_printf(0, "Start Application\r\n");

    R_ADC_Open(&g_adc0_ctrl, &g_adc0_cfg);
    R_ADC_ScanCfg(&g_adc0_ctrl, &g_adc0_channel_cfg);
    R_ADC_ScanStart(&g_adc0_ctrl);

    while(1) {
        R_ADC_Read(&g_adc0_ctrl, ADC_CHANNEL_0, &data_x);
        SEGGER_RTT_printf(0, "CDS: %d\r\n", data_x);

        R_ADC_Read(&g_adc0_ctrl, ADC_CHANNEL_1, &data_y);
        SEGGER_RTT_printf(0, "Potentiometer: %d\r\n", data_y);

        // 데이터 전송
        uint8_t data_to_send[4];
        data_to_send[0] = (data_x >> 8) & 0xFF;
        data_to_send[1] = data_x & 0xFF;
        data_to_send[2] = (data_y >> 8) & 0xFF;
        data_to_send[3] = data_y & 0xFF;
        g_sci_uart.p_api->write(g_sci_uart.p_ctrl, data_to_send, sizeof(data_to_send));

        R_BSP_SoftwareDelay(100, BSP_DELAY_UNITS_MILLISECONDS);
    }
}

void R_BSP_WarmStart(bsp_warm_start_event_t event) {
    if (BSP_WARM_START_RESET == event) {
    }

    if (BSP_WARM_START_POST_C == event) {
        R_IOPORT_Open(&g_ioport_ctrl, &g_ioport.p_cfg);
    }
}
