# Project Structure 📁

Automatic codegen using various hierarchical agent flows.

## Project Checklist ✅

- [✅] `./main.py` - Main script to run the project
- [✅] `./readme.md` - The project documentation

### Hierarchies

This is the core of the problem: how can we combine different agents and context to generate codebases?

Hierarchies are sequences of agent executions and different combinations of context provided at each stage.

### Agents 🤖

- [🚧] `./agents/builder_agent.py` - Defines the builder agent, which focuses on specific features
- [🚧] `./agents/planning_agent.py` - Defines the planning agent, which plans a task from a high-level

### Context 📚

The context folder enriches agents' prompts with necessary information and long-term memory. For example, it allows an agent to view the documentation for the framework that the project is using.

- [✅] `./context/fetch_commits.py` - Fetches commit data for a set of files
- [✅] `./context/fetch_docs.py` - Fetches framework documentation, e.g. NextJS docs
- [🚧] `./context/fetch_files.py` - Fetches file data for the project

### Embedding 🧩

- [✅] `./embedding/embed.py` - Embedding script for data processing
- [🚧] `./embedding/finetune.py` - Fine-tuning script for the embedding model

### Evaluation 📊

This allows the agents to determine if what they're doing is working.

- [🚧] `./eval/build.py` - Build evaluation script. Extracts from the package's build script and runs it with human consent and a high-level overview of existing commit changes.
- [🚧] `./eval/tsc.py` - TypeScript compilation script

### Infrastructure 🏗️

- [✅] `./infra/cache.py` - Cache management

### Models 🧠

- [✅] `./models.py/gpt4.py` - GPT-4 model for completions

### Utilities 🔧

- [✅] `./utils/process_repo.py` - Script to process repository data
- [🚧] `./utils/describe_commits.py` - Script to describe existing commits in English so the human can quickly review and give consent to run the code

## Contributing 🙌

Please feel free to submit pull requests, open issues, or contact the maintainers if you have any questions or suggestions.
