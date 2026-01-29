# How do I avoid Gmail's spam folder? and more

# How do I avoid Gmail's spam folder?

> Learn how to improve inbox placement in Gmail.

This guide is adapted from Google’s article to [Prevent mail from being
blocked or sent to
spam](https://support.google.com/mail/answer/81126?hl=en&vid=1-635789122382665739-3305764358&sjid=4594872399309427672-NA#thirdparty)

## ​Authenticate Your Email

 All communication is built on trust, and email is no different. When you send an email, you want to be sure that the recipient (and Gmail) knows who you are and that you are a legitimate sender. Email authentication is a way to prove that an email is really from you. It also helps to prevent your email from being spoofed or forged.

| Authentication | Requires Setup | Purpose |
| --- | --- | --- |
| SPF | No | Proves you are allowed to send from this domain |
| DKIM | No | Proves your email originated from you |
| DMARC | Yes | Proves you own the domain and instructs how to handle spoofs |
| BIMI | Yes | Proves you are the brand you say you are |

 **SPF** and **DKIM** are baseline requirements for all sending which is why both are automatically setup when you verify your domain with Resend. [DMARC](https://resend.com/docs/dashboard/domains/dmarc) and [BIMI](https://resend.com/docs/dashboard/domains/bimi) are both additional authentication methods that can build trust and further improve inbox placement. **Action Items**

1. [Setup DMARC](https://resend.com/docs/dashboard/domains/dmarc) for your domain
2. [Setup BIMI](https://resend.com/docs/dashboard/domains/bimi) for your domain

## ​Legitimize Your Domain

 Gmail is using many methods to identify who you are as a sender, and one way they do that is by looking at your domain. You should make sure that the domain you send with is the same domain where your website is hosted. If you send from `@example.com` but your website is hosted at `example.net`, Gmail won’t be able to use your site to help legitimize you. You can regularly check if your domain is listed as unsafe with [Google Safe Browsing](https://transparencyreport.google.com/safe-browsing/search?hl=en) to make sure Google isn’t classifying your domain as suspicious. **Action Items**

1. Host your website at the domain that you send from (especially for new domains)
2. Check if your domain is listed as unsafe with [Google Safe Browsing](https://transparencyreport.google.com/safe-browsing/search?hl=en)

## ​Manage your Mailing List

 Gmail monitors your sending across all Gmail inboxes to see if recipients want to receive your emails. This is mainly measured by their engagement with your messages (opens, clicks, replies). If Gmail doesn’t see this engagement, they will start to move your inbox placement towards promotional or even spam. It would seem like adding open and click tracking would be ideal to gather this information, but this has been seen to negatively impact your inbox placement. Instead, focus on sending to recipients who want to receive your emails. **Prevent sending to recipients who**:

- Didn’t ask to be sent to (opt-in)
- Show no signs of engagement with your emails or product
- Requested to be unsubscribed
- Marked your emails as spam (complained)
- Never received your email (bounced)

 **Action Items**

1. Make it easy to opt-out to your emails (including the [Unsubscribe Headers](https://resend.com/docs/dashboard/emails/add-unsubscribe-to-transactional-emails))
2. Use [Webhooks](https://resend.com/docs/webhooks/introduction) to remove bounced or complained recipients from your list
3. Use [Gmail’s Postmaster Tool](https://support.google.com/mail/answer/9981691?sjid=4594872399309427672-NA&visit_id=638259770782293948-1913697299&rd=1) to monitor your spam reports

## ​Monitor Affiliate Marketers

 Affiliate marketing programs offer rewards to companies or individuals that send visitors to your website. However, spammers can take advantage of these programs. If your brand is associated with marketing spam, other messages sent by you might be marked as spam. We recommend you regularly monitor affiliates, and remove any affiliates that send spam. **Action Items**

1. Monitor your affiliate marketers for any spam

## ​Make Content People Want to Read

 Trust is not only built with the domain, but also in the message. Sending content that people want to read and that is not misleading will help build trust with Gmail. A few good rules for content:

- Less is more (keep it simple and to the point)
- Plain text over complex HTML
- Links should be visible and match the sending domain
- No content should be hidden or manipulative

 **Action Items**

1. Reduce and simplify your email content
2. Make sure your links are using your sending domain

## ​Establish Sending Patterns

 This is especially true for new domains since Gmail doesn’t have any history of trust. Sending a large volume of emails from a new domain will likely result in poor inbox placement. Instead, start small and build up your sending volume over time. A great way to start is by sending regular person-to-person email with your gmail account. These messages will have high engagement and built trust quickly, which will carry over when you start integrating with a sending service like Resend. It can also be very helpful to segment your sending by sending address to give Gmail more indication of what type of sending you are doing. This allows Gmail to place your emails in the correct inbox tab (Primary, Promotions, etc.). Some examples of helpful email addresses:

- **Personal emails** should come from an address with a name like [marissa@domain.com](mailto:marissa@domain.com)
- **Transactional emails** should come from an address like [notifications@domain.com](mailto:notifications@domain.com)
- **Marketing emails** should come from an address like [updates@domain.com](mailto:updates@domain.com).

 **Action Items**

1. Send emails from your gmail account before sending transactional
2. Send transactional emails before sending marketing emails
3. Choose dedicated sending addresses for each type of email

## ​Summary

 Email deliverability is overwhelming. One way to simplify it is to think: **what would a phisher do?** **Then do the opposite!** Gmail’s goal is to only show emails that their users want to see and malicious emails are at the very bottom of the list. Reverse engineer phishing sending habits and consider how you could prove to Gmail at each step that you clearly have no malicious intent. Anything we missed? [Let us know](https://resend.com/help).

---

# How do I avoid Outlook's spam folder?

> Learn how to improve inbox placement in Outlook.

This guide is adapted from Microsoft’s article to [Improve your spam
reputation](https://support.microsoft.com/en-us/office/sender-support-in-outlook-com-05875e8d-1950-4d89-a5c3-adc355d0d652).
For high-volume senders (5,000+ messages per day), see [Microsoft’s bulk
sending requirements for
2025](https://resend.com/blog/microsoft-bulk-sending-requirements-2025).

- **Set up email authentication**. Configure [SPF, DKIM, and DMARC](https://resend.com/docs/dashboard/domains/introduction) for your domain. This is required for bulk senders (5,000+ messages per day) and strongly recommended for all senders.
- **Add your sender name**. Set your `from` like this: `"Name <name.domain.com>"`.
- **Engage with your own email**. Send an email to yourself, open it, and reply to it.
- **Add yourself as a contact**. See how to add contacts in [Outlook.com](https://support.microsoft.com/en-us/office/create-view-and-edit-contacts-and-contact-lists-in-outlook-com-5b909158-036e-4820-92f7-2a27f57b9f01).
- **Ask your recipients to add you in their contacts**. This can be done in [Outlook](https://support.microsoft.com/en-us/office/add-recipients-of-my-email-messages-to-the-safe-senders-list-be1baea0-beab-4a30-b968-9004332336ce) or [outlook.com](https://support.microsoft.com/en-us/office/safe-senders-in-outlook-com-470d4ee6-e3b6-402b-8cd9-a6f00eda7339).
- **Don’t blast to a BCC list**. Send separate emails if you are sending to a large number of recipients.
- **Prevent over sending**. Limits are impacted by historical engagements and sending volumes, but you should be hesitant to send too many emails at once. If you think this is an issue, reduce the frequency or volume.
- **Send to engaged recipients**. Don’t keep sending if there is no engagement from your recipients. This is especially true if a recipient has requested to unsubscribe or an address is bouncing. Keep spam complaint rates under 0.3%.
- **Include an unsubscribe option**. For bulk emails, include a clearly visible unsubscribe link. Consider implementing [one-click unsubscribe](https://resend.com/docs/dashboard/emails/add-unsubscribe-to-transactional-emails) for the best user experience.
- **Limit use of HTML**. Keep emails as close to plain text as possible.

---

# How do I create an email address or sender in Resend?

> Learn how sending from an email address works on Resend.

Resend does **not** require you to “create an email address”, “set up a sender identity”, or “add a from-address” before sending. Once a domain is verified in your Resend account, you can send from **any** email address at that domain. The email address you send from does **not** need to exist in another system.
However, we recommend using addresses that can receive replies.

## ​Common misconceptions

 Some platforms require you to create, register, or pre-approve a sending address.

Resend does **not**. After verifying your domain, you’re free to send from any address **@yourdomain**, with no extra setup, creation, or configuration of that address.

## ​Getting started

 To start sending emails with Resend:

1. [Sign up for a Resend account](https://resend.com/signup)
2. [Add and verify your domain](https://resend.com/domains)
3. [Create an API key](https://resend.com/api-keys)
4. Start sending emails immediately from any address at the domain you verified

 If you’re having trouble with domain verification or DNS records, see our [domain verification troubleshooting guide](https://resend.com/docs/knowledge-base/what-if-my-domain-is-not-verifying) or check our [DNS setup guides](https://resend.com/docs/knowledge-base/introduction) for your specific DNS provider.

---

# How do I ensure sensitive data isn't stored on Resend?

> Information on how we can help you protect your customer's information.

Resend can turn off message content storage for teams with additional compliance requirements. This is available to customers who meet the following criteria:

1. The team has been a Resend Pro or Scale subscriber for at least 1 month.
2. The team is sending from a domain with an active website.
3. The team has sent over 3,000 emails with a < 5% bounce rate.

 This feature requires a $50/mo add-on. If your account meets these requirements and you would like this turned on, contact our support team for help.

---

# How do I fix CORS issues?

> Information on recommended options to avoid CORS errors when sending emails.

## ​Problem

 It’s common for people to hit CORS (Cross-Origin Resource Sharing) issues when using the Resend API. This error typically shows as:

```
Access to XMLHttpRequest at 'https://api.resend.com/emails'
from origin 'http://localhost:3000' has been blocked by CORS policy:
Response to preflight request doesn't pass access control check:
No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

## ​Solution

 Usually CORS errors happens when you’re sending emails from the **client-side**. We recommend you to send the emails on the **server-side** to not expose your API keys and avoid CORS issues.

---

# How do I maximize deliverability for Supabase Auth emails?

> Everything you should do before you start sending authentication emails with Resend and Supabase.

If you haven’t yet, [configure your own Supabase
integration](https://resend.com/settings/integrations)! Below are **five steps to improve the deliverability of your authentication emails**. Prefer watching a video? Check out our video walkthrough below.

## ​1. Setup a custom domain on Supabase

 By default, Supabase generates a `supabase.co` domain for your project, and uses that domain for the links in your authentication emails (e.g., verify email, reset password). Once you are ready to go live, though, it is important to setup a custom domain. The key benefit here is to align the domains used in your `from` address and the links in your emails. Especially for something as sensitive as email verification and magic links, **giving confidence to the inbox providers that the origin of the email and the links in the body are the same** can be very impactful. This changes your links from:

```
https://039357829384.supabase.co/auth/v1/{code}
```

 To something like this:

```
https://auth.yourdomain.com/auth/v1/{code}
```

 Supabase has a helpful guide for [Setting up a custom domain](https://supabase.com/docs/guides/platform/custom-domains).

## ​2. Setup a dedicated subdomain

 There are many benefits to using a subdomain vs your root domain for sending, one being that you can isolate the reputation of the subdomain from your root domain. For authentication emails, using a subdomain is particularly helpful because it is a way to **signal your intention to the inbox provider**. For example, if you use `auth.yourdomain.com` for your authentication emails, you are communicating to the inbox provider that all emails from this subdomain are related to sending authentication emails. This clarity is essential because it helps the inbox provider understand that this subdomain is not used for sending marketing emails, which are more likely to be marked as spam. If you don’t want a subdomain just for auth, you can also achieve this by
establishing one subdomain for all your transactional emails (e.g.,
`notifications.yourdomain.com`). To add a subdomain to Resend, you can [add it as a domain on the dashboard](https://resend.com/domains). ![Create auth subdomain](https://mintcdn.com/resend/OWNnQaVDyqcGyhhN/images/kb-create-auth-subdomain.png?fit=max&auto=format&n=OWNnQaVDyqcGyhhN&q=85&s=3d0629c74757298069867f0019e69a90)

## ​3. Disable link and open tracking

 Link and open tracking can be great for marketing emails but not for transactional emails. This kind of **tracking can actually hurt your deliverability**. Open tracking embeds a 1x1 pixel image in the email, and link tracking rewrites the links in the email to point to Resend’s servers first. Both types can be seen as suspicious by the inbox provider and hurt your deliverability. Also, Supabase has noted that link tracking is [known for corrupting verification links](https://supabase.com/docs/guides/platform/going-into-prod), making them unusable for your users. You can disable link and open tracking by clicking on your domain and disabling at the bottom. ![Disable link and open tracking](https://mintcdn.com/resend/OWNnQaVDyqcGyhhN/images/kb-disable-tracking.png?fit=max&auto=format&n=OWNnQaVDyqcGyhhN&q=85&s=1deeae548895ad4047ca7283faad95c6)

## ​4. Prepare for link scanners

 Some inbox providers or enterprise systems have email scanners that run a `GET` request on all links in the body of the email. This type of scan can be problematic since Supabase Auth links are single-use. To get around this problem, consider altering the email template to replace the original magic link with a link to a domain you control. The domain can present the user with a “Sign-in” button, which redirects the user to the original magic link URL when clicked.

## ​5. Setup DMARC

 Like our human relationships, email deliverability is built on trust. The more inboxes can trust your emails, your domain, and your sending, the more likely your emails will be delivered to the inbox. This makes [Email Authentication a critical pillar](https://resend.com/blog/email-authentication-a-developers-guide) in the journey to excellent deliverability. That is where DMARC comes in. As the industry standard for email authentication, **DMARC is a way to tell the inbox provider that you are who you say you are**. It is a way to signal to the inbox provider that you are a legitimate sender and that your emails should be delivered to the inbox. Following security best practices like DMARC will show your validity and authenticity. ![DMARC policy details](https://mintcdn.com/resend/OWNnQaVDyqcGyhhN/images/kb-dmarc.png?fit=max&auto=format&n=OWNnQaVDyqcGyhhN&q=85&s=2b853e7501c2863ddd2ded6de271e0b6) You can use our [DMARC setup guide to get started](https://resend.com/docs/dashboard/domains/dmarc).

---

# How do I send with an avatar?

> Learn how to show your avatar in the inbox of your recipients.

[Recent studies](https://www.businesswire.com/news/home/20210720005361/en/Red-Sift-and-Entrust-Survey-Showing-a-Logo-Positively-Affects-Consumer-Interaction-With-Emails-Open-Rates-Buying-Behavior-Brand-Recall-and-Confidence) are showing meaningful benefits of displaying your logo in the inbox:

- Increases brand recall by 18%.
- Improves open rate by 21%.
- Boosts purchase likelihood by 34%.
- Reinforces confidence in email by 90%.

 ![Email with an avatar](https://mintcdn.com/resend/OWNnQaVDyqcGyhhN/images/sender-avatar.png?fit=max&auto=format&n=OWNnQaVDyqcGyhhN&q=85&s=af9242870f3967aaed057cb3f5f44c20)

## ​Gmail

 Follow these steps to add an avatar to your Gmail inbox:

1. Go to your [Google Account Settings](https://myaccount.google.com/personal-info)
2. Upload a profile picture

 Avatars in Gmail only display in the mobile app (including in push notifications) and inside opened emails on desktop.

## ​Outlook

 Follow these steps to add an avatar to your Outlook inbox:

1. Go to your [Outlook Profile Settings](https://account.microsoft.com/profile/)
2. Upload a profile picture

 Avatars in Outlook only display in the mobile app and inside opened emails on desktop.

## ​Yahoo

 Follow these steps to add an avatar to your Yahoo inbox:

1. Go to your [Yahoo Account Setting](https://login.yahoo.com/account/personalinfo)
2. Upload a profile picture

 Avatars in Yahoo only display in the mobile app and inside an opened email on desktop.

## ​Apple Mail

 Apple Mail only shows avatars if recipients have added images to contacts. Alternatively, you can set up [Apple Branded Mail](https://resend.com/docs/knowledge-base/how-do-i-set-set-up-apple-branded-mail), a proprietary Apple format introduced with iOS 18.2 that displays your logo as an avatar in the inbox of Apple Mail, or [set up BIMI](https://resend.com/docs/dashboard/domains/bimi#what-is-bimi) with a Verified Mark Certificate.

## ​Using Gravatar

 Some inbox service providers or email clients (e.g. Thunderbird, Airmail, and Postbox) rely on [Gravatar](https://gravatar.com/) to display an image. You can set up a free Gravatar account, add your avatar, and verify your addresses you’re sending from to that account to have your avatar displayed.

## ​Limitations

 Almost every email provider has its own way of adding a profile picture to an inbox. This means **you can only**:

1. Add your avatar to a real inbox, limiting it only to that provider
2. Send mail from the same address that you set the avatar on

 The way around this is [BIMI (Brand Indicators for Message Identification)](https://resend.com/docs/dashboard/domains/bimi). BIMI now supports Common Mark Certificates (CMC) in addition to Verified Mark Certificates (VMC), making it more accessible. It is supported by nearly all major providers and allows you to send from any address on that domain. Need assistance setting up BIMI? [We can help](https://resend.com/help).

---

# How do I set up Apple Branded Mail?

> Learn how to implement Apple Branded Mail to display your logo in Apple Mail clients.

## ​Prerequisites

 To get the most out of this guide, you will need to:

- [Create an Apple Business Connect account](https://www.apple.com/business/connect/)
- [Setup DMARC on your domain](https://resend.com/docs/dashboard/domains/dmarc)
- A company identification number for Apple to verify your company

 Prefer watching a video? Check out our video walkthrough below.

## ​What is Apple Branded Mail?

 Apple Branded Mail is a proprietary Apple format that displays your logo as an avatar in the inbox of Apple Mail. Displaying your logo can increase brand recognition and trust and improve engagement. There are a few benefits of Apple Branded mail over BIMI:

- Since it’s an Apple format, it does not require a certificate like [BIMI does](https://resend.com/docs/dashboard/domains/bimi).
- The image support is broader, supporting `.png`, `.heif`, and `.jpg` logos.

 Since Apple Branded Mail works only with Apple Mail on new iOS, iPadOS, and macOS versions, your logo will not show in other mail clients or older versions of Apple Mail. For this reason, we recommend following all possible methods for adding your logo to your emails, including Apple Branded Mail, [our general guide](https://resend.com/docs/knowledge-base/how-do-i-send-with-an-avatar), and [BIMI](https://resend.com/docs/dashboard/domains/bimi) if it fits your needs.

## ​Implementing Apple Branded Mail

### ​1. Configure DMARC

 If you haven’t set up DMARC yet, follow our [DMARC Setup
Guide](https://resend.com/docs/dashboard/domains/dmarc). To ensure your logo appears with Apple Branded Mail, set your DMARC policy to either `p=quarantine;` or `p=reject;`. This policy guarantees that your emails are authenticated and prevents others from spoofing your domain and sending emails with your logo. Here’s an overview of the required parameters:

| Parameter | Purpose | Required Value |
| --- | --- | --- |
| p | Policy | p=quarantine;orp=reject; |
| pct | Percentage | pct=100; |

 Here is an example of an adequate DMARC record:

```
"v=DMARC1; p=quarantine; pct=100; rua=mailto:[email protected]"
```

 As we mention in our [DMARC Setup Guide](https://resend.com/docs/dashboard/domains/dmarc), be sure to test your emails to make sure they are passing DMARC before changing your DMARC policy to `p=quarantine;` or `p=reject;`.

### ​2. Create an Apple Business Connect account

 Apple displays the logo you set in your Business Connect account. [Create an account](https://www.apple.com/business/connect/) if your company does not already have one. Make sure to use your company details when signing up.

### ​3. Add your company details

 Apple will prompt you to provide details like your company address and name.

### ​4. Add your brand details

 Once your company account is created, in Apple Business Connect, select the **Branded Mail** option in the left sidebar and provide details on your brand. Add details like the brand name and your brand website. ![Add your brand details](https://mintcdn.com/resend/ABWmVTZIHGIFNTFD/images/abm-step-4-add-brand-details-1.png?fit=max&auto=format&n=ABWmVTZIHGIFNTFD&q=85&s=8348f2b44a70bfb6c4e065046a7443dd) ![Add your brand details](https://mintcdn.com/resend/ABWmVTZIHGIFNTFD/images/abm-step-4-add-brand-details-2.png?fit=max&auto=format&n=ABWmVTZIHGIFNTFD&q=85&s=8ae25d711442f1f38620bd0aa1996fee)

### ​5. Add your logo

 Once you fill out the brand details, upload your logo. Apple requires the logo to be at least 1024 x 1024 px in a `.png`, `.heif`, or `.jpeg` format. ![Add your logo](https://mintcdn.com/resend/ABWmVTZIHGIFNTFD/images/abm-step-5-add-your-logo.png?fit=max&auto=format&n=ABWmVTZIHGIFNTFD&q=85&s=325d6466f5c237cd8c478eba3ac746d5)

### ​6. Add your domain

 Confirm the domains or email addresses where you want your brand logo to appear. You can register your logo for your root domain or a subdomain. If you don’t set a specific logo for a subdomain, the root domain logo will automatically display for any email sent from your subdomains.

### ​7. Verify your company

 Apple requires details to confirm your company identity. If you’re in the United States, provide a Federal Taxpayer Identification Number. Other countries will use a local equivalent for this step. Apple also asks that you add a DNS record to verify DNS access.

### ​8. Verify with Apple

 After you submit all your information, Apple will verify your details. This process may take up to seven business days. Once the logo is verified, Apple will send an email notification and note the verified status in Branded Mail. Your logo will start to display in compatible Apple Mail versions. ![Verified logo](https://mintcdn.com/resend/PWWYUiKcsGOVT_Rs/images/abm-step-8-verify-with-apple.png?fit=max&auto=format&n=PWWYUiKcsGOVT_Rs&q=85&s=bbf80629357b9a4df827d9911677b97d) See Apple’s documentation on [Apple Branded
Mail](https://support.apple.com/en-au/guide/apple-business-connect/abcb761b19d2/web)
for any detailed questions on adding your logo.

---

# How to Handle API Keys

> Learn our suggested practices for handling API keys.

API Keys are secret tokens used to authenticate your requests. They are unique to your account and should be kept confidential. You can create API keys in two ways:

- [via the Resend Dashboard](https://resend.com/docs/dashboard/api-keys/introduction)
- [via the API](https://resend.com/docs/api-reference/api-keys/create-api-key)

 For more help creating, deleting, and managing API keys, see the [API Keys
documentation](https://resend.com/docs/dashboard/api-keys/introduction).

## ​Best Practices

 It’s crucial you handle your API keys securely. Do not share your API key with others or expose it in the browser or other client-side code. Here are some general guidelines:

- Store API keys in environment variables.
- Never commit API keys to version control.
- Never hard-code API keys in your code or share them publicly.
- Rotate API keys regularly. If an API key hasn’t been used in the last 30 days, consider deleting it to keep your account secure.

 When you create an API key in Resend, you can view the key only once. This
practice helps encourage these best practices.

## ​Example

 Many programming languages have built-in support for environment variables. Here’s an example of how to store an API key in an environment variable in a Node.js application. 1

Create an environment variable

Once you create the API key, you can store it in an environment variable in a `.env` file..env

```
RESEND_API_KEY = 're_xxxxxxxxx';
```

2

Add the file to your gitignore

Add the `.env` file to your `.gitignore` file to prevent it from being committed to version control. Many frameworks already add `.env` to the `.gitignore` file by default..gitignore

```
.env
```

3

Use the environment variable in your code

app.ts

```
const resend = new Resend(process.env.RESEND_API_KEY);
```

The environment variables in your `.env` file will *not* be available automatically. You *must* load them. On Node.js `v20` and later, you can pass your `.env` file’s variables to your script using the `--env-file=.env` flag. Alternatively, you can use the `dotenv` package to load the variables.

---

# Introduction

> A collection of answers to frequently asked questions.

[Can I receive emails with Resend?Learn how to receive emails with Resend](https://resend.com/docs/dashboard/receiving/introduction)[How do Dedicated IPs Work?Learn how Dedicated IPs work and how to request them.](https://resend.com/docs/knowledge-base/how-do-dedicated-ips-work)[How do I avoid conflicts with my MX records?Learn how to avoid conflicts with your existing MX records when setting up a
Resend domain.](https://resend.com/docs/knowledge-base/how-do-i-avoid-conflicting-with-my-mx-records)[How do I avoid Gmail's spam folder?Learn how to improve inbox placement in Gmail.](https://resend.com/docs/knowledge-base/how-do-i-avoid-gmails-spam-folder)[How do I avoid Outlook's spam folder?Learn how to improve inbox placement in Outlook.](https://resend.com/docs/knowledge-base/how-do-i-avoid-outlooks-spam-folder)[How do I ensure sensitive data isn't stored on Resend?Information on how we can help you protect your customer’s information.](https://resend.com/docs/knowledge-base/how-do-i-ensure-sensitive-data-isnt-stored-on-resend)[How do I fix CORS issues?Information on recommended options to avoid CORS errors when sending emails.](https://resend.com/docs/knowledge-base/how-do-i-fix-cors-issues)[How do I maximize deliverability for Supabase Auth emails?Everything you should do before you start sending authentication emails with
Resend and Supabase.](https://resend.com/docs/knowledge-base/how-do-i-maximize-deliverability-for-supabase-auth-emails)[How do I send with an avatar?Learn how to show your avatar in the inbox of your recipients.](https://resend.com/docs/knowledge-base/how-do-i-send-with-an-avatar)[Is it better to send emails from a subdomain or the root domain?Discover why sending emails from a subdomain can be better than using a root
domain.](https://resend.com/docs/knowledge-base/is-it-better-to-send-emails-from-a-subdomain-or-the-root-domain)[What if an email says delivered but the recipient hasn't received it?Learn the steps to take when an email is delivered, but the recipient does not
receive it.](https://resend.com/docs/knowledge-base/what-if-an-email-says-delivered-but-the-recipient-has-not-received-it)[What if my domain is not verifying?Learn what steps to take when your domain doesn’t seem to be verifying.](https://resend.com/docs/knowledge-base/what-if-my-domain-is-not-verifying)[What is Resend Pricing?Learn more about Resend’s pricing plans.](https://resend.com/docs/knowledge-base/what-is-resend-pricing)[Why are my open rates not accurate?Learn why your open rate statistics are not accurate and what you can do about
it.](https://resend.com/docs/knowledge-base/why-are-my-open-rates-not-accurate)[How can I delete my Resend account?Learn how to permanently delete your Resend account and data.](https://resend.com/docs/knowledge-base/how-can-i-delete-my-resend-account)[Should I add an unsubscribe link to all of my emails sent with Resend?Learn when to add unsubscribe links to your transactional and marketing
emails.](https://resend.com/docs/knowledge-base/should-i-add-an-unsubscribe-link)[Why are my emails landing on the suppression list?Learn why your emails land on the suppression list, and how to remove them.](https://resend.com/docs/knowledge-base/why-are-my-emails-landing-on-the-suppression-list)

---

# IONOS

> Verify your domain on IONOS with Resend.

## ​Add Domain to Resend

 First, log in to your [Resend Account](https://resend.com/login) and [add a domain](https://resend.com/domains). ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-add-domain.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=418dd93c2f2ead0b0d83d1b7c2fb0970) It is [best practice to use a
subdomain](https://resend.com/docs/knowledge-base/is-it-better-to-send-emails-from-a-subdomain-or-the-root-domain)
(updates.example.com) instead of the root domain (example.com). Using a
subdomain allows for proper reputation segmentation based on topics or purpose
(e.g. marketing) and is especially important if receiving emails with Resend.

## ​Log in to IONOS

 Log in to your [IONOS account](https://my.ionos.com/domains):

1. Choose your Domain from the `Domain` list.
2. Select the `DNS` tab to get to the page to manage DNS records.

 ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-ionos-domains.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=ad87e97d0b64b83ef7076abdcca7f032)

## ​Add MX SPF Record

 Select “Add record” on IONOS to copy and paste the values MX from Resend.

1. On the `Add a DNS Record` page, select `MX`.
2. Type `send` for the `Name` of the record.
3. Copy the MX Value from Resend into the `Points to` field.
4. Use the default `Priority` of `10`.
5. Use the default TTL of `1 hour`.
6. Select `Save`.

 Omit your domain from the record values in Resend when you paste. Instead of
`send.example.com`, paste only `send` (or `send.subdomain` if you’re using a
subdomain). ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-spf-mx.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=bb0db2dd2809135194cfb62b695225cd) ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-ionos-spf-mx.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=1769321e813bf9a6d6ebe30105d1dc43) Below is a mapping of the record fields from Resend to IONOS:

| IONOS | Resend | Example Value |
| --- | --- | --- |
| Type | Type | MX Record |
| Name | Name | send |
| Points to | Value | feedback-smtp.us-east-1.amazonses.com |
| TTL | TTL | 1 hour |
| Priority | Priority | 10 |

 Do not use the same priority for multiple records. If Priority `10` is already
in use on another record, try a higher value `20` or `30`.

## ​Add TXT SPF Record

 In the same section, select “Add record” again.

1. On the `Add a DNS Record` page, select `TXT`.
2. Type `send` for the `Host name` of the record.
3. Copy the TXT Value Resend into the `TXT value` field.
4. Use the default TTL of `1 hour`.
5. Select `Save`.

 Omit your domain from the record values in Resend when you paste. Instead of
`send.example.com`, paste only `send` (or `send.subdomain` if you’re using a
subdomain). ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-spf-txt.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=747425d0a224baeee2846c9a707d5bbc) ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-ionos-spf-txt.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=b41183957e0b51879bf42e16f1927f91) Below is a mapping of the record fields from Resend to IONOS:

| IONOS | Resend | Example Value |
| --- | --- | --- |
| Type | Type | TXT Record |
| Host name | Name | send |
| TXT value | Value | "v=spf1 include:amazonses.com ~all" |
| TTL | - | 1 hour |

## ​Add TXT DKIM Records

 In the same section, select “Add record” again.

1. On the `Add a DNS Record` page, select `TXT`.
2. Type `resend._domainkey` for the `Host name` of the record.
3. Copy the record value from Resend into the `TXT value` field.
4. Use the default TTL of `1 hour`.
5. Select `Save`.

 Omit your domain from the record values in Resend when you paste. Instead of
`resend._domainkey.example.com`, paste only `resend._domainkey` (or
`resend._domainkey.subdomain` if you’re using a subdomain). ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-dkim.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=345d1dc6b7c138dbd92bd6928c634bd9) ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-ionos-dkim-txt.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=f824ef363e11048dd685cf8afad2cf53) Below is a mapping of the record fields from Resend to IONOS:

| IONOS | Resend | Example Value |
| --- | --- | --- |
| Type | Type | TXT Record |
| Host name | Name | send |
| TXT value | Value | p=example_demain_key_value |
| TTL | - | 1 hour |

## ​Receiving Emails

 If you want to receive emails at your domain, toggle the “Receiving” switch on the domain details page. ![Enable Receiving Emails for a verified domain](https://mintcdn.com/resend/B7wTVm7aKL5pNT-6/images/inbound-domain-toggle.png?fit=max&auto=format&n=B7wTVm7aKL5pNT-6&q=85&s=46f6b4c142fb90e04b57861e338ed2d0) When you enable Inbound on a domain, Resend receives *all emails* sent to that
specific domain depending on the priority of the MX record. For this reason,
we strongly recommend verifying a subdomain (`subdomain.example.com`) instead
of the root domain (`example.com`). Learn more about [avoiding conflicts with
your existing MX
records](https://resend.com/docs/knowledge-base/how-do-i-avoid-conflicting-with-my-mx-records). Select “Add record” on IONOS:

1. On the `Add a DNS Record` page, select `MX`.
2. Type `inbound` (or whatever your subdomain is) for the `Name` of the record.
3. Copy the MX Value from Resend into the `Points to` field.
4. Use the default `Priority` of `10`.
5. Use the default TTL of `1 hour`.
6. Select `Save`.

 Below is a mapping of the record fields from Resend to IONOS:

| IONOS | Resend | Example Value |
| --- | --- | --- |
| Type | Type | MX Record |
| Name | Name | inbound |
| Points to | Content | inbound-smtp.us-east-1.amazonaws.com |
| TTL | TTL | 1 hour |
| Priority | Priority | 10 |

 After verifying your domain, create a webhook to process incoming emails. For help setting up a webhook, how to access email data and attachments, forward emails, and more, see [our guide on receiving emails with Resend](https://resend.com/docs/dashboard/receiving/introduction).

## ​Complete Verification

 Now click [Verify DNS Records](https://resend.com/domains) on your Domain in Resend. It may take a few hours to complete the verification process (often much faster).

## ​Troubleshooting

 If your domain is not successfully verified, these are some common troubleshooting methods.

Resend shows my domain verification failed.

Review the records you added to IONOS to rule out copy and paste errors.

It has been longer than 72 hours and my domain is still Pending.

[Review our guide on a domain not verifying](https://resend.com/docs/knowledge-base/what-if-my-domain-is-not-verifying).

---

# Is it better to send emails from a subdomain or the root domain?

> Discover why sending emails from a subdomain can be better than using a root domain.

We recommend sending emails from a subdomain (`notifications.acme.com`) instead of your root/apex domain (`acme.com`). There are **two main goals you should achieve with your domain setup**:

- Reputation Isolation
- Sending Purpose Transparency

## ​Reputation Isolation

 Things happen. Maybe someone decides to DDOS your signup page and you get stuck sending tens of thousands of bounced verification emails to burner addresses. Or maybe a cold outreach campaign gets out of hand and your sending gets pegged as spam. Whatever it is, you want to be consistently hedging your reputation. One way to do this is by not using your root domain. This allows you to quarantine a compromised subdomain if needed. If your root domain ends up with a jeopardized reputation, it can be a long road to recovery.

## ​Sending Purpose Transparency

 All of us want all of our emails to go right to the top of the priority folder of the inbox, but the reality is, not all of our email should. A password reset email should have higher priority than a monthly product update. Inbox providers like Outlook and Gmail are constantly trying to triage incoming mail to put only the most important stuff in that priority spot, and move the rest towards Promotional or even Spam. By segmenting your sending purposes by subdomain, you are giving Inbox Providers clear indication of how they should place your emails, which will build trust and confidence.

## ​Avoid “Lookalike” Domains

 Never use domains that look like your main brand but aren’t actually your main brand. These brand-adjacent domains like `getacme-mail.com` or `acme-alerts.com` can appear suspicious to spam filters and confusing to your recipients. Inbox providers may flag them as phishing or spoofing attempts, and your users are more likely to ignore, delete, or even report the emails as spam. If you’re launching a new project or sending for a different purpose, again use a subdomain of your main domain. Sticking with clear, consistent subdomains helps reinforce your brand identity and builds trust with inbox providers and recipients alike. We cover this in depth in our [deliverability
guide](https://resend.com/docs/knowledge-base/how-do-i-avoid-gmails-spam-folder#establish-sending-patterns).

---

# Send emails with Leap and Resend

> Learn how to add the Resend integration to your Leap.new project.

[Leap](https://leap.new) is a platform for building full-stack web and mobile apps via chat.

## ​1. Ask Leap to add Resend

 You can add Resend in a Leap project by asking the chat to add email sending with Resend. **Example prompt**

```
When someone fills out the contact form, send an email using Resend.
```

## ​2. Add your Resend API key

 To use Resend with Leap, you’ll need to add a Resend API key, which you can create in the [Resend Dashboard](https://resend.com/api-keys). Do not share your API key with others or expose it in the browser or other client-side code. Leap will prompt you to set a secret value on the Infrastructure page. Paste your key value and click **Update secret**. ![adding the Resend integration to a leap.new chat](https://mintcdn.com/resend/OWNnQaVDyqcGyhhN/images/leap-new-integration.png?fit=max&auto=format&n=OWNnQaVDyqcGyhhN&q=85&s=d1c68aa7b6144ffcd8ee2793cdebe67d) Learn more about the Resend integration in the [Leap
documentation](https://docs.leap.new/integrations/resend).

## ​3. Add a custom domain to your Resend account

 By default, you can only send emails to your own email address. To send emails to other email addresses:

1. Add a [custom domain to your Resend account](https://resend.com/domains).
2. Add the custom domain to the `from` field in the `resend` function in Leap (or ask the chat to update these fields).

 Get more help adding a custom domain in [Resend’s documentation](https://resend.com/docs/dashboard/domains/introduction).

---

# Send emails with Lovable and Resend

> Learn how to add the Resend integration to your Lovable project.

[Lovable](https://lovable.dev) is a platform for building web sites, tools, apps, and projects via chat. You can add Resend in a Lovable project by asking the chat to add email sending with Resend. If you prefer to watch a video, check out our video walkthrough below.

## ​1. Add your Resend API key

 To use Resend with Lovable, you’ll need to add a Resend API key, which you can create in the [Resend Dashboard](https://resend.com/api-keys). Do not share your API key with others or expose it in the browser or other client-side code. Lovable may integrate Resend in a few different ways:

- Use the Supabase integration to store the API key **(highly recommended)**
- Ask users to provide their own API key
- Add the API key directly in the code

 You may need to prompt Lovable to store the API key for Resend using Supabase. Clicking **Add API key** will open a modal where you can add the API key. ![adding the Resend integration to a Lovable chat](https://mintcdn.com/resend/OWNnQaVDyqcGyhhN/images/lovable-integration.png?fit=max&auto=format&n=OWNnQaVDyqcGyhhN&q=85&s=c071ba3ae671bc6cafd8dfd43e12772d) At the time of writing, Lovable does not securely handle API keys
independently. Instead, it uses the [Supabase integration to store
secrets](https://docs.lovable.dev/integrations/supabase#storing-secrets-api-keys-%26-config).

## ​2. Add a custom domain to your Resend account

 By default, you can only send emails to your own email address. To send emails to other email addresses:

1. Add a [custom domain to your Resend account](https://resend.com/domains).
2. Add the custom domain to the `from` field in the `resend` function in Lovable (or ask the chat to update these fields).

 Get more help adding a custom domain in [Resend’s documentation](https://resend.com/docs/dashboard/domains/introduction).
