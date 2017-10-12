About
-----

Simple [OpenFaaS](https://github.com/openfaas/faas) function that can be used for image manipulation  
Function is based on [pillow](http://pillow.readthedocs.io/en/latest/index.html) python module


Install
-------

[faas-cli](https://github.com/openfaas/faas-cli)


Build
-----

Build docker image
```
docker build --no-cache -t imgmod .
```


Deploy
------

Deploy function  
**Note:** replace `gateway: http://<gateway_ip>:<gateway_port>` and `image: imgmod:latest` before deploy
```
faas-cli deploy -f imgmod.yaml
```


Execute
-------

 **query string**                    | **default**         | **description**
:------------------------------------|:--------------------|:-------------
`url=http://example.com/image.jpg`   | mandatory option    | source image
`fmt=png`                            | jpeg                | image format ([supported formats](http://pillow.readthedocs.io/en/latest/handbook/image-file-formats.html#image-file-formats))
`scale=0.5`                          | 1.0 (100%)          | scale the image up/down (in percentage)
`gray=true`                          | false               | make the image black and white
`negate=true`                        | false               | invert (negate) the image

**Note:** replace `<gateway_ip>:<gateway_port>` placeholders before execution

Keep original image size just encode it to JPEG format
```
curl -sSL -X POST -o test.jpg 'http://<gateway_ip>:<gateway_port>/function/imgmod?url=http://example.com/image.png'
```

Scale image up to 150% and encode it to PNG format
```
curl -sSL -X POST -o test.png 'http://<gateway_ip>:<gateway_port>/function/imgmod?url=http://example.com/image.png&scale=1.5&fmt=png'
```

Scale image down to 10%, encode it to PNG format and make it black and white
```
curl -sSL -X POST -o test.png 'http://<gateway_ip>:<gateway_port>/function/imgmod?url=http://example.com/image.png&scale=0.1&fmt=png&gray=true'
```

Scale image down to 60%, encode it to JPEG format and negate the colors
```
curl -sSL -X POST -o test.jpg 'http://<gateway_ip>:<gateway_port>/function/imgmod?url=http://example.com/image.png&scale=0.6&fmt=jpg&negate=true'
```


Remove
------

Remove previously deployed function
```
faas-cli rm -f imgmod.yaml
```