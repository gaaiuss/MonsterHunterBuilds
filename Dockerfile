FROM python:3.13-slim-bookworm
LABEL maintainer="caio.gui.castro@gmail.com"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY djangoapp /djangoapp
COPY scripts /scripts/

WORKDIR /djangoapp
EXPOSE 8000

RUN apt-get update && apt-get install -y dos2unix && \
    dos2unix /scripts/commands.sh && \
    apt-get install -y netcat-openbsd && \
    rm -rf /var/lib/apt/lists/* && \
    python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r /djangoapp/requirements.txt && \
    adduser --disabled-password --no-create-home duser && \
    mkdir -p /data/web/static /data/web/media && \
    chown -R duser:duser /venv /data /scripts && \
    chmod -R 755 /data/web && \
    chmod -R +x /scripts

ENV PATH="/scripts:/venv/bin:$PATH"

USER duser

CMD ["sh", "/scripts/commands.sh"]
