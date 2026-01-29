# REST API endpoints for dependency review and more

# REST API endpoints for dependency review

> Use the REST API to interact with dependency changes.

## About dependency review

You can use the REST API to view dependency changes, and the security impact of these changes, before you add them to your environment. You can view the diff of dependencies between two commits of a repository, including vulnerability data for any version updates with known vulnerabilities. For more information about dependency review, see [About dependency review](https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/about-dependency-review).

---

# REST API endpoints for dependency submission

> Use the REST API to submit dependencies.

## About dependency submissions

You can use the REST API to submit dependencies for a project. This enables you to add dependencies, such as those resolved when software is compiled or built, to GitHub's dependency graph feature, providing a more complete picture of all of your project's dependencies.

The dependency graph shows any dependencies you submit using the API in addition to any dependencies that are identified from manifest or lock files in the repository (for example, a `package-lock.json` file in a JavaScript project). For more information about viewing the dependency graph, see [Exploring the dependencies of a repository](https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/exploring-the-dependencies-of-a-repository#viewing-the-dependency-graph).

Submitted dependencies will receive Dependabot alerts and Dependabot security updates for any known vulnerabilities. You will only get Dependabot alerts for dependencies that are from one of the supported ecosystems for the GitHub Advisory Database. For more information about these ecosystems, see [About the GitHub Advisory database](https://docs.github.com/en/code-security/security-advisories/global-security-advisories/about-the-github-advisory-database#github-reviewed-advisories). For transitive dependencies submitted via the dependency submission API, Dependabot will automatically open pull requests to update the parent dependency, if an update is available.

Submitted dependencies will be shown in dependency review, but are *not* available in your organization's dependency insights.

Note

The dependency review API and the dependency submission API work together. This means that the dependency review API will include dependencies submitted via the dependency submission API.

You can submit dependencies in the form of a snapshot. A snapshot is a set of dependencies associated with a commit SHA and other metadata, that reflects the current state of your repository for a commit. You can choose to use pre-made actions or create your own actions to submit your dependencies in the required format each time your project is built. For more information, see [Using the dependency submission API](https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/using-the-dependency-submission-api).

You can submit multiple sets of dependencies to be included in your dependency graph. The REST API uses the `job.correlator` property and the `detector.name` category of the snapshot to ensure the latest submissions for each workflow get shown. The `correlator` property itself is the primary field you will use to keep independent submissions distinct. An example `correlator` could be a simple combination of two variables available in actions runs: `<GITHUB_WORKFLOW> <GITHUB_JOB>`.

Dependency graph can learn about dependencies in three different ways: static analysis, automatic submission, and manual submission. A repository can have multiple methods configured, which can cause the same package manifest to be scanned multiple times, potentially with different outputs from each scan. Dependency graph uses deduplication logic to parse the outputs, prioritizing the most accurate information for each manifest file.

Dependency graph displays only one instance of each manifest file using the following precedence rules.

1. **User submissions** take the highest priority, because they are usually created during artifact builds they have the most complete information.
  - If there are multiple manual snapshots from different detectors, they are sorted alphabetically by correlator and the first one used.
  - If there are two correlators with the same detector, the resolved dependencies are merged. For more information about correlators and detectors, see [REST API endpoints for dependency submission](https://docs.github.com/en/rest/dependency-graph/dependency-submission).
2. **Automatic submissions** have the second-highest priority since they are also created during artifact builds, but are not submitted by users.
3. **Static analysis results** are used when no other data is available.

---

# REST API endpoints for software bill of materials (SBOM)

> Use the REST API to export the software bill of materials (SBOM) for a repository.

If you have at least read access to the repository, you can export the dependency graph for the repository as an SPDX-compatible, Software Bill of Materials (SBOM), via the GitHub UI or GitHub REST API. For more information, see [Exporting a software bill of materials for your repository](https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/exporting-a-software-bill-of-materials-for-your-repository).

This article gives details about the REST API endpoint.
