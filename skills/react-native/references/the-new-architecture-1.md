# Advanced Topics on Native Modules Development and more

# Advanced Topics on Native Modules Development

> This document contains a set of advanced topics to implement more complex functionalities of Native Components. It is recommended to first read the Codegen section and the guides on Native Components.

This document contains a set of advanced topics to implement more complex functionalities of Native Components. It is recommended to first read the [Codegen](https://reactnative.dev/docs/the-new-architecture/what-is-codegen) section and the guides on [Native Components](https://reactnative.dev/docs/fabric-native-components-introduction).

This guide will cover the following topics:

- [Direct Manipulation](https://reactnative.dev/docs/the-new-architecture/direct-manipulation-new-architecture)
- [Measuring the Layout](https://reactnative.dev/docs/the-new-architecture/layout-measurements)
- [Invoking native functions on your native component](https://reactnative.dev/docs/next/the-new-architecture/fabric-component-native-commands)

Is this page useful?

---

# Advanced Topics on Native Modules Development

> This document contains a set of advanced topics to implement more complex functionalities of Native Modules. It is recommended to first read the Codegen section and the guides on Native Modules.

This document contains a set of advanced topics to implement more complex functionalities of Native Modules. It is recommended to first read the [Codegen](https://reactnative.dev/docs/the-new-architecture/what-is-codegen) section and the guides on [Native Modules](https://reactnative.dev/docs/turbo-native-modules-introduction).

This guide will cover the following topics:

- [Add custom C++ types to your C++ modules](https://reactnative.dev/docs/the-new-architecture/custom-cxx-types)
- [Use Swift in your Module](https://reactnative.dev/docs/next/the-new-architecture/turbo-modules-with-swift)
- [Emit custom events from your Native Modules](https://reactnative.dev/docs/next/the-new-architecture/native-modules-custom-events)
- [Native Modules Lifecycle](https://reactnative.dev/docs/next/the-new-architecture/native-modules-lifecycle)

Is this page useful?

---

# The Codegen CLI

> Calling Gradle or manually calling a script might be hard to remember and it requires a lot of ceremony.

Calling Gradle or manually calling a script might be hard to remember and it requires a lot of ceremony.

To simplify it, we created a CLI tool that can help you running those tasks: the **Codegen** cli. This command runs [@react-native/codegen](https://www.npmjs.com/package/@react-native/codegen) for your project. The following options are available:

 sh

```
npx @react-native-community/cli codegen --helpUsage: rnc-cli codegen [options]Options:  --verbose            Increase logging verbosity  --path <path>        Path to the React Native project root. (default: "/Users/MyUsername/projects/my-app")  --platform <string>  Target platform. Supported values: "android", "ios", "all". (default: "all")  --outputPath <path>  Path where generated artifacts will be output to.  -h, --help           display help for command
```

## Examples​

- Read `package.json` from the current working directory, generate code based on its codegenConfig.

 shell

```
npx @react-native-community/cli codegen
```

- Read `package.json` from the current working directory, generate iOS code in the location defined in the codegenConfig.

 shell

```
npx @react-native-community/cli codegen --platform ios
```

- Read `package.json` from `third-party/some-library`, generate Android code in `third-party/some-library/android/generated`.

 shell

```
npx @react-native-community/cli codegen \    --path third-party/some-library \    --platform android \    --outputPath third-party/some-library/android/generated
```

## Including Generated Code into Libraries​

The Codegen CLI is a great tool for library developers. It can be used to take a sneak-peek at the generated code to see which interfaces you need to implement.

Normally the generated code is not included in the library, and the app that uses the library is responsible for running the Codegen at build time.
This is a good setup for most cases, but Codegen also offers a mechanism to include the generated code in the library itself via the `includesGeneratedCode` property.

It's important to understand what are the implications of using `includesGeneratedCode = true`. Including the generated code comes with several benefits such as:

- No need to rely on the app to run **Codegen** for you, the generated code is always there.
- The implementation files are always consistent with the generated interfaces (this makes your library code more resilient against API changes in codegen).
- No need to include two sets of files to support both architectures on Android. You can only keep the New Architecture one, and it is guaranteed to be backwards compatible.
- Since all native code is there, it is possible to ship the native part of the library as a prebuild.

On the other hand, you also need to be aware of one drawback:

- The generated code will use the React Native version defined inside your library. So if your library is shipping with React Native 0.76, the generated code will be based on that version. This could mean that the generated code is not compatible with apps using **previous** React Native version used by the app (e.g. an App running on React Native 0.75).

## EnablingincludesGeneratedCode​

To enable this setup:

- Add the `includesGeneratedCode` property into your library's `codegenConfig` field in the `package.json` file. Set its value to `true`.
- Run **Codegen** locally with the codegen CLI.
- Update your `package.json` to include the generated code.
- Update your `podspec` to include the generated code.
- Update your `build.Gradle` file to include the generated code.
- Update `cmakeListsPath` in `react-native.config.js` so that Gradle doesn't look for CMakeLists file in the build directory but instead in your outputDir.

Is this page useful?

---

# Create a Library for Your Module

> React Native has a rich ecosystem of libraries to solve common problems. We collect React Native libraries in the reactnative.directory website, and this is a great resource to bookmark for every React Native developer.

React Native has a rich ecosystem of libraries to solve common problems. We collect React Native libraries in the [reactnative.directory](https://reactnative.directory) website, and this is a great resource to bookmark for every React Native developer.

Sometimes, you might be working on a module that is worth extracting in a separate library for code reuse. This can be a library that you want to reuse in all your apps, a library that you want to distribute to the ecosystem as an open source component, or even a library you'd like to sell.

In this guide, you'll learn:

- how to extract a module into a library
- how to distribute the library using NPM

## Extract the Module into a Library​

You can use the [create-react-native-library](https://callstack.github.io/react-native-builder-bob/create) tool to create a new library. This tool sets up a new library with all the boilerplate code that is needed: all the configuration files and all files required by the various platforms. It also comes with a nice interactive menu to guide you through the creation of the library.

To extract a module into a separate library, you can follow these steps:

1. Create the new library
2. Move the code from the App to the Library
3. Update the code to reflect the new structure
4. Publish it.

### 1. Create a Library​

1. Start the creation process by running the command:

 sh

```
npx create-react-native-library@latest <Name of Your Library>
```

1. Add a name for your module. It must be a valid npm name, so it should be all lowercase. You can use `-` to separate words.
2. Add a description for the package.
3. Continue filling the form until you reach the question *"What type of library do you want to develop?"* ![What type of Library](https://reactnative.dev/assets/images/what-library-82a9a474327fd86f807a7eedf6cd29fc.png)
4. For the sake of this guide, select the *Turbo module* option. Notice that you can create libraries for both New Architecture and Legacy Architecture.
5. Then, you can choose whether you want a library that access the platform (Kotlin & Objective-C) or a shared C++ library (C++ for Android and iOS).
6. Finally, select the `Test App` as last option. This option creates the library with a separate app already configured within the library folder.

Once the interactive prompt is done, the tool creates a folder whose structure looks like this in Visual Studio Code:

 ![Folder structure after initializing a new library.](https://reactnative.dev/docs/assets/turbo-native-modules/c++visualstudiocode.webp)

Feel free to explore the code that has been created for you. However, the most important parts:

- The `android` folder: this is where the Android code lives
- The `cpp` folder: this is where the c++ code lives
- The `ios` folder: this is where the iOS code lives
- The `src` folder: this is where the JS code lives.

The `package.json` is already configured with all the information that we provided to the `create-react-native-library` tool, including the name and the description of the package. Notice that the `package.json` is also already configured to run Codegen.

 json

```
"codegenConfig": {    "name": "RN<your module name>Spec",    "type": "all",    "jsSrcsDir": "src",    "outputDir": {      "ios": "ios/generated",      "android": "android/generated"    },    "android": {      "javaPackageName": "com.<name-of-the-module>"    }  },
```

Finally, the library contains already all the infrastructure to let the library be linked with iOS and Android.

### 2. Copy the Code over from Your App​

The rest of the guide assumes that you have a local Turbo Native Module in your app, created following the guidelines shown in the other guides in the website: platform specific Turbo Native Modules, or [cross-platform Turbo Native Modules](https://reactnative.dev/docs/the-new-architecture/pure-cxx-modules). But it works also for Components and legacy architecture modules and components. You'll have to adapt the files you need to copy and update.

1. **[Not required for legacy architecture modules and components]** Move the code you have in the `specs` folder in your app into the `src` folder created by the `create-react-native-library` folder.
2. Update the `index.ts` file to properly export the Turbo Native Module spec so that it is accessible from the library. For example:

 ts

```
import NativeSampleModule from './NativeSampleModule';export default NativeSampleModule;
```

1. Copy the native module over:
  - Replace the code in the `android/src/main/java/com/<name-of-the-module>` with the code you wrote in the app for your native module, if any.
  - Replace the code in the `ios` folder with the code you wrote in your app for your native module, if any.
  - Replace the code in the `cpp` folder with the code you wrote in your app for your native module, if any.
2. **[Not required for legacy architecture modules and components]** Update all the references from the previous spec name to the new spec name, the one that is defined in the `codegenConfig` field of the library's `package.json`. For example, if in the app `package.json` you set `AppSpecs` as `codegenConfig.name` and in the library it is called `RNNativeSampleModuleSpec`, you have to replace every occurrence of `AppSpecs` with `RNNativeSampleModuleSpec`.

That's it! You have moved all the required code out of your app and in a separate library.

## Testing your Library​

The `create-react-native-library` comes with a useful example application that is already configured to work properly with the library. This is a great way to test it!

If you look at the `example` folder, you can find the same structure of a new React Native application that you can create from the [react-native-community/template](https://github.com/react-native-community/template).

To test your library:

1. Navigate to the `example` folder.
2. Run `yarn install` to install all the dependencies.
3. For iOS only, you need to install CocoaPods: `cd ios && pod install`.
4. Build and run Android with `yarn android` from the `example` folder.
5. Build and run iOS with `yarn ios` from the `example` folder.

## Use your library as a Local Module​

There are some scenario where you might want to reuse your library as a local module for your applications, without publishing it to NPM.

In this case, you might end up in a scenario where you have your library sitting as a sibling of your apps.

 shell

```
Development├── App└── Library
```

You can use the library created with `create-react-native-library` also in this case.

1. add you library to your app by navigating into the `App` folder and running `yarn add ../Library`.
2. For iOS only, navigate in the `App/ios` folder and run `bundle exec pod install` to install your dependencies.
3. Update the `App.tsx` code to import the code in your library. For example:

 tsx

```
import NativeSampleModule from '../Library/src/index';
```

If you run your app right now, Metro would not find the JS files that it needs to serve to the app. That's because metro will be running starting from the `App` folder and it would not have access to the JS files located in the `Library` folder. To fix this, let's update the `metro.config.js` file as it follows

 diff

```
const {getDefaultConfig, mergeConfig} = require('@react-native/metro-config');/** * Metro configuration * https://reactnative.dev/docs/metro * * @type {import('metro-config').MetroConfig} */+ const path = require('path');- const config = {}+ const config = {+  // Make Metro able to resolve required external dependencies+  watchFolders: [+    path.resolve(__dirname, '../Library'),+  ],+  resolver: {+    extraNodeModules: {+      'react-native': path.resolve(__dirname, 'node_modules/react-native'),+    },+  },+};module.exports = mergeConfig(getDefaultConfig(__dirname), config);
```

The `watchFolders` configs tells Metro to watch for files and changes in some additional paths, in this case to the `../Library` path, which contains the `src/index` file you need.
The `resolver`property is required to feed to the library the React Native code used by the app. The library might refer and import code from React Native: without the additional resolver, the imports in the library will fail.

At this point, you can build and run your app as usual:

- Build and run Android with `yarn android` from the `example` folder.
- Build and run iOS with `yarn ios` from the `example` folder.

## Publish the Library on NPM​

The setup to publish everything on NPM is already in place, thanks to `create-react-native-library`.

1. Install the dependencies in your module `yarn install`.
2. Build the library running `yarn prepare`.
3. Release it with `yarn release`.

After a while, you'll find your library on NPM. To verify that, run:

 bash

```
npm view <package.name>
```

where `package.name` is the `name` you set up in the `package.json` file during the initialization of the library.

Now, you can install the library in your application by running:

 bash

```
yarn add <package.name>
```

 note

For iOS only, whenever you install a new module with some native code, you have to reinstall CocoaPods, by running `bundle exec pod install` (recommended) or `pod install` if you are not using Ruby's Bundler (not recommended).

Congratulations! You published your first React Native library.

Is this page useful?

---

# Advanced: Custom C++ Types

> This guide assumes that you are familiar with the Pure C++ Turbo Native Modules guide. This will build on top of that guide.

note

This guide assumes that you are familiar with the [Pure C++ Turbo Native Modules](https://reactnative.dev/docs/the-new-architecture/pure-cxx-modules) guide. This will build on top of that guide.

C++ Turbo Native Modules support [bridging functionality](https://github.com/facebook/react-native/tree/main/packages/react-native/ReactCommon/react/bridging) for most `std::` standard types. You can use most of those types in your modules without any additional code required.

If you want to add support for new and custom types in your app or library, you need to provide the necessary `bridging` header file.

## Adding a New Custom: Int64​

C++ Turbo Native Modules don't support `int64_t` numbers yet - because JavaScript doesn't support numbers greater 2^53. To represent numbers greater than 2^53, we can use a `string` type in JS and automatically convert it to `int64_t` in C++.

### 1. Create the Bridging Header file​

The first step to support a new custom type is to define the bridging header that takes care of converting the type **from** the JS representation to the C++ representation, and from the C++ representation **to** the JS one.

1. In the `shared` folder, add a new file called `Int64.h`
2. Add the following code to that file:

 Int64.h

```
#pragma once#include <react/bridging/Bridging.h>namespace facebook::react {template <>struct Bridging<int64_t> {  // Converts from the JS representation to the C++ representation  static int64_t fromJs(jsi::Runtime &rt, const jsi::String &value) {    try {      size_t pos;      auto str = value.utf8(rt);      auto num = std::stoll(str, &pos);      if (pos != str.size()) {        throw std::invalid_argument("Invalid number"); // don't support alphanumeric strings      }      return num;    } catch (const std::logic_error &e) {      throw jsi::JSError(rt, e.what());    }  }  // Converts from the C++ representation to the JS representation  static jsi::String toJs(jsi::Runtime &rt, int64_t value) {    return bridging::toJs(rt, std::to_string(value));  }};}
```

The key components for your custom bridging header are:

- Explicit specialization of the `Bridging` struct for your custom type. In this case, the template specify the `int64_t` type.
- A `fromJs` function to convert from the JS representation to the C++ representation
- A `toJs` function to convert from the C++ representation to the JS representation

 note

On iOS, remember to add the `Int64.h` file to the Xcode project.

### 2. Modify the JS Spec​

Now, we can modify the JS spec to add a method that uses the new type. As usual, we can use either Flow or TypeScript for our specs.

1. Open the `specs/NativeSampleTurbomodule`
2. Modify the spec as follows:

NativeSampleModule.ts

```
import {TurboModule, TurboModuleRegistry} from 'react-native';export interface Spec extends TurboModule {  readonly reverseString: (input: string) => string;+  readonly cubicRoot: (input: string) => number;}export default TurboModuleRegistry.getEnforcing<Spec>(  'NativeSampleModule',);
```

NativeSampleModule.js

```
// @flowimport type {TurboModule} from 'react-native';import { TurboModuleRegistry } from "react-native";export interface Spec extends TurboModule {  +reverseString: (input: string) => string;+  +cubicRoot: (input: string) => number;}export default (TurboModuleRegistry.getEnforcing<Spec>(  "NativeSampleModule"): Spec);
```

In this files, we are defining the function that needs to be implemented in C++.

### 3. Implement the Native Code​

Now, we need to implement the function that we declared in the JS specification.

1. Open the `specs/NativeSampleModule.h` file and apply the following changes:

 NativeSampleModule.h

```
#pragma once#include <AppSpecsJSI.h>#include <memory>#include <string>+ #include "Int64.h"namespace facebook::react {class NativeSampleModule : public NativeSampleModuleCxxSpec<NativeSampleModule> {public:  NativeSampleModule(std::shared_ptr<CallInvoker> jsInvoker);  std::string reverseString(jsi::Runtime& rt, std::string input);+ int32_t cubicRoot(jsi::Runtime& rt, int64_t input);};} // namespace facebook::react
```

1. Open the `specs/NativeSampleModule.cpp` file and apply the implement the new function:

 NativeSampleModule.cpp

```
#include "NativeSampleModule.h"+ #include <cmath>namespace facebook::react {NativeSampleModule::NativeSampleModule(std::shared_ptr<CallInvoker> jsInvoker)    : NativeSampleModuleCxxSpec(std::move(jsInvoker)) {}std::string NativeSampleModule::reverseString(jsi::Runtime& rt, std::string input) {  return std::string(input.rbegin(), input.rend());}+int32_t NativeSampleModule::cubicRoot(jsi::Runtime& rt, int64_t input) {+    return std::cbrt(input);+}} // namespace facebook::react
```

The implementation imports the `<cmath>` C++ library to perform mathematical operations, then it implements the `cubicRoot` function using the `cbrt` primitive from the `<cmath>` module.

### 4. Test your code in Your App​

Now, we can test the code in our app.

First, we need to update the `App.tsx` file to use the new method from the TurboModule. Then, we can build our apps in Android and iOS.

1. Open the `App.tsx` code apply the following changes:

 App.tsx

```
// ...+ const [cubicSource, setCubicSource] = React.useState('')+ const [cubicRoot, setCubicRoot] = React.useState(0)  return (    <SafeAreaView style={styles.container}>      <View>        <Text style={styles.title}>          Welcome to C++ Turbo Native Module Example        </Text>        <Text>Write down here the text you want to revert</Text>        <TextInput          style={styles.textInput}          placeholder="Write your text here"          onChangeText={setValue}          value={value}        />        <Button title="Reverse" onPress={onPress} />        <Text>Reversed text: {reversedValue}</Text>+        <Text>For which number do you want to compute the Cubic Root?</Text>+        <TextInput+          style={styles.textInput}+          placeholder="Write your text here"+          onChangeText={setCubicSource}+          value={cubicSource}+        />+        <Button title="Get Cubic Root" onPress={() => setCubicRoot(SampleTurboModule.cubicRoot(cubicSource))} />+        <Text>The cubic root is: {cubicRoot}</Text>      </View>    </SafeAreaView>  );}//...
```

1. To test the app on Android, run `yarn android` from the root folder of your project.
2. To test the app on iOS, run `yarn ios` from the root folder of your project.

## Adding a New Structured Custom Type: Address​

The approach above can be generalized to any kind of type. For structured types, React Native provides some helper functions that make it easier to bridge them from JS to C++ and vice versa.

Let's assume that we want to bridge a custom `Address` type with the following properties:

 ts

```
interface Address {  street: string;  num: number;  isInUS: boolean;}
```

### 1. Define the type in the specs​

For the first step, let's define the new custom type in the JS specs, so that Codegen can output all the supporting code. In this way, we don't have to manually write the code.

1. Open the `specs/NativeSampleModule` file and add the following changes.

NativeSampleModule (Add Address type and validateAddress function)

```
import {TurboModule, TurboModuleRegistry} from 'react-native';+export type Address = {+  street: string,+  num: number,+  isInUS: boolean,+};export interface Spec extends TurboModule {  readonly reverseString: (input: string) => string;+ readonly validateAddress: (input: Address) => boolean;}export default TurboModuleRegistry.getEnforcing<Spec>(  'NativeSampleModule',);
```

NativeSampleModule (Add Address type and validateAddress function)

```
// @flowimport type {TurboModule} from 'react-native';import { TurboModuleRegistry } from "react-native";+export type Address = {+  street: string,+  num: number,+  isInUS: boolean,+};export interface Spec extends TurboModule {  +reverseString: (input: string) => string;+ +validateAddress: (input: Address) => boolean;}export default (TurboModuleRegistry.getEnforcing<Spec>(  "NativeSampleModule"): Spec);
```

This code defines the new `Address` type and defines a new `validateAddress` function for the Turbo Native Module. Notice that the `validateFunction` requires an `Address` object as parameter.

It is also possible to have functions that return custom types.

### 2. Define the bridging code​

From the `Address` type defined in the specs, Codegen will generate two helper types: `NativeSampleModuleAddress` and `NativeSampleModuleAddressBridging`.

The first type is the definition of the `Address`. The second type contains all the infrastructure to bridge the custom type from JS to C++ and vice versa. The only extra step we need to add is to define the `Bridging` structure that extends the `NativeSampleModuleAddressBridging` type.

1. Open the `shared/NativeSampleModule.h` file
2. Add the following code in the file:

 NativeSampleModule.h (Bridging the Address type)

```
#include "Int64.h"#include <memory>#include <string>namespace facebook::react {+  using Address = NativeSampleModuleAddress<std::string, int32_t, bool>;+  template <>+  struct Bridging<Address>+      : NativeSampleModuleAddressBridging<Address> {};  // ...}
```

This code defines an `Address` typealias for the generic type `NativeSampleModuleAddress`. **The order of the generics matters**: the first template argument refers to the first data type of the struct, the second refers to the second, and so forth.

Then, the code adds the `Bridging` specialization for the new `Address` type, by extending `NativeSampleModuleAddressBridging` that is generated by Codegen.

 note

There is a convention that is followed to generate this types:

- The first part of the name is always the type of the module. `NativeSampleModule`, in this example.
- The second part of the name is always the name of the JS type defined in the specs. `Address`, in this example.

### 3. Implement the Native Code​

Now, we need to implement the `validateAddress` function in C++. First, we need to add the function declaration into the `.h` file, and then we can implement it in the `.cpp` file.

1. Open the `shared/NativeSampleModule.h` file and add the function definition

 NativeSampleModule.h (validateAddress function prototype)

```
std::string reverseString(jsi::Runtime& rt, std::string input);+  bool validateAddress(jsi::Runtime &rt, jsi::Object input);};} // namespace facebook::react
```

1. Open the `shared/NativeSampleModule.cpp` file and add the function implementation

 NativeSampleModule.cpp (validateAddress implementation)

```
bool NativeSampleModule::validateAddress(jsi::Runtime &rt, jsi::Object input) {  std::string street = input.getProperty(rt, "street").asString(rt).utf8(rt);  int32_t number = input.getProperty(rt, "num").asNumber();  return !street.empty() && number > 0;}
```

In the implementation, the object that represents the `Address` is a `jsi::Object`. To extract the values from this object, we need to use the accessors provided by `JSI`:

- `getProperty()` retrieves the property from and object by name.
- `asString()` converts the property to `jsi::String`.
- `utf8()` converts the `jsi::String` to a `std::string`.
- `asNumber()` converts the property to a `double`.

Once we manually parsed the object, we can implement the logic that we need.

 note

If you want to learn more about `JSI` and how it works, have a look at this [great talk](https://youtu.be/oLmGInjKU2U?feature=shared) from App.JS 2024

### 4. Testing the code in the app​

To test the code in the app, we have to modify the `App.tsx` file.

1. Open the `App.tsx` file. Remove the content of the `App()` function.
2. Replace the body of the `App()` function with the following code:

 App.tsx (App function body replacement)

```
const [street, setStreet] = React.useState('');const [num, setNum] = React.useState('');const [isValidAddress, setIsValidAddress] = React.useState<  boolean | null>(null);const onPress = () => {  let houseNum = parseInt(num, 10);  if (isNaN(houseNum)) {    houseNum = -1;  }  const address = {    street,    num: houseNum,    isInUS: false,  };  const result = SampleTurboModule.validateAddress(address);  setIsValidAddress(result);};return (  <SafeAreaView style={styles.container}>    <View>      <Text style={styles.title}>        Welcome to C Turbo Native Module Example      </Text>      <Text>Address:</Text>      <TextInput        style={styles.textInput}        placeholder="Write your address here"        onChangeText={setStreet}        value={street}      />      <Text>Number:</Text>      <TextInput        style={styles.textInput}        placeholder="Write your address here"        onChangeText={setNum}        value={num}      />      <Button title="Validate" onPress={onPress} />      {isValidAddress != null && (        <Text>          Your address is {isValidAddress ? 'valid' : 'not valid'}        </Text>      )}    </View>  </SafeAreaView>);
```

Congratulation! 🎉

You bridged your first types from JS to C++.

Is this page useful?

---

# Direct Manipulation

> It is sometimes necessary to make changes directly to a component without using state/props to trigger a re-render of the entire subtree. When using React in the browser for example, you sometimes need to directly modify a DOM node, and the same is true for views in mobile apps. setNativeProps is the React Native equivalent to setting properties directly on a DOM node.

It is sometimes necessary to make changes directly to a component without using state/props to trigger a re-render of the entire subtree. When using React in the browser for example, you sometimes need to directly modify a DOM node, and the same is true for views in mobile apps. `setNativeProps` is the React Native equivalent to setting properties directly on a DOM node.

 caution

Use `setNativeProps` when frequent re-rendering creates a performance bottleneck!

Direct manipulation will not be a tool that you reach for frequently. You will typically only be using it for creating continuous animations to avoid the overhead of rendering the component hierarchy and reconciling many views.
`setNativeProps` is imperative and stores state in the native layer (DOM, UIView, etc.) and not within your React components, which makes your code more difficult to reason about.

Before you use it, try to solve your problem with `setState` and [shouldComponentUpdate](https://react.dev/reference/react/Component#shouldcomponentupdate).

## setNativeProps to edit TextInput value

Another very common use case of `setNativeProps` is to edit the value of the TextInput. The `controlled` prop of TextInput can sometimes drop characters when the `bufferDelay` is low and the user types very quickly. Some developers prefer to skip this prop entirely and instead use `setNativeProps` to directly manipulate the TextInput value when necessary.

For example, the following code demonstrates editing the input when you tap a button:

You can use the [clear](https://reactnative.dev/docs/textinput#clear) method to clear the `TextInput` which clears the current input text using the same approach.

## Avoiding conflicts with the render function​

If you update a property that is also managed by the render function, you might end up with some unpredictable and confusing bugs because anytime the component re-renders and that property changes, whatever value was previously set from `setNativeProps` will be completely ignored and overridden.

Is this page useful?

---

# Measuring the Layout

> Sometimes, you need to measure the current layout to apply some changes to the overall layout or to make decisions and call some specific logic.

Sometimes, you need to measure the current layout to apply some changes to the overall layout or to make decisions and call some specific logic.

React Native provides some native methods to know what are the measurements of the views.

The best way to invoke those methods is in a `useLayoutEffect` hook: this will give you the most recent values for those measurements and it will let you apply changes in the same frame when the measurements are computed.

Typical code will look like this:

 tsx

```
function AComponent(children) {  const targetRef = React.useRef(null)  useLayoutEffect(() => {    targetRef.current?.measure((x, y, width, height, pageX, pageY) => {      //do something with the measurements    });  }, [ /* add dependencies here */]);  return (    <View ref={targetRef}>     {children}    <View />  );}
```

 note

The methods described here are available on most of the default components provided by React Native. However, they are *not* available on composite components that aren't directly backed by a native view. This will generally include most components that you define in your own app.

## measure(callback)​

Determines the location on screen (`x` and `y`), `width`, and `height` in the viewport of the given view. Returns the values via an async callback. If successful, the callback will be called with the following arguments:

- `x`: the `x` coordinate of the origin (top-left corner) of the measured view in the viewport.
- `y`: the `y` coordinate of the origin (top-left corner) of the measured view in the viewport.
- `width`: the `width` of the view.
- `height`: the `height` of the view.
- `pageX`: the `x` coordinate of the view in the viewport (typically the whole screen).
- `pageY`: the `y` coordinate of the view in the viewport (typically the whole screen).

Also the `width` and `height` returned by `measure()` are the `width` and `height` of the component in the viewport.

## measureInWindow(callback)​

Determines the location (`x` and `y`) of the given view in the window and returns the values via an async callback. If the React root view is embedded in another native view, this will give you the absolute coordinates. If successful, the callback will be called with the following arguments:

- `x`: the `x` coordinate of the view in the current window.
- `y`: the `y` coordinate of the view in the current window.
- `width`: the `width` of the view.
- `height`: the `height` of the view.

Is this page useful?
