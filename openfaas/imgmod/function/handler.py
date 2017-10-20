# Author: Milos Buncic
# Date: 2017/10/14
# Description: Image modifier function (output: byte stream)
# Supported parameters:
#   parms = {
#     'url': (str,),
#     'width': (int,),
#     'height': (int,),
#     'scale': (float,),
#     'gray': (bool,),
#     'invert': (bool,),
#     'flip': (bool,),
#     'mirror': (bool,),
#     'fmt': (str,)
#   }

import os
import sys
import json
import requests
from io import BytesIO
from PIL import Image, ImageOps


def json2dict(data):
  """
  Convert json to dict (output: dict)
  """
  try:
    return json.loads(data)
  except ValueError as e:
    print('error: Bad JSON format: {}'.format(e), file=sys.stderr)
    sys.exit()


def get_img(url, timeout=60):
  """
  Make request and return binary content
  """
  try:
    r = requests.get(url, timeout=timeout)
  except Exception as e:
    print('error: {}'.format(e), file=sys.stderr)
    sys.exit()
  else:
    if r.status_code == 200:
      return r.content
    else:
      print(
        'error: Image fetching failed, http code: {}'.format(r.status_code),
        file=sys.stderr
      )
      sys.exit()


def imgmod(image, **parms):
  """
  Image modifier (output: byte stream)
  """
  try:
    # Open the image
    img = Image.open(BytesIO(image))

    # Apply image modifiers
    if parms:
      # Resize the image
      if parms.get('width') and parms.get('height'):
        img = img.resize((int(parms['width']), int(parms['height'])))
      elif parms.get('width'):
        img = img.resize((int(parms['width']), img.height))
      elif parms.get('height'):
        img = img.resize((img.width, int(parms['height'])))
      elif parms.get('scale'):
        img = img.resize([
            int(size * float(parms['scale']))
            for size in img.size
          ])

      # Make image black and white
      if parms.get('gray'):
        img = ImageOps.grayscale(img)

      # Invert (negate) the image
      if parms.get('invert'):
        img = ImageOps.invert(img)

      # Flip the image vertically (top to bottom)
      if parms.get('flip'):
        img = ImageOps.flip(img)

      # Flip the image horizontally (left to right)
      if parms.get('mirror'):
        img = ImageOps.mirror(img)

    # Define desired image format (default: 'jpeg')
    fmt = parms.get('fmt') if parms.get('fmt') else 'jpeg'

    # Send image as byte stream to stdout
    out_file = BytesIO()
    img.save(out_file, fmt)
    out_file.seek(0)
    sys.stdout.buffer.write(out_file.read())
  except Exception as e:
    print('error: {}'.format(e), file=sys.stderr)
  finally:
    try:
      # Cleanup
      img.close()
      out_file.close()
    except:
      pass


def handle(data, **parms):
  """
  Caller function (will be called by run.py)
  """
  # Collect parms from stdin (json), if they don't exist, try query strings
  parms = json2dict(data) if data else parms

  # Supported parameters
  cfg_parms = {
    'url': (str,),
    'width': (int,),
    'height': (int,),
    'scale': (float,),
    'gray': (bool,),
    'invert': (bool,),
    'flip': (bool,),
    'mirror': (bool,),
    'fmt': (str,)
  }

  # Convert some of the parameters to boolean data type
  for p in cfg_parms:
    if p in ['gray', 'invert', 'flip', 'mirror']:
      parms[p] = True if parms.get(p) == 'true' else False

  # Start modifying the image
  imgmod(get_img(parms.get('url')), **parms)
