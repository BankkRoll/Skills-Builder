# 403 Error Using Verified Domain and more

# 403 Error Using Verified Domain

> Learn how to resolve a 403 error caused by using a domain in your API request that doesn't match your verified domain.

Learn how to resolve a 403 error caused by using a domain in your API request that doesn’t match your verified domain.

---

# 403 Error Using resend.dev Domain

> Learn how to resolve a 403 error when using the resend.dev domain to send emails to recipients other than your own.

Learn how to resolve a 403 error when using the resend.dev domain to send emails to recipients other than your own.

---

# What are Resend account quotas and limits?

> Learn what quotas and limits apply to accounts.

Resend regulates email volume in three ways:

1. email volume (quota) - for [Transactional Email](https://resend.com/docs/knowledge-base/what-sending-feature-to-use#what-is-a-transactional-email)
2. number of contacts - for [Marketing Email](https://resend.com/docs/knowledge-base/what-sending-feature-to-use#what-is-a-marketing-email)
3. sending rate

 These limits help improve your deliverability and likelihood of reaching your recipient’s inbox. Both **sent emails** and **received emails** (inbound) count towards your
account’s email quota. Each received email counts as 1 email against your
daily and monthly limits, just like sent emails.

## ​Free Account Quotas and Limits

 Free accounts have the following:

- Transactional emails: daily email quota of 100 emails/day and 3,000 emails/month. This quota includes both sent and received emails. Multiple `To`, `CC`, or `BCC` recipients in sent emails count as separate emails towards this quota.
- Marketing emails: unlimited emails to up to 1,000 contacts per month.

## ​Paid Plan Quota

- Transactional Pro, Scale and Enterprise plans have no daily quota limits, though the plan tier will dictate the monthly email quota. Both sent and received emails count towards this monthly quota. To see your current month usage, view the [Usage page](https://resend.com/settings/usage). Multiple `To`, `CC`, or `BCC` recipients in sent emails count as separate emails towards the monthly quota.
- Marketing Pro, Enterprise plans have unlimited emails, though the plan tier will dictate the monthly contacts.

## ​Overage Limits

 Paid plans include pay-as-you-go overages, which allow you to continue sending emails after you’ve reached your monthly quota. To prevent extreme overages and unexpected costs, we impose a hard limit of 5x your monthly quota. By default, overage usage is capped at **5x your plan’s monthly quota**. Once you reach this limit, sending will be paused until the next billing cycle.If you need to adjust this limit, please [contact support](https://resend.com/help). While overages provide flexibility for occasional spikes in email volume, they
can be more expensive per email than upgrading your plan. If you consistently
exceed your quota, consider [upgrading to a higher
tier](https://resend.com/settings/billing) for better value and more
predictable costs.

## ​Rate Limits

 All accounts start with a rate limit of 2 requests per second. The [rate limits](https://resend.com/docs/api-reference/introduction#rate-limit) follow the [IETF standard](https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-ratelimit-headers) for stating the rate limit in the response header. If you have specific requirements, [contact support](https://resend.com/help) to request a rate increase.

## ​Bounce Rate

 All accounts must maintain a bounce rate of under **4%**. The [Metrics page](https://resend.com/metrics) within an account and/or [webhooks](https://resend.com/docs/webhooks/event-types#email-bounced) allow you to monitor your account bounce rates. Maintaining a bounce rate above 4% may result in a temporary pause in sending until the bounce rate is reduced. Tips to keep a bounce rate low:

- Remove inactive user email addresses from email lists.
- Only send to recipients who have given consent to receive email.
- When testing, avoid sending to fake email addresses. Use Resend’s [test email addresses](https://resend.com/docs/dashboard/emails/send-test-emails) instead.
- If you are using open/click tracking, periodically remove recipients who are not engaging with your emails from your email lists.

## ​Spam Rate

 All accounts must have a spam rate of under **0.08%**. The [Metrics page](https://resend.com/metrics) within an account and/or [webhooks](https://resend.com/docs/webhooks/event-types#email-complained) allow you to monitor your account spam rates. Maintaining a spam rate over 0.08% may result in a temporary pause in sending until the spam rate is reduced. Tips to keep a spam rate low:

- Give recipients an easy way to opt-out of emails.
- Send relevant and timely emails.
- Only send to recipients who have given consent to receive email.

---

# How to add the Resend integration to your Anything project

> Learn how to add the Resend integration to your Anything project.

[Anything](https://createanything.com) is a platform for building web sites, tools, apps, and projects via chat. With their [Resend integration](https://www.createanything.com/docs/integrations/resend), you can send emails from your Anything project. If you prefer to watch a video, check out our video walkthrough below.

## ​1. Call the Resend integration in Anything

 Type `/Resend` in the chat and select the integration, and ask Anything to add email functionality to your project. ![adding the Resend integration to a Anything chat](https://mintcdn.com/resend/ABWmVTZIHGIFNTFD/images/create-xyz-integration.png?fit=max&auto=format&n=ABWmVTZIHGIFNTFD&q=85&s=810ab7bd912d16365530bbda50d339d8)

## ​2. Add your Resend API key

 Anything usually prompts you for a Resend API key, which you can add in the [Resend Dashboard](https://resend.com/api-keys). If Anything doesn’t prompt you for a Resend API key, click the **More options**  button and select **Secrets**. Click the  **Add new secret** button.

- **Name:** `RESEND_API_KEY`
- **Value:** Your Resend API key (e.g., `re_xxxxxxxxx0`)

 Learn more about [Secrets in Create](https://www.createanything.com/docs/essentials#project-settings).

## ​3. Add a custom domain to your Resend account

 By default, you can only send emails to your own email address. To send emails to other email addresses:

1. Add a [custom domain to your Resend account](https://resend.com/domains).
2. Add the custom domain to the `from` field in the `resend` function in Create.

 Learn more about [Functions in Create](https://www.createanything.com/docs/builder/functions).

---

# Audience Hygiene: How to keep your Audiences in good shape?

> Learn strategies for maintaining good audience hygiene and maximizing email deliverability.

Audience hygiene (*also known as list hygiene*) refers to the practice of keeping your email list clean, valid, and engaged. Maintaining proper audience hygiene is crucial for ensuring that your emails reach their intended recipients, maximizing your deliverability, and improving your sender reputation. By removing invalid, outdated, or disengaged contacts, you can improve the effectiveness of your email campaigns and avoid issues like high bounce rates, low engagement, and even being marked as spam.

---

# ​How to ensure emails are valid?

 To keep your list healthy, it’s essential to ensure that the email addresses you collect are valid, accurate, and belong to recipients who are truly interested in hearing from you. Here are a few strategies to help you achieve this:

### ​Prevent undesired or bot signups with CAPTCHA

 Bots can easily sign up for your emails, inflating your list with fake or low-quality contacts. To prevent this, implement CAPTCHA systems during your sign-up process. CAPTCHA challenges help ensure that sign-ups are coming from human users and not automated scripts. Some popular CAPTCHA services include:

- **Google reCAPTCHA**: One of the most widely used CAPTCHA services, offering both simple and advanced protection options.
- **hCaptcha**: An alternative to Google reCAPTCHA, providing similar protection but with a different user experience.
- **Friendly Captcha**: A privacy-focused CAPTCHA solution that doesn’t require users to click on anything, reducing friction in the sign-up process.

 Using these tools will help reduce bot sign-ups and ensure your email list consists of real users.

### ​Ensure the recipient is consenting with Double Opt-In

 Double opt-in is the process of confirming a user’s subscription after they’ve signed up for your emails. When a user submits their email address, you send them a confirmation email with a link they must click to complete the subscription process. This step ensures that the person who entered the email address is the one who actually wants to receive your communications. This is important to ensure:

- **Compliance with local regulations**: Double opt-in helps ensure that you comply with email marketing regulations such as the **CAN-SPAM Act** (U.S.) and **CASL** (Canada). Both of these laws require clear consent from subscribers before you can send them marketing emails.
- **Improved deliverability**: Double opt-in helps you maintain a clean list of genuinely interested users. This reduces bounce rates and prevents spam complaints, which in turn helps maintain your sender reputation with ISPs and inbox providers.
- **Verification of accuracy**: Double opt-in ensures the email addresses you collect are valid, accurate, and up to date, reducing the risk of sending to invalid addresses and impacting your deliverability.

### ​Use a third-party service to verify an address’ deliverability

 While you can verify that an email address follows the correct syntax (e.g., [user@example.com](mailto:user@example.com)) (also known as RFC 5322), you also need to ensure that the address is deliverable—that is, it’s an active inbox that can receive emails. Third-party email verification services can help you identify whether an email address is valid, reachable, or likely to result in a bounce. This reduces the risk of sending to addresses that won’t receive your emails and improves your overall deliverability. Some email verification services include:

- **Emailable**
- **ZeroBounce**
- **Kickbox**

 By using these services, you can clean up your existing email lists or prevent undeliverable emails to be added to them. This helps prevent unnecessary deliverability issues.

---

# ​How to proactively remove emails from your Segments

 Over time, certain recipients may become disengaged with your content. It’s important to manage your segments by removing inactive or unengaged users. Regularly filtering your segments ensures that you’re sending to only those who are actively interested, which in turn boosts engagement and deliverability. A healthy email list is one that is continuously nurtured with relevant and timely content. Instead of sporadic communication, maintain consistent engagement with your audience to keep them interested.

### ​Filter on engagement

 To keep your email list in top shape, focus on sending to engaged users. Major inbox providers like Gmail and Microsoft expect you to send emails to recipients who have recently opened or clicked on your emails. As a best practice, you should limit non-transactional email sends to recipients who have opened or clicked an email in the past 6 months. The exact timeframe may vary depending on your industry, sending frequency,
and audience behavior, but 6 months is a generally accepted standard. Regularly cleaning your list of disengaged recipients helps maintain a positive sender reputation and boosts your chances of landing in the inbox instead of the spam folder.

### ​Automatically remove bounced recipients

 Using our [Webhooks](https://resend.com/docs/webhooks/introduction), you can be notified when a delivery bounces or gets marked as spam by the recipient. This is an opportunity to proactively unsubscribe the recipient and prevent further sending. Indeed, while Resend will automatically suppress further deliveries to that email address, we don’t automatically unsubscribe it.

### ​Sunset unengaged recipients

 If certain recipients have not engaged with your emails over an extended period (e.g., 6+ months), consider removing them from your Marketing sends. Continuing to send to these unengaged users can harm your deliverability by increasing bounce rates and decreasing your open rates. To re-engage these users, you may want to send a re-engagement campaign or offer an incentive for them to stay on your list. If they don’t respond, it’s often best to remove them to keep your list healthy and avoid wasting resources on inactive contacts.

---

 By maintaining strong audience hygiene practices—including validating email addresses, ensuring consent, verifying deliverability, and removing unengaged recipients—you’ll improve your email deliverability and foster better relationships with your subscribers. This will help you achieve better engagement rates and a healthier sender reputation with inbox providers.

---

# Send emails with Base44 and Resend

> Learn how to add the Resend integration to your Base44 project.

[Base44](https://base44.com/) is a platform for building apps with AI. You can add Resend in a Base44 project by asking the chat to add email sending with Resend. This integration requires backend functions, a feature available only on
Builder tier and above. Learn more about [Base44
pricing](https://base44.com/pricing).

## ​1. Add the Resend integration in Base44

 **If starting a new app:**

1. Click **Integration** in the top nav.
2. Search for **Resend**, select it, and choose **Use This Integration**.

 ![Resend Integration page](https://mintcdn.com/resend/ABWmVTZIHGIFNTFD/images/base44-integration.png?fit=max&auto=format&n=ABWmVTZIHGIFNTFD&q=85&s=f98f8dda5a22d0a0aa0aadc40c9324f3) **If adding Resend to an existing app:**

1. Enable backend functions.
2. Ask the chat: “Add the Resend email integration to my app. Prompt me to provide the API key and send a welcome email to new users.”

 See the [Base44
documenation](https://docs.base44.com/Integrations/Resend-integration) for
more information.

## ​2. Add your Resend API key

 However you add Resend to your project, you’ll need to add a Resend API key, which you can create in the [Resend Dashboard](https://resend.com/api-keys). Do not share your API key with others or expose it in the browser or other client-side code. Copy the API key and paste it into the **RESEND_API_KEY** field in Base44. ![Adding your Resend API key to Base44](https://mintcdn.com/resend/ABWmVTZIHGIFNTFD/images/base44-integration-1.png?fit=max&auto=format&n=ABWmVTZIHGIFNTFD&q=85&s=e10a7a52b06dde106b7a2db585bb7b30)

## ​3. Add a custom domain to your Resend account

 By default, you can only send emails to your own email address. To send emails to other email addresses:

1. Add a [custom domain to your Resend account](https://resend.com/domains).
2. Add the custom domain to the `from` field in the `resend` function in the Base44 backend function (or ask the chat to update these fields).

 Get more help adding a custom domain in [Resend’s documentation](https://resend.com/docs/dashboard/domains/introduction).

---

# Send emails with Bolt.new and Resend

> Learn how to add the Resend integration to your Bolt.new project.

[Bolt.new](https://bolt.new) is a platform for building full-stack web and mobile apps via chat. You can add Resend in a Bolt.new project by asking the chat to add email sending with Resend. ![adding the Resend integration to a Bolt.new chat](https://mintcdn.com/resend/ABWmVTZIHGIFNTFD/images/bolt-new-integration.png?fit=max&auto=format&n=ABWmVTZIHGIFNTFD&q=85&s=702a20abddc5efbf7b7d0b3e25c431ed)

## ​1. Add your Resend API key

 To use Resend with Bolt.new, you’ll need to add a Resend API key, which you can create in the [Resend Dashboard](https://resend.com/api-keys). Do not share your API key with others or expose it in the browser or other client-side code. To safely store your Resend API key, use a `.env` file. You may need to
include this instruction in your prompt to bolt.new. Learn more about
[handling API keys](https://resend.com/docs/knowledge-base/how-to-handle-api-keys).

## ​2. Add a custom domain to your Resend account

 By default, you can only send emails to your own email address. To send emails to other email addresses:

1. Add a [custom domain to your Resend account](https://resend.com/domains).
2. Add the custom domain to the `from` field in the `resend` function in Bolt.new (or ask the chat to update these fields).

 Get more help adding a custom domain in [Resend’s documentation](https://resend.com/docs/dashboard/domains/introduction).

---

# Cloudflare

> Verify your domain on Cloudflare with Resend.

## ​Add Domain to Resend

 First, log in to your [Resend Account](https://resend.com/login) and [add a domain](https://resend.com/domains). ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-add-domain.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=418dd93c2f2ead0b0d83d1b7c2fb0970) It is [best practice to use a
subdomain](https://resend.com/docs/knowledge-base/is-it-better-to-send-emails-from-a-subdomain-or-the-root-domain)
(updates.example.com) instead of the root domain (example.com). Using a
subdomain allows for proper reputation segmentation based on topics or purpose
(e.g. marketing) and is especially important if receiving emails with Resend.

## ​Automatic Setup (Recommended)

 The fastest way to verify your domain on Cloudflare is using the **Sign in to Cloudflare** button on Resend. This uses Domain Connect to automatically configure your DNS records.

1. Go to your [Domains page](https://resend.com/domains) in Resend.
2. (Optional) If you want to receive emails, select `Manual setup` and toggle the “Receiving” switch on the domain details page. ([Learn more below](#receiving-emails))
3. Click **Sign in to Cloudflare** button.
4. Authorize Resend to access your Cloudflare DNS settings.
5. The DNS records will be added automatically.

  That’s it. Your domain will be verified within a few minutes.

## ​Manual Setup

 If you prefer to add DNS records manually, follow these steps.

### ​Log in to Cloudflare

 Log in to your [Cloudflare account](https://cloudflare.com) and go to the DNS Records of your domain. ![Domain Details](https://mintcdn.com/resend/ABWmVTZIHGIFNTFD/images/dashboard-domains-cloudflare-main.png?fit=max&auto=format&n=ABWmVTZIHGIFNTFD&q=85&s=ffd61997133f0af6f4ba8d14df82dcdc)

### ​Add MX SPF Record

 Click “Add Record” on Cloudflare:

1. Set the Type to `MX`.
2. Type `send` for the `Name` of the record.
3. Copy the MX Value from Resend into the `Mail Server` field.
4. Use the default `Auto` for `TTL`.
5. Add `10` for the `Priority`.
6. Select `Save`.

 ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-spf-mx.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=bb0db2dd2809135194cfb62b695225cd)
 ![Domain Details](https://mintcdn.com/resend/ABWmVTZIHGIFNTFD/images/dashboard-domains-cloudflare-spf-mx.png?fit=max&auto=format&n=ABWmVTZIHGIFNTFD&q=85&s=372024c515c4b6924e5a1314ad831b6f) Below is a mapping of the record fields from Resend to Cloudflare:

| Cloudflare | Resend | Example Value |
| --- | --- | --- |
| Type | Type | MX |
| Name | Name | send |
| Mail Server | Value | feedback-smtp.us-east-1.amazonses.com |
| Priority | Priority | 10 |

 Omit your domain from the record values in Resend when you paste. Instead of
`send.example.com`, paste only `send` (or `send.subdomain` if you’re using a
subdomain). Do not use the same priority for multiple records. If Priority `10` is already
in use, try a higher value `20` or `30`.

### ​Add TXT SPF Record

 Click “Add Record” on Cloudflare:

1. Set the Type to `TXT`.
2. Type `send` for the `Name` of the record.
3. Copy the TXT Value Resend into `Content` field.
4. Use the default `Auto` for `TTL`.
5. Select `Save`.

 ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-spf-txt.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=747425d0a224baeee2846c9a707d5bbc)
 ![Domain Details](https://mintcdn.com/resend/ABWmVTZIHGIFNTFD/images/dashboard-domains-cloudflare-spf-txt.png?fit=max&auto=format&n=ABWmVTZIHGIFNTFD&q=85&s=3a20409e0c792c602f4eb636dcfbc3ac) Below is a mapping of the record fields from Resend to Cloudflare:

| Cloudflare | Resend | Example Value |
| --- | --- | --- |
| Type | Type | TXT |
| Name | Name | send |
| Content | Content | "v=spf1 include:amazonses.com ~all" |
| TTL | - | Auto |

 Omit your domain from the record values in Resend when you paste. Instead of
`send.example.com`, paste only `send` (or `send.subdomain` if you’re using a
subdomain).

### ​Add TXT DKIM Records

 Click “Add Record” on Cloudflare:

1. Set the Type to `TXT`.
2. Type `resend._domainkey` for the `Name` of the record.
3. Copy the TXT Value Resend into `Content` field.
4. Use the default `Auto` for `TTL`.
5. Select `Save`.

 ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-dkim.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=345d1dc6b7c138dbd92bd6928c634bd9)
 ![Domain Details](https://mintcdn.com/resend/ABWmVTZIHGIFNTFD/images/dashboard-domains-cloudflare-dkim-txt.png?fit=max&auto=format&n=ABWmVTZIHGIFNTFD&q=85&s=dafb2d6d5050da130371a2b7a8390abd) Below is a mapping of the record fields from Resend to Cloudflare:

| Cloudflare | Resend | Example Value |
| --- | --- | --- |
| Type | Type | TXT |
| Name | Name | resend._domainkey |
| Target | Value | p=example_demain_key_value |
| Proxy Status | - | DNS Only (disabled) |
| TTL | - | Auto |

 Omit your domain from the record values in Resend when you paste. Instead of
`resend._domainkey.example.com`, paste only `resend._domainkey` (or
`resend._domainkey.subdomain` if you’re using a subdomain).

### ​Receiving Emails

 If you want to receive emails at your domain, toggle the “Receiving” switch on the domain details page. ![Enable Receiving Emails for a verified domain](https://mintcdn.com/resend/B7wTVm7aKL5pNT-6/images/inbound-domain-toggle.png?fit=max&auto=format&n=B7wTVm7aKL5pNT-6&q=85&s=46f6b4c142fb90e04b57861e338ed2d0) When you enable Inbound on a domain, Resend receives *all emails* sent to that
specific domain depending on the priority of the MX record. For this reason,
we strongly recommend verifying a subdomain (`subdomain.example.com`) instead
of the root domain (`example.com`). Learn more about [avoiding conflicts with
your existing MX
records](https://resend.com/docs/knowledge-base/how-do-i-avoid-conflicting-with-my-mx-records). Click “Add Record” on Cloudflare:

1. Set the Type to `MX`.
2. Type `inbound` (or whatever your subdomain is) for the `Name` of the record.
3. Copy the MX Value from Resend into the `Mail Server` field.
4. Use the default `Auto` for `TTL`.
5. Add `10` for the `Priority`.
6. Select `Save`.

 Below is a mapping of the record fields from Resend to Cloudflare:

| Cloudflare | Resend | Example Value |
| --- | --- | --- |
| Type | Type | MX |
| Name | Name | inbound |
| Mail Server | Content | inbound-smtp.us-east-1.amazonaws.com |
| Priority | Priority | 10 |

 After verifying your domain, create a webhook to process incoming emails. For help setting up a webhook, how to access email data and attachments, forward emails, and more, see [our guide on receiving emails with Resend](https://resend.com/docs/dashboard/receiving/introduction).

### ​Complete Verification

 Now click [Verify DNS Records](https://resend.com/domains) on your Domain in Resend. It may take up to 72 hours to complete the verification process (often much faster).

## ​Troubleshooting

 If your domain is not successfully verified, these are some common troubleshooting methods.

Cloudflare returns 'Code: 1004' when adding CNAME Records.

Confirm your proxy settings are set to `DNS Only` on the record you are adding.

Resend shows my domain verification failed.

Review the records you added to Cloudflare to rule out copy and paste errors.

It has been longer than 72 hours and my domain is still Pending.

[Review our guide on a domain not verifying](https://resend.com/docs/knowledge-base/what-if-my-domain-is-not-verifying).

---

# Does Resend require production approval?

> Learn about production access and account limitations on Resend.

No, Resend does **not** require production approval. All accounts, including free accounts, have immediate production access from the moment you sign up.

## ​Free accounts have production access

 Free accounts on Resend have full production access immediately. There is no sandbox mode, no approval process, and no waiting period. You can start sending transactional emails to your customers right away. Resend does not limit free accounts or require authorization to send
production emails. All accounts have the same production capabilities from day
one.

## ​Common misconceptions

 Some users may think they need production approval if:

- **DNS records aren’t generated yet**: If you’ve added a domain but haven’t completed DNS verification, the domain will show as “Pending” until you add the required DNS records. This is not related to account approval—it’s simply waiting for domain verification. Once you add and verify your DNS records, you can send from that domain.
- **Coming from other email services**: Some email service providers do require production approval or have sandbox modes. Resend does not have these restrictions.

## ​Getting started

 To start sending emails with Resend:

1. [Sign up for a Resend account](https://resend.com/signup)
2. [Add and verify your domain](https://resend.com/domains)
3. [Create an API key](https://resend.com/api-keys)
4. Start sending emails immediately

 If you’re having trouble with domain verification or DNS records, see our [domain verification troubleshooting guide](https://resend.com/docs/knowledge-base/what-if-my-domain-is-not-verifying) or check our [DNS setup guides](https://resend.com/docs/knowledge-base/introduction) for your specific DNS provider.

---

# Email Best Practices Skill

> Comprehensive guide for building production-ready email systems with AI agents.

The Email Best Practices skill provides AI agents with comprehensive knowledge for building production-ready email integrations in your applications. It covers authentication, compliance, deliverability, and operational best practices.

## ​Installation

 Install the skill using the following command:

```
npx skills add resend/email-best-practices
```

## ​Advantages

- **DNS authentication guidance**: Step-by-step instructions for setting up SPF, DKIM, and DMARC records.
- **Transactional and marketing email design**: Best practices for designing effective transactional and marketing emails.
- **Regional compliance**: Guidelines for CAN-SPAM, GDPR, CASL, and other regional email regulations.
- **Webhook event processing**: Patterns for handling delivery notifications, bounces, and complaints.
- **Suppression list management**: Strategies for maintaining healthy suppression lists and improving deliverability.

## ​Learn More

 [View on GitHubSee the full source code and documentation.](https://github.com/resend/email-best-practices)

---

# How to set up E2E testing with Playwright

> End to end testing ensures your entire app flow is fully functioning.

Below is a basic guide on setting up E2E testing with NextJS, Resend, and Playwright. Prefer watching a video? Check out our video walkthrough below.

## ​1. Create an endpoint.

 For simplicity, we’ll create a GET endpoint that sends an email to the testing account, `delivered@resend.dev` on fetch. app/api/send/route.ts

```
import { Resend } from 'resend';
const resend = new Resend(process.env.RESEND_API_KEY);

export async function GET() {
  try {
    const { data, error } = await resend.emails.send({
      from: 'Acme <onboarding@resend.dev>',
      to: ['delivered@resend.dev'],
      subject: 'Hello world',
      html: '<h1>Hello world</h1>',
    });

    if (error) {
      return Response.json({ error }, { status: 500 });
    }

    return Response.json({ data });
  } catch (error) {
    return Response.json({ error }, { status: 500 });
  }
}
```

## ​2. Write the test spec file

 Create a test spec file at `e2e/app.spec.ts`. You can test in two ways:

### ​Option 1: Call the Resend API

 Calling the Resend API tests the entire API flow, including Resend’s API responses, but counts towards your account’s sending quota. e2e/app.spec.ts

```
import { test, expect } from '@playwright/test';

test('does not mock the response and calls the Resend API', async ({
  page,
}) => {
  // Go to the page
  await page.goto('http://localhost:3000/api/send');

  // Assert that the response is visible
  await expect(page.getByText('id')).toBeVisible();
});
```

### ​Option 2: Mock a response

 Mocking the response lets you test *your* app’s flow without calling the Resend API and impacting your account’s sending quota. e2e/app.spec.ts

```
import { test, expect } from '@playwright/test';

test("mocks the response and doesn't call the Resend API", async ({ page }) => {
  // Sample response from Resend
  const body = JSON.stringify({
    data: {
      id: '621f3ecf-f4d2-453a-9f82-21332409b4d2',
    },
  });

  // Mock the api call before navigating
  await page.route('*/**/api/send', async (route) => {
    await route.fulfill({
      body,
      contentType: 'application/json',
      status: 200,
    });
  });
});
```

 However you test, it’s important to test using a test email address (e.g.,
[delivered@resend.dev](mailto:delivered@resend.dev)) so your tests don’t impact your deliverability. Resend’s
[test accounts](https://resend.com/docs/dashboard/emails/send-test-emails) run through the entire API
flow without harming your reputation.

## ​3. Create a Playwright config file

 Write your config file, paying special attention to a few properties:

- `testDir`: the directory containing your test files
- `outputDir`: the directory to store test results
- `webServer`: provide instructions for Playwright to run your app before starting the tests
- `projects`: an array of the browsers you want to test

 playwright.config.ts

```
import { defineConfig, devices } from '@playwright/test';
import path from 'path';

const baseURL = 'http://localhost:3000';

export default defineConfig({
  timeout: 30 * 1000,
  testDir: path.join(__dirname, 'e2e'),
  retries: 2,
  outputDir: 'test-results/',
  webServer: {
    command: 'npm run dev',
    url: baseURL,
    timeout: 120 * 1000,
    reuseExistingServer: !process.env.CI,
  },

  use: {
    baseURL,
    // Retry a test if its failing with enabled tracing. This allows you to analyze the DOM, console logs, network traffic etc.
    trace: 'retry-with-trace',
  },

  projects: [
    // Test against desktop browsers.
    {
      name: 'Desktop Chrome',
      use: {
        ...devices['Desktop Chrome'],
      },
    },
    {
      name: 'Desktop Firefox',
      use: {
        ...devices['Desktop Firefox'],
      },
    },
    {
      name: 'Desktop Safari',
      use: {
        ...devices['Desktop Safari'],
      },
    },
    // Test against mobile viewports.
    {
      name: 'Mobile Chrome',
      use: {
        ...devices['Pixel 5'],
      },
    },
    {
      name: 'Mobile Safari',
      use: devices['iPhone 12'],
    },
  ],
});
```

 [See the Playwright docs](https://playwright.dev/docs/intro) for more help.

## ​4. Run the test

 You can run the test by installing Playwright and running the tests.

```
npx playwright install
npx playwright test
```

 Playwright will run the tests in the browsers of your choice and show you the results. [Example repoSee the full source code.](https://github.com/resend/resend-nextjs-playwright-example)

---

# Forward emails with Resend Inbound

> Learn how to forward receiving emails to another email address with Resend Inbound.

Inbound enables you to receive emails with Resend. This guide demonstrates how to forward received emails using [NextJS](https://nextjs.org/), although you can use any framework you prefer. 1

Verify a domain with Inbound

[Verify a domain](https://resend.com/domains) and enable receiving emails for that domain. We strongly recommend verifying a subdomain (`subdomain.example.com`) instead of the root domain (`example.com`).![Verify a domain with Inbound](https://mintcdn.com/resend/Pc2KlUXbYPa-UCHT/images/forward-emails-with-resend-inbound.png?fit=max&auto=format&n=Pc2KlUXbYPa-UCHT&q=85&s=bb522c39f8fc29fafeda1166be728cca)Add the records in your DNS provider and wait for verification to finish in Resend. Learn more about [adding Domains in Resend](https://resend.com/docs/dashboard/domains/introduction).When you enable Inbound on a domain, Resend receives *all emails* sent to that
specific domain depending on the priority of the MX record. For this reason,
we strongly recommend verifying a subdomain (`subdomain.example.com`) instead
of the root domain (`example.com`). Learn more about [avoiding conflicts with
your existing MX
records](https://resend.com/docs/knowledge-base/how-do-i-avoid-conflicting-with-my-mx-records).2

Create a POST route

Resend can send a webhook to your application’s endpoint every time you receive an email.Add a new POST route to your application’s endpoint.app/api/inbound-webhook/route.ts

```
import type { NextRequest } from 'next/server';
import { NextResponse } from 'next/server';

export const POST = async (request: NextRequest) => {
  try {
    const payload = await request.text();

    return NextResponse.json(payload);
  } catch (error) {
    console.error(error);
    return new NextResponse(`Error: ${error}`, { status: 500 });
  }
};
```

3

Create a webhook in Resend

Go to the [Webhooks page](https://resend.com/webhooks) and click **Add Webhook**.

1. Add your publicly accessible HTTPS URL.
2. Select all events you want to observe (e.g., `email.received`).
3. Click **Add**.

![Create a webhook in Resend](https://mintcdn.com/resend/Pc2KlUXbYPa-UCHT/images/forward-emails-with-resend-inbound-1.png?fit=max&auto=format&n=Pc2KlUXbYPa-UCHT&q=85&s=43a04cb717556ed636109764863bf44a)For development, you can create a tunnel to your localhost server using a tool like
[ngrok](https://ngrok.com/download) or [VS Code Port Forwarding](https://code.visualstudio.com/docs/debugtest/port-forwarding). These tools serve your local dev environment at a public URL you can use to test your local webhook endpoint.Example: `https://example123.ngrok.io/api/webhook`4

Add Resend to your project

Add the Resend Node.js SDK to your project using your preferred package manager.

```
npm install resend
```

Create an [API key with “Full access” permission](https://resend.com/docs/dashboard/api-keys/introduction) in Resend and add it to your project’s .env file..env

```
RESEND_API_KEY=re_xxxxxxxxx
```

5

Verify the webhook request

Webhook signing secrets are used to validate the payload data sent to your application from Resend.Update your POST route to verify the webhook request using the webhook secret. First, copy the webhook secret from the webhook details page.![Webhook Secret](https://mintcdn.com/resend/Pc2KlUXbYPa-UCHT/images/forward-emails-with-resend-inbound-2.png?fit=max&auto=format&n=Pc2KlUXbYPa-UCHT&q=85&s=1f5b8a6ea354470d05869f61ffb087ec)Then, add it to your project’s .env file..env

```
RESEND_WEBHOOK_SECRET=whsec_xxxxxxxxxx
```

Update the POST route to verify the webhook request using the webhook secret.Make sure that you’re using the raw request body when verifying webhooks. The cryptographic signature is sensitive to even the slightest change. Some frameworks parse the request as JSON and then stringify it, and this will also break the signature verification.app/api/inbound-webhook/route.ts

```
import type { NextRequest } from 'next/server';
import { NextResponse } from 'next/server';
import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);

export async function POST(req: NextRequest) {
  try {
    // we need raw request text to verify the webhook
    const payload = await req.text();

    const id = req.headers.get('svix-id');
    const timestamp = req.headers.get('svix-timestamp');
    const signature = req.headers.get('svix-signature');

    if (!id || !timestamp || !signature) {
      return new NextResponse('Missing headers', { status: 400 });
    }

    // Throws an error if the webhook is invalid
    // Otherwise, returns the parsed payload object
    const result = resend.webhooks.verify({
      payload,
      headers: {
        id,
        timestamp,
        signature,
      },
      webhookSecret: process.env.RESEND_WEBHOOK_SECRET!,
    });

    return NextResponse.json(result);
  } catch (error) {
    console.error(error);
    return new NextResponse(`Error: ${error}`, { status: 500 });
  }
}
```

6

Process incoming emails

Once you verify the webhook, it returns the webhook payload as a JSON object. You can use this payload to forward the email to another email address. Note the following steps:

1. Add a guard clause to ensure the event type is `email.received`.
2. Get the incoming email’s content
3. Download and encode any attachments
4. Forward the email (remember to update the `from` and `to` addresses below)

You must call the [received emails
API](https://resend.com/docs/api-reference/emails/retrieve-received-email) to retrieve the email
content and the [attachments
API](https://resend.com/docs/api-reference/emails/list-received-email-attachments) to retrieve the
attachments. This design choice supports large payloads in serverless
environments that have limited request body sizes.app/api/inbound-webhook/route.ts

```
import type { NextRequest } from 'next/server';
import { NextResponse } from 'next/server';
import { Resend, type ListAttachmentsResponseSuccess } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);

export async function POST(req: NextRequest) {
  try {
    const payload = await req.text();

    const id = req.headers.get('svix-id');
    const timestamp = req.headers.get('svix-timestamp');
    const signature = req.headers.get('svix-signature');

    if (!id || !timestamp || !signature) {
      return new NextResponse('Missing headers', { status: 400 });
    }

    const result = resend.webhooks.verify({
      payload,
      headers: {
        id,
        timestamp,
        signature,
      },
      webhookSecret: process.env.RESEND_WEBHOOK_SECRET!,
    });

    // 1. Add a guard clause to ensure the event type is `email.received`.
    if (result.type !== 'email.received') {
      return NextResponse.json({ message: 'Invalid event' }, { status: 200 });
    }

    // 2. Get the incoming email's content
    const { data: email, error: emailError } =
      await resend.emails.receiving.get(result.data.email_id);

    if (emailError) {
      throw new Error(`Failed to fetch email: ${emailError.message}`);
    }

    // 3. Download and encode any attachments
    const { data: attachmentsData, error: attachmentsError } =
      await resend.emails.receiving.attachments.list({
        emailId: result.data.email_id,
      });

    if (attachmentsError) {
      throw new Error(
        `Failed to fetch attachments: ${attachmentsError.message}`,
      );
    }

    const attachments =
      attachmentsData?.data as ListAttachmentsResponseSuccess['data'] &
        { content: string }[];

    if (attachments && attachments.length > 0) {
      // download the attachments and encode them in base64
      for (const attachment of attachments) {
        const response = await fetch(attachment.download_url);
        const buffer = Buffer.from(await response.arrayBuffer());
        attachment.content = buffer.toString('base64');
      }
    }

    // 4. Forward the email
    const { data, error: sendError } = await resend.emails.send({
      from: 'onboarding@resend.dev', // replace with an email address from your verified domain
      to: ['delivered@resend.dev'], // replace with the email address you want to forward the email to
      subject: result.data.subject,
      html: email.html,
      text: email.text,
      attachments,
    });

    if (sendError) {
      throw new Error(`Failed to forward email: ${sendError.message}`);
    }

    return NextResponse.json({ message: 'Email forwarded successfully', data });
  } catch (error) {
    console.error(error);
    return new NextResponse(`Error: ${error}`, { status: 500 });
  }
}
```

7

Test the endpoint

You can test the endpoint by sending an email to the domain you verified.For example, if you verified `marketing.example.com`, send an email to `test@marketing.example.com`.

- Try a simple HTML email with a subject and a body.
- Try an email with an attachment or multiple attachments.

You can view the received email in the [Emails page](https://resend.com/emails/receiving) and see the webhook payload in the [Webhooks page](https://resend.com/webhooks).8

Go to Production

Once you’ve tested the endpoint:

1. Publish your application to your production environment.
2. Add your production POST endpoint as a new webhook in Resend.
