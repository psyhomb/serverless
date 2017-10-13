# docker build -t imgmod .

FROM python:3.6-alpine

WORKDIR /data/imgmod

COPY . .

ADD https://github.com/openfaas/faas/releases/download/0.6.6c/fwatchdog /usr/bin
RUN chmod +x /usr/bin/fwatchdog \
 && apk add --no-cache build-base jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
 && pip3 install -r requirements.txt \
 && apk del build-base \
 && rm -vf requirements.txt

ENV fprocess="python imgmod.py" \
    cgi_headers="true"

HEALTHCHECK --interval=1s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]
