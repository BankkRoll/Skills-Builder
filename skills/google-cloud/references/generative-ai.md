# Stay organized with collectionsSave and categorize content based on your preferences. and more

# Stay organized with collectionsSave and categorize content based on your preferences.

> Choose models and infrastructure for your generative AI application

![Venn diagram showing the components of a generative AI system](https://cloud.google.com/static/docs/generative-ai/choose-models-infra-for-ai/venn-diagram.png) ![Venn diagram showing the components of a generative AI system](https://cloud.google.com/static/docs/generative-ai/choose-models-infra-for-ai/venn-diagram-mobile.png)

1. **Application hosting:** Compute to host your application. Your application can use [Google Cloud's client libraries and SDKs](https://cloud.google.com/apis/docs/cloud-client-libraries) to talk to different Cloud products.
2. **Model hosting:** Scalable and secure hosting for a generative model.
3. **Model:** Generative model for text, chat, images, code, embeddings, and [multimodal](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/models).
4. **Grounding solution:** Anchor model output to verifiable, updated sources of information.
5. **Database:** Store your application's data. You might reuse your existing database as your grounding solution, by augmenting prompts via SQL query, and/or storing your data as vector embeddings using an extension like [pgvector](https://cloud.google.com/blog/products/databases/announcing-vector-support-in-postgresql-services-to-power-ai-enabled-applications).
6. **Storage:** Store files such as images, videos, or [static web frontends](https://cloud.google.com/storage/docs/hosting-static-website). You might also use Storage for the raw grounding data (eg. PDFs) that you later convert into embeddings and store in a vector database.

The sections below walk through each of those components, helping you choose which Google Cloud products to try.

### Application hosting infrastructure

Choose a product to host and serve your application workload, which makes calls out to the generative model.

Want managed serverless infrastructure?

 close check [Cloud Run](https://cloud.google.com/run/docs/overview/what-is-cloud-run)  close

Can your application be containerized?

 close check [Kubernetes Engine](https://cloud.google.com/kubernetes-engine/docs/concepts/kubernetes-engine-overview)  close  [Compute Engine](https://cloud.google.com/compute/docs/instances)

### Model hosting infrastructure

Google Cloud provides multiple ways to host a generative model, from the flagship Vertex AI platform, to customizable and portable hosting on Google Kubernetes Engine.

Using Gemini and need enterprise features like scaling, security, data privacy, and observability

 check close [Gemini Developer API](https://ai.google.dev/docs)  check

Want fully managed infrastructure, with first-class generative AI tools and APIs?

 close check [Vertex AI](https://cloud.google.com/vertex-ai/docs/generative-ai/learn/overview)  close

Does your model require a specialized kernel, legacy OS, or have special licensing terms?

 close check [Compute Engine](https://cloud.google.com/compute/docs/gpus/about-gpus)  close  [Kubernetes Engine](https://cloud.google.com/kubernetes-engine/docs/integrations/ai-infra)

### Model

Google Cloud provides a
  [set of state-of-the-art foundation models through Vertex AI](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/overview),
  including Gemini. You can also deploy a third-party model to either
  [Vertex AI Model Garden](https://cloud.google.com/vertex-ai/docs/start/explore-models) or
  [self-host on GKE](https://cloud.google.com/kubernetes-engine/docs/tutorials/serve-multiple-gpu#llama-2-70b), Cloud Run, or Compute Engine.

Generating code?

 close check [Codey (Vertex AI)](https://cloud.google.com/vertex-ai/docs/generative-ai/code/code-models-overview)  close

Generating images?

 close check [Imagen (Vertex AI)](https://cloud.google.com/vertex-ai/docs/generative-ai/image/overview)  close

Generating embeddings for search, classification, or clustering?

 close check [text-embedding (Vertex AI)](https://cloud.google.com/vertex-ai/docs/generative-ai/embeddings/get-text-embeddings)  close

Ok, you want to generate text. Would you like to include images or video in your text prompts? (multi-modal)

 close check [Gemini (Vertex AI)](https://cloud.google.com/vertex-ai/docs/generative-ai/start/quickstarts/quickstart-multimodal)  close

Ok, just text prompts. Want to leverage Google's most capable flagship model?

 close check [Gemini (Vertex AI)](https://cloud.google.com/vertex-ai/docs/generative-ai/start/quickstarts/quickstart-multimodal)  close

Deploy an open-source model to:
      [Vertex AI (Model Garden)](https://cloud.google.com/vertex-ai/docs/start/explore-models) [GKE (HuggingFace)](https://huggingface.co/models)

### Grounding and RAG

To ensure informed and accurate model responses, **ground** your generative AI application with [real-time data](https://cloud.google.com/blog/products/ai-machine-learning/how-to-use-grounding-for-your-llms-with-text-embeddings). This is called [retrieval-augmented generation (RAG)](https://cloud.google.com/use-cases/retrieval-augmented-generation).

If you want to generate content that’s grounded on up-to-date information from the internet, then Gemini models can evaluate whether the model's knowledge is sufficient or whether grounding with Google Search is required.

You can implement grounding using an index of your data with a search engine. Many search engines now store embeddings in a [vector database](https://cloud.google.com/discover/what-is-a-vector-database), which is an optimal format for [operations like similarity search](https://cloud.google.com/blog/products/ai-machine-learning/how-to-use-grounding-for-your-llms-with-text-embeddings). Google Cloud offers multiple vector database solutions, for different use cases.

Note: You can ground using non-vector databases by querying an existing database like Cloud SQL or Firestore, and you can use the result of the query in your model prompt.

Do you want a fully-managed optimized solution that supports most data sources and prevents direct access to the underlying embeddings?

 close check [Vertex AI Search](https://cloud.google.com/generative-ai-app-builder/docs/try-enterprise-search)   close You are building a search engine for RAG

Do you want to build a search engine for RAG using a managed orchestrator with a LlamaIndex-like interface?

 close check [Vertex AI RAG Engine](https://cloud.google.com/vertex-ai/generative-ai/docs/rag-overview)   close You might use a [reference architecture](https://cloud.google.com/architecture/ai-ml) to build a tailor-made search engine and a vector database for RAG use cases.  close

Do you need a low-latency vector search, large-scale serving, or a specialized and optimized vector database?

 close check [Vertex AI Vector Search](https://cloud.google.com/vertex-ai/docs/vector-search/overview)  close

Is your data accessed programmatically (OLTP)? Already using a SQL database?

 close check

Want to use Google AI models directly from your database? Require low latency?

  check close   [AlloyDB](https://cloud.google.com/alloydb/docs/ai/work-with-embeddings) [Cloud SQL](https://github.com/pgvector/pgvector?tab=readme-ov-file#pgvector)   close

Have a large analytical dataset (OLAP)? Require batch processing, and frequent SQL table access by humans or scripts (data science)?

 check [BigQuery](https://cloud.google.com/blog/products/ai-machine-learning/open-source-framework-for-connecting-llms-to-your-data)
            Create, deploy, and manage extensions that connect large language models to the APIs of external systems.

            Explore a variety of [document loaders](https://python.langchain.com/docs/integrations/components) and [API integrations](https://python.langchain.com/docs/integrations/tools) for your gen AI apps, from [YouTube](https://python.langchain.com/docs/integrations/tools/youtube) to [Google Scholar](https://python.langchain.com/docs/integrations/tools/google_scholar).

            If you're using models hosted in Vertex AI, you can ground model responses using Vertex AI Search, Google Search, or inline/infile text.

- [C# and .NET](https://cloud.google.com/dotnet/docs/setup)
- [C++](https://cloud.google.com/cpp/docs/setup)
- [Go](https://cloud.google.com/go/docs/setup)
- [Java](https://cloud.google.com/java/docs/setup)
- [JavaScript and Node.js](https://cloud.google.com/nodejs/docs/setup)
- [Python](https://cloud.google.com/python/docs/setup)
- [Ruby](https://cloud.google.com/ruby/docs/setup)

LangChain is an open source framework for generative AI apps that allows you to build context into your prompts, and take action based on the model's response.

- [Python (LangChain)](https://python.langchain.com/docs/integrations/llms/google_vertex_ai_palm)
- [JavaScript (LangChain.js)](https://js.langchain.com/docs/integrations/platforms/google)
- [Java (LangChain4j)](https://docs.langchain4j.dev/integrations/language-models/google-palm/)
- [Go (LangChainGo)](https://tmc.github.io/langchaingo/docs/)

View [code samples for popular use cases and deploy examples of generative AI applications](https://cloud.google.com/docs/generative-ai/code-samples) that are secure, efficient, resilient, high-performing, and cost-effective.

---

# Generative AI code samples and sample applicationsStay organized with collectionsSave and categorize content based on your preferences.

> Explore curated code samples for popular use cases and deploy examples of generative AI applications that are secure, efficient, resilient, high-performing, and cost-effective.

# Generative AI code samples and sample applicationsStay organized with collectionsSave and categorize content based on your preferences.

## Sample applications

Deploy a prebuilt generative AI sample application, then fork the code to modify it for your own use-case.

Macros

### Jump Start Solution: Document Summarization

Deploy a one-click sample application to summarize long documents with Vertex AI.

Beginner Python

### Jump Start Solution: Generative AI RAG with Cloud SQL

Deploy a one-click sample application that uses vector embeddings stored in Cloud SQL to improve the accuracy of responses from a chat application.

Beginner Python

### Jump Start Solution: Generative AI Knowledge Base

Deploy a one-click sample application that extracts question-and-answer pairs from a set of documents, along with a pipeline that triggers the application when a document is uploaded.

Beginner Python

### Generate a marketing campaign with Gemini

Build a web app to generate marketing campaign ideas, using Gemini on Vertex AI, Cloud Run, and [Streamlit](https://streamlit.io/).

Beginner Python

### Airport Assistant: RAG App

Sample app for retrieval-augmented generation with AlloyDB for PostgreSQL and Vertex AI. ([blog post](https://cloud.google.com/blog/products/databases/introducing-sample-genai-databases-retrieval-app), [codelab](https://codelabs.developers.google.com/codelabs/genai-db-retrieval-app)).

Intermediate Python

### GenWealth: RAG app

Learn to build a Node-based RAG app that provides investment recommendations for financial advisors. This sample integrates with Vertex AI, Cloud Run, AlloyDB, and Cloud Run functions. Built with Angular, TypeScript, Express.js, and LangChain.

Intermediate Node

### Fix My Car: RAG app

Learn to build a RAG app that helps car owners troubleshoot their vehicle, without having to flip through their owner's manual. Variants include Cloud SQL  with pgvector, and Vertex AI Search. Built with Java (Spring) and Python (Streamlit).

Intermediate Java

### Deploy Llama models on Cloud Run

Learn how to deploy and run Meta's Llama models on Cloud Run.

Beginner Python

## SDKs and Frameworks

Learn how to work with Google Cloud's generative AI APIs using SDK code snippets.

Macros

### Vertex AI - Gemini SDKs

Learn how to apply the Vertex AI Gemini SDKs to tasks like chat, multimodal prompts, and document processing. [Browse additional code samples here.](https://cloud.google.com/vertex-ai/docs/samples?text=gemini)

Beginner Python Node Java Go C#

### Vertex AI Search SDKs

Learn how to store and retrieve RAG documents using Vertex AI Search.

Beginner Python Node Java Go C# PHP Ruby

### Browse all Google Cloud client libraries

Integrating other products, like Cloud Storage or Firestore, into your generative AI app? Browse all Google Cloudclient libraries in your programming language of choice.

Beginner Python Node Java Go C# PHP Ruby

### LangChain (Python)

Explore code snippets for using LangChain alongside Google Cloud products, including chat models (Vertex AI), vector databases (AlloyDB, Cloud SQL, Firestore, Vertex AI Search, BigQuery, and others), and others (Google Drive, Google Maps, YouTube, and others).

Beginner Python

### LangChain.js (Node)

Explore code snippets for using LangChain alongside Google Cloud products, including chat models (Vertex AI), vector databases (Vertex AI Vector Search), and others (Google Search).

Beginner Node

### Genkit (Node)

Genkit is an open-source framework that helps you build, deploy, and monitor production-ready AI-powered web applications. Genkit comes with plugins for [Vertex AI](https://genkit.dev/docs/integrations/vertex-ai/), [Cloud Operations](https://genkit.dev/docs/integrations/google-cloud/?lang=go), and [Firestore](https://genkit.dev/docs/deployment/firebase/?lang=js).

Beginner Node

### LangChain4j (Java)

Explore code snippets for using LangChain alongside Google Cloud products, including chat models (Vertex AI).

Beginner Java

## Notebooks

Explore hands-on walkthroughs of generative AI use cases.

Macros

### Getting started with Vertex AI Gemini 1.5 Flash

Learn how to call Gemini 1.5 Flash, and leverage its long context window, using the Vertex AI SDK. This notebook includes text, video, and audio modalities.

Beginner Python

### Sheet Music Analysis with Gemini

Learn how to extract sheet music metadata, such as composer and tempo, from PDFs using the Vertex AI SDK.

Beginner Python

### Video Analysis with Gemini

Learn how to analyze video sentiment, including facial expressions, using the Vertex AI SDK.

Beginner Python

### Analyzing movie posters in BigQuery with Gemini

Learn how to extract information from movie posters by calling Gemini directly from BigQuery.

Intermediate Python

### Introduction to Vertex AI Embeddings - Text & Multimodal

Learn how to convert text and images to vector embeddings using the Vertex AI SDK, for use in a retrieval-augmented generation (RAG) application.

Intermediate Python

### Function-calling with Gemini

Learn how to augment Gemini's response with real-time data, such as a company's stock price and latest news.

Intermediate Python

### Code migration from PaLM to Gemini

Learn how to migrate your existing Vertex AI SDK code to call Gemini instead of PaLM.

Intermediate Python

### Supervised Tuning with Gemini for Question-answering

Learn how to tune Gemini using Vertex AI, to train the model to respond well to questions about Python coding.

Advanced Python

### Browse all notebooks

Explore dozens of other Vertex AI notebooks in the Google Cloud Sample Browser.

Intermediate Python

## Learn more

- [All Vertex AI code samples](https://cloud.google.com/vertex-ai/generative-ai/docs/samples)
- [Google Cloud sample browser](https://cloud.google.com/docs/samples)

---

# Generative AI glossaryStay organized with collectionsSave and categorize content based on your preferences.

> Learn about specific terms that are associated with generative AI.

# Generative AI glossaryStay organized with collectionsSave and categorize content based on your preferences.

This glossary defines generative artificial intelligence (AI) terms.

## AI agents

An *AI agent* is an application that achieves a goal by processing input,
performing reasoning with available tools, and taking actions based on its
decisions. AI agents use [function calling](#function-calling) to format the
input and ensure precise interactions with external tools. The following diagram
shows the components of an AI agent:

![An AI agent consists of an orchestration layer, a model, and tools.](https://cloud.google.com/static/docs/generative-ai/images/glossary-ai-agents.svg)

As shown in the preceding diagram, AI agents consist of the following
components:

- **Orchestration**: the orchestration layer of an agent manages memory,
  state, and decision-making by controlling the plan, tool usage, and data
  flow. Orchestration includes the following components:
  - **Profile and instructions**: the agent takes on a specific role
    or persona to direct its actions and decision-making.
  - **Memory**: to maintain context and state, the agent retains
    short-term memory and long-term memory. Short-term memory holds the
    immediate context and information that's necessary for the current
    task. Long-term memory retains the complete conversation history.
  - **Reasoning and planning**: the agent uses the model to perform
    task decomposition and reflection, and then it creates a plan. First,
    the agent separates the user prompt into sub-components to handle
    complex tasks by calling one or more functions. Next, the agent reflects
    on the function outputs by using reasoning and feedback to improve the
    response.
- **Model**: any generative language model that processes goals, creates
  plans, and generates responses. For optimal performance, a model should
  support function calling and it should be trained with data signatures from
  tools or reasoning steps.
- **Tools**: a collection of tools including APIs, services, or functions
  that fetch data and perform actions or transactions. Tools let agents
  interact with external data and services.

For applications that require autonomous decision-making, complex multi-step
workflow management, or adaptive experiences, AI agents perform better than
standard foundational models. Agents excel at solving problems in real-time by
using external data and at automating knowledge-intensive tasks. These
capabilities enable an agent to provide more robust results than the passive
text-generation capabilities of foundational models.

For more information about AI agents, see
[What is an AI Agent](https://cloud.google.com/discover/what-are-ai-agents).

---

## context window

A *context window* is the number of [tokens](#tokens) that a foundational model
can process in a given prompt. A larger context window lets the model access and
process more information, which leads to more coherent, relevant, and
comprehensive responses.

[Gemini models](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/models)
are purpose-built with long context windows to handle these larger amounts of
information. To give a sense of scale, a model with a context window of 1
million tokens can process any one of the following inputs:

- 50,000 lines of code (with the standard 80 characters per line)
- All of the text messages that you've sent in the last 5 years
- 8 average-length English-language novels
- Transcripts of over 200 average-length podcast episodes
- 1 hour of video without audio
- Approximately 45 minutes of video with audio
- 9.5 hours of audio

For more information about best practices for long context prompting, see
[Long context](https://cloud.google.com/vertex-ai/generative-ai/docs/long-context).

---

## embedding

An *embedding* is a numerical representation of data, such as text, images, or
videos, that captures relationships between different inputs. Embeddings are
generated during the training phase of a model by converting text, image, and
video into arrays of floating point numbers that are called *vectors*.
Embeddings often
[reduce the dimensionality](https://en.wikipedia.org/wiki/Dimensionality_reduction)
of data, which helps to enhance computational efficiency and to enable the
processing of large datasets. This reduction in dimensionality is crucial for
training and deploying complex models.

Machine learning (ML) models require data to be expressed in a format that they
can process. Embeddings meet that requirement by mapping data into a continuous
vector space where closer proximity reflects data points that have similar
meanings. Embeddings enable models to discern nuanced patterns and relationships
that would be obscured in raw data.

For example, [large language models (LLMs)](#large-language-model) rely on
embeddings in order to understand the context and meaning of text. That
understanding lets the LLM generate coherent and relevant responses. In image
generation, embeddings capture the visual features of images, which enables
models to create realistic and diverse outputs.

Systems that use
[retrieval-augmented generation (RAG)](#retrieval-augmented-generation) rely on
embeddings to match user queries with relevant knowledge. When a query is posed,
it's converted into an embedding, which is then compared to the embeddings of
documents that are within the knowledge base. This comparison, which is
facilitated by similarity searches in the vector space, lets the system
retrieve the most semantically relevant information.

For more information about embedding models and use cases, see
[Embedding APIs overview](https://cloud.google.com/vertex-ai/generative-ai/docs/embeddings).

---

## foundation model

*Foundation models* are large, powerful models that are trained on vast amounts
of data, which often spans multiple modalities like text, images, video, and
audio. These models use statistical modeling to predict likely responses to
[prompts](#prompting) and to generate new content. They learn patterns from
their training data, such as language patterns for text generation and diffusion
techniques for image generation.

Google offers a variety of
[generative AI foundation models](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/models)
that are accessible through a managed API. To access the foundation models that
are available in Google Cloud, use the Vertex AI
[model garden](https://cloud.google.com/vertex-ai/generative-ai/docs/model-garden/explore-models).

---

## function calling

*Function calling* is a feature that connects
[large language models (LLMs)](#large-language-model) to external tools like
APIs and functions to enhance the LLM's responses. This feature lets LLMs go
beyond static knowledge and enhance responses with real-time information and
services like databases, customer relationship management systems, and document
repositories.

To use function calling, you provide the model with a set of functions. Then,
when you [prompt](#prompting) the model, the model can select and call the
functions based on your request. The model analyzes the prompt and then it
generates structured data that specifies which function to call and the
parameter values. The structured data output calls the function and then it
returns the results to the model. The model incorporates the results into its
reasoning to generate a response. This process lets the model access and utilize
information that's beyond its internal knowledge, which lets the model perform
tasks that require external data or processing.

Function calling is a critical component in the architecture of
[AI agents](#ai-agents). Function calling provides a structured way for the
model to specify which tool to use and how to format the input, which helps to
ensure precise interactions with external systems.

For more information about function calling in Gemini, see
[Introduction to function calling](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/function-calling).

---

## generative AI

*Generative AI* is a type of AI that goes beyond the traditional AI focus on
[classification](https://developers.google.com/machine-learning/glossary#classification-model)
and
[prediction](https://developers.google.com/machine-learning/glossary#prediction).
Traditional AI models learn from existing data to classify information or to
predict future outcomes based on historical patterns. Generative AI uses
[foundation models](#foundation-model) to generate new content like text,
images, audio, or videos. This new content is generated by learning the
underlying patterns and style of the training data, which effectively lets the
model create outputs that resemble the data that it was trained on.

Learn more about
[when to use generative AI](https://cloud.google.com/docs/ai-ml/generative-ai/generative-ai-or-traditional-ai)
and
[generative AI business use cases](https://cloud.google.com/docs/ai-ml/generative-ai/evaluate-define-generative-ai-use-case).

---

## grounding

*Grounding* is the process of connecting a model's output to verifiable sources
of information. These sources might provide practical, context-specific
information, such as internal company documentation, project-specific data, or
communication records. Grounding helps to improve the accuracy, reliability, and
usefulness of AI outputs by providing the model with access to specific data
sources. Grounding reduces the likelihood of *hallucinations*—instances where
the model generates content that isn't factual. A common type of grounding is
[retrieval-augmented generation (RAG)](#retrieval-augmented-generation),
which involves retrieving relevant external information to enhance the model's
responses.

For more information about grounding with Google Search, see
[Grounding overview](https://cloud.google.com/vertex-ai/generative-ai/docs/grounding/overview).

---

## large language model (LLM)

A *large language model (LLM)* is a text-driven foundational model that's
trained on a vast amount of data. LLMs are used to perform natural language
processing (NLP) tasks, such as text generation, machine translation, text
summarization, and question answering. The term *LLM* is sometimes used
interchangeably with [foundation models](#foundation-model). However, LLMs are
text-based, whereas foundation models can be trained with and receive input from
multiple modalities, including text, images, audio, and video.

To learn the patterns and relationships within language, LLMs use techniques
such as
[reinforcement learning](https://developers.google.com/machine-learning/glossary#reinforcement_learning)
and instruction [fine-tuning](#tuning). When you [design prompts](#prompting),
it's important to consider the various factors that can influence the model's
responses.

---

## latency

*Latency* is the time that it takes for a model to process an input prompt and
generate a response. When you examine the latency of a model, consider the
following:

- **Time to First Token (TTFT)**: the time that it takes for the model to
  produce the first token of the response after it receives the prompt. TTFT
  is important for streaming applications where you want immediate feedback.
- **Time to Last Token (TTLT)**: the total time that the model takes to
  process the prompt and generate the complete response.

For information about reducing latency, see
[Best practices with large language models (LLMs)](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompt-best-practices).

---

## prompt engineering

*Prompt engineering* is the iterative process of creating a prompt and accessing
the model's response to get the response that you want. Writing well-structured
prompts can be an essential part of ensuring accurate, high quality responses
from a language model.

The following are common techniques that you can use to improve responses:

- **Zero-shot prompting**: provide a prompt without any examples and rely
  on the model's pre-existing knowledge.
- **One-shot prompting**: provide a single example in the prompt to guide
  the model's response.
- **Few-shot prompting**: provide multiple examples in the prompt to
  demonstrate the pattern or task that you want.

When you provide a model with examples, you help to control aspects of the
model's response, such as formatting, phrasing, scope, and overall patterns.
Effective few-shot prompts combine clear instructions with specific and varied
examples. It's important to experiment to determine the optimal number of
examples; too few examples might not provide enough guidance, but too many
examples can cause the model to overfit to the examples and fail to generalize
well.

For more information about best practices for prompting, see
[Overview of prompting strategies](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/prompt-design-strategies).

---

## prompting

A *prompt* is a natural language request that's sent to a generative AI model to
elicit a response. Depending on the model, a prompt can contain text, images,
videos, audio, documents, and other modalities or even multiple modalities
(multimodal).

An effective prompt consists of content and structure. Content provides all
relevant task information, such as instructions, examples, and context.
Structure ensures efficient parsing through organization, including ordering,
labeling, and delimiters. Depending on the output that you want, you might
consider additional
[components](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/prompt-design-strategies#components-of-a-prompt).

---

## model parameters

*Model parameters* are internal variables that a model uses to determine how the
model processes input data and how it generates outputs. During training, you
can adjust model parameters, such as weight and bias, to optimize the model's
performance. During inference, you can influence the model's output through
various prompting parameters, which doesn't directly change the learned model
parameters.

The following are some of the prompting parameters that affect content
generation in the Gemini API in Vertex AI:

- [temperature](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/inference#temperature):
  temperature changes the randomness of token selection during response
  generation, which influences the creativity and predictability of the
  output. The value of `temperature` ranges from `0` to `1`. Lower
  temperatures (closer to `0`) produce more deterministic and predictable
  results. Higher temperatures (closer to `1`) generate more diverse and
  creative text, but the results are potentially less coherent.
- [topP](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/inference#top-p):
  Top-P changes how the model samples and selects tokens for output. Top-P
  selects the smallest set of tokens whose cumulative probability exceeds a
  threshold, or `p`, and then samples from that distribution. The value of
  `topP` ranges from `0` to `1`. For example, if tokens A, B, and C have a
  probability of 0.3, 0.2, and 0.1, and the `topP` value is `0.5`, then the
  model will select either A or B as the next token by using temperature, and
  it will exclude C as a candidate.
- [topK](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/inference#topK):
  Top-K changes how the model samples and selects tokens for output. Top-K
  selects the most statistically likely tokens to generate a response. The
  value of `topK` represents a number of tokens from `1` to `40`, which the
  model will choose from before it generates a response. For example, if
  tokens A, B, C, and D have a probability of 0.6, 0.5, 0.2, and 0.1 and the
  top-K value is `3`, then the model will select either A, B, or C as the
  next token by using temperature, and it will exclude D as a candidate.
- [maxOutputTokens](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/inference#maxOutputTokens):
  the `maxOutputTokens` setting changes the maximum number of tokens that can
  be generated in the response. A lower value will generate shorter responses
  and a higher value will generate potentially longer responses.

For more information about sampling parameters in the
Gemini API in Vertex AI, see
[Content generation parameters](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/content-generation-parameters).

---

## retrieval-augmented generation (RAG)

*Retrieval-augmented generation (RAG)* is a technique to improve the quality
and accuracy of [large language model (LLM)](#large-language-model) output by
[grounding](#grounding) it with sources of knowledge that are retrieved after
the model was trained. RAG addresses LLM limitations, such as factual
inaccuracies, lack of access to current or specialized information, and
inability to cite sources. By providing access to information that's retrieved
from trusted knowledge bases or documents—including data that the model wasn't
trained on, proprietary data, or sensitive user-specific data—RAG enables LLMs
to generate more reliable and contextually relevant responses.

When a model that uses RAG receives your prompt, the RAG process completes these
stages:

1. **Retrieve**: search for data that's relevant to the prompt.
2. **Augment**: append the data that's retrieved to the prompt.
3. **Generate**:
  1. Instruct the LLM to create a summary or response that's based
    on the augmented prompt.
  2. Serve the response back.

For more information about Vertex AI and RAG, see
[Vertex AI RAG Engine overview](https://cloud.google.com/vertex-ai/generative-ai/docs/rag-overview).

---

## tokens

A *token* is a basic unit of data that a foundation model processes. Models
separate data in a prompt into tokens for processing. The set of all of the
tokens that are used by a model is called the *vocabulary*. Tokens can be single
characters like `z`, whole words like `cat`, or parts from longer words.

*Tokenizers* separate long words—such as complex or technical terms, compound
words, or words with punctuation and special characters—into several tokens. The
process of splitting text into tokens is called *tokenization*. The goal of
tokenization is to create tokens with semantic meaning that can be recombined to
understand the original word. For example, the word "predefined" can be split
into the following tokens: "pre", "define", "ed".

Tokens can represent multimodal input like images, videos, and audio.
[Embedding](#embedding) techniques transform multimodal input into numerical
representations that the model can process as tokens. The following are the
approximate token calculations for an example multimodal input, regardless of
display or file size:

- Images: 258 total tokens
- Video: 263 tokens per second
- Audio: 32 tokens per second

Each model has a limit on the number of tokens that it can handle in a prompt
and response. Additionally, model usage costs are calculated based on the number
of input and output tokens. For information about how to get the token count of
a prompt that was sent to a Gemini model, see
[List and count tokens](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/list-token).
For information about the cost of generative AI models on
Vertex AI, see
[Vertex AI pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing).

---

## tuning

*Tuning* is the process of adapting a
[foundation model](#foundation-model) to perform specific tasks with greater
precision and accuracy. Tuning is achieved by adjusting some or all of the
model's parameters or training a model on a dataset that contains examples that
replicate the tasks and results that you want. Tuning is an iterative process,
which can be complex and costly, but it has the potential to yield significant
performance improvements. Tuning is most effective when you have a labeled
dataset that has more than 100 examples, and you want to perform complex or
unique tasks where [prompting techniques](#prompt-engineering) aren't
sufficient.

The following are tuning techniques that are supported by
[Vertex AI](https://cloud.google.com/vertex-ai):

- **Full fine-tuning**: a technique that updates all of the model's parameters
  during the tuning process. Full fine-tuning can be computationally expensive
  and it can require a lot of data, but it also has the potential to achieve
  the highest levels of performance, especially for complex tasks.
- **Parameter-efficient tuning**: a technique that's also known as
  *adapter tuning*; parameter-efficient tuning updates some of the model's
  parameters during the tuning process. Parameter-efficient tuning is more
  resource efficient and more cost effective compared to full fine-tuning.
- **Supervised fine-tuning**: a technique that trains the model on labeled
  input-output pairs. Supervised fine-tuning is commonly used for tasks that
  involve classification, translation, and summarization.

For more information about tuning, see
[Introduction to tuning](https://cloud.google.com/vertex-ai/generative-ai/docs/models/tune-models).

   Was this helpful?
