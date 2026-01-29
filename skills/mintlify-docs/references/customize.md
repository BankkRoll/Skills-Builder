# Custom 404 page and more

# Custom 404 page

> Customize the title and description of your 404 error page.

All 404 pages automatically suggest relevant pages based on the requested URL. If users land on a 404 page, an agent analyzes the path and retrieves semantically related pages from your documentation to help them find what they’re looking for. You can customize the title and description of the 404 error page. Use the description to add helpful links or guidance.

## ​Configuration

 Configure your 404 page in the `errors.404` section of your `docs.json` file:

```
"errors": {
  "404": {
    "redirect": false,
    "title": "I can't be found",
    "description": "What ever **happened** to this _page_?"
  }
}
```

## ​Parameters

 [​](#param-redirect)redirectbooleanWhether to automatically redirect to the home page when a page is not found.Set to `true` to redirect to the home page.Set to `false` to show the custom 404 page. [​](#param-title)titlestringCustom title for the 404 error page. This replaces the default “Page not found” heading. [​](#param-description)descriptionstringCustom description for the 404 error page. Supports Markdown formatting.

---

# Custom domain

> Host your documentation on a custom domain.

To host your documentation on a custom domain:

1. Add your domain in your dashboard.
2. Configure DNS settings on your domain provider.
3. Allow time for DNS to propagate and TLS certificates to be automatically provisioned.

 Looking to set up a subpath like `example.com/docs`? See [/docs subpath](https://mintlify.com/docs/deploy/docs-subpath).

## ​Add your custom domain

1. Navigate to the [Custom domain setup](https://dashboard.mintlify.com/settings/deployment/custom-domain) page in your dashboard.
2. Enter your domain name. For example, `docs.example.com` or `www.example.com`.
3. Click **Add domain**.

 ![The Custom domain setup page showing the field to enter your custom domain URL.](https://mintcdn.com/mintlify/Br3zUjMmXXI3_HaI/images/domain/add-custom-domain-light.png?fit=max&auto=format&n=Br3zUjMmXXI3_HaI&q=85&s=d8c8e3f4b035a6714614e52b173bf3f6)![The Custom domain setup page showing the field to enter your custom domain URL.](https://mintcdn.com/mintlify/Br3zUjMmXXI3_HaI/images/domain/add-custom-domain-dark.png?fit=max&auto=format&n=Br3zUjMmXXI3_HaI&q=85&s=d6b5b7f57c57ff72142613135e77cc98)

## ​Configure your DNS

1. On your domain provider’s website, navigate to your domain’s DNS settings.
2. Create a new DNS record with the following values:

```
CNAME | docs | cname.mintlify-dns.com.
```

 Each domain provider has different ways to add DNS records. Refer to your domain provider’s documentation for specific instructions.

### ​DNS propagation

 DNS changes typically take 1-24 hours to propagate globally, though it can take up to 48 hours in some cases. You can verify your DNS is configured correctly using [DNSChecker](https://dnschecker.org). Once your DNS records are active, your documentation is first accessible via HTTP. HTTPS is available after Vercel provisions your TLS certificate.

### ​Automatic TLS provisioning

 Once your DNS records propagate and resolve correctly, Vercel automatically provisions a free SSL/TLS certificate for your domain using Let’s Encrypt. This typically completes within a few hours of DNS propagation, though it can take up to 24 hours in rare cases. Certificates are automatically renewed before expiration.

### ​CAA records

 If your domain uses CAA (Certification Authority Authorization) records, you must authorize Let’s Encrypt to issue certificates for your domain. Add the following CAA record to your DNS settings:

```
0 issue "letsencrypt.org"
```

### ​Reserved paths

 The `/.well-known/acme-challenge` path is reserved for certificate validation and cannot be redirected or rewritten. If you have configured redirects or rewrites for this path, certificate provisioning will fail.

### ​Provider-specific settings

Vercel verification

If Vercel is your domain provider, you must add a verification `TXT` record. This information appears on your dashboard after submitting your custom domain, and is emailed to you.

Cloudflare encryption mode

If Cloudflare is your DNS provider, you must enable the “Full (strict)” mode for the SSL/TLS encryption setting. Additionally, disable “Always Use HTTPS” in your Edge Certificates settings. Cloudflare’s HTTPS redirect will block Let’s Encrypt from validating your domain during certificate provisioning.

## ​Set a canonical URL

 After configuring your DNS, set a canonical URL to ensure search engines index your preferred domain. A canonical URL tells search engines which version of your documentation is the primary one. This improves SEO when your documentation is accessible from multiple URLs and prevents issues with duplicate content. Add the `canonical` meta tag to your `docs.json`:

```
"seo": {
    "metatags": {
        "canonical": "https://www.your-custom-domain-here.com"
    }
}
```

 Replace `https://www.your-custom-domain-here.com` with your actual custom domain. For example, if your custom domain is `docs.mintlify.com`, you would use:

```
"seo": {
    "metatags": {
        "canonical": "https://docs.mintlify.com"
    }
}
```

---

# Custom scripts

> Add custom JavaScript and CSS to fully customize the look and feel of your documentation.

Use CSS to style HTML elements or add custom CSS and JavaScript to fully customize the look and feel of your documentation.

## ​Styling with Tailwind CSS

 Use Tailwind CSS v3 to style HTML elements. You can control layout, spacing, colors, and other visual properties. Some common classes are:

- `w-full` - Full width
- `aspect-video` - 16:9 aspect ratio
- `rounded-xl` - Large rounded corners
- `block`, `hidden` - Display control
- `dark:hidden`, `dark:block` - Dark mode visibility

 Tailwind CSS arbitrary values are not supported. For custom values, use the `style` prop instead.

```
<img style={{ width: '350px', margin: '12px auto' }} src="/path/image.jpg" />
```

 Using the `style` prop can cause a layout shift on page load, especially on custom mode pages. Use Tailwind CSS classes or custom CSS files instead to avoid shifts or flickering.

## ​Custom CSS

 Add CSS files to your repository and their defined class names will be applied and available in all of your MDX files.

### ​Addingstyle.css

 For example, you can add the following `style.css` file to customize the styling of the navbar and footer.

```
#navbar {
  background: #fffff2;
  padding: 1rem;
}

footer {
  margin-top: 2rem;
}
```

### ​Using identifiers and selectors

 Mintlify has a set of common identifiers and selectors to help you tag important elements of the UI. Use inspect element to find references to elements you’re looking to customize.

Identifiers

- APIPlaygroundInput: `api-playground-input`
- AssistantEntry: `assistant-entry`
- AssistantEntryMobile: `assistant-entry-mobile`
- Banner: `banner`
- BodyContent: `body-content`
- ChangelogFilters: `changelog-filters`
- ChangelogFiltersContent: `changelog-filters-content`
- ChatAssistantSheet: `chat-assistant-sheet`
- ChatAssistantTextArea: `chat-assistant-textarea`
- ContentArea: `content-area`
- ContentContainer: `content-container`
- ContentSideLayout: `content-side-layout`
- FeedbackForm: `feedback-form`
- FeedbackFormCancel: `feedback-form-cancel`
- FeedbackFormInput: `feedback-form-input`
- FeedbackFormSubmit: `feedback-form-submit`
- FeedbackThumbsDown: `feedback-thumbs-down`
- FeedbackThumbsUp: `feedback-thumbs-up`
- Footer: `footer`
- Header: `header`
- NavBarTransition: `navbar-transition`
- NavigationItems: `navigation-items`
- Navbar: `navbar`
- PageContextMenu: `page-context-menu`
- PageContextMenuButton: `page-context-menu-button`
- PageTitle: `page-title`
- Pagination: `pagination`
- Panel: `panel`
- RequestExample: `request-example`
- ResponseExample: `response-example`
- SearchBarEntry: `search-bar-entry`
- SearchBarEntryMobile: `search-bar-entry-mobile`
- SearchInput: `search-input`
- Sidebar: `sidebar`
- SidebarContent: `sidebar-content`
- TableOfContents: `table-of-contents`
- TableOfContentsContent: `table-of-contents-content`
- TableOfContentsLayout: `table-of-contents-layout`
- TopbarCtaButton: `topbar-cta-button`

Selectors

- Accordion: `accordion`
- AccordionGroup: `accordion-group`
- AlmondLayout: `almond-layout`
- AlmondNavBottomSection: `almond-nav-bottom-section`
- AlmondNavBottomSectionDivider: `almond-nav-bottom-section-divider`
- Anchor: `nav-anchor`
- Anchors: `nav-anchors`
- APISection: `api-section`
- APISectionHeading: `api-section-heading`
- APISectionHeadingSubtitle: `api-section-heading-subtitle`
- APISectionHeadingTitle: `api-section-heading-title`
- Callout: `callout`
- Card: `card`
- CardGroup: `card-group`
- ChatAssistantSheet: `chat-assistant-sheet`
- ChatAssistantSheetHeader: `chat-assistant-sheet-header`
- ChatAssistantSheetContent: `chat-assistant-sheet-content`
- ChatAssistantInput: `chat-assistant-input`
- ChatAssistantSendButton: `chat-assistant-send-button`
- CodeBlock: `code-block`
- CodeGroup: `code-group`
- Content: `mdx-content`
- DropdownTrigger: `nav-dropdown-trigger`
- DropdownContent: `nav-dropdown-content`
- DropdownItem: `nav-dropdown-item`
- DropdownItemTextContainer: `nav-dropdown-item-text-container`
- DropdownItemTitle: `nav-dropdown-item-title`
- DropdownItemDescription: `nav-dropdown-item-description`
- DropdownItemIcon: `nav-dropdown-item-icon`
- Expandable: `expandable`
- Eyebrow: `eyebrow`
- FeedbackToolbar: `feedback-toolbar`
- Field: `field`
- Frame: `frame`
- Icon: `icon`
- Link: `link`
- LoginLink: `login-link`
- Logo: `nav-logo`
- Mermaid: `mermaid`
- MethodNavPill: `method-nav-pill`
- MethodPill: `method-pill`
- NavBarLink: `navbar-link`
- NavTagPill: `nav-tag-pill`
- NavTagPillText: `nav-tag-pill-text`
- OptionDropdown: `option-dropdown`
- PaginationNext: `pagination-next`
- PaginationPrev: `pagination-prev`
- PaginationTitle: `pagination-title`
- Panel: `panel`
- SidebarGroup: `sidebar-group`
- SidebarGroupIcon: `sidebar-group-icon`
- SidebarGroupHeader: `sidebar-group-header`
- SidebarNavGroupDivider: `sidebar-nav-group-divider`
- SidebarTitle: `sidebar-title`
- Step: `step`
- Steps: `steps`
- Tab: `tab`
- Tabs: `tabs`
- TabsBar: `nav-tabs`
- TabsBarItem: `nav-tabs-item`
- TableOfContents: `toc`
- TableOfContentsItem: `toc-item`
- Tooltip: `tooltip`
- TopbarRightContainer: `topbar-right-container`
- TryitButton: `tryit-button`
- Update: `update`

 References and the styling of common elements are subject to change as the platform evolves. Please use custom styling with caution.

## ​Custom JavaScript

 Custom JS allows you to add custom executable code globally. It is the equivalent of adding a `<script>` tag with JS code into every page.

### ​Adding custom JavaScript

 Any `.js` file inside the content directory of your docs will be included in every documentation page. For example, you can add the following `ga.js` file to enable [Google Analytics](https://marketingplatform.google.com/about/analytics) across the entire documentation.

```
window.dataLayer = window.dataLayer || [];
function gtag() {
  dataLayer.push(arguments);
}
gtag('js', new Date());

gtag('config', 'TAG_ID');
```

 Please use with caution to not introduce security vulnerabilities.

---

# Fonts

> Customize typography with Google Fonts or self-hosted fonts.

Set a custom font for your entire site or separately for headings and body text. Use Google Fonts, local font files, or externally hosted fonts. The default font varies by theme. Fonts are controlled by the [fonts property](https://mintlify.com/docs/organize/settings#param-fonts) in your `docs.json`.

## ​Google Fonts

 Mintlify automatically loads [Google Fonts](https://fonts.google.com) when you specify a font family name in your `docs.json`. docs.json

```
"fonts": {
  "family": "Inter"
}
```

## ​Local fonts

 To use local fonts, place your font files in your project directory and reference them in your `docs.json` configuration.

### ​Setting up local fonts

 1

Add font files to your project

For example, create a `fonts` directory and add your font files:

```
your-project/
├── fonts/
│   ├── InterDisplay-Regular.woff2
│   └── InterDisplay-Bold.woff2
├── docs.json
└── ...
```

2

Configure fonts in docs.json

Reference your local fonts using relative paths from your project root:docs.json

```
{
  "fonts": {
    "family": "InterDisplay",
    "source": "/fonts/InterDisplay-Regular.woff2",
    "format": "woff2",
    "weight": 400
  }
}
```

### ​Local fonts for headings and body

 Configure separate local fonts for headings and body text in your `docs.json`: docs.json

```
{
  "fonts": {
    "heading": {
      "family": "InterDisplay",
      "source": "/fonts/InterDisplay-Bold.woff2",
      "format": "woff2",
      "weight": 700
    },
    "body": {
      "family": "InterDisplay",
      "source": "/fonts/InterDisplay-Regular.woff2",
      "format": "woff2",
      "weight": 400
    }
  }
}
```

## ​Externally hosted fonts

 Use externally hosted fonts by referencing a font source URL in your `docs.json`: docs.json

```
{
  "fonts": {
    "family": "Hubot Sans",
    "source": "https://mintlify-assets.b-cdn.net/fonts/Hubot-Sans.woff2",
    "format": "woff2",
    "weight": 400
  }
}
```

## ​Font configuration reference

 [​](#param-fonts)fontsobjectFont configuration for your documentation.

Show Fonts

[​](#param-family)familystringrequiredFont family name, such as “Inter” or “Playfair Display”.[​](#param-weight)weightnumberFont weight, such as 400 or 700. Variable fonts support precise weights such as 550.[​](#param-source)sourcestring (uri)URL to your font source, such as `https://mintlify-assets.b-cdn.net/fonts/Hubot-Sans.woff2`, or path to your local font file, such as `/assets/fonts/InterDisplay.woff2`. Google Fonts are loaded automatically when you specify a Google Font `family` name, so no source URL is needed.[​](#param-format)format'woff' | 'woff2'Font file format. Required when using the `source` field.[​](#param-heading)headingobjectOverride font settings specifically for headings.

Show Heading

[​](#param-family-1)familystringrequiredFont family name for headings.[​](#param-weight-1)weightnumberFont weight for headings.[​](#param-source-1)sourcestring (uri)URL to your font source, such as `https://mintlify-assets.b-cdn.net/fonts/Hubot-Sans.woff2`, or path to your local font file for headings. Google Fonts are loaded automatically when you specify a Google Font `family` name, so no source URL is needed.[​](#param-format-1)format'woff' | 'woff2'Font file format for headings. Required when using the `source` field.[​](#param-body)bodyobjectOverride font settings specifically for body text.

Show Body

[​](#param-family-2)familystringrequiredFont family name for body text.[​](#param-weight-2)weightnumberFont weight for body text.[​](#param-source-2)sourcestring (uri)URL to your font source, such as `https://mintlify-assets.b-cdn.net/fonts/Hubot-Sans.woff2`, or path to your local font file for body text. Google Fonts are loaded automatically when you specify a Google Font `family` name, so no source URL is needed.[​](#param-format-2)format'woff' | 'woff2'Font file format for body text. Required when using the `source` field.

---

# React

> Build interactive and reusable elements with React components.

[React components](https://react.dev) are a powerful way to create interactive and reusable elements in your documentation.

## ​Using React components

 You can build React components directly in your MDX files using [React hooks](https://react.dev/reference/react/hooks).

### ​Example

 This example declares a `Counter` component and then uses it with `<Counter />`.

```
export const Counter = () => {
  const [count, setCount] = useState(0)

  const increment = () => setCount(count + 1)
  const decrement = () => setCount(count - 1)

  return (
  <div className="flex items-center justify-center">
      <div className="flex items-center rounded-xl overflow-hidden border border-zinc-950/20 dark:border-white/20">
        <button
          onClick={decrement}
          className="flex items-center justify-center h-8 w-8 text-zinc-950/80 dark:text-white/80 border-r border-zinc-950/20 dark:border-white/20"
          aria-label="Decrease"
        >
          -
        </button>

        <div className="flex text-sm items-center justify-center h-8 px-6 text-zinc-950/80 dark:text-white/80 font-medium min-w-[4rem] text-center">
          {count}
        </div>

        <button
          onClick={increment}
          className="flex items-center justify-center h-8 w-8 text-zinc-950/80 dark:text-white/80 border-l border-zinc-950/20 dark:border-white/20"
          aria-label="Increase"
        >
          +
        </button>
      </div>
    </div>
  )
}

<Counter />
```

 The counter renders as an interactive React component. 0

## ​Importing components

 To import React components in your MDX files, the component files must be located in the `/snippets/` folder. Learn more about [reusable snippets](https://mintlify.com/docs/create/reusable-snippets).

### ​Example

 This example declares a `ColorGenerator` component that uses multiple React hooks and then uses it in an MDX file. Create `color-generator.jsx` file in the `snippets` folder: /snippets/color-generator.jsx

```
export const ColorGenerator = () => {
  const [hue, setHue] = useState(180)
  const [saturation, setSaturation] = useState(50)
  const [lightness, setLightness] = useState(50)
  const [colors, setColors] = useState([])

  useEffect(() => {
    const newColors = []
    for (let i = 0; i < 5; i++) {
      const l = Math.max(10, Math.min(90, lightness - 20 + i * 10))
      newColors.push(`hsl(${hue}, ${saturation}%, ${l}%)`)
    }
    setColors(newColors)
  }, [hue, saturation, lightness])

  const copyToClipboard = (color) => {
    navigator.clipboard
      .writeText(color)
      .then(() => {
        console.log(`Copied ${color} to clipboard!`)
      })
      .catch((err) => {
        console.error("Failed to copy: ", err)
      })
  }

  return (
    <div className="p-4 border dark:border-zinc-950/80 rounded-xl not-prose">
      <div className="space-y-4">
        <div className="space-y-2">
          <label className="block text-sm text-zinc-950/70 dark:text-white/70">
            Hue: {hue}°
            <input
              type="range"
              min="0"
              max="360"
              value={hue}
              onChange={(e) => setHue(Number.parseInt(e.target.value))}
              className="w-full h-2 bg-zinc-950/20 rounded-lg appearance-none cursor-pointer dark:bg-white/20 mt-1"
              style={{
                background: `linear-gradient(to right,
                  hsl(0, ${saturation}%, ${lightness}%),
                  hsl(60, ${saturation}%, ${lightness}%),
                  hsl(120, ${saturation}%, ${lightness}%),
                  hsl(180, ${saturation}%, ${lightness}%),
                  hsl(240, ${saturation}%, ${lightness}%),
                  hsl(300, ${saturation}%, ${lightness}%),
                  hsl(360, ${saturation}%, ${lightness}%))`,
              }}
            />
          </label>

          <label className="block text-sm text-zinc-950/70 dark:text-white/70">
            Saturation: {saturation}%
            <input
              type="range"
              min="0"
              max="100"
              value={saturation}
              onChange={(e) => setSaturation(Number.parseInt(e.target.value))}
              className="w-full h-2 bg-zinc-950/20 rounded-lg appearance-none cursor-pointer dark:bg-white/20 mt-1"
              style={{
                background: `linear-gradient(to right,
                  hsl(${hue}, 0%, ${lightness}%),
                  hsl(${hue}, 50%, ${lightness}%),
                  hsl(${hue}, 100%, ${lightness}%))`,
              }}
            />
          </label>

          <label className="block text-sm text-zinc-950/70 dark:text-white/70">
            Lightness: {lightness}%
            <input
              type="range"
              min="0"
              max="100"
              value={lightness}
              onChange={(e) => setLightness(Number.parseInt(e.target.value))}
              className="w-full h-2 bg-zinc-950/20 rounded-lg appearance-none cursor-pointer dark:bg-white/20 mt-1"
              style={{
                background: `linear-gradient(to right,
                  hsl(${hue}, ${saturation}%, 0%),
                  hsl(${hue}, ${saturation}%, 50%),
                  hsl(${hue}, ${saturation}%, 100%))`,
              }}
            />
          </label>
        </div>

        <div className="flex space-x-1">
          {colors.map((color, idx) => (
            <div
              key={idx}
              className="h-16 rounded flex-1 cursor-pointer transition-transform hover:scale-105"
              style={{ backgroundColor: color }}
              title={`Click to copy: ${color}`}
              onClick={() => copyToClipboard(color)}
            />
          ))}
        </div>

        <div className="text-sm font-mono text-zinc-950/70 dark:text-white/70">
          <p>
            Base color: hsl({hue}, {saturation}%, {lightness}%)
          </p>
        </div>
      </div>
    </div>
  )
}
```

 Import the `ColorGenerator` component and use it in an MDX file:

```
import { ColorGenerator } from "/snippets/color-generator.jsx"

<ColorGenerator />
```

 The color generator renders as an interactive React component. Hue: 165°Saturation: 84%Lightness: 31%Base color: hsl(165, 84%, 31%)

## ​Considerations

Client-side rendering impact

React hook components render on the client-side, which has several implications:

- **SEO**: Search engines might not fully index dynamic content.
- **Initial load**: Visitors may experience a flash of loading content before components render.
- **Accessibility**: Ensure dynamic content changes are announced to screen readers.

Performance best practices

- **Optimize dependency arrays**: Include only necessary dependencies in your `useEffect` dependency arrays.
- **Memoize complex calculations**: Use `useMemo` or `useCallback` for expensive operations.
- **Reduce re-renders**: Break large components into smaller ones to prevent cascading re-renders.
- **Lazy loading**: Consider lazy loading complex components to improve initial page load time.

---

# Themes

> Choose the appearance of your documentation.

Core Concepts

# Themes

Customize the appearance of your documentation

Configure [theme](https://mintlify.com/docs/organize/settings#param-theme) in docs.json using one of the following themes.
[Mint"mint"Classic documentation theme with time-tested layouts and familiar navigation.See preview](https://mint.mintlify.app)[Maple"maple"Modern, clean aesthetics perfect for AI and SaaS products.See preview](https://maple.mintlify.app)[Palm"palm"Sophisticated fintech theme with deep customization for enterprise documentation.See preview](https://palm.mintlify.app)[Willow"willow"Stripped-back essentials for distraction-free documentation.See preview](https://willow.mintlify.app)[Linden"linden"Retro terminal vibes with monospace fonts for that 80s hacker aesthetic.See preview](https://linden.mintlify.app)[Almond"almond"Card-based organization meets minimalist design for intuitive navigation.See preview](https://almond.mintlify.app)[Aspen"aspen"Modern documentation crafted for complex navigation and custom components.See preview](https://aspen.mintlify.app)
