# Author: Milos Buncic
# Date: 2017/10/14
# Description: Convert YAML to JSON and vice versa (OpenFaaS function)

import os
import sys
import json
import yaml


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


def handle(data, **parms):
  if parms.get('reverse') == 'true':
    print(json2yaml(data))
  else:
    print(yaml2json(data))
