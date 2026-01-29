# REST API endpoints for codes of conduct

# REST API endpoints for codes of conduct

> Use the REST API to get information about codes of conduct.

## Get all codes of conduct

Returns array of all GitHub's codes of conduct.

### Fine-grained access tokens for "Get all codes of conduct"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token does not require any permissions.

This endpoint can be used without authentication if only public resources are requested.

### HTTP response status codes for "Get all codes of conduct"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 304 | Not modified |

### Code samples for "Get all codes of conduct"

#### Request example

get/codes_of_conduct

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/codes_of_conduct`

Response

-
-

`Status: 200``[
{
"key": "citizen_code_of_conduct",
"name": "Citizen Code of Conduct",
"url": "https://api.github.com/codes_of_conduct/citizen_code_of_conduct",
"html_url": "http://citizencodeofconduct.org/"
},
{
"key": "contributor_covenant",
"name": "Contributor Covenant",
"url": "https://api.github.com/codes_of_conduct/contributor_covenant",
"html_url": "https://www.contributor-covenant.org/version/2/0/code_of_conduct/"
}
]`

## Get a code of conduct

Returns information about the specified GitHub code of conduct.

### Fine-grained access tokens for "Get a code of conduct"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token does not require any permissions.

This endpoint can be used without authentication if only public resources are requested.

### Parameters for "Get a code of conduct"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| keystringRequired |

### HTTP response status codes for "Get a code of conduct"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 304 | Not modified |
| 404 | Resource not found |

### Code samples for "Get a code of conduct"

#### Request example

get/codes_of_conduct/{key}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/codes_of_conduct/KEY`

Response

-
-

`Status: 200``{
"key": "contributor_covenant",
"name": "Contributor Covenant",
"url": "https://api.github.com/codes_of_conduct/contributor_covenant",
"body": "# Contributor Covenant Code of Conduct\n\n## Our Pledge\n\nIn the interest of fostering an open and welcoming environment, we as contributors and maintainers pledge to making participation in our project and our community a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.\n\n## Our Standards\n\nExamples of behavior that contributes to creating a positive environment include:\n\n* Using welcoming and inclusive language\n* Being respectful of differing viewpoints and experiences\n* Gracefully accepting constructive criticism\n* Focusing on what is best for the community\n* Showing empathy towards other community members\n\nExamples of unacceptable behavior by participants include:\n\n* The use of sexualized language or imagery and unwelcome sexual attention or advances\n* Trolling, insulting/derogatory comments, and personal or political attacks\n* Public or private harassment\n* Publishing others' private information, such as a physical or electronic address, without explicit permission\n* Other conduct which could reasonably be considered inappropriate in a professional setting\n\n## Our Responsibilities\n\nProject maintainers are responsible for clarifying the standards of acceptable behavior and are expected to take appropriate and fair corrective action in response\n                  to any instances of unacceptable behavior.\n\nProject maintainers have the right and responsibility to remove, edit, or reject comments, commits, code, wiki edits, issues, and other contributions that are not aligned to this Code of Conduct, or to ban temporarily or permanently any contributor for other behaviors that they deem inappropriate, threatening, offensive, or harmful.\n\n## Scope\n\nThis Code of Conduct applies both within project spaces and in public spaces when an individual is representing the project or its community. Examples of representing a project or community include using an official project e-mail address,\n                  posting via an official social media account, or acting as an appointed representative at an online or offline event. Representation of a project may be further defined and clarified by project maintainers.\n\n## Enforcement\n\nInstances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project team at [EMAIL]. The project team will review and investigate all complaints, and will respond in a way that it deems appropriate to the circumstances. The project team is obligated to maintain confidentiality with regard to the reporter of an incident. Further details of specific enforcement policies may be posted separately.\n\nProject maintainers who do not follow or enforce the Code of Conduct in good faith may face temporary or permanent repercussions as determined by other members of the project's leadership.\n\n## Attribution\n\nThis Code of Conduct is adapted from the [Contributor Covenant](http://contributor-covenant.org), version 1.4, available at [http://contributor-covenant.org/version/1/4](http://contributor-covenant.org/version/1/4/).\n",
"html_url": "http://contributor-covenant.org/version/1/4/"
}`
