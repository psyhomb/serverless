# Author: Milos Buncic
# Date: 2017/10/14
# Description: Image modifier function
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
#     'fmt': (str,),
#     'filename': (str,)
#   }

import os
import sys
import json
import boto3
import requests
from uuid import uuid4
from io import BytesIO
from PIL import Image, ImageOps


s3_client = boto3.client('s3')


def s3_put(fp, key):
  """
  Put object to s3 bucket (output: dict)
  """
  bucket = os.environ['BUCKET'] if os.environ.get('BUCKET') else ''

  try:
    res = s3_client.put_object(
      ACL='private',
      Body=fp,
      Bucket=bucket,
      Key=key
    )
  except Exception as e:
    err_msg = '{}'.format(e)
    print(err_msg)
    raise Exception(502, err_msg)

  return res


def value2bool(d):
  """
  Convert specific string values to boolean (input: dict, output: dict)
  'true' to True and 'false' to False
  """
  for k,v in d.items():
    if v.lower() == 'true':
      d[k] = True
    elif v.lower() == 'false':
      d[k] = False

  return d


def json2dict(data):
  """
  Convert json to dict (input: json, output: dict)
  """
  try:
    d = json.loads(data)
  except ValueError as e:
    err_msg = 'Bad JSON format: {}'.format(e)
    print(err_msg)
    raise ValueError(400, err_msg)
  except TypeError as e:
    err_msg = 'Wrong type: {}'.format(e)
    print(err_msg)
    raise TypeError(400, err_msg)

  return d


def get_img(url, timeout=60):
  """
  Make request and return binary content
  """
  try:
    r = requests.get(url, timeout=timeout)
  except Exception as e:
    err_msg = 'Request error: {}'.format(e)
    print(err_msg)
    raise Exception(400, err_msg)
  else:
    if r.status_code == 200:
      return r.content
    else:
      msg = 'Fetching image from remote source failed'
      print(msg)
      raise Exception(r.status_code, msg)


def imgmod(event, context):
  """
  Image modifier caller function
  """
  # print(event)

  try:
    if event.get('body'):
      print('Collecting image parameters from body payload')
      parms = json2dict(event['body'])
    else:
      print('Collecting image parameters from query string')
      parms = value2bool(event.get('queryStringParameters'))

    print('Downloading the image')
    data = get_img(parms.get('url'), timeout=30)

    # Open the image
    img = Image.open(BytesIO(data))

    # Apply image modifiers
    if parms:
      # Resize the image
      print('Modifying the image')
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
      if parms.get('gray') is True:
        img = ImageOps.grayscale(img)

      # Invert (negate) the image
      if parms.get('invert') is True:
        img = ImageOps.invert(img)

      # Flip the image vertically (top to bottom)
      if parms.get('flip') is True:
        img = ImageOps.flip(img)

      # Flip the image horizontally (left to right)
      if parms.get('mirror') is True:
        img = ImageOps.mirror(img)

    # Image format (default: 'jpeg')
    fmt = parms['fmt'] if parms.get('fmt') else 'jpeg'

    # Image name (default: generated UUID)
    if parms.get('filename'):
      filename = '{}.{}'.format(
          os.path.splitext(parms['filename'])[0], fmt
        )
    else:
      filename = '{}.{}'.format(uuid4(), fmt)

    print('Pushing the image {} to S3'.format(filename))
    out_file = BytesIO()
    img.save(out_file, fmt)
    out_file.seek(0)
    res = s3_put(out_file, filename)
  except Exception as e:
    err_code = e.args[0]
    err_msg = e.args[1]

    return {
      'statusCode': err_code,
      'body': json.dumps({
        'message': '{}'.format(err_msg)
      })
    }
  else:
    msg = 'Image {} successfully pushed to S3'.format(filename)
    print(msg)

    return {
      'statusCode': 200,
      'headers': {
        'Location': filename
      },
      'body': json.dumps({
        'message': msg
      })
    }
  finally:
    try:
      # Cleanup
      img.close()
      out_file.close()
    except:
      pass
