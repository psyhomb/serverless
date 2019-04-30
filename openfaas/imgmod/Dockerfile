# docker build -t <function_name> .

FROM python:3-alpine

ENV fprocess="python3 index.py" \
    cgi_headers="true"

WORKDIR /src

COPY . .

ADD https://github.com/openfaas/faas/releases/download/0.13.0/fwatchdog /usr/bin
RUN adduser --system imgmod \
 && chmod +x /usr/bin/fwatchdog \
 && apk add --no-cache build-base jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
 && pip3 install -r requirements.txt -r function/requirements.txt \
 && apk del --no-cache build-base \
 && rm -vf requirements.txt function/requirements.txt

USER imgmod

HEALTHCHECK --interval=1s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]
