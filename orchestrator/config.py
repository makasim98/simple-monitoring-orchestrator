IMAGE_NAME="monitoring-agent"
FILE_NAME=f"{IMAGE_NAME}.tar"
REMOTE_PATH=f"/tmp/{FILE_NAME}"
LOCAL_PATH=f"docker_image/{FILE_NAME}"

BUILD_CONTEXT='.'