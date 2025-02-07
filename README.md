1. 使用uart版本的mlx90640
2. 使用ttyAMA4，修改 /boot/firmware/config.txt 增加
dtoverlay=uart4
3. 引脚
雷达：  VCC3.3 PIN17
        GND    PIN9
        OT2    PIN13(GPIO27)

热成像：VCC3.3v  PIN1
        GND    PIN6
        TX    PIN24
        RX    PIN21
4. 插座上电，有时候树莓派启动后又关机