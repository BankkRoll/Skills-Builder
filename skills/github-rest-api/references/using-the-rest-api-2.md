# GitHub event types

# GitHub event types

> For the GitHub Events API, learn about each event type, the triggering action on GitHub, and each event's unique properties.

The Events API can return different types of events triggered by activity on GitHub. Each event response contains shared properties, but has a unique `payload` object determined by its event type. The [Event object common properties](#event-object-common-properties) describes the properties shared by all events, and each event type describes the `payload` properties that are unique to the specific event.

## Event object common properties

The event objects returned from the Events API endpoints have the same structure.

| Event API attribute name | Type | Description |
| --- | --- | --- |
| id | integer | Unique identifier for the event. |
| type | string | The type of event. Events uses PascalCase for the name. |
| actor | object | The user that triggered the event. |
| actor.id | integer | The unique identifier for the actor. |
| actor.login | string | The username of the actor. |
| actor.display_login | string | The specific display format of the username. |
| actor.gravatar_id | string | The unique identifier of the Gravatar profile for the actor. |
| actor.url | string | The REST API URL used to retrieve the user object, which includes additional user information. |
| actor.avatar_url | string | The URL of the actor's profile image. |
| repo | object | The repository object where the event occurred. |
| repo.id | integer | The unique identifier of the repository. |
| repo.name | string | The name of the repository, which includes the owner and repository name. For example,octocat/hello-worldis the name of thehello-worldrepository owned by theoctocatpersonal account. |
| repo.url | string | The REST API URL used to retrieve the repository object, which includes additional repository information. |
| payload | object | The event payload object is unique to the event type. See the event type below for the event APIpayloadobject. |
| public | boolean | Whether the event is visible to all users. |
| created_at | string | The date and time when the event was triggered. It is formatted according to ISO 8601. |
| org | object | The organization that was chosen by the actor to perform action that triggers the event.The property appears in the event object only if it is applicable. |
| org.id | integer | The unique identifier for the organization. |
| org.login | string | The name of the organization. |
| org.gravatar_id | string | The unique identifier of the Gravatar profile for the organization. |
| org.url | string | The REST API URL used to retrieve the organization object, which includes additional organization information. |
| org.avatar_url | string | The URL of the organization's profile image. |

### Example WatchEvent event object

This example shows the format of the [WatchEvent](#watchevent) response when using the [Events API](https://docs.github.com/en/rest/activity/events).

```http
HTTP/2 200
Link: <https://api.github.com/resource?page=2>; rel="next",
      <https://api.github.com/resource?page=5>; rel="last"
```

```json
[
  {
    "id": "12345",
    "type": "WatchEvent",
    "actor": {
      "id": 1,
      "login": "octocat",
      "display_login": "octocat",
      "gravatar_id": "",
      "url": "https://api.github.com/users/octocat",
      "avatar_url": "https://github.com/images/error/octocat_happy.gif"
    },
    "repo": {
      "id": 3,
      "name": "octocat/Hello-World",
      "url": "https://api.github.com/repos/octocat/Hello-World"
    },
    "payload": {
      "action": "started"
    },
    "public": false,
    "created_at": "2011-09-06T17:26:27Z",
    "org": {
      "id": 1,
      "login": "github",
      "gravatar_id": "",
      "url": "https://api.github.com/orgs/github",
      "avatar_url": "https://github.com/images/error/octocat_happy.gif"
    },
  }
]
```

## CommitCommentEvent

A commit comment is created. The type of activity is specified in the `action` property of the payload object. For more information, see [REST API endpoints for commit comments](https://docs.github.com/en/rest/commits/comments).

The [event object](#event-object-common-properties) includes properties that are common for all events. Each event object includes a `payload` property and the value is unique to each event type. The `payload` object for this event is described below.

### Eventpayloadobject for CommitCommentEvent

| Key | Type | Description |
| --- | --- | --- |
| action | string | The action performed. Can becreated. |
| comment | object | Thecommit commentresource. |

## CreateEvent

A Git branch or tag is created. For more information, see [REST API endpoints for Git database](https://docs.github.com/en/rest/git#create-a-reference).

The [event object](#event-object-common-properties) includes properties that are common for all events. Each event object includes a `payload` property and the value is unique to each event type. The `payload` object for this event is described below.

### Eventpayloadobject for CreateEvent

| Key | Type | Description |
| --- | --- | --- |
| ref | string | Thegit refresource branch, ornullifref_typeisrepository. |
| ref_type | string | The type of Git ref object created in the repository. Can be eitherbranch,tag, orrepository. |
| full_ref | string | The fully-formed ref resource, meaning that for branches the format isrefs/heads/<branch_name>. |
| master_branch | string | The name of the repository's default branch (usuallymain). |
| description | string | The repository's current description. |
| pusher_type | string | Can be eitheruseror a deploy key. |

## DeleteEvent

A Git branch or tag is deleted. For more information, see the [REST API endpoints for Git database](https://docs.github.com/en/rest/git#delete-a-reference) REST API.

The [event object](#event-object-common-properties) includes properties that are common for all events. Each event object includes a `payload` property and the value is unique to each event type. The `payload` object for this event is described below.

### Eventpayloadobject for DeleteEvent

| Key | Type | Description |
| --- | --- | --- |
| ref | string | Thegit refresource branch. |
| ref_type | string | The type of Git ref object deleted in the repository. Can be eitherbranchortag. |
| full_ref | string | The fully-formed ref resource, meaning that for branches the format isrefs/heads/<branch_name>. |
| pusher_type | string | Can be eitheruseror a deploy key. |

## DiscussionEvent

A discussion is created in a repository. For more information, see [GitHub Discussions documentation](https://docs.github.com/en/discussions).

The [event object](#event-object-common-properties) includes properties that are common for all events. Each event object includes a `payload` property and the value is unique to each event type. The `payload` object for this event is described below.

### Eventpayloadobject for DiscussionEvent

| Key | Type | Description |
| --- | --- | --- |
| action | string | The action performed. Can becreated. |
| discussion | object | The discussion that was created. |

## ForkEvent

A user forks a repository. For more information, see [REST API endpoints for repositories](https://docs.github.com/en/rest/repos#forks).

The [event object](#event-object-common-properties) includes properties that are common for all events. Each event object includes a `payload` property and the value is unique to each event type. The `payload` object for this event is described below.

### Eventpayloadobject for ForkEvent

| Key | Type | Description |
| --- | --- | --- |
| action | string | The action performed. Can beforked. |
| forkee | object | The createdrepositoryresource. |

## GollumEvent

A wiki page is created or updated. For more information, see [About wikis](https://docs.github.com/en/communities/documenting-your-project-with-wikis/about-wikis).

The [event object](#event-object-common-properties) includes properties that are common for all events. Each event object includes a `payload` property and the value is unique to each event type. The `payload` object for this event is described below.

### Eventpayloadobject for GollumEvent

| Key | Type | Description |
| --- | --- | --- |
| pages | array | The pages that were updated. |
| pages[][page_name] | string | The name of the page. |
| pages[][title] | string | The current page title. |
| pages[][summary] | string | An optional note about the page. Can benull. |
| pages[][action] | string | The action that was performed on the page. Can becreatedoredited. |
| pages[][sha] | string | The latest commit SHA of the page. |
| pages[][html_url] | string | Points to the HTML wiki page. |

## IssueCommentEvent

Activity related to an issue or pull request comment. The type of activity is specified in the `action` property of the payload object. For more information, see the [REST API endpoints for issues](https://docs.github.com/en/rest/issues#comments).

The [event object](#event-object-common-properties) includes properties that are common for all events. Each event object includes a `payload` property and the value is unique to each event type. The `payload` object for this event is described below.

### Eventpayloadobject for IssueCommentEvent

| Key | Type | Description |
| --- | --- | --- |
| action | string | The action that was performed on the comment. Can becreated. |
| issue | object | Theissuethe comment belongs to. |
| comment | object | Thecommentitself. |

## IssuesEvent

Activity related to an issue. The type of activity is specified in the `action` property of the payload object. For more information, see the [REST API endpoints for issues](https://docs.github.com/en/rest/issues).

The [event object](#event-object-common-properties) includes properties that are common for all events. Each event object includes a `payload` property and the value is unique to each event type. The `payload` object for this event is described below.

### Eventpayloadobject for IssuesEvent

| Key | Type | Description |
| --- | --- | --- |
| action | string | The action that was performed. Can be one ofopened,closed,reopened. |
| issue | object | Theissueitself. |
| assignee | object | The optional user who was assigned or unassigned from the issue. |
| assignees | array | The optional array of assignee objects detailing the assignees on the issue. |
| label | object | The optional label that was added or removed from the issue. |
| labels | array | The optional array of label objects describing the labels on the issue. |

## MemberEvent

Activity related to repository collaborators. The type of activity is specified in the `action` property of the payload object. For more information, see [REST API endpoints for collaborators](https://docs.github.com/en/rest/collaborators/collaborators).

The [event object](#event-object-common-properties) includes properties that are common for all events. Each event object includes a `payload` property and the value is unique to each event type. The `payload` object for this event is described below.

### Eventpayloadobject for MemberEvent

| Key | Type | Description |
| --- | --- | --- |
| action | string | The action that was performed. Can beaddedto indicate a user accepted an invitation to a repository. |
| member | object | Theuserthat was added. |

## PublicEvent

When a private repository is made public.

### Eventpayloadobject for PublicEvent

This event returns an empty `payload` object.

## PullRequestEvent

Activity related to pull requests. The type of activity is specified in the `action` property of the payload object. For more information, see [REST API endpoints for pull requests](https://docs.github.com/en/rest/pulls).

The [event object](#event-object-common-properties) includes properties that are common for all events. Each event object includes a `payload` property and the value is unique to each event type. The `payload` object for this event is described below.

### Eventpayloadobject for PullRequestEvent

| Key | Type | Description |
| --- | --- | --- |
| action | string | The action that was performed. Can be one ofopened,closed,merged,reopened,assigned,unassigned,labeled, orunlabeled. |
| number | integer | The pull request number. |
| pull_request | object | Thepull requestitself. |
| assignee | object | The optional user who was assigned or unassigned from the issue. |
| assignees | array | The optional array of assignee objects detailing the assignees on the issue. |
| label | object | The optional label that was added or removed from the issue if the action waslabeledorunlabeled. |
| labels | array | The optional array of label objects describing the labels on the pull request if the action waslabeledorunlabeled. |

## PullRequestReviewEvent

Activity related to pull request reviews. The type of activity is specified in the `action` property of the payload object. For more information, see [REST API endpoints for pull requests](https://docs.github.com/en/rest/pulls#reviews).

The [event object](#event-object-common-properties) includes properties that are common for all events. Each event object includes a `payload` property and the value is unique to each event type. The `payload` object for this event is described below.

### Eventpayloadobject for PullRequestReviewEvent

| Key | Type | Description |
| --- | --- | --- |
| action | string | The action that was performed. Can becreated,updated, ordismissed. |
| pull_request | object | Thepull requestthe review pertains to. |
| review | object | Thereviewthat was affected. |

## PullRequestReviewCommentEvent

Activity related to pull request review comments in the pull request's unified diff. The type of activity is specified in the `action` property of the payload object. For more information, see [REST API endpoints for pull requests](https://docs.github.com/en/rest/pulls#comments).

The [event object](#event-object-common-properties) includes properties that are common for all events. Each event object includes a `payload` property and the value is unique to each event type. The `payload` object for this event is described below.

### Eventpayloadobject for PullRequestReviewCommentEvent

| Key | Type | Description |
| --- | --- | --- |
| action | string | The action that was performed on the comment. Can becreated. |
| pull_request | object | Thepull requestthe comment belongs to. |
| comment | object | Thecommentitself. |

## PushEvent

One or more commits are pushed to a repository branch or tag.

The [event object](#event-object-common-properties) includes properties that are common for all events. Each event object includes a `payload` property and the value is unique to each event type. The `payload` object for this event is described below.

### Eventpayloadobject for PushEvent

| Key | Type | Description |
| --- | --- | --- |
| repository_id | integer | The unique identifier of the repository where the push occurred. |
| push_id | integer | The unique identifier for the push. |
| ref | string | The fullgit refthat was pushed. Example:refs/heads/main. |
| head | string | The SHA of the most recent commit onrefafter the push. |
| before | string | The SHA of the most recent commit onrefbefore the push. |

## ReleaseEvent

Activity related to a release. The type of activity is specified in the `action` property of the payload object. For more information, see the [REST API endpoints for releases and release assets](https://docs.github.com/en/rest/releases) REST API.

The [event object](#event-object-common-properties) includes properties that are common for all events. Each event object includes a `payload` property and the value is unique to each event type. The `payload` object for this event is described below.

### Eventpayloadobject for ReleaseEvent

| Key | Type | Description |
| --- | --- | --- |
| action | string | The action that was performed. Can bepublished. |
| release | object | Thereleaseobject. |

## WatchEvent

When someone stars a repository. The type of activity is specified in the `action` property of the payload object. For more information, see [REST API endpoints for activity](https://docs.github.com/en/rest/activity#starring).

The [event object](#event-object-common-properties) includes properties that are common for all events. Each event object includes a `payload` property and the value is unique to each event type. The `payload` object for this event is described below.

### Eventpayloadobject for WatchEvent

| Key | Type | Description |
| --- | --- | --- |
| action | string | The action that was performed. Currently, can only bestarted. |
