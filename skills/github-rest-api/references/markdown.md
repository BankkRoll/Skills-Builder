# REST API endpoints for Markdown

# REST API endpoints for Markdown

> Use the REST API to render a markdown document as an HTML page or as raw text.

## Render a Markdown document

Depending on what is rendered in the Markdown, you may need to provide additional token scopes for labels, such as `issues:read` or `pull_requests:read`.

### Fine-grained access tokens for "Render a Markdown document"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Contents" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "Render a Markdown document"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| textstringRequiredThe Markdown text to render in HTML. |
| modestringThe rendering mode.Default:markdownCan be one of:markdown,gfm |
| contextstringThe repository context to use when creating references ingfmmode.  For example, settingcontexttoocto-org/octo-repowill change the text#42into an HTML link to issue 42 in theocto-org/octo-reporepository. |

### HTTP response status codes for "Render a Markdown document"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 304 | Not modified |

### Code samples for "Render a Markdown document"

#### Request example

post/markdown

-
-
-

`curl -L \
  -X POST \
  -H "Accept: text/html" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/markdown \
  -d '{"text":"Hello **world**"}'`

Example response

-
-

`Status: 200``"<p>Hello <strong>world</strong></p>"`

## Render a Markdown document in raw mode

You must send Markdown as plain text (using a `Content-Type` header of `text/plain` or `text/x-markdown`) to this endpoint, rather than using JSON format. In raw mode, [GitHub Flavored Markdown](https://github.github.com/gfm/) is not supported and Markdown will be rendered in plain format like a README.md file. Markdown content must be 400 KB or less.

### Fine-grained access tokens for "Render a Markdown document in raw mode"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token does not require any permissions.

This endpoint can be used without authentication if only public resources are requested.

### HTTP response status codes for "Render a Markdown document in raw mode"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 304 | Not modified |

### Code samples for "Render a Markdown document in raw mode"

#### Request examples

Select the example typeExample (text/plain)Rendering markdown (text/x-markdown)post/markdown/raw

-
-
-

`curl -L \
  -X POST \
  -H "Accept: text/html" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/markdown/raw \
  -d '{"text":"Hello **world**"}'`

Example response

-
-

`Status: 200``"<p>Hello <strong>world</strong></p>"`
