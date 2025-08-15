from .tresholds import Thresholds
class Endpoint:
    def __init__(
            self, hostname, name, username, password, identity_file,thresholds=None,
            is_deployed=False, timestamp=None, cpu_usage=None, memory_usage=None, disk_usage=None
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