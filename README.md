# CrewAI Alfresco Sample using LangChain-OpenDMA Integration

This sample shows how to give CrewAI agents access to documents stored in
Alfresco through the LangChain OpenDMA toolkit. Read [How to give CrewAI agents access to documents in Alfresco](https://dev.to/stefankopfxaldon/how-to-give-crewai-agents-access-to-documents-in-alfresco-4g2a) for the full story.

The sample does not ingest the Alfresco site into a vector store. The researcher
agent uses repository tools to discover the site, search documents, inspect
metadata and read selected document text.

## What This Demonstrates

- CrewAI using LangChain tools through CrewAI's built-in LangChain tool adapter.
- `AlfrescoToolkit` from `langchain-opendma`.
- A two-agent CrewAI workflow:
  - `Repository Researcher` with Alfresco/OpenDMA tools.
  - `Project Risk Analyst` without repository tools.
- A formal smoke-test command that checks the OpenDMA endpoint before any LLM
  call is made.

## Prerequisites

- Python 3.10 or newer.
- `uv`.
- A running Alfresco deployment.
- A running xaldon ECI Server exposing Alfresco as an OpenDMA endpoint.
- An OpenAI API key for the default model.

This README does not explain how to start Alfresco. It assumes Alfresco already
exists and focuses on exposing it through OpenDMA / ECI Server.

## Expose Alfresco Through OpenDMA / ECI Server

The sample expects an OpenDMA REST endpoint for Alfresco at:

```text
http://localhost:7070/opendma/alf
```

In ECI Server:

1. Open the web UI at `http://localhost:7070`.
2. Initialize the admin account.
3. Accept the license agreement.
4. Install a license key.
5. Navigate to `Admin` > `Connections`.
6. Add a new connection to `Alfresco Content Services`.
7. Use the connection settings for your Alfresco deployment.
8. Save the connection.
9. Navigate to `Admin` > `REST Endpoints`.
10. Add a new REST endpoint.
11. Set the slug to `opendma/alf`.
12. Select the Alfresco connection.
13. Keep inbound authentication as HTTP Basic / propagated inbound credentials
    unless your environment requires something else.
14. Save the endpoint.

Verify the endpoint in a browser:

```text
http://localhost:7070/opendma/alf/
```

Authenticate with Alfresco credentials that can read the Project Apollo site.

## Create The Project Apollo Site

Create an Alfresco site:

```text
Name: Project Apollo
Site ID: project-apollo
```

In the document library, create this folder structure:

```text
Contracts/
Reports/
Risks/
```

## Upload The Sample Project Apollo Files

Upload the files from `sample-data/` into the matching Alfresco folders:

```text
sample-data/
  Contracts/
    Supplier Agreement.md
    Service Agreement.md
  Reports/
    Status Report September.md
    Status Report October.md
  Risks/
    Risk Register.md
```

These sample files are Markdown on purpose. This demo is about repository
access from CrewAI agents, not document transformation. Keeping the files
text-like makes the tool trace easier to inspect.

## Configure Environment Variables

Copy `.env.example` to `.env` and adjust the values:

```bash
cp .env.example .env
```

```text
OPENDMA_ALFRESCO_ENDPOINT=http://localhost:7070/opendma/alf
OPENDMA_ALFRESCO_USERNAME=admin
OPENDMA_ALFRESCO_PASSWORD=admin
OPENDMA_ALFRESCO_REPOSITORY_ID=Alfresco
OPENAI_API_KEY=...
CREWAI_MODEL=openai/gpt-4o-mini
```

The default CrewAI model string is:

```text
openai/gpt-4o-mini
```

CrewAI also supports provider/model strings for other providers. Install the
required CrewAI extras and configure provider API keys before using them.

```text
# CREWAI_MODEL=anthropic/claude-3-5-haiku-latest
# CREWAI_MODEL=google/gemini-2.0-flash
```

## Install Dependencies

```bash
uv sync
```

## Run The Smoke Test

```bash
uv run alfresco-tools-smoke-test
```

The smoke test does not call an LLM. It creates the Alfresco toolkit, lists the
available tools, calls `alfresco_list_sites`, and verifies that `project-apollo`
is visible.

Use another site short name:

```bash
uv run alfresco-tools-smoke-test --site-short-name my-site
```

## Run The CrewAI Risk Briefing

Default Project Apollo question:

```bash
uv run alfresco-risk-briefing
```

Custom question:

```bash
uv run alfresco-risk-briefing \
  "Review the Project Apollo documents and identify the three most important project risks. Cite the documents supporting each finding."
```

More deterministic run with a site short-name hint:

```bash
uv run alfresco-risk-briefing \
  --site-short-name project-apollo \
  "Review the project documents and identify the three most important project risks. Cite the documents supporting each finding."
```

If `--site-short-name` is omitted, the researcher agent should use
`alfresco_list_sites` to discover the site matching the project name in the
question.

## Expected Trace

With verbose output enabled, you should see tool use similar to:

```text
alfresco_list_sites
opendma_search
opendma_list_children
opendma_get_metadata
opendma_read_text
```

The exact final answer depends on the model. It should identify risks such as:

- supplier delivery delay;
- unavailable cutover support;
- delayed retention-rule sign-off.

The final answer should cite Alfresco document names and object IDs.

## Further reading

- [How to give CrewAI agents access to documents in Alfresco](https://dev.to/stefankopfxaldon/how-to-give-crewai-agents-access-to-documents-in-alfresco-4g2a)
- OpenDMA: https://opendma.org/
- ECI Server: https://xaldon.com/products/eci-server
- LangChain OpenDMA integration: https://github.com/OpenDMA/langchain-opendma
- Tutorials: https://github.com/OpenDMA/langchain-opendma/tree/main/docs/tutorials
- LangChain OpenDMA Toolkit documentation: https://github.com/OpenDMA/langchain-opendma/blob/main/docs/Toolkit.md
