# Author: Milos Buncic
# Date: 2017/10/14
# Description: Image modifier function (output: byte stream)
# Supported parameters:
#   url, width, height, scale, gray, invert, flip, mirror and fmt

import os
import sys
import json
import requests
from uuid import uuid4
from io import BytesIO
from PIL import Image, ImageOps


def json2dict(data):
  """
  Convert json to dict (output: dict)
  """
  try:
    return json.loads(data)
  except Exception as e:
    print('error: {}'.format(e))
    sys.exit()


def get_img(url, timeout=60):
  """
  Make request and return binary content
  """
  try:
    return requests.get(url, timeout=timeout).content
  except Exception as e:
    print('error: {}'.format(e))
    sys.exit()


def imgmod(image, **parms):
  """
  Image modifier (output: byte stream)
  """
  try:
    # Open and resize the image
    img = Image.open(BytesIO(image))
    if parms['width'] and parms['height']:
      newimg = img.resize((int(parms['width']), int(parms['height'])))
    elif parms['width']:
      newimg = img.resize((int(parms['width']), img.height))
    elif parms['height']:
      newimg = img.resize((img.width, int(parms['height'])))
    else:
      newimg = img.resize([
          int(size * float(parms['scale']))
          for size in img.size
        ])

    # Make image black and white
    if parms['gray']:
      newimg = ImageOps.grayscale(newimg)

    # Invert (negate) the image
    if parms['invert']:
      newimg = ImageOps.invert(newimg)

    # Flip the image vertically (top to bottom)
    if parms['flip']:
      newimg = ImageOps.flip(newimg)

    # Flip the image horizontally (left to right)
    if parms['mirror']:
      newimg = ImageOps.mirror(newimg)

    # Send image as byte stream on stdout
    parms['fmt'] = 'jpeg' if parms['fmt'].lower() == 'jpg' else parms['fmt']
    filename = '/dev/shm/{}.{}'.format(
        uuid4(), parms['fmt']
      ).replace('-', '')
    newimg.save(filename, parms['fmt'])
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


def handle(data, **parms):
  """
  Caller function (will be called by run.py)
  """
  # Collect parms from stdin (json), if they don't exist, try query strings
  parms = json2dict(data) if data else parms

  cfg_parms = [
    'url',
    'width',
    'height',
    'scale',
    'gray',
    'invert',
    'flip',
    'mirror',
    'fmt'
  ]

  # Collect defined and set default values for supported parameters
  for p in cfg_parms:
    if p in ['url', 'width', 'height']:
      parms[p] = parms.get(p)
    elif p == 'scale':
      parms[p] = parms.get(p) if parms.get(p) else 1.0
    elif p == 'fmt':
      parms[p] = parms.get(p) if parms.get(p) else 'jpeg'
    else:
      # gray, invert, flip, mirror
      parms[p] = True if parms.get(p) == 'true' else False

  # Start modifying the image
  imgmod(get_img(parms['url']), **parms)
