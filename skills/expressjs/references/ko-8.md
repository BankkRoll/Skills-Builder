# Express와 함께 템플리트 엔진 사용 and more

# Express와 함께 템플리트 엔진 사용

> Discover how to integrate and use template engines like Pug, Handlebars, and EJS with Express.js to render dynamic HTML pages efficiently.

# Express와 함께 템플리트 엔진 사용

A *template engine* enables you to use static template files in your application. At runtime, the template engine replaces
variables in a template file with actual values, and transforms the template into an HTML file sent to the client.
This approach makes it easier to design an HTML page.

The [Express application generator](https://expressjs.com/ko/starter/generator.html) uses [Pug](https://pugjs.org/api/getting-started.html) as its default, but it also supports [Handlebars](https://www.npmjs.com/package/handlebars), and [EJS](https://www.npmjs.com/package/ejs), among others.

To render template files, set the following [application setting properties](https://expressjs.com/ko/4x/api.html#app.set), in the default `app.js` created by the generator:

- `views`, 템플리트가 있는 디렉토리. 예: `app.set('views', './views')`
  This defaults to the `views` directory in the application root directory.
- `view engine`, 사용할 템플리트 엔진. 예: `app.set('view engine', 'pug')`

이후 그에 맞는 템플리트 엔진 npm 패키지를 다음과 같이 설치하십시오.

```
$ npm install pug --save
```

Express와 호환되는 템플리트 엔진(예: Pug)은 `__express(filePath, options, callback)`라는 이름의 함수를 내보내며, 이 함수는 `res.render()` 함수에 의해 호출되어 템플리트 코드를 렌더링합니다.

일부 템플리트 엔진은 이러한 방식을 따르지 않습니다. [Consolidate.js](https://www.npmjs.org/package/consolidate) 라이브러리는 널리 이용되고 있는 모든 Node.js 템플리트 엔진을 맵핑함으로써 이러한 방식을 따르므로 Express 내에서 완벽하게 작동합니다.

보기 엔진을 설정한 후에는 앱에서 엔진을 지정하거나 템플리트 엔진 모듈을 로드할 필요가 없으며, Express는 아래에 표시된 것과 같이 내부적으로 모듈을 로드합니다(위의 예에 대한 코드).

```
app.set('view engine', 'pug')
```

다음의 내용이 입력된 `index.pug`라는 이름의 Pug 템플리트를 `views` 디렉토리에 작성하십시오.

```pug
html
  head
    title= title
  body
    h1= message
```

이후 `index.pug` 파일을 렌더링할 라우트를 작성하십시오. `view engine` 특성이 설정되어 있지 않은 경우에는 `view` 파일의 확장자를 지정해야 합니다. 해당 특성이 설정되어 있는 경우에는 확장자를 생략할 수 있습니다.

```
app.get('/', (req, res) => {
  res.render('index', { title: 'Hey', message: 'Hello there!' })
})
```

홈 페이지에 대한 요청을 실행할 때, `index.pug` 파일은 HTML 형식으로 렌더링됩니다.

The view engine cache does not cache the contents of the template’s output, only the underlying template itself. The view is still re-rendered with every request even when the cache is on.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/ko/guide/using-template-engines.md          )

---

# Express 앱에서 사용하기 위한 미들웨어 작성

> Learn how to write custom middleware functions for Express.js applications, including examples and best practices for enhancing request and response handling.

# Express 앱에서 사용하기 위한 미들웨어 작성

## 개요

*Middleware* functions are functions that have access to the [request object](https://expressjs.com/ko/5x/api.html#req) (`req`), the [response object](https://expressjs.com/ko/5x/api.html#res) (`res`), and the `next` function in the application’s request-response cycle. 그 다음의 미들웨어 함수는 일반적으로 `next`라는 이름의 변수로 표시됩니다.

미들웨어 함수는 다음과 같은 태스크를 수행할 수 있습니다.

- 모든 코드를 실행.
- 요청 및 응답 오브젝트에 대한 변경을 실행.
- 요청-응답 주기를 종료.
- 스택 내의 그 다음 미들웨어를 호출.

현재의 미들웨어 함수가 요청-응답 주기를 종료하지 않는 경우에는 `next()`를 호출하여 그 다음 미들웨어 함수에 제어를 전달해야 합니다. 그렇지 않으면 해당 요청은 정지된 채로 방치됩니다.

다음 예시에 미들웨어 함수 호출의 요소가 표시되어 있습니다.

|  | 미들웨어 함수가 적용되는 HTTP 메소드.</tbody>미들웨어 함수가 적용되는 경로(라우트).미들웨어 함수.미들웨어 함수에 대한 콜백 인수(일반적으로 "next"라 불림).HTTPresponseargument to the middleware function, called "res" by convention.HTTPrequestargument to the middleware function, called "req" by convention. |
| --- | --- |

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/ko/guide/writing-middleware.md          )

---

# 커뮤니티

> Connect with the Express.js community, learn about the technical committee, find resources, explore community-contributed modules, and get involved in discussions.

# 커뮤니티

## Technical committee

The Express technical committee meets online every two weeks (as needed) to discuss development and maintenance of Express,
and other issues relevant to the Express project. Each meeting is typically announced in an
[expressjs/discussions issue](https://github.com/expressjs/discussions/issues) with a link to join or view the meeting, which is
open to all observers.

The meetings are recorded; for a list of the recordings, see the [Express.js YouTube channel](https://www.youtube.com/channel/UCYjxjAeH6TRik9Iwy5nXw7g).

Members of the Express technical committee are:

**Active:**

- [@blakeembrey](https://github.com/blakeembrey) - Blake Embrey
- [@crandmck](https://github.com/crandmck) - Rand McKinney
- [@LinusU](https://github.com/LinusU) - Linus Unnebäck
- [@ulisesgascon](https://github.com/ulisesGascon) - Ulises Gascón
- [@sheplu](https://github.com/sheplu) - Jean Burellier
- [@wesleytodd](https://github.com/wesleytodd) - Wes Todd
- [@jonchurch](https://github.com/jonchurch) - Jon Church
- [@ctcpip](https://github.com/ctcpip/) - Chris de Almeida

**Inactive:**

- [@dougwilson](https://github.com/dougwilson) - Douglas Wilson
- [@hacksparrow](https://github.com/hacksparrow) - Hage Yaapa
- [@jonathanong](https://github.com/jonathanong) - jongleberry
- [@niftylettuce](https://github.com/niftylettuce) - niftylettuce
- [@troygoode](https://github.com/troygoode) - Troy Goode

## Express is made of many modules

활기찬 커뮤니티에서는 매우 다양한 확장기능, [미들웨어 모듈](https://expressjs.com/ko/resources/middleware.html)
및 상위 레벨 프레임워크가 개발되어 왔습니다.

Additionally, the Express community maintains modules in these two GitHub orgs:

- [jshttp](https://github.com/jshttp) modules providing useful utility functions; see [Utility modules](https://expressjs.com/ko/resources/utils.html).
- [pillarjs](https://github.com/pillarjs): low-level modules that Express uses internally.

To keep up with what is going on in the whole community, check out the [ExpressJS StatusBoard](https://expressjs.github.io/statusboard/).

## 문제

버그라고 생각되는 현상을 겪었거나, 기능에 대한 요청을 하기 원하는 경우에는
[issue queue](https://github.com/expressjs/express/issues)에서 티켓을 작성하십시오.

## 예제

API 설계에서부터 인증 및 템플리트 엔진 통합에 이르는 모든 주제를 다루는 저장소에서
수십 개의 Express 애플리케이션 [예제](https://github.com/expressjs/express/tree/master/examples)를
확인하십시오.

## Github Discussions

The [GitHub Discussions](https://github.com/expressjs/discussions) section is an excellent space to engage in conversations about the development and maintenance of Express, as well as to share ideas and discuss topics related to its usage.

# Branding of Express.js

## Express.js Logo

Express is a project of the OpenJS Foundation. Please review the [trademark policy](https://trademark-policy.openjsf.org/) for information about permissible use of Express.js logos and marks.

### Logotype

### Logomark

       [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/ko/resources/community.md          )

---

# Contributing to Express

> Find out how to contribute to Express.js, including guidelines for reporting issues, submitting pull requests, becoming a collaborator, and understanding security policies.

# Contributing to Express

### Looking to contribute to Expressjs.com? Clickhere.

Express and the other projects in the [expressjs organization on GitHub](https://github.com/expressjs) are projects of the [OpenJs Foundation](https://openjsf.org/).
These projects are governed under the general policies and guidelines of the Node.js Foundation along with the additional guidelines below.

- [Technical committee](#technical-committee)
- [Community contributing guide](#community-contributing-guide)
- [Collaborator’s guide](#collaborators-guide)
- [Security policies and procedures](#security-policies-and-procedures)

## Technical committee

The Express technical committee consists of active project members, and guides development and maintenance of the Express project. For more information, see [Express Community - Technical committee](https://expressjs.com/ko/resources/community.html#technical-committee).

## Community contributing guide

  SRC: expressjs/discussions docs/GOVERNANCE.md

The goal of this document is to create a contribution process that:

- Encourages new contributions.
- Encourages contributors to remain involved.
- Avoids unnecessary processes and bureaucracy whenever possible.
- Creates a transparent decision making process that makes it clear how
  contributors can be involved in decision making.

### Vocabulary

- A **Contributor** is any individual creating or commenting on an issue or pull request.
- A **Committer** is a subset of contributors who have been given write access to the repository.
- A **Project Captain** is the lead maintainer of a repository.
- A **TC (Technical Committee)** is a group of committers representing the required technical
  expertise to resolve rare disputes.
- A **Triager** is a subset of contributors who have been given triage access to the repository.

### Logging Issues

Log an issue for any question or problem you might have. When in doubt, log an issue, and
any additional policies about what to include will be provided in the responses. The only
exception is security disclosures which should be sent privately.

Committers may direct you to another repository, ask for additional clarifications, and
add appropriate metadata before the issue is addressed.

Please be courteous and respectful. Every participant is expected to follow the
project’s Code of Conduct.

### Contributions

Any change to resources in this repository must be through pull requests. This applies to all changes
to documentation, code, binary files, etc. Even long term committers and TC members must use
pull requests.

No pull request can be merged without being reviewed.

For non-trivial contributions, pull requests should sit for at least 36 hours to ensure that
contributors in other timezones have time to review. Consideration should also be given to
weekends and other holiday periods to ensure active committers all have reasonable time to
become involved in the discussion and review process if they wish.

The default for each contribution is that it is accepted once no committer has an objection.
During a review, committers may also request that a specific contributor who is most versed in a
particular area gives a “LGTM” before the PR can be merged. There is no additional “sign off”
process for contributions to land. Once all issues brought by committers are addressed it can
be landed by any committer.

In the case of an objection being raised in a pull request by another committer, all involved
committers should seek to arrive at a consensus by way of addressing concerns being expressed
by discussion, compromise on the proposed change, or withdrawal of the proposed change.

If a contribution is controversial and committers cannot agree about how to get it to land
or if it should land then it should be escalated to the TC. TC members should regularly
discuss pending contributions in order to find a resolution. It is expected that only a
small minority of issues be brought to the TC for resolution and that discussion and
compromise among committers be the default resolution mechanism.

### Becoming a Triager

Anyone can become a triager! Read more about the process of being a triager in
[the triage process document](https://github.com/expressjs/discussions/blob/master/Triager-Guide.md).

Currently, any existing [organization member](https://github.com/orgs/expressjs/people) can nominate
a new triager. If you are interested in becoming a triager, our best advice is to actively participate
in the community by helping triaging issues and pull requests. As well we recommend
to engage in other community activities like attending the TC meetings, and participating in the Slack
discussions. If you feel ready and have been helping triage some issues, reach out to an active member of the organization to ask if they’d
be willing to support you. If they agree, they can create a pull request to formalize your nomination. In the case of an objection to the nomination, the triage team is responsible for working with the individuals involved and finding a resolution.

You can also reach out to any of the [organization members](https://github.com/orgs/expressjs/people)
if you have questions or need guidance.

### Becoming a Committer

All contributors who have landed significant and valuable contributions should be onboarded in a timely manner,
and added as a committer, and be given write access to the repository.

Committers are expected to follow this policy and continue to send pull requests, go through
proper review, and have other committers merge their pull requests.

### TC Process

The TC uses a “consensus seeking” process for issues that are escalated to the TC.
The group tries to find a resolution that has no open objections among TC members.
If a consensus cannot be reached that has no objections then a majority wins vote
is called. It is also expected that the majority of decisions made by the TC are via
a consensus seeking process and that voting is only used as a last-resort.

Resolution may involve returning the issue to project captains with suggestions on
how to move forward towards a consensus. It is not expected that a meeting of the TC
will resolve all issues on its agenda during that meeting and may prefer to continue
the discussion happening among the project captains.

Members can be added to the TC at any time. Any TC member can nominate another committer
to the TC and the TC uses its standard consensus seeking process to evaluate whether or
not to add this new member. The TC will consist of a minimum of 3 active members and a
maximum of 10. If the TC should drop below 5 members the active TC members should nominate
someone new. If a TC member is stepping down, they are encouraged (but not required) to
nominate someone to take their place.

TC members will be added as admin’s on the Github orgs, npm orgs, and other resources as
necessary to be effective in the role.

To remain “active” a TC member should have participation within the last 12 months and miss
no more than six consecutive TC meetings. Our goal is to increase participation, not punish
people for any lack of participation, this guideline should be only be used as such
(replace an inactive member with a new active one, for example). Members who do not meet this
are expected to step down. If A TC member does not step down, an issue can be opened in the
discussions repo to move them to inactive status. TC members who step down or are removed due
to inactivity will be moved into inactive status.

Inactive status members can become active members by self nomination if the TC is not already
larger than the maximum of 10. They will also be given preference if, while at max size, an
active member steps down.

### Project Captains

The Express TC can designate captains for individual projects/repos in the
organizations. These captains are responsible for being the primary
day-to-day maintainers of the repo on a technical and community front.
Repo captains are empowered with repo ownership and package publication rights.
When there are conflicts, especially on topics that effect the Express project
at large, captains are responsible to raise it up to the TC and drive
those conflicts to resolution. Captains are also responsible for making sure
community members follow the community guidelines, maintaining the repo
and the published package, as well as in providing user support.

Like TC members, Repo captains are a subset of committers.

To become a captain for a project the candidate is expected to participate in that
project for at least 6 months as a committer prior to the request. They should have
helped with code contributions as well as triaging issues. They are also required to
have 2FA enabled on both their GitHub and npm accounts.

Any TC member or an existing captain on the **same** repo can nominate another committer
to the captain role. To do so, they should submit a PR to this document, updating the
**Active Project Captains** section (while maintaining the sort order) with the project
name, the nominee’s GitHub handle, and their npm username (if different).

- Repos can have as many captains as make sense for the scope of work.
- A TC member or an existing repo captain **on the same project** can nominate a new captain.
  Repo captains from other projects should not nominate captains for a different project.

The PR will require at least 2 approvals from TC members and 2 weeks hold time to allow
for comment and/or dissent.  When the PR is merged, a TC member will add them to the
proper GitHub/npm groups.

#### Active Projects and Captains

The list can be found at [https://github.com/expressjs/discussions/blob/HEAD/docs/contributing/captains_and_committers.md#active-projects-and-members](https://github.com/expressjs/discussions/blob/HEAD/docs/contributing/captains_and_committers.md#active-projects-and-members)

#### Current Initiative Captains

The list can be found at [https://github.com/expressjs/discussions/blob/HEAD/docs/contributing/captains_and_committers.md#current-initiative-captains](https://github.com/expressjs/discussions/blob/HEAD/docs/contributing/captains_and_committers.md#current-initiative-captains)

### Inactivity and Emeritus Policy for Any Role

To support the health and continuity of the project, all individuals holding a role within the community (such as Triager, Committer, WG member, Project Captain, or TC member) are encouraged to maintain active participation.

Inactivity is defined as the absence of meaningful involvement in the project—such as contributions, code reviews, triage, meeting attendance, or discussion participation—for a continuous period of 6 months.

#### Exceptions

Anyone may request a temporary leave from active participation due to personal or professional reasons. In such cases, the individual should inform the relevant team or the Technical Committee (TC). During this time, the inactivity policy is paused, and the individual will not be flagged as inactive.

#### Inactivity Process

- If someone is deemed inactive, the individual may be transitioned to an emeritus role that reflects their past contributions. A best effort will be made to inform them that this has occurred. They may request to be reinstated when they are ready to be active again.
- The emeritus status helps preserve a clear record of contributors who have meaningfully shaped the project over time.

#### Accountability

- The Technical Committee (TC) and the respective captains of each package/team are responsible for assessing activity levels and enacting this policy fairly and transparently, in coordination with other relevant teams.
- In case of disagreement, the situation can be discussed and resolved by consensus within the TC or appropriate team.

### Developer’s Certificate of Origin 1.1

```
By making a contribution to this project, I certify that:

 (a) The contribution was created in whole or in part by me and I
     have the right to submit it under the open source license
     indicated in the file; or

 (b) The contribution is based upon previous work that, to the best
     of my knowledge, is covered under an appropriate open source
     license and I have the right under that license to submit that
     work with modifications, whether created in whole or in part
     by me, under the same open source license (unless I am
     permitted to submit under a different license), as indicated
     in the file; or

 (c) The contribution was provided directly to me by some other
     person who certified (a), (b) or (c) and I have not modified
     it.

 (d) I understand and agree that this project and the contribution
     are public and that a record of the contribution (including all
     personal information I submit with it, including my sign-off) is
     maintained indefinitely and may be redistributed consistent with
     this project or the open source license(s) involved.
```

## Collaborator’s guide

  SRC: expressjs/.github CONTRIBUTING.md

### Website Issues

Open issues for the expressjs.com website in https://github.com/expressjs/expressjs.com.

For issues in other Express managed repos (everything in `expressjs`, `pillarjs` or `jshttp` other than `expressjs/express`), be sure to check their contributing guide and open issues and PRs in the appropriate repository.

### PRs and Code contributions

- Tests must pass.
- Follow the [JavaScript Standard Style](https://standardjs.com/) and `npm run lint`.
- If you fix a bug, add a test.

### Branches

Use the `master` branch for bug fixes or minor work that is intended for the
current release stream.

Use the correspondingly named branch, e.g. `6.x`, for anything intended for
a future release of Express.

### Steps for contributing

1. Create an issue for the
  bug you want to fix or the feature that you want to add.
2. Create your own fork on GitHub, then
  checkout your fork.
3. Write your code in your local copy. It’s good practice to create a branch for
  each new issue you work on, although not compulsory.
4. To run the test suite, first install the dependencies by running `npm install`,
  then run `npm test`.
5. Ensure your code is linted by running `npm run lint` – fix any issue you
  see listed.
6. If the tests pass, you can commit your changes to your fork and then create
  a pull request from there. Make sure to reference your issue from the pull
  request comments by including the issue number e.g. `#123`.

### Issues which are questions

We will typically close any vague issues or questions that are specific to some
app you are writing. Please double check the docs and other references before
being trigger happy with posting a question issue.

Things that will help get your question issue looked at:

- Full and runnable JS code.
- Clear description of the problem or unexpected behavior.
- Clear description of the expected result.
- Steps you have taken to debug it yourself.

If you post a question and do not outline the above items or make it easy for
us to understand and reproduce your issue, it will be closed.

If your question meets all of the above requirements but you do not believe it needs to be looked at
by the maintainers
(for example, if you are just looking for community input) please open it as a discussion topic instead
of an issue. If you
are unsure and open an issue, we may move it to discussions if we triage them and decide they do
not need high
visibility or maintainer input.

## Security Policies and Procedures

  SRC: expressjs/express SECURITY.md

This document outlines security procedures and general policies for the Express
project.

- [Reporting a Bug](#reporting-a-bug)
- [Disclosure Policy](#disclosure-policy)
- [Comments on this Policy](#comments-on-this-policy)

### Reporting a Bug

The Express team and community take all security bugs in Express seriously.
Thank you for improving the security of Express. We appreciate your efforts and
responsible disclosure and will make every effort to acknowledge your
contributions.

Report security bugs by emailing `[email protected]`.

To ensure the timely response to your report, please ensure that the entirety
of the report is contained within the email body and not solely behind a web
link or an attachment.

The lead maintainer will acknowledge your email within 48 hours, and will send a
more detailed response within 48 hours indicating the next steps in handling
your report. After the initial reply to your report, the security team will
endeavor to keep you informed of the progress towards a fix and full
announcement, and may ask for additional information or guidance.

Report security bugs in third-party modules to the person or team maintaining
the module.

### Pre-release Versions

Alpha and Beta releases are unstable and **not suitable for production use**.
Vulnerabilities found in pre-releases should be reported according to the [Reporting a Bug](#reporting-a-bug) section.
Due to the unstable nature of the branch it is not guaranteed that any fixes will be released in the next pre-release.

### Disclosure Policy

When the security team receives a security bug report, they will assign it to a
primary handler. This person will coordinate the fix and release process,
involving the following steps:

- Confirm the problem and determine the affected versions.
- Audit code to find any potential similar problems.
- Prepare fixes for all releases still under maintenance. These fixes will be
  released as fast as possible to npm.

### The Express Threat Model

We are currently working on a new version of the security model, the most updated version can be found [here](https://github.com/expressjs/security-wg/blob/main/docs/ThreatModel.md)

### Comments on this Policy

If you have suggestions on how this process could be improved please submit a
pull request.

---

# Contributing to Expressjs.com

  LOCAL: expressjs/expressjs.com ../../CONTRIBUTING.md

### The Official Documentation of the Express.js Framework

This is the contribution documentation for the [expressjs.com](https://github.com/expressjs/expressjs.com) website.

#### Need some ideas? These are some typical issues.

1. **Website issues**: If you see anything on the site that could use a tune-up, think about how to fix it.
  - Display or screen sizing problems
  - Mobile responsiveness issues
  - Missing or broken accessibility features
  - Website outages
  - Broken links
  - Page structure or user interface enhancements
2. **Content Issues**: Fix anything related to site content or typos.
  - Spelling errors
  - Incorrect/outdated Express.js documentation
  - Missing content
3. **Translation Issues**: Fix any translation errors or contribute new content.
  - Fix spelling errors
  - Fix incorrect/poorly translated words
  - Check out the [Contributing translations](#contributing-translations) section below for a contributing guide.

#### Want to work on a backlog issue?

We often have bugs or enhancements that need work. You can find these under our repo’s [Issues tab](https://github.com/expressjs/expressjs.com/issues). Check out the tags to find something that’s a good match for you.

#### Have an idea? Found a bug?

If you’ve found a bug or a typo, or if you have an idea for an enhancement, you can:

- Submit a [new issue](https://github.com/expressjs/expressjs.com/issues/new/choose) on our repo. Do this for larger proposals, or if you’d like to discuss or get feedback first.
- Make a [GitHub pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request). If you have already done work, and it’s ready to go, feel free to send it our way.

## Getting Started

The steps below will guide you through the Expressjs.com contribution process.

#### Step 1: (OPTIONAL) Open a New Issue

So you’ve found a problem that you want to fix, or have a site enhancement you want to make.

1. If you want to get feedback or discuss, open a discussion [issue](https://github.com/expressjs/expressjs.com/issues/new/choose) prior to starting work. This is not required, but encouraged for larger proposals.
  - While we highly encourage this step, it is only for submissions proposing significant change. It  helps us to clarify and focus the work, and ensure it aligns with overall project priorities.
  - For submissions proposing minor improvements or corrections, this is not needed. You can skip this step.
  - When opening an issue please give it a title and fill in the description section. The more details you provide, the more feedback we can give.
2. After receiving your issue the Express.js documentation team will respond with feedback. We read every submission and always try to respond quickly with feedback.
  - For submissions proposing significant change, we encourage you to follow the review process before starting work.

#### Step 2: Get the Application Code Base

Clone the repo and get the code:

```
git clone https://github.com/expressjs/expressjs.com.git
```

After you’ve got the code you’re ready to start making your changes!

But just in case you need a little extra explanation, this section below outlines the main sections of the code base, where most changes are likely to be made.

**Markdown Page Files**:

- These files render to html and make up the individual pages of the site. Most of the site’s documentation text content is written in `md` files.
- Change these to make changes to individual pages’ content/text or markup.
- Each language has its own complete set of pages, located under their respective language directories - all the Spanish markdown content is found in the `es` directory, for example.

**Includes Partials and Layout Templates**

- `_includes` are partials that are imported and reused across multiple pages.
  - These are used to import text content for reuse across pages, such as the API documentation, e.g., `_includes > api > en > 5x`, which is included in every language.
  - These are used to include the page components that make up site-wide user interface and periphery structure, e.g., Header, Footer, etc.
- `_layouts` are the templates used to wrap the site’s individual pages.
  - These are used to display the structure of the site’s periphery, such as the header and footer, and for injecting and displaying individual markdown pages inside the `content` tag.

**Blog Markdown Files**

- These files make up the individual blog posts. If you want to contribute a blog post please
  follow the specific instructions for [How to write a blog post.](https://expressjs.com/en/blog/write-post.html)
- Located under the `_posts` directory.

**CSS or Javascript**

- All css and js files are kept in `css` and `js` folders on the project root.

The Express.js website is built using [Jekyll](https://jekyllrb.com/) and is hosted on [GitHub Pages](https://pages.github.com/).

#### Step 3: Running the Application

Now you’ll need a way to see your changes, which means you’ll need a running version of the application. You have two options.

1. **Run Locally**: This gets the local version of the application up and running on your machine. Follow our [Local Setup Guide](https://github.com/expressjs/expressjs.com?tab=readme-ov-file#build-the-website-locally) to use this option.
  - This is the recommended option for moderate to complex work.
2. **Run using Deploy Preview**: Use this option if you don’t want to bother with a local installation. Part of our continuous integration pipeline includes [Netlify Deploy Preview](https://docs.netlify.com/deploy/deploy-types/deploy-previews/).
  1. To use this you’ll need to get your changes online - after you’ve made your first commit on your feature branch, make a *draft* pull request.
  2. After the build steps are complete, you’ll have access to a **Deploy Preview** tab that will run your changes on the web, rebuilding after each commit is pushed.
  3. After you are completely done your work, and it’s ready for review, remove the draft status on your pull request and submit your work.

## Contributing translations

We use Crowdin to manage our translations in multiple languages and achieve automatic translation with artificial intelligence. Since these translations can be inefficient in some cases, we need help from the community to provide accurate and helpful translations.

The documentation is translated into these languages:

- Chinese Simplified (`zh-cn`)
- Chinese Traditional (`zh-tw`)
- English (`en`)
- French (`fr`)
- German (`de`)
- Italian (`it`)
- Japanese (`ja`)
- Korean (`ko`)
- Brazilian Portuguese (`pt-br`)
- Spanish (`es`)

### How to translate

1. Request to join the Express.js Website project on [Crowdin](https://express.crowdin.com/website)
2. [Select the language you want to translate](https://support.crowdin.com/for-translators/#starting-translation)
3. [Start translating](https://support.crowdin.com/online-editor/)

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/ko/resources/contributing.md          )

---

# 용어집

> A comprehensive glossary of terms related to Express.js, Node.js, middleware, routing, and other key concepts to help you understand and use Express effectively.

# 용어집

### 애플리케이션(application)

일반적으로, 특정한 목적의 연산을 수행하도록 설계된 하나 이상의 프로그램입니다.  Express의 컨텍스트에서는, Node.js 플랫폼에서 실행되며 Express API를 사용하는 프로그램을 말합니다.  또한 [앱 오브젝트](https://expressjs.com/ko/api.html#express)를 지칭할 수도 있습니다.

### API

애플리케이션 프로그래밍 인터페이스(Application Programming Interface)입니다. 이 용어를 최초로 사용할 때는 약어를 풀어서 기재하십시오.

### Express

Node.js 애플리케이션을 위한 빠르고 개방적인 간결한 웹 프레임워크입니다. 일반적으로 “Express.js”보다 “Express”가 선호되지만, “Express.js”도 허용됩니다.

### libuv

비동기식 I/O에 초점을 둔 멀티플랫폼 지원 라이브러리이며, 주로 Node.js에 의해 사용되도록 개발됩니다.

### middleware

최종 요청 핸들러 이전의 Express 라우팅 계층에 의해 호출되는 함수이며, 따라서 원시 요청과 의도된 최종 라우트 사이의 미들웨어에 위치합니다. 미들웨어와 관련된 용어의 몇 가지 요점은 다음과 같습니다.

- `var foo = require('middleware')`는 Node.js 모듈을 *요구* 또는 _사용_하는 것으로 일컬어집니다. 이후 `var mw = foo()` 명령문은 일반적으로 미들웨어를 리턴합니다.
- `app.use(mw)`는 _미들웨어를 전역 처리 스택에 추가_하는 것으로 일컬어집니다.
- `app.get('/foo', mw, function (req, res) { ... })`는 _미들웨어를 “GET /foo” 처리 스택에 추가_하는 것으로 일컬어집니다.

### Node.js

확장 가능한 네트워크 애플리케이션을 개발하는 데 사용되는 소프트웨어 플랫폼입니다. Node.js는 JavaScript를 스크립팅 언어로 사용하며, 방해하지 않는 I/O 및 단일 스레드 이벤트 루프를 통해 높은 처리량을 달성합니다. [nodejs.org](http://nodejs.org/)를 참조하십시오. **활용 참고**: 최초에는 “Node.js”였으며 이후 “Node”가 되었습니다.

### 오픈 소스(open-source, open source)

When used as an adjective, hyphenate; for example: “This is open-source software.” (예: “이 소프트웨어는 오픈 소스 소프트웨어입니다” [Wikipedia의 Open-source software](http://en.wikipedia.org/wiki/Open-source_software)를 참조하십시오.)

참고

Although it is common not to hyphenate this term, we are using the standard English rules for hyphenating a compound adjective.

### 요청(request)

HTTP 요청입니다. 클라이언트는 HTTP 요청 메시지를 서버에 제출하며, 서버는 응답을 리턴합니다.  요청은 여러 [요청 메소드](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol#Request_methods) 중 하나를 사용해야 합니다(예: GET, POST 등).

### 응답(response)

HTTP 응답입니다. 서버는 HTTP 응답 메시지를 클라이언트에 리턴합니다. 응답에는 요청에 대한 완료 상태 정보가 포함되어 있으며 응답 메시지 본문에는 요청된 컨텐츠가 포함되어 있을 수도 있습니다.

### 라우트(route)

자원을 식별하는 URL의 일부입니다. 예를 들면, `http://foo.com/products/id`에서 “/products/id”가 라우트입니다.

### 라우터(router)

API 참조의 [라우터](https://expressjs.com/ko/4x/api.html#router)를 참조하십시오.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/ko/resources/glossary.md          )
