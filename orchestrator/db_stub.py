deployment_profiles = {
    1: {
        'auth': {
            'ssh_user': 'makasim',
            'ssh_password': 'Manaona98',
            'ssh_identity_file': None
        },
        'host': {
            'hostname': '192.168.0.101',
        },
        'res_tresholds': {}
    },
    2: {
        'auth': {
            'ssh_user': 'ec2-user',
            'ssh_password': None,
            'ssh_identity_file': 'auth/ec2-monitored.pem'
        },
        'host': {
            'hostname': 'ec2-18-219-160-73.us-east-2.compute.amazonaws.com',
        },
        'res_tresholds': {}
    }
}

def get_deployment_profile(id: int):
    return deployment_profiles.get(id)