# Authentication setup and more

# Authentication setup

> Control access to your documentation by authenticating users.

[Pro plans](https://mintlify.com/pricing?ref=authentication) include password authentication.[Custom plans](https://mintlify.com/pricing?ref=authentication) include all authentication methods. Authentication requires users to log in before accessing your documentation. When you enable authentication, users must log in to access any content. You can configure specific pages or groups as public while keeping other pages protected.

## ​Configure authentication

 Select the handshake method that you want to configure.

- Password
- Mintlify dashboard
- OAuth 2.0
- JWT

Password authentication provides access control only and does **not** support content personalization.

### ​Prerequisites

- Your security requirements allow sharing passwords among users.

### ​Set up

1

Create a password.

1. In your dashboard, go to [Authentication](https://dashboard.mintlify.com/settings/deployment/authentication).
2. Enable authentication.
3. In the **Password Protection** section, enter a secure password

After you enter a password, your site redploys. When it finishes deploying, anyone who visits your site must enter the password to access your content.2

Distribute access.

Securely share the password and documentation URL with authorized users.

### ​Example

Your host your documentation at `docs.foo.com` and you need basic access control without tracking individual users. You want to prevent public access while keeping setup simple.**Create a strong password** in your dashboard. **Share credentials** with authorized users. That’s it!

### ​Prerequisites

- Everyone who needs to access your documentation must be a member of your Mintlify organization.

### ​Set up

1

Enable Mintlify dashboard authentication.

1. In your dashboard, go to [Authentication](https://dashboard.mintlify.com/settings/deployment/authentication).
2. Enable authentication.
3. In the **Custom Authentication** section, click **Mintlify Auth**.
4. Click **Enable Mintlify Auth**.

After you enable Mintlify authentication, your site redeploys. When it finishes deploying, anyone who visits your site must log in to your Mintlify organization to access your content.2

Add authorized users.

1. In your dashboard, go to [Members](https://dashboard.mintlify.com/settings/organization/members).
2. Add each person who should have access to your documentation.
3. Assign appropriate roles based on their editing permissions.

### ​Example

Your host your documentation at `docs.foo.com` and your entire team has access to your dashboard. You want to restrict access to team members only.**Enable Mintlify authentication** in your dashboard settings.**Verify team access** by checking that all team members are active in your organization.

### ​Prerequisites

- An OAuth or OIDC server that supports the Authorization Code Flow.
- Ability to create an API endpoint accessible by OAuth access tokens (optional, to enable group-based access control).

### ​Set up

1

Configure your OAuth settings.

1. In your dashboard, go to [Authentication](https://dashboard.mintlify.com/settings/deployment/authentication).
2. Enable authentication.
3. In the **Custom Authentication** section, click **OAuth**.
4. Configure these fields:

- **Authorization URL**: Your OAuth endpoint.
- **Client ID**: Your OAuth 2.0 client identifier.
- **Client Secret**: Your OAuth 2.0 client secret.
- **Scopes** (optional): Permissions to request. Copy the **entire** scope string (for example, for a scope like `provider.users.docs`, copy the complete `provider.users.docs`). Use multiple scopes if you need different access levels.
- **Additional authorization parameters** (optional): Additional query parameters to add to the initial authorization request.
- **Token URL**: Your OAuth token exchange endpoint.
- **Info API URL** (optional): Endpoint on your server that Mintlify calls to retrieve user info. Required for group-based access control. If omitted, the OAuth flow only verifies identity.
- **Logout URL** (optional): The native logout URL for your OAuth provider. When users log out, Mintlify validates the logout redirect against this configured URL for security. The redirect only succeeds if it exactly matches the configured `logoutUrl`. If you do not configure a logout URL, users redirect to `/login`. Mintlify redirects users with a `GET` request and does not append query parameters, so include any parameters (for example, `returnTo`) directly in the URL.
- **Redirect URL** (optional): The URL to redirect users to after authentication.

1. Click **Save changes**.

After you configure your OAuth settings, your site redeploys. When it finishes deploying, anyone who visits your site must log in to your OAuth provider to access your content.2

Configure your OAuth server.

1. Copy the **Redirect URL** from your [authentication settings](https://dashboard.mintlify.com/settings/deployment/authentication).
2. Add the redirect URL as an authorized redirect URL for your OAuth server.

3

Create your user info endpoint (optional).

To enable group-based access control, create an API endpoint that:

- Responds to `GET` requests.
- Accepts an `Authorization: Bearer <access_token>` header for authentication.
- Returns user data in the `User` format. See [User data format](#user-data-format) for more information.

Mintlify calls this endpoint with the OAuth access token to retrieve user information. No additional query parameters are sent.Add this endpoint URL to the **Info API URL** field in your [authentication settings](https://dashboard.mintlify.com/settings/deployment/authentication).

### ​Example

Your host your documentation at `foo.com/docs` and you have an existing OAuth server at `auth.foo.com` that supports the Authorization Code Flow.**Configure your OAuth server details** in your dashboard:

- **Authorization URL**: `https://auth.foo.com/authorization`
- **Client ID**: `ydybo4SD8PR73vzWWd6S0ObH`
- **Scopes**: `['provider.users.docs']`
- **Token URL**: `https://auth.foo.com/exchange`
- **Info API URL**: `https://api.foo.com/docs/user-info`
- **Logout URL**: `https://auth.foo.com/logout?returnTo=https%3A%2F%2Ffoo.com%2Fdocs`

**Create a user info endpoint** at `api.foo.com/docs/user-info`, which requires an OAuth access token with the `provider.users.docs` scope, and returns:

```
{
  "groups": ["engineering", "admin"],
  "expiresAt": 1735689600
}
```

Control session length with the `expiresAt` field in your user info response. This is a Unix timestamp (seconds since epoch) indicating when the session should expire. See [User data format](#user-data-format) for more details.**Configure your OAuth server to allow redirects** to your callback URL.

### ​Prerequisites

- An authentication system that can generate and sign JWTs.
- A backend service that can create redirect URLs.

### ​Set up

1

Generate a private key.

1. In your dashboard, go to [Authentication](https://dashboard.mintlify.com/settings/deployment/authentication).
2. Enable authentication.
3. In the **Custom Authentication** section, click **JWT**.
4. Enter the URL of your existing login flow.
5. Click **Save changes**.
6. Click **Generate new key**.
7. Store your key securely where it can be accessed by your backend.

After you generate a private key, your site redeploys. When it finishes deploying, anyone who visits your site must log in to your JWT authentication system to access your content.2

Integrate Mintlify authentication into your login flow.

Modify your existing login flow to include these steps after user authentication:

- Create a JWT containing the authenticated user’s info in the `User` format. See [User data format](#user-data-format) for more information.
- Sign the JWT with your secret key, using the EdDSA algorithm.
- Create a redirect URL back to the `/login/jwt-callback` path of your docs, including the JWT as the hash.

### ​Example

Your host your documentation at `docs.foo.com` with an existing authentication system at `foo.com`. You want to extend your login flow to grant access to the docs while keeping your docs separate from your dashboard (or you don’t have a dashboard).Create a login endpoint at `https://foo.com/docs-login` that extends your existing authentication.After verifying user credentials:

- Generate a JWT with user data in Mintlify’s format.
- Sign the JWT and redirect to `https://docs.foo.com/login/jwt-callback#{SIGNED_JWT}`.

```
import * as jose from 'jose';
import { Request, Response } from 'express';

const TWO_WEEKS_IN_MS = 1000 * 60 * 60 * 24 * 7 * 2;

const signingKey = await jose.importPKCS8(process.env.MINTLIFY_PRIVATE_KEY, 'EdDSA');

export async function handleRequest(req: Request, res: Response) {
  const user = {
    expiresAt: Math.floor((Date.now() + TWO_WEEKS_IN_MS) / 1000), // 2 week session expiration
    groups: res.locals.user.groups,
  };

  const jwt = await new jose.SignJWT(user)
    .setProtectedHeader({ alg: 'EdDSA' })
    .setExpirationTime('10 s') // 10 second JWT expiration
    .sign(signingKey);

  return res.redirect(`https://docs.foo.com/login/jwt-callback#${jwt}`);
}
```

### ​Redirect unauthenticated users

When an unauthenticated user tries to access a protected page, the redirect to your login URL preserves the user’s intended destination.

1. User attempts to visit a protected page: `https://docs.foo.com/quickstart`.
2. Redirect to your login URL with a redirect query parameter: `https://foo.com/docs-login?redirect=%2Fquickstart`.
3. After authentication, redirect to `https://docs.foo.com/login/jwt-callback?redirect=%2Fquickstart#{SIGNED_JWT}`.
4. User lands in their original destination.

## ​Make pages public

 When using authentication, all pages require authentication to access by default. You can make specific pages viewable without authentication at the page or group level with the `public` property.

### ​Individual pages

 To make a page public, add `public: true` to the page’s frontmatter. Public page example

```
---
title: "Public page"
public: true
---
```

### ​Groups of pages

 To make all pages in a group public, add `"public": true` beneath the group’s name in the `navigation` object of your `docs.json`. Public group example

```
{
  "navigation": {
    "groups": [
      {
        "group": "Public group",
        "public": true,
        "icon": "play",
        "pages": [
          "quickstart",
          "installation",
          "settings"
        ]
      },
      {
        "group": "Private group",
        "icon": "pause",
        "pages": [
          "private-information",
          "secret-settings"
        ]
      }
    ]
  }
}
```

## ​Control access with groups

 When you use OAuth or JWT authentication, you can restrict specific pages to certain user groups. This is useful when you want different users to see different content based on their role or attributes. Manage groups through user data passed during authentication. See [User data format](#user-data-format) for details. Example user info

```
{
  "groups": ["admin", "beta-users"],
  "expiresAt": 1735689600
}
```

 Specify which groups can access specific pages using the `groups` property in frontmatter. Example page restricted to the admin group

```
---
title: "Admin dashboard"
groups: ["admin"]
---
```

 Users must belong to at least one of the listed groups to access the page. If a user tries to access a page without the required group, they’ll receive a 404 error.

### ​How groups interact with public pages

- All pages require authentication by default.
- Pages with a `groups` property are only accessible to authenticated users in those groups.
- Pages without a `groups` property are accessible to all authenticated users.
- Pages with `public: true` and no `groups` property are accessible to everyone.

```
---
title: "Public guide"
public: true
---
```

## ​User data format

 When using OAuth or JWT authentication, your system returns user data that controls session length and group membership for access control.

```
type User = {
  expiresAt?: number;
  groups?: string[];
};
```

 [​](#param-expires-at)expiresAtnumberSession expiration time in seconds since epoch. When the current time passes this value, the user must re-authenticate.**For JWT:** This differs from the JWT’s `exp` claim, which determines when a JWT is considered invalid. Set the JWT `exp` claim to a short duration (10 seconds or less) for security. Use `expiresAt` for the actual session length (hours to weeks). [​](#param-groups)groupsstring[]List of groups the user belongs to. Pages with matching `groups` in their frontmatter are accessible to this user.**Example**: A user with `groups: ["admin", "engineering"]` can access pages tagged with either the `admin` or `engineering` groups.

---

# CI checks

> Automate broken link checks, linting, and grammar validation in CI/CD.

[Pro and Custom plans](https://mintlify.com/pricing?ref=docs-ci) include CI checks for GitHub repositories. Use CI checks to lint your docs for errors and provide warnings before you deploy. Mintlify CI checks run on pull requests against a configured deployment branch.

## ​Installation

 To begin, follow the steps on the [GitHub](https://mintlify.com/docs/deploy/github) page. Only access to the repository where your documentation content exists is required, so it is highly recommended to only grant access to that repository.

## ​Configuration

 Configure the CI checks enabled for a deployment by navigating to the [Add-ons](https://dashboard.mintlify.com/products/addons) page of your dashboard. Enable the checks that you want to run. When enabling checks, you can choose to run them at a `Warning` or `Blocking` level.

- A `Warning` level check will never provide a failure status, even if there is an error or suggestions.
- A `Blocking` level check will provide a failure status if there is an error or suggestions.

## ​Available CI checks

### ​Broken links

 Similar to how the [CLI link checker](https://mintlify.com/docs/installation#find-broken-links) works on your local machine, the
broken link CI check automatically searches your documentation content for broken internal links. To see the results of this check, visit GitHub’s check results page for a specific commit.

### ​Vale

 [Vale](https://vale.sh/) is an open source rule-based prose linter which supports a range of document types, including Markdown and MDX. Use Vale to check for consistency of style and tone in your documentation. Mintlify supports automatically running Vale in a CI check and displaying the results as a check status.

#### ​Configuration

 If you have a `.vale.ini` file in the root content directory of your deployment, the Vale CI check uses that configuration file and any configuration files in your specified `stylesPath`. If you don’t have a Vale config file, the default configuration automatically loads. Default vale.ini configuration

```
# Top level styles
StylesPath = /app/styles
MinAlertLevel = suggestion
# Inline HTML tags to ignore (code/tt for code snippets, img/url for links/images, a for anchor tags)
IgnoredScopes = code, tt, img, url, a
SkippedScopes = script, style, pre, figure

# Vocabularies
Vocab = Mintlify

# Packages
Packages = MDX

# Only match MDX
[*.mdx]
BasedOnStyles = Vale
Vale.Terms = NO # Enforces really harsh capitalization rules, keep off

# Ignore JSX/MDX-specific syntax patterns
# `import ...`, `export ...`
# `<Component ... />`
# `<Component>...</Component>`
# `{ ... }`
TokenIgnores = (?sm)((?:import|export) .+?$), \
(?<!`)(<\w+ ?.+ ?\/>)(?!`), \
(<[A-Z]\w+>.+?<\/[A-Z]\w+>)

# Exclude multiline JSX and curly braces
# `<Component \n ... />`
BlockIgnores = (?sm)^(<\w+\n .*\s\/>)$, \
(?sm)^({.+.*})
```

 The default Vale vocabulary includes the following words. Default Vale vocabulary

```
Mintlify
mintlify
VSCode
openapi
OpenAPI
Github
APIs

repo
npm
dev

Lorem
ipsum
impsum
amet

const
myName
myObject
bearerAuth
favicon
topbar
url
borderRadius
args
modeToggle
ModeToggle
isHidden
autoplay

_italic_
Strikethrough
Blockquotes
Blockquote
Singleline
Multiline

onboarding

async
await
boolean
enum
func
impl
init
instanceof
typeof
params
stdin
stdout
stderr
stdout
stdin
var
const
let
null
undefined
struct
bool

cors
csrf
env
xhr
xhr2
jwt
oauth
websocket
localhost
middleware
runtime
webhook
stdin
stdout

json
yaml
yml
md
txt
tsx
jsx
css
scss
html
png
jpg
svg

cdn
cli
css
dom
dto
env
git
gui
http
https
ide
jvm
mvc
orm
rpc
sdk
sql
ssh
ssl
tcp
tls
uri
url
ux
ui

nodejs
npm
yarn
pnpm
eslint
pytest
golang
rustc
kubectl
mongo
postgres
redis

JavaScript
TypeScript
Python
Ruby
Rust
Go
Golang
Java
Kotlin
Swift
Node.js
NodeJS
Deno

React
Vue
Angular
Next.js
Nuxt
Express
Django
Flask
Spring
Laravel
Redux
Vuex
TensorFlow
PostgreSQL
MongoDB
Redis
PNPM

Docker
Kubernetes
AWS
Azure
GCP
Terraform
Jenkins
CircleCI
GitLab
Heroku

Git
git
GitHub
GitLab
Bitbucket
VSCode
Visual Studio Code
IntelliJ
WebStorm
ESLint
eslint
Prettier
prettier
Webpack
webpack
Vite
vite
Babel
babel
Jest
jest
Mocha
Cypress
Postman

HTTP
HTTPS
OAuth
JWT
GraphQL
REST
WebSocket
TCP/IP

NPM
Yarn
PNPM
Pip
PIP
Cargo
RubyGems

Swagger
OpenAPI
Markdown
MDX
Storybook
TypeDoc
JSDoc

MySQL
PostgreSQL
MongoDB
Redis
Elasticsearch
DynamoDB

Linux
Unix
macOS
iOS

Firefox
Chromium
WebKit

config
ctx
desc
dir
elem
err
len
msg
num
obj
prev
proc
ptr
req
res
str
tmp
val
vars

todo
href
lang
nav
prev
next
toc
```

 To add your own vocabulary for the default configuration, create a `styles/config/vocabularies/Mintlify` directory with `accept.txt` and `reject.txt` files.

- `accept.txt`: Words that should be ignored by the Vale linter. For example, product names or uncommon terms.
- `reject.txt`: Words that should be flagged as errors. For example, jargon or words that are not appropriate for the tone of your documentation.

 Example Vale file structure

```
/your-project
  |- docs.json
  |- .vale.ini
  |- styles/
    |- config/
      |- vocabularies/
        |- Mintlify/
          |- accept.txt
          |- reject.txt
  |- example-page.mdx
```

 Example monorepo Vale file structure

```
/your-monorepo
  |- main.ts
  |- docs/
    |- docs.json
    |- .vale.ini
    |- styles/
      |- config/
      |- vocabularies/
        |- Mintlify/
          |- accept.txt
          |- reject.txt
    |- example-page.mdx
  |- test/
```

 For security reasons, absolute `stylesPath`, or `stylesPath` which include `..` values aren’t supported.Use relative paths and include the `stylesPath` in your repository.

#### ​Packages

 Vale supports a range of [packages](https://vale.sh/docs/keys/packages), which can be used to check for spelling and style errors. Any packages you include in your repository under the correct `stylesPath` are automatically installed and used in your Vale configuration. For packages not included in your repository, you may specify any packages from the [Vale package registry](https://vale.sh/explorer), and they’re automatically downloaded and used in your Vale configuration. For security reasons, automatically downloading packages that aren’t from the [Vale package registry](https://vale.sh/explorer) is **not** supported.

#### ​Vale withMDX

 MDX native support requires Vale 3.10.0 or later. Check your Vale version with `vale --version`. To use Vale’s in-document comments in MDX files, use MDX-style comments `{/* ... */}`:

```
{/* vale off */}

This text is ignored by Vale

{/* vale on */}
```

 Vale automatically recognizes and respects these comments in MDX files without additional configuration. Use comments to skip lines or sections that should be ignored by the linter.

---

# Cloudflare

> Host documentation at a subpath on Cloudflare Workers.

To host your documentation at a subpath such as `yoursite.com/docs` using Cloudflare, you must create and configure a Cloudflare Worker. Before you begin, you need a Cloudflare account and a domain name (can be managed on or off Cloudflare).

## ​Set up a Cloudflare Worker

 Create a Cloudflare Worker by following the [Cloudflare Workers getting started guide](https://developers.cloudflare.com/workers/get-started/dashboard/), if you have not already. If your DNS provider is Cloudflare, disable proxying for the CNAME record to avoid potential configuration issues.

### ​Proxies with Vercel deployments

 If you use Cloudflare as a proxy with Vercel deployments, you must ensure proper configuration to avoid conflicts with Vercel’s domain verification and SSL certificate provisioning. Improper proxy configuration can prevent Vercel from provisioning Let’s Encrypt SSL certificates and cause domain verification failures.

#### ​Required path allowlist

 Your Cloudflare Worker must allow traffic to these specific paths without blocking or redirecting:

- `/.well-known/acme-challenge/*` - Required for Let’s Encrypt certificate verification
- `/.well-known/vercel/*` - Required for Vercel domain verification

 While Cloudflare automatically handles many verification rules, creating additional custom rules may inadvertently block this critical traffic.

#### ​Header forwarding requirements

 Ensure that the `HOST` header is correctly forwarded in your Worker configuration. Failure to properly forward headers will cause verification requests to fail.

### ​Configure routing

 In your Cloudflare dashboard, select **Edit Code** and add the following script into your Worker’s code. See the [Cloudflare documentation](https://developers.cloudflare.com/workers-ai/get-started/dashboard/#development) for more information on editing a Worker. Replace `[SUBDOMAIN]` with your unique subdomain, `[YOUR_DOMAIN]` with your website’s base URL, and `/docs` with your desired subpath if different.

```
addEventListener("fetch", (event) => {
  event.respondWith(handleRequest(event.request));
});

async function handleRequest(request) {
  try {
    const urlObject = new URL(request.url);

    // If the request is to a Vercel verification path, allow it to pass through
    if (urlObject.pathname.startsWith('/.well-known/')) {
      return await fetch(request);
    }

    // If the request is to the docs subpath
    if (/^\/docs/.test(urlObject.pathname)) {
      // Then Proxy to Mintlify
      const DOCS_URL = "[SUBDOMAIN].mintlify.dev";
      const CUSTOM_URL = "[YOUR_DOMAIN]";

      let url = new URL(request.url);
      url.hostname = DOCS_URL;

      let proxyRequest = new Request(url, request);

      proxyRequest.headers.set("Host", DOCS_URL);
      proxyRequest.headers.set("X-Forwarded-Host", CUSTOM_URL);
      proxyRequest.headers.set("X-Forwarded-Proto", "https");
      // If deploying to Vercel, preserve client IP
      proxyRequest.headers.set("CF-Connecting-IP", request.headers.get("CF-Connecting-IP"));

      return await fetch(proxyRequest);
    }
  } catch (error) {
    // If no action found, play the regular request
    return await fetch(request);
  }
}
```

 Select **Deploy** and wait for the changes to propagate. After configuring your DNS, custom subdomains are usually available within a few minutes. DNS propagation can sometimes take 1-4 hours, and in rare cases up to 48 hours. If your subdomain is not immediately available, please wait before troubleshooting.

### ​Test your Worker

 After your code deploys, test your Worker to ensure it routes to your Mintlify docs.

1. Test using the Worker’s preview URL: `your-worker.your-subdomain.workers.dev/docs`
2. Verify the Worker routes to your Mintlify docs and your website.

### ​Add custom domain

1. In your [Cloudflare dashboard](https://dash.cloudflare.com/), navigate to your Worker.
2. Go to **Settings > Domains & Routes > Add > Custom Domain**.
3. Add your domain.

 We recommend you add your domain both with and without `www.` prepended. See [Add a custom domain](https://developers.cloudflare.com/workers/configuration/routing/custom-domains/#add-a-custom-domain) in the Cloudflare documentation for more information.

### ​Resolve DNS conflicts

 If your domain already points to another service, you must remove the existing DNS record. Your Cloudflare Worker must be configured to control all traffic for your domain.

1. Delete the existing DNS record for your domain. See [Delete DNS records](https://developers.cloudflare.com/dns/manage-dns-records/how-to/create-dns-records/#delete-dns-records) in the Cloudflare documentation for more information.
2. Return to your Worker and add your custom domain.

## ​Webflow custom routing

 If you use Webflow to host your main site and want to serve Mintlify docs at `/docs` on the same domain, you’ll need to configure custom routing through Cloudflare Workers to proxy all non-docs traffic to your main site. Make sure your main site is set up on a landing page before deploying this Worker, or visitors to your main site will see errors.

1. In Webflow, set up a landing page for your main site like `landing.yoursite.com`. This will be the page that visitors see when they visit your site.
2. Deploy your main site to the landing page. This ensures that your main site remains accessible while you configure the Worker.
3. To avoid conflicts, update any absolute URLs in your main site to be relative.
4. In Cloudflare, select **Edit Code** and add the following script into your Worker’s code.

  Replace `[SUBDOMAIN]` with your unique subdomain, `[YOUR_DOMAIN]` with your website’s base URL, `[LANDING_DOMAIN]` with your landing page URL, and `/docs` with your desired subpath if different.

```
addEventListener("fetch", (event) => {
event.respondWith(handleRequest(event.request));
});
async function handleRequest(request) {
try {
  const urlObject = new URL(request.url);

  // If the request is to a Vercel verification path, allow it to pass through
  if (urlObject.pathname.startsWith('/.well-known/')) {
    return await fetch(request);
  }

  // If the request is to the docs subpath
  if (/^\/docs/.test(urlObject.pathname)) {
    // Proxy to Mintlify
    const DOCS_URL = "[SUBDOMAIN].mintlify.dev";
    const CUSTOM_URL = "[YOUR_DOMAIN]";
    let url = new URL(request.url);
    url.hostname = DOCS_URL;
    let proxyRequest = new Request(url, request);
    proxyRequest.headers.set("Host", DOCS_URL);
    proxyRequest.headers.set("X-Forwarded-Host", CUSTOM_URL);
    proxyRequest.headers.set("X-Forwarded-Proto", "https");
    // If deploying to Vercel, preserve client IP
    proxyRequest.headers.set("CF-Connecting-IP", request.headers.get("CF-Connecting-IP"));
    return await fetch(proxyRequest);
  }
  // Route everything else to main site
  const MAIN_SITE_URL = "[LANDING_DOMAIN]";
  if (MAIN_SITE_URL && MAIN_SITE_URL !== "[LANDING_DOMAIN]") {
    let mainSiteUrl = new URL(request.url);
    mainSiteUrl.hostname = MAIN_SITE_URL;
    return await fetch(mainSiteUrl, {
      method: request.method,
      headers: request.headers,
      body: request.body
    });
  }
} catch (error) {
  // If no action found, serve the regular request
  return await fetch(request);
}
}
```

1. Select **Deploy** and wait for the changes to propagate.

 After configuring your DNS, custom subdomains are usually available within a few minutes. DNS propagation can sometimes take 1-4 hours, and in rare cases up to 48 hours. If your subdomain is not immediately available, please wait before troubleshooting.

---

# Content Security Policy (CSP) configuration

> Configure CSP headers to allow Mintlify resources while maintaining security for reverse proxies, firewalls, and networks that enforce strict security policies.

Configure CSP headers to allow Mintlify resources while maintaining security for reverse proxies, firewalls, and networks that enforce strict security policies.

---

# Deployments

> Manage deployments, view history, and monitor status.

Your documentation site automatically deploys when you push changes to your connected repository. This requires the Mintlify GitHub app to be properly installed and connected. If your latest changes are not appearing on your live site, first check that the GitHub account or organization that owns your docs repository has the GitHub App installed. See [GitHub troubleshooting](https://mintlify.com/docs/deploy/github#troubleshooting) for more information. If you have the GitHub App installed, but changes are still not deploying, manually trigger a deployment from your dashboard.

## ​Manually trigger a deployment

 1

Verify your latest commit was successful.

Check that your latest commit appears in your docs repository and did not encounter any errors.2

Manually trigger a deployment.

Go to your [dashboard](https://dashboard.mintlify.com) and select the deploy button.![The manual update button emphasized with an orange rectangle.](https://mintcdn.com/mintlify/GiucHIlvP3i5L17o/images/deployments/manual-update-light.png?fit=max&auto=format&n=GiucHIlvP3i5L17o&q=85&s=23715eadbebd74b3bfa5b5c197479e51)![The manual update button emphasized with an orange rectangle.](https://mintcdn.com/mintlify/GiucHIlvP3i5L17o/images/deployments/manual-update-dark.png?fit=max&auto=format&n=GiucHIlvP3i5L17o&q=85&s=0e7abcfbc9fdadbcf12a781a45d6a938)

## ​Delete a deployment

 You can permanently delete a deployment from the [Danger zone](https://dashboard.mintlify.com/settings/organization/danger-zone) in your dashboard settings. This action is irreversible and removes all deployment data, including any associated preview deployments. 1

Navigate to the Danger zone.

Go to the [Danger zone](https://dashboard.mintlify.com/settings/organization/danger-zone) in the settings page of your dashboard.2

Delete the deployment.

1. In the **Delete my deployment** section, provide a reason for deletion.
2. Click the delete button and confirm that you want to delete the deployment.

 Deleting a deployment is permanent and cannot be undone. If you have an active subscription, you’ll receive a prorated credit for any unused time remaining in your billing period. If you have multiple deployments, you’ll be redirected to another deployment after deletion. If you delete your only deployment, you’ll be redirected to the Mintlify homepage. When you delete a deployment, the organization admin receives an email notification confirming the deletion.

---

# Overview

> Host your documentation at the /docs subpath on your domain.

Host your documentation at a subpath like `your-domain.com/docs` to keep your docs on your main domain, which makes them easier to find and maintains a cohesive brand experience for your users.

## ​Set up by hosting provider

 Setting up a `/docs` subpath varies depending on your hosting provider. Choose your hosting provider and follow the setup instructions.

- [Cloudflare](https://mintlify.com/docs/deploy/cloudflare): Set up Cloudflare Workers for your domain to serve your documentation at the `/docs` subpath.
- [AWS Route 53 and CloudFront](https://mintlify.com/docs/deploy/route53-cloudfront): Deploy your documentation at the `/docs` subpath using AWS with Route 53 DNS and CloudFront CDN.
- [Vercel](https://mintlify.com/docs/deploy/vercel#host-from-docs) - Use rewrites to deploy your documentation at the `/docs` subpath.
- [Custom reverse proxy](https://mintlify.com/docs/deploy/reverse-proxy) - For other hosting platforms, set up a reverse proxy to deploy your documentation at the `/docs` subpath.

### ​Additional configuration for strict security policies

 If you proxy all traffic on your custom domain, you may need to configure your proxy or firewall rules to add the correct [headers](https://mintlify.com/docs/deploy/csp-configuration) so your documentation displays properly.

---

# GitHub Enterprise Server

> Set up the GitHub App on your GitHub Enterprise Server installation.

This guide walks you through setting up the Mintlify GitHub App on your GitHub Enterprise Server (GHES) installation. To connect a GHES instance to Mintlify, you must create a local version of our app within your self-hosted environment that communicates with our remote server. If you use a cloud-hosted GitHub instance, see the [GitHub](https://mintlify.com/docs/deploy/github) page for setup instructions.

## ​Prerequisites

- Admin privileges on your GitHub Enterprise Server organization where you want to install the app
- Access to your organization’s repositories where you want to install the app
- Network connectivity to communicate with our external services (see [Network requirements](#network-requirements) section below)

### ​Network requirements

#### ​Outbound connectivity

 Your GitHub Enterprise Server must be able to reach:

- Mintlify’s API endpoints ([https://leaves.mintlify.com](https://leaves.mintlify.com))
- Webhook receivers (port 443)

#### ​Firewall configuration

 The following outbound connections must be allowed:

- Connections from Mintlify’s static IP: `54.242.90.151`
- HTTPS (port 443) to Mintlify’s service domains
- DNS resolution for Mintlify’s service domains

## ​Step 1: Register the GitHub App

 See [Registering a GitHub App](https://docs.github.com/en/enterprise-server@3.18/apps/creating-github-apps/registering-a-github-app/registering-a-github-app) in the GitHub documentation for detailed instructions. 1

Navigate to your organization settings

1. In the upper-right corner of any page on GitHub, click your profile picture.
  2.Click **Your organizations**.
2. Click **Settings** next to the organization that you want to create the app for.

2

Create a new GitHub App

1. In the left sidebar, click **Developer settings**.
2. Click **GitHub Apps**.
3. Click **New GitHub App**.

3

Configure basic app information

Set the following:

- **GitHub App name:** `Mintlify`
- **Description:** `Integration with Mintlify services`
- **Homepage URL:** `https://mintlify.com`
- **User authorization callback URL:** `https://your-github-server.com/` (replace with your actual GHES domain)

## ​Step 2: Configure app permissions

 1

Set repository permissions

Set the following permissions for the app. No Organization, Account, or Enterprise permissions are required:

- **Checks:** Read and write
- **Contents:** Read and write
- **Deployments:** Read and write
- **Metadata:** Read-only
- **Pull Requests:** Read and write

2

Subscribe to Events

Select the following webhook events:

- Installation
- Installation Target
- Create
- Delete
- Public
- Pull Request
- Push
- Repository

## ​Step 3: Generate and secure credentials

 1

Create the app

Click **Create GitHub App**.You’ll be redirected to the app’s settings page.2

Generate private key

1. Scroll down to the **Private keys** section.
2. Click **Generate a private key**.
3. Download the `.pem` file and securely store it.

3

Note app credentials

Record the following:

- **App ID** (visible at the top of the settings page)
- **Client ID** (in the “About” section)
- **Client Secret** (generate and record it securely)

## ​Step 4: Install the app

 1

Navigate to app installation

1. From the app settings page, click **Install App** in the left sidebar.
2. Select your organization from the list.

2

Choose installation scope

Select either:

- **All repositories** (for organization-wide access)
- **Only select repositories** (choose specific repositories)

We reccomend selecting “Only select repositories” and limiting the app to only the repositories where your documentation is located.3

Complete the installation

1. Click **Install**.
2. Record the installation ID from the URL. For example, in `https://your-github-server.com/settings/installations/12345`, the string `12345` is the installation ID.

## ​Step 5: Configure webhook URL

 1

Return to app settings

1. Go back to your app’s settings page.
2. Scroll to the **Webhook** section.

2

Set webhook URL

Configure the following:

- **Webhook URL:** `https://leaves.mintlify.com/github-enterprise/:subdomain` (replace `:subdomain` with the URL that we provide you with)
- **Webhook secret:** Generate a random string (32+ characters) and record it securely. Mintlify can also generate this and provide it to you.

## ​Share credentials with us

 Please share the following information with our team using your secure information transfer method of choice.

### ​Required credentials

- GitHub Enterprise Server base URL: [https://your-github-server.com](https://your-github-server.com)
- App ID: (from step 3)
- App client ID: (from step 3)
- App client secret: (from step 3)
- Installation ID: (from step 4)
- Private key: The entire contents of the `.pem` file (should be shared via secure file transfer)
- Webhook secret: (from step 5)

### ​Optional credentials for troubleshooting

- Organization name: Your GitHub organization name
- Repository names: Specific repositories where the app is installed
- GitHub Enterprise Server version: Found in your site admin dashboard

## ​Mintlify connection

 We take the credentials you provide us and store them, encrypted, in a secure location. Then we work with you to either:

- Integrate your GHES environment with an existing Mintlify deployment.
- Integrate your GHES environment with a new Mintlify deployment that we provision for you.

 After your GHES environment is integrated with a Mintlify deployment, you are ready to enable webhooks for your GitHub App. The webhook URL may change based on our configuration. We test the integration and provide you with the new URL.

## ​Test the integration

 1

Verify webhook delivery

1. Go to your GitHub App settings.
2. Click the **Advanced** tab.
3. Check “Recent Deliveries” for successful webhook deliveries.
4. Look for HTTP 200 responses.

2

Test repository access

1. Create a test issue or pull request in an installed repository.
2. Verify that Mintlify responds appropriately.

## ​FAQ and Troubleshooting

The app installation is failing with permission errors.

Ensure you have:

- Site admin privileges for app creation
- Organization owner or admin rights for app installation.
- Proper repository permissions if installing on specific repositories.

Webhooks aren't being delivered

- Verify the webhook URL is correct and accessible.
- Ensure your firewall allows outbound HTTPS connections.
- Check the webhook secret matches what was configured.
- Review webhook delivery logs in the “Advanced” tab of your GitHub App settings.

I'm getting SSL/TLS certificate errors

Your GHES might use self-signed certificates. Our services cannot verify your server’s certificate.**Solution:** Ensure your GHES has a valid SSL certificate.

The app installs, but doesn't respond to events.

- Ensure webhooks are being delivered and acknowledged by our server with response code 200.
- Required permissions were granted during installation.

Can I limit which repositories the app accesses?

Yes, during installation you can select “Only select repositories” and choose specific ones. You can modify this later in your organization’s installed apps settings. This is the recommended form of installation.

How do I update app permissions later?

- Go to the app settings as a site admin.
- Modify permissions as needed.
- The app will need to be re-approved by organization owners.
- Notify us of any permission changes as they may affect functionality.

Our GHES is behind a corporate firewall, nginx proxy, or similar setup.

You must:

- Whitelist our service domains in your firewall.
- Ensure outbound HTTPS (port 443) connectivity.
- If direct internet access is not allowed, set up a proxy.

Can this work with GHES in air-gapped environments?

No, your GHES must be able to communicate with our cloud-hosted server.

Who should I contact if I need help?

Please reach out to your customer success representative who you’ve spoken to at Mintlify, or our support team at [support@mintlify.com](mailto:support@mintlify.com) with:

- Your GitHub Enterprise Server version.
- Specific error messages.
- Screenshots of any issues.
- Network/firewall configuration details (if relevant).

---

# GitHub

> Connect to a GitHub repository for automated deployments, pull request previews, and continuous synchronization.

Connect to a GitHub repository for automated deployments, pull request previews, and continuous synchronization.

---

# GitLab

> Connect to a GitLab repository for automated deployments and preview builds.

We use access tokens and webhooks to authenticate and sync changes between GitLab and Mintlify.

- Mintlify uses access tokens to pull information from GitLab.
- GitLab uses webhooks to notify Mintlify when changes are made, enabling preview deployments for merge requests.

## ​Set up the connection

 **HTTPS cloning required**: Your GitLab project must have HTTPS cloning enabled for Mintlify to access your repository. You can verify this in GitLab by going to your project’s **Settings** > **General** > **Visibility and access controls** section. 1

Find your project ID

In your GitLab project, navigate to **Settings** > **General** and locate your **Project ID**.![The General Settings page in the GitLab dashboard. The Project ID is highlighted.](https://mintcdn.com/mintlify/GiucHIlvP3i5L17o/images/gitlab/gitlab-project-id.png?fit=max&auto=format&n=GiucHIlvP3i5L17o&q=85&s=4aae3ff6adbb509b607a63a4998992d0)2

Generate an access token

Navigate to **Settings** > **Access Tokens** and select **Add new token**.Configure the token with these settings:

- **Name**: Mintlify
- **Role**: Maintainer (required for private repos)
- **Scopes**: `api` and `read_api`

Click **Create project access token** and copy the token.If Project Access Tokens are not available, you can use a Personal Access Token instead. Note that Personal Access Tokens expire and must be updated.![The Access tokens page in the GitLab dashboard. The settings to configure for Mintlify are highlighted.](https://mintcdn.com/mintlify/GiucHIlvP3i5L17o/images/gitlab/gitlab-project-access-token.png?fit=max&auto=format&n=GiucHIlvP3i5L17o&q=85&s=59ef23c54d88cdd723632086bced658b)3

Set up the connection

In the [Mintlify dashboard](https://dashboard.mintlify.com/settings/deployment/git-settings):

1. Enter your project ID and access token.
2. Complete any other required configurations.
3. Click **Save Changes**.

![The Git Settings page in the Mintlify dashboard. The GitLab configuration settings are highlighted.](https://mintcdn.com/mintlify/GiucHIlvP3i5L17o/images/gitlab/gitlab-config.png?fit=max&auto=format&n=GiucHIlvP3i5L17o&q=85&s=882adfd7c2a3349608bc6240aa5b467d)

## ​Create the webhook

 Webhooks allow us to receive events when changes are made so that we can
automatically trigger deployments. 1

Navigate to Settings > Webhooks and click 'Add new Webhook'

![Screenshot of the Webhooks page in the GitLab dashboard.](https://mintcdn.com/mintlify/GiucHIlvP3i5L17o/images/gitlab/gitlab-webhook.png?fit=max&auto=format&n=GiucHIlvP3i5L17o&q=85&s=760e8faa2437ecf8ff2739c4dfa0bdc4)2

Set up URL and webhook

In the “URL” field, enter the endpoint `https://leaves.mintlify.com/gitlab-webhook` and name the webhook “Mintlify”.3

Paste token

Paste the Webhook token generated after setting up the connection.![Screenshot of the GitLab connection in the Mintlify dashboard. The Show Webtoken button is highlighted.](https://mintcdn.com/mintlify/GiucHIlvP3i5L17o/images/gitlab/gitlab-show-webtoken.png?fit=max&auto=format&n=GiucHIlvP3i5L17o&q=85&s=60c68dd86fa476e90af8cec2e5ee7c81)4

Select events

Select these events to trigger the webhook:

- **Push events** (All branches)
- **Merge requests events**

When you’re done it should look like this:![The Webhook page in the GitLab dashboard. The settings to configure for Mintlify are highlighted.](https://mintcdn.com/mintlify/GiucHIlvP3i5L17o/images/gitlab/gitlab-project-webtoken.png?fit=max&auto=format&n=GiucHIlvP3i5L17o&q=85&s=00c0ce70ce9e8dbc2712f71aaeef3362)5

Test the Webhook

After creating the Webhook, click the “Test” dropdown and select “Push events” to send a sample payload to ensure it’s configured correctly. It’ll say “Hook executed successfully: HTTP 200” if configured correctly.This will help you verify that everything is working correctly and that your documentation will sync properly with your GitLab repository.![Screenshot of the GitLab Webhooks page. The 'Push events' menu item is highlighted in the 'Test' menu.](https://mintcdn.com/mintlify/GiucHIlvP3i5L17o/images/gitlab/gitlab-project-webtoken-test.png?fit=max&auto=format&n=GiucHIlvP3i5L17o&q=85&s=3ad52f7ac39124a4c03944256d0b79d3)

---

# Monorepo setup

> Configure documentation path and content directory for monorepo projects.

Configure Mintlify to deploy documentation from a specific directory within a monorepo. This setup allows you to maintain documentation alongside your code in repositories that contain multiple projects or services.

## ​Prerequisites

- Admin access to your Mintlify project.
- Documentation files organized in a dedicated directory within your monorepo.
- A valid `docs.json` in your documentation directory.

## ​Configure monorepo deployment

 1

Access Git settings

Navigate to [Git Settings](https://dashboard.mintlify.com/settings/deployment/git-settings) in your dashboard.![The project settings panel in the Git Settings menu. The Set up as monorepo toggle button is enabled and a path to the /docs directory is specified.](https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/monorepo-light.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=796f90a80651694cb858c77f4f1145a8)![The project settings panel in the Git Settings menu. The Set up as monorepo toggle button is enabled and a path to the /docs directory is specified.](https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/monorepo-dark.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=03624a6ce64b3c3d504e27585cf857aa)2

Set your documentation path

1. Select the **Set up as monorepo** toggle button.
2. Enter the relative path to your docs directory. For example, if your docs are in the `docs` directory, enter `/docs`.

Do not include a trailing slash in the path.

1. Select **Save changes**.
