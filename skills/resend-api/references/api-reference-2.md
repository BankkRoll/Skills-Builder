# Cancel Email and more

# Cancel Email

> Cancel a scheduled email.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.emails.cancel(
  '49a3999c-0ce1-4ea6-ab68-afcd6dc2e794',
);
```

```
{
  "object": "email",
  "id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
}
```

POSThttps://api.resend.com/emails/:id/cancel

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.emails.cancel(
  '49a3999c-0ce1-4ea6-ab68-afcd6dc2e794',
);
```

```
{
  "object": "email",
  "id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
}
```

## ​Path Parameters

 [​](#param-id)idstringrequiredThe Email ID.[Update Email](https://resend.com/docs/api-reference/emails/update-email)[Retrieve Attachment](https://resend.com/docs/api-reference/emails/retrieve-email-attachment)Ctrl +I$/$

---

# List Attachments

> Retrieve a list of attachments from a sent email.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.emails.attachments.list({
  emailId: '4ef9a417-02e9-4d39-ad75-9611e0fcc33c',
});
```

```
{
  "object": "list",
  "has_more": false,
  "data": [
    {
      "id": "2a0c9ce0-3112-4728-976e-47ddcd16a318",
      "filename": "avatar.png",
      "size": 4096,
      "content_type": "image/png",
      "content_disposition": "inline",
      "content_id": "img001",
      "download_url": "https://outbound-cdn.resend.com/4ef9a417-02e9-4d39-ad75-9611e0fcc33c/attachments/2a0c9ce0-3112-4728-976e-47ddcd16a318?some-params=example&signature=sig-123",
      "expires_at": "2025-10-17T14:29:41.521Z"
    }
  ]
}
```

GEThttps://api.resend.com/emails/:email_id/attachments

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.emails.attachments.list({
  emailId: '4ef9a417-02e9-4d39-ad75-9611e0fcc33c',
});
```

```
{
  "object": "list",
  "has_more": false,
  "data": [
    {
      "id": "2a0c9ce0-3112-4728-976e-47ddcd16a318",
      "filename": "avatar.png",
      "size": 4096,
      "content_type": "image/png",
      "content_disposition": "inline",
      "content_id": "img001",
      "download_url": "https://outbound-cdn.resend.com/4ef9a417-02e9-4d39-ad75-9611e0fcc33c/attachments/2a0c9ce0-3112-4728-976e-47ddcd16a318?some-params=example&signature=sig-123",
      "expires_at": "2025-10-17T14:29:41.521Z"
    }
  ]
}
```

## Query Parameters

Note that the `limit` parameter is *optional*. If you do not provide a `limit`, all attachments will be returned in a single response.[​](#limit)limitnumberNumber of attachments to retrieve.

- Maximum value: `100`
- Minimum value: `1`

[​](#after)afterstringThe ID *after* which we'll retrieve more attachments (for pagination). This ID will *not* be included in the returned list. Cannot be used with the`before` parameter.[​](#before)beforestringThe ID *before* which we'll retrieve more attachments (for pagination). This ID will *not* be included in the returned list. Cannot be used with the `after` parameter.You can only use either `after` or `before` parameter, not both. See our [pagination guide](https://resend.com/docs/api-reference/pagination) for more information.

## ​Path Parameters

 [​](#param-email-id)email_idstringrequiredThe Email ID.[Retrieve Attachment](https://resend.com/docs/api-reference/emails/retrieve-email-attachment)[Retrieve Received Email](https://resend.com/docs/api-reference/emails/retrieve-received-email)Ctrl +I$/$

---

# List Sent Emails

> Retrieve a list of emails sent by your team.

[Resend home page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.emails.list();
```

```
{
  "object": "list",
  "has_more": false,
  "data": [
    {
      "id": "4ef9a417-02e9-4d39-ad75-9611e0fcc33c",
      "to": ["delivered@resend.dev"],
      "from": "Acme <onboarding@resend.dev>",
      "created_at": "2023-04-03T22:13:42.674981+00:00",
      "subject": "Hello World",
      "bcc": null,
      "cc": null,
      "reply_to": null,
      "last_event": "delivered",
      "scheduled_at": null
    },
    {
      "id": "3a9f8c2b-1e5d-4f8a-9c7b-2d6e5f8a9c7b",
      "to": ["user@example.com"],
      "from": "Acme <onboarding@resend.dev>",
      "created_at": "2023-04-03T21:45:12.345678+00:00",
      "subject": "Welcome to Acme",
      "bcc": null,
      "cc": null,
      "reply_to": null,
      "last_event": "opened",
      "scheduled_at": null
    }
  ]
}
```

GEThttps://api.resend.com/emails

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.emails.list();
```

```
{
  "object": "list",
  "has_more": false,
  "data": [
    {
      "id": "4ef9a417-02e9-4d39-ad75-9611e0fcc33c",
      "to": ["delivered@resend.dev"],
      "from": "Acme <onboarding@resend.dev>",
      "created_at": "2023-04-03T22:13:42.674981+00:00",
      "subject": "Hello World",
      "bcc": null,
      "cc": null,
      "reply_to": null,
      "last_event": "delivered",
      "scheduled_at": null
    },
    {
      "id": "3a9f8c2b-1e5d-4f8a-9c7b-2d6e5f8a9c7b",
      "to": ["user@example.com"],
      "from": "Acme <onboarding@resend.dev>",
      "created_at": "2023-04-03T21:45:12.345678+00:00",
      "subject": "Welcome to Acme",
      "bcc": null,
      "cc": null,
      "reply_to": null,
      "last_event": "opened",
      "scheduled_at": null
    }
  ]
}
```

You can list all emails sent by your team. The list returns references to individual emails. If needed, you can use the `id` of an email to retrieve the email HTML to plain text using the [Retrieve Email](https://resend.com/docs/api-reference/emails/retrieve-email) endpoint or the [Retrieve Attachments](https://resend.com/docs/api-reference/emails/list-email-attachments) endpoint to get an email’s attachments. This endpoint only returns emails sent by your team. If you need to list
emails received by your domain, use the [List Received
Emails](https://resend.com/docs/api-reference/emails/list-received-emails) endpoint.

## Query Parameters

[​](#limit)limitnumberNumber of emails to retrieve.

- Default value: `20`
- Maximum value: `100`
- Minimum value: `1`

[​](#after)afterstringThe ID *after* which we'll retrieve more emails (for pagination). This ID will *not* be included in the returned list. Cannot be used with the`before` parameter.[​](#before)beforestringThe ID *before* which we'll retrieve more emails (for pagination). This ID will *not* be included in the returned list. Cannot be used with the `after` parameter.You can only use either `after` or `before` parameter, not both. See our [pagination guide](https://resend.com/docs/api-reference/pagination) for more information.[Retrieve Email](https://resend.com/docs/api-reference/emails/retrieve-email)[Update Email](https://resend.com/docs/api-reference/emails/update-email)Ctrl+I

---

# List Attachments

> Retrieve a list of attachments from a received email.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.emails.receiving.attachments.list({
  emailId: '4ef9a417-02e9-4d39-ad75-9611e0fcc33c',
});
```

```
{
  "object": "list",
  "has_more": false,
  "data": [
    {
      "id": "2a0c9ce0-3112-4728-976e-47ddcd16a318",
      "filename": "avatar.png",
      "size": 4096,
      "content_type": "image/png",
      "content_disposition": "inline",
      "content_id": "img001",
      "download_url": "https://inbound-cdn.resend.com/4ef9a417-02e9-4d39-ad75-9611e0fcc33c/attachments/2a0c9ce0-3112-4728-976e-47ddcd16a318?some-params=example&signature=sig-123",
      "expires_at": "2025-10-17T14:29:41.521Z"
    }
  ]
}
```

GEThttps://api.resend.com/emails/receiving/:email_id/attachments

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.emails.receiving.attachments.list({
  emailId: '4ef9a417-02e9-4d39-ad75-9611e0fcc33c',
});
```

```
{
  "object": "list",
  "has_more": false,
  "data": [
    {
      "id": "2a0c9ce0-3112-4728-976e-47ddcd16a318",
      "filename": "avatar.png",
      "size": 4096,
      "content_type": "image/png",
      "content_disposition": "inline",
      "content_id": "img001",
      "download_url": "https://inbound-cdn.resend.com/4ef9a417-02e9-4d39-ad75-9611e0fcc33c/attachments/2a0c9ce0-3112-4728-976e-47ddcd16a318?some-params=example&signature=sig-123",
      "expires_at": "2025-10-17T14:29:41.521Z"
    }
  ]
}
```

## Query Parameters

Note that the `limit` parameter is *optional*. If you do not provide a `limit`, all  attachments  will be returned in a single response.[​](#limit)limitnumberNumber of  attachments  to retrieve.

- Maximum value: `100`
- Minimum value: `1`

[​](#after)afterstringThe ID *after* which we'll retrieve more  attachments  (for pagination). This ID will *not* be included in the returned list. Cannot be used with the`before` parameter.[​](#before)beforestringThe ID *before* which we'll retrieve more  attachments  (for pagination). This ID will *not* be included in the returned list. Cannot be used with the `after` parameter.You can only use either `after` or `before`  parameter, not both. See our  [pagination guide](https://resend.com/docs/api-reference/pagination) for more information.

## ​Path Parameters

 [​](#param-email-id)email_idstringrequiredThe Email ID.

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.emails.receiving.attachments.list({
  emailId: '4ef9a417-02e9-4d39-ad75-9611e0fcc33c',
});
```

```
{
  "object": "list",
  "has_more": false,
  "data": [
    {
      "id": "2a0c9ce0-3112-4728-976e-47ddcd16a318",
      "filename": "avatar.png",
      "size": 4096,
      "content_type": "image/png",
      "content_disposition": "inline",
      "content_id": "img001",
      "download_url": "https://inbound-cdn.resend.com/4ef9a417-02e9-4d39-ad75-9611e0fcc33c/attachments/2a0c9ce0-3112-4728-976e-47ddcd16a318?some-params=example&signature=sig-123",
      "expires_at": "2025-10-17T14:29:41.521Z"
    }
  ]
}
```

[Retrieve Attachment](https://resend.com/docs/api-reference/emails/retrieve-received-email-attachment)[Create Domain](https://resend.com/docs/api-reference/domains/create-domain)⌘ I$/$

---

# List Received Emails

> Retrieve a list of received emails for the authenticated user.

[Resend home page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.emails.receiving.list();
```

```
{
  "object": "list",
  "has_more": true,
  "data": [
    {
      "id": "a39999a6-88e3-48b1-888b-beaabcde1b33",
      "to": ["recipient@example.com"],
      "from": "sender@example.com",
      "created_at": "2025-10-09 14:37:40.951732+00",
      "subject": "Hello World",
      "bcc": [],
      "cc": [],
      "reply_to": [],
      "message_id": "<111-222-333@email.provider.example.com>",
      "attachments": [
        {
          "filename": "example.txt",
          "content_type": "text/plain",
          "content_id": null,
          "content_disposition": "attachment",
          "id": "47e999c7-c89c-4999-bf32-aaaaa1c3ff21",
          "size": 13
        }
      ]
    }
  ]
}
```

GEThttps://api.resend.com/emails/receiving

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.emails.receiving.list();
```

```
{
  "object": "list",
  "has_more": true,
  "data": [
    {
      "id": "a39999a6-88e3-48b1-888b-beaabcde1b33",
      "to": ["recipient@example.com"],
      "from": "sender@example.com",
      "created_at": "2025-10-09 14:37:40.951732+00",
      "subject": "Hello World",
      "bcc": [],
      "cc": [],
      "reply_to": [],
      "message_id": "<111-222-333@email.provider.example.com>",
      "attachments": [
        {
          "filename": "example.txt",
          "content_type": "text/plain",
          "content_id": null,
          "content_disposition": "attachment",
          "id": "47e999c7-c89c-4999-bf32-aaaaa1c3ff21",
          "size": 13
        }
      ]
    }
  ]
}
```

You can list all emails received by your team. The list returns references to individual emails. If needed, you can use the `id` of an email to retrieve the email HTML to plain text using the [Retrieve Received Email](https://resend.com/docs/api-reference/emails/retrieve-received-email) endpoint or the [Retrieve Received Attachment](https://resend.com/docs/api-reference/emails/retrieve-received-email-attachment) endpoint to get an email’s attachments. This endpoint only returns emails received by your team. If you need to list
emails sent by your team, use the [List Sent
Emails](https://resend.com/docs/api-reference/emails/list-emails) endpoint.

## Query Parameters

Note that the `limit` parameter is *optional*. If you do not provide a `limit`, all emails will be returned in a single response.[​](#limit)limitnumberNumber of emails to retrieve.

- Maximum value: `100`
- Minimum value: `1`

[​](#after)afterstringThe ID *after* which we'll retrieve more emails (for pagination). This ID will *not* be included in the returned list. Cannot be used with the`before` parameter.[​](#before)beforestringThe ID *before* which we'll retrieve more emails (for pagination). This ID will *not* be included in the returned list. Cannot be used with the `after` parameter.You can only use either `after` or `before` parameter, not both. See our [pagination guide](https://resend.com/docs/api-reference/pagination) for more information.[Retrieve Received Email](https://resend.com/docs/api-reference/emails/retrieve-received-email)[Retrieve Attachment](https://resend.com/docs/api-reference/emails/retrieve-received-email-attachment)Ctrl+I

---

# Retrieve Attachment

> Retrieve a single attachment from a sent email.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.emails.attachments.get({
  id: '2a0c9ce0-3112-4728-976e-47ddcd16a318',
  emailId: '4ef9a417-02e9-4d39-ad75-9611e0fcc33c',
});
```

```
{
  "object": "attachment",
  "id": "2a0c9ce0-3112-4728-976e-47ddcd16a318",
  "filename": "avatar.png",
  "size": 4096,
  "content_type": "image/png",
  "content_disposition": "inline",
  "content_id": "img001",
  "download_url": "https://outbound-cdn.resend.com/4ef9a417-02e9-4d39-ad75-9611e0fcc33c/attachments/2a0c9ce0-3112-4728-976e-47ddcd16a318?some-params=example&signature=sig-123",
  "expires_at": "2025-10-17T14:29:41.521Z"
}
```

GEThttps://api.resend.com/emails/:email_id/attachments/:id

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.emails.attachments.get({
  id: '2a0c9ce0-3112-4728-976e-47ddcd16a318',
  emailId: '4ef9a417-02e9-4d39-ad75-9611e0fcc33c',
});
```

```
{
  "object": "attachment",
  "id": "2a0c9ce0-3112-4728-976e-47ddcd16a318",
  "filename": "avatar.png",
  "size": 4096,
  "content_type": "image/png",
  "content_disposition": "inline",
  "content_id": "img001",
  "download_url": "https://outbound-cdn.resend.com/4ef9a417-02e9-4d39-ad75-9611e0fcc33c/attachments/2a0c9ce0-3112-4728-976e-47ddcd16a318?some-params=example&signature=sig-123",
  "expires_at": "2025-10-17T14:29:41.521Z"
}
```

## ​Path Parameters

 [​](#param-id)idstringrequiredThe Attachment ID. [​](#param-email-id)email_idstringrequiredThe Email ID.

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.emails.attachments.get({
  id: '2a0c9ce0-3112-4728-976e-47ddcd16a318',
  emailId: '4ef9a417-02e9-4d39-ad75-9611e0fcc33c',
});
```

```
{
  "object": "attachment",
  "id": "2a0c9ce0-3112-4728-976e-47ddcd16a318",
  "filename": "avatar.png",
  "size": 4096,
  "content_type": "image/png",
  "content_disposition": "inline",
  "content_id": "img001",
  "download_url": "https://outbound-cdn.resend.com/4ef9a417-02e9-4d39-ad75-9611e0fcc33c/attachments/2a0c9ce0-3112-4728-976e-47ddcd16a318?some-params=example&signature=sig-123",
  "expires_at": "2025-10-17T14:29:41.521Z"
}
```

[Cancel Email](https://resend.com/docs/api-reference/emails/cancel-email)[List Attachments](https://resend.com/docs/api-reference/emails/list-email-attachments)⌘ I$/$

---

# Retrieve Email

> Retrieve a single email.

[Resend home page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.emails.get(
  '37e4414c-5e25-4dbc-a071-43552a4bd53b',
);
```

```
{
  "object": "email",
  "id": "4ef9a417-02e9-4d39-ad75-9611e0fcc33c",
  "to": ["delivered@resend.dev"],
  "from": "Acme <onboarding@resend.dev>",
  "created_at": "2023-04-03T22:13:42.674981+00:00",
  "subject": "Hello World",
  "html": "Congrats on sending your <strong>first email</strong>!",
  "text": null,
  "bcc": [],
  "cc": [],
  "reply_to": [],
  "last_event": "delivered",
  "scheduled_at": null,
  "tags": [
    {
      "name": "category",
      "value": "confirm_email"
    }
  ]
}
```

GEThttps://api.resend.com/emails/:id

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.emails.get(
  '37e4414c-5e25-4dbc-a071-43552a4bd53b',
);
```

```
{
  "object": "email",
  "id": "4ef9a417-02e9-4d39-ad75-9611e0fcc33c",
  "to": ["delivered@resend.dev"],
  "from": "Acme <onboarding@resend.dev>",
  "created_at": "2023-04-03T22:13:42.674981+00:00",
  "subject": "Hello World",
  "html": "Congrats on sending your <strong>first email</strong>!",
  "text": null,
  "bcc": [],
  "cc": [],
  "reply_to": [],
  "last_event": "delivered",
  "scheduled_at": null,
  "tags": [
    {
      "name": "category",
      "value": "confirm_email"
    }
  ]
}
```

## ​Path Parameters

 [​](#param-id)idstringrequiredThe Email ID. See all available `last_event` types in [the Email Events
overview](https://resend.com/docs/dashboard/emails/introduction#understand-email-events).[Send Batch Emails](https://resend.com/docs/api-reference/emails/send-batch-emails)[List Sent Emails](https://resend.com/docs/api-reference/emails/list-emails)Ctrl+I

---

# Retrieve Attachment

> Retrieve a single attachment from a received email.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.emails.receiving.attachments.get({
  id: '2a0c9ce0-3112-4728-976e-47ddcd16a318',
  emailId: '4ef9a417-02e9-4d39-ad75-9611e0fcc33c',
});
```

```
{
  "object": "attachment",
  "id": "2a0c9ce0-3112-4728-976e-47ddcd16a318",
  "filename": "avatar.png",
  "size": 4096,
  "content_type": "image/png",
  "content_disposition": "inline",
  "content_id": "img001",
  "download_url": "https://inbound-cdn.resend.com/4ef9a417-02e9-4d39-ad75-9611e0fcc33c/attachments/2a0c9ce0-3112-4728-976e-47ddcd16a318?some-params=example&signature=sig-123",
  "expires_at": "2025-10-17T14:29:41.521Z"
}
```

GEThttps://api.resend.com/emails/receiving/:email_id/attachments/:id

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.emails.receiving.attachments.get({
  id: '2a0c9ce0-3112-4728-976e-47ddcd16a318',
  emailId: '4ef9a417-02e9-4d39-ad75-9611e0fcc33c',
});
```

```
{
  "object": "attachment",
  "id": "2a0c9ce0-3112-4728-976e-47ddcd16a318",
  "filename": "avatar.png",
  "size": 4096,
  "content_type": "image/png",
  "content_disposition": "inline",
  "content_id": "img001",
  "download_url": "https://inbound-cdn.resend.com/4ef9a417-02e9-4d39-ad75-9611e0fcc33c/attachments/2a0c9ce0-3112-4728-976e-47ddcd16a318?some-params=example&signature=sig-123",
  "expires_at": "2025-10-17T14:29:41.521Z"
}
```

## ​Path Parameters

 [​](#param-id)idstringrequiredThe Attachment ID. [​](#param-email-id)email_idstringrequiredThe Email ID.[List Received Emails](https://resend.com/docs/api-reference/emails/list-received-emails)[List Attachments](https://resend.com/docs/api-reference/emails/list-received-email-attachments)Ctrl +I$/$

---

# Retrieve Received Email

> Retrieve a single received email.

[Resend home page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.emails.receiving.get(
  '37e4414c-5e25-4dbc-a071-43552a4bd53b',
);
```

```
{
  "object": "email",
  "id": "4ef9a417-02e9-4d39-ad75-9611e0fcc33c",
  "to": ["delivered@resend.dev"],
  "from": "Acme <onboarding@resend.dev>",
  "created_at": "2023-04-03T22:13:42.674981+00:00",
  "subject": "Hello World",
  "html": "Congrats on sending your <strong>first email</strong>!",
  "text": null,
  "headers": {
    "return-path": "lucas.costa@resend.com",
    "mime-version": "1.0"
  },
  "bcc": [],
  "cc": [],
  "reply_to": [],
  "message_id": "<example+123>",
  "raw": {
    "download_url": "https://example.resend.com/receiving/raw/054da427-439a-4e91-b785-e4fb1966285f?Signature=...",
    "expires_at": "2023-04-03T23:13:42.674981+00:00"
  },
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
```

GEThttps://api.resend.com/emails/receiving/:id

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.emails.receiving.get(
  '37e4414c-5e25-4dbc-a071-43552a4bd53b',
);
```

```
{
  "object": "email",
  "id": "4ef9a417-02e9-4d39-ad75-9611e0fcc33c",
  "to": ["delivered@resend.dev"],
  "from": "Acme <onboarding@resend.dev>",
  "created_at": "2023-04-03T22:13:42.674981+00:00",
  "subject": "Hello World",
  "html": "Congrats on sending your <strong>first email</strong>!",
  "text": null,
  "headers": {
    "return-path": "lucas.costa@resend.com",
    "mime-version": "1.0"
  },
  "bcc": [],
  "cc": [],
  "reply_to": [],
  "message_id": "<example+123>",
  "raw": {
    "download_url": "https://example.resend.com/receiving/raw/054da427-439a-4e91-b785-e4fb1966285f?Signature=...",
    "expires_at": "2023-04-03T23:13:42.674981+00:00"
  },
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
```

## ​Path Parameters

 [​](#param-id)idstringrequiredThe ID for the received email.

## ​Response Parameters

 [​](#param-raw)rawobject | nullRaw email content download information. Contains a signed URL to download the original email file including all attachments.

Hide properties

[​](#param-download-url)download_urlstringSigned CloudFront URL to download the raw email file.[​](#param-expires-at)expires_atstringISO 8601 timestamp indicating when the download URL expires.[List Attachments](https://resend.com/docs/api-reference/emails/list-email-attachments)[List Received Emails](https://resend.com/docs/api-reference/emails/list-received-emails)Ctrl+I

---

# Send Batch Emails

> Trigger up to 100 batch emails at once.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.batch.send([
  {
    from: 'Acme <[email protected]>',
    to: ['[email protected]'],
    subject: 'hello world',
    html: '<h1>it works!</h1>',
  },
  {
    from: 'Acme <[email protected]>',
    to: ['[email protected]'],
    subject: 'world hello',
    html: '<p>it works!</p>',
  },
]);
```

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

POSThttps://api.resend.com/emails/batch

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.batch.send([
  {
    from: 'Acme <[email protected]>',
    to: ['[email protected]'],
    subject: 'hello world',
    html: '<h1>it works!</h1>',
  },
  {
    from: 'Acme <[email protected]>',
    to: ['[email protected]'],
    subject: 'world hello',
    html: '<p>it works!</p>',
  },
]);
```

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

Instead of sending one email per HTTP request, we provide a batching endpoint that permits you to send up to 100 emails in a single API call.

## ​Body Parameters

 [​](#param-from)fromstringrequiredSender email address.To include a friendly name, use the format `"Your Name <[email protected]>"`. [​](#param-to)tostring | string[]requiredRecipient email address. For multiple addresses, send as an array of strings.
Max 50. [​](#param-subject)subjectstringrequiredEmail subject. [​](#param-bcc)bccstring | string[]Bcc recipient email address. For multiple addresses, send as an array of
strings. [​](#param-cc)ccstring | string[]Cc recipient email address. For multiple addresses, send as an array of
strings.   [​](#param-html)htmlstringThe HTML version of the message. [​](#param-text)textstringThe plain text version of the message.If not provided, the HTML will be used to generate a plain text version. You
can opt out of this behavior by setting value to an empty string. [​](#param-react)reactReact.ReactNodeThe React component used to write the message. *Only available in the Node.js
SDK.* [​](#param-headers)headersobjectCustom headers to add to the email.   [​](#param-tags)tagsarrayCustom data passed in key/value pairs.[See examples](https://resend.com/docs/dashboard/emails/tags).

Hide   properties

[​](#param-name)namestringrequiredThe name of the email tag.It can only contain ASCII letters (a–z, A–Z), numbers (0–9), underscores (_), or dashes (-).It can contain no more than 256 characters.[​](#param-value)valuestringrequiredThe value of the email tag.It can only contain ASCII letters (a–z, A–Z), numbers (0–9), underscores (_), or dashes (-).It can contain no more than 256 characters. [​](#param-template)templateobjectTo send using a template, provide a `template` object with:

- `id`: the id *or* the alias of the published template
- `variables`: an object with a key for each variable (if applicable)

If a `template` is provided, you cannot send `html`, `text`, or `react` in the payload, otherwise the API will return a validation error.When sending a template, the payload for `from`, `subject`, and `reply_to` take precedence over the template’s defaults for these fields. If the template does not provide a default value for these fields, you must provide them in the payload. [​](#param-id)idstringrequiredThe id of the published email template. Required if `template` is provided. Only published templates can be used when sending emails. [​](#param-variables)variablesobjectTemplate variables object with key/value pairs.

```
variables: {
	CTA: 'Sign up now',
	CTA_LINK: 'https://example.com/signup'
}
```

When sending the template, the HTML will be parsed. If all the variables used in the template were provided, the email will be sent. If not, the call will throw a validation error.See the [errors reference](https://resend.com/docs/api-reference/errors) for more details or [learn more about templates](https://resend.com/docs/dashboard/templates/introduction).

Hide   properties

[​](#param-key)keystringrequiredThe key of the variable.May only contain ASCII letters (a–z, A–Z), numbers (0–9), and underscores (_). The following variable names are reserved and cannot be used: `FIRST_NAME`, `LAST_NAME`, `EMAIL`, `UNSUBSCRIBE_URL`.It can contain no more than 50 characters.[​](#param-value-1)valuestring | numberrequiredThe value of the variable.Observe these technical limitations:

- `string`: maximum length of 2,000 characters
- `number`: not greater than 2^53 - 1

## ​Headers

 [​](#param-idempotency-key)Idempotency-KeystringAdd an idempotency key to prevent duplicated emails.

- Should be **unique per API request**
- Idempotency keys expire after **24 hours**
- Have a maximum length of **256 characters**

[Learn more about idempotency keys →](https://resend.com/docs/dashboard/emails/idempotency-keys)

## ​Limitations

 The `attachments` and `scheduled_at` fields are not supported yet.

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.batch.send([
  {
    from: 'Acme <[email protected]>',
    to: ['[email protected]'],
    subject: 'hello world',
    html: '<h1>it works!</h1>',
  },
  {
    from: 'Acme <[email protected]>',
    to: ['[email protected]'],
    subject: 'world hello',
    html: '<p>it works!</p>',
  },
]);
```

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

[Send Email](https://resend.com/docs/api-reference/emails/send-email)[Retrieve Email](https://resend.com/docs/api-reference/emails/retrieve-email)⌘ I$/$

---

# Send Email

> Start sending emails through the Resend Email API.

[Resend home page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.emails.send({
  from: 'Acme <onboarding@resend.dev>',
  to: ['delivered@resend.dev'],
  subject: 'hello world',
  html: '<p>it works!</p>',
  replyTo: 'onboarding@resend.dev',
});
```

```
{
  "id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
}
```

POSThttps://api.resend.com/emails

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.emails.send({
  from: 'Acme <onboarding@resend.dev>',
  to: ['delivered@resend.dev'],
  subject: 'hello world',
  html: '<p>it works!</p>',
  replyTo: 'onboarding@resend.dev',
});
```

```
{
  "id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
}
```

## ​Body Parameters

 [​](#param-from)fromstringrequiredSender email address.To include a friendly name, use the format `"Your Name <sender@domain.com>"`. [​](#param-to)tostring | string[]requiredRecipient email address. For multiple addresses, send as an array of strings.
Max 50. [​](#param-subject)subjectstringrequiredEmail subject. [​](#param-bcc)bccstring | string[]Bcc recipient email address. For multiple addresses, send as an array of
strings. [​](#param-cc)ccstring | string[]Cc recipient email address. For multiple addresses, send as an array of
strings. [​](#scheduled-at)scheduledAtstringSchedule email to be sent later. The date should be in natural language (e.g.: `in 1 min`) or ISO 8601 format (e.g:
`2024-08-05T11:52:01.858Z`).[See examples](https://resend.com/docs/dashboard/emails/schedule-email) [​](#reply-to)replyTostring | string[]Reply-to email address. For multiple addresses, send as an array of strings. [​](#param-html)htmlstringThe HTML version of the message. [​](#param-text)textstringThe plain text version of the message.If not provided, the HTML will be used to generate a plain text version. You
can opt out of this behavior by setting value to an empty string. [​](#param-react)reactReact.ReactNodeThe React component used to write the message. *Only available in the Node.js
SDK.* [​](#param-headers)headersobjectCustom headers to add to the email. [​](#topic-id)topicIdstringThe topic ID to receive the email.

- If the recipient is a contact and has opted-in to the topic, the email is sent.
- If the recipient is a contact and has opted-out of the topic, the email is not sent and will be marked as failed.
- If the recipient is not a contact, the email is sent if the topic default subscription value is set to `opt-in`.

Each email address (to, cc, bcc) is checked and handled separately. [​](#param-attachments)attachmentsarrayFilename and content of attachments (max 40MB per email, after Base64 encoding of the attachments).[See examples](https://resend.com/docs/dashboard/emails/attachments)

Hide properties

[​](#param-content)contentbuffer | stringContent of an attached file, passed as a buffer or Base64 string.[​](#param-filename)filenamestringName of attached file.[​](#param-path)pathstringPath where the attachment file is hosted[​](#content-type)contentTypestringContent type for the attachment, if not set will be derived from the filename property[​](#content-id)contentIdstringYou can embed images using the content id parameter for the attachment. To show the image, you need to include the ID in the `src` attribute of the `img` tag (e.g., `<img src="cid:...">`) of your HTML. [Learn about inline images](https://resend.com/docs/dashboard/emails/embed-inline-images). [​](#param-tags)tagsarrayCustom data passed in key/value pairs.[See examples](https://resend.com/docs/dashboard/emails/tags).

Hide properties

[​](#param-name)namestringrequiredThe name of the email tag.It can only contain ASCII letters (a–z, A–Z), numbers (0–9), underscores (_), or dashes (-).It can contain no more than 256 characters.[​](#param-value)valuestringrequiredThe value of the email tag.It can only contain ASCII letters (a–z, A–Z), numbers (0–9), underscores (_), or dashes (-).It can contain no more than 256 characters. [​](#param-template)templateobjectTo send using a template, provide a `template` object with:

- `id`: the id *or* the alias of the published template
- `variables`: an object with a key for each variable (if applicable)

If a `template` is provided, you cannot send `html`, `text`, or `react` in the payload, otherwise the API will return a validation error.When sending a template, the payload for `from`, `subject`, and `reply_to` take precedence over the template’s defaults for these fields. If the template does not provide a default value for these fields, you must provide them in the payload. [​](#param-id)idstringrequiredThe id of the published email template. Required if `template` is provided. Only published templates can be used when sending emails. [​](#param-variables)variablesobjectTemplate variables object with key/value pairs.

```
variables: {
	CTA: 'Sign up now',
	CTA_LINK: 'https://example.com/signup'
}
```

When sending the template, the HTML will be parsed. If all the variables used in the template were provided, the email will be sent. If not, the call will throw a validation error.See the [errors reference](https://resend.com/docs/api-reference/errors) for more details or [learn more about templates](https://resend.com/docs/dashboard/templates/introduction).

Hide properties

[​](#param-key)keystringrequiredThe key of the variable.May only contain ASCII letters (a–z, A–Z), numbers (0–9), and underscores (_). The following variable names are reserved and cannot be used: `FIRST_NAME`, `LAST_NAME`, `EMAIL`, `UNSUBSCRIBE_URL`.It can contain no more than 50 characters.[​](#param-value-1)valuestring | numberrequiredThe value of the variable.Observe these technical limitations:

- `string`: maximum length of 2,000 characters
- `number`: not greater than 2^53 - 1

## ​Headers

 [​](#param-idempotency-key)Idempotency-KeystringAdd an idempotency key to prevent duplicated emails.

- Should be **unique per API request**
- Idempotency keys expire after **24 hours**
- Have a maximum length of **256 characters**

[Learn more](https://resend.com/docs/dashboard/emails/idempotency-keys)[Errors](https://resend.com/docs/api-reference/errors)[Send Batch Emails](https://resend.com/docs/api-reference/emails/send-batch-emails)Ctrl+I

---

# Update Email

> Update a scheduled email.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const oneMinuteFromNow = new Date(Date.now() + 1000 * 60).toISOString();

const { data, error } = await resend.emails.update({
  id: '49a3999c-0ce1-4ea6-ab68-afcd6dc2e794',
  scheduledAt: oneMinuteFromNow,
});
```

```
{
  "object": "email",
  "id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
}
```

PATCHhttps://api.resend.com/emails/:id

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const oneMinuteFromNow = new Date(Date.now() + 1000 * 60).toISOString();

const { data, error } = await resend.emails.update({
  id: '49a3999c-0ce1-4ea6-ab68-afcd6dc2e794',
  scheduledAt: oneMinuteFromNow,
});
```

```
{
  "object": "email",
  "id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
}
```

## ​Path Parameters

 [​](#param-id)idstringrequiredThe Email ID.

## ​Body Parameters

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const oneMinuteFromNow = new Date(Date.now() + 1000 * 60).toISOString();

const { data, error } = await resend.emails.update({
  id: '49a3999c-0ce1-4ea6-ab68-afcd6dc2e794',
  scheduledAt: oneMinuteFromNow,
});
```

```
{
  "object": "email",
  "id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
}
```

[List Sent Emails](https://resend.com/docs/api-reference/emails/list-emails)[Cancel Email](https://resend.com/docs/api-reference/emails/cancel-email)⌘ I$/$

---

# Errors

> Troubleshoot problems with this comprehensive breakdown of all error codes.

## ​Error schema

 We use standard HTTP response codes for success and failure notifications, and our errors are further classified by type.

### ​invalid_idempotency_key

- **Status:** 400
- **Message:** The key must be between 1-256 chars.
- **Suggested action:** Retry with a valid idempotency key.

### ​validation_error

- **Status:** 400
- **Message:** We found an error with one or more fields in the request.
- **Suggested action:** The message will contain more details about what field and error were found.

### ​missing_api_key

- **Status:** 401
- **Message:** Missing API key in the authorization header.
- **Suggested action:** Include the following header in the request: `Authorization: Bearer YOUR_API_KEY`.

### ​restricted_api_key

- **Status:** 401
- **Message:** This API key is restricted to only send emails.
- **Suggested action:** Make sure the API key has `Full access` to perform actions other than sending emails.

### ​invalid_api_key

- **Status:** 403
- **Message:** API key is invalid.
- **Suggested action:** Make sure the API key is correct or generate a new [API key in the dashboard](https://resend.com/api-keys).

### ​validation_error

- **Status:** 403
- **Message:** You can only send testing emails to your own email address (`[email protected]`). To send emails to other recipients, please verify a domain at resend.com/domains, and change the `from` address to an email using this domain.
- **Suggested action:** In [Resend’s Domain page](https://resend.com/domains), add and verify a domain for which you have DNS access. This allows you to send emails to addresses beyond your own. [Learn more about resolving this error](https://resend.com/docs/knowledge-base/403-error-resend-dev-domain).

### ​validation_error

- **Status:** 403
- **Message:** The `domain.com` domain is not verified. Please, add and verify your domain.
- **Suggested action:** Make sure the domain in your API request’s `from` field matches a domain you’ve verified in Resend. Update your API request to use your verified domain, or add and verify the domain you’re trying to use. [Learn more about resolving this error](https://resend.com/docs/knowledge-base/403-error-domain-mismatch).

### ​not_found

- **Status:** 404
- **Message:** The requested endpoint does not exist.
- **Suggested action:** Change your request URL to match a valid API endpoint.

### ​method_not_allowed

- **Status:** 405
- **Message:** Method is not allowed for the requested path.
- **Suggested action:** Change your API endpoint to use a valid method.

### ​invalid_idempotent_request

- **Status:** 409
- **Message:** Same idempotency key used with a different request payload.
- **Suggested action:** Change your idempotency key or payload.

### ​concurrent_idempotent_requests

- **Status:** 409
- **Message:** Same idempotency key used while original request is still in progress.
- **Suggested action:** Try the request again later.

### ​invalid_attachment

- **Status:** 422
- **Message:** Attachment must have either a `content` or `path`.
- **Suggested action:** Attachments must either have a `content` (strings, Buffer, or Stream contents) or `path` to a remote resource (better for larger attachments).

### ​invalid_from_address

- **Status:** 422
- **Message:** Invalid `from` field.
- **Suggested action:** Make sure the `from` field is valid. The email address needs to follow the `[email protected]` or `Name <[email protected]>` format.

### ​invalid_access

- **Status:** 422
- **Message:** Access must be “full_access” | “sending_access”.
- **Suggested action:** Make sure the API key has necessary permissions.

### ​invalid_parameter

- **Status:** 422
- **Message:** The `parameter` must be a valid UUID.
- **Suggested action:** Check the value and make sure it’s valid.

### ​invalid_region

- **Status:** 422
- **Message:** Region must be “us-east-1” | “eu-west-1” | “sa-east-1”.
- **Suggested action:** Make sure the correct region is selected.

### ​missing_required_field

- **Status:** 422
- **Message:** The request body is missing one or more required fields.
- **Suggested action:** Check the error message to see the list of missing fields.

### ​monthly_quota_exceeded

- **Status:** 429
- **Message:** You have reached your monthly email quota.
- **Suggested action:** [Upgrade your plan](https://resend.com/settings/billing) to increase the monthly email quota. Both sent and received emails count towards this quota.

### ​daily_quota_exceeded

- **Status:** 429
- **Message:** You have reached your daily email quota.
- **Suggested action:** [Upgrade your plan](https://resend.com/settings/billing) to remove the daily quota limit or wait until 24 hours have passed. Both sent and received emails count towards this quota.

### ​rate_limit_exceeded

- **Status:** 429
- **Message:** Too many requests. Please limit the number of requests per second. Or [contact support](https://resend.com/contact) to increase rate limit.
- **Suggested action:** You should read the [response headers](https://resend.com/docs/api-reference/introduction#rate-limit) and reduce the rate at which you request the API. This can be done by introducing a queue mechanism or reducing the number of concurrent requests per second. If you have specific requirements, [contact support](https://resend.com/contact) to request a rate increase.

### ​security_error

- **Status:** 451
- **Message:** We may have found a security issue with the request.
- **Suggested action:** The message will contain more details. [Contact support](https://resend.com/contact) for more information.

### ​application_error

- **Status:** 500
- **Message:** An unexpected error occurred.
- **Suggested action:** Try the request again later. If the error does not resolve, check our [status page](https://resend-status.com) for service updates.

### ​internal_server_error

- **Status:** 500
- **Message:** An unexpected error occurred.
- **Suggested action:** Try the request again later. If the error does not resolve, check our [status page](https://resend-status.com) for service updates.

---

# Introduction

> Understand general concepts, response codes, and authentication strategies.

## ​Base URL

 The Resend API is built on **REST** principles. We enforce **HTTPS** in every request to improve data security, integrity, and privacy. The API does not support **HTTP**. All requests contain the following base URL:

```
https://api.resend.com
```

## ​Authentication

 To authenticate you need to add an *Authorization* header with the contents of the header being `Bearer re_xxxxxxxxx` where `re_xxxxxxxxx` is your [API Key](https://resend.com/api-keys).

```
Authorization: Bearer re_xxxxxxxxx
```

## ​Response codes

 Resend uses standard HTTP codes to indicate the success or failure of your requests. In general, `2xx` HTTP codes correspond to success, `4xx` codes are for user-related failures, and `5xx` codes are for infrastructure issues.

| Status | Description |
| --- | --- |
| 200 | Successful request. |
| 400 | Check that the parameters were correct. |
| 401 | The API key used was missing. |
| 403 | The API key used was invalid. |
| 404 | The resource was not found. |
| 429 | The rate limit was exceeded. |
| 5xx | Indicates an error with Resend servers. |

 Check [Error Codes](https://resend.com/docs/api-reference/errors) for a comprehensive breakdown of
all possible API errors.

## ​Rate limit

 The default maximum rate limit is **2 requests per second**. This number can be increased for trusted senders by request. After that, you’ll hit the rate limit and receive a `429` response error code. Learn more about our [rate limits](https://resend.com/docs/api-reference/rate-limit).

## ​FAQ

How does pagination work with the API?

Some endpoints support cursor-based pagination to help you browse through
large datasets efficiently. Check our [pagination
guide](https://resend.com/docs/api-reference/pagination) for detailed information on how to use
pagination parameters.

How do you handle API versioning?

Currently, there’s no versioning system in place. We plan to add versioning
via calendar-based headers in the future.

---

# Pagination

> Learn how pagination works in the Resend API.

## ​Overview

 Several Resend API endpoints support **cursor-based pagination** to help you efficiently browse through large datasets. You can safely navigate lists with guaranteed stability, even if new objects are created or deleted while you’re still requesting pages. Paginated endpoints responses include:

- `object`: always set to `list`.
- `has_more`: indicates whether there are more elements available.
- `data`: the list of returned items.

 You can navigate through the results using the following parameters:

- `limit`: the number of items to return per page.
- `after`: the cursor to use to get the next page of results.
- `before`: the cursor to use to get the previous page of results.

 Use the `id` of objects as the cursor for pagination. The cursor itself is *excluded* from the results. For an example, see [pagination strategies below](#strategies).

## ​Currently-supported endpoints

 Existing list endpoints can optionally return paginated results:

- [List Domains](https://resend.com/docs/api-reference/domains/list-domains)
- [List API Keys](https://resend.com/docs/api-reference/api-keys/list-api-keys)
- [List Broadcasts](https://resend.com/docs/api-reference/broadcasts/list-broadcasts)
- [List Segments](https://resend.com/docs/api-reference/segments/list-segments)
- [List Contacts](https://resend.com/docs/api-reference/contacts/list-contacts)
- [List Receiving Emails](https://resend.com/docs/api-reference/emails/list-received-emails)
- [List Receiving Email Attachments](https://resend.com/docs/api-reference/emails/list-received-email-attachments)

 Note that for these endpoints, the `limit` parameter is optional. If you do
not provide a `limit`, all items will be returned in a single response. Newer list endpoints always return paginated results:

- [List Emails](https://resend.com/docs/api-reference/emails/list-emails)
- [List Templates](https://resend.com/docs/api-reference/templates/list-templates)
- [List Topics](https://resend.com/docs/api-reference/topics/list-topics)

## ​Parameters

 All paginated endpoints support the following query parameters: [​](#param-limit)limitnumberThe number of items to return per page. Default is `20`, maximum is `100`, and
minimum is `1`. [​](#param-after)afterstringThe cursor after which to start retrieving items. To get the next page, use
the ID of the last item from the current page. This will return the page that
**starts after** the object with this ID (excluding the passed ID itself). [​](#param-before)beforestringThe cursor before which to start retrieving items. To get the previous page,
use the ID of the first item from the current page. This will return the page
that **ends before** the object with this ID (excluding the passed ID itself). You can only use either `after` or `before`, not both simultaneously.

## ​Response Format

 Paginated endpoints return responses in the following format: Response Format

```
{
  "object": "list",
  "has_more": true,
  "data": [
    /* Array of resources */
  ]
}
```

 [​](#param-object)objectstringAlways set to `list` for paginated responses. [​](#param-has-more)has_morebooleanIndicates whether there are more items available beyond the current page. [​](#param-data)dataarrayAn array containing the actual resources for the current page.

## ​Strategies

### ​Forward Pagination

 To paginate forward through results (newer to older items), use the `after` parameter with the ID of the **last item** from the current page:

```
const resend = new Resend('re_xxxxxxxxx');

// First page
const { data: firstPage } = await resend.contacts.list({ limit: 50 });

// Second page (if has_more is true)
if (firstPage.has_more) {
  const lastId = firstPage.data[firstPage.data.length - 1].id;
  const { data: secondPage } = await resend.contacts.list({
    limit: 50,
    after: lastId,
  });
}
```

### ​Backward Pagination

 To paginate backward through results (older to newer items), use the `before` parameter with the ID of the **first item** from the current page (or the most recent ID you have in your system):

```
const resend = new Resend('re_xxxxxxxxx');

// Start from a specific point and go backward
const page = await resend.contacts.list({
  limit: 50,
  before: 'some-contact-id',
});

if (page.data.has_more) {
  const firstId = page.data.data[0].id;
  const previousPage = await resend.contacts.list({
    limit: 50,
    before: firstId,
  });
}
```

## ​Best Practices

Use appropriate page sizes

Choose a `limit` that balances performance and usability. Smaller pages are good for real-time applications, while larger pages
(hundreds of items) work better for bulk processing.

Handle pagination gracefully

Always check the `has_more` field before attempting to fetch additional pages.
This prevents unnecessary API calls when you’ve reached the end of the
dataset.

Consider rate limits

Be mindful of API rate limits when paginating through large datasets.
Implement appropriate delays or batching strategies if processing many
pages.

## ​Error Handling

 Pagination requests may return the following validation errors:

| Error | Description |
| --- | --- |
| validation_error | Invalid cursor format or limit out of range (1-100) |
| validation_error | Bothbeforeandafterparameters provided |

 Example error response: Error Response

```
{
  "name": "validation_error",
  "statusCode": 422,
  "message": "The pagination limit must be a number between 1 and 100. See https://resend.com/docs/pagination for more information."
}
```
