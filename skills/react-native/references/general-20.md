# Security and more

# Security

> Security is often overlooked when building apps. It is true that it is impossible to build software that is completely impenetrable—we’ve yet to invent a completely impenetrable lock (bank vaults do, after all, still get broken into). However, the probability of falling victim to a malicious attack or being exposed for a security vulnerability is inversely proportional to the effort you’re willing to put in to protecting your application against any such eventuality. Although an ordinary padlock is pickable, it is still much harder to get past than a cabinet hook!

Security is often overlooked when building apps. It is true that it is impossible to build software that is completely impenetrable—we’ve yet to invent a completely impenetrable lock (bank vaults do, after all, still get broken into). However, the probability of falling victim to a malicious attack or being exposed for a security vulnerability is inversely proportional to the effort you’re willing to put in to protecting your application against any such eventuality. Although an ordinary padlock is pickable, it is still much harder to get past than a cabinet hook!

 ![ ](https://reactnative.dev/docs/assets/d_security_chart.svg)

In this guide, you will learn about best practices for storing sensitive information, authentication, network security, and tools that will help you secure your app. This is not a preflight checklist—it is a catalogue of options, each of which will help further protect your app and users.

## Storing Sensitive Info​

Never store sensitive API keys in your app code. Anything included in your code could be accessed in plain text by anyone inspecting the app bundle. Tools like [react-native-dotenv](https://github.com/goatandsheep/react-native-dotenv) and [react-native-config](https://github.com/luggit/react-native-config/) are great for adding environment-specific variables like API endpoints, but they should not be confused with server-side environment variables, which can often contain secrets and API keys.

If you must have an API key or a secret to access some resource from your app, the most secure way to handle this would be to build an orchestration layer between your app and the resource. This could be a serverless function (e.g. using AWS Lambda or Google Cloud Functions) which can forward the request with the required API key or secret. Secrets in server side code cannot be accessed by the API consumers the same way secrets in your app code can.

**For persisted user data, choose the right type of storage based on its sensitivity.** As your app is used, you’ll often find the need to save data on the device, whether to support your app being used offline, cut down on network requests or save your user’s access token between sessions so they wouldn’t have to re-authenticate each time they use the app.

 info

**Persisted vs unpersisted** — persisted data is written to the device’s disk, which lets the data be read by your app across application launches without having to do another network request to fetch it or asking the user to re-enter it. But this also can make that data more vulnerable to being accessed by attackers. Unpersisted data is never written to disk—so there's no data to access!

### Async Storage​

[Async Storage](https://github.com/react-native-async-storage/async-storage) is a community-maintained module for React Native that provides an asynchronous, unencrypted, key-value store. Async Storage is not shared between apps: every app has its own sandbox environment and has no access to data from other apps.

| Douse async storage when... | Don'tuse async storage for... |
| --- | --- |
| Persisting non-sensitive data across app runs | Token storage |
| Persisting Redux state | Secrets |
| Persisting GraphQL state |  |
| Storing global app-wide variables |  |

#### Developer Notes​

note

Async Storage is the React Native equivalent of Local Storage from the web

### Secure Storage​

React Native does not come bundled with any way of storing sensitive data. However, there are pre-existing solutions for Android and iOS platforms.

#### iOS - Keychain Services​

[Keychain Services](https://developer.apple.com/documentation/security/keychain_services) allows you to securely store small chunks of sensitive info for the user. This is an ideal place to store certificates, tokens, passwords, and any other sensitive information that doesn’t belong in Async Storage.

#### Android - Secure Shared Preferences​

[Shared Preferences](https://developer.android.com/reference/android/content/SharedPreferences) is the Android equivalent for a persistent key-value data store. **Data in Shared Preferences is not encrypted by default**, but [Encrypted Shared Preferences](https://developer.android.com/topic/security/data) wraps the Shared Preferences class for Android, and automatically encrypts keys and values.

#### Android - Keystore​

The [Android Keystore](https://developer.android.com/training/articles/keystore) system lets you store cryptographic keys in a container to make it more difficult to extract from the device.

In order to use iOS Keychain services or Android Secure Shared Preferences, you can either write a bridge yourself or use a library which wraps them for you and provides a unified API at your own risk. Some libraries to consider:

- [expo-secure-store](https://docs.expo.dev/versions/latest/sdk/securestore/)
- [react-native-keychain](https://github.com/oblador/react-native-keychain)

 Caution

**Be mindful of unintentionally storing or exposing sensitive info.** This could happen accidentally, for example saving sensitive form data in redux state and persisting the whole state tree in Async Storage. Or sending user tokens and personal info to an application monitoring service such as Sentry or Crashlytics.

## Authentication and Deep Linking​

 ![ ](https://reactnative.dev/docs/assets/d_security_deep-linking.svg)

Mobile apps have a unique vulnerability that is non-existent in the web: **deep linking**. Deep linking is a way of sending data directly to a native application from an outside source. A deep link looks like `app://` where `app` is your app scheme and anything following the // could be used internally to handle the request.

For example, if you were building an ecommerce app, you could use `app://products/1` to deep link to your app and open the product detail page for a product with id 1. You can think of these kind of like URLs on the web, but with one crucial distinction:

Deep links are not secure and you should never send any sensitive information in them.

The reason deep links are not secure is because there is no centralized method of registering URL schemes. As an application developer, you can use almost any url scheme you choose by [configuring it in Xcode](https://developer.apple.com/documentation/uikit/inter-process_communication/allowing_apps_and_websites_to_link_to_your_content/defining_a_custom_url_scheme_for_your_app) for iOS or [adding an intent on Android](https://developer.android.com/training/app-links/deep-linking).

There is nothing stopping a malicious application from hijacking your deep link by also registering to the same scheme and then obtaining access to the data your link contains. Sending something like `app://products/1` is not harmful, but sending tokens is a security concern.

When the operating system has two or more applications to choose from when opening a link, Android will show the user a [Disambiguation dialog](https://developer.android.com/training/basics/intents/sending#disambiguation-dialog) and ask them to choose which application to use to open the link. On iOS however, the operating system will make the choice for you, so the user will be blissfully unaware. Apple has made steps to address this issue in later iOS versions (iOS 11) where they instituted a first-come-first-served principle, although this vulnerability could still be exploited in different ways which you can read more about [here](https://thehackernews.com/2019/07/ios-custom-url-scheme.html). Using [universal links](https://developer.apple.com/ios/universal-links/) will allow linking to content within your app securely in iOS.

### OAuth2 and Redirects​

The OAuth2 authentication protocol is incredibly popular nowadays, prided as the most complete and secure protocol around. The OpenID Connect protocol is also based on this. In OAuth2, the user is asked to authenticate via a third party. On successful completion, this third party redirects back to the requesting application with a verification code which can be exchanged for a JWT — a [JSON Web Token](https://jwt.io/introduction/). JWT is an open standard for securely transmitting information between parties on the web.

On the web, this redirect step is secure, because URLs on the web are guaranteed to be unique. This is not true for apps because, as mentioned earlier, there is no centralized method of registering URL schemes! In order to address this security concern, an additional check must be added in the form of PKCE.

[PKCE](https://oauth.net/2/pkce/), pronounced “Pixy” stands for Proof of Key Code Exchange, and is an extension to the OAuth 2 spec. This involves adding an additional layer of security which verifies that the authentication and token exchange requests come from the same client. PKCE uses the [SHA 256](https://www.movable-type.co.uk/scripts/sha256.html) Cryptographic Hash Algorithm. SHA 256 creates a unique “signature” for a text or file of any size, but it is:

- Always the same length regardless of the input file
- Guaranteed to always produce the same result for the same input
- One way (that is, you can’t reverse engineer it to reveal the original input)

Now you have two values:

- **code_verifier** - a large random string generated by the client
- **code_challenge** - the SHA 256 of the code_verifier

During the initial `/authorize` request, the client also sends the `code_challenge` for the `code_verifier` it keeps in memory. After the authorize request has returned correctly, the client also sends the `code_verifier` that was used to generate the `code_challenge`. The IDP will then calculate the `code_challenge`, see if it matches what was set on the very first `/authorize` request, and only send the access token if the values match.

This guarantees that only the application that triggered the initial authorization flow would be able to successfully exchange the verification code for a JWT. So even if a malicious application gets access to the verification code, it will be useless on its own. To see this in action, check out [this example](https://aaronparecki.com/oauth-2-simplified/#mobile-apps).

A library to consider for native OAuth is [react-native-app-auth](https://github.com/FormidableLabs/react-native-app-auth). React-native-app-auth is an SDK for communicating with OAuth2 providers. It wraps the native [AppAuth-iOS](https://github.com/openid/AppAuth-iOS) and [AppAuth-Android](https://github.com/openid/AppAuth-Android) libraries and can support PKCE.

 note

`react-native-app-auth` can support PKCE only if your Identity Provider supports it.

![OAuth2 with PKCE](https://reactnative.dev/assets/images/diagram_pkce-e0b4a829176ac05d07b0bcec73994985.svg)

## Network Security​

Your APIs should always use [SSL encryption](https://www.ssl.com/faqs/faq-what-is-ssl/). SSL encryption protects against the requested data being read in plain text between when it leaves the server and before it reaches the client. You’ll know the endpoint is secure, because it starts with `https://` instead of `http://`.

### SSL Pinning​

Using https endpoints could still leave your data vulnerable to interception. With https, the client will only trust the server if it can provide a valid certificate that is signed by a trusted Certificate Authority that is pre-installed on the client. An attacker could take advantage of this by installing a malicious root CA certificate to the user’s device, so the client would trust all certificates that are signed by the attacker. Thus, relying on certificates alone could still leave you vulnerable to a [man-in-the-middle attack](https://en.wikipedia.org/wiki/Man-in-the-middle_attack).

**SSL pinning** is a technique that can be used on the client side to avoid this attack. It works by embedding (or pinning) a list of trusted certificates to the client during development, so that only the requests signed with one of the trusted certificates will be accepted, and any self-signed certificates will not be.

 Caution

When using SSL pinning, you should be mindful of certificate expiry. Certificates expire every 1-2 years and when one does, it’ll need to be updated in the app as well as on the server. As soon as the certificate on the server has been updated, any apps with the old certificate embedded in them will cease to work.

## Summary​

There is no bulletproof way to handle security, but with conscious effort and diligence, it is possible to significantly reduce the likelihood of a security breach in your application. Invest in security proportional to the sensitivity of the data stored in your application, the number of users, and the damage a hacker could do when gaining access to their account. And remember: it’s significantly harder to access information that was never requested in the first place.

Is this page useful?

---

# Set Up Your Environment

> In this guide, you'll learn how to set up your environment, so that you can run your project with Android Studio and Xcode. This will allow you to develop with Android emulators and iOS simulators, build your app locally, and more.

In this guide, you'll learn how to set up your environment, so that you can run your project with Android Studio and Xcode. This will allow you to develop with Android emulators and iOS simulators, build your app locally, and more.

 info

This guide requires Android Studio or Xcode. If you already have one of these programs installed, you should be able to get up and running within a few minutes. If they are not installed, you should expect to spend about an hour installing and configuring them.

Is setting up my environment required?

Setting up your environment is not required if you're using a [Framework](https://reactnative.dev/architecture/glossary#react-native-framework). With a React Native Framework, you don't need to set up Android Studio or Xcode as it will take care of building the native app for you

If you have constraints that prevent you from using a Framework, or you'd like to write your own Framework, then setting up your local environment is a requirement. After your environment is set up, learn how to [get started without a framework](https://reactnative.dev/docs/getting-started-without-a-framework).

#### Development OS​

#### Target OS​

## Installing dependencies​

You will need Node, Watchman, the React Native command line interface, a JDK, and Android Studio.

While you can use any editor of your choice to develop your app, you will need to install Android Studio in order to set up the necessary tooling to build your React Native app for Android.

### Node & Watchman

We recommend installing Node and Watchman using [Homebrew](https://brew.sh/). Run the following commands in a Terminal after installing Homebrew:

 shell

```
brew install nodebrew install watchman
```

If you have already installed Node on your system, make sure it is Node 20.19.4 or newer.

[Watchman](https://facebook.github.io/watchman) is a tool by Facebook for watching changes in the filesystem. It is highly recommended you install it for better performance.

### Java Development Kit

We recommend installing the OpenJDK distribution called Azul **Zulu** using [Homebrew](https://brew.sh/). Run the following commands in a Terminal after installing Homebrew:

 shell

```
brew install --cask zulu@17# Get path to where cask was installed to find the JDK installerbrew info --cask zulu@17# ==> zulu@17: <version number># https://www.azul.com/downloads/# Installed# /opt/homebrew/Caskroom/zulu@17/<version number> (185.8MB) (note that the path is /usr/local/Caskroom on non-Apple Silicon Macs)# Installed using the formulae.brew.sh API on 2024-06-06 at 10:00:00# Navigate to the folderopen /opt/homebrew/Caskroom/zulu@17/<version number> # or /usr/local/Caskroom/zulu@17/<version number>
```

After opening Finder, double click the `Double-Click to Install Azul Zulu JDK 17.pkg` package to install the JDK.

After the JDK installation, add or update your `JAVA_HOME` environment variable in `~/.zshrc` (or in `~/.bash_profile`).

If you used above steps, JDK will likely be located at `/Library/Java/JavaVirtualMachines/zulu-17.jdk/Contents/Home`:

 shell

```
export JAVA_HOME=/Library/Java/JavaVirtualMachines/zulu-17.jdk/Contents/Home
```

The Zulu OpenJDK distribution offers JDKs for **both Intel and M1 Macs**. This will make sure your builds are faster on M1 Macs compared to using an Intel-based JDK.

If you have already installed JDK on your system, we recommend JDK 17. You may encounter problems using higher JDK versions.

### Android development environment

Setting up your development environment can be somewhat tedious if you're new to Android development. If you're already familiar with Android development, there are a few things you may need to configure. In either case, please make sure to carefully follow the next few steps.

#### 1. Install Android Studio

[Download and install Android Studio](https://developer.android.com/studio). While on Android Studio installation wizard, make sure the boxes next to all of the following items are checked:

- `Android SDK`
- `Android SDK Platform`
- `Android Virtual Device`

Then, click "Next" to install all of these components.

 note

If the checkboxes are grayed out, you will have a chance to install these components later on.

Once setup has finalized and you're presented with the Welcome screen, proceed to the next step.

#### 2. Install the Android SDK

Android Studio installs the latest Android SDK by default. Building a React Native app with native code, however, requires the `Android 15 (VanillaIceCream)` SDK in particular. Additional Android SDKs can be installed through the SDK Manager in Android Studio.

To do that, open Android Studio, click on "More Actions" button and select "SDK Manager".

![Android Studio Welcome](https://reactnative.dev/assets/images/GettingStartedAndroidStudioWelcomeMacOS-8af2dfd190d6acc795d58c7f89197dcd.png)

 tip

The SDK Manager can also be found within the Android Studio "Settings" dialog, under **Languages & Frameworks** → **Android SDK**.

Select the "SDK Platforms" tab from within the SDK Manager, then check the box next to "Show Package Details" in the bottom right corner. Look for and expand the `Android 15 (VanillaIceCream)` entry, then make sure the following items are checked:

- `Android SDK Platform 35`
- `Intel x86 Atom_64 System Image` or `Google APIs Intel x86 Atom System Image` or (for Apple M1 Silicon) `Google APIs ARM 64 v8a System Image`

Next, select the "SDK Tools" tab and check the box next to "Show Package Details" here as well. Look for and expand the "Android SDK Build-Tools" entry, then make sure that `36.0.0` and `Android SDK Command-line Tools (latest)` are selected.

Finally, click "Apply" to download and install the Android SDK and related build tools.

#### 3. Configure the ANDROID_HOME environment variable

The React Native tools require some environment variables to be set up in order to build apps with native code.

Add the following lines to your `~/.zprofile` or `~/.zshrc` (if you are using `bash`, then `~/.bash_profile` or `~/.bashrc`) config file:

 shell

```
export ANDROID_HOME=$HOME/Library/Android/sdkexport PATH=$PATH:$ANDROID_HOME/emulatorexport PATH=$PATH:$ANDROID_HOME/platform-tools
```

Run `source ~/.zprofile` (or `source ~/.bash_profile` for `bash`) to load the config into your current shell. Verify that ANDROID_HOME has been set by running `echo $ANDROID_HOME` and the appropriate directories have been added to your path by running `echo $PATH`.

 note

Please make sure you use the correct Android SDK path. You can find the actual location of the SDK in the Android Studio "Settings" dialog, under **Languages & Frameworks** → **Android SDK**.

## Preparing the Android device

You will need an Android device to run your React Native Android app. This can be either a physical Android device, or more commonly, you can use an Android Virtual Device which allows you to emulate an Android device on your computer.

Either way, you will need to prepare the device to run Android apps for development.

### Using a physical device

If you have a physical Android device, you can use it for development in place of an AVD by plugging it in to your computer using a USB cable and following the instructions [here](https://reactnative.dev/docs/running-on-device).

### Using a virtual device

If you use Android Studio to open `./AwesomeProject/android`, you can see the list of available Android Virtual Devices (AVDs) by opening the "AVD Manager" from within Android Studio. Look for an icon that looks like this:

 ![Android Studio AVD Manager](https://reactnative.dev/docs/assets/GettingStartedAndroidStudioAVD.svg)

If you have recently installed Android Studio, you will likely need to [create a new AVD](https://developer.android.com/studio/run/managing-avds.html). Select "Create Virtual Device...", then pick any Phone from the list and click "Next", then select the **VanillaIceCream** API Level 35 image.

Click "Next" then "Finish" to create your AVD. At this point you should be able to click on the green triangle button next to your AVD to launch it.

### That's it!

Congratulations! You successfully set up your development environment.

 ![image](https://reactnative.dev/docs/assets/GettingStartedCongratulations.png)

## Now what?

- If you want to add this new React Native code to an existing application, check out the [Integration guide](https://reactnative.dev/docs/integration-with-existing-apps).
- If you're curious to learn more about React Native, check out the [Introduction to React Native](https://reactnative.dev/docs/getting-started).

## Installing dependencies​

You will need Node, Watchman, the React Native command line interface, Xcode and CocoaPods.

While you can use any editor of your choice to develop your app, you will need to install Xcode in order to set up the necessary tooling to build your React Native app for iOS.

### Node & Watchman​

We recommend installing Node and Watchman using [Homebrew](https://brew.sh/). Run the following commands in a Terminal after installing Homebrew:

 shell

```
brew install nodebrew install watchman
```

If you have already installed Node on your system, make sure it is Node 20.19.4 or newer.

[Watchman](https://facebook.github.io/watchman) is a tool by Facebook for watching changes in the filesystem. It is highly recommended you install it for better performance.

### Xcode​

Please use the **latest version** of Xcode.

The easiest way to install Xcode is via the [Mac App Store](https://itunes.apple.com/us/app/xcode/id497799835?mt=12). Installing Xcode will also install the iOS Simulator and all the necessary tools to build your iOS app.

#### Command Line Tools​

You will also need to install the Xcode Command Line Tools. Open Xcode, then choose **Settings... (or Preferences...)** from the Xcode menu. Go to the Locations panel and install the tools by selecting the most recent version in the Command Line Tools dropdown.

![Xcode Command Line Tools](https://reactnative.dev/assets/images/GettingStartedXcodeCommandLineTools-a319295928960a4458698528086e3230.png)

#### Installing an iOS Simulator in Xcode​

To install a simulator, open **Xcode > Settings... (or Preferences...)** and select the **Platforms (or Components)** tab. Select a simulator with the corresponding version of iOS you wish to use.

If you are using Xcode version 14.0 or greater to install a simulator, open **Xcode > Settings > Platforms** tab, then click "+" icon and select **iOS…** option.

#### CocoaPods​

[CocoaPods](https://cocoapods.org/) is one of the dependency management system available for iOS. CocoaPods is a Ruby [gem](https://en.wikipedia.org/wiki/RubyGems). You can install CocoaPods using the version of Ruby that ships with the latest version of macOS.

For more information, please visit [CocoaPods Getting Started guide](https://guides.cocoapods.org/using/getting-started.html).

### [Optional] Configuring your environment​

Starting from React Native version 0.69, it is possible to configure the Xcode environment using the `.xcode.env` file provided by the template.

The `.xcode.env` file contains an environment variable to export the path to the `node` executable in the `NODE_BINARY` variable.
This is the **suggested approach** to decouple the build infrastructure from the system version of `node`. You should customize this variable with your own path or your own `node` version manager, if it differs from the default.

On top of this, it's possible to add any other environment variable and to source the `.xcode.env` file in your build script phases. If you need to run script that requires some specific environment, this is the **suggested approach**: it allows to decouple the build phases from a specific environment.

 info

If you are already using [NVM](https://nvm.sh/) (a command which helps you install and switch between versions of Node.js) and [zsh](https://ohmyz.sh/), you might want to move the code that initialize NVM from your `~/.zshrc` into a `~/.zshenv` file to help Xcode find your Node executable:

zsh

```
export NVM_DIR="$HOME/.nvm"[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
```

You might also want to ensure that all "shell script build phase" of your Xcode project, is using `/bin/zsh` as its shell.

### That's it!

Congratulations! You successfully set up your development environment.

 ![image](https://reactnative.dev/docs/assets/GettingStartedCongratulations.png)

## Now what?

- If you want to add this new React Native code to an existing application, check out the [Integration guide](https://reactnative.dev/docs/integration-with-existing-apps).
- If you're curious to learn more about React Native, check out the [Introduction to React Native](https://reactnative.dev/docs/getting-started).

#### Target OS​

## Installing dependencies

You will need Node, the React Native command line interface, a JDK, and Android Studio.

While you can use any editor of your choice to develop your app, you will need to install Android Studio in order to set up the necessary tooling to build your React Native app for Android.

### Node, JDK

We recommend installing Node via [Chocolatey](https://chocolatey.org/install), a popular package manager for Windows.

It is recommended to use an LTS version of Node. If you want to be able to switch between different versions, you might want to install Node via [nvm-windows](https://github.com/coreybutler/nvm-windows), a Node version manager for Windows.

React Native also requires [Java SE Development Kit (JDK)](https://openjdk.java.net/projects/jdk/17/), which can be installed using Chocolatey as well.

Open an Administrator Command Prompt (right click Command Prompt and select "Run as Administrator"), then run the following command:

 powershell

```
choco install -y nodejs-lts microsoft-openjdk17
```

If you have already installed Node on your system, make sure it is Node 20.19.4 or newer. If you already have a JDK on your system, we recommend JDK17. You may encounter problems using higher JDK versions.

 note

You can find additional installation options on [Node's Downloads page](https://nodejs.org/en/download/).

 info

If you're using the latest version of Java Development Kit, you'll need to change the Gradle version of your project so it can recognize the JDK. You can do that by going to `{project root folder}\android\gradle\wrapper\gradle-wrapper.properties` and changing the `distributionUrl` value to upgrade the Gradle version. You can check out [here the latest releases of Gradle](https://gradle.org/releases/).

### Android development environment

Setting up your development environment can be somewhat tedious if you're new to Android development. If you're already familiar with Android development, there are a few things you may need to configure. In either case, please make sure to carefully follow the next few steps.

#### 1. Install Android Studio

[Download and install Android Studio](https://developer.android.com/studio). While on Android Studio installation wizard, make sure the boxes next to all of the following items are checked:

- `Android SDK`
- `Android SDK Platform`
- `Android Virtual Device`
- If you are not already using Hyper-V: `Performance (Intel ® HAXM)` ([See here for AMD or Hyper-V](https://android-developers.googleblog.com/2018/07/android-emulator-amd-processor-hyper-v.html))

Then, click "Next" to install all of these components.

 note

If the checkboxes are grayed out, you will have a chance to install these components later on.

Once setup has finalized and you're presented with the Welcome screen, proceed to the next step.

#### 2. Install the Android SDK

Android Studio installs the latest Android SDK by default. Building a React Native app with native code, however, requires the `Android 15 (VanillaIceCream)` SDK in particular. Additional Android SDKs can be installed through the SDK Manager in Android Studio.

To do that, open Android Studio, click on "More Actions" button and select "SDK Manager".

![Android Studio Welcome](https://reactnative.dev/assets/images/GettingStartedAndroidStudioWelcomeWindows-8a34e703bcb79bb67f84764b04f3e05c.png)

 tip

The SDK Manager can also be found within the Android Studio "Settings" dialog, under **Languages & Frameworks** → **Android SDK**.

Select the "SDK Platforms" tab from within the SDK Manager, then check the box next to "Show Package Details" in the bottom right corner. Look for and expand the `Android 15 (VanillaIceCream)` entry, then make sure the following items are checked:

- `Android SDK Platform 35`
- `Intel x86 Atom_64 System Image` or `Google APIs Intel x86 Atom System Image`

Next, select the "SDK Tools" tab and check the box next to "Show Package Details" here as well. Look for and expand the `Android SDK Build-Tools` entry, then make sure that `36.0.0` and `Android SDK Command-line Tools (latest)` are selected.

Finally, click "Apply" to download and install the Android SDK and related build tools.

#### 3. Configure the ANDROID_HOME environment variable

The React Native tools require some environment variables to be set up in order to build apps with native code.

1. Open the **Windows Control Panel.**
2. Click on **User Accounts,** then click **User Accounts** again
3. Click on **Change my environment variables**
4. Click on **New...** to create a new `ANDROID_HOME` user variable that points to the path to your Android SDK:

![ANDROID_HOME Environment Variable](data:image/png;base64,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)

The SDK is installed, by default, at the following location:

 powershell

```
%LOCALAPPDATA%\Android\Sdk
```

You can find the actual location of the SDK in the Android Studio "Settings" dialog, under **Languages & Frameworks** → **Android SDK**.

Open a new Command Prompt window to ensure the new environment variable is loaded before proceeding to the next step.

1. Open powershell
2. Copy and paste **Get-ChildItem -Path Env:\** into powershell
3. Verify `ANDROID_HOME` has been added

#### 4. Add platform-tools to Path

1. Open the **Windows Control Panel.**
2. Click on **User Accounts,** then click **User Accounts** again
3. Click on **Change my environment variables**
4. Select the **Path** variable.
5. Click **Edit.**
6. Click **New** and add the path to platform-tools to the list.

The default location for this folder is:

 powershell

```
%LOCALAPPDATA%\Android\Sdk\platform-tools
```

## Preparing the Android device

You will need an Android device to run your React Native Android app. This can be either a physical Android device, or more commonly, you can use an Android Virtual Device which allows you to emulate an Android device on your computer.

Either way, you will need to prepare the device to run Android apps for development.

### Using a physical device

If you have a physical Android device, you can use it for development in place of an AVD by plugging it in to your computer using a USB cable and following the instructions [here](https://reactnative.dev/docs/running-on-device).

### Using a virtual device

If you use Android Studio to open `./AwesomeProject/android`, you can see the list of available Android Virtual Devices (AVDs) by opening the "AVD Manager" from within Android Studio. Look for an icon that looks like this:

 ![Android Studio AVD Manager](https://reactnative.dev/docs/assets/GettingStartedAndroidStudioAVD.svg)

If you have recently installed Android Studio, you will likely need to [create a new AVD](https://developer.android.com/studio/run/managing-avds.html). Select "Create Virtual Device...", then pick any Phone from the list and click "Next", then select the **VanillaIceCream** API Level 35 image.

 note

If you don't have HAXM installed, click on "Install HAXM" or follow [these instructions](https://github.com/intel/haxm/wiki/Installation-Instructions-on-Windows) to set it up, then go back to the AVD Manager.

Click "Next" then "Finish" to create your AVD. At this point you should be able to click on the green triangle button next to your AVD to launch it.

### That's it!

Congratulations! You successfully set up your development environment.

 ![image](https://reactnative.dev/docs/assets/GettingStartedCongratulations.png)

## Now what?

- If you want to add this new React Native code to an existing application, check out the [Integration guide](https://reactnative.dev/docs/integration-with-existing-apps).
- If you're curious to learn more about React Native, check out the [Introduction to React Native](https://reactnative.dev/docs/getting-started).

## Unsupported​

info

A Mac is required to build projects with native code for iOS. You can use [Expo Go](https://expo.dev/go) from [Expo](https://reactnative.dev/docs/environment-setup#start-a-new-react-native-project-with-expo) to develop your app on your iOS device.

#### Target OS​

## Installing dependencies​

You will need Node, the React Native command line interface, a JDK, and Android Studio.

While you can use any editor of your choice to develop your app, you will need to install Android Studio in order to set up the necessary tooling to build your React Native app for Android.

### Node

Follow the [installation instructions for your Linux distribution](https://nodejs.org/en/download/package-manager/) to install Node 20.19.4 or newer.

### Java Development Kit

React Native currently recommends version 17 of the Java SE Development Kit (JDK). You may encounter problems using higher JDK versions. You may download and install [OpenJDK](https://openjdk.java.net) from [AdoptOpenJDK](https://adoptopenjdk.net/) or your system packager.

### Android development environment

Setting up your development environment can be somewhat tedious if you're new to Android development. If you're already familiar with Android development, there are a few things you may need to configure. In either case, please make sure to carefully follow the next few steps.

#### 1. Install Android Studio

[Download and install Android Studio](https://developer.android.com/studio). While on Android Studio installation wizard, make sure the boxes next to all of the following items are checked:

- `Android SDK`
- `Android SDK Platform`
- `Android Virtual Device`

Then, click "Next" to install all of these components.

 note

If the checkboxes are grayed out, you will have a chance to install these components later on.

Once setup has finalized and you're presented with the Welcome screen, proceed to the next step.

#### 2. Install the Android SDK

Android Studio installs the latest Android SDK by default. Building a React Native app with native code, however, requires the `Android 15 (VanillaIceCream)` SDK in particular. Additional Android SDKs can be installed through the SDK Manager in Android Studio.

To do that, open Android Studio, click on "Configure" button and select "SDK Manager".

 tip

The SDK Manager can also be found within the Android Studio "Settings" dialog, under **Languages & Frameworks** → **Android SDK**.

Select the "SDK Platforms" tab from within the SDK Manager, then check the box next to "Show Package Details" in the bottom right corner. Look for and expand the `Android 15 (VanillaIceCream)` entry, then make sure the following items are checked:

- `Android SDK Platform 35`
- `Intel x86 Atom_64 System Image` or `Google APIs Intel x86 Atom System Image`

Next, select the "SDK Tools" tab and check the box next to "Show Package Details" here as well. Look for and expand the "Android SDK Build-Tools" entry, then make sure that `36.0.0` and `Android SDK Command-line Tools (latest)` are selected.

Finally, click "Apply" to download and install the Android SDK and related build tools.

#### 3. Configure the ANDROID_HOME environment variable

The React Native tools require some environment variables to be set up in order to build apps with native code.

Add the following lines to your `$HOME/.bash_profile` or `$HOME/.bashrc` (if you are using `zsh` then `~/.zprofile` or `~/.zshrc`) config file:

 shell

```
export ANDROID_HOME=$HOME/Android/Sdkexport PATH=$PATH:$ANDROID_HOME/emulatorexport PATH=$PATH:$ANDROID_HOME/platform-tools
```

 note

`.bash_profile` is specific to `bash`. If you're using another shell, you will need to edit the appropriate shell-specific config file.

Type `source $HOME/.bash_profile` for `bash` or `source $HOME/.zprofile` to load the config into your current shell. Verify that ANDROID_HOME has been set by running `echo $ANDROID_HOME` and the appropriate directories have been added to your path by running `echo $PATH`.

 note

Please make sure you use the correct Android SDK path. You can find the actual location of the SDK in the Android Studio "Settings" dialog, under **Languages & Frameworks** → **Android SDK**.

### Watchman

Follow the [Watchman installation guide](https://facebook.github.io/watchman/docs/install#buildinstall) to compile and install Watchman from source.

 info

[Watchman](https://facebook.github.io/watchman/docs/install) is a tool by Facebook for watching changes in the filesystem. It is highly recommended you install it for better performance and increased compatibility in certain edge cases (translation: you may be able to get by without installing this, but your mileage may vary; installing this now may save you from a headache later).

## Preparing the Android device

You will need an Android device to run your React Native Android app. This can be either a physical Android device, or more commonly, you can use an Android Virtual Device which allows you to emulate an Android device on your computer.

Either way, you will need to prepare the device to run Android apps for development.

### Using a physical device

If you have a physical Android device, you can use it for development in place of an AVD by plugging it in to your computer using a USB cable and following the instructions [here](https://reactnative.dev/docs/running-on-device).

### Using a virtual device

If you use Android Studio to open `./AwesomeProject/android`, you can see the list of available Android Virtual Devices (AVDs) by opening the "AVD Manager" from within Android Studio. Look for an icon that looks like this:

 ![Android Studio AVD Manager](https://reactnative.dev/docs/assets/GettingStartedAndroidStudioAVD.svg)

If you have recently installed Android Studio, you will likely need to [create a new AVD](https://developer.android.com/studio/run/managing-avds.html). Select "Create Virtual Device...", then pick any Phone from the list and click "Next", then select the **VanillaIceCream** API Level 35 image.

 tip

We recommend configuring [VM acceleration](https://developer.android.com/studio/run/emulator-acceleration.html#vm-linux) on your system to improve performance. Once you've followed those instructions, go back to the AVD Manager.

Click "Next" then "Finish" to create your AVD. At this point you should be able to click on the green triangle button next to your AVD to launch it.

### That's it!

Congratulations! You successfully set up your development environment.

 ![image](https://reactnative.dev/docs/assets/GettingStartedCongratulations.png)

## Now what?

- If you want to add this new React Native code to an existing application, check out the [Integration guide](https://reactnative.dev/docs/integration-with-existing-apps).
- If you're curious to learn more about React Native, check out the [Introduction to React Native](https://reactnative.dev/docs/getting-started).

## Unsupported​

info

A Mac is required to build projects with native code for iOS. You can use [Expo Go](https://expo.dev/go) from [Expo](https://reactnative.dev/docs/environment-setup#start-a-new-react-native-project-with-expo) to develop your app on your iOS device.

Is this page useful?

---

# Settings

> Settings serves as a wrapper for NSUserDefaults, a persistent key-value store available only on iOS.

`Settings` serves as a wrapper for [NSUserDefaults](https://developer.apple.com/documentation/foundation/nsuserdefaults), a persistent key-value store available only on iOS.

## Example​

---

# Reference

## Methods​

### clearWatch()​

 tsx

```
static clearWatch(watchId: number);
```

`watchId` is the number returned by `watchKeys()` when the subscription was originally configured.

---

### get()​

 tsx

```
static get(key: string): any;
```

Get the current value for a given `key` in `NSUserDefaults`.

---

### set()​

 tsx

```
static set(settings: Record<string, any>);
```

Set one or more values in `NSUserDefaults`.

---

### watchKeys()​

 tsx

```
static watchKeys(keys: string | array<string>, callback: () => void): number;
```

Subscribe to be notified when the value for any of the keys specified by the `keys` parameter has been changed in `NSUserDefaults`. Returns a `watchId` number that may be used with `clearWatch()` to unsubscribe.

 note

`watchKeys()` by design ignores internal `set()` calls and fires callback only on changes preformed outside of React Native code.

Is this page useful?
