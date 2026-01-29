# Preview deployments and more

# Preview deployments

> Get unique preview URLs for pull requests to review changes before merging.

Preview deployments are available on [Pro and Custom plans](https://mintlify.com/pricing?ref=preview-deployments). Preview deployments let you see how changes to your docs will look before merging to production. Each preview creates a shareable URL that updates automatically as you push new changes. Preview URLs are publicly viewable by default. Share a preview link with anyone who needs to review your changes.

## ​Create preview deployments

 Preview deployments are created automatically through pull requests or manually from your dashboard.

### ​Automatic previews

 Automatic previews are only created for pull requests targeting your [deployment branch](https://mintlify.com/docs/guides/git-concepts#deployment-branch). When you create a pull request, the Mintlify bot automatically adds a link to view the preview deployment in your pull request. The preview updates each time you push new commits to the branch. ![Link to view deployment in the pull request timeline](https://mintcdn.com/mintlify/f7fo9pnTEtzBD70_/images/previews/preview-deployment-light.png?fit=max&auto=format&n=f7fo9pnTEtzBD70_&q=85&s=4cbf574001b521afbd8c9f6717ed907f)![Link to view deployment in the pull request timeline](https://mintcdn.com/mintlify/f7fo9pnTEtzBD70_/images/previews/preview-deployment-dark.png?fit=max&auto=format&n=f7fo9pnTEtzBD70_&q=85&s=9fbb5054761316d1bbb8168646ed51bf)

### ​Manual previews

 You can manually create a preview for any branch.

1. Go to your [dashboard](https://dashboard.mintlify.com/).
2. Select **Previews**.
3. Select **Create custom preview**.
4. Enter the name of the branch you want to preview.
5. Select **Create deployment**.

## ​Redeploy a preview

 Redeploy a preview to refresh content or retry after a failed deployment.

1. Select the preview from your [dashboard](https://dashboard.mintlify.com/).
2. Select **Redeploy**.

 ![The Previews menu with the deploy button emphasized by an orange rectangle.](https://mintcdn.com/mintlify/f7fo9pnTEtzBD70_/images/previews/redeploy-preview-light.png?fit=max&auto=format&n=f7fo9pnTEtzBD70_&q=85&s=eaa1711b0c580931036f1d1f4685312e)![The Previews menu with the deploy button emphasized by an orange rectangle.](https://mintcdn.com/mintlify/f7fo9pnTEtzBD70_/images/previews/redeploy-preview-dark.png?fit=max&auto=format&n=f7fo9pnTEtzBD70_&q=85&s=086e0340522fc6a620e47e3e35703ae2)

## ​Preview widget

 The preview widget appears on preview deployments to help you navigate and review updated pages. The widget is a floating button in the bottom-right corner of your preview deployment. ![Preview widget expanded to show list of changed files.](https://mintcdn.com/mintlify/AjqaLQO45zsoo98J/images/previews/widget-light.png?fit=max&auto=format&n=AjqaLQO45zsoo98J&q=85&s=c6928d2ead75217426f1cc703fef5271)![Preview widget expanded to show list of changed files.](https://mintcdn.com/mintlify/AjqaLQO45zsoo98J/images/previews/widget-dark.png?fit=max&auto=format&n=AjqaLQO45zsoo98J&q=85&s=cdeb39bd833e56e69563ff226a106708)

1. Click the widget to show all added, modified, or removed files in the preview.
2. Click a file to view the changes on the corresponding page.
3. Use the search bar to filter the list of changed files.

 The widget only appears on preview deployments, not on your live site or local previews.

## ​Restrict access to preview deployments

 By default, preview deployments are publicly accessible to anyone with the URL. You can restrict access to authenticated members of your Mintlify organization.

1. Navigate to the **Previews** section in the [Add-ons](https://dashboard.mintlify.com/products/addons) page of your dashboard.
2. Click the **Preview authentication** toggle to enable or disable preview authentication.

 ![The preview authentication toggle in the Add-ons page](https://mintcdn.com/mintlify/JpjPdD_YybFKEYPk/images/previews/preview-auth-light.png?fit=max&auto=format&n=JpjPdD_YybFKEYPk&q=85&s=efbbd50e1a18d29953f17fb8a9d7138b)![The preview authentication toggle in the Add-ons page](https://mintcdn.com/mintlify/JpjPdD_YybFKEYPk/images/previews/preview-auth-dark.png?fit=max&auto=format&n=JpjPdD_YybFKEYPk&q=85&s=b5d877ae3918afcd852a8047eab98233)

## ​Troubleshooting preview deployments

 If your preview deployment fails, try these troubleshooting steps.

- **View the build logs**: In your [dashboard](https://dashboard.mintlify.com/), go to **Previews** and click the failed preview. The deployment logs show errors that caused failures.
- **Check your configuration**:
  - Invalid `docs.json` syntax
  - Missing or incorrect file paths referenced in your navigation
  - Invalid frontmatter in MDX files
  - Broken image links or missing image files
- **Validate locally**: Run `mint dev` locally to catch build errors before pushing to the repository.
- **Check recent changes**: Review the most recent commits in your branch to identify what changes caused the build to fail.

---

# Reverse proxy

> Configure a custom reverse proxy to serve your documentation.

Reverse proxy configurations are only supported for [Custom plans](https://mintlify.com/pricing?ref=reverse-proxy). To serve your documentation through a custom reverse proxy, you must configure routing rules, caching policies, and header forwarding. When you implement a reverse proxy, monitor for potential issues with domain verification, SSL certificate provisioning, authentication flows, performance, and analytics tracking.

## ​Routing configuration

 Proxy these paths to your Mintlify subdomain with the specified caching policies:

| Path | Destination | Caching |
| --- | --- | --- |
| /.well-known/acme-challenge/* | <your-subdomain>.mintlify.app | No cache |
| /.well-known/vercel/* | <your-subdomain>.mintlify.app | No cache |
| /.well-known/skills/* | <your-subdomain>.mintlify.app | No cache |
| /skill.md | <your-subdomain>.mintlify.app | No cache |
| /mintlify-assets/_next/static/* | <your-subdomain>.mintlify.app | Cache enabled |
| /_mintlify/* | <your-subdomain>.mintlify.app | No cache |
| /* | <your-subdomain>.mintlify.app | No cache |
| / | <your-subdomain>.mintlify.app | No cache |

## ​Required header configuration

 Configure your reverse proxy with these header requirements:

- **Origin**: Contains the target subdomain `<your-subdomain>.mintlify.app`
- **X-Forwarded-For**: Preserves client IP information
- **X-Forwarded-Proto**: Preserves original protocol (HTTP/HTTPS)
- **X-Real-IP**: Forwards the real client IP address
- **User-Agent**: Forwards the user agent

 Ensure that the `Host` header is not forwarded

## ​Example nginx configuration

```
server {
    listen 80;
    server_name <your-domain>.com;

    # Let's Encrypt verification paths
    location ~ ^/\.well-known/acme-challenge/ {
        proxy_pass https://<your-subdomain>.mintlify.app;
        proxy_set_header Origin <your-subdomain>.mintlify.app;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header User-Agent $http_user_agent;

        # Disable caching for verification paths
        add_header Cache-Control "no-cache, no-store, must-revalidate";
    }

    # Vercel verification paths
    location ~ ^/\.well-known/vercel/ {
        proxy_pass https://<your-subdomain>.mintlify.app;
        proxy_set_header Origin <your-subdomain>.mintlify.app;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header User-Agent $http_user_agent;

        # Disable caching for verification paths
        add_header Cache-Control "no-cache, no-store, must-revalidate";
    }

    # AI skills paths
    location ^~ /.well-known/skills/ {
        proxy_pass https://<your-subdomain>.mintlify.app;
        proxy_set_header Origin <your-subdomain>.mintlify.app;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header User-Agent $http_user_agent;

        # Disable caching for verification paths
        add_header Cache-Control "no-cache, no-store, must-revalidate";
    }

    # Skill manifest
    location = /skill.md {
        proxy_pass https://<your-subdomain>.mintlify.app;
        proxy_set_header Origin <your-subdomain>.mintlify.app;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header User-Agent $http_user_agent;

        # Disable caching for skill manifest
        add_header Cache-Control "no-cache, no-store, must-revalidate";
    }

    # Static assets with caching
    location ~ ^/mintlify-assets/_next/static/ {
        proxy_pass https://<your-subdomain>.mintlify.app;
        proxy_set_header Origin <your-subdomain>.mintlify.app;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header User-Agent $http_user_agent;

        # Enable caching for static assets
        add_header Cache-Control "public, max-age=86400";
    }

    # Mintlify-specific paths
    location ~ ^/_mintlify/ {
        proxy_pass https://<your-subdomain>.mintlify.app;
        proxy_set_header Origin <your-subdomain>.mintlify.app;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header User-Agent $http_user_agent;

        # Disable caching for Mintlify paths
        add_header Cache-Control "no-cache, no-store, must-revalidate";
    }

    # Root path
    location = / {
        proxy_pass https://<your-subdomain>.mintlify.app;
        proxy_set_header Origin <your-subdomain>.mintlify.app;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header User-Agent $http_user_agent;

        # Disable caching for dynamic content
        add_header Cache-Control "no-cache, no-store, must-revalidate";
    }

    # All other documentation paths
    location / {
        proxy_pass https://<your-subdomain>.mintlify.app;
        proxy_set_header Origin <your-subdomain>.mintlify.app;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header User-Agent $http_user_agent;

        # Disable caching for dynamic content
        add_header Cache-Control "no-cache, no-store, must-revalidate";
    }
}
```

## ​Troubleshooting

### ​404 error

 **Symptoms**: Documentation loads, but features don’t work. API calls fail. **Cause**: `Host` header is being forwarded or `Origin` header is missing. **Solution**:

- Remove `Host` header forwarding
- Set `Origin` header to `<your-subdomain>.mintlify.app`

### ​Performance issues

 **Symptoms**: Slow page loads and layout shifts. **Cause**: Incorrect caching configuration. **Solution**: Enable caching only for `/mintlify-assets/_next/static/*` paths.

---

# AWS Route 53 and CloudFront

> Deploy documentation at a subpath on AWS with Route 53 DNS and CloudFront CDN.

To host your documentation at a subpath such as `yoursite.com/docs` using AWS Route 53 and CloudFront, you must configure your DNS provider to point to your CloudFront distribution.

## ​Overview

 Route traffic to these paths with a Cache Policy of **CachingDisabled**:

- `/.well-known/acme-challenge/*` - Required for Let’s Encrypt certificate verification
- `/.well-known/vercel/*` - Required for domain verification
- `/docs/*` - Required for subpath routing
- `/docs/` - Required for subpath routing

 Route traffic to this path with a Cache Policy of **CachingEnabled**:

- `/mintlify-assets/_next/static/*`
- `Default (*)`	- Your websites landing page

 All Behaviors must have the an **origin request policy** of `AllViewerExceptHostHeader`. ![CloudFront "Behaviors" page with 4 behaviors: /docs/*, /docs, Default, and /.well-known/*.](https://mintcdn.com/mintlify/in3v2q9tGvWcAFWD/images/cloudfront/all-behaviors.png?fit=max&auto=format&n=in3v2q9tGvWcAFWD&q=85&s=666a7c785bcc7f6b2aa23424f8c1c668)

## ​Create CloudFront distribution

1. Navigate to [CloudFront](https://aws.amazon.com/cloudfront) inside the AWS console.
2. Select **Create distribution**.

 ![CloudFront Distributions page with the "Create distribution" button emphasized.](https://mintcdn.com/mintlify/WXXCCJWDplNJgTwZ/images/cloudfront/create-distribution.png?fit=max&auto=format&n=WXXCCJWDplNJgTwZ&q=85&s=cd402e36a077943e5de51319a2fba9c3)

1. For the Origin domain, input `[SUBDOMAIN].mintlify.dev` where `[SUBDOMAIN]` is your project’s unique subdomain.

 ![CloudFront "Create distribution" page showing "acme.mintlify.dev" as the origin domain.](https://mintcdn.com/mintlify/WXXCCJWDplNJgTwZ/images/cloudfront/origin-name.png?fit=max&auto=format&n=WXXCCJWDplNJgTwZ&q=85&s=3bccb966a96cba7ec83364dabf5ba788)

1. For “Web Application Firewall (WAF),” enable security protections.

 ![Web Application Firewall (WAF) options with "Enable security protections" selected.](https://mintcdn.com/mintlify/WXXCCJWDplNJgTwZ/images/cloudfront/enable-security-protections.png?fit=max&auto=format&n=WXXCCJWDplNJgTwZ&q=85&s=73a02de58bfbce884656443bb5d1ec42)

1. The remaining settings should be default.
2. Select **Create distribution**.

## ​Add default origin

1. After creating the distribution, navigate to the “Origins” tab.

 ![A CloudFront distribution with the "Origins" tab highlighted.](https://mintcdn.com/mintlify/GiucHIlvP3i5L17o/images/cloudfront/origins.png?fit=max&auto=format&n=GiucHIlvP3i5L17o&q=85&s=bbf7cd128d5fa29b2d957e224757d90c)

1. Find your staging URL that mirrors the main domain. This is highly variant depending on how your landing page is hosted. For example, the Mintlify staging URL is [mintlify-landing-page.vercel.app](https://mintlify-landing-page.vercel.app).

 If your landing page is hosted on Webflow, use Webflow’s staging URL. It would look like `.webflow.io`.If you use Vercel, use the `.vercel.app` domain available for every project.

1. Create a new Origin and add your staging URL as the “Origin domain.”

 ![CloudFront "Create origin" page with a "Origin domain" input field highlighted.](https://mintcdn.com/mintlify/WXXCCJWDplNJgTwZ/images/cloudfront/default-origin.png?fit=max&auto=format&n=WXXCCJWDplNJgTwZ&q=85&s=c67257bc20e907ea4da1a8719fae0543) By this point, you should have two Origins: one with `[SUBDOMAIN].mintlify.app` and another with your staging URL. ![CloudFront "Origins" page with two origins: One for mintlify and another for mintlify-landing-page.](https://mintcdn.com/mintlify/WXXCCJWDplNJgTwZ/images/cloudfront/final-origins.png?fit=max&auto=format&n=WXXCCJWDplNJgTwZ&q=85&s=c1fdd6d6e346e0e7b3a669daba284fba)

## ​Set behaviors

 Behaviors in CloudFront enable control over the subpath logic. At a high level, we’re looking to create the following logic:

- **If a user lands on your custom subpath**, go to `[SUBDOMAIN].mintlify.dev`.
- **If a user lands on any other page**, go the current landing page.

1. Navigate to the “Behaviors” tab of your CloudFront distribution.

 ![CloudFront "Behaviors" tab highlighted.](https://mintcdn.com/mintlify/WXXCCJWDplNJgTwZ/images/cloudfront/behaviors.png?fit=max&auto=format&n=WXXCCJWDplNJgTwZ&q=85&s=6ab02a43a5427d2d1306dfd6d313bc49)

1. Select the **Create behavior** button and create the following behaviors.

### ​/.well-known/*

 Create behaviors for Vercel domain verification paths with a **Path pattern** of `/.well-known/*` and set **Origin and origin groups** to your docs URL. For “Cache policy,” select **CachingDisabled** to ensure these verification requests pass through without caching. ![CloudFront "Create behavior" page with a "Path pattern" of "/.well-known/*" and "Origin and origin groups" pointing to the staging URL.](https://mintcdn.com/mintlify/GiucHIlvP3i5L17o/images/cloudfront/well-known-policy.png?fit=max&auto=format&n=GiucHIlvP3i5L17o&q=85&s=374fd2e53349cc9796515cda82a9b165) If `.well-known/*` is too generic, it can be narrowed down to 2 behaviors at a minimum for Vercel:

- `/.well-known/vercel/*` - Required for Vercel domain verification
- `/.well-known/acme-challenge/*` - Required for Let’s Encrypt certificate verification

### ​Your subpath

 Create a behavior with a **Path pattern** of your chosen subpath, for example `/docs`, with **Origin and origin groups** pointing to the `.mintlify.dev` URL (in our case `acme.mintlify.dev`).

- Set “Cache policy” to **CachingOptimized**.
- Set “Origin request policy” to **AllViewerExceptHostHeader**.
- Set Viewer Protocol Policy to **Redirect HTTP to HTTPS**

 ![CloudFront "Create behavior" page with a "Path pattern" of "/docs/*" and "Origin and origin groups" pointing to the acme.mintlify.dev URL.](https://mintcdn.com/mintlify/in3v2q9tGvWcAFWD/images/cloudfront/behavior-1.png?fit=max&auto=format&n=in3v2q9tGvWcAFWD&q=85&s=0ce9e6db0d16c0c095abf1bc44e68833)

### ​Your subpath with wildcard

 Create a behavior with a **Path pattern** of your chosen subpath followed by `/*`, for example `/docs/*`, and **Origin and origin groups** pointing to the same `.mintlify.dev` URL. These settings should exactly match your base subpath behavior. With the exception of the **Path pattern**.

- Set “Cache policy” to **CachingOptimized**.
- Set “Origin request policy” to **AllViewerExceptHostHeader**.
- Set “Viewer protocol policy” to **Redirect HTTP to HTTPS**

### ​/mintlify-assets/_next/static/*

- Set “Cache policy” to **CachingOptimized**
- Set “Origin request policy” to **AllViewerExceptHostHeader**
- Set “Viewer protocol policy” to **Redirect HTTP to HTTPS**

### ​Default (*)

 Lastly, we’re going to edit the `Default (*)` behavior. ![A CloudFront distribution with the "Default (*)" behavior selected and the Edit button emphasized.](https://mintcdn.com/mintlify/WXXCCJWDplNJgTwZ/images/cloudfront/default-behavior-1.png?fit=max&auto=format&n=WXXCCJWDplNJgTwZ&q=85&s=d1404011b4a312d88c7e523bbcf94316)

1. Change the default behavior’s **Origin and origin groups** to the staging URL (in our case `mintlify-landing-page.vercel.app`).

 ![CloudFront "Edit behavior" page with the "Origin and origin groups" input field highlighted.](https://mintcdn.com/mintlify/WXXCCJWDplNJgTwZ/images/cloudfront/default-behavior-2.png?fit=max&auto=format&n=WXXCCJWDplNJgTwZ&q=85&s=3c81d60889bc1157954524865a0bde14)

1. Select **Save changes**.

### ​Check behaviors are set up correctly

 If you follow the above steps, your behaviors should look like this: ![CloudFront "Behaviors" page with 4 behaviors: /docs/*, /docs, Default, and /.well-known/*.](https://mintcdn.com/mintlify/in3v2q9tGvWcAFWD/images/cloudfront/all-behaviors.png?fit=max&auto=format&n=in3v2q9tGvWcAFWD&q=85&s=666a7c785bcc7f6b2aa23424f8c1c668)

## ​Preview distribution

 You can now test if your distribution is set up properly by going to the “General” tab and visiting the **Distribution domain name** URL. ![CloudFront "General" tab with the "Distribution domain name" URL highlighted.](https://mintcdn.com/mintlify/GiucHIlvP3i5L17o/images/cloudfront/preview-distribution.png?fit=max&auto=format&n=GiucHIlvP3i5L17o&q=85&s=b7f0582640bb6650054c7b40ee9bdd57) All pages should be directing to your main landing page, but if you append your chosen subpath, for example `/docs`, to the URL, you should see it going to your Mintlify documentation instance.

## ​Connect with Route53

 Now, we’re going to bring the functionality of the CloudFront distribution into your primary domain. For this section, you can also refer to AWS’s official guide on [Configuring
Amazon Route 53 to route traffic to a CloudFront
distribution](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-to-cloudfront-distribution.html#routing-to-cloudfront-distribution-config)

1. Navigate to [Route53](https://aws.amazon.com/route53) inside the AWS console.
2. Navigate to the “Hosted zone” for your primary domain.
3. Select **Create record**.

 ![Route 53 "Records" page with the "Create record" button emphasized.](https://mintcdn.com/mintlify/GiucHIlvP3i5L17o/images/cloudfront/route53-create-record.png?fit=max&auto=format&n=GiucHIlvP3i5L17o&q=85&s=27a00457e2401c2d55262291dda15579)

1. Toggle `Alias` and then **Route traffic to** the `Alias to CloudFront distribution` option.

 ![Route 53 "Create record" page with the "Alias" toggle and the "Route traffic to" menu highlighted.](https://mintcdn.com/mintlify/WXXCCJWDplNJgTwZ/images/cloudfront/create-record-alias.png?fit=max&auto=format&n=WXXCCJWDplNJgTwZ&q=85&s=cb7dbe0320f3f73233ed6452ac3b0372)

1. Select **Create records**.

 You may need to remove the existing A record if one currently exists. Your documentation is now live at your chosen subpath for your primary domain. After configuring your DNS, custom subdomains are usually available within a few minutes. DNS propagation can sometimes take 1-4 hours, and in rare cases up to 48 hours. If your subdomain is not immediately available, please wait before troubleshooting.

---

# External proxies with Vercel

> Configure external proxies in front of your Vercel deployment.

If you have an external proxy like Cloudflare or AWS CloudFront in front of your Vercel deployment, you must configure it properly to avoid conflicts with Vercel’s domain verification and SSL certificate provisioning. Improper proxy configuration can prevent Vercel from provisioning Let’s Encrypt SSL certificates and cause domain verification failures. See the [supported providers](https://vercel.com/guides/how-to-setup-verified-proxy#supported-providers-verified-proxy-lite) in the Vercel documentation.

## ​Required path allowlist

 Your external proxy must allow traffic to these specific paths without blocking, redirecting, or heavily caching:

- `/.well-known/acme-challenge/*` - Required for Let’s Encrypt certificate verification
- `/.well-known/vercel/*` - Required for Vercel domain verification
- `/mintlify-assets/_next/static/*` - Required for static assets

 These paths should pass through directly to your Vercel deployment without modification.

## ​Header forwarding requirements

 Ensure that your proxy correctly forwards the `HOST` header. Without proper header forwarding, verification requests will fail.

## ​Testing your proxy setup

 To verify your proxy is correctly configured:

1. Test that `https://[yourdomain].com/.well-known/vercel/` returns a response.
2. Ensure SSL certificates are provisioning correctly in your Vercel dashboard.
3. Check that domain verification completes successfully.

---

# Vercel

> Deploy documentation to a subpath on Vercel.

Configure your `vercel.json` file to proxy requests from your main domain to your documentation at a subpath.

## ​vercel.json file

 The `vercel.json` file configures how your project builds and deploys. It sits in your project’s root directory and controls various aspects of your deployment, including routing, redirects, headers, and build settings. We use the `rewrites` configuration in your `vercel.json` file to proxy requests from your main domain to your documentation. Rewrites map incoming requests to different destinations without changing the URL in the browser. When someone visits `yoursite.com/docs`, Vercel internally fetches content from `your-subdomain.mintlify.dev/docs`, but the user still sees `yoursite.com/docs` in their browser. This is different from redirects, which send users to another URL entirely.

## ​Configuration

### ​Host at/docssubpath

1. Navigate to [Custom domain setup](https://dashboard.mintlify.com/settings/deployment/custom-domain) in your dashboard.
2. Click the **Host at/docs** toggle to the on position. ![Screenshot of the Custom domain setup page. The Host at `/docs` toggle is on and highlighted by an orange rectangle.](https://mintcdn.com/mintlify/y0I2fgo5Rzv873ju/images/subpath/toggle-light.png?fit=max&auto=format&n=y0I2fgo5Rzv873ju&q=85&s=7e32943b9dd517e21030678381a60b40)![Screenshot of the Custom domain setup page. The Host at `/docs` toggle is on and highlighted by an orange rectangle.](https://mintcdn.com/mintlify/y0I2fgo5Rzv873ju/images/subpath/toggle-dark.png?fit=max&auto=format&n=y0I2fgo5Rzv873ju&q=85&s=9e0fd7047a7937d5a6d9cfc2c55acb09)
3. Enter your domain.
4. Select **Add domain**.
5. Add the following rewrites to your `vercel.json` file. Replace `[subdomain]` with your subdomain, which is found at the end of your dashboard URL. For example, `dashboard.mintlify.com/your-organization/your-subdomain` has a domain identifier of `your-subdomain`.
  ```
  {
    "rewrites": [
      {
        "source": "/docs",
        "destination": "https://[subdomain].mintlify.dev/docs"
      },
      {
        "source": "/docs/:match*",
        "destination": "https://[subdomain].mintlify.dev/docs/:match*"
      }
    ]
  }
  ```

 The `rewrites` configuration maps the `/docs` subpath on your domain to the `/docs` subpath on your documentation.

- **source**: The path pattern on your domain that triggers the rewrite.
- **destination**: Where the request should be proxied to.
- **:match***: A wildcard that captures any path segments after your subpath.

 For more information, see [Configuring projects with vercel.json: Rewrites](https://vercel.com/docs/projects/project-configuration#rewrites) in the Vercel documentation.

### ​Host at custom subpath

 To use a custom subpath (any path other than `/docs`), you must organize your documentation files within your repository to match your subpath structure. For example, if your documentation is hosted at `yoursite.com/help`, your documentation files must be in a `help/` directory. Use the generator below to create your rewrites configuration. Add the rewrites to your `vercel.json` file. SubdomainSubpath

```
{
  "rewrites": [
    {
      "source": "/_mintlify/:path*",
      "destination": "https://[SUBDOMAIN].mintlify.app/_mintlify/:path*"
    },
    {
      "source": "/api/request",
      "destination": "https://[SUBDOMAIN].mintlify.app/_mintlify/api/request"
    },
    {
      "source": "/[SUBPATH]",
      "destination": "https://[SUBDOMAIN].mintlify.app/[SUBPATH]"
    },
    {
      "source": "/[SUBPATH]/llms.txt",
      "destination": "https://[SUBDOMAIN].mintlify.app/llms.txt"
    },
    {
      "source": "/[SUBPATH]/llms-full.txt",
      "destination": "https://[SUBDOMAIN].mintlify.app/llms-full.txt"
    },
    {
      "source": "/[SUBPATH]/sitemap.xml",
      "destination": "https://[SUBDOMAIN].mintlify.app/sitemap.xml"
    },
    {
      "source": "/[SUBPATH]/robots.txt",
      "destination": "https://[SUBDOMAIN].mintlify.app/robots.txt"
    },
    {
      "source": "/[SUBPATH]/mcp",
      "destination": "https://[SUBDOMAIN].mintlify.app/mcp"
    },
    {
      "source": "/[SUBPATH]/:path*",
      "destination": "https://[SUBDOMAIN].mintlify.app/[SUBPATH]/:path*"
    },
    {
      "source": "/mintlify-assets/:path+",
      "destination": "https://[SUBDOMAIN].mintlify.app/mintlify-assets/:path+"
    }
  ]
}
```
