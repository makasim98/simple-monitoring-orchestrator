import requests as req
import time
from orchestrator.deployment import deploy_agent


# The target host must configure passwordles sudo for apt, systemctl, dokcer and usermod
# ```echo "$USER ALL=(ALL) NOPASSWD: /usr/bin/apt-get, /usr/bin/systemctl, /usr/sbin/usermod" | sudo tee /etc/sudoers.d/docker-install```

HOST_URI=f"http://192.168.0.101:5000"
STATUS_ENDPOINT = HOST_URI + "/status"
METRICS_ENDPOINT = HOST_URI + "/metrics"

def test():
    while True:
        resp = req.get(url=METRICS_ENDPOINT)
        if resp.status_code == 200:
            metrics = resp.json()
            print(f"CPU% - {metrics['cpu']}% | MEM% - {metrics['mem']}% | DISK% - {metrics['disk']}%")
        time.sleep(2)

# test()
# deploy_agent(1)