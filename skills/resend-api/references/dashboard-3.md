# Forward Received Emails and more

# Forward Received Emails

> Forward Received emails to another email address.

Received emails can also be forwarded to another email address. Webhooks do not include the actual HTML or Plain Text body of the email. You
must call the [received emails
API](https://resend.com/docs/api-reference/emails/retrieve-received-email) to retrieve them. This
design choice supports large payloads in serverless environments that have
limited request body sizes.

## ​Using theforwardhelper method

 The Node.js SDK provides a `forward()` helper method that simplifies forwarding received emails. This method automatically handles fetching the email content and attachments. Here’s an example of forwarding an email in a Next.js application: app/api/events/route.ts

```
import type { NextRequest } from 'next/server';
import { NextResponse } from 'next/server';
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

export const POST = async (request: NextRequest) => {
  const event = await request.json();

  if (event.type === 'email.received') {
    const { data, error } = await resend.emails.receiving.forward({
      emailId: event.data.email_id,
      to: 'delivered@resend.dev',
      from: 'onboarding@resend.dev',
    });

    if (error) {
      return new NextResponse(`Error: ${error.message}`, { status: 500 });
    }

    return NextResponse.json(data);
  }

  return NextResponse.json({});
};
```

 By default, the `forward` method forwards the email in a way that preserves the original email content and attachments exactly as received. Alternatively, you can forward emails as if they had been forwarded through an email client, with the `forwarded message` footer. For that, use `passthrough: false` and provide custom text or HTML content. The original email will be shown after the `forwarded message` footer: app/api/events/route.ts

```
const { data, error } = await resend.emails.receiving.forward({
  emailId: event.data.email_id,
  to: 'delivered@resend.dev',
  from: 'onboarding@resend.dev',
  passthrough: false,
  text: 'See attached forwarded message.',
  html: '<p>See attached forwarded message.</p>',
});
```

## ​Manual forwarding

 If you’re not using Node.js or prefer not to use the `forward` helper method, you can manually forward received emails using the [Send Email API](https://resend.com/docs/api-reference/emails/send-email). The recommended approach is to download the raw email and parse it to properly extract content and attachments (especially for inline images). Then, you can send a new email with the extracted content and attachments using the [Send Email API](https://resend.com/docs/api-reference/emails/send-email). app/api/events/route.ts

```
import type { NextRequest } from 'next/server';
import { NextResponse } from 'next/server';
import { Resend } from 'resend';
import { simpleParser } from 'mailparser';

const resend = new Resend('re_xxxxxxxxx');

export const POST = async (request: NextRequest) => {
  const event = await request.json();

  if (event.type === 'email.received') {
    // Get the email metadata
    const { data: email } = await resend
      .emails
      .receiving
      .get(event.data.email_id);

    // Download the raw email content if available
    if (!email?.raw?.download_url) {
      return new NextResponse('Raw email not available', { status: 500 });
    }

    const rawResponse = await fetch(email.raw.download_url);
    const rawEmailContent = await rawResponse.text();

    // Parse the raw email to extract content and attachments
    const parsed = await simpleParser(rawEmailContent, {
      skipImageLinks: true,
    });

    // Extract attachments with content_id for inline images
    const attachments = parsed.attachments.map((attachment) => {
      // Strip < and > from content IDs for proper inline image handling
      const contentId = attachment.contentId
        ? attachment.contentId.replace(/^<|>$/g, '')
        : undefined;

      return {
        filename: attachment.filename,
        content: attachment.content.toString('base64'),
        content_type: attachment.contentType,
        content_id: contentId || undefined,
      };
    });

    const { data, error } = await resend.emails.send({
      from: 'Acme <onboarding@resend.dev>',
      to: ['delivered@resend.dev'],
      subject: email.subject || '(no subject)',
      html: parsed.html || undefined,
      text: parsed.text || undefined,
      attachments: attachments.length > 0 ? attachments : undefined,
    });

    if (error) {
      return new NextResponse(`Error: ${error.message}`, { status: 500 });
    }

    return NextResponse.json(data);
  }

  return NextResponse.json({});
};
```

 This example uses the [mailparser](https://www.npmjs.com/package/mailparser)
library (`npm install mailparser`) to parse the raw email. For other
languages/SDKs, you’ll need an equivalent email parsing library capable of
processing emails compliant to [RFC
5322](https://datatracker.ietf.org/doc/html/rfc5322).

---

# Get Email Content

> Get the body and headers of a received email.

Receiving emails contain the HTML and Plain Text body of the email, as well as the headers. Webhooks do not include the actual HTML or Plain Text body of the email. You
must call the [received emails
API](https://resend.com/docs/api-reference/emails/retrieve-received-email) to retrieve them. This
design choice supports large payloads in serverless environments that have
limited request body sizes. After receiving the webhook event, call the [Receiving API](https://resend.com/docs/api-reference/emails/retrieve-received-email). Here’s an example in a Next.js application: app/api/events/route.ts

```
import type { NextRequest } from 'next/server';
import { NextResponse } from 'next/server';
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

export const POST = async (request: NextRequest) => {
  const event = await request.json();

  if (event.type === 'email.received') {
    const { data: email } = await resend
      .emails
      .receiving
      .get(event.data.email_id);

    console.log(email.html);
    console.log(email.text);
    console.log(email.headers);

    return NextResponse.json(email);
  }

  return NextResponse.json({});
};
```

---

# Receiving Emails

> Learn how to receive emails via webhooks.

Resend supports receiving emails (commonly called inbound) in addition to sending emails. This is useful for:

- Receiving support emails from users
- Processing forwarded attachments
- Replying to emails from customers

## ​How does it work

 Resend processes all incoming emails for your receiving domain, parses the contents and attachments, and then sends a `POST` request to an endpoint that you choose. To receive emails, you can either use a domain managed by Resend, or [set up a custom domain](https://resend.com/docs/dashboard/receiving/custom-domains). ![Receiving email process](https://mintcdn.com/resend/bxWCBKtofKnXvbvf/images/receiving-emails.jpeg?fit=max&auto=format&n=bxWCBKtofKnXvbvf&q=85&s=faa9d79f48a43f320d2b5a800256060e) Importantly, *any email* sent to your receiving domain will be received by Resend and forwarded to your webhook. You can intelligently route based on the `to` field in the webhook event.For example, if your domain is `cool-hedgehog.resend.app`, you will receive
emails sent to `[email protected]`.The same applies to [custom domains](https://resend.com/docs/dashboard/receiving/custom-domains). If
your domain is `yourdomain.tld`, you will receive emails sent to
`[email protected]`. Here’s how to start receiving emails using a domain managed by Resend.

## ​1. Get your.resend.appdomain

 Any emails sent to an `<anything>@<id>.resend.app` address will be received by Resend and forwarded to your webhook. To see your Resend domain:

1. Go to the [emails page](https://resend.com/emails).
2. Select the [“Receiving” tab](https://resend.com/emails/receiving).
3. Click the three dots button and select “Receiving address.”

 ![Get your Resend domain](https://mintcdn.com/resend/stmz8SfTchQy1hpq/images/inbound-resend-domain.jpg?fit=max&auto=format&n=stmz8SfTchQy1hpq&q=85&s=c26fcec3f9dc5def25041d44cb8c501a)

## ​2. Configure webhooks

1. Go to the [Webhooks](https://resend.com/webhooks) page.
2. Click `Add Webhook`.
3. Enter the URL of your webhook endpoint.
4. Select the event type `email.received`.
5. Click `Add`.

 For development, you can create a tunnel to your localhost server using a tool like
[ngrok](https://ngrok.com/download) or [VS Code Port Forwarding](https://code.visualstudio.com/docs/debugtest/port-forwarding). These tools serve your local dev environment at a public URL you can use to test your local webhook endpoint.Example: `https://example123.ngrok.io/api/webhook` ![Add Webhook for Receiving Emails](https://mintcdn.com/resend/1QlhxulUFE6jxYM_/images/inbound-webhook-setup.jpg?fit=max&auto=format&n=1QlhxulUFE6jxYM_&q=85&s=55ae3e35788d91065d59ff4ddebff7e6)

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
    "from": "Acme <[email protected]>",
    "to": ["[email protected]"],
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

## ​What can you do with Receiving emails

 Once you receive an email, you can process it in a variety of ways. Here are some common actions you can take:

- [Get email content](https://resend.com/docs/dashboard/receiving/get-email-content)
- [Process attachments](https://resend.com/docs/dashboard/receiving/attachments)
- [Forward emails to another address](https://resend.com/docs/dashboard/receiving/forward-emails)
- [Reply to emails in the same thread](https://resend.com/docs/dashboard/receiving/reply-to-emails)

 Webhooks do not include the email body, headers, or attachments, only their
metadata. You must call the [Received emails
API](https://resend.com/docs/api-reference/emails/retrieve-received-email) or the [Attachments
API](https://resend.com/docs/api-reference/emails/list-received-email-attachments) to retrieve them.
This design choice supports large attachments in serverless environments that
have limited request body sizes.

## ​FAQ

Will I receive emails for any address at my domain?

Yes. Once you add the MX record to your [custom domains](https://resend.com/docs/dashboard/receiving/custom-domains), you will receive emails for
any address at that domain.For example, if your domain is `yourdomain.tld`, you will receive
emails sent to `<anything>@yourdomain.tld`. You can then filter or
route based on the `to` field in the webhook event.The same applies if you use the domain managed by Resend. If the domain given to you is `cool-hedgehog.resend.app`,
you’ll receive any email send to `<anything>@cool-hedgehog.resend.app`.

Can I receive emails on a subdomain?

Yes. You can add the MX record to any subdomain (e.g.
`subdomain.yourdomain.tld`) and receive emails there.

Should I add the `MX` records for my root domain or a subdomain?

If you already have existing MX records for your root domain, we recommend
that you create a subdomain (e.g. `subdomain.yourdomain.tld`) and add the MX
record there. This way, you can use Resend for receiving emails without
affecting your existing email service.If you still want to use the same domain both in for Resend and your day-to-day
email service, you can also set up forwarding rules in your existing email service
to forward emails to an address that’s configured in Resend or forward them directly
to the SMTP server address that appears in the receiving `MX` record.

Will I lose my emails if my webhook endpoint is down?

No, you will not lose your emails. Resend stores emails as soon as they come
in.Even if your webhook endpoint is down, you can still see your emails in
the dashboard and retrieve them using the [Receiving
API](https://resend.com/docs/api-reference/emails/retrieve-received-email).Additionally, we will retry delivering the webhook event on the schedule
described in our [webhooks documentation](https://resend.com/docs/webhooks/introduction#faq)
and you can also replay individual webhook events from the
[webhooks](https://resend.com/docs/webhooks/introduction) page in the dashboard.

How can I make sure that it's Resend who's sending me webhooks?

All of Resend’s webhooks include a secret and headers that you can use to verify
the authenticity of the request.In our SDKs, you can verify webhooks using
`resend.webhooks.verify()`, as shown below.

```
// throws an error if the webhook is invalid
// otherwise, returns the parsed payload object
const result = resend.webhooks.verify({
  payload: JSON.stringify(req.body),
  headers: {
    id: req.headers['svix-id'],
    timestamp: req.headers['svix-timestamp'],
    signature: req.headers['svix-signature'],
  },
  webhookSecret: process.env.RESEND_WEBHOOK_SECRET,
})
```

You can find more code samples and instructions on how to verify webhooks in our
[webhook verification documentation](https://resend.com/docs/webhooks/verify-webhooks-requests).

---

# Reply to Receiving Emails

> Reply to Receiving emails in the same thread.

Email clients thread emails by using the `message_id` metadata. If you want to reply to an email, you should add the `In-Reply-To` header set to the `message_id` of the received email. We also recommend setting the subject to start with `Re:` so that email clients can group the replies together. Here’s an example of replying to an email in a Next.js application: app/api/events/route.ts

```
import type { NextRequest } from 'next/server';
import { NextResponse } from 'next/server';
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

export const POST = async (request: NextRequest) => {
  const event = await request.json();

  if (event.type === 'email.received') {
    const { data, error } = await resend.emails.send({
      from: 'Acme <onboarding@resend.dev>',
      to: ['delivered@resend.dev'],
      subject: `Re: ${event.data.subject}`,
      html: '<p>Thanks for your email!</p>',
      headers: {
        'In-Reply-To': event.data.message_id,
      },
      attachments,
    });

    return NextResponse.json(data);
  }

  return NextResponse.json({});
};
```

 If you’re replying multiple times within the same thread, make sure to also append
the previous `message_id`s to the `References` header, separated by spaces.
This helps email clients maintain the correct threading structure.

```
const previousReferences = ['<msg_id1@domain.com>', '<msg_id2@domain.com>'];

const { data, error } = await resend.emails.send({
  from: 'Acme <onboarding@resend.dev>',
  to: ['delivered@resend.dev'],
  subject: `Re: ${event.data.subject}`,
  html: '<p>Thanks for your email!</p>',
  headers: {
    'In-Reply-To': event.data.message_id,
    'References': [...previousReferences, event.data.message_id].join(' '),
  },
  attachments,
});
```

---

# Managing Segments

> Learn how to create, retrieve, and delete segments.

Segments are used to group and manage your [Contacts](https://resend.com/docs/dashboard/audiences/contacts). Segments are not visible to your Contacts, but are used for your own internal Contact organization.

## ​Send emails to your Segment

 Segments were designed to be used in conjunction with [Broadcasts](https://resend.com/docs/dashboard/broadcasts/introduction). You can send a Broadcast to an Segment from the Resend dashboard or from the Broadcast API.

### ​From Resend’s no-code editor

 You can send emails to your Segment by creating a new Broadcast and selecting the Segment you want to send it to. ![Send emails to your Segment](https://mintcdn.com/resend/m2xttJpF68pi6Mw0/images/audiences-intro-2.png?fit=max&auto=format&n=m2xttJpF68pi6Mw0&q=85&s=aaf9ac3f30d822ea5831b16db95d938e) You can include the Unsubscribe Footer in your Broadcasts, which will be automatically replaced with the correct link for each Contact.

### ​From the Broadcast API

 You can also use our [Broadcast API](https://resend.com/docs/api-reference/broadcasts/create-broadcast) to create and send a Broadcast to your Segment.

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.broadcasts.create({
  segmentId: '78261eea-8f8b-4381-83c6-79fa7120f1cf',
  from: 'Acme <onboarding@resend.dev>',
  subject: 'hello world',
  html: 'Hi {{{FIRST_NAME|there}}}, you can unsubscribe here: {{{RESEND_UNSUBSCRIBE_URL}}}',
});
```

## ​How to customize the unsubscribe link in my Broadcast?

 Resend generates a unique link for each recipient and each Broadcast. You can use `{{{RESEND_UNSUBSCRIBE_URL}}}` as the link target. ![Unsubscribe Link](https://mintcdn.com/resend/ABWmVTZIHGIFNTFD/images/audiences-intro-3.png?fit=max&auto=format&n=ABWmVTZIHGIFNTFD&q=85&s=4b37fb9c380e19ca0b53b80a3c925c8f)

## ​Automatic Unsubscribes

 When you send emails to your Segment, Resend will automatically handle the unsubscribe flow for you. ![Automatic Unsubscribes](https://mintcdn.com/resend/m2xttJpF68pi6Mw0/images/audiences-intro-4.png?fit=max&auto=format&n=m2xttJpF68pi6Mw0&q=85&s=b9715a7bb5d97a3795cf82978073895e) If a Contact unsubscribes from your emails, they will be presented with a preference page.

- If you don’t have any [Topics](https://resend.com/docs/dashboard/topics/introduction) configured, the Contact will be unsubscribed from all emails from your account.
- If you have [Topics](https://resend.com/docs/dashboard/topics/introduction) configured, the Contact will be presented with a preference page where they can subscribe or unsubscribe from specific types of emails (all `public` Topics will be shown).

 Learn more about [managing your unsubscribe list](https://resend.com/docs/dashboard/audiences/managing-unsubscribe-list) or [customizing your unsubscribe page](https://resend.com/docs/dashboard/settings/unsubscribe-page). Whenever possible, you should add a [Topic to your
Broadcast](https://resend.com/docs/dashboard/topics/introduction), as this will allow your Contacts
to unsubscribe from specific types of emails (instead of unsubscribing from
all emails from your account).

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

# Migrating from Audiences to Segments

> Learn how to migrate from Audiences to Segments

We’ve recently changed how Contacts are segmented. Before, each Contact was part of one Audience and if you created another contact with the same email address in a different Audience, it would be a completely separate object. In the new model, Contacts are now independent of Audiences, which are now called Segments. A Contact can be in zero, one or multiple Segments and still count as one when calculating your quota usage. Contacts API endpoints that previously required an `audience_id` can now be used directly instead.

## ​What’s changing?

 We’re moving to a **Global Contacts** model.

- **Before**: If a Contact with the same email appeared in multiple Segments, it was counted as multiple Contacts.
- **Now**: Each email address is treated as a single Contact across your team, even if it appears in multiple Segments.

 The new model offers three concepts:

- **Contact**: a global entity linked to a specific email address.
- **Segment**: an internal segmentation tool for your team to organize sending.
- **Topic**: a user-facing tool for managing email preferences.

## ​Unsubscribing

 Previously, when a contact clicked “unsubscribe,” their contact status were marked was “Unsubscribed” only from the specific Audience used in that Broadcast. From now on, contacts will see a preference page where they can:

- Unsubscribe from certain **Topics** (email’s preference).
- Or unsubscribe from **everything** you send (update contact status).

## ​What you should do

 If you’ve been using Audiences for both segmentation and unsubscribes, we recommend switching your unsubscribe logic to **Topics**:

1. Create a Topic for each type of email you send.
2. Assign the right users to each Topic.
3. Use Segments purely for your internal organization.

 With this setup, when you send a Broadcast, your users can choose which Topics to unsubscribe from—or opt out completely. For details on the new API endpoints view:

- [Contacts](https://resend.com/docs/api-reference/contacts/create-contact)
- [Topics](https://resend.com/docs/api-reference/topics/create-topic)
- [Segments](https://resend.com/docs/api-reference/segments/create-segment)

## ​How can we help?

 If you have a use case not covered here, [please reach out](https://resend.com/help). We’ll make sure your transition is smooth.

---

# Managing Billing

> Manage your account subscription and billing information

The [Billing](https://resend.com/settings/billing) page in the Settings section provides a clear view of your subscription details, billing email, payment method, and account invoices. From here, you can:

- View and manage your subscription - Upgrade, downgrade, or modify your current plan.
- Manage billing contacts - Ensure the right people receive billing-related notifications.
- Update payment information - Add or change your credit card or billing details.
- Access invoices - Download past invoices for your records.

 For any other billing inquiries, please [contact support](https://resend.com/help).

## ​How to cancel your subscription

1. Go to the [Billing](https://resend.com/settings/billing) page.
2. Click on the three dots  next to your plan.
3. Select **Cancel Subscription** from the dropdown menu.

 ![Cancel subscription](https://mintcdn.com/resend/ABWmVTZIHGIFNTFD/images/dashboard-billing.jpg?fit=max&auto=format&n=ABWmVTZIHGIFNTFD&q=85&s=3331d4b449ffd37fc0fe24f89e6f7dde)

---

# Managing Teams

> Manage your account across multiple teams

Resend allows multiple teams to be managed under a single email address. Each team is distinct, with its own API keys, billing, and usage.

## ​Inviting new members to a team

1. Navigate to your [Team Settings](https://resend.com/settings/team).
2. Click **Invite**. Input an email address and select a role (**Admin** or **Member**).
  - **Members** have access to manage emails, domains and webhooks.
  - **Admins** have all Member permissions plus the ability to invite users, update payments, and delete the team.
3. The new member will receive an email invitation to join the team.

## ​Add a team avatar

1. Navigate to your [Team Settings](https://resend.com/settings/team).
2. Click **Upload Image** next to the avatar placeholders.
3. Upload an image file to use as the team avatar.

## ​Switching between teams

 After accepting an invite from the account owner, users can switch between teams:

1. Click on the **team name** in the top left corner of any Resend page.
2. A dropdown menu will appear, listing all the teams you belong to.
3. Select a team to switch between them.

 ![image](https://mintcdn.com/resend/OWNnQaVDyqcGyhhN/images/teams-toggle.png?fit=max&auto=format&n=OWNnQaVDyqcGyhhN&q=85&s=d873d8c43f65af895d4fb025648f59d9)

## ​Change the team member roles

 As an admin of your team, you can change the role of members in your team.

1. Navigate to your [Team Settings](https://resend.com/settings/team).
2. Find the user you want to change.
3. Select the more options button  and choose **Change role**.

 ![Change role popover visible for team member](https://mintcdn.com/resend/OWNnQaVDyqcGyhhN/images/how-can-i-change-team-roles-1.png?fit=max&auto=format&n=OWNnQaVDyqcGyhhN&q=85&s=656430ad540c2b6143998583b2a71c97) Upon confirmation, your team member will be given the new role.

## ​Leave your Resend team

 You can leave your team by following these steps:

1. Navigate to your [Team Settings](https://resend.com/settings/team).
2. Under members, click on  next to your name for more options.
3. Select the **Leave Team** button.

 Upon confirmation, you will leave your team. If you are the last member of the team, leaving will permanently delete the
team and all its data. You will be prompted to confirm this action by typing
**DELETE**. If the team still has other members, but you are the only admin,
you will be prompted to promote another member to admin before leaving.

---

# Custom Unsubscribe Page

> Customize your unsubscribe page

When sending to Resend Audiences, Resend can [automatically handle the unsubscribe flow for you](https://resend.com/docs/dashboard/audiences/introduction#automatic-unsubscribes). You can customize your unsubscribe page to match your brand. Your unsubscribe page is used for every domain on your team.

1. Navigate to your [Unsubscribe Page](https://resend.com/settings/unsubscribe-page).
2. Click **Edit**.

 You can customize the following:

- **Title**: The title of the unsubscribe page.
- **Description**: The description of the unsubscribe page.
- **Logo**: The logo of the unsubscribe page.
- **Background Color**: The background color of the unsubscribe page.
- **Text Color**: The text color of the unsubscribe page.
- **Accent Color**: The accent color of the unsubscribe page.

  Pro plan users or higher can also remove the “Powered by Resend” footer.

---

# Using Templates

> Learn how to use templates to send emails.

Templates are stored on Resend and can be referenced when you send transactional emails. With Templates, define the structure and layout of a message and optionally include custom variables which will be replaced with the actual values when sending the email. Send only the Template `id` and `variables` (instead of sending the HTML), and Resend will render your final email and send it out.

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

await resend.emails.send({
  from: 'Acme <[email protected]>',
  to: '[email protected]',
  template: {
    id: 'order-confirmation',
    variables: {
      PRODUCT: 'Vintage Macintosh',
      PRICE: 499,
    },
  },
});
```

 Use Templates for transactional emails like:

- Login/Auth
- Onboarding
- Ecommerce
- Notifications
- Automations

## ​Add a Template

 You can add a Template:

- [In the dashboard](#add-a-template-in-the-dashboard)
- [From an existing email](#add-a-template-from-an-existing-email)
- [Using the API](#create-a-template-by-using-the-api)

### ​Add a Template in the dashboard

 The [Templates dashboard](https://resend.com/templates) shows all existing templates. Click **Create template** to start a new Template. ![Add a template](https://mintcdn.com/resend/8sUIFX1U2gAd2pqE/images/templates-introduction-dashboard.png?fit=max&auto=format&n=8sUIFX1U2gAd2pqE&q=85&s=d921d511df35a296c57e3a0223573f00)

### ​Add a Template from an existing email

 You can create a Template from an existing Broadcast. Locate your desired Broadcast in the [Broadcast dashboard](https://resend.com/broadcasts), click the more options button , and choose **Clone as template**. ![Add a template from an existing email](https://mintcdn.com/resend/8sUIFX1U2gAd2pqE/images/templates-clone-as-template.png?fit=max&auto=format&n=8sUIFX1U2gAd2pqE&q=85&s=f4757b737a5c4159636b32815f1efeb3) You can also import an HTML or [React Email](https://react.email) file to create a Template from your existing code. Create a new Template, then paste or drag in your HTML or React Email content.

### ​Create a Template by using the API

 You can also programmatically create a Template by using the API. The payload can optionally include variables to be used in the Template.

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

await resend.templates.create({
  name: 'order-confirmation',
  from: 'Resend Store <[email protected]>',
  subject: 'Thanks for your order!',
  html: '<p>Name: {{{PRODUCT}}}</p><p>Total: {{{PRICE}}}</p>',
  variables: [
    {
      key: 'PRODUCT',
      type: 'string',
      fallbackValue: 'item',
    },
    {
      key: 'PRICE',
      type: 'number',
      fallbackValue: 20,
    },
  ],
});
```

 View the [API reference](https://resend.com/docs/api-reference/templates/create-template) for more details.

## ​Add Variables

 Each Template may contain up to 20 variables. To add a custom variable, select **Variable** in the commands palette or type `{{` in the editor. Define the `name`, `type`, and `fallback_value` (optional). ![variable dropdown](https://mintcdn.com/resend/j2QOddewHJcRH5o-/images/templates-introduction-variables-custom.png?fit=max&auto=format&n=j2QOddewHJcRH5o-&q=85&s=88a202c3830e629559bc01785a33a138) You can also define custom variables [via the API](https://resend.com/docs/dashboard/templates/template-variables). The following variable names are reserved and cannot be used: `FIRST_NAME`,
`LAST_NAME`, `EMAIL`, `RESEND_UNSUBSCRIBE_URL`, `contact`,`this`. [Learn more about working with variables](https://resend.com/docs/dashboard/templates/template-variables).

## ​Send Test Emails

 You can send test emails to your inbox to preview your Template before sending it to your audience. Provide variable values to test the rendered Template in your inbox.

## ​Publish a Template

 By default, Templates are in a **draft** state. To use a Template to send emails, you must first **publish** it via the dashboard or [via the API](https://resend.com/docs/api-reference/templates/publish-template). ![Publish a template](https://mintcdn.com/resend/8sUIFX1U2gAd2pqE/images/templates-introduction-publish.png?fit=max&auto=format&n=8sUIFX1U2gAd2pqE&q=85&s=c39c711baf5719d8199ecdc3b2221480) For a more streamlined flow, create and publish a template in a single step. Node.js

```
await resend.templates.create({ ... }).publish();
```

 Once a Template is published, you can continue to edit it without impacting existing emails sent using the Template. As you work, your changes are saved as a draft, although you can also manually save drafts by pressing Cmd + S (Mac) or Ctrl + S (Windows). Only after publishing again will the changes be reflected in emails using the Template. [Learn more about Template version history](https://resend.com/docs/dashboard/templates/version-history).

## ​Send Emails with Templates

 When sending a transactional email, you can reference your Template and include your variables in the call. The Template variables will be replaced with the actual values.

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

await resend.emails.send({
  from: 'Acme <[email protected]>',
  to: '[email protected]',
  template: {
    id: 'order-confirmation',
    variables: {
      PRODUCT: 'Vintage Macintosh',
      PRICE: 499,
    },
  },
});
```

 Learn more about [sending emails](https://resend.com/docs/api-reference/emails/send-email) or sending [batch emails](https://resend.com/docs/api-reference/emails/send-batch-emails) with Templates via the API.

## ​Duplicate a Template

 You can also duplicate an existing Template in the dashboard or [via the API](https://resend.com/docs/api-reference/templates/duplicate-template). ![Duplicate a template](https://mintcdn.com/resend/8sUIFX1U2gAd2pqE/images/templates-introduction-duplicate.png?fit=max&auto=format&n=8sUIFX1U2gAd2pqE&q=85&s=05d9c56edfa20ed9e03b3a83c01cd130)

You can create a Template from an existing Broadcast. Locate your desired
Broadcast in the [Broadcast dashboard](https://resend.com/broadcasts), click
the more options button, and choose **Clone as template**.

## ​Delete a Template

 You can delete a Template via the dashboard by clicking on the **Delete** button or [via the API](https://resend.com/docs/api-reference/templates/delete-template). ![Delete a template](https://mintcdn.com/resend/8sUIFX1U2gAd2pqE/images/templates-introduction-delete.png?fit=max&auto=format&n=8sUIFX1U2gAd2pqE&q=85&s=5e7bc7c5e86e28f831c1d133d7961d73)

## ​Validation errors

 When sending an email using a Template, the Template variables will be replaced with the actual values. If a variable is not provided, the fallback value will be used. If no fallback value is provided, the email will not be sent and a validation error will be returned. [See the API reference for more details](https://resend.com/docs/api-reference/templates/create-template) or the [errors reference](https://resend.com/docs/api-reference/errors).

---

# Working with Variables

> How to work with custom variables in Templates.

Custom Template variables provide your team flexibility when sending emails. Define custom variables for your Template with optional fallback values which will be replaced with the actual values when sending the email.

## ​Create custom variables

 Each Template may contain up to 50 variables. To add a custom variable, select **Variable** in the commands palette or type `{{` in the editor. Define the `name`, `type`, and `fallback_value` (optional). ![variable dropdown](https://mintcdn.com/resend/j2QOddewHJcRH5o-/images/templates-introduction-variables-custom.png?fit=max&auto=format&n=j2QOddewHJcRH5o-&q=85&s=88a202c3830e629559bc01785a33a138)

You can also define custom variables via the API. The payload can optionally
include variables to be used in the Template.

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

await resend.templates.create({
  name: 'order-confirmation',
  html: '<p>Name: {{{PRODUCT}}}</p><p>Total: {{{PRICE}}}</p>',
  variables: [
    {
      key: 'PRODUCT',
      type: 'string',
      fallbackValue: 'item',
    },
    {
      key: 'PRICE',
      type: 'number',
      fallbackValue: 25,
    },
  ],
});
```

 The following variable names are reserved and cannot be used: `FIRST_NAME`,
`LAST_NAME`, `EMAIL`, `UNSUBSCRIBE_URL`, `contact`,`this`. Each variable is an object with the following properties:

- `key`: The key of the variable. We recommend capitalizing the key. (e.g. `PRODUCT_NAME`).
- `type`: The type of the variable (`'string'` or `'number'`).
- `fallback_value`: The fallback value of the variable. If no fallback value is provided, you must provide a value for the variable when sending an email using the template.

 [See the API reference for more details](https://resend.com/docs/api-reference/templates/create-template).

## ​Fallback values

 When you define a variable, you can optionally define a fallback value. This value will be used when sending the email if you fail to provide a value in your call.  In the editor, if you fail to provide a fallback value, a warning sign will show for the variable. To edit a variable’s fallback value, click on the variable chip in your template and use the Inspector sidebar on the right to update the fallback value. [As shown above](#create-template-with-variables), you can also include fallback values when creating a Template via the API.

## ​Send Test Emails

 You can send test emails to your inbox to preview your Template before sending it to your audience. Provide variable values to test the rendered Template in your inbox.

## ​Send a Template with Variables

 When sending a transactional email, you can reference your Template and include your variables in the call. The Template variables will be replaced with the actual values.

- `id`: id of the published template
- `variables`: array of variable objects (if applicable)

 Both the `/emails` and `/emails/batch` endpoints support Templates.

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.emails.send({
  from: 'Acme <[email protected]>',
  to: ['[email protected]'],
  subject: 'hello world',
  template: {
    id: 'f3b9756c-f4f4-44da-bc00-9f7903c8a83f',
    variables: {
      PRODUCT: 'Laptop',
    },
  },
});
```

 If a `template` is provided, you cannot send `html`, `text`, or `react` in the payload, otherwise the API will return a validation error.When sending a template, the payload for `from`, `subject`, and `reply_to` take precedence over the template’s defaults for these fields. If the template does not provide a default value for these fields, you must provide them in the payload. Learn more about [sending emails](https://resend.com/docs/api-reference/emails/send-email) or sending [batch emails](https://resend.com/docs/api-reference/emails/send-batch-emails) with Templates via the API.

---

# Version History

> Best practices for using templates in production environments.

Templates in production require a workflow that lets you make changes safely without disrupting active emails. As you build your Template, your entire team can collaborate on the content and design in real-time with full version history.

## ​Draft vs Published

 Templates start in a **draft** state and must be published before they can be used to send emails. This separation allows you to:

- Test templates thoroughly before going live
- Make changes without affecting active emails
- Maintain version control over your email content

 Once you **publish** a template, this published version will be used to send emails until you publish again. You can continue to work on a template in draft state without affecting the published version and the editor will automaticalyl save your progress.

```
// Create template
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

await resend.templates.create({
  name: 'order-confirmation',
  from: 'Resend Store <store@resend.com>',
  subject: 'Thanks for your order!',
  html: "<p>Name: {{{PRODUCT}}}</p><p>Total: {{{PRICE}}}</p>",
  variables: [
    {
      key: 'PRODUCT',
      type: 'string',
      fallbackValue: 'item'
    },
    {
      key: 'PRICE',
      type: 'number',
      fallbackValue: 20
    }
  ]
});

// Publish template
await resend.templates.publish('template_id');

// Or create and publish a template in one step
await resend.templates.create({ ... }).publish();
```

 After you publish a template, you can freely work on it through the editor or [via the API](https://resend.com/docs/api-reference/templates/update-template) without affecting the published version. This allows you to test and validate new edits before sending them to users.

## ​Version History

 As you work on a Template, your changes are saved as a draft, although you can also manually save drafts by pressing Cmd + S (Mac) or Ctrl + S (Windows). Only after publishing again will the changes be reflected in emails using the Template. Each template contains a version history that helps you track changes your team has made over time. You can view the version history by clicking the three dots in the top right corner of the template editor and selecting **Version History**. Through the version history, you can preview each version, who made them, and when they were made. You can also revert to a previous version if needed.  Reverting creates a new draft based on the selected version’s content, without affecting the published template.

## ​Iterating on a template

 You can work on a new draft version of your published template, update the design and messaging, then test it thoroughly before publishing it again. Your email sending will continue to use the current published version until you’re ready to make the switch, without the need to create a new separate template or risk leaking your new logo. This behavior is also useful to avoid breaking changes when you need to edit a template that’s in production. Add or remove variables, update the design, and more without affecting your existing emails or raising validation errors.

---

# Topics

> Give your users more control over their subscription preferences.

Managing subscribers and unsubscribers is a critical part of any email implementation. Topics are used by your contacts to manage their email preferences. When you send [Broadcasts](https://resend.com/docs/dashboard/broadcasts/introduction), you can optionally scope sending to a particular Topic. Not only does scoping your sending help you send more precisely, but it also allows your users to manage their preferences with more control. Learn more about [customizing your team’s unsubscribe
page](https://resend.com/docs/dashboard/settings/unsubscribe-page)

## ​Add a Topic

 You can create a new Topic from the [dashboard](https://resend.com/audience/topics) or [via the API](https://resend.com/docs/api-reference/topics/create-topic).

1. Click **Create Topic**.
2. Give your Topic a name.
3. Give your Topic a description (optional).
4. Select **Opt-in** or **Opt-out** as the default subscription. This value **cannot** be changed later.
  - **Opt-in**: all Contacts will receive the email unless they have explicitly unsubscribed from that Topic.
  - **Opt-out**: subscribers will not receive the email unless they have explicitly subscribed to that Topic.
5. Select **Public** or **Private** as the visibility.
  - **Private**: only Contacts who are opted in to the Topic can see it on the unsubscribe page.
  - **Public**: all Contacts can see the Topic on the unsubscribe page.

 ![Add Topic](https://mintcdn.com/resend/WTZjpSkJsZf7Ubl_/images/dashboard-topics-add.png?fit=max&auto=format&n=WTZjpSkJsZf7Ubl_&q=85&s=0f3f95d5f53d7628b164c04e28e7b4be)

## ​View all Topics

 The [dashboard](https://resend.com/audience/topics) shows you all the Topics you have created along with their details. ![View All Topics](https://mintcdn.com/resend/WTZjpSkJsZf7Ubl_/images/dashboard-topics-view-all.png?fit=max&auto=format&n=WTZjpSkJsZf7Ubl_&q=85&s=172afe116b01792855837fc4f987a4be) You can also [retrieve a single Topic](https://resend.com/docs/api-reference/topics/get-topic) or [list all your Topics](https://resend.com/docs/api-reference/topics/list-topics) via the API.

## ​Edit Topic details

 After creating a Topic, you can edit the following details:

- Name
- Description
- Visibility

 To edit a Topic, click the **More options**  button and then **Edit Topic**. ![View edit topic](https://mintcdn.com/resend/WTZjpSkJsZf7Ubl_/images/dashboard-topics-edit.png?fit=max&auto=format&n=WTZjpSkJsZf7Ubl_&q=85&s=7f683116ec1dc37aa82c33de94bbd941) You can also [update a Topic](https://resend.com/docs/api-reference/topics/update-topic) via the API. You cannot edit the default subscription value after it has been created.

## ​Delete a Topic

 You can delete a Topic by clicking the **More options**  button and then **Remove Topic**. ![Delete Topic](https://mintcdn.com/resend/WTZjpSkJsZf7Ubl_/images/dashboard-topics-remove.png?fit=max&auto=format&n=WTZjpSkJsZf7Ubl_&q=85&s=ad5a6bf19aa0f4d858959b91792de167) You can also [delete a Topic](https://resend.com/docs/api-reference/topics/delete-topic) via the API.

## ​Editing Topics for a Contact

 As you receive [proper consent to email Contacts](https://resend.com/docs/knowledge-base/what-counts-as-email-consent), add the Contact to a given Topic. A Contact can belong to multiple Topics. You can add a Contact to a Topic via the dashboard by expanding the **More options**  and then **Edit Contact**. Add or remove Topics for a given Contact. ![Add Contact to Topic](https://mintcdn.com/resend/WTZjpSkJsZf7Ubl_/images/dashboard-save-contact-topic.png?fit=max&auto=format&n=WTZjpSkJsZf7Ubl_&q=85&s=66e212d282f450c371f42a1b214029cd) The **Subscribed** status is a global setting that enables or disables sending to a Contact for Broadcasts.

- If a Contact’s **Subscribed** status is
  **false**, they will not receive emails from your account, even if they have
  opted-in to a specific Topic.
- If the **Subscribed** status is **true**, they
  can receive emails from your account.

Learn more about [managing your unsubscribe list](https://resend.com/docs/dashboard/audiences/managing-unsubscribe-list).

## ​Sending Broadcast with a Topic

 You can send with a Topic in the Broadcast editor from the Topics dropdown menu. ![Send emails with a Topic](https://mintcdn.com/resend/m2xttJpF68pi6Mw0/images/dashboard-broadcast-topics.png?fit=max&auto=format&n=m2xttJpF68pi6Mw0&q=85&s=95c0a3999269605a66102c15400c5a58) You can also send with a Topic via the [Broadcast API](https://resend.com/docs/api-reference/broadcasts/create-broadcast).

## ​Unsubscribing from a Topic

 If a Contact clicks a Broadcast unsubscribe link, they will see a preference page where they can:

- Unsubscribe from certain **Topics** (types of email)
- Or unsubscribe from **everything** you send

 If they unsubscribe from a Topic or several Topics, they will no longer receive emails for those Topics. If they unsubscribe from all emails from your account, Broadcasts will no longer send to them. You can [customize your unsubscribe page with your branding](https://resend.com/docs/dashboard/settings/unsubscribe-page) from your team settings. ![See Topics on the Unsubscribe Page](https://mintcdn.com/resend/WTZjpSkJsZf7Ubl_/images/dashboard-unsubscribe-page-topics.png?fit=max&auto=format&n=WTZjpSkJsZf7Ubl_&q=85&s=11896d54a3e2bdb510a5b666ae7ee8a8)
