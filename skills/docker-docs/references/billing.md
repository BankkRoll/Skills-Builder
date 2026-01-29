# Use 3D Secure authentication for Docker billing and more

# Use 3D Secure authentication for Docker billing

> Docker billing supports 3D Secure (3DS) for secure payment authentication. Learn how 3DS works with Docker subscriptions.

# Use 3D Secure authentication for Docker billing

   Table of contents

---

Docker supports 3D Secure (3DS), an extra layer of authentication required
for certain credit card payments. If your bank or card issuer requires 3DS, you
may need to verify your identity before your payment can be completed.

## How it works

When a 3DS check is triggered during checkout, your bank or card issuer
may ask you to verify your identity. This can include:

- Entering a one-time password sent to your phone
- Approving the charge through your mobile banking app
- Answering a security question or using biometrics

The exact verification steps depend on your financial institution's
requirements.

## When you need to verify

You may be asked to verify your identity when performing any of the following
actions:

- Starting a [paid subscription](https://docs.docker.com/subscription/setup/)
- Changing your
  [billing cycle](https://docs.docker.com/billing/cycle/) from monthly to annual
- [Upgrading your subscription](https://docs.docker.com/subscription/change/)
- [Adding seats](https://docs.docker.com/subscription/manage-seats/) to an existing subscription

If 3DS is required and your payment method supports it, the verification prompt
will appear during checkout.

## Troubleshooting payment verification

If you're unable to complete your payment due to 3DS:

1. Retry your transaction. Make sure you're completing the verification
  prompt in the same browser tab.
2. Use a different payment method. Some cards may not support 3DS properly
  or be blocked.
3. Contact your bank. Your bank may be blocking the payment or the 3DS
  verification attempt.

> Note
>
> Disabling ad blockers or browser extensions that block pop-ups can help
> the 3DS prompt display correctly.

---

# Change your billing cycle

> Learn to change your billing cycle for your Docker subscription

# Change your billing cycle

   Table of contents

---

You can choose between a monthly or annual billing cycle when purchasing a
subscription. If you have a monthly billing cycle, you can choose to
switch to an annual billing cycle.

If you're on a monthly plan, you can switch to a yearly plan at any time.
However, switching from a yearly to a monthly cycle isn't supported.

When you change your billing cycle:

- Your next billing date reflects the new cycle. To find your next billing date,
  see [View renewal date](https://docs.docker.com/billing/history/#view-renewal-date).
- Your subscription's start date resets. For example, if the monthly
  subscription started on March 1 and ended on April 1, switching the billing
  duration on March 15, 2024, resets the new start date to March 15, 2024, with
  an end date of March 15, 2025.
- Any unused portion of your monthly subscription is prorated and applied as
  credit toward an annual subscription. For example, if your monthly cost is $10
  and you're used value is $5, when you switch to an annual cycle ($100), the
  final charge is $95 ($100-$5).

> Important
>
> For United States customers, Docker began collecting sales tax on July 1, 2024.
> For European customers, Docker began collecting VAT on March 1, 2025.
> For United Kingdom customers, Docker began collecting VAT on May 1, 2025.
>
>
>
> To ensure that tax assessments are correct, make sure that your
> [billing information](https://docs.docker.com/billing/details/) and VAT/Tax ID, if applicable, are
> updated. If you're exempt from sales tax, see
> [Register a tax certificate](https://docs.docker.com/billing/tax-certificate/).

## Change personal account to an annual cycle

> Important
>
> Pay by invoice is not available for subscription upgrades or changes.

To change your billing cycle:

1. Sign in to [Docker Home](https://app.docker.com/) and select
  your organization.
2. Select **Billing**.
3. On the plans and usage page, select **Switch to annual billing**.
4. Verify your billing information.
5. Select **Continue to payment**.
6. Verify payment information and select **Upgrade subscription**.

> Note
>
> If you choose to pay using a US bank account, you must verify the account. For
> more information, see
> [Verify a bank account](https://docs.docker.com/billing/payment-method/#verify-a-bank-account).

The billing plans and usage page will now reflect your new annual plan details.

Follow these steps to switch from a monthly to annual billing cycle for
a legacy Docker subscription:

1. Sign in to [Docker Hub](https://hub.docker.com).
2. Select your organization, then select **Billing**.
3. In the bottom-right of the **Plan** tab, select **Switch to annual billing**.
4. Review the information displayed on the **Change to an Annual subscription**
  page and select **Accept Terms and Purchase** to confirm.

## Change organization to an annual cycle

You must be an organization owner to make changes to the payment information.

> Important
>
> Pay by invoice is not available for subscription upgrades or changes.

Follow these steps to switch from a monthly to annual billing cycle for your
organization's Docker subscription:

1. Sign in to [Docker Home](https://app.docker.com/) and select
  your organization.
2. Select **Billing**.
3. On the plans and usage page, select **Switch to annual billing**.
4. Verify your billing information.
5. Select **Continue to payment**.
6. Verify payment information and select **Upgrade subscription**.

> Note
>
> If you choose to pay using a US bank account, you must verify the account. For
> more information, see
> [Verify a bank account](https://docs.docker.com/billing/payment-method/#verify-a-bank-account).

Follow these steps to switch from a monthly to annual billing cycle for a
legacy Docker organization subscription:

1. Sign in to [Docker Hub](https://hub.docker.com).
2. Select your organization, then select **Billing**.
3. Select **Switch to annual billing**.
4. Review the information displayed on the **Change to an Annual subscription**
  page and select **Accept Terms and Purchase** to confirm.

---

# Manage your billing information

> Learn how to update your billing information in Docker Hub

# Manage your billing information

   Table of contents

---

You can update the billing information for your personal account or for an
organization. When you update your billing information, these changes apply to
future billing invoices. The email address you provide for a billing account is
where Docker sends all invoices and other billing related communications.

> Note
>
> Existing invoices, whether paid or unpaid, cannot be updated.
> Changes only apply to future invoices.

> Important
>
> For United States customers, Docker began collecting sales tax on July 1, 2024.
> For European customers, Docker began collecting VAT on March 1, 2025.
> For United Kingdom customers, Docker began collecting VAT on May 1, 2025.
>
>
>
> To ensure that tax assessments are correct, make sure that your
> [billing information](https://docs.docker.com/billing/details/) and VAT/Tax ID, if applicable, are
> updated. If you're exempt from sales tax, see
> [Register a tax certificate](https://docs.docker.com/billing/tax-certificate/).

## Manage billing information

### Personal account

To update your billing information:

1. Sign in to [Docker Home](https://app.docker.com/) and select your
  organization.
2. Select **Billing**.
3. Select **Billing information** from the left-hand navigation.
4. On your billing information card, select **Change**.
5. Update your billing contact and billing address information.
6. Optional. To add or update a VAT ID, select the **I'm purchasing as a business** checkbox and enter your Tax ID.
  > Important
  >
  > Your VAT number must include your country prefix. For example, if you are
  > entering a VAT number for Germany, you would enter `DE123456789`.
7. Select **Update**.

To update your billing information:

1. Sign in to [Docker Hub](https://hub.docker.com).
2. Select your organization, then select **Billing**.
3. Select **Billing Address** and enter your updated billing information.
4. Optional. To add or update a VAT ID, enter your **Tax ID/VAT**.
  > Important
  >
  > Your VAT number must include your country prefix. For example, if you are
  > entering a VAT number for Germany, you would enter `DE123456789`.
5. Select **Submit**.

### Organization

> Note
>
> You must be an organization owner to make changes to the billing information.

To update your billing information:

1. Sign in to [Docker Home](https://app.docker.com/) and select your
  organization.
2. Select **Billing**.
3. Select **Billing information** from the left-hand navigation.
4. On your billing information card, select **Change**.
5. Update your billing contact and billing address information.
6. Optional. To add or update a VAT ID, select the **I'm purchasing as a business** checkbox and enter your Tax ID.
  > Important
  >
  > Your VAT number must include your country prefix. For example, if you are
  > entering a VAT number for Germany, you would enter `DE123456789`.
7. Select **Update**.

To update your billing information:

1. Sign in to [Docker Hub](https://hub.docker.com).
2. Select your organization, then select **Billing**.
3. Select **Billing Address**.
4. Optional. To add or update a VAT ID, enter your **Tax ID/VAT**.
  > Important
  >
  > Your VAT number must include your country prefix. For example, if you are
  > entering a VAT number for Germany, you would enter `DE123456789`.
5. Select **Submit**.

## Update your billing email address

Docker sends the following billing-related emails:

- Confirmations (new subscriptions, paid invoices)
- Notifications (card failure, card expiration)
- Reminders (subscription renewal)

You can update the email address that receives billing invoices at any time.

### Personal account

To update your billing email address:

1. Sign in to [Docker Home](https://app.docker.com/) and select your
  organization.
2. Select **Billing**.
3. Select **Billing information** from the left-hand navigation.
4. On your billing information card, select **Change**.
5. Update your billing contact information and select **Update**.

To update your billing email address:

1. Sign in to [Docker Hub](https://hub.docker.com).
2. Select your organization, then select **Billing**.
3. Select **Billing Address**.
4. Update the email address in the **Billing contact** section.
5. Select **Submit**.

### Organizations

To update your billing email address:

1. Sign in to [Docker Home](https://app.docker.com/) and select
  your organization.
2. Select **Billing**.
3. Select **Billing information** from the left-hand navigation.
4. On your billing information card, select **Change**.
5. Update your billing contact information and select **Update**.

To update your billing email address:

1. Sign in to [Docker Hub](https://hub.docker.com).
2. Select your organization, then select **Billing**.
3. Select the name of the organization.
4. Select **Billing Address**.
5. Update the email address in the **Billing contact** section.
6. Select **Submit**.

---

# Billing FAQs

> Frequently asked questions related to billing

# Billing FAQs

   Table of contents

---

### What happens if my subscription payment fails?

If your subscription payment fails, there is a grace period of 15 days,
including the due date. Docker retries to collect the payment 3 times using the
following schedule:

- 3 days after the due date
- 5 days after the previous attempt
- 7 days after the previous attempt

Docker also sends an email notification
`Action Required - Credit Card Payment Failed` with an attached unpaid invoice
after each failed payment attempt.

Once the grace period is over and the invoice is still not paid, the
subscription downgrades to a free subscription and all paid features are
disabled.

### Can I manually retry a failed payment?

No. Docker retries failed payments on a
[retry schedule](https://docs.docker.com/billing/faqs/#what-happens-if-my-subscription-payment-fails).

To ensure a retired payment is successful, verify your default payment is
updated. If you need to update your default payment method, see
[Manage payment method](https://docs.docker.com/billing/payment-method/#manage-payment-method).

### Does Docker collect sales tax and/or VAT?

Docker collects sales tax and/or VAT from the following:

- For United States customers, Docker began collecting sales tax on July 1, 2024.
- For European customers, Docker began collecting VAT on March 1, 2025.
- For United Kingdom customers, Docker began collecting VAT on May 1, 2025.

To ensure that tax assessments are correct, make sure that your billing
information and VAT/Tax ID, if applicable, are updated. See
[Update the billing information](https://docs.docker.com/billing/details/).

If you're exempt from sales tax, see
[Register a tax certificate](https://docs.docker.com/billing/tax-certificate/).

### Does Docker offer academic pricing?

For academic pricing, contact the
[Docker Sales Team](https://www.docker.com/company/contact).

### Can I use pay by invoice for upgrades or additional seats?

No. Pay by invoice is only available for renewing annual subscriptions, not for
purchasing upgrades or additional seats. You must use card payment or US bank
accounts for these changes.

For a list of supported payment methods, see
[Add or update a payment method](https://docs.docker.com/billing/payment-method/).

---

# Invoices and billing history

> Learn how to view invoices and your billing history

# Invoices and billing history

   Table of contents

---

Learn how to view and pay invoices, view your billing history, and verify
your billing renewal date. All monthly and annual subscriptions are
automatically renewed at the end of the subscription term using your default
payment method.

> Important
>
> For United States customers, Docker began collecting sales tax on July 1, 2024.
> For European customers, Docker began collecting VAT on March 1, 2025.
> For United Kingdom customers, Docker began collecting VAT on May 1, 2025.
>
>
>
> To ensure that tax assessments are correct, make sure that your
> [billing information](https://docs.docker.com/billing/details/) and VAT/Tax ID, if applicable, are
> updated. If you're exempt from sales tax, see
> [Register a tax certificate](https://docs.docker.com/billing/tax-certificate/).

## View an invoice

Your invoice includes the following:

- Invoice number
- Date of issue
- Due date
- Your "Bill to" information
- Amount due (in USD)
- Pay online: Select this link to pay your invoice online
- Description of your order, quantity if applicable, unit price, and
  amount (in USD)
- Subtotal, discount (if applicable), and total

The information listed in the "Bill to" section of your invoice is based on
your billing information. Not all fields are required. The billing information
includes the following:

- Name (required): The name of the administrator or company
- Address (required)
- Email address (required): The email address that receives all billing-related
  emails for the account
- Phone number
- Tax ID or VAT

You can’t make changes to a paid or unpaid billing invoice. When you update
your billing information, this change won't update an existing invoice.

If you need
to update your billing information, make sure you do so before your
subscription renewal date when your invoice is finalized.

For more information, see [Update billing information](https://docs.docker.com/billing/details/).

## Pay an invoice

> Note
>
> Pay by invoice is only available for subscribers on an annual billing cycle.
> To change your billing cycle, see
> [Change your billing cycle](https://docs.docker.com/billing/cycle/).

If you've selected pay by invoice for your subscription, you'll receive email
reminders to pay your invoice at 10 days before the due date, on the due date,
and 15 days after the due date.

You can pay an invoice from the Docker Billing Console:

1. Sign in to [Docker Home](https://app.docker.com/) and choose your organization.
2. Select **Billing**.
3. Select **Invoices** and locate the invoice you want to pay.
4. In the **Actions** column, select **Pay invoice**.
5. Fill out your payment details and select **Pay**.

When your payment has processed, the invoice's **Status** column will update to
**Paid** and you will receive a confirmation email.

If you choose to pay using a US bank account, you must verify the account. For
more information, see [Verify a bank account](https://docs.docker.com/billing/payment-method/#verify-a-bank-account).

### View renewal date

You receive your invoice when the subscription renews. To verify your renewal
date, sign in to the [Docker Home Billing](https://app.docker.com/billing).
Your renewal date and amount are displayed on your subscription plan card.

You receive your invoice when the subscription renews. To verify your renewal
date:

1. Sign in to [Docker Hub](https://hub.docker.com).
2. Select your user avatar to open the drop-down menu.
3. Select **Billing**.
4. Select the user or organization account to view the billing details. Here
  you can find your renewal date and the renewal amount.

## Include your VAT number on your invoice

> Note
>
> If the VAT number field is not available, complete the
> [Contact Support form](https://hub.docker.com/support/contact/). This field
> may need to be manually added.

To add or update your VAT number:

1. Sign in to [Docker Home](https://app.docker.com/) and choose your
  organization.
2. Select **Billing**.
3. Select **Billing information** from the left-hand menu.
4. Select **Change** on your billing information card.
5. Ensure the **I'm purchasing as a business** checkbox is checked.
6. Enter your VAT number in the Tax ID section.
  > Important
  >
  > Your VAT number must include your country prefix. For example, if you are
  > entering a VAT number for Germany, you would enter `DE123456789`.
7. Select **Update**.

Your VAT number will be included on your next invoice.

To add or update your VAT number:

1. Sign in to [Docker Hub](https://hub.docker.com).
2. Select your organization, then select **Billing**.
3. Select the **Billing address** link.
4. In the **Billing Information** section, select **Update information**.
5. Enter your VAT number in the Tax ID section.
  > Important
  >
  > Your VAT number must include your country prefix. For example, if you are
  > entering a VAT number for Germany, you would enter `DE123456789`.
6. Select **Save**.

Your VAT number will be included on your next invoice.

## View billing history

You can view your billing history and download past invoices for a personal
account or organization.

### Personal account

To view billing history:

1. Sign in to [Docker Home](https://app.docker.com/) and choose your
  organization.
2. Select **Billing**.
3. Select **Invoices** from the left-hand menu.
4. Optional. Select the **Invoice number** to open invoice details.
5. Optional. Select the **Download** button to download an invoice.

To view billing history:

1. Sign in to [Docker Hub](https://hub.docker.com).
2. Select your organization, then select **Billing**.
3. Select the **Payment methods and billing history** link.

You can find your past invoices in the **Invoice History** section, where
you can download an invoice.

### Organization

You must be an owner of the organization to view the billing history.

To view billing history:

1. Sign in to [Docker Home](https://app.docker.com/) and select your
  organization.
2. Select **Billing**.
3. Select **Invoices** from the left-hand menu.
4. Optional. Select the **invoice number** to open invoice details.
5. Optional. Select the **download** button to download an invoice.

To view billing history:

1. Sign in to [Docker Hub](https://hub.docker.com).
2. Select your organization, then select **Billing**.
3. Select the **Payment methods and billing history** link.

You can find your past invoices in the **Invoice History** section, where you
can download an invoice.

---

# Add or update a payment method

> Learn how to add or update a payment method in Docker Hub

# Add or update a payment method

   Table of contents

---

This page describes how to add or update a payment method for your personal
account or for an organization.

You can add a payment method or update your account's existing payment method
at any time.

> Important
>
> If you want to remove all payment methods, you must first downgrade your
> subscription to a free subscription. See [Downgrade](https://docs.docker.com/subscription/change/).

The following payment methods are supported:

- Cards
  - Visa
  - MasterCard
  - American Express
  - Discover
  - JCB
  - Diners
  - UnionPay
- Wallets
  - Stripe Link
- Bank accounts
  - Automated Clearing House (ACH) transfer with a
    [verified](https://docs.docker.com/billing/payment-method/#verify-a-bank-account) US
    bank account
- [Pay by invoice](https://docs.docker.com/billing/history/)

All charges are in United States dollars (USD).

> Important
>
> For United States customers, Docker began collecting sales tax on July 1, 2024.
> For European customers, Docker began collecting VAT on March 1, 2025.
> For United Kingdom customers, Docker began collecting VAT on May 1, 2025.
>
>
>
> To ensure that tax assessments are correct, make sure that your
> [billing information](https://docs.docker.com/billing/details/) and VAT/Tax ID, if applicable, are
> updated. If you're exempt from sales tax, see
> [Register a tax certificate](https://docs.docker.com/billing/tax-certificate/).

## Manage payment method

### Personal account

To add a payment method:

1. Sign in to [Docker Home](https://app.docker.com/) and select your
  organization.
2. Select **Billing**.
3. Select **Payment methods** from the left-hand menu.
4. Select **Add payment method**.
5. Enter your new payment information:
  - Add a card:
    - Select **Card** and fill out the card information form.
  - Add a Link payment:
    - Select **Secure, 1-click checkout with Link** and enter your
      Link **email address** and **phone number**.
    - If you don't already use Link, you must fill out the card information
      form to store a card for Link payments.
  - Add a bank account:
    - Select **US bank account**.
    - Verify your **Email** and **Full name**.
    - If your bank is listed, select your bank's name.
    - If your bank is not listed, select **Search for your bank**.
    - To verify your bank account, see
      [Verify a bank account](https://docs.docker.com/billing/payment-method/#verify-a-bank-account).
6. Select **Add payment method**.
7. Optional. You can set a new default payment method by selecting
  the **Set as default** action.
8. Optional. You can remove non-default payment methods by selecting
  the **Delete** action.

> Note
>
> If you want to set a US bank account as your default payment method, you must
> [verify the account](#verify-a-bank-account) first.

To add a payment method:

1. Sign in to [Docker Hub](https://hub.docker.com).
2. Select **Billing**.
3. Select the **Payment methods** link.
4. Select **Add payment method**.
5. Enter your new payment information:
  - Add a card:
    - Select **Card** and fill out the card information form.
  - Add a Link payment:
    - Select **Secure, 1-click checkout with Link** and enter your
      Link **email address** and **phone number**.
    - If you are not an existing Link customer, you must fill out the
      card information form to store a card for Link payments.
6. Select **Add**.
7. Select the **Actions** icon, then select **Make default** to ensure that
  your new payment method applies to all purchases and subscriptions.
8. Optional. You can remove non-default payment methods by selecting
  the **Actions** icon. Then, select **Delete**.

### Organization

> Note
>
> You must be an organization owner to make changes to the payment information.

To add a payment method:

1. Sign in to [Docker Home](https://app.docker.com/) and select your
  organization.
2. Select **Billing**.
3. Select **Payment methods** from the left-hand menu.
4. Select **Add payment method**.
5. Enter your new payment information:
  - Add a card:
    - Select **Card** and fill out the card information form.
  - Add a Link payment:
    - Select **Secure, 1-click checkout with Link** and enter your
      Link **email address** and **phone number**.
    - If you are not an existing Link customer, you must fill out the
      card information form to store a card for Link payments.
  - Add a bank account:
    - Select **US bank account**.
    - Verify your **Email** and **Full name**.
    - If your bank is listed, select your bank's name.
    - If your bank is not listed, select **Search for your bank**.
    - To verify your bank account, see [Verify a bank account](https://docs.docker.com/billing/payment-method/#verify-a-bank-account).
6. Select **Add payment method**.
7. Optional. You can set a new default payment method by selecting
  the **Set as default** action.
8. Optional. You can remove non-default payment methods by selecting
  the **Delete** action.

> Note
>
> If you want to set a US bank account as your default payment method, you must
> verify the account first.

To add a payment method:

1. Sign in to [Docker Hub](https://hub.docker.com).
2. Select your organization, then select **Billing**.
3. Select the **Payment methods** link.
4. Select **Add payment method**.
5. Enter your new payment information:
  - Add a card:
    - Select **Card** and fill out the card information form.
  - Add a Link payment:
    - Select **Secure, 1-click checkout with Link** and enter your
      Link **email address** and **phone number**.
    - If you are not an existing Link customer, you must fill out the
      card information form to store a card for Link payments.
6. Select **Add payment method**.
7. Select the **Actions** icon, then select **Make default** to ensure that
  your new payment method applies to all purchases and subscriptions.
8. Optional. You can remove non-default payment methods by selecting
  the **Actions** icon. Then, select **Delete**.

## Enable pay by invoice

Subscription: Team  Business

Pay by invoice is available for Teams and Business customers with annual
subscriptions, starting with your first renewal. When you select this
payment method, you'll pay upfront for your first subscription period using a
payment card or ACH bank transfer.

At renewal time, instead of automatic payment, you'll receive an invoice via
email that you must pay manually. Pay by invoice is not available for
subscription upgrades or changes.

1. Sign in to [Docker Home](https://app.docker.com/) and select your
  organization.
2. Select **Billing**.
3. Select **Payment methods**, then **Pay by invoice**.
4. To enable pay by invoice, select the toggle.
5. Confirm your billing contact details. If you need to change them, select
  **Change** and enter your new details.

## Verify a bank account

There are two ways to verify a bank account as a payment method:

- Instant verification: Docker supports several major banks for instant
  verification.
- Manual verification: All other banks must be verified manually.

### Instant verification

To verify your bank account instantly, you must sign in to your bank account
from the Docker billing flow:

1. Choose **US bank account** as your payment method.
2. Verify your **Email** and **Full name**.
3. If your bank is listed, select your bank's name or
  select **Search for your bank**.
4. Sign in to your bank and review the terms and conditions. This agreement
  allows Docker to debit payments from your connected bank account.
5. Select **Agree and continue**.
6. Select an account to link and verify, and select **Connect account**.

When the account is verified, you will see a success message in the pop-up
modal.

### Manual verification

To verify your bank account manually, you must enter the micro-deposit amount
from your bank statement:

1. Choose **US bank account** as your payment method.
2. Verify your **Email** and **First and last name**.
3. Select **Enter bank details manually instead**.
4. Enter your bank details: **Routing number** and **Account number**.
5. Select **Submit**.
6. You will receive an email with instructions on how to manually verify.

Manual verification uses micro-deposits. You’ll see a small deposit
(such as $0.01) in your bank account within 1–2 business days. Open your manual
verification email and enter the amount of this deposit to verify your account.

## Failed payments

> Note
>
> You can't manually retry a failed payment. Docker will retry failed payments
> based on the retry schedule.

If your subscription payment fails, there is a grace period of 15 days,
including the due date. Docker retries to collect the payment 3 times using the
following schedule:

- 3 days after the due date
- 5 days after the previous attempt
- 7 days after the previous attempt

Docker also sends an email notification
`Action Required - Credit Card Payment Failed` with an attached unpaid invoice
after each failed payment attempt.

Once the grace period is over and the invoice is still not paid, the
subscription downgrades to a free subscription and all paid features are
disabled.

---

# Submit a tax exemption certificate

> Learn how to submit a tax exemption or VAT certificate for Docker billing.

# Submit a tax exemption certificate

   Table of contents

---

If you're a customer in the United States and are exempt from sales tax, you
can submit a valid tax exemption certificate to Docker Support.

If you're a global customer subject to VAT, make sure to include your
[VAT number](https://docs.docker.com/billing/history/#include-your-vat-number-on-your-invoice)
along with your country prefix when you update your billing profile.

> Important
>
> For United States customers, Docker began collecting sales tax on July 1, 2024.
> For European customers, Docker began collecting VAT on March 1, 2025.
> For United Kingdom customers, Docker began collecting VAT on May 1, 2025.
>
>
>
> To ensure that tax assessments are correct, make sure that your
> [billing information](https://docs.docker.com/billing/details/) and VAT/Tax ID, if applicable, are
> updated. If you're exempt from sales tax, see
> [Register a tax certificate](https://docs.docker.com/billing/tax-certificate/).

## Prerequisites

Before submitting your certificate:

- The customer name must match the name on the certificate.
- The certificate must list Docker Inc. as the Seller or Vendor, with all
  relevant fields completed.
- The certificate must be signed, dated, and not expired.
- You must include the Docker ID or namespace(s) for all accounts to
  apply the certificate to.

> Important
>
> You can use the same certificate for multiple namespaces, if applicable.

## Contact information

Use the following contact information on your certificate:

Docker, Inc.
3790 El Camino Real #1052
Palo Alto, CA 94306
(415) 941-0376

## Register a tax certificate

1. [Submit a Docker Support ticket](https://hub.docker.com/support/contact?topic=Billing&subtopic=Tax%20information) to initiate the process to register a tax certificate.
2. Enter **Tax certificate** as the support ticket **Subject**.
3. In the **Details** field, enter **Submitting a tax certificate**.
4. Instructions will populate on how to submit a tax certificate.
5. Fill out all required fields on the support form.
6. In the file upload section, add the tax certificate by dragging and dropping
  the file, or selecting **Browse files**.
7. Select **Submit**.

Docker's support team will reach out to you if any additional information is
required. You'll receive an e-mail confirmation from Docker once your tax
exemption status is applied to your account.
