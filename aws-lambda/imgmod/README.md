About
-----

Simple AWS lambda function that can be used for image manipulation  
Function is based on [pillow](http://pillow.readthedocs.io/en/latest/index.html) python module


Install
-------

The [Serverless Framework](https://serverless.com/framework/docs/providers/aws/guide/installation/) helps you develop and deploy your AWS Lambda functions, along with the AWS infrastructure resources they require.
It's a CLI that offers structure, automation and best practices out-of-the-box, allowing you to focus on building sophisticated,
event-driven, serverless architectures, comprised of Functions and Events.

The Serverless Framework is different from other application frameworks because:

- It manages your code as well as your infrastructure
- It supports multiple languages (Node.js, Python, Java, and more)


Deploy
------

Before we can start deploymnet process we first have to set a unique bucket name in the `serverless.yaml` configuration file  
This is the S3 bucket where images will be pushed to after every invocation
```yaml
custom:
  bucket: <bucket_name>
```

Install required plugins
```
sls plugin install -n serverless-python-requirements
```

Deploy entire stack
```
sls deploy -v
```

Because we're going to use API gateway to trigger an event, after successful deployment HTTP endpoints will be printed out in your console  
**Note:** This is just an example endpoint, URL will look totally different for you
```
endpoints:
  POST - https://llecvyp03h.execute-api.eu-central-1.amazonaws.com/dev/imgmod
```

If you perhaps only want to redeploy a function itself you can use this command
```
sls deploy function -f imgmod
```


Invoke
------

 **query string**                    | **default**         | **description**
:------------------------------------|:--------------------|:-------------
`url=http://example.com/image.jpg`   | mandatory parameter | source image
`width=1920`                         | none                | explicitly change the image width (has precedence over scale)
`height=1080`                        | none                | explicitly change the image height (has precedence over scale)
`scale=0.5`                          | none                | scale the image up or down (percentage in decimal form)
`gray=true`                          | false               | make the image black and white
`invert=true`                        | false               | invert (negate) the image
`flip=true  `                        | false               | flip the image vertically (top to bottom)
`mirror=true`                        | false               | flip the image horizontally (left to right)
`fmt=png`                            | jpeg                | image format ([supported formats](http://pillow.readthedocs.io/en/latest/handbook/image-file-formats.html#image-file-formats))
`filename=foo-bar`                   | auto-generated      | filename of the image object that will be created on S3


Keep original image, just change the format to JPEG
```
curl -sSL -X POST 'https://llecvyp03h.execute-api.eu-central-1.amazonaws.com/dev/imgmod?url=http://example.com/image.png'
```

Scale the image up to 150% and change the format to PNG
```
curl -sSL -X POST 'https://llecvyp03h.execute-api.eu-central-1.amazonaws.com/dev/imgmod?url=http://example.com/image.png&scale=1.5&fmt=png'
```

Scale the image down to 10%, change the format to PNG and make the image black and white
```
curl -sSL -X POST 'https://llecvyp03h.execute-api.eu-central-1.amazonaws.com/dev/imgmod?url=http://example.com/image.png&scale=0.1&fmt=png&gray=true'
```

Scale the image down to 60%, change the format to JPEG and negate the colors
```
curl -sSL -X POST 'https://llecvyp03h.execute-api.eu-central-1.amazonaws.com/dev/imgmod?url=http://example.com/image.png&scale=0.6&fmt=jpg&invert=true'
```

Change the image width and height (1280x720) explicitly
```
curl -sSL -X POST 'https://llecvyp03h.execute-api.eu-central-1.amazonaws.com/dev/imgmod?url=http://example.com/image.png&width=1280&height=720'
```


or you can send any of these parameters via body payload in json format  
`parms.json`
```json
{
  "url": "http://example.com/image.jpg",
  "scale": 0.5,
  "gray": true,
  "mirror": false
}
```

```
curl -sSL -X POST -d '@parms.json' 'https://llecvyp03h.execute-api.eu-central-1.amazonaws.com/dev/imgmod'
```

or pass the parameters inline

```
curl -sSL -X POST -d '{"url": "http://example.com/image.png", "gray": "true"}' 'https://llecvyp03h.execute-api.eu-central-1.amazonaws.com/dev/imgmod'
```


Remove
------

Remove the whole stack  
**WARNING:** In order for this command to succeed S3 bucket must be empty
```
sls remove -v
```
