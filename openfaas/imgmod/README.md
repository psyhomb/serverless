imgmod
======

About
-----

Simple [OpenFaaS](https://github.com/openfaas/faas) function that can be used for image manipulation.  
Function is based on [pillow](http://pillow.readthedocs.io/en/latest/index.html) python module.

Install
-------

[faas-cli](https://github.com/openfaas/faas-cli)

Build
-----

Build docker image

```plain
faas-cli build --no-cache --image imgmod --name imgmod --lang Dockerfile --handler .
```

Deploy
------

Deploy function

**Note:** replace `gateway: http://<gateway_ip>:<gateway_port>` and `image: imgmod` before deploy

```plain
faas-cli deploy -f imgmod.yaml
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

**Note:** replace `<gateway_ip>:<gateway_port>` placeholders before execution

Keep original image just encode it to JPEG format

```plain
curl -sSL -X POST -o test.jpg 'http://<gateway_ip>:<gateway_port>/function/imgmod?url=http://example.com/image.png'
```

Scale the image up to 150% and encode it to PNG format

```plain
curl -sSL -X POST -o test.png 'http://<gateway_ip>:<gateway_port>/function/imgmod?url=http://example.com/image.png&scale=1.5&fmt=png'
```

Scale the image down to 10%, encode it to PNG format and make it black and white

```plain
curl -sSL -X POST -o test.png 'http://<gateway_ip>:<gateway_port>/function/imgmod?url=http://example.com/image.png&scale=0.1&fmt=png&gray=true'
```

Scale the image down to 60%, encode it to JPEG format and negate the colors

```plain
curl -sSL -X POST -o test.jpg 'http://<gateway_ip>:<gateway_port>/function/imgmod?url=http://example.com/image.png&scale=0.6&fmt=jpg&invert=true'
```

Change the image width and height (1280x720) explicitly

```plain
curl -sSL -X POST -o test.jpg 'http://<gateway_ip>:<gateway_port>/function/imgmod?url=http://example.com/image.png&width=1280&height=720'
```

or you can send any of these parameters via body payload in json format

**Note:** boolean values must be enclosed within quotes

```json
{
  "url": "http://example.com/image.jpg",
  "gray": "true"
}
```

```bash
echo -n '{"url": "http://example.com/image.png", "gray": "true"}' | faas-cli invoke imgmod > test.jpg
```

```bash
cat parms.json | faas-cli invoke imgmod > test.jpg
```

```plain
curl -sSL -X POST -d '{"url": "http://example.com/image.png", "gray": "true"}' -o test.jpg 'http://<gateway_ip>:<gateway_port>/function/imgmod'
```

```plain
curl -sSL -X POST -d '@parms.json' -o test.jpg 'http://<gateway_ip>:<gateway_port>/function/imgmod'
```

Remove
------

Remove previously deployed function

```plain
faas-cli rm -f imgmod.yaml
```
