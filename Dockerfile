FROM python:3.11-slim

COPY entrypoint.prod.sh /entrypoint.prod.sh
COPY entrypoint.dev.sh /entrypoint.dev.sh

COPY sshd_config /etc/ssh/

RUN apt-get update \
    && apt-get install -y --no-install-recommends dialog \
    && apt-get install -y --no-install-recommends openssh-server \
    && apt-get install -y --no-install-recommends ffmpeg \
    && echo "root:Docker!" | chpasswd \
    && chmod u+x /entrypoint.prod.sh \
    && chmod u+x /entrypoint.dev.sh 

WORKDIR /app

# copy only this file to cache the dependencies
# ref: https://fastapi.tiangolo.com/deployment/docker/#docker-cache
COPY ./app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app .

EXPOSE 8000 2222

# for dev, entrypoint will be overriden in compose.yml
ENTRYPOINT [ "/entrypoint.prod.sh" ] 