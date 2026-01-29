# Develop a generative AI applicationStay organized with collectionsSave and categorize content based on your preferences. and more

# Develop a generative AI applicationStay organized with collectionsSave and categorize content based on your preferences.

> Learn how to address the challenges of developing a generative AI application.

# Develop a generative AI applicationStay organized with collectionsSave and categorize content based on your preferences.

This document helps you learn how to address the challenges in each stage of
developing a generative AI application. It describes how to select a model,
customize the model's output to meet your needs, evaluate your customizations,
and deploy your model. This document assumes that you already have a use case in
mind, and that the use case is suitable for generative AI. For information about
how to develop a use case, see
[Evaluate and define your generative AI business use case](https://cloud.google.com/docs/ai-ml/generative-ai/evaluate-define-generative-ai-use-case).

Before you start developing a generative AI application, assess your
organization's technical readiness (capabilities and infrastructure). For
information about how to assess your AI capabilities and create a roadmap to
harness its potential, see
[AI Readiness Workshop](https://cloud.google.com/consulting/ai-readiness-workshop).
If you plan to develop workflows that are automated by generative AI, assess
whether humans should be included in the loop for critical decision stages.
Human review can help with decisions like ensuring responsible use, meeting
specific quality control requirements, or monitoring generated content.

## Generative AI models

Generative AI
[foundation models](https://www.youtube.com/watch?v=YCZ6nwGnL4o)
are trained on multi-terabyte datasets of text, images, code or other
multimedia. The data and the model architecture enable the models to identify
complex patterns and gain a deep, contextual understanding and produce new
content like text, images, music, or videos driven by the training data.

Foundation models form the core upon which numerous generative AI applications
are built. The models' capabilities translate into emergent abilities: with a
simple text prompt instruction, generative AI foundation models can learn to
perform a variety of tasks—like translate languages, answer questions, write a
poem, or write code—without explicit training for each task. Generative AI
foundation models can also adapt to perform specific tasks with some
[prompt techniques](https://cloud.google.com/vertex-ai/docs/generative-ai/learn/prompt-design-strategies)
or they can be fine-tuned with minimal additional training data.

[Large language models (LLMs)](https://cloud.google.com/ai/llms#features)
are trained on text, and they're one example of foundation models that are
typically based on deep-learning architectures, such as the Transformer
developed by Google in 2017. LLMs can be trained on billions of text samples and
other content, and an LLM can be customized for specific domains.

Other
[multimodal](https://cloud.google.com/vertex-ai/docs/generative-ai/docs/learn/models)
models extend the ability of a generative AI application to process information
from multiple modalities including images, videos, audio, and text.
[Multimodal prompts](https://developers.google.com/solutions/ai-images)
combine multiple input formats such as text, images, and audio. For example, you
can input an image and ask a generative AI application to list or describe the
objects in the image. Google's
[Gemini models](https://blog.google/technology/ai/google-gemini-ai)
are built from the ground up for multimodality, and they can reason seamlessly
across text, images, video, audio, and code. Google Cloud's
[Model Garden](https://cloud.google.com/model-garden)
and
[Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/docs/overview)
can help you to find and customize a range of foundation models from Google,
open source, and third party sources.

## Choose a model

When you choose a model, consider the model's modality, size, and cost. Choose
the most affordable model that still meets your response quality and latency
requirements.

- **Modality**: As described in the preceding section, the modality of a
  model corresponds to high-level data categories that a model is trained
  for, like text, images, and video. Typically, your use case and the model's
  modality are closely associated. If your use case involves text-to-image
  generation, you need to find a model trained on text and image data. If you
  need the flexibility of multiple modalities, as in multimodal search, there
  are models that also support multimodal use cases, but cost and latency
  might be higher.
  - [Vertex AI models](https://cloud.google.com/vertex-ai/docs/generative-ai/learn/models)
    offers a large list of generative AI models that you can use.
  - [Model Garden](https://cloud.google.com/vertex-ai/docs/start/explore-models)
    provides a list of first party and open source ML model offerings on
    Google Cloud.
- **Size**: The size of a model is typically measured by the number of
  parameters. In general, a larger model can learn more complex patterns and
  relationships within data, which can result in higher quality responses.
  Because larger models in the same family can have higher latency and costs,
  you might need to experiment and evaluate models to determine which model
  size works best for your use case.
- **Cost**: The cost of a model is related to its capabilities, which
  usually relates to the model's parameter count. Models can also be metered
  and charged differently. For example, some models are charged based on the
  number of input and output tokens. Other models are charged based on the
  number of node hours that are used while the model is deployed.
  - For information about generative AI model pricing on
    Vertex AI, see
    [Vertex AI pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing).
  - For information about the cost to deploy models on
    Google Kubernetes Engine (GKE), see
    [GKE pricing](https://cloud.google.com/kubernetes-engine/pricing).
- **Features**: Not all models support features like tuning and
  distillation. If those capabilities are important to you, check the
  features that are supported by each model.

## Design prompts

Prompt design is the process of authoring prompt and response pairs to give
language models additional context and instructions. After you author prompts,
you feed them to the model as a prompt dataset for pretraining. When a model
serves predictions, it responds with your instructions built in.

If you want to get a specific output, you can use prompt design strategies,
such as instructing the model to complete partial input or giving the model
examples of ideal responses. For more information, see
[Introduction to prompt design](https://cloud.google.com/vertex-ai/docs/generative-ai/learn/introduction-prompt-design).

## Customize a model

After prompt design, you might find that a model's responses work well, so you
don't need to customize it. If the model isn't performing well—for
example if it's hallucinating—you can use additional customization
techniques. The following sections introduce such techniques and can help you
understand how these options influence your model's output.

### Function calling and extensions

[Function calling](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/function-calling)
and
[Vertex AI Extensions](https://cloud.google.com/vertex-ai/generative-ai/docs/extensions/overview)
expand the capabilities of your model. Consider the use cases for your
application and where using a model alone might be insufficient. You can assist
the model by adding function calling or extensions. For example, your model can
extract calendar information from text and then use an extension to find and
book a reservation.

Although you can use function calling and extensions interchangeably, there are
some high-level differences. Function calling is an asynchronous operation and
you don't need to include credentials in your code. Vertex AI
Extensions provide prebuilt options that you can use for complex tasks so that
you don't need to write your own functions. However, because
Vertex AI Extensions returns and calls functions for you,
extensions require you to include credentials in your code.

### Grounding

*Grounding* refers to augmenting model responses by anchoring them to
verifiable sources of information. To ground a model, you connect it to a data
source. Grounding a model helps enhance the trustworthiness of the generated
content by reducing hallucinations.

*Retrieval augmented generation* (RAG) is a commonly used grounding technique.
RAG uses search functionality to find relevant information and then it adds that
information to a model prompt. When you use RAG, output is grounded in facts and
the latest information. RAG search uses vector embeddings and vector databases,
which store data as numerical representations of unstructured data like text and
images. For more information, see
[What is a vector database](https://cloud.google.com/discover/what-is-a-vector-database).

To learn about grounding in Vertex AI, see
[Grounding overview](https://cloud.google.com/vertex-ai/docs/generative-ai/grounding/overview).
For information about how to set up an embedding workflow in AlloyDB for PostgreSQL,
see the
[example embedding workflow](https://cloud.google.com/alloydb/docs/ai/example-embeddings).

### Model tuning

Specialized tasks, such as training a language model on specific terminology,
might require more training than you can do with prompt design alone. In that
scenario, you can use model tuning to improve performance and have the model
adhere to specific output requirements.

To tune a model, you must build a training dataset and then select a tuning
method, such as supervised tuning, reinforcement learning from human feedback
(RLHF) tuning, or model distillation. The size of the dataset and the tuning
methods depends on your model and what you're optimizing for. For example,
specialized, niche tasks require a smaller dataset to get significant
improvements. To learn more about model tuning, see
[Tune language foundation models](https://cloud.google.com/vertex-ai/docs/generative-ai/models/tune-models).

## Evaluate a model

Model evaluation helps you assess how your prompts and customizations affect a
model's performance. Each evaluation method has its own strengths and weaknesses
to consider. For example,
[metrics-based evaluations](https://cloud.google.com/vertex-ai/docs/generative-ai/models/evaluate-models)
can be automated and scaled quickly with a quantifiable way to measure
performance. However, metrics can oversimplify results and miss context and
nuances of natural language. To mitigate these shortcomings, use a wide range of
metrics in combination with human evaluations.

Generative AI on Vertex AI offers automatic
[side-by-side evaluation](https://cloud.google.com/vertex-ai/docs/generative-ai/models/side-by-side-eval),
which lets you compare the output of two models against the
[ground truth](https://developers.google.com/machine-learning/glossary/#ground-truth).
A third model helps you to select the higher quality responses. Automatic
side-by-side evaluation is on par with human evaluators, but it's quicker and
available on demand. However, to perform the comparisons, this method requires a
model that's larger than the models that you're evaluating, which can exhibit
inherent biases. You should therefore still perform some human evaluations.

For all evaluation methods, you need an evaluation dataset. An evaluation
dataset includes prompt and ground truth (ideal response) pairs that you create.
When you build your dataset, include a diverse set of examples that align with
the task you're evaluating to get meaningful results.

## Deploy a model

Deploying a model associates an endpoint and physical machine resources with
your model for serving online, low-latency predictions. Not all models require
deployment. For example, Google's foundation models that are available in
generative AI on Vertex AI already have endpoints. The endpoints
are specific to your Google Cloud project and they're immediately available for your
use. However, if you tune any of those models, you must deploy them to an
endpoint.

When you deploy a model, decide if you prefer to deploy models in a fully
managed environment or a self-managed environment. In a fully managed
environment, you select the physical resources that you need, like the machine
type and accelerator type, and then Vertex AI instantiates and
manages the resources for you. For example, to enable online predictions where
Vertex AI manages the deployment resources for you, see
[Deploy a model to an endpoint](https://cloud.google.com/vertex-ai/docs/general/deployment).
In a self-managed environment, you have more fine-grained control over your
resources, but you manage them on your own. With self-managed environments, you
can
[serve models on platforms like GKE](https://cloud.google.com/kubernetes-engine/docs/tutorials/serve-multiple-gpu).

After you decide what type of environment you want to deploy in, consider your
anticipated traffic, latency requirements, and budget. You need to balance these
factors with your physical resources. For example, if lower cost is a priority,
you might be able to tolerate higher latency with lower-cost machines. Test
environments are a good example of this tradeoff. For more information about how
to choose a machine type, see the notebook
[Determining the ideal machine type to use for Vertex AI endpoints](https://github.com/GoogleCloudPlatform/vertex-ai-samples/blob/main/notebooks/community/vertex_endpoints/find_ideal_machine_type/find_ideal_machine_type.ipynb).

## Responsible AI

Generative AI on Vertex AI is designed with Google's AI
principles in mind. However, it's important that you test models to ensure that
they're used safely and responsibly. Because of the incredible versatility of
LLMs, it's difficult to predict unintended or unforeseen responses.

When you develop applications for your use case, consider the limitations of
generative AI models so that you can properly mitigate potential misuse and
unintended issues. One example of a model limitation is that a model is only as
good as the data that you use. If you give the model suboptimal data—like
inaccurate or incomplete data—you can't expect optimal performance.
Verify that your input data and prompts are accurate. Otherwise, the model can
have suboptimal performance or false model outputs. To learn more about
generative AI model limitations, see
[Responsible AI](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/responsible-ai#limitations).

## What's next

- Try out the
  [Vertex AI notebook tutorials](https://cloud.google.com/vertex-ai/docs/generative-ai/tutorials).
- Learn about
  [Machine Learning Operations (MLOps) for Generative AI](https://www.cloudskillsboost.google/course_templates/927?locale=es&qlcampaign=gc-dms).

   Was this helpful?

---

# Evaluate and define your generative AI business use caseStay organized with collectionsSave and categorize content based on your preferences.

> Learn about generative and traditional AI use cases and define your own AI business use case by using a business value-driven decision approach.

# Evaluate and define your generative AI business use caseStay organized with collectionsSave and categorize content based on your preferences.

This document helps you define an AI business use case by following a business
value-driven decision approach.

Generative AI and traditional AI solutions are powerful tools, but they should
always support your business goals, and they shouldn't exist in isolation. To
create successful generative AI or traditional AI solutions, begin by clearly
identifying the specific measurable business goals or needs that you want to
address. Then work backward from the business outcomes that you want–such as
increased employee efficiency or enhanced customer satisfaction–to make sure
that the solution directly contributes to your business goals.

To define your generative AI or traditional AI use case with a business-value
focus, use the following simplified decision process:

1. **Business goal and success criteria**: Identify measurable business goals.
  - Focus on the
    [business goal](https://developers.google.com/machine-learning/problem-framing/problem#state_the_goal)
    and value to be achieved, such as increasing efficiency and productivity,
    cost reduction, enhancing customer experiences, and competitive advantage.
  - Clarify how the business plans to measure the success of the identified
    goals and objectives. Return on Investment (ROI) is one of the key
    measures of AI project success. ROI can be measured through several
    metrics like the following:
    - **Direct financial gains**: Increased revenue or reduced costs.
    - **Operational efficiency**: Faster time-to-market or quicker issue
      resolution.
    - **Customer experience**: Increased satisfaction scores or improved
      retention.
  - Identify any potential business constraints and considerations, such as
    ensuring that security and privacy aspects meet specific industry
    compliances or country regulatory requirements.
2. **Type of AI/ML**: Determine whether AI/ML is the right approach for
  solving your business problem or achieving the identified goal.
  Decide whether the identified business expectation requires generative AI,
  other types of AI, or whether it doesn't require AI to achieve it. For
  more information, see
  [Identify the output you need](https://developers.google.com/machine-learning/problem-framing/ml-framing#identify_the_output_you_need)
  in "Framing an ML problem."
3. **User experience expectation**: Identify the end users of the use case
  and how they might interact with the generative AI- or traditional
  AI-powered application or service. Consider what the user expectations or
  preferences might be.
4. **Business driven and user-centric AI solution**: Connect the optimal
  generative AI or traditional AI technology use case with measurable
  business requirements, the organization's executive priorities, and user
  expectations. Consider the following:
  - How the business can drive optimized efficiency and
    productivity by using generative AI or traditional AI to achieve more
    outcomes at a faster pace, and with less operational complexity or with
    reduced efforts (and potentially with cost savings).
  - How the business can drive enhanced customer or product experience by
    using generative AI or traditional AI.
  - How you can create business value in an innovative way by using generative
    AI or traditional AI:
    - Analyze your existing business offerings and capabilities to identify
      areas where generative AI or traditional AI can improve your existing
      solutions, enhance creativity, or enable you to explore new
      possibilities.
    - Understand how AI can enable innovative enhancements that set your
      business apart. Generative AI can help create differentiated
      capabilities and value, help you go beyond solving immediate business
      pain points, and explore ways to boost your existing offerings.
    - Prioritize using technology to enhance business capabilities that
      align with the organization's priority goals.
5. **Business process change**: Identify the changes that the business has
  to make to existing processes or workflows to adapt to the generative AI or
  traditional AI use case.
  Consider how the AI solution will change the way that employees
  or customers interact with the company's systems and workflows, such as
  through a mobile app or customer support chatbot. These interactions
  might require backend processes to be changed or reinvented in order to
  leverage AI capabilities like workflow automation and to help the
  business realize the benefits of AI.

## Generative AI business use case example

The following sections provide a simplified example that demonstrates how to
identify and connect measurable business needs and expectations to impactful
generative AI business use cases.

### Business problem statement

In this scenario, customer support service teams are overloaded with a high
volume of repetitive inquiries, manual tickets management, and constant support
emails communication. The overload strains resources, increases agents' working
hours, and slows resolution times, which results in decreased customer
satisfaction and retention.

### Potential areas of optimization with measurable business value

The following are examples of the possible measurable business values that can
be achieved by using a technology solution (a chatbot) that's powered by
generative AI capabilities to address the preceding business challenges. Based
on their business model and priorities, the business might consider some or all
of these measurable targets.

- **Enhance customer support efficiency**: Reduce support costs and
  streamline agent workflows. Measurable success criteria include the following:
  - Percentage decrease in customer support operational costs over
    a defined period (such as quarterly).
  - Percentage increase in the volume of customer inquiries handled
    by the chatbot.
  - Average reduction in agent working hours for repetitive tasks.
- **Optimize ticket resolution**: Improve resolution speed and increase
  the percentage of issues that are resolved directly by the chatbot.
  Measurable success criteria include the following:
  - Average decrease in time-to-resolution for inquiries that the chatbot
    handles.
  - Percentage of tickets resolved without human intervention.
  - Percentage decrease in the volume of tickets that must be escalated to the
    technical support team due to complexity.
  - Increase in first-contact resolution rate (issues solved in a single
    interaction).
  - Percentage increase in the volume of customer inquiries that the chatbot
    handles and resolves.
- **Enhance customer experience**: Boost customer satisfaction by offering
  responsiveness and personalized support that's available 24 hours per day.
  Measurable success criteria include the following:
  - Increase in customer satisfaction (CSAT) scores in surveys tied
    to chatbot usage.
  - Reduced average customer wait times for initial interaction.
  - Increase of issues solved in a single interaction.
  - Percentage of positive sentiment detected in chatbot conversations and
    feedback surveys.
  - Improved customer retention rate.
- **Support business operations growth**: Handle increase in customer
  demand without incurring linearly increasing costs or increase in wait times
  for initial customer interaction. Measurable success criteria include the
  following:
  - Ability to handle a specified percentage increase in support request volume
    without human intervention.
  - Maintain consistent CSAT scores and time-to-resolution during periods of
    high demand.
  - Maintain consistent customer wait times for initial interaction.

### Generative AI-powered solutions

**Conversational chatbot**: Generative AI-powered chatbots or virtual agents
offer a significant enhancement in personalization and natural, human-like
conversation. This is due to the ability of generative AI to understand complex
context, sentiment, and relationships within language. This ability leads to
more natural interaction, asking relevant questions, and providing tailored
recommendations for an improved user experience.

Generative AI abilities also help organizations to drive more work efficiencies
and productivity. In contrast, a traditional rule-based chatbot is commonly
limited to predefined keywords and intent patterns. Therefore, as conversational
patterns evolve or new questions arise, a rule-based chatbot requires additional
operational effort, for rule updates and refinements and intent training. For
this use case, generative AI chatbots provide the following benefits compared to
traditional rule-based chatbots:

- Generative AI-powered chatbot answers aren't limited to frequently
  asked questions (FAQs). The chatbot can find answers within large datasets
  from different sources like historical data of support cases, websites,
  product documentation, inventory, emails, and old chat conversations with
  resolution. It can also understand conversational queries and summarize
  complex information.
- Generative AI virtual agents synthesize information from all your data
  sources. This synthesis enables them to provide specific, reasoned, and
  actionable responses that are based on the data that you have provided and
  that are aligned with your business expectations.
- Generative AI interprets the complex language and nuances within a ticket.
  It can understand the full context of a customer's issue; a traditional AI
  chatbot primarily focuses on specific keywords.
- Generative AI chatbots provide the flexibility for customers to express
  themselves using their preferred method (text, voice, image), while the
  chatbot leverages all input to improve issue resolution. For example,
  customers can share photos of a damaged product during the chat
  conversation, and generative AI can combine the customer's description with
  the photo in order to help enhance diagnostic and troubleshooting accuracy.

**Case management and insight-generation workflow**: A Generative AI-powered
chatbot can automatically generate tickets from every interaction. The chatbot
utilizes generative AI capabilities to understand the urgency, sentiment
analysis, and complexity of the issue. These capabilities ensure that tickets
are prioritized effectively. The chatbot can interact with your ticketing system
in these ways:

- The generative AI chatbot interfaces directly with your support
  ticketing system to create and populate the support ticket with required
  information like the following:
  - Customer details
  - Technical issue categorization and priority
  - A full transcript of the conversation for context
  - Summarization of the core issue
- For new, complex issues, the chatbot can assign the ticket to the
  correct team with supporting context such as a summary of the issue and
  conversation.

## What's next

- Learn about how generative AI might apply to your use case in
  [Generative AI examples](https://cloud.google.com/use-cases/generative-ai).
- Learn more about the stages of developing a generative AI application and
  choose the best products and tools for your use case in
  [Build a generative AI application on Google Cloud](https://cloud.google.com/docs/ai-ml/generative-ai).
- Assess your AI capabilities and create a roadmap to harness its
  potential with the
  [AI Readiness Workshop](https://cloud.google.com/consulting/ai-readiness-workshop).

---

# When to use generative AI or traditional AIStay organized with collectionsSave and categorize content based on your preferences.

> Learn when to use generative AI, traditional AI, or a combination of both.

# When to use generative AI or traditional AIStay organized with collectionsSave and categorize content based on your preferences.

This document helps you identify when generative AI, traditional AI, or a
combination of both might suit your business use case.

In this document, *traditional AI* refers to AI capabilities and use cases
that might not require employing generative AI capabilities, like some
[classification](https://developers.google.com/machine-learning/crash-course/classification/video-lecture)
and
[predictive](https://cloud.google.com/learn/what-is-predictive-analytics)
AI use cases. Traditional AI models excel at learning from existing data to
classify information or predict future outcomes based on historical patterns.
Generative AI models expand these capabilities to create summaries, uncover
complex hidden correlations, or generate new content—like text, images, or
videos—that reflect the style and patterns within the training data.

## When to use generative AI

In general, generative AI solutions excel at tasks like the following:

- Creating and recommending content.
- Powering conversational search and chatbots.
- Scaling and automating workflow for repetitive tasks.
- Using associative reasoning to find insights and relationships within
  documents and data.
- Generating code and assisting developers in writing, explaining, and
  documenting code.

The following sections provide examples of these common, general generative AI
use cases that can be customized to different industries.

### Content creation and recommendation

- Generating marketing related content such as product images, social
  media posts, and emails with relevant images.
- Translating content such as documents, website content, and multilingual
  chatbot conversations.
- Summarizing text content, including documents, articles, customer
  feedback, and reports, to help with more informed data-driven decisions.
- Creating summaries of information from multiple sources that can include
  text, images, and video or audio components.
- Automatic captioning or subtitling of videos.
- Creating creative multimedia content such as creating new images from
  text prompt descriptions, modifying or fixing images using text prompts
  (for example, removing an object or changing color scheme), and generating
  short videos or animations from text prompts or scripts.
- Generating realistic synthetic voices for audio such as voice-over
  tracks and music.
- Analyzing and understanding user behavior, preferences, reviews, and
  past interactions to provide personalized content recommendations. Analysis
  can be combined with real-time factors like location to tailor content
  recommendations across content like products, articles, and videos.

### Conversational search and chatbots

- Building virtual assistants for user interactions like customer support
  and online sales.
- Enabling conversational search through large knowledge bases with
  natural language queries.
- Finding answers to complex questions that combine textual inquiries with
  related images.

### Document and data understanding

- Extracting data and analyzing content from text such as reports,
  invoices, receipts, financial transactions, or contracts to highlight
  possible errors or compliance issues, identify potential risks, or uncover
  anomalies that are indicative of fraud.
- Analyzing the sentiment of user-generated content like social media
  posts and product reviews.
- Analyzing transcribed call center conversations to extract insights such
  as the most common reasons that customers give a low rating to call center
  interactions.
- Analyzing cybersecurity data such as threat reports, articles, and
  repositories to extract key threat indicators. This analysis enables
  proactive cybersecurity defense to summarize and prioritize mitigation
  strategies with recommendations for faster response.
  Analysis can translate complex attack graphs to plain-text explanations of
  exposure. It can also simulate possible attack paths to highlight impacted
  assets, and it can recommend mitigations before assets can be exploited.

### Code generation and developer assistance

Generative AI can help with the following kinds of tasks at all stages of the
software development lifecycle (SDLC):

- Generating APIs specs and documentation by using natural language prompts.
- Creating assets such as code, functions, command-line commands, and
  Terraform scripts from natural language prompts.
- Generating tests and code explanations, including comments and
  documentation to explain code.

For more information about how generative AI can transform business operations
like customer service, employee productivity, and process automation, see
[Business use cases](https://cloud.google.com/ai/generative-ai#business-use-cases)
in "Generative AI on Google Cloud."

## When to use traditional AI

Traditional AI use cases typically focus on predicting future outcomes or
classifying a category based on an AI model that's trained on existing
historical data sources like
[tabular](https://cloud.google.com/vertex-ai/docs/tabular-data/tabular101)
data and images. Traditional AI solutions often suffice to address several
classification and predictive AI use cases such as the following:

- **Classification use cases**:
  - Filtering email spam by classifying emails as *spam* or *not
    spam*, based on a traditional classification AI model that's trained on
    historical data.
  - Training a traditional image classification model on specific
    images of good and defective products to effectively help with
    real-time inspection and defect detection in manufacturing.
- **Regression use cases**:
  - Predicting continuous numerical values like predicting house
    prices based on specific house features and location.
  - Predicting how much revenue a customer of an ecommerce platform
    will generate during their relationship with the company based on
    historical purchase data.
- **Time series forecasting use cases**: Forecasting sales and demand.
- **Clustering use cases**: Performing customer segmentation.

For more information about using traditional AI, see
[Uses and examples of predictive analytics](https://cloud.google.com/learn/what-is-predictive-analytics#section-5)
in "What is predictive analytics?"

## Decide between traditional AI and generative AI

The following simplified decision tree provides a high-level reference for some
use case-based decision paths. In some cases, it might be best to use both
traditional AI and generative AI, as described in the next section, "When to
combine generative AI with traditional AI."

![A decision tree shows when to use generative AI, traditional classification or predictive AI, or a pre-trained AI model.](https://cloud.google.com/static/docs/ai-ml/generative-ai/images/evaluate-define-generative-ai-use-case-decision-tree.svg)

The decision tree includes the following use case-driven questions and
answers:

- If your use case is related to classification or detection, check
  whether a
  [pre-trained traditional AI model](https://cloud.google.com/vertex-ai/docs#vertex-ai-and-cloud-ml-products)
  can meet your use case requirements. Pre-trained traditional models include
  AI APIs like Document AI, Vision AI, Natural Language API,
  and Video Intelligence API.
  - If a pre-trained model meets your requirements, use the
    pre-trained model.
  - If a pre-trained model can't meet your requirements, check
    whether enough training data is available to custom train a model.
    - If sufficient training data is available, what should
      be prioritized: more control of model training or achieving faster
      go-to-market (GTM)?
      - If you require high control of the model
        training with customizations like using any preferred model
        algorithm, developing your own loss functions, using specific
        features of model
        [explainability](https://cloud.google.com/explainable-ai),
        the number of layers in the model, learning rate, and other
        model
        [hyperparameters](https://developers.google.com/machine-learning/guides/text-classification/step-5),
        use a custom training of a traditional AI model. For
        information about the differences between custom training or
        training a model in Vertex AI by using
        AutoML, see
        [Choose a training method](https://cloud.google.com/vertex-ai/docs/start/training-methods).
      - If your business priority is a faster GTM, use
        generative AI. If your use case is specialized, you can improve
        the performance of a model by using model tuning like
        [supervised tuning](https://cloud.google.com/vertex-ai/generative-ai/docs/models/tune-models#how-tuning-works)
        for classification, sentiment analysis, or entity extraction.
    - If a training dataset isn't available, or if available
      datasets aren't large enough to custom train a model, use
      generative AI models with
      [prompt engineering](https://cloud.google.com/discover/what-is-prompt-engineering).
      These models can be tuned further to perform specialized tasks by
      using
      [data examples](https://cloud.google.com/vertex-ai/generative-ai/docs/models/gemini-supervised-tuning-prepare).
- If your use case is related to predictive AI use cases, use traditional
  AI. Traditional predictive AI is particularly effective with structured data.
- If your use case is related to generative AI use cases like
  summarization, content generation, or advanced transcription, use
  generative AI. Use of generative AI includes use cases that require
  processing and inputting information from multiple modalities like text,
  images, videos, or audio.

Although data scientists and ML engineers commonly lead the model selection
process, it's important to also consider the input of key stakeholders like
business leaders, product owners, domain experts, and end users. For example,
these stakeholders might engage in the following ways:

- **Business leaders and decision-makers**: Approve the selection when
  it's aligned with the business priorities.
- **Product owners**: Might require influence or have more control of the
  model behavior to align it with the product priorities.
- **Domain experts**: Apply their domain expertise to improve model
  effectiveness.
- **End users**: Might need to understand the output of the model, and how
  to incorporate the output for more informed decision-making.

## When to combine generative AI with traditional AI

Traditional AI and generative AI aren't mutually exclusive. In some business
use cases, they can be used to complement each other to address the ultimate
business goal. For example, you can use output from a traditional AI model as
part of the prompt for a generative AI model. The following are some examples of
use cases for combining traditional and generative AI capabilities:

- Traditional predictive AI can analyze historical data to forecast
  customer churn probability. This analysis can be integrated with an LLM or
  generative AI-powered chatbot, which empowers your sales team to explore
  the predictions by using natural language conversations. You can also
  generate business intelligence (BI) dashboards through simple conversation
  with the chatbot.
- Traditional predictive AI can forecast risks of a specific use case,
  while generative AI can simulate different scenarios to help in formulating
  possible mitigation strategies.
- Traditional predictive AI can identify customer segments to help create
  personalized marketing and campaign creation. You can then use generative
  AI to generate personalized marketing content that's tailored to each
  identified segment.
- Traditional AI computer vision can detect and classify sign language to
  translate video input into text. Generative AI can add understanding of
  context and nuance within sign language, allowing for more optimized
  translation into written text, including multiple languages. Generative AI
  can also generate voice output from the text translation, enabling seamless
  two-way communication between signers and non-signers.
- Traditional AI can perform video analytics and use video intelligence
  capabilities to extract vital insights and features from video assets. For
  example, it can perform object detection, person detection, text detection,
  and extraction from video assets. Generative AI can then use those insights
  to create novel experiences like chatbots, listings, reports, or articles.

To maximize the business benefits of your generative AI and traditional AI
investments, prioritize necessary business outcomes and user needs
(business-driven and user-centric AI solutions). This approach ensures that
solutions stay relevant, drive adoption, enhance efficiency, and foster
innovation. Prioritizing the user experience in AI-powered solutions helps to
align expectations and deliver meaningful results.

## What's next

- Learn how to [evaluate and define your generative AI business use case](https://cloud.google.com/docs/ai-ml/generative-ai/evaluate-define-generative-ai-use-case).
- Learn more about the stages of developing a generative AI application and
  choose the best products and tools for your use case in
  [Build a generative AI application on Google Cloud](https://cloud.google.com/docs/ai-ml/generative-ai).
- Assess your AI capabilities and create a roadmap to harness its
  potential with the
  [AI Readiness Workshop](https://cloud.google.com/consulting/ai-readiness-workshop).

   Was this helpful?
