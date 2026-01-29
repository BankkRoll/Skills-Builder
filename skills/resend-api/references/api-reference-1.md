# Create API key and more

# Create API key

> Add a new API key to authenticate communications with Resend.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.apiKeys.create({ name: 'Production' });
```

```
{
  "id": "dacf4072-4119-4d88-932f-6202748ac7c8",
  "token": "re_c1tpEyD8_NKFusih9vKVQknRAQfmFcWCv"
}
```

POSThttps://api.resend.com/api-keys

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.apiKeys.create({ name: 'Production' });
```

```
{
  "id": "dacf4072-4119-4d88-932f-6202748ac7c8",
  "token": "re_c1tpEyD8_NKFusih9vKVQknRAQfmFcWCv"
}
```

## ​Body Parameters

 [​](#param-name)namestringrequiredThe API key name. Maximum 50 characters. [​](#param-permission)permissionfull_access | sending_accessThe API key can have full access to Resend’s API or be only restricted to send
emails. * `full_access`: Can create, delete, get, and update any resource. *
`sending_access`: Can only send emails.

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.apiKeys.create({ name: 'Production' });
```

```
{
  "id": "dacf4072-4119-4d88-932f-6202748ac7c8",
  "token": "re_c1tpEyD8_NKFusih9vKVQknRAQfmFcWCv"
}
```

[Delete Domain](https://resend.com/docs/api-reference/domains/delete-domain)[List API keys](https://resend.com/docs/api-reference/api-keys/list-api-keys)⌘ I$/$

---

# Delete API key

> Remove an existing API key.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.apiKeys.remove(
  'b6d24b8e-af0b-4c3c-be0c-359bbd97381e',
);
```

```
HTTP 200 OK
```

DELETEhttps://api.resend.com/api-keys/:api_key_id

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.apiKeys.remove(
  'b6d24b8e-af0b-4c3c-be0c-359bbd97381e',
);
```

```
HTTP 200 OK
```

## ​Path Parameters

 [​](#api-key-id)apiKeyIdstringrequiredThe API key ID.[List API keys](https://resend.com/docs/api-reference/api-keys/list-api-keys)[Create Broadcast](https://resend.com/docs/api-reference/broadcasts/create-broadcast)Ctrl +I$/$

---

# List API keys

> Retrieve a list of API keys for the authenticated user.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.apiKeys.list();
```

```
{
  "object": "list",
  "has_more": false,
  "data": [
    {
      "id": "91f3200a-df72-4654-b0cd-f202395f5354",
      "name": "Production",
      "created_at": "2023-04-08T00:11:13.110779+00:00"
    }
  ]
}
```

GEThttps://api.resend.com/api-keys

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.apiKeys.list();
```

```
{
  "object": "list",
  "has_more": false,
  "data": [
    {
      "id": "91f3200a-df72-4654-b0cd-f202395f5354",
      "name": "Production",
      "created_at": "2023-04-08T00:11:13.110779+00:00"
    }
  ]
}
```

## Query Parameters

Note that the `limit` parameter is *optional*. If you do not provide a `limit`, all API keys will be returned in a single response.[​](#limit)limitnumberNumber of API keys to retrieve.

- Maximum value: `100`
- Minimum value: `1`

[​](#after)afterstringThe ID *after* which we'll retrieve more API keys (for pagination). This ID will *not* be included in the returned list. Cannot be used with the`before` parameter.[​](#before)beforestringThe ID *before* which we'll retrieve more API keys (for pagination). This ID will *not* be included in the returned list. Cannot be used with the `after` parameter.You can only use either `after` or `before` parameter, not both. See our [pagination guide](https://resend.com/docs/api-reference/pagination) for more information.[Create API key](https://resend.com/docs/api-reference/api-keys/create-api-key)[Delete API key](https://resend.com/docs/api-reference/api-keys/delete-api-key)Ctrl +I$/$

---

# Create Broadcast

> Create a new broadcast to send to your contacts.

[Resend home page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

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

```
{
  "id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
}
```

POSThttps://api.resend.com/broadcasts

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

```
{
  "id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
}
```

## ​Body Parameters

 [​](#segment-id)segmentIdstringrequiredThe ID of the segment you want to send to.Audiences are now called Segments. Follow the [Migration
Guide](https://resend.com/docs/dashboard/segments/migrating-from-audiences-to-segments). [​](#param-from)fromstringrequiredSender email address.To include a friendly name, use the format `"Your Name <sender@domain.com>"`. [​](#param-subject)subjectstringrequiredEmail subject. [​](#reply-to)replyTostring | string[]Reply-to email address. For multiple addresses, send as an array of strings. [​](#param-html)htmlstringThe HTML version of the message. You can include Contact Properties in the
body of the Broadcast. Learn more about [Contact
Properties](https://resend.com/docs/dashboard/audiences/contacts). [​](#param-text)textstringThe plain text version of the message. You can include Contact Properties in the body of the Broadcast. Learn more about [Contact Properties](https://resend.com/docs/dashboard/audiences/contacts).If not provided, the HTML will be used to generate a plain text version. You
can opt out of this behavior by setting value to an empty string. [​](#param-react)reactReact.ReactNodeThe React component used to write the message. *Only available in the Node.js
SDK.* [​](#param-name)namestringThe friendly name of the broadcast. Only used for internal reference. [​](#topic-id)topicIdstringThe topic ID that the broadcast will be scoped to.[Delete API key](https://resend.com/docs/api-reference/api-keys/delete-api-key)[Send Broadcast](https://resend.com/docs/api-reference/broadcasts/send-broadcast)Ctrl+I

---

# Delete Broadcast

> Remove an existing broadcast.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.broadcasts.remove(
  '559ac32e-9ef5-46fb-82a1-b76b840c0f7b',
);
```

```
{
  "object": "broadcast",
  "id": "559ac32e-9ef5-46fb-82a1-b76b840c0f7b",
  "deleted": true
}
```

DELETEhttps://api.resend.com/broadcasts/:broadcast_id

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.broadcasts.remove(
  '559ac32e-9ef5-46fb-82a1-b76b840c0f7b',
);
```

```
{
  "object": "broadcast",
  "id": "559ac32e-9ef5-46fb-82a1-b76b840c0f7b",
  "deleted": true
}
```

 You can only delete broadcasts that are in the `draft` status. In addition, if you delete a broadcast that has already been scheduled to be sent, we will automatically cancel the scheduled delivery and it won’t be sent.

## ​Path Parameters

 [​](#broadcast-id)broadcastIdstringrequiredThe broadcast ID.[Update Broadcast](https://resend.com/docs/api-reference/broadcasts/update-broadcast)[Create Contact](https://resend.com/docs/api-reference/contacts/create-contact)Ctrl +I$/$

---

# Retrieve Broadcast

> Retrieve a single broadcast.

[Resend home page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.broadcasts.get(
  '559ac32e-9ef5-46fb-82a1-b76b840c0f7b',
);
```

```
{
  "object": "broadcast",
  "id": "559ac32e-9ef5-46fb-82a1-b76b840c0f7b",
  "name": "Announcements",
  "audience_id": "78261eea-8f8b-4381-83c6-79fa7120f1cf", // now called segment_id
  "segment_id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
  "from": "Acme <onboarding@resend.dev>",
  "subject": "hello world",
  "reply_to": null,
  "preview_text": "Check out our latest announcements",
  "html": "<p>Hello {{{FIRST_NAME|there}}}!</p>",
  "text": "Hello {{{FIRST_NAME|there}}}!",
  "status": "draft",
  "created_at": "2024-12-01T19:32:22.980Z",
  "scheduled_at": null,
  "sent_at": null,
  "topic_id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"
}
```

GEThttps://api.resend.com/broadcasts/:broadcast_id

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.broadcasts.get(
  '559ac32e-9ef5-46fb-82a1-b76b840c0f7b',
);
```

```
{
  "object": "broadcast",
  "id": "559ac32e-9ef5-46fb-82a1-b76b840c0f7b",
  "name": "Announcements",
  "audience_id": "78261eea-8f8b-4381-83c6-79fa7120f1cf", // now called segment_id
  "segment_id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
  "from": "Acme <onboarding@resend.dev>",
  "subject": "hello world",
  "reply_to": null,
  "preview_text": "Check out our latest announcements",
  "html": "<p>Hello {{{FIRST_NAME|there}}}!</p>",
  "text": "Hello {{{FIRST_NAME|there}}}!",
  "status": "draft",
  "created_at": "2024-12-01T19:32:22.980Z",
  "scheduled_at": null,
  "sent_at": null,
  "topic_id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"
}
```

You can retrieve broadcasts created via both this API and the Resend dashboard.

## ​Path Parameters

 [​](#broadcast-id)broadcastIdstringrequiredThe broadcast ID. See all available `status` types in [the Broadcasts
overview](https://resend.com/docs/dashboard/broadcasts/introduction#understand-broadcast-statuses).[Send Broadcast](https://resend.com/docs/api-reference/broadcasts/send-broadcast)[List Broadcasts](https://resend.com/docs/api-reference/broadcasts/list-broadcasts)Ctrl+I

---

# List Broadcasts

> Retrieve a list of broadcast.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.broadcasts.list();
```

```
{
  "object": "list",
  "has_more": false,
  "data": [
    {
      "id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794",
      "audience_id": "78261eea-8f8b-4381-83c6-79fa7120f1cf", // now called segment_id
      "segment_id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
      "status": "draft",
      "created_at": "2024-11-01T15:13:31.723Z",
      "scheduled_at": null,
      "sent_at": null,
      "topic_id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"
    },
    {
      "id": "559ac32e-9ef5-46fb-82a1-b76b840c0f7b",
      "audience_id": "78261eea-8f8b-4381-83c6-79fa7120f1cf", // now called segment_id
      "segment_id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
      "status": "sent",
      "created_at": "2024-12-01T19:32:22.980Z",
      "scheduled_at": "2024-12-02T19:32:22.980Z",
      "sent_at": "2024-12-02T19:32:22.980Z",
      "topic_id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"
    }
  ]
}
```

GEThttps://api.resend.com/broadcasts

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.broadcasts.list();
```

```
{
  "object": "list",
  "has_more": false,
  "data": [
    {
      "id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794",
      "audience_id": "78261eea-8f8b-4381-83c6-79fa7120f1cf", // now called segment_id
      "segment_id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
      "status": "draft",
      "created_at": "2024-11-01T15:13:31.723Z",
      "scheduled_at": null,
      "sent_at": null,
      "topic_id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"
    },
    {
      "id": "559ac32e-9ef5-46fb-82a1-b76b840c0f7b",
      "audience_id": "78261eea-8f8b-4381-83c6-79fa7120f1cf", // now called segment_id
      "segment_id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
      "status": "sent",
      "created_at": "2024-12-01T19:32:22.980Z",
      "scheduled_at": "2024-12-02T19:32:22.980Z",
      "sent_at": "2024-12-02T19:32:22.980Z",
      "topic_id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"
    }
  ]
}
```

See all available `status` types in [the Broadcasts
overview](https://resend.com/docs/dashboard/broadcasts/introduction#understand-broadcast-statuses).

## Query Parameters

Note that the `limit` parameter is *optional*. If you do not provide a `limit`, all broadcasts will be returned in a single response.[​](#limit)limitnumberNumber of broadcasts to retrieve.

- Maximum value: `100`
- Minimum value: `1`

[​](#after)afterstringThe ID *after* which we'll retrieve more broadcasts (for pagination). This ID will *not* be included in the returned list. Cannot be used with the`before` parameter.[​](#before)beforestringThe ID *before* which we'll retrieve more broadcasts (for pagination). This ID will *not* be included in the returned list. Cannot be used with the `after` parameter.You can only use either `after` or `before` parameter, not both. See our [pagination guide](https://resend.com/docs/api-reference/pagination) for more information.[Retrieve Broadcast](https://resend.com/docs/api-reference/broadcasts/get-broadcast)[Update Broadcast](https://resend.com/docs/api-reference/broadcasts/update-broadcast)Ctrl +I$/$

---

# Send Broadcast

> Start sending broadcasts to your audience through the Resend API.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.broadcasts.send(
  '559ac32e-9ef5-46fb-82a1-b76b840c0f7b',
  {
    scheduledAt: 'in 1 min',
  },
);
```

```
{
  "id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
}
```

POSThttps://api.resend.com/broadcasts/:broadcast_id/send

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.broadcasts.send(
  '559ac32e-9ef5-46fb-82a1-b76b840c0f7b',
  {
    scheduledAt: 'in 1 min',
  },
);
```

```
{
  "id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
}
```

  You can send broadcasts only if they were created via the API.

## ​Path Parameters

 [​](#broadcast-id)broadcastIdstringrequiredThe broadcast ID.

## ​Body Parameters

 [​](#scheduled-at)scheduledAtstringSchedule email to be sent later. The date should be in natural language (e.g.:
`in 1 min`) or ISO 8601 format (e.g: `2024-08-05T11:52:01.858Z`).[Create Broadcast](https://resend.com/docs/api-reference/broadcasts/create-broadcast)[Retrieve Broadcast](https://resend.com/docs/api-reference/broadcasts/get-broadcast)Ctrl +I$/$

---

# Update Broadcast

> Update a broadcast to send to your contacts.

[Resend home page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.broadcasts.update(
  '49a3999c-0ce1-4ea6-ab68-afcd6dc2e794',
  {
    html: 'Hi {{{FIRST_NAME|there}}}, you can unsubscribe here: {{{RESEND_UNSUBSCRIBE_URL}}}',
  },
);
```

```
{
  "id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
}
```

PATCHhttps://api.resend.com/broadcasts/:id

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.broadcasts.update(
  '49a3999c-0ce1-4ea6-ab68-afcd6dc2e794',
  {
    html: 'Hi {{{FIRST_NAME|there}}}, you can unsubscribe here: {{{RESEND_UNSUBSCRIBE_URL}}}',
  },
);
```

```
{
  "id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794"
}
```

## ​Path Parameters

 [​](#broadcast-id)broadcastIdstringrequiredThe ID of the broadcast you want to update.

## ​Body Parameters

 [​](#segment-id)segmentIdstringThe ID of the segment you want to send to.Audiences are now called Segments. Follow the [Migration
Guide](https://resend.com/docs/dashboard/segments/migrating-from-audiences-to-segments). [​](#param-from)fromstringSender email address.To include a friendly name, use the format `"Your Name <sender@domain.com>"`. [​](#param-subject)subjectstringEmail subject. [​](#reply-to)replyTostring | string[]Reply-to email address. For multiple addresses, send as an array of strings. [​](#param-html)htmlstringThe HTML version of the message. [​](#param-text)textstringThe plain text version of the message.If not provided, the HTML will be used to generate a plain text version. You
can opt out of this behavior by setting value to an empty string. [​](#param-react)reactReact.ReactNodeThe React component used to write the message. *Only available in the Node.js
SDK.* [​](#param-name)namestringThe friendly name of the broadcast. Only used for internal reference. [​](#topic-id)topicIdstringThe topic ID that the broadcast will be scoped to.[List Broadcasts](https://resend.com/docs/api-reference/broadcasts/list-broadcasts)[Delete Broadcast](https://resend.com/docs/api-reference/broadcasts/delete-broadcast)Ctrl+I

---

# Create Contact Property

> Create a custom property for your contacts.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.contactProperties.create({
  key: 'company_name',
  type: 'string',
  fallbackValue: 'Acme Corp',
});
```

```
{
  "object": "contact_property",
  "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"
}
```

POSThttps://api.resend.com/contact-properties

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.contactProperties.create({
  key: 'company_name',
  type: 'string',
  fallbackValue: 'Acme Corp',
});
```

```
{
  "object": "contact_property",
  "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"
}
```

## ​Body Parameters

 [​](#key)keystringrequiredThe property key. Max length is `50` characters. Only alphanumeric characters
and underscores are allowed. [​](#type)typestringrequiredThe property type. Possible values: `string` or `number`. [​](#fallback-value)fallbackValuestring | numberThe default value to use when the property is not set for a contact. Must
match the type specified in the `type` field.[Update Contact Topics](https://resend.com/docs/api-reference/contacts/update-contact-topics)[Retrieve Contact Property](https://resend.com/docs/api-reference/contact-properties/get-contact-property)Ctrl +I$/$

---

# Delete Contact Property

> Remove an existing contact property.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.contactProperties.remove(
  'b6d24b8e-af0b-4c3c-be0c-359bbd97381e',
);
```

```
{
  "object": "contact_property",
  "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
  "deleted": true
}
```

DELETEhttps://api.resend.com/contact-properties/:contact_property_id

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.contactProperties.remove(
  'b6d24b8e-af0b-4c3c-be0c-359bbd97381e',
);
```

```
{
  "object": "contact_property",
  "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
  "deleted": true
}
```

## ​Path Parameters

 [​](#contact-property-id)contactPropertyIdstringrequiredThe Contact Property ID.[Update Contact Property](https://resend.com/docs/api-reference/contact-properties/update-contact-property)[Create Segment](https://resend.com/docs/api-reference/segments/create-segment)Ctrl +I$/$

---

# Retrieve Contact Property

> Retrieve a contact property by its ID.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.contactProperties.get(
  'b6d24b8e-af0b-4c3c-be0c-359bbd97381e',
);
```

```
{
  "object": "contact_property",
  "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
  "key": "company_name",
  "type": "string",
  "fallback_value": "Acme Corp",
  "created_at": "2023-04-08T00:11:13.110779+00:00"
}
```

GEThttps://api.resend.com/contact-properties/:contact_property_id

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.contactProperties.get(
  'b6d24b8e-af0b-4c3c-be0c-359bbd97381e',
);
```

```
{
  "object": "contact_property",
  "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
  "key": "company_name",
  "type": "string",
  "fallback_value": "Acme Corp",
  "created_at": "2023-04-08T00:11:13.110779+00:00"
}
```

## ​Path Parameters

 [​](#contact-property-id)contactPropertyIdstringrequiredThe Contact Property ID.[Create Contact Property](https://resend.com/docs/api-reference/contact-properties/create-contact-property)[List Contact Properties](https://resend.com/docs/api-reference/contact-properties/list-contact-properties)Ctrl +I$/$

---

# List Contact Properties

> Retrieve a list of contact properties.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.contactProperties.list();
```

```
{
  "object": "list",
  "has_more": false,
  "data": [
    {
      "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
      "key": "company_name",
      "type": "string",
      "fallback_value": "Acme Corp",
      "created_at": "2023-04-08T00:11:13.110779+00:00"
    }
  ]
}
```

GEThttps://api.resend.com/contact-properties

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.contactProperties.list();
```

```
{
  "object": "list",
  "has_more": false,
  "data": [
    {
      "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
      "key": "company_name",
      "type": "string",
      "fallback_value": "Acme Corp",
      "created_at": "2023-04-08T00:11:13.110779+00:00"
    }
  ]
}
```

## Query Parameters

[​](#limit)limitnumberNumber of  contact-properties  to retrieve.

- Default value: `20`
- Maximum value: `100`
- Minimum value: `1`

[​](#after)afterstringThe ID *after* which we'll retrieve more  contact-properties  (for pagination). This ID will *not* be included in the returned list. Cannot be used with the`before` parameter.[​](#before)beforestringThe ID *before* which we'll retrieve more  contact-properties  (for pagination). This ID will *not* be included in the returned list. Cannot be used with the `after` parameter.You can only use either `after` or `before`  parameter, not both. See our  [pagination guide](https://resend.com/docs/api-reference/pagination) for more information.

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.contactProperties.list();
```

```
{
  "object": "list",
  "has_more": false,
  "data": [
    {
      "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
      "key": "company_name",
      "type": "string",
      "fallback_value": "Acme Corp",
      "created_at": "2023-04-08T00:11:13.110779+00:00"
    }
  ]
}
```

[Retrieve Contact Property](https://resend.com/docs/api-reference/contact-properties/get-contact-property)[Update Contact Property](https://resend.com/docs/api-reference/contact-properties/update-contact-property)⌘ I$/$

---

# Update Contact Property

> Update an existing contact property.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.contactProperties.update({
  id: 'b6d24b8e-af0b-4c3c-be0c-359bbd97381e',
  fallbackValue: 'Example Company',
});
```

```
{
  "object": "contact_property",
  "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"
}
```

PATCHhttps://api.resend.com/contact-properties/:contact_property_id

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.contactProperties.update({
  id: 'b6d24b8e-af0b-4c3c-be0c-359bbd97381e',
  fallbackValue: 'Example Company',
});
```

```
{
  "object": "contact_property",
  "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"
}
```

## ​Path Parameters

 [​](#contact-property-id)contactPropertyIdstringrequiredThe Contact Property ID. The `key` and `type` fields cannot be changed after creation. This preserves
data integrity for existing contact values.

## ​Body Parameters

 [​](#fallback-value)fallbackValuestring | numberThe default value to use when the property is not set for a contact. Must
match the type of the property.[List Contact Properties](https://resend.com/docs/api-reference/contact-properties/list-contact-properties)[Delete Contact Property](https://resend.com/docs/api-reference/contact-properties/delete-contact-property)Ctrl +I$/$

---

# Add Contact to Segment

> Add an existing contact to a segment.

[Resend home page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

// Add by contact id
const { data, error } = await resend.contacts.segments.add({
  contactId: 'e169aa45-1ecf-4183-9955-b1499d5701d3',
  segmentId: '78261eea-8f8b-4381-83c6-79fa7120f1cf',
});

// Add by contact email
const { data, error } = await resend.contacts.segments.add({
  email: 'steve.wozniak@gmail.com',
  segmentId: '78261eea-8f8b-4381-83c6-79fa7120f1cf',
});
```

```
{
  "id": "78261eea-8f8b-4381-83c6-79fa7120f1cf"
}
```

POSThttps://api.resend.com/contacts/:contact_id/segments/:segment_id

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

// Add by contact id
const { data, error } = await resend.contacts.segments.add({
  contactId: 'e169aa45-1ecf-4183-9955-b1499d5701d3',
  segmentId: '78261eea-8f8b-4381-83c6-79fa7120f1cf',
});

// Add by contact email
const { data, error } = await resend.contacts.segments.add({
  email: 'steve.wozniak@gmail.com',
  segmentId: '78261eea-8f8b-4381-83c6-79fa7120f1cf',
});
```

```
{
  "id": "78261eea-8f8b-4381-83c6-79fa7120f1cf"
}
```

## ​Path Parameters

 Either `id` or `email` must be provided. [​](#param-id)idstringThe Contact ID. [​](#param-email)emailstringThe Contact Email. [​](#segment-id)segmentIdstringrequiredThe Segment ID.[Delete Contact](https://resend.com/docs/api-reference/contacts/delete-contact)[List Contact Segments](https://resend.com/docs/api-reference/contacts/list-contact-segments)Ctrl+I

---

# Create Contact

> Create a contact.

[Resend home page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.contacts.create({
  email: 'steve.wozniak@gmail.com',
  firstName: 'Steve',
  lastName: 'Wozniak',
  unsubscribed: false,
});
```

```
{
  "object": "contact",
  "id": "479e3145-dd38-476b-932c-529ceb705947"
}
```

POSThttps://api.resend.com/contacts

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.contacts.create({
  email: 'steve.wozniak@gmail.com',
  firstName: 'Steve',
  lastName: 'Wozniak',
  unsubscribed: false,
});
```

```
{
  "object": "contact",
  "id": "479e3145-dd38-476b-932c-529ceb705947"
}
```

## ​Body Parameters

 [​](#param-email)emailstringrequiredThe email address of the contact. [​](#first-name)firstNamestringThe first name of the contact. [​](#last-name)lastNamestringThe last name of the contact. [​](#param-unsubscribed)unsubscribedbooleanThe Contact’s global subscription status. If set to `true`, the contact will
be unsubscribed from all Broadcasts. [​](#param-properties)propertiesobjectA map of custom property keys and values to create.

Hide custom properties

[​](#param-key)keystringrequiredThe property key.[​](#param-value)valuestringrequiredThe property value. [​](#param-segments)segmentsarrayArray of segment IDs to add the contact to.

Hide segments

[​](#param-id)idstringrequiredThe segment ID. [​](#param-topics)topicsarrayArray of topic subscriptions for the contact.

Hide topics

[​](#param-id-1)idstringrequiredThe topic ID.[​](#param-subscription)subscription'opt_in' | 'opt_out'requiredThe subscription status for this topic.[Delete Broadcast](https://resend.com/docs/api-reference/broadcasts/delete-broadcast)[Retrieve Contact](https://resend.com/docs/api-reference/contacts/get-contact)Ctrl+I

---

# Delete Contact Segment

> Remove an existing contact from a segment.

[Resend home page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

// Remove by contact id
const { data, error } = await resend.contacts.segments.remove({
  id: 'e169aa45-1ecf-4183-9955-b1499d5701d3',
  segmentId: '78261eea-8f8b-4381-83c6-79fa7120f1cf',
});

// Remove by contact email
const { data, error } = await resend.contacts.segments.remove({
  email: 'steve.wozniak@gmail.com',
  segmentId: '78261eea-8f8b-4381-83c6-79fa7120f1cf',
});
```

```
{
  "id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
  "deleted": true
}
```

DELETEhttps://api.resend.com/contacts/:contact_id/segments/:segment_id

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

// Remove by contact id
const { data, error } = await resend.contacts.segments.remove({
  id: 'e169aa45-1ecf-4183-9955-b1499d5701d3',
  segmentId: '78261eea-8f8b-4381-83c6-79fa7120f1cf',
});

// Remove by contact email
const { data, error } = await resend.contacts.segments.remove({
  email: 'steve.wozniak@gmail.com',
  segmentId: '78261eea-8f8b-4381-83c6-79fa7120f1cf',
});
```

```
{
  "id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
  "deleted": true
}
```

## ​Path Parameters

 Either `id` or `email` must be provided. [​](#param-id)idstringThe Contact ID. [​](#param-email)emailstringThe Contact Email. [​](#segment-id)segmentIdstringrequiredThe Segment ID.[List Contact Segments](https://resend.com/docs/api-reference/contacts/list-contact-segments)[Retrieve Contact Topics](https://resend.com/docs/api-reference/contacts/get-contact-topics)Ctrl+I

---

# Delete Contact

> Remove an existing contact.

[Resend home page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

// Delete by contact id
const { data, error } = await resend.contacts.remove({
  id: '520784e2-887d-4c25-b53c-4ad46ad38100',
});

// Delete by contact email
const { data, error } = await resend.contacts.remove({
  email: 'acme@example.com',
});
```

```
{
  "object": "contact",
  "contact": "520784e2-887d-4c25-b53c-4ad46ad38100",
  "deleted": true
}
```

DELETEhttps://api.resend.com/contacts/:id

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

// Delete by contact id
const { data, error } = await resend.contacts.remove({
  id: '520784e2-887d-4c25-b53c-4ad46ad38100',
});

// Delete by contact email
const { data, error } = await resend.contacts.remove({
  email: 'acme@example.com',
});
```

```
{
  "object": "contact",
  "contact": "520784e2-887d-4c25-b53c-4ad46ad38100",
  "deleted": true
}
```

## ​Path Parameters

 Either `id` or `email` must be provided. [​](#param-id)idstringThe Contact ID. [​](#param-email)emailstringThe Contact email.[Update Contact](https://resend.com/docs/api-reference/contacts/update-contact)[Add Contact to Segment](https://resend.com/docs/api-reference/contacts/add-contact-to-segment)Ctrl+I

---

# Retrieve Contact Topics

> Retrieve a list of topics subscriptions for a contact.

[Resend home page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

// Get by contact id
const { data, error } = await resend.contacts.topics.list({
  id: 'e169aa45-1ecf-4183-9955-b1499d5701d3',
});

// Get by contact email
const { data, error } = await resend.contacts.topics.list({
  email: 'steve.wozniak@gmail.com',
});
```

```
{
  "object": "list",
  "has_more": false,
  "data": [
    {
      "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
      "name": "Product Updates",
      "description": "New features, and latest announcements.",
      "subscription": "opt_in"
    }
  ]
}
```

GEThttps://api.resend.com/contacts/:contact_id/topics

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

// Get by contact id
const { data, error } = await resend.contacts.topics.list({
  id: 'e169aa45-1ecf-4183-9955-b1499d5701d3',
});

// Get by contact email
const { data, error } = await resend.contacts.topics.list({
  email: 'steve.wozniak@gmail.com',
});
```

```
{
  "object": "list",
  "has_more": false,
  "data": [
    {
      "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
      "name": "Product Updates",
      "description": "New features, and latest announcements.",
      "subscription": "opt_in"
    }
  ]
}
```

## ​Path Parameters

 Either `id` or `email` must be provided. [​](#param-id)idstringThe Contact ID. [​](#param-email)emailstringThe Contact Email.

## Query Parameters

Note that the `limit` parameter is *optional*. If you do not provide a `limit`, all topics will be returned in a single response.[​](#limit)limitnumberNumber of topics to retrieve.

- Maximum value: `100`
- Minimum value: `1`

[​](#after)afterstringThe ID *after* which we'll retrieve more topics (for pagination). This ID will *not* be included in the returned list. Cannot be used with the`before` parameter.[​](#before)beforestringThe ID *before* which we'll retrieve more topics (for pagination). This ID will *not* be included in the returned list. Cannot be used with the `after` parameter.You can only use either `after` or `before` parameter, not both. See our [pagination guide](https://resend.com/docs/api-reference/pagination) for more information.[Delete Contact Segment](https://resend.com/docs/api-reference/contacts/delete-contact-segment)[Update Contact Topics](https://resend.com/docs/api-reference/contacts/update-contact-topics)Ctrl+I

---

# Retrieve Contact

> Retrieve a single contact.

[Resend home page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

// Get by contact id
const { data, error } = await resend.contacts.get({
  id: 'e169aa45-1ecf-4183-9955-b1499d5701d3',
});

// Get by contact email
const { data, error } = await resend.contacts.get({
  email: 'steve.wozniak@gmail.com',
});
```

```
{
  "object": "contact",
  "id": "e169aa45-1ecf-4183-9955-b1499d5701d3",
  "email": "steve.wozniak@gmail.com",
  "first_name": "Steve",
  "last_name": "Wozniak",
  "created_at": "2023-10-06T23:47:56.678Z",
  "unsubscribed": false,
  "properties": {
    "company_name": "Acme Corp",
    "department": "Engineering"
  }
}
```

GEThttps://api.resend.com/contacts/:id

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

// Get by contact id
const { data, error } = await resend.contacts.get({
  id: 'e169aa45-1ecf-4183-9955-b1499d5701d3',
});

// Get by contact email
const { data, error } = await resend.contacts.get({
  email: 'steve.wozniak@gmail.com',
});
```

```
{
  "object": "contact",
  "id": "e169aa45-1ecf-4183-9955-b1499d5701d3",
  "email": "steve.wozniak@gmail.com",
  "first_name": "Steve",
  "last_name": "Wozniak",
  "created_at": "2023-10-06T23:47:56.678Z",
  "unsubscribed": false,
  "properties": {
    "company_name": "Acme Corp",
    "department": "Engineering"
  }
}
```

## ​Path Parameters

 Either `id` or `email` must be provided. [​](#param-id)idstringThe Contact ID. [​](#param-email)emailstringThe Contact Email.[Create Contact](https://resend.com/docs/api-reference/contacts/create-contact)[List Contacts](https://resend.com/docs/api-reference/contacts/list-contacts)Ctrl+I

---

# List Contact Segments

> Retrieve a list of segments that a contact is part of.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.contacts.segments.list({
  id: 'e169aa45-1ecf-4183-9955-b1499d5701d3',
});
```

```
{
  "object": "list",
  "data": [
    {
      "id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
      "name": "Registered Users",
      "created_at": "2023-10-06T22:59:55.977Z"
    }
  ],
  "has_more": false
}
```

GEThttps://api.resend.com/contacts/:id/segments

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.contacts.segments.list({
  id: 'e169aa45-1ecf-4183-9955-b1499d5701d3',
});
```

```
{
  "object": "list",
  "data": [
    {
      "id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
      "name": "Registered Users",
      "created_at": "2023-10-06T22:59:55.977Z"
    }
  ],
  "has_more": false
}
```

## ​Path Parameters

 Either `id` or `email` must be provided. [​](#param-id)idstringThe Contact ID. [​](#param-email)emailstringThe Contact Email.

## Query Parameters

Note that the `limit` parameter is *optional*. If you do not provide a `limit`, all segments will be returned in a single response.[​](#limit)limitnumberNumber of segments to retrieve.

- Maximum value: `100`
- Minimum value: `1`

[​](#after)afterstringThe ID *after* which we'll retrieve more segments (for pagination). This ID will *not* be included in the returned list. Cannot be used with the`before` parameter.[​](#before)beforestringThe ID *before* which we'll retrieve more segments (for pagination). This ID will *not* be included in the returned list. Cannot be used with the `after` parameter.You can only use either `after` or `before` parameter, not both. See our [pagination guide](https://resend.com/docs/api-reference/pagination) for more information.[Add Contact to Segment](https://resend.com/docs/api-reference/contacts/add-contact-to-segment)[Delete Contact Segment](https://resend.com/docs/api-reference/contacts/delete-contact-segment)Ctrl +I$/$

---

# List Contacts

> Show all contacts.

[Resend home page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.contacts.list();
```

```
{
  "object": "list",
  "has_more": false,
  "data": [
    {
      "id": "e169aa45-1ecf-4183-9955-b1499d5701d3",
      "email": "steve.wozniak@gmail.com",
      "first_name": "Steve",
      "last_name": "Wozniak",
      "created_at": "2023-10-06T23:47:56.678Z",
      "unsubscribed": false,
      "properties": {
        "company_name": "Acme Corp",
        "department": "Engineering"
      }
    }
  ]
}
```

GEThttps://api.resend.com/contacts

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.contacts.list();
```

```
{
  "object": "list",
  "has_more": false,
  "data": [
    {
      "id": "e169aa45-1ecf-4183-9955-b1499d5701d3",
      "email": "steve.wozniak@gmail.com",
      "first_name": "Steve",
      "last_name": "Wozniak",
      "created_at": "2023-10-06T23:47:56.678Z",
      "unsubscribed": false,
      "properties": {
        "company_name": "Acme Corp",
        "department": "Engineering"
      }
    }
  ]
}
```

## ​Path Parameters

 [​](#segment-id)segmentIdstringThe Segment ID to filter contacts by. If provided, only contacts in this Segment will be returned.

## Query Parameters

Note that the `limit` parameter is *optional*. If you do not provide a `limit`, all contacts will be returned in a single response.[​](#limit)limitnumberNumber of contacts to retrieve.

- Maximum value: `100`
- Minimum value: `1`

[​](#after)afterstringThe ID *after* which we'll retrieve more contacts (for pagination). This ID will *not* be included in the returned list. Cannot be used with the`before` parameter.[​](#before)beforestringThe ID *before* which we'll retrieve more contacts (for pagination). This ID will *not* be included in the returned list. Cannot be used with the `after` parameter.You can only use either `after` or `before` parameter, not both. See our [pagination guide](https://resend.com/docs/api-reference/pagination) for more information.[Retrieve Contact](https://resend.com/docs/api-reference/contacts/get-contact)[Update Contact](https://resend.com/docs/api-reference/contacts/update-contact)Ctrl+I

---

# Update Contact Topics

> Update topic subscriptions for a contact.

[Resend home page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

// Update by contact id
const { data, error } = await resend.contacts.topics.update({
  id: 'e169aa45-1ecf-4183-9955-b1499d5701d3',
  topics: [
    {
      id: 'b6d24b8e-af0b-4c3c-be0c-359bbd97381e',
      subscription: 'opt_out',
    },
    {
      id: '07d84122-7224-4881-9c31-1c048e204602',
      subscription: 'opt_in',
    },
  ],
});

// Update by contact email
const { data, error } = await resend.contacts.topics.update({
  email: 'steve.wozniak@gmail.com',
  topics: [
    {
      id: '07d84122-7224-4881-9c31-1c048e204602',
      subscription: 'opt_out',
    },
    {
      id: '07d84122-7224-4881-9c31-1c048e204602',
      subscription: 'opt_in',
    },
  ],
});
```

```
{
  "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"
}
```

PATCHhttps://api.resend.com/contacts/:contact_id/topics

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

// Update by contact id
const { data, error } = await resend.contacts.topics.update({
  id: 'e169aa45-1ecf-4183-9955-b1499d5701d3',
  topics: [
    {
      id: 'b6d24b8e-af0b-4c3c-be0c-359bbd97381e',
      subscription: 'opt_out',
    },
    {
      id: '07d84122-7224-4881-9c31-1c048e204602',
      subscription: 'opt_in',
    },
  ],
});

// Update by contact email
const { data, error } = await resend.contacts.topics.update({
  email: 'steve.wozniak@gmail.com',
  topics: [
    {
      id: '07d84122-7224-4881-9c31-1c048e204602',
      subscription: 'opt_out',
    },
    {
      id: '07d84122-7224-4881-9c31-1c048e204602',
      subscription: 'opt_in',
    },
  ],
});
```

```
{
  "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"
}
```

## ​Path Parameters

 Either `id` or `email` must be provided. [​](#param-id)idstringThe Contact ID. [​](#param-email)emailstringThe Contact Email.

## ​Body Parameters

 [​](#param-topics)topicsarrayrequiredArray of topic subscription updates.

Hide properties

[​](#param-id-1)idstringrequiredThe Topic ID.[​](#param-subscription)subscriptionstringrequiredThe subscription action. Must be either `opt_in` or `opt_out`.[Retrieve Contact Topics](https://resend.com/docs/api-reference/contacts/get-contact-topics)[Create Contact Property](https://resend.com/docs/api-reference/contact-properties/create-contact-property)Ctrl+I

---

# Update Contact

> Update an existing contact.

[Resend home page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

// Update by contact id
const { data, error } = await resend.contacts.update({
  id: 'e169aa45-1ecf-4183-9955-b1499d5701d3',
  unsubscribed: true,
});

// Update by contact email
const { data, error } = await resend.contacts.update({
  email: 'acme@example.com',
  unsubscribed: true,
});
```

```
{
  "object": "contact",
  "id": "479e3145-dd38-476b-932c-529ceb705947"
}
```

PATCHhttps://api.resend.com/contacts/:id

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

// Update by contact id
const { data, error } = await resend.contacts.update({
  id: 'e169aa45-1ecf-4183-9955-b1499d5701d3',
  unsubscribed: true,
});

// Update by contact email
const { data, error } = await resend.contacts.update({
  email: 'acme@example.com',
  unsubscribed: true,
});
```

```
{
  "object": "contact",
  "id": "479e3145-dd38-476b-932c-529ceb705947"
}
```

## ​Path Parameters

 Either `id` or `email` must be provided. [​](#param-id)idstringThe Contact ID. [​](#param-email)emailstringThe Contact Email.

## ​Body Parameters

 [​](#first-name)firstNamestringThe first name of the contact. [​](#last-name)lastNamestringThe last name of the contact. [​](#param-unsubscribed)unsubscribedbooleanThe Contact’s global subscription status. If set to `true`, the contact will
be unsubscribed from all Broadcasts. [​](#param-properties)propertiesobjectA map of custom property keys and values to update.

Hide custom properties

[​](#param-key)keystringrequiredThe property key.[​](#param-value)valuestringrequiredThe property value.[List Contacts](https://resend.com/docs/api-reference/contacts/list-contacts)[Delete Contact](https://resend.com/docs/api-reference/contacts/delete-contact)Ctrl+I

---

# Create Domain

> Create a domain through the Resend Email API.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.domains.create({ name: 'example.com' });
```

```
{
  "id": "4dd369bc-aa82-4ff3-97de-514ae3000ee0",
  "name": "example.com",
  "created_at": "2023-03-28T17:12:02.059593+00:00",
  "status": "not_started",
  "capabilities": {
    "sending": "enabled",
    "receiving": "disabled"
  },
  "records": [
    {
      "record": "SPF",
      "name": "send",
      "type": "MX",
      "ttl": "Auto",
      "status": "not_started",
      "value": "feedback-smtp.us-east-1.amazonses.com",
      "priority": 10
    },
    {
      "record": "SPF",
      "name": "send",
      "value": "\"v=spf1 include:amazonses.com ~all\"",
      "type": "TXT",
      "ttl": "Auto",
      "status": "not_started"
    },
    {
      "record": "DKIM",
      "name": "nhapbbryle57yxg3fbjytyodgbt2kyyg._domainkey",
      "value": "nhapbbryle57yxg3fbjytyodgbt2kyyg.dkim.amazonses.com.",
      "type": "CNAME",
      "status": "not_started",
      "ttl": "Auto"
    },
    {
      "record": "DKIM",
      "name": "xbakwbe5fcscrhzshpap6kbxesf6pfgn._domainkey",
      "value": "xbakwbe5fcscrhzshpap6kbxesf6pfgn.dkim.amazonses.com.",
      "type": "CNAME",
      "status": "not_started",
      "ttl": "Auto"
    },
    {
      "record": "DKIM",
      "name": "txrcreso3dqbvcve45tqyosxwaegvhgn._domainkey",
      "value": "txrcreso3dqbvcve45tqyosxwaegvhgn.dkim.amazonses.com.",
      "type": "CNAME",
      "status": "not_started",
      "ttl": "Auto"
    }
  ],
  "region": "us-east-1"
}
```

POSThttps://api.resend.com/domains

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.domains.create({ name: 'example.com' });
```

```
{
  "id": "4dd369bc-aa82-4ff3-97de-514ae3000ee0",
  "name": "example.com",
  "created_at": "2023-03-28T17:12:02.059593+00:00",
  "status": "not_started",
  "capabilities": {
    "sending": "enabled",
    "receiving": "disabled"
  },
  "records": [
    {
      "record": "SPF",
      "name": "send",
      "type": "MX",
      "ttl": "Auto",
      "status": "not_started",
      "value": "feedback-smtp.us-east-1.amazonses.com",
      "priority": 10
    },
    {
      "record": "SPF",
      "name": "send",
      "value": "\"v=spf1 include:amazonses.com ~all\"",
      "type": "TXT",
      "ttl": "Auto",
      "status": "not_started"
    },
    {
      "record": "DKIM",
      "name": "nhapbbryle57yxg3fbjytyodgbt2kyyg._domainkey",
      "value": "nhapbbryle57yxg3fbjytyodgbt2kyyg.dkim.amazonses.com.",
      "type": "CNAME",
      "status": "not_started",
      "ttl": "Auto"
    },
    {
      "record": "DKIM",
      "name": "xbakwbe5fcscrhzshpap6kbxesf6pfgn._domainkey",
      "value": "xbakwbe5fcscrhzshpap6kbxesf6pfgn.dkim.amazonses.com.",
      "type": "CNAME",
      "status": "not_started",
      "ttl": "Auto"
    },
    {
      "record": "DKIM",
      "name": "txrcreso3dqbvcve45tqyosxwaegvhgn._domainkey",
      "value": "txrcreso3dqbvcve45tqyosxwaegvhgn.dkim.amazonses.com.",
      "type": "CNAME",
      "status": "not_started",
      "ttl": "Auto"
    }
  ],
  "region": "us-east-1"
}
```

## ​Body Parameters

 [​](#param-name)namestringrequiredThe name of the domain you want to create. [​](#param-region)regionstringdefault:"us-east-1"The region where emails will be sent from. Possible values: `'us-east-1' |     'eu-west-1' | 'sa-east-1' | 'ap-northeast-1'` [​](#custom-return-path)customReturnPathstringdefault:"send"For advanced use cases, choose a subdomain for the Return-Path address. The
custom return path is used for SPF authentication, DMARC alignment, and
handling bounced emails. Defaults to `send` (i.e., `send.yourdomain.tld`). Avoid
setting values that could undermine credibility (e.g. `testing`), as they may
be exposed to recipients.Learn more about [custom return paths](https://resend.com/docs/dashboard/domains/introduction#custom-return-path). [​](#open-tracking)openTrackingbooleanTrack the open rate of each email. [​](#click-tracking)clickTrackingbooleanTrack clicks within the body of each HTML email. [​](#param-tls)tlsstringdefault:"opportunistic"

- `opportunistic`: Opportunistic TLS means that it always attempts to make a
  secure connection to the receiving mail server. If it can’t establish a
  secure connection, it sends the message unencrypted.
- `enforced`: Enforced TLS on the other hand, requires that the email
  communication must use TLS no matter what. If the receiving server does
  not support TLS, the email will not be sent.

 [​](#param-capabilities)capabilitiesobjectConfigure the domain capabilities for sending and receiving emails. At least one capability must be enabled.

Show properties

[​](#param-sending)sendingstringdefault:"enabled"Enable or disable sending emails from this domain. Possible values: `'enabled' | 'disabled'`[​](#param-receiving)receivingstringdefault:"disabled"Enable or disable receiving emails to this domain. Possible values: `'enabled' | 'disabled'` See all available `status` types in [the Domains
overview](https://resend.com/docs/dashboard/domains/introduction#understand-a-domain-status).[List Attachments](https://resend.com/docs/api-reference/emails/list-received-email-attachments)[Verify Domain](https://resend.com/docs/api-reference/domains/verify-domain)Ctrl +I$/$

---

# Delete Domain

> Remove an existing domain.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.domains.remove(
  'd91cd9bd-1176-453e-8fc1-35364d380206',
);
```

```
{
  "object": "domain",
  "id": "d91cd9bd-1176-453e-8fc1-35364d380206",
  "deleted": true
}
```

DELETEhttps://api.resend.com/domains/:domain_id

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.domains.remove(
  'd91cd9bd-1176-453e-8fc1-35364d380206',
);
```

```
{
  "object": "domain",
  "id": "d91cd9bd-1176-453e-8fc1-35364d380206",
  "deleted": true
}
```

## ​Path Parameters

 [​](#domain-id)domainIdstringrequiredThe Domain ID.[Update Domain](https://resend.com/docs/api-reference/domains/update-domain)[Create API key](https://resend.com/docs/api-reference/api-keys/create-api-key)Ctrl +I$/$

---

# Retrieve Domain

> Retrieve a single domain for the authenticated user.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.domains.get(
  'd91cd9bd-1176-453e-8fc1-35364d380206',
);
```

```
{
  "object": "domain",
  "id": "d91cd9bd-1176-453e-8fc1-35364d380206",
  "name": "example.com",
  "status": "not_started",
  "created_at": "2023-04-26T20:21:26.347412+00:00",
  "region": "us-east-1",
  "capabilities": {
    "sending": "enabled",
    "receiving": "disabled"
  },
  "records": [
    {
      "record": "SPF",
      "name": "send",
      "type": "MX",
      "ttl": "Auto",
      "status": "not_started",
      "value": "feedback-smtp.us-east-1.amazonses.com",
      "priority": 10
    },
    {
      "record": "SPF",
      "name": "send",
      "value": "\"v=spf1 include:amazonses.com ~all\"",
      "type": "TXT",
      "ttl": "Auto",
      "status": "not_started"
    },
    {
      "record": "DKIM",
      "name": "resend._domainkey",
      "value": "p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDsc4Lh8xilsngyKEgN2S84+21gn+x6SEXtjWvPiAAmnmggr5FWG42WnqczpzQ/mNblqHz4CDwUum6LtY6SdoOlDmrhvp5khA3cd661W9FlK3yp7+jVACQElS7d9O6jv8VsBbVg4COess3gyLE5RyxqF1vYsrEXqyM8TBz1n5AGkQIDAQA2",
      "type": "TXT",
      "status": "not_started",
      "ttl": "Auto"
    }
  ]
}
```

GEThttps://api.resend.com/domains/:domain_id

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.domains.get(
  'd91cd9bd-1176-453e-8fc1-35364d380206',
);
```

```
{
  "object": "domain",
  "id": "d91cd9bd-1176-453e-8fc1-35364d380206",
  "name": "example.com",
  "status": "not_started",
  "created_at": "2023-04-26T20:21:26.347412+00:00",
  "region": "us-east-1",
  "capabilities": {
    "sending": "enabled",
    "receiving": "disabled"
  },
  "records": [
    {
      "record": "SPF",
      "name": "send",
      "type": "MX",
      "ttl": "Auto",
      "status": "not_started",
      "value": "feedback-smtp.us-east-1.amazonses.com",
      "priority": 10
    },
    {
      "record": "SPF",
      "name": "send",
      "value": "\"v=spf1 include:amazonses.com ~all\"",
      "type": "TXT",
      "ttl": "Auto",
      "status": "not_started"
    },
    {
      "record": "DKIM",
      "name": "resend._domainkey",
      "value": "p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDsc4Lh8xilsngyKEgN2S84+21gn+x6SEXtjWvPiAAmnmggr5FWG42WnqczpzQ/mNblqHz4CDwUum6LtY6SdoOlDmrhvp5khA3cd661W9FlK3yp7+jVACQElS7d9O6jv8VsBbVg4COess3gyLE5RyxqF1vYsrEXqyM8TBz1n5AGkQIDAQA2",
      "type": "TXT",
      "status": "not_started",
      "ttl": "Auto"
    }
  ]
}
```

## ​Path Parameters

 [​](#domain-id)domainIdstringrequiredThe Domain ID. See all available `status` types in [the Domains
overview](https://resend.com/docs/dashboard/domains/introduction#understand-a-domain-status).[Verify Domain](https://resend.com/docs/api-reference/domains/verify-domain)[List Domains](https://resend.com/docs/api-reference/domains/list-domains)Ctrl +I$/$

---

# List Domains

> Retrieve a list of domains for the authenticated user.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.domains.list();
```

```
{
  "object": "list",
  "has_more": false,
  "data": [
    {
      "id": "d91cd9bd-1176-453e-8fc1-35364d380206",
      "name": "example.com",
      "status": "not_started",
      "created_at": "2023-04-26T20:21:26.347412+00:00",
      "region": "us-east-1",
      "capabilities": {
        "sending": "enabled",
        "receiving": "disabled"
      }
    }
  ]
}
```

GEThttps://api.resend.com/domains

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.domains.list();
```

```
{
  "object": "list",
  "has_more": false,
  "data": [
    {
      "id": "d91cd9bd-1176-453e-8fc1-35364d380206",
      "name": "example.com",
      "status": "not_started",
      "created_at": "2023-04-26T20:21:26.347412+00:00",
      "region": "us-east-1",
      "capabilities": {
        "sending": "enabled",
        "receiving": "disabled"
      }
    }
  ]
}
```

See all available `status` types in [the Domains
overview](https://resend.com/docs/dashboard/domains/introduction#understand-a-domain-status).

## Query Parameters

Note that the `limit` parameter is *optional*. If you do not provide a `limit`, all domains will be returned in a single response.[​](#limit)limitnumberNumber of domains to retrieve.

- Maximum value: `100`
- Minimum value: `1`

[​](#after)afterstringThe ID *after* which we'll retrieve more domains (for pagination). This ID will *not* be included in the returned list. Cannot be used with the`before` parameter.[​](#before)beforestringThe ID *before* which we'll retrieve more domains (for pagination). This ID will *not* be included in the returned list. Cannot be used with the `after` parameter.You can only use either `after` or `before` parameter, not both. See our [pagination guide](https://resend.com/docs/api-reference/pagination) for more information.[Retrieve Domain](https://resend.com/docs/api-reference/domains/get-domain)[Update Domain](https://resend.com/docs/api-reference/domains/update-domain)Ctrl +I$/$

---

# Update Domain

> Update an existing domain.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.domains.update({
  id: 'b8617ad3-b712-41d9-81a0-f7c3d879314e',
  openTracking: false,
  clickTracking: true,
  tls: 'enforced',
});
```

```
{
  "object": "domain",
  "id": "b8617ad3-b712-41d9-81a0-f7c3d879314e"
}
```

PATCHhttps://api.resend.com/domains/:domain_id

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.domains.update({
  id: 'b8617ad3-b712-41d9-81a0-f7c3d879314e',
  openTracking: false,
  clickTracking: true,
  tls: 'enforced',
});
```

```
{
  "object": "domain",
  "id": "b8617ad3-b712-41d9-81a0-f7c3d879314e"
}
```

## ​Path Parameters

## ​Body Parameters

     [​](#param-tls)tlsstringdefault:"opportunistic"

- `opportunistic`: Opportunistic TLS means that it always attempts to make a
  secure connection to the receiving mail server. If it can’t establish a
  secure connection, it sends the message unencrypted.
- `enforced`: Enforced TLS on the other hand, requires that the email
  communication must use TLS no matter what. If the receiving server does
  not support TLS, the email will not be sent.

 [​](#param-capabilities)capabilitiesobjectUpdate the domain capabilities for sending and receiving emails. You can specify one or both fields. Omitted fields will keep their current value. At least one capability must remain enabled.

Show   properties

[​](#param-sending)sendingstringEnable or disable sending emails from this domain. Possible values: `'enabled' | 'disabled'`[​](#param-receiving)receivingstringEnable or disable receiving emails to this domain. Possible values: `'enabled' | 'disabled'`

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.domains.update({
  id: 'b8617ad3-b712-41d9-81a0-f7c3d879314e',
  openTracking: false,
  clickTracking: true,
  tls: 'enforced',
});
```

```
{
  "object": "domain",
  "id": "b8617ad3-b712-41d9-81a0-f7c3d879314e"
}
```

[List Domains](https://resend.com/docs/api-reference/domains/list-domains)[Delete Domain](https://resend.com/docs/api-reference/domains/delete-domain)⌘ I$/$

---

# Verify Domain

> Verify an existing domain.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.domains.verify(
  'd91cd9bd-1176-453e-8fc1-35364d380206',
);
```

```
{
  "object": "domain",
  "id": "d91cd9bd-1176-453e-8fc1-35364d380206"
}
```

POSThttps://api.resend.com/domains/:domain_id/verify

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.domains.verify(
  'd91cd9bd-1176-453e-8fc1-35364d380206',
);
```

```
{
  "object": "domain",
  "id": "d91cd9bd-1176-453e-8fc1-35364d380206"
}
```

## ​Path Parameters

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.domains.verify(
  'd91cd9bd-1176-453e-8fc1-35364d380206',
);
```

```
{
  "object": "domain",
  "id": "d91cd9bd-1176-453e-8fc1-35364d380206"
}
```

[Create Domain](https://resend.com/docs/api-reference/domains/create-domain)[Retrieve Domain](https://resend.com/docs/api-reference/domains/get-domain)⌘ I$/$
