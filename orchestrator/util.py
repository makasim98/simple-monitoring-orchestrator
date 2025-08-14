import subprocess
import paramiko

# Connect to the remote host with SSH. 
def connect_to_remote(hostname: str, username: str, password=None, key_filename=None) -> paramiko.SSHClient:
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    print(f"Connecting to {hostname}...")
    try:
        if key_filename:
            print(f"Using identity file: {key_filename}")
            ssh_client.connect(hostname=hostname, username=username, key_filename=key_filename)
        else:
            print("Using password authentication.")
            ssh_client.connect(hostname=hostname, username=username, password=password)
        print("Connection successful.")
        return ssh_client
    except paramiko.AuthenticationException as e:
        raise Exception(f"Authentication failed. Check credentials or key path: {e}")
    except paramiko.SSHException as e:
        raise Exception(f"SSH connection failed: {e}")
    except Exception as e:
        raise Exception(f"Could not connect to {hostname}: {e}")

# Executes a list of commands on the remote host and print the output.
def run_remote_commands(ssh_client: paramiko.SSHClient, commands: list[str]):
    for command in commands:
        print(f"  > Executing remote command: '{command}'")
        stdin, stdout, stderr = ssh_client.exec_command(command)
        stdout_output = stdout.read().decode().strip()
        stderr_output = stderr.read().decode().strip()
        
        if stdout_output:
            print(f"    - STDOUT: {stdout_output}")
        if stderr_output:
            print(f"    - STDERR: {stderr_output}")
        exit_code = stdout.channel.recv_exit_status()
        if exit_code != 0:
            raise Exception(f"Remote command failed: '{command}'")

# Runs a local shell command and returns the output or raises an error.
def run_local_commands(commands: list[str]):
    for command in commands:
        print(f"  > Executing local command: '{command}'")
        try:
            result = subprocess.run(command, check=True, shell=True, capture_output=True, text=True)
            if result.stdout:
                print(f"    - STDOUT: {result.stdout.strip()}")
            if result.stderr:
                print(f"    - STDERR: {result.stderr.strip()}")
        except subprocess.CalledProcessError as e:
            raise Exception(f"Local command failed: '{command}'\nSTDOUT: {e.stdout}\nSTDERR: {e.stderr}")
        
def get_remote_distro(ssh_client: paramiko.SSHClient) -> str:
    print("Detecting remote OS distribution...")
    
    try:
        stdin, stdout, stderr = ssh_client.exec_command("cat /etc/os-release")
        os_info = stdout.read().decode().strip()

        if "Ubuntu" in os_info:
            return "ubuntu"
        elif "Debian" in os_info:
            return "debian"
        elif "Amazon Linux" in os_info:
            return "amazon"
        elif "Red Hat" in os_info or "CentOS" in os_info or "Fedora" in os_info:
            return "rhel_family"
        else:
            raise Exception("Unsupported remote OS distribution.")

    except Exception as e:
         raise Exception(f"Failed to detect remote OS distribution: {e}")


def get_docker_install_cmd(os: str) -> list[str]:   
    match os:
        case "ubuntu" | "debian":
            return [
                "sudo apt-get update",
                "DEBIAN_FRONTEND=noninteractive sudo apt-get install -y docker.io",
                "sudo systemctl start docker",
            ]
        case "amazon":
            return [
                "sudo dnf update -y",
                "sudo dnf install -y docker",
            ]
        case "rhel_family":
            return [
                "sudo dnf install -y yum-utils device-mapper-persistent-data lvm2",
                "sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo",
                "sudo dnf install -y docker-ce docker-ce-cli containerd.io",
            ]
        case _:
            raise ValueError(f"Unsupported distribution: {os}")