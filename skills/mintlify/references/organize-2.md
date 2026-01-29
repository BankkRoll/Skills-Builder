# Global settings

# Global settings

> Configure site-wide settings in docs.json.

The `docs.json` file lets you turn a collection of Markdown files into a navigable, customized documentation site. This required configuration file controls styling, navigation, integrations, and more. Think of it as the blueprint for your documentation. Settings in `docs.json` apply globally to all pages.

## ​Setting up yourdocs.json

 To get started, you only need to specify `theme`, `name`, `colors.primary`, and `navigation`. Other fields are optional and you can add them as your documentation needs grow. For the best editing experience, include the schema reference at the top of your `docs.json` file. This enables autocomplete, validation, and helpful tooltips in most code editors:

```
{
  "$schema": "https://mintlify.com/docs.json",
  "theme": "mint",
  "name": "Your Docs",
  "colors": {
    "primary": "#ff0000"
  },
  "navigation": {
    // Your navigation structure
  }
  // The rest of your configuration
}
```

## ​Reference

 This section contains the full reference for the `docs.json` file.

### ​Customization

 [​](#param-theme)themerequiredThe layout theme of your site.One of the following: `mint`, `maple`, `palm`, `willow`, `linden`, `almond`, `aspen`.See [Themes](https://mintlify.com/docs/customize/themes) for more information. [​](#param-name)namestringrequiredThe name of your project, organization, or product. [​](#param-colors)colorsobjectrequiredThe colors used in your documentation. Colors are applied differently across themes. If you only provide a primary color, it applies to all color elements.

Show Colors

[​](#param-primary)primarystring matching ^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$requiredThe primary color for your documentation. Generally used for emphasis in light mode, with some variation by theme.Must be a hex code beginning with `#`.[​](#param-light)lightstring matching ^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$The color used for emphasis in dark mode.Must be a hex code beginning with `#`.[​](#param-dark)darkstring matching ^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$The color used for buttons and hover states across both light and dark modes, with some variation by theme.Must be a hex code beginning with `#`. [​](#param-description)descriptionstringDescription of your site for SEO and AI indexing. [​](#param-logo)logostring or objectSet your logo for both light and dark mode.

Show Logo

[​](#param-light-1)lightstringrequiredPath pointing to your logo file for light mode. Include the file extension. Example: `/logo.png`[​](#param-dark-1)darkstringrequiredPath pointing to your logo file for dark mode. Include the file extension. Example: `/logo-dark.png`[​](#param-href)hrefstring (uri)The URL to redirect to when clicking the logo. If not provided, the logo links to your homepage. Example: `https://mintlify.com` [​](#param-favicon)faviconstring or objectPath to your favicon file, including the file extension. Automatically resized to appropriate favicon sizes. Can be a single file or separate files for light and dark mode. Example: `/favicon.png`

Show Favicon

[​](#param-light-2)lightstringrequiredPath to your favicon file for light mode. Include the file extension. Example: `/favicon.png`[​](#param-dark-2)darkstringrequiredPath to your favicon file for dark mode. Include the file extension. Example: `/favicon-dark.png` [​](#param-thumbnails)thumbnailsobjectThumbnail customization for social media and page previews.

Show Thumbnails

[​](#param-appearance)appearance"light" | "dark"The visual theme of your thumbnails. If not specified, thumbnails use your site’s color scheme defined by the `colors` field.[​](#param-background)backgroundstringBackground image for your thumbnails. Can be a relative path or absolute URL.[​](#param-fonts)fontsobjectFont configuration for thumbnails. Only supports Google Fonts family names.

Show Fonts

[​](#param-family)familystringrequiredFont family name, such as “Open Sans” or “Playfair Display”. Supports [Google Fonts](https://fonts.google.com) family names. [​](#param-styling)stylingobjectVisual styling configurations.

Show Styling

[​](#param-eyebrows)eyebrows"section" | "breadcrumbs"The style of the page eyebrow. Choose `section` to show the section name or `breadcrumbs` to show the full navigation path. Defaults to `section`.[​](#param-latex)latexbooleanControls whether LaTeX stylesheets are included, overriding automatic detection. By default, Mintlify automatically detects LaTeX usage in your content and loads the necessary stylesheets.

- Set to `true` to force-load LaTeX stylesheets when automatic detection fails to recognize your mathematical expressions.
- Set to `false` to prevent loading LaTeX stylesheets for improved performance if you don’t use mathematical expressions but have content that triggers false-positive detection.

[​](#param-codeblocks)codeblocks"system" | "dark" | string | objectCode block theme configuration. Defaults to `"system"`.**Simple configuration:**

- `"system"`: Match current site mode (light or dark)
- `"dark"`: Always use dark mode

**Custom theme configuration:**

- Use a string to specify a single [Shiki theme](https://shiki.style/themes) for all code blocks
- Use an object to specify separate [Shiki themes](https://shiki.style/themes) for light and dark modes

[​](#param-theme-1)themestringA single Shiki theme name to use for both light and dark modes.

```
"styling": {
  "codeblocks": {
    "theme": "dracula"
  }
}
```

[​](#param-theme-2)themeobjectSeparate themes for light and dark modes.

Show theme

[​](#param-light-3)lightstringrequiredA Shiki theme name for light mode.[​](#param-dark-3)darkstringrequiredA Shiki theme name for dark mode.

```
"styling": {
  "codeblocks": {
    "theme": {
      "light": "github-light",
      "dark": "github-dark"
    }
  }
}
```

[​](#param-languages)languagesobjectCustom language configuration for code blocks.

Show languages

[​](#param-custom)customarray of stringPaths to JSON files describing custom Shiki languages. Use this to add syntax highlighting for languages not included in Shiki’s default set.The JSON file must follow the [TextMate grammar format](https://macromates.com/manual/en/language_grammars) used by Shiki.

```
"styling": {
  "codeblocks": {
    "languages": {
      "custom": ["/languages/my-custom-language.json"]
    }
  }
}
```

 [​](#param-icons)iconsobjectIcon library settings.

Show Icons

[​](#param-library)library"fontawesome" | "lucide"requiredIcon library to use throughout your documentation. Defaults to `fontawesome`.You can only use one icon library for your project. All icon names in your documentation must come from the same library.You can specify a URL to an externally hosted icon or a path to an icon file in your project for any individual icon, regardless of the library setting. [​](#param-fonts-1)fontsobjectSet custom fonts for your documentation. The default font varies by theme.

Show Fonts

[​](#param-family-1)familystringrequiredFont family, such as “Open Sans.” Supports [Google Fonts](https://fonts.google.com) family names.[​](#param-weight)weightnumberFont weight, such as 400 or 700. Variable fonts support precise weights such as 550.[​](#param-source)sourcestring (uri)One of:

- URL to a hosted font, such as [https://mintlify-assets.b-cdn.net/fonts/Hubot-Sans.woff2](https://mintlify-assets.b-cdn.net/fonts/Hubot-Sans.woff2).
- Path to a local font file, such as `/fonts/Hubot-Sans.woff2`.

[Google Fonts](https://fonts.google.com) are loaded automatically when you specify a Google Font `family` name, so no source URL is needed.[​](#param-format)format"woff" | "woff2"Font file format. Required when using the `source` field.[​](#param-heading)headingobjectOverride font settings specifically for headings.

Show Heading

[​](#param-family-2)familystringrequiredFont family, such as “Open Sans”, “Playfair Display.” Supports [Google Fonts](https://fonts.google.com) family names.[​](#param-weight-1)weightnumberFont weight, such as 400, 700. Variable fonts support precise weights such as 550.[​](#param-source-1)sourcestring (uri)One of:

- URL to a hosted font, such as [https://mintlify-assets.b-cdn.net/fonts/Hubot-Sans.woff2](https://mintlify-assets.b-cdn.net/fonts/Hubot-Sans.woff2).
- Path to a local font file, such as `/fonts/Hubot-Sans.woff2`.

[Google Fonts](https://fonts.google.com) are loaded automatically when you specify a Google Font `family` name, so no source URL is needed.[​](#param-format-1)format"woff" | "woff2"Font file format. Required when using the `source` field.[​](#param-body)bodyobjectOverride font settings specifically for body text.

Show Body

[​](#param-family-3)familystringrequiredFont family, such as “Open Sans”, “Playfair Display.” Supports [Google Fonts](https://fonts.google.com) family names.[​](#param-weight-2)weightnumberFont weight, such as 400, 700. Variable fonts support precise weights such as 550.[​](#param-source-2)sourcestring (uri)One of:

- URL to a hosted font, such as [https://mintlify-assets.b-cdn.net/fonts/Hubot-Sans.woff2](https://mintlify-assets.b-cdn.net/fonts/Hubot-Sans.woff2).
- Path to a local font file, such as `/fonts/Hubot-Sans.woff2`.

[Google Fonts](https://fonts.google.com) are loaded automatically when you specify a Google Font `family` name, so no source URL is needed.[​](#param-format-2)format"woff" | "woff2"Font file format. Required when using the `source` field. [​](#param-appearance-1)appearanceobjectLight/dark mode toggle settings.

Show Appearance

[​](#param-default)default"system" | "light" | "dark"Default theme mode. Choose `system` to match users’ OS settings, or `light` or `dark` to force a specific mode. Defaults to `system`.[​](#param-strict)strictbooleanWhether to hide the light/dark mode toggle. Defaults to `false`. [​](#param-background-1)backgroundobjectBackground color and decoration settings.

Show Background

[​](#param-image)imagestring or objectBackground image for your site. Can be a single file or separate files for light and dark mode.

Show Image

[​](#param-light-4)lightstringrequiredPath to your background image for light mode. Include the file extension. Example: `/background.png`.[​](#param-dark-4)darkstringrequiredPath to your background image for dark mode. Include the file extension. Example: `/background-dark.png`.[​](#param-decoration)decoration"gradient" | "grid" | "windows"Background decoration for your theme.[​](#param-color)colorobjectCustom background colors for light and dark modes.

Show Color

[​](#param-light-5)lightstring matching ^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$Background color for light mode.Must be a hex code beginning with `#`.[​](#param-dark-5)darkstring matching ^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$Background color for dark mode.Must be a hex code beginning with `#`.

### ​Structure

 [​](#param-navbar)navbarobjectNavigation bar items to external links.

Show Navbar

[​](#param-links)linksarray of objectLinks to display in the navbar

Show Links

[​](#param-label)labelstringrequiredText for the link.[​](#param-href-1)hrefstring (uri)requiredLink destination. Must be a valid external URL.[​](#param-icon)iconstringThe icon to display.Options:

- [Font Awesome](https://fontawesome.com/icons) icon name, if you have the `icons.library` [property](https://mintlify.com/docs/organize/settings#param-icons) set to `fontawesome` in your `docs.json`
- [Lucide](https://lucide.dev/icons) icon name, if you have the `icons.library` [property](https://mintlify.com/docs/organize/settings#param-icons) set to `lucide` in your `docs.json`
- URL to an externally hosted icon
- Path to an icon file in your project
- SVG code wrapped in curly braces

For custom SVG icons:

1. Convert your SVG using the [SVGR converter](https://react-svgr.com/playground/).
2. Paste your SVG code into the SVG input field.
3. Copy the complete `<svg>...</svg>` element from the JSX output field.
4. Wrap the JSX-compatible SVG code in curly braces: `icon={<svg ...> ... </svg>}`.
5. Adjust `height` and `width` as needed.

[​](#param-icon-type)iconTypestringThe [Font Awesome](https://fontawesome.com/icons) icon style. Only used with Font Awesome icons.Options: `regular`, `solid`, `light`, `thin`, `sharp-solid`, `duotone`, `brands`.[​](#param-primary-1)primaryobjectPrimary button in the navbar.

Show Primary

[​](#param-type)type"button" | "github"requiredButton style. Choose `button` for a standard button with a label or `github` for a link to a GitHub repository with icon.[​](#param-label-1)labelstringrequiredButton text. Only applies when `type` is `button`.[​](#param-href-2)hrefstring (uri)requiredButton destination. Must be an external URL. If `type` is `github`, must be a GitHub repository URL. [​](#param-navigation)navigationobjectrequiredThe navigation structure of your content.

Show Navigation

[​](#param-global)globalobjectGlobal navigation elements that appear across all pages and sections.

Show Global

[​](#param-languages-1)languagesarray of objectLanguage switcher configuration for localized sites.

Show Languages

[​](#param-language)language"en" | "cn" | "zh" | "zh-Hans" | "zh-Hant" | "es" | "fr" | "ja" | "jp" | "pt" | "pt-BR" | "de" | "ko" | "it" | "ru" | "id" | "ar" | "tr"requiredLanguage code in ISO 639-1 format[​](#param-default-1)defaultbooleanWhether this is the default language.[​](#param-hidden)hiddenbooleanWhether to hide this language option by default.[​](#param-href-3)hrefstring (uri)requiredA valid path or external link to this language version of your documentation.[​](#param-versions)versionsarray of objectVersion switcher configuration for multi-version sites.

Show Versions

[​](#param-version)versionstringrequiredDisplay name of the version.Minimum length: 1[​](#param-default-2)defaultbooleanWhether this is the default version.[​](#param-hidden-1)hiddenbooleanWhether to hide this version option by default.[​](#param-href-4)hrefstring (uri)requiredURL or path to this version of your documentation.[​](#param-tabs)tabsarray of objectTop-level navigation tabs for organizing major sections.

Show Tabs

[​](#param-tab)tabstringrequiredDisplay name of the tab.Minimum length: 1[​](#param-icon-1)iconstringThe icon to display.Options:

- [Font Awesome](https://fontawesome.com/icons) icon name, if you have the `icons.library` [property](https://mintlify.com/docs/organize/settings#param-icons) set to `fontawesome` in your `docs.json`
- [Lucide](https://lucide.dev/icons) icon name, if you have the `icons.library` [property](https://mintlify.com/docs/organize/settings#param-icons) set to `lucide` in your `docs.json`
- URL to an externally hosted icon
- Path to an icon file in your project
- SVG code wrapped in curly braces

For custom SVG icons:

1. Convert your SVG using the [SVGR converter](https://react-svgr.com/playground/).
2. Paste your SVG code into the SVG input field.
3. Copy the complete `<svg>...</svg>` element from the JSX output field.
4. Wrap the JSX-compatible SVG code in curly braces: `icon={<svg ...> ... </svg>}`.
5. Adjust `height` and `width` as needed.

[​](#param-icon-type-1)iconTypestringThe [Font Awesome](https://fontawesome.com/icons) icon style. Only used with Font Awesome icons.Options: `regular`, `solid`, `light`, `thin`, `sharp-solid`, `duotone`, `brands`.[​](#param-hidden-2)hiddenbooleanWhether to hide this tab by default.[​](#param-href-5)hrefstring (uri)requiredURL or path for the tab destination.[​](#param-anchors)anchorsarray of objectAnchored links that appear prominently in the sidebar navigation.

Show Anchors

[​](#param-anchor)anchorstringrequiredDisplay name of the anchor.Minimum length: 1[​](#param-icon-2)iconstringThe icon to display.Options:

- [Font Awesome](https://fontawesome.com/icons) icon name, if you have the `icons.library` [property](https://mintlify.com/docs/organize/settings#param-icons) set to `fontawesome` in your `docs.json`
- [Lucide](https://lucide.dev/icons) icon name, if you have the `icons.library` [property](https://mintlify.com/docs/organize/settings#param-icons) set to `lucide` in your `docs.json`
- URL to an externally hosted icon
- Path to an icon file in your project
- SVG code wrapped in curly braces

For custom SVG icons:

1. Convert your SVG using the [SVGR converter](https://react-svgr.com/playground/).
2. Paste your SVG code into the SVG input field.
3. Copy the complete `<svg>...</svg>` element from the JSX output field.
4. Wrap the JSX-compatible SVG code in curly braces: `icon={<svg ...> ... </svg>}`.
5. Adjust `height` and `width` as needed.

[​](#param-icon-type-2)iconTypestringThe [Font Awesome](https://fontawesome.com/icons) icon style. Only used with Font Awesome icons.Options: `regular`, `solid`, `light`, `thin`, `sharp-solid`, `duotone`, `brands`.[​](#param-color-1)colorobjectCustom colors for the anchor.

Show Color

[​](#param-light-6)lightstring matching ^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$Anchor color for light mode.Must be a hex code beginning with `#`.[​](#param-dark-6)darkstring matching ^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$Anchor color for dark mode.Must be a hex code beginning with `#`.[​](#param-hidden-3)hiddenbooleanWhether to hide this anchor by default.[​](#param-href-6)hrefstring (uri)requiredURL or path for the anchor destination.[​](#param-dropdowns)dropdownsarray of objectDropdown menus for organizing related content.

Show Dropdowns

[​](#param-dropdown)dropdownstringrequiredDisplay name of the dropdown.Minimum length: 1[​](#param-icon-3)iconstringThe icon to display.Options:

- [Font Awesome](https://fontawesome.com/icons) icon name, if you have the `icons.library` [property](https://mintlify.com/docs/organize/settings#param-icons) set to `fontawesome` in your `docs.json`
- [Lucide](https://lucide.dev/icons) icon name, if you have the `icons.library` [property](https://mintlify.com/docs/organize/settings#param-icons) set to `lucide` in your `docs.json`
- URL to an externally hosted icon
- Path to an icon file in your project
- SVG code wrapped in curly braces

For custom SVG icons:

1. Convert your SVG using the [SVGR converter](https://react-svgr.com/playground/).
2. Paste your SVG code into the SVG input field.
3. Copy the complete `<svg>...</svg>` element from the JSX output field.
4. Wrap the JSX-compatible SVG code in curly braces: `icon={<svg ...> ... </svg>}`.
5. Adjust `height` and `width` as needed.

[​](#param-icon-type-3)iconTypestringThe [Font Awesome](https://fontawesome.com/icons) icon style. Only used with Font Awesome icons.Options: `regular`, `solid`, `light`, `thin`, `sharp-solid`, `duotone`, `brands`.[​](#param-hidden-4)hiddenbooleanWhether to hide this dropdown by default.[​](#param-href-7)hrefstring (uri)requiredURL or path for the dropdown destination.[​](#param-products)productsarray of objectProducts for organizing content into sections.

Show Products

[​](#param-product)productstringrequiredDisplay name of the product.[​](#param-description-1)descriptionstringDescription of the product.[​](#param-icon-4)iconstringThe icon to display.Options:

- [Font Awesome](https://fontawesome.com/icons) icon name, if you have the `icons.library` [property](https://mintlify.com/docs/organize/settings#param-icons) set to `fontawesome` in your `docs.json`
- [Lucide](https://lucide.dev/icons) icon name, if you have the `icons.library` [property](https://mintlify.com/docs/organize/settings#param-icons) set to `lucide` in your `docs.json`
- URL to an externally hosted icon
- Path to an icon file in your project
- SVG code wrapped in curly braces

For custom SVG icons:

1. Convert your SVG using the [SVGR converter](https://react-svgr.com/playground/).
2. Paste your SVG code into the SVG input field.
3. Copy the complete `<svg>...</svg>` element from the JSX output field.
4. Wrap the JSX-compatible SVG code in curly braces: `icon={<svg ...> ... </svg>}`.
5. Adjust `height` and `width` as needed.

[​](#param-icon-type-4)iconTypestringThe [Font Awesome](https://fontawesome.com/icons) icon style. Only used with Font Awesome icons.Options: `regular`, `solid`, `light`, `thin`, `sharp-solid`, `duotone`, `brands`.[​](#param-languages-2)languagesarray of objectLanguage switcher for [multi-language](https://mintlify.com/docs/organize/navigation#languages) sites.[​](#param-versions-1)versionsarray of objectVersion switcher for sites with multiple [versions](https://mintlify.com/docs/organize/navigation#versions).[​](#param-tabs-1)tabsarray of objectTop-level navigation [tabs](https://mintlify.com/docs/organize/navigation#tabs).[​](#param-anchors-1)anchorsarray of objectSidebar [anchors](https://mintlify.com/docs/organize/navigation#anchors).[​](#param-dropdowns-1)dropdownsarray of object[Dropdowns](https://mintlify.com/docs/organize/navigation#dropdowns) for grouping related content.[​](#param-products-1)productsarray of objectProduct switcher for sites with multiple [products](https://mintlify.com/docs/organize/navigation#products).[​](#param-groups)groupsarray of object[Groups](https://mintlify.com/docs/organize/navigation#groups) for organizing content into sections.[​](#param-pages)pagesarray of string or objectIndividual [pages](https://mintlify.com/docs/organize/navigation#pages) that make up your documentation. [​](#param-interaction)interactionobjectUser interaction settings for navigation elements.

Show Interaction

[​](#param-drilldown)drilldownbooleanControl automatic navigation behavior when selecting navigation groups. Set to `true` to force navigation to the first page when a navigation group expands. Set to `false` to prevent navigation and only expand or collapse the group. Leave unset to use the theme’s default behavior. [​](#param-metadata)metadataobjectMetadata configuration for documentation pages.

Show Metadata

[​](#param-timestamp)timestampbooleanEnable the last modified date on all pages. When enabled, all pages display the date the content was last modified. Defaults to `false`.You can override this setting on individual pages with the `timestamp` frontmatter field. See [Pages](https://mintlify.com/docs/organize/pages#last-modified-timestamp) for more information. [​](#param-footer)footerobjectFooter content and social media links.

Show Footer

[​](#param-socials)socialsobjectSocial media profiles to display in the footer. Each key is a platform name and each value is your profile URL. For example:

```
{
  "x": "https://x.com/mintlify"
}
```

Valid property names: `x`, `website`, `facebook`, `youtube`, `discord`, `slack`, `github`, `linkedin`, `instagram`, `hacker-news`, `medium`, `telegram`, `twitter`, `x-twitter`, `earth-americas`, `bluesky`, `threads`, `reddit`, `podcast`[​](#param-links-1)linksarray of objectLinks to display in the footer.

Show Links

[​](#param-header)headerstringHeader title for the column.Minimum length: 1[​](#param-items)itemsarray of objectrequiredLinks to display in the column.

Show Items

[​](#param-label-2)labelstringrequiredLink text.Minimum length: 1[​](#param-href-8)hrefstring (uri)requiredLink destination URL. [​](#param-banner)bannerobjectSite-wide banner displayed at the top of pages.

Show Banner

[​](#param-content)contentstringrequiredThe text content displayed in the banner. Supports basic MDX formatting including links, bold, and italic text. Custom components are not supported. For example:

```
{
  "content": "🚀 Banner is live! [Learn more](mintlify.com)"
}
```

[​](#param-dismissible)dismissiblebooleanWhether to show the dismiss button on the right side of the banner. Defaults to `false`. [​](#param-redirects)redirectsarray of objectRedirects for moved, renamed, or deleted pages.

Show Redirects

[​](#param-source-3)sourcestringrequiredSource path to redirect from. Example: `/old-page`[​](#param-destination)destinationstringrequiredDestination path to redirect to. Example: `/new-page`[​](#param-permanent)permanentbooleanWhether to use a permanent redirect (301). Defaults to `true`. [​](#param-contextual)contextualobjectContextual menu for AI-optimized content and integrations.

Show Contextual

[​](#param-options)optionsarray of "copy" | "view" | "chatgpt" | "claude" | "perplexity" | "mcp" | "cursor" | "vscode" | objectrequiredActions available in the contextual menu. The first option appears as the default.

- `copy`: Copy the current page as Markdown to the clipboard.
- `view`: View the current page as Markdown in a new tab.
- `chatgpt`: Send the current page content to ChatGPT.
- `claude`: Send the current page content to Claude.
- `perplexity`: Send the current page content to Perplexity.
- `mcp`: Copies your MCP server URL to the clipboard.
- `cursor`: Installs your hosted MCP server in Cursor.
- `vscode`: Installs your hosted MCP server in VSCode.

Define custom contextual menu options as objects with the following properties:

Show Custom option

[​](#param-title)titlestringrequiredDisplay title for the custom option.[​](#param-description-2)descriptionstringrequiredDescription text for the custom option.[​](#param-icon-5)iconstringIcon for the custom option. Supports icon library names, URLs, paths, or SVG code.[​](#param-href-9)hrefstring or objectrequiredLink destination for the custom option. Can be a simple URL string or an object with `base` and optional `query` parameters.Placeholder values:

- `$page`: Current page content
- `$path`: Current page path
- `$mcp`: MCP server URL

![Contextual Menu](https://mintcdn.com/mintlify/f7fo9pnTEtzBD70_/images/page-context-menu.png?fit=max&auto=format&n=f7fo9pnTEtzBD70_&q=85&s=8833b554020642ceb0495df962ae833b)The contextual menu is only available on preview and production deployments.

### ​API configurations

 [​](#param-api)apiobjectAPI documentation and interactive playground settings.

Show api

[​](#param-openapi)openapistring or array or objectOpenAPI specification files for generating API documentation. Can be a single URL/path or an array of URLs/paths.

Show openapi

[​](#param-source-4)sourcestringURL or path to your OpenAPI specification file.Minimum length: 1[​](#param-directory)directorystringDirectory to search for OpenAPI files.Do not include a leading slash.

```
"openapi": "openapi.json"
```

[​](#param-asyncapi)asyncapistring or array or objectAsyncAPI specification files for generating API documentation. Can be a single URL/path or an array of URLs/paths.

Show asyncapi

[​](#param-source-5)sourcestringURL or path to your AsyncAPI specification file.Minimum length: 1[​](#param-directory-1)directorystringDirectory to search for AsyncAPI files.Do not include a leading slash.

```
"asyncapi": "asyncapi.json"
```

[​](#param-params)paramsobjectDisplay settings for API parameters.

Show Params

[​](#param-expanded)expanded"all" | "closed"Whether to expand all parameters by default. Defaults to `closed`.[​](#param-playground)playgroundobjectAPI playground settings.

Show Playground

[​](#param-display)display"interactive" | "simple" | "none"The display mode of the API playground. Defaults to `interactive`.[​](#param-proxy)proxybooleanWhether to pass API requests through a proxy server. Defaults to `true`.[​](#param-examples)examplesobjectConfigurations for the autogenerated API examples.

Show Examples

[​](#param-languages-3)languagesarray of stringExample languages for the autogenerated API snippets. Supported languages include:

- `bash` (displayed as cURL)
- `go`
- `java`
- `javascript`
- `node` (displayed as Node.js)
- `php`
- `powershell`
- `python`
- `ruby`
- `swift`

Common aliases are also supported: `curl`, `golang`, `js`,  `nodejs`, `rb`, `sh`.[​](#param-defaults)defaults"required" | "all"Whether to show optional parameters in API examples. Defaults to `all`.[​](#param-prefill)prefillbooleanWhether to prefill the API playground with data from schema examples. When enabled, the playground automatically populates request fields with example values from your OpenAPI specification. Defaults to `false`.[​](#param-autogenerate)autogeneratebooleanWhether to generate code samples for endpoints from API specifications. Defaults to `true`. When set to `false`, only manually-written code samples (from `x-codeSamples` in OpenAPI specifications or `<RequestExample>` components in MDX) appear in the API playground.[​](#param-mdx)mdxobjectConfigurations for API pages generated from MDX files.

Show Mdx

[​](#param-auth)authobjectAuthentication configuration for MDX-based API requests.

Show Auth

[​](#param-method)method"bearer" | "basic" | "key" | "cobo"Authentication method for API requests.[​](#param-name-1)namestringAuthentication name for API requests.[​](#param-server)serverstring or arrayServer configuration for API requests.

### ​SEO and search

 [​](#param-seo)seoobjectSEO indexing configurations.

Show Seo

[​](#param-metatags)metatagsobjectMeta tags added to every page. Must be a valid key-value pair. See [common meta tags reference](https://mintlify.com/docs/optimize/seo#common-meta-tags-reference) for options.[​](#param-indexing)indexing"navigable" | "all"Specify which pages search engines should index. Choose `navigable` to index only pages that are in your `docs.json` navigation or choose `all` to index every page. Defaults to `navigable`. [​](#param-search)searchobjectSearch display settings.

Show Search

[​](#param-prompt)promptstringPlaceholder text to display in the search bar.

### ​Integrations

 [​](#param-integrations)integrationsobjectThird-party integrations.

Show Integrations

[​](#param-amplitude)amplitudeobjectAmplitude analytics integration.

Show Amplitude

[​](#param-api-key)apiKeystringrequiredYour Amplitude API key.[​](#param-clarity)clarityobjectMicrosoft Clarity integration.

Show Clarity

[​](#param-project-id)projectIdstringrequiredYour Microsoft Clarity project ID.[​](#param-clearbit)clearbitobjectClearbit data enrichment integration.

Show Clearbit

[​](#param-public-api-key)publicApiKeystringrequiredYour Clearbit API key.[​](#param-fathom)fathomobjectFathom analytics integration.

Show Fathom

[​](#param-site-id)siteIdstringrequiredYour Fathom site ID.[​](#param-frontchat)frontchatobjectFront chat integration.

Show Frontchat

[​](#param-snippet-id)snippetIdstringrequiredYour Front chat snippet ID.Minimum length: 6[​](#param-ga4)ga4objectGoogle Analytics 4 integration.

Show Ga4

[​](#param-measurement-id)measurementIdstring matching ^GrequiredYour Google Analytics 4 measurement ID.Must match pattern: ^G[​](#param-gtm)gtmobjectGoogle Tag Manager integration.

Show Gtm

[​](#param-tag-id)tagIdstring matching ^GrequiredYour Google Tag Manager tag ID.Must match pattern: ^G[​](#param-heap)heapobjectHeap analytics integration.

Show Heap

[​](#param-app-id)appIdstringrequiredYour Heap app ID.[​](#param-hightouch)hightouchobjectHightouch integration.

Show Hightouch

[​](#param-write-key)writeKeystringrequiredYour Hightouch write key.[​](#param-api-host)apiHoststringYour Hightouch API host.[​](#param-hotjar)hotjarobjectHotjar integration.

Show Hotjar

[​](#param-hjid)hjidstringrequiredYour Hotjar ID.[​](#param-hjsv)hjsvstringrequiredYour Hotjar script version.[​](#param-intercom)intercomobjectIntercom integration.

Show Intercom

[​](#param-app-id-1)appIdstringrequiredYour Intercom app ID.Minimum length: 6[​](#param-logrocket)logrocketobjectLogRocket integration.

Show Logrocket

[​](#param-app-id-2)appIdstringrequiredYour LogRocket app ID.[​](#param-mixpanel)mixpanelobjectMixpanel integration.

Show Mixpanel

[​](#param-project-token)projectTokenstringrequiredYour Mixpanel project token.[​](#param-osano)osanoobjectOsano integration.

Show Osano

[​](#param-script-source)scriptSourcestringrequiredYour Osano script source.[​](#param-pirsch)pirschobjectPirsch analytics integration.

Show Pirsch

[​](#param-id)idstringrequiredYour Pirsch ID.[​](#param-posthog)posthogobjectPostHog integration.

Show Posthog

[​](#param-api-key-1)apiKeystring matching ^phc\_requiredYour PostHog API key.Must match pattern: ^phc_[​](#param-api-host-1)apiHoststring (uri)Your PostHog API host.[​](#param-plausible)plausibleobjectPlausible analytics integration.

Show Plausible

[​](#param-domain)domainstringrequiredYour Plausible domain.[​](#param-server-1)serverstringYour Plausible server.[​](#param-segment)segmentobjectSegment integration.

Show Segment

[​](#param-key)keystringrequiredYour Segment key.[​](#param-telemetry)telemetryobjectTelemetry settings.

Show Telemetry

[​](#param-enabled)enabledbooleanWhether to enable telemetry.When set to `false`, feedback features are also disabled and do not appear on your documentation pages.[​](#param-cookies)cookiesobjectCookie settings.

Show Cookies

[​](#param-key-1)keystringKey for cookies.[​](#param-value)valuestringValue for cookies.

### ​Errors

 [​](#param-errors)errorsobjectError handling settings.

Show Errors

[​](#param-404)404object404 “Page not found” error handling.

Show 404

[​](#param-redirect)redirectbooleanWhether to automatically redirect to the home page when a page is not found. Defaults to `true`.[​](#param-title-1)titlestringCustom title for the 404 error page.[​](#param-description-3)descriptionstringCustom description for the 404 error page. Supports basic MDX formatting including links, bold, and italic text. Custom components are not supported.

## ​Examples

- Basic example
- Interactive API example
- Multi-language example

docs.json

```
{
  "$schema": "https://mintlify.com/docs.json",
  "theme": "maple",
  "name": "Example Co.",
  "description": "Example Co. is a company that provides example content and placeholder text.",
  "colors": {
    "primary": "#3B82F6",
    "light": "#F8FAFC",
    "dark": "#0F172A"
  },
  "navigation": {
    "dropdowns": [
      {
        "dropdown": "Documentation",
        "icon": "book",
        "description": "How to use the Example Co. product",
        "groups": [
          {
            "group": "Getting started",
            "pages": [
              "index",
              "quickstart"
            ]
          },
          {
            "group": "Customization",
            "pages": [
              "settings",
              "users",
              "features"
            ]
          },
          {
            "group": "Billing",
            "pages": [
              "billing/overview",
              "billing/payments",
              "billing/subscriptions"
            ]
          }
        ]
      },
      {
        "dropdown": "Changelog",
        "icon": "history",
        "description": "Updates and changes",
        "pages": [
          "changelog"
        ]
      }
    ]
  },
  "logo": {
    "light": "/logo-light.svg",
    "dark": "/logo-dark.svg",
    "href": "https://example.com"
  },
  "navbar": {
    "links": [
      {
        "label": "Community",
        "href": "https://example.com/community"
      }
    ],
    "primary": {
      "type": "button",
      "label": "Get Started",
      "href": "https://example.com/start"
    }
  },
  "footer": {
    "socials": {
      "x": "https://x.com/example",
      "linkedin": "https://www.linkedin.com/company/example",
      "github": "https://github.com/example",
      "slack": "https://example.com/community"
    },
    "links": [
      {
        "header": "Resources",
        "items": [
          {
            "label": "Customers",
            "href": "https://example.com/customers"
          },
          {
            "label": "Enterprise",
            "href": "https://example.com/enterprise"
          },
          {
            "label": "Request Preview",
            "href": "https://example.com/preview"
          }
        ]
      },
      {
        "header": "Company",
        "items": [
          {
            "label": "Careers",
            "href": "https://example.com/careers"
          },
          {
            "label": "Blog",
            "href": "https://example.com/blog"
          },
          {
            "label": "Privacy Policy",
            "href": "https://example.com/legal/privacy"
          }
        ]
      }
    ]
  },
  "integrations": {
    "ga4": {
      "measurementId": "G-XXXXXXXXXX"
    },
    "telemetry": {
      "enabled": true
    },
    "cookies": {
      "key": "example_cookie_key",
      "value": "example_cookie_value"
    }
  },
  "contextual": {
    "options": [
      "copy",
      "view",
      "chatgpt",
      "claude"
    ]
  },
  "errors": {
    "404": {
      "redirect": false,
      "title": "I can't be found",
      "description": "What ever **happened** to this _page_?"
    }
  }
}
```

docs.json

```
{
  "$schema": "https://mintlify.com/docs.json",
  "theme": "maple",
  "name": "Example Co.",
  "description": "Example Co. is a company that provides example content and placeholder text.",
  "colors": {
    "primary": "#3B82F6",
    "light": "#F8FAFC",
    "dark": "#0F172A"
  },
  "navigation": {
    "dropdowns": [
      {
        "dropdown": "Documentation",
        "icon": "book",
        "description": "How to use the Example Co. product",
        "groups": [
          {
            "group": "Getting started",
            "pages": [
              "index",
              "quickstart"
            ]
          },
          {
            "group": "Customization",
            "pages": [
              "settings",
              "users",
              "features"
            ]
          },
          {
            "group": "Billing",
            "pages": [
              "billing/overview",
              "billing/payments",
              "billing/subscriptions"
            ]
          }
        ]
      },
      {
        "dropdown": "API reference",
        "icon": "terminal",
        "description": "How to use the Example Co. API",
        "groups": [
          {
            "group": "API reference",
            "pages": [
              "api-reference/introduction"
            ]
          },
          {
            "group": "Endpoints",
            "openapi": {
              "source": "openapi.json"
            }
          }
        ]
      },
      {
        "dropdown": "Changelog",
        "icon": "history",
        "description": "Updates and changes",
        "pages": [
          "changelog"
        ]
      }
    ]
  },
  "api": {
    "playground": {
      "display": "interactive"
    },
    "examples": {
      "languages": ["javascript", "curl", "python"]
    }
  },
  "logo": {
    "light": "/logo-light.svg",
    "dark": "/logo-dark.svg",
    "href": "https://example.com"
  },
  "navbar": {
    "links": [
      {
        "label": "Community",
        "href": "https://example.com/community"
      }
    ],
    "primary": {
      "type": "button",
      "label": "Get Started",
      "href": "https://example.com/start"
    }
  },
  "footer": {
    "socials": {
      "x": "https://x.com/example",
      "linkedin": "https://www.linkedin.com/company/example",
      "github": "https://github.com/example",
      "slack": "https://example.com/community"
    },
    "links": [
      {
        "header": "Resources",
        "items": [
          {
            "label": "Customers",
            "href": "https://example.com/customers"
          },
          {
            "label": "Enterprise",
            "href": "https://example.com/enterprise"
          },
          {
            "label": "Request Preview",
            "href": "https://example.com/preview"
          }
        ]
      },
      {
        "header": "Company",
        "items": [
          {
            "label": "Careers",
            "href": "https://example.com/careers"
          },
          {
            "label": "Blog",
            "href": "https://example.com/blog"
          },
          {
            "label": "Privacy Policy",
            "href": "https://example.com/legal/privacy"
          }
        ]
      }
    ]
  },
  "integrations": {
    "ga4": {
      "measurementId": "G-XXXXXXXXXX"
    },
    "telemetry": {
      "enabled": true
    },
    "cookies": {
      "key": "example_cookie_key",
      "value": "example_cookie_value"
    }
  },
  "contextual": {
    "options": [
      "copy",
      "view",
      "chatgpt",
      "claude"
    ]
  },
  "errors": {
    "404": {
      "redirect": false,
      "title": "I can't be found",
      "description": "What ever **happened** to this _page_?"
    }
  }
}
```

docs.json

```
{
  "$schema": "https://mintlify.com/docs.json",
  "theme": "maple",
  "name": "Example Co.",
  "description": "Example Co. is a company that provides example content and placeholder text.",
  "colors": {
    "primary": "#3B82F6",
    "light": "#F8FAFC",
    "dark": "#0F172A"
  },
  "navigation": {
    "global": {
      "anchors": [
        {
          "anchor": "Documentation",
          "href": "https://mintlify.com/docs"
        },
        {
          "anchor": "Changelog",
          "href": "https://mintlify.com/docs/changelog"
        }
      ]
    },
    "languages": [
      {
        "language": "en",
        "dropdowns": [
          {
            "dropdown": "Documentation",
            "icon": "book",
            "description": "How to use the Example Co. product",
            "pages": [
              {
                "group": "Getting started",
                "pages": ["index", "quickstart"]
              },
              {
                "group": "Customization",
                "pages": ["settings", "users", "features"]
              },
              {
                "group": "Billing",
                "pages": [
                  "billing/overview",
                  "billing/payments",
                  "billing/subscriptions"
                ]
              }
            ]
          },
          {
            "dropdown": "Changelog",
            "icon": "history",
            "description": "Updates and changes",
            "pages": ["changelog"]
          }
        ]
      },
      {
        "language": "es",
        "dropdowns": [
          {
            "dropdown": "Documentación",
            "icon": "book",
            "description": "Cómo usar el producto de Example Co.",
            "pages": [
              {
                "group": "Comenzando",
                "pages": ["es/index", "es/quickstart"]
              },
              {
                "group": "Personalización",
                "pages": ["es/settings", "es/users", "es/features"]
              },
              {
                "group": "Billing",
                "pages": [
                  "es/billing/overview",
                  "es/billing/payments",
                  "es/billing/subscriptions"
                ]
              }
            ]
          },
          {
            "dropdown": "Changelog",
            "icon": "history",
            "description": "Actualizaciones y cambios",
            "pages": ["es/changelog"]
          }
        ]
      }
    ]
  },
  "logo": {
    "light": "/logo-light.svg",
    "dark": "/logo-dark.svg",
    "href": "https://example.com"
  },
  "navbar": {
    "links": [
      {
        "label": "Community",
        "href": "https://example.com/community"
      }
    ],
    "primary": {
      "type": "button",
      "label": "Get Started",
      "href": "https://example.com/start"
    }
  },
  "footer": {
    "socials": {
      "x": "https://x.com/example",
      "linkedin": "https://www.linkedin.com/company/example",
      "github": "https://github.com/example",
      "slack": "https://example.com/community"
    },
    "links": [
      {
        "header": "Resources",
        "items": [
          {
            "label": "Customers",
            "href": "https://example.com/customers"
          },
          {
            "label": "Enterprise",
            "href": "https://example.com/enterprise"
          },
          {
            "label": "Request Preview",
            "href": "https://example.com/preview"
          }
        ]
      },
      {
        "header": "Company",
        "items": [
          {
            "label": "Careers",
            "href": "https://example.com/careers"
          },
          {
            "label": "Blog",
            "href": "https://example.com/blog"
          },
          {
            "label": "Privacy Policy",
            "href": "https://example.com/legal/privacy"
          }
        ]
      }
    ]
  },
  "integrations": {
    "ga4": {
      "measurementId": "G-XXXXXXXXXX"
    },
    "telemetry": {
      "enabled": true
    },
    "cookies": {
      "key": "example_cookie_key",
      "value": "example_cookie_value"
    }
  },
  "contextual": {
    "options": ["copy", "view", "chatgpt", "claude"]
  },
  "errors": {
    "404": {
      "redirect": false,
      "title": "I can't be found",
      "description": "What ever **happened** to this _page_?"
    }
  }
}
```

## ​Upgrading frommint.json

 If your docs project uses the deprecated `mint.json` file, follow these steps to upgrade to `docs.json`. 1

Install or update the CLI

If you haven’t installed the [CLI](https://mintlify.com/docs/installation), install it now:

```
npm i -g mint
```

If you already have the CLI installed, make sure it is up to date:

```
mint update
```

2

Create your docs.json file

In your docs repository, run:

```
mint upgrade
```

This command creates a `docs.json` file from your existing `mint.json`. Review the generated file to ensure all settings are correct.3

Delete your mint.json file

After verifying your `docs.json` is configured properly, you can safely delete your old `mint.json` file.
