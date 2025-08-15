# -------------- DOCKER IMAGE CONFIGURATION --------------
IMAGE_NAME="monitoring-agent"
FILE_NAME=f"{IMAGE_NAME}.tar"
REMOTE_PATH=f"/tmp/{FILE_NAME}"
LOCAL_PATH=f"docker_image/{FILE_NAME}"
BUILD_CONTEXT='.'

# -------------- ALERT CONFIGURATION --------------
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "maxluch98@gmail.com"
SMTP_PASS = "prmgiekapmqdfkmz"
RECIPIENT_EMAIL = "makasim.devtest@gmail.com"
NEXT_EMAIL_DELAY = 300  # seconds