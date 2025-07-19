1. 使用uart版本的mlx90640
2. 使用ttyAMA4，修改 /boot/firmware/config.txt 增加
dtoverlay=uart4
3. 树莓派4B 3.3v引脚 单个GPIO建议3mA，最大16mA，所有GPIO总共不能超过272mA
   树莓派4B 5v引脚是适配器输出，和USB一起的，建议使用电流不要超过1.5A。
4. 引脚
雷达：  VCC5    PIN2
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

2025-02-25:
增加IP显示
 pip install netifaces --break-system-packages

2025-02-25:
树莓派重启后哦时间会记住上一次的时间，一直到和网络时间同步
等到同步结束，才开启关机命令
去掉rc.local关机，在代码里定时关机

查看log:journalctl -u wpa_supplicant.service, wifi经常会断，
sudo iwlist wlan0 scan | grep -E "SSID|Quality" Quality是-70dbm
购买一个旧的路由器加在原来的路由器上，新建一个ssid中不能有下划线

2025-3-9
购买5v购电的ld2402G，和热成像分享PIN2 5v输出

2025-4-25
早晨开机发现LD2402G一直输出高电平，测量输入电压是5.1v，比5.3v低
这个问题之前也遇到过，可能1个月会发生一次。
更换LD2402G的线，改为比较柔软的杜邦线，再继续观察

2025-6-2
oled显示平均温度，这样就能实时看到温度传感器是否正常工作

2025-7-13
增加客厅一个树莓派加喇叭，防止厨房喇叭声音太小听不到
设置树莓派固定ip，运行mqtt local broker，使用mqtt通信
borker安装：
sudo apt install mosquitto mosquitto-clients
需修改/etc/mosquitto/mosquitto.conf添加：
listener 1883 0.0.0.0

on_connect函数没有被调用，必须调用 loop_start()（异步）或 loop_forever()（阻塞）以处理网络流量和回调。

python schedule不成功，需要while循环schedule.run_pending()





