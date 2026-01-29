# The Django source code repository¶ and more

# The Django source code repository¶

# The Django source code repository¶

When deploying a Django application into a real production environment, you
will almost always want to use [an official packaged release of Django](https://www.djangoproject.com/download/).

However, if you’d like to try out in-development code from an upcoming release
or contribute to the development of Django, you’ll need to obtain a clone of
Django’s source code repository.

This document covers the way the code repository is laid out and how to work
with and find things in it.

## High-level overview¶

The Django source code repository uses [Git](https://git-scm.com/) to track changes to the code
over time, so you’ll need a copy of the Git client (a program called `git`)
on your computer, and you’ll want to familiarize yourself with the basics of
how Git works.

Git’s website offers downloads for various operating systems. The site also
contains vast amounts of [documentation](https://git-scm.com/doc).

The Django Git repository is located online at [github.com/django/django](https://github.com/django/django). It contains the full source code for all
Django releases, which you can browse online.

The Git repository includes several [branches](https://github.com/django/django/branches):

- `main` contains the main in-development code which will become
  the next packaged release of Django. This is where most development
  activity is focused.
- `stable/A.B.x` are the branches where release preparation work happens.
  They are also used for bugfix and security releases which occur as necessary
  after the initial release of a feature version.

The Git repository also contains [tags](https://github.com/django/django/tags). These are the exact revisions from
which packaged Django releases were produced, since version 1.0.

A number of tags also exist under the `archive/` prefix for [archived
work](#archived-feature-development-work).

The source code for the [Djangoproject.com](https://www.djangoproject.com/)
website can be found at [github.com/django/djangoproject.com](https://github.com/django/djangoproject.com).

## The main branch¶

If you’d like to try out the in-development code for the next release of
Django, or if you’d like to contribute to Django by fixing bugs or developing
new features, you’ll want to get the code from the main branch.

Note

Prior to March 2021, the main branch was called `master`.

Note that this will get *all* of Django: in addition to the top-level
`django` module containing Python code, you’ll also get a copy of Django’s
documentation, test suite, packaging scripts and other miscellaneous bits.
Django’s code will be present in your clone as a directory named
`django`.

To try out the in-development code with your own applications, place the
directory containing your clone on your Python import path. Then `import`
statements which look for Django will find the `django` module within your
clone.

If you’re going to be working on Django’s code (say, to fix a bug or
develop a new feature), you can probably stop reading here and move
over to [the documentation for contributing to Django](https://docs.djangoproject.com/en/5.0/contributing/), which covers things like the preferred
coding style and how to generate and submit a patch.

## Stable branches¶

Django uses branches to prepare for releases of Django. Each major release
series has its own stable branch.

These branches can be found in the repository as `stable/A.B.x`
branches and will be created right after the first alpha is tagged.

For example, immediately after *Django 1.5 alpha 1* was tagged, the branch
`stable/1.5.x` was created and all further work on preparing the code for the
final 1.5 release was done there.

These branches also provide bugfix and security support as described in
[Supported versions](https://docs.djangoproject.com/en/5.0/release-process/#supported-versions-policy).

For example, after the release of Django 1.5, the branch `stable/1.5.x`
receives only fixes for security and critical stability bugs, which are
eventually released as Django 1.5.1 and so on, `stable/1.4.x` receives only
security and data loss fixes, and `stable/1.3.x` no longer receives any
updates.

Historical information

This policy for handling `stable/A.B.x` branches was adopted starting
with the Django 1.5 release cycle.

Previously, these branches weren’t created until right after the releases
and the stabilization work occurred on the main repository branch. Thus,
no new feature development work for the next release of Django could be
committed until the final release happened.

For example, shortly after the release of Django 1.3 the branch
`stable/1.3.x` was created. Official support for that release has expired,
and so it no longer receives direct maintenance from the Django project.
However, that and all other similarly named branches continue to exist, and
interested community members have occasionally used them to provide
unofficial support for old Django releases.

## Tags¶

Each Django release is tagged and signed by the releaser.

The tags can be found on GitHub’s [tags](https://github.com/django/django/tags) page.

### Archived feature-development work¶

Historical information

Since Django moved to Git in 2012, anyone can clone the repository and
create their own branches, alleviating the need for official branches in
the source code repository.

The following section is mostly useful if you’re exploring the repository’s
history, for example if you’re trying to understand how some features were
designed.

Feature-development branches tend by their nature to be temporary. Some
produce successful features which are merged back into Django’s main branch to
become part of an official release, but others do not; in either case, there
comes a time when the branch is no longer being actively worked on by any
developer. At this point the branch is considered closed.

Django used to be maintained with the Subversion revision control system, that
has no standard way of indicating this. As a workaround, branches of Django
which are closed and no longer maintained were moved into `attic`.

A number of tags exist under the `archive/` prefix to maintain a reference to
this and other work of historical interest.

The following tags under the `archive/attic/` prefix reference the tip of
branches whose code eventually became part of Django itself:

- `boulder-oracle-sprint`: Added support for Oracle databases to
  Django’s object-relational mapper. This has been part of Django
  since the 1.0 release.
- `gis`: Added support for geographic/spatial queries to Django’s
  object-relational mapper. This has been part of Django since the 1.0
  release, as the bundled application `django.contrib.gis`.
- `i18n`: Added [internationalization support](https://docs.djangoproject.com/en/topics/i18n/) to
  Django. This has been part of Django since the 0.90 release.
- `magic-removal`: A major refactoring of both the internals and
  public APIs of Django’s object-relational mapper. This has been part
  of Django since the 0.95 release.
- `multi-auth`: A refactoring of [Django’s bundled
  authentication framework](https://docs.djangoproject.com/en/topics/auth/) which added support for
  [authentication backends](https://docs.djangoproject.com/en/topics/auth/customizing/#authentication-backends). This has
  been part of Django since the 0.95 release.
- `new-admin`: A refactoring of [Django’s bundled
  administrative application](https://docs.djangoproject.com/en/ref/contrib/admin/). This became part of
  Django as of the 0.91 release, but was superseded by another
  refactoring (see next listing) prior to the Django 1.0 release.
- `newforms-admin`: The second refactoring of Django’s bundled
  administrative application. This became part of Django as of the 1.0
  release, and is the basis of the current incarnation of
  `django.contrib.admin`.
- `queryset-refactor`: A refactoring of the internals of Django’s
  object-relational mapper. This became part of Django as of the 1.0
  release.
- `unicode`: A refactoring of Django’s internals to consistently use
  Unicode-based strings in most places within Django and Django
  applications. This became part of Django as of the 1.0 release.

Additionally, the following tags under the `archive/attic/` prefix reference
the tips of branches that were closed, but whose code was never merged into
Django, and the features they aimed to implement were never finished:

- `full-history`
- `generic-auth`
- `multiple-db-support`
- `per-object-permissions`
- `schema-evolution`
- `schema-evolution-ng`
- `search-api`
- `sqlalchemy`

Finally, under the `archive/` prefix, the repository contains
`soc20XX/<project>` tags referencing the tip of branches that were used by
students who worked on Django during the 2009 and 2010 Google Summer of Code
programs.

---

# Mailing lists and Forum¶

# Mailing lists and Forum¶

Important

Please report security issues **only** to
[security@djangoproject.com](mailto:security%40djangoproject.com).  This is a private list only open to
long-time, highly trusted Django developers, and its archives are
not public. For further details, please see [our security
policies](https://docs.djangoproject.com/en/5.0/security/).

## Django Forum¶

Django has an [official Forum](https://forum.djangoproject.com) where you can input and ask questions.

There are several categories of discussion including:

- [Using Django](https://forum.djangoproject.com/c/users/6): to ask any question regarding the installation, usage, or
  debugging of Django.
- [Internals](https://forum.djangoproject.com/c/internals/5): for discussion of the development of Django itself.

In addition, Django has several official mailing lists on Google Groups that
are open to anyone.

## django-users¶

Note

The [Using Django](https://forum.djangoproject.com/c/users/6) category of the [official Forum](https://forum.djangoproject.com) is now the preferred
venue for asking usage questions.

This is the right place if you are looking to ask any question regarding the
installation, usage, or debugging of Django.

Note

If it’s the first time you send an email to this list, your email must be
accepted first so don’t worry if [your message does not appear](https://docs.djangoproject.com/en/faq/help/#message-does-not-appear-on-django-users) instantly.

- [django-users mailing archive](https://groups.google.com/g/django-users)
- [django-users subscription email address](mailto:django-users+subscribe%40googlegroups.com)
- [django-users posting email](mailto:django-users%40googlegroups.com)

## django-developers¶

Note

The [Internals](https://forum.djangoproject.com/c/internals/5) category of the [official Forum](https://forum.djangoproject.com) is now the preferred
venue for discussing the development of Django.

The discussion about the development of Django itself takes place here.

Before asking a question about how to contribute, read
[Contributing to Django](https://docs.djangoproject.com/en/5.0/contributing/). Many frequently asked questions are
answered there.

Note

Please make use of
[django-users mailing list](#django-users-mailing-list) if you want
to ask for tech support, doing so in this list is inappropriate.

- [django-developers mailing archive](https://groups.google.com/g/django-developers)
- [django-developers subscription email address](mailto:django-developers+subscribe%40googlegroups.com)
- [django-developers posting email](mailto:django-developers%40googlegroups.com)

## django-announce¶

A (very) low-traffic list for announcing [upcoming security releases](https://docs.djangoproject.com/en/5.0/security/#security-disclosure), new releases of Django, and security advisories.

- [django-announce mailing archive](https://groups.google.com/g/django-announce)
- [django-announce subscription email address](mailto:django-announce+subscribe%40googlegroups.com)
- [django-announce posting email](mailto:django-announce%40googlegroups.com)

## django-updates¶

All the ticket updates are mailed automatically to this list, which is tracked
by developers and interested community members.

- [django-updates mailing archive](https://groups.google.com/g/django-updates)
- [django-updates subscription email address](mailto:django-updates+subscribe%40googlegroups.com)
- [django-updates posting email](mailto:django-updates%40googlegroups.com)

---

# Organization of the Django Project¶

# Organization of the Django Project¶

## Principles¶

The Django Project is managed by a team of volunteers pursuing three goals:

- Driving the development of the Django web framework,
- Fostering the ecosystem of Django-related software,
- Leading the Django community in accordance with the values described in the
  [Django Code of Conduct](https://www.djangoproject.com/conduct/).

The Django Project isn’t a legal entity. The [Django Software Foundation](https://www.djangoproject.com/foundation/), a
non-profit organization, handles financial and legal matters related to the
Django Project. Other than that, the Django Software Foundation lets the
Django Project manage the development of the Django framework, its ecosystem
and its community.

## Mergers¶

### Role¶

[Mergers](https://www.djangoproject.com/foundation/teams/#mergers-team) are a small set of people who merge pull requests to the [Django Git
repository](https://github.com/django/django/).

### Prerogatives¶

Mergers hold the following prerogatives:

- Merging any pull request which constitutes a [minor change](https://github.com/django/deps/blob/main/final/0010-new-governance.rst#terminology) (small enough
  not to require the use of the [DEP process](https://github.com/django/deps/blob/main/final/0001-dep-process.rst)). A Merger must not merge a
  change primarily authored by that Merger, unless the pull request has been
  approved by:
  - another Merger,
  - a steering council member,
  - a member of the [triage & review team](https://www.djangoproject.com/foundation/teams/#triage-review-team), or
  - a member of the [security team](https://www.djangoproject.com/foundation/teams/#security-team).
- Initiating discussion of a minor change in the appropriate venue, and request
  that other Mergers refrain from merging it while discussion proceeds.
- Requesting a vote of the steering council regarding any minor change if, in
  the Merger’s opinion, discussion has failed to reach a consensus.
- Requesting a vote of the steering council when a [major change](https://github.com/django/deps/blob/main/final/0010-new-governance.rst#terminology) (significant
  enough to require the use of the [DEP process](https://github.com/django/deps/blob/main/final/0001-dep-process.rst)) reaches one of its
  implementation milestones and is intended to merge.

### Membership¶

[The steering council](https://www.djangoproject.com/foundation/teams/#steering-council-team) selects [Mergers](https://www.djangoproject.com/foundation/teams/#mergers-team) as necessary to maintain their number
at a minimum of three, in order to spread the workload and avoid over-burdening
or burning out any individual Merger. There is no upper limit to the number of
Mergers.

It’s not a requirement that a Merger is also a Django Fellow, but the Django
Software Foundation has the power to use funding of Fellow positions as a way
to make the role of Merger sustainable.

The following restrictions apply to the role of Merger:

- A person must not simultaneously serve as a member of the steering council. If
  a Merger is elected to the steering council, they shall cease to be a Merger
  immediately upon taking up membership in the steering council.
- A person may serve in the roles of Releaser and Merger simultaneously.

The selection process, when a vacancy occurs or when the steering council deems
it necessary to select additional persons for such a role, occur as follows:

- Any member in good standing of an appropriate discussion venue, or the Django
  Software Foundation board acting with the input of the DSF’s Fellowship
  committee, may suggest a person for consideration.
- The steering council considers the suggestions put forth, and then any member
  of the steering council formally nominates a candidate for the role.
- The steering council votes on nominees.

Mergers may resign their role at any time, but should endeavor to provide some
advance notice in order to allow the selection of a replacement. Termination of
the contract of a Django Fellow by the Django Software Foundation temporarily
suspends that person’s Merger role until such time as the steering council can
vote on their nomination.

Otherwise, a Merger may be removed by:

- Becoming disqualified due to election to the steering council.
- Becoming disqualified due to actions taken by the Code of Conduct committee
  of the Django Software Foundation.
- A vote of the steering council.

## Releasers¶

### Role¶

[Releasers](https://www.djangoproject.com/foundation/teams/#releasers-team) are a small set of people who have the authority to upload packaged
releases of Django to the [Python Package Index](https://pypi.org/project/Django/) and to the
[djangoproject.com](https://www.djangoproject.com/download/) website.

### Prerogatives¶

[Releasers](https://www.djangoproject.com/foundation/teams/#releasers-team) [build Django releases](https://docs.djangoproject.com/en/5.0/howto-release-django/) and
upload them to the [Python Package Index](https://pypi.org/project/Django/) and to the
[djangoproject.com](https://www.djangoproject.com/download/) website.

### Membership¶

[The steering council](https://www.djangoproject.com/foundation/teams/#steering-council-team) selects [Releasers](https://www.djangoproject.com/foundation/teams/#releasers-team) as necessary to maintain their number
at a minimum of three, in order to spread the workload and avoid over-burdening
or burning out any individual Releaser. There is no upper limit to the number
of Releasers.

It’s not a requirement that a Releaser is also a Django Fellow, but the Django
Software Foundation has the power to use funding of Fellow positions as a way
to make the role of Releaser sustainable.

A person may serve in the roles of Releaser and Merger simultaneously.

The selection process, when a vacancy occurs or when the steering council deems
it necessary to select additional persons for such a role, occur as follows:

- Any member in good standing of an appropriate discussion venue, or the Django
  Software Foundation board acting with the input of the DSF’s Fellowship
  committee, may suggest a person for consideration.
- The steering council considers the suggestions put forth, and then any member
  of the steering council formally nominates a candidate for the role.
- The steering council votes on nominees.

Releasers may resign their role at any time, but should endeavor to provide
some advance notice in order to allow the selection of a replacement.
Termination of the contract of a Django Fellow by the Django Software
Foundation temporarily suspends that person’s Releaser role until such time as
the steering council can vote on their nomination.

Otherwise, a Releaser may be removed by:

- Becoming disqualified due to actions taken by the Code of Conduct committee
  of the Django Software Foundation.
- A vote of the steering council.

## Steering council¶

### Role¶

The steering council is a group of experienced contributors who:

- provide oversight of Django’s development and release process,
- assist in setting the direction of feature development and releases,
- take part in filling certain roles, and
- have a tie-breaking vote when other decision-making processes fail.

Their main concern is to maintain the quality and stability of the Django Web
Framework.

### Prerogatives¶

The steering council holds the following prerogatives:

- Making a binding decision regarding any question of a technical change to
  Django.
- Vetoing the merging of any particular piece of code into Django or ordering
  the reversion of any particular merge or commit.
- Announcing calls for proposals and ideas for the future technical direction
  of Django.
- Setting and adjusting the schedule of releases of Django.
- Selecting and removing mergers and releasers.
- Participating in the removal of members of the steering council, when deemed
  appropriate.
- Calling elections of the steering council outside of those which are
  automatically triggered, at times when the steering council deems an election
  is appropriate.
- Participating in modifying Django’s governance (see
  [Changing the organization](#organization-change)).
- Declining to vote on a matter the steering council feels is unripe for a
  binding decision, or which the steering council feels is outside the scope of
  its powers.
- Taking charge of the governance of other technical teams within the Django
  open-source project, and governing those teams accordingly.

### Membership¶

[The steering council](https://www.djangoproject.com/foundation/teams/#steering-council-team) is an elected group of five experienced contributors
who demonstrate:

- A history of substantive contributions to Django or the Django ecosystem.
  This history must begin at least 18 months prior to the individual’s
  candidacy for the Steering Council, and include substantive contributions in
  at least two of these bullet points:
  - Code contributions on Django projects or major third-party packages in the Django ecosystem
  - Reviewing pull requests and/or triaging Django project tickets
  - Documentation, tutorials or blog posts
  - Discussions about Django on the django-developers mailing list or the Django Forum
  - Running Django-related events or user groups
- A history of engagement with the direction and future of Django. This does
  not need to be recent, but candidates who have not engaged in the past three
  years must still demonstrate an understanding of Django’s changes and
  direction within those three years.

A new council is elected after each release cycle of Django. The election process
works as follows:

1. The steering council directs one of its members to notify the Secretary of the
  Django Software Foundation, in writing, of the triggering of the election,
  and the condition which triggered it. The Secretary post to the appropriate
  venue – the [django-developers](https://docs.djangoproject.com/en/5.0/mailing-lists/#django-developers-mailing-list) mailing list and the [Django forum](https://forum.djangoproject.com/) to
  announce the election and its timeline.
2. As soon as the election is announced, the [DSF Board](https://www.djangoproject.com/foundation/#board) begin a period of
  voter registration. All [individual members of the DSF](https://www.djangoproject.com/foundation/individual-members/) are automatically
  registered and need not explicitly register. All other persons who believe
  themselves eligible to vote, but who have not yet registered to vote, may
  make an application to the DSF Board for voting privileges. The voter
  registration form and roll of voters is maintained by the DSF Board. The DSF
  Board may challenge and reject the registration of voters it believes are
  registering in bad faith or who it believes have falsified their
  qualifications or are otherwise unqualified.
3. Registration of voters close one week after the announcement of the
  election. At that point, registration of candidates begin. Any qualified
  person may register as a candidate. The candidate registration form and
  roster of candidates are maintained by the DSF Board, and candidates must
  provide evidence of their qualifications as part of registration. The DSF
  Board may challenge and reject the registration of candidates it believes do
  not meet the qualifications of members of the Steering Council, or who it
  believes are registering in bad faith.
4. Registration of candidates close one week after it has opened. One week
  after registration of candidates closes, the Secretary of the DSF publish
  the roster of candidates to the [django-developers](https://docs.djangoproject.com/en/5.0/mailing-lists/#django-developers-mailing-list) mailing list and the
  [Django forum](https://forum.djangoproject.com/), and the election begin. The DSF Board provide a voting form
  accessible to registered voters, and is the custodian of the votes.
5. Voting is by secret ballot containing the roster of candidates, and any
  relevant materials regarding the candidates, in a randomized order. Each
  voter may vote for up to five candidates on the ballot.
6. The election conclude one week after it begins. The DSF Board then tally the
  votes and produce a summary, including the total number of votes cast and
  the number received by each candidate. This summary is ratified by a
  majority vote of the DSF Board, then posted by the Secretary of the DSF to
  the [django-developers](https://docs.djangoproject.com/en/5.0/mailing-lists/#django-developers-mailing-list) mailing list and the Django Forum. The five
  candidates with the highest vote totals are immediately become the new
  steering council.

A member of the steering council may be removed by:

- Becoming disqualified due to actions taken by the Code of Conduct committee
  of the Django Software Foundation.
- Determining that they did not possess the qualifications of a member of the
  steering council. This determination must be made jointly by the other members
  of the steering council, and the [DSF Board](https://www.djangoproject.com/foundation/#board). A valid determination of
  ineligibility requires that all other members of the steering council and all
  members of the DSF Board vote who can vote on the issue (the affected person,
  if a DSF Board member, must not vote) vote “yes” on a motion that the person
  in question is ineligible.

## Changing the organization¶

Changes to this document require the use of the [DEP process](https://github.com/django/deps/blob/main/final/0001-dep-process.rst), with
modifications described in [DEP 0010](https://github.com/django/deps/blob/main/final/0010-new-governance.rst#changing-this-governance-process).

---

# Django’s release process¶

# Django’s release process¶

## Official releases¶

Since version 1.0, Django’s release numbering works as follows:

- Versions are numbered in the form `A.B` or `A.B.C`.
- `A.B` is the *feature release* version number. Each version will be mostly
  backwards compatible with the previous release. Exceptions to this rule will
  be listed in the release notes.
- `C` is the *patch release* version number, which is incremented for bugfix
  and security releases. These releases will be 100% backwards-compatible with
  the previous patch release. The only exception is when a security or data
  loss issue can’t be fixed without breaking backwards-compatibility. If this
  happens, the release notes will provide detailed upgrade instructions.
- Before a new feature release, we’ll make alpha, beta, and release candidate
  releases. These are of the form `A.B alpha/beta/rc N`, which means the
  `Nth` alpha/beta/release candidate of version `A.B`.

In git, each Django release will have a tag indicating its version number,
signed with the Django release key. Additionally, each release series has its
own branch, called `stable/A.B.x`, and bugfix/security releases will be
issued from those branches.

For more information about how the Django project issues new releases for
security purposes, please see [our security policies](https://docs.djangoproject.com/en/5.0/security/).

  Feature release[¶](#term-Feature-release)

Feature releases (A.B, A.B+1, etc.) will happen roughly every eight months
– see [release process](#id2) for details. These releases will contain new
features, improvements to existing features, and such.

  Patch release[¶](#term-Patch-release)

Patch releases (A.B.C, A.B.C+1, etc.) will be issued as needed, to fix
bugs and/or security issues.

These releases will be 100% compatible with the associated feature release,
unless this is impossible for security reasons or to prevent data loss.
So the answer to “should I upgrade to the latest patch release?” will always
be “yes.”

  Long-term support release[¶](#term-Long-term-support-release)

Certain feature releases will be designated as long-term support (LTS)
releases. These releases will get security and data loss fixes applied for
a guaranteed period of time, typically three years.

See [the download page](https://www.djangoproject.com/download/) for the releases that have been designated for
long-term support.

## Release cadence¶

Starting with Django 2.0, version numbers will use a loose form of [semantic
versioning](https://semver.org/) such that each version following an LTS will
bump to the next “dot zero” version. For example: 2.0, 2.1, 2.2 (LTS), 3.0,
3.1, 3.2 (LTS), etc.

SemVer makes it easier to see at a glance how compatible releases are with each
other. It also helps to anticipate when compatibility shims will be removed.
It’s not a pure form of SemVer as each feature release will continue to have a
few documented backwards incompatibilities where a deprecation path isn’t
possible or not worth the cost. Also, deprecations started in an LTS release
(X.2) will be dropped in a non-dot-zero release (Y.1) to accommodate our policy
of keeping deprecation shims for at least two feature releases. Read on to the
next section for an example.

## Deprecation policy¶

A feature release may deprecate certain features from previous releases. If a
feature is deprecated in feature release A.x, it will continue to work in all
A.x versions (for all versions of x) but raise warnings. Deprecated features
will be removed in the B.0 release, or B.1 for features deprecated in the last
A.x feature release to ensure deprecations are done over at least 2 feature
releases.

So, for example, if we decided to start the deprecation of a function in
Django 4.2:

- Django 4.2 will contain a backwards-compatible replica of the function which
  will raise a `RemovedInDjango51Warning`.
- Django 5.0 (the version that follows 4.2) will still contain the
  backwards-compatible replica.
- Django 5.1 will remove the feature outright.

The warnings are silent by default. You can turn on display of these warnings
with the `python -Wd` option.

A more generic example:

- X.0
- X.1
- X.2 LTS
- Y.0: Drop deprecation shims added in X.0 and X.1.
- Y.1: Drop deprecation shims added in X.2.
- Y.2 LTS: No deprecation shims dropped (while Y.0 is no longer supported,
  third-party apps need to maintain compatibility back to X.2 LTS to ease
  LTS to LTS upgrades).
- Z.0: Drop deprecation shims added in Y.0 and Y.1.

See also the [Deprecating a feature](https://docs.djangoproject.com/en/5.0/contributing/writing-code/submitting-patches/#deprecating-a-feature) guide.

## Supported versions¶

At any moment in time, Django’s developer team will support a set of releases to
varying levels. See [the supported versions section](https://www.djangoproject.com/download/#supported-versions) of the download
page for the current state of support for each version.

- The current development branch `main` will get new features and bug fixes
  requiring non-trivial refactoring.
- Patches applied to the main branch must also be applied to the last feature
  release branch, to be released in the next patch release of that feature
  series, when they fix critical problems:
  - Security issues.
  - Data loss bugs.
  - Crashing bugs.
  - Major functionality bugs in new features of the latest stable release.
  - Regressions from older versions of Django introduced in the current release
    series.
  The rule of thumb is that fixes will be backported to the last feature
  release for bugs that would have prevented a release in the first place
  (release blockers).
- Security fixes and data loss bugs will be applied to the current main branch,
  the last two feature release branches, and any other supported long-term
  support release branches.
- Documentation fixes generally will be more freely backported to the last
  release branch. That’s because it’s highly advantageous to have the docs for
  the last release be up-to-date and correct, and the risk of introducing
  regressions is much less of a concern.

As a concrete example, consider a moment in time halfway between the release of
Django 5.1 and 5.2. At this point in time:

- Features will be added to the development main branch, to be released as
  Django 5.2.
- Critical bug fixes will be applied to the `stable/5.1.x` branch, and
  released as 5.1.1, 5.1.2, etc.
- Security fixes and bug fixes for data loss issues will be applied to
  `main` and to the `stable/5.1.x`, `stable/5.0.x`, and
  `stable/4.2.x` (LTS) branches. They will trigger the release of `5.1.1`,
  `5.0.5`, `4.2.8`, etc.
- Documentation fixes will be applied to main, and, if easily backported, to
  the latest stable branch, `5.1.x`.

## Release process¶

Django uses a time-based release schedule, with feature releases every eight
months or so.

After each feature release, the release manager will announce a timeline for
the next feature release.

### Release cycle¶

Each release cycle consists of three parts:

#### Phase one: feature proposal¶

The first phase of the release process will include figuring out what major
features to include in the next version. This should include a good deal of
preliminary work on those features – working code trumps grand design.

Major features for an upcoming release will be added to the wiki roadmap page,
e.g. [https://code.djangoproject.com/wiki/Version1.11Roadmap](https://code.djangoproject.com/wiki/Version1.11Roadmap).

#### Phase two: development¶

The second part of the release schedule is the “heads-down” working period.
Using the roadmap produced at the end of phase one, we’ll all work very hard to
get everything on it done.

At the end of phase two, any unfinished features will be postponed until the
next release.

Phase two will culminate with an alpha release. At this point, the
`stable/A.B.x` branch will be forked from `main`.

#### Phase three: bugfixes¶

The last part of a release cycle is spent fixing bugs – no new features will
be accepted during this time. We’ll try to release a beta release one month
after the alpha and a release candidate one month after the beta.

The release candidate marks the string freeze, and it happens at least two
weeks before the final release. After this point, new translatable strings
must not be added.

During this phase, mergers will be more and more conservative with backports,
to avoid introducing regressions. After the release candidate, only release
blockers and documentation fixes should be backported.

In parallel to this phase, `main` can receive new features, to be released
in the `A.B+1` cycle.

### Bug-fix releases¶

After a feature release (e.g. A.B), the previous release will go into bugfix
mode.

The branch for the previous feature release (e.g. `stable/A.B-1.x`) will
include bugfixes. Critical bugs fixed on main must *also* be fixed on the
bugfix branch; this means that commits need to cleanly separate bug fixes from
feature additions. The developer who commits a fix to main will be
responsible for also applying the fix to the current bugfix branch.
