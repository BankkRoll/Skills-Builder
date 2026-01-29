# Critical Security Vulnerability in React Server Components and more

# Critical Security Vulnerability in React Server Components

[Blog](https://react.dev/blog)

# Critical Security Vulnerability in React Server Components

December 3, 2025 by [The React Team](https://react.dev/community/team)

---

There is an unauthenticated remote code execution vulnerability in React Server Components.

We recommend upgrading immediately.

---

On November 29th, Lachlan Davidson reported a security vulnerability in React that allows unauthenticated remote code execution by exploiting a flaw in how React decodes payloads sent to React Server Function endpoints.

Even if your app does not implement any React Server Function endpoints it may still be vulnerable if your app supports React Server Components.

This vulnerability was disclosed as [CVE-2025-55182](https://www.cve.org/CVERecord?id=CVE-2025-55182) and is rated CVSS 10.0.

The vulnerability is present in versions 19.0, 19.1.0, 19.1.1, and 19.2.0 of:

- [react-server-dom-webpack](https://www.npmjs.com/package/react-server-dom-webpack)
- [react-server-dom-parcel](https://www.npmjs.com/package/react-server-dom-parcel)
- [react-server-dom-turbopack](https://www.npmjs.com/package/react-server-dom-turbopack?activeTab=readme)

## Immediate Action Required

A fix was introduced in versions [19.0.1](https://github.com/facebook/react/releases/tag/v19.0.1), [19.1.2](https://github.com/facebook/react/releases/tag/v19.1.2), and [19.2.1](https://github.com/facebook/react/releases/tag/v19.2.1). If you are using any of the above packages please upgrade to any of the fixed versions immediately.

If your app’s React code does not use a server, your app is not affected by this vulnerability. If your app does not use a framework, bundler, or bundler plugin that supports React Server Components, your app is not affected by this vulnerability.

### Affected frameworks and bundlers

Some React frameworks and bundlers depended on, had peer dependencies for, or included the vulnerable React packages. The following React frameworks & bundlers are affected: [next](https://www.npmjs.com/package/next), [react-router](https://www.npmjs.com/package/react-router), [waku](https://www.npmjs.com/package/waku), [@parcel/rsc](https://www.npmjs.com/package/@parcel/rsc), [@vitejs/plugin-rsc](https://www.npmjs.com/package/@vitejs/plugin-rsc), and [rwsdk](https://www.npmjs.com/package/rwsdk).

See the [update instructions below](#update-instructions) for how to upgrade to these patches.

### Hosting Provider Mitigations

We have worked with a number of hosting providers to apply temporary mitigations.

You should not depend on these to secure your app, and still update immediately.

### Vulnerability overview

[React Server Functions](https://react.dev/reference/rsc/server-functions) allow a client to call a function on a server. React provides integration points and tools that frameworks and bundlers use to help React code run on both the client and the server. React translates requests on the client into HTTP requests which are forwarded to a server. On the server, React translates the HTTP request into a function call and returns the needed data to the client.

An unauthenticated attacker could craft a malicious HTTP request to any Server Function endpoint that, when deserialized by React, achieves remote code execution on the server. Further details of the vulnerability will be provided after the rollout of the fix is complete.

## Update Instructions

### Note

These instructions have been updated to include the new vulnerabilities:

- **Denial of Service - High Severity**: [CVE-2025-55184](https://www.cve.org/CVERecord?id=CVE-2025-55184) and [CVE-2025-67779](https://www.cve.org/CVERecord?id=CVE-2025-67779) (CVSS 7.5)
- **Source Code Exposure - Medium Severity**: [CVE-2025-55183](https://www.cve.org/CVERecord?id=CVE-2025-55183) (CVSS 5.3)
- **Denial of Service - High Severity**: January 26, 2026 [CVE-2026-23864](https://www.cve.org/CVERecord?id=CVE-2026-23864) (CVSS 7.5)

See the [follow-up blog post](https://react.dev/blog/2025/12/11/denial-of-service-and-source-code-exposure-in-react-server-components) for more info.

---

*Updated January 26, 2026.*

### Next.js

All users should upgrade to the latest patched version in their release line:

 $

```
npm install next@14.2.35  // for 13.3.x, 13.4.x, 13.5.x, 14.xnpm install next@15.0.8   // for 15.0.xnpm install next@15.1.12  // for 15.1.xnpm install next@15.2.9   // for 15.2.xnpm install next@15.3.9   // for 15.3.xnpm install next@15.4.11  // for 15.4.xnpm install next@15.5.10  // for 15.5.xnpm install next@16.0.11  // for 16.0.xnpm install next@16.1.5   // for 16.1.xnpm install next@15.6.0-canary.60   // for 15.x canary releasesnpm install next@16.1.0-canary.19   // for 16.x canary releases
```

/$

15.0.8, 15.1.12, 15.2.9, 15.3.9, 15.4.10, 15.5.10, 15.6.0-canary.61, 16.0.11, 16.1.5

If you are on version `13.3` or later version of Next.js 13 (`13.3.x`, `13.4.x`, or `13.5.x`) please upgrade to version `14.2.35`.

If you are on `next@14.3.0-canary.77` or a later canary release, downgrade to the latest stable 14.x release:

 $

```
npm install next@14
```

/$

See the [Next.js blog](https://nextjs.org/blog/security-update-2025-12-11) for the latest update instructions and the [previous changelog](https://nextjs.org/blog/CVE-2025-66478) for more info.

### React Router

If you are using React Router’s unstable RSC APIs, you should upgrade the following package.json dependencies if they exist:

 $

```
npm install react@latestnpm install react-dom@latestnpm install react-server-dom-parcel@latestnpm install react-server-dom-webpack@latestnpm install @vitejs/plugin-rsc@latest
```

/$

### Expo

To learn more about mitigating, read the article on [expo.dev/changelog](https://expo.dev/changelog/mitigating-critical-security-vulnerability-in-react-server-components).

### Redwood SDK

Ensure you are on rwsdk>=1.0.0-alpha.0

For the latest beta version:

 $

```
npm install rwsdk@latest
```

/$

Upgrade to the latest `react-server-dom-webpack`:

 $

```
npm install react@latest react-dom@latest react-server-dom-webpack@latest
```

/$

See [Redwood docs](https://docs.rwsdk.com/migrating/) for more migration instructions.

### Waku

Upgrade to the latest `react-server-dom-webpack`:

 $

```
npm install react@latest react-dom@latest react-server-dom-webpack@latest waku@latest
```

/$

See [Waku announcement](https://github.com/wakujs/waku/discussions/1823) for more migration instructions.

### @vitejs/plugin-rsc

Upgrade to the latest RSC plugin:

 $

```
npm install react@latest react-dom@latest @vitejs/plugin-rsc@latest
```

/$

### react-server-dom-parcel

Update to the latest version:

 $

```
npm install react@latest react-dom@latest react-server-dom-parcel@latest
```

/$

### react-server-dom-turbopack

Update to the latest version:

 $

```
npm install react@latest react-dom@latest react-server-dom-turbopack@latest
```

/$

### react-server-dom-webpack

Update to the latest version:

 $

```
npm install react@latest react-dom@latest react-server-dom-webpack@latest
```

/$

### React Native

For React Native users not using a monorepo or `react-dom`, your `react` version should be pinned in your `package.json`, and there are no additional steps needed.

If you are using React Native in a monorepo, you should update *only* the impacted packages if they are installed:

- `react-server-dom-webpack`
- `react-server-dom-parcel`
- `react-server-dom-turbopack`

This is required to mitigate the security advisory, but you do not need to update `react` and `react-dom` so this will not cause the version mismatch error in React Native.

See [this issue](https://github.com/facebook/react-native/issues/54772#issuecomment-3617929832) for more information.

## Timeline

- **November 29th**: Lachlan Davidson reported the security vulnerability via [Meta Bug Bounty](https://bugbounty.meta.com/).
- **November 30th**: Meta security researchers confirmed and began working with the React team on a fix.
- **December 1st**: A fix was created and the React team began working with affected hosting providers and open source projects to validate the fix, implement mitigations and roll out the fix
- **December 3rd**: The fix was published to npm and the publicly disclosed as CVE-2025-55182.

## Attribution

Thank you to [Lachlan Davidson](https://github.com/lachlan2k) for discovering, reporting, and working to help fix this vulnerability.

[PreviousDenial of Service and Source Code Exposure in React Server Components](https://react.dev/blog/2025/12/11/denial-of-service-and-source-code-exposure-in-react-server-components)[NextReact Conf 2025 Recap](https://react.dev/blog/2025/10/16/react-conf-2025-recap)

---

# Denial of Service and Source Code Exposure in React Server Components

[Blog](https://react.dev/blog)

# Denial of Service and Source Code Exposure in React Server Components

December 11, 2025 by [The React Team](https://react.dev/community/team)

*Updated January 26, 2026.*

---

Security researchers have found and disclosed two additional vulnerabilities in React Server Components while attempting to exploit the patches in last week’s critical vulnerability.

**These new vulnerabilities do not allow for Remote Code Execution.** The patch for React2Shell remains effective at mitigating the Remote Code Execution exploit.

---

The new vulnerabilities are disclosed as:

- **Denial of Service - High Severity**: [CVE-2025-55184](https://www.cve.org/CVERecord?id=CVE-2025-55184), [CVE-2025-67779](https://www.cve.org/CVERecord?id=CVE-2025-67779), and [CVE-2026-23864](https://www.cve.org/CVERecord?id=CVE-2026-23864) (CVSS 7.5)
- **Source Code Exposure - Medium Severity**: [CVE-2025-55183](https://www.cve.org/CVERecord?id=CVE-2025-55183) (CVSS 5.3)

We recommend upgrading immediately due to the severity of the newly disclosed vulnerabilities.

### Note

#### The patches published earlier are vulnerable.

If you already updated for the previous vulnerabilities, you will need to update again.

If you updated to 19.0.3, 19.1.4, and 19.2.3, [these are incomplete](#additional-fix-published), and you will need to update again.

Please see [the instructions in the previous post](https://react.dev/blog/2025/12/03/critical-security-vulnerability-in-react-server-components#update-instructions) for upgrade steps.

---

*Updated January 26, 2026.*

Further details of these vulnerabilities will be provided after the rollout of the fixes are complete.

## Immediate Action Required

These vulnerabilities are present in the same packages and versions as [CVE-2025-55182](https://react.dev/blog/2025/12/03/critical-security-vulnerability-in-react-server-components).

This includes 19.0.0, 19.0.1, 19.0.2, 19.0.3, 19.1.0, 19.1.1, 19.1.2, 19.1.3, 19.2.0, 19.2.1, 19.2.2, and 19.2.3 of:

- [react-server-dom-webpack](https://www.npmjs.com/package/react-server-dom-webpack)
- [react-server-dom-parcel](https://www.npmjs.com/package/react-server-dom-parcel)
- [react-server-dom-turbopack](https://www.npmjs.com/package/react-server-dom-turbopack?activeTab=readme)

Fixes were backported to versions 19.0.4, 19.1.5, and 19.2.4. If you are using any of the above packages please upgrade to any of the fixed versions immediately.

As before, if your app’s React code does not use a server, your app is not affected by these vulnerabilities. If your app does not use a framework, bundler, or bundler plugin that supports React Server Components, your app is not affected by these vulnerabilities.

### Note

#### It’s common for critical CVEs to uncover follow‑up vulnerabilities.

When a critical vulnerability is disclosed, researchers scrutinize adjacent code paths looking for variant exploit techniques to test whether the initial mitigation can be bypassed.

This pattern shows up across the industry, not just in JavaScript. For example, after [Log4Shell](https://nvd.nist.gov/vuln/detail/cve-2021-44228), additional CVEs ([1](https://nvd.nist.gov/vuln/detail/cve-2021-45046), [2](https://nvd.nist.gov/vuln/detail/cve-2021-45105)) were reported as the community probed the original fix.

Additional disclosures can be frustrating, but they are generally a sign of a healthy response cycle.

### Affected frameworks and bundlers

Some React frameworks and bundlers depended on, had peer dependencies for, or included the vulnerable React packages. The following React frameworks & bundlers are affected: [next](https://www.npmjs.com/package/next), [react-router](https://www.npmjs.com/package/react-router), [waku](https://www.npmjs.com/package/waku), [@parcel/rsc](https://www.npmjs.com/package/@parcel/rsc), [@vite/rsc-plugin](https://www.npmjs.com/package/@vitejs/plugin-rsc), and [rwsdk](https://www.npmjs.com/package/rwsdk).

Please see [the instructions in the previous post](https://react.dev/blog/2025/12/03/critical-security-vulnerability-in-react-server-components#update-instructions) for upgrade steps.

### Hosting Provider Mitigations

As before, we have worked with a number of hosting providers to apply temporary mitigations.

You should not depend on these to secure your app, and still update immediately.

### React Native

For React Native users not using a monorepo or `react-dom`, your `react` version should be pinned in your `package.json`, and there are no additional steps needed.

If you are using React Native in a monorepo, you should update *only* the impacted packages if they are installed:

- `react-server-dom-webpack`
- `react-server-dom-parcel`
- `react-server-dom-turbopack`

This is required to mitigate the security advisories, but you do not need to update `react` and `react-dom` so this will not cause the version mismatch error in React Native.

See [this issue](https://github.com/facebook/react-native/issues/54772#issuecomment-3617929832) for more information.

---

## High Severity: Multiple Denial of Service

**CVEs:** [CVE-2026-23864](https://www.cve.org/CVERecord?id=CVE-2026-23864) **Base Score:** 7.5 (High)
**Date**: January 26, 2025

Security researchers discovered additional DoS vulnerabilities still exist in React Server Components.

The vulnerabilities are triggered by sending specially crafted HTTP requests to Server Function endpoints, and could lead to server crashes, out-of-memory exceptions or excessive CPU usage; depending on the vulnerable code path being exercised, the application configuration and application code.

The patches published January 26th mitigate these DoS vulnerabilities.

### Note

#### Additional fixes published

The original fix addressing the DoS in [CVE-2025-55184](https://www.cve.org/CVERecord?id=CVE-2025-55184) was incomplete.

This left previous versions vulnerable. Versions 19.0.4, 19.1.5, 19.2.4 are safe.

---

*Updated January 26, 2026.*

---

## High Severity: Denial of Service

**CVEs:** [CVE-2025-55184](https://www.cve.org/CVERecord?id=CVE-2025-55184) and [CVE-2025-67779](https://www.cve.org/CVERecord?id=CVE-2025-67779) **Base Score:** 7.5 (High)

Security researchers have discovered that a malicious HTTP request can be crafted and sent to any Server Functions endpoint that, when deserialized by React, can cause an infinite loop that hangs the server process and consumes CPU. Even if your app does not implement any React Server Function endpoints it may still be vulnerable if your app supports React Server Components.

This creates a vulnerability vector where an attacker may be able to deny users from accessing the product, and potentially have a  performance impact on the server environment.

The patches published today mitigate by preventing the infinite loop.

## Medium Severity: Source Code Exposure

**CVE:** [CVE-2025-55183](https://www.cve.org/CVERecord?id=CVE-2025-55183) **Base Score**: 5.3 (Medium)

A security researcher has discovered that a malicious HTTP request sent to a vulnerable Server Function may unsafely return the source code of any Server Function. Exploitation requires the existence of a Server Function which explicitly or implicitly exposes a stringified argument:

 $

```
'use server';export async function serverFunction(name) {  const conn = db.createConnection('SECRET KEY');  const user = await conn.createUser(name); // implicitly stringified, leaked in db  return {   id: user.id,   message: `Hello, ${name}!` // explicitly stringified, leaked in reply  }}
```

/$

An attacker may be able to leak the following:

 $

```
0:{"a":"$@1","f":"","b":"Wy43RxUKdxmr5iuBzJ1pN"}1:{"id":"tva1sfodwq","message":"Hello, async function(a){console.log(\"serverFunction\");let b=i.createConnection(\"SECRET KEY\");return{id:(await b.createUser(a)).id,message:`Hello, ${a}!`}}!"}
```

/$

The patches published today prevent stringifying the Server Function source code.

### Note

#### Only secrets in source code may be exposed.

Secrets hardcoded in source code may be exposed, but runtime secrets such as `process.env.SECRET` are not affected.

The scope of the exposed code is limited to the code inside the Server Function, which may include other functions depending on the amount of inlining your bundler provides.

Always verify against production bundles.

---

## Timeline

- **December 3rd**: Leak reported to Vercel and [Meta Bug Bounty](https://bugbounty.meta.com/) by [Andrew MacPherson](https://github.com/AndrewMohawk).
- **December 4th**: Initial DoS reported to [Meta Bug Bounty](https://bugbounty.meta.com/) by [RyotaK](https://ryotak.net).
- **December 6th**: Both issues confirmed by the React team, and the team began investigating.
- **December 7th**: Initial fixes created and the React team began verifying and planning new patch.
- **December 8th**: Affected hosting providers and open source projects notified.
- **December 10th**: Hosting provider mitigations in place and patches verified.
- **December 11th**: Additional DoS reported to [Meta Bug Bounty](https://bugbounty.meta.com/) by Shinsaku Nomura.
- **December 11th**: Patches published and publicly disclosed as [CVE-2025-55183](https://www.cve.org/CVERecord?id=CVE-2025-55183) and [CVE-2025-55184](https://www.cve.org/CVERecord?id=CVE-2025-55184).
- **December 11th**: Missing DoS case found internally, patched and publicly disclosed as [CVE-2025-67779](https://www.cve.org/CVERecord?id=CVE-2025-67779).
- **January 26th**: Additional DoS cases found, patched, and publicly disclosed as [CVE-2026-23864](https://www.cve.org/CVERecord?id=CVE-2026-23864).

---

## Attribution

Thank you to [Andrew MacPherson (AndrewMohawk)](https://github.com/AndrewMohawk) for reporting the Source Code Exposure, [RyotaK](https://ryotak.net) from GMO Flatt Security Inc and Shinsaku Nomura of Bitforest Co., Ltd. for reporting the Denial of Service vulnerabilities. Thank you to [Mufeed VH](https://x.com/mufeedvh) from [Winfunc Research](https://winfunc.com), [Joachim Viide](https://jviide.iki.fi), [RyotaK](https://ryotak.net) from [GMO Flatt Security Inc](https://flatt.tech/en/) and Xiangwei Zhang of Tencent Security YUNDING LAB for reporting the additional DoS vulnerabilities.

[PreviousBlog](https://react.dev/blog)[NextCritical Security Vulnerability in React Server Components](https://react.dev/blog/2025/12/03/critical-security-vulnerability-in-react-server-components)

---

# Not Found

[Learn React](https://react.dev/learn)

# Not Found

This page doesn’t exist.

If this is a mistake , [let us know](https://github.com/reactjs/react.dev/issues/new),  and we will try to fix it!
