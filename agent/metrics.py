import psutil, time, platform, os
from datetime import datetime, timezone

def get_system_info():
    try:
        # Get the OS information
        os_name = "Other"
        if psutil.LINUX: os_name = 'Linux'
        elif psutil.WINDOWS: os_name = 'Windows'
        elif psutil.MACOS: os_name = 'macOS'

        # Get HW information
        cpu_cores = psutil.cpu_count(logical=True)
        cpu_physical_cores = psutil.cpu_count(logical=False)
        total_memory_bytes = psutil.virtual_memory().total
        total_disk_bytes = psutil.disk_usage('/').total

        # Get uptime
        uptime_seconds = time.time() - psutil.boot_time()
        
        return {
            "os": os_name,
            "cpu_cores": cpu_cores,
            "cpu_physical_cores": cpu_physical_cores,
            "total_memory_bytes": total_memory_bytes,
            "total_disk_bytes": total_disk_bytes,
            "uptime_sec": uptime_seconds,
        }
    except Exception as e:
        raise Exception(f"Unexpected Error while retrieving system information: {e}")

def get_sys_metrics():
    try:
        # Get HW metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        mem_percent = mem.percent
        mem_used_gb = round(mem.used / (1024 ** 3), 2)
        mem_available_gb = round(mem.available / (1024 ** 3), 2)
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        disk_used_gb = round(disk.used / (1024 ** 3), 2)
        disk_free_gb = round(disk.free / (1024 ** 3), 2)
        net_io = psutil.net_io_counters()
        bytes_sent_mb = round(net_io.bytes_sent / (1024 * 1024), 2)
        bytes_recv_mb = round(net_io.bytes_recv / (1024 * 1024), 2)

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "cpu_percent": cpu_percent,
            "mem_percent": mem_percent,
            "mem_used_gb": mem_used_gb,
            "mem_available_gb": mem_available_gb,
            "disk_percent": disk_percent,
            "disk_used_gb": disk_used_gb,
            "disk_free_gb": disk_free_gb,
            "bytes_sent_mb": bytes_sent_mb,
            "bytes_recv_mb": bytes_recv_mb,
            "status": "UP"
        }
    except Exception as e:
        raise Exception(f"Unexpected Error while retrieving system information: {e}")