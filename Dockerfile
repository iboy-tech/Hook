FROM python:3.8-alpine

ENV TZ Asia/Shanghai
ENV CHROME_BIN="/usr/bin/chromium-browser"
ENV LIGHTHOUSE_CHROMIUM_PATH /usr/bin/chromium-browser
WORKDIR /app

COPY pyproject.toml poetry.lock  bot.py docker-entrypoint.sh  ./

COPY ./data/static/font.ttf  /usr/share/fonts/

RUN set -ex; \
    sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories; \
    chmod +x docker-entrypoint.sh; \
    apk --update  add --no-cache --virtual build-dependencies  build-base gcc   python3-dev musl-dev jpeg-dev libressl-dev libffi-dev libxslt-dev  zlib-dev  openssl-dev; \
    apk add --no-cache  tzdata; \
    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime; \
    echo "Asia/Shanghai" > /etc/timezone; \
    apk add  --no-cache chromium dbus; \
    pip config set global.index-url https://mirrors.aliyun.com/pypi/simple; \
    pip install -U setuptools pip; \
    python3 -m pip install poetry; \
    poetry config virtualenvs.create false; \
    poetry install --no-root --no-dev; \
    pyppeteer-install; \
    rm -rf /var/cache/apk/*; \
    rm -rf /root/.cache; \
    rm -rf /tmp/* /var/tmp/* ;\
    apk --purge del build-dependencies;

ENTRYPOINT [ "./docker-entrypoint.sh" ]