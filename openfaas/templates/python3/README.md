About
-----

<!-- Short description -->


Install
-------

[faas-cli](https://github.com/openfaas/faas-cli)


Deploy
------

```
faas-cli deploy -f <function_name>.yaml
```


Execute
-------

### faas-cli

```
echo <body_payload> | faas-cli invoke -f <function_name>.yaml --name <function_name>
```

### curl

```
curl -sSL -X POST --data-binary <body_payload> 'http://<gateway_ip>:<gateway_port>/function/<function_name>?<query_string>'
```


Remove
------

```
faas-cli rm -f <function_name>.yaml
```
