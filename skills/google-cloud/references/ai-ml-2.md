# Stay organized with collectionsSave and categorize content based on your preferences.

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
