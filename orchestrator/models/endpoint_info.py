from .tresholds import Thresholds

class EndpointInfo:
    def __init__(
            self, hostname, name, username=None, password=None, identity_file=None, thresholds=None,
            is_deployed=False, timestamp=None, cpu_usage=None, memory_usage=None, disk_usage=None,
            os=None, cpu_cores=None, total_mem=None, total_disk=None, state=None
        ):
        self.name = name
        self.hostname = hostname
        self.username = username
        self.password = password
        self.identity_file = identity_file
        self.is_deployed = is_deployed
        self.thresholds = thresholds if thresholds is not None else Thresholds()
        self.timestamp = timestamp
        self.cpu_usage = cpu_usage
        self.memory_usage = memory_usage
        self.disk_usage = disk_usage
        self.os = os
        self.cpu_cores = cpu_cores
        self.total_mem = total_mem
        self.total_disk = total_disk
        self.state = state