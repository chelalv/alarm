1. 使用uart版本的mlx90640
2. 使用ttyAMA4，修改 /boot/firmware/config.txt 增加
dtoverlay=uart4
3. 树莓派4B 3.3v引脚 单个GPIO建议3mA，最大16mA，所有GPIO总共不能超过272mA
   树莓派4B 5v引脚是适配器输出，和USB一起的，建议使用电流不要超过1.5A。
4. 引脚
雷达：  VCC3.3 外接电源
        GND    PIN9
        OT2    PIN13(GPIO27)
每个距离门0.75m 
LD2420只能使用3.3v，平均电流50mA，
热成像：VCC5v  PIN2
        GND    PIN14
        TX    PIN24
        RX    PIN21
热成像模块工作电流42mA，5V最大输出3A
Max Power: 15W (5V @ 3V)  Adapter Output: DC 5V, up to 3A.
OLED: 5V PIN4
    GND PIN6
    SCL PIN5 
    SDA PIN3
1. 插座上电，有时候树莓派启动后又关机

2025-02-15：
加上RGBLED显示程序已经在运行，
GND: PIN34
R: PIN35(GPIO19)
pulse：程序正常运行
blink: 检测到高温
需要购买数字信号控制的LED(Vcc, GND, S)，如果只使用GPIO驱动(GPIO, GND)，会消耗GPIO很多电流(几百毫安)

现在发现海凌科24G毫米波雷达 LD2420人体微动运动感应模块智能传感器
检测有问题，会检测错误，不断输出高低电平，实际没人在运动
2420平均工作电流是50mA，偏大了一些，
电压是3.3V，网上说使用电流不能超过50mA。
电压如果是5V，电流不能超过1.5A。
将热成像换到5V，暂时没有误测的问题

2025-02-19：
RGB灯很耗电，购买OLED I2C通信，平均电流10mA。
https://learn.adafruit.com/monochrome-oled-breakouts



