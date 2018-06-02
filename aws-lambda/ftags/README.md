FTags
======

About
-----

Simple AWS lambda function for fetching tags for specified instance id

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

or if you are using [AWS named profiles](https://docs.aws.amazon.com/cli/latest/userguide/cli-multiple-profiles.html)

```plain
sls deploy -v --aws-profile $profilename
```

Because we're going to use API gateway to trigger an event, after successful deployment HTTP endpoints will be printed out in your console

**Note:** This is just an example endpoint, URL will look different for you

```plain
endpoints:
  GET - https://llecvyp03h.execute-api.eu-central-1.amazonaws.com/prod/ftags
```

If you perhaps only want to redeploy a function itself you can use this command

```plain
sls deploy function -f ftags
```

Invoke
------

 **query string**                    | **default**         | **description**
:------------------------------------|:--------------------|:-------------
`instance_id=i-0da1cd1ade0980159`    | mandatory parameter | EC2 instance ID

**Note:** If you are sending request from EC2 instance itself you can discover `instance_id` simply by sending request to the local metadata HTTP API

```bash
curl -s http://169.254.169.254/latest/meta-data/instance-id | xargs
```

Now use `instance_id` to fetch EC2 tags

```bash
curl -sSL -H 'x-api-key: a9FWDjfn8X7y7QgExAB3q21CZ7CRME584qo5MmSy' 'https://lleetyp04h.execute-api.eu-central-1.amazonaws.com/prod/ftags?instance_id=i-0da1cd1ade0980159'
```

Remove
------

Remove the whole stack

```plain
sls remove -v
```
