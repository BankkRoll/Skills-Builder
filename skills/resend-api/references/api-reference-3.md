# Usage Limits and more

# Usage Limits

> Learn about API rate limits, email sending quotas, and contact quotas.

The Resend API enforces three types of limits: **rate limits** control how many API requests you can make per second, **email quotas** control the total number of emails you can send per day and month, and **contact quotas** control how many marketing contacts you can store.

## ​Rate Limits

### ​Response Headers

 The response headers describe your current rate limit following every request in conformance with the [sixth IETF standard draft](https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-ratelimit-headers-06):

| Header name | Description |
| --- | --- |
| ratelimit-limit | Maximum number of requests allowed within a window. |
| ratelimit-remaining | How many requests you have left within the current window. |
| ratelimit-reset | How many seconds until the limits are reset. |
| retry-after | How many seconds you should wait before making a follow-up request. |

 The default maximum rate limit is **2 requests per second**. This number can be increased for trusted senders upon request. After that, you’ll hit the rate limit and receive a `429` response error code. You can find all 429 responses by filtering for 429 at the [Resend Logs page](https://resend.com/logs?status=429). To prevent this, we recommend reducing the rate at which you request the API. This can be done by introducing a queue mechanism or reducing the number of concurrent requests per second. If you have specific requirements, [contact support](https://resend.com/contact) to request a rate increase.

## ​Email Quotas

### ​Response Headers

 In addition to rate limits, the API returns headers that track your email sending quotas:

| Header name | Description |
| --- | --- |
| x-resend-daily-quota | Your used daily email sending quota. Only sent to free plan users. |
| x-resend-monthly-quota | Your used monthly email sending quota. |

 These headers help you monitor your usage and avoid hitting quota limits. When you exceed your quota limits, you’ll receive a `429` response error code with one of the following error types:

- **daily_quota_exceeded** - You have reached your daily email quota. [Upgrade your plan](https://resend.com/settings/billing) to remove the daily quota limit or wait until 24 hours have passed.
- **monthly_quota_exceeded** - You have reached your monthly email quota. [Upgrade your plan](https://resend.com/settings/billing) to increase the monthly email quota.

 Both sent and received emails count towards these quotas. See the full list of [error codes](https://resend.com/docs/api-reference/errors) for more details.

## ​Contact Quotas

 Contact quotas restrict the number of contacts you can store for marketing emails and broadcasts. You can add more contacts beyond your plan’s limit, but you won’t be able to send broadcasts until you upgrade your plan. When you attempt to send a broadcast after reaching your contact limit, you’ll receive a `403` response error code with a `validation_error` type and the message: “You have reached your contacts quota. Please upgrade your plan to send more emails.” To increase your contact limit, [upgrade your Marketing plan](https://resend.com/settings/billing).

---

# Create Segment

> Create a new segment for contacts to be added to.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.segments.create({
  name: 'Registered Users',
});
```

```
{
  "object": "segment",
  "id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
  "name": "Registered Users"
}
```

POSThttps://api.resend.com/segments

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.segments.create({
  name: 'Registered Users',
});
```

```
{
  "object": "segment",
  "id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
  "name": "Registered Users"
}
```

## ​Body Parameters

 [​](#param-name)namestringrequiredThe name of the segment you want to create.[Delete Contact Property](https://resend.com/docs/api-reference/contact-properties/delete-contact-property)[Retrieve Segment](https://resend.com/docs/api-reference/segments/get-segment)Ctrl +I$/$

---

# Delete Segment

> Remove an existing segment.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.segments.remove(
  '78261eea-8f8b-4381-83c6-79fa7120f1cf',
);
```

```
{
  "object": "segment",
  "id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
  "deleted": true
}
```

DELETEhttps://api.resend.com/segments/:segment_id

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.segments.remove(
  '78261eea-8f8b-4381-83c6-79fa7120f1cf',
);
```

```
{
  "object": "segment",
  "id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
  "deleted": true
}
```

## ​Path Parameters

 [​](#segment-id)segmentIdstringrequiredThe Segment ID.[List Segments](https://resend.com/docs/api-reference/segments/list-segments)[Create Audience](https://resend.com/docs/api-reference/audiences/create-audience)Ctrl +I$/$

---

# Retrieve Segment

> Retrieve a single segment.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.segments.get(
  '78261eea-8f8b-4381-83c6-79fa7120f1cf',
);
```

```
{
  "object": "segment",
  "id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
  "name": "Registered Users",
  "created_at": "2023-10-06T22:59:55.977Z"
}
```

GEThttps://api.resend.com/segments/:segment_id

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.segments.get(
  '78261eea-8f8b-4381-83c6-79fa7120f1cf',
);
```

```
{
  "object": "segment",
  "id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
  "name": "Registered Users",
  "created_at": "2023-10-06T22:59:55.977Z"
}
```

## ​Path Parameters

 [​](#segment-id)segmentIdstringrequiredThe Segment ID.[Create Segment](https://resend.com/docs/api-reference/segments/create-segment)[List Segments](https://resend.com/docs/api-reference/segments/list-segments)Ctrl +I$/$

---

# List Segments

> Retrieve a list of segments.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.segments.list();
```

```
{
  "object": "list",
  "has_more": false,
  "data": [
    {
      "id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
      "name": "Registered Users",
      "created_at": "2023-10-06T22:59:55.977Z"
    }
  ]
}
```

GEThttps://api.resend.com/segments

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.segments.list();
```

```
{
  "object": "list",
  "has_more": false,
  "data": [
    {
      "id": "78261eea-8f8b-4381-83c6-79fa7120f1cf",
      "name": "Registered Users",
      "created_at": "2023-10-06T22:59:55.977Z"
    }
  ]
}
```

## Query Parameters

Note that the `limit` parameter is *optional*. If you do not provide a `limit`, all segments will be returned in a single response.[​](#limit)limitnumberNumber of segments to retrieve.

- Maximum value: `100`
- Minimum value: `1`

[​](#after)afterstringThe ID *after* which we'll retrieve more segments (for pagination). This ID will *not* be included in the returned list. Cannot be used with the`before` parameter.[​](#before)beforestringThe ID *before* which we'll retrieve more segments (for pagination). This ID will *not* be included in the returned list. Cannot be used with the `after` parameter.You can only use either `after` or `before` parameter, not both. See our [pagination guide](https://resend.com/docs/api-reference/pagination) for more information.[Retrieve Segment](https://resend.com/docs/api-reference/segments/get-segment)[Delete Segment](https://resend.com/docs/api-reference/segments/delete-segment)Ctrl +I$/$

---

# Create Template

> Create a new template with optional variables.

[Resend home page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.templates.create({
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
    }
  ],
});

// Or create and publish a template in one step
await resend.templates.create({ ... }).publish();
```

```
{
  "id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794",
  "object": "template"
}
```

POSThttps://api.resend.com/templates

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.templates.create({
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
    }
  ],
});

// Or create and publish a template in one step
await resend.templates.create({ ... }).publish();
```

```
{
  "id": "49a3999c-0ce1-4ea6-ab68-afcd6dc2e794",
  "object": "template"
}
```

## ​Body Parameters

 [​](#param-name)namestringrequiredThe name of the template. [​](#param-html)htmlstringrequiredThe HTML version of the template. [​](#param-alias)aliasstringThe alias of the template. [​](#param-from)fromstringSender email address.To include a friendly name, use the format `"Your Name <sender@domain.com>"`.If provided, this value can be overridden when sending an email using the template. [​](#param-subject)subjectstringDefault email subject.This value can be overridden when sending an email using the template. [​](#reply-to)replyTostring | string[]Default Reply-to email address. For multiple addresses, send as an array of strings.This value can be overridden when sending an email using the template. [​](#param-text)textstringThe plain text version of the message.If not provided, the HTML will be used to generate a plain text version. You can opt out of this behavior by setting value to an empty string. [​](#param-react)reactReact.ReactNodeThe React component used to write the template. *Only available in the Node.js
SDK.* [​](#param-variables)variablesarrayThe array of variables used in the template. Each template may contain up to 50 variables.Each variable is an object with the following properties:

Hide properties

[​](#param-key)keystringrequiredThe key of the variable. We recommend capitalizing the key (e.g. `PRODUCT_NAME`). The following variable names are reserved and cannot be used:
`FIRST_NAME`, `LAST_NAME`, `EMAIL`, `RESEND_UNSUBSCRIBE_URL`, `contact`, and `this`.[​](#param-type)type'string' | 'number'requiredThe type of the variable.Can be `'string'` or `'number'`[​](#fallback-value)fallbackValuestring | numberThe fallback value of the variable. The value must match the type of the variable.If no fallback value is provided, you must provide a value for the variable when sending an email using the template.Before you can use a template, you must publish it first. To publish a
template, use the [Templates dashboard](https://resend.com/templates) or
[publish template API](https://resend.com/docs/api-reference/templates/publish-template).[Learn more about Templates](https://resend.com/docs/dashboard/templates/introduction).[Delete Topic](https://resend.com/docs/api-reference/topics/delete-topic)[Get Template](https://resend.com/docs/api-reference/templates/get-template)Ctrl+I

---

# Delete Template

> Delete a template.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.templates.remove(
  '34a080c9-b17d-4187-ad80-5af20266e535',
);
```

```
{
  "object": "template",
  "id": "34a080c9-b17d-4187-ad80-5af20266e535",
  "deleted": true
}
```

DELETEhttps://api.resend.com/templates/:id

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.templates.remove(
  '34a080c9-b17d-4187-ad80-5af20266e535',
);
```

```
{
  "object": "template",
  "id": "34a080c9-b17d-4187-ad80-5af20266e535",
  "deleted": true
}
```

## ​Path Parameters

 [​](#param-id-alias)id | aliasstringThe ID or alias of the template to delete.[Update Template](https://resend.com/docs/api-reference/templates/update-template)[Publish Template](https://resend.com/docs/api-reference/templates/publish-template)Ctrl +I$/$

---

# Duplicate Template

> Duplicate a template.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.templates.duplicate(
  '34a080c9-b17d-4187-ad80-5af20266e535',
);
```

```
{
  "object": "template",
  "id": "e169aa45-1ecf-4183-9955-b1499d5701d3"
}
```

POSThttps://api.resend.com/templates/:id/duplicate

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.templates.duplicate(
  '34a080c9-b17d-4187-ad80-5af20266e535',
);
```

```
{
  "object": "template",
  "id": "e169aa45-1ecf-4183-9955-b1499d5701d3"
}
```

## ​Path Parameters

 [​](#param-id-alias)id | aliasstringThe ID or alias of the template to duplicate.[Publish Template](https://resend.com/docs/api-reference/templates/publish-template)[Create Webhook](https://resend.com/docs/api-reference/webhooks/create-webhook)Ctrl +I$/$

---

# Get Template

> Get a template by ID.

[Resend home page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.templates.get(
  '34a080c9-b17d-4187-ad80-5af20266e535',
);
```

```
{
  "object": "template",
  "id": "34a080c9-b17d-4187-ad80-5af20266e535",
  "current_version_id": "b2693018-7abb-4b4b-b4cb-aadf72dc06bd",
  "alias": "reset-password",
  "name": "reset-password",
  "created_at": "2023-10-06T23:47:56.678Z",
  "updated_at": "2023-10-06T23:47:56.678Z",
  "status": "published",
  "published_at": "2023-10-06T23:47:56.678Z",
  "from": "John Doe <john.doe@example.com>",
  "subject": "Hello, world!",
  "reply_to": null,
  "html": "<h1>Hello, world!</h1>",
  "text": "Hello, world!",
  "variables": [
    {
      "id": "e169aa45-1ecf-4183-9955-b1499d5701d3",
      "key": "user_name",
      "type": "string",
      "fallback_value": "John Doe",
      "created_at": "2023-10-06T23:47:56.678Z",
      "updated_at": "2023-10-06T23:47:56.678Z"
    }
  ],
  "has_unpublished_versions": true
}
```

GEThttps://api.resend.com/templates/:id

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.templates.get(
  '34a080c9-b17d-4187-ad80-5af20266e535',
);
```

```
{
  "object": "template",
  "id": "34a080c9-b17d-4187-ad80-5af20266e535",
  "current_version_id": "b2693018-7abb-4b4b-b4cb-aadf72dc06bd",
  "alias": "reset-password",
  "name": "reset-password",
  "created_at": "2023-10-06T23:47:56.678Z",
  "updated_at": "2023-10-06T23:47:56.678Z",
  "status": "published",
  "published_at": "2023-10-06T23:47:56.678Z",
  "from": "John Doe <john.doe@example.com>",
  "subject": "Hello, world!",
  "reply_to": null,
  "html": "<h1>Hello, world!</h1>",
  "text": "Hello, world!",
  "variables": [
    {
      "id": "e169aa45-1ecf-4183-9955-b1499d5701d3",
      "key": "user_name",
      "type": "string",
      "fallback_value": "John Doe",
      "created_at": "2023-10-06T23:47:56.678Z",
      "updated_at": "2023-10-06T23:47:56.678Z"
    }
  ],
  "has_unpublished_versions": true
}
```

## ​Path Parameters

 [​](#param-id-alias)id | aliasstringThe ID or alias of the template to get.[Create Template](https://resend.com/docs/api-reference/templates/create-template)[List Templates](https://resend.com/docs/api-reference/templates/list-templates)Ctrl+I

---

# List Templates

> List all templates.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.templates.list({
  limit: 2,
  after: '34a080c9-b17d-4187-ad80-5af20266e535',
});
```

```
{
  "object": "list",
  "data": [
    {
      "id": "e169aa45-1ecf-4183-9955-b1499d5701d3",
      "name": "reset-password",
      "status": "draft",
      "published_at": null,
      "created_at": "2023-10-06T23:47:56.678Z",
      "updated_at": "2023-10-06T23:47:56.678Z",
      "alias": "reset-password"
    },
    {
      "id": "b7f9c2e1-1234-4abc-9def-567890abcdef",
      "name": "welcome-message",
      "status": "published",
      "published_at": "2023-10-06T23:47:56.678Z",
      "created_at": "2023-10-06T23:47:56.678Z",
      "updated_at": "2023-10-06T23:47:56.678Z",
      "alias": "welcome-message"
    }
  ],
  "has_more": false
}
```

GEThttps://api.resend.com/templates

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.templates.list({
  limit: 2,
  after: '34a080c9-b17d-4187-ad80-5af20266e535',
});
```

```
{
  "object": "list",
  "data": [
    {
      "id": "e169aa45-1ecf-4183-9955-b1499d5701d3",
      "name": "reset-password",
      "status": "draft",
      "published_at": null,
      "created_at": "2023-10-06T23:47:56.678Z",
      "updated_at": "2023-10-06T23:47:56.678Z",
      "alias": "reset-password"
    },
    {
      "id": "b7f9c2e1-1234-4abc-9def-567890abcdef",
      "name": "welcome-message",
      "status": "published",
      "published_at": "2023-10-06T23:47:56.678Z",
      "created_at": "2023-10-06T23:47:56.678Z",
      "updated_at": "2023-10-06T23:47:56.678Z",
      "alias": "welcome-message"
    }
  ],
  "has_more": false
}
```

By default, the API will return the most recent 20 templates. You can optionally use the `limit` parameter to return a different number of templates or control the pagination of the results with the `after` or `before` parameters.

## Query Parameters

[​](#limit)limitnumberNumber of templates to retrieve.

- Default value: `20`
- Maximum value: `100`
- Minimum value: `1`

[​](#after)afterstringThe ID *after* which we'll retrieve more templates (for pagination). This ID will *not* be included in the returned list. Cannot be used with the`before` parameter.[​](#before)beforestringThe ID *before* which we'll retrieve more templates (for pagination). This ID will *not* be included in the returned list. Cannot be used with the `after` parameter.You can only use either `after` or `before` parameter, not both. See our [pagination guide](https://resend.com/docs/api-reference/pagination) for more information.[Get Template](https://resend.com/docs/api-reference/templates/get-template)[Update Template](https://resend.com/docs/api-reference/templates/update-template)Ctrl +I$/$

---

# Publish Template

> Publish a template.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.templates.publish(
  '34a080c9-b17d-4187-ad80-5af20266e535',
);
```

```
{
  "id": "34a080c9-b17d-4187-ad80-5af20266e535",
  "object": "template"
}
```

POSThttps://api.resend.com/templates/:id/publish

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.templates.publish(
  '34a080c9-b17d-4187-ad80-5af20266e535',
);
```

```
{
  "id": "34a080c9-b17d-4187-ad80-5af20266e535",
  "object": "template"
}
```

## ​Path Parameters

 [​](#param-id-alias)id | aliasstringThe ID or alias of the template to publish.[Delete Template](https://resend.com/docs/api-reference/templates/delete-template)[Duplicate Template](https://resend.com/docs/api-reference/templates/duplicate-template)Ctrl +I$/$

---

# Update Template

> Update a template.

[Resend home page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.templates.update(
  '34a080c9-b17d-4187-ad80-5af20266e535',
  {
    name: 'order-confirmation',
    html: '<p>Total: {{{PRICE}}}</p><p>Name: {{{PRODUCT}}}</p>',
  },
);
```

```
{
  "id": "34a080c9-b17d-4187-ad80-5af20266e535",
  "object": "template"
}
```

PATCHhttps://api.resend.com/templates/:id

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.templates.update(
  '34a080c9-b17d-4187-ad80-5af20266e535',
  {
    name: 'order-confirmation',
    html: '<p>Total: {{{PRICE}}}</p><p>Name: {{{PRODUCT}}}</p>',
  },
);
```

```
{
  "id": "34a080c9-b17d-4187-ad80-5af20266e535",
  "object": "template"
}
```

## ​Path Parameters

 [​](#param-id-alias)id | aliasstringThe ID or alias of the template to duplicate.

## ​Body Parameters

 [​](#param-name)namestringThe name of the template. [​](#param-html)htmlstringThe HTML version of the template. [​](#param-alias)aliasstringThe alias of the template. [​](#param-from)fromstringSender email address.To include a friendly name, use the format `"Your Name <sender@domain.com>"`.If provided, this value can be overridden when sending an email using the template. [​](#param-subject)subjectstringDefault email subject.This value can be overridden when sending an email using the template. [​](#reply-to)replyTostring | string[]Default Reply-to email address. For multiple addresses, send as an array of strings.This value can be overridden when sending an email using the template. [​](#param-text)textstringThe plain text version of the message.If not provided, the HTML will be used to generate a plain text version. You can opt out of this behavior by setting value to an empty string. [​](#param-react)reactReact.ReactNodeThe React component used to write the template. *Only available in the Node.js
SDK.* [​](#param-variables)variablesarrayThe array of variables used in the template. Each template may contain up to 50 variables.Each variable is an object with the following properties:

Hide properties

[​](#param-key)keystringrequiredThe key of the variable. We recommend capitalizing the key (e.g. `PRODUCT_NAME`). The following variable names are reserved and cannot be used:
`FIRST_NAME`, `LAST_NAME`, `EMAIL`, `RESEND_UNSUBSCRIBE_URL`, `contact`, and `this`.[​](#param-type)type'string' | 'number'requiredThe type of the variable.Can be `'string'` or `'number'`[​](#fallback-value)fallbackValuestring | numberThe fallback value of the variable. The value must match the type of the variable.If no fallback value is provided, you must provide a value for the variable when sending an email using the template.Before you can use a template, you must publish it first. To publish a
template, use the [Templates dashboard](https://resend.com/templates) or
[publish template API](https://resend.com/docs/api-reference/templates/publish-template).[Learn more about Templates](https://resend.com/docs/dashboard/templates/introduction).[List Templates](https://resend.com/docs/api-reference/templates/list-templates)[Delete Template](https://resend.com/docs/api-reference/templates/delete-template)Ctrl+I

---

# Create Topic

> Create and email topics to segment your audience.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.topics.create({
  name: 'Weekly Newsletter',
  defaultSubscription: 'opt_in',
});
```

```
{
  "object": "topic",
  "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"
}
```

POSThttps://api.resend.com/topics

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.topics.create({
  name: 'Weekly Newsletter',
  defaultSubscription: 'opt_in',
});
```

```
{
  "object": "topic",
  "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"
}
```

## ​Body Parameters

 [​](#param-name)namestringrequiredThe topic name. Max length is `50` characters. [​](#default-subscription)defaultSubscriptionstringrequiredThe default subscription preference for new contacts. Possible values:
`opt_in` or `opt_out`.This value cannot be changed later. [​](#param-description)descriptionstringThe topic description. Max length is `200` characters. [​](#visibility)visibilitystringThe visibility of the topic on the unsubscribe page. Possible values: `public` or `private`.

- `private`: only contacts who are opted in to the topic can see it on the unsubscribe page.
- `public`: all contacts can see the topic on the unsubscribe page.

If not specified, defaults to `private`.[Delete Audience](https://resend.com/docs/api-reference/audiences/delete-audience)[Retrieve Topic](https://resend.com/docs/api-reference/topics/get-topic)Ctrl +I$/$

---

# Delete Topic

> Remove an existing topic.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.topics.remove(
  'b6d24b8e-af0b-4c3c-be0c-359bbd97381e',
);
```

```
{
  "object": "topic",
  "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
  "deleted": true
}
```

DELETEhttps://api.resend.com/topics/:topic_id

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.topics.remove(
  'b6d24b8e-af0b-4c3c-be0c-359bbd97381e',
);
```

```
{
  "object": "topic",
  "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
  "deleted": true
}
```

## ​Path Parameters

 [​](#topic-id)topicIdstringrequiredThe topic ID.[Update Topic](https://resend.com/docs/api-reference/topics/update-topic)[Create Template](https://resend.com/docs/api-reference/templates/create-template)Ctrl +I$/$

---

# Retrieve Topic

> Retrieve a topic by its ID.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.topics.get(
  'b6d24b8e-af0b-4c3c-be0c-359bbd97381e',
);
```

```
{
  "object": "topic",
  "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
  "name": "Weekly Newsletter",
  "description": "Weekly newsletter for our subscribers",
  "default_subscription": "opt_in",
  "visibility": "public",
  "created_at": "2023-04-08T00:11:13.110779+00:00"
}
```

GEThttps://api.resend.com/topics/:topic_id

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.topics.get(
  'b6d24b8e-af0b-4c3c-be0c-359bbd97381e',
);
```

```
{
  "object": "topic",
  "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
  "name": "Weekly Newsletter",
  "description": "Weekly newsletter for our subscribers",
  "default_subscription": "opt_in",
  "visibility": "public",
  "created_at": "2023-04-08T00:11:13.110779+00:00"
}
```

## ​Path Parameters

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.topics.get(
  'b6d24b8e-af0b-4c3c-be0c-359bbd97381e',
);
```

```
{
  "object": "topic",
  "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
  "name": "Weekly Newsletter",
  "description": "Weekly newsletter for our subscribers",
  "default_subscription": "opt_in",
  "visibility": "public",
  "created_at": "2023-04-08T00:11:13.110779+00:00"
}
```

[Create Topic](https://resend.com/docs/api-reference/topics/create-topic)[List Topics](https://resend.com/docs/api-reference/topics/list-topics)⌘ I$/$

---

# List Topics

> Retrieve a list of topics for the authenticated user.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.topics.list();
```

```
{
  "object": "list",
  "has_more": false,
  "data": [
    {
      "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
      "name": "Weekly Newsletter",
      "description": "Weekly newsletter for our subscribers",
      "default_subscription": "opt_in",
      "visibility": "public",
      "created_at": "2023-04-08T00:11:13.110779+00:00"
    }
  ]
}
```

GEThttps://api.resend.com/topics

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.topics.list();
```

```
{
  "object": "list",
  "has_more": false,
  "data": [
    {
      "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e",
      "name": "Weekly Newsletter",
      "description": "Weekly newsletter for our subscribers",
      "default_subscription": "opt_in",
      "visibility": "public",
      "created_at": "2023-04-08T00:11:13.110779+00:00"
    }
  ]
}
```

## Query Parameters

[​](#limit)limitnumberNumber of topics to retrieve.

- Default value: `20`
- Maximum value: `100`
- Minimum value: `1`

[​](#after)afterstringThe ID *after* which we'll retrieve more topics (for pagination). This ID will *not* be included in the returned list. Cannot be used with the`before` parameter.[​](#before)beforestringThe ID *before* which we'll retrieve more topics (for pagination). This ID will *not* be included in the returned list. Cannot be used with the `after` parameter.You can only use either `after` or `before` parameter, not both. See our [pagination guide](https://resend.com/docs/api-reference/pagination) for more information.[Retrieve Topic](https://resend.com/docs/api-reference/topics/get-topic)[Update Topic](https://resend.com/docs/api-reference/topics/update-topic)Ctrl +I$/$

---

# Update Topic

> Update an existing topic.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.topics.update(
  'b6d24b8e-af0b-4c3c-be0c-359bbd97381e',
  {
    name: 'Weekly Newsletter',
    description: 'Weekly newsletter for our subscribers',
  },
);
```

```
{
  "object": "topic",
  "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"
}
```

PATCHhttps://api.resend.com/topics/:topic_id

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.topics.update(
  'b6d24b8e-af0b-4c3c-be0c-359bbd97381e',
  {
    name: 'Weekly Newsletter',
    description: 'Weekly newsletter for our subscribers',
  },
);
```

```
{
  "object": "topic",
  "id": "b6d24b8e-af0b-4c3c-be0c-359bbd97381e"
}
```

## ​Path Parameters

 [​](#topic-id)topicIdstringrequiredThe Topic ID.

## ​Body Parameters

 [​](#param-name)namestringThe topic name. Max length is `50` characters. [​](#param-description)descriptionstringThe topic description. Max length is `200` characters. [​](#visibility)visibilitystringThe visibility of the topic on the unsubscribe page. Possible values: `public` or `private`.

- `private`: only contacts who are opted in to the topic can see it on the unsubscribe page.
- `public`: all contacts can see the topic on the unsubscribe page.

[List Topics](https://resend.com/docs/api-reference/topics/list-topics)[Delete Topic](https://resend.com/docs/api-reference/topics/delete-topic)Ctrl +I$/$

---

# Create Webhook

> Create a webhook to receive real-time notifications about email events.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.webhooks.create({
  endpoint: 'https://example.com/handler',
  events: ['email.sent'],
});
```

```
{
  "object": "webhook",
  "id": "4dd369bc-aa82-4ff3-97de-514ae3000ee0",
  "signing_secret": "whsec_xxxxxxxxxx"
}
```

POSThttps://api.resend.com/webhooks

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.webhooks.create({
  endpoint: 'https://example.com/handler',
  events: ['email.sent'],
});
```

```
{
  "object": "webhook",
  "id": "4dd369bc-aa82-4ff3-97de-514ae3000ee0",
  "signing_secret": "whsec_xxxxxxxxxx"
}
```

## ​Body Parameters

 [​](#param-endpoint)endpointstringrequiredThe URL where webhook events will be sent. [​](#param-events)eventsstring[]requiredArray of event types to subscribe to.See [event types](https://resend.com/docs/webhooks/event-types) for available options.[Duplicate Template](https://resend.com/docs/api-reference/templates/duplicate-template)[Retrieve Webhook](https://resend.com/docs/api-reference/webhooks/get-webhook)Ctrl +I$/$

---

# Delete Webhook

> Remove an existing webhook.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.webhooks.remove(
  '4dd369bc-aa82-4ff3-97de-514ae3000ee0',
);
```

```
{
  "object": "webhook",
  "id": "4dd369bc-aa82-4ff3-97de-514ae3000ee0",
  "deleted": true
}
```

DELETEhttps://api.resend.com/webhooks/:webhook_id

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.webhooks.remove(
  '4dd369bc-aa82-4ff3-97de-514ae3000ee0',
);
```

```
{
  "object": "webhook",
  "id": "4dd369bc-aa82-4ff3-97de-514ae3000ee0",
  "deleted": true
}
```

## ​Path Parameters

 [​](#webhook-id)webhookIdstringrequiredThe Webhook ID.[Update Webhook](https://resend.com/docs/api-reference/webhooks/update-webhook)Ctrl +I$/$

---

# Retrieve Webhook

> Retrieve a single webhook for the authenticated user.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.webhooks.get(
  '4dd369bc-aa82-4ff3-97de-514ae3000ee0',
);
```

```
{
  "object": "webhook",
  "id": "4dd369bc-aa82-4ff3-97de-514ae3000ee0",
  "created_at": "2023-08-22T15:28:00.000Z",
  "status": "enabled",
  "endpoint": "https://example.com/handler",
  "events": ["email.sent"],
  "signing_secret": "whsec_xxxxxxxxxx"
}
```

GEThttps://api.resend.com/webhooks/:webhook_id

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.webhooks.get(
  '4dd369bc-aa82-4ff3-97de-514ae3000ee0',
);
```

```
{
  "object": "webhook",
  "id": "4dd369bc-aa82-4ff3-97de-514ae3000ee0",
  "created_at": "2023-08-22T15:28:00.000Z",
  "status": "enabled",
  "endpoint": "https://example.com/handler",
  "events": ["email.sent"],
  "signing_secret": "whsec_xxxxxxxxxx"
}
```

## ​Path Parameters

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.webhooks.get(
  '4dd369bc-aa82-4ff3-97de-514ae3000ee0',
);
```

```
{
  "object": "webhook",
  "id": "4dd369bc-aa82-4ff3-97de-514ae3000ee0",
  "created_at": "2023-08-22T15:28:00.000Z",
  "status": "enabled",
  "endpoint": "https://example.com/handler",
  "events": ["email.sent"],
  "signing_secret": "whsec_xxxxxxxxxx"
}
```

[Create Webhook](https://resend.com/docs/api-reference/webhooks/create-webhook)[List Webhooks](https://resend.com/docs/api-reference/webhooks/list-webhooks)⌘ I$/$

---

# List Webhooks

> Retrieve a list of webhooks for the authenticated user.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.webhooks.list();
```

```
{
  "object": "list",
  "has_more": false,
  "data": [
    {
      "id": "7ab123cd-ef45-6789-abcd-ef0123456789",
      "created_at": "2023-09-10T10:15:30.000Z",
      "status": "disabled",
      "endpoint": "https://first-webhook.example.com/handler",
      "events": ["email.sent"]
    },
    {
      "id": "4dd369bc-aa82-4ff3-97de-514ae3000ee0",
      "created_at": "2023-08-22T15:28:00.000Z",
      "status": "enabled",
      "endpoint": "https://second-webhook.example.com/receive",
      "events": ["email.received"]
    }
  ]
}
```

GEThttps://api.resend.com/webhooks

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.webhooks.list();
```

```
{
  "object": "list",
  "has_more": false,
  "data": [
    {
      "id": "7ab123cd-ef45-6789-abcd-ef0123456789",
      "created_at": "2023-09-10T10:15:30.000Z",
      "status": "disabled",
      "endpoint": "https://first-webhook.example.com/handler",
      "events": ["email.sent"]
    },
    {
      "id": "4dd369bc-aa82-4ff3-97de-514ae3000ee0",
      "created_at": "2023-08-22T15:28:00.000Z",
      "status": "enabled",
      "endpoint": "https://second-webhook.example.com/receive",
      "events": ["email.received"]
    }
  ]
}
```

## Query Parameters

Note that the `limit` parameter is *optional*. If you do not provide a `limit`, all webhooks will be returned in a single response.[​](#limit)limitnumberNumber of webhooks to retrieve.

- Maximum value: `100`
- Minimum value: `1`

[​](#after)afterstringThe ID *after* which we'll retrieve more webhooks (for pagination). This ID will *not* be included in the returned list. Cannot be used with the`before` parameter.[​](#before)beforestringThe ID *before* which we'll retrieve more webhooks (for pagination). This ID will *not* be included in the returned list. Cannot be used with the `after` parameter.You can only use either `after` or `before` parameter, not both. See our [pagination guide](https://resend.com/docs/api-reference/pagination) for more information.[Retrieve Webhook](https://resend.com/docs/api-reference/webhooks/get-webhook)[Update Webhook](https://resend.com/docs/api-reference/webhooks/update-webhook)Ctrl +I$/$

---

# Update Webhook

> Update an existing webhook configuration.

$/$[Resendhome page](https://resend.com)

- [Documentation](https://resend.com/docs/introduction)
- [API Reference](https://resend.com/docs/api-reference/introduction)
- [Webhook Events](https://resend.com/docs/webhooks/introduction)
- [Knowledge Base](https://resend.com/docs/knowledge-base/introduction)

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.webhooks.update(
  '430eed87-632a-4ea6-90db-0aace67ec228',
  {
    endpoint: 'https://new-webhook.example.com/handler',
    events: ['email.sent', 'email.delivered'],
    status: 'enabled',
  },
);
```

```
{
  "object": "webhook",
  "id": "430eed87-632a-4ea6-90db-0aace67ec228"
}
```

PATCHhttps://api.resend.com/webhooks/:webhook_id

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.webhooks.update(
  '430eed87-632a-4ea6-90db-0aace67ec228',
  {
    endpoint: 'https://new-webhook.example.com/handler',
    events: ['email.sent', 'email.delivered'],
    status: 'enabled',
  },
);
```

```
{
  "object": "webhook",
  "id": "430eed87-632a-4ea6-90db-0aace67ec228"
}
```

## ​Path Parameters

## ​Body Parameters

 [​](#param-endpoint)endpointstringThe URL where webhook events will be sent. [​](#param-events)eventsstring[]Array of event types to subscribe to.See [event types](https://resend.com/docs/webhooks/event-types) for available options. [​](#param-status)statusstringThe webhook status. Can be either `enabled` or `disabled`.

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.webhooks.update(
  '430eed87-632a-4ea6-90db-0aace67ec228',
  {
    endpoint: 'https://new-webhook.example.com/handler',
    events: ['email.sent', 'email.delivered'],
    status: 'enabled',
  },
);
```

```
{
  "object": "webhook",
  "id": "430eed87-632a-4ea6-90db-0aace67ec228"
}
```

[List Webhooks](https://resend.com/docs/api-reference/webhooks/list-webhooks)[Delete Webhook](https://resend.com/docs/api-reference/webhooks/delete-webhook)⌘ I$/$
