Imgmod
===============

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

Before we can start deployment process we first have to set a unique bucket name and configure unique API key in the `serverless.yaml` configuration file

**Note:** S3 bucket is where modified images will be pushed to after every invocation (replace `<BUCKET_NAME>`)

```yaml
custom:
  bucket: <BUCKET_NAME>
```

**Note:** Use `x-api-key` header on the client side if you want to provide valid API key to the API Gateway

**Note:** API key specified under `apiKeys` section is just a name, `API_KEY` itself will be automatically generated and printed out at the end once the deploy has completed successfully.

```yaml
provider:
  apiKeys:
    - ${opt:stage, self:provider.stage}-<API_KEY_NAME>
```

Install required plugins

**Note:** `serverless-python-requirements` plugin requires `node` version 6+

```plain
sls plugin install -n serverless-python-requirements
```

Deploy entire stack

```plain
sls deploy -v
```

Because we're going to use API gateway to trigger an event, after successful deployment HTTP endpoints will be printed out in your console

**Note:** This is just an example endpoint, URL will look different for you

```plain
endpoints:
  POST - https://llecvyp03h.execute-api.eu-central-1.amazonaws.com/dev/imgmod
```

If you perhaps only want to redeploy a function itself you can use this command

```plain
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
`flip=true`                        | false               | flip the image vertically (top to bottom)
`mirror=true`                        | false               | flip the image horizontally (left to right)
`fmt=png`                            | jpeg                | image format ([supported formats](http://pillow.readthedocs.io/en/latest/handbook/image-file-formats.html#image-file-formats))
`filename=foo-bar`                   | auto-generated      | filename of the image object that will be created on S3

Keep original image, just change the format to JPEG

```bash
curl -sSL -X POST 'https://llecvyp03h.execute-api.eu-central-1.amazonaws.com/dev/imgmod?url=http://example.com/image.png'
```

Scale the image up to 150% and change the format to PNG

```bash
curl -sSL -X POST 'https://llecvyp03h.execute-api.eu-central-1.amazonaws.com/dev/imgmod?url=http://example.com/image.png&scale=1.5&fmt=png'
```

Scale the image down to 10%, change the format to PNG and make the image black and white

```bash
curl -sSL -X POST 'https://llecvyp03h.execute-api.eu-central-1.amazonaws.com/dev/imgmod?url=http://example.com/image.png&scale=0.1&fmt=png&gray=true'
```

Scale the image down to 60%, change the format to JPEG and negate the colors

```bash
curl -sSL -X POST 'https://llecvyp03h.execute-api.eu-central-1.amazonaws.com/dev/imgmod?url=http://example.com/image.png&scale=0.6&fmt=jpg&invert=true'
```

Change the image width and height (1280x720) explicitly

```bash
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

```bash
curl -sSL -X POST -d '@parms.json' 'https://llecvyp03h.execute-api.eu-central-1.amazonaws.com/dev/imgmod'
```

or pass the parameters inline

```bash
curl -sSL -X POST -d '{"url": "http://example.com/image.png", "gray": "true"}' 'https://llecvyp03h.execute-api.eu-central-1.amazonaws.com/dev/imgmod'
```


Remove
------

Remove the whole stack

**WARNING:** In order for this command to succeed S3 bucket must be empty

```plain
sls remove -v
```
