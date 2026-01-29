# Gandi and more

# Gandi

> Verify your domain on Gandi with Resend.

## ​Add Domain to Resend

 First, log in to your [Resend Account](https://resend.com/login) and [add a domain](https://resend.com/domains). ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-add-domain.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=418dd93c2f2ead0b0d83d1b7c2fb0970) It is [best practice to use a
subdomain](https://resend.com/docs/knowledge-base/is-it-better-to-send-emails-from-a-subdomain-or-the-root-domain)
(updates.example.com) instead of the root domain (example.com). Using a
subdomain allows for proper reputation segmentation based on topics or purpose
(e.g. marketing) and is especially important if receiving emails with Resend.

## ​Log in to Gandi

 Log in to your [Gandi account](https://admin.gandi.net/domain/):

1. Choose your Domain from the `Domain` list.
2. Select the `DNS Records` tab to get to the page to manage DNS records.

 ![Domain Details](https://mintcdn.com/resend/ABWmVTZIHGIFNTFD/images/dashboard-domains-gandi-domains.png?fit=max&auto=format&n=ABWmVTZIHGIFNTFD&q=85&s=db72a28a42a006e10ca7617fc004ecb5)

## ​Add MX SPF Record

 Select “Add record” on Gandi to copy and paste the values MX from Resend.

1. On the `Type` page, choose `MX`.
2. Use the default TTL of `10800`.
3. Type `send` for the `Name` of the record.
4. Use the default `Priority` of `10`.
5. Copy the MX Value from Resend into the `Hostname` field.
6. Select `Create`.

 Gandi requires your MX record to have a trailing period when adding. Resend
will include the trailing period when copying. Removing the period will cause
the verification to fail. ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-spf-mx.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=bb0db2dd2809135194cfb62b695225cd) ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-gandi-spf-mx.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=41f5e1b53f159b7e8e05f4f1ffa7e5ad) Below is a mapping of the record fields from Resend to Gandi:

| Gandi | Resend | Example Value |
| --- | --- | --- |
| Type | Type | MX Record |
| Name | Name | send |
| Hostname | Value | feedback-smtp.us-east-1.amazonses.com. |
| TTL | - | 10800 |
| Priority | Priority | 10 |

 Do not use the same priority for multiple records. If Priority `10` is already
in use on another record, try a higher value `20` or `30`.

## ​Add TXT SPF Record

 In the same section, select “Add record” again.

1. On the `Type` page, choose `TXT`.
2. Use the default TTL of `10800`.
3. Type `send` for the `Name` of the record.
4. Copy the TXT Value Resend into the `Text value` field.
5. Select `Create`.

 Omit your domain from the record values in Resend when you paste. Instead of
`send.example.com`, paste only `send` (or `send.subdomain` if you’re using a
subdomain). ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-spf-txt.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=747425d0a224baeee2846c9a707d5bbc) ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-gandi-spf-txt.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=7f75828142bfae8186b3f577d379c910) Below is a mapping of the record fields from Resend to Gandi:

| Gandi | Resend | Example Value |
| --- | --- | --- |
| Type | Type | TXT Record |
| Name | Name | send |
| Text value | Value | "v=spf1 include:amazonses.com ~all" |
| TTL | - | 10800 |

## ​Add TXT DKIM Records

 In the same section, select “Add record” again.

1. On the `Type` page, choose `TXT`.
2. Use the default TTL of `10800`.
3. Type `resend._domainkey` for the `Host name` of the record.
4. Copy the record value from Resend into the `TXT value` field.
5. Select `Create`.

 Omit your domain from the record values in Resend when you paste. Instead of
`resend._domainkey.example.com`, paste only `resend._domainkey` (or
`resend._domainkey.subdomain` if you’re using a subdomain). ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-dkim.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=345d1dc6b7c138dbd92bd6928c634bd9) ![Domain Details](https://mintcdn.com/resend/ABWmVTZIHGIFNTFD/images/dashboard-domains-gandi-dkim-txt.png?fit=max&auto=format&n=ABWmVTZIHGIFNTFD&q=85&s=097889c1a13da8b1634cddadfe294887) Below is a mapping of the record fields from Resend to Gandi:

| Gandi | Resend | Example Value |
| --- | --- | --- |
| Type | Type | TXT Record |
| Name | Name | send |
| Text value | Value | p=example_demain_key_value |
| TTL | - | 1 hour |

## ​Receiving Emails

 If you want to receive emails at your domain, toggle the “Receiving” switch on the domain details page. ![Enable Receiving Emails for a verified domain](https://mintcdn.com/resend/B7wTVm7aKL5pNT-6/images/inbound-domain-toggle.png?fit=max&auto=format&n=B7wTVm7aKL5pNT-6&q=85&s=46f6b4c142fb90e04b57861e338ed2d0) When you enable Inbound on a domain, Resend receives *all emails* sent to that
specific domain depending on the priority of the MX record. For this reason,
we strongly recommend verifying a subdomain (`subdomain.example.com`) instead
of the root domain (`example.com`). Learn more about [avoiding conflicts with
your existing MX
records](https://resend.com/docs/knowledge-base/how-do-i-avoid-conflicting-with-my-mx-records). Select “Add record” on Gandi:

1. On the `Type` page, choose `MX`.
2. Use the default TTL of `10800`.
3. Type `inbound` (or whatever your subdomain is) for the `Name` of the record.
4. Use the default `Priority` of `10`.
5. Copy the MX Value from Resend into the `Hostname` field.
6. Select `Create`.

 Below is a mapping of the record fields from Resend to Gandi:

| Gandi | Resend | Example Value |
| --- | --- | --- |
| Type | Type | MX Record |
| Name | Name | inbound |
| Hostname | Content | inbound-smtp.us-east-1.amazonaws.com. |
| TTL | - | 10800 |
| Priority | Priority | 10 |

 After verifying your domain, create a webhook to process incoming emails. For help setting up a webhook, how to access email data and attachments, forward emails, and more, see [our guide on receiving emails with Resend](https://resend.com/docs/dashboard/receiving/introduction).

## ​Complete Verification

 Now click [Verify DNS Records](https://resend.com/domains) on your Domain in Resend. It may take a few hours to complete the verification process (often much faster).

## ​Troubleshooting

 If your domain is not successfully verified, these are some common troubleshooting methods.

Resend shows my domain verification failed.

Review the records you added to Gandi to rule out copy and paste errors.

It has been longer than 72 hours and my domain is still Pending.

[Review our guide on a domain not verifying](https://resend.com/docs/knowledge-base/what-if-my-domain-is-not-verifying).

---

# Get Started with Resend and Supabase

> A quick jumpstart to using Resend with Supabase.

In this guide, we’ll help you get started with Resend by:

- [Setting up Resend](#set-up-resend)
- [Send Auth Emails with Resend](#send-auth-emails-with-resend)
- [Send Emails with Supabase Edge Functions](#send-emails-with-supabase-edge-functions)

## ​Set up Resend

 In order to send emails with your Supabase project, you’ll need to first verify it in Resend. Go to [the Domains page](https://resend.com/domains) and click on **Add Domain**.

1. Add your domain name (we recommend [using a subdomain](https://resend.com/docs/knowledge-base/is-it-better-to-send-emails-from-a-subdomain-or-the-root-domain) like `updates.yourdomain.com`).
2. Add the DNS records to your DNS provider ([learn more about these records](https://resend.com/docs/dashboard/domains/introduction)).  ![Resend Domains page](https://mintcdn.com/resend/_kGPo-rF0-rO9nI4/images/resend-domain-records.png?fit=max&auto=format&n=_kGPo-rF0-rO9nI4&q=85&s=24107151c9a59db661aca80c64338bfe)
3. Click on **I’ve added the records** to begin the verification process.
4. Wait for the verification to complete (usually takes 5–10 minutes)

 Resend requires you own your domain (i.e., not a shared or public domain).
Adding DNS records gives Resend the authority to send emails on your behalf
and signals to the inbox providers that you’re a legitimate sender.

## ​Send Auth Emails with Resend

 If you want to use Resend to send your Supabase Auth Emails, you have three options:

1. [Using the Resend Integration](#1-using-the-resend-integration): simplest, but less customizable email templates.
2. [Custom Auth Functions](#2-custom-auth-functions): more customizable email templates, but requires more setup.
3. [Self-hosted with Custom SMTP](#3-self-hosted-with-custom-smtp): only for those self-hosting Supabase.

### ​1. Using the Resend Integration

 Resend includes a pre-built integration with Supabase. Connecting Resend as your email provider will allow you to send your Supabase emails (i.e., password resets, email confirmations, etc.) through Resend.

1. Open the [Resend Integrations settings](https://resend.com/settings/integrations).
2. Click **Connect to Supabase** and login to your Supabase account if prompted.  ![Resend Integrations settings](https://mintcdn.com/resend/_kGPo-rF0-rO9nI4/images/resend-integrations-settings.png?fit=max&auto=format&n=_kGPo-rF0-rO9nI4&q=85&s=b954067bfb28d84f7d8201e05a449815)
3. Select a project and click **Select Project**, then select your domain and click **Add API Key**. Resend will create an API key for you. Add a sender name and click **Configure SMTP Integration**.  ![Resend Integrations settings](https://mintcdn.com/resend/_kGPo-rF0-rO9nI4/images/resend-supabase-setup-smtp.png?fit=max&auto=format&n=_kGPo-rF0-rO9nI4&q=85&s=e744247952bc105d6083babcc315b0a6)

 Click on **Supabase Dashboard** to confirm the integration. ![Resend Integrations settings](https://mintcdn.com/resend/_kGPo-rF0-rO9nI4/images/resend-supabase-setup-confirm.png?fit=max&auto=format&n=_kGPo-rF0-rO9nI4&q=85&s=d72c13ba50f60530587107b6d7040223) Supabase has a rate limit on the number of emails you can send per hour and
requires you to [connect a custom email provider for more than 2
emails/hour](https://supabase.com/docs/guides/auth/rate-limits). Once you set
Resend as your email provider, you can send additional emails (by default, 25
emails/hour, although you can change the rate limit in your project’s
[authentication
settings](https://supabase.com/docs/guides/deployment/going-into-prod#rate-limiting-resource-allocation--abuse-prevention)).

### ​2. Custom Auth Functions

 Benefit of using custom auth functions:

- More control over the email sending process since you control the sending function.
- More control over the email template using React Email or Resend Templates.

 Note that this requires enabling [Supabase Auth Hooks](https://supabase.com/docs/guides/auth/auth-hooks).  [Supabase Auth Hooks with Resend TemplatesSee the full source code.](https://github.com/resend/supabase-auth-hooks-with-resend-templates)

### ​3. Self-hosted with Custom SMTP

 If you’re self-hosting Supabase, you can use a custom SMTP server to send your emails. [Learn more here](https://resend.com/docs/send-with-smtp).

## ​Send Emails with Supabase Edge Functions

 If you’re using Supabase Edge Functions, you can add email sending to your function by using the Resend Node.js SDK. You can use these functions for Auth Emails ([as shown above](#2-custom-auth-functions)) or for other emails (e.g., app notifications, account activity, etc.). First, make sure you have the latest version of the [Supabase CLI](https://supabase.com/docs/guides/cli#installation) installed.

### ​1. Create Supabase function

 Create a new function locally:

```
supabase functions new resend
```

### ​2. Edit the handler function

 Paste the following code into the `index.ts` file: index.ts

```
import { serve } from "https://deno.land/[email protected]/http/server.ts";

const RESEND_API_KEY = 're_xxxxxxxxx';

const handler = async (_request: Request): Promise<Response> => {
    const res = await fetch('https://api.resend.com/emails', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${RESEND_API_KEY}`
        },
        body: JSON.stringify({
            from: 'Acme <[email protected]>',
            to: ['[email protected]'],
            subject: 'hello world',
            html: '<strong>it works!</strong>',
        })
    });

    const data = await res.json();

    return new Response(JSON.stringify(data), {
        status: 200,
        headers: {
            'Content-Type': 'application/json',
        },
    });
};

serve(handler);
```

### ​3. Deploy and send email

 Run function locally:

```
supabase functions start
supabase functions serve resend --no-verify-jwt
```

 Deploy function to Supabase:

```
supabase functions deploy resend
```

 Open the endpoint URL to send an email: ![Supabase Edge Functions - Deploy Function](https://mintcdn.com/resend/OWNnQaVDyqcGyhhN/images/supabase-edge-functions-deploy-function.png?fit=max&auto=format&n=OWNnQaVDyqcGyhhN&q=85&s=e28cab375d10a57f712e77ff3c888005)

### ​4. Try it yourself

 [Supabase Edge Functions ExampleSee the full source code.](https://github.com/resend/resend-supabase-edge-functions-example)

## ​Happy sending!

 If you have any questions, please let us know at [[email protected]](https://resend.com/cdn-cgi/l/email-protection#a9dadcd9d9c6dbdde9dbccdaccc7cd87cac6c4).

---

# GoDaddy

> Verify your domain on GoDaddy with Resend.

Prefer watching a video? Check out our video walkthrough below.

## ​Add Domain to Resend

 First, log in to your [Resend Account](https://resend.com/login) and [add a domain](https://resend.com/domains). ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-add-domain.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=418dd93c2f2ead0b0d83d1b7c2fb0970) It is [best practice to use a
subdomain](https://resend.com/docs/knowledge-base/is-it-better-to-send-emails-from-a-subdomain-or-the-root-domain)
(updates.example.com) instead of the root domain (example.com). Using a
subdomain allows for proper reputation segmentation based on topics or purpose
(e.g. marketing) and is especially important if receiving emails with Resend.

## ​Log in to GoDaddy

 Log in to your [GoDaddy account](https://sso.godaddy.com):

1. Select `DNS` from the left navigation
2. Find your domain in the list and select the domain
3. This will take you to the DNS management page for the domain

 ![Domain Details](https://mintcdn.com/resend/lQ2IedTbqKrTHWy8/images/dashboard-domains-godaddy-manage.png?fit=max&auto=format&n=lQ2IedTbqKrTHWy8&q=85&s=544f608675414a8e562ee15665a9b102)

## ​Add MX SPF Record

 Copy and paste the values MX in Resend to GoDaddy.

1. Click `Add New Record` to create a new record
2. Set the Type to `MX`.
3. Type `send` for the `Name` of the record.
4. Copy the MX Value from Resend into the `Value` field.
5. Add `10` for the `Priority`.
6. Set the TTL to `600` (or use the default).
7. Click `Save`.

 Omit your domain from the record values in Resend when you paste. Instead of
`send.example.com`, paste only `send` (or `send.subdomain` if you’re using a
subdomain). ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-spf-mx.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=bb0db2dd2809135194cfb62b695225cd) ![Domain Details](https://mintcdn.com/resend/lQ2IedTbqKrTHWy8/images/dashboard-domains-godaddy-spf-mx.png?fit=max&auto=format&n=lQ2IedTbqKrTHWy8&q=85&s=22442a78539dc70a959a152a396e8508) Below is a mapping of the record fields from Resend to GoDaddy:

| GoDaddy | Resend | Example Value |
| --- | --- | --- |
| Type | Type | MX Record |
| Name | Name | send |
| Value | Value | feedback-smtp.us-east-1.amazonses.com |
| TTL | - | 600(or use default) |
| Priority | Priority | 10 |

 Do not use the same priority for multiple records. If Priority `10` is already
in use on another record, try a higher value `20` or `30`.

## ​Add TXT SPF Record

 In the same section, add another record in GoDaddy.

1. Click `Add New Record` to create a new record
2. Set the Type to `TXT`.
3. Type `send` for the `Name` of the record.
4. Copy the TXT Value from Resend into the `Value` field.
5. Set the TTL to `600` (or use the default).
6. Click `Save`.

 Omit your domain from the record values in Resend when you paste. Instead of
`send.example.com`, paste only `send` (or `send.subdomain` if you’re using a
subdomain). ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-spf-txt.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=747425d0a224baeee2846c9a707d5bbc) ![Domain Details](https://mintcdn.com/resend/lQ2IedTbqKrTHWy8/images/dashboard-domains-godaddy-spf-txt.png?fit=max&auto=format&n=lQ2IedTbqKrTHWy8&q=85&s=849bd76a0e5c14daa2f727ed2f284036) Below is a mapping of the record fields from Resend to GoDaddy:

| GoDaddy | Resend | Example Value |
| --- | --- | --- |
| Type | Type | TXT Record |
| Name | Name | send |
| Value | Value | "v=spf1 include:amazonses.com ~all" |
| TTL | - | 600(or use default) |

## ​Add TXT DKIM Records

 In the same section, add another record in GoDaddy.

1. Click `Add New Record` to create a new record
2. Set the Type to `TXT`.
3. Type `resend._domainkey` for the `Name` of the record.
4. Copy the record value from Resend into the `Value` field.
5. Set the TTL to `600` (or use the default).
6. Click `Save`.

 Omit your domain from the record values in Resend when you paste. Instead of
`resend._domainkey.example.com`, paste only `resend._domainkey` (or
`resend._domainkey.subdomain` if you’re using a subdomain). ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-dkim.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=345d1dc6b7c138dbd92bd6928c634bd9) ![Domain Details](https://mintcdn.com/resend/lQ2IedTbqKrTHWy8/images/dashboard-domains-godaddy-dkim-txt.png?fit=max&auto=format&n=lQ2IedTbqKrTHWy8&q=85&s=2df8ab88c72f0944f8071121e95295aa) Below is a mapping of the record fields from Resend to GoDaddy:

| GoDaddy | Resend | Example Value |
| --- | --- | --- |
| Type | Type | TXT Record |
| Name | Name | resend._domainkey |
| Value | Value | p=example_demain_key_value |
| TTL | - | 600(or use default) |

## ​Receiving Emails

 If you want to receive emails at your domain, toggle the “Receiving” switch on the domain details page. ![Enable Receiving Emails for a verified domain](https://mintcdn.com/resend/B7wTVm7aKL5pNT-6/images/inbound-domain-toggle.png?fit=max&auto=format&n=B7wTVm7aKL5pNT-6&q=85&s=46f6b4c142fb90e04b57861e338ed2d0) When you enable Inbound on a domain, Resend receives *all emails* sent to that
specific domain depending on the priority of the MX record. For this reason,
we strongly recommend verifying a subdomain (`subdomain.example.com`) instead
of the root domain (`example.com`). Learn more about [avoiding conflicts with
your existing MX
records](https://resend.com/docs/knowledge-base/how-do-i-avoid-conflicting-with-my-mx-records). Click `Add New Record` to create a new record:

1. Set the Type to `MX`.
2. Type `inbound` (or whatever your subdomain is) for the `Name` of the record.
3. Copy the MX Value from Resend into the `Value` field.
4. Add `10` for the `Priority`.
5. Set the TTL to `600` (or use the default).
6. Click `Save`.

 Below is a mapping of the record fields from Resend to GoDaddy:

| GoDaddy | Resend | Example Value |
| --- | --- | --- |
| Type | Type | MX Record |
| Name | Name | inbound |
| Value | Content | inbound-smtp.us-east-1.amazonaws.com |
| TTL | - | 600(or use default) |
| Priority | Priority | 10 |

 After verifying your domain, create a webhook to process incoming emails. For help setting up a webhook, how to access email data and attachments, forward emails, and more, see [our guide on receiving emails with Resend](https://resend.com/docs/dashboard/receiving/introduction).

## ​Complete Verification

 Now click [Verify DNS Records](https://resend.com/domains) on your Domain in Resend. It may take a few hours to complete the verification process (often much faster).

## ​Troubleshooting

 If your domain is not successfully verified, these are some common troubleshooting methods.

Resend shows my domain verification failed.

Review the records you added to GoDaddy to rule out copy and paste errors.

It has been longer than 72 hours and my domain is still Pending.

[Review our guide on a domain not verifying](https://resend.com/docs/knowledge-base/what-if-my-domain-is-not-verifying).

---

# Hetzner

> Verify your domain on Hetzner with Resend.

## ​Add Domain to Resend

 First, log in to your [Resend Account](https://resend.com/login) and [add a domain](https://resend.com/domains). ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-add-domain.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=418dd93c2f2ead0b0d83d1b7c2fb0970) It is [best practice to use a
subdomain](https://resend.com/docs/knowledge-base/is-it-better-to-send-emails-from-a-subdomain-or-the-root-domain)
(updates.example.com) instead of the root domain (example.com). Using a
subdomain allows for proper reputation segmentation based on topics or purpose
(e.g. marketing) and is especially important if receiving emails with Resend.

## ​Log in to Hetzner

 Log in to your [Hetzner account](https://dns.hetzner.com):

1. Choose your Domain from the `Your Zones` list.
2. Select the `Records` tab to get to the page to manage DNS records.

 ![Domain Details](https://mintcdn.com/resend/ABWmVTZIHGIFNTFD/images/dashboard-domains-Hetzner-domains.png?fit=max&auto=format&n=ABWmVTZIHGIFNTFD&q=85&s=145c6cbd9d047e33dd8daad7b07bff8c)

## ​Add MX SPF Record

 In the `Create Record` section on Hetzner copy and paste the values MX from Resend:

1. On the `Type` page, choose `MX`.
2. Type `send` for the `Name` of the record.
3. Select the `Value` field.
4. Use the default `Priority` of `10`.
5. Copy the MX Value from Resend into the `Mail server` field.
6. Select the TTL of `1800`.
7. Select `Add Record`.

 Hetzner requires your MX record to have a trailing period when adding. Resend
will include the trailing period when copying. Removing the period will cause
the verification to fail. ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-spf-mx.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=bb0db2dd2809135194cfb62b695225cd) ![Domain Details](https://mintcdn.com/resend/ABWmVTZIHGIFNTFD/images/dashboard-domains-Hetzner-spf-mx.png?fit=max&auto=format&n=ABWmVTZIHGIFNTFD&q=85&s=db6f4da36c4e408a86c54ca3e42d6ea9) Below is a mapping of the record fields from Resend to Hetzner:

| Hetzner | Resend | Example Value |
| --- | --- | --- |
| Type | Type | MX Record |
| Name | Name | send |
| Mail server | Value | feedback-smtp.us-east-1.amazonses.com. |
| TTL | TTL | 1800 |
| Priority | Priority | 10 |

 Do not use the same priority for multiple records. If Priority `10` is already
in use on another record, try a higher value `20` or `30`.

## ​Add TXT SPF Record

 On the same `Create Record` section:

1. On the `Type` page, choose `TXT`.
2. Type `send` for the `Name` of the record.
3. Copy the TXT Value Resend into the `Value` field.
4. Select the TTL of `1800`.
5. Select `Add Record`.

 Omit your domain from the record values in Resend when you paste. Instead of
`send.example.com`, paste only `send` (or `send.subdomain` if you’re using a
subdomain). ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-spf-txt.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=747425d0a224baeee2846c9a707d5bbc) ![Domain Details](https://mintcdn.com/resend/ABWmVTZIHGIFNTFD/images/dashboard-domains-Hetzner-spf-txt.png?fit=max&auto=format&n=ABWmVTZIHGIFNTFD&q=85&s=89bce49d989f8a9006f8cf465202a2ca) Below is a mapping of the record fields from Resend to Hetzner:

| Hetzner | Resend | Example Value |
| --- | --- | --- |
| Type | Type | TXT Record |
| Name | Name | send |
| Value | Value | "v=spf1 include:amazonses.com ~all" |
| TTL | TTL | 10800 |

## ​Add TXT DKIM Records

 On the same `Create Record` section:

1. On the `Type` page, choose `TXT`.
2. Type `resend._domainkey` for the `Name` of the record.
3. Copy the TXT Value Resend into the `Value` field.
4. Select the TTL of `1800`.
5. Select `Add Record`.

 Omit your domain from the record values in Resend when you paste. Instead of
`resend._domainkey.example.com`, paste only `resend._domainkey` (or
`resend._domainkey.subdomain` if you’re using a subdomain). ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-dkim.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=345d1dc6b7c138dbd92bd6928c634bd9) ![Domain Details](https://mintcdn.com/resend/ABWmVTZIHGIFNTFD/images/dashboard-domains-Hetzner-dkim-txt.png?fit=max&auto=format&n=ABWmVTZIHGIFNTFD&q=85&s=3a29ae90720d7d9c31cc7cfa5892cd57) Below is a mapping of the record fields from Resend to Hetzner:

| Hetzner | Resend | Example Value |
| --- | --- | --- |
| Type | Type | TXT Record |
| Name | Name | send |
| Value | Value | p=example_demain_key_value |
| TTL | TTL | 1 hour |

## ​Receiving Emails

 If you want to receive emails at your domain, toggle the “Receiving” switch on the domain details page. ![Enable Receiving Emails for a verified domain](https://mintcdn.com/resend/B7wTVm7aKL5pNT-6/images/inbound-domain-toggle.png?fit=max&auto=format&n=B7wTVm7aKL5pNT-6&q=85&s=46f6b4c142fb90e04b57861e338ed2d0) When you enable Inbound on a domain, Resend receives *all emails* sent to that
specific domain depending on the priority of the MX record. For this reason,
we strongly recommend verifying a subdomain (`subdomain.example.com`) instead
of the root domain (`example.com`). Learn more about [avoiding conflicts with
your existing MX
records](https://resend.com/docs/knowledge-base/how-do-i-avoid-conflicting-with-my-mx-records). In the `Create Record` section on Hetzner:

1. On the `Type` page, choose `MX`.
2. Type `inbound` (or whatever your subdomain is) for the `Name` of the record.
3. Select the `Value` field.
4. Use the default `Priority` of `10`.
5. Copy the MX Value from Resend into the `Mail server` field.
6. Select the TTL of `1800`.
7. Select `Add Record`.

 Below is a mapping of the record fields from Resend to Hetzner:

| Hetzner | Resend | Example Value |
| --- | --- | --- |
| Type | Type | MX Record |
| Name | Name | inbound |
| Mail server | Content | inbound-smtp.us-east-1.amazonaws.com. |
| TTL | TTL | 1800 |
| Priority | Priority | 10 |

 After verifying your domain, create a webhook to process incoming emails. For help setting up a webhook, how to access email data and attachments, forward emails, and more, see [our guide on receiving emails with Resend](https://resend.com/docs/dashboard/receiving/introduction).

## ​Complete Verification

 Now click [Verify DNS Records](https://resend.com/domains) on your Domain in Resend. It may take a few hours to complete the verification process (often much faster).

## ​Troubleshooting

 If your domain is not successfully verified, these are some common troubleshooting methods.

Resend shows my domain verification failed.

Review the records you added to Hetzner to rule out copy and paste errors.

It has been longer than 72 hours and my domain is still Pending.

[Review our guide on a domain not verifying](https://resend.com/docs/knowledge-base/what-if-my-domain-is-not-verifying).

---

# Hostinger

> Verify your domain on Hostinger with Resend.

## ​Add Domain to Resend

 First, log in to your [Resend Account](https://resend.com/login) and [add a domain](https://resend.com/domains). ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-add-domain.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=418dd93c2f2ead0b0d83d1b7c2fb0970) It is [best practice to use a
subdomain](https://resend.com/docs/knowledge-base/is-it-better-to-send-emails-from-a-subdomain-or-the-root-domain)
(updates.example.com) instead of the root domain (example.com). Using a
subdomain allows for proper reputation segmentation based on topics or purpose
(e.g. marketing) and is especially important if receiving emails with Resend.

## ​Log in to Hostinger

 Log in to your [Hostinger account](https://auth.hostinger.com/login):

1. Select the `Domains` tab
2. Choose your Domain from the `Domain portfolio` list.
3. Select the `DNS / Nameservers` to get to the page to manage DNS records.

 ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-hostinger-domains.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=d7fcfa6f62bc4c8eb8c7eccbc12068c3)

## ​Add MX SPF Record

 Copy and paste the values MX in Resend to Hostinger.

1. Set the Type to `MX`.
2. Type `send` for the `Name` of the record.
3. Copy the MX Value from Resend into the `Mail Server` field.
4. Add `10` for the `Priority`.
5. Set the TTL to `3600`.
6. Select `Add Record`.

 Omit your domain from the record values in Resend when you paste. Instead of
`send.example.com`, paste only `send` (or `send.subdomain` if you’re using a
subdomain). ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-spf-mx.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=bb0db2dd2809135194cfb62b695225cd) ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-hostinger-spf-mx.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=d9600d2ba927c8ee8a3222139280d396) Below is a mapping of the record fields from Resend to Hostinger:

| Hostinger | Resend | Example Value |
| --- | --- | --- |
| Type | Type | MX Record |
| Name | Name | send |
| Mail Server | Value | feedback-smtp.us-east-1.amazonses.com |
| TTL | - | Set to 3660 |
| Priority | Priority | 10 |

 Do not use the same priority for multiple records. If Priority `10` is already
in use on another record, try a higher value `20` or `30`.

## ​Add TXT SPF Record

 In the same section, add another record in Hostinger.

1. Set the Type to `TXT`.
2. Type `send` for the `Name` of the record.
3. Copy the TXT Value Resend into the `TXT value` field.
4. Set the TTL to `3600`.
5. Select `Add Record`.

 Omit your domain from the record values in Resend when you paste. Instead of
`send.example.com`, paste only `send` (or `send.subdomain` if you’re using a
subdomain). ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-spf-txt.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=747425d0a224baeee2846c9a707d5bbc) ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-hostinger-spf-txt.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=8854129a0f11574f79016d5ad56a0ed2) Below is a mapping of the record fields from Resend to Hostinger:

| Hostinger | Resend | Example Value |
| --- | --- | --- |
| Type | Type | TXT Record |
| Name | Name | send |
| TXT value | Value | "v=spf1 include:amazonses.com ~all" |
| TTL | - | Set to 3600 |

## ​Add TXT DKIM Records

 In the same section, add another record in Hostinger.

1. Set the Type to `TXT`.
2. Type `resend._domainkey` for the `Name` of the record.
3. Copy the record value from Resend into the `TXT value` field.
4. Set the TTL to `3600`.
5. Select `Add Record`.

 Omit your domain from the record values in Resend when you paste. Instead of
`resend._domainkey.example.com`, paste only `resend._domainkey` (or
`resend._domainkey.subdomain` if you’re using a subdomain). ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-dkim.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=345d1dc6b7c138dbd92bd6928c634bd9) ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-hostinger-dkim-txt.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=31350bb523d1959c348a0fde5f8d5734) Below is a mapping of the record fields from Resend to Hostinger:

| Hostinger | Resend | Example Value |
| --- | --- | --- |
| Type | Type | TXT Record |
| Name | Name | send |
| TXT value | Value | p=example_demain_key_value |
| TTL | - | Set to 3600 |

## ​Receiving Emails

 If you want to receive emails at your domain, toggle the “Receiving” switch on the domain details page. ![Enable Receiving Emails for a verified domain](https://mintcdn.com/resend/B7wTVm7aKL5pNT-6/images/inbound-domain-toggle.png?fit=max&auto=format&n=B7wTVm7aKL5pNT-6&q=85&s=46f6b4c142fb90e04b57861e338ed2d0) When you enable Inbound on a domain, Resend receives *all emails* sent to that
specific domain depending on the priority of the MX record. For this reason,
we strongly recommend verifying a subdomain (`subdomain.example.com`) instead
of the root domain (`example.com`). Learn more about [avoiding conflicts with
your existing MX
records](https://resend.com/docs/knowledge-base/how-do-i-avoid-conflicting-with-my-mx-records). Copy and paste the values MX in Resend to Hostinger:

1. Set the Type to `MX`.
2. Type `inbound` (or whatever your subdomain is) for the `Name` of the record.
3. Copy the MX Value from Resend into the `Mail Server` field.
4. Add `10` for the `Priority`.
5. Set the TTL to `3600`.
6. Select `Add Record`.

 Below is a mapping of the record fields from Resend to Hostinger:

| Hostinger | Resend | Example Value |
| --- | --- | --- |
| Type | Type | MX Record |
| Name | Name | inbound |
| Mail Server | Content | inbound-smtp.us-east-1.amazonaws.com |
| TTL | - | Set to 3660 |
| Priority | Priority | 10 |

 After verifying your domain, create a webhook to process incoming emails. For help setting up a webhook, how to access email data and attachments, forward emails, and more, see [our guide on receiving emails with Resend](https://resend.com/docs/dashboard/receiving/introduction).

## ​Complete Verification

 Now click [Verify DNS Records](https://resend.com/domains) on your Domain in Resend. It may take a few hours to complete the verification process (often much faster).

## ​Troubleshooting

 If your domain is not successfully verified, these are some common troubleshooting methods.

Resend shows my domain verification failed.

Review the records you added to Hostinger to rule out copy and paste errors.

It has been longer than 72 hours and my domain is still Pending.

[Review our guide on a domain not verifying](https://resend.com/docs/knowledge-base/what-if-my-domain-is-not-verifying).

---

# How can I change my Resend email address?

> How to change the email address associated with your Resend account.

To change the email address associated with your Resend account:

1. Navigate to your [Profile](https://resend.com/profile) page.
2. Under **Your email**, enter your new email address in the **Email address** field.
3. Click the **Update email** button.

 After clicking **Update email**, you will be signed out and two confirmation emails will be sent:

- **To your new email address**: An email with the subject “Confirm email change for Resend” asking you to confirm the update.
- **To your current email address**: An email with the subject “Request to change your email” asking you to confirm the request.

 Click the confirmation link in **both** emails to complete the email change. Once both confirmations are complete, you can log in with your new email address.

---

# How can I delete my Resend account?

> How to request your Resend account and data to be deleted.

To delete your Resend account:

1. [Leave the team](https://resend.com/docs/dashboard/settings/team#leave-your-resend-team) associated with your Resend account.
2. Select the **Delete account** button.

 Upon confirmation, Resend will delete your account and all account data. Please note that this action is not reversible, so please proceed with
caution.

---

# How can I delete my Resend team?

> How to request your Resend team and team data to be deleted.

To request your Resend team and team data to be deleted:

1. Navigate to your [Team Settings](https://resend.com/settings/team).
2. Select the **Delete Team** button.

 Upon confirmation, Resend will delete your team and all your team data. If you are the last member of a team, you can also delete it by selecting
**Leave Team** instead. The system will automatically delete the team when the
last member leaves. Please note that this action is not reversible, so please proceed with
caution.

---

# Can I receive emails with Resend?

> Receiving emails is in early access.

We’re currently working on inbound email, [sign-up to join our early access waitlist](https://resend.com/inbound). The key components of this feature will include:

- Receive emails using webhooks. Get notified when emails are received.
- Parse content and attachments. Extract and process email data automatically.
- Reply to your users. Respond directly to incoming messages.

 While this feature is in early access, you can still [set a Reply To Address](https://resend.com/docs/knowledge-base/api-reference/emails/send-email) (`reply_to`) on your outbound emails to direct any responses to a different location like an existing inbox, slack channel, etc. Here are a few current workarounds that could help:

- **Sending to existing inbox**: You could set the `reply_to` as your personal email address. If any recipient replies to your email, it will be sent to the `reply_to` address. This could be a different address on the same domain, or a different domain entirely.
- **Sending to Slack**: You could set the `reply_to` as a [channel email address in Slack](https://slack.com/help/articles/206819278-Send-emails-to-Slack). This will create a new message in slack with the contents of the reply.

---

# How do Dedicated IPs work?

> When are Dedicated IPs helpful, and how can they be requested.

## ​What is a Dedicated IP?

 In email delivery, the sending IP address serves as a key identifier. Inbox Providers like Gmail track the reputation of these IPs based on the quality and quantity of emails sent from them, factoring this information into filtering and inbox placement decisions. By default, all Resend users utilize our shared IPs, which are a collection of IPs shared across many senders. Optionally, you can purchase a dedicated IP pool so a range of IPs are exclusively assigned to your sending. Resend goes one step further and exclusively provisions “Managed Dedicated IP Pools”. These managed pools handle multiple delicate and time consuming aspects of dedicated IPs:

- **Automatic warmup**: New IPs have no reputation and are therefore under scrutiny by inbox providers. We carefully migrate your sending over from the shared pool to your dedicated pool.
- **Automatic scaling**: IPs can only send at a certain rate based on the specifications of each inbox provider. We scale your pool dynamically based on the inbox provider feedback, without you lifting a finger.
- **Continuous monitoring**: Resend continuously monitors the reputation and performance of your dedicated IPs.
- **Fully dedicated**: You can segregate your emails from sending on shared pools to reduce risk of “noisy neighbors”.

 Resend only provisions Managed Dedicated IP Pools, but we will refer to them
as **Dedicated IPs** in this article to be succinct.

## ​When are Dedicated IPs helpful?

 Historically, Dedicated IPs were seen as the primary ingredient to great deliverability. This is not true anymore as Inbox Providers have incorporated dozens of other factors like sending history, domain reputation, and sending feedback (bounces and complaints) more predominantly than IP reputation. Though Dedicated IPs are not a deliverability silver bullet, they maintain a very helpful benefit: **removing risk of noisy neighbors**. There is power in numbers, and for many senders it can be very helpful to leverage the positive reputation of other senders in an IP pool. For some senders though, they want to maintain their own IP reputation without any chance of being impacted, positively or negatively, by other senders. For them, Dedicated IPs are a helpful solution.

## ​When are Dedicated IPs not helpful?

 Dedicated IPs can be very helpful, but there are some situations where they can actually hinder your ability to reach the inbox. If any of these situations match your use case, Dedicated IPs may hinder more than help:

- **Low email volume**: Sending less than 30k emails a month may not be enough to keep the IPs warm.
- **Inconsistent sending**: Sudden changes in email volume can hurt your IP reputation.
- **Poor email practices**: A Dedicated IP simply exposes your sending behavior even more.
- **New sender**: If you’re just starting out and have no sending history.
- **IP Allowlisting**: Resend does not expose the IPs included in your dedicated pool.

## ​How does IP warmup work?

 With Resend’s Managed Dedicated IP Pools, the warmup process is handled automatically:

1. **Automatic scaling**: Add or remove IP addresses based on your sending volume.
2. **Gradual increase**: Gradually increase the volume of emails sent through new IPs over time.
3. **Traffic distribution**: During warmup, traffic is distributed across shared and dedicated IPs.
4. **Reputation monitoring**: Continuously monitor the reputation of your dedicated IPs.
5. **Adaptive warmup**: Adapt the warmup process to your sending patterns.

 Often IP warmup is a highly manual process and requires great care if you don’t want a deliverability degradation in the process. With this automatic warmup process, we handle that for you so you can simply focus on sending. Because Managed Dedicated IP Pools are dynamically scaled, **we do not expose
the list of IPs** in your dedicated pool.

## ​Requirements for a Dedicated IP

 Before we can provision a Dedicated IP, **we require** that:

- Your domains are in the same region (Dedicated IPs are provisioned per region).
- Your sending volume exceeds 500 emails sent per day.
- You already have an active Transactional Scale or Marketing Pro subscription.
- All domains you want added to the Dedicated IP are already verified on Resend.

## ​How to request a Dedicated IP

 You can request a Dedicated IP by [chatting with support](https://resend.com/help). **We will request the following information**:

- What types of emails are you sending?
- How many emails are you sending per day and month on average?
- Is your sending consistent every day, or do you send in bursts?
- Which domains do you want included in your Dedicated IP?

---

# How do I avoid conflicts with my MX records?

> Learn how to avoid conflicts with your existing MX records when setting up a Resend domain.

## ​What is an MX record?

 MX (Mail Exchanger) records specify where incoming mail should be delivered on behalf of a domain. Every MX value has a unique priority (also known as preference) value. The lower the number, the higher the priority. Resend requires that you setup a MX record on two occasions:

1. **Enabling your domain to send emails**: You need to setup an MX record on `send.yourdomain.com` to establish a return-path for bounce/complaint reports from Inbox Providers. We set this return path in the email headers of every email you send through Resend.
2. **Enabling your domain to receive emails**: You can setup an MX record on your domain to route all received emails to Resend.

## ​Won’t this conflict with my existing Inbox Provider?

 Let’s look at an example for each occasion Resend requires you to setup a MX record. Say you’re using G Suite for your email. You’ll have an MX record that looks something like this:

```
yourdomain.com     MX    10 alt3.aspmx.l.google.com.
```

 This records specifies that any incoming mail to `<anything>@yourdomain.com` should be delivered to the google servers. Now, let’s say you want to use Resend to send emails from `@yourdomain.com`. You’ll need to add an MX record for `send.yourdomain.com` that looks something like this:

```
send.yourdomain.com     MX    10 feedback-smtp.us-east-1.amazonses.com
```

 This **won’t** conflict because the MX record is for `send.yourdomain.com`, not `yourdomain.com`. MX records only impact the subdomain they are associated to, so the Resend MX record will not affect your existing records on the root domain. Now say you want to start receiving emails through Resend. Because you already have the MX record `yourdomain.com`, you have two options:

1. **[Recommended] Create a MX record for a subdomain** (e.g. `subdomain.yourdomain.com`). Now emails sent to `<anything>@yourdomain.com` will continue going to G Suite, and emails sent to `<anything>@subdomain.domain.com` will go to Resend.
2. **Create a MX record with the lowest priority** among the other MX record for your domain.
  Since on our example, you already had a MX record for `yourdomain.com` point to G Suite, you would create:

```
yourdomain.com    MX    9  inbound-smtp.us-east-1.amazonaws.com
```

 Now this MX record priority has a lower value (higher priority) so it will be prioritized. But keep in mind that:

- This *will* route **all** emails destined to `<anything>@yourdomain.com` to Resend, insted of your previous provider(e.g. G Suite)
- If two MX records have the same priority value, this does **not** mean it will send to both servers — instead only one server will be chosen, randomly, per email delivery attempt.

## ​Solving common conflicts

Conflicts with existing records

If you already have a MX record set for `send.yourdomain.com`, you will need to remove it before adding the Resend MX record.If you need to keep the existing record, you can add a subdomain to your domain (e.g. `sub.yourdomain.com`) which will move the Resend MX location to `send.sub.yourdomain.com`.

Conflicts with existing priority

Each MX should have a unique priority value. We suggest using 10 for your MX record on `send.yourdomain.com`, but you can use a lower number (higher priority) if 10 is already in use.The lowest possible value (highest priority) is 0. So if you already have a record with this priority, you’ll need to remove it in order to create the MX record for Resend.
