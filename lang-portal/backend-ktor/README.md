# Lang Portal Backend (Ktor)
I decided to build backend using Ktor, a kotlin-based framework for client-server applications. 

Technical specs are in [Project.md](docs/Project.md) file!

## Takeaways
I followed the backend API specification from the bootcamp video. I wanted to work with IntelliJ IDE, and so I searched for various copilot plugins. After trying 4 different plugins, I settled on Proxy AI, as it was the most flexible one. Eventually, I switched to Gemini 2.0 Flash, which worked amazingly well as a "copilot", as it was able to work with the full context of the project.

I also experimented with the trial version of Windsurf, but quickly ran out of the Claude queries, and the free model performed poorly.

But with help of AI, I was able to build a working (ish) server.

Key takeaway: if the library is new or unstable, the AI tools struggle to generate valid code. Rather than using bleeding edge, it's better to choose a widely used solution.

## Why Ktor
- I know Kotlin, that's what I do for a living.
- I never used Ktor and so I wanted to try it out.
- I wanted to work with IntelliJ Idea and I wanted to see how well the AI integrates and what's the best plugin.

## Intellij Idea Plugin Evaluation
- OllamAssist - has potential, but very early in development.
- Continue - utter garbage, at least in IntelliJ.
- JetBrains AI Assistant - good, fast, but expensive; tried trial version only.
- CodeGPT - my favourite so far, very good chat, allows cloud API integration as well as local models; autocomplete is a hit or miss, though
    - CodeGPT got renamed to ProxyAI and added support for Gemini 2.0 Flash. No autocomplete, but very large context window.

## Local ollama models I tried with ProxyAI:
- deepseek-r1:14b - not good, the `<think>` tags break formatting
- llama3.1:8b - fast but dumb
- codegemma - same as llama above
- codestral - so far my favorite; slow-ish, but good output

## Building & Running

To build or run the project, use one of the following tasks:

| Task                          | Description                                                          |
| -------------------------------|---------------------------------------------------------------------- |
| `./gradlew test`              | Run the tests                                                        |
| `./gradlew build`             | Build everything                                                     |
| `buildFatJar`                 | Build an executable JAR of the server with all dependencies included |
| `buildImage`                  | Build the docker image to use with the fat JAR                       |
| `publishImageToLocalRegistry` | Publish the docker image locally                                     |
| `run`                         | Run the server                                                       |
| `runDocker`                   | Run using the local docker image                                     |

If the server starts successfully, you'll see the following output:

```
2024-12-04 14:32:45.584 [main] INFO  Application - Application started in 0.303 seconds.
2024-12-04 14:32:45.682 [main] INFO  Application - Responding at http://0.0.0.0:8080
```

## Testing
### Swagger
When server is running, navigate to `http://0.0.0.0:8080/openapi`.
*NOTE: Swagger documentation might be a little out of date.*
