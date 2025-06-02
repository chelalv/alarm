# encoding:utf-8
# 红外传感器
import RPi.GPIO as GPIO
import time

# 配置 GPIO 引脚
GPIO_PIN = 27        # 假设使用 BCM 编号的 GPIO 17
DEBOUNCE_TIME = 0.5 # 防抖延时时间（秒）

# 初始化 GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 启用内部上拉电阻

# 初始状态和计时器
last_state = GPIO.input(GPIO_PIN)
last_time = time.time()

try:
    while True:
        current_state = GPIO.input(GPIO_PIN)
        current_time = time.time()

        # 如果状态变化且超过防抖时间
        if current_state != last_state and (current_time - last_time) > DEBOUNCE_TIME:
            last_state = current_state
            last_time = current_time

            if current_state == GPIO.HIGH:
                print("有人")
            else:
                print("人离开")

        time.sleep(0.01)  # 降低 CPU 占用率

except KeyboardInterrupt:
    print("程序终止")

finally:
    GPIO.cleanup()  # 清理 GPIO 资源