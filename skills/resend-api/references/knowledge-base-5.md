# Vercel and more

# Vercel

> Verify your domain on Vercel with Resend.

This guide helps you verify your domain on Vercel with Resend. We also have
[an official integration for
Vercel](https://resend.com/blog/vercel-integration) that helps you set up your
API keys on Vercel projects so you can start sending emails with Resend. [View
the integration here](https://vercel.com/resend/~/integrations/resend).

## ​Add Domain to Resend

 First, log in to your [Resend Account](https://resend.com/login) and [add a domain](https://resend.com/domains). ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-add-domain.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=418dd93c2f2ead0b0d83d1b7c2fb0970) It is [best practice to use a
subdomain](https://resend.com/docs/knowledge-base/is-it-better-to-send-emails-from-a-subdomain-or-the-root-domain)
(updates.example.com) instead of the root domain (example.com). Using a
subdomain allows for proper reputation segmentation based on topics or purpose
(e.g. marketing) and is especially important if receiving emails with Resend.

## ​Log in to Vercel

 Log in to your [Vercel account](https://vercel.com/login) and select the `Domains` tab. ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-vercel-domains.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=4b4ab73110a36775175b39587eea68f0)

## ​Add MX SPF Record

 Copy and paste the values in Resend to Vercel.

1. Type `send` for the `Name` of the record in Vercel.
2. Expand the `Type` dropdown and select `MX`.
3. Copy the record value from Resend into the `Value` field in Vercel.
4. Add `10` for the `Priority`.
5. Select `Add`.

 Omit your domain from the record values in Resend when you paste. Instead of
`send.example.com`, paste only `send` (or `send.subdomain` if you’re using a
subdomain). ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-spf-mx.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=bb0db2dd2809135194cfb62b695225cd) ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-vercel-spf-mx.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=9d91de47106d0bd4005bac0cfe68779e) Below is a mapping of the record fields from Resend to Vercel:

| Vercel | Resend | Example Value |
| --- | --- | --- |
| Type | Type | MX Record |
| Name | Name | send |
| Value | Value | feedback-smtp.us-east-1.amazonses.com |
| TTL | TTL | Use Vercel default (60) |
| Priority | Priority | 10 |

 Do not use the same priority for multiple records. If Priority `10` is already
in use on another record, try a higher value `20` or `30`.

## ​Add TXT SPF Record

 In the same section, add another record in Vercel.

1. Type `send` for the `Name` of the record.
2. Expand the `Type` dropdown and select `TXT`.
3. Copy the `TXT` record value from Resend into the `Value` field in Vercel.
4. Use the default TTL of `60`.
5. Select `Add`.

 Omit your domain from the record values in Resend when you paste. Instead of
`send.example.com`, paste only `send` (or `send.subdomain` if you’re using a
subdomain). ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-spf-txt.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=747425d0a224baeee2846c9a707d5bbc) ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-vercel-spf-txt.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=27b350fc1a7745dd47c623fdaf9a2df4) Below is a mapping of the record fields from Resend to Vercel:

| Vercel | Resend | Example Value |
| --- | --- | --- |
| Type | Type | TXT Record |
| Name | Name | send |
| Value | Value | "v=spf1 include:amazonses.com ~all" |
| TTL | TTL | Use Vercel default (60) |

## ​Add TXT DKIM Records

 In the same section, add another record in Vercel.

1. Type `resend._domainkey` for the `Name` of the record.
2. Expand the `Type` dropdown and select `TXT`.
3. Copy the record value from Resend into the `Value` field in Vercel.

 Omit your domain from the record values in Resend when you paste. Instead of
`resend._domainkey.example.com`, paste only `resend._domainkey` (or
`resend._domainkey.subdomain` if you’re using a subdomain). ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-dkim.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=345d1dc6b7c138dbd92bd6928c634bd9) ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-vercel-dkim-txt.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=8553d093e572970b0335c1fe9b83e003) Below is a mapping of the record fields from Resend to Vercel:

| Vercel | Resend | Example Value |
| --- | --- | --- |
| Type | Type | TXT Record |
| Name | Name | resend._domainkey |
| Value | Value | p=example_demain_key_value |
| TTL | TTL | Use Vercel default (60) |

## ​Receiving Emails

 If you want to receive emails at your domain, toggle the “Receiving” switch on the domain details page. ![Enable Receiving Emails for a verified domain](https://mintcdn.com/resend/B7wTVm7aKL5pNT-6/images/inbound-domain-toggle.png?fit=max&auto=format&n=B7wTVm7aKL5pNT-6&q=85&s=46f6b4c142fb90e04b57861e338ed2d0) When you enable Inbound on a domain, Resend receives *all emails* sent to that
specific domain depending on the priority of the MX record. For this reason,
we strongly recommend verifying a subdomain (`subdomain.example.com`) instead
of the root domain (`example.com`). Learn more about [avoiding conflicts with
your existing MX
records](https://resend.com/docs/knowledge-base/how-do-i-avoid-conflicting-with-my-mx-records). Copy and paste the values in Resend to Vercel:

1. Type `inbound` (or whatever your subdomain is) for the `Name` of the record in Vercel.
2. Expand the `Type` dropdown and select `MX`.
3. Copy the MX Value from Resend into the `Value` field in Vercel.
4. Add `10` for the `Priority`.
5. Select `Add`.

 Below is a mapping of the record fields from Resend to Vercel:

| Vercel | Resend | Example Value |
| --- | --- | --- |
| Type | Type | MX Record |
| Name | Name | inbound |
| Value | Content | inbound-smtp.us-east-1.amazonaws.com |
| TTL | TTL | Use Vercel default (60) |
| Priority | Priority | 10 |

 After verifying your domain, create a webhook to process incoming emails. For help setting up a webhook, how to access email data and attachments, forward emails, and more, see [our guide on receiving emails with Resend](https://resend.com/docs/dashboard/receiving/introduction).

## ​Complete Verification

 Now click [Verify DNS Records](https://resend.com/domains) on your Domain in Resend. It may take a few hours to complete the verification process (often much faster).

## ​Troubleshooting

 If your domain is not successfully verified, these are some common troubleshooting methods.

Resend shows my domain verification failed.

Review the records you added to Vercel to rule out copy and paste errors.

It has been longer than 72 hours and my domain is still Pending.

[Review our guide on a domain not verifying](https://resend.com/docs/knowledge-base/what-if-my-domain-is-not-verifying).

---

# Domain and/or IP Warm

> Learn how to warm up a domain or IP to avoid deliverability issues.

Warming up a domain or IP refers to the practice of progressively increasing your sending volume to maximize your deliverability. The goal is to send at a consistent rate and avoid any spikes in email volume that might be concerning to inbox service providers. Whenever you change your sending patterns—whether because you’re using a new domain, a new IP, or a new vendor, or because your volume will increase—you should warm-up your domain and/or IP. A thought-out warm-up plan limits greylisting and delivery throttling, as well as helping establish a good domain and IP reputation. As your volume increases, you’ll need to monitor your bounce rate to ensure it remains below 4%, and your spam rate below 0.08%. An increase in these rates would be a sign that your warm-up plan needs to be slowed down and an investigation into the root causes of the increases started. Following these rules and metrics will establish a good domain reputation. Each sender has different constraints and needs, so these numbers are meant as
a baseline. Our [Support team](https://resend.com/help) can work with you on
devising a plan adapted to your needs.

## ​Existing domain

 If you’re already sending from an existing domain with established reputation and volumes, you can use the following guidelines to start sending with Resend.

| Day | Messages per day | Messages per hour |
| --- | --- | --- |
| 1 | Up to 1,000 emails | 100 Maximum |
| 2 | Up to 2,500 emails | 300 Maximum |
| 3 | Up to 5,000 emails | 600 Maximum |
| 4 | Up to 5,000 emails | 800 Maximum |
| 5 | Up to 7,500 emails | 1,000 Maximum |
| 6 | Up to 7,500 emails | 1,500 Maximum |
| 7 | Up to 10,000 emails | 2,000 Maximum |

## ​New domain

 Before you start sending emails with a brand new domain, it’s especially important to have a warm-up plan so you can maximize your deliverability right from the start.

| Day | Messages per day | Messages per hour |
| --- | --- | --- |
| 1 | Up to 150 emails |  |
| 2 | Up to 250 emails |  |
| 3 | Up to 400 emails |  |
| 4 | Up to 700 emails | 50 Maximum |
| 5 | Up to 1,000 emails | 75 Maximum |
| 6 | Up to 1,500 emails | 100 Maximum |
| 7 | Up to 2,000 emails | 150 Maximum |

## ​Warm-up calculator

 Use the calculator below to generate a personalized warm-up schedule based on your specific needs. Enter your target volume, timeline, and domain type to get a custom plan. The guide is meant as a general plan, but always pay careful attention to your deliverability and adjust accordingly. If you have specific questions, [please reach out to us](https://resend.com/help).

# ​Warming up your Dedicated IP with Resend

 In order for a Dedicated IP to be beneficial or useful, you first need to establish a certain sending volume and patterns. Once you’ve established this volume and these patterns, our [Support team](https://resend.com/help) can set it up for you. We provide an automatic warm-up process so that you can simply focus on sending. [Learn more about requesting a Dedicated IP](https://resend.com/docs/knowledge-base/how-do-dedicated-ips-work#how-to-request-a-dedicated-ip).

# ​What about third-party warm-up services?

 We know email deliverability is important, and it can be tempting to use services promising quick fixes. However, using tools that artificially boost engagement can harm your long-term sender reputation. These services often rely on manipulating anti-spam filters, which can backfire as email providers like Gmail adjust their systems. Instead, we recommend focusing on sustainable practices—such as sending relevant content, maintaining a clean list, and using proper authentication. These methods build trust with email providers and improve your deliverability over time.

---

# What attachment types are not supported?

> Learn which file attachment extensions you can't send.

You can **send** any file attachment types except for those in the following list.

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| .adp | .app | .asp | .bas | .bat |
| .cer | .chm | .cmd | .com | .cpl |
| .crt | .csh | .der | .exe | .fxp |
| .gadget | .hlp | .hta | .inf | .ins |
| .isp | .its | .js | .jse | .ksh |
| .lib | .lnk | .mad | .maf | .mag |
| .mam | .maq | .mar | .mas | .mat |
| .mau | .mav | .maw | .mda | .mdb |
| .mde | .mdt | .mdw | .mdz | .msc |
| .msh | .msh1 | .msh2 | .mshxml | .msh1xml |
| .msh2xml | .msi | .msp | .mst | .ops |
| .pcd | .pif | .plg | .prf | .prg |
| .reg | .scf | .scr | .sct | .shb |
| .shs | .sys | .ps1 | .ps1xml | .ps2 |
| .ps2xml | .psc1 | .psc2 | .tmp | .url |
| .vb | .vbe | .vbs | .vps | .vsmacros |
| .vss | .vst | .vsw | .vxd | .ws |
| .wsc | .wsf | .wsh | .xnk |  |

 You can *receive* any file attachment types, including those listed above.
These restrictions only apply to *sending* attachments.

---

# What counts as email consent?

> Learn what valid email permission looks like and why it matters.

Getting consent to send email isn’t just a legal requirement. It’s also essential for keeping your deliverability strong and your Resend account in good standing. This guide explains what valid email permission looks like, why it matters, and how to set it up properly.

## ​Why consent matters

 Many senders assume that if someone provides an email address, that automatically means it’s okay to email them. But that’s not always true and can often cause large-scale deliverability problems, especially for marketing or bulk messages. Mailbox providers like Gmail and Outlook closely monitor how recipients react to your emails, paying special attention to whether people mark your emails as spam. High complaint rates or low overall engagement signal that your messages weren’t wanted, which can hurt your reputation and lead to filtering, blocking, or delivery issues.

## ​Whatdoesn’tcount as permission

 These common methods are **not** considered valid:

- Including a clause in your Terms of Service that says users “agree to receive emails”
- Using a **pre-checked** box on your signup form for marketing messages
- Assuming someone is opted in unless they unsubscribe

 These approaches violate email best practices and don’t meet legal standards [like GDPR](https://gdpr-info.eu/art-7-gdpr/).

## ​Whatdoescount as permission

 Valid consent means the recipient **clearly and knowingly agreed** to receive the specific kind of email you’re sending. [According to GDPR](https://gdpr-info.eu/recitals/no-32/) (and general best practices), consent must be:

- **Freely given** – without pressure, bundling, or tricks
- **Specific** – clearly describes the type of messages the user will receive
- **Informed** – the user knows who you are and how you’ll use their data
- **Unambiguous** – requires an active opt-in (like checking a box)

 In other words, recipients should be able to consent to each message type from a particular sender.

## ​What happens if you send without consent?

 If you send to recipients who didn’t explicitly opt in, here’s what can happen:

1. Some of those people will **mark the message as spam**.
2. Mailbox providers may **block your mail or filter it to the spam folder**.
3. If your spam complaint or bounce rate remains high, [Resend may have topause or terminate your account](https://resend.com/legal/acceptable-use) to protect our sending reputation.

 And this applies *globally*, not just in the EU. Even if your emails are technically legal in your country, violating consent can lead to your mail being blocked or filtered to the spam folder.

## ​Best practice: Let people say “yes”

 The easiest way to get consent is to **ask for it clearly and separately**. Add an unchecked checkbox to your signup form, like this:

> Yes, I want to receive product updates and occasional marketing emails

 **Follow these best practices:**

- Keep it **optional** and **unchecked** by default
- Make the wording clear and specific
- Place it outside of your Terms of Service
- Include a one-click unsubscribe link in every email

 ![Example of a consent checkbox and unsubscribe link](https://mintcdn.com/resend/lyl6PQTYhtWhUjuS/images/what-counts-as-email-consent.jpeg?fit=max&auto=format&n=lyl6PQTYhtWhUjuS&q=85&s=db80d9ae5b8eae269c0f7237d0f92ef0)

## ​Still have questions?

 Following best practices helps everyone — your recipients, your deliverability, and the health of the email ecosystem. When you start with clear consent, your messages are the ones people are *glad* to receive. If you’re new to permission-based sending, please reach out to [Support](https://resend.com/help) and we’ll help you make sure everything’s on track.

---

# What email addresses to use for testing?

> Learn what email addresses are safe to use for testing with Resend

## ​Safe email addresses for testing

 When testing email functionality, it’s important to use designated test addresses to avoid unintended consequences like deliverability issues or spam complaints. Resend provides a set of safe email addresses specifically designed for testing, ensuring that you can simulate different email events without affecting your domain’s reputation.

### ​Why not use @example.com or @test.com?

 Many developers attempt to use domains like `@example.com` or `@test.com` for testing purposes. However, these domains are not designed for email traffic and often reject messages, leading to bounces. A high bounce rate can negatively impact your sender reputation and affect future deliverability. To prevent this, Resend blocks such addresses and returns a `422 Unprocessable Entity` error if you attempt to send to them.

### ​List of addresses to use

 To help you safely test email functionality, Resend provides the following test addresses, each designed to simulate a different delivery event:

| Address | Delivery event simulated |
| --- | --- |
| [email protected] | Email being delivered |
| [email protected] | Email bouncing |
| [email protected] | Email marked as spam |
| [email protected] | Email being suppressed |

 Using these addresses in your tests allows you to validate email flows without risking real-world deliverability problems. For more help sending test emails, see our [testing documentation](https://resend.com/docs/dashboard/emails/send-test-emails).

### ​Labeling support

 Most test email addresses support labeling, which enables you to send emails to the same test address in multiple ways. You can add a label after the `+` symbol to help track and differentiate between different test scenarios:

- `[email protected]`
- `[email protected]`
- `[email protected]`

 This is particularly useful for testing different email flows, tracking webhook responses, and matching responses with the specific email address that triggered the event. Whether you need to confirm that an email has been sent, track engagement events, or simulate a bounce scenario, these addresses provide a controlled and predictable way to test your email integration with Resend. The suppressed test email address does not support labeling yet

---

# What if an email says delivered but the recipient has not received it?

> Learn the steps to take when an email is delivered, but the recipient does not receive it.

Some emails may be marked as `Delivered` but not reach the recipient’s inbox due to various inbox sorting variables. This guide provides reasons for and advice on avoiding such issues.

## ​Why does this happen

 When an email is sent, it is marked as `Delivered` once the recipient server accepts it with a `250 OK` response. However, the server can then direct the email to the inbox, queue it for later, route it to the spam folder, or even discard it. This is done by major inbox providers (e.g., Gmail, Yahoo, Outlook), as well as by IT departments and individual users who set up firewalls or filtering rules. As a result, even though most legitimate emails should land in the intended inboxes, your message might end up in the spam/junk folder or, in rare cases, be deleted. **Inbox Providers do not share any information on how the messages are later filtered.** Resend is only notified about the initial acceptance and marks the email as `Delivered`. Any subsequent events (e.g., open/click events, unsubscribes) require recipient engagement.

## ​How to avoid this

### ​If you are in contact with the user

 The easiest way to solve this is by cooperating with the end user. If you have direct communication with the recipient, you can ask them to **check these places for your email**:

- Corporate spam filters or firewalls
- Personal inbox filtering
- Promotional, spam, or deleted folders
- Group inboxes or queues

 If they find it, ask them to mark the email as `Not Spam` or add your domain to an allowlist.

### ​If you are not in contact with the user

 Debugging without direct contact with the user is challenging. However, there are some optimizations that can **improve your chances of delivering to their inbox next time**:

- [Configure DMARC](https://resend.com/docs/dashboard/domains/dmarc) to build trust with the inbox provider
- Warm up new domains slowly before sending large volumes
- Change all links in your email to use your own domain (matching your sender domain)
- Turn off open and click tracking
- Reduce the number of images in your email
- Improve wording to be succinct, clear, and avoid spammy words

 We have an [extensive but practical deliverability guide](https://resend.com/docs/knowledge-base/how-do-i-avoid-gmails-spam-folder) that covers these topics in more detail.

---

# What if my domain is not verifying?

> Learn what steps to take when your domain doesn't seem to be verifying.

Verifying a domain involves a few steps:

1. Add your domain to Resend
2. Copy the required DNS records from Resend
3. Add these records to your DNS provider
4. Wait for verification to complete

 When this process is completed correctly, your domain will often verify within 15 minutes of adding the DNS records. What should you do if your domain isn’t verifying? If you are having any conflict issues with the `MX` records, [check out this
guide](https://resend.com/docs/knowledge-base/how-do-i-avoid-conflicting-with-my-mx-records).

## ​Common verification issues

 When your domain doesn’t verify as expected, it’s typically due to DNS configuration issues. This guide will help you troubleshoot and resolve common verification problems. Resend provides real-time DNS validation when viewing your domain details.
When viewing your domain, you’ll see specific error messages and visual
indicators highlighting any issues with your DNS records in case you’ve added
them incorrectly.

### ​Incorrect DNS records

 Usually when a domain doesn’t verify, it’s because the DNS records were not added correctly. Here’s how to check:

1. Confirm that you’ve added all required records (DKIM, SPF, and MX)
2. Verify that the records are added at the correct location (the `send` subdomain, not the root domain)
3. Check that record values match exactly what Resend generated for you
4. Look for red wavy underlines on the domain details page (these indicate specific DNS record errors)

 ![Check for errors in the domain details page](https://mintcdn.com/resend/bOYCnBDaGARkhUDn/images/domain-not-verifying-3.png?fit=max&auto=format&n=bOYCnBDaGARkhUDn&q=85&s=f86be9e2a150af3c29aca6c69689842a)

### ​DNS provider auto-appending domain names

 Some DNS providers automatically append your domain name to record MX values, causing verification failures. **Problem:** Your MX record appears as: `feedback-smtp.eu-west-1.amazonses.com.yourdomain.com` Instead of: `feedback-smtp.eu-west-1.amazonses.com` **Solution:** In your DNS provider, add a trailing period (dot) at the end of the record value: `feedback-smtp.eu-west-1.amazonses.com.` The trailing period tells your DNS provider that this is a fully qualified domain name that should not be modified. Note: The region your domain is added to is in this MX record. It may be
`us-east-1`, `eu-west-1`, `ap-northeast-1`, or `sa-east-1` depending on the
region.

### ​Nameserver conflicts

 If your domain’s DNS is managed in multiple places (e.g., Vercel, Cloudflare, your domain registrar), you might be adding records in the wrong location. **How to check:** Run a nameserver lookup for your domain using a tool like [dns.email](https://dns.email) to see which provider actually controls your DNS. Add the Resend records at that provider, not elsewhere.

### ​Region mismatch errors

 If your MX records point to a different AWS region than where your domain is configured, you’ll see a “region-mismatch” error. This happens when:

- Your domain is configured in one region (e.g., `us-east-1`)
- But your MX record points to a different region (e.g., `eu-west-1`)

 **Solution:** Update your MX record to match the region shown in your Resend domain configuration. The correct MX record value is displayed in the DNS records table on your domain details page.

### ​Multiple regions detected

 If you have multiple MX records pointing to different AWS regions, you’ll see a “multiple-regions” error. All MX records for a domain must point to the same region. **Solution:** Remove any MX records pointing to incorrect regions, keeping only the one that matches your domain’s configured region.

### ​DKIM record value mismatches

 The DKIM record must match exactly what Resend generated. Common mistakes include:

1. Adding extra quotes or spaces
2. Truncating long values
3. Adding SPF information to the DKIM record
4. Not copying the entire value

 Always copy and paste the exact value from Resend’s domain configuration page. If there’s a mismatch, you’ll see a red wavy underline on the incorrect value.

### ​DNS Propagation

 After adding or correcting your DNS records:

1. DNS changes can take up to 72 hours to propagate globally (though often much faster)
2. Use the “Restart verification” button in the Resend dashboard to trigger a fresh verification check
3. If verification still fails after 24 hours, use [dns.email](https://dns.email) to check if your records are visible publicly

## ​Need more help?

 If you’ve followed all the steps above and your domain still isn’t verifying, contact [Resend support](https://resend.com/help) with:

1. Your domain name
2. Screenshots of your DNS configuration

 Our team will help identify any remaining issues preventing successful verification.

Check your records in the browser

Tools like [dns.email](https://dns.email) allow you to check your DNS records in the browser.Go to this URL and replace `yourdomain.com` with the domain you added in Resend.![Check domain records with dns.email](https://mintcdn.com/resend/OWNnQaVDyqcGyhhN/images/domain-not-verifying-1.png?fit=max&auto=format&n=OWNnQaVDyqcGyhhN&q=85&s=0eb947321d0b35119432dab44d756260)You are looking to see the same values that you see in Resend.

Check your records in the terminal

Checking your DNS records in the terminal is just as easy. You can use the `nslookup` command and a record type flag to get the same information.Replace `yourdomain.com` with whatever you added as the domain in Resend:Check your DKIM `TXT` record:

```
nslookup -type=TXT resend._domainkey.yourdomain.com
```

Check your SPF `TXT` record:

```
nslookup -type=TXT send.yourdomain.com
```

Check your SPF `MX` record:

```
nslookup -type=MX send.yourdomain.com
```

![Check domain records with nslookup](https://mintcdn.com/resend/OWNnQaVDyqcGyhhN/images/domain-not-verifying-2.png?fit=max&auto=format&n=OWNnQaVDyqcGyhhN&q=85&s=e48a16939eebfc986f9216a2cfd49b08)You are looking to see the same values that you see in Resend.

---

# What is Resend Pricing

> Learn more about Resend's pricing plans.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

You can learn more about Resend’s pricing at [resend.com/pricing](https://resend.com/pricing).[Production Approval](https://resend.com/docs/knowledge-base/does-resend-require-production-approval)[Configuring TLS](https://resend.com/docs/knowledge-base/whats-the-difference-between-opportunistic-tls-vs-enforced-tls)⌘ I$/$

---

# What sending feature should I be using?

> How to pick between our different sending features depending on your number of recipients and the nature of the message.

How to pick between our different sending features depending on your number of recipients and the nature of the message.

---

# What's the difference between Opportunistic TLS vs Enforced TLS?

> Understand the different TLS configurations available.

Resend supports TLS 1.2, TLS 1.1 and TLS 1.0 for TLS connections. There are two types of TLS configurations available:

- Opportunistic TLS
- Enforced TLS

## ​What is Opportunistic TLS?

 Opportunistic TLS means that Resend always attempts to make a secure connection to the receiving mail server. If the receiving server does not support TLS, the fallback is sending the message unencrypted.

## ​What is Enforced TLS?

 Enforced TLS means that the email communication must use TLS no matter what. If the receiving server does not support TLS, the email will not be sent.

## ​Is Enforced TLS better than Opportunistic TLS?

 One strategy is not necessarily better than the other. The decision is less about one option being safe and the other being unsafe, and more about one option being safe and the other being safer. When you have Enforced TLS enabled, you might see an increase in bounce rates because some outdated mail servers do not support TLS. So it’s important to understand the different use cases for each configuration. If you’re sending sensitive information like authentication emails, you might want to use Enforced TLS. If you’re sending marketing emails, you might want to use Opportunistic TLS. In simple terms, with Opportunistic TLS, delivery is more important than security. On the other hand, with Enforced TLS, security is more important than delivery.

---

# Why are my emails landing on the Suppression List?

> Learn why your emails land on the Suppression List and how to remove them.

When sending to an email address results in a hard bounce, Resend places this address on the Suppression List. Emails placed on the list cannot be sent to until they are removed. We place emails on the Suppression List to protect domain reputation, both
yours and ours. Sending an email to a known hard bounce recipient can damage
domain reputation and affect email deliverability.

## ​Reasons emails are placed on the Suppression List

 Here are some possible reasons an email address is placed on the Suppression List:

- The recipient’s email address **contains a typo**.
- The recipient’s email address **doesn’t exist**.
- The recipient’s email server has **permanently blocked delivery**.
- The recipient has marked the delivery as spam.

## ​View email bounce details

 You can view the reason an email bounced on the [Emails](https://resend.com/emails) page:

1. Open the [Emails](https://resend.com/emails) page and search for the recipient’s email address in question.
2. Click on the email to view its details.
3. Hover over the `Bounced` status indicator to see a summary of the bounce reason.

 ![Email Bounce Notification](https://mintcdn.com/resend/OWNnQaVDyqcGyhhN/images/email-bounce-details-1.png?fit=max&auto=format&n=OWNnQaVDyqcGyhhN&q=85&s=f0f99293137b8de4a9862b05cfd87d74) For more technical details and suggested next steps, click the **See details** button. The drawer will open on the right side of your screen with the bounce type, subtype, and suggestions on how to proceed.

## ​What happens if you try sending to a recipient on the suppression list?

 Whenever you send an email with Resend, we check if the recipient is on the suppression list. If they are, we’ll [suppress](https://resend.com/docs/dashboard/emails/email-suppressions.mdx) the delivery to prevent damaging your sender reputation and our infrastructure.

## ​Removing an email address from the Suppression List

 You may be able to send a message to the same recipient in the future if the issue that caused the message to bounce is resolved and the email address is removed from the Suppression List. Remember, if you do not address the issue that caused the email to bounce, the
email address will return to the Suppression List the next time you attempt to
send to it. To remove your recipient from the Suppression List, click on the email in the [emails dashboard](https://resend.com/emails), and click **Remove from suppression list**. ![Email Bounced button](https://mintcdn.com/resend/OWNnQaVDyqcGyhhN/images/email-suppression-list-2.png?fit=max&auto=format&n=OWNnQaVDyqcGyhhN&q=85&s=baf9f0a40313b856be978b728fb1d01c)

---

# Why are my open rates not accurate?

> Learn why your open rate statistics are not accurate and what you can do about it.

## ​How are open rates tracked?

 A 1x1 pixel transparent GIF image is inserted in each email and includes a unique reference. When the image is downloaded, an open event is triggered.

## ​Why are my open rates not accurate?

 Open tracking is generally not accurate because each inbox handles incoming email differently. **Clipped messages in Gmail** happen when you send a message over 102KB. A message over this size won’t be counted as an open unless the recipient views the entire message. Resend’s Deliverability Insights on the email will note if a message exceeds this threshold. **Some inboxes do not download images by default** or block/cache assets with a corporate firewall. This approach can prevent the open event from being tracked. **Other inboxes open the email prior to delivering** in order to scan for malware or to [protect user privacy](https://www.apple.com/newsroom/2021/06/apple-advances-its-privacy-leadership-with-ios-15-ipados-15-macos-monterey-and-watchos-8/). This approach can trigger an open event without the recipient reading your email. **Emails sent with only a plain text version** will not include open tracking at all. Since open tracking relies on a 1x1 pixel image, plain text emails cannot trigger open events. Only emails with an HTML version can be tracked for opens. Because of this, open tracking is **not a statistically accurate way** of detecting if your users are engaging with your content.

## ​Does open tracking impact inbox placement?

 Though open tracking should not impact if your email is delivered, it most likely will impact your inbox placement. Trackers are generally **used by marketers and even spammers**. Because of this, inbox providers will often use open tracking as a signal that your email is promotional, or even spam, and categorize accordingly. **We suggest disabling open rates for transactional email**, to maximize inbox placement.

## ​What’s the alternative?

 Instead of relying on open rates, there are a few other ways to still understand your sending.

1. **Track Clicks:** Monitoring the link clicks is an even more granular way to know how a recipient engaged with your email. By knowing if they clicked, you also know that they read parts of your email and took action.
2. **Track Outside the Inbox:** Often emails are sent as a means to an end. Maybe it’s to increase page visits of an announcement or convert free users to paid. Tracking your sending by metrics outside of the inbox can be a great way to understand the true impact of your sending.

---

# Why and when to use Topics?

> Learn when to use Topics to improve deliverability and give recipients control over their email preferences.

Learn when to use Topics to improve deliverability and give recipients control over their email preferences.
