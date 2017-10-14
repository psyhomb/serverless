# Author: Milos Buncic
# Date: 2017/10/14

import os
import sys
from function import handler


def get_stdin():
  """
  Collect data received on stdin (output: string)
  """
  s = ''
  for l in sys.stdin:
    s += l

  return s


def get_qs():
  """
  Collect query string parameters (output: dict)
  """
  d = {}

  qs = os.environ.get('Http_Query')

  if qs is not None and '=' in qs:
    qs = qs[qs.find('?')+1:]
    for e in qs.split('&'):
      for k,v in [e.split('=')]:
        d[k] = v

  return d


if __name__ == '__main__':
  data = get_stdin()
  parms = get_qs()

  handler.handle(data, **parms)
