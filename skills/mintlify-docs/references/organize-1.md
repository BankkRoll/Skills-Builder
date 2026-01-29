# Hidden page example and more

# Hidden page example

> Common use cases for hidden pages.

This page is hidden! It is not included in the `docs.json` navigation so you can only access it by its URL. See [Hidden pages](https://mintlify.com/docs/organize/hidden-pages) for more information.

## ​Common use cases for hidden pages

 By default, hidden pages are publicly accessible, but not discoverable through the navigation. If you want to restrict access to a hidden page, you must configure [authentication](https://mintlify.com/docs/deploy/authentication-setup).

- **Beta documentation**: Information that can be public, but should not be discoverable through the navigation.
- **Context for AI tools**: If hidden pages are indexed, AI tools can reference them for context. Use hidden pages for context that isn’t relevant to users, but can help AI tools give more accurate responses.
- **Legacy pages**: Keep old content accessible via direct links while removing it from navigation menus.
- **Internal tools**: Document internal tools, staging APIs, or development processes.

## ​Examples

### ​AI context

```
---
title: "Context for API version"
description: "This page is context for AI tools responding to questions about API versions"
---

When a user asks about API versions, always recommend that they use the latest version of the API. Never generate responses for versions older than 1.0.4.
```

### ​Internal API endpoint

```
---
title: "Internal API endpoint"
description: "This page is a hidden page that documents an internal API endpoint"
---

```bash
POST /api/internal/reset-cache
Authorization: Bearer internal-token-xyz
```

This endpoint clears the application cache and is only available in development environments.

<Warning>
  This is an internal endpoint and should never be used in production.
</Warning>
```

---

# Hidden pages

> Hide pages from your navigation while keeping them accessible.

Hidden pages are not included in your site’s navigation but remain publicly accessible to anyone who knows their URL. Use hidden pages for content that you want to be accessible on your site or referenced as context for AI tools, but not discoverable through the navigation. For content requiring strict access control, you must configure [authentication](https://mintlify.com/docs/deploy/authentication-setup). To restrict pages to specific groups of users, configure [group-based access control](https://mintlify.com/docs/deploy/authentication-setup#control-access-with-groups).

## ​Hiding a page

 To hide a page, remove it from your navigation structure. Any pages that are not included in your `docs.json` navigation are hidden. Hidden pages use the same URL structure as regular pages based on their file path. For example,  `guides/hidden-page.mdx` would be accessible at `docs.yoursite.com/guides/hidden-page`. See an [example of a hidden page](https://mintlify.com/docs/organize/hidden-page-example). Some navigation elements like sidebars, dropdowns, and tabs may appear empty or shift layout on hidden pages.

## ​Hiding a group of pages

 A group of pages is hidden if the `hidden` property is set to `true` in your `docs.json` file:

```
"groups": [
  {
    "group": "Getting started",
    "hidden": true,
    "pages": [
      "index",
      "quickstart"
    ]
  },
  {
    "group": "Guides",
    "pages": [
      "guides/hidden-page.mdx",
      "guides/hidden-groups.mdx"
    ]
  }
]
```

 In this example, the `Getting started` group is hidden, but the `Guides` group is visible.

### ​Hiding a tab

 You can also hide a tab by adding the `hidden` property to your `docs.json` file:

```
"tabs": [
  {
    "tab": "Home",
    "hidden": true,
    "pages": [
      "index",
      "quickstart"
    ]
  }
]
```

## ​Search, SEO, and AI indexing

 By default, hidden pages are excluded from indexing for search engines, internal search within your docs, and as context for the AI assistant. To include hidden pages in search results and as context for the assistant, add the `seo` property to your `docs.json`:

```
"seo": {
    "indexing": "all"
}
```

 To exclude a specific page, add `noindex: true` to its frontmatter.

---

# Exclude files from publishing

> Exclude specific files and directories from your published documentation with a .mintignore file.

The `.mintignore` file allows you to exclude specific files and directories in your documentation repository from being processed and published to your documentation site. Use `.mintignore` to keep drafts, internal notes, and source files out of your public documentation while maintaining them in your repository.

## ​Create a .mintignore file

 Create a `.mintignore` file in the root of your docs directory. This file uses the same pattern syntax as `.gitignore`. .mintignore

```
# Exclude draft documents
drafts/
*.draft.mdx

# Exclude internal documentation
internal/

# Exclude specific files
private-notes.md
```

 When Mintlify builds your documentation, it reads the `.mintignore` file and excludes any matching files or directories from processing. Excluded files:

- Don’t appear in your published documentation.
- Aren’t indexed for search.
- Aren’t accessible to visitors.
- Are ignored by [broken link checks](https://mintlify.com/docs/installation#find-broken-links). Links that point to ignored files are broken.

## ​Default ignored patterns

 Mintlify automatically ignores the following directories and files without requiring any configuration:

- `.git`
- `.github`
- `.claude`
- `.agents`
- `.idea`
- `node_modules`
- `README.md`
- `LICENSE.md`
- `CHANGELOG.md`
- `CONTRIBUTING.md`

 You don’t need to add these to your `.mintignore` file. Unlike [hidden pages](https://mintlify.com/docs/organize/hidden-pages), files excluded by `.mintignore`
are completely removed from your site and cannot be accessed by URL.

## ​Pattern syntax

 The `.mintignore` file follows `.gitignore` syntax. Some common patterns include:

| Pattern | Description |
| --- | --- |
| drafts/ | Excludes the entiredraftsdirectory |
| *.draft.mdx | Excludes all files ending in.draft.mdx |
| private-notes.md | Excludes a specific file |
| **/internal/** | Excludes anyinternaldirectory at any level |
| !important.mdx | Negates a previous pattern (includes the file) |

---

# Navigation

> Design information architecture that aligns with user needs.

The [navigation](https://mintlify.com/docs/organize/settings#param-navigation) property in `docs.json` controls the structure and information hierarchy of your documentation. With proper navigation configuration, you can organize your content so that users can find exactly what they’re looking for. Choose one primary organizational pattern at the root level of your navigation. Once you’ve chosen your primary pattern, you can nest other navigation elements within it.

## ​Pages

 Pages are the most fundamental navigation component. Each page is an MDX file in your documentation repository. ![Decorative graphic of pages.](https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/navigation/pages-light.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=d9531be8cc28553992a6513ff09fc6ed) ![Decorative graphic of pages.](https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/navigation/pages-dark.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=ec51691241465e13d49afafcd30748f8) In the `navigation` object, `pages` is an array where each entry must reference the path to a [page file](https://mintlify.com/docs/organize/pages).

```
{
  "navigation": {
    "pages": [
      "settings",
      "pages",
      "navigation",
      "themes",
      "custom-domain"
    ]
  }
}
```

## ​Groups

 Use groups to organize your sidebar navigation into sections. Groups can be nested within each other, labeled with tags, and styled with icons. ![Decorative graphic of groups.](https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/navigation/groups-light.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=393243b71cd60407c0ea883359592699) ![Decorative graphic of groups.](https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/navigation/groups-dark.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=834d116249fcd1484808f1a534ea2892) In the `navigation` object, `groups` is an array where each entry is an object that requires a `group` field and a `pages` field. The `icon`, `tag`, and `expanded` fields are optional.

```
{
  "navigation": {
    "groups": [
      {
        "group": "Getting started",
        "icon": "play",
        "pages": [
          "quickstart",
          {
            "group": "Editing",
            "expanded": false,
            "icon": "pencil",
            "pages": [
              "installation",
              "editor"
            ]
          }
        ]
      },
      {
        "group": "Writing content",
        "icon": "notebook-text",
        "tag": "NEW",
        "pages": [
          "writing-content/page",
          "writing-content/text"
        ]
      }
    ]
  }
}
```

### ​Default expanded state

 Use the `expanded` property to control the default state of a nested group in the navigation sidebar.

- `expanded: true`: Group is expanded by default.
- `expanded: false` or omitted: Group is collapsed by default.

 The `expanded` property only affects nested groups—groups within groups. Top-level groups are always expanded and cannot be collapsed.

```
{
  "group": "Getting started",
  "pages": [
    "quickstart",
    {
      "group": "Advanced",
      "expanded": false,
      "pages": ["installation", "configuration"]
    }
  ]
}
```

## ​Tabs

 Tabs create distinct sections of your documentation with separate URL paths. Tabs create a horizontal navigation bar at the top of your documentation that lets users switch between sections. ![Decorative graphic of a tab navigation.](https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/navigation/tabs-light.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=aeec785d0771a3a7a87d941e318bf8e7) ![Decorative graphic of a tab navigation.](https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/navigation/tabs-dark.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=20637c7abbe07ee7b2c41c4df26d2ffd) In the `navigation` object, `tabs` is an array where each entry is an object that requires a `tab` field and can contain other navigation fields such as groups, pages, icons, or links to external pages.

```
{
  "navigation": {
    "tabs": [
      {
        "tab": "API reference",
        "icon": "square-terminal",
        "pages": [
          "api-reference/get",
          "api-reference/post",
          "api-reference/delete"
        ]
      },
      {
        "tab": "SDKs",
        "icon": "code",
        "pages": [
          "sdk/fetch",
          "sdk/create",
          "sdk/delete"
        ]
      },
      {
        "tab": "Blog",
        "icon": "newspaper",
        "href": "https://external-link.com/blog"
      }
    ]
  }
}
```

### ​Menus

 Menus add dropdown navigation items to a tab. Use menus to help users go directly to specific pages within a tab. In the `navigation` object, `menu` is an array where each entry is an object that requires an `item` field and can contain other navigation fields such as groups, pages, icons, or links to external pages. Menu items can only contain groups, pages, and external links.

```
{
  "navigation": {
    "tabs": [
      {
        "tab": "Developer tools",
        "icon": "square-terminal",
        "menu": [
          {
            "item": "API reference",
            "icon": "rocket",
            "groups": [
              {
                "group": "Core endpoints",
                "icon": "square-terminal",
                "pages": [
                  "api-reference/get",
                  "api-reference/post",
                  "api-reference/delete"
                ]
              }
            ]
          },
          {
            "item": "SDKs",
            "icon": "code",
            "description": "SDKs are used to interact with the API.",
            "pages": [
              "sdk/fetch",
              "sdk/create",
              "sdk/delete"
            ]
          }
        ]
      }
    ]
  }
}
```

## ​Anchors

 Anchors add persistent navigation items to the top of your sidebar. Use anchors to section your content, provide quick access to external resources, or create prominent calls to action. ![Decorative graphic of an anchor navigation.](https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/navigation/anchors-light.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=e66255f62fc5d17ca135f21f84ed9325) ![Decorative graphic of an anchor navigation.](https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/navigation/anchors-dark.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=734e33b5fd52071d6f4019b273f2a0e8) In the `navigation` object, `anchors` is an array where each entry is an object that requires an `anchor` field and can contain other navigation fields such as groups, pages, icons, or links to external pages.

```
{
  "navigation": {
    "anchors": [
      {
        "anchor": "Documentation",
        "icon": "book-open",
        "pages": [
          "quickstart",
          "development",
          "navigation"
        ]
      },
      {
        "anchor": "API reference",
        "icon": "square-terminal",
        "pages": [
          "api-reference/get",
          "api-reference/post",
          "api-reference/delete"
        ]
      },
      {
        "anchor": "Blog",
        "href": "https://external-link.com/blog"
      }
    ]
  }
}
```

### ​Global anchors

 Use global anchors for external links that should appear on all pages, regardless of which section of your navigation the user is viewing. Global anchors are particularly useful for linking to resources outside your documentation, such as a blog, community forum, or support portal. Global anchors must include an `href` field pointing to an external URL. They cannot contain relative paths.

```
{
  "navigation": {
    "global":  {
      "anchors": [
        {
          "anchor": "Blog",
          "icon": "pencil",
          "href": "https://mintlify.com/blog"
        }
      ]
    },
    "tabs": /*...*/
  }
}
```

## ​Dropdowns

 Dropdowns are contained in an expandable menu at the top of your sidebar navigation. Each item in a dropdown directs to a section of your documentation. ![Decorative graphic of a dropdown navigation.](https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/navigation/dropdowns-light.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=f04faa13e4a15c6866b8ceee98362018) ![Decorative graphic of a dropdown navigation.](https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/navigation/dropdowns-dark.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=4ee16248cae08fee00fe98952b599041) In the `navigation` object, `dropdowns` is an array where each entry is an object that requires a `dropdown` field and can contain other navigation fields such as groups, pages, icons, or links to external pages.

```
{
  "navigation": {
    "dropdowns": [
      {
        "dropdown": "Documentation",
        "icon": "book-open",
        "pages": [
          "quickstart",
          "development",
          "navigation"
        ]
      },
      {
        "dropdown": "API reference",
        "icon": "square-terminal",
        "pages": [
          "api-reference/get",
          "api-reference/post",
          "api-reference/delete"
        ]
      },
      {
        "dropdown": "Blog",
        "href": "https://external-link.com/blog"
      }
    ]
  }
}
```

## ​Products

 ![Decorative graphic of a product switcher.](https://mintcdn.com/mintlify/uTIQZECUoznwRp7Y/images/navigation/product-switcher-light.png?fit=max&auto=format&n=uTIQZECUoznwRp7Y&q=85&s=ab051b15c6e533eb2d723fed8f400704) ![Decorative graphic of a product switcher.](https://mintcdn.com/mintlify/uTIQZECUoznwRp7Y/images/navigation/product-switcher-dark.png?fit=max&auto=format&n=uTIQZECUoznwRp7Y&q=85&s=4827f6913945eeadb2c54362ee0f748d) Products create a dedicated navigation division for organizing product-specific documentation. Use products to separate different offerings, services, or major feature sets within your documentation. In the `navigation` object, `products` is an array where each entry is an object that requires a `product` field and can contain other navigation fields such as groups, pages, icons, or links to external pages.

```
{
  "navigation": {
    "products": [
      {
        "product": "Core API",
        "description": "Core API description",
        "icon": "api",
        "groups": [
          {
            "group": "Getting started",
            "pages": [
              "core-api/quickstart",
              "core-api/authentication"
            ]
          },
          {
            "group": "Endpoints",
            "pages": [
              "core-api/users",
              "core-api/orders"
            ]
          }
        ]
      },
      {
        "product": "Analytics Platform",
        "description": "Analytics Platform description",
        "icon": "chart-bar",
        "pages": [
          "analytics/overview",
          "analytics/dashboard",
          "analytics/reports"
        ]
      },
      {
        "product": "Mobile SDK",
        "description": "Mobile SDK description",
        "icon": "smartphone",
        "href": "https://mobile-sdk-docs.example.com"
      }
    ]
  }
}
```

## ​OpenAPI

 Integrate OpenAPI specifications directly into your navigation structure to automatically generate API documentation. Create dedicated API sections or place endpoint pages within other navigation components. Set a default OpenAPI specification at any level of your navigation hierarchy. Child elements will inherit this specification unless they define their own specification. When you add the `openapi` property to a navigation element (such as an anchor, tab, or group) without specifying any pages, Mintlify automatically generates pages for **all endpoints** defined in your OpenAPI specification.To control which endpoints appear, explicitly list the desired endpoints in a `pages` array. For more information about referencing OpenAPI endpoints in your docs, see the [OpenAPI setup](https://mintlify.com/docs/api-playground/openapi-setup).

```
{
  "navigation": {
    "groups": [
      {
        "group": "API reference",
        "openapi": "/path/to/openapi-v1.json",
        "pages": [
          "overview",
          "authentication",
          "GET /users",
          "POST /users",
          {
            "group": "Products",
            "openapi": "/path/to/openapi-v2.json",
            "pages": [
              "GET /products",
              "POST /products"
            ]
          }
        ]
      }
    ]
  }
}
```

## ​Versions

 Partition your navigation into different versions. Versions are selectable from a dropdown menu. ![Decorative graphic of a version switcher.](https://mintcdn.com/mintlify/f7fo9pnTEtzBD70_/images/navigation/versions-light.png?fit=max&auto=format&n=f7fo9pnTEtzBD70_&q=85&s=85e9cca71a814be044a285028cf9a2a1) ![Decorative graphic of a version switcher.](https://mintcdn.com/mintlify/f7fo9pnTEtzBD70_/images/navigation/versions-dark.png?fit=max&auto=format&n=f7fo9pnTEtzBD70_&q=85&s=fdb637aea218b4035afdaca14dae7d38) In the `navigation` object, `versions` is an array where each entry is an object that requires a `version` field and can contain any other navigation fields.

```
{
  "navigation": {
    "versions": [
      {
        "version": "1.0.0",
        "groups": [
          {
            "group": "Getting started",
            "pages": ["v1/overview", "v1/quickstart", "v1/development"]
          }
        ]
      },
      {
        "version": "2.0.0",
        "groups": [
          {
            "group": "Getting started",
            "pages": ["v2/overview", "v2/quickstart", "v2/development"]
          }
        ]
      }
    ]
  }
}
```

## ​Languages

 Partition your navigation into different languages. Languages are selectable from a dropdown menu. ![Decorative graphic of a language switcher.](https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/navigation/languages-light.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=e451ef6550588674e26e264ce2cbe399) ![Decorative graphic of a language switcher.](https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/navigation/languages-dark.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=99a90032d57cfefe2b46fb0d191391c7) In the `navigation` object, `languages` is an array where each entry is an object that requires a `language` field and can contain any other navigation fields, including language-specific banner configurations. We currently support the following languages for localization: ![https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/navigation/languages/ar.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=3d848d9025b508f338803a8ec6e0cfcf](https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/navigation/languages/ar.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=3d848d9025b508f338803a8ec6e0cfcf)

## Arabic (ar)

![https://mintcdn.com/mintlify/BTaDCk_Uxbf62Se-/images/navigation/languages/cs.png?fit=max&auto=format&n=BTaDCk_Uxbf62Se-&q=85&s=b880294f53cff62c04d639e8e281f4dc](https://mintcdn.com/mintlify/BTaDCk_Uxbf62Se-/images/navigation/languages/cs.png?fit=max&auto=format&n=BTaDCk_Uxbf62Se-&q=85&s=b880294f53cff62c04d639e8e281f4dc)

## Czech (cs)

![https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/navigation/languages/cn.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=77d74a80d5ef3abcbef683a48c26c799](https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/navigation/languages/cn.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=77d74a80d5ef3abcbef683a48c26c799)

## Chinese (cn)

![https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/navigation/languages/cn.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=77d74a80d5ef3abcbef683a48c26c799](https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/navigation/languages/cn.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=77d74a80d5ef3abcbef683a48c26c799)

## Chinese (zh-Hant)

![https://mintcdn.com/mintlify/4vDiMoxdniYs_vyk/images/navigation/languages/nl.png?fit=max&auto=format&n=4vDiMoxdniYs_vyk&q=85&s=da927dcce7501df5f80aba862868355b](https://mintcdn.com/mintlify/4vDiMoxdniYs_vyk/images/navigation/languages/nl.png?fit=max&auto=format&n=4vDiMoxdniYs_vyk&q=85&s=da927dcce7501df5f80aba862868355b)

## Dutch (nl)

![https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/navigation/languages/en.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=25d8b8c6c7473091d33c16b602eb381a](https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/navigation/languages/en.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=25d8b8c6c7473091d33c16b602eb381a)

## English (en)

![https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/navigation/languages/fr.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=ccf6b50a06031c5961d642aeb92d87b1](https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/navigation/languages/fr.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=ccf6b50a06031c5961d642aeb92d87b1)

## French (fr)

![https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/navigation/languages/de.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=831c61a2dfd61b73164938b664507542](https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/navigation/languages/de.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=831c61a2dfd61b73164938b664507542)

## German (de)

![https://mintcdn.com/mintlify/Xr3wiklTC3GE1PaM/images/navigation/languages/he.png?fit=max&auto=format&n=Xr3wiklTC3GE1PaM&q=85&s=e51655c25bcdf50287eb43dbade78598](https://mintcdn.com/mintlify/Xr3wiklTC3GE1PaM/images/navigation/languages/he.png?fit=max&auto=format&n=Xr3wiklTC3GE1PaM&q=85&s=e51655c25bcdf50287eb43dbade78598)

## Hebrew (he)

![https://mintcdn.com/mintlify/BTaDCk_Uxbf62Se-/images/navigation/languages/hi.png?fit=max&auto=format&n=BTaDCk_Uxbf62Se-&q=85&s=9bb83682ddc748abb1e6be010852f9d1](https://mintcdn.com/mintlify/BTaDCk_Uxbf62Se-/images/navigation/languages/hi.png?fit=max&auto=format&n=BTaDCk_Uxbf62Se-&q=85&s=9bb83682ddc748abb1e6be010852f9d1)

## Hindi (hi)

![https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/navigation/languages/id.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=8fbde287fb60df0d0712f3d0db7aba1b](https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/navigation/languages/id.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=8fbde287fb60df0d0712f3d0db7aba1b)

## Indonesian (id)

![https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/navigation/languages/it.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=dc39bd6cd67e91394e03842e588681df](https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/navigation/languages/it.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=dc39bd6cd67e91394e03842e588681df)

## Italian (it)

![https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/navigation/languages/jp.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=69b17ac2f3202e4bf28945e8408f67e3](https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/navigation/languages/jp.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=69b17ac2f3202e4bf28945e8408f67e3)

## Japanese (jp)

![https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/navigation/languages/ko.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=a555f0a68a4beb076b3556a7f0264b5e](https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/navigation/languages/ko.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=a555f0a68a4beb076b3556a7f0264b5e)

## Korean (ko)

![https://mintcdn.com/mintlify/4vDiMoxdniYs_vyk/images/navigation/languages/lv.png?fit=max&auto=format&n=4vDiMoxdniYs_vyk&q=85&s=61c384db51dc61621e62f4c565935b02](https://mintcdn.com/mintlify/4vDiMoxdniYs_vyk/images/navigation/languages/lv.png?fit=max&auto=format&n=4vDiMoxdniYs_vyk&q=85&s=61c384db51dc61621e62f4c565935b02)

## Latvian (lv)

![https://mintcdn.com/mintlify/4vDiMoxdniYs_vyk/images/navigation/languages/no.png?fit=max&auto=format&n=4vDiMoxdniYs_vyk&q=85&s=993784e6321e0da6be58d4b8451a9425](https://mintcdn.com/mintlify/4vDiMoxdniYs_vyk/images/navigation/languages/no.png?fit=max&auto=format&n=4vDiMoxdniYs_vyk&q=85&s=993784e6321e0da6be58d4b8451a9425)

## Norwegian (no)

![https://mintcdn.com/mintlify/Xr3wiklTC3GE1PaM/images/navigation/languages/pl.png?fit=max&auto=format&n=Xr3wiklTC3GE1PaM&q=85&s=c032c7a1341941978d80307821c82c34](https://mintcdn.com/mintlify/Xr3wiklTC3GE1PaM/images/navigation/languages/pl.png?fit=max&auto=format&n=Xr3wiklTC3GE1PaM&q=85&s=c032c7a1341941978d80307821c82c34)

## Polish (pl)

![https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/navigation/languages/pt-br.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=96a015424865291e54cefc8633cc8d78](https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/navigation/languages/pt-br.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=96a015424865291e54cefc8633cc8d78)

## Portuguese (pt-BR)

![https://mintcdn.com/mintlify/BTaDCk_Uxbf62Se-/images/navigation/languages/ro.png?fit=max&auto=format&n=BTaDCk_Uxbf62Se-&q=85&s=5a3925857c9de6c3c818edde060f51c9](https://mintcdn.com/mintlify/BTaDCk_Uxbf62Se-/images/navigation/languages/ro.png?fit=max&auto=format&n=BTaDCk_Uxbf62Se-&q=85&s=5a3925857c9de6c3c818edde060f51c9)

## Romanian (ro)

![https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/navigation/languages/ru.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=0f52006163f89fe293525925000eb554](https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/navigation/languages/ru.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=0f52006163f89fe293525925000eb554)

## Russian (ru)

![https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/navigation/languages/es.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=14af4f5bf5e19c20d2062465ca6b9011](https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/navigation/languages/es.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=14af4f5bf5e19c20d2062465ca6b9011)

## Spanish (es)

![https://mintcdn.com/mintlify/bbYdWMDGyp4158HR/images/navigation/languages/sv.png?fit=max&auto=format&n=bbYdWMDGyp4158HR&q=85&s=b62a991d880845b46daa65220ca451b5](https://mintcdn.com/mintlify/bbYdWMDGyp4158HR/images/navigation/languages/sv.png?fit=max&auto=format&n=bbYdWMDGyp4158HR&q=85&s=b62a991d880845b46daa65220ca451b5)

## Swedish (sv)

![https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/navigation/languages/tr.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=e52a73a891fa250497c853c557b0a91f](https://mintcdn.com/mintlify/Y6rP0BmbzgwHuEoU/images/navigation/languages/tr.png?fit=max&auto=format&n=Y6rP0BmbzgwHuEoU&q=85&s=e52a73a891fa250497c853c557b0a91f)

## Turkish (tr)

![https://mintcdn.com/mintlify/8p1xhF2gnPXDMRE_/images/navigation/languages/ua.png?fit=max&auto=format&n=8p1xhF2gnPXDMRE_&q=85&s=2e0f017cadda1fa0305e0e57c9de2860](https://mintcdn.com/mintlify/8p1xhF2gnPXDMRE_/images/navigation/languages/ua.png?fit=max&auto=format&n=8p1xhF2gnPXDMRE_&q=85&s=2e0f017cadda1fa0305e0e57c9de2860)

## Ukrainian (ua)

![https://mintcdn.com/mintlify/Xr3wiklTC3GE1PaM/images/navigation/languages/uz.png?fit=max&auto=format&n=Xr3wiklTC3GE1PaM&q=85&s=dd6427a746dcfc6e8972e8ea0b5dc20f](https://mintcdn.com/mintlify/Xr3wiklTC3GE1PaM/images/navigation/languages/uz.png?fit=max&auto=format&n=Xr3wiklTC3GE1PaM&q=85&s=dd6427a746dcfc6e8972e8ea0b5dc20f)

## Uzbek (uz)

![https://mintcdn.com/mintlify/BTaDCk_Uxbf62Se-/images/navigation/languages/vi.png?fit=max&auto=format&n=BTaDCk_Uxbf62Se-&q=85&s=970f4a7e12c0dd29f3980c22cbddad9e](https://mintcdn.com/mintlify/BTaDCk_Uxbf62Se-/images/navigation/languages/vi.png?fit=max&auto=format&n=BTaDCk_Uxbf62Se-&q=85&s=970f4a7e12c0dd29f3980c22cbddad9e)

## Vietnamese (vi)

```
{
  "navigation": {
    "languages": [
      {
        "language": "en",
        "banner": {
          "content": "🚀 Version 2.0 is now live! See our [changelog](/en/changelog) for details.",
          "dismissible": true
        },
        "groups": [
          {
            "group": "Getting started",
            "pages": ["en/overview", "en/quickstart", "en/development"]
          }
        ]
      },
      {
        "language": "es",
        "banner": {
          "content": "🚀 ¡La versión 2.0 ya está disponible! Consulta nuestro [registro de cambios](/es/changelog).",
          "dismissible": true
        },
        "groups": [
          {
            "group": "Getting started",
            "pages": ["es/overview", "es/quickstart", "es/development"]
          }
        ]
      }
    ]
  }
}
```

 For automated translations, [contact our sales team](mailto:gtm@mintlify.com) to discuss solutions.

## ​Nesting

 Navigation elements can be nested within each other to create complex hierarchies. You must have one root-level parent navigation element such as tabs, groups, or a dropdown. You can nest other types of navigation elements within your primary navigation pattern. Each navigation element can contain one type of child element at each level of your navigation hierarchy. For example, a tab can contain anchors that contain groups, but a tab cannot contain both anchors and groups at the same level.

```
{
  "navigation": {
    "tabs": [
      {
        "tab": "Documentation",
        "anchors": [
          {
            "anchor": "Guides",
            "icon": "book-open",
            "pages": ["quickstart", "tutorial"]
          },
          {
            "anchor": "API Reference",
            "icon": "code",
            "pages": ["api/overview", "api/endpoints"]
          }
        ]
      },
      {
        "tab": "Resources",
        "groups": [
          {
            "group": "Help",
            "pages": ["support", "faq"]
          }
        ]
      }
    ]
  }
}
```

## ​Breadcrumbs

 Breadcrumbs display the full navigation path at the top of pages. Some themes have breadcrumbs enabled by default and others do not. You can control whether breadcrumbs are enabled for your site using the `styling` property in your `docs.json`.

```
"styling": {
  "eyebrows": "breadcrumbs"
}
```

## ​Interaction configuration

 Control how users interact with navigation elements using the `interaction` property in your `docs.json`.

### ​Enable auto-navigation for groups

 When a user expands a navigation group, some themes will automatically navigate to the first page in the group. You can override a theme’s default behavior using the `drilldown` option.

- Set to `true` to force automatic navigation to the first page when a navigation group is selected.
- Set to `false` to prevent navigation and only expand or collapse the group when it is selected.
- Leave unset to use the theme’s default behavior.

```
"interaction": {
  "drilldown": true  // Force navigation to first page when a user expands a dropdown
}
```

---

# Pages

> Configure page metadata, titles, and frontmatter properties.

Each page is a Markdown file. Both `.mdx` and `.md` file types are supported. We recommend using MDX, which combines Markdown with React components to create rich, interactive documentation. Plain Markdown (`.md`) is supported for easier migration from other platforms, but should be updated to MDX for full functionality.

## ​Page metadata

 Every page starts with frontmatter, the YAML metadata enclosed by `---` at the beginning of a file. This metadata defines how your page appears and behaves. Use frontmatter to control:

- Page titles and descriptions
- Sidebar titles, icons, and tags
- Page layouts
- SEO meta tags
- Custom metadata

 [​](#param-title)titlestringrequiredThe title of your page that appears in navigation and browser tabs. [​](#param-description)descriptionstringA brief description of what this page covers. Appears under the title and improves SEO. [​](#param-sidebar-title)sidebarTitlestringA short title that displays in the sidebar navigation. [​](#param-icon)iconstringThe icon to display.Options:

- [Font Awesome icon](https://fontawesome.com/icons) name
- [Lucide icon](https://lucide.dev/icons) name
- URL to an externally hosted icon
- Path to an icon file in your project

 [​](#param-icon-type)iconTypestringThe [Font Awesome](https://fontawesome.com/icons) icon style. Only used with Font Awesome icons.Options: `regular`, `solid`, `light`, `thin`, `sharp-solid`, `duotone`, `brands`. [​](#param-tag)tagstringA tag that appears next to your page title in the sidebar. [​](#param-custom)<custom>stringAny valid YAML frontmatter. For example, `product: "API"` or `version: "1.0.0"`. Example YAML frontmatter

```
---
title: "About frontmatter"
description: "Frontmatter is the metadata that controls how your page appears and behaves"
sidebarTitle: "Frontmatter"
icon: "book"
tag: "NEW"
---
```

## ​Page mode

 Control how your page displays with the `mode` setting.

### ​Default

 If no mode is defined, defaults to a standard layout with a sidebar navigation and table of contents.

```
---
title: "Default page title"
---
```

### ​Wide

 Wide mode hides the table of contents. This is useful for pages that do not have any headings or if you prefer to use the extra horizontal space. Wide mode is available for all themes.

```
---
title: "Wide page title"
mode: "wide"
---
```

### ​Custom

 Custom mode provides a minimalist layout that removes all elements except for the top navbar. Custom mode is a blank canvas to create landing pages or any other unique layouts that you want to have minimal navigation elements for. Custom mode is available for all themes.

```
---
title: "Custom page title"
mode: "custom"
---
```

 Using the `style` property on custom mode pages can cause a layout shift on page load. Use [Tailwind CSS or custom CSS](https://mintlify.com/docs/customize/custom-scripts) instead to avoid this issue.

### ​Frame

 Frame mode provides a layout similar to custom mode, but preserves the sidebar navigation. This page mode allows for custom HTML and components while maintaining the default navigation experience. Frame mode is only available for Aspen and Almond themes.

```
---
title: "Frame page title"
mode: "frame"
---
```

### ​Center

 Center mode removes the sidebar and table of contents, centering the content. This is useful for changelogs or other pages where you want to emphasize the content. Center mode is available for Mint and Linden themes.

```
---
title: "Center page title"
mode: "center"
---
```

## ​API pages

 Create interactive API playgrounds by adding an API specification to your frontmatter, `api` or `openapi`.

```
---
openapi: "GET /endpoint"
---
```

 Learn more about building [API documentation](https://mintlify.com/docs/api-playground/overview).

## ​External links

 Link to external sites directly from your navigation with the `url` metadata.

```
---
title: "npm Package"
url: "https://www.npmjs.com/package/mint"
---
```

## ​Search engine optimization

 Most SEO meta tags are automatically generated. You can set SEO meta tags manually to improve your site’s SEO, social sharing, and browser compatibility. Meta tags with colons must be wrapped in quotes.

```
---
"twitter:image": "/images/social-preview.jpg"
---
```

 See [SEO](https://mintlify.com/docs/optimize/seo) for complete SEO metadata options.

## ​Internal search keywords

 Enhance a specific page’s discoverability in the built-in search by providing `keywords` in your metadata. These keywords won’t appear as part of the page content or in search results, but users that search for them will be shown the page as a result.

```
---
keywords: ['configuration', 'setup', 'getting started']
---
```

## ​Last modified timestamp

 Add a “Last modified on [date]” timestamp to all pages by enabling `metadata.timestamp` in your [global settings](https://mintlify.com/docs/organize/settings#metadata). docs.json

```
"metadata": {
  "timestamp": true
}
```

 Override the global timestamp setting on individual pages with the `timestamp` frontmatter field. Use this field to selectively show or hide timestamps on specific pages.

```
---
title: "Page title"
timestamp: false
---
```

 When set to `true`, the timestamp displays even if the global setting is `false`. When set to `false`, the timestamp is hidden even if the global setting is `true`.
