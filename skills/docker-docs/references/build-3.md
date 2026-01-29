# Remote Bake file definition and more

# Remote Bake file definition

> Build with Bake using a remote file definition using Git or HTTP

# Remote Bake file definition

   Table of contents

---

You can build Bake files directly from a remote Git repository or HTTPS URL:

```console
$ docker buildx bake "https://github.com/docker/cli.git#v20.10.11" --print
#1 [internal] load git source https://github.com/docker/cli.git#v20.10.11
#1 0.745 e8f1871b077b64bcb4a13334b7146492773769f7       refs/tags/v20.10.11
#1 2.022 From https://github.com/docker/cli
#1 2.022  * [new tag]         v20.10.11  -> v20.10.11
#1 DONE 2.9s
```

This fetches the Bake definition from the specified remote location and
executes the groups or targets defined in that file. If the remote Bake
definition doesn't specify a build context, the context is automatically set to
the Git remote. For example, [this case](https://github.com/docker/cli/blob/2776a6d694f988c0c1df61cad4bfac0f54e481c8/docker-bake.hcl#L17-L26)
uses `https://github.com/docker/cli.git`:

```json
{
  "group": {
    "default": {
      "targets": ["binary"]
    }
  },
  "target": {
    "binary": {
      "context": "https://github.com/docker/cli.git#v20.10.11",
      "dockerfile": "Dockerfile",
      "args": {
        "BASE_VARIANT": "alpine",
        "GO_STRIP": "",
        "VERSION": ""
      },
      "target": "binary",
      "platforms": ["local"],
      "output": ["build"]
    }
  }
}
```

## Use the local context with a remote definition

When building with a remote Bake definition, you may want to consume local
files relative to the directory where the Bake command is executed. You can
define contexts as relative to the command context using a `cwd://` prefix.

https://github.com/dvdksn/buildx/blob/bake-remote-example/docker-bake.hcl

```hcl
target "default" {
  context = "cwd://"
  dockerfile-inline = <<EOT
FROM alpine
WORKDIR /src
COPY . .
RUN ls -l && stop
EOT
}
```

```console
$ touch foo bar
$ docker buildx bake "https://github.com/dvdksn/buildx.git#bake-remote-example"
```

```text
...
 > [4/4] RUN ls -l && stop:
#8 0.101 total 0
#8 0.102 -rw-r--r--    1 root     root             0 Jul 27 18:47 bar
#8 0.102 -rw-r--r--    1 root     root             0 Jul 27 18:47 foo
#8 0.102 /bin/sh: stop: not found
```

You can append a path to the `cwd://` prefix if you want to use a specific
local directory as a context. Note that if you do specify a path, it must be
within the working directory where the command gets executed. If you use an
absolute path, or a relative path leading outside of the working directory,
Bake will throw an error.

### Local named contexts

You can also use the `cwd://` prefix to define local directories in the Bake
execution context as named contexts.

The following example defines the `docs` context as `./src/docs/content`,
relative to the current working directory where Bake is run as a named context.

docker-bake.hcl

```hcl
target "default" {
  contexts = {
    docs = "cwd://src/docs/content"
  }
  dockerfile = "Dockerfile"
}
```

By contrast, if you omit the `cwd://` prefix, the path would be resolved
relative to the build context.

## Specify the Bake definition to use

When loading a Bake file from a remote Git repository, if the repository
contains more than one Bake file, you can specify which Bake definition to use
with the `--file` or `-f` flag:

```console
docker buildx bake -f bake.hcl "https://github.com/crazy-max/buildx.git#remote-with-local"
```

```text
...
#4 [2/2] RUN echo "hello world"
#4 0.270 hello world
#4 DONE 0.3s
```

## Combine local and remote Bake definitions

You can also combine remote definitions with local ones using the `cwd://`
prefix with `-f`.

Given the following local Bake definition in the current working directory:

```hcl
# local.hcl
target "default" {
  args = {
    HELLO = "foo"
  }
}
```

The following example uses `-f` to specify two Bake definitions:

- `-f bake.hcl`: this definition is loaded relative to the Git URL.
- `-f cwd://local.hcl`: this definition is loaded relative to the current
  working directory where the Bake command is executed.

```console
docker buildx bake -f bake.hcl -f cwd://local.hcl "https://github.com/crazy-max/buildx.git#remote-with-local" --print
```

```json
{
  "target": {
    "default": {
      "context": "https://github.com/crazy-max/buildx.git#remote-with-local",
      "dockerfile": "Dockerfile",
      "args": {
        "HELLO": "foo"
      },
      "target": "build",
      "output": [
        {
          "type": "cacheonly"
        }
      ]
    }
  }
}
```

One case where combining local and remote Bake definitions becomes necessary is
when you're building with a remote Bake definition in GitHub Actions and want
to use the [metadata-action](https://github.com/docker/metadata-action) to
generate tags, annotations, or labels. The metadata action generates a Bake
file available in the runner's local Bake execution context. To use both the
remote definition and the local "metadata-only" Bake file, specify both files
and use the `cwd://` prefix for the metadata Bake file:

```yml
- name: Build
        uses: docker/bake-action@v6
        with:
          files: |
            ./docker-bake.hcl
            cwd://${{ steps.meta.outputs.bake-file }}
          targets: build
```

## Remote definition in a private repository

If you want to use a remote definition that lives in a private repository,
you may need to specify credentials for Bake to use when fetching the definition.

If you can authenticate to the private repository using the default `SSH_AUTH_SOCK`,
then you don't need to specify any additional authentication parameters for Bake.
Bake automatically uses your default agent socket.

For authentication using an HTTP token, or custom SSH agents,
use the following environment variables to configure Bake's authentication strategy:

- [BUILDX_BAKE_GIT_AUTH_TOKEN](https://docs.docker.com/build/building/variables/#buildx_bake_git_auth_token)
- [BUILDX_BAKE_GIT_AUTH_HEADER](https://docs.docker.com/build/building/variables/#buildx_bake_git_auth_header)
- [BUILDX_BAKE_GIT_SSH](https://docs.docker.com/build/building/variables/#buildx_bake_git_ssh)

---

# Bake standard library functions

# Bake standard library functions

   Table of contents

---

| Name | Description |
| --- | --- |
| absolute | If the given number is negative then returns its positive equivalent, or otherwise returns the given number unchanged. |
| add | Returns the sum of the two given numbers. |
| and | Applies the logical AND operation to the given boolean values. |
| base64decode | Decodes a string containing a base64 sequence. |
| base64encode | Encodes a string to a base64 sequence. |
| basename | Returns the last element of a path. |
| bcrypt | Computes a hash of the given string using the Blowfish cipher. |
| byteslen | Returns the total number of bytes in the given buffer. |
| bytesslice | Extracts a subslice from the given buffer. |
| can | Tries to evaluate the expression given in its first argument. |
| ceil | Returns the smallest whole number that is greater than or equal to the given value. |
| chomp | Removes one or more newline characters from the end of the given string. |
| chunklist | Splits a single list into multiple lists where each has at most the given number of elements. |
| cidrhost | Calculates a full host IP address within a given IP network address prefix. |
| cidrnetmask | Converts an IPv4 address prefix given in CIDR notation into a subnet mask address. |
| cidrsubnet | Calculates a subnet address within a given IP network address prefix. |
| cidrsubnets | Calculates many consecutive subnet addresses at once, rather than just a single subnet extension. |
| coalesce | Returns the first of the given arguments that isn't null, or raises an error if there are no non-null arguments. |
| coalescelist | Returns the first of the given sequences that has a length greater than zero. |
| compact | Removes all empty string elements from the given list of strings. |
| concat | Concatenates together all of the given lists or tuples into a single sequence, preserving the input order. |
| contains | Returns true if the given value is a value in the given list, tuple, or set, or false otherwise. |
| convert | Converts a value to a specified type constraint, using HCL's customdecode extension for type expression support. |
| csvdecode | Parses the given string as Comma Separated Values (as defined by RFC 4180) and returns a map of objects representing the table of data, using the first row as a header row to define the object attributes. |
| dirname | Returns the directory of a path. |
| distinct | Removes any duplicate values from the given list, preserving the order of remaining elements. |
| divide | Divides the first given number by the second. |
| element | Returns the element with the given index from the given list or tuple, applying the modulo operation to the given index if it's greater than the number of elements. |
| equal | Returns true if the two given values are equal, or false otherwise. |
| flatten | Transforms a list, set, or tuple value into a tuple by replacing any given elements that are themselves sequences with a flattened tuple of all of the nested elements concatenated together. |
| floor | Returns the greatest whole number that is less than or equal to the given value. |
| format | Constructs a string by applying formatting verbs to a series of arguments, using a similar syntax to the C function "printf". |
| formatdate | Formats a timestamp given in RFC 3339 syntax into another timestamp in some other machine-oriented time syntax, as described in the format string. |
| formatlist | Constructs a list of strings by applying formatting verbs to a series of arguments, using a similar syntax to the C function "printf". |
| greaterthan | Returns true if and only if the second number is greater than the first. |
| greaterthanorequalto | Returns true if and only if the second number is greater than or equal to the first. |
| hasindex | Returns true if if the given collection can be indexed with the given key without producing an error, or false otherwise. |
| homedir | Returns the current user's home directory. |
| indent | Adds a given number of spaces after each newline character in the given string. |
| index | Returns the element with the given key from the given collection, or raises an error if there is no such element. |
| indexof | Finds the element index for a given value in a list. |
| int | Discards any fractional portion of the given number. |
| join | Concatenates together the elements of all given lists with a delimiter, producing a single string. |
| jsondecode | Parses the given string as JSON and returns a value corresponding to what the JSON document describes. |
| jsonencode | Returns a string containing a JSON representation of the given value. |
| keys | Returns a list of the keys of the given map in lexicographical order. |
| length | Returns the number of elements in the given collection. |
| lessthan | Returns true if and only if the second number is less than the first. |
| lessthanorequalto | Returns true if and only if the second number is less than or equal to the first. |
| log | Returns the logarithm of the given number in the given base. |
| lookup | Returns the value of the element with the given key from the given map, or returns the default value if there is no such element. |
| lower | Returns the given string with all Unicode letters translated to their lowercase equivalents. |
| max | Returns the numerically greatest of all of the given numbers. |
| md5 | Computes the MD5 hash of a given string and encodes it with hexadecimal digits. |
| merge | Merges all of the elements from the given maps into a single map, or the attributes from given objects into a single object. |
| min | Returns the numerically smallest of all of the given numbers. |
| modulo | Divides the first given number by the second and then returns the remainder. |
| multiply | Returns the product of the two given numbers. |
| negate | Multiplies the given number by -1. |
| not | Applies the logical NOT operation to the given boolean value. |
| notequal | Returns false if the two given values are equal, or true otherwise. |
| or | Applies the logical OR operation to the given boolean values. |
| parseint | Parses the given string as a number of the given base, or raises an error if the string contains invalid characters. |
| pow | Returns the given number raised to the given power (exponentiation). |
| range | Returns a list of numbers spread evenly over a particular range. |
| regex | Applies the given regular expression pattern to the given string and returns information about a single match, or raises an error if there is no match. |
| regex_replace | Applies the given regular expression pattern to the given string and replaces all matches with the given replacement string. |
| regexall | Applies the given regular expression pattern to the given string and returns a list of information about all non-overlapping matches, or an empty list if there are no matches. |
| replace | Replaces all instances of the given substring in the given string with the given replacement string. |
| reverse | Returns the given string with all of its Unicode characters in reverse order. |
| reverselist | Returns the given list with its elements in reverse order. |
| rsadecrypt | Decrypts an RSA-encrypted ciphertext. |
| sanitize | Replaces all non-alphanumeric characters with a underscore, leaving only characters that are valid for a Bake target name. |
| semvercmp | Returns true if version satisfies a constraint. |
| sethaselement | Returns true if the given set contains the given element, or false otherwise. |
| setintersection | Returns the intersection of all given sets. |
| setproduct | Calculates the cartesian product of two or more sets. |
| setsubtract | Returns the relative complement of the two given sets. |
| setsymmetricdifference | Returns the symmetric difference of the two given sets. |
| setunion | Returns the union of all given sets. |
| sha1 | Computes the SHA1 hash of a given string and encodes it with hexadecimal digits. |
| sha256 | Computes the SHA256 hash of a given string and encodes it with hexadecimal digits. |
| sha512 | Computes the SHA512 hash of a given string and encodes it with hexadecimal digits. |
| signum | Returns 0 if the given number is zero, 1 if the given number is positive, or -1 if the given number is negative. |
| slice | Extracts a subslice of the given list or tuple value. |
| sort | Applies a lexicographic sort to the elements of the given list. |
| split | Produces a list of one or more strings by splitting the given string at all instances of a given separator substring. |
| strlen | Returns the number of Unicode characters (technically: grapheme clusters) in the given string. |
| substr | Extracts a substring from the given string. |
| subtract | Returns the difference between the two given numbers. |
| timeadd | Adds the duration represented by the given duration string to the given RFC 3339 timestamp string, returning another RFC 3339 timestamp. |
| timestamp | Returns a string representation of the current date and time. |
| title | Replaces one letter after each non-letter and non-digit character with its uppercase equivalent. |
| trim | Removes consecutive sequences of characters in "cutset" from the start and end of the given string. |
| trimprefix | Removes the given prefix from the start of the given string, if present. |
| trimspace | Removes any consecutive space characters (as defined by Unicode) from the start and end of the given string. |
| trimsuffix | Removes the given suffix from the start of the given string, if present. |
| try | Variadic function that tries to evaluate all of is arguments in sequence until one succeeds, in which case it returns that result, or returns an error if none of them succeed. |
| upper | Returns the given string with all Unicode letters translated to their uppercase equivalents. |
| urlencode | Applies URL encoding to a given string. |
| uuidv4 | Generates and returns a Type-4 UUID in the standard hexadecimal string format. |
| uuidv5 | Generates and returns a Type-5 UUID in the standard hexadecimal string format. |
| values | Returns the values of elements of a given map, or the values of attributes of a given object, in lexicographic order by key or attribute name. |
| zipmap | Constructs a map from a list of keys and a corresponding list of values, which must both be of the same length. |

## absolute

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    val = "${absolute(-42)}" # => 42
  }
}
```

## add

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${add(123, 1)}" # => 124
  }
}
```

## and

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${and(true, false)}" # => false
  }
}
```

## base64decode

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    decoded = "${base64decode("SGVsbG8=")}" # => "Hello"
  }
}
```

## base64encode

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    encoded = "${base64encode("Hello")}" # => "SGVsbG8="
  }
}
```

## basename

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    file = "${basename("/usr/local/bin/docker")}" # => "docker"
  }
}
```

## bcrypt

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    hash = "${bcrypt("mypassword")}" # => "$2a$10$..."
  }
}
```

## byteslen

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    length = "${byteslen("Docker")}" # => 6
  }
}
```

## bytesslice

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    part = "${bytesslice("Docker", 0, 3)}" # => "Doc"
  }
}
```

## can

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    safe = "${can(parseint("123", 10))}" # => true
  }
}
```

## ceil

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    rounded = "${ceil(3.14)}" # => 4"
  }
}
```

## chomp

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${chomp("Hello\n\n")}" # => "Hello"
  }
}
```

## chunklist

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${chunklist([1,2,3,4,5], 2)}"     # => [[1,2],[3,4],[5]]
  }
}
```

## cidrhost

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${cidrhost("10.0.0.0/16", 5)}"   # => "10.0.0.5"
  }
}
```

## cidrnetmask

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    mask = "${cidrnetmask("10.0.0.0/16")}"     # => "255.255.0.0"
  }
}
```

## cidrsubnet

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    subnet = "${cidrsubnet("10.0.0.0/16", 4, 2)}" # => "10.0.32.0/20"
  }
}
```

## cidrsubnets

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    subs = "${cidrsubnets("10.0.0.0/16", 4, 4)}" # => ["10.0.0.0/20","10.0.16.0/20",...]
  }
}
```

## coalesce

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    first = "${coalesce(null, "", "docker")}"  # => "docker"
  }
}
```

## coalescelist

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    first = "${coalescelist([], [1,2], [3])}" # => [1,2]
  }
}
```

## compact

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    list = "${compact(["a", "", "b", ""])}" # => ["a","b"]
  }
}
```

## concat

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    list = "${concat([1,2],[3,4])}" # => [1,2,3,4]
  }
}
```

## contains

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    check = "${contains([1,2,3], 2)}" # => true
  }
}
```

## convert

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${convert("42", number)}" # => 42
  }
}
```

## csvdecode

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    data = "${csvdecode("name,age\nAlice,30\nBob,40")}" # => [{"name":"Alice","age":"30"},{"name":"Bob","age":"40"}]
  }
}
```

## dirname

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    dir = "${dirname("/usr/local/bin/docker")}" # => "/usr/local/bin"
  }
}
```

## distinct

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${distinct([1,2,2,3,3,3])}" # => [1,2,3]
  }
}
```

## divide

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${divide(10, 2)}" # => 5
  }
}
```

## element

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    val = "${element(["a","b","c"], 1)}" # => "b"
  }
}
```

## equal

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    check = "${equal(2, 2)}" # => true
  }
}
```

## flatten

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    flat = "${flatten([[1,2],[3,4],[5]])}" # => [1,2,3,4,5]
  }
}
```

## floor

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${floor(3.99)}" # => 3
  }
}
```

## format

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${format("Hello, %s!", "World")}" # => "Hello, World!"
  }
}
```

## formatdate

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    date = "${formatdate("YYYY-MM-DD", "2025-09-16T12:00:00Z")}" # => "2025-09-16"
  }
}
```

## formatlist

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    list = "${formatlist("Hi %s", ["Alice", "Bob"])}" # => ["Hi Alice","Hi Bob"]
  }
}
```

## greaterthan

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${greaterthan(2, 5)}" # => true
  }
}
```

## greaterthanorequalto

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${greaterthanorequalto(5, 5)}" # => true
  }
}
```

## hasindex

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    exists = "${hasindex([10, 20, 30], 1)}"  # => true
    missing = "${hasindex([10, 20, 30], 5)}" # => false
  }
}
```

## homedir

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    home = "${homedir()}" # => e.g., "/home/user"
  }
}
```

## indent

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    text = "${indent(4, "Hello\nWorld")}"
    # => "    Hello\n    World"
  }
}
```

## index

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    val = "${index({foo = "bar", baz = "qux"}, "baz")}" # => "qux"
  }
}
```

## indexof

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    pos = "${indexof(["a","b","c"], "b")}" # => 1
  }
}
```

## int

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    number = "${int(3.75)}" # => 3
  }
}
```

## join

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    csv = "${join(",", ["a","b","c"])}" # => "a,b,c"
  }
}
```

## jsondecode

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    obj = "${jsondecode("{\"name\":\"Docker\",\"stars\":5}")}" # => {"name":"Docker","stars":5}
  }
}
```

## jsonencode

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    str = "${jsonencode({name="Docker", stars=5})}" # => "{\"name\":\"Docker\",\"stars\":5}"
  }
}
```

## keys

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    list = "${keys({foo = 1, bar = 2, baz = 3})}"
    # => ["bar","baz","foo"] (sorted order)
  }
}
```

## length

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    size = "${length([1,2,3,4])}" # => 4
  }
}
```

## lessthan

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${lessthan(10, 3)}" # => false
  }
}
```

## lessthanorequalto

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${lessthanorequalto(5, 7)}" # => true
  }
}
```

## log

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    val = "${log(100, 10)}" # => 2
  }
}
```

## lookup

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    found    = "${lookup({a="apple", b="banana"}, "a", "none")}" # => "apple"
    fallback = "${lookup({a="apple", b="banana"}, "c", "none")}" # => "none"
  }
}
```

## lower

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    val = "${lower("HELLO")}" # => "hello"
  }
}
```

## max

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${max(3, 9, 7)}" # => 9
  }
}
```

## md5

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    hash = "${md5("docker")}" # => "597dd5f6a..." (hex string)
  }
}
```

## merge

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    combined = "${merge({a=1, b=2}, {b=3, c=4})}" # => {a=1, b=3, c=4}
  }
}
```

## min

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${min(3, 9, 7)}" # => 3
  }
}
```

## modulo

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${modulo(10, 3)}" # => 1
  }
}
```

## multiply

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${multiply(6, 7)}" # => 42
  }
}
```

## negate

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${negate(7)}" # => -7
  }
}
```

## not

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${not(true)}" # => false
  }
}
```

## notequal

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${notequal(4, 5)}" # => true
  }
}
```

## or

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${or(true, false)}" # => true
  }
}
```

## parseint

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${parseint("ff", 16)}" # => 255
  }
}
```

## pow

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${pow(3, 2)}" # => 9
  }
}
```

## range

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${range(0, 5)}" # => [0,1,2,3,4]
  }
}
```

## regex

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${regex("h.llo", "hello")}" # => "hello"
  }
}
```

## regex_replace

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${regex_replace("[0-9]+", "abc123xyz", "NUM")}" # => "abcNUMxyz"
  }
}
```

## regexall

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = matches = "${regexall("[a-z]+", "abc123xyz")}" # => ["abc","xyz"]
  }
}
```

## replace

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${replace("banana", "na", "--")}" # => "ba-- --"
  }
}
```

## reverse

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${reverse("stressed")}" # => "desserts"
  }
}
```

## reverselist

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${reverselist([1,2,3])}" # => [3,2,1]
  }
}
```

## rsadecrypt

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${rsadecrypt("eczGaDhXDbOFRZ...", "MIIEowIBAAKCAQEAgUElV5...")}"
  }
}
```

## sanitize

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${sanitize("My App! v1.0")}" # => "My_App__v1_0"
  }
}
```

## semvercmp

This function checks if a semantic version fits within a set of constraints.
See [Checking Version Constraints](https://github.com/Masterminds/semver?tab=readme-ov-file#checking-version-constraints)
for details.

```hcl
# docker-bake.hcl
variable "ALPINE_VERSION" {
  default = "3.23"
}

target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  platforms = semvercmp(ALPINE_VERSION, ">= 3.20") ? [
    "linux/amd64",
    "linux/arm64",
    "linux/riscv64"
  ] : [
    "linux/amd64",
    "linux/arm64"
  ]
}
```

## sethaselement

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${sethaselement([1,2,3], 2)}"  # => true
  }
}
```

## setintersection

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${setintersection(["a","b","c"], ["b","c","d"])}" # => ["b","c"]
  }
}
```

## setproduct

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${setproduct(["x","y"], [1,2])}" # => [["x",1],["x",2],["y",1],["y",2]]
  }
}
```

## setsubtract

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${setsubtract([1,2,3], [2])}" # => [1,3]
  }
}
```

## setsymmetricdifference

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${setsymmetricdifference([1,2,3], [3,4])}" # => [1,2,4]
  }
}
```

## setunion

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${setunion(["a","b"], ["b","c"])}" # => ["a","b","c"]
  }
}
```

## sha1

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${sha1("hello")}" # => "aaf4c61d..." (hex)
  }
}
```

## sha256

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${sha256("hello")}" # => "2cf24dba..." (hex)
  }
}
```

## sha512

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${sha512("hello")}" # => "9b71d224..." (hex)
  }
}
```

## signum

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    zero = "${signum(0)}"    # => 0
    pos  = "${signum(12)}"   # => 1
    neg  = "${signum(-12)}"  # => -1
  }
}
```

## slice

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${slice(["a","b","c","d"], 1, 3)}" # => ["b","c"]
  }
}
```

## sort

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${sort(["b","c","a"])}" # => ["a","b","c"]
  }
}
```

## split

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${split(",", "a,b,c")}" # => ["a","b","c"]
  }
}
```

## strlen

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${strlen("Docker")}" # => 6
  }
}
```

## substr

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${substr("abcdef", 2, 3)}" # => "cde"
  }
}
```

## subtract

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${subtract(10, 3)}" # => 7
  }
}
```

## timeadd

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${timeadd("2025-09-24T12:00:00Z", "1h30m")}" # => "2025-09-24T13:30:00Z"
  }
}
```

## timestamp

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${timestamp()}" # => current RFC3339 time at evaluation
  }
}
```

## title

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${title("hello world-from_docker")}" # => "Hello World-From_Docker"
  }
}
```

## trim

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${trim("--hello--", "-")}" # => "hello"
  }
}
```

## trimprefix

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${trimprefix("docker-build", "docker-")}" # => "build"
  }
}
```

## trimspace

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${trimspace("   hello   ")}" # => "hello"
  }
}
```

## trimsuffix

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${trimsuffix("filename.txt", ".txt")}" # => "filename"
  }
}
```

## try

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    # First expr errors (invalid hex), second succeeds → returns 255
    val1 = "${try(parseint("zz", 16), parseint("ff", 16))}" # => 255

    # First expr errors (missing key), fallback string is used
    val2 = "${try(index({a="apple"}, "b"), "fallback")}"    # => "fallback"
  }
}
```

## upper

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    result = "${upper("hello")}" # => "HELLO"
  }
}
```

## urlencode

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    url = "${urlencode("a b=c&d")}" # => "a+b%3Dc%26d"
  }
}
```

## uuidv4

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    id = "${uuidv4()}" # => random v4 UUID each evaluation
  }
}
```

## uuidv5

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    # Uses the DNS namespace UUID per RFC 4122
    # "6ba7b810-9dad-11d1-80b4-00c04fd430c8"
    id = "${uuidv5("6ba7b810-9dad-11d1-80b4-00c04fd430c8", "example.com")}"
    # => always "9073926b-929f-31c2-abc9-fad77ae3e8eb" for "example.com"
  }
}
```

## values

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    vals = "${values({a=1, c=3, b=2})}" # => [1,2,3] (ordered by key: a,b,c)
  }
}
```

## zipmap

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    obj = "${zipmap(["name","stars"], ["Docker", 5])}" # => {name="Docker", stars=5}
  }
}
```
