# Introduction and more

# Introduction

> Visualize all the API Keys on the Resend Dashboard.

## ​What is an API Key

 API Keys are secret tokens used to authenticate your requests. They are unique to your account and should be kept confidential.

## ​Add API Key

 You can create a new API Key from the [API Key Dashboard](https://resend.com/api-keys).

1. Click **Create API Key**.
2. Give your API Key a name (maximum 50 characters).
3. Select **Full access** or **Sending access** as the permission.
4. If you select **Sending access**, you can choose the domain you want to restrict access to.

 ![Add API Key](https://mintcdn.com/resend/ABWmVTZIHGIFNTFD/images/dashboard-api-keys-add.png?fit=max&auto=format&n=ABWmVTZIHGIFNTFD&q=85&s=1ecfaf7a2d2a780b826f941078e427b5) For security reasons, you can only view the API Key once. Learn more about
[API key best practices](https://resend.com/docs/knowledge-base/how-to-handle-api-keys).

## ​Set API Key permissions

 There are two different permissions of API Keys:

1. **Full access**: grants access to create, delete, get, and update any resource.
2. **Sending access**: grants access only to send emails.

 With API Key permissions, you can isolate different application actions to different API Keys. Using multiple keys, you can view logs per key, detect possible abuse, and control the damage that may be done accidentally or maliciously.

## ​View all API Keys

 The [API Dashboard](https://resend.com/api-keys) shows you all the API Keys you have created along with their details, including the **last time you used** an API Key. Different color indicators let you quickly scan and detect which API Keys are being used and which are not. ![View All API Keys](https://mintcdn.com/resend/ABWmVTZIHGIFNTFD/images/dashboard-api-keys-view-all.jpg?fit=max&auto=format&n=ABWmVTZIHGIFNTFD&q=85&s=f195ef7f60a110407e2739f30c10ca2a)

## ​Edit API Key details

 After creating an API Key, you can edit the following details:

- Name
- Permission
- Domain

 To edit an API Key, click the **More options**  button and then **Edit API Key**. ![View Inactive API Key](https://mintcdn.com/resend/ABWmVTZIHGIFNTFD/images/dashboard-api-keys-edit.jpeg?fit=max&auto=format&n=ABWmVTZIHGIFNTFD&q=85&s=7abe8e055cf311a7f66a40477db7946a) You cannot edit an API Key value after it has been created.

## ​Delete inactive API Keys

 If an API Key **hasn’t been used in the last 30 days**, consider deleting it to keep your account secure. ![View Inactive API Key](https://mintcdn.com/resend/ABWmVTZIHGIFNTFD/images/dashboard-api-keys-view-inactive.jpg?fit=max&auto=format&n=ABWmVTZIHGIFNTFD&q=85&s=fa99650454696902100e03b669d3a9c1) You can delete an API Key by clicking the **More options**  button and then **Remove API Key**. ![Delete API Key](https://mintcdn.com/resend/ABWmVTZIHGIFNTFD/images/dashboard-api-keys-remove.jpeg?fit=max&auto=format&n=ABWmVTZIHGIFNTFD&q=85&s=9fc76ff5dc4cd38f465539cd3a435706)

## ​View API Key logs

 When visualizing an active API Key, you can see the **total number of requests** made to the key. For more detailed logging information, select the underlined number of requests to view all logs for that API Key. ![View Active API Key](https://mintcdn.com/resend/ABWmVTZIHGIFNTFD/images/dashboard-api-keys-view-active.jpg?fit=max&auto=format&n=ABWmVTZIHGIFNTFD&q=85&s=e0c0584545565e1e78e460b240d2c221)

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

# Managing Contacts

> Learn how to work with Contacts with Resend.

Contacts in Resend are global entities linked to a specific email address. After adding Contacts, send [Broadcasts](https://resend.com/docs/dashboard/broadcasts/introduction) to groups of Contacts. If you previously used our Audience model, learn how to [migrate to the new
Contacts model](https://resend.com/docs/dashboard/segments/migrating-from-audiences-to-segments).

## ​Add Contacts

 You can add a Contact in three different ways: via API, CSV upload, or manually.

### ​1. Add Contacts programmatically via API

 You can add contacts programmatically using the [contacts](https://resend.com/docs/api-reference/contacts/create-contact) endpoint.

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

resend.contacts.create({
  email: 'steve.wozniak@gmail.com',
  firstName: 'Steve',
  lastName: 'Wozniak',
});
```

 When creating a Contact, you can optionally set the following properties:

- `first_name`: The first name of the contact.
- `last_name`: The last name of the contact.
- `unsubscribed`: Whether the contact is unsubscribed from all Broadcasts.
- `properties`: A map of custom property keys and values to create (learn more about [custom properties](https://resend.com/docs/dashboard/audiences/properties)).

 Once a Contact is created, you can update it using the [update contact](https://resend.com/docs/api-reference/contacts/update-contact) endpoint or [add the contact to a Segment](https://resend.com/docs/api-reference/contacts/add-contact-to-segment).

### ​2. Add Contacts by uploading a .csv

 You can also add Contacts by uploading a .csv file. This is a convenient way to add multiple Contacts at once.

1. Go to the [Contacts](https://resend.com/audience) page, and select **Add Contacts**.
2. Select **Import CSV**.
3. Upload your CSV file from your computer.
4. Map the fields you want to use. You can map the fields to: `email`, `first_name`, `last_name`, and `unsubscribed`, or any Contact properties you’ve already created.
5. Optionally add the contacts to an existing Segment.
6. Select **Continue**, review the contacts, and finish the upload.

### ​3. Add Contacts manually

1. Go to the [Contacts](https://resend.com/audience) page, and select **Add Contacts**.
2. Select **Add Manually**.
3. Add the email address of the contact in the text field (separated by commas or new lines for multiple contacts).
4. Optionally add the contact to an existing Segment.
5. Confirm and click **Add**.

## ​Contact Properties

 Contact Properties can be used to store additional information about your Contacts and then personalize your Broadcasts. ![Properties](https://mintcdn.com/resend/2SHIfycCcJlAJEpt/images/contact-properties.png?fit=max&auto=format&n=2SHIfycCcJlAJEpt&q=85&s=6eb917dc7ac58dd515c033cf443e0734) Resend includes a few default properties:

- `first_name`: The first name of the contact.
- `last_name`: The last name of the contact.
- `unsubscribed`: Whether the contact is unsubscribed from all Broadcasts.
- `email`: The email address of the contact.

 You can create additional custom Contact Properties for your Contacts to store additional information. These properties can be used to personalize your Broadcasts across all Segments. Learn more about [Contact Properties](https://resend.com/docs/dashboard/audiences/properties).

## ​View Contacts

 You can view your Contacts in the [Contacts](https://resend.com/audience) page.

1. Go to the [Contacts](https://resend.com/audience) page.
2. Click on the Contact you want to view.
3. View the Contact details.

 Each Contact includes the metadata associated with the contact, as well as a full history of all marketing interactions with the Contact. ![View Contact](https://mintcdn.com/resend/fJVhfUIq0WYU6NCn/images/contacts-view.png?fit=max&auto=format&n=fJVhfUIq0WYU6NCn&q=85&s=7d9d97f84af0603a528dd841a4f77637) You can also retrieve a [single Contact](https://resend.com/docs/api-reference/contacts/get-contact) or [list all Contacts](https://resend.com/docs/api-reference/contacts/list-contacts) via the API or SDKs.

## ​Edit Contacts

1. Go to the [Contacts](https://resend.com/audience) page.
2. Click on the **More options**  button and then **Edit Contact**.
3. Edit the Contact details and choose **Save**.

 You can edit any Contact property (excluding the email address), assign
the Contact to a [Segment](https://resend.com/docs/dashboard/segments/introduction) or [Topic](https://resend.com/docs/dashboard/topics/introduction), or unsubscribe the Contact from all Broadcasts. You can also [update a Contact](https://resend.com/docs/api-reference/contacts/update-contact) via the API or SDKs using the `id` or `email` of the Contact.

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

## ​Bulk Actions

 You can perform actions on multiple Contacts at once by selecting them from the [Contacts](https://resend.com/audience) page.

1. Go to the [Contacts](https://resend.com/audience) page.
2. Select multiple Contacts by clicking the checkbox next to each Contact.
3. Click the **Edit** button in the bulk actions bar.
4. Choose an action:
  - **Add to segments**: Add the selected Contacts to one or more Segments.
  - **Subscribe to topics**: Subscribe the selected Contacts to one or more Topics.

 You can also delete multiple Contacts at once by clicking the **Delete** button in the bulk actions bar.

## ​Delete Contacts

1. Go to the [Contacts](https://resend.com/audience) page.
2. Click on the **More options**  button and then **Delete Contact**.
3. Confirm the deletion.

 You can also [delete a Contact](https://resend.com/docs/api-reference/contacts/delete-contact) via the API or SDKs.

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

---

# Your Resend Audience

> Learn how to manage your Contacts and send personalized Broadcasts to them.

The [Audience Page](https://resend.com/audience) is for your marketing Broadcasts and provides tools for managing your Contacts and sending personalized Broadcasts to them. [Broadcasts](https://resend.com/docs/dashboard/broadcasts/introduction) also handle all your unsubscribe flows for you automatically. The Audience page includes four areas:

- [Contacts](#contacts): individual email addresses
- [Properties](#properties): custom properties for your Contacts
- [Segments](#segments): groups of Contacts for your organization
- [Topics](#topics): user-facing tools for managing email preferences

 ![Contacts](https://mintcdn.com/resend/2SHIfycCcJlAJEpt/images/audiences-contacts-intro.png?fit=max&auto=format&n=2SHIfycCcJlAJEpt&q=85&s=82101b2b495815ad50f8b7eb823876bd)

## ​Contacts

 Contacts in Resend are global entities linked to a specific email address. ![Properties](https://mintcdn.com/resend/2SHIfycCcJlAJEpt/images/audiences-properties-intro.png?fit=max&auto=format&n=2SHIfycCcJlAJEpt&q=85&s=001cb276f96ad54b6a64042eada0c9c3) Each Contact:

- is associated with a single email address
- can have custom properties
- can be in zero, one or multiple Segments
- can be opted in or out of Topics

 Each Contact shows a history of all marketing interactions with the Contact. Learn more about [Contacts](https://resend.com/docs/dashboard/audiences/contacts).

## ​Properties

 Contact Properties can be used to store additional information about your Contacts and then personalize your Broadcasts. ![Properties](https://mintcdn.com/resend/2SHIfycCcJlAJEpt/images/contact-properties.png?fit=max&auto=format&n=2SHIfycCcJlAJEpt&q=85&s=6eb917dc7ac58dd515c033cf443e0734) Resend includes a few default properties:

- `first_name`: The first name of the contact.
- `last_name`: The last name of the contact.
- `unsubscribed`: Whether the contact is unsubscribed from all Broadcasts.
- `email`: The email address of the contact.

 You can create additional custom Contact Properties for your Contacts to store additional information. These properties can be used to personalize your Broadcasts across all Segments. Learn more about [Contact Properties](https://resend.com/docs/dashboard/audiences/properties).

## ​Segments

 Segments are groups of Contacts for your organization. You can use Segments to send emails to a specific group of Contacts using [Broadcasts](https://resend.com/docs/dashboard/broadcasts/introduction). ![Segment](https://mintcdn.com/resend/2SHIfycCcJlAJEpt/images/audiences-intro-segment.png?fit=max&auto=format&n=2SHIfycCcJlAJEpt&q=85&s=550570d03d1b5611a89e5dddeadf79f9) Learn more about [Segments](https://resend.com/docs/dashboard/segments/introduction).

## ​Topics

 Topics are user-facing tools for managing email preferences. You can use them to manage your Contacts’ email preferences. ![Topics](https://mintcdn.com/resend/m2xttJpF68pi6Mw0/images/audience-topics-intro.png?fit=max&auto=format&n=m2xttJpF68pi6Mw0&q=85&s=0530a26f226771b486012abe36e9970a) When you send [Broadcasts](https://resend.com/docs/dashboard/broadcasts/introduction), you can optionally scope sending to a particular Topic. Not only does scoping your sending help you send more precisely, but it also allows your users to manage their preferences with more control. Learn more about [Topics](https://resend.com/docs/dashboard/topics/introduction). You can [customize your unsubscribe page with your
branding](https://resend.com/docs/dashboard/settings/unsubscribe-page) from your team settings.

---

# Managing Unsubscribed Contacts

> Learn how to check and remove recipients who have unsubscribed to your marketing emails.

It’s essential to update your Contact list when someone unsubscribes to maintain a good sender reputation. Benefits of managing your unsubscribe list:

- reduces the likelihood of your emails being marked as spam
- improves deliverability for any other marketing or transactional emails you send

 When you include an [an unsubscribe link in your Broadcasts](https://resend.com/docs/dashboard/segments/introduction#automatic-unsubscribes), Resend will automatically handle the unsubscribe flow for you.

## ​Unsubscribe Statuses

 The Contacts page shows the global unsubscribe status of each Contact. ![Unsubscribe Statuses](https://mintcdn.com/resend/2SHIfycCcJlAJEpt/images/audiences-contacts-intro.png?fit=max&auto=format&n=2SHIfycCcJlAJEpt&q=85&s=82101b2b495815ad50f8b7eb823876bd)

- **Unsubscribed**: the Contact has unsubscribed from all emails from your account.
- **Subscribed**: the Contact is subscribed to at least one Topic.

 To filter by Status, click on the **All Statuses** filter next to the search bar, then select a value.

## ​Topic Subscription Statuses

 You can view the subscription status of each Topic for a given Contact by clicking on the Contact’s row. ![Topic Subscription Statuses](https://mintcdn.com/resend/m2xttJpF68pi6Mw0/images/audiences-contacts-topics.png?fit=max&auto=format&n=m2xttJpF68pi6Mw0&q=85&s=56b25853b46fec447005f7aab32796fa)

- **Subscribed**: the global subscription status for the Contact.
- **Topics**: the list of Topics the Contact is subscribed to.

 You can also check a Contact’s Topic subscription status [via the API or SDKs](https://resend.com/docs/api-reference/contacts/get-contact-topics).

## ​Updating a Topic Subscription for a Contact

 You can update a Topic subscription for a Contact by clicking the **Edit** button in the Topic’s row. ![Add Contact to Topic](https://mintcdn.com/resend/WTZjpSkJsZf7Ubl_/images/dashboard-save-contact-topic.png?fit=max&auto=format&n=WTZjpSkJsZf7Ubl_&q=85&s=66e212d282f450c371f42a1b214029cd) You can also update a Topic subscription for a Contact [via the API or SDKs](https://resend.com/docs/api-reference/contacts/update-contact-topics).

### ​Bulk Subscribe to Topics

 You can subscribe multiple Contacts to Topics at once:

1. Go to the [Contacts](https://resend.com/audience) page.
2. Select multiple Contacts by clicking the checkbox next to each Contact.
3. Click the **Edit** button in the bulk actions bar.
4. Select **Subscribe to topics**.
5. Choose the Topics you want to subscribe the Contacts to.
6. Click **Subscribe**.

 Learn more about [bulk actions for Contacts](https://resend.com/docs/dashboard/audiences/contacts#bulk-actions).

---

# Contact Properties

> Learn how to work with Contact Properties with Resend.

Contact Properties can be used to store additional information about your Contacts and then personalize your Broadcasts. Resend includes a few default properties:

- `first_name`: The first name of the contact.
- `last_name`: The last name of the contact.
- `unsubscribed`: Whether the contact is unsubscribed from all Broadcasts.
- `email`: The email address of the contact.

## ​Add Custom Contact Properties

 You can create additional custom Contact Properties for your Contacts to store additional information. These properties can be used to personalize your Broadcasts across all Segments. Each Contact Property has a key, a value, and optional fallback value.

- `key`: The key of the property (must be alphanumeric and underscore only, max `50` characters).
- `value`: The value of the property (may be a `string` or `number`).
- `fallback_value`: The fallback value of the property (must match the type of the property).

  You can also create Contact Properties [via the API or SDKs](https://resend.com/docs/api-reference/contact-properties/create-contact-property).

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.contactProperties.create({
  key: 'company_name',
  type: 'string',
  fallbackValue: 'Acme Corp',
});
```

## ​Add Properties to a Contact

 When you create a Contact Property you can provide a fallback value. This value will be used whenever you don’t provide a custom value for a Contact. To provide a custom value for a Contact, you can use the dashboard:

1. Go to the [Contacts](https://resend.com/audience) page.
2. Click the **more options**  button and then **Edit Contact**.
3. Add the property key and value.
4. Click on the **Save** button.

  You can also add properties to a Contact when you [create a Contact](https://resend.com/docs/api-reference/contacts/create-contact).

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

const { data, error } = await resend.contacts.create({
  email: '[email protected]',
  firstName: 'Steve',
  lastName: 'Wozniak',
  unsubscribed: false,
  properties: {
    company_name: 'Acme Corp',
  },
});
```

 Or you can update a Contact to add or change a property value [using the update contact endpoint](https://resend.com/docs/api-reference/contacts/update-contact).

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

// Update by contact id
const { data, error } = await resend.contacts.update({
  id: 'e169aa45-1ecf-4183-9955-b1499d5701d3',
  properties: {
    company_name: 'Acme Corp',
  },
});

// Update by contact email
const { data, error } = await resend.contacts.update({
  email: '[email protected]',
  properties: {
    company_name: 'Acme Corp',
  },
});
```

 When you create or update a Contact with properties, the properties are added to the Contact, but only if the property key already exists and the value type is valid. You can [list all Contact Properties](https://resend.com/docs/api-reference/contact-properties/list-contact-properties) to see all available properties.

What happens if the properties don't exist?

If the properties don’t exist, they are not added to the Contact and the
call fails. An error is returned.

Property keys are case sensitive, right?

Yes, property keys are case sensitive. If you create a property with a key
of “company_name”, you cannot use “CompanyName” or “company_Name” in your
Contacts.

What happens if the value isn't the right type?

If the value isn’t the right type, the property value is not added to the
Contact and the call fails. An error is returned.

## ​Use Contact Properties in Broadcasts

 You can use Contact Properties in your Broadcasts to personalize your emails.  You can also use Contact Properties in your Broadcast HTML and Text content when you [create a Broadcast using the API or SDKs](https://resend.com/docs/api-reference/broadcasts/create-broadcast).

---

# Managing Broadcasts

> Send marketing emails efficiently without code.

Broadcasts allow you to send email blasts to your customers using a no-code editor on Resend, or from our [Broadcast API](https://resend.com/docs/api-reference/broadcasts/create-broadcast). You can use this to send email blasts such as:

- Newsletters
- Product Launches
- Investor Updates
- Promotions
- Changelogs

## ​Sending a Broadcast from Resend

 Our Broadcasts feature was made to enable your entire team to send email campaigns without having to ask for help from developers.

### ​No-Code Editor

### ​Markdown Support

 You can also write your emails using Markdown. This works with headings, lists, italic, bold, links, and quotes. You can easily copy and paste content from applications like Notion, Google Docs, iA Writter and many others maintaining formatting consistency.

### ​Custom Styling

 You can customize the look and feel of your email by changing **global styles** such as the background color, link color, and container size, allowing you to create emails aligned with your brand identity. To do this, click on **Styles** at the top left of the Broadcast editor. You can edit specific images or lines of texts by selecting or highlighting them prior to clicking on **Styles**.  You can also edit individual styles for each component, including the font size, font weight, and text alignment. You can also set custom properties for each component, such as image alt, button links, and social links,

### ​Personalize your content

 When creating broadcasts, you can include dynamic audience data to personalize the email content.

- `{{{FIRST_NAME|fallback}}}`
- `{{{LAST_NAME|fallback}}}`
- `{{{EMAIL}}}`
- `{{{RESEND_UNSUBSCRIBE_URL}}}`

 When you include the `{{{RESEND_UNSUBSCRIBE_URL}}}` placeholder in the call, Resend includes an unsubscribe link in the email to automatically handle unsubscribe requests. Learn how to create a [custom Unsubscribe
Page](https://resend.com/docs/dashboard/settings/unsubscribe-page).

### ​Testing & Sending

 Once you’re finished writing your email, you can preview it in your personal inbox or send it to your team for feedback. To do this, click on **Test Email** on the top right of your screen. Enter in the email address you’d like to send your email to, and then click on **Send Test Email** to complete. Once you’re ready to send your email to your Audience, click on **Send**, and slide to confirm.  **Note**: Test emails do not include any custom Reply-To address that may have been configured. This behavior is limited to test mode and does not affect actual email sends.

## ​Sending a Broadcast from the Broadcast API

 We also offer the option to send your Broadcasts from our [Broadcast API](https://resend.com/docs/api-reference/broadcasts/create-broadcast). The Broadcast API offers 6 endpoints for programmatically creating, updating, and sending broadcasts.

## ​Understand broadcast statuses

 Here are all the statuses that can be associated with a broadcast:

- `draft` - The broadcast is a draft (note: if a broadcast is scheduled, it will be in the `draft` status until the scheduled time).
- `sent` - The broadcast was sent.
- `queued` - The broadcast is queued for delivery.

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

# Performance Tracking

> Track your Broadcasts email performance in real-time

Once your broadcast is sent, you can track its performance right away. The insights you can view are emails delivered, unsubscribed, click rate, and open rate. You can view these insights by clicking on [Broadcast](https://resend.com/broadcasts) in the left column, and then clicking on the Broadcast that you want to view.  Please note, at times, open rates can be inaccurate for a number of reasons due to the way inbox providers handle incoming emails. You can [read more about this here.](https://resend.com/docs/knowledge-base/why-are-my-open-rates-not-accurate)

---

# Implementing BIMI

> Set up BIMI to gain brand recognition by displaying your logo in the inbox.

## ​Prerequisites

 To get the most out of this guide, you will need to:

- Establish verifiable use of your logo
  - Obtain a registered trademark for your logo
  - Or, use your logo for over one year
- [Add a DMARC record on your domain](https://resend.com/docs/dashboard/domains/dmarc)

## ​What is BIMI?

 BIMI ([Brand Indicators for Message Identification](https://bimigroup.org/)) is a standard that allows you to specify a logo (and sometimes a checkmark) to display next to your email in the inbox. These indicators can increase brand recognition and trust and improve engagement. ![bimi-example](https://mintcdn.com/resend/ABWmVTZIHGIFNTFD/images/bimi-example.png?fit=max&auto=format&n=ABWmVTZIHGIFNTFD&q=85&s=7cad76755f1a51e03465d90d413df055) Though this standard is newer, most major mailbox providers now support it. This gives BIMI adoption a competitive edge for brand recognition in the inbox. Most mailbox providers show brand indicators for those who purchase a certificate, of which there are two types: a Common Mark Certificate (CMC) and a Verified Mark Certificate (VMC). Here’s an overview of current email client support:

| Client | BIMI w/a CMC | BIMI w/a VMC | BIMI w/out a VMC or CMC |
| --- | --- | --- | --- |
| Apple Mail | X | ✓ | X |
| Gmail | ✓ | ✓ | X |
| Outlook | X | X | X |
| Yahoo | ✓ | ✓ | ✓ |

## ​Implementing BIMI

### ​1. Configure DMARC

 If you haven’t set up DMARC yet, follow our [DMARC Setup
Guide](https://resend.com/docs/dashboard/domains/dmarc). BIMI requires a DMARC policy of `p=quarantine;` or `p=reject;`. This policy assures that your emails are properly authenticated and that no one else can spoof your domain and send them with your logo. Here’s an overview of the required parameters:

| Parameter | Purpose | Required Value |
| --- | --- | --- |
| p | Policy | p=quarantine;orp=reject; |
| pct | Percentage | pct=100; |

 Here is an example of an adequate DMARC record:

```
"v=DMARC1; p=quarantine; pct=100; rua=mailto:dmarcreports@example.com"
```

 For BIMI on a subdomain, the root or APEX domain must also have a DMARC policy
of `p=quarantine` or `p=reject` in addition to the subdomain. If not, the
subdomain will not be compliant to display a BIMI logo.

### ​2. Establish verifiable use of your logo

 To display your logo in most email clients using BIMI, you need to prove ownership of your logo by obtaining a mark certificate. This process is similar to acquiring an SSL certificate for your website. You can purchase a mark certificate from one of the following [authorized mark verifying authorities](https://bimigroup.org/vmc-issuers/):

- [DigiCert](https://www.digicert.com/tls-ssl/verified-mark-certificates)
- [GlobalSign](https://www.globalsign.com/)
- [SSL.com](https://www.ssl.com/)

 There are two possible mark Certificate’s to verify the use of your logo:

- **Verified Mark Certificate (VMC)**: A certificate issued by a Certificate Authority (CA) that is used to verify that you are the owner of the logo you are trying to display. A VMC is available if you have a trademark of your logo. With a VMC, Gmail will display a blue checkmark.
- **Common Mark Certificate (CMC)**: A certificate also issued by Certificate Authority (CA) to verify you. A CMC is available to you if you can establish that you’ve used your logo for one year. Currently, only Gmail supports a CMC.

 A VMC offers the widest email client support, though the barrier of a trademark means a CMC is an easier path if you have established use of your logo for one year. Here are a some things to know before starting the certificate purchase process:

- If you don’t hold a trademark for your logo or have not used your logo for a year, you will not be able to purchase a certificate.
- The process could take weeks, so start early and respond to their requests quickly.
- You will need to provide a [SVG Tiny P/S formatted logo](https://bimigroup.org/creating-bimi-svg-logo-files/).
- You will need to prove you own the domain by adding a DNS record.
- You will need to prove you are the owner of the trademark or logo by providing identification.
- You will need publicly available proof that your business exists. For newer startups, recommend [Yellow Pages](https://marketing.yellowpages.com/en/) or [Google Business Profiles](https://support.google.com/business/answer/3039617?hl=en) as the easiest method for proving your existence

## ​3. Set your BIMI DNS Record

 Once you have your VMC, you can set your BIMI DNS record. This TXT record points to the location of your VMC and your logo.

| Name | Type | Value |
| --- | --- | --- |
| default._bimi | TXT | v=BIMI1; l=link_to_logo; a=link_to_certificate; |

 Here is an example of a BIMI record:

```
v=BIMI1; l=https://vmc.digicert.com/00-00.svg; a=https://vmc.digicert.com/00-00.pem;
```

 Ensure your logo uses an HTTPS URL. Mailbox providers will not display the
logo if served from an HTTP URL. It contains a publicly and programmatically accessible link to your verified logo (.svg) and a link to your VMC (.pem). To confirm that your BIMI record is published correctly, the [BIMI working group offers a tool](https://bimigroup.org/bimi-generator/) to check it. It often takes a few days for your logo to display in inboxes after this record propagates. Mailbox providers will also conditionally decide to show the logo based on the domain’s sending email volume and reputation. A domain with a high spam or bounce rate may not have their avatar displayed.

## ​Reference

| Parameter | Purpose | Example |
| --- | --- | --- |
| v | The version of BIMI | v=BIMI1 |
| l | Logo | l=https://vmc.digicert.com/00-00.svg |
| a | Certificate | a=https://vmc.digicert.com/00-00.pem |
| s | Selector | s=springlogo |

 The BIMI standard allows for multiple logos using the [selector
parameter](https://bimigroup.org/how-and-why-to-implement-bimi-selectors/). Having issues setting up BIMI? [We can help](https://resend.com/help).

---

# Implementing DMARC

> Implement DMARC to build trust in your domain and protect against email spoofing and unauthorized use of your domain in email messages.

Implement DMARC to build trust in your domain and protect against email spoofing and unauthorized use of your domain in email messages.

---

# Managing Domains

> Visualize all the domains on the Resend Dashboard.

Domain not verifying? [Try
this](https://resend.com/docs/knowledge-base/what-if-my-domain-is-not-verifying).

## ​Verifying a domain

 Resend sends emails using a domain you own. We recommend using subdomains (e.g., `updates.yourdomain.com`) to isolate your sending reputation and communicate your intent. Learn more about [using subdomains](https://resend.com/docs/knowledge-base/is-it-better-to-send-emails-from-a-subdomain-or-the-root-domain). In order to verify a domain, you must set two DNS entries:

1. [SPF](#what-are-spf-records): list of IP addresses authorized to send email on behalf of your domain
2. [DKIM](#what-are-dkim-records): public key used to verify email authenticity

 These two DNS entries grant Resend permission to send email on your behalf. Once SPF and DKIM verify, you can optionally add a [DMARC record](https://resend.com/docs/dashboard/domains/dmarc) to build additional trust with mailbox providers. Resend requires you own your domain (i.e., not a shared or public domain).

## ​View domain details

 The [Domains dashboard](https://resend.com/domains) shows information about your domain name, its verification status, and history. ![Domain Details](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=feb6b86344d63199055cdaa7b15735fa) Need specific help with a provider? View our [knowledge base DNS
Guides](https://resend.com/docs/knowledge-base).

## ​What are SPF records

 Sender Policy Framework (SPF) is an email authentication standard that allows you to list all the IP addresses that are authorized to send email on behalf of your domain. The SPF configuration is made of a TXT record that lists the IP addresses approved by the domain owner. It also includes a MX record that allows the recipient to send bounce and complaint feedback to your domain. ![SPF Records](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-spf.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=630f500feba7768e05a69340e8a6dae5)

## ​Custom Return Path

 By default, Resend will use the `send` subdomain for the Return-Path address. You can change this by setting the optional `custom_return_path` parameter when [creating a domain](https://resend.com/docs/api-reference/domains/create-domain) via the API or under **Advanced options** in the dashboard. ![Custom Return Path](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-custom-return-path.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=569a75fc160aad18116efc93bcebe148) For the API, optionally pass the custom return path parameter.

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

resend.domains.create({ name: 'example.com', customReturnPath: 'outbound' });
```

 Custom return paths must adhere to the following rules:

- Must be 63 characters or less
- Must start with a letter, end with a letter or number, and contain only letters, numbers, and hyphens

 Avoid setting values that could undermine credibility (e.g. `testing`), as they may be exposed to recipients in some email clients.

## ​What are DKIM records

 DomainKeys Identified Mail (DKIM) is an email security standard designed to make sure that an email that claims to have come from a specific domain was indeed authorized by the owner of that domain. The DKIM configuration is made of a TXT record that contains a public key that is used to verify the authenticity of the email. ![DKIM Records](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-resend-dkim.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=345d1dc6b7c138dbd92bd6928c634bd9)

## ​Understand a domain status

 Domains can have different statuses, including:

- `not_started`: You’ve added a domain to Resend, but you haven’t clicked on `Verify DNS Records` yet.
- `pending`: Resend is still trying to verify the domain.
- `verified`: Your domain is successfully verified for sending in Resend.
- `failed`: Resend was unable to detect the DNS records within 72 hours.
- `temporary_failure`: For a previously verified domain, Resend will periodically check for the DNS record required for verification. If at some point, Resend is unable to detect the record, the status would change to “Temporary Failure”. Resend will recheck for the DNS record for 72 hours, and if it’s unable to detect the record, the domain status would change to “Failure”. If it’s able to detect the record, the domain status would change to “Verified”.

## ​Open and Click Tracking

 Open and click tracking is disabled by default for all domains. You can enable it by clicking on the toggles within the domain settings. ![Open and Click Tracking](https://mintcdn.com/resend/JHWt09hsc7E33HK2/images/dashboard-domains-open-and-click-tracking.png?fit=max&auto=format&n=JHWt09hsc7E33HK2&q=85&s=b753867f46e27a252b8d8d8a93a3fedb) For best deliverability, we recommend disabling click and open tracking [for
sensitive transactional
emails](https://resend.com/docs/dashboard/emails/deliverability-insights#disable-click-tracking).

## ​How Open Tracking Works

 A 1x1 pixel transparent GIF image is inserted in each email and includes a unique reference to this image file. When the image is downloaded, Resend can tell exactly which message was opened and by whom.

## ​How Click Tracking Works

 To track clicks, Resend modifies each link in the body of the HTML email. When recipients open a link, they are sent to a Resend server, and are immediately redirected to the URL destination.

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

# Choosing a Region

> Resend offers sending from multiple regions

Resend users have the option to send transactional and marketing emails from four different regions:

- North Virginia (us-east-1)
- Ireland (eu-west-1)
- São Paulo (sa-east-1)
- Tokyo (ap-northeast-1)

 No matter where your users are, you can ensure that they receive your emails in a timely and efficient manner. You can visualize the different regions in the Resend dashboard: ![Multi Region Domains](https://mintcdn.com/resend/OWNnQaVDyqcGyhhN/images/multi-region-1.png?fit=max&auto=format&n=OWNnQaVDyqcGyhhN&q=85&s=0572cd0780bdcfc50ad558666dd8d7a5)

## ​Why is this important?

 Especially for transactional emails like magic links, password resets, and welcome messages, users expect to receive them right away. If they don’t, they might not be able to access your service right away, which could be a missed opportunity for your organization. Here are some of the other benefits of using our multi-region email sending feature:

1. **Faster delivery:** By sending emails from the region closest to your user, you can reduce latency and ensure a faster time-to-inbox. This can be the difference between people using/buying your product or not.
2. **Easier account management:** Instead of having to maintain different accounts for each region, we’re providing multi-region within the same account. That way, you aren’t juggling different login credentials.
3. **Increased resilience:** In case of disruption in one region, our multi-region feature enables you to send emails from a backup domain in a separate region, guaranteeing maximum uptime.

## ​Get Started

 To start using our multi-region email sending feature, go to **Domains**, then select the option to add a new domain. Finally, select the region you want to send your emails.

## ​How to set up multi-region for the same domain

 For advanced needs, you can set up multiple regions for the same domain. We recommend setting a unique subdomain for each region (e.g., us.domain.com, eu.domain.com). When sending transactional emails or marketing emails, choose the right domain for your users.

## ​Changing Domain Region

 If you’d like to switch the region your domain is currently set to:

1. Delete your current domain in the [Domain’s page](https://resend.com/domains).
2. Add the same domain again, selecting the new region.
3. Update your DNS records to point to the new domain.

 For more help, please reach out to [Support](https://resend.com/help), and we can help you out.

---

# Add an unsubscribe link to transactional emails

> Learn how to give email recipients the ability to unsubscribe without searching for the unsubscribe link.

Learn how to give email recipients the ability to unsubscribe without searching for the unsubscribe link.

---

# Attachments

> Send emails with attachments.

There are two ways to send attachments:

1. [From a remote file](#send-attachments-from-a-remote-file)
2. [From a local file](#send-attachments-from-a-local-file)

 We currently do not support sending attachments [when using our batch
endpoint](https://resend.com/docs/api-reference/emails/send-batch-emails).

## ​Send attachments from a remote file

 Include the `path` parameter to send attachments from a remote file. This parameter accepts a URL to the file you want to attach. Define the file name that will be attached using the `filename` parameter.

```
import { Resend } from 'resend';

const resend = new Resend('re_xxxxxxxxx');

await resend.emails.send({
  from: 'Acme <onboarding@resend.dev>',
  to: ['delivered@resend.dev'],
  subject: 'Receipt for your payment',
  html: '<p>Thanks for the payment</p>',
  attachments: [
    {
      path: 'https://resend.com/static/sample/invoice.pdf',
      filename: 'invoice.pdf',
    },
  ],
});
```

## ​Send attachments from a local file

 Include the `content` parameter to send attachments from a local file. This parameter accepts the Base64 encoded content of the file you want to attach. Define the file name that will be attached using the `filename` parameter.

```
import { Resend } from 'resend';
import fs from 'fs';

const resend = new Resend('re_xxxxxxxxx');

const filepath = `${__dirname}/static/invoice.pdf`;
const attachment = fs.readFileSync(filepath).toString('base64');

await resend.emails.send({
  from: 'Acme <onboarding@resend.dev>',
  to: ['delivered@resend.dev'],
  subject: 'Receipt for your payment',
  text: '<p>Thanks for the payment</p>',
  attachments: [
    {
      content: attachment,
      filename: 'invoice.pdf',
    },
  ],
});
```

## ​Embed Images using CID

 You can optionally embed an image in the HTML body of the email. Both remote and local attachments are supported. All attachment requirements, options, and limitations apply to embedded inline images as well. Embedding images requires two steps: **1. Add the CID in the email HTML.** Use the prefix `cid:` to reference the ID in the `src` attribute of an image tag in the HTML body of the email.

```
<img src="cid:logo-image" />
```

 **2. Reference the CID in the attachment** The content id is an arbitrary string set by you, and must be less than 128 characters.

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

 Learn more about [embedding images](https://resend.com/docs/dashboard/emails/embed-inline-images).

## ​View and Download Attachments

 You can view and download attachments when viewing a sent email that includes them. To view and download attachments:

1. Go to [Emails](https://resend.com/emails).
2. Navigate to any email you sent with an attachment.
3. Click on the attachment to download it locally.

 Attachments include the filename and an icon to help you identify the type of attachment. We show unique icons for each attachment type:

- Image
- PDF
- Spreadsheet
- Default (for unknown types)

## ​Attachment Limitations

- Emails can be no larger than 40MB (including attachments after Base64 encoding).
- Not all file types are supported. See the list of [unsupported file types](https://resend.com/docs/knowledge-base/what-attachment-types-are-not-supported).
- Emails with attachments cannot be sent using our [batching endpoint](https://resend.com/docs/api-reference/emails/send-batch-emails).

## ​Examples

 [Attachments with Next.js (remote file)See the full source code.](https://github.com/resend/resend-examples/tree/main/with-attachments)[Attachments with Next.js (local file)See the full source code.](https://github.com/resend/resend-examples/tree/main/with-attachments-content)
