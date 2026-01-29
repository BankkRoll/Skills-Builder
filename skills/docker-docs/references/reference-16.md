# Registry authentication and more

# Registry authentication

> Specifies the Docker Registry v2 authentication

# Registry authentication

   Table of contents

---

This document outlines the registry authentication scheme:

![v2 registry auth](https://docs.docker.com/reference/api/registry/images/v2-registry-auth.png)  ![v2 registry auth](https://docs.docker.com/reference/api/registry/images/v2-registry-auth.png)

1. Attempt to begin a push/pull operation with the registry.
2. If the registry requires authorization it will return a `401 Unauthorized`
  HTTP response with information on how to authenticate.
3. The registry client makes a request to the authorization service for a
  Bearer token.
4. The authorization service returns an opaque Bearer token representing the
  client's authorized access.
5. The client retries the original request with the Bearer token embedded in
  the request's Authorization header.
6. The Registry authorizes the client by validating the Bearer token and the
  claim set embedded within it and begins the push/pull session as usual.

## Requirements

- Registry clients which can understand and respond to token auth challenges
  returned by the resource server.
- An authorization server capable of managing access controls to their
  resources hosted by any given service (such as repositories in a Docker
  Registry).
- A Docker Registry capable of trusting the authorization server to sign tokens
  which clients can use for authorization and the ability to verify these
  tokens for single use or for use during a sufficiently short period of time.

## Authorization server endpoint descriptions

The described server is meant to serve as a standalone access control manager
for resources hosted by other services which want to authenticate and manage
authorizations using a separate access control manager.

A service like this is used by the official Docker Registry to authenticate
clients and verify their authorization to Docker image repositories.

As of Docker 1.6, the registry client within the Docker Engine has been updated
to handle such an authorization workflow.

## How to authenticate

Registry V1 clients first contact the index to initiate a push or pull. Under
the Registry V2 workflow, clients should contact the registry first. If the
registry server requires authentication it will return a `401 Unauthorized`
response with a `WWW-Authenticate` header detailing how to authenticate to this
registry.

For example, say I (username `jlhawn`) am attempting to push an image to the
repository `samalba/my-app`. For the registry to authorize this, I will need
`push` access to the `samalba/my-app` repository. The registry will first
return this response:

```text
HTTP/1.1 401 Unauthorized
Content-Type: application/json; charset=utf-8
Docker-Distribution-Api-Version: registry/2.0
Www-Authenticate: Bearer realm="https://auth.docker.io/token",service="registry.docker.io",scope="repository:samalba/my-app:pull,push"
Date: Thu, 10 Sep 2015 19:32:31 GMT
Content-Length: 235
Strict-Transport-Security: max-age=31536000

{"errors":[{"code":"UNAUTHORIZED","message":"access to the requested resource is not authorized","detail":[{"Type":"repository","Name":"samalba/my-app","Action":"pull"},{"Type":"repository","Name":"samalba/my-app","Action":"push"}]}]}
```

Note the HTTP Response Header indicating the auth challenge:

```text
Www-Authenticate: Bearer realm="https://auth.docker.io/token",service="registry.docker.io",scope="repository:samalba/my-app:pull,push"
```

This format is documented in [Section 3 of RFC 6750: The OAuth 2.0 Authorization Framework: Bearer Token Usage](https://tools.ietf.org/html/rfc6750#section-3)

This challenge indicates that the registry requires a token issued by the
specified token server and that the request the client is attempting will
need to include sufficient access entries in its claim set. To respond to this
challenge, the client will need to make a `GET` request to the URL
`https://auth.docker.io/token` using the `service` and `scope` values from the
`WWW-Authenticate` header.

## Requesting a token

Defines getting a bearer and refresh token using the token endpoint.

### Query parameters

#### service

The name of the service which hosts the resource.

#### offline_token

Whether to return a refresh token along with the bearer token. A refresh token
is capable of getting additional bearer tokens for the same subject with
different scopes. The refresh token does not have an expiration and should be
considered completely opaque to the client.

#### client_id

String identifying the client. This `client_id` does not need to be registered
with the authorization server but should be set to a meaningful value in order
to allow auditing keys created by unregistered clients. Accepted syntax is
defined in [RFC6749 Appendix
A.1](https://tools.ietf.org/html/rfc6749#appendix-A.1).

#### scope

The resource in question, formatted as one of the space-delimited entries from
the `scope` parameters from the `WWW-Authenticate` header shown previously. This
query parameter should be specified multiple times if there is more than one
`scope` entry from the `WWW-Authenticate` header. The previous example would be
specified as: `scope=repository:samalba/my-app:push`. The scope field may be
empty to request a refresh token without providing any resource permissions to
the returned bearer token.

### Token response fields

#### token

An opaque `Bearer` token that clients should supply to subsequent
requests in the `Authorization` header.

#### access_token

For compatibility with OAuth 2.0, the `token` under the name `access_token` is
also accepted. At least one of these fields must be specified, but both may
also appear (for compatibility with older clients). When both are specified,
they should be equivalent; if they differ the client's choice is undefined.

#### expires_in

(Optional) The duration in seconds since the token was issued that it will
remain valid. When omitted, this defaults to 60 seconds. For compatibility
with older clients, a token should never be returned with less than 60 seconds
to live.

#### issued_at

(Optional) The [RFC3339](https://www.ietf.org/rfc/rfc3339.txt)-serialized UTC
standard time at which a given token was issued. If `issued_at` is omitted, the
expiration is from when the token exchange completed.

#### refresh_token

(Optional) Token which can be used to get additional access tokens for
the same subject with different scopes. This token should be kept secure
by the client and only sent to the authorization server which issues
bearer tokens. This field will only be set when `offline_token=true` is
provided in the request.

### Example

For this example, the client makes an HTTP GET request to the following URL:

```text
https://auth.docker.io/token?service=registry.docker.io&scope=repository:samalba/my-app:pull,push
```

The token server should first attempt to authenticate the client using any
authentication credentials provided with the request. From Docker 1.11 the
Docker Engine supports both Basic Authentication and OAuth2 for
getting tokens. Docker 1.10 and before, the registry client in the Docker Engine
only supports Basic Authentication. If an attempt to authenticate to the token
server fails, the token server should return a `401 Unauthorized` response
indicating that the provided credentials are invalid.

Whether the token server requires authentication is up to the policy of that
access control provider. Some requests may require authentication to determine
access (such as pushing or pulling a private repository) while others may not
(such as pulling from a public repository).

After authenticating the client (which may simply be an anonymous client if
no attempt was made to authenticate), the token server must next query its
access control list to determine whether the client has the requested scope. In
this example request, if I have authenticated as user `jlhawn`, the token
server will determine what access I have to the repository `samalba/my-app`
hosted by the entity `registry.docker.io`.

Once the token server has determined what access the client has to the
resources requested in the `scope` parameter, it will take the intersection of
the set of requested actions on each resource and the set of actions that the
client has in fact been granted. If the client only has a subset of the
requested access **it must not be considered an error** as it is not the
responsibility of the token server to indicate authorization errors as part of
this workflow.

Continuing with the example request, the token server will find that the
client's set of granted access to the repository is `[pull, push]` which when
intersected with the requested access `[pull, push]` yields an equal set. If
the granted access set was found only to be `[pull]` then the intersected set
would only be `[pull]`. If the client has no access to the repository then the
intersected set would be empty, `[]`.

It is this intersected set of access which is placed in the returned token.

The server then constructs an implementation-specific token with this
intersected set of access, and returns it to the Docker client to use to
authenticate to the audience service (within the indicated window of time):

```text
HTTP/1.1 200 OK
Content-Type: application/json

{"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IlBZWU86VEVXVTpWN0pIOjI2SlY6QVFUWjpMSkMzOlNYVko6WEdIQTozNEYyOjJMQVE6WlJNSzpaN1E2In0.eyJpc3MiOiJhdXRoLmRvY2tlci5jb20iLCJzdWIiOiJqbGhhd24iLCJhdWQiOiJyZWdpc3RyeS5kb2NrZXIuY29tIiwiZXhwIjoxNDE1Mzg3MzE1LCJuYmYiOjE0MTUzODcwMTUsImlhdCI6MTQxNTM4NzAxNSwianRpIjoidFlKQ08xYzZjbnl5N2tBbjBjN3JLUGdiVjFIMWJGd3MiLCJhY2Nlc3MiOlt7InR5cGUiOiJyZXBvc2l0b3J5IiwibmFtZSI6InNhbWFsYmEvbXktYXBwIiwiYWN0aW9ucyI6WyJwdXNoIl19XX0.QhflHPfbd6eVF4lM9bwYpFZIV0PfikbyXuLx959ykRTBpe3CYnzs6YBK8FToVb5R47920PVLrh8zuLzdCr9t3w", "expires_in": 3600,"issued_at": "2009-11-10T23:00:00Z"}
```

## Using the Bearer token

Once the client has a token, it will try the registry request again with the
token placed in the HTTP `Authorization` header like so:

```text
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IkJWM0Q6MkFWWjpVQjVaOktJQVA6SU5QTDo1RU42Ok40SjQ6Nk1XTzpEUktFOkJWUUs6M0ZKTDpQT1RMIn0.eyJpc3MiOiJhdXRoLmRvY2tlci5jb20iLCJzdWIiOiJCQ0NZOk9VNlo6UUVKNTpXTjJDOjJBVkM6WTdZRDpBM0xZOjQ1VVc6NE9HRDpLQUxMOkNOSjU6NUlVTCIsImF1ZCI6InJlZ2lzdHJ5LmRvY2tlci5jb20iLCJleHAiOjE0MTUzODczMTUsIm5iZiI6MTQxNTM4NzAxNSwiaWF0IjoxNDE1Mzg3MDE1LCJqdGkiOiJ0WUpDTzFjNmNueXk3a0FuMGM3cktQZ2JWMUgxYkZ3cyIsInNjb3BlIjoiamxoYXduOnJlcG9zaXRvcnk6c2FtYWxiYS9teS1hcHA6cHVzaCxwdWxsIGpsaGF3bjpuYW1lc3BhY2U6c2FtYWxiYTpwdWxsIn0.Y3zZSwaZPqy4y9oRBVRImZyv3m_S9XDHF1tWwN7mL52C_IiA73SJkWVNsvNqpJIn5h7A2F8biv_S2ppQ1lgkbw
```

This is also described in [Section 2.1 of RFC 6750: The OAuth 2.0 Authorization Framework: Bearer Token Usage](https://tools.ietf.org/html/rfc6750#section-2.1)

---

# Supported registry API for Docker Hub

> Supported registry API endpoints.

- General
  - Overview
  - Authentication
  - Pulling Images
  - Pushing Images
  - Deleting Images
- API
  - Manifests
    - getGet image manifest
    - putPut image manifest
    - headCheck if manifest exists
    - delDelete image manifest
  - Blobs
    - postInitiate blob upload or attempt cross-repository blob mount
    - headCheck existence of blob
    - getRetrieve blob
    - getGet blob upload status
    - putComplete blob upload
    - patchUpload blob chunk
    - delCancel blob upload

[API docs by Redocly](https://redocly.com/redoc/)

# Supported registry API for Docker Hub

Download OpenAPI specification:[Download](https://docs.docker.com/reference/api/registry/latest.yaml)

Docker Hub is an OCI-compliant registry, which means it adheres to the open
standards defined by the Open Container Initiative (OCI) for distributing
container images. This ensures compatibility with a wide range of tools and
platforms in the container ecosystem.

This reference documents the Docker Hub-supported subset of the Registry HTTP API V2.
It focuses on pulling, pushing, and deleting images. It does not cover the full OCI Distribution Specification.

For the complete OCI specification, see [OCI Distribution Specification](https://github.com/opencontainers/distribution-spec).

## Overview

All endpoints in this API are prefixed by the version and repository name, for example:

```
/v2/<name>/
```

This format provides structured access control and URI-based scoping of image operations.

For example, to interact with the `library/ubuntu` repository, use:

```
/v2/library/ubuntu/
```

Repository names must meet these requirements:

1. Consist of path components matching `[a-z0-9]+(?:[._-][a-z0-9]+)*`
2. If more than one component, they must be separated by `/`
3. Full repository name must be fewer than 256 characters

## Authentication

Specifies registry authentication.

 [Detailed authentication workflow and token usage](https://docs.docker.com/reference/api/registry/auth/)

## Pulling Images

Pulling an image involves retrieving the manifest and downloading each of the image's layer blobs. This section outlines the general steps followed by a working example.

1. [Get a bearer token for the repository](https://docs.docker.com/reference/api/registry/auth/).
2. [Get the image manifest](#operation/GetImageManifest).
3. If the response in the previous step is a multi-architecture manifest list, you must do the following:
  - Parse the `manifests[]` array to locate the digest for your target platform (e.g., `linux/amd64`).
  - [Get the image manifest](#operation/GetImageManifest) using the located digest.
4. [Check if the blob exists](#operation/CheckBlobExists) before downloading. The client should send a `HEAD` request for each layer digest.
5. [Download each layer blob](#operation/GetBlob) using the digest obtained from the manifest. The client should send a `GET` request for each layer digest.

The following bash script example pulls `library/ubuntu:latest` from Docker Hub.

```bash
#!/bin/bash

# Step 1: Get a bearer token
TOKEN=$(curl -s "https://auth.docker.io/token?service=registry.docker.io&scope=repository:library/ubuntu:pull" | jq -r .token)

# Step 2: Get the image manifest. In this example, an image manifest list is returned.
curl -s -H "Authorization: Bearer $TOKEN" \
     -H "Accept: application/vnd.docker.distribution.manifest.list.v2+json" \
     https://registry-1.docker.io/v2/library/ubuntu/manifests/latest \
     -o manifest-list.json

# Step 3a: Parse the `manifests[]` array to locate the digest for your target platform (e.g., `linux/amd64`).
IMAGE_MANIFEST_DIGEST=$(jq -r '.manifests[] | select(.platform.architecture == "amd64" and .platform.os == "linux") | .digest' manifest-list.json)

# Step 3b: Get the platform-specific image manifest
curl -s -H "Authorization: Bearer $TOKEN" \
     -H "Accept: application/vnd.docker.distribution.manifest.v2+json" \
     https://registry-1.docker.io/v2/library/ubuntu/manifests/$IMAGE_MANIFEST_DIGEST \
     -o manifest.json

# Step 4: Send a HEAD request to check if the layer blob exists
DIGEST=$(jq -r '.layers[0].digest' manifest.json)
curl -I -H "Authorization: Bearer $TOKEN" \
     https://registry-1.docker.io/v2/library/ubuntu/blobs/$DIGEST

# Step 5: Download the layer blob
curl -L -H "Authorization: Bearer $TOKEN" \
     https://registry-1.docker.io/v2/library/ubuntu/blobs/$DIGEST
```

This example pulls the manifest and the first layer for the `ubuntu:latest` image on the `linux/amd64` platform. Repeat steps 4 and 5 for each digest in the `.layers[]` array in the manifest.

## Pushing Images

Pushing an image involves uploading any image blobs (such as the config or layers), and then uploading the manifest that references those blobs.

This section outlines the basic steps to push an image using the registry API.

1. [Get a bearer token for the repository](https://docs.docker.com/reference/api/registry/auth/)
2. [Check if the blob exists](#operation/CheckBlobExists) using a `HEAD` request for each blob digest.
3. If the blob does not exist, [upload the blob](#operation/CompleteBlobUpload) using a monolithic `PUT` request:
  - First, [initiate the upload](#operation/InitiateBlobUpload) with `POST`.
  - Then [upload and complete](#operation/CompleteBlobUpload) with `PUT`.
  **Note**:  Alternatively, you can upload the blob in multiple chunks by using `PATCH` requests to send each chunk, followed by a final `PUT` request to complete the upload. This is known as a [chunked upload](#operation/UploadBlobChunk) and is useful for large blobs or when resuming interrupted uploads.
4. [Upload the image manifest](#operation/PutImageManifest) using a `PUT` request to associate the config and layers.

The following bash script example pushes a dummy config blob and manifest to `yourusername/helloworld:latest` on Docker Hub. You can replace `yourusername` with your Docker Hub username and `dckr_pat` with your Docker Hub personal access token.

```bash
#!/bin/bash

USERNAME=yourusername
PASSWORD=dckr_pat
REPO=yourusername/helloworld
TAG=latest
CONFIG=config.json
MIME_TYPE=application/vnd.docker.container.image.v1+json

# Step 1: Get a bearer token
TOKEN=$(curl -s -u "$USERNAME:$PASSWORD" \
"https://auth.docker.io/token?service=registry.docker.io&scope=repository:$REPO:push,pull" \
| jq -r .token)

# Create a dummy config blob and compute its digest
echo '{"architecture":"amd64","os":"linux","config":{},"rootfs":{"type":"layers","diff_ids":[]}}' > $CONFIG
DIGEST="sha256:$(sha256sum $CONFIG | awk '{print $1}')"

# Step 2: Check if the blob exists
STATUS=$(curl -s -o /dev/null -w "%{http_code}" -I \
  -H "Authorization: Bearer $TOKEN" \
  https://registry-1.docker.io/v2/$REPO/blobs/$DIGEST)

if [ "$STATUS" != "200" ]; then
  # Step 3: Upload blob using monolithic upload
  LOCATION=$(curl -sI -X POST \
    -H "Authorization: Bearer $TOKEN" \
    https://registry-1.docker.io/v2/$REPO/blobs/uploads/ \
    | grep -i Location | tr -d '\r' | awk '{print $2}')

  curl -s -X PUT "$LOCATION&digest=$DIGEST" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/octet-stream" \
    --data-binary @$CONFIG
fi

# Step 4: Upload the manifest that references the config blob
MANIFEST=$(cat <<EOF
{
  "schemaVersion": 2,
  "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
  "config": {
    "mediaType": "$MIME_TYPE",
    "size": $(stat -c%s $CONFIG),
    "digest": "$DIGEST"
  },
  "layers": []
}
EOF
)

curl -s -X PUT \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/vnd.docker.distribution.manifest.v2+json" \
  -d "$MANIFEST" \
  https://registry-1.docker.io/v2/$REPO/manifests/$TAG

echo "Pushed image to $REPO:$TAG"
```

This example pushes a minimal image with no layers. To push a complete image, repeat steps 2–3 for each layer and include the layer digests in the `layers[]` field of the manifest.

## Deleting Images

Deleting an image involves removing its manifest by digest. You must first retrieve the manifest digest, then issue a `DELETE` request using that digest.

Only untagged manifests (or those not referenced by other tags or images) can be deleted. If a manifest is still referenced, the registry returns `403 Forbidden`.

This section outlines the basic steps to delete an image using the registry API.

1. [Get a bearer token for the repository](https://docs.docker.com/reference/api/registry/auth/).
2. [Get the manifest](#operation/GetImageManifest) using the image's tag.
3. Retrieve the `Docker-Content-Digest` header from the manifest response. This digest uniquely identifies the manifest.
4. [Delete the manifest](#operation/DeleteImageManifest) using a `DELETE` request and the digest.

The following bash script example deletes the `latest` tag from `yourusername/helloworld` on Docker Hub. Replace `yourusername` with your Docker Hub username and `dckr_pat` with your Docker Hub personal access token.

```bash
#!/bin/bash

USERNAME=yourusername
PASSWORD=dckr_pat
REPO=yourusername/helloworld
TAG=latest

# Step 1: Get a bearer token
TOKEN=$(curl -s -u "$USERNAME:$PASSWORD" \
  "https://auth.docker.io/token?service=registry.docker.io&scope=repository:$REPO:pull,push,delete" \
  | jq -r .token)

# Step 2 and 3: Get the manifest and extract the digest from response headers
DIGEST=$(curl -sI -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/vnd.docker.distribution.manifest.v2+json" \
  https://registry-1.docker.io/v2/$REPO/manifests/$TAG \
  | grep -i Docker-Content-Digest | tr -d '\r' | awk '{print $2}')

echo "Deleting manifest with digest: $DIGEST"

# Step 4: Delete the manifest by digest
curl -s -X DELETE \
  -H "Authorization: Bearer $TOKEN" \
  https://registry-1.docker.io/v2/$REPO/manifests/$DIGEST

echo "Deleted image: $REPO@$DIGEST"
```

This example deletes the manifest for the `latest` tag. To fully delete all references to an image, ensure no other tags or referrers point to the same manifest digest.

## Manifests

Image manifests are JSON documents that describe an image: its configuration blob, the digests of each layer blob, and metadata such as media‑types and annotations.

## Get image manifest

Fetch the manifest identified by `name` and `reference`, where `reference` can be a tag (e.g., `latest`) or a digest (e.g., `sha256:...`).

The manifest contains metadata about the image, including configuration and layer digests. It is required for pulling images from the registry.

This endpoint requires authentication. Use the `Authorization: Bearer <token>` header.

##### path Parameters

| namerequired | stringExample:library/ubuntuName of the target repository |
| --- | --- |
| referencerequired | stringExamples:latest- Tagsha256:abc123def456...- DigestTag or digest of the target manifest |

##### header Parameters

| Authorizationrequired | stringRFC7235-compliant authorization header (e.g.,Bearer <token>). |
| --- | --- |
| Accept | stringMedia type(s) the client supports for the manifest.The registry supports the following media types:application/vnd.docker.distribution.manifest.v2+jsonapplication/vnd.docker.distribution.manifest.list.v2+jsonapplication/vnd.oci.image.manifest.v1+jsonapplication/vnd.oci.image.index.v1+json |

### Responses

### Request samples

- cURL

```
# GET a manifest (by tag or digest)
curl -H "Authorization: Bearer $TOKEN" \
     -H "Accept: application/vnd.docker.distribution.manifest.v2+json" \
     https://registry-1.docker.io/v2/library/ubuntu/manifests/latest
```

### Response samples

- 200

Content typeapplication/vnd.docker.distribution.manifest.v2+json`{"schemaVersion": 2,"mediaType": "application/vnd.docker.distribution.manifest.v2+json","config": {"mediaType": "application/vnd.docker.container.image.v1+json","size": 7023,"digest": "sha256:123456abcdef..."},"layers": [{"mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip","size": 32654,"digest": "sha256:abcdef123456..."},{"mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip","size": 16724,"digest": "sha256:7890abcdef12..."}]}`

## Put image manifest

Upload an image manifest for a given tag or digest. This operation registers a manifest in a repository, allowing it to be pulled using the specified reference.

This endpoint is typically used after all layer and config blobs have been uploaded to the registry.

The manifest must conform to the expected schema and media type. For Docker image manifest schema version 2, use:
`application/vnd.docker.distribution.manifest.v2+json`

Requires authentication via a bearer token with `push` scope for the target repository.

##### path Parameters

| namerequired | stringExample:library/ubuntuName of the target Repository |
| --- | --- |
| referencerequired | stringExamples:latest- Tagsha256:abc123def456...- DigestTag or digest to associate with the uploaded Manifest |

##### header Parameters

| Authorizationrequired | stringRFC7235-compliant authorization header (e.g.,Bearer <token>). |
| --- | --- |
| Content-Typerequired | stringExample:application/vnd.docker.distribution.manifest.v2+jsonMedia type of the manifest being uploaded. |

##### Request Body schema:application/vnd.docker.distribution.manifest.v2+jsonrequired

| schemaVersionrequired | integer |
| --- | --- |
| mediaTyperequired | string |
| required | object |
| required | Array ofobjects |

### Responses

### Request samples

- Payload
- cURL

Content typeapplication/vnd.docker.distribution.manifest.v2+json`{"schemaVersion": 2,"mediaType": "application/vnd.docker.distribution.manifest.v2+json","config": {"mediaType": "application/vnd.docker.container.image.v1+json","size": 7023,"digest": "sha256:123456abcdef..."},"layers": [{"mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip","size": 32654,"digest": "sha256:abcdef123456..."}]}`

## Check if manifest exists

Use this endpoint to verify whether a manifest exists by tag or digest.

This is a lightweight operation that returns only headers (no body). It is useful for:

- Checking for the existence of a specific image version
- Determining the digest or size of a manifest before downloading or deleting

This endpoint requires authentication with pull scope.

##### path Parameters

| namerequired | stringExample:library/ubuntuName of the Repository |
| --- | --- |
| referencerequired | stringExamples:latest- Tagsha256:abc123def456...- DigestTag or digest to check |

##### header Parameters

| Authorizationrequired | stringBearer token for authentication |
| --- | --- |
| Accept | stringExample:application/vnd.docker.distribution.manifest.v2+jsonMedia type of the manifest to check. The response will match one of the accepted types. |

### Responses

### Request samples

- cURL

```
# HEAD /v2/{name}/manifests/{reference}
curl -I \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/vnd.docker.distribution.manifest.v2+json" \
  https://registry-1.docker.io/v2/library/ubuntu/manifests/latest
```

## Delete image manifest

Delete an image manifest from a repository by digest.

Only untagged or unreferenced manifests can be deleted. If the manifest is still referenced by a tag or another image, the registry will return `403 Forbidden`.

This operation requires `delete` access to the repository.

##### path Parameters

| namerequired | stringExample:yourusername/helloworldName of the repository |
| --- | --- |
| referencerequired | stringExample:sha256:abc123def456...Digest of the manifest to delete (e.g.,sha256:...) |

##### header Parameters

| Authorizationrequired | stringBearer token withdeleteaccess |
| --- | --- |

### Responses

### Request samples

- cURL

```
# DELETE a manifest by digest
curl -X DELETE \
  -H "Authorization: Bearer $TOKEN" \
  https://registry-1.docker.io/v2/yourusername/helloworld/manifests/sha256:abc123def456...
```

## Blobs

Blobs are the binary objects referenced from manifests:
the config JSON and one or more compressed layer tarballs.

## Initiate blob upload or attempt cross-repository blob mount

Initiate an upload session for a blob (layer or config) in a repository.

This is the first step in uploading a blob. It returns a `Location` URL where the blob can be uploaded using `PATCH` (chunked) or `PUT` (monolithic).

Instead of uploading a blob, a client may attempt to mount a blob from another repository (if it has read access) by including the `mount` and `from` query parameters.

If successful, the registry responds with `201 Created` and the blob is reused without re-upload.

If the mount fails, the upload proceeds as usual and returns a `202 Accepted`.

You must authenticate with `push` access to the target repository.

##### path Parameters

| namerequired | stringExample:library/ubuntuName of the target repository |
| --- | --- |

##### query Parameters

| mount | stringExample:mount=sha256:abc123def456...Digest of the blob to mount from another repository |
| --- | --- |
| from | stringExample:from=library/busyboxSource repository to mount the blob from |

##### header Parameters

| Authorizationrequired | stringBearer token for authentication withpushscope |
| --- | --- |

### Responses

### Request samples

- cURL (Initiate Standard Upload)
- cURL (Cross-Repository Blob Mount)

```
# Initiate a standard blob upload session
curl -i -X POST \
  -H "Authorization: Bearer $TOKEN" \
  https://registry-1.docker.io/v2/library/ubuntu/blobs/uploads/
```

## Check existence of blob

Check whether a blob (layer or config) exists in the registry.

This is useful before uploading a blob to avoid duplicates.

If the blob is present, the registry returns a `200 OK` response with headers like `Content-Length` and `Docker-Content-Digest`.

If the blob does not exist, the response will be `404 Not Found`.

##### path Parameters

| namerequired | stringExample:library/ubuntuName of the Repository |
| --- | --- |
| digestrequired | stringExample:sha256:abc123def4567890...Digest of the blob |

##### header Parameters

| Authorizationrequired | stringExample:Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6...Bearer token with pull or push scope |
| --- | --- |

### Responses

### Request samples

- cURL

```
# HEAD to check if a blob exists
curl -I \
  -H "Authorization: Bearer $TOKEN" \
  https://registry-1.docker.io/v2/library/ubuntu/blobs/sha256:abc123...
```

### Response samples

- 200

Content typeapplication/jsonExampleSample requestSample 200 response headersSample request`{"method": "HEAD","url": "/v2/library/ubuntu/blobs/sha256:abc123def4567890...","headers": {"Authorization": "Bearer <token>","Accept": "*/*"}}`

## Retrieve blob

Download the blob identified by digest from the registry.

Blobs include image layers and configuration objects. Clients must use the digest from the manifest to retrieve a blob.

This endpoint may return a `307 Temporary Redirect` to a CDN or storage location. Clients must follow the redirect to obtain the actual blob content.

The blob content is typically a gzipped tarball (for layers) or JSON (for configs). The MIME type is usually `application/octet-stream`.

##### path Parameters

| namerequired | stringExample:library/ubuntuRepository Name |
| --- | --- |
| digestrequired | stringExample:sha256:abc123def456...Digest of the Blob |

##### header Parameters

| Authorizationrequired | stringExample:Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6...Bearer token with pull scope |
| --- | --- |

### Responses

### Request samples

- cURL

```
# GET (download) a blob
curl -L \
  -H "Authorization: Bearer $TOKEN" \
  https://registry-1.docker.io/v2/library/ubuntu/blobs/sha256:abc123... \
  -o layer.tar.gz
```

### Response samples

- 200

Content typeapplication/octet-stream

```
<binary data not shown>
```

## Get blob upload status

Retrieve the current status of an in-progress blob upload.

This is useful for:

- Resuming an interrupted upload
- Determining how many bytes have been accepted so far
- Retrying from the correct offset in chunked uploads

The response includes the `Range` header indicating the byte range received so far, and a `Docker-Upload-UUID` for identifying the session.

##### path Parameters

| namerequired | stringExample:library/ubuntuRepository Name |
| --- | --- |
| uuidrequired | stringExample:abc123Upload session UUID |

##### header Parameters

| Authorizationrequired | stringExample:Bearer eyJhbGciOi... |
| --- | --- |

### Responses

### Request samples

- cURL

```
# GET upload status
curl -I \
  -H "Authorization: Bearer $TOKEN" \
  https://registry-1.docker.io/v2/library/ubuntu/blobs/uploads/abc123
```

## Complete blob upload

Complete the upload of a blob by finalizing an upload session.

This request must include the `digest` query parameter and optionally the last chunk of data. When the registry receives this request, it verifies the digest and stores the blob.

This endpoint supports:

- Monolithic uploads (upload entire blob in this request)
- Finalizing chunked uploads (last chunk plus `digest`)

##### path Parameters

| namerequired | stringExample:library/ubuntuRepository name |
| --- | --- |
| uuidrequired | stringExample:abc123Upload session UUID returned from the POST request |

##### query Parameters

| digestrequired | stringExample:digest=sha256:abcd1234...Digest of the uploaded blob |
| --- | --- |

##### header Parameters

| Authorizationrequired | stringExample:Bearer eyJhbGciOi... |
| --- | --- |

##### Request Body schema:application/octet-streamoptional

string <binary>

### Responses

### Request samples

- Payload
- cURL

Content typeapplication/octet-stream

```
<binary data not shown>
```

## Upload blob chunk

Upload a chunk of a blob to an active upload session.

Use this method for **chunked uploads**, especially for large blobs or when resuming interrupted uploads.

The client sends binary data using `PATCH`, optionally including a `Content-Range` header.

After each chunk is accepted, the registry returns a `202 Accepted` response with:

- `Range`: current byte range stored
- `Docker-Upload-UUID`: identifier for the upload session
- `Location`: URL to continue the upload or finalize with `PUT`

##### path Parameters

| namerequired | stringExample:library/ubuntuRepository name |
| --- | --- |
| uuidrequired | stringExample:abc123Upload session UUID |

##### header Parameters

| Authorizationrequired | stringExample:Bearer eyJhbGciOi... |
| --- | --- |
| Content-Range | stringExample:bytes 0-65535Optional. Byte range of the chunk being sent |

##### Request Body schema:application/octet-streamrequired

string <binary>

### Responses

### Request samples

- Payload
- cURL

Content typeapplication/octet-stream

```
<binary data not shown>
```

## Cancel blob upload

Cancel an in-progress blob upload session.

This operation discards any data that has been uploaded and invalidates the upload session.

Use this when:

- An upload fails or is aborted mid-process
- The client wants to clean up unused upload sessions

After cancellation, the UUID is no longer valid and a new `POST` must be issued to restart the upload.

##### path Parameters

| namerequired | stringExample:library/ubuntuName of the repository |
| --- | --- |
| uuidrequired | stringExample:abc123Upload session UUID |

##### header Parameters

| Authorizationrequired | stringExample:Bearer eyJhbGciOi... |
| --- | --- |

### Responses

### Request samples

- cURL

```
# DELETE – cancel an upload session
curl -X DELETE \
  -H "Authorization: Bearer $TOKEN" \
  https://registry-1.docker.io/v2/library/ubuntu/blobs/uploads/abc123`
```

---

# ConsistentInstructionCasing

> All commands within the Dockerfile should use the same casing (either upper or lower)

# ConsistentInstructionCasing

   Table of contents

---

## Output

```text
Command 'EntryPoint' should be consistently cased
```

## Description

Instruction keywords should use consistent casing (all lowercase or all
uppercase). Using a case that mixes uppercase and lowercase, such as
`PascalCase` or `snakeCase`, letters result in poor readability.

## Examples

❌ Bad: don't mix uppercase and lowercase.

```dockerfile
From alpine
Run echo hello > /greeting.txt
EntRYpOiNT ["cat", "/greeting.txt"]
```

✅ Good: all uppercase.

```dockerfile
FROM alpine
RUN echo hello > /greeting.txt
ENTRYPOINT ["cat", "/greeting.txt"]
```

✅ Good: all lowercase.

```dockerfile
from alpine
run echo hello > /greeting.txt
entrypoint ["cat", "/greeting.txt"]
```

---

# CopyIgnoredFile

> Attempting to Copy file that is excluded by .dockerignore

# CopyIgnoredFile

   Table of contents

---

## Output

```text
Attempting to Copy file "./tmp/Dockerfile" that is excluded by .dockerignore
```

## Description

When you use the Add or Copy instructions from within a Dockerfile, you should
ensure that the files to be copied into the image do not match a pattern
present in `.dockerignore`.

Files which match the patterns in a `.dockerignore` file are not present in the
context of the image when it is built. Trying to copy or add a file which is
missing from the context will result in a build error.

## Examples

With the given `.dockerignore` file:

```text
*/tmp/*
```

❌ Bad: Attempting to Copy file "./tmp/Dockerfile" that is excluded by .dockerignore

```dockerfile
FROM scratch
COPY ./tmp/helloworld.txt /helloworld.txt
```

✅ Good: Copying a file which is not excluded by .dockerignore

```dockerfile
FROM scratch
COPY ./forever/helloworld.txt /helloworld.txt
```

---

# DuplicateStageName

> Stage names should be unique

# DuplicateStageName

   Table of contents

---

## Output

```text
Duplicate stage name 'foo-base', stage names should be unique
```

## Description

Defining multiple stages with the same name results in an error because the
builder is unable to uniquely resolve the stage name reference.

## Examples

❌ Bad: `builder` is declared as a stage name twice.

```dockerfile
FROM debian:latest AS builder
RUN apt-get update; apt-get install -y curl

FROM golang:latest AS builder
```

✅ Good: stages have unique names.

```dockerfile
FROM debian:latest AS deb-builder
RUN apt-get update; apt-get install -y curl

FROM golang:latest AS go-builder
```

---

# ExposeInvalidFormat

> IP address and host-port mapping should not be used in EXPOSE instruction. This will become an error in a future release

# ExposeInvalidFormat

   Table of contents

---

## Output

```text
EXPOSE instruction should not define an IP address or host-port mapping, found '127.0.0.1:80:80'
```

## Description

The [EXPOSE](https://docs.docker.com/reference/dockerfile/#expose) instruction
in a Dockerfile is used to indicate which ports the container listens on at
runtime. It should not include an IP address or host-port mapping, as this is
not the intended use of the `EXPOSE` instruction. Instead, it should only
specify the port number and optionally the protocol (TCP or UDP).

> Important
>
> This will become an error in a future release.

## Examples

❌ Bad: IP address and host-port mapping used.

```dockerfile
FROM alpine
EXPOSE 127.0.0.1:80:80
```

✅ Good: only the port number is specified.

```dockerfile
FROM alpine
EXPOSE 80
```

❌ Bad: Host-port mapping used.

```dockerfile
FROM alpine
EXPOSE 80:80
```

✅ Good: only the port number is specified.

```dockerfile
FROM alpine
EXPOSE 80
```

---

# ExposeProtoCasing

> Protocol in EXPOSE instruction should be lowercase

# ExposeProtoCasing

   Table of contents

---

## Output

```text
Defined protocol '80/TcP' in EXPOSE instruction should be lowercase
```

## Description

Protocol names in the [EXPOSE](https://docs.docker.com/reference/dockerfile/#expose)
instruction should be specified in lowercase to maintain consistency and
readability. This rule checks for protocols that are not in lowercase and
reports them.

## Examples

❌ Bad: protocol is not in lowercase.

```dockerfile
FROM alpine
EXPOSE 80/TcP
```

✅ Good: protocol is in lowercase.

```dockerfile
FROM alpine
EXPOSE 80/tcp
```

---

# FromAsCasing

> The 'as' keyword should match the case of the 'from' keyword

# FromAsCasing

   Table of contents

---

## Output

```text
'as' and 'FROM' keywords' casing do not match
```

## Description

While Dockerfile keywords can be either uppercase or lowercase, mixing case
styles is not recommended for readability. This rule reports violations where
mixed case style occurs for a `FROM` instruction with an `AS` keyword declaring
a stage name.

## Examples

❌ Bad: `FROM` is uppercase, `AS` is lowercase.

```dockerfile
FROM debian:latest as builder
```

✅ Good: `FROM` and `AS` are both uppercase

```dockerfile
FROM debian:latest AS deb-builder
```

✅ Good: `FROM` and `AS` are both lowercase.

```dockerfile
from debian:latest as deb-builder
```

## Related errors

- [FileConsistentCommandCasing](https://docs.docker.com/reference/build-checks/consistent-instruction-casing/)

---

# FromPlatformFlagConstDisallowed

> FROM --platform flag should not use a constant value

# FromPlatformFlagConstDisallowed

   Table of contents

---

## Output

```text
FROM --platform flag should not use constant value "linux/amd64"
```

## Description

Specifying `--platform` in the Dockerfile `FROM` instruction forces the image to build on only one target platform. This prevents building a multi-platform image from this Dockerfile and you must build on the same platform as specified in `--platform`.

The recommended approach is to:

- Omit `FROM --platform` in the Dockerfile and use the `--platform` argument on the command line.
- Use `$BUILDPLATFORM` or some other combination of variables for the `--platform` argument.
- Stage name should include the platform, OS, or architecture name to indicate that it only contains platform-specific instructions.

## Examples

❌ Bad: using a constant argument for `--platform`

```dockerfile
FROM --platform=linux/amd64 alpine AS base
RUN apk add --no-cache git
```

✅ Good: using the default platform

```dockerfile
FROM alpine AS base
RUN apk add --no-cache git
```

✅ Good: using a meta variable

```dockerfile
FROM --platform=${BUILDPLATFORM} alpine AS base
RUN apk add --no-cache git
```

✅ Good: used in a multi-stage build with a target architecture

```dockerfile
FROM --platform=linux/amd64 alpine AS build_amd64
...

FROM --platform=linux/arm64 alpine AS build_arm64
...

FROM build_${TARGETARCH} AS build
...
```

---

# InvalidDefaultArgInFrom

> Default value for global ARG results in an empty or invalid base image name

# InvalidDefaultArgInFrom

   Table of contents

---

## Output

```text
Using the global ARGs with default values should produce a valid build.
```

## Description

An `ARG` used in an image reference should be valid when no build arguments are used. An image build should not require `--build-arg` to be used to produce a valid build.

## Examples

❌ Bad: don't rely on an ARG being set for an image reference to be valid

```dockerfile
ARG TAG
FROM busybox:${TAG}
```

✅ Good: include a default for the ARG

```dockerfile
ARG TAG=latest
FROM busybox:${TAG}
```

✅ Good: ARG can be empty if the image would be valid with it empty

```dockerfile
ARG VARIANT
FROM busybox:stable${VARIANT}
```

✅ Good: Use a default value if the build arg is not present

```dockerfile
ARG TAG
FROM alpine:${TAG:-3.14}
```

---

# InvalidDefinitionDescription

> Comment for build stage or argument should follow the format: `# <arg/stage name> <description>`. If this is not intended to be a description comment, add an empty line or comment between the instruction and the comment.

# InvalidDefinitionDescription

   Table of contents

---

> Note
>
> This check is experimental and is not enabled by default. To enable it, see
> [Experimental checks](https://docs.docker.com/go/build-checks-experimental/).

## Output

```text
Comment for build stage or argument should follow the format: `# <arg/stage name> <description>`. If this is not intended to be a description comment, add an empty line or comment between the instruction and the comment.
```

## Description

The [--call=outline](https://docs.docker.com/reference/cli/docker/buildx/build/#call-outline)
and [--call=targets](https://docs.docker.com/reference/cli/docker/buildx/build/#call-outline)
flags for the `docker build` command print descriptions for build targets and arguments.
The descriptions are generated from [Dockerfile comments](https://docs.docker.com/reference/cli/docker/buildx/build/#descriptions)
that immediately precede the `FROM` or `ARG` instruction
and that begin with the name of the build stage or argument.
For example:

```dockerfile
# build-cli builds the CLI binary
FROM alpine AS build-cli
# VERSION controls the version of the program
ARG VERSION=1
```

In cases where preceding comments are not meant to be descriptions,
add an empty line or comment between the instruction and the preceding comment.

## Examples

❌ Bad: A non-descriptive comment on the line preceding the `FROM` command.

```dockerfile
# a non-descriptive comment
FROM scratch AS base

# another non-descriptive comment
ARG VERSION=1
```

✅ Good: An empty line separating non-descriptive comments.

```dockerfile
# a non-descriptive comment

FROM scratch AS base

# another non-descriptive comment

ARG VERSION=1
```

✅ Good: Comments describing `ARG` keys and stages immediately proceeding the command.

```dockerfile
# base is a stage for compiling source
FROM scratch AS base
# VERSION This is the version number.
ARG VERSION=1
```

---

# JSONArgsRecommended

> JSON arguments recommended for ENTRYPOINT/CMD to prevent unintended behavior related to OS signals

# JSONArgsRecommended

   Table of contents

---

## Output

```text
JSON arguments recommended for ENTRYPOINT/CMD to prevent unintended behavior related to OS signals
```

## Description

`ENTRYPOINT` and `CMD` instructions both support two different syntaxes for
arguments:

- Shell form: `CMD my-cmd start`
- Exec form: `CMD ["my-cmd", "start"]`

When you use shell form, the executable runs as a child process to a shell,
which doesn't pass signals. This means that the program running in the
container can't detect OS signals like `SIGTERM` and `SIGKILL` and respond to
them correctly.

## Examples

❌ Bad: the `ENTRYPOINT` command doesn't receive OS signals.

```dockerfile
FROM alpine
ENTRYPOINT my-program start
# entrypoint becomes: /bin/sh -c my-program start
```

To make sure the executable can receive OS signals, use the exec form for `CMD`
and `ENTRYPOINT`, which lets you run the executable as the main process (`PID 1`) in the container, avoiding a shell parent process.

✅ Good: the `ENTRYPOINT` receives OS signals.

```dockerfile
FROM alpine
ENTRYPOINT ["my-program", "start"]
# entrypoint becomes: my-program start
```

Note that running programs as PID 1 means the program now has the special
responsibilities and behaviors associated with PID 1 in Linux, such as reaping
child processes.

### Workarounds

There might still be cases when you want to run your containers under a shell.
When using exec form, shell features such as variable expansion, piping (`|`)
and command chaining (`&&`, `||`, `;`), are not available. To use such
features, you need to use shell form.

Here are some ways you can achieve that. Note that this still means that
executables run as child-processes of a shell.

#### Create a wrapper script

You can create an entrypoint script that wraps your startup commands, and
execute that script with a JSON-formatted `ENTRYPOINT` command.

✅ Good: the `ENTRYPOINT` uses JSON format.

```dockerfile
FROM alpine
RUN apk add bash
COPY --chmod=755 <<EOT /entrypoint.sh
#!/usr/bin/env bash
set -e
my-background-process &
my-program start
EOT
ENTRYPOINT ["/entrypoint.sh"]
```

#### Explicitly specify the shell

You can use the [SHELL](https://docs.docker.com/reference/dockerfile/#shell)
Dockerfile instruction to explicitly specify a shell to use. This will suppress
the warning since setting the `SHELL` instruction indicates that using shell
form is a conscious decision.

✅ Good: shell is explicitly defined.

```dockerfile
FROM alpine
RUN apk add bash
SHELL ["/bin/bash", "-c"]
ENTRYPOINT echo "hello world"
```
