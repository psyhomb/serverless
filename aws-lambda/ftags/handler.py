# Author: Milos Buncic
# Date: 2018/06/01
# Description: Fetch EC2 tags for specified instance id

import json
import boto3


ec2_client = boto3.client('ec2')


def collect_tags(instance_id):
  """
  Collect tags for specified instance id (output: dict)
  """
  r = ec2_client.describe_tags(
    Filters = [
      {
        'Name': 'resource-type',
        'Values': [
          'instance'
        ]
      },
      {
        'Name': 'resource-id',
        'Values': [
          instance_id
        ]
      }
    ],
    MaxResults = 100,
    # NextToken = 'NextBlockOfTags'
  )

  tags = {}
  for e in r['Tags']:
    tags[e['Key']] = e['Value']

  return tags


def ftags(event, context):
  """
  Fetch and return EC2 tags (output: json)
  """
  # print(event)

  print('Retrieving instance id...')
  instance_id = ''
  if event.get('queryStringParameters', {}):
    instance_id = event.get('queryStringParameters').get('instance_id', '')

  if instance_id:
    print('Fetching EC2 tags...')
    tags = collect_tags(instance_id)

    status_code = 200
    body = {
      'data': {
        'instance_id': instance_id,
        'tags': tags
      }
    }
  else:
    status_code = 400
    body = {
      'message': 'Missing instance_id'
    }

  return {
    'statusCode': status_code,
    'body': json.dumps(body)
  }
