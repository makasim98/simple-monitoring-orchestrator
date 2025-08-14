import psutil, time
from datetime import datetime, timezone

def get_sysinfo():
    os = 'Other'
    if psutil.LINUX: os='Linux'
    if psutil.WINDOWS: os='Windows'

    cpu_cores = psutil.cpu_count()
    cpu_freq = psutil.cpu_freq()
    total_memory = psutil.virtual_memory().total
    total_disk = psutil.disk_usage('/').total

    last_boot = psutil.boot_time()
    curr_time = time.time()
    uptime_mins = curr_time - last_boot / 60

    return {
        "os": os,
        "cpu_cores": cpu_cores,
        "cpu_freq": {"min": cpu_freq.min, "max": cpu_freq.max},
        "total_mem": total_memory,
        "total_disk": total_disk,
        "status": 'UP' if uptime_mins > 1 else 'BOOTING'
    }

def gather_metrics():
    cpu_load = get_cpu()
    mem_usage = get_mem()
    disk_usage = get_disk()
    return {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        "cpu": cpu_load,
        "mem": mem_usage,
        "disk": disk_usage
    }

def get_cpu():
     return psutil.cpu_percent()

def get_mem():
    return psutil.virtual_memory().percent

def get_disk():
    return psutil.disk_usage('/').percent