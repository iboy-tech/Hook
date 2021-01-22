FROM python:3.8-alpine

ENV TZ Asia/Shanghai
ENV CHROME_BIN="/usr/bin/chromium-browser"
ENV LIGHTHOUSE_CHROMIUM_PATH /usr/bin/chromium-browser
WORKDIR /app

COPY pyproject.toml poetry.lock  bot.py docker-entrypoint.sh  ./

COPY ./data/static/font.ttf  /usr/share/fonts/

RUN set -ex; \
    sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories; \
    apk --update  add --no-cache --virtual build-dependencies  build-base gcc   python3-dev musl-dev jpeg-dev libressl-dev libffi-dev libxslt-dev  zlib-dev  openssl-dev; \
    apk add --no-cache  tzdata curl; \
    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime; \
    echo "Asia/Shanghai" > /etc/timezone; \
    apk add  --no-cache chromium dbus; \
    pip config set global.index-url https://mirrors.aliyun.com/pypi/simple; \
    pip install  --upgrade pip; \
    pip install -U setuptools pip; \
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python; \
    source $HOME/.poetry/env; \
    poetry config virtualenvs.create false; \
    poetry install; \
    poetry update; \
    poetry install; \
    rm -rf /var/cache/apk/*; \
    rm -rf /root/.cache; \
    rm -rf /tmp/* /var/tmp/* ;
#apk --purge del build-dependencies; \

ENTRYPOINT [ "./docker-entrypoint.sh" ]