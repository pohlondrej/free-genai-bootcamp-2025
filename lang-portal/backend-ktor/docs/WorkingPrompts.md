# Working prompts
## Prompts for documentation generation:
#### For EACH API endpoint, generate example JSON string response so that it maps to the database schema. Hint: I don't want you to write code, just JSON responses.
- Worked fine, but left out last 6 JSON examples. Did it time out?
  - No, it ran out of response tokens. Increased response tokens to 20000.
- Markdown formatting is not great.
##### Follow-up prompt: You missed a couple of JSON responses, can you complete them for these two endpoints?
- Worked fine.
#### Can you generate complete Swagger documentation based on the API specification?
- Easy.
## Prompts for code generation
#### Can you generate data class for each database table? These data classes should be serializable using Kotlin Serialization. Each should be individual file. Each file should be in com.pohlondrej.langportal.backend.data package. If a key contains an underscore, it should be replaced by camelCase and a SerialName annotation with the actual name.
- Needed to be told about underscores and packages, but otherwise piece of cake.
## Random prompts
#### Where can I get kotlinx.datetime.LocalDateTime from? I'm using version catalog and Ktor.