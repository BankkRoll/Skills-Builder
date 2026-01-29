# Amplitude and more

# Amplitude

> Track user behavior and documentation analytics with Amplitude.

Add the following to your `docs.json` file to send analytics to Amplitude.

```
"integrations": {
    "amplitude": {
        "apiKey": "required"
    }
}
```

---

# Clarity

> Track user sessions with Microsoft Clarity analytics.

Add the following to your `docs.json` file to send analytics to Microsoft Clarity.

```
"integrations": {
    "clarity": {
        "projectId": "required"
    }
}
```

## ​Get your project ID

1. Create a [Clarity account](https://clarity.microsoft.com/projects).
2. Click **Get tracking code.**
3. Copy your project ID from the tracking code.

---

# Clearbit

> Enrich user data with Clearbit intelligence.

Add the following to your `docs.json` file to send analytics to Clearbit.

```
"integrations": {
    "clearbit": {
        "publicApiKey": "required"
    }
}
```

---

# Fathom

> Track documentation analytics with Fathom.

Add the following to your `docs.json` file to send analytics to Fathom. You can get the `siteId` from your script settings.

```
"integrations": {
    "fathom": {
        "siteId": "required"
    }
}
```

---

# Google Analytics 4

> Track visitor behavior and engagement with Google Analytics.

You will need to generate a new  property to use with Mintlify. The data collected will go into the same project as your other Google Analytics data. If you are using the old version of Google Analytics, Universal Analytics, you will still be able to generate a  property.  data is slightly different from UA data but still gets collected in the same project.

## ​How to Connect GA4 to Mintlify

### ​Create a Web Stream

 You will need to create a web stream to get the Measurement ID to put into Mintlify. Click the cog at the bottom left of the Google Analytics screen. Then click on Data Streams. ![Screenshot of the Data Streams page in the Google Analytics dashboard.](https://mintcdn.com/mintlify/GiucHIlvP3i5L17o/images/ga4-web-streams.png?fit=max&auto=format&n=GiucHIlvP3i5L17o&q=85&s=3da279b4cbc0f73f3f08e72fa8502b94) Create a Web Stream and put the URL of your Mintlify docs site as the stream URL. Your Measurement ID looks like `G-XXXXXXX` and will show up under Stream Details immediately after you create the Web Stream.

### ​Put Measurement ID in docs.json

 Add your Measurement ID to your `docs.json` file like so: docs.json

```
"integrations": {
    "ga4": {
        "measurementId": "G-XXXXXXX"
    }
}
```

### ​Wait

 Google Analytics takes two to three days to show your data. You can use the [Google Analytics Debugger](https://chrome.google.com/webstore/detail/google-analytics-debugger/jnkmfdileelhofjcijamephohjechhna?hl=en) to check analytics are enabled correctly. The extension will log to your browser’s console every time GA4 makes a request. Preview links have analytics turned off.

---

# Google Tag Manager

> Manage analytics tags and events with Google Tag Manager.

Add your tag ID to `docs.json` file and we’ll inject the Google Tag Manager script to all your pages. You are responsible for setting up cookie consent banners with Google Tag Manager if you need them.

```
"integrations": {
    "gtm": {
        "tagId": "required"
    }
}
```

---

# Heap

> Track user interactions with Heap analytics.

Add the following to your `docs.json` file to send analytics to Heap.

```
"integrations": {
    "heap": {
        "appId": "required"
    }
}
```

---

# Hightouch

> Sync data to Hightouch for audience activation.

Add the following to your `docs.json` file to send analytics to Hightouch. Do not include `https://` for the `apiHost`.

```
"integrations": {
    "hightouch": {
        "writeKey": "required"
        "apiHost": "optional"
    }
}
```

---

# HotJar

> Capture user feedback and heatmaps with HotJar.

Add the following to your `docs.json` file to send analytics to HotJar. Analytics options in docs.json

```
"integrations": {
    "hotjar": {
        "hjid": "required",
        "hjsv": "required"
    }
}
```

---

# LogRocket

> Monitor user sessions and errors with LogRocket.

Add the following to your `docs.json` file to send analytics to LogRocket. Analytics options in docs.json

```
"integrations": {
    "logrocket": {
        "apiKey": "required"
    }
}
```

---

# Mixpanel

> Track product analytics and user behavior with Mixpanel.

Add the following to your `docs.json` file to send analytics to Mixpanel. Analytics options in docs.json

```
"integrations": {
    "mixpanel": {
        "projectToken": "YOUR_MIXPANEL_PROJECT_TOKEN"
    }
}
```

 Replace `YOUR_MIXPANEL_PROJECT_TOKEN` with your Mixpanel project token. You can find this in your [Mixpanel project settings](https://mixpanel.com/settings/project).

## ​Tracked events

 Mintlify automatically tracks the following user interactions:

- Page views
- Search queries
- Feedback submissions
- Context menu interactions
- Navigation clicks

 If you’re not seeing events in Mixpanel, ensure your project token is correct and that no content security policies are blocking the Mixpanel script.

---

# Analytics integrations

> Connect to analytics platforms to track user engagement and documentation usage.

Track how users interact with your documentation by connecting to third-party analytics platforms. Mintlify sends engagement events to your configured analytics providers.

## ​How analytic integrations work

 When you add analytics integrations to your documentation site, Mintlify tracks user interactions like page views, search queries, API playground requests, and feedback submissions and sends them to your analytics providers. You can connect any number of supported analytics providers by adding your API keys to the `docs.json` file. Analytics events flow to your providers as soon as you add them to your configuration with no further configuration required.

## ​Supported platforms

 [Amplitude](https://mintlify.com/docs/integrations/analytics/amplitude)[Mixpanel](https://mintlify.com/docs/integrations/analytics/mixpanel)[Clarity](https://mintlify.com/docs/integrations/analytics/clarity)[PostHog](https://mintlify.com/docs/integrations/analytics/posthog)[Google Analytics 4](https://mintlify.com/docs/integrations/analytics/google-analytics)[Google Tag Manager](https://mintlify.com/docs/integrations/analytics/google-tag-manager)[Hightouch](https://mintlify.com/docs/integrations/analytics/hightouch)[HotJar](https://mintlify.com/docs/integrations/analytics/hotjar)[LogRocket](https://mintlify.com/docs/integrations/analytics/logrocket)[Pirsch](https://mintlify.com/docs/integrations/analytics/pirsch)[Plausible](https://mintlify.com/docs/integrations/analytics/plausible)[Fathom](https://mintlify.com/docs/integrations/analytics/fathom)[Clearbit](https://mintlify.com/docs/integrations/analytics/clearbit)[Heap](https://mintlify.com/docs/integrations/analytics/heap)[Segment](https://mintlify.com/docs/integrations/analytics/segment)

## ​Setup

 Add your analytics provider credentials to the `integrations` object in `docs.json`. Only include the platforms you want to use. docs.json

```
"integrations": {
    "amplitude": {
        "apiKey": "required"
    },
    "clarity": {
        "projectId": "required"
    },
    "clearbit": {
        "publicApiKey": "required"
    },
    "cookies": {
      "key": "required",
      "value": "required"
    },
    "fathom": {
        "siteId": "required"
    },
    "ga4": {
        "measurementId": "required"
    },
    "gtm": {
        "tagId": "required"
    },
    "hightouch": {
        "apiKey": "required",
        "apiHost": "optional"
    },
    "hotjar": {
        "hjid": "required",
        "hjsv": "required"
    },
    "logrocket": {
        "appId": "required"
    },
    "mixpanel": {
        "projectToken": "required"
    },
    "pirsch": {
        "id": "required"
    },
    "plausible": {
        "domain": "required"
    },
    "posthog": {
        "apiKey": "required",
        "apiHost": "optional"
    },
    "segment": {
      "key": "required"
    },
    "telemetry": {
      "enabled": "boolean"
    }
}
```

### ​Example configuration

 docs.json

```
{
  "integrations": {
    "ga4": {
      "measurementId": "G-XXXXXXXXXX"
    },
    "posthog": {
      "apiKey": "phc_xxxxxxxxxxxxx",
      "apiHost": "https://app.posthog.com"
    },
    "mixpanel": {
      "projectToken": "xxxxxxxxxxxxx"
    }
  }
}
```

## ​Tracked events

 All tracked events use the `docs.` prefix.

### ​Navigation and page views

| Event name | Description |
| --- | --- |
| docs.content.view | User views a page. Only sent to providers that don’t track page views by default. |
| docs.navitem.click | User clicks a header navigation item. |
| docs.navitem.cta_click | User clicks a call to action button. |
| docs.footer.powered_by_mintlify_click | User clicks the “Powered by Mintlify” link. |

### ​Search

| Event name | Description |
| --- | --- |
| docs.search.query | User performs a search query. |
| docs.search.close | User closes the search bar. |
| docs.search.result_click | User clicks a search result. |

### ​Code and API playground

| Event name | Description |
| --- | --- |
| docs.code_block.copy | User copies code from a code block. |
| docs.code_block.ask_ai | User asks the assistant to explain a code block. |
| docs.api_playground.request | User makes an API request in the API playground. |

### ​Interactive components

| Event name | Description |
| --- | --- |
| docs.accordion.open | User opens an accordion. |
| docs.accordion.close | User closes an accordion. |
| docs.expandable.open | User opens an expandable. |
| docs.expandable.close | User closes an expandable. |

### ​Assistant and agent

| Event name | Description |
| --- | --- |
| docs.assistant.enter | User opens the AI assistant. |
| docs.assistant.completed | Chat session completes. |
| docs.assistant.source_click | User clicks a citation in a chat response. |
| docs.assistant.suggestion_click | User clicks a suggested question. |
| docs.assistant.ask_ai_on_text_selection | User selects text and clicks “Ask AI.” |
| docs.assistant.shared | User shares a chat conversation. |
| docs.assistant.thumbs_up | User clicks the positive feedback button on an assistant response. |
| docs.assistant.thumbs_down | User clicks the negative feedback button on an assistant response. |
| docs.assistant.spam_detected | The assistant detects spam in a user message. |
| docs.autopilot.suggestion.created | The agent creates a documentation suggestion. |
| docs.autopilot.suggestion.no_suggestion | The agent determines no documentation update is needed. |

### ​Contextual menu

| Event name | Description |
| --- | --- |
| docs.context_menu.copy_page | User copies the current page as markdown. |
| docs.context_menu.copy_mcp_link | User copies the hosted MCP server link. |
| docs.context_menu.ai_provider_click | User clicks an AI provider to create a conversation with the current page as context. |
| docs.context_menu.install_mcp_server | User installs the hosted MCP server on code editors. |

---

# Pirsch

> Track privacy-focused analytics with Pirsch.

Add the following to your `docs.json` file to send analytics to Pirsch. You can get your site ID from Settings > Developer > Identification Code.

```
"integrations": {
    "pirsch": {
        "id": "required"
    }
}
```

---

# Plausible

> Track simple, privacy-respecting analytics with Plausible.

Add your site’s domain to `docs.json` to send analytics to Plausible. Do not include `https://` for the domain or server.

```
"integrations": {
    "plausible": {
        "domain": "required - your documentation domain",
        "server": "optional - your self-hosted Plausible server URL"
    }
}
```

---

# PostHog

> Track product analytics and feature usage with PostHog.

Add the following to your `docs.json` file to send analytics to PostHog. You only need to include `apiHost` if you are self-hosting PostHog. We send events to `https://app.posthog.com` by default.

```
"integrations": {
    "posthog": {
        "apiKey": "YOUR_POSTHOG_PROJECT_API_KEY",
        "apiHost": "optional",
        "sessionRecording": true
    }
}
```

### ​Configuration options

 [​](#param-api-key)apiKeystringrequiredYour PostHog project API key. Must start with `phc_`. [​](#param-api-host)apiHoststringThe URL of your PostHog instance. Only required if you are self-hosting PostHog. Defaults to `https://app.posthog.com`. [​](#param-session-recording)sessionRecordingbooleandefault:"true"Enable or disable session recording. Set to `false` to disable session recordings while keeping analytics enabled.

## ​Session recordings

 Session recordings are enabled by default when you configure PostHog. To disable session recordings while keeping analytics enabled, set `sessionRecording` to `false` in your configuration. Disable session recordings

```
"integrations": {
    "posthog": {
        "apiKey": "phc_your-key",
        "sessionRecording": false
    }
}
```

 You need to add the URL for your docs website to PostHog’s “Authorized domains for recordings” before you can receive session recordings. The option to add your URL is in PostHog’s project settings.

---

# Segment

> Send analytics events to Segment and downstream tools.

Add your Segment write key to your `docs.json` file to send analytics to Segment.

```
"integrations": {
    "segment": {
        "key": "required",
    }
}
```

---

# Osano

> Manage cookie consent with Osano privacy platform.

Add the following to your `docs.json` file to add the [Osano](https://www.osano.com/) cookie consent manager.

```
"integrations": {
    "osano": {
        "scriptSource": "SOURCE"
    }
}
```

 The `scriptSource` value can be found as the `src` value in the code snippet generated by Osano. It always starts with `https://cmp.osano.com/` and ends with `/osano.js`. Code snippet from Osano

```
<script src="https://cmp.osano.com/placeholder/placeholder/osano.js"/>
```

## ​Troubleshooting

Pages not loading with Strict compliance mode

If your documentation pages aren’t loading properly when using Osano’s **Strict** compliance mode, you’ll need to whitelist Mintlify’s domain to allow images and other assets to load.1

Navigate to Managed Rules

In your Osano dashboard, go to **Scripts** → **Managed Rules**.2

Add Mintlify domain

Add `.mintlify.app/` as a managed rule.![Osano managed rule](https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/integrations/osano-managed-rule.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=66a71862fce8aa19564959a171927597)This ensures that all Mintlify-served assets (including images, stylesheets, and other documentation resources) are treated as essential and will load even when Osano blocks uncategorized third-party content.

---

# Privacy integrations

> Integrate with data privacy platforms for compliance.

[Osano](https://mintlify.com/docs/integrations/privacy/osano)

## ​Enabling Data Privacy Integrations

 You can add data privacy platforms onto your docs. Add the `integrations` field into your `docs.json` file with your respective scripts.

```
"integrations": {
    "osano": "SOURCE"
  }
```

## ​Cookie Consent and Disabling Telemetry

 If you need to check if a user has already consented to cookies for GDPR compliance, you can specify a local storage key and value under `cookies`:

```
"integrations": {
    "cookies": {
      "key": "LOCAL STORAGE KEY",
      "value": "LOCAL STORAGE VALUE"
    }
  }
```

 If these values are set, local storage will be checked to see if the user has consented to cookies. If they have not, telemetry will be disabled. If you’d like to disable telemetry for all users, you can add the following to your `docs.json` file:

```
"integrations": {
    "telemetry": {
      "enabled": false
    }
  }
```

 If you disable telemetry, you cannot collect feedback on your documentation pages, even if you enable feedback in your dashboard.

---

# Speakeasy

> Automate SDK code samples in your API playground.

Autogenerated code snippets from Speakeasy SDKs can be integrated directly into Mintlify API reference documentation. SDK usage snippets are shown in the [interactive playground](https://mintlify.com/docs/api-playground/overview) of Mintlify-powered documentation sites. ![A Mintlify API playground with Speakeasy code snippets.](https://mintcdn.com/mintlify/f7fo9pnTEtzBD70_/images/speakeasy/mintlify-with-speakeasy-openapi.png?fit=max&auto=format&n=f7fo9pnTEtzBD70_&q=85&s=61aa5501cca4cb4156fdbed1f9fcbe03)

## ​Prerequisites

 To integrate Mintlify with Speakeasy, you’ll need the following:

- A [Mintlify documentation repository](https://mintlify.com/docs/quickstart#creating-the-repository).
- A Speakeasy-generated SDK with a configured [automated code sample URL](https://www.speakeasy.com/docs/code-samples/automated-code-sample-urls).

## ​Setting up the integration

 To integrate Speakeasy with Mintlify, you must get the API’s combined spec public URL from the registry and update your `docs.json` configuration file.

### ​Get the API’s combined spec public URL from the registry

 Navigate to your [Speakeasy Dashboard](https://app.speakeasy.com) and open the **API Registry** tab. Open the `*-with-code-samples` entry for the API. ![Screenshot of the Speakeasy API Registry page. The API Registry tab is emphasized with a red square and the number 1 and the entry for the API is emphasized with a red square and the number 2.](https://mintcdn.com/mintlify/f7fo9pnTEtzBD70_/images/speakeasy/openapi-registry-and-combined-spec.png?fit=max&auto=format&n=f7fo9pnTEtzBD70_&q=85&s=c31db82b03febfd0d6fa239c810c116f) If the entry is not labeled **Combined Spec**, ensure that the API has an [automatic code sample URL](https://www.speakeasy.com/docs/code-samples/automated-code-sample-urls) configured. From the registry entry’s page, copy the provided public URL. ![Screenshot showing the combined spec registry entry with the copy URL function emphasized with a red square.](https://mintcdn.com/mintlify/f7fo9pnTEtzBD70_/images/speakeasy/copy-combined-spec-url.png?fit=max&auto=format&n=f7fo9pnTEtzBD70_&q=85&s=7d315613202f1097255a94940cce881b)

### ​Update yourdocs.jsonconfiguration file

 Add the combined spec URL to an **Anchors** or **Tabs** section in your `docs.json` file. Add the combined spec URL to an anchor by updating the `anchor` field in your `docs.json` file as follows: docs.json

```
{
  "anchors": [
    {
      "name": "API Reference",
      // !mark
      "openapi": "SPEAKEASY_COMBINED_SPEC_URL",
      "url": "api-reference",
      "icon": "square-terminal"
    }
  ]
}
```

 Add the combined spec URL to a tab by updating the `tab` field in the `docs.json` file as follows: docs.json

```
{
  "tabs": [
    {
      "name": "API Reference",
      "url": "api-reference",
      // !mark
      "openapi": "SPEAKEASY_COMBINED_SPEC_URL"
    }
  ]
}
```

 Speakeasy-generated code snippets can now be viewed in your API docs and interacted with in the playground.

---

# Stainless

> Automate SDK code samples in your API playground.

## ​Prerequisites

- Have a [Stainless](https://app.stainless.com) account.

## ​Integrate with Stainless

 1

Set up OpenAPI decoration in Stainless.

In your `stainless.yml` config file, add `openapi.code_samples: 'mintlify'`. See the [Stainless documentation](https://app.stainless.com/docs/guides/integrate-docs) for more information.2

Publish the URL to your OpenAPI spec.

In your Stainless project:

1. Select the **Release** tab.
2. Select **Setup OpenAPI publishing**.
3. Copy the URL to your publicly accessible OpenAPI spec.

![Stainless release page with the OpenAPI spec URL highlighted with a green box.](https://mintcdn.com/mintlify/f7fo9pnTEtzBD70_/images/stainless-public-OpenAPI-spec.png?fit=max&auto=format&n=f7fo9pnTEtzBD70_&q=85&s=74e968242d6e3c42818a57f2523ecdfe)3

Add your OpenAPI spec URL to your `docs.json`.

In your `docs.json` file, add the URL from Stainless to the `openapi` field. See [OpenAPI Setup](https://mintlify.com/docs/api-playground/openapi-setup) for more information.

---

# Front

> Connect Front chat for customer support conversations.

Add the following to your `docs.json` file to add a [Front Chat](https://front.com) widget.

```
"integrations": {
    "frontchat": "CHAT_ID"
}
```

---

# Intercom

> Connect Intercom for in-app customer messaging.

Add the following to your `docs.json` file to add an [Intercom](https://www.intercom.com) widget.

```
"integrations": {
      "intercom": {
            "appId": "APP_ID"
      }
}
```

---

# Support integrations

> Integrate with support platforms for customer assistance.

[Intercom](https://mintlify.com/docs/integrations/support/intercom)[Front](https://mintlify.com/docs/integrations/support/front)

## ​Enabling support integrations

 Integrate customer support widgets into your documentation. Add the `integrations` field to your `docs.json` file with your respective app ID or chat ID. See each integration’s documentation for instructions on finding your ID.
