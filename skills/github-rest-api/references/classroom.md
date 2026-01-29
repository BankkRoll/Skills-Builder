# REST API endpoints for GitHub Classroom

# REST API endpoints for GitHub Classroom

> Use the REST API to interact with GitHub Classroom.

## Get an assignment

Gets a GitHub Classroom assignment. Assignment will only be returned if the current user is an administrator of the GitHub Classroom for the assignment.

### Fine-grained access tokens for "Get an assignment"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token does not require any permissions.

This endpoint can be used without authentication if only public resources are requested.

### Parameters for "Get an assignment"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| assignment_idintegerRequiredThe unique identifier of the classroom assignment. |

### HTTP response status codes for "Get an assignment"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |

### Code samples for "Get an assignment"

#### Request example

get/assignments/{assignment_id}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/assignments/ASSIGNMENT_ID`

Response

-
-

`Status: 200``{
"id": "12,",
"public_repo": "false,",
"title": "Intro to Binaries",
"type": "individual",
"invite_link": "https://classroom.github.com/a/Lx7jiUgx",
"invitations_enabled": "true,",
"slug": "intro-to-binaries",
"students_are_repo_admins": false,
"feedback_pull_requests_enabled": true,
"max_teams": 0,
"max_members": 0,
"editor": "codespaces",
"accepted": 100,
"submitted": 40,
"passing": 10,
"language": "ruby",
"deadline": "2011-01-26T19:06:43Z",
"stater_code_repository": {
"id": 1296269,
"full_name": "octocat/Hello-World",
"html_url": "https://github.com/octocat/Hello-World",
"node_id": "MDEwOlJlcG9zaXRvcnkxMjk2MjY5",
"private": false,
"default_branch": "main"
},
"classroom": {
"id": 1296269,
"name": "Programming Elixir",
"archived": "false,",
"url": "https://classroom.github.com/classrooms/1-programming-elixir"
}
}`

## List accepted assignments for an assignment

Lists any assignment repositories that have been created by students accepting a GitHub Classroom assignment. Accepted assignments will only be returned if the current user is an administrator of the GitHub Classroom for the assignment.

### Fine-grained access tokens for "List accepted assignments for an assignment"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token does not require any permissions.

This endpoint can be used without authentication if only public resources are requested.

### Parameters for "List accepted assignments for an assignment"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| assignment_idintegerRequiredThe unique identifier of the classroom assignment. |

| Name, Type, Description |
| --- |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |

### HTTP response status codes for "List accepted assignments for an assignment"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "List accepted assignments for an assignment"

#### Request example

get/assignments/{assignment_id}/accepted_assignments

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/assignments/ASSIGNMENT_ID/accepted_assignments`

Response

-
-

`Status: 200``{
"id": "12,",
"submitted": "false,",
"passing": "false,",
"commit_count": 5,
"grade": "5/10",
"students": [
{
"id": 1,
"login": "octocat",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"html_url": "https://github.com/octocat"
}
],
"repository": {
"id": 1296269,
"full_name": "octocat/Hello-World",
"html_url": "https://github.com/octocat/Hello-World",
"node_id": "MDEwOlJlcG9zaXRvcnkxMjk2MjY5",
"private": false,
"default_branch": "main"
},
"assignment": {
"id": "12,",
"public_repo": "false,",
"title": "Intro to Binaries",
"type": "individual",
"invite_link": "https://classroom.github.com/a/Lx7jiUgx",
"invitations_enabled": "true,",
"slug": "intro-to-binaries",
"students_are_repo_admins": false,
"feedback_pull_requests_enabled": true,
"max_teams": 0,
"max_members": 0,
"editor": "codespaces",
"accepted": 100,
"submitted": 40,
"passing": 10,
"language": "ruby",
"classroom": {
"id": 1296269,
"name": "Programming Elixir",
"archived": "false,",
"url": "https://classroom.github.com/classrooms/1-programming-elixir"
}
}
}`

## Get assignment grades

Gets grades for a GitHub Classroom assignment. Grades will only be returned if the current user is an administrator of the GitHub Classroom for the assignment.

### Fine-grained access tokens for "Get assignment grades"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token does not require any permissions.

This endpoint can be used without authentication if only public resources are requested.

### Parameters for "Get assignment grades"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| assignment_idintegerRequiredThe unique identifier of the classroom assignment. |

### HTTP response status codes for "Get assignment grades"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |

### Code samples for "Get assignment grades"

#### Request example

get/assignments/{assignment_id}/grades

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/assignments/ASSIGNMENT_ID/grades`

Response

-
-

`Status: 200``[
{
"assignment_name": "Introduction to Strings",
"assignment_url": "https://classroom.github.com/classrooms/1337/assignments/1337",
"starter_code_url": "",
"github_username": "octocat",
"roster_identifier": "octocat@github.com",
"student_repository_name": "intro-to-strings-1337-octocat",
"student_repository_url": "https://github.com/timeforschool/intro-to-strings-1337-octocat",
"submission_timestamp": "2018-11-12 01:02",
"points_awarded": 10,
"points_available": 15,
"group_name": "octocat-and-friends"
},
{
"assignment_name": "Introduction to Strings",
"assignment_url": "https://classroom.github.com/classrooms/1337/assignments/1337",
"starter_code_url": "",
"github_username": "monalisa",
"roster_identifier": "monalisa@github.com",
"student_repository_name": "intro-to-strings-1337-monalisa",
"student_repository_url": "https://github.com/timeforschool/intro-to-strings-1337-monalisa",
"submission_timestamp": "2018-11-12 01:11",
"points_awarded": 15,
"points_available": 15,
"group_name": "monalisa-and-friends"
}
]`

## List classrooms

Lists GitHub Classroom classrooms for the current user. Classrooms will only be returned if the current user is an administrator of one or more GitHub Classrooms.

### Fine-grained access tokens for "List classrooms"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token does not require any permissions.

This endpoint can be used without authentication if only public resources are requested.

### Parameters for "List classrooms"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |

### HTTP response status codes for "List classrooms"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "List classrooms"

#### Request example

get/classrooms

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/classrooms`

Response

-
-

`Status: 200``{
"id": 1296269,
"name": "Programming Elixir",
"archived": "false,",
"url": "https://classroom.github.com/classrooms/1-programming-elixir"
}`

## Get a classroom

Gets a GitHub Classroom classroom for the current user. Classroom will only be returned if the current user is an administrator of the GitHub Classroom.

### Fine-grained access tokens for "Get a classroom"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token does not require any permissions.

This endpoint can be used without authentication if only public resources are requested.

### Parameters for "Get a classroom"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| classroom_idintegerRequiredThe unique identifier of the classroom. |

### HTTP response status codes for "Get a classroom"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |

### Code samples for "Get a classroom"

#### Request example

get/classrooms/{classroom_id}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/classrooms/CLASSROOM_ID`

Response

-
-

`Status: 200``{
"id": 1296269,
"name": "Programming Elixir",
"archived": "false,",
"organization": {
"id": 1,
"login": "programming-elixir",
"node_id": "MDEyOk9yZ2FuaXphdGlvbjE=",
"html_url": "https://github.com/programming-elixir",
"name": "Learn how to build fault tolerant applications",
"avatar_url": "https://avatars.githubusercontent.com/u/9919?v=4"
},
"url": "https://classroom.github.com/classrooms/1-programming-elixir"
}`

## List assignments for a classroom

Lists GitHub Classroom assignments for a classroom. Assignments will only be returned if the current user is an administrator of the GitHub Classroom.

### Fine-grained access tokens for "List assignments for a classroom"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token does not require any permissions.

This endpoint can be used without authentication if only public resources are requested.

### Parameters for "List assignments for a classroom"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| classroom_idintegerRequiredThe unique identifier of the classroom. |

| Name, Type, Description |
| --- |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |

### HTTP response status codes for "List assignments for a classroom"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "List assignments for a classroom"

#### Request example

get/classrooms/{classroom_id}/assignments

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/classrooms/CLASSROOM_ID/assignments`

Response

-
-

`Status: 200``{
"id": "12,",
"public_repo": "false,",
"title": "Intro to Binaries",
"type": "individual",
"invite_link": "https://classroom.github.com/a/Lx7jiUgx",
"invitations_enabled": "true,",
"slug": "intro-to-binaries",
"students_are_repo_admins": false,
"feedback_pull_requests_enabled": true,
"max_teams": 0,
"max_members": 0,
"editor": "codespaces",
"accepted": 100,
"submitted": 40,
"passing": 10,
"language": "ruby",
"deadline": "2020-01-11T11:59:22Z",
"classroom": {
"id": 1296269,
"name": "Programming Elixir",
"archived": "false,",
"url": "https://classroom.github.com/classrooms/1-programming-elixir"
}
}`
