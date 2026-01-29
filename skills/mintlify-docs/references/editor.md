# Collaborate in the web editor and more

# Collaborate in the web editor

> Work together on documentation with branches, pull requests, and preview deployments.

Collaborate with your team on documentation using branch-based workflows, pull requests, and preview deployments. If you aren’t familiar with Git, see [Git concepts](https://mintlify.com/docs/guides/git-concepts).

## ​Branch-based collaboration

 Use branches to work on documentation updates in parallel without affecting your live site.

### ​Why use branches

- **Isolate changes**: Work on updates without affecting your live documentation.
- **Review before publishing**: Get feedback from team members before changes go live.
- **Parallel work**: Multiple team members can work on different branches simultaneously.

## ​Recommended workflow

 Use pull requests to propose changes and collaborate with your team before merging to your live documentation. This workflow ensures your team reviews changes before publishing and maintains a clear history of updates. 1

Create a pull request

Create a pull request from the editor when you’re ready to publish your changes. See [Publish changes in the web editor](https://mintlify.com/editor/publish) for more information on using pull requests.2

Review pull requests

Review pull requests in your Git provider like GitHub or GitLab.3

Respond to feedback

When reviewers request changes, make the requested changes and save your changes. Additional changes automatically push to the existing pull request.4

Merge pull requests

Merge your pull request after addressing all requested changes, required reviewers approve the pull request, and any automated checks pass.

## ​Preview deployments

 Preview deployments create temporary URLs where you can see your changes before they go live.

### ​Access preview deployments

1. Click **Share** in the editor tool bar.
2. Click **Preview** to open the preview deployment in a new tab.
3. The preview URL shows your documentation with all saved changes applied.

 ![Share button in the editor toolbar](https://mintcdn.com/mintlify/fv0sH0FEeyPeiSH6/images/editor/share-preview-light.png?fit=max&auto=format&n=fv0sH0FEeyPeiSH6&q=85&s=d525d944b4f1fd68321f8370b24a58fc)![Share button in the editor toolbar](https://mintcdn.com/mintlify/fv0sH0FEeyPeiSH6/images/editor/share-preview-dark.png?fit=max&auto=format&n=fv0sH0FEeyPeiSH6&q=85&s=7f06c3db7134f80d0727264c9df7c153)

### ​Share previews

 Share the preview deployment URL with team members to gather feedback. Previews update automatically when you save additional changes.

### ​Preview authentication

 Preview URLs are publicly accessible by default. Enable preview authentication in the [Add-ons](https://dashboard.mintlify.com/products/addons) page of your dashboard to restrict access to authenticated organization members.

---

# Configurations

> Configure pages, navigation elements, and media using configuration sheets.

Configure your documentation site’s branding, appearance, and features from the **Configurations** panel in the web editor. ![Configurations settings in the sidebar in light mode.](https://mintcdn.com/mintlify/jISy-KDPfnBIRyDx/images/editor/configurations-light.png?fit=max&auto=format&n=jISy-KDPfnBIRyDx&q=85&s=81542317fdddce57b43dcfa05b176c64)![Configurations settings in the sidebar in dark mode.](https://mintcdn.com/mintlify/jISy-KDPfnBIRyDx/images/editor/configurations-dark.png?fit=max&auto=format&n=jISy-KDPfnBIRyDx&q=85&s=c49c482193cc072ec2c55bd072382943)

## ​Brand your site

 Set your site’s identity and how it appears to visitors.

- **Docs title**: The name of your documentation. Appears in browser tabs and search results.
- **Description**: Brief summary of your documentation. Used for SEO and site metadata.
- **Favicon**: Small icon that appears in browser tabs. Upload ICO, PNG, GIF, or JPG files.
- **Theme**: Choose a [theme](https://mintlify.com/docs/customize/themes) for your documentation’s overall appearance.

## ​Customize colors and appearance

 Control your site’s visual identity and color scheme.

- **Primary color**: The main accent color used throughout your site for links, buttons, and highlights.
- **Light mode color**: Accent color variation for light mode. How themes apply this varies by theme.
- **Dark mode color**: Accent color variation for dark mode. How themes apply this varies by theme.
- **Logo**: Your brand logo. Upload SVG, PNG, or JPG files. You can set different logos for light and dark modes.
- **Logo link**: Where users go when they click your logo. Typically your homepage or marketing site.
- **Background colors**: Set custom background colors for light and dark modes separately.
- **Background image**: Add a background image to your site. Upload PNG, GIF, or JPG files.
- **Background decoration**: Apply visual styles to your background image.
- **Theme toggle**: Show or hide the light/dark mode switcher for users.
- **Default theme**: Set whether your site loads in light or dark mode by default.

## ​Set custom fonts

 Replace default fonts with your brand’s typography.

- **Default font**: The base font family and weight for all text. Provide a source URL and format (WOFF or WOFF2).
- **Heading font**: Font family and weight specifically for headings (h1, h2, etc.). Set separately from body text.
- **Body font**: Font family and weight for body text and paragraphs.

 For each font, specify the family name, weight, source URL (like Google Fonts), and format.

## ​Configure header

 Add navigation elements to the top of your site.

- **Navbar button**: Add a primary call-to-action button in your header. Set the button type, label, and destination URL.
- **Navbar links**: Add additional navigation links in your header. Each link includes text and a URL.

## ​Configure footer

 Add links and social media handles to your site footer.

- **Social links**: Add your profiles on platforms like GitHub, X (Twitter), LinkedIn, Discord, YouTube, Slack, and more.
- **Footer columns**: Organize footer links into columns with custom headings and link groups.

## ​Enhance content

 Customize how content appears on your site.

- **Thumbnail background**: Set a custom background image for page thumbnails and social previews.
- **Thumbnail appearance**: Control how thumbnails display.
- **Thumbnail font**: Set a custom font for text in thumbnails.
- **Page eyebrow**: Add small labels above page titles.
- **Code block theme**: Choose the syntax highlighting theme for code blocks.
- **LaTeX support**: Enable mathematical notation rendering with LaTeX.

## ​Set up AI chat and search

 Customize the search experience.

- **Search placeholder**: The text that appears in the search box before users type. Default is “Search or ask…”.

## ​Configure API specifications

 Add [OpenAPI](https://mintlify.com/docs/api-playground/openapi-setup) or [AsyncAPI](https://mintlify.com/docs/api-playground/asyncapi-setup) specification files to document endpoints.

- **OpenAPI specs**: Upload an OpenAPI specification file or enter a URL to an external OpenAPI file.
- **AsyncAPI specs**: Upload an AsyncAPI specification file or enter a URL to an external AsyncAPI file.
- **Playground display**: Choose to display the [interactive API playground](https://mintlify.com/docs/api-playground/overview#visibility-modes), simple API playground, or no API playground.
- **Proxy server**: Enable or disable the proxy server for API requests.

## ​Add analytics and integrations

 Connect analytics and third-party tools to your documentation. Track visitor behavior with:

- **Amplitude, Mixpanel, Heap**: Product analytics platforms
- **Google Analytics, Google Tag Manager**: Web analytics
- **PostHog, Plausible, Fathom**: Privacy-focused analytics
- **Segment, Hightouch**: Customer data platforms
- **Hotjar, LogRocket**: Session replay and heatmaps
- **Microsoft Clarity**: User behavior analytics
- **Intercom**: Customer messaging
- **Clearbit, Koala**: Visitor identification

 Additional integrations:

- **Telemetry**: Enable or disable usage telemetry
- **Cookies**: Set custom cookie key and value pairs

---

# Web editor overview

> Edit and publish documentation in your browser.

![Decorative image in light mode](https://mintcdn.com/mintlify/GiucHIlvP3i5L17o/images/editor/editor-light.png?fit=max&auto=format&n=GiucHIlvP3i5L17o&q=85&s=0579093c2743bb8f55c4f81bece9e902) ![Decorative image in dark mode](https://mintcdn.com/mintlify/GiucHIlvP3i5L17o/images/editor/editor-dark.png?fit=max&auto=format&n=GiucHIlvP3i5L17o&q=85&s=09938d1ca65739f048de43183a5bbaab) Create, edit, and publish documentation directly in your browser with the web editor. View and share previews of your changes; manage your site’s navigation structure with drag-and-drop components; and publish updates using your team’s preferred workflow.

## ​Key features

- **Visual and Markdown editing**: Switch between visual and Markdown editing modes as you work.
- **Live preview**: See real-time changes without creating a preview deployment.
- **Shareable preview links**: Create preview links for your team from the editor.
- **Drag-and-drop navigation**: Organize your site structure visually without editing configuration files.
- **Built-in media manager**: Upload and organize images, videos, and other assets.
- **Git synchronization**: All changes sync automatically with your documentation repository.
- **Branch workflows**: Work on feature branches and create pull requests for review.
- **Team collaboration**: Multiple team members can work simultaneously with preview deployments.

## ​Get started

 [Create and edit pagesCreate, edit, and organize pages.](https://mintlify.com/docs/editor/pages) [Organize navigationStructure your site navigation.](https://mintlify.com/docs/editor/navigation) [Add mediaUpload and use images, videos, and other assets.](https://mintlify.com/docs/editor/media) [Live previewPreview your site in real time as you edit.](https://mintlify.com/docs/editor/live-preview)

## ​Publish and collaborate

 [Publish changesSave and publish your documentation updates.](https://mintlify.com/docs/editor/publish) [CollaborateWork with teams using branches and pull requests.](https://mintlify.com/docs/editor/collaborate)

## ​Reference

 [ConfigurationsConfigure site branding, colors, and features.](https://mintlify.com/docs/editor/configurations) [Keyboard shortcutsSpeed up your workflow with keyboard shortcuts.](https://mintlify.com/docs/editor/keyboard-shortcuts)

---

# Keyboard shortcuts

> Reference of keyboard shortcuts for the web editor.

Use keyboard shortcuts to navigate and edit faster in the web editor. The editor supports common shortcuts like copy, paste, undo, and select all, along with the shortcuts listed below.

## ​Visual mode

 Use these shortcuts when editing in Visual mode.

### ​Search and navigation

| Command | macOS | Windows |
| --- | --- | --- |
| Search files | Cmd+P | Ctrl+P |
| Open agent | Cmd+I | Ctrl+I |

### ​Text formatting

| Command | macOS | Windows |
| --- | --- | --- |
| Bold | Cmd+B | Ctrl+B |
| Underline | Cmd+U | Ctrl+U |
| Strikethrough | Cmd+Shift+S | Ctrl+Shift+S |
| Code | Cmd+E | Ctrl+E |
| Subscript | Cmd+, | Ctrl+, |
| Superscript | Cmd+. | Ctrl+. |

### ​Headings

| Command | macOS | Windows |
| --- | --- | --- |
| Text | Cmd+Option+0 | Ctrl+Alt+0 |
| Heading 1 | Cmd+Option+1 | Ctrl+Alt+1 |
| Heading 2 | Cmd+Option+2 | Ctrl+Alt+2 |
| Heading 3 | Cmd+Option+3 | Ctrl+Alt+3 |
| Heading 4 | Cmd+Option+4 | Ctrl+Alt+4 |

### ​Lists and blocks

| Command | macOS | Windows |
| --- | --- | --- |
| Unordered list | Cmd+Shift+8 | Ctrl+Shift+8 |
| Blockquote | Cmd+Shift+B | Ctrl+Shift+B |

### ​Content actions

| Command | macOS | Windows |
| --- | --- | --- |
| Add link | Cmd+K | Ctrl+K |
| Add line break | Cmd+Enter | Ctrl+Enter |
| Component menu | / | / |

## ​Markdown mode

 Markdown mode uses the Monaco editor, which supports standard VS Code keyboard shortcuts.

### ​Search and navigation

| Command | macOS | Windows |
| --- | --- | --- |
| Search files | Cmd+P | Ctrl+P |
| Find | Cmd+F | Ctrl+F |

### ​Editing

| Command | macOS | Windows |
| --- | --- | --- |
| Toggle comment | Cmd+/ | Ctrl+/ |
| Indent line | Tab | Tab |
| Outdent line | Shift+Tab | Shift+Tab |
| Move line up | Option+↑ | Alt+↑ |
| Move line down | Option+↓ | Alt+↓ |
| Duplicate line | Shift+Option+↓ | Shift+Alt+↓ |

### ​Multiple cursors

| Command | macOS | Windows |
| --- | --- | --- |
| Add cursor | Option+ Click | Alt+ Click |
| Add cursor above | Cmd+Option+↑ | Ctrl+Alt+↑ |
| Add cursor below | Cmd+Option+↓ | Ctrl+Alt+↓ |

---

# Live preview

> Preview your documentation site and see changes in real time as you edit.

Preview your documentation site as you edit. Live preview shows your pages exactly as they appear when published, updating in real time as you make changes to content, navigation, and configuration.

## ​Open live preview

 Click the  button in the toolbar to open a live preview in a new tab. ![Live preview button on the editor toolbar.](https://mintcdn.com/mintlify/OJeK62hgxFqOZjzS/images/editor/live-preview-light.png?fit=max&auto=format&n=OJeK62hgxFqOZjzS&q=85&s=f9fd975ba0d4c4e1b97730ee944ce240)![Live preview button on the editor toolbar.](https://mintcdn.com/mintlify/OJeK62hgxFqOZjzS/images/editor/live-preview-dark.png?fit=max&auto=format&n=OJeK62hgxFqOZjzS&q=85&s=d95cc78b97514e3ad08943ce8fbf048e) Live preview is only available for public documentation. If your documentation requires authentication, the editor displays a “Live preview unavailable” message.

## ​Live preview versus preview deployments

|  | Live preview | Preview deployment |
| --- | --- | --- |
| Speed | Instant | Requires build time |
| Access | Local URL | Shareable URL |
| Use case | View changes while editing | Share with team for review |
| Availability | While the editor is open | As long as the branch exists |

 Use live preview for immediate feedback as you work. Create preview deployments when you need to share changes with your team or test on different devices.

---

# Add media

> Upload and use images and assets in your documentation.

## ​Supported file types

- **Images**: PNG, JPG, JPEG, SVG, GIF, WebP
- **Videos**: MP4, WebM
- **Fonts**: TTF, WOFF, WOFF2
- **Other**: PDF, ICO (favicons)

## ​Add media to a page

### ​Drag and drop

 Drag and drop media from your computer or the asset manager onto a page in visual mode. Files save to the root of your `images/` folder.

### ​Slash command

 Type /image to open the image menu, then upload a new image or select an existing one.

### ​Upload files

 Use the asset manager in the sidebar to upload or search for files. ![Assets manager selected in the editor sidebar menu.](https://mintcdn.com/mintlify/OJeK62hgxFqOZjzS/images/editor/assets-light.png?fit=max&auto=format&n=OJeK62hgxFqOZjzS&q=85&s=3d046b4640b7d0eb3db71aed63eb7264)![Assets manager selected in the editor sidebar menu.](https://mintcdn.com/mintlify/tyM8nhezBDC6wj19/images/editor/assets-dark.png?fit=max&auto=format&n=tyM8nhezBDC6wj19&q=85&s=d453a3bc99aff5c44ae89feb439dea9b) Click **Upload** in the asset manager to add files from your computer.

## ​Manage assets

### ​Organize with folders

 Click the **+** button in the file explorer to create a new folder. Drag and drop files and folders in the file tree to reorganize them.

### ​Rename and edit assets

 Hover over an asset and click the **…** button to rename the file or update its alt text.

### ​Delete assets

 Hover over an asset and click the  delete button.

## ​Best practices

- **Use descriptive names**: Name files clearly, like `api-dashboard-light.png` instead of `img1.png`.
- **Add alt text**: Provide descriptive alt text for accessibility and SEO.
- **Organize with folders**: Group related assets, such as light and dark mode variants or assets for a specific feature area.
- **Use appropriate formats**: PNG for graphics with transparency, JPG for photos, SVG for icons and logos.

---

# Organize navigation

> Organize your documentation structure with the visual navigation editor.

Use the navigation sidebar to organize your documentation. Changes you make in the web editor’s navigation tree appear in your site’s navigation sidebar and sync to your `docs.json` configuration file.

## ​Add navigation elements

 To add a new navigation element, click **Add new** at the bottom of the navigation tree. ![Add new navigation element.](https://mintcdn.com/mintlify/DLSr2FhOurD6ae47/images/editor/navigation-light.png?fit=max&auto=format&n=DLSr2FhOurD6ae47&q=85&s=2562e8efb53c7b39ce60729bed6bd465)![Add new navigation element.](https://mintcdn.com/mintlify/DLSr2FhOurD6ae47/images/editor/navigation-dark.png?fit=max&auto=format&n=DLSr2FhOurD6ae47&q=85&s=713cfecdc840df31c0faac94b7e6f0d6) To add a navigation element nested inside another element, click the **+** button next to the name of the parent element. After creating an element, drag and drop it to reorder or nest it within other elements. Right-click any element to configure its properties, duplicate it, hide it from navigation, or delete it. Some elements cannot nest inside other elements. For example, tabs cannot nest inside groups. The web editor prevents you from nesting invalid elements.

### ​Add existing files

 Add files from your repository that aren’t yet in navigation.

1. Click the plus button, , where you want to add the file.
2. Click **Add existing file**.

 ![Add existing file menu expanded.](https://mintcdn.com/mintlify/-qEr0KdFgYiJikkw/images/editor/add-existing-file-menu-light.png?fit=max&auto=format&n=-qEr0KdFgYiJikkw&q=85&s=9312867a92d47d8cc157b63af791d7f0)![Add existing file menu expandeda.](https://mintcdn.com/mintlify/-qEr0KdFgYiJikkw/images/editor/add-existing-file-menu-dark.png?fit=max&auto=format&n=-qEr0KdFgYiJikkw&q=85&s=ff766655773ec13b2badf8e4935d8d70) You can also drag files from the **Unused pages** section directly into your navigation tree.

## ​Organize into sections

 Choose the right navigation structure for your documentation’s scope and audience.

### ​When to use pages

 Use pages for individual documentation files. Pages are the core building blocks of your navigation—every piece of content lives on a page. Add pages to your navigation to make them visible in your site’s sidebar. Pages can exist at the root level, within groups, tabs, anchors, dropdowns, or menus. If files are not in another navigation element, they appear in the **Unused pages** section. Unused pages are [hidden](https://mintlify.com/docs/organize/hidden-pages) from your published documentation.

### ​When to use groups

 Use groups to organize related pages into collapsible sections. Groups help users scan your navigation by clustering similar content together, like grouping all authentication-related pages or all API endpoint references. Groups can nest within other groups to create a hierarchical organization. Groups can exist within tabs, anchors, dropdowns, or at the root level.

### ​When to use tabs

 Use tabs to create separate top-level sections with horizontal navigation at the top of your site. Tabs work well when you have distinct areas like API Reference, Guides, and SDKs that users need to switch between. Tabs can contain pages, groups, and menu items. Configure tabs to add icons or link to external resources.

### ​When to use anchors

 Use anchors to create persistent navigation items at the top of your sidebar. Anchors help when you want to section your content or provide quick access to external resources without switching tabs. Anchors can contain pages and groups, or link to external URLs. **Global anchors:** Create global anchors that appear on all pages regardless of which section users are viewing. Global anchors must link to external URLs and are useful for resources like blogs, status pages, or support links.

### ​When to use dropdowns

 Use dropdowns to create an expandable menu at the top of your sidebar. Dropdowns work well when you have multiple related sections that users might want to explore but don’t need constant visibility like tabs. Dropdowns can contain pages and groups, or link to external URLs.

### ​When to use menus

 Use menus to add dropdown navigation items within a tab. Menus help users navigate directly to specific pages from the top navigation bar. Menus can contain pages and groups.

### ​When to use products

 Use products when you have multiple distinct product offerings that each need their own documentation. Products create a switcher menu that lets users navigate between different product documentation sets. Each product can have its own navigation structure with tabs, pages, and groups.

### ​When to use versions

 Use versions when you maintain multiple versions of your documentation simultaneously, like v1.0, v2.0, and v3.0 of an API. Versions create a switcher menu that lets users select which version they want to view. Each version can have different content and navigation structure.

### ​When to use languages

 Use languages when you provide documentation in multiple languages. Languages create a switcher menu that lets users view documentation in their preferred language. Each language maintains the same navigation structure with translated content.

## ​Customize appearance

 **Add icons:**

1. Right-click a navigation item.
2. Click **Configure**.
3. Click the icon field.

 **Add tags:**

1. Right-click a navigation item.
2. Click **Configure**.
3. Click the tag field.
4. Enter a tag like “NEW” or “BETA” that highlights important items.

 **Control visibility:** Hide the content within a navigation element without deleting it from your repository.

1. Right-click any item.
2. Click the toggle by the **Hide** label.

---

# Create and edit pages

> Create, edit, and organize documentation pages in the web editor.

## ​Navigate files

 Browse your documentation pages in the **Navigation** tab of the left panel.

- Click navigation elements to expand or collapse them.
- Click pages to open them in the editor.
- Click the search icon or press Cmd + P (macOS) or Ctrl + P (Windows) to search for files by filename. Search matches exact filenames, so use hyphens between words (for example, `get-agent-job` instead of `get agent job`).

### ​View unused pages

 The **Unused pages** section at the bottom of the **Settings** section of the sidebar shows pages and other files that exist in your repository, but aren’t included in your navigation. These are [hidden](https://mintlify.com/docs/organize/hidden-pages) pages that don’t appear on your published site until you add them to navigation.

## ​Create new pages

1. Click the **+** button in the navigation element where you want to add a page.
2. Click **Add a page**.
3. Enter a filename. The editor adds the `.mdx` extension automatically.

## ​Add unused pages to navigation

 Add pages from the **Unused pages** section to your navigation. **Drag and drop:**

1. Find the page in the **Unused pages** section.
2. Drag the page to the desired location in your navigation tree.

 **In the navigation tree:**

1. Click the plus button, , where you want to add the file.
2. Click **Add existing file**.
3. Select the page you want to add.

## ​Edit content

 Switch between visual and Markdown mode with the toggle in the toolbar. The web editor saves your changes when switching modes. ![Mode toggle in the toolbar.](https://mintcdn.com/mintlify/DLSr2FhOurD6ae47/images/editor/mode-toggle-light.png?fit=max&auto=format&n=DLSr2FhOurD6ae47&q=85&s=499c9121271dd33043363241461de5c3)![Mode toggle in the toolbar.](https://mintcdn.com/mintlify/SuQEK9bgpZedn8cX/images/editor/mode-toggle-dark.png?fit=max&auto=format&n=SuQEK9bgpZedn8cX&q=85&s=93f0045aa2ba662011376d8f812c8076)

### ​Visual mode

 Edit content with real-time previews that show how the content looks when published.

- **Add text**: Type in the editor to see how the text appears when published.
- **Format text**: Use the toolbar to bold, italicize, or apply other formatting to text.
- **Add components**: Press / to open the component menu and select components.
- **Add images**: Use the image component from the / menu.
- **Insert links**: Select text and press Cmd + K.

 See [Components](https://mintlify.com/docs/components) for the complete list of available components.

### ​Markdown mode

 Edit the MDX source code.

- **Direct MDX editing**: Write MDX and Markdown syntax for precise control over content.
- **Component properties**: Set component properties and configurations.
- **Frontmatter**: Edit page metadata at the top of the file.

 See [Format text](https://mintlify.com/docs/create/text) and [Format code](https://mintlify.com/docs/create/code) for more information on MDX syntax.

## ​Configure pages

 Configure page settings to control how pages appear in navigation, search results, and your site layout.

1. Right-click a file.
2. Click **Configure**.

### ​Customize navigation appearance

 Control how the page appears in your site’s navigation sidebar.

- **Title**: Set the main heading. Appears in navigation, browser tabs, and search results.
- **Sidebar title**: Display shorter text in navigation when the full title is too long for the sidebar.
- **Icon**: Add a visual marker next to the page to help users identify it quickly.
- **External URL**: Link to an external site instead of a page. Use this to add external resources to your navigation.

### ​Optimize for search and sharing

 Help users find your page and improve how it appears when shared.

- **Description**: Write a brief summary. Appears in search results and SEO meta tags.
- **Keywords**: Add relevant search terms to help users discover this page.
- **OG Image URL**: Set a custom preview image for social media shares and link previews.

### ​Control page layout

 Choose how the page displays to match your content needs.

- **Standard layout** (`default`): Default page with sidebar navigation and table of contents.
- **Full-width layout** (`wide`): Hides table of contents to allow wider layouts for tables, diagrams, or other content.
- **Centered layout** (`center`): Hides sidebar and table of contents for better readability of text-heavy pages like changelogs.
- **Custom width** (`custom`): Minimal layout with only the top navbar for landing pages or other unique layouts.

## ​Manage pages

### ​Move pages

 Drag and drop pages to reorder them in your navigation or move files between folders in the file tree.

### ​Duplicate pages

 Right-click a page and select **Duplicate**.

### ​Delete pages

 Right-click a page and select **Delete**. Deleting a page removes it from your navigation automatically.

### ​Hide pages

 To remove a page from navigation without deleting the file, right-click the page and click **Hide Page**. The file remains in your repository and you can unhide the page by adding it to your `docs.json` navigation.

---

# Publish changes in the web editor

> Save your work and publish changes to your documentation site.

## ​Publishing workflows

 The editor supports two workflows for publishing documentation updates. The workflow you use depends on your repository’s branch protection rules and the branch you work on.

- **Create pull requests**: If your repository has a branch protection rule that requires pull requests before changes can merge into your deployment branch, the editor creates a pull request when you publish changes.
- **Publish directly**: If your repository has no branch protection rules, your changes merge to the deployment branch and deploy immediately when you publish.

| Branch type | Branch protection | Publishing workflow |
| --- | --- | --- |
|  | None | Commits and deploys changes |
| Deployment branch | Pull requests required | Creates a pull request |
|  | None | Merges changes to deployment branch and deploys changes |
| Feature branch | Pull requests required | Creates a pull request |

 Configure branch protection rules in your Git provider to require pull requests. See [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) in the GitHub docs or [Protected branches](https://docs.gitlab.com/user/project/repository/branches/protected/) in the GitLab docs.

## ​Save changes

 As you edit, the editor tracks your changes.

- New or deleted files.
- Content edits in pages.
- Navigation structure changes.
- Media uploads and organization.
- Configuration updates.

 When you work on your deployment branch, your changes save automatically. ![Web editor toolbar showing one pending change.](https://mintcdn.com/mintlify/DLSr2FhOurD6ae47/images/editor/toolbar-light.png?fit=max&auto=format&n=DLSr2FhOurD6ae47&q=85&s=efde7a0f763db2116c4ee8ee2189c031)![Web editor toolbar showing one pending change.](https://mintcdn.com/mintlify/DLSr2FhOurD6ae47/images/editor/toolbar-dark.png?fit=max&auto=format&n=DLSr2FhOurD6ae47&q=85&s=1687db26e20f029dee0e824cdf45ee1c)

Changes on a deployment branch.

 When you work on a feature branch, you can save changes to the branch as . ![Web editor toolbar showing one pending change and the Save as commit button on a feature branch.](https://mintcdn.com/mintlify/DLSr2FhOurD6ae47/images/editor/toolbar-branch-light.png?fit=max&auto=format&n=DLSr2FhOurD6ae47&q=85&s=42bdbeaea7772e86fd6cdac02e415c74)![Web editor toolbar showing one pending change and the Save as commit button on a feature branch.](https://mintcdn.com/mintlify/DLSr2FhOurD6ae47/images/editor/toolbar-branch-dark.png?fit=max&auto=format&n=DLSr2FhOurD6ae47&q=85&s=67fc18a74266c7974bf278e8f6d5b2d0)

Changes on a feature branch.

 To discard changes, click **Undo changes** beside a file name in the **Changes** dropdown.

### ​Publish your changes

 Click **Publish** in the toolbar. Depending on your workflow, your changes deploy immediately or create a pull request for you to merge in your Git provider. If you are on a feature branch, save your changes before publishing. The **Publish** button is disabled when there are no pending changes or when a pull request for the current branch is already open.

## ​Resolve conflicts

 Conflicts occur when your branch and the deployment branch have incompatible changes to the same files.

### ​What causes conflicts

 Conflicts happen when:

- You and another team member edit the same lines in a file.
- Files are moved or deleted in one branch but modified in another.

### ​Resolve conflicts

 The editor displays warnings when conflicts prevent operations like publishing or switching branches. To resolve conflicts, follow the instructions in the editor to choose which changes to keep.

## ​Commit signing

 Sign commits with your GitHub account by authorizing it in your [account settings](https://dashboard.mintlify.com/settings/account). Without authorization, the Mintlify GitHub App signs commits made in the web editor. Attributing commits to your account maintains an accurate history of who made changes to your documentation.
