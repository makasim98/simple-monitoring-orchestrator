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
        
def get_remote_pkgm(ssh_client: paramiko.SSHClient) -> str:
    print("Detecting remote package manager...")
    
    try:
        # Check for apt (Ubuntu/Debian)
        run_remote_commands(ssh_client, ["which apt"])
        return "ubuntu"
    except Exception:
        pass

    try:
        # Check for dnf/yum (RHEL/CentOS)
        run_remote_commands(ssh_client, ["which yum || which dnf"])
        return "rhel"
    except Exception:
        pass

    raise Exception("Unsupported remote OS type. Neither apt, yum, nor dnf were found.")