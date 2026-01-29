# Token typesStay organized with collectionsSave and categorize content based on your preferences.

# Token typesStay organized with collectionsSave and categorize content based on your preferences.

# Token typesStay organized with collectionsSave and categorize content based on your preferences.

Google Cloud issues multiple types of tokens, which differ by their purpose and
the parties they're exchanged between.

The following table gives an overview of the main token categories, within which
are different token types.

| Token category | Communication path | Purpose |
| --- | --- | --- |
| Access tokens | Authorization server⭢Client⭢Google API | Lets clients call Google Cloud APIs. |
| Token-granting tokens | Authorization server⭤Client | Lets clients obtain new or different tokens, possibly at a later point
        in time. |
| Identity tokens | Authorization server⭢Client | Lets clients identify the user they're interacting with. |

Access and identity tokens are *bearer tokens*. Bearer tokens are a general
class of token that grant access to the party in possession of the token.

Using bearer tokens for authentication relies on the security provided by an
encrypted protocol, such as HTTPS. If a bearer token is intercepted, it can be
used by a bad actor to gain access.

If bearer tokens don't provide sufficient security for your use case, you can
decrease the risk of token theft by using
[context-aware access](https://support.google.com/a/answer/12645308), limiting
the lifetime of access tokens, or by using a mutual Transport Layer Security
(mTLS) solution such as
[Chrome Enterprise Premium](https://cloud.google.com/chrome-enterprise-premium/docs/securing-resources-with-certificate-based-access).

## Access tokens

Access tokens allow clients to make authenticated calls to Google Cloud APIs.
Google Cloud supports multiple different types of access tokens, which have the
following properties in common:

- They authenticate a principal, which can be a user or a workload.
- They're issued to one particular client.
- They're short-lived and expire after at most a few hours.
- They're restricted to certain OAuth scopes, endpoints, or resources. This
  means that an access token typically doesn't grant access to all of a user's
  resources, but only to a certain subset of them.

Access tokens can differ in the following ways:

- **Issuer**: The party that issues the token.
- **Principal**: The type of principal that the token can authenticate.
- **Restrictions**: The restrictions that can be imposed on the token.

The following table lists the different types of access tokens:

| Token type | Issuer | Principals | Restrictions |
| --- | --- | --- | --- |
| User access token | Google authorization server | User (managed user)User (consumer account) | OAuth scope |
| Service account access token | Google authorization serverGoogle Cloud IAM authorization server | Service account | OAuth scope |
| Domain-wide delegation token | Google authorization server | User (managed user) | OAuth scope |
| Service account JSON Web Token (JWT) | Client | Service account | OAuth scope or API |
| Federated access token | Google Cloud IAM authorization server | Workforce identity pool principalWorkload identity pool principal | OAuth scope |
| Credential access boundary token | Google Cloud IAM authorization server | User (managed user)User (consumer account)Service account | Specific Cloud Storage objects |
| Client-issued credential access boundary token | Client | Service account | Specific Cloud Storage objects |

The different types of access tokens also exhibit different security properties:

- **Format**: Some access tokens are opaque, meaning they are in a proprietary
  format and can't be inspected. Other tokens are encoded as a JSON Web Token,
  which can be decoded by the client.
- **Introspectability**: Some opaque tokens can be introspected using the
  Google Cloud API, whereas others can't.
- **Lifetime**: Tokens differ in lifetime and to what extent they can be
  modified.
- **Revocability**: Some tokens can be revoked. Other tokens remain valid until
  expiry.

The following table summarizes the differences between the access token types.

| Token type | Format | Introspectable | Lifetime | Revocable |
| --- | --- | --- | --- | --- |
| User access token | Opaque | Yes | 1 hour | Yes |
| Service account access token | Opaque | Yes | 5 minutes–12 hours | No |
| Domain-wide delegation token | Opaque | Yes | 1 hour | No |
| Service account JSON Web Token (JWT) | JWT | N/A | 5 minutes–1 hour | No |
| Federated access token | Opaque | No | SeeFederated access tokens | No |
| Credential access boundary token | Opaque | No | SeeCredential access boundary tokens | No |
| Client-issued credential access boundary token | Opaque | No | N/A | No |

### User access tokens

User access tokens authenticate a user and authorize a client to act on the
user's behalf:

The authenticated principal is either a
[managed user account](https://cloud.google.com/architecture/identity/overview-google-authentication#managed_user_account)
or a
[consumer account](https://cloud.google.com/architecture/identity/overview-google-authentication#consumer_account).
The client can be a web application or a native application.

User access tokens are opaque. For diagnostic purposes, you can introspect an
access token by using the following command, replacing
`ACCESS_TOKEN` with a valid access token:

```
curl "https://oauth2.googleapis.com/tokeninfo?access_token=ACCESS_TOKEN"
```

This command produces output similar to the following example:

```
{
  "azp": "0000000000.apps.googleusercontent.com",
  "aud": "0000000000.apps.googleusercontent.com",
  "sub": "00000000000000000000",
  "scope": "openid https://www.googleapis.com/auth/userinfo.email",
  "exp": "1744687132",
  "expires_in": "3568",
  "email": "user@example.com",
  "email_verified": "true"
}
```

The output includes the following fields:

| Field | Name | Description |
| --- | --- | --- |
| aud | Audience | The OAuth client that this token is for, identified by itsOAuth client ID.OAuth clients can obtain access tokens for other OAuth clients that
          belong to the same project. The audience might differ from the
          authorized party. |
| azp | Authorized party | The OAuth client that requested the token, identified by its OAuth
        client ID. |
| email | Primary email address | The user's primary email address.This field is only present if the token includes thehttps://www.googleapis.com/auth/userinfo.emailscope. |
| exp | Expiry | The expiry time of the token, in Unix epoch time format. |
| scope | OAuth scopes | The set of APIs that the client is allowed to access on behalf of the
        user, identified byOAuth scope. |
| sub | Subject | The authenticated principal, identified by their unique ID.This ID is equivalent to the ID exposed in theDirectory API. |

User access tokens automatically expire after one hour, but can be
[revoked](https://developers.google.com/identity/protocols/oauth2/web-server#tokenrevoke)
earlier if needed.

By default, user access tokens are bearer tokens, which means they're not bound
to any particular communication channel, network, or additional credential.
You can optionally implement token binding by
[deploying certificate-based access](https://cloud.google.com/chrome-enterprise-premium/docs/securing-resources-with-certificate-based-access)
so that user access tokens can only be used in conjunction with a valid mTLS
client certificate.

### Service account access tokens

Service account access tokens authenticate a service account. The tokens are
opaque
and you can introspect them using the
[https://oauth2.googleapis.com/tokeninfo](https://oauth2.googleapis.com/tokeninfo)
API.

For a service account access token, the API returns output similar to the
following example:

```
{
  "azp": "000000000000000000000",
  "aud": "000000000000000000000",
  "scope": "https://www.googleapis.com/auth/userinfo.email",
  "exp": "1744687132",
  "expires_in": "3568",
  "email": "service-account@example.iam.gserviceaccount.com",
  "email_verified": "true",
  "access_type": "online"
}
```

A service account token includes the following fields:

| Field | Name | Description |
| --- | --- | --- |
| aud | Audience | The service account that the token is for, equivalent to the
        authorized party. |
| azp | Authorized party | The service account that requested the token, identified by its unique
        ID. |
| email | Primary email address | The service account's email address.This field is only present if the token includes thehttps://www.googleapis.com/auth/userinfo.emailscope. |
| exp | Expiry | The expiry time of the token, in Unix epoch time format. |

Service account access tokens can't be revoked and stay valid until they expire.

By default, service account access tokens expire after one hour. By using the
[serviceAccounts.generateAccessToken](https://cloud.google.com/iam/docs/reference/credentials/rest/v1/projects.serviceAccounts/generateAccessToken)
method, you can request tokens with different lifetimes. Because longer token
lifetimes can increase risk, you must configure the
[iam.allowServiceAccountCredentialLifetimeExtension](https://cloud.google.com/resource-manager/docs/organization-policy/restricting-service-accounts#extend_oauth_ttl)
constraint to allow clients to request service account access tokens with
lifetimes longer than one hour.

### Domain-wide delegation tokens

Domain-wide delegation tokens authenticate a user and authorize a service
account to act on the user's behalf. The tokens are opaque and you can
introspect them using the
[https://oauth2.googleapis.com/tokeninfo](https://oauth2.googleapis.com/tokeninfo)
API.

For a domain-wide delegation token, the API returns output similar to the
following example:

```
{
  "azp": "000000000000000000000",
  "aud": "000000000000000000000",
  "scope": "https://www.googleapis.com/auth/admin.directory.user.readonly https://www.googleapis.com/auth/userinfo.email",
  "exp": "1744688957",
  "expires_in": "3540",
  "email": "user@example.com",
  "email_verified": "true",
  "access_type": "offline"
}
```

A domain-wide delegation token includes the following fields:

| Field | Name | Description |
| --- | --- | --- |
| aud | Audience | The service account that the token is for, equivalent to the authorized
        party. |
| azp | Authorized party | The service account that requested the token, identified by its unique
        ID. |
| email | Primary email address | The impersonated user's primary email address.This field is only present if the token includes thehttps://www.googleapis.com/auth/userinfo.emailscope. |
| exp | Expiry | The expiry time of the token, in Unix epoch time format. |
| scope | OAuth scopes | The set of APIs that the client is allowed to access on behalf of the
        impersonated user, identified byOAuthscope. |

Domain-wide delegation tokens automatically expire after one hour, and they
can't be revoked.

### Service account JSON Web Tokens

Service account JSON Web Tokens (JWTs) authenticate a service account. Whereas
[service account access tokens](#sa-access-tokens) are issued by an
authorization server, service account JWTs can be issued by the client itself.

Sometimes these are called "self-signed" JWTs. They can be useful when you need
to authenticate to some Google APIs without getting an access token from the
authorization server—for example, when creating your own client libraries.

To issue a service account JWT, clients must perform the following steps:

1. Prepare a JSON web signature payload that includes the service account's
  email address, an OAuth scope or API endpoint, and an expiry time.
2. Sign the payload using a service account key of the respective service
  account. Clients can sign the payload offline by using a user-managed
  service account key, or online by using the `signJwt` method and a
  Google-managed service account key. For more information, see
  [Create a self-signed JSON Web Token](https://cloud.google.com/iam/docs/create-short-lived-credentials-direct#sa-credentials-jwt)

A decoded service account JWT looks similar to the following, with
`SIGNATURE` replaced by the token's signature:

```
{
  "alg": "RS256",
  "kid": "290b7bf588eee0c35d02bf1164f4336229373300",
  "typ": "JWT"
}.{
  "iss": "service-account@example.iam.gserviceaccount.com",
  "sub": "service-account@example.iam.gserviceaccount.com",
  "scope": "https://www.googleapis.com/auth/cloud-platform",
  "exp": 1744851267,
  "iat": 1744850967
}.SIGNATURE
```

Instead of specifying an OAuth scope in the `scope` key, a service account JWT
can specify an API endpoint in the `aud` key:

```
{
  "alg": "RS256",
  "kid": "290b7bf588eee0c35d02bf1164f4336229373300",
  "typ": "JWT"
}.{
  "iss": "service-account@example.iam.gserviceaccount.com",
  "sub": "service-account@example.iam.gserviceaccount.com",
  "aud": "https://cloudresourcemanager.googleapis.com/",
  "exp": 1744854799,
  "iat": 1744851199
}.SIGNATURE
```

A service account JWT includes the following fields:

| Field | Name | Description |
| --- | --- | --- |
| aud | Audience | API endpoints that the client is allowed to access. Only valid ifscopeisn't specified. |
| exp | Expiry | The expiry time of the token, in Unix epoch time format. |
| iat | Issue time | The time the token was issued, in Unix epoch time format. |
| iss | Issuer | The issuer of the token, which is the service account itself. |
| scope | OAuth scopes | The set of APIs that the client is allowed to access, identified byOAuth scope. Only valid ifaudisn't specified. |
| sub | Subject | Authenticated principal, which is the service account itself. |

Service account JWTs can be valid for up to one hour, and they can't be revoked.

### Federated access tokens

Federated access tokens authenticate a identity workforce pool principal or a
workload identity pool principal.

Workforce Identity Federation lets clients exchange an external token against a
federated access token that authenticates a workforce pool principal. The
workforce identity pool principal is identified by a principal identifier similar
to the following:

```
principal://iam.googleapis.com/locations/global/workforcePools/POOL/subject/raha@altostrat.com.
```

Workload Identity Federation lets clients exchange an external token against a
federated access token that authenticates a workload pool principal. The
workload identity pool principal is identified by a principal identifier similar
to the following:

```
principal://iam.googleapis.com/projects/PROJECT/locations/global/workloadIdentityPools/POOL/subject/SUBJECT_ATTRIBUTE_VALUE
```

Federated access tokens are opaque and can't be introspected. The tokens can't
be revoked and remain valid until expiry. The expiries for each token type are
set as follows:

- Workforce Identity Federation sets the token expiry to the smaller of the
  following two values:
  - Time left until the Workforce Identity Federation session expires
  - 1 hour
  The expiry of the Workforce Identity Federation session is determined based on
  the time of sign-in and the session duration configured for the
  Workforce Identity Federation pool.
- Workload Identity Federation sets the token expiry so that it matches the expiry
  of the external token.

### Credential access boundary tokens

Credential access boundary tokens authenticate a user or service account and
[include an access boundary](https://cloud.google.com/iam/docs/downscoping-short-lived-credentials). The
access boundary restricts the token so that it can only be used to access a
defined subset of Cloud Storage resources.

Credential access boundary tokens are sometimes referred to as *downscoped*
because they're derived from an input token, but are more restricted in the
resources they grant access to.

The expiry of credential access boundary tokens is derived from the expiry of
the input token, which
can be a [user access token](#user-access-tokens) or
[service account access token](#sa-access-tokens). Credential access boundary
tokens are opaque and they can't be introspected or revoked.

### Client-issued credential access boundary tokens

Client-issued credential access boundary tokens are similar to
[credential access boundary tokens](#cred-access-boundary-tokens), but are
optimized for scenarios in which clients need to obtain credential access
boundary tokens with different access boundaries at high frequency.

Clients can create client-issued credential access boundary tokens locally by
using the Cloud Client Libraries and an access boundary intermediary token,
which they must refresh periodically.

Client-issued credential access boundary tokens are opaque and they can't be
introspected or revoked.

## Token-granting tokens

Token-granting tokens allow clients to obtain new or different tokens, possibly
at a later time. Google Cloud supports multiple different types of
token-granting tokens, and they all have the following in common:

- They represent a prior authentication.
- They authenticate a principal, which can be a Google identity (a user or
  workload) or an external identity.
- They can be redeemed for an access token.
- They can't be used for making Google API calls, which distinguishes them from
  access tokens.

Token-granting tokens can differ in the following ways:

- **Issuer**: The party that issues the token.
- **Principal**: The type of principal identity that the token can authenticate.
- **Restrictions**: The restrictions that can be imposed on the token.

The following table lists the different types of token-granting tokens.

| Token type | Issuer | Redeemed access token type | Principals | Restrictions |
| --- | --- | --- | --- | --- |
| Refresh token | Google authorization server | User access token | User (managed user)User (consumer account) | OAuth scope |
| Authorization code | Google authorization server | User access token | User (managed user)User (consumer account) | OAuth scope |
| Federated refresh token | Google Cloud IAM authorization server | Federated access token | Workforce identity pool principal | OAuth scope |
| Federated authorization code | Google Cloud IAM authorization server | Federated access token | Workforce identity pool principal | OAuth scope |
| Service account JSON Web Token assertion | Client | Domain-wide delegation tokenService account access token | User (managed user)Service account | OAuth scope |
| External JSON Web Token | External identity provider | Federated access token | External principal | None |
| External SAML assertion or response | External identity provider | Federated access token | External principal | None |
| Amazon Web Services (AWS)GetCallerIdentitytoken | External identity provider | Federated access token | External principal | None |

The different types of token-granting tokens also exhibit different security
properties:

- **Format**: Some tokens are opaque. Other tokens can be decoded by the client.
- **Lifetime**: Tokens differ in lifetime, and to what extent they can be
  modified.
- **Multi-use**: Some token-granting tokens can only be used once. Other tokens
  can be used multiple times.
- **Revocability**: Some tokens can be revoked. Other tokens remain valid until
  expiry.

The following table summarizes the differences between these properties for
token-granting tokens:

| Token type | Format | Lifetime | Revocable | Multi-use |
| --- | --- | --- | --- | --- |
| Refresh token | Opaque | Varies, seeRefresh tokens | Yes | Yes |
| Authorization code | Opaque | 10 minutes | No | No |
| Federated refresh token | Opaque | Varies, seeFederated refresh tokens | No | Yes |
| Federated authorization code | Opaque | 10 minutes | No | No |
| Service account JSON Web Token assertion | JWT | 5 minutes–1 hour | No | Yes |
| External token or external JSON Web Token | JWT | Depends on identity provider | Depends on identity provider | Yes |
| External SAML assertion or response | SAML | Depends on identity provider | Depends on identity provider | Yes |
| Amazon Web Services (AWS)GetCallerIdentitytoken | Text blob | Depends on identity provider | Depends on identity provider | Yes |

### Refresh tokens

Refresh tokens are opaque tokens that let clients obtain ID tokens and access
tokens for a user, if the user previously authorized a client to act on their
behalf.

Refresh tokens are tied to a specific client and can only be used in combination
with valid client credentials; for example, a client ID and client secret.

If the client's authorization includes one or more
[Google Cloud OAuth scopes](https://developers.google.com/identity/protocols/oauth2/scopes),
then the lifetime of the refresh token is subject to the
[Google Cloud session length](https://support.google.com/a/answer/9368756)
control. Otherwise, refresh tokens remain valid until the user revokes their
authorization or other
[token-revoking events](https://developers.google.com/identity/protocols/oauth2#expiration)
occur.

### Authorization codes

Authorization codes are opaque, short-lived tokens.
[The codes are only intended to be used during user authentication as an intermediary](https://datatracker.ietf.org/doc/html/rfc6749#section-1.3.1)
between the client and the Google authorization server.

Like [refresh tokens](#refresh-tokens), authorization codes are tied to a client
and can only be used in combination with valid client credentials. Unlike
refresh tokens, authorization codes can only be used once.

### Federated refresh tokens

Federated refresh tokens are opaque tokens that let clients obtain access
tokens for a workforce identity pool principal, if the user previously
authorized a client to act on their behalf.

Like [refresh tokens](#refresh-tokens), federated refresh tokens are tied to a
specific client and can only be used in combination with valid client
credentials; for example, a client ID and client secret.

Unlike refresh tokens, federated refresh tokens can't be revoked. The lifetime
of a federated refresh token is linked to the workforce identity session that
was used to obtain the token and it remains valid until the session expires.

### Federated authorization codes

Like [authorization codes](#authorization-codes), federated authorization codes
are opaque, short-lived tokens.
[The codes are only intended to be used during user authentication as an intermediary](https://datatracker.ietf.org/doc/html/rfc6749#section-1.3.1)
between the client and the Google Cloud IAM authorization server.

Authorization codes are tied to a client, can only be used in combination with
valid client credentials, and can only be used once.

### Service account JSON Web Token assertions

Service account JSON Web Tokens (JWTs) assertions assert the identity of a
service account. Workloads can use service account JWT assertions to obtain
[service account access tokens](#sa-access-tokens) or
[domain-wide delegation tokens](#domain-wide-delegation-tokens). The service
account JWT assertion is signed by a service account key.

A decoded service account JWT assertion looks similar to the following, with
`SIGNATURE` replaced by the token's signature:

```
{
  "alg": "RS256",
  "kid": "290b7bf588eee0c35d02bf1164f4336229373300",
  "typ": "JWT"
}.{
  "iss": "service-account@example.iam.gserviceaccount.com",
  "scope": "https://www.googleapis.com/auth/devstorage.read_only",
  "aud": "https://oauth2.googleapis.com/token",
  "exp": 1744851267,
  "iat": 1744850967
}.SIGNATURE
```

Service account JWT assertions are structurally similar to
[service account JWTs](#sa-jwts): both types of tokens can be issued by the
client itself, and are signed by a service account key. However, the two types
of tokens use different payloads, as described in the following table.

| Field | Service account JWT | Service account JWT assertion |
| --- | --- | --- |
| aud | Google Cloud API, omitted ifscopeis specified | Must behttps://oauth2.googleapis.com/token |
| exp | Expiry | Expiry |
| iat | Issue time | Issue time |
| iss | Email address of the service account | Email address of the service account |
| scope | OAuth scopes, omitted ifaudis specified | OAuth scopes |
| sub | Email address of the service account | Email address of a user account for domain wide delegation, omitted
        otherwise |

Service account JWT assertions can be valid up to one hour, and they can't be
revoked.

### External JSON Web Tokens

External JSON Web Tokens (JWTs) are issued by an external identity provider such
as Microsoft Entra ID, Okta, Kubernetes, or GitHub. They might differ in their
structure and contents.

By configuring Workforce Identity Federation or Workload Identity Federation, you can
set up a trust relationship between Google Cloud and an external identity
provider. Workloads can then use external JWTs as token-granting tokens to
obtain [federated access tokens](#fed-access-tokens).

When you use Workforce Identity Federation, the resulting federated access token
authenticates a *workforce* identity pool principal.

When you use Workload Identity Federation, the resulting federated access token
authenticates a *workload* identity pool principal.

In both cases, the principal identifier is derived from one or more claims of
the external JWT.

To be compatible with Workforce Identity Federation or Workload Identity Federation,
external JWTs must satisfy
[specific requirements](https://cloud.google.com/iam/docs/workload-identity-federation-with-other-providers#prepare).

### External SAML assertions or responses

External
[Security Assertion Markup Language](https://wiki.oasis-open.org/security)
(SAML) assertions are SAML 2.0 assertions that are issued by an external
identity provider such as Microsoft Entra ID, Okta, or Active Directory
Federation Services. These external SAML assertions can optionally be enclosed
in a SAML 2.0 response or be encrypted.

Like with [external JSON Web Tokens](#external-jwts), you can configure
Workforce Identity Federation or Workload Identity Federation so that workloads can use
external SAML assertions or responses as token-granting tokens to obtain
[federated access tokens](#fed-access-tokens).

To be compatible with Workforce Identity Federation or Workload Identity Federation,
external SAML assertions must satisfy
[specific requirements](https://cloud.google.com/iam/docs/workload-identity-federation-with-other-providers#prepare).

### Amazon Web Services (AWS)GetCallerIdentitytoken

External AWS `GetCallerIdentity` tokens are text blobs that contain a signed
request to the AWS
[GetCallerIdentityAPI](https://docs.aws.amazon.com/STS/latest/APIReference/API_GetCallerIdentity.html).
Similar to external JSON Web Tokens
and SAML assertions, you can configure Workforce Identity Federation or Workload Identity Federation so
that workloads can use these text blobs as a token-granting token to obtain
[federated access tokens](#fed-access-tokens).

## Identity tokens

Identity (ID) tokens let clients identify the user that they're interacting
with. Google Cloud supports multiple different types of identity tokens, and
they all have the following in common:

- They're formatted as JSON Web Tokens (JWTs) so that they can be decoded,
  verified, and interpreted by the client.
- They authenticate a principal, which can be a user or a workload.
- They're issued to one particular client.
- They're short-lived and expire after at most one hour.
- They're not revocable.
- They can't be used for making Google API calls, which distinguishes them from
  [access tokens](#access-tokens).
- They can't be used to obtain access tokens, which distinguishes them from
  [token-granting tokens](#token-granting-tokens).
- They can be used to authenticate
  [calls between microservices](https://cloud.google.com/run/docs/authenticating/service-to-service), or
  to [programmatically authenticate to
  Identity-Aware Proxy (IAP)](https://cloud.google.com/iap/docs/authentication-howto).

Identity tokens can differ in the following ways:

- **Audience**: The party that's intended to decode and consume the token.
- **Issuer**: The party that issues the token.
- **Lifetime**: The tokens differ in lifetime, and to what extent they can be
  modified.
- **Principal**: The type of principal identity that the token can authenticate.

The following table lists the different types of identity tokens.

| Token type | Issuer | Audience | Principal | Lifetime |
| --- | --- | --- | --- | --- |
| User ID token | Google authorization server | OAuth/OIDC client | User (managed user)User (consumer account) | 1 hour |
| Service account ID token | Google Cloud IAM authorization server | Free to choose any audience | Service account | 1 hour |
| Identity-Aware Proxy (IAP) assertion | IAP | BackendApp Engine app | User (managed user)User (consumer account)Workforce identity pool principal | 10 minutes |
| SAML assertion | Google authorization server | SAML app | User (managed user) | 10 minutes |

### User ID tokens

User ID tokens are JSON Web Tokens (JWTs) that authenticate a user. Clients can
obtain a user ID Token by initiating an
[OIDC authentication flow](https://developers.google.com/identity/openid-connect/openid-connect#authenticatingtheuser).

User ID tokens are signed using the Google JSON Web Key Set (JWKS). The Google
JWKS is a global resource, and the same signing keys are used for different
types of users, including the following:

- Managed user accounts
- Consumer user accounts
- Service accounts

A decoded user ID token looks similar to the following, with
`SIGNATURE` replaced by the token's signature:

```
{
  "alg": "RS256",
  "kid": "c37da75c9fbe18c2ce9125b9aa1f300dcb31e8d9",
  "typ": "JWT"
}.{
  "iss": "https://accounts.google.com",
  "azp": "1234567890-123456789abcdef.apps.googleusercontent.com",
  "aud": "1234567890-123456789abcdef.apps.googleusercontent.com",
  "sub": "12345678901234567890",
  "at_hash": "y0LZEe-ervzRNSxn4R-t9w",
  "name": "Example user",
  "picture": "https://lh3.googleusercontent.com/a/...",
  "given_name": "Example",
  "family_name": "User",
  "hd": "example.com",
  "iat": 1745361695,
  "exp": 1745365295
}.SIGNATURE
```

An ID token includes the following fields:

| Field | Name | Description |
| --- | --- | --- |
| aud | Audience | The OAuth client that this token is for, identified by its OAuth
          client ID.OAuth clients can obtain access tokens for other OAuth clients that
          belong to the same project. In this case, the audience might differ
          from the authorized party. |
| azp | Authorized party | The OAuth client that performed the OIDC authentication flow, identified
        by itsOAuth client ID. |
| exp | Expiry | The expiry time of the token, in Unix epoch time format. |
| hd | Hosted domain | The primary domain of the user's Cloud Identity or
          Google Workspace account.This claim is only present if the user is a managed user account and
          the client specified thehdparameter in the authentication request. |
| iss | Issuer | The issuer of the token. Always set tohttps://accounts.google.com. |
| sub | Subject | The authenticated principal, identified by their unique ID.This ID is equivalent to the ID exposed in theDirectory API. |

The exact set of claims included in an ID token depends on the `scope` parameter
in the authentication request.

To identify whether a user is a managed user account, or to identify the
Cloud Identity or Google Workspace account a user belongs to, clients must
inspect the [hd](#hd) claim.

User ID tokens are valid for one hour, and can't be revoked.

### Service account ID tokens

Service account ID tokens are JSON Web Tokens (JWTs) that authenticate a service
account.

Unlike [service account JWTs](#sa-jwts) and
[service account JWT assertions](#sa-jwt-assertions), service account ID tokens
aren't signed by a service account key. Instead, service account ID tokens are
signed by the Google JSON Web Key Set (JWKS).

A decoded service account ID token looks similar to the following, with
`SIGNATURE` replaced by the token's signature:

```
{
  "alg": "RS256",
  "kid": "c37da75c9fbe18c2ce9125b9aa1f300dcb31e8d9",
  "typ": "JWT"
}.{
  "aud": "example-audience",
  "azp": "112010400000000710080",
  "email": "service-account@example.iam.gserviceaccount.com",
  "email_verified": true,
  "exp": 1745365618,
  "iat": 1745362018,
  "iss": "https://accounts.google.com",
  "sub": "112010400000000710080"
}.SIGNATURE
```

A service account ID token includes the following fields:

| Field | Name | Description |
| --- | --- | --- |
| aud | Audience | Identifier of the party that this token is for. The value can be freely
        chosen by the token requester. |
| azp | Authorized party | The service account that requested the token, identified by its unique
        ID. |
| exp | Expiry | The expiry time of the token, in Unix epoch time format. |
| iss | Issuer | The issuer of the token, always set tohttps://accounts.google.com. |
| sub | Subject | The service account that requested the token, identified by its unique
        ID. |

The exact set of claims included in an ID token depends on the way the ID token
is requested. For example, ID tokens requested by the Compute Engine
metadata server can optionally include additional claims that
[assert the identity of the VM](https://cloud.google.com/compute/docs/instances/verifying-instance-identity).
ID Tokens requested by using the
[IAM Credentials API](https://cloud.google.com/iam/docs/reference/credentials/rest/v1/projects.serviceAccounts/generateIdToken)
can optionally contain the organization ID of the service account's project.

Unlike user ID tokens, service account ID tokens don't support the [hd](#hd)
claim.

Service account ID tokens are valid for one hour, and can't be revoked.

### Identity-Aware Proxy assertions

[Identity-Aware Proxy (IAP)](https://cloud.google.com/iap/docs/concepts-overview) assertions are JSON
Web Tokens (JWTs) that IAP passes to
IAP-protected web applications in the `x-goog-iap-jwt-assertion`
HTTP request header. IAP assertions authenticate a user and also
serve as proof that a request was authorized by IAP.

Unlike [user ID tokens](#user-id-tokens) and
[service account ID tokens](#sa-id-tokens), IAP assertions aren't
signed using the Google JSON Web Key Set (JWKS). Instead, IAP
assertions are signed using a separate JWKS,
the
[IAP JWKS](https://www.gstatic.com/iap/verify/public_key-jwk).
This JWKS is a global resource, and the same signing keys are used for different
types of users, including the following:

- Managed user accounts
- Consumer accounts
- Service accounts
- Workforce identity pool principals

A decoded IAP assertion looks similar to the following, with
`SIGNATURE` replaced by the token's signature:

 `json {:.readonly}
{
  "alg": "ES256",
  "typ": "JWT",
  "kid": "4BCyVw"
}.{
  "aud": "/projects/0000000000/global/backendServices/000000000000",
  "azp": "/projects/0000000000/global/backendServices/000000000000",
  "email": "user@example.com",
  "exp": 1745362883,
  "google": {
    "access_levels": [
      "accessPolicies/0000000000/accessLevels/Australia"
    ]
  },
  "hd": "example.com",
  "iat": 1745362283,
  "identity_source": "GOOGLE",
  "iss": "https://cloud.google.com/iap",
  "sub": "accounts.google.com:112010400000000710080"
}.SIGNATURE`

If you
[configure IAP to use Workforce Identity Federation](https://cloud.google.com/iap/docs/use-workforce-identity-federation)
instead of Google identities, IAP assertions look slightly
different:

```
{
  "alg": "ES256",
  "typ": "JWT",
  "kid": "4BCyVw"
}.{
  "aud": "/projects/0000000000/global/backendServices/000000000000",
  "azp": "/projects/0000000000/global/backendServices/000000000000",
  "email": "user@example.com",
  "exp": 1745374290,
  "google": {
    "access_levels": [
      "accessPolicies/0000000000/accessLevels/Australia"
    ]
  },
  "iat": 1745373690,
  "identity_source": "WORKFORCE_IDENTITY",
  "iss": "https://cloud.google.com/iap",
  "sub": "sts.google.com:AAFTZ...Q",
  "workforce_identity": {
    "iam_principal": "principal://iam.googleapis.com/locations/global/workforcePools/example/subject/user-0000000000",
    "workforce_pool_name": "locations/global/workforcePools/example"
  }
}.SIGNATURE
```

An IAP assertion includes the following fields:

| Field | Name | Description |
| --- | --- | --- |
| aud | Audience | The backend service, App Engine application, or Cloud Run
        service that the IAP assertion is intended for. |
| iss | Issuer | The issuer of the token, always set tohttps://cloud.google.com/iap |
| sub | Subject | The authenticated principal, identified by their unique ID.If IAP is configured to use Google identities, this ID
          is equivalent to the ID exposed in theDirectory API. |

For further details about the IAP assertion claims, see
[Verifying the JWT payload](https://cloud.google.com/iap/docs/signed-headers-howto#verifying_the_jwt_payload).

IAP assertions are valid for 10 minutes, and can't be revoked.

### SAML assertions

[Security Assertion Markup Language](https://wiki.oasis-open.org/security)
(SAML) assertions authenticate a managed user account and authorize them to
access a
[custom SAML app](https://support.google.com/cloudidentity/answer/6087519). SAML
assertions are issued and signed by Cloud Identity and can only be used to
authenticate managed user accounts.

Unlike ID tokens which are signed by using global key, SAML assertions are
signed by using a key that is specific to a Cloud Identity or
Google Workspace account.

A decoded SAML response assertion looks similar to the following:

```
<saml2:Assertion
  xmlns:saml2="urn:oasis:names:tc:SAML:2.0:assertion"
  ID="..."
  IssueInstant="2025-04-23T22:47:20.881Z"
  Version="2.0">
  <saml2:Issuer>
    https://accounts.google.com/o/saml2?idpid=C0123456789
  </saml2:Issuer>
  <ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#">...</ds:Signature>
  <saml2:Subject>
    <saml2:NameID
      Format="urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified">
        user@example.com
    </saml2:NameID>
    <saml2:SubjectConfirmation Method="urn:oasis:names:tc:SAML:2.0:cm:bearer">
      <saml2:SubjectConfirmationData
        NotOnOrAfter="2025-04-23T22:52:20.881Z"
        Recipient="https://app.example.com/"/>
    </saml2:SubjectConfirmation>
  </saml2:Subject>

  <saml2:Conditions
    NotBefore="2025-04-23T22:42:20.881Z"
    NotOnOrAfter="2025-04-23T22:52:20.881Z">
    <saml2:AudienceRestriction>
      <saml2:Audience>example-app</saml2:Audience>
    </saml2:AudienceRestriction>
  </saml2:Conditions>

  <saml2:AuthnStatement
    AuthnInstant="2025-04-23T22:46:44.000Z"
    SessionIndex="...">
    <saml2:AuthnContext>
      <saml2:AuthnContextClassRef>
        urn:oasis:names:tc:SAML:2.0:ac:classes:unspecified
      </saml2:AuthnContextClassRef>
    </saml2:AuthnContext>
  </saml2:AuthnStatement>
</saml2:Assertion>
```

A SAML assertion includes the following fields:

| Field | Name | Description |
| --- | --- | --- |
| Audience | Audience | Entity ID of the SAML app. |
| Issuer | Issuer | Issuer of the token, specific to a Cloud Identity or
        Google Workspace account. |
| NameID | Subject | The authenticated principal. The format of the identifier depends on the
        SAML app's configuration. |

The exact set of attributes included in a SAML assertion depends on the SAML
app's configuration.

SAML assertions are valid for 10 minutes, and can't be revoked.

 Was this helpful?
