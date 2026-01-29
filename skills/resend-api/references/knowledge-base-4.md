# MCP Server and more

# MCP Server

> Learn how to use the MCP Server to send emails.

## ​What is an MCP Server?

 MCP is an open protocol that standardizes how applications provide context to LLMs. Among other benefits, it provides LLMs tools to act on your behalf. If you prefer to watch a video, check out our video walkthrough below.

## ​What can Resend’s MCP Server do?

 Currently, Resend’s MCP Server is a simple server you must build locally that can send emails using Resend’s API on your behalf.

- Send plain text and HTML emails
- Schedule emails for future delivery
- Add CC and BCC recipients
- Configure reply-to addresses
- Customizable sender email (requires verification)

 As an example, you could use this to run local scripts, chat with Claude, or process data and send the results to yourself or your team.

## ​How to use Resend’s MCP Server

 Build the project locally to use this MCP server to use it in a [supported MCP client](#mcp-client-integrations). 1

Clone this project locally.

```
git clone https://github.com/resend/mcp-send-email.git
```

2

Build the project

```
npm install
npm run build
```

3

Setup Resend

1. [Create an API Key](https://resend.com/api-keys): copy this key to your clipboard
2. [Verify your own domain](https://resend.com/domains): to send to email addresses other than your own

## ​MCP Client Integrations

 With the MCP server built, you can now add it to a supported MCP client.

### ​Cursor

 1

Open Cursor Settings

Open the command palette (`cmd`+`shift`+`p` on macOS or `ctrl`+`shift`+`p` on Windows) and choose **Cursor Settings**.2

Add the MCP server

Select **MCP** from the left sidebar and click **Add new global MCP server** and add the following config:

```
{
  "mcpServers": {
    "resend": {
      "type": "command",
      "command": "node ABSOLUTE_PATH_TO_MCP_SEND_EMAIL_PROJECT/build/index.js --key=YOUR_RESEND_API_KEY"
    }
  }
}
```

You can get the absolute path to your build script by right-clicking on the `/build/index.js` file in Cursor and selecting `Copy Path`.**Possible arguments**

- `--key`: Your Resend API key (required)
- `--sender`: Your sender email address from a verified domain (optional)
- `--reply-to`: Your reply-to email address (optional)

If you don’t provide a sender email address, the MCP server will ask you to
provide one each time you call the tool.Adding the MCP server to Cursor’s global settings will let you send emails from any project on your machine using Cursor’s Agent mode.3

Test the sending

Test sending emails by going to `email.md` in the cloned project.

- Replace the to: email address with your own
- Select all text in `email.md`, and press `cmd+l`
- Tell cursor to “send this as an email” in the chat (make sure cursor is in Agent mode by selecting “Agent” on lower left side dropdown).

![Cursor chat with email.md file selected and Agent mode enabled](https://mintcdn.com/resend/OWNnQaVDyqcGyhhN/images/mcp-server-1.png?fit=max&auto=format&n=OWNnQaVDyqcGyhhN&q=85&s=fa2e1425ad8347080815dcd1dde4b7d8)

### ​Claude Desktop

 1

Open Claude Desktop settings

Open Claude Desktop settings and navigate to the “Developer” tab. Click `Edit Config`.2

Add the MCP server

Add the following config:

```
{
  "mcpServers": {
    "resend": {
      "command": "node",
      "args": ["ABSOLUTE_PATH_TO_MCP_SEND_EMAIL_PROJECT/build/index.js"],
      "env": {
        "RESEND_API_KEY": "YOUR_RESEND_API_KEY"
      }
    }
  }
}
```

You can get the absolute path to your build script by right-clicking on the `/build/index.js` file in your IDE and selecting `Copy Path`.**Possible environment variables**

- `RESEND_API_KEY`: Your Resend API key (required)
- `SENDER_EMAIL_ADDRESS`: Your sender email address from a verified domain (optional)
- `REPLY_TO_EMAIL_ADDRESS`: Your reply-to email address (optional)

If you don’t provide a sender email address, the MCP server will ask you to
provide one each time you call the tool.3

Test the server

Close and reopen Claude Desktop. Verify that the `resend` tool is available in the Claude developer settings.![Claude Desktop developer settings with Resend MCP server showing](https://mintcdn.com/resend/OWNnQaVDyqcGyhhN/images/mcp-server-2.png?fit=max&auto=format&n=OWNnQaVDyqcGyhhN&q=85&s=4d5c737476c68debac2d0adef163fa6f)Chat with Claude and tell it to send you an email using the `resend` tool.

---

# Namecheap

> Verify your domain on Namecheap with Resend.

## ​Add Domain to Resend

 First, log in to your [Resend Account](https://resend.com/login) and [add a domain](https://resend.com/domains). ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-add-domain.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=418dd93c2f2ead0b0d83d1b7c2fb0970) It is [best practice to use a
subdomain](https://resend.com/docs/knowledge-base/is-it-better-to-send-emails-from-a-subdomain-or-the-root-domain)
(updates.example.com) instead of the root domain (example.com). Using a
subdomain allows for proper reputation segmentation based on topics or purpose
(e.g. marketing) and is especially important if receiving emails with Resend.

## ​Log in to Namecheap

1. Log in to your [Namecheap account](https://ap.www.namecheap.com).
2. Click `Manage` for the domain. ![Domain Details](https://mintcdn.com/resend/svdlrksWLy8Dr3X-/images/dashboard-domains-namecheap-manage.png?fit=max&auto=format&n=svdlrksWLy8Dr3X-&q=85&s=cb8698fd0e0cab38eb335766a9d0b7d8) You may need to expand a dropdown to see the `Manage` button.
3. Go to the `Advanced DNS` page for the domain you want to verify. ![Domain Details](https://mintcdn.com/resend/svdlrksWLy8Dr3X-/images/dashboard-domains-namecheap-advanced-dns.png?fit=max&auto=format&n=svdlrksWLy8Dr3X-&q=85&s=b958e136050178c70eb4820e703803c6)

## ​Add MX SPF Record

 If you are changing the MX configuration from `Gmail` to `Custom MX`, you need
to [setup new MX records for
Gmail](https://support.google.com/a/answer/174125). If you don’t setup new
records, receiving mail in your gmail inboxes will stop. Under the `Mail Settings` section, click the dropdown and select `Custom MX`:

1. Type `send` for the `Host` of the record.
2. Copy the MX Value from Resend into the `Value` field.
3. Use the `Automatic` TTL.
4. Select `Save all changes`.

 ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-spf-mx.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=bb0db2dd2809135194cfb62b695225cd)
 ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-namecheap-spf-mx.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=dda5ff041cce1341e22123fd70111ef3) Below is a mapping of the record fields from Resend to Namecheap:

| Namecheap | Resend | Example Value |
| --- | --- | --- |
| Type | Type | MX Record |
| Host | Name | send |
| TTL | TTL | Automatic |
| Value | Value | feedback-smtp.us-east-1.amazonses.com |
| - | Priority | 10 |

 Omit your domain from the record values in Resend when you paste. Instead of
`send.example.com`, paste only `send` (or `send.subdomain` if you’re using a
subdomain). Namecheap does not label the `priority` column. It is the empty column after
`Value`. Do not use the same priority for multiple records. If Priority `10`
is already in use, try a higher value `20` or `30`.

## ​Add TXT SPF Record

 Under the `Host Records` section, click `Add New Record`:

1. Set the `Type` to `TXT Record`.
2. Enter `send` into the `Host` field.
3. Copy the TXT Value from Resend into the `Value` field.
4. Use the `Automatic` TTL.
5. Select `Save all changes`.

 ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-spf-txt.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=747425d0a224baeee2846c9a707d5bbc)
 ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-namecheap-spf-txt.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=b742409a1de5a3291dc64e1846c2cf77) Below is a mapping of the record fields from Resend to Namecheap:

| Namecheap | Resend | Example Value |
| --- | --- | --- |
| Type | Type | TXT Record |
| Host | Name | send |
| TTL | TTL | Automatic |
| Value | Value | "v=spf1 include:amazonses.com ~all" |

 Omit your domain from the record values in Resend when you paste. Instead of
`send.example.com`, paste only `send` (or `send.subdomain` if you’re using a
subdomain).

## ​Add TXT DKIM Records

 In that same `Host Records` section, click `Add New Record`.

1. Set the `Type` to `TXT Record`.
2. Enter `resend._domainkey` into the `Host` field.
3. Copy the TXT Value from Resend into the `Value` field.
4. Use the `Automatic` TTL.
5. Select `Save all changes`.

 ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-dkim.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=345d1dc6b7c138dbd92bd6928c634bd9)
 ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-namecheap-dkim-txt.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=0cd6480b613eaed711006b58c7b7a67a) Below is a mapping of the record fields from Resend to Namecheap:

| Namecheap | Resend | Example Value |
| --- | --- | --- |
| Type | Type | TXT Record |
| Host | Name | resend._domainkey |
| TTL | TTL | Automatic |
| Value | Value | p=example_demain_key_value |

 Omit your domain from the record values in Resend when you paste. Instead of
`resend._domainkey.example.com`, paste only `resend._domainkey` (or
`resend._domainkey.subdomain` if you’re using a subdomain).

## ​Receiving Emails

 If you want to receive emails at your domain, toggle the “Receiving” switch on the domain details page. ![Enable Receiving Emails for a verified domain](https://mintcdn.com/resend/B7wTVm7aKL5pNT-6/images/inbound-domain-toggle.png?fit=max&auto=format&n=B7wTVm7aKL5pNT-6&q=85&s=46f6b4c142fb90e04b57861e338ed2d0) When you enable Inbound on a domain, Resend receives *all emails* sent to that
specific domain depending on the priority of the MX record. For this reason,
we strongly recommend verifying a subdomain (`subdomain.example.com`) instead
of the root domain (`example.com`). Learn more about [avoiding conflicts with
your existing MX
records](https://resend.com/docs/knowledge-base/how-do-i-avoid-conflicting-with-my-mx-records). Under the `Mail Settings` section, click the dropdown and select `Custom MX`:

1. Type `inbound` (or whatever your subdomain is) for the `Host` of the record.
2. Copy the MX Value from Resend into the `Value` field.
3. Use the `Automatic` TTL.
4. Select `Save all changes`.

 Below is a mapping of the record fields from Resend to Namecheap:

| Namecheap | Resend | Example Value |
| --- | --- | --- |
| Type | Type | MX Record |
| Host | Name | inbound |
| TTL | TTL | Automatic |
| Value | Content | inbound-smtp.us-east-1.amazonaws.com |
| - | Priority | 10 |

 After verifying your domain, create a webhook to process incoming emails. For help setting up a webhook, how to access email data and attachments, forward emails, and more, see [our guide on receiving emails with Resend](https://resend.com/docs/dashboard/receiving/introduction).

## ​Complete Verification

 Now click [Verify DNS Records](https://resend.com/domains) on your Domain in Resend. It may take up to 72 hours to complete the verification process (often much faster).

## ​Troubleshooting

 If your domain is not successfully verified, these are some common troubleshooting methods.

Resend shows my domain verification failed.

Review the records you added to Namecheap to rule out copy and paste errors.

It has been longer than 72 hours and my domain is still Pending.

[Review our guide on a domain not verifying](https://resend.com/docs/knowledge-base/what-if-my-domain-is-not-verifying).

---

# Porkbun

> Verify your domain on Porkbun with Resend.

## ​Add Domain to Resend

 First, log in to your [Resend Account](https://resend.com/login) and [add a domain](https://resend.com/domains). ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-add-domain.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=418dd93c2f2ead0b0d83d1b7c2fb0970) It is [best practice to use a
subdomain](https://resend.com/docs/knowledge-base/is-it-better-to-send-emails-from-a-subdomain-or-the-root-domain)
(updates.example.com) instead of the root domain (example.com). Using a
subdomain allows for proper reputation segmentation based on topics or purpose
(e.g. marketing) and is especially important if receiving emails with Resend.

## ​Log in to Porkbun

 Log in to your [Porkbun account](https://porkbun.com/account/domainsSpeedy):

1. Select the `DNS` option under your domain to manage DNS records.

 ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-porkbun-domains.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=44389c4ae53707e508d38a34a794cec3)

## ​Add MX SPF Record

 In the `DNS` section on Porkbun copy and paste the values MX from Resend:

1. On the `Type` page, choose `MX`.
2. Type `send` for the `Host` of the record.
3. Copy the MX Value from Resend into the `Answer / Value` field.
4. Use the default TTL of `600`.
5. In the `Priority` field enter `10`.
6. Select `Add`.

 ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-spf-mx.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=bb0db2dd2809135194cfb62b695225cd) ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-porkbun-spf-mx.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=65428888fca00600f2bdf31d14db8eaf) Below is a mapping of the record fields from Resend to Porkbun:

| Porkbun | Resend | Example Value |
| --- | --- | --- |
| Type | Type | MX Record |
| Host | Name | send |
| Answer / Value | Value | feedback-smtp.us-east-1.amazonses.com |
| TTL | TTL | 600 |
| Priority | Priority | 10 |

 Do not use the same priority for multiple records. If Priority `10` is already
in use on another record, try a higher value `20` or `30`.

## ​Add TXT SPF Record

 On the same section:

1. On the `Type` page, choose `TXT`.
2. Type `send` for the `Host` of the record.
3. Copy the TXT Value Resend into the `Answer / Value` field.
4. Use the default TTL of `600`.
5. Select `Add Record`.

 Omit your domain from the record values in Resend when you paste. Instead of
`send.example.com`, paste only `send` (or `send.subdomain` if you’re using a
subdomain). ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-spf-txt.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=747425d0a224baeee2846c9a707d5bbc) ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-porkbun-spf-txt.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=7ef4c8c51fd01d854c6404b96b2a1a27) Below is a mapping of the record fields from Resend to Porkbun:

| Porkbun | Resend | Example Value |
| --- | --- | --- |
| Type | Type | TXT Record |
| Host | Name | send |
| Answer / Value | Value | "v=spf1 include:amazonses.com ~all" |
| TTL | TTL | 600 |

## ​Add TXT DKIM Records

 On the same `Create Record` section:

1. On the `Type` page, choose `TXT`.
2. Type `resend._domainkey` for the `Host` of the record.
3. Copy the TXT Value Resend into the `Answer / Value` field.
4. Use the default TTL of `600`.
5. Select `Add Record`.

 Omit your domain from the record values in Resend when you paste. Instead of
`resend._domainkey.example.com`, paste only `resend._domainkey` (or
`resend._domainkey.subdomain` if you’re using a subdomain). ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-dkim.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=345d1dc6b7c138dbd92bd6928c634bd9) ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-porkbun-dkim-txt.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=9f3a33882f02d34489d5adc55f28c7b8) Below is a mapping of the record fields from Resend to Porkbun:

| Porkbun | Resend | Example Value |
| --- | --- | --- |
| Type | Type | TXT Record |
| Host | Name | send |
| Answer / Value | Value | p=example_demain_key_value |
| TTL | TTL | 600 |

## ​Receiving Emails

 If you want to receive emails at your domain, toggle the “Receiving” switch on the domain details page. ![Enable Receiving Emails for a verified domain](https://mintcdn.com/resend/B7wTVm7aKL5pNT-6/images/inbound-domain-toggle.png?fit=max&auto=format&n=B7wTVm7aKL5pNT-6&q=85&s=46f6b4c142fb90e04b57861e338ed2d0) When you enable Inbound on a domain, Resend receives *all emails* sent to that
specific domain depending on the priority of the MX record. For this reason,
we strongly recommend verifying a subdomain (`subdomain.example.com`) instead
of the root domain (`example.com`). Learn more about [avoiding conflicts with
your existing MX
records](https://resend.com/docs/knowledge-base/how-do-i-avoid-conflicting-with-my-mx-records). In the `DNS` section on Porkbun:

1. On the `Type` page, choose `MX`.
2. Type `inbound` (or whatever your subdomain is) for the `Host` of the record.
3. Copy the MX Value from Resend into the `Answer / Value` field.
4. Use the default TTL of `600`.
5. In the `Priority` field enter `10`.
6. Select `Add`.

 Below is a mapping of the record fields from Resend to Porkbun:

| Porkbun | Resend | Example Value |
| --- | --- | --- |
| Type | Type | MX Record |
| Host | Name | inbound |
| Answer / Value | Content | inbound-smtp.us-east-1.amazonaws.com |
| TTL | TTL | 600 |
| Priority | Priority | 10 |

 After verifying your domain, create a webhook to process incoming emails. For help setting up a webhook, how to access email data and attachments, forward emails, and more, see [our guide on receiving emails with Resend](https://resend.com/docs/dashboard/receiving/introduction).

## ​Complete Verification

 Now click [Verify DNS Records](https://resend.com/domains) on your Domain in Resend. It may take a few hours to complete the verification process (often much faster).

## ​Troubleshooting

 If your domain is not successfully verified, these are some common troubleshooting methods.

Resend shows my domain verification failed.

Review the records you added to Porkbun to rule out copy and paste errors.

It has been longer than 72 hours and my domain is still Pending.

[Review our guide on a domain not verifying](https://resend.com/docs/knowledge-base/what-if-my-domain-is-not-verifying).

---

# React Email Skill

> Build HTML emails using React components with AI agents.

The React Email skill enables AI agents to build production-ready HTML emails using React components. It provides a modern development experience for creating responsive, cross-client compatible emails.

## ​Installation

 Install the skill using the following command:

```
npx skills add resend/react-email
```

## ​Advantages

- **Component-based email development**: Build emails using reusable React components for consistent, maintainable templates.
- **Brand-consistent styling with Tailwind**: Use Tailwind CSS to style emails with your brand’s design system.
- **Multi-format rendering**: Automatically generate both HTML and plain text versions of your emails.
- **Email client compatibility handling**: Built-in support for rendering emails correctly across all major email clients.
- **Built-in preview server**: Preview your emails in real-time during development with hot reloading.

## ​Learn More

 [View on GitHubSee the full source code and documentation.](https://github.com/resend/react-email/tree/canary/skills)

---

# Send emails with Replit and Resend

> Learn how to add the Resend integration to your Replit project.

[Replit](https://replit.com/) is a platform for building sites and apps with AI. You can add Resend in a Replit project by asking the chat to add email sending with Resend. **Example prompt**

```
When someone fills out the contact form, send an email using Resend.
```

 Prefer watching a video? Check out our video walkthrough below.

## ​1. Add a custom domain to your Resend account

 By default, you can only send emails to your own email address. To send emails to other email addresses:

1. Add a [custom domain to your Resend account](https://resend.com/domains).
2. Add the custom domain to the `from` field in the `resend` function in Replit (or ask the chat to update these fields).

 Get more help adding a custom domain in [Resend’s documentation](https://resend.com/docs/dashboard/domains/introduction).

## ​2. Add your Resend API key and from address

 To use Resend with Replit, you’ll need to add a Resend API key, which you can create in the [Resend Dashboard](https://resend.com/api-keys). Do not share your API key with others or expose it in the browser or other client-side code. The from address is the email address that will be used to send emails. Use your custom domain you added in step 1 here (e.g., `hello@yourdomain.com`). ![adding the Resend integration to a Replit chat](https://mintcdn.com/resend/873NN72QQCCHs00J/images/replit-integration.png?fit=max&auto=format&n=873NN72QQCCHs00J&q=85&s=7c6dee645c882748990a7973150b252f) Replit tracks the details of your Resend integration in the [Integrations
page](https://replit.com/integrations).

---

# Resend Skill

> Send emails through the Resend API with AI agents.

The Resend skill enables AI agents to send emails through the Resend API using our official recommendations. It provides a streamlined interface for sending single and batch emails with built-in error handling and retry logic.

## ​Installation

 Install the skill using the following command:

```
npx skills add resend/resend-skills
```

## ​Advantages

 Build with our official recommendations for sending emails with Resend.

- **Single and batch email sending**: Send individual emails or batch up to 100 emails per request.
- **Built-in error handling and retry logic**: Automatic retries with exponential backoff for transient failures.
- **Idempotency key support**: Prevent duplicate sends with idempotency keys for safe retries.
- **Multi-language SDK support**: Works with Node.js, Python, Ruby, Go, and other supported SDKs.
- **Automatic activation for email tasks**: AI agents automatically use this skill when email sending is needed.

## ​Learn More

 [View on GitHubSee the full source code and documentation.](https://github.com/resend/resend-skills)

---

# AWS Route 53

> Verify your domain on Route 53 with Resend.

## ​Add Domain to Resend

 First, log in to your [Resend Account](https://resend.com/login) and [add a domain](https://resend.com/domains). ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-add-domain.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=418dd93c2f2ead0b0d83d1b7c2fb0970) It is [best practice to use a
subdomain](https://resend.com/docs/knowledge-base/is-it-better-to-send-emails-from-a-subdomain-or-the-root-domain)
(updates.example.com) instead of the root domain (example.com). Using a
subdomain allows for proper reputation segmentation based on topics or purpose
(e.g. marketing) and is especially important if receiving emails with Resend.

## ​Log in to Route 53

 Then, log in to your [AWS Management Console, and open Route 53 console](https://console.aws.amazon.com/route53/), then click on your domain name. From there, click on `Create Record`. ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-route53-createrecord.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=93d90903872f328b3f593e933d29f4fe)

## ​Add MX SPF Record

1. Type in `send` for the `Record name`.
2. Select the `Record type` dropdown, and choose `MX`.
3. Copy the MX Value from your domain in Resend into the `Value` field.
4. Be sure to include the `10` in the `Value` field, as seen in the screenshot.

 Omit your domain from the record values in Resend when you paste. Instead of
`send.example.com`, paste only `send` (or `send.subdomain` if you’re using a
subdomain). ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-spf-mx.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=bb0db2dd2809135194cfb62b695225cd) ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-route53-spf-mx.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=8b798e983ecec8edb48c777143edfce5) Below is a mapping of the record fields from Resend to Route 53:

| Route 53 | Resend | Example Value |
| --- | --- | --- |
| Record Type | Type | MX Record |
| Record name | Name | send |
| Value | Value & Priority | 10 feedback-smtp.us-east-1.amazonses.com |
| TTL | TTL | Use Route 53 Default (300) |
| Routing policy | - | Simple routing |

 Route 53 does not label the `priority` column, and you will need to add this
in to the `Value` section, as shown in the screenshot. Do not use the same
priority for multiple records. If Priority `10` is already in use, try a
number slightly higher like `11` or `12`.

## ​Add TXT SPF Record

 In the same section, choose `Add another record`:

1. Type in `send` for the `Record name`.
2. Click the `Record type` dropdown.
3. Select the `Record type` dropdown, and choose `TXT`.
4. Copy TXT Value from your domain in Resend into the `Value` field.

 ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-spf-txt.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=747425d0a224baeee2846c9a707d5bbc) ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-route53-spf-txt.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=79d4f534f637964bc06005f34cafe92b) Below is a mapping of the record fields from Resend to Route 53:

| Route 53 | Resend | Example Value |
| --- | --- | --- |
| Record type | Type | TXT Record |
| Record name | Name | send |
| Value | Value | "v=spf1 include:amazonses.com ~all" |
| TTL | TTL | Use Route 53 Default (300) |
| Routing policy | - | Simple routing |

 Omit your domain from the record values in Resend when you paste. Instead of
`send.example.com`, paste only `send` (or `send.subdomain` if you’re using a
subdomain).

## ​Add TXT DKIM Records

 In the same section, choose `Add another record`:

1. Type in `resend._domainkey` for the `Record name`.
2. Change the `Record Type` to `TXT`.
3. Copy the TXT Value value from your domain in Resend to the `Value` text box.
4. Click on `Create Records`.

 ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-dkim.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=345d1dc6b7c138dbd92bd6928c634bd9) ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-route53-dkim-txt.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=00e9fa493cb8a6541fa0d16323b1a7af) Below is a mapping of the record fields from Resend to Route 53:

| Route 53 | Resend | Example Value |
| --- | --- | --- |
| Record type | Type | TXT Record |
| Record name | Name | resend._domainkey |
| Value | Value | p=example_demain_key_value |
| TTL | TTL | Use Route 53 Default (300) |
| Routing policy | - | Simple routing |

 Omit your domain from the record values in Resend when you paste. Instead of
`resend._domainkey.example.com`, paste only `resend._domainkey` (or
`resend._domainkey.subdomain` if you’re using a subdomain).

## ​Receiving Emails

 If you want to receive emails at your domain, toggle the “Receiving” switch on the domain details page. ![Enable Receiving Emails for a verified domain](https://mintcdn.com/resend/B7wTVm7aKL5pNT-6/images/inbound-domain-toggle.png?fit=max&auto=format&n=B7wTVm7aKL5pNT-6&q=85&s=46f6b4c142fb90e04b57861e338ed2d0) When you enable Inbound on a domain, Resend receives *all emails* sent to that
specific domain depending on the priority of the MX record. For this reason,
we strongly recommend verifying a subdomain (`subdomain.example.com`) instead
of the root domain (`example.com`). Learn more about [avoiding conflicts with
your existing MX
records](https://resend.com/docs/knowledge-base/how-do-i-avoid-conflicting-with-my-mx-records). In the Route 53 console, click `Create Record`:

1. Type in `inbound` (or whatever your subdomain is) for the `Record name`.
2. Select the `Record type` dropdown, and choose `MX`.
3. Copy the MX Value from your domain in Resend into the `Value` field.
4. Be sure to include the `10` in the `Value` field (e.g., `10 inbound-smtp.us-east-1.amazonaws.com`).

 Below is a mapping of the record fields from Resend to Route 53:

| Route 53 | Resend | Example Value |
| --- | --- | --- |
| Record Type | Type | MX Record |
| Record name | Name | inbound |
| Value | Content & Priority | 10 inbound-smtp.us-east-1.amazonaws.com |
| TTL | TTL | Use Route 53 Default (300) |
| Routing policy | - | Simple routing |

 After verifying your domain, create a webhook to process incoming emails. For help setting up a webhook, how to access email data and attachments, forward emails, and more, see [our guide on receiving emails with Resend](https://resend.com/docs/dashboard/receiving/introduction).

## ​Complete Verification

 Now click [Verify DNS Records](https://resend.com/domains) on your Domain in Resend. It may take up to 5 hours to complete the verification process (often much faster).

## ​Troubleshooting

 If your domain is not successfully verified, these are some common troubleshooting methods.

Resend shows my domain verification failed.

Review the records you added to Route 53 to rule out copy and paste errors.

It has been longer than 72 hours and my domain is still Pending.

[Review our guide on a domain not verifying](https://resend.com/docs/knowledge-base/what-if-my-domain-is-not-verifying).

---

# How to prevent bounces with @privaterelay.appleid.com recipients?

> Sending to Apple Private Email Relay requires specific configuration steps to ensure your emails get delivered

Sending to Apple Private Email Relay requires specific configuration steps to ensure your emails get delivered

---

# Should I add an unsubscribe link to all of my emails sent with Resend?

> Learn best practices about using unsubscribe links.

Transactional emails are generally exempt from including an unsubscribe link. Unlike marketing emails, transactional emails serve a functional purpose, such as account confirmation, password resets, and order confirmations. As a best practice, we recommend telling recipients how to opt out of receiving future email from you if the content is more related to nurturing relationships with your customers, rather than pragmatic, action-oriented emails. Laws enforced by the FTC and GDPR prioritize giving recipients an easy way to give and withdraw their consent to receiving email marketing content. Additionally, not having an option for opting out of emails risks recipients complaining or marking the email as spam, which can hurt your reputation as a sender. Here is more on how to [manually add and manage unsubscribe links](https://resend.com/docs/dashboard/emails/add-unsubscribe-to-transactional-emails). If you’re using [Resend Broadcasts](https://resend.com/docs/dashboard/audiences/managing-unsubscribe-list), the unsubscribe headers are added automatically to your emails. You can include the Unsubscribe Footer in your Broadcasts, which will be automatically replaced with the correct link for each contact or use `{{{RESEND_UNSUBSCRIBE_URL}}}` as a link target should you want to customize the unsubscribe footer.

---

# Squarespace

> Verify your domain on Squarespace with Resend.

## ​Add Domain to Resend

 First, log in to your [Resend Account](https://resend.com/login) and [add a domain](https://resend.com/domains). ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-add-domain.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=418dd93c2f2ead0b0d83d1b7c2fb0970) It is [best practice to use a
subdomain](https://resend.com/docs/knowledge-base/is-it-better-to-send-emails-from-a-subdomain-or-the-root-domain)
(updates.example.com) instead of the root domain (example.com). Using a
subdomain allows for proper reputation segmentation based on topics or purpose
(e.g. marketing) and is especially important if receiving emails with Resend.

## ​Log in to Squarespace

 Log in to your [Squarespace domains page](https://account.squarespace.com/domains) and click on your domain. ![Domain Details](https://mintcdn.com/resend/OWNnQaVDyqcGyhhN/images/squarespace-domains-main.png?fit=max&auto=format&n=OWNnQaVDyqcGyhhN&q=85&s=8362f1932f033cb983149883a9a459b6)

## ​Add MX SPF Record

 Scroll down to the **Custom records** section and select `Add record` on Squarespace.

1. Type `send` for the `Host` of the record.
2. Set the `Type` to `MX`.
3. Set the `Priority` to `10`.
4. Use the Default 4 hours for `TTL`.
5. Copy the MX Value from Resend into the `Mail Server` field
6. Select `Save`.

 ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-spf-mx.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=bb0db2dd2809135194cfb62b695225cd) ![Domain Details](https://mintcdn.com/resend/OWNnQaVDyqcGyhhN/images/squarespace-spf-mx.png?fit=max&auto=format&n=OWNnQaVDyqcGyhhN&q=85&s=1222dfd2f85a612e61a52f15c2ac9818) Below is a mapping of the record fields from Resend to Squarespace:

| Squarespace | Resend | Example Value |
| --- | --- | --- |
| Type | Type | MX |
| Host | Name | send |
| TTL | TTL | 4 hrs(default) |
| Mail Server | Value | feedback-smtp.us-east-1.amazonses.com |
| Priority | Priority | 10 |

 Omit your domain from the record values in Resend when you paste. Instead of
`send.example.com`, paste only `send` (or `send.subdomain` if you’re using a
subdomain). Do not use the same priority for multiple records. If Priority `10` is already
in use, try a higher value `20` or `30`.

## ​Add TXT SPF Record

 In the same **Custom records** section, select `Add Record` on Squarespace.

1. Type `send` for the `Host` of the record.
2. Set the `Type` to `TXT`.
3. Use the Default 4 hours for `TTL`.
4. Copy the TXT Value from Resend into the `Text` field
5. Select `Save`.

 Add the **TXT Record** from your domain in Resend to Squarespace and click “Save”. ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-spf-txt.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=747425d0a224baeee2846c9a707d5bbc)
 ![Domain Details](https://mintcdn.com/resend/OWNnQaVDyqcGyhhN/images/squarespace-spf-txt.png?fit=max&auto=format&n=OWNnQaVDyqcGyhhN&q=85&s=13d1b0604c22b16161d1b99e9bc2f8d8) Below is a mapping of the record fields from Resend to Squarespace:

| Squarespace | Resend | Example Value |
| --- | --- | --- |
| Type | Type | TXT |
| Host | Name | send |
| TTL | TTL | 4 hrs(default) |
| Text | Value | "v=spf1 include:amazonses.com ~all" |

 Omit your domain from the record values in Resend when you paste. Instead of
`send.example.com`, paste only `send` (or `send.subdomain` if you’re using a
subdomain).

## ​Add TXT DKIM Records

 In the same **Custom records** section, select `Add Record` on Squarespace.

1. Type `resend._domainkey` for the `Host` of the record.
2. Set the `Type` to `TXT`.
3. Use the Default 4 hours for `TTL`.
4. Copy the TXT Value from Resend into the `Text` field
5. Select `Save`.

 ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-dkim.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=345d1dc6b7c138dbd92bd6928c634bd9) ![Domain Details](https://mintcdn.com/resend/OWNnQaVDyqcGyhhN/images/squarespace-dkim-txt.png?fit=max&auto=format&n=OWNnQaVDyqcGyhhN&q=85&s=119a6ade9688e65297e2dbff30e8256d) Below is a mapping of the record fields from Resend to Squarespace:

| Squarespace | Resend | Example Value |
| --- | --- | --- |
| Type | Type | TXT |
| Host | Name | resend._domainkey |
| TTL | TTL | 4 hrs(default) |
| Text | Value | p=example_demain_key_value |

 Omit your domain from the record values in Resend when you paste. Instead of
`resend._domainkey.example.com`, paste only `resend._domainkey` (or
`resend._domainkey.subdomain` if you’re using a subdomain).

## ​Receiving Emails

 If you want to receive emails at your domain, toggle the “Receiving” switch on the domain details page. ![Enable Receiving Emails for a verified domain](https://mintcdn.com/resend/B7wTVm7aKL5pNT-6/images/inbound-domain-toggle.png?fit=max&auto=format&n=B7wTVm7aKL5pNT-6&q=85&s=46f6b4c142fb90e04b57861e338ed2d0) When you enable Inbound on a domain, Resend receives *all emails* sent to that
specific domain depending on the priority of the MX record. For this reason,
we strongly recommend verifying a subdomain (`subdomain.example.com`) instead
of the root domain (`example.com`). Learn more about [avoiding conflicts with
your existing MX
records](https://resend.com/docs/knowledge-base/how-do-i-avoid-conflicting-with-my-mx-records). Scroll down to the **Custom records** section and select `Add record` on Squarespace:

1. Type `inbound` (or whatever your subdomain is) for the `Host` of the record.
2. Set the `Type` to `MX`.
3. Set the `Priority` to `10`.
4. Use the Default 4 hours for `TTL`.
5. Copy the MX Value from Resend into the `Mail Server` field.
6. Select `Save`.

 Below is a mapping of the record fields from Resend to Squarespace:

| Squarespace | Resend | Example Value |
| --- | --- | --- |
| Type | Type | MX |
| Host | Name | inbound |
| TTL | TTL | 4 hrs(default) |
| Mail Server | Content | inbound-smtp.us-east-1.amazonaws.com |
| Priority | Priority | 10 |

 After verifying your domain, create a webhook to process incoming emails. For help setting up a webhook, how to access email data and attachments, forward emails, and more, see [our guide on receiving emails with Resend](https://resend.com/docs/dashboard/receiving/introduction).

## ​Complete Verification

 Now click [Verify DNS Records](https://resend.com/domains) on your Domain in Resend. It may take up to 72 hours to complete the verification process (often much faster).

## ​Troubleshooting

 If your domain is not successfully verified, these are some common troubleshooting methods.

Resend shows my domain verification failed.

Review the records you added to Squarespace to rule out copy and paste errors.

It has been longer than 72 hours and my domain is still Pending.

[Review our guide on a domain not verifying](https://resend.com/docs/knowledge-base/what-if-my-domain-is-not-verifying).

---

# Strato

> Verify your domain on Strato with Resend.

## ​Add Domain to Resend

 First, log in to your [Resend Account](https://resend.com/login) and [add a domain](https://resend.com/domains). ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-add-domain.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=418dd93c2f2ead0b0d83d1b7c2fb0970) It is [best practice to use a
subdomain](https://resend.com/docs/knowledge-base/is-it-better-to-send-emails-from-a-subdomain-or-the-root-domain)
(updates.example.com) instead of the root domain (example.com). Using a
subdomain allows for proper reputation segmentation based on topics or purpose
(e.g. marketing) and is especially important if receiving emails with Resend.

## ​Log in to Strato

 Log in to your [Strato account](https://www.strato.es/apps/CustomerService):

1. In the left-hand navigation, go to Domains > Manage Domain.

 ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-strato-domain-manager.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=684004473fd6679100907921ce2767df)

## ​Add MX SPF Record

1. On the domain page, click on the gear icon to redirect to Settings.
2. Create a new subdomain named `send`.
3. Navigate to the subdomain settings.
4. Go to the `DNS` tab, you’ll see a list of DNS records you can update. Click on `manage` MX record.
5. Select own mail server.
6. Copy MX value from Resend into `Server` field.
7. Use the default priority `Low`.
8. Save settings.

 By default, Strato domains use Strato mail server which uses `mail` as their
send path. You will need to bypass this default behavior by creating a
subdomain and setting the MX record there. ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-spf-mx.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=bb0db2dd2809135194cfb62b695225cd) ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-strato-mx.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=9c884d56f98f468503cb10d28b6cd60f) Below is a mapping of the record fields from Resend to Strato:

| Strato | Resend | Example Value |
| --- | --- | --- |
| Type | Type | MX Record |
| Name | Name | send |
| Mail server | Value | feedback-smtp.eu-west-1.amazonses.com. |
| Priority | Priority | Low |

## ​Add TXT SPF Record

 On the base domain settings:

1. Go to the `DNS` tab.
2. Manage TXT and CNAME records.
3. On the bottom, click `Create another record`.
4. Choose `TXT` type.
5. Add `send` for the `name` record.
6. For `value` input `v=spf1 include:amazonses.com ~all`.
7. Save settings.

 Strato provides a standard DMARC record similar to Resend’s recommended value:
`v=DMARC1;p=reject;`. ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-spf-txt.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=747425d0a224baeee2846c9a707d5bbc) ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-strato-spf-dkim.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=d3484aaa1f6eda375fce393939d69ada) Below is a mapping of the record fields from Resend to Strato:

| Strato | Resend | Example Value |
| --- | --- | --- |
| Type | Type | TXT Record |
| Name | Name | send |
| Value | Value | v=spf1 include:amazonses.com ~all |

## ​Add TXT DKIM Records

 On the same TXT and CNAME manage page:

1. Click `Create another record`.
2. Choose `TXT` type.
3. Add `resend._domainkey` for the `Name` record.
4. Copy the record value from Resend into the TXT value field.
5. Save settings.

 Omit your domain from the record values in Resend when you paste. Instead of
`resend._domainkey.example.com`, paste only `resend._domainkey` (or
`resend._domainkey.subdomain` if you’re using a subdomain). ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-dkim.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=345d1dc6b7c138dbd92bd6928c634bd9) ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-strato-spf-dkim.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=d3484aaa1f6eda375fce393939d69ada) Below is a mapping of the record fields from Resend to Strato:

| Strato | Resend | Example Value |
| --- | --- | --- |
| Type | Type | TXT Record |
| Name | Name | send |
| Value | Value | p=example_demain_key_value |

 Copy DKIM value using the small copy icon in Resend. DKIM records are
case-sensitive and must match up exactly.

## ​Receiving Emails

 If you want to receive emails at your domain, toggle the “Receiving” switch on the domain details page. ![Enable Receiving Emails for a verified domain](https://mintcdn.com/resend/B7wTVm7aKL5pNT-6/images/inbound-domain-toggle.png?fit=max&auto=format&n=B7wTVm7aKL5pNT-6&q=85&s=46f6b4c142fb90e04b57861e338ed2d0) When you enable Inbound on a domain, Resend receives *all emails* sent to that
specific domain depending on the priority of the MX record. For this reason,
we strongly recommend verifying a subdomain (`subdomain.example.com`) instead
of the root domain (`example.com`). Learn more about [avoiding conflicts with
your existing MX
records](https://resend.com/docs/knowledge-base/how-do-i-avoid-conflicting-with-my-mx-records).

1. Create a new subdomain named `inbound` (or whatever your subdomain is).
2. Navigate to the subdomain settings.
3. Go to the `DNS` tab and click on `manage` MX record.
4. Select own mail server.
5. Copy MX value from Resend into `Server` field.
6. Use the default priority `Low`.
7. Save settings.

 Below is a mapping of the record fields from Resend to Strato:

| Strato | Resend | Example Value |
| --- | --- | --- |
| Type | Type | MX Record |
| Name | Name | inbound |
| Mail server | Content | inbound-smtp.us-east-1.amazonaws.com. |
| Priority | Priority | Low |

 After verifying your domain, create a webhook to process incoming emails. For help setting up a webhook, how to access email data and attachments, forward emails, and more, see [our guide on receiving emails with Resend](https://resend.com/docs/dashboard/receiving/introduction).

## ​Complete Verification

 Now click [Verify DNS Records](https://resend.com/domains) on your Domain in Resend. It may take a few hours to complete the verification process (often much faster).

## ​Troubleshooting

 If your domain is not successfully verified, these are some common troubleshooting methods.

Resend shows my domain verification failed.

Review the records you added to Strato to rule out copy and paste errors.

It has been longer than 72 hours and my domain is still Pending.

[Review our guide on a domain not verifying](https://resend.com/docs/knowledge-base/what-if-my-domain-is-not-verifying).

---

# Send emails with v0 and Resend

> Learn how to add the Resend integration to your v0 project.

[v0](https://v0.dev) by Vercel is a platform for building web sites, tools, apps, and projects via chat. You can add Resend in a v0 project by asking the chat to add email sending with Resend.

## ​1. Add your Resend API key

 To use Resend with v0, you’ll need to add a Resend API key, which you can create in the [Resend Dashboard](https://resend.com/api-keys). Do not share your API key with others or expose it in the browser or other
client-side code. ![adding the Resend integration to a v0 chat](https://mintcdn.com/resend/lyl6PQTYhtWhUjuS/images/v0-integration.png?fit=max&auto=format&n=lyl6PQTYhtWhUjuS&q=85&s=cb85c63c4d0bca95571920a08324432f)

## ​2. Add a custom domain to your Resend account

 By default, you can only send emails to your own email address. To send emails to other email addresses:

1. Add a [custom domain to your Resend account](https://resend.com/domains).
2. Add the custom domain to the `from` field in the `resend` function in v0 (or ask the chat to update these fields).

 Get more help adding a custom domain in [Resend’s documentation](https://resend.com/docs/dashboard/domains/introduction).
