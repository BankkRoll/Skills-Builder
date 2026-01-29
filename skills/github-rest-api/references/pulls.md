# REST API endpoints for pull request review comments and more

# REST API endpoints for pull request review comments

> Use the REST API to interact with pull request review comments.

## About pull request review comments

Pull request review comments are comments made on a portion of the unified diff during a pull request review. These are different from commit comments and issue comments in a pull request. For more information, see [REST API endpoints for commit comments](https://docs.github.com/en/rest/commits/comments) and [REST API endpoints for issue comments](https://docs.github.com/en/rest/issues/comments).

---

# REST API endpoints for pull requests

> Use the REST API to interact with pull requests.

## About pull requests

You can list, view, edit, create, and merge pull requests using the REST API. For information about how to interact with comments on a pull request, see [REST API endpoints for issue comments](https://docs.github.com/en/rest/issues/comments).

Pull requests are a type of issue. Any actions that are available in both pull requests and issues, like managing assignees, labels, and milestones, are handled by the REST API to manage issues. To perform these actions on pull requests, you must use the issues API endpoints (for example, `/repos/{owner}/{repo}/issues/{issue_number}`), not the pull requests endpoints. For more information, see [REST API endpoints for issues](https://docs.github.com/en/rest/issues).

### Link Relations

Pull requests have these possible link relations:

- `self`: The API location of this pull request
- `html`: The HTML location of this pull request
- `issue`: The API location of this pull request's [issue](https://docs.github.com/en/rest/issues)
- `comments`: The API location of this pull request's [issue comments](https://docs.github.com/en/rest/issues/comments)
- `review_comments`: The API location of this pull request's [review comments](https://docs.github.com/en/rest/pulls/comments)
- `review_comment`: The [URL template](https://docs.github.com/en/rest/using-the-rest-api/getting-started-with-the-rest-api#hypermedia) to construct the API location for a [review comment](https://docs.github.com/en/rest/pulls/comments) in this pull request's repository
- `commits`: The API location of this pull request's [commits](#list-commits-on-a-pull-request)
- `statuses`: The API location of this pull request's [commit statuses](https://docs.github.com/en/rest/commits#commit-statuses), which are the statuses of its `head` branch

---

# REST API endpoints for review requests

> Use the REST API to interact with review requests.

## About review requests

Pull request authors and repository owners and collaborators can request a pull request review from anyone with write access to the repository. Each requested reviewer will receive a notification asking them to review the pull request.

---

# REST API endpoints for pull request reviews

> Use the REST API to interact with pull request reviews.

## About pull request reviews

Pull Request Reviews are groups of pull request review comments on a pull request, grouped together with a state and optional body comment.
