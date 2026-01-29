# REST API endpoints for rules

# REST API endpoints for rules

> Use the REST API to manage rulesets for repositories. Rulesets control how people can interact with selected branches and tags in a repository.

## Get rules for a branch

Returns all active rules that apply to the specified branch. The branch does not need to exist; rules that would apply
to a branch with that name will be returned. All active rules that apply will be returned, regardless of the level
at which they are configured (e.g. repository or organization). Rules in rulesets with "evaluate" or "disabled"
enforcement statuses are not returned.

### Fine-grained access tokens for "Get rules for a branch"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Metadata" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "Get rules for a branch"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| branchstringRequiredThe name of the branch. Cannot contain wildcard characters. To use wildcard characters in branch names, usethe GraphQL API. |

| Name, Type, Description |
| --- |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |

### HTTP response status codes for "Get rules for a branch"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "Get rules for a branch"

#### Request example

get/repos/{owner}/{repo}/rules/branches/{branch}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/rules/branches/BRANCH`

Response

-
-

`Status: 200``[
{
"type": "commit_message_pattern",
"ruleset_source_type": "Repository",
"ruleset_source": "monalisa/my-repo",
"ruleset_id": 42,
"parameters": {
"operator": "starts_with",
"pattern": "issue"
}
},
{
"type": "commit_author_email_pattern",
"ruleset_source_type": "Organization",
"ruleset_source": "my-org",
"ruleset_id": 73,
"parameters": {
"operator": "contains",
"pattern": "github"
}
}
]`

## Get all repository rulesets

Get all the rulesets for a repository.

### Fine-grained access tokens for "Get all repository rulesets"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Metadata" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "Get all repository rulesets"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |
| includes_parentsbooleanInclude rulesets configured at higher levels that apply to this repositoryDefault:true |
| targetsstringA comma-separated list of rule targets to filter by.
If provided, only rulesets that apply to the specified targets will be returned.
For example,branch,tag,push. |

### HTTP response status codes for "Get all repository rulesets"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |
| 500 | Internal Error |

### Code samples for "Get all repository rulesets"

#### Request example

get/repos/{owner}/{repo}/rulesets

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/rulesets`

Response

-
-

`Status: 200``[
{
"id": 42,
"name": "super cool ruleset",
"source_type": "Repository",
"source": "monalisa/my-repo",
"enforcement": "enabled",
"node_id": "RRS_lACkVXNlcgQB",
"_links": {
"self": {
"href": "https://api.github.com/repos/monalisa/my-repo/rulesets/42"
},
"html": {
"href": "https://github.com/monalisa/my-repo/rules/42"
}
},
"created_at": "2023-07-15T08:43:03Z",
"updated_at": "2023-08-23T16:29:47Z"
},
{
"id": 314,
"name": "Another ruleset",
"source_type": "Repository",
"source": "monalisa/my-repo",
"enforcement": "enabled",
"node_id": "RRS_lACkVXNlcgQQ",
"_links": {
"self": {
"href": "https://api.github.com/repos/monalisa/my-repo/rulesets/314"
},
"html": {
"href": "https://github.com/monalisa/my-repo/rules/314"
}
},
"created_at": "2023-08-15T08:43:03Z",
"updated_at": "2023-09-23T16:29:47Z"
}
]`

## Create a repository ruleset

Create a ruleset for a repository.

### Fine-grained access tokens for "Create a repository ruleset"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Create a repository ruleset"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |

| Name, Type, Description |
| --- |
| namestringRequiredThe name of the ruleset. |
| targetstringThe target of the rulesetDefault:branchCan be one of:branch,tag,push |
| enforcementstringRequiredThe enforcement level of the ruleset.evaluateallows admins to test rules before enforcing them. Admins can view insights on the Rule Insights page (evaluateis only available with GitHub Enterprise).Can be one of:disabled,active,evaluate |
| bypass_actorsarray of objectsThe actors that can bypass the rules in this ruleset |
| Name, Type, Descriptionactor_idinteger or nullThe ID of the actor that can bypass a ruleset. Required forIntegration,RepositoryRole, andTeamactor types. Ifactor_typeisOrganizationAdmin,actor_idis ignored. Ifactor_typeisDeployKey, this should be null.OrganizationAdminis not applicable for personal repositories.actor_typestringRequiredThe type of actor that can bypass a ruleset.Can be one of:Integration,OrganizationAdmin,RepositoryRole,Team,DeployKeybypass_modestringWhen the specified actor can bypass the ruleset.pull_requestmeans that an actor can only bypass rules on pull requests.pull_requestis not applicable for theDeployKeyactor type. Also,pull_requestis only applicable to branch rulesets. Whenbypass_modeisexempt, rules will not be run for that actor and a bypass audit entry will not be created.Default:alwaysCan be one of:always,pull_request,exempt |
| Name, Type, Description |
| actor_idinteger or nullThe ID of the actor that can bypass a ruleset. Required forIntegration,RepositoryRole, andTeamactor types. Ifactor_typeisOrganizationAdmin,actor_idis ignored. Ifactor_typeisDeployKey, this should be null.OrganizationAdminis not applicable for personal repositories. |
| actor_typestringRequiredThe type of actor that can bypass a ruleset.Can be one of:Integration,OrganizationAdmin,RepositoryRole,Team,DeployKey |
| bypass_modestringWhen the specified actor can bypass the ruleset.pull_requestmeans that an actor can only bypass rules on pull requests.pull_requestis not applicable for theDeployKeyactor type. Also,pull_requestis only applicable to branch rulesets. Whenbypass_modeisexempt, rules will not be run for that actor and a bypass audit entry will not be created.Default:alwaysCan be one of:always,pull_request,exempt |
| conditionsobjectParameters for a repository ruleset ref name condition |
| Name, Type, Descriptionref_nameobjectName, Type, Descriptionincludearray of stringsArray of ref names or patterns to include. One of these patterns must match for the condition to pass. Also accepts~DEFAULT_BRANCHto include the default branch or~ALLto include all branches.excludearray of stringsArray of ref names or patterns to exclude. The condition will not pass if any of these patterns match. |
| Name, Type, Description |
| ref_nameobject |
| Name, Type, Descriptionincludearray of stringsArray of ref names or patterns to include. One of these patterns must match for the condition to pass. Also accepts~DEFAULT_BRANCHto include the default branch or~ALLto include all branches.excludearray of stringsArray of ref names or patterns to exclude. The condition will not pass if any of these patterns match. |
| Name, Type, Description |
| includearray of stringsArray of ref names or patterns to include. One of these patterns must match for the condition to pass. Also accepts~DEFAULT_BRANCHto include the default branch or~ALLto include all branches. |
| excludearray of stringsArray of ref names or patterns to exclude. The condition will not pass if any of these patterns match. |
| rulesarray of objectsAn array of rules within the ruleset. |
| Name, Type, DescriptioncreationobjectOnly allow users with bypass permission to create matching refs.Name, Type, DescriptiontypestringRequiredValue:creationupdateobjectOnly allow users with bypass permission to update matching refs.Name, Type, DescriptiontypestringRequiredValue:updateparametersobjectName, Type, Descriptionupdate_allows_fetch_and_mergebooleanRequiredBranch can pull changes from its upstream repositorydeletionobjectOnly allow users with bypass permissions to delete matching refs.Name, Type, DescriptiontypestringRequiredValue:deletionrequired_linear_historyobjectPrevent merge commits from being pushed to matching refs.Name, Type, DescriptiontypestringRequiredValue:required_linear_historymerge_queueobjectMerges must be performed via a merge queue.Name, Type, DescriptiontypestringRequiredValue:merge_queueparametersobjectName, Type, Descriptioncheck_response_timeout_minutesintegerRequiredMaximum time for a required status check to report a conclusion. After this much time has elapsed, checks that have not reported a conclusion will be assumed to have failedgrouping_strategystringRequiredWhen set to ALLGREEN, the merge commit created by merge queue for each PR in the group must pass all required checks to merge. When set to HEADGREEN, only the commit at the head of the merge group, i.e. the commit containing changes from all of the PRs in the group, must pass its required checks to merge.Can be one of:ALLGREEN,HEADGREENmax_entries_to_buildintegerRequiredLimit the number of queued pull requests requesting checks and workflow runs at the same time.max_entries_to_mergeintegerRequiredThe maximum number of PRs that will be merged together in a group.merge_methodstringRequiredMethod to use when merging changes from queued pull requests.Can be one of:MERGE,SQUASH,REBASEmin_entries_to_mergeintegerRequiredThe minimum number of PRs that will be merged together in a group.min_entries_to_merge_wait_minutesintegerRequiredThe time merge queue should wait after the first PR is added to the queue for the minimum group size to be met. After this time has elapsed, the minimum group size will be ignored and a smaller group will be merged.required_deploymentsobjectChoose which environments must be successfully deployed to before refs can be pushed into a ref that matches this rule.Name, Type, DescriptiontypestringRequiredValue:required_deploymentsparametersobjectName, Type, Descriptionrequired_deployment_environmentsarray of stringsRequiredThe environments that must be successfully deployed to before branches can be merged.required_signaturesobjectCommits pushed to matching refs must have verified signatures.Name, Type, DescriptiontypestringRequiredValue:required_signaturespull_requestobjectRequire all commits be made to a non-target branch and submitted via a pull request before they can be merged.Name, Type, DescriptiontypestringRequiredValue:pull_requestparametersobjectName, Type, Descriptionallowed_merge_methodsarray of stringsArray of allowed merge methods. Allowed values includemerge,squash, andrebase. At least one option must be enabled.
Supported values are:merge,squash,rebasedismiss_stale_reviews_on_pushbooleanRequiredNew, reviewable commits pushed will dismiss previous pull request review approvals.require_code_owner_reviewbooleanRequiredRequire an approving review in pull requests that modify files that have a designated code owner.require_last_push_approvalbooleanRequiredWhether the most recent reviewable push must be approved by someone other than the person who pushed it.required_approving_review_countintegerRequiredThe number of approving reviews that are required before a pull request can be merged.required_review_thread_resolutionbooleanRequiredAll conversations on code must be resolved before a pull request can be merged.required_reviewersarray of objectsNoterequired_reviewersis in beta and subject to change.A collection of reviewers and associated file patterns. Each reviewer has a list of file patterns which determine the files that reviewer is required to review.Name, Type, Descriptionfile_patternsarray of stringsRequiredArray of file patterns. Pull requests which change matching files must be approved by the specified team. File patterns use fnmatch syntax.minimum_approvalsintegerRequiredMinimum number of approvals required from the specified team. If set to zero, the team will be added to the pull request but approval is optional.reviewerobjectRequiredA required reviewing teamName, Type, DescriptionidintegerRequiredID of the reviewer which must review changes to matching files.typestringRequiredThe type of the reviewerValue:Teamrequired_status_checksobjectChoose which status checks must pass before the ref is updated. When enabled, commits must first be pushed to another ref where the checks pass.Name, Type, DescriptiontypestringRequiredValue:required_status_checksparametersobjectName, Type, Descriptiondo_not_enforce_on_createbooleanAllow repositories and branches to be created if a check would otherwise prohibit it.required_status_checksarray of objectsRequiredStatus checks that are required.Name, Type, DescriptioncontextstringRequiredThe status check context name that must be present on the commit.integration_idintegerThe optional integration ID that this status check must originate from.strict_required_status_checks_policybooleanRequiredWhether pull requests targeting a matching branch must be tested with the latest code. This setting will not take effect unless at least one status check is enabled.non_fast_forwardobjectPrevent users with push access from force pushing to refs.Name, Type, DescriptiontypestringRequiredValue:non_fast_forwardcommit_message_patternobjectParameters to be used for the commit_message_pattern ruleName, Type, DescriptiontypestringRequiredValue:commit_message_patternparametersobjectName, Type, DescriptionnamestringHow this rule will appear to users.negatebooleanIf true, the rule will fail if the pattern matches.operatorstringRequiredThe operator to use for matching.Can be one of:starts_with,ends_with,contains,regexpatternstringRequiredThe pattern to match with.commit_author_email_patternobjectParameters to be used for the commit_author_email_pattern ruleName, Type, DescriptiontypestringRequiredValue:commit_author_email_patternparametersobjectName, Type, DescriptionnamestringHow this rule will appear to users.negatebooleanIf true, the rule will fail if the pattern matches.operatorstringRequiredThe operator to use for matching.Can be one of:starts_with,ends_with,contains,regexpatternstringRequiredThe pattern to match with.committer_email_patternobjectParameters to be used for the committer_email_pattern ruleName, Type, DescriptiontypestringRequiredValue:committer_email_patternparametersobjectName, Type, DescriptionnamestringHow this rule will appear to users.negatebooleanIf true, the rule will fail if the pattern matches.operatorstringRequiredThe operator to use for matching.Can be one of:starts_with,ends_with,contains,regexpatternstringRequiredThe pattern to match with.branch_name_patternobjectParameters to be used for the branch_name_pattern ruleName, Type, DescriptiontypestringRequiredValue:branch_name_patternparametersobjectName, Type, DescriptionnamestringHow this rule will appear to users.negatebooleanIf true, the rule will fail if the pattern matches.operatorstringRequiredThe operator to use for matching.Can be one of:starts_with,ends_with,contains,regexpatternstringRequiredThe pattern to match with.tag_name_patternobjectParameters to be used for the tag_name_pattern ruleName, Type, DescriptiontypestringRequiredValue:tag_name_patternparametersobjectName, Type, DescriptionnamestringHow this rule will appear to users.negatebooleanIf true, the rule will fail if the pattern matches.operatorstringRequiredThe operator to use for matching.Can be one of:starts_with,ends_with,contains,regexpatternstringRequiredThe pattern to match with.file_path_restrictionobjectPrevent commits that include changes in specified file and folder paths from being pushed to the commit graph. This includes absolute paths that contain file names.Name, Type, DescriptiontypestringRequiredValue:file_path_restrictionparametersobjectName, Type, Descriptionrestricted_file_pathsarray of stringsRequiredThe file paths that are restricted from being pushed to the commit graph.max_file_path_lengthobjectPrevent commits that include file paths that exceed the specified character limit from being pushed to the commit graph.Name, Type, DescriptiontypestringRequiredValue:max_file_path_lengthparametersobjectName, Type, Descriptionmax_file_path_lengthintegerRequiredThe maximum amount of characters allowed in file paths.file_extension_restrictionobjectPrevent commits that include files with specified file extensions from being pushed to the commit graph.Name, Type, DescriptiontypestringRequiredValue:file_extension_restrictionparametersobjectName, Type, Descriptionrestricted_file_extensionsarray of stringsRequiredThe file extensions that are restricted from being pushed to the commit graph.max_file_sizeobjectPrevent commits with individual files that exceed the specified limit from being pushed to the commit graph.Name, Type, DescriptiontypestringRequiredValue:max_file_sizeparametersobjectName, Type, Descriptionmax_file_sizeintegerRequiredThe maximum file size allowed in megabytes. This limit does not apply to Git Large File Storage (Git LFS).workflowsobjectRequire all changes made to a targeted branch to pass the specified workflows before they can be merged.Name, Type, DescriptiontypestringRequiredValue:workflowsparametersobjectName, Type, Descriptiondo_not_enforce_on_createbooleanAllow repositories and branches to be created if a check would otherwise prohibit it.workflowsarray of objectsRequiredWorkflows that must pass for this rule to pass.Name, Type, DescriptionpathstringRequiredThe path to the workflow filerefstringThe ref (branch or tag) of the workflow file to userepository_idintegerRequiredThe ID of the repository where the workflow is definedshastringThe commit SHA of the workflow file to usecode_scanningobjectChoose which tools must provide code scanning results before the reference is updated. When configured, code scanning must be enabled and have results for both the commit and the reference being updated.Name, Type, DescriptiontypestringRequiredValue:code_scanningparametersobjectName, Type, Descriptioncode_scanning_toolsarray of objectsRequiredTools that must provide code scanning results for this rule to pass.Name, Type, Descriptionalerts_thresholdstringRequiredThe severity level at which code scanning results that raise alerts block a reference update. For more information on alert severity levels, see "About code scanning alerts."Can be one of:none,errors,errors_and_warnings,allsecurity_alerts_thresholdstringRequiredThe severity level at which code scanning results that raise security alerts block a reference update. For more information on security severity levels, see "About code scanning alerts."Can be one of:none,critical,high_or_higher,medium_or_higher,alltoolstringRequiredThe name of a code scanning toolcopilot_code_reviewobjectRequest Copilot code review for new pull requests automatically if the author has access to Copilot code review and their premium requests quota has not reached the limit.Name, Type, DescriptiontypestringRequiredValue:copilot_code_reviewparametersobjectName, Type, Descriptionreview_draft_pull_requestsbooleanCopilot automatically reviews draft pull requests before they are marked as ready for review.review_on_pushbooleanCopilot automatically reviews each new push to the pull request. |
| Name, Type, Description |
| creationobjectOnly allow users with bypass permission to create matching refs. |
| Name, Type, DescriptiontypestringRequiredValue:creation |
| Name, Type, Description |
| typestringRequiredValue:creation |
| updateobjectOnly allow users with bypass permission to update matching refs. |
| Name, Type, DescriptiontypestringRequiredValue:updateparametersobjectName, Type, Descriptionupdate_allows_fetch_and_mergebooleanRequiredBranch can pull changes from its upstream repository |
| Name, Type, Description |
| typestringRequiredValue:update |
| parametersobject |
| Name, Type, Descriptionupdate_allows_fetch_and_mergebooleanRequiredBranch can pull changes from its upstream repository |
| Name, Type, Description |
| update_allows_fetch_and_mergebooleanRequiredBranch can pull changes from its upstream repository |
| deletionobjectOnly allow users with bypass permissions to delete matching refs. |
| Name, Type, DescriptiontypestringRequiredValue:deletion |
| Name, Type, Description |
| typestringRequiredValue:deletion |
| required_linear_historyobjectPrevent merge commits from being pushed to matching refs. |
| Name, Type, DescriptiontypestringRequiredValue:required_linear_history |
| Name, Type, Description |
| typestringRequiredValue:required_linear_history |
| merge_queueobjectMerges must be performed via a merge queue. |
| Name, Type, DescriptiontypestringRequiredValue:merge_queueparametersobjectName, Type, Descriptioncheck_response_timeout_minutesintegerRequiredMaximum time for a required status check to report a conclusion. After this much time has elapsed, checks that have not reported a conclusion will be assumed to have failedgrouping_strategystringRequiredWhen set to ALLGREEN, the merge commit created by merge queue for each PR in the group must pass all required checks to merge. When set to HEADGREEN, only the commit at the head of the merge group, i.e. the commit containing changes from all of the PRs in the group, must pass its required checks to merge.Can be one of:ALLGREEN,HEADGREENmax_entries_to_buildintegerRequiredLimit the number of queued pull requests requesting checks and workflow runs at the same time.max_entries_to_mergeintegerRequiredThe maximum number of PRs that will be merged together in a group.merge_methodstringRequiredMethod to use when merging changes from queued pull requests.Can be one of:MERGE,SQUASH,REBASEmin_entries_to_mergeintegerRequiredThe minimum number of PRs that will be merged together in a group.min_entries_to_merge_wait_minutesintegerRequiredThe time merge queue should wait after the first PR is added to the queue for the minimum group size to be met. After this time has elapsed, the minimum group size will be ignored and a smaller group will be merged. |
| Name, Type, Description |
| typestringRequiredValue:merge_queue |
| parametersobject |
| Name, Type, Descriptioncheck_response_timeout_minutesintegerRequiredMaximum time for a required status check to report a conclusion. After this much time has elapsed, checks that have not reported a conclusion will be assumed to have failedgrouping_strategystringRequiredWhen set to ALLGREEN, the merge commit created by merge queue for each PR in the group must pass all required checks to merge. When set to HEADGREEN, only the commit at the head of the merge group, i.e. the commit containing changes from all of the PRs in the group, must pass its required checks to merge.Can be one of:ALLGREEN,HEADGREENmax_entries_to_buildintegerRequiredLimit the number of queued pull requests requesting checks and workflow runs at the same time.max_entries_to_mergeintegerRequiredThe maximum number of PRs that will be merged together in a group.merge_methodstringRequiredMethod to use when merging changes from queued pull requests.Can be one of:MERGE,SQUASH,REBASEmin_entries_to_mergeintegerRequiredThe minimum number of PRs that will be merged together in a group.min_entries_to_merge_wait_minutesintegerRequiredThe time merge queue should wait after the first PR is added to the queue for the minimum group size to be met. After this time has elapsed, the minimum group size will be ignored and a smaller group will be merged. |
| Name, Type, Description |
| check_response_timeout_minutesintegerRequiredMaximum time for a required status check to report a conclusion. After this much time has elapsed, checks that have not reported a conclusion will be assumed to have failed |
| grouping_strategystringRequiredWhen set to ALLGREEN, the merge commit created by merge queue for each PR in the group must pass all required checks to merge. When set to HEADGREEN, only the commit at the head of the merge group, i.e. the commit containing changes from all of the PRs in the group, must pass its required checks to merge.Can be one of:ALLGREEN,HEADGREEN |
| max_entries_to_buildintegerRequiredLimit the number of queued pull requests requesting checks and workflow runs at the same time. |
| max_entries_to_mergeintegerRequiredThe maximum number of PRs that will be merged together in a group. |
| merge_methodstringRequiredMethod to use when merging changes from queued pull requests.Can be one of:MERGE,SQUASH,REBASE |
| min_entries_to_mergeintegerRequiredThe minimum number of PRs that will be merged together in a group. |
| min_entries_to_merge_wait_minutesintegerRequiredThe time merge queue should wait after the first PR is added to the queue for the minimum group size to be met. After this time has elapsed, the minimum group size will be ignored and a smaller group will be merged. |
| required_deploymentsobjectChoose which environments must be successfully deployed to before refs can be pushed into a ref that matches this rule. |
| Name, Type, DescriptiontypestringRequiredValue:required_deploymentsparametersobjectName, Type, Descriptionrequired_deployment_environmentsarray of stringsRequiredThe environments that must be successfully deployed to before branches can be merged. |
| Name, Type, Description |
| typestringRequiredValue:required_deployments |
| parametersobject |
| Name, Type, Descriptionrequired_deployment_environmentsarray of stringsRequiredThe environments that must be successfully deployed to before branches can be merged. |
| Name, Type, Description |
| required_deployment_environmentsarray of stringsRequiredThe environments that must be successfully deployed to before branches can be merged. |
| required_signaturesobjectCommits pushed to matching refs must have verified signatures. |
| Name, Type, DescriptiontypestringRequiredValue:required_signatures |
| Name, Type, Description |
| typestringRequiredValue:required_signatures |
| pull_requestobjectRequire all commits be made to a non-target branch and submitted via a pull request before they can be merged. |
| Name, Type, DescriptiontypestringRequiredValue:pull_requestparametersobjectName, Type, Descriptionallowed_merge_methodsarray of stringsArray of allowed merge methods. Allowed values includemerge,squash, andrebase. At least one option must be enabled.
Supported values are:merge,squash,rebasedismiss_stale_reviews_on_pushbooleanRequiredNew, reviewable commits pushed will dismiss previous pull request review approvals.require_code_owner_reviewbooleanRequiredRequire an approving review in pull requests that modify files that have a designated code owner.require_last_push_approvalbooleanRequiredWhether the most recent reviewable push must be approved by someone other than the person who pushed it.required_approving_review_countintegerRequiredThe number of approving reviews that are required before a pull request can be merged.required_review_thread_resolutionbooleanRequiredAll conversations on code must be resolved before a pull request can be merged.required_reviewersarray of objectsNoterequired_reviewersis in beta and subject to change.A collection of reviewers and associated file patterns. Each reviewer has a list of file patterns which determine the files that reviewer is required to review.Name, Type, Descriptionfile_patternsarray of stringsRequiredArray of file patterns. Pull requests which change matching files must be approved by the specified team. File patterns use fnmatch syntax.minimum_approvalsintegerRequiredMinimum number of approvals required from the specified team. If set to zero, the team will be added to the pull request but approval is optional.reviewerobjectRequiredA required reviewing teamName, Type, DescriptionidintegerRequiredID of the reviewer which must review changes to matching files.typestringRequiredThe type of the reviewerValue:Team |
| Name, Type, Description |
| typestringRequiredValue:pull_request |
| parametersobject |
| Name, Type, Descriptionallowed_merge_methodsarray of stringsArray of allowed merge methods. Allowed values includemerge,squash, andrebase. At least one option must be enabled.
Supported values are:merge,squash,rebasedismiss_stale_reviews_on_pushbooleanRequiredNew, reviewable commits pushed will dismiss previous pull request review approvals.require_code_owner_reviewbooleanRequiredRequire an approving review in pull requests that modify files that have a designated code owner.require_last_push_approvalbooleanRequiredWhether the most recent reviewable push must be approved by someone other than the person who pushed it.required_approving_review_countintegerRequiredThe number of approving reviews that are required before a pull request can be merged.required_review_thread_resolutionbooleanRequiredAll conversations on code must be resolved before a pull request can be merged.required_reviewersarray of objectsNoterequired_reviewersis in beta and subject to change.A collection of reviewers and associated file patterns. Each reviewer has a list of file patterns which determine the files that reviewer is required to review.Name, Type, Descriptionfile_patternsarray of stringsRequiredArray of file patterns. Pull requests which change matching files must be approved by the specified team. File patterns use fnmatch syntax.minimum_approvalsintegerRequiredMinimum number of approvals required from the specified team. If set to zero, the team will be added to the pull request but approval is optional.reviewerobjectRequiredA required reviewing teamName, Type, DescriptionidintegerRequiredID of the reviewer which must review changes to matching files.typestringRequiredThe type of the reviewerValue:Team |
| Name, Type, Description |
| allowed_merge_methodsarray of stringsArray of allowed merge methods. Allowed values includemerge,squash, andrebase. At least one option must be enabled.
Supported values are:merge,squash,rebase |
| dismiss_stale_reviews_on_pushbooleanRequiredNew, reviewable commits pushed will dismiss previous pull request review approvals. |
| require_code_owner_reviewbooleanRequiredRequire an approving review in pull requests that modify files that have a designated code owner. |
| require_last_push_approvalbooleanRequiredWhether the most recent reviewable push must be approved by someone other than the person who pushed it. |
| required_approving_review_countintegerRequiredThe number of approving reviews that are required before a pull request can be merged. |
| required_review_thread_resolutionbooleanRequiredAll conversations on code must be resolved before a pull request can be merged. |
| required_reviewersarray of objectsNoterequired_reviewersis in beta and subject to change.A collection of reviewers and associated file patterns. Each reviewer has a list of file patterns which determine the files that reviewer is required to review. |
| Name, Type, Descriptionfile_patternsarray of stringsRequiredArray of file patterns. Pull requests which change matching files must be approved by the specified team. File patterns use fnmatch syntax.minimum_approvalsintegerRequiredMinimum number of approvals required from the specified team. If set to zero, the team will be added to the pull request but approval is optional.reviewerobjectRequiredA required reviewing teamName, Type, DescriptionidintegerRequiredID of the reviewer which must review changes to matching files.typestringRequiredThe type of the reviewerValue:Team |
| Name, Type, Description |
| file_patternsarray of stringsRequiredArray of file patterns. Pull requests which change matching files must be approved by the specified team. File patterns use fnmatch syntax. |
| minimum_approvalsintegerRequiredMinimum number of approvals required from the specified team. If set to zero, the team will be added to the pull request but approval is optional. |
| reviewerobjectRequiredA required reviewing team |
| Name, Type, DescriptionidintegerRequiredID of the reviewer which must review changes to matching files.typestringRequiredThe type of the reviewerValue:Team |
| Name, Type, Description |
| idintegerRequiredID of the reviewer which must review changes to matching files. |
| typestringRequiredThe type of the reviewerValue:Team |
| required_status_checksobjectChoose which status checks must pass before the ref is updated. When enabled, commits must first be pushed to another ref where the checks pass. |
| Name, Type, DescriptiontypestringRequiredValue:required_status_checksparametersobjectName, Type, Descriptiondo_not_enforce_on_createbooleanAllow repositories and branches to be created if a check would otherwise prohibit it.required_status_checksarray of objectsRequiredStatus checks that are required.Name, Type, DescriptioncontextstringRequiredThe status check context name that must be present on the commit.integration_idintegerThe optional integration ID that this status check must originate from.strict_required_status_checks_policybooleanRequiredWhether pull requests targeting a matching branch must be tested with the latest code. This setting will not take effect unless at least one status check is enabled. |
| Name, Type, Description |
| typestringRequiredValue:required_status_checks |
| parametersobject |
| Name, Type, Descriptiondo_not_enforce_on_createbooleanAllow repositories and branches to be created if a check would otherwise prohibit it.required_status_checksarray of objectsRequiredStatus checks that are required.Name, Type, DescriptioncontextstringRequiredThe status check context name that must be present on the commit.integration_idintegerThe optional integration ID that this status check must originate from.strict_required_status_checks_policybooleanRequiredWhether pull requests targeting a matching branch must be tested with the latest code. This setting will not take effect unless at least one status check is enabled. |
| Name, Type, Description |
| do_not_enforce_on_createbooleanAllow repositories and branches to be created if a check would otherwise prohibit it. |
| required_status_checksarray of objectsRequiredStatus checks that are required. |
| Name, Type, DescriptioncontextstringRequiredThe status check context name that must be present on the commit.integration_idintegerThe optional integration ID that this status check must originate from. |
| Name, Type, Description |
| contextstringRequiredThe status check context name that must be present on the commit. |
| integration_idintegerThe optional integration ID that this status check must originate from. |
| strict_required_status_checks_policybooleanRequiredWhether pull requests targeting a matching branch must be tested with the latest code. This setting will not take effect unless at least one status check is enabled. |
| non_fast_forwardobjectPrevent users with push access from force pushing to refs. |
| Name, Type, DescriptiontypestringRequiredValue:non_fast_forward |
| Name, Type, Description |
| typestringRequiredValue:non_fast_forward |
| commit_message_patternobjectParameters to be used for the commit_message_pattern rule |
| Name, Type, DescriptiontypestringRequiredValue:commit_message_patternparametersobjectName, Type, DescriptionnamestringHow this rule will appear to users.negatebooleanIf true, the rule will fail if the pattern matches.operatorstringRequiredThe operator to use for matching.Can be one of:starts_with,ends_with,contains,regexpatternstringRequiredThe pattern to match with. |
| Name, Type, Description |
| typestringRequiredValue:commit_message_pattern |
| parametersobject |
| Name, Type, DescriptionnamestringHow this rule will appear to users.negatebooleanIf true, the rule will fail if the pattern matches.operatorstringRequiredThe operator to use for matching.Can be one of:starts_with,ends_with,contains,regexpatternstringRequiredThe pattern to match with. |
| Name, Type, Description |
| namestringHow this rule will appear to users. |
| negatebooleanIf true, the rule will fail if the pattern matches. |
| operatorstringRequiredThe operator to use for matching.Can be one of:starts_with,ends_with,contains,regex |
| patternstringRequiredThe pattern to match with. |
| commit_author_email_patternobjectParameters to be used for the commit_author_email_pattern rule |
| Name, Type, DescriptiontypestringRequiredValue:commit_author_email_patternparametersobjectName, Type, DescriptionnamestringHow this rule will appear to users.negatebooleanIf true, the rule will fail if the pattern matches.operatorstringRequiredThe operator to use for matching.Can be one of:starts_with,ends_with,contains,regexpatternstringRequiredThe pattern to match with. |
| Name, Type, Description |
| typestringRequiredValue:commit_author_email_pattern |
| parametersobject |
| Name, Type, DescriptionnamestringHow this rule will appear to users.negatebooleanIf true, the rule will fail if the pattern matches.operatorstringRequiredThe operator to use for matching.Can be one of:starts_with,ends_with,contains,regexpatternstringRequiredThe pattern to match with. |
| Name, Type, Description |
| namestringHow this rule will appear to users. |
| negatebooleanIf true, the rule will fail if the pattern matches. |
| operatorstringRequiredThe operator to use for matching.Can be one of:starts_with,ends_with,contains,regex |
| patternstringRequiredThe pattern to match with. |
| committer_email_patternobjectParameters to be used for the committer_email_pattern rule |
| Name, Type, DescriptiontypestringRequiredValue:committer_email_patternparametersobjectName, Type, DescriptionnamestringHow this rule will appear to users.negatebooleanIf true, the rule will fail if the pattern matches.operatorstringRequiredThe operator to use for matching.Can be one of:starts_with,ends_with,contains,regexpatternstringRequiredThe pattern to match with. |
| Name, Type, Description |
| typestringRequiredValue:committer_email_pattern |
| parametersobject |
| Name, Type, DescriptionnamestringHow this rule will appear to users.negatebooleanIf true, the rule will fail if the pattern matches.operatorstringRequiredThe operator to use for matching.Can be one of:starts_with,ends_with,contains,regexpatternstringRequiredThe pattern to match with. |
| Name, Type, Description |
| namestringHow this rule will appear to users. |
| negatebooleanIf true, the rule will fail if the pattern matches. |
| operatorstringRequiredThe operator to use for matching.Can be one of:starts_with,ends_with,contains,regex |
| patternstringRequiredThe pattern to match with. |
| branch_name_patternobjectParameters to be used for the branch_name_pattern rule |
| Name, Type, DescriptiontypestringRequiredValue:branch_name_patternparametersobjectName, Type, DescriptionnamestringHow this rule will appear to users.negatebooleanIf true, the rule will fail if the pattern matches.operatorstringRequiredThe operator to use for matching.Can be one of:starts_with,ends_with,contains,regexpatternstringRequiredThe pattern to match with. |
| Name, Type, Description |
| typestringRequiredValue:branch_name_pattern |
| parametersobject |
| Name, Type, DescriptionnamestringHow this rule will appear to users.negatebooleanIf true, the rule will fail if the pattern matches.operatorstringRequiredThe operator to use for matching.Can be one of:starts_with,ends_with,contains,regexpatternstringRequiredThe pattern to match with. |
| Name, Type, Description |
| namestringHow this rule will appear to users. |
| negatebooleanIf true, the rule will fail if the pattern matches. |
| operatorstringRequiredThe operator to use for matching.Can be one of:starts_with,ends_with,contains,regex |
| patternstringRequiredThe pattern to match with. |
| tag_name_patternobjectParameters to be used for the tag_name_pattern rule |
| Name, Type, DescriptiontypestringRequiredValue:tag_name_patternparametersobjectName, Type, DescriptionnamestringHow this rule will appear to users.negatebooleanIf true, the rule will fail if the pattern matches.operatorstringRequiredThe operator to use for matching.Can be one of:starts_with,ends_with,contains,regexpatternstringRequiredThe pattern to match with. |
| Name, Type, Description |
| typestringRequiredValue:tag_name_pattern |
| parametersobject |
| Name, Type, DescriptionnamestringHow this rule will appear to users.negatebooleanIf true, the rule will fail if the pattern matches.operatorstringRequiredThe operator to use for matching.Can be one of:starts_with,ends_with,contains,regexpatternstringRequiredThe pattern to match with. |
| Name, Type, Description |
| namestringHow this rule will appear to users. |
| negatebooleanIf true, the rule will fail if the pattern matches. |
| operatorstringRequiredThe operator to use for matching.Can be one of:starts_with,ends_with,contains,regex |
| patternstringRequiredThe pattern to match with. |
| file_path_restrictionobjectPrevent commits that include changes in specified file and folder paths from being pushed to the commit graph. This includes absolute paths that contain file names. |
| Name, Type, DescriptiontypestringRequiredValue:file_path_restrictionparametersobjectName, Type, Descriptionrestricted_file_pathsarray of stringsRequiredThe file paths that are restricted from being pushed to the commit graph. |
| Name, Type, Description |
| typestringRequiredValue:file_path_restriction |
| parametersobject |
| Name, Type, Descriptionrestricted_file_pathsarray of stringsRequiredThe file paths that are restricted from being pushed to the commit graph. |
| Name, Type, Description |
| restricted_file_pathsarray of stringsRequiredThe file paths that are restricted from being pushed to the commit graph. |
| max_file_path_lengthobjectPrevent commits that include file paths that exceed the specified character limit from being pushed to the commit graph. |
| Name, Type, DescriptiontypestringRequiredValue:max_file_path_lengthparametersobjectName, Type, Descriptionmax_file_path_lengthintegerRequiredThe maximum amount of characters allowed in file paths. |
| Name, Type, Description |
| typestringRequiredValue:max_file_path_length |
| parametersobject |
| Name, Type, Descriptionmax_file_path_lengthintegerRequiredThe maximum amount of characters allowed in file paths. |
| Name, Type, Description |
| max_file_path_lengthintegerRequiredThe maximum amount of characters allowed in file paths. |
| file_extension_restrictionobjectPrevent commits that include files with specified file extensions from being pushed to the commit graph. |
| Name, Type, DescriptiontypestringRequiredValue:file_extension_restrictionparametersobjectName, Type, Descriptionrestricted_file_extensionsarray of stringsRequiredThe file extensions that are restricted from being pushed to the commit graph. |
| Name, Type, Description |
| typestringRequiredValue:file_extension_restriction |
| parametersobject |
| Name, Type, Descriptionrestricted_file_extensionsarray of stringsRequiredThe file extensions that are restricted from being pushed to the commit graph. |
| Name, Type, Description |
| restricted_file_extensionsarray of stringsRequiredThe file extensions that are restricted from being pushed to the commit graph. |
| max_file_sizeobjectPrevent commits with individual files that exceed the specified limit from being pushed to the commit graph. |
| Name, Type, DescriptiontypestringRequiredValue:max_file_sizeparametersobjectName, Type, Descriptionmax_file_sizeintegerRequiredThe maximum file size allowed in megabytes. This limit does not apply to Git Large File Storage (Git LFS). |
| Name, Type, Description |
| typestringRequiredValue:max_file_size |
| parametersobject |
| Name, Type, Descriptionmax_file_sizeintegerRequiredThe maximum file size allowed in megabytes. This limit does not apply to Git Large File Storage (Git LFS). |
| Name, Type, Description |
| max_file_sizeintegerRequiredThe maximum file size allowed in megabytes. This limit does not apply to Git Large File Storage (Git LFS). |
| workflowsobjectRequire all changes made to a targeted branch to pass the specified workflows before they can be merged. |
| Name, Type, DescriptiontypestringRequiredValue:workflowsparametersobjectName, Type, Descriptiondo_not_enforce_on_createbooleanAllow repositories and branches to be created if a check would otherwise prohibit it.workflowsarray of objectsRequiredWorkflows that must pass for this rule to pass.Name, Type, DescriptionpathstringRequiredThe path to the workflow filerefstringThe ref (branch or tag) of the workflow file to userepository_idintegerRequiredThe ID of the repository where the workflow is definedshastringThe commit SHA of the workflow file to use |
| Name, Type, Description |
| typestringRequiredValue:workflows |
| parametersobject |
| Name, Type, Descriptiondo_not_enforce_on_createbooleanAllow repositories and branches to be created if a check would otherwise prohibit it.workflowsarray of objectsRequiredWorkflows that must pass for this rule to pass.Name, Type, DescriptionpathstringRequiredThe path to the workflow filerefstringThe ref (branch or tag) of the workflow file to userepository_idintegerRequiredThe ID of the repository where the workflow is definedshastringThe commit SHA of the workflow file to use |
| Name, Type, Description |
| do_not_enforce_on_createbooleanAllow repositories and branches to be created if a check would otherwise prohibit it. |
| workflowsarray of objectsRequiredWorkflows that must pass for this rule to pass. |
| Name, Type, DescriptionpathstringRequiredThe path to the workflow filerefstringThe ref (branch or tag) of the workflow file to userepository_idintegerRequiredThe ID of the repository where the workflow is definedshastringThe commit SHA of the workflow file to use |
| Name, Type, Description |
| pathstringRequiredThe path to the workflow file |
| refstringThe ref (branch or tag) of the workflow file to use |
| repository_idintegerRequiredThe ID of the repository where the workflow is defined |
| shastringThe commit SHA of the workflow file to use |
| code_scanningobjectChoose which tools must provide code scanning results before the reference is updated. When configured, code scanning must be enabled and have results for both the commit and the reference being updated. |
| Name, Type, DescriptiontypestringRequiredValue:code_scanningparametersobjectName, Type, Descriptioncode_scanning_toolsarray of objectsRequiredTools that must provide code scanning results for this rule to pass.Name, Type, Descriptionalerts_thresholdstringRequiredThe severity level at which code scanning results that raise alerts block a reference update. For more information on alert severity levels, see "About code scanning alerts."Can be one of:none,errors,errors_and_warnings,allsecurity_alerts_thresholdstringRequiredThe severity level at which code scanning results that raise security alerts block a reference update. For more information on security severity levels, see "About code scanning alerts."Can be one of:none,critical,high_or_higher,medium_or_higher,alltoolstringRequiredThe name of a code scanning tool |
| Name, Type, Description |
| typestringRequiredValue:code_scanning |
| parametersobject |
| Name, Type, Descriptioncode_scanning_toolsarray of objectsRequiredTools that must provide code scanning results for this rule to pass.Name, Type, Descriptionalerts_thresholdstringRequiredThe severity level at which code scanning results that raise alerts block a reference update. For more information on alert severity levels, see "About code scanning alerts."Can be one of:none,errors,errors_and_warnings,allsecurity_alerts_thresholdstringRequiredThe severity level at which code scanning results that raise security alerts block a reference update. For more information on security severity levels, see "About code scanning alerts."Can be one of:none,critical,high_or_higher,medium_or_higher,alltoolstringRequiredThe name of a code scanning tool |
| Name, Type, Description |
| code_scanning_toolsarray of objectsRequiredTools that must provide code scanning results for this rule to pass. |
| Name, Type, Descriptionalerts_thresholdstringRequiredThe severity level at which code scanning results that raise alerts block a reference update. For more information on alert severity levels, see "About code scanning alerts."Can be one of:none,errors,errors_and_warnings,allsecurity_alerts_thresholdstringRequiredThe severity level at which code scanning results that raise security alerts block a reference update. For more information on security severity levels, see "About code scanning alerts."Can be one of:none,critical,high_or_higher,medium_or_higher,alltoolstringRequiredThe name of a code scanning tool |
| Name, Type, Description |
| alerts_thresholdstringRequiredThe severity level at which code scanning results that raise alerts block a reference update. For more information on alert severity levels, see "About code scanning alerts."Can be one of:none,errors,errors_and_warnings,all |
| security_alerts_thresholdstringRequiredThe severity level at which code scanning results that raise security alerts block a reference update. For more information on security severity levels, see "About code scanning alerts."Can be one of:none,critical,high_or_higher,medium_or_higher,all |
| toolstringRequiredThe name of a code scanning tool |
| copilot_code_reviewobjectRequest Copilot code review for new pull requests automatically if the author has access to Copilot code review and their premium requests quota has not reached the limit. |
| Name, Type, DescriptiontypestringRequiredValue:copilot_code_reviewparametersobjectName, Type, Descriptionreview_draft_pull_requestsbooleanCopilot automatically reviews draft pull requests before they are marked as ready for review.review_on_pushbooleanCopilot automatically reviews each new push to the pull request. |
| Name, Type, Description |
| typestringRequiredValue:copilot_code_review |
| parametersobject |
| Name, Type, Descriptionreview_draft_pull_requestsbooleanCopilot automatically reviews draft pull requests before they are marked as ready for review.review_on_pushbooleanCopilot automatically reviews each new push to the pull request. |
| Name, Type, Description |
| review_draft_pull_requestsbooleanCopilot automatically reviews draft pull requests before they are marked as ready for review. |
| review_on_pushbooleanCopilot automatically reviews each new push to the pull request. |

### HTTP response status codes for "Create a repository ruleset"

| Status code | Description |
| --- | --- |
| 201 | Created |
| 404 | Resource not found |
| 500 | Internal Error |

### Code samples for "Create a repository ruleset"

#### Request example

post/repos/{owner}/{repo}/rulesets

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/rulesets \
  -d '{"name":"super cool ruleset","target":"branch","enforcement":"active","bypass_actors":[{"actor_id":234,"actor_type":"Team","bypass_mode":"always"}],"conditions":{"ref_name":{"include":["refs/heads/main","refs/heads/master"],"exclude":["refs/heads/dev*"]}},"rules":[{"type":"commit_author_email_pattern","parameters":{"operator":"contains","pattern":"github"}}]}'`

Response

-
-

`Status: 201``{
"id": 42,
"name": "super cool ruleset",
"target": "branch",
"source_type": "Repository",
"source": "monalisa/my-repo",
"enforcement": "active",
"bypass_actors": [
{
"actor_id": 234,
"actor_type": "Team",
"bypass_mode": "always"
}
],
"conditions": {
"ref_name": {
"include": [
"refs/heads/main",
"refs/heads/master"
],
"exclude": [
"refs/heads/dev*"
]
}
},
"rules": [
{
"type": "commit_author_email_pattern",
"parameters": {
"operator": "contains",
"pattern": "github"
}
}
],
"node_id": "RRS_lACkVXNlcgQB",
"_links": {
"self": {
"href": "https://api.github.com/repos/monalisa/my-repo/rulesets/42"
},
"html": {
"href": "https://github.com/monalisa/my-repo/rules/42"
}
},
"created_at": "2023-07-15T08:43:03Z",
"updated_at": "2023-08-23T16:29:47Z"
}`

## Get a repository ruleset

Get a ruleset for a repository.

**Note:** To prevent leaking sensitive information, the `bypass_actors` property is only returned if the user
making the API request has write access to the ruleset.

### Fine-grained access tokens for "Get a repository ruleset"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Metadata" repository permissions (read)

This endpoint can be used without authentication or the aforementioned permissions if only public resources are requested.

### Parameters for "Get a repository ruleset"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| ruleset_idintegerRequiredThe ID of the ruleset. |

| Name, Type, Description |
| --- |
| includes_parentsbooleanInclude rulesets configured at higher levels that apply to this repositoryDefault:true |

### HTTP response status codes for "Get a repository ruleset"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |
| 500 | Internal Error |

### Code samples for "Get a repository ruleset"

#### Request example

get/repos/{owner}/{repo}/rulesets/{ruleset_id}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/rulesets/RULESET_ID`

Response

-
-

`Status: 200``{
"id": 42,
"name": "super cool ruleset",
"target": "branch",
"source_type": "Repository",
"source": "monalisa/my-repo",
"enforcement": "active",
"bypass_actors": [
{
"actor_id": 234,
"actor_type": "Team",
"bypass_mode": "always"
}
],
"conditions": {
"ref_name": {
"include": [
"refs/heads/main",
"refs/heads/master"
],
"exclude": [
"refs/heads/dev*"
]
}
},
"rules": [
{
"type": "commit_author_email_pattern",
"parameters": {
"operator": "contains",
"pattern": "github"
}
}
],
"node_id": "RRS_lACkVXNlcgQB",
"_links": {
"self": {
"href": "https://api.github.com/repos/monalisa/my-repo/rulesets/42"
},
"html": {
"href": "https://github.com/monalisa/my-repo/rules/42"
}
},
"created_at": "2023-07-15T08:43:03Z",
"updated_at": "2023-08-23T16:29:47Z"
}`

## Update a repository ruleset

Update a ruleset for a repository.

### Fine-grained access tokens for "Update a repository ruleset"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Update a repository ruleset"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| ruleset_idintegerRequiredThe ID of the ruleset. |

| Name, Type, Description |
| --- |
| namestringThe name of the ruleset. |
| targetstringThe target of the rulesetCan be one of:branch,tag,push |
| enforcementstringThe enforcement level of the ruleset.evaluateallows admins to test rules before enforcing them. Admins can view insights on the Rule Insights page (evaluateis only available with GitHub Enterprise).Can be one of:disabled,active,evaluate |
| bypass_actorsarray of objectsThe actors that can bypass the rules in this ruleset |
| Name, Type, Descriptionactor_idinteger or nullThe ID of the actor that can bypass a ruleset. Required forIntegration,RepositoryRole, andTeamactor types. Ifactor_typeisOrganizationAdmin,actor_idis ignored. Ifactor_typeisDeployKey, this should be null.OrganizationAdminis not applicable for personal repositories.actor_typestringRequiredThe type of actor that can bypass a ruleset.Can be one of:Integration,OrganizationAdmin,RepositoryRole,Team,DeployKeybypass_modestringWhen the specified actor can bypass the ruleset.pull_requestmeans that an actor can only bypass rules on pull requests.pull_requestis not applicable for theDeployKeyactor type. Also,pull_requestis only applicable to branch rulesets. Whenbypass_modeisexempt, rules will not be run for that actor and a bypass audit entry will not be created.Default:alwaysCan be one of:always,pull_request,exempt |
| Name, Type, Description |
| actor_idinteger or nullThe ID of the actor that can bypass a ruleset. Required forIntegration,RepositoryRole, andTeamactor types. Ifactor_typeisOrganizationAdmin,actor_idis ignored. Ifactor_typeisDeployKey, this should be null.OrganizationAdminis not applicable for personal repositories. |
| actor_typestringRequiredThe type of actor that can bypass a ruleset.Can be one of:Integration,OrganizationAdmin,RepositoryRole,Team,DeployKey |
| bypass_modestringWhen the specified actor can bypass the ruleset.pull_requestmeans that an actor can only bypass rules on pull requests.pull_requestis not applicable for theDeployKeyactor type. Also,pull_requestis only applicable to branch rulesets. Whenbypass_modeisexempt, rules will not be run for that actor and a bypass audit entry will not be created.Default:alwaysCan be one of:always,pull_request,exempt |
| conditionsobjectParameters for a repository ruleset ref name condition |
| Name, Type, Descriptionref_nameobjectName, Type, Descriptionincludearray of stringsArray of ref names or patterns to include. One of these patterns must match for the condition to pass. Also accepts~DEFAULT_BRANCHto include the default branch or~ALLto include all branches.excludearray of stringsArray of ref names or patterns to exclude. The condition will not pass if any of these patterns match. |
| Name, Type, Description |
| ref_nameobject |
| Name, Type, Descriptionincludearray of stringsArray of ref names or patterns to include. One of these patterns must match for the condition to pass. Also accepts~DEFAULT_BRANCHto include the default branch or~ALLto include all branches.excludearray of stringsArray of ref names or patterns to exclude. The condition will not pass if any of these patterns match. |
| Name, Type, Description |
| includearray of stringsArray of ref names or patterns to include. One of these patterns must match for the condition to pass. Also accepts~DEFAULT_BRANCHto include the default branch or~ALLto include all branches. |
| excludearray of stringsArray of ref names or patterns to exclude. The condition will not pass if any of these patterns match. |
| rulesarray of objectsAn array of rules within the ruleset. |
| Name, Type, DescriptioncreationobjectOnly allow users with bypass permission to create matching refs.Name, Type, DescriptiontypestringRequiredValue:creationupdateobjectOnly allow users with bypass permission to update matching refs.Name, Type, DescriptiontypestringRequiredValue:updateparametersobjectName, Type, Descriptionupdate_allows_fetch_and_mergebooleanRequiredBranch can pull changes from its upstream repositorydeletionobjectOnly allow users with bypass permissions to delete matching refs.Name, Type, DescriptiontypestringRequiredValue:deletionrequired_linear_historyobjectPrevent merge commits from being pushed to matching refs.Name, Type, DescriptiontypestringRequiredValue:required_linear_historymerge_queueobjectMerges must be performed via a merge queue.Name, Type, DescriptiontypestringRequiredValue:merge_queueparametersobjectName, Type, Descriptioncheck_response_timeout_minutesintegerRequiredMaximum time for a required status check to report a conclusion. After this much time has elapsed, checks that have not reported a conclusion will be assumed to have failedgrouping_strategystringRequiredWhen set to ALLGREEN, the merge commit created by merge queue for each PR in the group must pass all required checks to merge. When set to HEADGREEN, only the commit at the head of the merge group, i.e. the commit containing changes from all of the PRs in the group, must pass its required checks to merge.Can be one of:ALLGREEN,HEADGREENmax_entries_to_buildintegerRequiredLimit the number of queued pull requests requesting checks and workflow runs at the same time.max_entries_to_mergeintegerRequiredThe maximum number of PRs that will be merged together in a group.merge_methodstringRequiredMethod to use when merging changes from queued pull requests.Can be one of:MERGE,SQUASH,REBASEmin_entries_to_mergeintegerRequiredThe minimum number of PRs that will be merged together in a group.min_entries_to_merge_wait_minutesintegerRequiredThe time merge queue should wait after the first PR is added to the queue for the minimum group size to be met. After this time has elapsed, the minimum group size will be ignored and a smaller group will be merged.required_deploymentsobjectChoose which environments must be successfully deployed to before refs can be pushed into a ref that matches this rule.Name, Type, DescriptiontypestringRequiredValue:required_deploymentsparametersobjectName, Type, Descriptionrequired_deployment_environmentsarray of stringsRequiredThe environments that must be successfully deployed to before branches can be merged.required_signaturesobjectCommits pushed to matching refs must have verified signatures.Name, Type, DescriptiontypestringRequiredValue:required_signaturespull_requestobjectRequire all commits be made to a non-target branch and submitted via a pull request before they can be merged.Name, Type, DescriptiontypestringRequiredValue:pull_requestparametersobjectName, Type, Descriptionallowed_merge_methodsarray of stringsArray of allowed merge methods. Allowed values includemerge,squash, andrebase. At least one option must be enabled.
Supported values are:merge,squash,rebasedismiss_stale_reviews_on_pushbooleanRequiredNew, reviewable commits pushed will dismiss previous pull request review approvals.require_code_owner_reviewbooleanRequiredRequire an approving review in pull requests that modify files that have a designated code owner.require_last_push_approvalbooleanRequiredWhether the most recent reviewable push must be approved by someone other than the person who pushed it.required_approving_review_countintegerRequiredThe number of approving reviews that are required before a pull request can be merged.required_review_thread_resolutionbooleanRequiredAll conversations on code must be resolved before a pull request can be merged.required_reviewersarray of objectsNoterequired_reviewersis in beta and subject to change.A collection of reviewers and associated file patterns. Each reviewer has a list of file patterns which determine the files that reviewer is required to review.Name, Type, Descriptionfile_patternsarray of stringsRequiredArray of file patterns. Pull requests which change matching files must be approved by the specified team. File patterns use fnmatch syntax.minimum_approvalsintegerRequiredMinimum number of approvals required from the specified team. If set to zero, the team will be added to the pull request but approval is optional.reviewerobjectRequiredA required reviewing teamName, Type, DescriptionidintegerRequiredID of the reviewer which must review changes to matching files.typestringRequiredThe type of the reviewerValue:Teamrequired_status_checksobjectChoose which status checks must pass before the ref is updated. When enabled, commits must first be pushed to another ref where the checks pass.Name, Type, DescriptiontypestringRequiredValue:required_status_checksparametersobjectName, Type, Descriptiondo_not_enforce_on_createbooleanAllow repositories and branches to be created if a check would otherwise prohibit it.required_status_checksarray of objectsRequiredStatus checks that are required.Name, Type, DescriptioncontextstringRequiredThe status check context name that must be present on the commit.integration_idintegerThe optional integration ID that this status check must originate from.strict_required_status_checks_policybooleanRequiredWhether pull requests targeting a matching branch must be tested with the latest code. This setting will not take effect unless at least one status check is enabled.non_fast_forwardobjectPrevent users with push access from force pushing to refs.Name, Type, DescriptiontypestringRequiredValue:non_fast_forwardcommit_message_patternobjectParameters to be used for the commit_message_pattern ruleName, Type, DescriptiontypestringRequiredValue:commit_message_patternparametersobjectName, Type, DescriptionnamestringHow this rule will appear to users.negatebooleanIf true, the rule will fail if the pattern matches.operatorstringRequiredThe operator to use for matching.Can be one of:starts_with,ends_with,contains,regexpatternstringRequiredThe pattern to match with.commit_author_email_patternobjectParameters to be used for the commit_author_email_pattern ruleName, Type, DescriptiontypestringRequiredValue:commit_author_email_patternparametersobjectName, Type, DescriptionnamestringHow this rule will appear to users.negatebooleanIf true, the rule will fail if the pattern matches.operatorstringRequiredThe operator to use for matching.Can be one of:starts_with,ends_with,contains,regexpatternstringRequiredThe pattern to match with.committer_email_patternobjectParameters to be used for the committer_email_pattern ruleName, Type, DescriptiontypestringRequiredValue:committer_email_patternparametersobjectName, Type, DescriptionnamestringHow this rule will appear to users.negatebooleanIf true, the rule will fail if the pattern matches.operatorstringRequiredThe operator to use for matching.Can be one of:starts_with,ends_with,contains,regexpatternstringRequiredThe pattern to match with.branch_name_patternobjectParameters to be used for the branch_name_pattern ruleName, Type, DescriptiontypestringRequiredValue:branch_name_patternparametersobjectName, Type, DescriptionnamestringHow this rule will appear to users.negatebooleanIf true, the rule will fail if the pattern matches.operatorstringRequiredThe operator to use for matching.Can be one of:starts_with,ends_with,contains,regexpatternstringRequiredThe pattern to match with.tag_name_patternobjectParameters to be used for the tag_name_pattern ruleName, Type, DescriptiontypestringRequiredValue:tag_name_patternparametersobjectName, Type, DescriptionnamestringHow this rule will appear to users.negatebooleanIf true, the rule will fail if the pattern matches.operatorstringRequiredThe operator to use for matching.Can be one of:starts_with,ends_with,contains,regexpatternstringRequiredThe pattern to match with.file_path_restrictionobjectPrevent commits that include changes in specified file and folder paths from being pushed to the commit graph. This includes absolute paths that contain file names.Name, Type, DescriptiontypestringRequiredValue:file_path_restrictionparametersobjectName, Type, Descriptionrestricted_file_pathsarray of stringsRequiredThe file paths that are restricted from being pushed to the commit graph.max_file_path_lengthobjectPrevent commits that include file paths that exceed the specified character limit from being pushed to the commit graph.Name, Type, DescriptiontypestringRequiredValue:max_file_path_lengthparametersobjectName, Type, Descriptionmax_file_path_lengthintegerRequiredThe maximum amount of characters allowed in file paths.file_extension_restrictionobjectPrevent commits that include files with specified file extensions from being pushed to the commit graph.Name, Type, DescriptiontypestringRequiredValue:file_extension_restrictionparametersobjectName, Type, Descriptionrestricted_file_extensionsarray of stringsRequiredThe file extensions that are restricted from being pushed to the commit graph.max_file_sizeobjectPrevent commits with individual files that exceed the specified limit from being pushed to the commit graph.Name, Type, DescriptiontypestringRequiredValue:max_file_sizeparametersobjectName, Type, Descriptionmax_file_sizeintegerRequiredThe maximum file size allowed in megabytes. This limit does not apply to Git Large File Storage (Git LFS).workflowsobjectRequire all changes made to a targeted branch to pass the specified workflows before they can be merged.Name, Type, DescriptiontypestringRequiredValue:workflowsparametersobjectName, Type, Descriptiondo_not_enforce_on_createbooleanAllow repositories and branches to be created if a check would otherwise prohibit it.workflowsarray of objectsRequiredWorkflows that must pass for this rule to pass.Name, Type, DescriptionpathstringRequiredThe path to the workflow filerefstringThe ref (branch or tag) of the workflow file to userepository_idintegerRequiredThe ID of the repository where the workflow is definedshastringThe commit SHA of the workflow file to usecode_scanningobjectChoose which tools must provide code scanning results before the reference is updated. When configured, code scanning must be enabled and have results for both the commit and the reference being updated.Name, Type, DescriptiontypestringRequiredValue:code_scanningparametersobjectName, Type, Descriptioncode_scanning_toolsarray of objectsRequiredTools that must provide code scanning results for this rule to pass.Name, Type, Descriptionalerts_thresholdstringRequiredThe severity level at which code scanning results that raise alerts block a reference update. For more information on alert severity levels, see "About code scanning alerts."Can be one of:none,errors,errors_and_warnings,allsecurity_alerts_thresholdstringRequiredThe severity level at which code scanning results that raise security alerts block a reference update. For more information on security severity levels, see "About code scanning alerts."Can be one of:none,critical,high_or_higher,medium_or_higher,alltoolstringRequiredThe name of a code scanning toolcopilot_code_reviewobjectRequest Copilot code review for new pull requests automatically if the author has access to Copilot code review and their premium requests quota has not reached the limit.Name, Type, DescriptiontypestringRequiredValue:copilot_code_reviewparametersobjectName, Type, Descriptionreview_draft_pull_requestsbooleanCopilot automatically reviews draft pull requests before they are marked as ready for review.review_on_pushbooleanCopilot automatically reviews each new push to the pull request. |
| Name, Type, Description |
| creationobjectOnly allow users with bypass permission to create matching refs. |
| Name, Type, DescriptiontypestringRequiredValue:creation |
| Name, Type, Description |
| typestringRequiredValue:creation |
| updateobjectOnly allow users with bypass permission to update matching refs. |
| Name, Type, DescriptiontypestringRequiredValue:updateparametersobjectName, Type, Descriptionupdate_allows_fetch_and_mergebooleanRequiredBranch can pull changes from its upstream repository |
| Name, Type, Description |
| typestringRequiredValue:update |
| parametersobject |
| Name, Type, Descriptionupdate_allows_fetch_and_mergebooleanRequiredBranch can pull changes from its upstream repository |
| Name, Type, Description |
| update_allows_fetch_and_mergebooleanRequiredBranch can pull changes from its upstream repository |
| deletionobjectOnly allow users with bypass permissions to delete matching refs. |
| Name, Type, DescriptiontypestringRequiredValue:deletion |
| Name, Type, Description |
| typestringRequiredValue:deletion |
| required_linear_historyobjectPrevent merge commits from being pushed to matching refs. |
| Name, Type, DescriptiontypestringRequiredValue:required_linear_history |
| Name, Type, Description |
| typestringRequiredValue:required_linear_history |
| merge_queueobjectMerges must be performed via a merge queue. |
| Name, Type, DescriptiontypestringRequiredValue:merge_queueparametersobjectName, Type, Descriptioncheck_response_timeout_minutesintegerRequiredMaximum time for a required status check to report a conclusion. After this much time has elapsed, checks that have not reported a conclusion will be assumed to have failedgrouping_strategystringRequiredWhen set to ALLGREEN, the merge commit created by merge queue for each PR in the group must pass all required checks to merge. When set to HEADGREEN, only the commit at the head of the merge group, i.e. the commit containing changes from all of the PRs in the group, must pass its required checks to merge.Can be one of:ALLGREEN,HEADGREENmax_entries_to_buildintegerRequiredLimit the number of queued pull requests requesting checks and workflow runs at the same time.max_entries_to_mergeintegerRequiredThe maximum number of PRs that will be merged together in a group.merge_methodstringRequiredMethod to use when merging changes from queued pull requests.Can be one of:MERGE,SQUASH,REBASEmin_entries_to_mergeintegerRequiredThe minimum number of PRs that will be merged together in a group.min_entries_to_merge_wait_minutesintegerRequiredThe time merge queue should wait after the first PR is added to the queue for the minimum group size to be met. After this time has elapsed, the minimum group size will be ignored and a smaller group will be merged. |
| Name, Type, Description |
| typestringRequiredValue:merge_queue |
| parametersobject |
| Name, Type, Descriptioncheck_response_timeout_minutesintegerRequiredMaximum time for a required status check to report a conclusion. After this much time has elapsed, checks that have not reported a conclusion will be assumed to have failedgrouping_strategystringRequiredWhen set to ALLGREEN, the merge commit created by merge queue for each PR in the group must pass all required checks to merge. When set to HEADGREEN, only the commit at the head of the merge group, i.e. the commit containing changes from all of the PRs in the group, must pass its required checks to merge.Can be one of:ALLGREEN,HEADGREENmax_entries_to_buildintegerRequiredLimit the number of queued pull requests requesting checks and workflow runs at the same time.max_entries_to_mergeintegerRequiredThe maximum number of PRs that will be merged together in a group.merge_methodstringRequiredMethod to use when merging changes from queued pull requests.Can be one of:MERGE,SQUASH,REBASEmin_entries_to_mergeintegerRequiredThe minimum number of PRs that will be merged together in a group.min_entries_to_merge_wait_minutesintegerRequiredThe time merge queue should wait after the first PR is added to the queue for the minimum group size to be met. After this time has elapsed, the minimum group size will be ignored and a smaller group will be merged. |
| Name, Type, Description |
| check_response_timeout_minutesintegerRequiredMaximum time for a required status check to report a conclusion. After this much time has elapsed, checks that have not reported a conclusion will be assumed to have failed |
| grouping_strategystringRequiredWhen set to ALLGREEN, the merge commit created by merge queue for each PR in the group must pass all required checks to merge. When set to HEADGREEN, only the commit at the head of the merge group, i.e. the commit containing changes from all of the PRs in the group, must pass its required checks to merge.Can be one of:ALLGREEN,HEADGREEN |
| max_entries_to_buildintegerRequiredLimit the number of queued pull requests requesting checks and workflow runs at the same time. |
| max_entries_to_mergeintegerRequiredThe maximum number of PRs that will be merged together in a group. |
| merge_methodstringRequiredMethod to use when merging changes from queued pull requests.Can be one of:MERGE,SQUASH,REBASE |
| min_entries_to_mergeintegerRequiredThe minimum number of PRs that will be merged together in a group. |
| min_entries_to_merge_wait_minutesintegerRequiredThe time merge queue should wait after the first PR is added to the queue for the minimum group size to be met. After this time has elapsed, the minimum group size will be ignored and a smaller group will be merged. |
| required_deploymentsobjectChoose which environments must be successfully deployed to before refs can be pushed into a ref that matches this rule. |
| Name, Type, DescriptiontypestringRequiredValue:required_deploymentsparametersobjectName, Type, Descriptionrequired_deployment_environmentsarray of stringsRequiredThe environments that must be successfully deployed to before branches can be merged. |
| Name, Type, Description |
| typestringRequiredValue:required_deployments |
| parametersobject |
| Name, Type, Descriptionrequired_deployment_environmentsarray of stringsRequiredThe environments that must be successfully deployed to before branches can be merged. |
| Name, Type, Description |
| required_deployment_environmentsarray of stringsRequiredThe environments that must be successfully deployed to before branches can be merged. |
| required_signaturesobjectCommits pushed to matching refs must have verified signatures. |
| Name, Type, DescriptiontypestringRequiredValue:required_signatures |
| Name, Type, Description |
| typestringRequiredValue:required_signatures |
| pull_requestobjectRequire all commits be made to a non-target branch and submitted via a pull request before they can be merged. |
| Name, Type, DescriptiontypestringRequiredValue:pull_requestparametersobjectName, Type, Descriptionallowed_merge_methodsarray of stringsArray of allowed merge methods. Allowed values includemerge,squash, andrebase. At least one option must be enabled.
Supported values are:merge,squash,rebasedismiss_stale_reviews_on_pushbooleanRequiredNew, reviewable commits pushed will dismiss previous pull request review approvals.require_code_owner_reviewbooleanRequiredRequire an approving review in pull requests that modify files that have a designated code owner.require_last_push_approvalbooleanRequiredWhether the most recent reviewable push must be approved by someone other than the person who pushed it.required_approving_review_countintegerRequiredThe number of approving reviews that are required before a pull request can be merged.required_review_thread_resolutionbooleanRequiredAll conversations on code must be resolved before a pull request can be merged.required_reviewersarray of objectsNoterequired_reviewersis in beta and subject to change.A collection of reviewers and associated file patterns. Each reviewer has a list of file patterns which determine the files that reviewer is required to review.Name, Type, Descriptionfile_patternsarray of stringsRequiredArray of file patterns. Pull requests which change matching files must be approved by the specified team. File patterns use fnmatch syntax.minimum_approvalsintegerRequiredMinimum number of approvals required from the specified team. If set to zero, the team will be added to the pull request but approval is optional.reviewerobjectRequiredA required reviewing teamName, Type, DescriptionidintegerRequiredID of the reviewer which must review changes to matching files.typestringRequiredThe type of the reviewerValue:Team |
| Name, Type, Description |
| typestringRequiredValue:pull_request |
| parametersobject |
| Name, Type, Descriptionallowed_merge_methodsarray of stringsArray of allowed merge methods. Allowed values includemerge,squash, andrebase. At least one option must be enabled.
Supported values are:merge,squash,rebasedismiss_stale_reviews_on_pushbooleanRequiredNew, reviewable commits pushed will dismiss previous pull request review approvals.require_code_owner_reviewbooleanRequiredRequire an approving review in pull requests that modify files that have a designated code owner.require_last_push_approvalbooleanRequiredWhether the most recent reviewable push must be approved by someone other than the person who pushed it.required_approving_review_countintegerRequiredThe number of approving reviews that are required before a pull request can be merged.required_review_thread_resolutionbooleanRequiredAll conversations on code must be resolved before a pull request can be merged.required_reviewersarray of objectsNoterequired_reviewersis in beta and subject to change.A collection of reviewers and associated file patterns. Each reviewer has a list of file patterns which determine the files that reviewer is required to review.Name, Type, Descriptionfile_patternsarray of stringsRequiredArray of file patterns. Pull requests which change matching files must be approved by the specified team. File patterns use fnmatch syntax.minimum_approvalsintegerRequiredMinimum number of approvals required from the specified team. If set to zero, the team will be added to the pull request but approval is optional.reviewerobjectRequiredA required reviewing teamName, Type, DescriptionidintegerRequiredID of the reviewer which must review changes to matching files.typestringRequiredThe type of the reviewerValue:Team |
| Name, Type, Description |
| allowed_merge_methodsarray of stringsArray of allowed merge methods. Allowed values includemerge,squash, andrebase. At least one option must be enabled.
Supported values are:merge,squash,rebase |
| dismiss_stale_reviews_on_pushbooleanRequiredNew, reviewable commits pushed will dismiss previous pull request review approvals. |
| require_code_owner_reviewbooleanRequiredRequire an approving review in pull requests that modify files that have a designated code owner. |
| require_last_push_approvalbooleanRequiredWhether the most recent reviewable push must be approved by someone other than the person who pushed it. |
| required_approving_review_countintegerRequiredThe number of approving reviews that are required before a pull request can be merged. |
| required_review_thread_resolutionbooleanRequiredAll conversations on code must be resolved before a pull request can be merged. |
| required_reviewersarray of objectsNoterequired_reviewersis in beta and subject to change.A collection of reviewers and associated file patterns. Each reviewer has a list of file patterns which determine the files that reviewer is required to review. |
| Name, Type, Descriptionfile_patternsarray of stringsRequiredArray of file patterns. Pull requests which change matching files must be approved by the specified team. File patterns use fnmatch syntax.minimum_approvalsintegerRequiredMinimum number of approvals required from the specified team. If set to zero, the team will be added to the pull request but approval is optional.reviewerobjectRequiredA required reviewing teamName, Type, DescriptionidintegerRequiredID of the reviewer which must review changes to matching files.typestringRequiredThe type of the reviewerValue:Team |
| Name, Type, Description |
| file_patternsarray of stringsRequiredArray of file patterns. Pull requests which change matching files must be approved by the specified team. File patterns use fnmatch syntax. |
| minimum_approvalsintegerRequiredMinimum number of approvals required from the specified team. If set to zero, the team will be added to the pull request but approval is optional. |
| reviewerobjectRequiredA required reviewing team |
| Name, Type, DescriptionidintegerRequiredID of the reviewer which must review changes to matching files.typestringRequiredThe type of the reviewerValue:Team |
| Name, Type, Description |
| idintegerRequiredID of the reviewer which must review changes to matching files. |
| typestringRequiredThe type of the reviewerValue:Team |
| required_status_checksobjectChoose which status checks must pass before the ref is updated. When enabled, commits must first be pushed to another ref where the checks pass. |
| Name, Type, DescriptiontypestringRequiredValue:required_status_checksparametersobjectName, Type, Descriptiondo_not_enforce_on_createbooleanAllow repositories and branches to be created if a check would otherwise prohibit it.required_status_checksarray of objectsRequiredStatus checks that are required.Name, Type, DescriptioncontextstringRequiredThe status check context name that must be present on the commit.integration_idintegerThe optional integration ID that this status check must originate from.strict_required_status_checks_policybooleanRequiredWhether pull requests targeting a matching branch must be tested with the latest code. This setting will not take effect unless at least one status check is enabled. |
| Name, Type, Description |
| typestringRequiredValue:required_status_checks |
| parametersobject |
| Name, Type, Descriptiondo_not_enforce_on_createbooleanAllow repositories and branches to be created if a check would otherwise prohibit it.required_status_checksarray of objectsRequiredStatus checks that are required.Name, Type, DescriptioncontextstringRequiredThe status check context name that must be present on the commit.integration_idintegerThe optional integration ID that this status check must originate from.strict_required_status_checks_policybooleanRequiredWhether pull requests targeting a matching branch must be tested with the latest code. This setting will not take effect unless at least one status check is enabled. |
| Name, Type, Description |
| do_not_enforce_on_createbooleanAllow repositories and branches to be created if a check would otherwise prohibit it. |
| required_status_checksarray of objectsRequiredStatus checks that are required. |
| Name, Type, DescriptioncontextstringRequiredThe status check context name that must be present on the commit.integration_idintegerThe optional integration ID that this status check must originate from. |
| Name, Type, Description |
| contextstringRequiredThe status check context name that must be present on the commit. |
| integration_idintegerThe optional integration ID that this status check must originate from. |
| strict_required_status_checks_policybooleanRequiredWhether pull requests targeting a matching branch must be tested with the latest code. This setting will not take effect unless at least one status check is enabled. |
| non_fast_forwardobjectPrevent users with push access from force pushing to refs. |
| Name, Type, DescriptiontypestringRequiredValue:non_fast_forward |
| Name, Type, Description |
| typestringRequiredValue:non_fast_forward |
| commit_message_patternobjectParameters to be used for the commit_message_pattern rule |
| Name, Type, DescriptiontypestringRequiredValue:commit_message_patternparametersobjectName, Type, DescriptionnamestringHow this rule will appear to users.negatebooleanIf true, the rule will fail if the pattern matches.operatorstringRequiredThe operator to use for matching.Can be one of:starts_with,ends_with,contains,regexpatternstringRequiredThe pattern to match with. |
| Name, Type, Description |
| typestringRequiredValue:commit_message_pattern |
| parametersobject |
| Name, Type, DescriptionnamestringHow this rule will appear to users.negatebooleanIf true, the rule will fail if the pattern matches.operatorstringRequiredThe operator to use for matching.Can be one of:starts_with,ends_with,contains,regexpatternstringRequiredThe pattern to match with. |
| Name, Type, Description |
| namestringHow this rule will appear to users. |
| negatebooleanIf true, the rule will fail if the pattern matches. |
| operatorstringRequiredThe operator to use for matching.Can be one of:starts_with,ends_with,contains,regex |
| patternstringRequiredThe pattern to match with. |
| commit_author_email_patternobjectParameters to be used for the commit_author_email_pattern rule |
| Name, Type, DescriptiontypestringRequiredValue:commit_author_email_patternparametersobjectName, Type, DescriptionnamestringHow this rule will appear to users.negatebooleanIf true, the rule will fail if the pattern matches.operatorstringRequiredThe operator to use for matching.Can be one of:starts_with,ends_with,contains,regexpatternstringRequiredThe pattern to match with. |
| Name, Type, Description |
| typestringRequiredValue:commit_author_email_pattern |
| parametersobject |
| Name, Type, DescriptionnamestringHow this rule will appear to users.negatebooleanIf true, the rule will fail if the pattern matches.operatorstringRequiredThe operator to use for matching.Can be one of:starts_with,ends_with,contains,regexpatternstringRequiredThe pattern to match with. |
| Name, Type, Description |
| namestringHow this rule will appear to users. |
| negatebooleanIf true, the rule will fail if the pattern matches. |
| operatorstringRequiredThe operator to use for matching.Can be one of:starts_with,ends_with,contains,regex |
| patternstringRequiredThe pattern to match with. |
| committer_email_patternobjectParameters to be used for the committer_email_pattern rule |
| Name, Type, DescriptiontypestringRequiredValue:committer_email_patternparametersobjectName, Type, DescriptionnamestringHow this rule will appear to users.negatebooleanIf true, the rule will fail if the pattern matches.operatorstringRequiredThe operator to use for matching.Can be one of:starts_with,ends_with,contains,regexpatternstringRequiredThe pattern to match with. |
| Name, Type, Description |
| typestringRequiredValue:committer_email_pattern |
| parametersobject |
| Name, Type, DescriptionnamestringHow this rule will appear to users.negatebooleanIf true, the rule will fail if the pattern matches.operatorstringRequiredThe operator to use for matching.Can be one of:starts_with,ends_with,contains,regexpatternstringRequiredThe pattern to match with. |
| Name, Type, Description |
| namestringHow this rule will appear to users. |
| negatebooleanIf true, the rule will fail if the pattern matches. |
| operatorstringRequiredThe operator to use for matching.Can be one of:starts_with,ends_with,contains,regex |
| patternstringRequiredThe pattern to match with. |
| branch_name_patternobjectParameters to be used for the branch_name_pattern rule |
| Name, Type, DescriptiontypestringRequiredValue:branch_name_patternparametersobjectName, Type, DescriptionnamestringHow this rule will appear to users.negatebooleanIf true, the rule will fail if the pattern matches.operatorstringRequiredThe operator to use for matching.Can be one of:starts_with,ends_with,contains,regexpatternstringRequiredThe pattern to match with. |
| Name, Type, Description |
| typestringRequiredValue:branch_name_pattern |
| parametersobject |
| Name, Type, DescriptionnamestringHow this rule will appear to users.negatebooleanIf true, the rule will fail if the pattern matches.operatorstringRequiredThe operator to use for matching.Can be one of:starts_with,ends_with,contains,regexpatternstringRequiredThe pattern to match with. |
| Name, Type, Description |
| namestringHow this rule will appear to users. |
| negatebooleanIf true, the rule will fail if the pattern matches. |
| operatorstringRequiredThe operator to use for matching.Can be one of:starts_with,ends_with,contains,regex |
| patternstringRequiredThe pattern to match with. |
| tag_name_patternobjectParameters to be used for the tag_name_pattern rule |
| Name, Type, DescriptiontypestringRequiredValue:tag_name_patternparametersobjectName, Type, DescriptionnamestringHow this rule will appear to users.negatebooleanIf true, the rule will fail if the pattern matches.operatorstringRequiredThe operator to use for matching.Can be one of:starts_with,ends_with,contains,regexpatternstringRequiredThe pattern to match with. |
| Name, Type, Description |
| typestringRequiredValue:tag_name_pattern |
| parametersobject |
| Name, Type, DescriptionnamestringHow this rule will appear to users.negatebooleanIf true, the rule will fail if the pattern matches.operatorstringRequiredThe operator to use for matching.Can be one of:starts_with,ends_with,contains,regexpatternstringRequiredThe pattern to match with. |
| Name, Type, Description |
| namestringHow this rule will appear to users. |
| negatebooleanIf true, the rule will fail if the pattern matches. |
| operatorstringRequiredThe operator to use for matching.Can be one of:starts_with,ends_with,contains,regex |
| patternstringRequiredThe pattern to match with. |
| file_path_restrictionobjectPrevent commits that include changes in specified file and folder paths from being pushed to the commit graph. This includes absolute paths that contain file names. |
| Name, Type, DescriptiontypestringRequiredValue:file_path_restrictionparametersobjectName, Type, Descriptionrestricted_file_pathsarray of stringsRequiredThe file paths that are restricted from being pushed to the commit graph. |
| Name, Type, Description |
| typestringRequiredValue:file_path_restriction |
| parametersobject |
| Name, Type, Descriptionrestricted_file_pathsarray of stringsRequiredThe file paths that are restricted from being pushed to the commit graph. |
| Name, Type, Description |
| restricted_file_pathsarray of stringsRequiredThe file paths that are restricted from being pushed to the commit graph. |
| max_file_path_lengthobjectPrevent commits that include file paths that exceed the specified character limit from being pushed to the commit graph. |
| Name, Type, DescriptiontypestringRequiredValue:max_file_path_lengthparametersobjectName, Type, Descriptionmax_file_path_lengthintegerRequiredThe maximum amount of characters allowed in file paths. |
| Name, Type, Description |
| typestringRequiredValue:max_file_path_length |
| parametersobject |
| Name, Type, Descriptionmax_file_path_lengthintegerRequiredThe maximum amount of characters allowed in file paths. |
| Name, Type, Description |
| max_file_path_lengthintegerRequiredThe maximum amount of characters allowed in file paths. |
| file_extension_restrictionobjectPrevent commits that include files with specified file extensions from being pushed to the commit graph. |
| Name, Type, DescriptiontypestringRequiredValue:file_extension_restrictionparametersobjectName, Type, Descriptionrestricted_file_extensionsarray of stringsRequiredThe file extensions that are restricted from being pushed to the commit graph. |
| Name, Type, Description |
| typestringRequiredValue:file_extension_restriction |
| parametersobject |
| Name, Type, Descriptionrestricted_file_extensionsarray of stringsRequiredThe file extensions that are restricted from being pushed to the commit graph. |
| Name, Type, Description |
| restricted_file_extensionsarray of stringsRequiredThe file extensions that are restricted from being pushed to the commit graph. |
| max_file_sizeobjectPrevent commits with individual files that exceed the specified limit from being pushed to the commit graph. |
| Name, Type, DescriptiontypestringRequiredValue:max_file_sizeparametersobjectName, Type, Descriptionmax_file_sizeintegerRequiredThe maximum file size allowed in megabytes. This limit does not apply to Git Large File Storage (Git LFS). |
| Name, Type, Description |
| typestringRequiredValue:max_file_size |
| parametersobject |
| Name, Type, Descriptionmax_file_sizeintegerRequiredThe maximum file size allowed in megabytes. This limit does not apply to Git Large File Storage (Git LFS). |
| Name, Type, Description |
| max_file_sizeintegerRequiredThe maximum file size allowed in megabytes. This limit does not apply to Git Large File Storage (Git LFS). |
| workflowsobjectRequire all changes made to a targeted branch to pass the specified workflows before they can be merged. |
| Name, Type, DescriptiontypestringRequiredValue:workflowsparametersobjectName, Type, Descriptiondo_not_enforce_on_createbooleanAllow repositories and branches to be created if a check would otherwise prohibit it.workflowsarray of objectsRequiredWorkflows that must pass for this rule to pass.Name, Type, DescriptionpathstringRequiredThe path to the workflow filerefstringThe ref (branch or tag) of the workflow file to userepository_idintegerRequiredThe ID of the repository where the workflow is definedshastringThe commit SHA of the workflow file to use |
| Name, Type, Description |
| typestringRequiredValue:workflows |
| parametersobject |
| Name, Type, Descriptiondo_not_enforce_on_createbooleanAllow repositories and branches to be created if a check would otherwise prohibit it.workflowsarray of objectsRequiredWorkflows that must pass for this rule to pass.Name, Type, DescriptionpathstringRequiredThe path to the workflow filerefstringThe ref (branch or tag) of the workflow file to userepository_idintegerRequiredThe ID of the repository where the workflow is definedshastringThe commit SHA of the workflow file to use |
| Name, Type, Description |
| do_not_enforce_on_createbooleanAllow repositories and branches to be created if a check would otherwise prohibit it. |
| workflowsarray of objectsRequiredWorkflows that must pass for this rule to pass. |
| Name, Type, DescriptionpathstringRequiredThe path to the workflow filerefstringThe ref (branch or tag) of the workflow file to userepository_idintegerRequiredThe ID of the repository where the workflow is definedshastringThe commit SHA of the workflow file to use |
| Name, Type, Description |
| pathstringRequiredThe path to the workflow file |
| refstringThe ref (branch or tag) of the workflow file to use |
| repository_idintegerRequiredThe ID of the repository where the workflow is defined |
| shastringThe commit SHA of the workflow file to use |
| code_scanningobjectChoose which tools must provide code scanning results before the reference is updated. When configured, code scanning must be enabled and have results for both the commit and the reference being updated. |
| Name, Type, DescriptiontypestringRequiredValue:code_scanningparametersobjectName, Type, Descriptioncode_scanning_toolsarray of objectsRequiredTools that must provide code scanning results for this rule to pass.Name, Type, Descriptionalerts_thresholdstringRequiredThe severity level at which code scanning results that raise alerts block a reference update. For more information on alert severity levels, see "About code scanning alerts."Can be one of:none,errors,errors_and_warnings,allsecurity_alerts_thresholdstringRequiredThe severity level at which code scanning results that raise security alerts block a reference update. For more information on security severity levels, see "About code scanning alerts."Can be one of:none,critical,high_or_higher,medium_or_higher,alltoolstringRequiredThe name of a code scanning tool |
| Name, Type, Description |
| typestringRequiredValue:code_scanning |
| parametersobject |
| Name, Type, Descriptioncode_scanning_toolsarray of objectsRequiredTools that must provide code scanning results for this rule to pass.Name, Type, Descriptionalerts_thresholdstringRequiredThe severity level at which code scanning results that raise alerts block a reference update. For more information on alert severity levels, see "About code scanning alerts."Can be one of:none,errors,errors_and_warnings,allsecurity_alerts_thresholdstringRequiredThe severity level at which code scanning results that raise security alerts block a reference update. For more information on security severity levels, see "About code scanning alerts."Can be one of:none,critical,high_or_higher,medium_or_higher,alltoolstringRequiredThe name of a code scanning tool |
| Name, Type, Description |
| code_scanning_toolsarray of objectsRequiredTools that must provide code scanning results for this rule to pass. |
| Name, Type, Descriptionalerts_thresholdstringRequiredThe severity level at which code scanning results that raise alerts block a reference update. For more information on alert severity levels, see "About code scanning alerts."Can be one of:none,errors,errors_and_warnings,allsecurity_alerts_thresholdstringRequiredThe severity level at which code scanning results that raise security alerts block a reference update. For more information on security severity levels, see "About code scanning alerts."Can be one of:none,critical,high_or_higher,medium_or_higher,alltoolstringRequiredThe name of a code scanning tool |
| Name, Type, Description |
| alerts_thresholdstringRequiredThe severity level at which code scanning results that raise alerts block a reference update. For more information on alert severity levels, see "About code scanning alerts."Can be one of:none,errors,errors_and_warnings,all |
| security_alerts_thresholdstringRequiredThe severity level at which code scanning results that raise security alerts block a reference update. For more information on security severity levels, see "About code scanning alerts."Can be one of:none,critical,high_or_higher,medium_or_higher,all |
| toolstringRequiredThe name of a code scanning tool |
| copilot_code_reviewobjectRequest Copilot code review for new pull requests automatically if the author has access to Copilot code review and their premium requests quota has not reached the limit. |
| Name, Type, DescriptiontypestringRequiredValue:copilot_code_reviewparametersobjectName, Type, Descriptionreview_draft_pull_requestsbooleanCopilot automatically reviews draft pull requests before they are marked as ready for review.review_on_pushbooleanCopilot automatically reviews each new push to the pull request. |
| Name, Type, Description |
| typestringRequiredValue:copilot_code_review |
| parametersobject |
| Name, Type, Descriptionreview_draft_pull_requestsbooleanCopilot automatically reviews draft pull requests before they are marked as ready for review.review_on_pushbooleanCopilot automatically reviews each new push to the pull request. |
| Name, Type, Description |
| review_draft_pull_requestsbooleanCopilot automatically reviews draft pull requests before they are marked as ready for review. |
| review_on_pushbooleanCopilot automatically reviews each new push to the pull request. |

### HTTP response status codes for "Update a repository ruleset"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |
| 500 | Internal Error |

### Code samples for "Update a repository ruleset"

#### Request example

put/repos/{owner}/{repo}/rulesets/{ruleset_id}

-
-
-

`curl -L \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/rulesets/RULESET_ID \
  -d '{"name":"super cool ruleset","target":"branch","enforcement":"active","bypass_actors":[{"actor_id":234,"actor_type":"Team","bypass_mode":"always"}],"conditions":{"ref_name":{"include":["refs/heads/main","refs/heads/master"],"exclude":["refs/heads/dev*"]}},"rules":[{"type":"commit_author_email_pattern","parameters":{"operator":"contains","pattern":"github"}}]}'`

Response

-
-

`Status: 200``{
"id": 42,
"name": "super cool ruleset",
"target": "branch",
"source_type": "Repository",
"source": "monalisa/my-repo",
"enforcement": "active",
"bypass_actors": [
{
"actor_id": 234,
"actor_type": "Team",
"bypass_mode": "always"
}
],
"conditions": {
"ref_name": {
"include": [
"refs/heads/main",
"refs/heads/master"
],
"exclude": [
"refs/heads/dev*"
]
}
},
"rules": [
{
"type": "commit_author_email_pattern",
"parameters": {
"operator": "contains",
"pattern": "github"
}
}
],
"node_id": "RRS_lACkVXNlcgQB",
"_links": {
"self": {
"href": "https://api.github.com/repos/monalisa/my-repo/rulesets/42"
},
"html": {
"href": "https://github.com/monalisa/my-repo/rules/42"
}
},
"created_at": "2023-07-15T08:43:03Z",
"updated_at": "2023-08-23T16:29:47Z"
}`

## Delete a repository ruleset

Delete a ruleset for a repository.

### Fine-grained access tokens for "Delete a repository ruleset"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Delete a repository ruleset"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| ruleset_idintegerRequiredThe ID of the ruleset. |

### HTTP response status codes for "Delete a repository ruleset"

| Status code | Description |
| --- | --- |
| 204 | No Content |
| 404 | Resource not found |
| 500 | Internal Error |

### Code samples for "Delete a repository ruleset"

#### Request example

delete/repos/{owner}/{repo}/rulesets/{ruleset_id}

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/rulesets/RULESET_ID`

Response

`Status: 204`

## Get repository ruleset history

Get the history of a repository ruleset.

### Fine-grained access tokens for "Get repository ruleset history"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Get repository ruleset history"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| ruleset_idintegerRequiredThe ID of the ruleset. |

| Name, Type, Description |
| --- |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| pageintegerThe page number of the results to fetch. For more information, see "Using pagination in the REST API."Default:1 |

### HTTP response status codes for "Get repository ruleset history"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |
| 500 | Internal Error |

### Code samples for "Get repository ruleset history"

#### Request example

get/repos/{owner}/{repo}/rulesets/{ruleset_id}/history

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/rulesets/RULESET_ID/history`

Response

-
-

`Status: 200``[
{
"version_id": 3,
"actor": {
"id": 1,
"type": "User"
},
"updated_at": "2024-010-23T16:29:47Z"
},
{
"version_id": 2,
"actor": {
"id": 2,
"type": "User"
},
"updated_at": "2024-09-23T16:29:47Z"
},
{
"version_id": 1,
"actor": {
"id": 1,
"type": "User"
},
"updated_at": "2024-08-23T16:29:47Z"
}
]`

## Get repository ruleset version

Get a version of a repository ruleset.

### Fine-grained access tokens for "Get repository ruleset version"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Administration" repository permissions (write)

### Parameters for "Get repository ruleset version"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| ownerstringRequiredThe account owner of the repository. The name is not case sensitive. |
| repostringRequiredThe name of the repository without the.gitextension. The name is not case sensitive. |
| ruleset_idintegerRequiredThe ID of the ruleset. |
| version_idintegerRequiredThe ID of the version |

### HTTP response status codes for "Get repository ruleset version"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |
| 500 | Internal Error |

### Code samples for "Get repository ruleset version"

#### Request example

get/repos/{owner}/{repo}/rulesets/{ruleset_id}/history/{version_id}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/rulesets/RULESET_ID/history/VERSION_ID`

Response

-
-

`Status: 200``[
{
"version_id": 3,
"actor": {
"id": 1,
"type": "User"
},
"updated_at": "2024-010-23T16:29:47Z",
"state": {
"id": 42,
"name": "super cool ruleset",
"target": "branch",
"source_type": "Repository",
"source": "monalisa/my-repo",
"enforcement": "active",
"bypass_actors": [
{
"actor_id": 234,
"actor_type": "Team",
"bypass_mode": "always"
}
],
"conditions": {
"ref_name": {
"include": [
"refs/heads/main",
"refs/heads/master"
],
"exclude": [
"refs/heads/dev*"
]
}
},
"rules": [
{
"type": "commit_author_email_pattern",
"parameters": {
"operator": "contains",
"pattern": "github"
}
}
]
}
}
]`
