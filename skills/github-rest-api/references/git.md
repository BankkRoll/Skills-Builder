# REST API endpoints for Git blobs and more

# REST API endpoints for Git blobs

> Use the REST API to interact with a Git blob (binary large object), the object type used to store the contents of each file in a repository.

## About Git blobs

A Git blob (binary large object) is the object type used to store the contents of each file in a repository. The file's SHA-1 hash is computed and stored in the blob object. These endpoints allow you to read and write [blob objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects)
to your Git database on GitHub. Blobs leverage [these custom media types](#custom-media-types-for-blobs). For more information about the use of media types in the API, see [Getting started with the REST API](https://docs.github.com/en/rest/overview/media-types).

---

# REST API endpoints for Git commits

> Use the REST API to interact with commit objects in your Git database on GitHub.

## About Git commits

A Git commit is a snapshot of the hierarchy ([Git tree](https://docs.github.com/en/rest/git/trees)) and the contents of the files ([Git blob](https://docs.github.com/en/rest/git/blobs)) in a Git repository. These endpoints allow you to read and write [commit objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects#_git_commit_objects) to your Git database on GitHub.

---

# REST API endpoints for Git references

> Use the REST API to interact with references in your Git database on GitHub

## About Git references

A Git reference (`git ref`) is a file that contains a Git commit SHA-1 hash. When referring to a Git commit, you can use the Git reference, which is an easy-to-remember name, rather than the hash. The Git reference can be rewritten to point to a new commit. A branch is a Git reference that stores the new Git commit hash. These endpoints allow you to read and write [references](https://git-scm.com/book/en/v2/Git-Internals-Git-References) to your Git database on GitHub.

---

# REST API endpoints for Git tags

> Use the REST API to interact with tag objects in your Git database on GitHub.

## About Git tags

A Git tag is similar to a [Git reference](https://docs.github.com/en/rest/git/refs), but the Git commit that it points to never changes. Git tags are helpful when you want to point to specific releases. These endpoints allow you to read and write [tag objects](https://git-scm.com/book/en/v2/Git-Internals-Git-References#_tags) to your Git database on GitHub. The API only supports [annotated tag objects](https://git-scm.com/book/en/v2/Git-Internals-Git-References#_tags), not lightweight tags.

---

# REST API endpoints for Git trees

> Use the REST API to interact with tree objects in your Git database on GitHub.

## About Git trees

A Git tree object creates the hierarchy between files in a Git repository. You can use the Git tree object to create the relationship between directories and the files they contain. These endpoints allow you to read and write [tree objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects#_tree_objects) to your Git database on GitHub.
