import platform
import os
import psutil
import time as t
from datetime import datetime
import collections

# Defining functions to get disk stats
if hasattr(os, 'statvfs'):  # POSIX (UNIX)
    def disk_usage(path):
        st = os.statvfs(path)
        free = st.f_bavail * st.f_frsize
        total = st.f_blocks * st.f_frsize
        used = (st.f_blocks - st.f_bfree) * st.f_frsize
        return total, used, free

elif os.name == 'nt':       # Windows
    import ctypes
    import sys

    def disk_usage(path):
        _, total, free = ctypes.c_ulonglong(), ctypes.c_ulonglong(), \
                           ctypes.c_ulonglong()
        if sys.version_info >= (3,) or isinstance(path, unicode):
            fun = ctypes.windll.kernel32.GetDiskFreeSpaceExW
        else:
            fun = ctypes.windll.kernel32.GetDiskFreeSpaceExA
        ret = fun(path, ctypes.byref(_), ctypes.byref(total), ctypes.byref(free))
        if ret == 0:
            raise ctypes.WinError()
        used = total.value - free.value
        return total.value, used, free.value
else:
    raise NotImplementedError("platform not supported")

# Start of actual program
OS = "" + platform.uname()[0] + " " + platform.uname()[2]
name = platform.uname()[1]
print("Operating System:", OS)
print("Computer Name:", name)


print("Time\t\tCPU Usage\tRAM Usage\tDisk Usage")
while(True):
    diskTotal = 0
    diskUsed = 0
    if(hasattr(os, 'statvfs')):
        diskTotal, diskUsage, _ = disk_usage('/')

    elif(os.name == 'nt'):
        diskTotal, diskUsage, _ = str(disk_usage('C:\\'))

    time = datetime.now().strftime('%H:%M:%S')
    diskPercent = round((diskUsage/diskTotal) * 100, 3)
    ramPercentage = psutil.virtual_memory()[2]
    print(time + "\t" + str(psutil.cpu_percent()) + "%\t\t" + str(ramPercentage) + "%\t\t" + str(diskPercent) + "%")
    t.sleep(5)
