# REST API endpoints for check runs and more

# REST API endpoints for check runs

> Use the REST API to manage check runs.

Note

Write permission for the REST API to interact with checks is only available to GitHub Apps. OAuth apps and authenticated users can view check runs and check suites, but they are not able to create them. If you aren't building a GitHub App, you might be interested in using the REST API to interact with [commit statuses](https://docs.github.com/en/rest/commits#commit-statuses).

---

# REST API endpoints for check suites

> Use the REST API to manage check suites.

Note

Write permission for the REST API to interact with checks is only available to GitHub Apps. OAuth apps and authenticated users can view check runs and check suites, but they are not able to create them. If you aren't building a GitHub App, you might be interested in using the REST API to interact with [commit statuses](https://docs.github.com/en/rest/commits#commit-statuses).

Note

A GitHub App usually only receives one [check_suite](https://docs.github.com/en/webhooks-and-events/webhooks/webhook-events-and-payloads#check_suite) event per commit SHA, even if you push the commit SHA to more than one branch. To find out when a commit SHA is pushed to a branch, you can subscribe to branch [create](https://docs.github.com/en/webhooks-and-events/webhooks/webhook-events-and-payloads#create) events.
