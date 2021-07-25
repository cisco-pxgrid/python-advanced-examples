# pxGrid Python Advanced Examples

The pxGrid python samples demonstrate how to develop pxGrid clients in python.

## Before Running Samples

- Install Python 3.6 or later
- Install necessary python packages using pip:

        ~$ pip3 install -r requirements.txt

## Description Of Samples

There are several simple test scripts:

| Script Name | Description |
|:--|:--|
| `session-query-by-ip` | performs a query on the session topic using a given IP address
| `session-query-all` | downloads all current sessions
| `sgacls-query-all` | download all current SG-ACL definitions
| `px-subscribe` | general purpose script to display details on multiple services and to all subscriptions for named services and topics


## To Generate pxGrid Certificates from ISE

If you wish to mutual cert-based authentication:

- Navigate to ISE Admin GUI via any web browser and authorized login
- Navigate to Administration -> pxGrid Services
- Click on the Certificates tab
- Fill in the form as follows:
    - I want to: **Generate a single certificate (without a certificate signing request)**
        - Common Name (CN): {fill in any name}
        - Certificate Download Format: Certificate in Privacy Enhanced Electronic Mail (PEM) format, key in PKCS8 PEM format (including certificate chain)
        - Certificate Password: {fill in a password}
        - Confirm Password: {fill in the same password as above}
- Click the 'Create' button. A zip file should download to your machine
- Extract the downloaded file.


## Sample Invocations

### `px-subscribe`

#### Using password authentication plus server public cert


```
$ px-subscribe \
    -a tl-enn-ise-1.cisco.com \
    -n nodename \
    -s /path/to/ise/public/server/cert \
    -w node-access-secret \
    --services
[
  {
    "services": [
      {
        "name": "com.cisco.ise.mdm",
        "nodeName": "ise-admin-tl-enn-ise-1",
        "properties": {
          "endpointTopic": "/topic/com.cisco.ise.mdm.endpoint",
          "restBaseURL": "https://tl-enn-ise-1.cisco.com:8910/pxgrid/mdm/bd",
          "restBaseUrl": "https://tl-enn-ise-1.cisco.com:8910/pxgrid/ise/mdm",
          "wsPubsubService": "com.cisco.ise.pubsub"
        }
      }
    ]
  },
  ...etc...
```

#### Ignoring server cert check

Please note that this is **_unsafe for production_**:

```
$ px-subscribe \
    -a tl-enn-ise-1.cisco.com \
    -n nodename \
    -w node-access-secret \
    --services
/opt/git-repos/pxgrid-rest-ws/python/config.py:95: UserWarning: check_hostname and cert not used; unsafe for production use
  warnings.warn("check_hostname and cert not used; unsafe for production use")
[
  {
    "services": [
      {
        "name": "com.cisco.ise.mdm",
        "nodeName": "ise-admin-tl-enn-ise-1",
        "properties": {
          "endpointTopic": "/topic/com.cisco.ise.mdm.endpoint",
          "restBaseURL": "https://tl-enn-ise-1.cisco.com:8910/pxgrid/mdm/bd",
          "restBaseUrl": "https://tl-enn-ise-1.cisco.com:8910/pxgrid/ise/mdm",
          "wsPubsubService": "com.cisco.ise.pubsub"
        }
      }
    ]
  },
  ...etc...
```

#### Subscribing for sessions ignoring server cert check

Please note that this is **_unsafe for production_**:

```
$ px-subscribe \
    -a tl-enn-ise-1.cisco.com \
    -n nodename \
    -w node-access-secret \
    --service com.cisco.ise.session \
    --topic sessionTopic
/opt/git-repos/pxgrid-rest-ws/python/config.py:95: UserWarning: check_hostname and cert not used; unsafe for production use
  warnings.warn("check_hostname and cert not used; unsafe for production use")
2020-03-31 09:45:13,980:stomp:DEBUG:write
2020-03-31 09:45:13,980:ws_stomp:DEBUG:stomp_connect completed
2020-03-31 09:45:13,980:stomp:DEBUG:write
2020-03-31 09:45:13,981:ws_stomp:DEBUG:stomp_subscribe completed
2020-03-31 09:45:14,014:stomp:DEBUG:parse
2020-03-31 09:45:14,014:stomp:DEBUG:parse frame content:
2020-03-31 09:45:14,014:ws_stomp:DEBUG:STOMP CONNECTED version=1.2
```

### `session-query-all`

Using password authentication plus server public cert:

```
session-query-all \
    -a tl-enn-ise-1.cisco.com \
    -n nodename \
    -s /path/to/ise/public/server/cert
    -w node-access-secret
{"sessions":[]}
```

### `sgacls-query-all`

Using password authentication plus server public cert:

```
$ sgacls-query-all \
    -a 10.53.27.75 \
    -n einarnn \
    -s einarnn/tl-enn-ise-1.cisco.com_10.53.27.75.cer \
    -w PgnAQs5CEGyjj9xq \
| jq -C .
{
  "securityGroupAcls": [
    {
      "id": "8dfd0610-6e9a-11ea-8892-626791db3907",
      "name": "DOPE_00001",
      "description": "DOPE Test SGACL DOPE_00001",
      "ipVersion": "IPV4",
      "acl": "permit tcp dst range 1 10 \ndeny ip\n",
      "generationId": "0"
    },
    ...etc...
```
