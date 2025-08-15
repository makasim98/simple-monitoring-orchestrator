from paramiko import SSHClient
from pathlib import Path
from services.util import run_local_commands, connect_to_remote, run_remote_commands, get_remote_distro, get_docker_install_cmd
from services.db.db_methods import get_deployment_profile, update_deployment_status

IMAGE_NAME="monitoring-agent"
FILE_NAME=f"{IMAGE_NAME}.tar"
REMOTE_PATH=f"/tmp/{FILE_NAME}"
LOCAL_PATH=f"docker_image/{FILE_NAME}"
BUILD_CONTEXT='.'

# The target host must configure passwordles sudo for apt, systemctl, dokcer and usermod
# ```echo "$USER ALL=(ALL) NOPASSWD: /usr/bin/apt-get, /usr/bin/systemctl, /usr/sbin/usermod" | sudo tee /etc/sudoers.d/docker-install```

# Orchestrates monitoring agent (container) deployment on remote machines
def deploy_agent(profile_id: int):
    profile = get_deployment_profile(profile_id)
    if not profile:
        raise ValueError(f"No deployment profile found for ID: {profile_id}")
    
    remote_host = profile['hostname']
    ssh_user = profile['ssh_user']
    ssh_pass = profile['ssh_pass']
    ssh_idFile = profile['ssh_identity_file'].decode('utf-8').strip() if profile['ssh_identity_file'] else None

    try:
        image_tag = build_and_save_agent_image()
        ssh_client = connect_to_remote(hostname=remote_host, username=ssh_user, password=ssh_pass, pKey=ssh_idFile)
   
        if check_and_install_docker(ssh_client):
            ssh_client.close()
            ssh_client = connect_to_remote(hostname=remote_host, username=ssh_user, password=ssh_pass, pKey=ssh_idFile)

        transfer_image(ssh_client)
        load_and_run_container(ssh_client, image_tag)
        
        print("\nSUCCESS: Deployment completed successfully!")
        update_deployment_status(profile_id, True)
    except Exception as e:
        print(f"\nERROR: An error occurred during deployment: {e}")
    finally:
        if 'ssh_client' in locals() and ssh_client:
            ssh_client.close()
            print("SSH connection closed.")

# Orchestrates monitoring agent (container) removal from remote machines
def remove_agent(profile_id: int):
    profile = get_deployment_profile(profile_id)
    if not profile:
        raise ValueError(f"No deployment profile found for ID: {profile_id}")

    remote_host = profile['hostname']
    ssh_user = profile['ssh_user']
    ssh_pass = profile['ssh_pass']
    ssh_idFile = profile['ssh_identity_file'].decode('utf-8').strip() if profile['ssh_identity_file'] else None

    try:
        ssh_client = connect_to_remote(hostname=remote_host, username=ssh_user, password=ssh_pass, pKey=ssh_idFile)
        commands = [
            f"docker ps -q --filter 'name={IMAGE_NAME}' | xargs -r docker stop",
            f"docker ps -aq --filter 'name={IMAGE_NAME}' | xargs -r docker rm",
            f"docker images -q {IMAGE_NAME} | xargs -r docker rmi",
        ]
        run_remote_commands(ssh_client, commands)
        print("\nSUCCESS: Agent removed successfully!")
        update_deployment_status(profile_id, False)
    except Exception as e:
        print(f"\nERROR: An error occurred during removal: {e}")
    finally:
        if 'ssh_client' in locals() and ssh_client:
            ssh_client.close()
            print("SSH connection closed.")


def build_and_save_agent_image():
    image_tag = f"{IMAGE_NAME}:latest"
    local_image_path = Path(LOCAL_PATH)
    local_image_dir = local_image_path.parent

    if Path(LOCAL_PATH).exists():
        print(f"Docker image tar file '{local_image_path}' already exists. Skipping build and save step.")
        return image_tag
    
    print(f"Docker image tar file '{local_image_path}' not found. Building and saving...")
    local_image_dir.mkdir(exist_ok=True)
    
    commands = [
        f"docker build -t {image_tag} {BUILD_CONTEXT}",
        f"docker save -o {LOCAL_PATH} {image_tag}"
    ]

    run_local_commands(commands)

    print(f"Docker image saved to {LOCAL_PATH}")
    return image_tag


def check_and_install_docker(ssh_client: SSHClient):
    print("Checking for Docker installation on the remote host...")
    try:
        run_remote_commands(ssh_client, ["docker --version"])
        print("Docker is already installed.")
        return False
    except Exception:
        print("Docker is not installed. Attempting to install...")
        os_type = get_remote_distro(ssh_client)
        commands = get_docker_install_cmd(os_type)
        commands.extend([
            "sudo systemctl start docker",
            "sudo systemctl enable docker",
            "sudo usermod -aG docker $USER"
        ])
        run_remote_commands(ssh_client, commands)
        print("Docker installed and configured. Reconnecting to apply new group membership...")
        return True


def transfer_image(ssh_client: SSHClient):
    if not Path(LOCAL_PATH).exists():
        raise FileNotFoundError(f"Local Docker image file not found: {LOCAL_PATH}")

    print(f"Transferring {LOCAL_PATH} to remote {REMOTE_PATH}...")
    try:
        sftp = ssh_client.open_sftp()
        sftp.put(LOCAL_PATH, REMOTE_PATH)
        sftp.close()
        print("File transferred successfully.")
    except Exception as e:
        raise Exception(f"SFTP file transfer failed: {e}")


def load_and_run_container(ssh_client: SSHClient, image_tag: str):
    print(f"Loading and running the Docker container on the remote host...")
    commands = [
        f"docker load -i {REMOTE_PATH}",
        f"docker stop {IMAGE_NAME} || true",
        f"docker rm {IMAGE_NAME} || true",
        f"docker run -d --name {IMAGE_NAME} --restart unless-stopped --net=host -v /proc:/host/proc:ro --pid=host {image_tag}"
    ]
    run_remote_commands(ssh_client, commands)
    print("Container started successfully.")