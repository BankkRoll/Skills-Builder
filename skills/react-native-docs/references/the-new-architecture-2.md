# Cross and more

# Cross

> Writing a module in C++ is the best way to share platform-agnostic code between Android and iOS. With pure C++ modules, you can write your logic only once and reuse it right away from all the platforms, without the need of writing platform-specific code.

Writing a module in C++ is the best way to share platform-agnostic code between Android and iOS. With pure C++ modules, you can write your logic only once and reuse it right away from all the platforms, without the need of writing platform-specific code.

In this guide, we will go through the creation of a pure C++ Turbo Native Module:

1. Create the JS specs
2. Configure Codegen to generate the scaffolding
3. Implement the Native logic
4. Register the module in the Android and iOS application
5. Test your changes in JS

The rest of this guide assumes that you have created your application running the command:

 shell

```
npx @react-native-community/cli@latest init SampleApp --version 0.83
```

## 1. Create the JS specs​

Pure C++ Turbo Native Modules are Turbo Native Modules. They need a specification file (also called spec file) so that Codegen can create the scaffolding code for us. The specification file is also what we use to access the Turbo Native Module in JS.

Spec files need to be written in a typed JS dialect. React Native currently supports Flow or TypeScript.

1. Inside the root folder of your app, create a new folder called `specs`.
2. Create a new file called `NativeSampleModule.ts` with the following code:

 warning

All Native Turbo Module spec files must have the prefix `Native`, otherwise Codegen will ignore them.

specs/NativeSampleModule.ts

```
// @flowimport type {TurboModule} from 'react-native'import { TurboModuleRegistry } from "react-native";export interface Spec extends TurboModule {  +reverseString: (input: string) => string;}export default (TurboModuleRegistry.getEnforcing<Spec>(  "NativeSampleModule"): Spec);
```

specs/NativeSampleModule.ts

```
import {TurboModule, TurboModuleRegistry} from 'react-native';export interface Spec extends TurboModule {  readonly reverseString: (input: string) => string;}export default TurboModuleRegistry.getEnforcing<Spec>(  'NativeSampleModule',);
```

## 2. Configure Codegen​

The next step is to configure [Codegen](https://reactnative.dev/docs/the-new-architecture/what-is-codegen) in your `package.json`. Update the file to include:

 package.json

```
"start": "react-native start",     "test": "jest"   },   "codegenConfig": {     "name": "AppSpecs",     "type": "modules",     "jsSrcsDir": "specs",     "android": {       "javaPackageName": "com.sampleapp.specs"     }   },   "dependencies": {
```

This configuration tells Codegen to look for spec files in the `specs` folder. It also instructs Codegen to only generate code for `modules` and to namespace the generated code as `AppSpecs`.

## 3. Write the Native Code​

Writing a C++ Turbo Native Module allows you to share the code between Android and iOS. Therefore we will be writing the code once, and we will look into what changes we need to apply to the platforms so that the C++ code can be picked up.

1. Create a folder named `shared` at the same level as the `android` and `ios` folders.
2. Inside the `shared` folder, create a new file called `NativeSampleModule.h`.
   shared/NativeSampleModule.h
  ```
  #pragma once#include <AppSpecsJSI.h>#include <memory>#include <string>namespace facebook::react {class NativeSampleModule : public NativeSampleModuleCxxSpec<NativeSampleModule> {public:  NativeSampleModule(std::shared_ptr<CallInvoker> jsInvoker);  std::string reverseString(jsi::Runtime& rt, std::string input);};} // namespace facebook::react
  ```
3. Inside the `shared` folder, create a new file called `NativeSampleModule.cpp`.
   shared/NativeSampleModule.cpp
  ```
  #include "NativeSampleModule.h"namespace facebook::react {NativeSampleModule::NativeSampleModule(std::shared_ptr<CallInvoker> jsInvoker)    : NativeSampleModuleCxxSpec(std::move(jsInvoker)) {}std::string NativeSampleModule::reverseString(jsi::Runtime& rt, std::string input) {  return std::string(input.rbegin(), input.rend());}} // namespace facebook::react
  ```

Let's have a look at the two files we created:

- The `NativeSampleModule.h` file is the header file for a Pure C++ TurboModule. The `include` statements make sure that we include the specs that will be created by Codegen and that contains the interface and the base class we need to implement.
- The module lives in the `facebook::react` namespace to have access to all the types that live in that namespace.
- The class `NativeSampleModule` is the actual Turbo Native Module class and it extends the `NativeSampleModuleCxxSpec` class which contains some glue code and boilerplate code to let this class behave as a Turbo Native Module.
- Finally, we have the constructor, that accepts a pointer to the `CallInvoker`, to communicate with JS if needed and the function's prototype we have to implement.

The `NativeSampleModule.cpp` file is the actual implementation of our Turbo Native Module and implements the constructor and the method that we declared in the specs.

## 4. Register the Module in the platform​

The next steps will let us register the module in the platform. This is the step that exposes the native code to JS so that the React Native application can finally call the native methods from the JS layer.

This is the only time when we will have to write some platform-specific code.

### Android​

To make sure that the Android app can effectively build the C++ Turbo Native Module, we need to:

1. Create a `CMakeLists.txt` to access our C++ code.
2. Modify `build.gradle` to point to the newly created `CMakeLists.txt` file.
3. Create an `OnLoad.cpp` file in our Android app to register the new Turbo Native Module.

#### 1. Create theCMakeLists.txtfile​

Android uses CMake to build. CMake needs to access the files we defined in our shared folder to be able to build them.

1. Create a new folder `SampleApp/android/app/src/main/jni`. The `jni` folder is where the C++ side of Android lives.
2. Create a `CMakeLists.txt` file and add this context:

 CMakeLists.txt

```
cmake_minimum_required(VERSION 3.13)# Define the library name here.project(appmodules)# This file includes all the necessary to let you build your React Native applicationinclude(${REACT_ANDROID_DIR}/cmake-utils/ReactNative-application.cmake)# Define where the additional source code lives. We need to crawl back the jni, main, src, app, android folderstarget_sources(${CMAKE_PROJECT_NAME} PRIVATE ../../../../../shared/NativeSampleModule.cpp)# Define where CMake can find the additional header files. We need to crawl back the jni, main, src, app, android folderstarget_include_directories(${CMAKE_PROJECT_NAME} PUBLIC ../../../../../shared)
```

The CMake file does the following things:

- Defines the `appmodules` library, where all the app C++ code will be included.
- Loads the base React Native's CMake file.
- Adds the Module C++ source code that we need to build with the `target_sources` directives. By default React Native will already populate the `appmodules` library with default sources, here we include our custom one. You can see that we need to crawl back from the `jni` folder to the `shared` folder where our C++ Turbo Module lives.
- Specifies where CMake can find the module header files. Also in this case we need to crawl back from the `jni` folder.

#### 2. Modifybuild.gradleto include the custom C++ code​

Gradle is the tool that orchestrates the Android build. We need to tell it where it can find the `CMake` files to build the Turbo Native Module.

1. Open the `SampleApp/android/app/build.gradle` file.
2. Add the following block into the Gradle file, within the existing `android` block:

 android/app/build.gradle

```
buildTypes {        debug {            signingConfig signingConfigs.debug        }        release {            // Caution! In production, you need to generate your own keystore file.            // see https://reactnative.dev/docs/signed-apk-android.            signingConfig signingConfigs.debug            minifyEnabled enableProguardInReleaseBuilds            proguardFiles getDefaultProguardFile("proguard-android.txt"), "proguard-rules.pro"        }    }+   externalNativeBuild {+       cmake {+           path "src/main/jni/CMakeLists.txt"+       }+   }}
```

This block tells the Gradle file where to look for the CMake file. The path is relative to the folder where the `build.gradle` file lives, so we need to add the path to the `CMakeLists.txt` files in the `jni` folder.

#### 3. Register the new Turbo Native Module​

The final step is to register the new C++ Turbo Native Module in the runtime, so that when JS requires the C++ Turbo Native Module, the app knows where to find it and can return it.

1. From the folder `SampleApp/android/app/src/main/jni`, run the following command:

 shell

```
curl -O https://raw.githubusercontent.com/facebook/react-native/v0.83.0/packages/react-native/ReactAndroid/cmake-utils/default-app-setup/OnLoad.cpp
```

1. Then, modify this file as follows:

 android/app/src/main/jni/OnLoad.cpp

```
#include <DefaultComponentsRegistry.h>#include <DefaultTurboModuleManagerDelegate.h>#include <autolinking.h>#include <fbjni/fbjni.h>#include <react/renderer/componentregistry/ComponentDescriptorProviderRegistry.h>#include <rncore.h>+ // Include the NativeSampleModule header+ #include <NativeSampleModule.h>//...std::shared_ptr<TurboModule> cxxModuleProvider(    const std::string& name,    const std::shared_ptr<CallInvoker>& jsInvoker) {  // Here you can provide your CXX Turbo Modules coming from  // either your application or from external libraries. The approach to follow  // is similar to the following (for a module called `NativeCxxModuleExample`):  //  // if (name == NativeCxxModuleExample::kModuleName) {  //   return std::make_shared<NativeCxxModuleExample>(jsInvoker);  // }+  // This code registers the module so that when the JS side asks for it, the app can return it+  if (name == NativeSampleModule::kModuleName) {+    return std::make_shared<NativeSampleModule>(jsInvoker);+  }  // And we fallback to the CXX module providers autolinked  return autolinking_cxxModuleProvider(name, jsInvoker);}// leave the rest of the file
```

These steps download the original `OnLoad.cpp` file from React Native, so that we can safely override it to load the C++ Turbo Native Module in the app.

Once we downloaded the file, we can modify it by:

- Including the header file that points to our module
- Registering the Turbo Native Module so that when JS requires it, the app can return it.

Now, you can run `yarn android` from the project root to see your app building successfully.

### iOS​

To make sure that the iOS app can effectively build the C++ Turbo Native Module, we need to:

1. Install pods and run Codegen.
2. Add the `shared` folder to our iOS project.
3. Register the C++ Turbo Native Module in the application.

#### 1. Install Pods and Run Codegen.​

The first step we need to run is the usual steps we run every time we have to prepare our iOS application. CocoaPods is the tool we use to setup and install React Native dependencies and, as part of the process, it will also run Codegen for us.

 bash

```
cd iosbundle installbundle exec pod install
```

#### 2. Add the shared folder to the iOS project​

This step adds the `shared` folder to the project to make it visible to Xcode.

1. Open the CocoaPods generated Xcode Workspace.

 bash

```
cd iosopen SampleApp.xcworkspace
```

1. Click on the `SampleApp` project on the left and select `Add files to "Sample App"...`.

![Add Files to Sample App...](https://reactnative.dev/assets/images/AddFilesToXcode1-801bbeb4251cda02929c1863939466c5.png)

1. Select the `shared` folder and click on `Add`.

![Add Files to Sample App...](https://reactnative.dev/assets/images/AddFilesToXcode2-f22d79daca6d0e121ad57c63225e43c6.png)

If you did everything right, your project on the left should look like this:

![Xcode Project](https://reactnative.dev/assets/images/CxxTMGuideXcodeProject-96458e4d285dbdde12b12edaf7193e57.png)

#### 3. Registering the Cxx Turbo Native Module in your app​

To register a pure Cxx Turbo Native Module in your app, you need to:

1. Create a `ModuleProvider` for the Native Module
2. Configure the `package.json` to associate the JS module name with the ModuleProvider class.

The ModuleProvider is an Objective-C++ that glues together the Pure C++ module with the rest of your iOS App.

##### 3.1 Create the ModuleProvider​

1. From Xcode, select the `SampleApp` project and press ⌘ + N to create a new file.
2. Select the `Cocoa Touch Class` template
3. Add the name `NativeSampleModuleProvider` (keep the other field as `Subclass of: NSObject` and `Language: Objective-C`)
4. Click Next to generate the files.
5. Rename the `NativeSampleModuleProvider.m` to `NativeSampleModuleProvider.mm`. The `mm` extension denotes an Objective-C++ file.
6. Implement the content of the `NativeSampleModuleProvider.h` with the following:

 NativeSampleModuleProvider.h

```
#import <Foundation/Foundation.h>#import <ReactCommon/RCTTurboModule.h>NS_ASSUME_NONNULL_BEGIN@interface NativeSampleModuleProvider : NSObject <RCTModuleProvider>@endNS_ASSUME_NONNULL_END
```

This declares a `NativeSampleModuleProvider` object that conforms to the `RCTModuleProvider` protocol.

1. Implement the content of the `NativeSampleModuleProvider.mm` with the following:

 NativeSampleModuleProvider.mm

```
#import "NativeSampleModuleProvider.h"#import <ReactCommon/CallInvoker.h>#import <ReactCommon/TurboModule.h>#import "NativeSampleModule.h"@implementation NativeSampleModuleProvider- (std::shared_ptr<facebook::react::TurboModule>)getTurboModule:    (const facebook::react::ObjCTurboModule::InitParams &)params{  return std::make_shared<facebook::react::NativeSampleModule>(params.jsInvoker);}@end
```

This code implements the `RCTModuleProvider` protocol by creating the pure C++ `NativeSampleModule` when the `getTurboModule:` method is called.

##### 3.2 Update the package.json​

The last step consists in updating the `package.json` to tell React Native about the link between the JS specs of the Native Module and the concrete implementation of those spec in native code.

Modify the `package.json` as it follows:

 package.json

```
"start": "react-native start",     "test": "jest"   },   "codegenConfig": {     "name": "AppSpecs",     "type": "modules",     "jsSrcsDir": "specs",     "android": {       "javaPackageName": "com.sampleapp.specs"     },     "ios": {        "modulesProvider": {          "NativeSampleModule":  "NativeSampleModuleProvider"        }     }   },   "dependencies": {
```

At this point, you need to re-install the pods to make sure that codegen runs again to generate the new files:

 bash

```
# from the ios folderbundle exec pod installopen SampleApp.xcworkspace
```

If you now build your application from Xcode, you should be able to build successfully.

## 5. Testing your Code​

It's now time to access our C++ Turbo Native Module from JS. To do so, we have to modify the `App.tsx` file to import the Turbo Native Module and to call it in our code.

1. Open the `App.tsx` file.
2. Replace the content of the template with the following code:

 App.tsx

```
import React from 'react';import {  Button,  SafeAreaView,  StyleSheet,  Text,  TextInput,  View,} from 'react-native';import SampleTurboModule from './specs/NativeSampleModule';function App(): React.JSX.Element {  const [value, setValue] = React.useState('');  const [reversedValue, setReversedValue] = React.useState('');  const onPress = () => {    const revString = SampleTurboModule.reverseString(value);    setReversedValue(revString);  };  return (    <SafeAreaView style={styles.container}>      <View>        <Text style={styles.title}>          Welcome to C++ Turbo Native Module Example        </Text>        <Text>Write down here the text you want to reverse</Text>        <TextInput          style={styles.textInput}          placeholder="Write your text here"          onChangeText={setValue}          value={value}        />        <Button title="Reverse" onPress={onPress} />        <Text>Reversed text: {reversedValue}</Text>      </View>    </SafeAreaView>  );}const styles = StyleSheet.create({  container: {    flex: 1,    justifyContent: 'center',    alignItems: 'center',  },  title: {    fontSize: 18,    marginBottom: 20,  },  textInput: {    borderColor: 'black',    borderWidth: 1,    borderRadius: 5,    padding: 10,    marginTop: 10,  },});export default App;
```

The interesting lines in this app are:

- `import SampleTurboModule from './specs/NativeSampleModule';`: this line imports the Turbo Native Module in the app,
- `const revString = SampleTurboModule.reverseString(value);` in the `onPress` callback: this is how you can use the Turbo Native Module in your app.

 warning

For the sake of this example and to keep it as short as possible, we directly imported the spec file in our app.
The best practice in this case is to create a separate file to wrap the specs and use that file into your application.
This allows you to prepare the input for the specs and gives you more control over them in JS.

Congratulations, you wrote your first C++ Turbo Native Module!

| Android | iOS |
| --- | --- |
|  |  |

---

# Using Codegen

> This guide teaches how to:

This guide teaches how to:

- Configure **Codegen**.
- Invoke it manually for each platform.

It also describes the generated code.

## Prerequisites​

You always need a React Native app to generate the code properly, even when invoking the **Codegen** manually.

The **Codegen** process is tightly coupled with the build of the app, and the scripts are located in the `react-native` NPM package.

For the sake of this guide, create a project using the React Native CLI as follows:

 shell

```
npx @react-native-community/cli@latest init SampleApp --version 0.83
```

**Codegen** is used to generate the glue-code for your custom modules or components. See the guides for Turbo Native Modules and Fabric Native Components for more details on how to create them.

## ConfiguringCodegen​

**Codegen** can be configured in your app by modifying the `package.json` file. **Codegen** is controlled by a custom field called `codegenConfig`.

 package.json

```
"codegenConfig": {    "name": "<SpecName>",    "type": "<types>",    "jsSrcsDir": "<source_dir>",    "android": {      "javaPackageName": "<java.package.name>"    },    "ios": {      "modules": {        "TestModule": {          "className": "<iOS-class-implementing-the-RCTModuleProvider-protocol>",          "unstableRequiresMainQueueSetup": false,          "conformsToProtocols": ["RCTImageURLLoader", "RCTURLRequestHandler", "RCTImageDataDecoder"],        }      },      "components": {        "TestComponent": {          "className": "<iOS-class-implementing-the-component>"        }      }    }  },
```

You can add this snippet to your app and customize the various fields:

- `name:` Name of the codegen config. This will customize the codegen output: the filenames, and the code.
- `type:`
  - `modules:` Only generate code for modules.
  - `components:` Only generate code for components.
  - `all`: Generate code for everything.
- `jsSrcsDir`: The root folder where all your specs live.
- `android`: Codegen configuration for Android (all optional):
  - `.javaPackageName`: Configure the package name of the Android Java codegen output.
- `ios`: Codegen configuration for iOS (all optional):
  - `.modules[moduleName]:`
    - `.className`: This module's ObjC class. Or, if it's a [C++-only module](https://reactnative.dev/docs/next/the-new-architecture/pure-cxx-modules), its `RCTModuleProvider` class.
    - `.unstableRequiresMainQueueSetup`: Initialize this module on the UI Thread, before running any JavaScript.
    - `.conformsToProtocols`: Annotate which of these protocols this module conforms to any of the following protocols: [RCTImageURLLoader](https://github.com/facebook/react-native/blob/00d5caee9921b6c10be8f7d5b3903c6afe8dbefa/packages/react-native/Libraries/Image/RCTImageURLLoader.h#L26-L81), [RCTURLRequestHandler](https://github.com/facebook/react-native/blob/00d5caee9921b6c10be8f7d5b3903c6afe8dbefa/packages/react-native/React/Base/RCTURLRequestHandler.h#L11-L52), [RCTImageDataDecoder](https://github.com/facebook/react-native/blob/00d5caee9921b6c10be8f7d5b3903c6afe8dbefa/packages/react-native/Libraries/Image/RCTImageDataDecoder.h#L15-L53).
  - `.components[componentName]`:
    - `.className`: This component's ObjC class (e.g: `TextInput` -> `RCTTextInput`).

When **Codegen** runs, it searches among all the dependencies of the app, looking for JS files that respects some specific conventions, and it generates the required code:

- Turbo Native Modules require that the spec files are prefixed with `Native`. For example, `NativeLocalStorage.ts` is a valid name for a spec file.
- Native Fabric Components require that the spec files are suffixed with `NativeComponent`. For example, `WebViewNativeComponent.ts` is a valid name for a spec file.

## RunningCodegen​

The rest of this guide assumes that you have a Native Turbo Module, a Native Fabric Component or both already set up in your project. We also assume that you have valid specification files in the `jsSrcsDir` specified in the `package.json`.

### Android​

**Codegen** for Android is integrated with the React Native Gradle Plugin (RNGP). The RNGP contains a task that can be invoked that reads the configurations defined in the `package.json` file and execute **Codegen**. To run the gradle task, first navigate inside the `android` folder of your project. Then run:

 bash

```
./gradlew generateCodegenArtifactsFromSchema
```

This task invokes the `generateCodegenArtifactsFromSchema` command on all the imported projects of the app (the app and all the node modules which are linked to it). It generates the code in the corresponding `node_modules/<dependency>` folder. For example, if you have a Fabric Native Component whose Node module is called `my-fabric-component`, the generated code is located in the `SampleApp/node_modules/my-fabric-component/android/build/generated/source/codegen` path. For the app, the code is generated in the `android/app/build/generated/source/codegen` folder.

#### The Generated Code​

After running the gradle command above, you will find the codegen code in the `SampleApp/android/app/build` folder. The structure will look like this:

```
build└── generated    └── source        └── codegen            ├── java            │   └── com            │       ├── facebook            │       │   └── react            │       │       └── viewmanagers            │       │           ├── <nativeComponent>ManagerDelegate.java            │       │           └── <nativeComponent>ManagerInterface.java            │       └── sampleapp            │           └── NativeLocalStorageSpec.java            ├── jni            │   ├── <codegenConfig.name>-generated.cpp            │   ├── <codegenConfig.name>.h            │   ├── CMakeLists.txt            │   └── react            │       └── renderer            │           └── components            │               └── <codegenConfig.name>            │                   ├── <codegenConfig.name>JSI-generated.cpp            │                   ├── <codegenConfig.name>.h            │                   ├── ComponentDescriptors.cpp            │                   ├── ComponentDescriptors.h            │                   ├── EventEmitters.cpp            │                   ├── EventEmitters.h            │                   ├── Props.cpp            │                   ├── Props.h            │                   ├── ShadowNodes.cpp            │                   ├── ShadowNodes.h            │                   ├── States.cpp            │                   └── States.h            └── schema.json
```

The generated code is split in two folders:

- `java` which contains the platform specific code
- `jni` which contains the C++ code required to let JS and Java interact correctly.

In the `java` folder, you can find the Fabric Native component generated code in the `com/facebook/viewmanagers` subfolder.

- the `<nativeComponent>ManagerDelegate.java` contains the methods that the `ViewManager` can call on the custom Native Component
- the `<nativeComponent>ManagerInterface.java` contains the interface of the `ViewManager`.

In the folder whose name was set up in the `codegenConfig.android.javaPackageName`, instead, you can find the abstract class that a Turbo Native Module has to implement to carry out its tasks.

In the `jni` folder, finally, there is all the boilerplate code to connect JS to Android.

- `<codegenConfig.name>.h` this contains the interface of your custom C++ Turbo Native Modules.
- `<codegenConfig.name>-generated.cpp` this contains the glue code of your custom C++ Turbo Native Modules.
- `react/renderer/components/<codegenConfig.name>`: this folder contains all the glue-code required by your custom component.

This structure has been generated by using the value `all` for the `codegenConfig.type` field. If you use the value `modules`, expect to see no `react/renderer/components/` folder. If you use the value `components`, expect not to see any of the other files.

### iOS​

**Codegen** for iOS relies on some Node scripts that are invoked during the build process. The scripts are located in the `SampleApp/node_modules/react-native/scripts/` folder.

The main script is the `generate-codegen-artifacts.js` script. To invoke the script, you can run this command from the root folder of your app:

 bash

```
node node_modules/react-native/scripts/generate-codegen-artifacts.jsUsage: generate-codegen-artifacts.js -p [path to app] -t [target platform] -o [output path]Options:      --help            Show help                                      [boolean]      --version         Show version number                            [boolean]  -p, --path            Path to the React Native project root.        [required]  -t, --targetPlatform  Target platform. Supported values: "android", "ios",                        "all".                                        [required]  -o, --outputPath      Path where generated artifacts will be output to.
```

where:

- `--path` is the path to the root folder of your app.
- `--outputPath` is the destination where **Codegen** will write the generated files.
- `--targetPlatform` is the platform you'd like to generate the code for.

#### The Generated Code​

Running the script with these arguments:

 shell

```
node node_modules/react-native/scripts/generate-codegen-artifacts.js \    --path . \    --outputPath ios/ \    --targetPlatform ios
```

Will generate these files in the `ios/build` folder:

```
build└── generated    └── ios        ├── <codegenConfig.name>        │   ├── <codegenConfig.name>-generated.mm        │   └── <codegenConfig.name>.h        ├── <codegenConfig.name>JSI-generated.cpp        ├── <codegenConfig.name>JSI.h        ├── FBReactNativeSpec        │   ├── FBReactNativeSpec-generated.mm        │   └── FBReactNativeSpec.h        ├── FBReactNativeSpecJSI-generated.cpp        ├── FBReactNativeSpecJSI.h        ├── RCTModulesConformingToProtocolsProvider.h        ├── RCTModulesConformingToProtocolsProvider.mm        └── react            └── renderer                └── components                    └── <codegenConfig.name>                        ├── ComponentDescriptors.cpp                        ├── ComponentDescriptors.h                        ├── EventEmitters.cpp                        ├── EventEmitters.h                        ├── Props.cpp                        ├── Props.h                        ├── RCTComponentViewHelpers.h                        ├── ShadowNodes.cpp                        ├── ShadowNodes.h                        ├── States.cpp                        └── States.h
```

Part of these generated files are used by React Native in the Core. Then there is a set of files which contains the same name you specified in the package.json `codegenConfig.name` field.

- `<codegenConfig.name>/<codegenConfig.name>.h`: this contains the interface of your custom iOS Turbo Native Modules.
- `<codegenConfig.name>/<codegenConfig.name>-generated.mm`: this contains the glue code of your custom iOS Turbo Native Modules.
- `<codegenConfig.name>JSI.h`: this contains the interface of your custom C++ Turbo Native Modules.
- `<codegenConfig.name>JSI-generated.h`: this contains the glue code of your custom C++ Turbo Native Modules.
- `react/renderer/components/<codegenConfig.name>`: this folder contains all the glue-code required by your custom component.

This structure has been generated by using the value `all` for the `codegenConfig.type` field. If you use the value `modules`, expect to see no `react/renderer/components/` folder. If you use the value `components`, expect not to see any of the other files.

Is this page useful?

---

# What is Codegen?

> Codegen is a tool to avoid writing a lot of repetitive code. Using Codegen is not mandatory: you can write all the generated code manually. However, Codegen generates scaffolding code that could save you a lot of time.

**Codegen** is a tool to avoid writing a lot of repetitive code. Using Codegen **is not mandatory**: you can write all the generated code manually. However, Codegen generates scaffolding code that could save you a lot of time.

React Native invokes Codegen automatically every time an iOS or Android app is built. Occasionally, you would like to manually run the Codegen scripts to know which types and files are actually generated: this is a common scenario when developing [Turbo Native Modules](https://reactnative.dev/docs/turbo-native-modules-introduction) and Fabric Native Components.

## How Codegen Works​

**Codegen** is a process that is tightly coupled with a React Native app. The Codegen scripts live inside the `react-native` NPM package and the apps call those scripts at build time.

Codegen crawls the folders in your project, starting from a directory you specify in your `package.json`, looking for some specific JS files that contain the specification (or specs) for your custom modules and components. Spec files are JS files written in a typed dialect: React Native currently supports Flow and TypeScript.

Every time Codegen finds a spec file, it generates boilerplate code associated with it. Codegen generates some C++ glue-code and then it generates platform-specific code, using Java for Android and Objective-C++ for iOS.

Is this page useful?
