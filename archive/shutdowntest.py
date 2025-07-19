# encoding:utf-8
# 在客厅树莓派上不能自动关机，这是测试程序

import os
import subprocess
import schedule
import netifaces
import time

DOWN_TIME = "15:14"
def shutdown_task():
    print("即将于 {DOWN_TIME} 关机...")
    #os.system("sudo shutdown -h now")

def start_cron(shutdown_time):
    result = subprocess.run(["timedatectl", "status"], capture_output=True, text=True)
    output = result.stdout
    # 检查输出中是否包含特定输出"
    if "System clock synchronized: yes" in output:
        schedule.every().day.at(shutdown_time).do(shutdown_task)
        return True
    else:
        return False

shutdown_time = input("Enter time to shutdown\n")
while True:
    start_cron(shutdown_time)
    schedule.run_pending()
    print("当前时间: ", time.strftime("%H:%M"))
    time.sleep(1)
