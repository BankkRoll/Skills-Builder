# Batch Sending and more

# Batch Sending

> Send up to 100 emails in a single API call.

Batch sending allows you to send multiple emails at once (up to 100) instead of making individual API requests for each email.

## ​When to use batch sending

 Use batch sending when you need to:

- Send multiple transactional emails (e.g., order confirmations, notifications, etc.)
- Trigger emails to different recipients with unique content
- Reduce the number of API calls to improve performance

 For marketing campaigns, [use our no-code editor,
Broadcasts](https://resend.com/docs/dashboard/broadcasts/introduction), instead.

## ​Send batch emails

 You can send up to 100 emails in a single API call using the batch endpoint. Each email in the batch can have different recipients, subjects, and content.

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.batch.send([
  {
    from: 'Acme <onboarding@resend.dev>',
    to: ['delivered@resend.dev'],
    subject: 'Welcome to Acme',
    html: '<p>Thanks for signing up!</p>',
  },
  {
    from: 'Acme <onboarding@resend.dev>',
    to: ['delivered@resend.dev'],
    subject: 'Order Confirmation',
    html: '<p>Your order has been confirmed.</p>',
  },
]);

console.log(data);
```

## ​Response format

 The batch endpoint returns an array of email IDs for successfully created emails.

```
{
  "data": [
    {
      "id": "ae2014de-c168-4c61-8267-70d2662a1ce1"
    },
    {
      "id": "faccb7a5-8a28-4e9a-ac64-8da1cc3bc1cb"
    }
  ]
}
```

 If the request fails, the response will include an `error` object with a `message` property. You can find more information about the error in the [Errors](https://resend.com/docs/api-reference/errors) section of the API Reference.

## ​Limitations

 When using batch sending, keep in mind:

- Maximum of **100 emails** per batch request
- The `attachments` field is not supported yet
- The `scheduled_at` field is not supported yet
- Each email in the batch is processed independently
- The request will fail and return an error if any email in your payload is invalid (e.g., required fields are missing, fields contain invalid data, etc.).

## ​View batch emails

 All emails sent via the batch endpoint appear in the [Emails](https://resend.com/emails) page of your dashboard, just like individually sent emails. Each email will have a `queued` status initially before being processed.

## ​API Reference

 For complete API documentation, see the [Send Batch Emails API reference](https://resend.com/docs/api-reference/emails/send-batch-emails).

---

# Custom Headers

> Customize how emails are sent with your own headers.

Email headers are typically hidden from the end user but are crucial for deliverability. They include information about the sender, receiver, timestamp, and more. Resend already includes all the necessary headers for you, but now you can also add your own custom headers. This is a fairly advanced feature, but it can be useful for a few things:

- Prevent threading on Gmail with the **X-Entity-Ref-ID** header ([Example](https://github.com/resend/resend-examples/tree/main/with-prevent-thread-on-gmail))
- Include a shortcut for users to unsubscribe with the **List-Unsubscribe** header ([Example](https://github.com/resend/resend-examples/tree/main/with-unsubscribe-url-header))

 Here’s how you can add custom headers to your emails:

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

await resend.emails.send({
  from: 'Acme <[email protected]>',
  to: ['[email protected]'],
  subject: 'hello world',
  html: '<p>it works!</p>',
  headers: {
    'X-Entity-Ref-ID': 'xxx_xxxx',
  },
});
```

---

# Deliverability Insights

> Improve your deliverability with tailored insights based on your sending.

When you view your email within Resend, there is a “Insights” option. When selected, this will run eight deliverability best practice checks on your email and recommend possible changes to improve deliverability. ![Deliverability Insights](https://mintcdn.com/resend/OWNnQaVDyqcGyhhN/images/deliverability-insights-1.jpg?fit=max&auto=format&n=OWNnQaVDyqcGyhhN&q=85&s=78f3941a7a90d4546200c6cba6607270) If a check passes, you’ll get a nice green check. Resend will provide advice if it fails. We break these into two categories: Attention and Improvements.

## ​Attention Insights

 Changes to your email that can improve deliverability. ![Attention Insights](https://mintcdn.com/resend/OWNnQaVDyqcGyhhN/images/deliverability-insights-2.jpg?fit=max&auto=format&n=OWNnQaVDyqcGyhhN&q=85&s=158b0b42d45e7172f150a8818671a03e)

#### ​Link URLs match sending domain

 Ensure that the URLs in your email match the sending domain. Mismatched URLs can trigger spam filters. For example, if your sending domain is `@widgets.com`, ensure links within the message point back to `https://widgets.com`.

#### ​DMARC Record is Valid

 DMARC is a TXT record published in the DNS that specifies how email receivers should handle messages from your domain that don’t pass SPF or DKIM validation. [A valid DMARC record](https://resend.com/docs/dashboard/domains/dmarc) can help improve email deliverability. Starting in 2024, Gmail and Yahoo require senders to have a DMARC record published. When [viewing your domain](https://resend.com/domains) in Resend, we provide a suggested DMARC record if you’re unsure what to publish.

#### ​Include Plain Text Version

 Including a plain text version of your email ensures that your message is accessible to all recipients, including those who have email clients that do not support HTML. If you’re using Resend’s API, [plain text is passed via thetextparameter](https://resend.com/docs/api-reference/emails/send-email). This can also generate plain text using [React Email](https://react.email/docs/utilities/render#4-convert-to-plain-text).

#### ​Don’t use “no-reply”

 Indicating that this is a one-way communication decreases trust. Some email providers use engagement (email replies) when deciding how to filter your email. A valid email address allows you to communicate with your recipients easily if they have questions.

#### ​Keep email body size small

 Gmail limits the size of each email message to 102 KB. Once that limit is reached, the remaining content is clipped and hidden behind a link to view the entire message. Keep your email body size small to avoid this issue. This check will show the current size of your email.

## ​Improvement Insights

 If you’re diagnosing a deliverability issue, changing your email practices could be helpful. ![Improvement Insights](https://mintcdn.com/resend/OWNnQaVDyqcGyhhN/images/deliverability-insights-3.jpg?fit=max&auto=format&n=OWNnQaVDyqcGyhhN&q=85&s=64e4640b71c022a296f423ce4afdfbc8)

#### ​Use a Subdomain

 Using a subdomain instead of the root domain helps segment your sending by purpose. This protects different types of sending from impacting the reputation of others and clearly shows the sending purpose.

#### ​Disable Click Tracking

 Click tracking modifies links, sometimes causing spam filters to flag emails as suspicious or phishing attempts. Disabling click tracking can help with email deliverability, especially for sensitive transactional emails like login or email verification. If on, you can [disable click tracking on your domain in Resend](https://resend.com/domains).

#### ​Disable Open Tracking

 Spam filters are sensitive to tracking pixels, flagging them as potential spam. Without these tracking elements, emails may bypass these filters more effectively, especially for sensitive transactional emails like login or email verification. If on, you can [disable open tracking on your domain in Resend](https://resend.com/domains).

---

# Email Bounces

> Understanding and resolving delivery issues.

## ​Why does an email bounce?

 A bounce happens when an email cannot be delivered to the person it was meant for, and is returned to the sender. It essentially “bounces” back to the person who sent it. Some reasons include invalid email addresses, full mailboxes, technical issues with email servers, spam filters, message size restrictions, or blacklisting of the sender’s email server.

## ​Bounce Types and Subtypes

 When an email bounces, Resend receives a message from the recipient’s mail server. The bounce message explains why the delivery failed so the sender can fix the issue. There are three types of bounces:

1. `Permanent` - also known as “hard bounce,” where the recipient’s mail server rejects the email and will never be delivered.
  - `General` - The recipient’s email provider sent a hard bounce message.
  - `NoEmail` - It was not possible to retrieve the recipient email address from the bounce message.
2. `Transient` - also known as “soft bounce,” where the recipient’s mail server rejects the email but it could be delivered in the future.
  - `General` - The recipient’s email provider sent a general bounce message. You might be able to send a message to the same recipient in the future if the issue that caused the message to bounce is resolved.
  - `MailboxFull` - The recipient’s email provider sent a bounce message because the recipient’s inbox was full. You might be able to send to the same recipient in the future when the mailbox is no longer full.
  - `MessageTooLarge` - The recipient’s email provider sent a bounce message because message you sent was too large. You might be able to send a message to the same recipient if you reduce the size of the message.
  - `ContentRejected` - The recipient’s email provider sent a bounce message because the message you sent contains content that the provider doesn’t allow. You might be able to send a message to the same recipient if you change the content of the message.
  - `AttachmentRejected` - The recipient’s email provider sent a bounce message because the message contained an unacceptable attachment. For example, some email providers may reject messages with attachments of a certain file type, or messages with very large attachments. You might be able to send a message to the same recipient if you remove or change the content of the attachment.

 Sometimes, inboxes use autoresponders to signal a bounce. A `transient` status
could mean it’s related to the autoresponder, and it’s not a permanent issue.

1. `Undetermined` - where the recipient’s email server bounced, but the bounce message didn’t contain enough information for Resend to determine the underlying reason.
  - `Undetermined` - The recipient’s email provider sent a bounce message. The bounce message didn’t contain enough information for Resend to determine the reason for the bounce.

## ​Viewing Bounce Details in Resend

 You can see the bounce details by clicking on the email, and hovering over the `Bounced` label. ![Email Bounce Notification](https://mintcdn.com/resend/OWNnQaVDyqcGyhhN/images/email-bounce-details-1.png?fit=max&auto=format&n=OWNnQaVDyqcGyhhN&q=85&s=f0f99293137b8de4a9862b05cfd87d74) Once you click **See Details**, the drawer will open on the right side of your screen with the bounce type, subtype, along with suggestions on how to proceed. If the email is on the suppression list, you can click **Remove from Suppression List** to remove it. ![Email Bounce Drawer](https://mintcdn.com/resend/OWNnQaVDyqcGyhhN/images/email-suppression-list-2.png?fit=max&auto=format&n=OWNnQaVDyqcGyhhN&q=85&s=baf9f0a40313b856be978b728fb1d01c)

---

# Email Suppressions

> Understanding and resolving delivery issues.

## ​What does it mean that the email wassuppressed?

 A suppression happens when you try sending an email to a recipient that previously [bounced](https://resend.com/docs/dashboard/emails/email-bounces) or marked your email as spam. To protect your sender reputation and our sending infrastructure, we proactively stop that delivery from happening.

## ​What caused the suppression?

 The suppression is caused by:

- `Bounced` when the recipient’s mail server rejects the email and the response indicates a permanent failure to deliver. There could be [multiple reasons why an emailbounced](https://resend.com/docs/dashboard/emails/email-bounces#bounce-types-and-subtypes).
- `Complained` when the recipient marked your email as spam.

 Not all Inbox Service Providers return a `complained` event. Most notably,
Gmail/Google Workspace doesn’t.

## ​Viewing Suppression Details in Resend

 You can see the suppressed details by clicking on the email, and hovering over the `Suppressed` label. ![Email Suppression Notification](https://mintcdn.com/resend/03eaUBXyB1UIHhJ_/images/email-suppression-visibility-1.png?fit=max&auto=format&n=03eaUBXyB1UIHhJ_&q=85&s=b7e1336eb062d3fe1aeedde51443db9e) Once you click **See Details**, the drawer will open on the right side of your screen with the suppression reason along with suggestions on how to proceed. You can also click **Remove from Suppression List** to prevent the address from being suppressed. Do note that if it bounces or is marked as spam again, it’ll be suppressed again. Multiple or repeated bounces will negatively impact your sender reputation.

---

# Embed Inline Images

> Send emails with inline images.

You can optionally embed an image in the HTML body of the email. This allows you to include images without needing to host them in an external server. We currently do not support sending attachments (including inline images)
[when using our batch endpoint](https://resend.com/docs/api-reference/emails/send-batch-emails). 1

Add the CID in the email HTML.

Use the prefix `cid:` to reference the ID in the `src` attribute of an image tag in the HTML body of the email.

```
<img src="cid:logo-image">
```

2

Reference the CID in the attachment.

Include the content id parameter in the attachment object (see below for example implementations). The ID is an arbitrary string set by you, and must be less than 128 characters.

## ​Implementation details

 Both remote and local attachments are supported. All attachment [requirements, options, and limitations](https://resend.com/docs/dashboard/emails/attachments) apply to inline images as well. As with all our features, inline images are available across all our SDKs.

### ​Remote image example

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

await resend.emails.send({
  from: 'Acme <onboarding@resend.dev>',
  to: ['delivered@resend.dev'],
  subject: 'Thank you for contacting us',
  html: '<p>Here is our <img src="cid:logo-image"/> inline logo</p>',
  attachments: [
    {
      path: 'https://resend.com/static/sample/logo.png',
      filename: 'logo.png',
      contentId: 'logo-image',
    },
  ],
});
```

### ​Local image example

```
import { Resend } from 'resend';
import fs from 'fs';

const resend = new Resend('re_xxxxxxxxx');

const filepath = `${__dirname}/static/logo.png`;
const attachment = fs.readFileSync(filepath).toString('base64');

await resend.emails.send({
  from: 'Acme <onboarding@resend.dev>',
  to: ['delivered@resend.dev'],
  subject: 'Thank you for contacting us',
  text: '<p>Here is our <img src="cid:logo-image"/> inline logo</p>',
  attachments: [
    {
      content: attachment,
      filename: 'logo.png',
      contentId: 'logo-image',
    },
  ],
});
```

## ​Other considerations

 Before adding inline images, consider the following.

- As these images are sent as attachments, you need to encode your image as Base64 when sending the raw content via the API. There is no need to do this when passing the path of a remote image (the API handles this for you).
- Inline images increase the size of the email.
- Inline images may be rejected by some clients (especially webmail).
- As with all attachments, we recommend adding a `content_type` (e.g. `image/png`) or `filename` (e.g. `logo.png`) parameter to the attachment object, as this often helps email clients render the attachment correctly.

 All attachments (including inline images) do not currently display in the
[emails dashboard](https://resend.com/emails) when previewing email HTML.

---

# Idempotency Keys

> Use idempotency keys to ensure that emails are sent only once.

Include an idempotency key in any email requests to ensure that the same email request is processed only once, even if it’s sent multiple times. Idempotency keys are currently supported on the `POST /emails` and the `POST     /emails/batch` endpoints on the Resend API.

## ​How does it work?

 When you send an email with an idempotency key, we check if an email with the same idempotency key has already been sent in the last 24 hours. **This is an optional feature** that simplifies managing retries on your side. This makes it safe to retry requests that send an email. You don’t have to worry about checking if the original request was sent — you can just make the same request and our API will give the same response, without actually sending the email again.

## ​How to use idempotency keys?

 Idempotency keys can be **up to 256 characters** and should be unique per API request. We **recommend using a UUID** or other string that uniquely identifies that specific email. If you have multiple events that trigger emails related to a single entity in your system, you can format your idempotency keys to take advantage of that entity’s ID. One idea is to format idempotency keys like `<event-type>/<entity-id>`, for example `welcome-user/123456789`. The specific format you use is up to you. Send the key in the `Idempotency-Key` HTTP header in your API requests. Our SDKs also provide a convenient way to set this header. If you’re using SMTP, you can set the `Resend-Idempotency-Key` email header instead. We keep idempotency keys in our system for **24 hours**. This should give you an ample window to retry any failed processes on your end without having to keep track of the sent status.

### ​POST /emailsendpoint example

```
await resend.emails.send(
  {
    from: 'Acme <onboarding@resend.dev>',
    to: ['delivered@resend.dev'],
    subject: 'hello world',
    html: '<p>it works!</p>',
  },
  {
    idempotencyKey: 'welcome-user/123456789',
  },
);
```

### ​POST /emails/batchendpoint example

 Format your idempotency keys to take advantage of that entity’s ID (i.e.,
`<event-type>/<entity-id>`). For batch sends, choose a key that represents the whole batch, like a team, workspace, or project (i.e., `team-quota/123456789`).

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

await resend.batch.send(
  [
    {
      from: 'Acme <onboarding@resend.dev>',
      to: ['foo@gmail.com'],
      subject: 'hello world',
      html: '<h1>it works!</h1>',
    },
    {
      from: 'Acme <onboarding@resend.dev>',
      to: ['bar@outlook.com'],
      subject: 'world hello',
      html: '<p>it works!</p>',
    },
  ],
  {
    idempotencyKey: 'team-quota/123456789',
  },
);
```

## ​Possible responses

 After checking if an email with the same idempotency key has already been sent, Resend returns one of the following responses:

- **Successful responses** will return the email ID of the sent email.
- **Error responses** will return one of the following errors:
  - `400`: `invalid_idempotency_key` - the idempotency key has to be between 1-256 characters. You can retry with a valid key or without supplying an idempotency key.
  - `409`: `invalid_idempotent_request` - this idempotency key has already been used on a request that had a different payload. Retrying this request is useless without changing the idempotency key or payload.
  - `409`: `concurrent_idempotent_requests` - another request with the same idempotency key is currently in progress. As it isn’t finished yet, Resend can’t return its original response, but it is safe to retry this request later if needed.

---

# Managing Emails

> Learn how to view and manage all sent emails on the Resend Dashboard.

## ​View email details

 See all the metadata associated with an email, including the sender address, recipient address, subject, and more from the [Emails](https://resend.com/emails) page. Select any email to view its details. ![Email Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-emails-item.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=406e90f545d6b4f4289cd86311a2642a) Each email contains a **Preview**, **Plain Text**, and **HTML** version to visualize the content of your sent email in its various formats.

## ​Understand email events

 Here are all the events that can be associated with an email:

- `bounced` - The recipient’s mail server rejected the email. ([Learn more about bounced emails](https://resend.com/docs/dashboard/emails/email-bounces))
- `canceled` - The scheduled email was canceled (by user).
- `clicked` - The recipient clicked on a link in the email.
- `complained` - The email was successfully delivered to the recipient’s mail server, but the recipient marked it as spam.
- `delivered` - Resend successfully delivered the email to the recipient’s mail server.
- `delivery_delayed` - The email couldn’t be delivered to the recipient’s mail server because a temporary issue occurred. Delivery delays can occur, for example, when the recipient’s inbox is full, or when the receiving email server experiences a transient issue.
- `failed` - The email failed to be sent.
- `opened` - The recipient opened the email.
- `queued` - The email created from Broadcasts or Batches is queued for delivery.
- `scheduled` - The email is scheduled for delivery.
- `sent` - The email was sent successfully.
- `suppressed` - The email was not sent because the recipient is on the suppression list. ([Learn more about the suppression list](https://resend.com/docs/knowledge-base/why-are-my-emails-landing-on-the-suppression-list))

## ​Share email link

 You can share a public link of a sent email, which is valid for 48 hours. Anyone with the link can visualize the email. To share a link, click on the **dropdown menu** , and select **Share email**. ![Email - Share Link Option](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-emails-share-option.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=1e3019a33d90161bc41a77817e2a54c5) Then copy the URL and share it with your team members. ![Email - Share Link Modal](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-emails-share-modal.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=467d298ee78312a1f1b8356ea61457e5) Anyone with the link can visualize the email without authenticating for 48 hours. ![Email - Share Link Item](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-emails-share-item.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=05c438ac1b5e0721475b3f028a6f6934)

## ​See associated logs

 You can check all the logs associated with an email. This will help you troubleshoot any issues with the request itself. To view the logs, click on the dropdown menu, and select “View log”. ![Email - View Logs Option](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-emails-log-option.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=ad69ba9d638fe43f62974a0d76b1e01e) This will take you to logs, where you can see all the logs associated with the email. ![Email - View Logs Item](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-emails-log-item.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=936f066559e1ae477523be37aa959f90)

## ​Export your data

 Admins can download your data in CSV format for the following resources:

- Emails
- Broadcasts
- Contacts
- Segments
- Domains
- Logs
- API keys

 Currently, exports are limited to admin users of your team. To start, apply filters to your data and click on the “Export” button. Confirm your filters before exporting your data.  If your exported data includes 1,000 items or less, the export will download immediately. For larger exports, you’ll receive an email with a link to download your data. All admins on your team can securely access the export for 7 days. Unavailable exports are marked as “Expired.” All exports your team creates are listed in the
[Exports](https://resend.com/exports) page under **Settings** > **Team** >
**Exports**. Select any export to view its details page. All members of your
team can view your exports, but only admins can download the data.

---

# Schedule Email

> Send emails at a specific time without additional complexity.

While some emails need to be delivered as soon as possible, like password resets or magic links, others can be scheduled for a specific time. Here are some examples of when you might want to schedule an email:

- Send welcome email **5 minutes after** signup
- Trigger a reminder email **24 hours before** an event
- Schedule a weekly digest email for the **next day at 9am PST**

 Before, you had to use external services to handle the scheduling logic, but now you can use the new Resend API to schedule emails. Emails can be scheduled up to 30 days in advance. There are two ways to schedule an email:

1. [Using natural language](#1-schedule-using-natural-language)
2. [Using date format](#2-schedule-using-date-format)

## ​1. Schedule using natural language

 You can use the various Resend SDKs to schedule emails. The date can be defined using natural language, such as `"in 1 hour"`, `"tomorrow at 9am"`, or `"Friday at 3pm ET"`.

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

await resend.emails.send({
  from: 'Acme <[email protected]>',
  to: ['[email protected]'],
  subject: 'hello world',
  html: '<p>it works!</p>',
  scheduledAt: 'in 1 min',
});
```

## ​2. Schedule using date format

 You can also use a date in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format (e.g: `2024-08-05T11:52:01.858Z`).

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const oneMinuteFromNow = new Date(Date.now() + 1000 * 60).toISOString();

await resend.emails.send({
  from: 'Acme <[email protected]>',
  to: ['[email protected]'],
  subject: 'hello world',
  html: '<p>it works!</p>',
  scheduledAt: oneMinuteFromNow,
});
```

## ​View a scheduled email

 Once you schedule an email, you can see the scheduled time in the Resend dashboard.

## ​Reschedule an email

 After scheduling an email, you might need to update the scheduled time. You can do so with the following method:

```
resend.emails.update({
  id: '49a3999c-0ce1-4ea6-ab68-afcd6dc2e794',
  scheduledAt: 'in 1 min',
});
```

 You can also reschedule an email directly in the Resend dashboard.

## ​Cancel a scheduled email

 Once an email is canceled, it cannot be rescheduled. If you need to cancel a scheduled email, you can do so with the following code:

```
resend.emails.cancel('49a3999c-0ce1-4ea6-ab68-afcd6dc2e794');
```

 You can also cancel a scheduled email in the Resend dashboard.

## ​Scheduled email failures

 Scheduled emails may fail to send for several reasons. When this happens, you’ll see a failure notification in the email details screen with specific information about why the email couldn’t be sent. Common failure reasons include:

- **API key is no longer active** - The API key used to schedule the email has been deleted, expired, or suspended. The email cannot be sent.
- **Account under review** - Your account has been flagged for review and sending has been temporarily suspended. Contact [[email protected]](https://resend.com/cdn-cgi/l/email-protection#b0c3c5c0c0dfc2c4f0c2d5c3d5ded49ed3dfdd) if you believe this is an error.

 You can view the failure reason and details in the Resend dashboard by clicking on the failed email.

## ​Limitations

- Emails sent via SMTP cannot be scheduled

---

# Send Test Emails

> Simulate different events by sending test emails.

## ​How to send test emails

 During development, it’s important to test different deliverability scenarios.

> **Example**: When an email hard bounces or is marked as spam, it’s important to stop sending emails to the recipient, as continuing to send emails to those addresses will damage your domain reputation. We recommend [creating a webhook endpoint](https://resend.com/docs/webhooks/introduction) to capture these events and remove the addresses from your mailing lists.

 When testing, avoid:

- sending to fake email addresses
- setting up a fake SMTP server

 We provide the following test email addresses to help you simulate different email events without damaging your domain reputation. These test emails enable the safe use of Resend’s Dashboard, Webhooks, and API when developing your application. All test email addresses support labeling, which enables you to send emails to the same test address in multiple ways. You can add a label after the `+` symbol (e.g., `[email protected]`) to help track and differentiate between different test scenarios in your application.

## ​Test delivered emails

 To test that your emails are being successfully delivered, you can send an email to:

```
[email protected]
```

 With labeling support, you can also use:

```
[email protected]
[email protected]
[email protected]
```

## ​Test bounced emails

 To test that the recipient’s email provider rejected your email, you can send an email to:

```
[email protected]
```

 With labeling support, you can also use:

```
[email protected]
[email protected]
[email protected]
```

 This will generate a SMTP 550 5.1.1 (“Unknown User”) response code.

## ​Test “Marked as Spam” emails

 To test that your emails are being received but marked as spam, you can send an email to:

```
[email protected]
```

 With labeling support, you can also use:

```
[email protected]
[email protected]
[email protected]
```

## ​Test suppressed emails

 To test that your emails are being suppressed, you can send an email to:

```
[email protected]
```

 When using this test email, the suppression reason will indicate the address
was previously bounced

## ​Using labels effectively

 The suppressed test email address does not support labeling yet The labeling feature allows you to use any string as a label after the `+` symbol. This is particularly useful for:

- Testing different email flows (e.g., `[email protected]`, `[email protected]`)
- Tracking webhook responses for specific test scenarios
- Differentiating between multiple test runs
- Matching responses with the specific email address that triggered the event

---

# Managing Tags

> Add unique identifiers to emails sent.

Tags are unique identifiers you can add to your emails. They help associate emails with your application. They are passed in key/value pairs. After the email is sent, the tag is included in the webhook event. Tags can include ASCII letters, numbers, underscores, or dashes. Some examples of when to use a tag:

- Associate the email a “customer ID” from your application
- Add a label from your database like “free” or “enterprise”
- Note the category of email sent, like “welcome” or “password reset”

 Here’s how you can add custom tags to your emails.

## ​Add tags on thePOST /emailsendpoint

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

await resend.emails.send({
  from: 'Acme <[email protected]>',
  to: ['[email protected]'],
  subject: 'hello world',
  html: '<p>it works!</p>',
  tags: [
    {
      name: 'category',
      value: 'confirm_email',
    },
  ],
});
```

## ​Add tags on thePOST /emails/batchendpoint

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.batch.send([
  {
    from: 'Acme <[email protected]>',
    to: ['[email protected]'],
    subject: 'hello world',
    html: '<h1>it works!</h1>',
    tags: [
      {
        name: 'category',
        value: 'confirm_email',
      },
    ],
  },
  {
    from: 'Acme <[email protected]>',
    to: ['[email protected]'],
    subject: 'world hello',
    html: '<p>it works!</p>',
    tags: [
      {
        name: 'category',
        value: 'confirm_email',
      },
    ],
  },
]);
```

---

# Introduction

> Learn how to view and troubleshoot API logs in the Resend Dashboard.

## ​Overview

 The Logs page provides detailed information about every API request made to Resend, helping you monitor activity and troubleshoot issues quickly.

## ​Viewing logs

 Access your logs from the [Logs page](https://resend.com/logs) in the dashboard. ![Logs](https://mintcdn.com/resend/jNLP19MmH13tZf-I/images/logs-page.png?fit=max&auto=format&n=jNLP19MmH13tZf-I&q=85&s=c6255bb12281961d20606de92a778b99) Each log entry shows:

- **Endpoint** - The API endpoint called (e.g., `/domains`, `/api-keys`, `/contacts`)
- **Status** - The HTTP response status code (200, 201, etc.)
- **Method** - The HTTP method used (GET, POST, DELETE, etc.)
- **Created** - When the request was made (displayed as relative time)

## ​Searching Logs

 Use the search bar to find specific logs. This is useful when tracking down a particular request or debugging an issue.

## ​Filtering Logs

 Filter logs by response status to quickly identify issues:

- **All Statuses** - View all logs
- **Successes** - Show only successful requests (2xx status codes)
- **Errors** - Show only failed requests (4xx and 5xx status codes)
- **Specific codes** - Select one or more specific HTTP status codes (200, 201, 403, 429, etc.)

 You can select multiple status codes to create custom filters.

- **Date range** - Adjust the time period for logs (e.g., Last 15 days)
- **User Agents** - Filter by SDK or client
- **API Keys** - Filter by specific API key

## ​Log details

 Click any log entry to view complete details. ![Logs](https://mintcdn.com/resend/jNLP19MmH13tZf-I/images/logs-page-details.png?fit=max&auto=format&n=jNLP19MmH13tZf-I&q=85&s=dd6d948f384d6b90e8a5bed33ec237f0)

### ​Request information

- **Request body** - The full JSON payload sent to the API (with copyable code blocks)
- **HTTP method** - GET, POST, etc.
- **Endpoint** - The API endpoint called
- **User-Agent** - The client or SDK used, with automatic SDK detection showing name and version

### ​Response information

- **Response body** - The complete API response (with copyable code blocks)
- **Status code** - The HTTP status code returned
- **Timestamp** - When the request was processed

### ​SDK detection

 The dashboard automatically detects and displays Resend SDK information from the User-Agent header, showing:

- SDK name (e.g., “Resend Node.js”)
- Version number

## ​Troubleshooting errors

 For supported error types, click the **Help me fix** button to open a troubleshooting drawer. ![Logs](https://mintcdn.com/resend/jNLP19MmH13tZf-I/images/logs-page-error.png?fit=max&auto=format&n=jNLP19MmH13tZf-I&q=85&s=60e6190acbb51c2d97a08f0bac177d74) The drawer includes:

- **Raw response** - The complete API response
- **Detailed guidance** - Step-by-step instructions to resolve the issue
- **Relevant links** - Documentation and knowledge base articles
- **Contextual information** - Your current rate limits, verified domains, and other relevant data

 View a comprehensive list of error codes and their meanings in the [Resend API
Reference](https://resend.com/docs/api-reference/errors).

## ​Export your data

 Admins can download your data in CSV format for the following resources:

- Emails
- Broadcasts
- Contacts
- Segments
- Domains
- Logs
- API keys

 Currently, exports are limited to admin users of your team. To start, apply filters to your data and click on the “Export” button. Confirm your filters before exporting your data.  If your exported data includes 1,000 items or less, the export will download immediately. For larger exports, you’ll receive an email with a link to download your data. All admins on your team can securely access the export for 7 days. Unavailable exports are marked as “Expired.” All exports your team creates are listed in the
[Exports](https://resend.com/exports) page under **Settings** > **Team** >
**Exports**. Select any export to view its details page. All members of your
team can view your exports, but only admins can download the data.

---

# Process Receiving Attachments

> Process attachments from receiving emails.

A common use case for Receiving emails is to process attachments. Webhooks do not include the actual content of attachments, only their
metadata. You must call the [Attachments
API](https://resend.com/docs/api-reference/emails/list-received-email-attachments) to retrieve the
content. This design choice supports large attachments in serverless
environments that have limited request body sizes. Users can forward airplane tickets, receipts, and expenses to you. Then, you can extract key information from attachments and use that data. To do this, call the [Attachments API](https://resend.com/docs/api-reference/emails/list-received-email-attachments) after receiving the webhook event. That API will return a list of attachments with their metadata and a `download_url` that you can use to download the actual content. Note that the `download_url` is valid for 1 hour. After that, you will need to call the
[Attachments API](https://resend.com/docs/api-reference/emails/list-received-email-attachments)
again to get a new `download_url`. You can also check the `expires_at` field on
each attachment to see exactly when it will expire. Here’s an example of getting attachment data in a Next.js application: app/api/events/route.ts

```
import type { NextRequest } from 'next/server';
import { NextResponse } from 'next/server';
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

export const POST = async (request: NextRequest) => {
  const event = await request.json();

  if (event.type === 'email.received') {
    const { data: attachments } = await resend
      .emails
      .receiving
      .attachments
      .list({ emailId: event.data.email_id });

    for (const attachment of attachments) {
      // use the download_url to download attachments however you want
      const response = await fetch(attachment.download_url);
      if (!response.ok) {
        console.error(`Failed to download ${attachment.filename}`);
        continue;
      }

      // get the file's contents
      const buffer = Buffer.from(await response.arrayBuffer());

      // process the content (e.g., save to storage, analyze, etc.)
    }

    return NextResponse.json({ attachmentsProcessed: attachments.length });
  }

  return NextResponse.json({});
};
```

 Once you process attachments, you may want to forward the email to another address. Learn more about [forwarding emails](https://resend.com/docs/dashboard/receiving/forward-emails).

---

# Custom Receiving Domains

> Receive emails using your own domain.

Besides [using Resend-managed domains](https://resend.com/docs/dashboard/receiving/introduction), you can also receive emails using your own custom domain, such as `yourdomain.tld`. Here’s how to receive emails using a *new* custom domain.

## ​1. Add the DNS record

 First, [verify your domain](https://resend.com/docs/dashboard/domains/introduction). Receiving emails requires an extra [MX record](https://resend.com/knowledge-base/how-do-i-avoid-conflicting-with-my-mx-records) to work. You’ll need to add this record to your DNS provider.

1. Go to the [Domains](https://resend.com/domains) page
2. Copy the MX record
3. Paste the MX record into your domain’s DNS service

 ![Add DNS records for Receiving Emails](https://mintcdn.com/resend/1QlhxulUFE6jxYM_/images/inbound-custom-domain-dns.jpg?fit=max&auto=format&n=1QlhxulUFE6jxYM_&q=85&s=0bb3258dbd1e9fc5efeb9ead53b219a2) If you already have existing MX records for your domain (because you’re already
using it for a real inbox, for example), we recommend that you
create a subdomain (e.g. `subdomain.yourdomain.tld`) and add the MX record
there. This way, you can use Resend for receiving emails without affecting
your existing email service. Note that you will *not* receive emails at Resend
if the required `MX` record is not the lowest priority value for the domain.Alternatively, you can configure your email service to forward emails to an address
that’s configured in Resend or forward them directly to the SMTP server address
that appears in the receiving `MX` record.

## ​2. Configure webhooks

 Next, create a new webhook endpoint to receive email events.

1. Go to the [Webhooks](https://resend.com/webhooks) page
2. Click “Add Webhook”
3. Enter the URL of your webhook endpoint
4. Select the event type `email.received`
5. Click “Add”

 ![Add Webhook for Receiving Emails](https://mintcdn.com/resend/1QlhxulUFE6jxYM_/images/inbound-webhook-setup.jpg?fit=max&auto=format&n=1QlhxulUFE6jxYM_&q=85&s=55ae3e35788d91065d59ff4ddebff7e6)

## ​3. Receive email events

 In your application, create a new route that can accept `POST` requests. For example, here’s how you can add an API route in a Next.js application: app/api/events/route.ts

```
import type { NextRequest } from 'next/server';
import { NextResponse } from 'next/server';

export const POST = async (request: NextRequest) => {
  const event = await request.json();

  if (event.type === 'email.received') {
    return NextResponse.json(event);
  }

  return NextResponse.json({});
};
```

 Once you receive the email event, you can process the email body and attachments. We also recommend implementing [webhook request verification](https://resend.com/docs/webhooks/verify-webhooks-requests) to secure your webhook endpoint.

```
{
  "type": "email.received",
  "created_at": "2024-02-22T23:41:12.126Z",
  "data": {
    "email_id": "56761188-7520-42d8-8898-ff6fc54ce618",
    "created_at": "2024-02-22T23:41:11.894719+00:00",
    "from": "Acme <onboarding@resend.dev>",
    "to": ["delivered@resend.dev"],
    "bcc": [],
    "cc": [],
    "message_id": "<example+123>",
    "subject": "Sending this example",
    "attachments": [
      {
        "id": "2a0c9ce0-3112-4728-976e-47ddcd16a318",
        "filename": "avatar.png",
        "content_type": "image/png",
        "content_disposition": "inline",
        "content_id": "img001"
      }
    ]
  }
}
```

## ​Enabling receiving for an existing domain

 If you already have a verified domain, you can enable receiving by using the toggle in the receiving section of the domain details page. ![Enable Receiving Emails for a verified domain](https://mintcdn.com/resend/cxinN79qDVOa7Vo6/images/inbound-enable-receiving.jpg?fit=max&auto=format&n=cxinN79qDVOa7Vo6&q=85&s=43ea9fce84b46236ce4d58efc6004a24) After enabling receiving, you’ll see a modal showing the MX record that you need to add to your DNS provider to start receiving emails. Once you add the MX record, confirm by clicking the “I’ve added the record” button and wait for the receiving record to show as “verified”.

## ​FAQ

What happens if I already have MX records for my domain?

If you already have existing MX records for your domain, we recommend that you
create a subdomain (e.g. `subdomain.yourdomain.tld`) and add the MX record
there.That’s because emails will usually only be delivered to the MX record with the lowest
priority value. Therefore, if you add Resend’s MX record to your root domain alongside existing MX records,
it will either not receive any emails at all (if the existing MX records have a lower priority),
or it will interfere with your existing email service (if Resend’s MX record has a lower priority). If you
use the same priority, email delivery will be unpredictable and may hit either Resend or your existing email
service.If you still want to use the same domain both in for Resend and your day-to-day
email service, you can also set up forwarding rules in your existing email service
to forward emails to an address that’s configured in Resend or forward them directly
to the SMTP server address that appears in the receiving `MX` record.

I have already verified my domain for sending. Do I need to verify it again for receiving?

No, you do not need to verify your entire domain again. If you already have a
verified domain for sending, you can simply enable receiving for that domain,
add the required MX record to your DNS provider, and click “I’ve added the record”
to start verifying *only* the MX record.
