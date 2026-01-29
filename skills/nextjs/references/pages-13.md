# How to use CSS in your application and more

# How to use CSS in your application

> Learn about the different ways to add CSS to your application, including CSS Modules, Global CSS, Tailwind CSS, and more.

[Pages Router](https://nextjs.org/docs/pages)[Getting Started](https://nextjs.org/docs/pages/getting-started)CSSYou are currently viewing the documentation for Pages Router.

# How to use CSS in your application

Last updated  August 6, 2025

Next.js provides several ways to style your application using CSS, including:

- [Tailwind CSS](#tailwind-css)
- [CSS Modules](#css-modules)
- [Global CSS](#global-css)
- [External Stylesheets](#external-stylesheets)
- [Sass](https://nextjs.org/docs/app/guides/sass)
- [CSS-in-JS](https://nextjs.org/docs/app/guides/css-in-js)

## Tailwind CSS

[Tailwind CSS](https://tailwindcss.com/) is a utility-first CSS framework that provides low-level utility classes to build custom designs.

Install Tailwind CSS:

Terminal

```
pnpm add -D tailwindcss @tailwindcss/postcss
```

Add the PostCSS plugin to your `postcss.config.mjs` file:

postcss.config.mjs

```
export default {
  plugins: {
    '@tailwindcss/postcss': {},
  },
}
```

Import Tailwind in your global CSS file:

styles/globals.css

```
@import 'tailwindcss';
```

Import the CSS file in your `pages/_app.js` file:

pages/_app.js

```
import '@/styles/globals.css'

export default function MyApp({ Component, pageProps }) {
  return <Component {...pageProps} />
}
```

Now you can start using Tailwind's utility classes in your application:

pages/index.tsxJavaScriptTypeScript

```
export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <h1 className="text-4xl font-bold">Welcome to Next.js!</h1>
    </main>
  )
}
```

> **Good to know:** If you need broader browser support for very old browsers, see the [Tailwind CSS v3 setup instructions](https://nextjs.org/docs/app/guides/tailwind-v3-css).

## CSS Modules

CSS Modules locally scope CSS by generating unique class names. This allows you to use the same class in different files without worrying about naming collisions.

To start using CSS Modules, create a new file with the extension `.module.css` and import it into any component inside the `pages` directory:

/styles/blog.module.css

```
.blog {
  padding: 24px;
}
```

pages/blog/index.tsxJavaScriptTypeScript

```
import styles from './blog.module.css'

export default function Page() {
  return <main className={styles.blog}></main>
}
```

## Global CSS

You can use global CSS to apply styles across your application.

Import the stylesheet in the `pages/_app.js` file to apply the styles to **every route** in your application:

pages/_app.js

```
import '@/styles/global.css'

export default function MyApp({ Component, pageProps }) {
  return <Component {...pageProps} />
}
```

Due to the global nature of stylesheets, and to avoid conflicts, you should import them inside [pages/_app.js](https://nextjs.org/docs/pages/building-your-application/routing/custom-app).

## External stylesheets

Next.js allows you to import CSS files from a JavaScript file. This is possible because Next.js extends the concept of [import](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Statements/import) beyond JavaScript.

### Import styles fromnode_modules

Since Next.js **9.5.4**, importing a CSS file from `node_modules` is permitted anywhere in your application.

For global stylesheets, like `bootstrap` or `nprogress`, you should import the file inside `pages/_app.js`. For example:

pages/_app.js

```
import 'bootstrap/dist/css/bootstrap.css'

export default function MyApp({ Component, pageProps }) {
  return <Component {...pageProps} />
}
```

To import CSS required by a third-party component, you can do so in your component. For example:

components/example-dialog.js

```
import { useState } from 'react'
import { Dialog } from '@reach/dialog'
import VisuallyHidden from '@reach/visually-hidden'
import '@reach/dialog/styles.css'

function ExampleDialog(props) {
  const [showDialog, setShowDialog] = useState(false)
  const open = () => setShowDialog(true)
  const close = () => setShowDialog(false)

  return (
    <div>
      <button onClick={open}>Open Dialog</button>
      <Dialog isOpen={showDialog} onDismiss={close}>
        <button className="close-button" onClick={close}>
          <VisuallyHidden>Close</VisuallyHidden>
          <span aria-hidden>×</span>
        </button>
        <p>Hello there. I am a dialog</p>
      </Dialog>
    </div>
  )
}
```

## Ordering and Merging

Next.js optimizes CSS during production builds by automatically chunking (merging) stylesheets. The **order of your CSS** depends on the **order you import styles in your code**.

For example, `base-button.module.css` will be ordered before `page.module.css` since `<BaseButton>` is imported before `page.module.css`:

 page.tsxJavaScriptTypeScript

```
import { BaseButton } from './base-button'
import styles from './page.module.css'

export default function Page() {
  return <BaseButton className={styles.primary} />
}
```

   base-button.tsxJavaScriptTypeScript

```
import styles from './base-button.module.css'

export function BaseButton() {
  return <button className={styles.primary} />
}
```

### Recommendations

To keep CSS ordering predictable:

- Try to contain CSS imports to a single JavaScript or TypeScript entry file
- Import global styles and Tailwind stylesheets in the root of your application.
- **Use Tailwind CSS** for most styling needs as it covers common design patterns with utility classes.
- Use CSS Modules for component-specific styles when Tailwind utilities aren't sufficient.
- Use a consistent naming convention for your CSS modules. For example, using `<name>.module.css` over `<name>.tsx`.
- Extract shared styles into shared components to avoid duplicate imports.
- Turn off linters or formatters that auto-sort imports like ESLint’s [sort-imports](https://eslint.org/docs/latest/rules/sort-imports).
- You can use the [cssChunking](https://nextjs.org/docs/app/api-reference/config/next-config-js/cssChunking) option in `next.config.js` to control how CSS is chunked.

## Development vs Production

- In development (`next dev`), CSS updates apply instantly with [Fast Refresh](https://nextjs.org/docs/architecture/fast-refresh).
- In production (`next build`), all CSS files are automatically concatenated into **many minified and code-split** `.css` files, ensuring the minimal amount of CSS is loaded for a route.
- CSS still loads with JavaScript disabled in production, but JavaScript is required in development for Fast Refresh.
- CSS ordering can behave differently in development, always ensure to check the build (`next build`) to verify the final CSS order.

## Next Steps

Learn more about the features mentioned in this page.[Tailwind CSSStyle your Next.js Application using Tailwind CSS.](https://nextjs.org/docs/pages/guides/tailwind-v3-css)[SassLearn how to use Sass in your Next.js application.](https://nextjs.org/docs/pages/guides/sass)[CSS-in-JSUse CSS-in-JS libraries with Next.js](https://nextjs.org/docs/pages/guides/css-in-js)

Was this helpful?

supported.

---

# How to deploy your Next.js application

> Learn how to deploy your Next.js application.

[Pages Router](https://nextjs.org/docs/pages)[Getting Started](https://nextjs.org/docs/pages/getting-started)DeployingYou are currently viewing the documentation for Pages Router.

# How to deploy your Next.js application

Last updated  April 22, 2025

Next.js can be deployed as a Node.js server, Docker container, static export, or adapted to run on different platforms.

| Deployment Option | Feature Support |
| --- | --- |
| Node.js server | All |
| Docker container | All |
| Static export | Limited |
| Adapters | Platform-specific |

## Node.js server

Next.js can be deployed to any provider that supports Node.js. Ensure your `package.json` has the `"build"` and `"start"` scripts:

 package.json

```
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  }
}
```

Then, run `npm run build` to build your application and `npm run start` to start the Node.js server. This server supports all Next.js features. If needed, you can also eject to a [custom server](https://nextjs.org/docs/app/guides/custom-server).

Node.js deployments support all Next.js features. Learn how to [configure them](https://nextjs.org/docs/app/guides/self-hosting) for your infrastructure.

### Templates

- [Flightcontrol](https://github.com/nextjs/deploy-flightcontrol)
- [Railway](https://github.com/nextjs/deploy-railway)
- [Replit](https://github.com/nextjs/deploy-replit)

## Docker

Next.js can be deployed to any provider that supports [Docker](https://www.docker.com/) containers. This includes container orchestrators like Kubernetes or a cloud provider that runs Docker.

Docker deployments support all Next.js features. Learn how to [configure them](https://nextjs.org/docs/app/guides/self-hosting) for your infrastructure.

> **Note for development:** While Docker is excellent for production deployments, consider using local development (`npm run dev`) instead of Docker during development on Mac and Windows for better performance. [Learn more about optimizing local development](https://nextjs.org/docs/app/guides/local-development).

### Templates

- [Docker](https://github.com/vercel/next.js/tree/canary/examples/with-docker)
- [Docker Multi-Environment](https://github.com/vercel/next.js/tree/canary/examples/with-docker-multi-env)
- [DigitalOcean](https://github.com/nextjs/deploy-digitalocean)
- [Fly.io](https://github.com/nextjs/deploy-fly)
- [Google Cloud Run](https://github.com/nextjs/deploy-google-cloud-run)
- [Render](https://github.com/nextjs/deploy-render)
- [SST](https://github.com/nextjs/deploy-sst)

## Static export

Next.js enables starting as a static site or [Single-Page Application (SPA)](https://nextjs.org/docs/app/guides/single-page-applications), then later optionally upgrading to use features that require a server.

Since Next.js supports [static exports](https://nextjs.org/docs/app/guides/static-exports), it can be deployed and hosted on any web server that can serve HTML/CSS/JS static assets. This includes tools like AWS S3, Nginx, or Apache.

Running as a [static export](https://nextjs.org/docs/app/guides/static-exports) **does not** support Next.js features that require a server. [Learn more](https://nextjs.org/docs/app/guides/static-exports#unsupported-features).

### Templates

- [GitHub Pages](https://github.com/nextjs/deploy-github-pages)

## Adapters

Next.js can be adapted to run on different platforms to support their infrastructure capabilities.

Refer to each provider's documentation for information on supported Next.js features:

- [Appwrite Sites](https://appwrite.io/docs/products/sites/quick-start/nextjs)
- [AWS Amplify Hosting](https://docs.amplify.aws/nextjs/start/quickstart/nextjs-app-router-client-components)
- [Cloudflare](https://developers.cloudflare.com/workers/frameworks/framework-guides/nextjs)
- [Deno Deploy](https://docs.deno.com/examples/next_tutorial)
- [Firebase App Hosting](https://firebase.google.com/docs/app-hosting/get-started)
- [Netlify](https://docs.netlify.com/frameworks/next-js/overview/#next-js-support-on-netlify)
- [Vercel](https://vercel.com/docs/frameworks/nextjs)

> **Note:** We are working on a [Deployment Adapters API](https://github.com/vercel/next.js/discussions/77740) for all platforms to adopt. After completion, we will add documentation on how to write your own adapters.

Was this helpful?

supported.

---

# How to use fonts

> Learn how to use fonts in Next.js

[Pages Router](https://nextjs.org/docs/pages)[Getting Started](https://nextjs.org/docs/pages/getting-started)FontsYou are currently viewing the documentation for Pages Router.

# How to use fonts

Last updated  May 8, 2025

The [next/font](https://nextjs.org/docs/app/api-reference/components/font) module automatically optimizes your fonts and removes external network requests for improved privacy and performance.

It includes **built-in self-hosting** for any font file. This means you can optimally load web fonts with no layout shift.

To start using `next/font`, import it from [next/font/local](#local-fonts) or [next/font/google](#google-fonts), call it as a function with the appropriate options, and set the `className` of the element you want to apply the font to. For example, you can apply fonts globally in your [Custom App](https://nextjs.org/docs/pages/building-your-application/routing/custom-app) (`pages/_app`):

pages/_app.tsxJavaScriptTypeScript

```
import { Geist } from 'next/font/google'
import type { AppProps } from 'next/app'

const geist = Geist({
  subsets: ['latin'],
})

export default function MyApp({ Component, pageProps }: AppProps) {
  return (
    <main className={geist.className}>
      <Component {...pageProps} />
    </main>
  )
}
```

If you want to apply the font to the `<html>` element, you can use a [Custom Document](https://nextjs.org/docs/pages/building-your-application/routing/custom-document) (`pages/_document`):

pages/_document.tsxJavaScriptTypeScript

```
import { Html, Head, Main, NextScript } from 'next/document'
import { Geist } from 'next/font/google'

const geist = Geist({
  subsets: ['latin'],
})

export default function Document() {
  return (
    <Html lang="en" className={geist.className}>
      <Head />
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  )
}
```

## Google fonts

You can automatically self-host any Google Font. Fonts are included stored as static assets and served from the same domain as your deployment, meaning no requests are sent to Google by the browser when the user visits your site.

To start using a Google Font, import your chosen font from `next/font/google`:

   pages/_app.tsxJavaScriptTypeScript

```
import { Geist } from 'next/font/google'
import type { AppProps } from 'next/app'

const geist = Geist({
  subsets: ['latin'],
})

export default function MyApp({ Component, pageProps }: AppProps) {
  return (
    <main className={geist.className}>
      <Component {...pageProps} />
    </main>
  )
}
```

We recommend using [variable fonts](https://fonts.google.com/variablefonts) for the best performance and flexibility. But if you can't use a variable font, you will need to specify a weight:

   pages/_app.tsxJavaScriptTypeScript

```
import { Roboto } from 'next/font/google'
import type { AppProps } from 'next/app'

const roboto = Roboto({
  weight: '400',
  subsets: ['latin'],
})

export default function MyApp({ Component, pageProps }: AppProps) {
  return (
    <main className={roboto.className}>
      <Component {...pageProps} />
    </main>
  )
}
```

## Local fonts

To use a local font, import your font from `next/font/local` and specify the [src](https://nextjs.org/docs/pages/api-reference/components/font#src) of your local font file. Fonts can be stored in the [public](https://nextjs.org/docs/pages/api-reference/file-conventions/public-folder) folder or inside the `pages` folder. For example:

pages/_app.tsxJavaScriptTypeScript

```
import localFont from 'next/font/local'
import type { AppProps } from 'next/app'

const myFont = localFont({
  src: './my-font.woff2',
})

export default function MyApp({ Component, pageProps }: AppProps) {
  return (
    <main className={myFont.className}>
      <Component {...pageProps} />
    </main>
  )
}
```

If you want to use multiple files for a single font family, `src` can be an array:

```
const roboto = localFont({
  src: [
    {
      path: './Roboto-Regular.woff2',
      weight: '400',
      style: 'normal',
    },
    {
      path: './Roboto-Italic.woff2',
      weight: '400',
      style: 'italic',
    },
    {
      path: './Roboto-Bold.woff2',
      weight: '700',
      style: 'normal',
    },
    {
      path: './Roboto-BoldItalic.woff2',
      weight: '700',
      style: 'italic',
    },
  ],
})
```

## API Reference

See the API Reference for the full feature set of Next.js Font[FontAPI Reference for the Font Module](https://nextjs.org/docs/pages/api-reference/components/font)

Was this helpful?

supported.

---

# Image Optimization

> Optimize your images with the built-in `next/image` component.

[Pages Router](https://nextjs.org/docs/pages)[Getting Started](https://nextjs.org/docs/pages/getting-started)ImagesYou are currently viewing the documentation for Pages Router.

# Image Optimization

Last updated  May 8, 2025

The Next.js [<Image>](https://nextjs.org/docs/app/api-reference/components/image) component extends the HTML `<img>` element to provide:

- **Size optimization:** Automatically serving correctly sized images for each device, using modern image formats like WebP.
- **Visual stability:** Preventing [layout shift](https://web.dev/articles/cls) automatically when images are loading.
- **Faster page loads:** Only loading images when they enter the viewport using native browser lazy loading, with optional blur-up placeholders.
- **Asset flexibility:** Resizing images on-demand, even images stored on remote servers.

To start using `<Image>`, import it from `next/image` and render it within your component.

 app/page.tsxJavaScriptTypeScript

```
import Image from 'next/image'

export default function Page() {
  return <Image src="" alt="" />
}
```

The `src` property can be a [local](#local-images) or [remote](#remote-images) image.

> **🎥 Watch:** Learn more about how to use `next/image` → [YouTube (9 minutes)](https://youtu.be/IU_qq_c_lKA).

## Local images

You can store static files, like images and fonts, under a folder called [public](https://nextjs.org/docs/app/api-reference/file-conventions/public-folder) in the root directory. Files inside `public` can then be referenced by your code starting from the base URL (`/`).

 ![Folder structure showing app and public folders](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Fpublic-folder.png&w=3840&q=75)![Folder structure showing app and public folders](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Fpublic-folder.png&w=3840&q=75) app/page.tsxJavaScriptTypeScript

```
import Image from 'next/image'

export default function Page() {
  return (
    <Image
      src="/profile.png"
      alt="Picture of the author"
      width={500}
      height={500}
    />
  )
}
```

If the image is statically imported, Next.js will automatically determine the intrinsic [width](https://nextjs.org/docs/app/api-reference/components/image#width-and-height) and [height](https://nextjs.org/docs/app/api-reference/components/image#width-and-height). These values are used to determine the image ratio and prevent [Cumulative Layout Shift](https://web.dev/articles/cls) while your image is loading.

 app/page.tsxJavaScriptTypeScript

```
import Image from 'next/image'
import ProfileImage from './profile.png'

export default function Page() {
  return (
    <Image
      src={ProfileImage}
      alt="Picture of the author"
      // width={500} automatically provided
      // height={500} automatically provided
      // blurDataURL="data:..." automatically provided
      // placeholder="blur" // Optional blur-up while loading
    />
  )
}
```

## Remote images

To use a remote image, you can provide a URL string for the `src` property.

 app/page.tsxJavaScriptTypeScript

```
import Image from 'next/image'

export default function Page() {
  return (
    <Image
      src="https://s3.amazonaws.com/my-bucket/profile.png"
      alt="Picture of the author"
      width={500}
      height={500}
    />
  )
}
```

Since Next.js does not have access to remote files during the build process, you'll need to provide the [width](https://nextjs.org/docs/app/api-reference/components/image#width-and-height), [height](https://nextjs.org/docs/app/api-reference/components/image#width-and-height) and optional [blurDataURL](https://nextjs.org/docs/app/api-reference/components/image#blurdataurl) props manually. The `width` and `height` are used to infer the correct aspect ratio of image and avoid layout shift from the image loading in. Alternatively, you can use the [fillproperty](https://nextjs.org/docs/app/api-reference/components/image#fill) to make the image fill the size of the parent element.

To safely allow images from remote servers, you need to define a list of supported URL patterns in [next.config.js](https://nextjs.org/docs/app/api-reference/config/next-config-js). Be as specific as possible to prevent malicious usage. For example, the following configuration will only allow images from a specific AWS S3 bucket:

 next.config.tsJavaScriptTypeScript

```
import type { NextConfig } from 'next'

const config: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 's3.amazonaws.com',
        port: '',
        pathname: '/my-bucket/**',
        search: '',
      },
    ],
  },
}

export default config
```

## API Reference

See the API Reference for the full feature set of Next.js Image[ImageOptimize Images in your Next.js Application using the built-in `next/image` Component.](https://nextjs.org/docs/pages/api-reference/components/image)

Was this helpful?

supported.

---

# Create a new Next.js application

> How to create a new Next.js application with `create-next-app`. Set up TypeScript, ESLint,and configure your `next.config.js` file.

[Pages Router](https://nextjs.org/docs/pages)[Getting Started](https://nextjs.org/docs/pages/getting-started)InstallationYou are currently viewing the documentation for Pages Router.

# Create a new Next.js application

Last updated  November 6, 2024

## System requirements

Before you begin, make sure your development environment meets the following requirements:

- Minimum Node.js version: [20.9](https://nodejs.org/)
- Operating systems: macOS, Windows (including WSL), and Linux.

## Supported browsers

Next.js supports modern browsers with zero configuration.

- Chrome 111+
- Edge 111+
- Firefox 111+
- Safari 16.4+

Learn more about [browser support](https://nextjs.org/docs/architecture/supported-browsers), including how to configure polyfills and target specific browsers.

## Create with the CLI

The quickest way to create a new Next.js app is using [create-next-app](https://nextjs.org/docs/app/api-reference/cli/create-next-app), which sets up everything automatically for you. To create a project, run:

 Terminal

```
npx create-next-app@latest
```

On installation, you'll see the following prompts:

 Terminal

```
What is your project named? my-app
Would you like to use the recommended Next.js defaults?
    Yes, use recommended defaults - TypeScript, ESLint, Tailwind CSS, App Router, Turbopack
    No, reuse previous settings
    No, customize settings - Choose your own preferences
```

If you choose to `customize settings`, you'll see the following prompts:

 Terminal

```
Would you like to use TypeScript? No / Yes
Which linter would you like to use? ESLint / Biome / None
Would you like to use React Compiler? No / Yes
Would you like to use Tailwind CSS? No / Yes
Would you like your code inside a `src/` directory? No / Yes
Would you like to use App Router? (recommended) No / Yes
Would you like to customize the import alias (`@/*` by default)? No / Yes
What import alias would you like configured? @/*
```

After the prompts, [create-next-app](https://nextjs.org/docs/app/api-reference/cli/create-next-app) will create a folder with your project name and install the required dependencies.

## Manual installation

To manually create a new Next.js app, install the required packages:

 Terminal

```
pnpm i next@latest react@latest react-dom@latest
```

> **Good to know**: The App Router uses [React canary releases](https://react.dev/blog/2023/05/03/react-canaries) built-in, which include all the stable React 19 changes, as well as newer features being validated in frameworks. The Pages Router uses the React version you install in `package.json`.

Then, add the following scripts to your `package.json` file:

 package.json

```
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "eslint",
    "lint:fix": "eslint --fix"
  }
}
```

These scripts refer to the different stages of developing an application:

- `next dev`: Starts the development server using Turbopack (default bundler).
- `next build`: Builds the application for production.
- `next start`: Starts the production server.
- `eslint`: Runs ESLint.

Turbopack is now the default bundler. To use Webpack run `next dev --webpack` or `next build --webpack`. See the [Turbopack docs](https://nextjs.org/docs/app/api-reference/turbopack) for configuration details.

### Create thepagesdirectory

Next.js uses file-system routing, which means the routes in your application are determined by how you structure your files.

Create a `pages` directory at the root of your project. Then, add an `index.tsx` file inside your `pages` folder. This will be your home page (`/`):

pages/index.tsxJavaScriptTypeScript

```
export default function Page() {
  return <h1>Hello, Next.js!</h1>
}
```

Next, add an `_app.tsx` file inside `pages/` to define the global layout. Learn more about the [custom App file](https://nextjs.org/docs/pages/building-your-application/routing/custom-app).

pages/_app.tsxJavaScriptTypeScript

```
import type { AppProps } from 'next/app'

export default function App({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />
}
```

Finally, add a `_document.tsx` file inside `pages/` to control the initial response from the server. Learn more about the [custom Document file](https://nextjs.org/docs/pages/building-your-application/routing/custom-document).

pages/_document.tsxJavaScriptTypeScript

```
import { Html, Head, Main, NextScript } from 'next/document'

export default function Document() {
  return (
    <Html>
      <Head />
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  )
}
```

### Create thepublicfolder (optional)

Create a [publicfolder](https://nextjs.org/docs/app/api-reference/file-conventions/public-folder) at the root of your project to store static assets such as images, fonts, etc. Files inside `public` can then be referenced by your code starting from the base URL (`/`).

You can then reference these assets using the root path (`/`). For example, `public/profile.png` can be referenced as `/profile.png`:

 app/page.tsxJavaScriptTypeScript

```
import Image from 'next/image'

export default function Page() {
  return <Image src="/profile.png" alt="Profile" width={100} height={100} />
}
```

## Run the development server

1. Run `npm run dev` to start the development server.
2. Visit `http://localhost:3000` to view your application.
3. Edit the `pages/index.tsx` file and save it to see the updated result in your browser.

## Set up TypeScript

> Minimum TypeScript version: `v5.1.0`

Next.js comes with built-in TypeScript support. To add TypeScript to your project, rename a file to `.ts` / `.tsx` and run `next dev`. Next.js will automatically install the necessary dependencies and add a `tsconfig.json` file with the recommended config options.

See the [TypeScript reference](https://nextjs.org/docs/app/api-reference/config/typescript) page for more information.

## Set up linting

Next.js supports linting with either ESLint or Biome. Choose a linter and run it directly via `package.json` scripts.

- Use **ESLint** (comprehensive rules):

 package.json

```
{
  "scripts": {
    "lint": "eslint",
    "lint:fix": "eslint --fix"
  }
}
```

- Or use **Biome** (fast linter + formatter):

 package.json

```
{
  "scripts": {
    "lint": "biome check",
    "format": "biome format --write"
  }
}
```

If your project previously used `next lint`, migrate your scripts to the ESLint CLI with the codemod:

 Terminal

```
npx @next/codemod@canary next-lint-to-eslint-cli .
```

If you use ESLint, create an explicit config (recommended `eslint.config.mjs`). ESLint supports both [the legacy.eslintrc.*and the newereslint.config.mjsformats](https://eslint.org/docs/latest/use/configure/configuration-files#configuring-eslint). See the [ESLint API reference](https://nextjs.org/docs/app/api-reference/config/eslint#with-core-web-vitals) for a recommended setup.

> **Good to know**: Starting with Next.js 16, `next build` no longer runs the linter automatically. Instead, you can run your linter through NPM scripts.

See the [ESLint Plugin](https://nextjs.org/docs/app/api-reference/config/eslint) page for more information.

## Set up Absolute Imports and Module Path Aliases

Next.js has in-built support for the `"paths"` and `"baseUrl"` options of `tsconfig.json` and `jsconfig.json` files.

These options allow you to alias project directories to absolute paths, making it easier and cleaner to import modules. For example:

```
// Before
import { Button } from '../../../components/button'

// After
import { Button } from '@/components/button'
```

To configure absolute imports, add the `baseUrl` configuration option to your `tsconfig.json` or `jsconfig.json` file. For example:

 tsconfig.json or jsconfig.json

```
{
  "compilerOptions": {
    "baseUrl": "src/"
  }
}
```

In addition to configuring the `baseUrl` path, you can use the `"paths"` option to `"alias"` module paths.

For example, the following configuration maps `@/components/*` to `components/*`:

 tsconfig.json or jsconfig.json

```
{
  "compilerOptions": {
    "baseUrl": "src/",
    "paths": {
      "@/styles/*": ["styles/*"],
      "@/components/*": ["components/*"]
    }
  }
}
```

Each of the `"paths"` are relative to the `baseUrl` location.

Was this helpful?

supported.

---

# Project Structure and Organization

> Learn about the folder and file conventions in a Next.js project, and how to organize your project.

[Pages Router](https://nextjs.org/docs/pages)[Getting Started](https://nextjs.org/docs/pages/getting-started)Project StructureYou are currently viewing the documentation for Pages Router.

# Project Structure and Organization

Last updated  November 7, 2024

This page provides an overview of **all** the folder and file conventions in Next.js, and recommendations for organizing your project.

## Folder and file conventions

### Top-level folders

Top-level folders are used to organize your application's code and static assets.

 ![Route segments to path segments](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Flight%2Ftop-level-folders.png&w=3840&q=75)![Route segments to path segments](https://nextjs.org/_next/image?url=https%3A%2F%2Fh8DxKfmAPhn8O0p3.public.blob.vercel-storage.com%2Fdocs%2Fdark%2Ftop-level-folders.png&w=3840&q=75)

|  |  |
| --- | --- |
| app | App Router |
| pages | Pages Router |
| public | Static assets to be served |
| src | Optional application source folder |

### Top-level files

Top-level files are used to configure your application, manage dependencies, run proxy, integrate monitoring tools, and define environment variables.

|  |  |
| --- | --- |
| Next.js |  |
| next.config.js | Configuration file for Next.js |
| package.json | Project dependencies and scripts |
| instrumentation.ts | OpenTelemetry and Instrumentation file |
| proxy.ts | Next.js request proxy |
| .env | Environment variables (should not be tracked by version control) |
| .env.local | Local environment variables (should not be tracked by version control) |
| .env.production | Production environment variables (should not be tracked by version control) |
| .env.development | Development environment variables (should not be tracked by version control) |
| eslint.config.mjs | Configuration file for ESLint |
| .gitignore | Git files and folders to ignore |
| next-env.d.ts | TypeScript declaration file for Next.js (should not be tracked by version control) |
| tsconfig.json | Configuration file for TypeScript |
| jsconfig.json | Configuration file for JavaScript |

### File conventions

|  |  |  |
| --- | --- | --- |
| _app | .js.jsx.tsx | Custom App |
| _document | .js.jsx.tsx | Custom Document |
| _error | .js.jsx.tsx | Custom Error Page |
| 404 | .js.jsx.tsx | 404 Error Page |
| 500 | .js.jsx.tsx | 500 Error Page |

### Routes

|  |  |  |
| --- | --- | --- |
| Folder convention |  |  |
| index | .js.jsx.tsx | Home page |
| folder/index | .js.jsx.tsx | Nested page |
| File convention |  |  |
| index | .js.jsx.tsx | Home page |
| file | .js.jsx.tsx | Nested page |

### Dynamic routes

|  |  |  |
| --- | --- | --- |
| Folder convention |  |  |
| [folder]/index | .js.jsx.tsx | Dynamic route segment |
| [...folder]/index | .js.jsx.tsx | Catch-all route segment |
| [[...folder]]/index | .js.jsx.tsx | Optional catch-all route segment |
| File convention |  |  |
| [file] | .js.jsx.tsx | Dynamic route segment |
| [...file] | .js.jsx.tsx | Catch-all route segment |
| [[...file]] | .js.jsx.tsx | Optional catch-all route segment |

Was this helpful?

supported.

---

# Getting Started

> Learn how to create full-stack web applications with Next.js with the Pages Router.

[Next.js Docs](https://nextjs.org/docs)[Pages Router](https://nextjs.org/docs/pages)Getting StartedYou are currently viewing the documentation for Pages Router.

# Getting Started - Pages Router

Last updated  November 7, 2024[InstallationHow to create a new Next.js application with `create-next-app`. Set up TypeScript, ESLint,and configure your `next.config.js` file.](https://nextjs.org/docs/pages/getting-started/installation)[Project StructureLearn about the folder and file conventions in a Next.js project, and how to organize your project.](https://nextjs.org/docs/pages/getting-started/project-structure)[ImagesOptimize your images with the built-in `next/image` component.](https://nextjs.org/docs/pages/getting-started/images)[FontsLearn how to use fonts in Next.js](https://nextjs.org/docs/pages/getting-started/fonts)[CSSLearn about the different ways to add CSS to your application, including CSS Modules, Global CSS, Tailwind CSS, and more.](https://nextjs.org/docs/pages/getting-started/css)[DeployingLearn how to deploy your Next.js application.](https://nextjs.org/docs/pages/getting-started/deploying)

Was this helpful?

supported.

---

# How to set up analytics

> Measure and track page performance using Next.js

[Pages Router](https://nextjs.org/docs/pages)[Guides](https://nextjs.org/docs/pages/guides)AnalyticsYou are currently viewing the documentation for Pages Router.

# How to set up analytics

Last updated  April 24, 2025

Next.js has built-in support for measuring and reporting performance metrics. You can either use the [useReportWebVitals](https://nextjs.org/docs/app/api-reference/functions/use-report-web-vitals) hook to manage reporting yourself, or alternatively, Vercel provides a [managed service](https://vercel.com/analytics?utm_source=next-site&utm_medium=docs&utm_campaign=next-website) to automatically collect and visualize metrics for you.

## Client Instrumentation

For more advanced analytics and monitoring needs, Next.js provides a `instrumentation-client.js|ts` file that runs before your application's frontend code starts executing. This is ideal for setting up global analytics, error tracking, or performance monitoring tools.

To use it, create an `instrumentation-client.js` or `instrumentation-client.ts` file in your application's root directory:

 instrumentation-client.js

```
// Initialize analytics before the app starts
console.log('Analytics initialized')

// Set up global error tracking
window.addEventListener('error', (event) => {
  // Send to your error tracking service
  reportError(event.error)
})
```

## Build Your Own

 pages/_app.js

```
import { useReportWebVitals } from 'next/web-vitals'

function MyApp({ Component, pageProps }) {
  useReportWebVitals((metric) => {
    console.log(metric)
  })

  return <Component {...pageProps} />
}
```

View the [API Reference](https://nextjs.org/docs/pages/api-reference/functions/use-report-web-vitals) for more information.

## Web Vitals

[Web Vitals](https://web.dev/vitals/) are a set of useful metrics that aim to capture the user
experience of a web page. The following web vitals are all included:

- [Time to First Byte](https://developer.mozilla.org/docs/Glossary/Time_to_first_byte) (TTFB)
- [First Contentful Paint](https://developer.mozilla.org/docs/Glossary/First_contentful_paint) (FCP)
- [Largest Contentful Paint](https://web.dev/lcp/) (LCP)
- [First Input Delay](https://web.dev/fid/) (FID)
- [Cumulative Layout Shift](https://web.dev/cls/) (CLS)
- [Interaction to Next Paint](https://web.dev/inp/) (INP)

You can handle all the results of these metrics using the `name` property.

 pages/_app.js

```
import { useReportWebVitals } from 'next/web-vitals'

function MyApp({ Component, pageProps }) {
  useReportWebVitals((metric) => {
    switch (metric.name) {
      case 'FCP': {
        // handle FCP results
      }
      case 'LCP': {
        // handle LCP results
      }
      // ...
    }
  })

  return <Component {...pageProps} />
}
```

## Custom Metrics

In addition to the core metrics listed above, there are some additional custom metrics that
measure the time it takes for the page to hydrate and render:

- `Next.js-hydration`: Length of time it takes for the page to start and finish hydrating (in ms)
- `Next.js-route-change-to-render`: Length of time it takes for a page to start rendering after a
  route change (in ms)
- `Next.js-render`: Length of time it takes for a page to finish render after a route change (in ms)

You can handle all the results of these metrics separately:

```
export function reportWebVitals(metric) {
  switch (metric.name) {
    case 'Next.js-hydration':
      // handle hydration results
      break
    case 'Next.js-route-change-to-render':
      // handle route-change to render results
      break
    case 'Next.js-render':
      // handle render results
      break
    default:
      break
  }
}
```

These metrics work in all browsers that support the [User Timing API](https://caniuse.com/#feat=user-timing).

## Sending results to external systems

You can send results to any endpoint to measure and track
real user performance on your site. For example:

```
useReportWebVitals((metric) => {
  const body = JSON.stringify(metric)
  const url = 'https://example.com/analytics'

  // Use `navigator.sendBeacon()` if available, falling back to `fetch()`.
  if (navigator.sendBeacon) {
    navigator.sendBeacon(url, body)
  } else {
    fetch(url, { body, method: 'POST', keepalive: true })
  }
})
```

> **Good to know**: If you use [Google Analytics](https://analytics.google.com/analytics/web/), using the
> `id` value can allow you to construct metric distributions manually (to calculate percentiles,
> etc.)

> ```
> useReportWebVitals((metric) => {
>   // Use `window.gtag` if you initialized Google Analytics as this example:
>   // https://github.com/vercel/next.js/blob/canary/examples/with-google-analytics
>   window.gtag('event', metric.name, {
>     value: Math.round(
>       metric.name === 'CLS' ? metric.value * 1000 : metric.value
>     ), // values must be integers
>     event_label: metric.id, // id unique to current page load
>     non_interaction: true, // avoids affecting bounce rate.
>   })
> })
> ```
>
>
>
> Read more about [sending results to Google Analytics](https://github.com/GoogleChrome/web-vitals#send-the-results-to-google-analytics).

Was this helpful?

supported.
