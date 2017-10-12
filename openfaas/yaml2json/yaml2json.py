#!/usr/bin/env python3
# Author: Milos Buncic
# Date: 2017/10/07
# Description: Convert YAML to JSON and vice versa (OpenFaaS function)

import os
import sys
import json
import yaml


def get_stdin():
  """
  Collect data received on stdin (output: string)
  """
  s = ''
  for l in sys.stdin:
    s += l

  return s


def get_parms():
  """
  Collect querystring or header parameters (output: dict)
  Note: querystring has precedence over header
  """
  d = {}

  qs = os.environ.get('Http_Query')
  reverse = os.environ.get('Http_X_Reverse_Conversion')

  if qs is not None and '=' in qs:
    qs = qs[qs.find('?')+1:]
    for e in qs.split('&'):
      for k,v in [e.split('=')]:
        d[k] = v
  elif reverse == 'true':
    d['reverse'] = reverse

  return d


def yaml2json(data):
  """
  Convert YAML to JSON (output: JSON)
  """
  try:
    d = yaml.load(data, Loader=yaml.BaseLoader)
  except Exception as e:
    d = {'error': '{}'.format(e)}

  return json.dumps(d)


def json2yaml(data):
  """
  Convert JSON to YAML (output: YAML)
  """
  try:
    d = json.loads(data)
  except Exception as e:
    d = {'error': '{}'.format(e)}

  return yaml.dump(d, default_flow_style=False)


def main():
  parms = get_parms()

  if parms.get('reverse') == 'true':
    print(json2yaml(get_stdin()))
  else:
    print(yaml2json(get_stdin()))


if __name__ == '__main__':
  main()
