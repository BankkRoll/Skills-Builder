# How to use and optimize videos and more

# How to use and optimize videos

> Recommendations and best practices for optimizing videos in your Next.js application.

[App Router](https://nextjs.org/docs/app)[Guides](https://nextjs.org/docs/app/guides)Videos

# How to use and optimize videos

Last updated  September 3, 2025

This page outlines how to use videos with Next.js applications, showing how to store and display video files without affecting performance.

## Using<video>and<iframe>

Videos can be embedded on the page using the HTML **<video>** tag for direct video files and **<iframe>** for external platform-hosted videos.

### <video>

The HTML [<video>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/video) tag can embed self-hosted or directly served video content, allowing full control over the playback and appearance.

 app/ui/video.jsx

```
export function Video() {
  return (
    <video width="320" height="240" controls preload="none">
      <source src="/path/to/video.mp4" type="video/mp4" />
      <track
        src="/path/to/captions.vtt"
        kind="subtitles"
        srcLang="en"
        label="English"
      />
      Your browser does not support the video tag.
    </video>
  )
}
```

### Common<video>tag attributes

| Attribute | Description | Example Value |
| --- | --- | --- |
| src | Specifies the source of the video file. | <video src="/path/to/video.mp4" /> |
| width | Sets the width of the video player. | <video width="320" /> |
| height | Sets the height of the video player. | <video height="240" /> |
| controls | If present, it displays the default set of playback controls. | <video controls /> |
| autoPlay | Automatically starts playing the video when the page loads. Note: Autoplay policies vary across browsers. | <video autoPlay /> |
| loop | Loops the video playback. | <video loop /> |
| muted | Mutes the audio by default. Often used withautoPlay. | <video muted /> |
| preload | Specifies how the video is preloaded. Values:none,metadata,auto. | <video preload="none" /> |
| playsInline | Enables inline playback on iOS devices, often necessary for autoplay to work on iOS Safari. | <video playsInline /> |

> **Good to know**: When using the `autoPlay` attribute, it is important to also include the `muted` attribute to ensure the video plays automatically in most browsers and the `playsInline` attribute for compatibility with iOS devices.

For a comprehensive list of video attributes, refer to the [MDN documentation](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/video#attributes).

### Video best practices

- **Fallback Content:** When using the `<video>` tag, include fallback content inside the tag for browsers that do not support video playback.
- **Subtitles or Captions:** Include subtitles or captions for users who are deaf or hard of hearing. Utilize the [<track>](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/track) tag with your `<video>` elements to specify caption file sources.
- **Accessible Controls:** Standard HTML5 video controls are recommended for keyboard navigation and screen reader compatibility. For advanced needs, consider third-party players like [react-player](https://github.com/cookpete/react-player) or [video.js](https://videojs.com/), which offer accessible controls and consistent browser experience.

### <iframe>

The HTML `<iframe>` tag allows you to embed videos from external platforms like YouTube or Vimeo.

 app/page.jsx

```
export default function Page() {
  return (
    <iframe src="https://www.youtube.com/embed/19g66ezsKAg" allowFullScreen />
  )
}
```

### Common<iframe>tag attributes

| Attribute | Description | Example Value |
| --- | --- | --- |
| src | The URL of the page to embed. | <iframe src="https://example.com" /> |
| width | Sets the width of the iframe. | <iframe width="500" /> |
| height | Sets the height of the iframe. | <iframe height="300" /> |
| allowFullScreen | Allows the iframe content to be displayed in full-screen mode. | <iframe allowFullScreen /> |
| sandbox | Enables an extra set of restrictions on the content within the iframe. | <iframe sandbox /> |
| loading | Optimize loading behavior (e.g., lazy loading). | <iframe loading="lazy" /> |
| title | Provides a title for the iframe to support accessibility. | <iframe title="Description" /> |

For a comprehensive list of iframe attributes, refer to the [MDN documentation](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe#attributes).

### Choosing a video embedding method

There are two ways you can embed videos in your Next.js application:

- **Self-hosted or direct video files:** Embed self-hosted videos using the `<video>` tag for scenarios requiring detailed control over the player's functionality and appearance. This integration method within Next.js allows for customization and control of your video content.
- **Using video hosting services (YouTube, Vimeo, etc.):** For video hosting services like YouTube or Vimeo, you'll embed their iframe-based players using the `<iframe>` tag. While this method limits some control over the player, it offers ease of use and features provided by these platforms.

Choose the embedding method that aligns with your application's requirements and the user experience you aim to deliver.

### Embedding externally hosted videos

To embed videos from external platforms, you can use Next.js to fetch the video information and React Suspense to handle the fallback state while loading.

**1. Create a Server Component for video embedding**

The first step is to create a [Server Component](https://nextjs.org/docs/app/getting-started/server-and-client-components) that generates the appropriate iframe for embedding the video. This component will fetch the source URL for the video and render the iframe.

 app/ui/video-component.jsx

```
export default async function VideoComponent() {
  const src = await getVideoSrc()

  return <iframe src={src} allowFullScreen />
}
```

**2. Stream the video component using React Suspense**

After creating the Server Component to embed the video, the next step is to [stream](https://nextjs.org/docs/app/api-reference/file-conventions/loading) the component using [React Suspense](https://react.dev/reference/react/Suspense).

 app/page.jsx

```
import { Suspense } from 'react'
import VideoComponent from '../ui/VideoComponent.jsx'

export default function Page() {
  return (
    <section>
      <Suspense fallback={<p>Loading video...</p>}>
        <VideoComponent />
      </Suspense>
      {/* Other content of the page */}
    </section>
  )
}
```

> **Good to know**: When embedding videos from external platforms, consider the following best practices:
>
>
>
> - Ensure the video embeds are responsive. Use CSS to make the iframe or video player adapt to different screen sizes.
> - Implement [strategies for loading videos](https://yoast.com/site-speed-tips-for-faster-video/) based on network conditions, especially for users with limited data plans.

This approach results in a better user experience as it prevents the page from blocking, meaning the user can interact with the page while the video component streams in.

For a more engaging and informative loading experience, consider using a loading skeleton as the fallback UI. So instead of showing a simple loading message, you can show a skeleton that resembles the video player like this:

 app/page.jsx

```
import { Suspense } from 'react'
import VideoComponent from '../ui/VideoComponent.jsx'
import VideoSkeleton from '../ui/VideoSkeleton.jsx'

export default function Page() {
  return (
    <section>
      <Suspense fallback={<VideoSkeleton />}>
        <VideoComponent />
      </Suspense>
      {/* Other content of the page */}
    </section>
  )
}
```

## Self-hosted videos

Self-hosting videos may be preferable for several reasons:

- **Complete control and independence**: Self-hosting gives you direct management over your video content, from playback to appearance, ensuring full ownership and control, free from external platform constraints.
- **Customization for specific needs**: Ideal for unique requirements, like dynamic background videos, it allows for tailored customization to align with design and functional needs.
- **Performance and scalability considerations**: Choose storage solutions that are both high-performing and scalable, to support increasing traffic and content size effectively.
- **Cost and integration**: Balance the costs of storage and bandwidth with the need for easy integration into your Next.js framework and broader tech ecosystem.

### Using Vercel Blob for video hosting

[Vercel Blob](https://vercel.com/docs/storage/vercel-blob?utm_source=next-site&utm_medium=docs&utm_campaign=next-website) offers an efficient way to host videos, providing a scalable cloud storage solution that works well with Next.js. Here's how you can host a video using Vercel Blob:

**1. Uploading a video to Vercel Blob**

In your Vercel dashboard, navigate to the "Storage" tab and select your [Vercel Blob](https://vercel.com/docs/storage/vercel-blob?utm_source=next-site&utm_medium=docs&utm_campaign=next-website) store. In the Blob table's upper-right corner, find and click the "Upload" button. Then, choose the video file you wish to upload. After the upload completes, the video file will appear in the Blob table.

Alternatively, you can upload your video using a server action. For detailed instructions, refer to the Vercel documentation on [server-side uploads](https://vercel.com/docs/storage/vercel-blob/server-upload). Vercel also supports [client-side uploads](https://vercel.com/docs/storage/vercel-blob/client-upload). This method may be preferable for certain use cases.

**2. Displaying the video in Next.js**

Once the video is uploaded and stored, you can display it in your Next.js application. Here's an example of how to do this using the `<video>` tag and React Suspense:

 app/page.jsx

```
import { Suspense } from 'react'
import { list } from '@vercel/blob'

export default function Page() {
  return (
    <Suspense fallback={<p>Loading video...</p>}>
      <VideoComponent fileName="my-video.mp4" />
    </Suspense>
  )
}

async function VideoComponent({ fileName }) {
  const { blobs } = await list({
    prefix: fileName,
    limit: 1,
  })
  const { url } = blobs[0]

  return (
    <video controls preload="none" aria-label="Video player">
      <source src={url} type="video/mp4" />
      Your browser does not support the video tag.
    </video>
  )
}
```

In this approach, the page uses the video's `@vercel/blob` URL to display the video using the `VideoComponent`. React Suspense is used to show a fallback until the video URL is fetched and the video is ready to be displayed.

### Adding subtitles to your video

If you have subtitles for your video, you can easily add them using the `<track>` element inside your `<video>` tag. You can fetch the subtitle file from [Vercel Blob](https://vercel.com/docs/storage/vercel-blob?utm_source=next-site&utm_medium=docs&utm_campaign=next-website) in a similar way as the video file. Here's how you can update the `<VideoComponent>` to include subtitles.

 app/page.jsx

```
async function VideoComponent({ fileName }) {
  const { blobs } = await list({
    prefix: fileName,
    limit: 2,
  })
  const { url } = blobs[0]
  const { url: captionsUrl } = blobs[1]

  return (
    <video controls preload="none" aria-label="Video player">
      <source src={url} type="video/mp4" />
      <track src={captionsUrl} kind="subtitles" srcLang="en" label="English" />
      Your browser does not support the video tag.
    </video>
  )
}
```

By following this approach, you can effectively self-host and integrate videos into your Next.js applications.

## Resources

To continue learning more about video optimization and best practices, please refer to the following resources:

- **Understanding video formats and codecs**: Choose the right format and codec, like MP4 for compatibility or WebM for web optimization, for your video needs. For more details, see [Mozilla's guide on video codecs](https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Video_codecs).
- **Video compression**: Use tools like FFmpeg to effectively compress videos, balancing quality with file size. Learn about compression techniques at [FFmpeg's official website](https://www.ffmpeg.org/).
- **Resolution and bitrate adjustment**: Adjust [resolution and bitrate](https://www.dacast.com/blog/bitrate-vs-resolution/#:~:text=The%20two%20measure%20different%20aspects,yield%20different%20qualities%20of%20video) based on the viewing platform, with lower settings for mobile devices.
- **Content Delivery Networks (CDNs)**: Utilize a CDN to enhance video delivery speed and manage high traffic. When using some storage solutions, such as Vercel Blob, CDN functionality is automatically handled for you. [Learn more](https://vercel.com/docs/edge-network/overview?utm_source=next-site&utm_medium=docs&utm_campaign=next-website) about CDNs and their benefits.

Explore these video streaming platforms for integrating video into your Next.js projects:

### Open sourcenext-videocomponent

- Provides a `<Video>` component for Next.js, compatible with various hosting services including [Vercel Blob](https://vercel.com/docs/storage/vercel-blob?utm_source=next-site&utm_medium=docs&utm_campaign=next-website), S3, Backblaze, and Mux.
- [Detailed documentation](https://next-video.dev/docs) for using `next-video.dev` with different hosting services.

### Cloudinary Integration

- Official [documentation and integration guide](https://next.cloudinary.dev/) for using Cloudinary with Next.js.
- Includes a `<CldVideoPlayer>` component for [drop-in video support](https://next.cloudinary.dev/cldvideoplayer/basic-usage).
- Find [examples](https://github.com/cloudinary-community/cloudinary-examples/?tab=readme-ov-file#nextjs) of integrating Cloudinary with Next.js including [Adaptive Bitrate Streaming](https://github.com/cloudinary-community/cloudinary-examples/tree/main/examples/nextjs-cldvideoplayer-abr).
- Other [Cloudinary libraries](https://cloudinary.com/documentation) including a Node.js SDK are also available.

### Mux Video API

- Mux provides a [starter template](https://github.com/muxinc/video-course-starter-kit) for creating a video course with Mux and Next.js.
- Learn about Mux's recommendations for embedding [high-performance video for your Next.js application](https://www.mux.com/for/nextjs).
- Explore an [example project](https://with-mux-video.vercel.app/) demonstrating Mux with Next.js.

### Fastly

- Learn more about integrating Fastly's solutions for [video on demand](https://www.fastly.com/products/streaming-media/video-on-demand) and streaming media into Next.js.

### ImageKit.io Integration

- Check out the [official quick start guide](https://imagekit.io/docs/integration/nextjs) for integrating ImageKit with Next.js.
- The integration provides an `<IKVideo>` component, offering [seamless video support](https://imagekit.io/docs/integration/nextjs#rendering-videos).
- You can also explore other [ImageKit libraries](https://imagekit.io/docs), such as the Node.js SDK, which is also available.

Was this helpful?

supported.

---

# Guides

> Learn how to implement common patterns and real-world use cases using Next.js

[Next.js Docs](https://nextjs.org/docs)[App Router](https://nextjs.org/docs/app)Guides

# Guides

Last updated  June 11, 2025[AnalyticsMeasure and track page performance using Next.js Speed Insights](https://nextjs.org/docs/app/guides/analytics)[AuthenticationLearn how to implement authentication in your Next.js application.](https://nextjs.org/docs/app/guides/authentication)[Backend for FrontendLearn how to use Next.js as a backend framework](https://nextjs.org/docs/app/guides/backend-for-frontend)[CachingAn overview of caching mechanisms in Next.js.](https://nextjs.org/docs/app/guides/caching)[CI Build CachingLearn how to configure CI to cache Next.js builds](https://nextjs.org/docs/app/guides/ci-build-caching)[Content Security PolicyLearn how to set a Content Security Policy (CSP) for your Next.js application.](https://nextjs.org/docs/app/guides/content-security-policy)[CSS-in-JSUse CSS-in-JS libraries with Next.js](https://nextjs.org/docs/app/guides/css-in-js)[Custom ServerStart a Next.js app programmatically using a custom server.](https://nextjs.org/docs/app/guides/custom-server)[Data SecurityLearn the built-in data security features in Next.js and learn best practices for protecting your application's data.](https://nextjs.org/docs/app/guides/data-security)[DebuggingLearn how to debug your Next.js application with VS Code, Chrome DevTools, or Firefox DevTools.](https://nextjs.org/docs/app/guides/debugging)[Draft ModeNext.js has draft mode to toggle between static and dynamic pages. You can learn how it works with App Router here.](https://nextjs.org/docs/app/guides/draft-mode)[Environment VariablesLearn to add and access environment variables in your Next.js application.](https://nextjs.org/docs/app/guides/environment-variables)[FormsLearn how to create forms in Next.js with React Server Actions.](https://nextjs.org/docs/app/guides/forms)[ISRLearn how to create or update static pages at runtime with Incremental Static Regeneration.](https://nextjs.org/docs/app/guides/incremental-static-regeneration)[InstrumentationLearn how to use instrumentation to run code at server startup in your Next.js app](https://nextjs.org/docs/app/guides/instrumentation)[InternationalizationAdd support for multiple languages with internationalized routing and localized content.](https://nextjs.org/docs/app/guides/internationalization)[JSON-LDLearn how to add JSON-LD to your Next.js application to describe your content to search engines and AI.](https://nextjs.org/docs/app/guides/json-ld)[Lazy LoadingLazy load imported libraries and React Components to improve your application's loading performance.](https://nextjs.org/docs/app/guides/lazy-loading)[Development EnvironmentLearn how to optimize your local development environment with Next.js.](https://nextjs.org/docs/app/guides/local-development)[Next.js MCP ServerLearn how to use Next.js MCP support to allow coding agents access to your application state](https://nextjs.org/docs/app/guides/mcp)[MDXLearn how to configure MDX and use it in your Next.js apps.](https://nextjs.org/docs/app/guides/mdx)[Memory UsageOptimize memory used by your application in development and production.](https://nextjs.org/docs/app/guides/memory-usage)[MigratingLearn how to migrate from popular frameworks to Next.js](https://nextjs.org/docs/app/guides/migrating)[Multi-tenantLearn how to build multi-tenant apps with the App Router.](https://nextjs.org/docs/app/guides/multi-tenant)[Multi-zonesLearn how to build micro-frontends using Next.js Multi-Zones to deploy multiple Next.js apps under a single domain.](https://nextjs.org/docs/app/guides/multi-zones)[OpenTelemetryLearn how to instrument your Next.js app with OpenTelemetry.](https://nextjs.org/docs/app/guides/open-telemetry)[Package BundlingLearn how to analyze and optimize your application's server and client bundles with the Next.js Bundle Analyzer for Turbopack, and the `@next/bundle-analyzer` plugin for Webpack.](https://nextjs.org/docs/app/guides/package-bundling)[PrefetchingLearn how to configure prefetching in Next.js](https://nextjs.org/docs/app/guides/prefetching)[ProductionRecommendations to ensure the best performance and user experience before taking your Next.js application to production.](https://nextjs.org/docs/app/guides/production-checklist)[PWAsLearn how to build a Progressive Web Application (PWA) with Next.js.](https://nextjs.org/docs/app/guides/progressive-web-apps)[Public pagesLearn how to build public, "static" pages that share data across users, such as landing pages, list pages (products, blogs, etc.), marketing and news sites.](https://nextjs.org/docs/app/guides/public-static-pages)[RedirectingLearn the different ways to handle redirects in Next.js.](https://nextjs.org/docs/app/guides/redirecting)[SassStyle your Next.js application using Sass.](https://nextjs.org/docs/app/guides/sass)[ScriptsOptimize 3rd party scripts with the built-in Script component.](https://nextjs.org/docs/app/guides/scripts)[Self-HostingLearn how to self-host your Next.js application on a Node.js server, Docker image, or static HTML files (static exports).](https://nextjs.org/docs/app/guides/self-hosting)[SPAsNext.js fully supports building Single-Page Applications (SPAs).](https://nextjs.org/docs/app/guides/single-page-applications)[Static ExportsNext.js enables starting as a static site or Single-Page Application (SPA), then later optionally upgrading to use features that require a server.](https://nextjs.org/docs/app/guides/static-exports)[Tailwind CSS v3Style your Next.js Application using Tailwind CSS v3 for broader browser support.](https://nextjs.org/docs/app/guides/tailwind-v3-css)[TestingLearn how to set up Next.js with four commonly used testing tools — Cypress, Playwright, Vitest, and Jest.](https://nextjs.org/docs/app/guides/testing)[Third Party LibrariesOptimize the performance of third-party libraries in your application with the `@next/third-parties` package.](https://nextjs.org/docs/app/guides/third-party-libraries)[UpgradingLearn how to upgrade to the latest versions of Next.js.](https://nextjs.org/docs/app/guides/upgrading)[VideosRecommendations and best practices for optimizing videos in your Next.js application.](https://nextjs.org/docs/app/guides/videos)

Was this helpful?

supported.
