from datetime import datetime, timezone
import random as rnd

deployment_profiles = {
    1: {
        'deployed': True,
        'auth': {
            'ssh_user': 'makasim',
            'ssh_password': 'Manaona98',
            'ssh_identity_file': None
        },
        'host': {
            'name': 'Ubuntu-Monitored',
            'hostname': '192.168.0.101',
        },
        'res_tresholds': {},
        'status': {
            'state': 'UP',
        }
    },
    2: {
        'deployed': True,
        'auth': {
            'ssh_user': 'ec2-user',
            'ssh_password': None,
            'ssh_identity_file': 'auth/ec2-monitored.pem'
        },
        'host': {
            'name': 'EC2-Monitored',
            'hostname': '18.219.160.73',
        },
        'res_tresholds': {},
        'status': {
            'state': 'DOWN',
        }
    },
}

def grp():
    return float(rnd.randint(0,100))

metrics = [
    {'remote_id': 1, 'timestamp': datetime(2025,8,14,13,30,0,0, tzinfo=timezone.utc), 'cpu': grp(), 'mem': grp(), 'disk': grp()},
    {'remote_id': 1, 'timestamp': datetime(2025,8,14,13,31,0,0, tzinfo=timezone.utc), 'cpu': grp(), 'mem': grp(), 'disk': grp()},
    {'remote_id': 1, 'timestamp': datetime(2025,8,14,13,32,0,0, tzinfo=timezone.utc), 'cpu': grp(), 'mem': grp(), 'disk': grp()},
    {'remote_id': 2, 'timestamp': datetime(2025,8,14,13,30,0,0, tzinfo=timezone.utc), 'cpu': grp(), 'mem': grp(), 'disk': grp()},
    {'remote_id': 1, 'timestamp': datetime(2025,8,14,13,33,0,0, tzinfo=timezone.utc), 'cpu': grp(), 'mem': grp(), 'disk': grp()},
    {'remote_id': 1, 'timestamp': datetime(2025,8,14,13,34,0,0, tzinfo=timezone.utc), 'cpu': grp(), 'mem': grp(), 'disk': grp()},
    {'remote_id': 2, 'timestamp': datetime(2025,8,14,13,31,0,0, tzinfo=timezone.utc), 'cpu': grp(), 'mem': grp(), 'disk': grp()},
    {'remote_id': 1, 'timestamp': datetime(2025,8,14,13,35,0,0, tzinfo=timezone.utc), 'cpu': grp(), 'mem': grp(), 'disk': grp()},
    {'remote_id': 1, 'timestamp': datetime(2025,8,14,13,36,0,0, tzinfo=timezone.utc), 'cpu': grp(), 'mem': grp(), 'disk': grp()},
    {'remote_id': 2, 'timestamp': datetime(2025,8,14,13,32,0,0, tzinfo=timezone.utc), 'cpu': grp(), 'mem': grp(), 'disk': grp()},
    {'remote_id': 1, 'timestamp': datetime(2025,8,14,13,37,0,0, tzinfo=timezone.utc), 'cpu': grp(), 'mem': grp(), 'disk': grp()},
    {'remote_id': 1, 'timestamp': datetime(2025,8,14,13,37,0,0, tzinfo=timezone.utc), 'cpu': grp(), 'mem': grp(), 'disk': grp()},
    {'remote_id': 2, 'timestamp': datetime(2025,8,14,13,33,0,0, tzinfo=timezone.utc), 'cpu': grp(), 'mem': grp(), 'disk': grp()},
    {'remote_id': 1, 'timestamp': datetime(2025,8,14,13,39,0,0, tzinfo=timezone.utc), 'cpu': grp(), 'mem': grp(), 'disk': grp()},
    {'remote_id': 2, 'timestamp': datetime(2025,8,14,13,34,0,0, tzinfo=timezone.utc), 'cpu': grp(), 'mem': grp(), 'disk': grp()},
]

def get_deployment_profiles():
    return deployment_profiles

def get_deployment_profile(deployment_id: int):
    return deployment_profiles.get(deployment_id)

def update_host_status(deployment_id: int, status: str):
    deployment_profiles[deployment_id]['status']['state'] = status

def get_deployment_metrics(deployment_id: int):
    return list(filter(lambda m: m['remote_id'] == deployment_id, metrics))

def save_deployment_metrics(remote_id: int, host_metrics):
    metrics.append({
        'remote_id': remote_id,
        'timestamp': datetime.fromisoformat(host_metrics['timestamp']),
        'cpu': host_metrics['cpu'],
        'mem': host_metrics['mem'],
        'disk': host_metrics['disk']
    })