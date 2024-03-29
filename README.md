
[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/cisco-pxgrid/python-advanced-examples)

# pxGrid Python Advanced Examples

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [pxGrid Python Advanced Examples](#pxgrid-python-advanced-examples)
  - [Introduction](#introduction)
  - [Before Running Samples](#before-running-samples)
  - [Description Of Samples](#description-of-samples)
  - [Sample Invocations](#sample-invocations)
    - [`px-publish`](#px-publish)
    - [`px-subscribe`](#px-subscribe)
      - [Using password authentication plus server public cert](#using-password-authentication-plus-server-public-cert)
      - [Ignoring server cert check](#ignoring-server-cert-check)
      - [Subscribing for sessions ignoring server cert check](#subscribing-for-sessions-ignoring-server-cert-check)
    - [`session-query-all`](#session-query-all)
    - [`sgacls-query-all`](#sgacls-query-all)
    - [anc-policy](#anc-policy)
      - [Get the policies you have defined in your deployment](#get-the-policies-you-have-defined-in-your-deployment)
      - [Get all endpoints with an ANC policy, including the applied policy](#get-all-endpoints-with-an-anc-policy-including-the-applied-policy)
      - [Get the policy applied to a specific endpoint, by MAC address](#get-the-policy-applied-to-a-specific-endpoint-by-mac-address)
      - [Apply policy by MAC address](#apply-policy-by-mac-address)
      - [Clear policy by MAC address](#clear-policy-by-mac-address)
      - [Apply policy by IP address](#apply-policy-by-ip-address)
      - [Clear policy by IP address](#clear-policy-by-ip-address)
  - [To Generate pxGrid Certificates From ISE](#to-generate-pxgrid-certificates-from-ise)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Introduction

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

1. Have **Python 3.8 or later** available on your system
2. Optionally (but strongly recommended) create a virtual environment
2. Install the examples and support module using pip:

        pip3 install pxgrid-util


## Description Of Samples

There are several simple test scripts, listend below.

| Script Name | Description |
|:--|:--|
| `anc-policy` | Download ANC policies, endpoints with ANC policies applied, and apply ANC policy |
| `create-new-pxgrid-account` | Create a simple password authentication pxGrid client if you have an ISE admin username and password |
| `matrix-query-all` | Download all cells of the TrustSec policy matrix |
| `profiles-query-all` | Download all ISE Profiler profiles |
| `px-publish` | Simple utility to publish a simple message to a custom service and topic. More of a template to copy. |
| `px-subscribe` | General purpose utility to display details on multiple services and to allow subscriptions to topics of named services |
| `session-query-all` | Download all current sessions |
| `session-query-by-ip` | Perform a query on the session topic using a given IP address |
| `sgacls-query-all` | Download all current SG-ACL definitions |
| `sgts-query-all`| Download all SGT definitions |
| `sxp-query-bindings` | Download all SXP bindings |
| `system-query-all` | Download performance or health metrics from an ISE installation |
| `user-groups-query` | Query for the groups associated with users authenticated to ISE |

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


### `px-publish`

This example uses `--insecure`.

```
$ px-publish \
   --insecure \
   -a ise-3-2.hareshaw.net \
   -w **************** \
   -n producer \
   --service com.cisco.einarnn.special \
   --topic customTopic \
   --verbose
2023-08-27 21:08:38,587:pxgrid_util.pxgrid:DEBUG:account_activate
2023-08-27 21:08:38,587:pxgrid_util.pxgrid:DEBUG:send_rest_request AccountActivate
2023-08-27 21:08:38,644:pxgrid_util.pxgrid:DEBUG:service_register com.cisco.einarnn.special
2023-08-27 21:08:38,644:pxgrid_util.pxgrid:DEBUG:send_rest_request ServiceRegister
2023-08-27 21:08:38,788:__main__:DEBUG:[service_register_response] {
2023-08-27 21:08:38,788:__main__:DEBUG:[service_register_response]   "id": "b96aa465-5252-41cd-a961-c43ab0c46475",
2023-08-27 21:08:38,788:__main__:DEBUG:[service_register_response]   "reregisterTimeMillis": 300000
2023-08-27 21:08:38,788:__main__:DEBUG:[service_register_response] }
2023-08-27 21:08:38,788:pxgrid_util.pxgrid:DEBUG:service_lookup com.cisco.einarnn.special
2023-08-27 21:08:38,788:pxgrid_util.pxgrid:DEBUG:send_rest_request ServiceLookup
2023-08-27 21:08:38,821:__main__:DEBUG:service lookup response:
2023-08-27 21:08:38,821:__main__:DEBUG:  {
2023-08-27 21:08:38,822:__main__:DEBUG:    "services": [
2023-08-27 21:08:38,822:__main__:DEBUG:      {
2023-08-27 21:08:38,822:__main__:DEBUG:        "name": "com.cisco.einarnn.special",
2023-08-27 21:08:38,822:__main__:DEBUG:        "nodeName": "producer",
2023-08-27 21:08:38,822:__main__:DEBUG:        "properties": {
2023-08-27 21:08:38,822:__main__:DEBUG:          "customTopic": "/topic/com.cisco.einarnn.special",
2023-08-27 21:08:38,822:__main__:DEBUG:          "wsPubsubService": "com.cisco.ise.pubsub"
2023-08-27 21:08:38,822:__main__:DEBUG:        }
2023-08-27 21:08:38,822:__main__:DEBUG:      }
2023-08-27 21:08:38,822:__main__:DEBUG:    ]
2023-08-27 21:08:38,822:__main__:DEBUG:  }
2023-08-27 21:08:38,822:pxgrid_util.pxgrid:DEBUG:service_lookup com.cisco.ise.pubsub
2023-08-27 21:08:38,822:pxgrid_util.pxgrid:DEBUG:send_rest_request ServiceLookup
2023-08-27 21:08:38,868:pxgrid_util.pxgrid:DEBUG:get_access_secret ~ise-pubsub-ise-3-2
2023-08-27 21:08:38,868:pxgrid_util.pxgrid:DEBUG:send_rest_request AccessSecret
2023-08-27 21:08:38,897:__main__:DEBUG:[default_publisher_loop] starting subscription to /topic/com.cisco.einarnn.special at wss://ise-3-2.hareshaw.net:8910/pxgrid/ise/pubsub
2023-08-27 21:08:38,897:__main__:DEBUG:[default_publish_loop] opening web socket and stomp
2023-08-27 21:08:38,897:__main__:DEBUG:[default_publish_loop] connect websocket
2023-08-27 21:08:38,897:pxgrid_util.ws_stomp:DEBUG:WebSocket Connect, ws_url=wss://ise-3-2.hareshaw.net:8910/pxgrid/ise/pubsub
2023-08-27 21:08:38,945:__main__:DEBUG:[default_publish_loop] connect STOMP node ~ise-pubsub-ise-3-2
2023-08-27 21:08:38,946:pxgrid_util.ws_stomp:DEBUG:STOMP CONNECT host=~ise-pubsub-ise-3-2
2023-08-27 21:08:38,946:pxgrid_util.stomp:DEBUG:write
2023-08-27 21:08:38,946:pxgrid_util.ws_stomp:DEBUG:stomp_connect completed
2023-08-27 21:08:39,947:pxgrid_util.ws_stomp:DEBUG:STOMP SEND topic=/topic/com.cisco.einarnn.special
2023-08-27 21:08:39,948:pxgrid_util.stomp:DEBUG:write
2023-08-27 21:08:39,949:pxgrid_util.ws_stomp:DEBUG:stomp_send completed
2023-08-27 21:08:39,949:__main__:DEBUG:[default_publish_loop] message published to node ~ise-pubsub-ise-3-2, topic /topic/com.cisco.einarnn.special
...
```


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

### anc-policy

#### Get the policies you have defined in your deployment

```
anc-policy \
    -a your.server.fqdn \
    -n NODENAME \
    -w NODESECRET \
    --insecure \
    --get-anc-policies
```

#### Get all endpoints with an ANC policy, including the applied policy

```
anc-policy \
    -a your.server.fqdn \
    -n NODENAME \
    -w NODESECRET \
    --insecure \
    --get-anc-endpoints
```

#### Get the policy applied to a specific endpoint, by MAC address

```
anc-policy \
    -a your.server.fqdn \
    -n NODENAME \
    -w NODESECRET \
    --insecure \
    --get-anc-policy-by-mac \
    --anc-mac-address 02:42:0A:14:04:23
```

#### Apply policy by MAC address

The MAC address specified does not need to be for an active session.

```
anc-policy \
    -a your.server.fqdn \
    -n NODENAME \
    -w NODESECRET \
    --insecure \
    --apply-anc-policy-by-mac \
    --anc-mac-address 02:42:0A:14:04:23 \
    --anc-policy YOUR_POLICY
```

#### Clear policy by MAC address

The MAC address specified does not need to be for an active session.

```
anc-policy \
    -a your.server.fqdn \
    -n NODENAME \
    -w NODESECRET \
    --insecure \
    --clear-anc-policy-by-mac \
    --anc-mac-address 02:42:0A:14:04:23
```

#### Apply policy by IP address

Note that ISE will map from the IP address to the MAC address of an **active** session for this command.

```
anc-policy \
    -a your.server.fqdn \
    -n NODENAME \
    -w NODESECRET \
    --insecure \
    --apply-anc-policy-by-ip  \
    --anc-ip-address 1.2.3.4 \
    --anc-policy YOUR_POLICY
```

#### Clear policy by IP address

Note that ISE will map from the IP address to the MAC address of an **active** session for this command.

```
anc-policy \
    -a your.server.fqdn \
    -n NODENAME \
    -w NODESECRET \
    --insecure \
    --clear-anc-policy-by-ip  \
    --anc-ip-address 1.2.3.4
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

