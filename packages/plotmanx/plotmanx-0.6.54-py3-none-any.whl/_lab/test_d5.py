import re

import psutil
from psutil.tests import sh


def commaInt(x: str) -> int:
    return int(x.strip(" ").replace(',', ''))


# if not found.. sudo: nvme: command not found
# sudo nvme smart-log /dev/nvme0
# 'NR==1{print $1}'
# lsblk | grep nvme | grep disk | sort | awk '{print $1}'
# lsblk | grep nvme | sort | awk 'NR==1{print $1}'
# lsblk|grep nvme|grep disk|sort|awk '{print $1}`
sample1 = """
nvme0n1
nvme1n1
nvme2n1
nvme3n1
"""
sample2 = """
Smart Log for NVME device:nvme0n1 namespace-id:ffffffff
critical_warning                    : 0
temperature                         : 44 C
available_spare                     : 100%
available_spare_threshold           : 10%
percentage_used                     : 6%
data_units_read                     : 1,453,614,235
data_units_written                  : 1,706,252,589
host_read_commands                  : 2,582,632,560
host_write_commands                 : 3,177,813,741
controller_busy_time                : 31,993
power_cycles                        : 7
power_on_hours                      : 3,966
unsafe_shutdowns                    : 3
media_errors                        : 0
num_err_log_entries                 : 0
Warning Temperature Time            : 0
Critical Composite Temperature Time : 0
Temperature Sensor 1                : 44 C
Temperature Sensor 2                : 44 C
Temperature Sensor 3                : 49 C
Thermal Management T1 Trans Count   : 0
Thermal Management T2 Trans Count   : 0
Thermal Management T1 Total Time    : 0
Thermal Management T2 Total Time    : 0
"""


def devNvmeList() -> list:
    devices = []
    try:
        output0 = sh("lsblk | grep nvme | grep disk | sort | awk '{print $1}'").strip()
        lines = output0.split('\n')

        for dev in lines:
            ok = re.match("^nvme(.*)", dev)
            if ok:
                print(f"sudo nvme smart-log /dev/{dev}")
                output = sh(f"sudo nvme smart-log /dev/{dev}").strip()
                if output == "sudo: nvme: command not found":
                    return []

                lines = output.split('\n')
                setting = dict()

                for l in lines:
                    if l == "":
                        continue
                    if re.match(r"^Smart Log for", l):
                        continue

                    # print("ok read. ")
                    # print(l)

                    r = l.split(":")
                    if r[0].strip(" ").strip("\n") == 'data_units_written':
                        dev_ex = r[1].strip(" ").strip("\n")
                        setting.setdefault("data_units_written", commaInt(dev_ex))

                    if r[0].strip(" ").strip("\n") == 'host_write_commands':
                        dev_ex = r[1].strip(" ").strip("\n")
                        setting.setdefault("host_write_commands", commaInt(dev_ex))

                    if r[0].strip(" ").strip("\n") == 'percentage_used':
                        dev_ex = r[1].strip(" ").strip("\n")
                        setting.setdefault("percentage_used", dev_ex.strip(" "))
                devices.append(setting)


    except UserWarning as u:
        print("not working... ps command not found")

    return devices


def crawl_exd():
    try:
        print("check --1")
        disk_counters = psutil.disk_io_counters(perdisk=True)
        for device_name in disk_counters:
            m0 = re.match("^nvme(.*)", device_name)
            if m0:
                # meta = dffnvme(device_name)
                meta = dict()
                print(f'Disk Health - {device_name}: {meta.get("host_write_commands")} b')

        print("check --3")
    except OSError as e:
        print(
            u'Caught exception when crawling disk I/O counters: {0}'.format(e))


print("before __name__ guard")
if __name__ == '__main__':
    s = devNvmeList()
    print(s)
print("after __name__ guard")
