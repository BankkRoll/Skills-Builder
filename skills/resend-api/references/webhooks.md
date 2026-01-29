# contact.created and more

# contact.created

> Received when a contact is created.

Event triggered whenever a **contact was successfully created**. *Note: When importing multiple contacts using CSV, these events won’t be triggered.Contact supportif you have any questions.*

## Response Body Parameters

All webhook payloads follow a consistent top-level structure with event-specific data nested within the `data` object.[​](#type)typestringThe event type that triggered the webhook (e.g., `contact.created`).[​](#created-at)created_atstringISO 8601 timestamp when the webhook event was created.[​](#data)dataobjectEvent-specific data containing detailed information about the event. The data object for the `contact.created` event contains the following parameters:

Hide object parameters

[​](#param-id)idstringUnique identifier for the contact[​](#param-audience-id)audience_idstringUnique identifier for the audience this contact belongs to[​](#param-segment-ids)segment_idsarrayArray of segment IDs the contact belongs to[​](#param-created-at)created_atstringISO 8601 timestamp when the contact was created[​](#param-updated-at)updated_atstringISO 8601 timestamp when the contact was last updated[​](#param-email)emailstringContact’s email address[​](#param-first-name)first_namestringContact’s first name[​](#param-last-name)last_namestringContact’s last name[​](#param-unsubscribed)unsubscribedbooleanWhether the contact has unsubscribed from all emails sent from your team

---

# contact.deleted

> Received when a contact is deleted.

Event triggered whenever a **contact was successfully deleted**.

## Response Body Parameters

All webhook payloads follow a consistent top-level structure with event-specific data nested within the `data` object.[​](#type)typestringThe event type that triggered the webhook (e.g., `contact.deleted`).[​](#created-at)created_atstringISO 8601 timestamp when the webhook event was created.[​](#data)dataobjectEvent-specific data containing detailed information about the event. The data object for the `contact.deleted` event contains the following parameters:

Hide object parameters

[​](#param-id)idstringUnique identifier for the contact[​](#param-audience-id)audience_idstringUnique identifier for the audience this contact belongs to[​](#param-segment-ids)segment_idsarrayArray of segment IDs the contact belongs to[​](#param-created-at)created_atstringISO 8601 timestamp when the contact was created[​](#param-updated-at)updated_atstringISO 8601 timestamp when the contact was last updated[​](#param-email)emailstringContact’s email address[​](#param-first-name)first_namestringContact’s first name[​](#param-last-name)last_namestringContact’s last name[​](#param-unsubscribed)unsubscribedbooleanWhether the contact has unsubscribed from all emails sent from your team

---

# contact.updated

> Received when a contact is updated.

Event triggered whenever a **contact was successfully updated**.

## Response Body Parameters

All webhook payloads follow a consistent top-level structure with event-specific data nested within the `data` object.[​](#type)typestringThe event type that triggered the webhook (e.g., `contact.updated`).[​](#created-at)created_atstringISO 8601 timestamp when the webhook event was created.[​](#data)dataobjectEvent-specific data containing detailed information about the event. The data object for the `contact.updated` event contains the following parameters:

Hide object parameters

[​](#param-id)idstringUnique identifier for the contact[​](#param-audience-id)audience_idstringUnique identifier for the audience this contact belongs to[​](#param-segment-ids)segment_idsarrayArray of segment IDs the contact belongs to[​](#param-created-at)created_atstringISO 8601 timestamp when the contact was created[​](#param-updated-at)updated_atstringISO 8601 timestamp when the contact was last updated[​](#param-email)emailstringContact’s email address[​](#param-first-name)first_namestringContact’s first name[​](#param-last-name)last_namestringContact’s last name[​](#param-unsubscribed)unsubscribedbooleanWhether the contact has unsubscribed from all emails sent from your team

---

# domain.created

> Received when a domain is created.

Event triggered when a **domain was successfully created**. If you’re having issues verifying your domain, [review our guide on a domain
not verifying](https://resend.com/docs/knowledge-base/what-if-my-domain-is-not-verifying) for
troubleshooting steps.

## Response Body Parameters

All webhook payloads follow a consistent top-level structure with event-specific data nested within the `data` object.[​](#type)typestringThe event type that triggered the webhook (e.g., `domain.created`).[​](#created-at)created_atstringISO 8601 timestamp when the webhook event was created.[​](#data)dataobjectEvent-specific data containing detailed information about the event. The data object for the `domain.created` event contains the following parameters:

Hide object parameters

[​](#param-id)idstringUnique identifier for the domain[​](#param-name)namestringDomain name (e.g., `example.com`)[​](#param-status)statusverified | partially_failed | failed | pending | not_startedCurrent verification status of the domain:

- `verified`: The domain is verified and can be used to send or receive emails.
- `partially_failed`: The domain is verified but one of the features (send or receive) is not verified.
- `pending`: The domain is pending verification and cannot be used to send or receive emails.
- `not_started`: Verification has not started yet, so the domain cannot be used to send or receive emails.
- `failed`: The domain failed verification.

The `data.status` field represents an aggregated status of the domain. For
domains that can both [send](https://resend.com/docs/dashboard/emails/introduction) and
[receive](https://resend.com/docs/dashboard/receiving/introduction) emails, the status may be
`partially_failed`, which indicates that one of these features is verified
while the other is not.[​](#param-created-at)created_atstringISO 8601 timestamp when the domain was created[​](#param-region)regionus-east-1 | eu-west-1 | sa-east-1 | ap-northeast-1AWS region where the domain is configured.[​](#param-records)recordsarrayArray of DNS record objects required for domain verification

Hide record object

[​](#param-record)recordSPF | DKIM | Receiving MXRecord type purpose. Learn more about [domain verification records](https://resend.com/docs/dashboard/domains/introduction).[​](#param-name-1)namestringDNS record name/subdomain[​](#param-type)typeMX | TXT | CNAMEDNS record type[​](#param-value)valuestringDNS record value to be set[​](#param-ttl)ttlstringTime to live for the DNS record[​](#param-status-1)statusstringVerification status of this specific record[​](#param-priority)prioritynumberPriority value for MX records (optional)

---

# domain.deleted

> Received when a domain is deleted.

Event triggered when a **domain was successfully deleted**. If you’re having issues verifying your domain, [review our guide on a domain
not verifying](https://resend.com/docs/knowledge-base/what-if-my-domain-is-not-verifying) for
troubleshooting steps.

## Response Body Parameters

All webhook payloads follow a consistent top-level structure with event-specific data nested within the `data` object.[​](#type)typestringThe event type that triggered the webhook (e.g., `domain.deleted`).[​](#created-at)created_atstringISO 8601 timestamp when the webhook event was created.[​](#data)dataobjectEvent-specific data containing detailed information about the event. The data object for the `domain.deleted` event contains the following parameters:

Hide object parameters

[​](#param-id)idstringUnique identifier for the domain[​](#param-name)namestringDomain name (e.g., `example.com`)[​](#param-status)statusverified | partially_failed | failed | pending | not_startedCurrent verification status of the domain:

- `verified`: The domain is verified and can be used to send or receive emails.
- `partially_failed`: The domain is verified but one of the features (send or receive) is not verified.
- `pending`: The domain is pending verification and cannot be used to send or receive emails.
- `not_started`: Verification has not started yet, so the domain cannot be used to send or receive emails.
- `failed`: The domain failed verification.

The `data.status` field represents an aggregated status of the domain. For
domains that can both [send](https://resend.com/docs/dashboard/emails/introduction) and
[receive](https://resend.com/docs/dashboard/receiving/introduction) emails, the status may be
`partially_failed`, which indicates that one of these features is verified
while the other is not.[​](#param-created-at)created_atstringISO 8601 timestamp when the domain was created[​](#param-region)regionus-east-1 | eu-west-1 | sa-east-1 | ap-northeast-1AWS region where the domain is configured.[​](#param-records)recordsarrayArray of DNS record objects required for domain verification

Hide record object

[​](#param-record)recordSPF | DKIM | Receiving MXRecord type purpose. Learn more about [domain verification records](https://resend.com/docs/dashboard/domains/introduction).[​](#param-name-1)namestringDNS record name/subdomain[​](#param-type)typeMX | TXT | CNAMEDNS record type[​](#param-value)valuestringDNS record value to be set[​](#param-ttl)ttlstringTime to live for the DNS record[​](#param-status-1)statusstringVerification status of this specific record[​](#param-priority)prioritynumberPriority value for MX records (optional)

---

# domain.updated

> Received when a domain is updated.

Event triggered when a **domain was successfully updated**. If you’re having issues verifying your domain, [review our guide on a domain
not verifying](https://resend.com/docs/knowledge-base/what-if-my-domain-is-not-verifying) for
troubleshooting steps.

## Response Body Parameters

All webhook payloads follow a consistent top-level structure with event-specific data nested within the `data` object.[​](#type)typestringThe event type that triggered the webhook (e.g., `domain.updated`).[​](#created-at)created_atstringISO 8601 timestamp when the webhook event was created.[​](#data)dataobjectEvent-specific data containing detailed information about the event. The data object for the `domain.updated` event contains the following parameters:

Hide object parameters

[​](#param-id)idstringUnique identifier for the domain[​](#param-name)namestringDomain name (e.g., `example.com`)[​](#param-status)statusverified | partially_failed | failed | pending | not_startedCurrent verification status of the domain:

- `verified`: The domain is verified and can be used to send or receive emails.
- `partially_failed`: The domain is verified but one of the features (send or receive) is not verified.
- `pending`: The domain is pending verification and cannot be used to send or receive emails.
- `not_started`: Verification has not started yet, so the domain cannot be used to send or receive emails.
- `failed`: The domain failed verification.

The `data.status` field represents an aggregated status of the domain. For
domains that can both [send](https://resend.com/docs/dashboard/emails/introduction) and
[receive](https://resend.com/docs/dashboard/receiving/introduction) emails, the status may be
`partially_failed`, which indicates that one of these features is verified
while the other is not.[​](#param-created-at)created_atstringISO 8601 timestamp when the domain was created[​](#param-region)regionus-east-1 | eu-west-1 | sa-east-1 | ap-northeast-1AWS region where the domain is configured.[​](#param-records)recordsarrayArray of DNS record objects required for domain verification

Hide record object

[​](#param-record)recordSPF | DKIM | Receiving MXRecord type purpose. Learn more about [domain verification records](https://resend.com/docs/dashboard/domains/introduction).[​](#param-name-1)namestringDNS record name/subdomain[​](#param-type)typeMX | TXT | CNAMEDNS record type[​](#param-value)valuestringDNS record value to be set[​](#param-ttl)ttlstringTime to live for the DNS record[​](#param-status-1)statusstringVerification status of this specific record[​](#param-priority)prioritynumberPriority value for MX records (optional)

---

# email.bounced

> Received when an email bounces.

Event triggered whenever the recipient’s mail server **permanently rejected the email**.

## Response Body Parameters

All webhook payloads follow a consistent top-level structure with event-specific data nested within the `data` object.[​](#type)typestringThe event type that triggered the webhook (e.g., `email.bounced`).[​](#created-at)created_atstringISO 8601 timestamp when the webhook event was created.[​](#data)dataobjectEvent-specific data containing detailed information about the event. The data object for the `email.bounced` event contains the following parameters:

Hide object parameters

[​](#param-broadcast-id)broadcast_idstringUnique identifier for the broadcast campaign (if applicable)[​](#param-created-at)created_atstringISO 8601 timestamp when the email was created[​](#param-email-id)email_idstringUnique identifier for the specific email[​](#param-from)fromstringSender email address and name in the format “Name
<[email@domain.com](mailto:email@domain.com)>”[​](#param-to)toarrayArray of impacted recipient email addresses[​](#param-subject)subjectstringEmail subject line[​](#param-template-id)template_idstringUnique identifier for the template used (if applicable)[​](#param-tags)tagsarrayArray of tag objects associated with the email

Show tag object

[​](#param-name)namestringThe tag key[​](#param-value)valuestringThe tag value[​](#param-bounce)bounceobjectBounce details from the receiving server

Hide bounce object

[​](#param-diagnostic-code)diagnosticCodearrayArray of SMTP diagnostic responses from the receiving server, including the status code and reason for the bounce (e.g., `smtp; 550 5.5.0 Requested action not taken: mailbox unavailable`)[​](#param-message)messagestringDetailed bounce message from the receiving server[​](#param-sub-type)subTypestringBounce sub-type (e.g., `Suppressed`, `MessageRejected`)[​](#param-type)typestringBounce type (e.g., `Permanent`, `Temporary`)Learn more about [bounce types and subtypes](https://resend.com/docs/dashboard/emails/email-bounces).

---

# email.clicked

> Received when an email link is clicked.

Event triggered whenever the **recipient clicks on an email link**.

## Response Body Parameters

All webhook payloads follow a consistent top-level structure with event-specific data nested within the `data` object.[​](#type)typestringThe event type that triggered the webhook (e.g., `email.clicked`).[​](#created-at)created_atstringISO 8601 timestamp when the webhook event was created.[​](#data)dataobjectEvent-specific data containing detailed information about the event. The data object for the `email.clicked` event contains the following parameters:

Hide object parameters

[​](#param-broadcast-id)broadcast_idstringUnique identifier for the broadcast campaign (if applicable)[​](#param-created-at)created_atstringISO 8601 timestamp when the email was created[​](#param-email-id)email_idstringUnique identifier for the specific email[​](#param-from)fromstringSender email address and name in the format “Name
<[email@domain.com](mailto:email@domain.com)>”[​](#param-to)toarrayArray of impacted recipient email addresses[​](#param-subject)subjectstringEmail subject line[​](#param-template-id)template_idstringUnique identifier for the template used (if applicable)[​](#param-tags)tagsarrayArray of tag objects associated with the email

Show tag object

[​](#param-name)namestringThe tag key[​](#param-value)valuestringThe tag value[​](#param-click)clickobjectClick tracking details

Hide click object

[​](#param-ip-address)ipAddressstringIP address of the user who clicked the link[​](#param-link)linkstringThe URL that was clicked[​](#param-timestamp)timestampstringISO 8601 timestamp when the click occurred[​](#param-user-agent)userAgentstringUser agent string of the browser that clicked the link

---

# email.complained

> Received when an email is marked as spam.

Event triggered whenever the email was successfully **delivered, but the recipient marked it as spam**.

## Response Body Parameters

All webhook payloads follow a consistent top-level structure with event-specific data nested within the `data` object.[​](#type)typestringThe event type that triggered the webhook (e.g., `email.complained`).[​](#created-at)created_atstringISO 8601 timestamp when the webhook event was created.[​](#data)dataobjectEvent-specific data containing detailed information about the event. The data object for the `email.complained` event contains the following parameters:

Hide object parameters

[​](#param-broadcast-id)broadcast_idstringUnique identifier for the broadcast campaign (if applicable)[​](#param-created-at)created_atstringISO 8601 timestamp when the email was created[​](#param-email-id)email_idstringUnique identifier for the specific email[​](#param-from)fromstringSender email address and name in the format “Name
<[email@domain.com](mailto:email@domain.com)>”[​](#param-to)toarrayArray of impacted recipient email addresses[​](#param-subject)subjectstringEmail subject line[​](#param-template-id)template_idstringUnique identifier for the template used (if applicable)[​](#param-tags)tagsarrayArray of tag objects associated with the email

Show tag object

[​](#param-name)namestringThe tag key[​](#param-value)valuestringThe tag value

---

# email.delivered

> Received when an email is delivered.

Event triggered whenever Resend **successfully delivered the email** to the recipient’s mail server. Learn more about what to do [when an email is delivered, but the recipient
does not receive
it](https://resend.com/docs/knowledge-base/what-if-an-email-says-delivered-but-the-recipient-has-not-received-it).

## Response Body Parameters

All webhook payloads follow a consistent top-level structure with event-specific data nested within the `data` object.[​](#type)typestringThe event type that triggered the webhook (e.g., `email.delivered`).[​](#created-at)created_atstringISO 8601 timestamp when the webhook event was created.[​](#data)dataobjectEvent-specific data containing detailed information about the event. The data object for the `email.delivered` event contains the following parameters:

Hide object parameters

[​](#param-broadcast-id)broadcast_idstringUnique identifier for the broadcast campaign (if applicable)[​](#param-created-at)created_atstringISO 8601 timestamp when the email was created[​](#param-email-id)email_idstringUnique identifier for the specific email[​](#param-from)fromstringSender email address and name in the format “Name
<[email@domain.com](mailto:email@domain.com)>”[​](#param-to)toarrayArray of impacted recipient email addresses[​](#param-subject)subjectstringEmail subject line[​](#param-template-id)template_idstringUnique identifier for the template used (if applicable)[​](#param-tags)tagsarrayArray of tag objects associated with the email

Show tag object

[​](#param-name)namestringThe tag key[​](#param-value)valuestringThe tag value

---

# email.delivery_delayed

> Received when an email delivery is delayed.

Event triggered whenever the **email couldn’t be delivered due to a temporary issue**. Delivery delays can occur, for example, when the recipient’s inbox is full, or when the receiving email server experiences a transient issue.

## Response Body Parameters

All webhook payloads follow a consistent top-level structure with event-specific data nested within the `data` object.[​](#type)typestringThe event type that triggered the webhook (e.g., `email.delivery_delayed`).[​](#created-at)created_atstringISO 8601 timestamp when the webhook event was created.[​](#data)dataobjectEvent-specific data containing detailed information about the event. The data object for the `email.delivery_delayed` event contains the following parameters:

Hide object parameters

[​](#param-broadcast-id)broadcast_idstringUnique identifier for the broadcast campaign (if applicable)[​](#param-created-at)created_atstringISO 8601 timestamp when the email was created[​](#param-email-id)email_idstringUnique identifier for the specific email[​](#param-from)fromstringSender email address and name in the format “Name
<[email@domain.com](mailto:email@domain.com)>”[​](#param-to)toarrayArray of impacted recipient email addresses[​](#param-subject)subjectstringEmail subject line[​](#param-template-id)template_idstringUnique identifier for the template used (if applicable)[​](#param-tags)tagsarrayArray of tag objects associated with the email

Show tag object

[​](#param-name)namestringThe tag key[​](#param-value)valuestringThe tag value

---

# email.failed

> Received when an email fails to send.

Event triggered whenever the **email failed to send due to an error**. This event is triggered when there are issues such as invalid recipients, API key problems, domain verification issues, email quota limits, or other sending failures.

## Response Body Parameters

All webhook payloads follow a consistent top-level structure with event-specific data nested within the `data` object.[​](#type)typestringThe event type that triggered the webhook (e.g., `email.failed`).[​](#created-at)created_atstringISO 8601 timestamp when the webhook event was created.[​](#data)dataobjectEvent-specific data containing detailed information about the event. The data object for the `email.failed` event contains the following parameters:

Hide object parameters

[​](#param-broadcast-id)broadcast_idstringUnique identifier for the broadcast campaign (if applicable)[​](#param-created-at)created_atstringISO 8601 timestamp when the email was created[​](#param-email-id)email_idstringUnique identifier for the specific email[​](#param-from)fromstringSender email address and name in the format “Name
<[email@domain.com](mailto:email@domain.com)>”[​](#param-to)toarrayArray of impacted recipient email addresses[​](#param-subject)subjectstringEmail subject line[​](#param-template-id)template_idstringUnique identifier for the template used (if applicable)[​](#param-tags)tagsarrayArray of tag objects associated with the email

Show tag object

[​](#param-name)namestringThe tag key[​](#param-value)valuestringThe tag value[​](#param-failed)failedobjectFailure details

Hide failed object

[​](#param-reason)reasonstringReason for the email failure (e.g., `reached_daily_quota`)

---

# email.opened

> Received when an email is opened.

Event triggered whenever the **recipient opened the email**.

## Response Body Parameters

All webhook payloads follow a consistent top-level structure with event-specific data nested within the `data` object.[​](#type)typestringThe event type that triggered the webhook (e.g., `email.opened`).[​](#created-at)created_atstringISO 8601 timestamp when the webhook event was created.[​](#data)dataobjectEvent-specific data containing detailed information about the event. The data object for the `email.opened` event contains the following parameters:

Hide object parameters

[​](#param-broadcast-id)broadcast_idstringUnique identifier for the broadcast campaign (if applicable)[​](#param-created-at)created_atstringISO 8601 timestamp when the email was created[​](#param-email-id)email_idstringUnique identifier for the specific email[​](#param-from)fromstringSender email address and name in the format “Name
<[email@domain.com](mailto:email@domain.com)>”[​](#param-to)toarrayArray of impacted recipient email addresses[​](#param-subject)subjectstringEmail subject line[​](#param-template-id)template_idstringUnique identifier for the template used (if applicable)[​](#param-tags)tagsarrayArray of tag objects associated with the email

Show tag object

[​](#param-name)namestringThe tag key[​](#param-value)valuestringThe tag value

---

# email.received

> Received when an inbound email is received.

Event triggered whenever Resend **successfully receives an email**.

## Response Body Parameters

All webhook payloads follow a consistent top-level structure with event-specific data nested within the `data` object.[​](#type)typestringThe event type that triggered the webhook (e.g., `email.received`).[​](#created-at)created_atstringISO 8601 timestamp when the webhook event was created.[​](#data)dataobjectEvent-specific data containing detailed information about the event. The data object for the `email.received` event contains the following parameters:

Hide object parameters

[​](#param-broadcast-id)broadcast_idstringUnique identifier for the broadcast campaign (if applicable)[​](#param-created-at)created_atstringISO 8601 timestamp when the email was created[​](#param-email-id)email_idstringUnique identifier for the specific email[​](#param-from)fromstringSender email address and name in the format “Name
<[email@domain.com](mailto:email@domain.com)>”[​](#param-to)toarrayArray of impacted recipient email addresses[​](#param-subject)subjectstringEmail subject line[​](#param-template-id)template_idstringUnique identifier for the template used (if applicable)[​](#param-tags)tagsarrayArray of tag objects associated with the email

Show tag object

[​](#param-name)namestringThe tag key[​](#param-value)valuestringThe tag value

---

# email.scheduled

> Received when an email is scheduled to be sent.

Event triggered whenever the **email is scheduled to be sent**.

## Response Body Parameters

All webhook payloads follow a consistent top-level structure with event-specific data nested within the `data` object.[​](#type)typestringThe event type that triggered the webhook (e.g., `email.scheduled`).[​](#created-at)created_atstringISO 8601 timestamp when the webhook event was created.[​](#data)dataobjectEvent-specific data containing detailed information about the event. The data object for the `email.scheduled` event contains the following parameters:

Hide object parameters

[​](#param-broadcast-id)broadcast_idstringUnique identifier for the broadcast campaign (if applicable)[​](#param-created-at)created_atstringISO 8601 timestamp when the email was created[​](#param-email-id)email_idstringUnique identifier for the specific email[​](#param-from)fromstringSender email address and name in the format “Name
<[email@domain.com](mailto:email@domain.com)>”[​](#param-to)toarrayArray of impacted recipient email addresses[​](#param-subject)subjectstringEmail subject line[​](#param-template-id)template_idstringUnique identifier for the template used (if applicable)[​](#param-tags)tagsarrayArray of tag objects associated with the email

Show tag object

[​](#param-name)namestringThe tag key[​](#param-value)valuestringThe tag value

---

# email.sent

> Received when an email is sent.

Event triggered whenever the **API request was successful**. Resend will attempt to deliver the message to the recipient’s mail server.

## Response Body Parameters

All webhook payloads follow a consistent top-level structure with event-specific data nested within the `data` object.[​](#type)typestringThe event type that triggered the webhook (e.g., `email.sent`).[​](#created-at)created_atstringISO 8601 timestamp when the webhook event was created.[​](#data)dataobjectEvent-specific data containing detailed information about the event. The data object for the `email.sent` event contains the following parameters:

Hide object parameters

[​](#param-broadcast-id)broadcast_idstringUnique identifier for the broadcast campaign (if applicable)[​](#param-created-at)created_atstringISO 8601 timestamp when the email was created[​](#param-email-id)email_idstringUnique identifier for the specific email[​](#param-from)fromstringSender email address and name in the format “Name
<[email@domain.com](mailto:email@domain.com)>”[​](#param-to)toarrayArray of impacted recipient email addresses[​](#param-subject)subjectstringEmail subject line[​](#param-template-id)template_idstringUnique identifier for the template used (if applicable)[​](#param-tags)tagsarrayArray of tag objects associated with the email

Show tag object

[​](#param-name)namestringThe tag key[​](#param-value)valuestringThe tag value

---

# email.suppressed

> Received when an email is suppressed.

Event triggered whenever the **email is suppressed** by Resend. Learn more about [suppressed
emails](https://resend.com/docs/knowledge-base/why-are-my-emails-landing-on-the-suppression-list).

## Response Body Parameters

All webhook payloads follow a consistent top-level structure with event-specific data nested within the `data` object.[​](#type)typestringThe event type that triggered the webhook (e.g., `email.suppressed`).[​](#created-at)created_atstringISO 8601 timestamp when the webhook event was created.[​](#data)dataobjectEvent-specific data containing detailed information about the event. The data object for the `email.suppressed` event contains the following parameters:

Hide object parameters

[​](#param-broadcast-id)broadcast_idstringUnique identifier for the broadcast campaign (if applicable)[​](#param-created-at)created_atstringISO 8601 timestamp when the email was created[​](#param-email-id)email_idstringUnique identifier for the specific email[​](#param-from)fromstringSender email address and name in the format “Name
<[email@domain.com](mailto:email@domain.com)>”[​](#param-to)toarrayArray of impacted recipient email addresses[​](#param-subject)subjectstringEmail subject line[​](#param-template-id)template_idstringUnique identifier for the template used (if applicable)[​](#param-tags)tagsarrayArray of tag objects associated with the email

Show tag object

[​](#param-name)namestringThe tag key[​](#param-value)valuestringThe tag value

---

# Event Types

> List of supported event types and their payload.

## ​Email Events

  [email.bounced](https://resend.com/docs/webhooks/emails/bounced)Occurs whenever the recipient’s mail server **permanently rejected the
email**. [email.clicked](https://resend.com/docs/webhooks/emails/clicked)Occurs whenever the **recipient clicks on an email link**. [email.complained](https://resend.com/docs/webhooks/emails/complained)Occurs whenever the email was successfully **delivered, but the recipient
marked it as spam**. [email.delivered](https://resend.com/docs/webhooks/emails/delivered)Occurs whenever Resend **successfully delivered the email** to the
recipient’s mail server. [email.delivery_delayed](https://resend.com/docs/webhooks/emails/delivery-delayed)Occurs whenever the **email couldn’t be delivered due to a temporary
issue**. Delivery delays can occur, for example, when the recipient’s
inbox is full, or when the receiving email server experiences a transient
issue. [email.failed](https://resend.com/docs/webhooks/emails/failed)Occurs whenever the **email failed to send due to an error**. This event
is triggered when there are issues such as invalid recipients, API key
problems, domain verification issues, email quota limits, or other sending
failures. [email.opened](https://resend.com/docs/webhooks/emails/opened)Occurs whenever the **recipient opened the email**. [email.received](https://resend.com/docs/webhooks/emails/received)Occurs whenever Resend **successfully receives an email**. [email.scheduled](https://resend.com/docs/webhooks/emails/scheduled)Occurs whenever the **email is scheduled to be sent**. [email.sent](https://resend.com/docs/webhooks/emails/sent)Occurs whenever the **API request was successful**. Resend will attempt to
deliver the message to the recipient’s mail server. [email.suppressed](https://resend.com/docs/webhooks/emails/suppressed)Occurs whenever the **email is suppressed** by Resend.

## ​Domain Events

  [domain.created](https://resend.com/docs/webhooks/domains/created)Occurs when a **domain was successfully created**. [domain.updated](https://resend.com/docs/webhooks/domains/updated)Occurs when a **domain was successfully updated**. [domain.deleted](https://resend.com/docs/webhooks/domains/deleted)Occurs when a **domain was successfully deleted**.

## ​Contact Events

  [contact.created](https://resend.com/docs/webhooks/contacts/created)Occurs whenever a **contact was successfully created**.*Note: When importing multiple contacts using CSV, these events won’t be
triggered.Contact supportif you have any
questions.* [contact.updated](https://resend.com/docs/webhooks/contacts/updated)Occurs whenever a **contact was successfully updated**. [contact.deleted](https://resend.com/docs/webhooks/contacts/deleted)Occurs whenever a **contact was successfully deleted**.

---

# Webhook Ingester

> A self-hosted solution to store all your Resend webhook events in your own database.

The Resend Webhook Ingester is an open-source Next.js application that receives, verifies, and stores all your webhook events in your own database. Deploy it to your infrastructure and gain full control over your email event data. For more details on why you should store your webhook data, see the [data
storage guide](https://resend.com/docs/dashboard/webhooks/how-to-store-webhooks-data).

## ​Why use the Webhook Ingester?

 While you can build your own webhook handler, the Webhook Ingester provides a production-ready solution with:

- **Signature verification** using Svix to ensure webhook authenticity
- **Idempotent storage** that safely handles duplicate webhook deliveries
- **Multiple database support** including PostgreSQL, MySQL, MongoDB, and data warehouses
- **One-click deployment** to Vercel, Railway, or Render

 [GitHub RepositoryView the source code and contribute](https://github.com/resend/resend-webhooks-ingester)[Docker ImagePull the official Docker image](https://ghcr.io/resend/resend-webhooks-ingester)

## ​Deploy

 Get started in minutes with one-click deployment:    Or use Docker:

```
docker pull ghcr.io/resend/resend-webhooks-ingester
```

## ​Supported Databases

| Database | Endpoint | Best For |
| --- | --- | --- |
| Supabase | /supabase | Quick setup with managed Postgres |
| PostgreSQL | /postgresql | Self-hosted or managed Postgres (Neon, Railway, Render) |
| MySQL | /mysql | Self-hosted or managed MySQL |
| PlanetScale | /planetscale | Serverless MySQL |
| MongoDB | /mongodb | Document database (Atlas, self-hosted) |
| Snowflake | /snowflake | Data warehousing and analytics |
| BigQuery | /bigquery | Google Cloud analytics |
| ClickHouse | /clickhouse | High-performance analytics |

## ​Quick Start

 1

Clone and install

```
git clone https://github.com/resend/resend-webhooks-ingester.git
cd resend-webhooks-ingester
pnpm install
```

2

Configure environment variables

Copy the example environment file and add your credentials:

```
cp .env.example .env.local
```

At minimum, you need:.env.local

```
# Required: Your Resend webhook signing secret
RESEND_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxxxxxxxxxx

# Database credentials (example for PostgreSQL)
POSTGRESQL_URL=postgresql://user:password@host:5432/database
```

Get your webhook signing secret from the [Resend
Dashboard](https://resend.com/webhooks) when creating a webhook.3

Set up your database

Set up your database and run the provided schema for your database. The ingester supports PostgreSQL, MySQL, MongoDB, and several data warehouses. Schema files can be found in the `schemas/` directory.

```
pnpm db:setup --postgresql
# or use a different flag for a different database
```

4

Deploy and register webhook

Deploy to your preferred platform, then register your webhook endpoint in the [Resend Dashboard](https://resend.com/webhooks) and select all the events you’d like to store.Your endpoint URL will be: `https://your-domain.com/{connector}`For example: `https://your-app.vercel.app/postgresql`

## ​Database Schemas

 The ingester creates three tables to store webhook events:

| Table | Description |
| --- | --- |
| resend_wh_emails | All email events (sent, delivered, bounced, opened, clicked, etc.) |
| resend_wh_contacts | Contact events (created, updated, deleted) |
| resend_wh_domains | Domain events (created, updated, deleted) |

 Each table includes:

- `svix_id` - Unique webhook event ID for idempotency
- `event_type` - The type of event (e.g., `email.delivered`)
- `event_created_at` - When the event occurred
- `webhook_received_at` - When the webhook was received
- Event-specific fields (email details, bounce info, click data, etc.)

## ​Idempotency

 The ingester handles duplicate webhooks automatically. Each webhook includes a unique `svix-id` header, and the ingester uses this to ensure events are stored only once. If Resend retries a webhook delivery (due to a temporary failure), the duplicate will be safely ignored without creating duplicate records in your database.

## ​Configuration Reference

### ​Required Environment Variables

| Variable | Description |
| --- | --- |
| RESEND_WEBHOOK_SECRET | Your webhook signing secret from Resend |

### ​Database-Specific Variables

Supabase

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

PostgreSQL

```
POSTGRESQL_URL=postgresql://user:password@host:5432/database
```

MySQL

```
MYSQL_URL=mysql://user:password@host:3306/database
```

PlanetScale

```
PLANETSCALE_URL=mysql://username:password@host/database?ssl={"rejectUnauthorized":true}
```

MongoDB

```
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
MONGODB_DATABASE=resend_webhooks
```

Snowflake

```
SNOWFLAKE_ACCOUNT=your-account-identifier
SNOWFLAKE_USERNAME=your-username
SNOWFLAKE_PASSWORD=your-password
SNOWFLAKE_DATABASE=your-database
SNOWFLAKE_SCHEMA=your-schema
SNOWFLAKE_WAREHOUSE=your-warehouse
```

BigQuery

```
BIGQUERY_PROJECT_ID=your-project-id
BIGQUERY_DATASET_ID=your-dataset-id
BIGQUERY_CREDENTIALS={"type":"service_account","project_id":"..."}
```

ClickHouse

```
CLICKHOUSE_URL=https://your-instance.clickhouse.cloud:8443
CLICKHOUSE_USERNAME=default
CLICKHOUSE_PASSWORD=your-password
CLICKHOUSE_DATABASE=default
```

## ​Example Queries

 Once your data is stored, you can run analytics queries. Here’s an example to get email status counts by day:

```
SELECT
  DATE(event_created_at) AS day,
  event_type,
  COUNT(*) AS count
FROM resend_wh_emails
GROUP BY DATE(event_created_at), event_type
ORDER BY day DESC, event_type;
```

 See the
[queries_examples.md](https://github.com/resend/resend-webhooks-ingester/blob/main/queries_examples.md)
file in the repository for more analytics queries including bounce rates, open
rates, and click-through rates.

## ​Data Retention

 By default, webhook events are stored indefinitely. To implement data retention policies, you can set up scheduled jobs to delete old events. Example for PostgreSQL (delete events older than 90 days):

```
DELETE FROM resend_wh_emails
WHERE event_created_at < NOW() - INTERVAL '90 days';
```

 For Supabase, use
[pg_cron](https://supabase.com/docs/guides/database/extensions/pg_cron) to
schedule cleanup queries. For MongoDB, consider using [TTL
indexes](https://www.mongodb.com/docs/manual/core/index-ttl/) or [Atlas
scheduled
triggers](https://www.mongodb.com/docs/atlas/app-services/triggers/scheduled-triggers/).

## ​Troubleshooting

Webhook signature verification failing

- Ensure `RESEND_WEBHOOK_SECRET` matches the signing secret in your Resend
  Dashboard - Make sure you’re using the raw request body for verification -
  Check that the secret hasn’t been rotated in Resend

Database connection errors

- Verify your database credentials are correct - Check that the schema has
  been applied to your database - Ensure your database is accessible from your
  deployment (check firewall rules)

Webhooks not being received

- Verify your endpoint URL is publicly accessible - Check the webhook status
  in your [Resend Dashboard](https://resend.com/webhooks) - Ensure your server
  responds with HTTP 200 for successful requests

## ​Learn More

 [Webhook Event TypesView all available webhook event types and their payloads](https://resend.com/docs/webhooks/event-types)[Verify WebhooksLearn how webhook signature verification works](https://resend.com/docs/webhooks/verify-webhooks-requests)[Retries and ReplaysUnderstand webhook retry behavior](https://resend.com/docs/webhooks/retries-and-replays)[Storing Webhooks DataLearn why and how to store your webhook data](https://resend.com/docs/dashboard/webhooks/how-to-store-webhooks-data)

---

# Managing Webhooks

> Use webhooks to notify your application about events from Resend.

## ​What is a webhook?

 Resend uses webhooks, which are real-time HTTPS requests that tell your application an event occurred, such as an email delivery notification or subscription status update.

## ​Why use webhooks?

 All webhooks use HTTPS and deliver a JSON payload that can be used by your application. You can use webhook feeds to do things like:

- Automatically remove bounced email addresses from mailing lists
- Create alerts in your messaging or incident tools based on event types
- Store all send events in your own database for custom reporting/retention
- Receive emails using [Inbound](https://resend.com/docs/dashboard/receiving/introduction)

## ​How to receive webhooks

 To receive real-time events in your app via webhooks, follow these steps:

### ​1. Create a dev endpoint to receive requests.

 In your local application, create a new route that can accept POST requests. For example, you can add an API route: pages/api/webhooks.ts

```
export default (req, res) => {
  if (req.method === 'POST') {
    const event = req.body;
    console.log(event);
    res.status(200);
  }
};
```

 On receiving an event, you should respond with an `HTTP 200 OK` to signal to Resend that the event was successfully delivered. For development, you can create a tunnel to your localhost server using a tool like
[ngrok](https://ngrok.com/download) or [VS Code Port Forwarding](https://code.visualstudio.com/docs/debugtest/port-forwarding). These tools serve your local dev environment at a public URL you can use to test your local webhook endpoint.Example: `https://example123.ngrok.io/api/webhook`

### ​2. Add a webhook in Resend.

 Navigate to the [Webhooks page](https://resend.com/webhooks), then select **Add Webhook**.

1. Add your publicly accessible HTTPS URL
2. Select all events you want to observe

 ![Add Webhook](https://mintcdn.com/resend/Yj8a87v7gte2iMlD/images/dashboard-webhooks-add.jpg?fit=max&auto=format&n=Yj8a87v7gte2iMlD&q=85&s=222f2ef78900140d2d18bcaef4a925af) Resend also supports managing webhooks via the API or the SDKs. View the [API reference](https://resend.com/docs/api-reference/webhooks/create-webhook) for more details.

### ​3. Test your local endpoint.

 To ensure your endpoint is successfully receiving events, perform an event you are tracking with your webhook, like sending an email, creating a contact, or creating a domain. The webhook will send a JSON payload to your endpoint with the event details. For example:

```
{
  "type": "email.bounced",
  "created_at": "2024-11-22T23:41:12.126Z",
  "data": {
    "broadcast_id": "8b146471-e88e-4322-86af-016cd36fd216",
    "created_at": "2024-11-22T23:41:11.894719+00:00",
    "email_id": "56761188-7520-42d8-8898-ff6fc54ce618",
    "from": "Acme <onboarding@resend.dev>",
    "to": ["delivered@resend.dev"],
    "subject": "Sending this example",
    "template_id": "43f68331-0622-4e15-8202-246a0388854b",
    "bounce": {
      "message": "The recipient's email address is on the suppression list because it has a recent history of producing hard bounces.",
      "subType": "Suppressed",
      "type": "Permanent"
    },
    "tags": {
      "category": "confirm_email"
    }
  }
}
```

 You can also see the webhook details in the dashboard. ![Webhook Events List](https://mintcdn.com/resend/Yj8a87v7gte2iMlD/images/dashboard-webhook-events-list.png?fit=max&auto=format&n=Yj8a87v7gte2iMlD&q=85&s=c593c9b5e09e91d2d9eed3106aa0a81b) View all possible [event types and their webhook payload
responses](https://resend.com/docs/webhooks/event-types).

### ​4. Update and deploy your production endpoint.

 Once you successfully receive events, update your endpoint to process the events. For example, update your API route: pages/api/webhooks.ts

```
export default (req:, res) => {
  if (req.method === 'POST') {
    const event = req.body;
    if(event.type === "email.bounced"){
      //
    }
    res.status(200);
  }
};
```

 After you’re done testing, deploy your webhook endpoint to production.

### ​5. Register your production webhook endpoint

 Once your webhook endpoint is deployed to production, you can register it in the Resend dashboard.

## ​FAQ

What is the retry schedule?

If Resend does not receive a 200 response from a webhook server, we will retry the webhooks.Each message is attempted based on the following schedule, where each period is started following the failure of the preceding attempt:

- 5 seconds
- 5 minutes
- 30 minutes
- 2 hours
- 5 hours
- 10 hours

You can see when a message will be retried next in the webhook message details in the dashboard.

What IPs do webhooks POST from?

If your server requires an allowlist, our webhooks come from the following IP addresses:

- `44.228.126.217`
- `50.112.21.217`
- `52.24.126.164`
- `54.148.139.208`
- `2600:1f24:64:8000::/52`

Can I retry webhook events manually?

Yes. You can retry webhook events manually from the dashboard.To retry a webhook event, click to see your webhook details
and then click the link to the event you want to retry.On that page, you will see both the payload for the event
and a button to replay the webhook event and get it sent to
the configured webhook endpoint.

## ​Try it yourself

 [Webhook Code ExampleSee an example of how to receive webhooks events for Resend emails.](https://github.com/resend/resend-examples/tree/main/with-webhooks)

---

# Retries and Replays

> Learn how to use the retries and replays to handle webhook failures.

## ​Automatic Retries

 We attempt to deliver each webhook message based on a schedule with exponential backoff. Each message is attempted based on the following schedule, where each period is started following the failure of the preceding attempt:

- Immediately
- 5 seconds
- 5 minutes
- 30 minutes
- 2 hours
- 5 hours
- 10 hours
- 10 hours (in addition to the previous)

 If an endpoint is removed or disabled delivery attempts to the endpoint will be disabled as well. To see when a message will be retried next, check the webhook message details in the dashboard. For example, an attempt that fails three times before eventually succeeding will be delivered roughly 35 minutes and 5 seconds following the first attempt.

## ​Manual Replays

 If a webhook message fails, you can manually replay it. You can replay both `failed` and `succeeded` webhook messages. ![Replay Webhook](https://mintcdn.com/resend/qZ1nhePh39wY_UO4/images/webhooks-replay-1.jpg?fit=max&auto=format&n=qZ1nhePh39wY_UO4&q=85&s=aeae9936eeea92d71da580af9f82cbb5) Here’s how to replay a webhook message:

1. Go to the [Webhooks](https://resend.com/webhooks) page
2. Navigate to the Webhook Endpoint you are using
3. Go to the Webhook Message you want to replay
4. Click on the “Replay” button

---

# Verify Webhooks Requests

> Learn how to use the signing secret to verify your webhooks.

Webhook signing secrets are used to validate the payload data sent to your application from Resend. You can find the signing secret on the webhook details page. ![Signing Secret](https://mintcdn.com/resend/qZ1nhePh39wY_UO4/images/webhooks-secret-1.png?fit=max&auto=format&n=qZ1nhePh39wY_UO4&q=85&s=fa5955e5da08d6263850dfd024c642bb) Calls to [create](https://resend.com/docs/api-reference/webhooks/create-webhook), [retrieve](https://resend.com/docs/api-reference/webhooks/get-webhook), or [list](https://resend.com/docs/api-reference/webhooks/list-webhooks) webhooks will also return the signing secret in the response body. To verify the webhook request, you can use the Resend SDK, as in the example below. Make sure that you’re using the raw request body when verifying webhooks. The
cryptographic signature is sensitive to even the slightest change. Some
frameworks parse the request as JSON and then stringify it, and this will also
break the signature verification.

```
export async function POST(req: NextRequest) {
  try {
    const payload = await req.text();

    // Throws an error if the webhook is invalid
    // Otherwise, returns the parsed payload object
    const result = resend.webhooks.verify({
      payload,
      headers: {
        id: req.headers['svix-id'],
        timestamp: req.headers['svix-timestamp'],
        signature: req.headers['svix-signature'],
      },
      webhookSecret: process.env.RESEND_WEBHOOK_SECRET,
    });

    // Handle the result after validating it
  } catch {
    return new NextResponse('Invalid webhook', { status: 400 });
  }
}
```

 Alternatively, you can manually use the Svix libraries and manually pass it the headers, body, and webhook secret. [Learn more and view all supported languages here.](https://docs.svix.com/receiving/verifying-payloads/how) To verify manually, start by installing the Svix libaries.

```
npm install svix
```

 Then, verify the webhooks using the code below. The payload is the raw (string) body of the request, and the headers are the headers passed in the request.

```
import { Webhook } from 'svix';

const secret = process.env.WEBHOOK_SECRET;

// These were all sent from the server
const headers = {
  'svix-id': 'msg_p5jXN8AQM9LWM0D4loKWxJek',
  'svix-timestamp': '1614265330',
  'svix-signature': 'v1,g0hM9SsE+OTPJTGt/tmIKtSyZlE3uFJELVlNIOLJ1OE=',
};
const payload = '{"test": 2432232314}';

const wh = new Webhook(secret);
// Throws on error, returns the verified content on success
wh.verify(payload, headers);
```

 If you prefer, you can also [manually verify the headers as well.](https://docs.svix.com/receiving/verifying-payloads/how-manual)

## ​Why should I verify webhooks?

 Webhooks are vulnerable because attackers can send fake HTTP POST requests to endpoints, pretending to be legitimate services. This can lead to security risks or operational issues. To mitigate this, each webhook and its metadata are signed with a unique key specific to the endpoint. This signature helps verify the source of the webhook, allowing only authenticated webhooks to be processed. Another security concern is replay attacks, where intercepted valid payloads, complete with their signatures, are resent to endpoints. These payloads would pass the signature verification and be executed, posing a potential security threat.
