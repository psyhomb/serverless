#!/usr/bin/env python3
# Author: Milos Buncic
# Date: 2017/10/10
# Description: Image modifier (OpenFaaS function)

import os
import sys
import requests
from uuid import uuid4
from io import BytesIO
from PIL import Image
from PIL import ImageOps


# def get_stdin():
#   """
#   Collect data received on stdin (output: string)
#   """
#   s = ''
#   for l in sys.stdin:
#     s += l
#
#   return s


def get_parms():
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


def imgmod(**parms):
  """
  Image modifier function (output: byte stream)
  supported parameters: url, format, scale, gray and invert
  """
  # Collect values for supported parameters
  url = parms.get('url')
  fmt = parms.get('fmt') if parms.get('fmt') else 'jpeg'
  scale = parms.get('scale') if parms.get('scale') else 1.0
  gray = parms.get('gray') if parms.get('gray') else False
  invert = parms.get('invert') if parms.get('invert') else False
  flip = parms.get('flip') if parms.get('flip') else False
  mirror = parms.get('mirror') if parms.get('mirror') else False

  try:
    # Get image from the web
    r = requests.get(url, timeout=30)

    # Open and resize the image
    img = Image.open(BytesIO(r.content))
    newimg = img.resize([
        int(size * float(scale))
        for size in img.size
      ])

    # Make image black and white
    if gray:
      newimg = ImageOps.grayscale(newimg)

    # Invert (negate) the image
    if invert:
      newimg = ImageOps.invert(newimg)

    # Flip the image vertically (top to bottom)
    if flip:
      newimg = ImageOps.flip(newimg)

    # Flip the image horizontally (left to right)
    if mirror:
      newimg = ImageOps.mirror(newimg)

    # Send image as byte stream on stdout
    fmt = 'jpeg' if fmt.lower() == 'jpg' else fmt
    filename = '/dev/shm/{}.{}'.format(uuid4(), fmt).replace('-', '')
    newimg.save(filename, fmt)
    with open(filename, 'rb') as f:
      sys.stdout.buffer.write(f.read())
  except Exception as e:
    print('error: {}'.format(e), file=sys.stderr)
  finally:
    try:
      # Cleanup
      newimg.close()
      img.close()
      os.remove(filename)
    except:
      pass


def main():
  parms = get_parms()

  parms['gray'] = True if parms.get('gray') == 'true' else False
  parms['invert'] = True if parms.get('invert') == 'true' else False
  parms['flip'] = True if parms.get('flip') == 'true' else False
  parms['mirror'] = True if parms.get('mirror') == 'true' else False

  if parms.get('url'):
    imgmod(**parms)
  else:
    print(
      'Missing URL parameter in the query string',
      'e.g. /?url=http://example.com/image.jpeg',
      file=sys.stderr
    )


if __name__ == '__main__':
  main()
