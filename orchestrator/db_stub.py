deployment_profiles = {
    1: {
        'auth': {
            'ssh_user': 'makasim',
            'ssh_password': 'Manaona98',
            'ssh_identity_file': None
        },
        'host': {
            'hostname': '192.168.0.101'
        },
        'res_tresholds': {}
    }
}

def get_deployment_profile(id: int):
    return deployment_profiles.get(id)