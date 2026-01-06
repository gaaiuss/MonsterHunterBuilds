FROM python:3.11.3-alpine3.18
LABEL mantainer='caio.gui.castro@gmail.com'

# This environment variable is used to control if Python must save bytecode 
# files on the disk. 1 - No, 0 - Yes
ENV PYTHONDONTWRITEBYTECODE 1

# Defines that Python prints will be immediately exhibited on the console or
# on another exit device, without being stored in buffer.
# On resume, you will see Python outputs in real time.
ENV PYTHONUNBUFFERED 1

# Copies the "djangoapp" folder and "scripts" inside the container.
COPY djangoapp /djangoapp
COPY scripts /scripts

# Enters in the djangoapp folder on the container
WORKDIR /djangoapp

# The port 8000 will be available for external connections to access the 
# container. This is the port that we will use for Django.
EXPOSE 8000

# RUN executes commands in a shell inside the container to build an image.
# The command execution result is stored in the files system of the image as a
# new layer.
# Group the commands in a single RUN can reduce the quantity of layers of the
# image and make it more efficient. 
RUN python -m venv /venv && \
  /venv/bin/pip install --upgrade pip && \
  /venv/bin/pip install -r /djangoapp/requirements.txt && \
  adduser --disabled-password --no-create-home duser && \
  mkdir -p /data/web/static && \
  mkdir -p /data/web/media && \
  chown -R duser:duser /venv && \
  chown -R duser:duser /data/web/static && \
  chown -R duser:duser /data/web/media && \
  chmod -R 755 /data/web/static && \
  chmod -R 755 /data/web/media && \
  chmod -R +x /scripts

# Add the scripts and venv/bin folders to $PATH on the container.
ENV PATH="/scripts:/venv/bin:$PATH"

# Changes the user to duser
USER duser

# Executes the scripts/commands.sh file
CMD ["commands.sh"]