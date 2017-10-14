# docker build -t <function_name> .

FROM python:3-alpine

ENV fprocess="python3 run.py" \
    cgi_headers="true"

WORKDIR /src

COPY . .

ADD https://github.com/openfaas/faas/releases/download/0.6.6c/fwatchdog /usr/bin
RUN chmod +x /usr/bin/fwatchdog \
 && pip3 install -r requirements.txt -r function/requirements.txt \
 && rm -vf requirements.txt function/requirements.txt

HEALTHCHECK --interval=1s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]
