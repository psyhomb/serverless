About
-----

Simple OpenFaaS function for YAML to JSON conversion and vice versa


Install
-------

[faas-cli](https://github.com/openfaas/faas-cli)


Deploy
------

Deploy function  
**Note:** replace `gateway: http://<gateway_ip>:<gateway_port>` and `image: yaml2json` before deploy
```
faas-cli deploy -f yaml2json.yaml
```


Execute
-------

### faas-cli

Convert YAML to JSON
```bash
cat test.yaml | faas-cli invoke -f yaml2json.yaml --name yamltojson
```

### curl

**Note:** replace `<gateway_ip>:<gateway_port>` placeholders before execution

Convert YAML to JSON
```
curl -sSL -X POST --data-binary '@test.yaml' 'http://<gateway_ip>:<gateway_port>/function/yamltojson'
```

Convert JSON to YAML
```
curl -sSL -X POST --data-binary '@test.json' 'http://<gateway_ip>:<gateway_port>/function/yamltojson?reverse=true'
```


Remove
------

Remove previously deployed function
```
faas-cli rm -f yaml2json.yaml
```
