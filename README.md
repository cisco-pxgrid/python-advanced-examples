# pxGrid Python Advanced Examples

This repository contains the source code for a number of advanced pxGrid examples written in python. The code is based on extending a set of examples found in [https://github.com/cisco-pxgrid/pxgrid-rest-ws](https://github.com/cisco-pxgrid/pxgrid-rest-ws). Please note that what was initially common code has diverged from the code in that repository.

All the examples here are based on exercising the pxGrid 2.0 services defined at [https://github.com/cisco-pxgrid/pxgrid-rest-ws/wiki/pxGrid-Provider](https://github.com/cisco-pxgrid/pxgrid-rest-ws/wiki/pxGrid-Provider). However, not all services will necessarily be exercised, but examples will be added over time.

Basic pxGrid setup on ISE is **not** covered here. Some instructions are provided for creating a suitable client cert for use with the Python examples.

Each sample script, when able to run successfully, produces JSON to STDOUT, allowing processing by tools such as [jq](https://stedolan.github.io/jq/) or any other that ingests JSON. For example, using the `session-query-all` example combined with [jq](https://stedolan.github.io/jq/) to extract an array of client MAC addresses for currently attached sessions:

```
$ session-query-all
    --host HOSTNAME \
    -n NODENAME \
    -w NODESECRET \
    --insecure | \
    jq -C '[ .sessions[] | select(.state == "STARTED") | .macAddress ]'
[
  "00:50:56:94:39:9F",
  "00:50:56:94:6F:90",
  "00:50:56:94:91:67",
  "00:50:56:94:AA:9B",
  "00:50:56:94:D8:7E",
  "00:50:56:94:DF:7D",
  "00:50:56:94:E4:31",
  "00:50:56:94:E7:97"
]
```


## Before Running Samples

All the examples may be installed using `pip`, making the examples available in your environment.

1. Have Python 3.8 or later available on your system
2. Optionally (but strongly recommended) create a virtual environment
2. Install the examples and support module using pip:

        pip3 install pxgrid-util


## Description Of Samples

There are several simple test scripts, listend below.

| Script Name | Description |
|:--|:--|
| `anc-policy` | Download ANC policies, endpoints with ANC policies applied, and apply ANC policy |
| `matrix-query-all` | Download all cells of the TrustSec policy matrix |
| `profiles-query-all` | Download all ISE Profiler profiles |
| `px-subscribe` | General purpose utility to display details on multiple services and to allow subscriptions to topics of named services |
| `session-query-all` | Download all current sessions |
| `session-query-by-ip` | Perform a query on the session topic using a given IP address |
| `sgacls-query-all` | Download all current SG-ACL definitions |
| `sgts-query-all`| Download all SGT definitions |
| `sxp-query-bindings` | Download all SXP bindings |
| `system-query-all` | |
| `user-groups-query` ||

Each script has, at minimum, a set of shared options relating to pxGrid node name, shared secrets, cert parameters, etc. These common options are:

```
  -h, --help            show this help message and exit
  -a HOSTNAME, --hostname HOSTNAME
                        pxGrid controller host name (multiple ok)
  --port PORT           pxGrid controller port (default 8910)
  -n NODENAME, --NODENAME NODENAME
                        Client node name
  -w PASSWORD, --password PASSWORD
                        Password (optional)
  -d DESCRIPTION, --description DESCRIPTION
                        Description (optional)
  -c CLIENTCERT, --clientcert CLIENTCERT
                        Client certificate chain pem filename (optional)
  -k CLIENTKEY, --clientkey CLIENTKEY
                        Client key filename (optional)
  -p CLIENTKEYPASSWORD, --clientkeypassword CLIENTKEYPASSWORD
                        Client key password (optional)
  -s SERVERCERT, --servercert SERVERCERT
                        Server certificates pem filename
  --insecure            Allow insecure server connections when using SSL
  -v, --verbose         Verbose output
```


## Sample Invocations

Note that most of the examples below focus on using pxGrid 2.0 **without certs**, enabled by the command line option `--insecure`. This is for simplicity. Please refer to pxGrid 2.0 documentation on DevNet or to the [basic examples repo](ttps://github.com/cisco-pxgrid/pxgrid-rest-ws) for examples of how to run with certs.

Also, not all example scripts will be demonstrated here.


### `px-subscribe`

#### Using password authentication plus server public cert

The option `--insecure` isn't passed here as we provide a server cert.

```
$ px-subscribe \
    -a your.server.fqdn \
    -n NODENAME \
    -s /path/to/ise/public/server.cer \
    -w NODESECRET \
    --services
[
  {
    "services": [
      {
        "name": "com.cisco.ise.mdm",
        "NODENAME": "ise-admin-tl-enn-ise-1",
        "properties": {
          "endpointTopic": "/topic/com.cisco.ise.mdm.endpoint",
          "restBaseURL": "https://your.server.fqdn:8910/pxgrid/mdm/bd",
          "restBaseUrl": "https://your.server.fqdn:8910/pxgrid/ise/mdm",
          "wsPubsubService": "com.cisco.ise.pubsub"
        }
      }
    ]
  },
  ...etc...
]
```



#### Ignoring server cert check

Please note that this is **_unsafe for production_**:

```
$ px-subscribe \
    -a your.server.fqdn \
    -n NODENAME \
    -w NODESECRET \
    --services \
    --insecure
[
  {
    "services": [
      {
        "name": "com.cisco.ise.mdm",
        "NODENAME": "ise-admin-tl-enn-ise-1",
        "properties": {
          "endpointTopic": "/topic/com.cisco.ise.mdm.endpoint",
          "restBaseURL": "https://your.server.fqdn:8910/pxgrid/mdm/bd",
          "restBaseUrl": "https://your.server.fqdn:8910/pxgrid/ise/mdm",
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
    -a your.server.fqdn \
    -n NODENAME \
    -w NODESECRET \
    --service com.cisco.ise.session \
    --topic sessionTopic
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
    -a your.server.fqdn \
    -n NODENAME \
    -s /path/to/ise/public/server/cert
    -w NODESECRET
{"sessions":[]}
```

### `sgacls-query-all`

Using password authentication plus server public cert:

```
$ sgacls-query-all \
    --host HOSTNAME \
    -n NODENAME \
    -w NODESECRET \
    --insecure | \
    jq -C .
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

## To Generate pxGrid Certificates From ISE

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

