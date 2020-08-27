# GoHarbor

## Installation

1. Download from official site repository - https://github.com/goharbor/harbor/releases
2. Unpack
3. Run 'prepare'
4. Then 'install.sh'



## Problem with http and https it affects login to registry

With command below http transport  protocolcan be checked wheteher it in use.

`curl -X GET -I "https://my.registry.company.com/v2/"`

example below:

```
aa@ws01:~$ curl -X GET -I  "https://dockerhub.robolab.innopolis.university/v2/"
HTTP/1.1 401 Unauthorized
Content-Length: 87
Content-Type: application/json; charset=utf-8
Server: nginx Microsoft-HTTPAPI/2.0
Docker-Distribution-Api-Version: registry/2.0
Set-Cookie: _xsrf=WkQ0Tmg3dnN6NWNJMTFWYlRnMWVOZkFNWTlIMlF3UFM=|1589371336326078646|7d083411e882667b81c753fd90bc43bec79c84daa489d504895efa616c2be0c2; Expires=Wed, 13 May 2020 13:02:16 UTC; Max-Age=3600; Path=/
Set-Cookie: sid=4a9c7c159bc752fc8cab2b24c8a1497a; Path=/; HttpOnly
WWW-Authenticate: Bearer realm="http://dockerhub.robolab.innopolis.university/service/token",service="harbor-registry"
Date: Wed, 13 May 2020 12:02:15 GMT

```
From this command we see that it uses  realm="http://my.registry.company.com/v2//service/token". it was **http**, not **https**.

So edit **common/config/registry/config.yml**，and fixed it.
```
auth:
  token:
    issuer: harbor-token-issuer
    realm: https://my.registry.company.com/service/token  # http -> https
    rootcertbundle: /some/root.crt
    service: harbor-registry
```


Result 

```
aa@ws01:~$ curl -X GET -I  "https://dockerhub.robolab.innopolis.university/v2/"
HTTP/1.1 401 Unauthorized
Content-Length: 87
Content-Type: application/json; charset=utf-8
Server: nginx Microsoft-HTTPAPI/2.0
Docker-Distribution-Api-Version: registry/2.0
Set-Cookie: _xsrf=VTVjU3I0RzM2dmRzdlhMUFNzN3BSM2dKWGc1NXZTY0k=|1589371446677790653|30777e780bdc482b783812aecfcdd0fd5ec08ec5df2de13f0eb795d86abcad7a; Expires=Wed, 13 May 2020 13:04:06 UTC; Max-Age=3600; Path=/
Set-Cookie: sid=9df81e0f8b3f5264557a915548932cf8; Path=/; HttpOnly
WWW-Authenticate: Bearer realm="https://dockerhub.robolab.innopolis.university/service/token",service="harbor-registry"
Date: Wed, 13 May 2020 12:04:06 GMT

```

After that you are able to login

```
aa@ws01:~$ docker login dockerhub.robolab.innopolis.university -u a.kurbanniyazov -p Your_account token
WARNING! Using --password via the CLI is insecure. Use --password-stdin.
Login Succeeded

```


### Sources

1. https://goharbor.io/docs/1.10/administration/configure-authentication/oidc-auth/

2. https://github.com/goharbor/harbor/issues/8422

3. [GoHarbor behind proxy](https://github.com/goharbor/harbor/issues/6405)

4. [Installation GoHarbor](https://computingforgeeks.com/how-to-install-harbor-docker-image-registry-on-centos-debian-ubuntu/)



