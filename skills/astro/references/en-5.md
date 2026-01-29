# Firebase & Astro and more

# Firebase & Astro

> Add a backend to your project with Firebase

# Firebase & Astro

[Firebase](https://firebase.google.com/) is an app development platform that provides a NoSQL database, authentication, realtime subscriptions, functions, and storage.

See our separate guide for [deploying to Firebase hosting](https://docs.astro.build/en/guides/deploy/firebase/).

## Initializing Firebase in Astro

[Section titled “Initializing Firebase in Astro”](#initializing-firebase-in-astro)

### Prerequisites

[Section titled “Prerequisites”](#prerequisites)

- A [Firebase project with a web app configured](https://firebase.google.com/docs/web/setup).
- An Astro project with [output: 'server'for on-demand rendering](https://docs.astro.build/en/guides/on-demand-rendering/) enabled.
- Firebase credentials: You will need two sets of credentials to connect Astro to Firebase:
  - Web app credentials: These credentials will be used by the client side of your app. You can find them in the Firebase console under *Project settings > General*. Scroll down to the **Your apps** section and click on the **Web app** icon.
  - Project credentials: These credentials will be used by the server side of your app. You can generate them in the Firebase console under *Project settings > Service accounts > Firebase Admin SDK > Generate new private key*.

### Adding Firebase credentials

[Section titled “Adding Firebase credentials”](#adding-firebase-credentials)

To add your Firebase credentials to Astro, create an `.env` file in the root of your project with the following variables:

 .env

```
FIREBASE_PRIVATE_KEY_ID=YOUR_PRIVATE_KEY_IDFIREBASE_PRIVATE_KEY=YOUR_PRIVATE_KEYFIREBASE_PROJECT_ID=YOUR_PROJECT_IDFIREBASE_CLIENT_EMAIL=YOUR_CLIENT_EMAILFIREBASE_CLIENT_ID=YOUR_CLIENT_IDFIREBASE_AUTH_URI=YOUR_AUTH_URIFIREBASE_TOKEN_URI=YOUR_TOKEN_URIFIREBASE_AUTH_CERT_URL=YOUR_AUTH_CERT_URLFIREBASE_CLIENT_CERT_URL=YOUR_CLIENT_CERT_URL
```

Now, these environment variables are available for use in your project.

If you would like to have IntelliSense for your Firebase environment variables, edit or create the file `env.d.ts` in your `src/` directory and configure your types:

 src/env.d.ts

```
interface ImportMetaEnv {  readonly FIREBASE_PRIVATE_KEY_ID: string;  readonly FIREBASE_PRIVATE_KEY: string;  readonly FIREBASE_PROJECT_ID: string;  readonly FIREBASE_CLIENT_EMAIL: string;  readonly FIREBASE_CLIENT_ID: string;  readonly FIREBASE_AUTH_URI: string;  readonly FIREBASE_TOKEN_URI: string;  readonly FIREBASE_AUTH_CERT_URL: string  readonly FIREBASE_CLIENT_CERT_URL: string;}
interface ImportMeta {  readonly env: ImportMetaEnv;}
```

Your project should now include these new files:

- Directorysrc/
  - **env.d.ts**
- **.env**
- astro.config.mjs
- package.json

### Installing dependencies

[Section titled “Installing dependencies”](#installing-dependencies)

To connect Astro with Firebase, install the following packages using the single command below for your preferred package manager:

- `firebase` - the Firebase SDK for the client side
- `firebase-admin` - the Firebase Admin SDK for the server side

- [npm](#tab-panel-2735)
- [pnpm](#tab-panel-2736)
- [Yarn](#tab-panel-2737)

   Terminal window

```
npm install firebase firebase-admin
```

   Terminal window

```
pnpm add firebase firebase-admin
```

   Terminal window

```
yarn add firebase firebase-admin
```

Next, create a folder named `firebase` in the `src/` directory and add two new files to this folder: `client.ts` and `server.ts`.

In `client.ts`, add the following code to initialize Firebase in the client using your web app credentials and the `firebase` package:

 src/firebase/client.ts

```
import { initializeApp } from "firebase/app";
const firebaseConfig = {  apiKey: "my-public-api-key",  authDomain: "my-auth-domain",  projectId: "my-project-id",  storageBucket: "my-storage-bucket",  messagingSenderId: "my-sender-id",  appId: "my-app-id",};
export const app = initializeApp(firebaseConfig);
```

In `server.ts`, add the following code to initialize Firebase in the server using your project credentials and the `firebase-admin` package:

 src/firebase/server.ts

```
import type { ServiceAccount } from "firebase-admin";import { initializeApp, cert, getApps } from "firebase-admin/app";
const activeApps = getApps();const serviceAccount = {  type: "service_account",  project_id: import.meta.env.FIREBASE_PROJECT_ID,  private_key_id: import.meta.env.FIREBASE_PRIVATE_KEY_ID,  private_key: import.meta.env.FIREBASE_PRIVATE_KEY,  client_email: import.meta.env.FIREBASE_CLIENT_EMAIL,  client_id: import.meta.env.FIREBASE_CLIENT_ID,  auth_uri: import.meta.env.FIREBASE_AUTH_URI,  token_uri: import.meta.env.FIREBASE_TOKEN_URI,  auth_provider_x509_cert_url: import.meta.env.FIREBASE_AUTH_CERT_URL,  client_x509_cert_url: import.meta.env.FIREBASE_CLIENT_CERT_URL,};
const initApp = () => {  if (import.meta.env.PROD) {    console.info('PROD env detected. Using default service account.')    // Use default config in firebase functions. Should be already injected in the server by Firebase.    return initializeApp()  }  console.info('Loading service account from env.')  return initializeApp({    credential: cert(serviceAccount as ServiceAccount)  })}
export const app = activeApps.length === 0 ? initApp() : activeApps[0];
```

Finally, your project should now include these new files:

- Directorysrc
  - env.d.ts
  - Directoryfirebase
    - **client.ts**
    - **server.ts**
- .env
- astro.config.mjs
- package.json

## Adding authentication with Firebase

[Section titled “Adding authentication with Firebase”](#adding-authentication-with-firebase)

### Prerequisites

[Section titled “Prerequisites”](#prerequisites-1)

- An Astro project [initialized with Firebase](#initializing-firebase-in-astro).
- A Firebase project with email/password authentication enabled in the Firebase console under *Authentication > Sign-in* method.

### Creating auth server endpoints

[Section titled “Creating auth server endpoints”](#creating-auth-server-endpoints)

Firebase authentication in Astro requires the following three [Astro server endpoints](https://docs.astro.build/en/guides/endpoints/):

- `GET /api/auth/signin` - to sign in a user
- `GET /api/auth/signout` - to sign out a user
- `POST /api/auth/register` - to register a user

Create three endpoints related to authentication in a new directory `src/pages/api/auth/`: `signin.ts`, `signout.ts` and `register.ts`.

`signin.ts` contains the code to sign in a user using Firebase:

 src/pages/api/auth/signin.ts

```
import type { APIRoute } from "astro";import { app } from "../../../firebase/server";import { getAuth } from "firebase-admin/auth";
export const GET: APIRoute = async ({ request, cookies, redirect }) => {  const auth = getAuth(app);
  /* Get token from request headers */  const idToken = request.headers.get("Authorization")?.split("Bearer ")[1];  if (!idToken) {    return new Response(      "No token found",      { status: 401 }    );  }
  /* Verify id token */  try {    await auth.verifyIdToken(idToken);  } catch (error) {    return new Response(      "Invalid token",      { status: 401 }    );  }
  /* Create and set session cookie */  const fiveDays = 60 * 60 * 24 * 5 * 1000;  const sessionCookie = await auth.createSessionCookie(idToken, {    expiresIn: fiveDays,  });
  cookies.set("__session", sessionCookie, {    path: "/",  });
  return redirect("/dashboard");};
```

`signout.ts` contains the code to log out a user by deleting the session cookie:

 src/pages/api/auth/signout.ts

```
import type { APIRoute } from "astro";
export const GET: APIRoute = async ({ redirect, cookies }) => {  cookies.delete("__session", {    path: "/",  });  return redirect("/signin");};
```

`register.ts` contains the code to register a user using Firebase:

 src/pages/api/auth/register.ts

```
import type { APIRoute } from "astro";import { getAuth } from "firebase-admin/auth";import { app } from "../../../firebase/server";
export const POST: APIRoute = async ({ request, redirect }) => {  const auth = getAuth(app);
  /* Get form data */  const formData = await request.formData();  const email = formData.get("email")?.toString();  const password = formData.get("password")?.toString();  const name = formData.get("name")?.toString();
  if (!email || !password || !name) {    return new Response(      "Missing form data",      { status: 400 }    );  }
  /* Create user */  try {    await auth.createUser({      email,      password,      displayName: name,    });  } catch (error: any) {    return new Response(      "Something went wrong",      { status: 400 }    );  }  return redirect("/signin");};
```

After creating server endpoints for authentication, your project directory should now include these new files:

- Directorysrc
  - env.d.ts
  - Directoryfirebase
    - client.ts
    - server.ts
  - Directorypages
    - Directoryapi
      - Directoryauth
        - **signin.ts**
        - **signout.ts**
        - **register.ts**
- .env
- astro.config.mjs
- package.json

### Creating pages

[Section titled “Creating pages”](#creating-pages)

Create the pages that will use the Firebase endpoints:

- `src/pages/register` - will contain a form to register a user
- `src/pages/signin` - will contain a form to sign in a user
- `src/pages/dashboard` - will contain a dashboard that can only be accessed by authenticated users

The example `src/pages/register.astro` below includes a form that will send a `POST` request to the `/api/auth/register` endpoint. This endpoint will create a new user using the data from the form and then will redirect the user to the `/signin` page.

 src/pages/register.astro

```
---import Layout from "../layouts/Layout.astro";---
<Layout title="Register">  <h1>Register</h1>  <p>Already have an account? <a href="/signin">Sign in</a></p>  <form action="/api/auth/register" method="post">    <label for="name">Name</label>    <input type="text" name="name" id="name" />    <label for="email" for="email">Email</label>    <input type="email" name="email" id="email" />    <label for="password">Password</label>    <input type="password" name="password" id="password" />    <button type="submit">Login</button>  </form></Layout>
```

`src/pages/signin.astro` uses the Firebase server app to verify the user’s session cookie. If the user is authenticated, the page will redirect the user to the `/dashboard` page.

The example page below contains a form that will send a `POST` request to the `/api/auth/signin` endpoint with the ID token generated by the Firebase client app.

The endpoint will verify the ID token and create a new session cookie for the user. Then, the endpoint will redirect the user to the `/dashboard` page.

 src/pages/signin.astro

```
---import { app } from "../firebase/server";import { getAuth } from "firebase-admin/auth";import Layout from "../layouts/Layout.astro";
/* Check if the user is authenticated */const auth = getAuth(app);if (Astro.cookies.has("__session")) {  const sessionCookie = Astro.cookies.get("__session")!.value;  const decodedCookie = await auth.verifySessionCookie(sessionCookie);  if (decodedCookie) {    return Astro.redirect("/dashboard");  }}---
<Layout title="Sign in">  <h1>Sign in</h1>  <p>New here? <a href="/register">Create an account</a></p>  <form action="/api/auth/signin" method="post">    <label for="email" for="email">Email</label>    <input type="email" name="email" id="email" />    <label for="password">Password</label>    <input type="password" name="password" id="password" />    <button type="submit">Login</button>  </form></Layout><script>  import {    getAuth,    inMemoryPersistence,    signInWithEmailAndPassword,  } from "firebase/auth";  import { app } from "../firebase/client";
  const auth = getAuth(app);  // This will prevent the browser from storing session data  auth.setPersistence(inMemoryPersistence);
  const form = document.querySelector("form") as HTMLFormElement;  form.addEventListener("submit", async (e) => {    e.preventDefault();    const formData = new FormData(form);    const email = formData.get("email")?.toString();    const password = formData.get("password")?.toString();
    if (!email || !password) {      return;    }    const userCredential = await signInWithEmailAndPassword(      auth,      email,      password    );    const idToken = await userCredential.user.getIdToken();    const response = await fetch("/api/auth/signin", {      method: "GET",      headers: {        Authorization: `Bearer ${idToken}`,      },    });
    if (response.redirected) {      window.location.assign(response.url);    }  });</script>
```

`src/pages/dashboard.astro` will verify the user’s session cookie using the Firebase server app. If the user is not authenticated, the page will redirect the user to the `/signin` page.

The example page below display the user’s name and a button to sign out. Clicking the button will send a `GET` request to the `/api/auth/signout` endpoint.

The endpoint will delete the user’s session cookie and redirect the user to the `/signin` page.

 src/pages/dashboard.astro

```
---import { app } from "../firebase/server";import { getAuth } from "firebase-admin/auth";import Layout from "../layouts/Layout.astro";
const auth = getAuth(app);
/* Check current session */if (!Astro.cookies.has("__session")) {  return Astro.redirect("/signin");}const sessionCookie = Astro.cookies.get("__session")!.value;const decodedCookie = await auth.verifySessionCookie(sessionCookie);const user = await auth.getUser(decodedCookie.uid);
if (!user) {  return Astro.redirect("/signin");}---
<Layout title="dashboard">  <h1>Welcome {user.displayName}</h1>  <p>We are happy to see you here</p>  <form action="/api/auth/signout">    <button type="submit">Sign out</button>  </form></Layout>
```

### Adding OAuth providers

[Section titled “Adding OAuth providers”](#adding-oauth-providers)

To add OAuth providers to your app, you need to enable them in the Firebase console.

In the Firebase console, go to the **Authentication** section and click on the **Sign-in method** tab. Then, click on the **Add a new provider** button and enable the providers you want to use.

The example below uses the **Google** provider.

Edit the `signin.astro` page to add:

- a button to sign in with Google underneath the existing form
- an event listener on the button to handle the sign in process in the existing `<script>`.

 src/pages/signin.astro

```
---import { app } from "../firebase/server";import { getAuth } from "firebase-admin/auth";import Layout from "../layouts/Layout.astro";
/* Check if the user is authenticated */const auth = getAuth(app);if (Astro.cookies.has("__session")) {  const sessionCookie = Astro.cookies.get("__session")!.value;  const decodedCookie = await auth.verifySessionCookie(sessionCookie);  if (decodedCookie) {    return Astro.redirect("/dashboard");  }}---
<Layout title="Sign in">  <h1>Sign in</h1>  <p>New here? <a href="/register">Create an account</a></p>  <form action="/api/auth/signin" method="post">    <label for="email" for="email">Email</label>    <input type="email" name="email" id="email" />    <label for="password">Password</label>    <input type="password" name="password" id="password" />    <button type="submit">Login</button>  </form>  <button id="google">Sign in with Google</button></Layout><script>  import {    getAuth,    inMemoryPersistence,    signInWithEmailAndPassword,    GoogleAuthProvider,    signInWithPopup,  } from "firebase/auth";  import { app } from "../firebase/client";
  const auth = getAuth(app);  auth.setPersistence(inMemoryPersistence);
  const form = document.querySelector("form") as HTMLFormElement;  form.addEventListener("submit", async (e) => {    e.preventDefault();    const formData = new FormData(form);    const email = formData.get("email")?.toString();    const password = formData.get("password")?.toString();
    if (!email || !password) {      return;    }    const userCredential = await signInWithEmailAndPassword(      auth,      email,      password    );    const idToken = await userCredential.user.getIdToken();    const response = await fetch("/api/auth/signin", {      headers: {        Authorization: `Bearer ${idToken}`,      },    });
    if (response.redirected) {      window.location.assign(response.url);    }  });
  const googleSignin = document.querySelector("#google") as HTMLButtonElement;  googleSignin.addEventListener("click", async () => {    const provider = new GoogleAuthProvider();    const userCredential = await signInWithPopup(auth, provider);    const idToken = await userCredential.user.getIdToken();    const res = await fetch("/api/auth/signin", {      headers: {        Authorization: `Bearer ${idToken}`,      },    });
    if (res.redirected) {      window.location.assign(res.url);    }  });</script>
```

When clicked, the Google sign in button will open a popup window to sign in with Google. Once the user signs in, it will send a `POST` request to the `/api/auth/signin` endpoint with the ID token generated by OAuth provider.

The endpoint will verify the ID token and create a new session cookie for the user. Then, the endpoint will redirect the user to the `/dashboard` page.

## Connecting to Firestore database

[Section titled “Connecting to Firestore database”](#connecting-to-firestore-database)

### Prerequisites

[Section titled “Prerequisites”](#prerequisites-2)

- An Astro project initialized with Firebase as described in the [Initializing Firebase in Astro](#initializing-firebase-in-astro) section.
- A Firebase project with a Firestore database. You can follow the [Firebase documentation to create a new project and set up a Firestore database](https://firebase.google.com/docs/firestore/quickstart).

In this recipe, the Firestore collection will be called **friends** and will contain documents with the following fields:

- `id`: autogenerated by Firestore
- `name`: a string field
- `age`: a number field
- `isBestFriend`: a boolean field

### Creating the server endpoints

[Section titled “Creating the server endpoints”](#creating-the-server-endpoints)

Create two new files in a new directory `src/pages/api/friends/`: `index.ts` and `[id].ts`. These will create two server endpoints to interact with the Firestore database in the following ways:

- `POST /api/friends`: to create a new document in the friends collection.
- `POST /api/friends/:id`: to update a document in the friends collection.
- `DELETE /api/friends/:id`: to delete a document in the friends collection.

`index.ts` will contain the code to create a new document in the friends collection:

 src/pages/api/friends/index.ts

```
import type { APIRoute } from "astro";import { app } from "../../../firebase/server";import { getFirestore } from "firebase-admin/firestore";
export const POST: APIRoute = async ({ request, redirect }) => {  const formData = await request.formData();  const name = formData.get("name")?.toString();  const age = formData.get("age")?.toString();  const isBestFriend = formData.get("isBestFriend") === "on";
  if (!name || !age) {    return new Response("Missing required fields", {      status: 400,    });  }  try {    const db = getFirestore(app);    const friendsRef = db.collection("friends");    await friendsRef.add({      name,      age: parseInt(age),      isBestFriend,    });  } catch (error) {    return new Response("Something went wrong", {      status: 500,    });  }  return redirect("/dashboard");};
```

`[id].ts` will contain the code to update and delete a document in the friends collection:

 src/pages/api/friends/[id].ts

```
import type { APIRoute } from "astro";import { app } from "../../../firebase/server";import { getFirestore } from "firebase-admin/firestore";
const db = getFirestore(app);const friendsRef = db.collection("friends");
export const POST: APIRoute = async ({ params, redirect, request }) => {  const formData = await request.formData();  const name = formData.get("name")?.toString();  const age = formData.get("age")?.toString();  const isBestFriend = formData.get("isBestFriend") === "on";
  if (!name || !age) {    return new Response("Missing required fields", {      status: 400,    });  }
  if (!params.id) {    return new Response("Cannot find friend", {      status: 404,    });  }
  try {    await friendsRef.doc(params.id).update({      name,      age: parseInt(age),      isBestFriend,    });  } catch (error) {    return new Response("Something went wrong", {      status: 500,    });  }  return redirect("/dashboard");};
export const DELETE: APIRoute = async ({ params, redirect }) => {  if (!params.id) {    return new Response("Cannot find friend", {      status: 404,    });  }
  try {    await friendsRef.doc(params.id).delete();  } catch (error) {    return new Response("Something went wrong", {      status: 500,    });  }  return redirect("/dashboard");};
```

After creating server endpoints for Firestore, your project directory should now include these new files:

- Directorysrc
  - env.d.ts
  - Directoryfirebase
    - client.ts
    - server.ts
  - Directorypages
    - Directoryapi
      - Directoryfriends
        - **index.ts**
        - **[id].ts**
- .env
- astro.config.mjs
- package.json

### Creating pages

[Section titled “Creating pages”](#creating-pages-1)

Create the pages that will use the Firestore endpoints:

- `src/pages/add.astro` - will contain a form to add a new friend.
- `src/pages/edit/[id].astro` - will contain a form to edit a friend and a button to delete a friend.
- `src/pages/friend/[id].astro` - will contain the details of a friend.
- `src/pages/dashboard.astro` - will display a list of friends.

#### Add a new record

[Section titled “Add a new record”](#add-a-new-record)

The example `src/pages/add.astro` below includes a form that will send a `POST` request to the `/api/friends` endpoint. This endpoint will create a new friend using the data from the form and then will redirect the user to the `/dashboard` page.

 src/pages/add.astro

```
---import Layout from "../layouts/Layout.astro";---
<Layout title="Add a new friend">  <h1>Add a new friend</h1>  <form method="post" action="/api/friends">    <label for="name">Name</label>    <input type="text" id="name" name="name" />    <label for="age">Age</label>    <input type="number" id="age" name="age" />    <label for="isBestFriend">Is best friend?</label>    <input type="checkbox" id="isBestFriend" name="isBestFriend" />    <button type="submit">Add friend</button>  </form></Layout>
```

#### Edit or Delete a record

[Section titled “Edit or Delete a record”](#edit-or-delete-a-record)

`src/pages/edit/[id].astro` will contain a form to edit a friend data and a button to delete a friend. On submit, this page will send a `POST` request to the `/api/friends/:id` endpoint to update a friend data.

If the user clicks the delete button, this page will send a `DELETE` request to the `/api/friends/:id` endpoint to delete a friend.

 src/pages/edit/[id].astro

```
---import Layout from "../../layouts/Layout.astro";import { app } from "../../firebase/server";import { getFirestore } from "firebase-admin/firestore";
interface Friend {  name: string;  age: number;  isBestFriend: boolean;}
const { id } = Astro.params;
if (!id) {  return Astro.redirect("/404");}
const db = getFirestore(app);const friendsRef = db.collection("friends");const friendSnapshot = await friendsRef.doc(id).get();
if (!friendSnapshot.exists) {  return Astro.redirect("/404");}
const friend = friendSnapshot.data() as Friend;---
<Layout title="Edit {friend.name}">  <h1>Edit {friend.name}</h1>  <p>Here you can edit or delete your friend's data.</p>  <form method="post" action={`/api/friends/${id}`}>    <label for="name">Name</label>    <input type="text" id="name" name="name" value={friend.name} />    <label for="age">Age</label>    <input type="number" id="age" name="age" value={friend.age} />    <label for="isBestFriend">Is best friend?</label>    <input      type="checkbox"      id="isBestFriend"      name="isBestFriend"      checked={friend.isBestFriend}    />    <button type="submit">Edit friend</button>  </form>  <button type="button" id="delete-document">Delete</button></Layout><script>  const deleteButton = document.getElementById(    "delete-document"  ) as HTMLButtonElement;  const url = document.querySelector("form")?.getAttribute("action") as string;  deleteButton.addEventListener("click", async () => {    const response = await fetch(url, {      method: "DELETE",    });    if (response.redirected) {      window.location.assign(response.url);    }  });</script>
```

#### Display an individual record

[Section titled “Display an individual record”](#display-an-individual-record)

`src/pages/friend/[id].astro` will display the details of a friend.

 src/pages/friend/[id].astro

```
---import Layout from "../../layouts/Layout.astro";import { app } from "../../firebase/server";import { getFirestore } from "firebase-admin/firestore";
interface Friend {  name: string;  age: number;  isBestFriend: boolean;}
const { id } = Astro.params;
if (!id) {  return Astro.redirect("/404");}
const db = getFirestore(app);const friendsRef = db.collection("friends");const friendSnapshot = await friendsRef.doc(id).get();
if (!friendSnapshot.exists) {  return Astro.redirect("/404");}
const friend = friendSnapshot.data() as Friend;---
<Layout title={friend.name}>  <h1>{friend.name}</h1>  <p>Age: {friend.age}</p>  <p>Is best friend: {friend.isBestFriend ? "Yes" : "No"}</p></Layout>
```

#### Display a list of records with an edit button

[Section titled “Display a list of records with an edit button”](#display-a-list-of-records-with-an-edit-button)

Finally, `src/pages/dashboard.astro` will display a list of friends. Each friend will have a link to their details page and an edit button that will redirect the user to the edit page.

 src/pages/dashboard.astro

```
---import { app } from "../firebase/server";import { getFirestore } from "firebase-admin/firestore";import Layout from "../layouts/Layout.astro";
interface Friend {  id: string;  name: string;  age: number;  isBestFriend: boolean;}
const db = getFirestore(app);const friendsRef = db.collection("friends");const friendsSnapshot = await friendsRef.get();const friends = friendsSnapshot.docs.map((doc) => ({  id: doc.id,  ...doc.data(),})) as Friend[];---
<Layout title="My friends">  <h1>Friends</h1>  <ul>    {      friends.map((friend) => (        <li>          <a href={`/friend/${friend.id}`}>{friend.name}</a>          <span>({friend.age})</span>          <strong>{friend.isBestFriend ? "Bestie" : "Friend"}</strong>          <a href={`/edit/${friend.id}`}>Edit</a>        </li>      ))    }  </ul></Layout>
```

After creating all the pages, you should have the following file structure:

- Directorysrc
  - env.d.ts
  - Directoryfirebase
    - client.ts
    - server.ts
  - Directorypages
    - dashboard.astro
    - add.astro
    - Directoryedit
      - [id].astro
    - Directoryfriend
      - [id].astro
    - Directoryapi
      - Directoryfriends
        - index.ts
        - [id].ts
- .env
- astro.config.mjs
- package.json

## Community Resources

[Section titled “Community Resources”](#community-resources)

- [Astro and Firebase SSR app example](https://github.com/kevinzunigacuellar/astro-firebase)
- [Using Firebase Realtime Database in Astro with Vue: A Step-by-Step Guide](https://www.launchfa.st/blog/vue-astro-firebase-realtime-database)

## More backend service guides

- ![](https://docs.astro.build/logos/appwriteio.svg)
  ### Appwrite
- ![](https://docs.astro.build/logos/firebase.svg)
  ### Firebase
- ![](https://docs.astro.build/logos/neon.svg)
  ### Neon
- ![](https://docs.astro.build/logos/prisma-postgres.svg)
  ### Prisma Postgres
- ![](https://docs.astro.build/logos/sentry.svg)
  ### Sentry
- ![](https://docs.astro.build/logos/supabase.svg)
  ### Supabase
- ![](https://docs.astro.build/logos/turso.svg)
  ### Turso
- ![](https://docs.astro.build/logos/xata.svg)
  ### Xata

   Recipes     [Contribute](https://docs.astro.build/en/contribute/) [Community](https://astro.build/chat) [Sponsor](https://opencollective.com/astrodotbuild)

---

# Neon Postgres & Astro

> Add a serverless Postgres database to your Astro project with Neon

# Neon Postgres & Astro

[Neon](https://neon.tech) is a fully managed serverless Postgres database. It separates storage and compute to offer autoscaling, branching, and bottomless storage.

## Adding Neon to your Astro project

[Section titled “Adding Neon to your Astro project”](#adding-neon-to-your-astro-project)

### Prerequisites

[Section titled “Prerequisites”](#prerequisites)

- A [Neon](https://console.neon.tech/signup) account with a created project
- Neon database connection string
- An Astro project with [on-demand rendering (SSR)](https://docs.astro.build/en/guides/on-demand-rendering/) enabled

### Environment configuration

[Section titled “Environment configuration”](#environment-configuration)

To use Neon with Astro, you will need to set a Neon environment variable. Create or edit the `.env` file in your project root, and add the following code, replacing your own project details:

 .env

```
NEON_DATABASE_URL="postgresql://<user>:<password>@<endpoint_hostname>.neon.tech:<port>/<dbname>?sslmode=require"
```

For better TypeScript support, define environment variables in a `src/env.d.ts` file:

 src/env.d.ts

```
interface ImportMetaEnv {  readonly NEON_DATABASE_URL: string;}
interface ImportMeta {  readonly env: ImportMetaEnv;}
```

   Learn more about [environment variables](https://docs.astro.build/en/guides/environment-variables/) and `.env` files in Astro.

### Installing dependencies

[Section titled “Installing dependencies”](#installing-dependencies)

Install the `@neondatabase/serverless` package to connect to Neon:

 Terminal window

```
npm install @neondatabase/serverless
```

### Creating a Neon client

[Section titled “Creating a Neon client”](#creating-a-neon-client)

Create a new file `src/lib/neon.ts` with the following code to initialize your Neon client:

 src/lib/neon.ts

```
import { neon } from '@neondatabase/serverless';
export const sql = neon(import.meta.env.NEON_DATABASE_URL);
```

## Querying your Neon database

[Section titled “Querying your Neon database”](#querying-your-neon-database)

You can now use the Neon client to query your database from any `.astro` component. The following example fetches the current time from the Postgres database:

 src/pages/index.astro

```
---import { sql } from '../lib/neon';
const response =  await  sql`SELECT NOW() as current_time`;const currentTime = response[0].current_time;---
<h1>Current Time</h1><p>The time is: {currentTime}</p>
```

## Database branching with Neon

[Section titled “Database branching with Neon”](#database-branching-with-neon)

Neon’s branching feature lets you create copies of your database for development or testing. Use this in your Astro project by creating different environment variables for each branch:

 .env.development

```
NEON_DATABASE_URL=your_development_branch_url
```

 .env.production

```
NEON_DATABASE_URL=your_production_branch_url
```

## Resources

[Section titled “Resources”](#resources)

- [Neon documentation](https://neon.tech/docs/introduction)
- [Neon serverless driver GitHub](https://github.com/neondatabase/serverless)
- [Connect an Astro site or application to Neon Postgres](https://neon.tech/docs/guides/astro)

## More backend service guides

- ![](https://docs.astro.build/logos/appwriteio.svg)
  ### Appwrite
- ![](https://docs.astro.build/logos/firebase.svg)
  ### Firebase
- ![](https://docs.astro.build/logos/neon.svg)
  ### Neon
- ![](https://docs.astro.build/logos/prisma-postgres.svg)
  ### Prisma Postgres
- ![](https://docs.astro.build/logos/sentry.svg)
  ### Sentry
- ![](https://docs.astro.build/logos/supabase.svg)
  ### Supabase
- ![](https://docs.astro.build/logos/turso.svg)
  ### Turso
- ![](https://docs.astro.build/logos/xata.svg)
  ### Xata

   Recipes     [Contribute](https://docs.astro.build/en/contribute/) [Community](https://astro.build/chat) [Sponsor](https://opencollective.com/astrodotbuild)

---

# Prisma Postgres & Astro

> Add a serverless Postgres database to your Astro project with Prisma Postgres

# Prisma Postgres & Astro

[Prisma Postgres](https://www.prisma.io/) is a fully managed, serverless Postgres database built for modern web apps.

## Connect with Prisma ORM (Recommended)

[Section titled “Connect with Prisma ORM (Recommended)”](#connect-with-prisma-orm-recommended)

[Prisma ORM](https://www.prisma.io/orm) is the recommended way to connect to your Prisma Postgres database. It provides type-safe queries, migrations, and global performance.

### Prerequisites

[Section titled “Prerequisites”](#prerequisites)

- An Astro project with an adapter installed to enable [on-demand rendering (SSR)](https://docs.astro.build/en/guides/on-demand-rendering/).

### Install dependencies and initialize Prisma

[Section titled “Install dependencies and initialize Prisma”](#install-dependencies-and-initialize-prisma)

Run the following commands to install the necessary Prisma dependencies:

 Terminal window

```
npm install prisma tsx --save-devnpm install @prisma/adapter-pg @prisma/client
```

Once installed, initialize Prisma in your project with the following command:

 Terminal window

```
npx prisma init --db --output ./generated
```

You’ll need to answer a few questions while setting up your Prisma Postgres database. Select the region closest to your location and a memorable name for your database, like “My Astro Project.”

This will create:

- A `prisma/` directory with a `schema.prisma` file
- A `.env` file with a `DATABASE_URL` already set

### Define a Model

[Section titled “Define a Model”](#define-a-model)

Even if you don’t need any specific data models yet, Prisma requires at least one model in the schema in order to generate a client and apply migrations.

The following example defines a `Post` model as a placeholder. Add the model to your schema to get started. You can safely delete or replace it later with models that reflect your actual data.

 prisma/schema.prisma

```
generator client {  provider = "prisma-client"  output   = "./generated"}
datasource db {  provider = "postgresql"  url      = env("DATABASE_URL")}
model Post {  id        Int     @id @default(autoincrement())  title     String  content   String?  published Boolean @default(false)}
```

Learn more about configuring your Prisma ORM setup in the [Prisma schema reference](https://www.prisma.io/docs/concepts/components/prisma-schema).

### Generate client

[Section titled “Generate client”](#generate-client)

Run the following command to generate the Prisma Client from your schema:

 Terminal window

```
npx prisma generate
```

### Generate migration files

[Section titled “Generate migration files”](#generate-migration-files)

Run the following command to create the database tables and generate the Prisma Client from your schema. This will also create a `prisma/migrations/` directory with migration history files.

 Terminal window

```
npx prisma migrate dev --name init
```

### Create a Prisma Client

[Section titled “Create a Prisma Client”](#create-a-prisma-client)

Inside of `/src/lib`, create a `prisma.ts` file. This file will initialize and export your Prisma Client instance so you can query your database throughout your Astro project.

 src/lib/prisma.ts

```
import { PrismaPg } from '@prisma/adapter-pg';import { PrismaClient } from '../../prisma/generated/client';
const connectionString = import.meta.env.DATABASE_URL;const adapter = new PrismaPg({ connectionString });const prisma = new PrismaClient({ adapter });
export default prisma;
```

### Querying and displaying data

[Section titled “Querying and displaying data”](#querying-and-displaying-data)

The following example shows fetching only your published posts with the Prisma Client sorted by `id`, and then displaying titles and post content in your Astro template:

 src/pages/posts.astro

```
---import prisma from '../lib/prisma';
const posts = await prisma.post.findMany({  where: { published: true },  orderBy: { id: 'desc' }});---
<html>  <head>    <title>Published Posts</title>  </head>  <body>    <h1>Published Posts</h1>    <ul>      {posts.map((post) => (        <li>          <h2>{post.title}</h2>          {post.content && <p>{post.content}</p>}        </li>      ))}    </ul>  </body></html>
```

It is best practice to handle queries in an API route. For more information on how to use Prisma ORM in your Astro project, see the [Astro + Prisma ORM Guide](https://www.prisma.io/docs/guides/astro).

## Connect with Other ORMs and Libraries

[Section titled “Connect with Other ORMs and Libraries”](#connect-with-other-orms-and-libraries)

You can connect to Prisma Postgres via direct TCP using any other ORM, database library, or tool of your choice. Create a direct connection string in your Prisma Console to get started.

### Prerequisites

[Section titled “Prerequisites”](#prerequisites-1)

- An Astro project with an adapter installed to enable [on-demand rendering (SSR)](https://docs.astro.build/en/guides/on-demand-rendering/).
- A [Prisma Postgres](https://pris.ly/ppg) database with a TCP enabled connection string

### Install dependencies

[Section titled “Install dependencies”](#install-dependencies)

This example uses [pg, a PostgreSQL client for Node.js](https://github.com/brianc/node-postgres) to make a direct TCP connection.

Run the following command to install  the `pg` package:

 Terminal window

```
npm install pg
```

### Query your database client

[Section titled “Query your database client”](#query-your-database-client)

Provide your connection string to the `pg` client to communicate with your SQL server and fetch data from your database.

The following example of creating a table and inserting data can be used to validate your query URL and TCP connection:

 src/pages/index.astro

```
---import { Client } from 'pg';const client = new Client({  connectionString: import.meta.env.DATABASE_URL,  ssl: { rejectUnauthorized: false }});await client.connect();
await client.query(`  CREATE TABLE IF NOT EXISTS posts (    id SERIAL PRIMARY KEY,    title TEXT UNIQUE,    content TEXT  );
  INSERT INTO posts (title, content)  VALUES ('Hello', 'World')  ON CONFLICT (title) DO NOTHING;`);
const { rows } = await client.query('SELECT * FROM posts');await client.end();---
<h1>Posts</h1><p>{rows[0].title}: {rows[0].content}</p>
```

## Official Resources

[Section titled “Official Resources”](#official-resources)

- [Astro + Prisma ORM Guide](https://www.prisma.io/docs/guides/astro)

## More backend service guides

- ![](https://docs.astro.build/logos/appwriteio.svg)
  ### Appwrite
- ![](https://docs.astro.build/logos/firebase.svg)
  ### Firebase
- ![](https://docs.astro.build/logos/neon.svg)
  ### Neon
- ![](https://docs.astro.build/logos/prisma-postgres.svg)
  ### Prisma Postgres
- ![](https://docs.astro.build/logos/sentry.svg)
  ### Sentry
- ![](https://docs.astro.build/logos/supabase.svg)
  ### Supabase
- ![](https://docs.astro.build/logos/turso.svg)
  ### Turso
- ![](https://docs.astro.build/logos/xata.svg)
  ### Xata

   Recipes     [Contribute](https://docs.astro.build/en/contribute/) [Community](https://astro.build/chat) [Sponsor](https://opencollective.com/astrodotbuild)

---

# Monitor your Astro Site with Sentry

> How to monitor your Astro site with Sentry

# Monitor your Astro Site with Sentry

[Sentry](https://sentry.io) offers a comprehensive application monitoring and error tracking service designed to help developers identify, diagnose, and resolve issues in real-time.

Read more on our blog about [Astro’s partnership with Sentry](https://astro.build/blog/sentry-official-monitoring-partner/) and Sentry’s Spotlight dev toolbar app that brings a rich debug overlay into your Astro development environment. Spotlight shows errors, traces, and important context right in your browser during local development.

Sentry’s Astro SDK enables automatic reporting of errors and tracing data in your Astro application.

## Project Configuration

[Section titled “Project Configuration”](#project-configuration)

A full list of prerequisites can be found in [the Sentry guide for Astro](https://docs.sentry.io/platforms/javascript/guides/astro/#prerequisites).

## Install

[Section titled “Install”](#install)

Sentry captures data by using an SDK within your application’s runtime.

Install the SDK by running the following command for the package manager of your choice in the Astro CLI:

- [npm](#tab-panel-2738)
- [pnpm](#tab-panel-2739)
- [Yarn](#tab-panel-2740)

   Terminal window

```
npx astro add @sentry/astro
```

   Terminal window

```
pnpm astro add @sentry/astro
```

   Terminal window

```
yarn astro add @sentry/astro
```

The astro CLI installs the SDK package and adds the Sentry integration to your `astro.config.mjs` file.

## Configure

[Section titled “Configure”](#configure)

To configure the Sentry integration, you need to provide the following credentials in your `astro.config.mjs` file.

1. **Client key (DSN)** - You can find the DSN in your Sentry project settings under *Client keys (DSN)*.
2. **Project name** - You can find the project name in your Sentry project settings under *General settings*.
3. **Auth token** - You can create an auth token in your Sentry organization settings under *Auth tokens*.

  astro.config.mjs

```
import { defineConfig } from 'astro/config';import sentry from '@sentry/astro';
export default defineConfig({  integrations: [    sentry({      dsn: 'https://examplePublicKey@o0.ingest.sentry.io/0',      sourceMapsUploadOptions: {        project: 'example-project',        authToken: process.env.SENTRY_AUTH_TOKEN,      },    }),  ],});
```

Once you’ve configured your `sourceMapsUploadOptions` and added your `dsn`, the SDK will automatically capture and send errors and performance events to Sentry.

## Test your setup

[Section titled “Test your setup”](#test-your-setup)

Add the following `<button>` element to one of your `.astro` pages. This will allow you to manually trigger an error so you can test the error reporting process.

 src/pages/index.astro

```
<button onclick="throw new Error('This is a test error')">Throw test error</button>
```

To view and resolve the recorded error, log into [sentry.io](https://sentry.io/) and open your project.

## More backend service guides

- ![](https://docs.astro.build/logos/appwriteio.svg)
  ### Appwrite
- ![](https://docs.astro.build/logos/firebase.svg)
  ### Firebase
- ![](https://docs.astro.build/logos/neon.svg)
  ### Neon
- ![](https://docs.astro.build/logos/prisma-postgres.svg)
  ### Prisma Postgres
- ![](https://docs.astro.build/logos/sentry.svg)
  ### Sentry
- ![](https://docs.astro.build/logos/supabase.svg)
  ### Supabase
- ![](https://docs.astro.build/logos/turso.svg)
  ### Turso
- ![](https://docs.astro.build/logos/xata.svg)
  ### Xata

   Recipes     [Contribute](https://docs.astro.build/en/contribute/) [Community](https://astro.build/chat) [Sponsor](https://opencollective.com/astrodotbuild)
