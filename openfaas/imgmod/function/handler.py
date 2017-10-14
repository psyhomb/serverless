# Author: Milos Buncic
# Date: 2017/10/14
# Description: Image modifier function (output: byte stream)
# Supported parameters:
#   url, width, height, scale, gray, invert, flip, mirror and fmt

import os
import sys
import requests
from uuid import uuid4
from io import BytesIO
from PIL import Image, ImageOps


def handle(data, **parms):
  # Collect values for supported parameters
  url = parms.get('url')
  width = parms.get('width')
  height = parms.get('height')
  scale = parms.get('scale') if parms.get('scale') else 1.0
  gray = True if parms.get('gray') == 'true' else False
  invert = True if parms.get('invert') == 'true' else False
  flip = True if parms.get('flip') == 'true' else False
  mirror = True if parms.get('mirror') == 'true' else False
  fmt = parms.get('fmt') if parms.get('fmt') else 'jpeg'

  try:
    # Get image from the web
    r = requests.get(url, timeout=30)

    # Open and resize the image
    img = Image.open(BytesIO(r.content))
    if width and height:
      newimg = img.resize((int(width), int(height)))
    elif width:
      newimg = img.resize((int(width), img.height))
    elif height:
      newimg = img.resize((img.width, int(height)))
    else:
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
