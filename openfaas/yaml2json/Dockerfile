# docker build -t yaml2json .

FROM python:3.6-alpine

WORKDIR /data/yaml2json

COPY . .

ADD https://github.com/openfaas/faas/releases/download/0.6.6c/fwatchdog /usr/bin
RUN chmod +x /usr/bin/fwatchdog \
 && pip install -r requirements.txt \
 && rm -vf requirements.txt

ENV fprocess="python3 yaml2json.py" \
    cgi_headers="true"

HEALTHCHECK --interval=1s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]
