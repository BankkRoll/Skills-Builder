# Send emails with Phoenix and more

# Send emails with Phoenix

> Learn how to send your first email using Phoenix and the Resend Elixir SDK.

This guides utilizes an [open source
library](https://github.com/elixir-saas/resend-elixir) contributed by a
community member. It’s not developed, maintained, or supported by Resend
directly.

## ​Prerequisites

 To get the most out of this guide, you’ll need to:

- [Create an API key](https://resend.com/api-keys)
- [Verify your domain](https://resend.com/domains)

## ​1. Install

 Install by adding `resend` to your list of dependencies in `mix.exs`:

```
def deps do
  [
    {:resend, "~> 0.4.5"}
  ]
end
```

## ​2. Send email using Swoosh

 This library includes a Swoosh adapter to make using Resend with a new Phoenix project as easy as possible. All you have to do is configure your Mailer:

```
config :my_app, MyApp.Mailer,
  adapter: Resend.Swoosh.Adapter,
  api_key: System.fetch_env!("RESEND_API_KEY")
```

 If you’re configuring your app for production, configure your adapter in `prod.exs`, and your API key from the environment in `runtime.exs`:

```
config :my_app, MyApp.Mailer, adapter: Resend.Swoosh.Adapter
```

## ​3. Try it yourself

 [Phoenix ExampleSee the full source code.](https://github.com/resend/resend-phoenix-example)

---

# Send emails with PHP

> Learn how to send your first email using the Resend PHP SDK.

## ​Prerequisites

 To get the most out of this guide, you will need to:

- [Create an API key](https://resend.com/api-keys)
- [Verify your domain](https://resend.com/domains)

 Prefer watching a video? Check out this video walkthrough below.

## ​1. Install

 Get the Resend PHP SDK. Composer

```
composer require resend/resend-php
```

## ​2. Send email using HTML

 The easiest way to send an email is by using the `html` parameter. index.php

```
<?php

require __DIR__ . '/vendor/autoload.php';

$resend = Resend::client('re_xxxxxxxxx');

$resend->emails->send([
  'from' => 'Acme <onboarding@resend.dev>',
  'to' => ['delivered@resend.dev'],
  'subject' => 'hello world',
  'html' => '<strong>it works!</strong>',
]);
```

## ​3. Try it yourself

 [PHP ExampleSee the full source code.](https://github.com/resend/resend-php-example)

---

# Send emails using PHPMailer with SMTP

> Learn how to send your first email using PHPMailer with SMTP.

## ​Prerequisites

 To get the most out of this guide, you’ll need to:

- [Create an API key](https://resend.com/api-keys)
- [Verify your domain](https://resend.com/domains)

## ​1. Install

 Get the [PHPMailer](https://github.com/PHPMailer/PHPMailer) package.

```
composer require phpmailer/phpmailer
```

## ​2. Send email using SMTP

 When configuring your SMTP integration, you’ll need to use the following credentials:

- **Host**: `smtp.resend.com`
- **Port**: `587`
- **Username**: `resend`
- **Password**: `YOUR_API_KEY`

 Then use these credentials to send with PHPMailer:

```
<?php

// Include Composer autoload file to load PHPMailer classes
require __DIR__ . '/vendor/autoload.php';

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

$mail = new PHPMailer(true);

try {
    $mail->isSMTP();
    $mail->Host = 'smtp.resend.com';
    $mail->SMTPAuth = true;
    $mail->Username = 'resend';
    $mail->Password = 're_xxxxxxxxx';
    $mail->SMTPSecure = 'tls';
    $mail->Port = 587;

    // Set email format to HTML
    $mail->isHTML(true);

    $mail->setFrom('onboarding@resend.dev');
    $mail->addAddress('delivered@resend.dev');
    $mail->Subject = 'Hello World';
    $mail->Body = '<strong>It works!</strong>';

    $mail->send();

    // Log the successfully sent message
    echo 'Email successfully sent';
} catch (Exception $e) {
    // Log the detailed error for debugging
    error_log('Mailer Error: ' . $mail->ErrorInfo);
    // Show a generic error message to the user
    echo 'There was an error sending the email.';
}
```

## ​3. Try it yourself

 [PHPMailer SMTP ExampleSee the full source code.](https://github.com/resend/resend-phpmailer-smtp-example)

---

# Send emails with Python

> Learn how to send your first email using the Resend Python SDK.

## ​Prerequisites

 To get the most out of this guide, you’ll need to:

- [Create an API key](https://resend.com/api-keys)
- [Verify your domain](https://resend.com/domains)

## ​1. Install

 Get the Resend Python SDK.

```
pip install resend
```

## ​2. Send email using HTML

 The easiest way to send an email is by using the `html` parameter. index.py

```
import os
import resend

resend.api_key = os.environ["RESEND_API_KEY"]

params: resend.Emails.SendParams = {
    "from": "Acme <onboarding@resend.dev>",
    "to": ["delivered@resend.dev"],
    "subject": "hello world",
    "html": "<strong>it works!</strong>",
}

email = resend.Emails.send(params)
print(email)
```

## ​3. Try it yourself

 [Python ExampleSee the full source code.](https://github.com/resend/resend-python-example)

---

# Send emails using Rails with SMTP

> Learn how to integrate Rails with Resend SMTP.

## ​Prerequisites

 To get the most out of this guide, you’ll need to:

- [Create an API key](https://resend.com/api-keys)
- [Verify your domain](https://resend.com/domains)

## ​1. Setup your environment

 Add these lines of code into your environment config file. config/environments/environment.rb

```
config.action_mailer.delivery_method = :smtp
config.action_mailer.smtp_settings = {
  :address   => 'smtp.resend.com',
  :port      => 465,
  :user_name => 'resend',
  :password  => ENV['RESEND_API_KEY'],
  :tls => true
}
```

## ​2. Send email using Rails Action Mailer

 Then create a `UserMailer` class definition. app/mailers/user_mailer.rb

```
class UserMailer < ApplicationMailer
  default from: 'Acme <[email protected]>' # this domain must be verified with Resend
  def welcome_email
    @user = params[:user]
    @url = 'http://example.com/login'
    mail(to: ["[email protected]"], subject: 'hello world')
  end
end
```

 And create your ERB email template. app/views/user_mailer/welcome_email.html.erb

```
<!doctype html>
<html>
  <head>
    <meta content="text/html; charset=UTF-8" http-equiv="Content-Type" />
  </head>
  <body>
    <h1>Welcome to example.com, <%= @user.name %></h1>
    <p>You have successfully signed up to example.com,</p>
    <p>To log in to the site, just follow this link: <%= @url %>.</p>
    <p>Thanks for joining and have a great day!</p>
  </body>
</html>
```

 Initialize your `UserMailer` class. This should return a `UserMailer` instance.

```
u = User.new name: "derich"
mailer = UserMailer.with(user: u).welcome_email

# => #<Mail::Message:153700, Multipart: false, Headers: <From: [email protected]>, <To: [email protected]>, <Subject: hello world>, <Mime-Version: 1.0>...
```

 Finally, you can now send emails using the `deliver_now!` method:

```
mailer.deliver_now!

# => {:id=>"a193c81e-9ac5-4708-a569-5caf14220539", :from=>....}
```

## ​3. Try it yourself

 [Rails SMTP ExampleSee the full source code.](https://github.com/resend/resend-rails-smtp-example)

---

# Send emails with Rails

> Learn how to send your first email using Rails and the Resend Ruby SDK.

## ​Prerequisites

 To get the most out of this guide, you’ll need to:

- [Create an API key](https://resend.com/api-keys)
- [Verify your domain](https://resend.com/domains)

## ​1. Install

 Get the Resend Ruby SDK.

```
gem install resend
```

## ​2. Send email using Rails Action Mailer

 This gem can be used as an Action Mailer delivery method. First, let’s update or create your mailer initializer file with your Resend API Key. config/initializers/mailer.rb

```
Resend.api_key = "re_xxxxxxxxx"
```

 Add these lines of code into your environment config file. config/environments/environment.rb

```
config.action_mailer.delivery_method = :resend
```

 Then create a `UserMailer` class definition. app/mailers/user_mailer.rb

```
class UserMailer < ApplicationMailer
  default from: 'Acme <onboarding@resend.dev>' # this domain must be verified with Resend
  def welcome_email
    @user = params[:user]
    @url = 'http://example.com/login'
    mail(to: ["delivered@resend.dev"], subject: 'hello world')
  end
end
```

 And create your ERB email template. app/views/user_mailer/welcome_email.html.erb

```
<!doctype html>
<html>
  <head>
    <meta content="text/html; charset=UTF-8" http-equiv="Content-Type" />
  </head>
  <body>
    <h1>Welcome to example.com, <%= @user.name %></h1>
    <p>You have successfully signed up to example.com,</p>
    <p>To log in to the site, just follow this link: <%= @url %>.</p>
    <p>Thanks for joining and have a great day!</p>
  </body>
</html>
```

 Initialize your `UserMailer` class. This should return a `UserMailer` instance.

```
u = User.new name: "derich"
mailer = UserMailer.with(user: u).welcome_email

# => #<Mail::Message:153700, Multipart: false, Headers: <From: from@example.com>, <To: to@example.com>, <Subject: hello world>, <Mime-Version: 1.0>...
```

 Finally, you can now send emails using the `deliver_now!` method:

```
mailer.deliver_now!

# => {:id=>"a193c81e-9ac5-4708-a569-5caf14220539", :from=>....}
```

## ​3. Try it yourself

 [Rails ExampleSee the full source code.](https://github.com/resend/resend-rails-example)

---

# Send emails with Railway

> Learn how to send your first email using Railway and the Resend Node.js SDK.

[Railway](https://railway.com/?referralCode=resend) enables you to focus on building product instead of managing infrastructure, automatically scaling to support your needs as you grow.

## ​Prerequisites

 To get the most out of this guide, you’ll need to:

- [Create an API key](https://resend.com/api-keys)
- [Verify your domain](https://resend.com/domains)

## ​1. Install

 We’ve created a [Resend template](https://railway.com/deploy/resend?referralCode=resend&utm_medium=integration&utm_source=template&utm_campaign=generic) using the Resend Node.js SDK as an introduction to using Resend on Railway. To get started, you deploy the template to Railway.  ![Deploy button highlighted on Railway](https://mintcdn.com/resend/UGYfPeFBYurSSqVy/images/send-with-railway.png?fit=max&auto=format&n=UGYfPeFBYurSSqVy&q=85&s=a4b37d9be58e4df72a9eec8e89352e1c)

## ​2. Add your API key

 [Add an API key](https://resend.com/api-keys) from Resend and click **Deploy**. ![Template modal with API key field highlighted](https://mintcdn.com/resend/UGYfPeFBYurSSqVy/images/send-with-railway-1.png?fit=max&auto=format&n=UGYfPeFBYurSSqVy&q=85&s=0efcfbf778a0193a8c9aa353a07635b6)

## ​3. Send your first email

 Once your deployment finishes, click the deploy URL to open the app and send your first email. ![Deployment link highlighted](https://mintcdn.com/resend/UGYfPeFBYurSSqVy/images/send-with-railway-2.png?fit=max&auto=format&n=UGYfPeFBYurSSqVy&q=85&s=c4a9f0838a4efb406d349c4e815c1c80) While this example uses the [Resend Node.js SDK](https://www.npmjs.com/package/@resend/node), you can add Resend using [any of our Official SDKs](https://resend.com/docs/sdks) that Railway supports. Keep in mind that as a basic project, this template sends an email with your
account each time someone visits your deployment URL, so share the link with
discretion. You can also [set up the project locally](https://docs.railway.com/develop/cli) and make changes to the projectusing the Railway CLI.

## ​4. Try it yourself

 [Railway TemplateSee the full source code.](https://github.com/resend/resend-node-railway-starter)

---

# Send emails with RedwoodJS

> Learn how to send your first email using Redwood.js and the Resend Node.js SDK.

### ​Prerequisites

 To get the most out of this guide, you’ll need to:

- [Create an API key](https://resend.com/api-keys)
- [Verify your domain](https://resend.com/domains)

### ​1. Install

 Get the Resend Node.js SDK.

```
yarn workspace api add resend
```

### ​2. Send email using HTML

```
yarn rw g function send
```

 The easiest way to send an email is by using the `html` parameter. api/src/functions/send/send.ts

```
import { Resend } from 'resend';
import type { APIGatewayEvent, Context } from 'aws-lambda';

const resend = new Resend('re_xxxxxxxxx');

export const handler = async (event: APIGatewayEvent, context: Context) => {
  const { data, error } = await resend.emails.send({
    from: 'Acme <onboarding@resend.dev>',
    to: ['delivered@resend.dev'],
    subject: 'hello world',
    html: '<strong>it works!</strong>',
  });

  if (error) {
    return {
      statusCode: 500,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ error }),
    };
  }

  return {
    statusCode: 200,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ data }),
  };
};
```

### ​3. Try it yourself

 [Redwood.js ExampleSee the full source code.](https://github.com/resend/resend-redwoodjs-example)

---

# Send emails with Remix

> Learn how to send your first email using Remix and the Resend Node.js SDK.

## ​Prerequisites

 To get the most out of this guide, you’ll need to:

- [Create an API key](https://resend.com/api-keys)
- [Verify your domain](https://resend.com/domains)

## ​1. Install

 Get the Resend Node.js SDK.

```
npm install resend
```

## ​2. Send email using HTML

 Create a [Resource Route](https://remix.run/docs/en/1.16.1/guides/resource-routes) under `app/routes/send.ts`. The easiest way to send an email is by using the `html` parameter.

```
import { json } from '@remix-run/node';
import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);

export const loader = async () => {
  const { data, error } = await resend.emails.send({
    from: 'Acme <onboarding@resend.dev>',
    to: ['delivered@resend.dev'],
    subject: 'Hello world',
    html: '<strong>It works!</strong>',
  });

  if (error) {
    return json({ error }, 400);
  }

  return json(data, 200);
};
```

## ​3. Try it yourself

 [Remix ExampleSee the full source code.](https://github.com/resend/resend-remix-example)

---

# Send emails using Retool with SMTP

> Learn how to integrate Retool with Resend SMTP.

### ​Prerequisites

 To get the most out of this guide, you’ll need to:

- [Create an API key](https://resend.com/api-keys)
- [Verify your domain](https://resend.com/domains)

## ​1. Get the Resend SMTP credentials

 When configuring your SMTP integration, you’ll need to use the following credentials:

- **Host**: `smtp.resend.com`
- **Port**: `465`
- **Username**: `resend`
- **Password**: `YOUR_API_KEY`

## ​2. Integrate with Retool SMTP

 Log into your [Retool](https://retool.com) account and create a new SMTP Resource.

1. Go to **Resources** and click **Create New**

 ![Retool SMTP - Create new Resources](https://mintcdn.com/resend/OWNnQaVDyqcGyhhN/images/retool-smtp-1.png?fit=max&auto=format&n=OWNnQaVDyqcGyhhN&q=85&s=c6edda6c2512e895bfec5b7e47627d96)

1. Search for **SMTP** and select it

 ![Retool SMTP - Search for SMTP](https://mintcdn.com/resend/OWNnQaVDyqcGyhhN/images/retool-smtp-2.png?fit=max&auto=format&n=OWNnQaVDyqcGyhhN&q=85&s=b95716d79754f6d2f8cedd6522d8e8f8)

1. Add name and SMTP credentials

 ![Retool SMTP - Add SMTP credentials](https://mintcdn.com/resend/OWNnQaVDyqcGyhhN/images/retool-smtp-3.png?fit=max&auto=format&n=OWNnQaVDyqcGyhhN&q=85&s=cbd6221e4b03dfc909f00f966afc4a2a)

---

# Send emails with Ruby

> Learn how to send your first email using the Resend Ruby SDK.

## ​Prerequisites

 To get the most out of this guide, you’ll need to:

- [Create an API key](https://resend.com/api-keys)
- [Verify your domain](https://resend.com/domains)

## ​1. Install

 Get the Resend Ruby SDK.

```
gem install resend
```

## ​2. Send email using HTML

 The easiest way to send an email is by using the `html` parameter. index.rb

```
require "resend"

Resend.api_key = "re_xxxxxxxxx"

params = {
  "from": "Acme <onboarding@resend.dev>",
  "to": ["delivered@resend.dev"],
  "subject": "hello world",
  "html": "<strong>it works!</strong>"
}

sent = Resend::Emails.send(params)
puts sent
```

## ​3. Try it yourself

 [Ruby ExampleSee the full source code.](https://github.com/resend/resend-ruby-example)

---

# Send emails with Rust

> Learn how to send your first email using the Resend Rust SDK.

## ​Prerequisites

 To get the most out of this guide, you’ll need to:

- [Create an API key](https://resend.com/api-keys)

## ​Install

 First, create a rust project with cargo and `cd` into it.

```
cargo init resend-rust-example
cd resend-rust-example
```

 Next, add add the Rust Resend SDK as well as [Tokio](https://tokio.rs):

```
cargo add resend-rs
cargo add tokio -F macros,rt-multi-thread
```

 The Rust SDK is Async-first so Tokio is needed.

## ​Send email

```
use resend_rs::types::CreateEmailBaseOptions;
use resend_rs::{Resend, Result};

#[tokio::main]
async fn main() -> Result<()> {
  let resend = Resend::new("re_xxxxxxxxx");

  let from = "Acme <onboarding@resend.dev>";
  let to = ["delivered@resend.dev"];
  let subject = "Hello World";

  let email = CreateEmailBaseOptions::new(from, to, subject)
    .with_html("<strong>It works!</strong>");

  let _email = resend.emails.send(email).await?;

  Ok(())
}
```

## ​Reading the API key

 Instead of using `Resend::new` and hardcoding the API key, the `RESEND_API_KEY` environment variable
can be used instead. The `Resend::default()` should be used in that scenario instead.

### ​Reading the API key from a.envfile

 Another popular option is to use a `.env` file for environment variables. You can use the
[dotenvy](https://crates.io/crates/dotenvy) crate for that:

```
cargo add dotenvy
```

```
// main.rs
use dotenvy::dotenv;
use resend_rs::types::CreateEmailBaseOptions;
use resend_rs::{Resend, Result};

#[tokio::main]
async fn main() -> Result<()> {
  let _env = dotenv().unwrap();

  let resend = Resend::default();

  let from = "Acme <onboarding@resend.dev>";
  let to = ["delivered@resend.dev"];
  let subject = "Hello World";

  let email = CreateEmailBaseOptions::new(from, to, subject)
    .with_html("<strong>It works!</strong>");

  let _email = resend.emails.send(email).await?;

  Ok(())
}
```

```
# .env
RESEND_API_KEY=re_xxxxxxxxx
```

## ​3. Try it yourself

 [Rust ExamplesSee the full source code.](https://github.com/resend/resend-rust-example)

---

# Send emails with Sinatra

> Learn how to send your first email using Sinatra and the Resend Ruby SDK.

## ​Prerequisites

 To get the most out of this guide, you’ll need to:

- [Create an API key](https://resend.com/api-keys)
- [Verify your domain](https://resend.com/domains)

## ​1. Install

 Get the Resend Ruby SDK.

```
gem install resend
```

## ​2. Send email using HTML

 The easiest way to send an email is by using the `html` parameter. index.rb

```
require "sinatra"
require "resend"

set :port, 5000
set :bind, "0.0.0.0"

Resend.api_key = ENV["RESEND_API_KEY"]

get "/" do

  content_type :json

  params = {
    from: 'Acme <onboarding@resend.dev>',
    to: ['delivered@resend.dev'],
    subject: 'hello world',
    html: '<strong>it works!</strong>',
  }

  Resend::Emails.send(params).to_hash.to_json
end
```

## ​3. Try it yourself

 [Sinatra ExampleSee the full source code.](https://github.com/resend/resend-sinatra-example)

---

# Send emails with SMTP

> Learn how to integrate Resend via SMTP.

## ​Prerequisites

 To get the most out of this guide, you’ll need to:

- [Create an API key](https://resend.com/api-keys)
- [Verify your domain](https://resend.com/domains)

 Prefer watching a video? Check out our video walkthrough below.

## ​SMTP Credentials

 When configuring your SMTP integration, you’ll need to use the following credentials:

- **Host**: `smtp.resend.com`
- **Port**: `25`, `465`, `587`, `2465`, or `2587`
- **Username**: `resend`
- **Password**: `YOUR_API_KEY`

 Ports help to instruct the type of security you want to use in your SMTP connection.

| Type | Port | Security |
| --- | --- | --- |
| SMTPS | 465,2465 | Implicit SSL/TLS (Immediately connects via SSL/TLS) |
| STARTTLS | 25,587,2587 | Explicit SSL/TLS (First connects via plaintext, then upgrades to SSL/TLS) |

## ​Idempotency Key

 Idempotency keys are used to prevent duplicate emails. You can add the `Resend-Idempotency-Key` header to your emails sent with SMTP to prevent duplicate emails. SMTP

```
From: Acme <[email protected]>
To: [email protected]
Subject: hello world
Resend-Idempotency-Key: welcome-user/123456789

<p>it works!</p>
```

 Learn more about [idempotency keys](https://resend.com/docs/dashboard/emails/idempotency-keys).

## ​Custom Headers

 If your SMTP client supports it, you can add custom headers to your emails. Here are some common use cases for custom headers:

- Prevent threading on Gmail with the `X-Entity-Ref-ID` header
- Include a shortcut for users to unsubscribe with the `List-Unsubscribe` header

## ​FAQ

 Once configured, you should be able to start sending emails via SMTP. Below are some frequently asked questions:

What if I need logs from the server to debug?

We currently don’t provide SMTP server logs for debugging. If you run into
issues, please [reach out to support](https://resend.com/help).

Where do I see the emails sent with SMTP?

Emails sent with SMTP will show in your [emails
table](https://resend.com/emails).

Does the rate limit apply when sending with SMTP?

Yes, the rate limit is the [same as the
API](https://resend.com/docs/api-reference/introduction#rate-limit).

---

# Send emails with Supabase Edge Functions

> Learn how to send your first email using Supabase Edge Functions.

## ​Prerequisites

 To get the most out of this guide, you’ll need to:

- [Create an API key](https://resend.com/api-keys)
- [Verify your domain](https://resend.com/domains)

 Make sure you have the latest version of the [Supabase CLI](https://supabase.com/docs/guides/cli#installation) installed.

## ​1. Create Supabase function

 Create a new function locally:

```
supabase functions new resend
```

## ​2. Edit the handler function

 Paste the following code into the `index.ts` file: index.ts

```
const RESEND_API_KEY = Deno.env.get('RESEND_API_KEY');

const handler = async (_request: Request): Promise<Response> => {
  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${RESEND_API_KEY}`,
    },
    body: JSON.stringify({
      from: 'Acme <onboarding@resend.dev>',
      to: ['delivered@resend.dev'],
      subject: 'hello world',
      html: '<strong>it works!</strong>',
    }),
  });

  const data = await res.json();

  return new Response(JSON.stringify(data), {
    status: 200,
    headers: {
      'Content-Type': 'application/json',
    },
  });
};

Deno.serve(handler);
```

## ​3. Deploy and send email

 Run function locally:

```
supabase functions start
supabase functions serve resend --no-verify-jwt
```

 Deploy function to Supabase:

```
supabase functions deploy resend
```

 Open the endpoint URL to send an email: ![Supabase Edge Functions - Deploy Function](https://mintcdn.com/resend/OWNnQaVDyqcGyhhN/images/supabase-edge-functions-deploy-function.png?fit=max&auto=format&n=OWNnQaVDyqcGyhhN&q=85&s=e28cab375d10a57f712e77ff3c888005)

## ​4. Try it yourself

 [Supabase Edge Functions ExampleSee the full source code.](https://github.com/resend/resend-supabase-edge-functions-example)

---

# Send emails using Supabase with SMTP

> Learn how to integrate Supabase Auth with Resend SMTP.

## ​Prerequisites

 To get the most out of this guide, you’ll need to:

- [Create an API key](https://resend.com/api-keys)
- [Verify your domain](https://resend.com/domains)

## ​1. Get the Resend SMTP credentials

 When configuring your SMTP integration, you’ll need to use the following credentials:

- **Host**: `smtp.resend.com`
- **Port**: `465`
- **Username**: `resend`
- **Password**: `YOUR_API_KEY`

## ​2. Integrate with Supabase SMTP

 After logging into your Supabase account, you’ll need to enable the SMTP integration.

1. Go to your Supabase project
2. Click on **Project Settings** in the left sidebar
3. Select the **Authentication** tab
4. Find the SMTP section and toggle the **Enable Custom SMTP** option
5. Add your Sender email and name (these are required fields). For example: `support@acme.com` and `ACME Support`.

 ![Supabase Auth - SMTP Sender email and name settings](https://mintcdn.com/resend/OWNnQaVDyqcGyhhN/images/supabase-auth-smtp-sender-email-name.png?fit=max&auto=format&n=OWNnQaVDyqcGyhhN&q=85&s=1db59a322b21efb38bc298a5796d32b3)

1. You can copy-and-paste the [SMTP credentials](https://resend.com/settings/smtp) from Resend to Supabase.

 ![Supabase Auth - SMTP Settings](https://mintcdn.com/resend/OWNnQaVDyqcGyhhN/images/supabase-auth-smtp-settings.png?fit=max&auto=format&n=OWNnQaVDyqcGyhhN&q=85&s=70c068d96e4f03c7e2f03b6e71219d4f) After that, you can click the **Save** button and all of your emails will be sent through Resend.

---

# Send emails with SvelteKit

> Learn how to send your first email using SvelteKit and the Resend Node.js SDK.

## ​Prerequisites

 To get the most out of this guide, you’ll need to:

- [Create an API key](https://resend.com/api-keys)
- [Verify your domain](https://resend.com/domains)

## ​1. Install

 Get the Resend Node.js SDK.

```
npm install resend
```

## ​2. Send email using HTML

 Create a [+server API route](https://svelte.dev/docs/kit/routing#server) under `src/routes/send/+server.ts`. The easiest way to send an email is by using the `html` parameter.

```
import { Resend } from 'resend';
import { RESEND_API_KEY } from '$env/static/private'; // define in your .env file

const resend = new Resend(RESEND_API_KEY);

export async function POST() {
  try {
    const { data, error } = await resend.emails.send({
      from: 'Acme <onboarding@resend.dev>',
      to: ['delivered@resend.dev'],
      subject: 'Hello world',
      html: '<p>Hello world</p>',
    });

    if (error) {
      return Response.json({ error }, { status: 500 });
    }

    return Response.json({ data });
  } catch (error) {
    return Response.json({ error }, { status: 500 });
  }
}
```

## ​3. Try it yourself

 [SvelteKit ExampleSee the full source code.](https://github.com/resend/resend-svelte-kit-example)

---

# Send emails with Symfony

> Learn how to send your first email using the Symfony Resend Mailer Bridge.

## ​Prerequisites

 To get the most out of this guide, you will need to:

- [Create an API key](https://resend.com/api-keys)
- [Verify your domain](https://resend.com/domains)

## ​1. Install

 Get the Resend Mailer Bridge package. Composer

```
composer require symfony/resend-mailer
```

 If your application relies on Resend webhook events, you should also install the Symfony Webhook Component. Composer

```
composer require symfony/webhook
```

## ​2. Configuring Mailer

 In your `.env.local` file, which you can create if needed, add the following:

```
MAILER_DSN=resend+api://API_KEY@default
MAILER_RESEND_SECRET=SIGNING_SECRET
```

 Replace `API_KEY` with your Resend API key, and `SIGNING_SECRET` with your webhook secret, which can be retrieved from the Resend dashboard after creating a new webhook endpoint (see below).

## ​3. Send your first email

 In a controller, inject the `Mailer`:

```
public function __construct(
    private readonly MailerInterface $mailer,
) {
}
```

 In a controller action, use the `$this->mailer` to send your email:

```
$this->mailer->send(
    (new Email())
        ->from('Acme <onboarding@resend.dev>')
        ->to('delivered@resend.dev')
        ->subject('Hello world')
        ->html('<strong>it works!</strong>')
);
```

 Learn more about sending emails with Mailer Component in [Symfony’s documentation](https://symfony.com/doc/current/mailer.html#creating-sending-messages).

## ​4. Receive and handle webhooks

 Thanks to the Webhook Component, you can create a webhook listener. src/Webhook/ResendWebhookListener.php

```
#[AsRemoteEventConsumer('mailer_resend')]
readonly class ResendWebhookListener implements ConsumerInterface
{
    public function __construct(
        #[Autowire(param: 'kernel.project_dir')] private string $projectDir,
    ) {
    }

    public function consume(RemoteEvent $event): void
    {
        if ($event instanceof MailerDeliveryEvent) {
            $this->handleMailDelivery($event);
        } elseif ($event instanceof MailerEngagementEvent) {
            $this->handleMailEngagement($event);
        } else {
            // This is not an email event
            return;
        }
    }

    private function handleMailDelivery(MailerDeliveryEvent $event): void
    {
        // Todo
    }

    private function handleMailEngagement(MailerEngagementEvent $event): void
    {
        // Todo
    }
}
```

 Bind your listener to the Webhook routing config: config/packages/webhook.yaml

```
framework:
  webhook:
    routing:
      mailer_resend:
        service: 'mailer.webhook.request_parser.resend'
        secret: '%env(MAILER_RESEND_SECRET)%'
```

 Next, register your application’s webhook endpoint URL (example: `https://{app_domain}/webhook/mailer_resend`) in the [Resend Dashboard](https://resend.com/webhooks):

## ​5. Try it yourself

 [Symfony ExampleSee the full source code.](https://github.com/resend/resend-symfony-example)

---

# Send emails with Vercel Functions

> Learn how to send your first email using Vercel Functions.

## ​Prerequisites

 To get the most out of this guide, you’ll need to:

- [Create an API key](https://resend.com/api-keys)
- [Verify your domain](https://resend.com/domains)

 Make sure you have the latest version of the [Vercel CLI](https://vercel.com/docs/cli#installing-vercel-cli) installed.

## ​1. Install dependencies

 Install the Resend SDK:

```
npm install resend
```

## ​2. Set up environment variables

 Add your Resend API key to your environment variables: .env.local

```
RESEND_API_KEY=re_xxxxxxxxx
```

## ​3. Create a Next.js function

 Create a route file under `app/api/send/route.ts` if you’re using the [App Router](https://nextjs.org/docs/app/building-your-application/routing/router-handlers). route.ts

```
import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);

export async function POST() {
  const response = await resend.emails.send({
    from: 'Acme <onboarding@resend.dev>',
    to: ['delivered@resend.dev'],
    subject: 'hello world',
    html: '<strong>it works!</strong>',
  });

  return Response.json(response, {
    status: response.error ? 500 : 200,
  });
}
```

## ​4. Send email locally

 Run function locally:

```
npm run dev
```

 Open the endpoint URL to send an email: `http://localhost:3000/api/send`

## ​5. Send email in production

 Deploy function to Vercel:

```
vercel
```

 Make sure to add your `RESEND_API_KEY` environment variable in your Vercel project settings. Open the endpoint URL to send an email: `https://your-project.vercel.app/api/send`

## ​6. Try it yourself

 [Vercel Functions ExampleSee the full source code.](https://github.com/resend/resend-vercel-functions-example)

---

# Send emails using WordPress with SMTP

> Learn how to send your first email using Wordpress.

## ​Prerequisites

 To get the most out of this guide, you’ll need to:

- [Create an API key](https://resend.com/api-keys)
- [Verify your domain](https://resend.com/domains)

## ​1. Install a plugin

 First, you’ll need to install and activate the [WP Mail SMTP](https://wordpress.org/plugins/wp-mail-smtp/) plugin. Once the plugin is activated you will see the setup wizard. You can skip this step as we’ll guide you through how to configure the plugin for Resend. Just click on **Go to the Dashboard** at the bottom of the screen to exit the setup wizard. ![WP Mail SMTP - Setup Wizard](https://mintcdn.com/resend/lyl6PQTYhtWhUjuS/images/wordpress-setup-wizard.png?fit=max&auto=format&n=lyl6PQTYhtWhUjuS&q=85&s=034e82ed82a43c1cc25e9119995ac558)

## ​2. Configuration

 From your admin dashboard, visit the **WP Mail SMTP > Settings** page to configure the plugin. Firstly, configure your **From Email**, **From Name**, and **Return Path**. Next, we’ll configure the SMTP settings for Resend. Select **Other SMTP** in the **Mailer** section. ![WP Mail SMTP - Settings](https://mintcdn.com/resend/lyl6PQTYhtWhUjuS/images/wordpress-configure.png?fit=max&auto=format&n=lyl6PQTYhtWhUjuS&q=85&s=12cb502dcffbc76cad7f6bbef00a7f43) In the **Other SMTP** section, configure the following settings:

- **SMTP Host**: `smtp.resend.com`
- **Encryption**: `SSL`
- **SMTP Port**: `465`
- **Auto TLS**: `ON`
- **Authentication**: `ON`
- **SMTP Username**: `resend`
- **SMTP Password**: `YOUR_API_KEY`

 Make sure to replace `YOUR_API_KEY` with an existing key or create a new [API Key](https://resend.com/api-keys).

## ​3. Sending a test email

 From your admin dashboard, visit the **WP Mail SMTP > Tools** page to send a test email. ![WP Mail SMTP - Send a Test Email](https://mintcdn.com/resend/lyl6PQTYhtWhUjuS/images/wordpress-test-email.png?fit=max&auto=format&n=lyl6PQTYhtWhUjuS&q=85&s=bffb755f5673f14a03d84d36a4b361ca)
