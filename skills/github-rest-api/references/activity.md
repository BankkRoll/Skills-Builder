# REST API endpoints for events and more

# REST API endpoints for events

> Use the REST API to interact with GitHub events.

## About GitHub events

GitHub events power the various activity streams on the site.

You can use the REST API to return different types of events triggered by activity on GitHub. For more information about the specific events that you can receive, see [GitHub event types](https://docs.github.com/en/webhooks-and-events/events/github-event-types). Endpoints for repository issues are also available. For more information, see [REST API endpoints for issue events](https://docs.github.com/en/rest/issues/events).

Events are optimized for polling with the "ETag" header. If no new events have been triggered, you will see a "304 Not Modified" response, and your current rate limit will be untouched. There is also an "X-Poll-Interval" header that specifies how often (in seconds) you are allowed to poll. In times of high server load, the time may increase. Please obey the header.

```shell
$ curl -I https://api.github.com/users/tater/events
> HTTP/2 200
> X-Poll-Interval: 60
> ETag: "a18c3bded88eb5dbb5c849a489412bf3"

# The quotes around the ETag value are important
$ curl -I https://api.github.com/users/tater/events \
$    -H 'If-None-Match: "a18c3bded88eb5dbb5c849a489412bf3"'
> HTTP/2 304
> X-Poll-Interval: 60
```

The timeline will include up to 300 events. Only events created within the past 30 days will be included. Events older than 30 days will not be included (even if the total number of events in the timeline is less than 300).

---

# REST API endpoints for feeds

> Use the REST API to interact with GitHub feeds.

## Get feeds

Lists the feeds available to the authenticated user. The response provides a URL for each feed. You can then get a specific feed by sending a request to one of the feed URLs.

- **Timeline**: The GitHub global public timeline
- **User**: The public timeline for any user, using `uri_template`. For more information, see "[Hypermedia](https://docs.github.com/rest/using-the-rest-api/getting-started-with-the-rest-api#hypermedia)."
- **Current user public**: The public timeline for the authenticated user
- **Current user**: The private timeline for the authenticated user
- **Current user actor**: The private timeline for activity created by the authenticated user
- **Current user organizations**: The private timeline for the organizations the authenticated user is a member of.
- **Security advisories**: A collection of public announcements that provide information about security-related vulnerabilities in software on GitHub.

By default, timeline resources are returned in JSON. You can specify the `application/atom+xml` type in the `Accept` header to return timeline resources in Atom format. For more information, see "[Media types](https://docs.github.com/rest/using-the-rest-api/getting-started-with-the-rest-api#media-types)."

Note

Private feeds are only returned when [authenticating via Basic Auth](https://docs.github.com/rest/authentication/authenticating-to-the-rest-api#using-basic-authentication) since current feed URIs use the older, non revocable auth tokens.

### Fine-grained access tokens for "Get feeds"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token does not require any permissions.

### HTTP response status codes for "Get feeds"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "Get feeds"

#### Request example

get/feeds

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/feeds`

Response

-
-

`Status: 200``{
"timeline_url": "https://github.com/timeline",
"user_url": "https://github.com/{user}",
"current_user_public_url": "https://github.com/octocat",
"current_user_url": "https://github.com/octocat.private?token=abc123",
"current_user_actor_url": "https://github.com/octocat.private.actor?token=abc123",
"current_user_organization_url": "",
"current_user_organization_urls": [
"https://github.com/organizations/github/octocat.private.atom?token=abc123"
],
"security_advisories_url": "https://github.com/security-advisories",
"_links": {
"timeline": {
"href": "https://github.com/timeline",
"type": "application/atom+xml"
},
"user": {
"href": "https://github.com/{user}",
"type": "application/atom+xml"
},
"current_user_public": {
"href": "https://github.com/octocat",
"type": "application/atom+xml"
},
"current_user": {
"href": "https://github.com/octocat.private?token=abc123",
"type": "application/atom+xml"
},
"current_user_actor": {
"href": "https://github.com/octocat.private.actor?token=abc123",
"type": "application/atom+xml"
},
"current_user_organization": {
"href": "",
"type": ""
},
"current_user_organizations": [
{
"href": "https://github.com/organizations/github/octocat.private.atom?token=abc123",
"type": "application/atom+xml"
}
],
"security_advisories": {
"href": "https://github.com/security-advisories",
"type": "application/atom+xml"
}
}
}`

---

# REST API endpoints for notifications

> Use the REST API to manage GitHub notifications.

## About GitHub notifications

Note

These endpoints only support authentication using a personal access token (classic). For more information, see [Managing your personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token).

You can use the REST API to manage GitHub notifications. For more information about notifications, see [About notifications](https://docs.github.com/en/account-and-profile/managing-subscriptions-and-notifications-on-github/setting-up-notifications/about-notifications).

All calls to these endpoints require the `notifications` or `repo` scopes. You will need the `repo` scope to access issues and commits from their respective endpoints.

Notifications are returned as "threads". A thread contains information about the current discussion of an issue, pull request, or commit.

Notifications are optimized for polling with the `Last-Modified` header. If there are no new notifications, you will see a `304 Not Modified` response, leaving your current rate limit untouched. There is an `X-Poll-Interval` header that specifies how often (in seconds) you are allowed to poll. In times of high server load, the time may increase. Please obey the header.

```shell
# Add authentication to your requests
$ curl -I https://api.github.com/notifications
HTTP/2 200
Last-Modified: Thu, 25 Oct 2012 15:16:27 GMT
X-Poll-Interval: 60

# Pass the Last-Modified header exactly
$ curl -I https://api.github.com/notifications
$    -H "If-Modified-Since: Thu, 25 Oct 2012 15:16:27 GMT"
> HTTP/2 304
> X-Poll-Interval: 60
```

### About notification reasons

These GET endpoints return a `reason` key. These `reason`s correspond to events that trigger a notification.

There are a few potential `reason`s for receiving a notification.

| Reason Name | Description |
| --- | --- |
| approval_requested | You were requested to review and approve a deployment. For more information, seeReviewing deployments. |
| assign | You were assigned to the issue. |
| author | You created the thread. |
| ci_activity | A GitHub Actions workflow run that you triggered was completed. |
| comment | You commented on the thread. |
| invitation | You accepted an invitation to contribute to the repository. |
| manual | You subscribed to the thread (via an issue or pull request). |
| member_feature_requested | Organization members have requested to enable a feature such as Copilot. |
| mention | You were specifically@mentionedin the content. |
| review_requested | You, or a team you're a member of, were requested to review a pull request. |
| security_advisory_credit | You were credited for contributing to a security advisory. |
| security_alert | GitHub discovered asecurity vulnerabilityin your repository. |
| state_change | You changed the thread state (for example, closing an issue or merging a pull request). |
| subscribed | You're watching the repository. |
| team_mention | You were on a team that was mentioned. |

Note that the `reason` is modified on a per-thread basis, and can change, if the `reason` on a later notification is different.

For example, if you are the author of an issue, subsequent notifications on that issue will have a `reason` of `author`. If you're then **@mentioned** on the same issue, the notifications you fetch thereafter will have a `reason` of `mention`. The `reason` remains as `mention`, regardless of whether you're ever mentioned again.

---

# REST API endpoints for starring

> Use the REST API to bookmark a repository.

## About starring

You can use the REST API to star (bookmark) a repository. Stars are shown next to repositories to show an approximate level of interest. Stars have no effect on notifications or the activity feed. For more information, see [Saving repositories with stars](https://docs.github.com/en/get-started/exploring-projects-on-github/saving-repositories-with-stars).

### Starring versus watching

In August 2012, we [changed the way watching
works](https://github.com/blog/1204-notifications-stars) on GitHub. Some API
client applications may still be using the original "watcher" endpoints for accessing
this data. You should now use the "star" endpoints instead (described
below). For more information, see [REST API endpoints for watching](https://docs.github.com/en/rest/activity/watching) and the [changelog post](https://developer.github.com/changes/2012-09-05-watcher-api/).

In responses from the REST API, `watchers`, `watchers_count`, and `stargazers_count` correspond to the number of users that have starred a repository, whereas `subscribers_count` corresponds to the number of watchers.

---

# REST API endpoints for watching

> Use the REST API to subscribe to notifications for activity in a repository.

## About watching

You can use the REST API to subscribe to notifications for activity in a repository. To bookmark a repository instead, see [REST API endpoints for starring](https://docs.github.com/en/rest/activity/starring).

### Watching versus starring

In August 2012, we [changed the way watching
works](https://github.com/blog/1204-notifications-stars) on GitHub. Some API
client applications may still be using the original "watcher" endpoints for accessing
this data. You should now use the "star" endpoints instead. For more information, [REST API endpoints for starring](https://docs.github.com/en/rest/activity/starring) and the [changelog post](https://developer.github.com/changes/2012-09-05-watcher-api/).

In responses from the REST API, `subscribers_count` corresponds to the number of watchers, whereas `watchers`, `watchers_count`, and `stargazers_count` correspond to the number of users that have starred a repository.
