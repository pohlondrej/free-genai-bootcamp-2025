# Action Plan

## Tasks

### 1. Project Setup and Exploration

* Study ChatQnA example in `GenAIExamples/`:
    * Identify the model(s) used
    * Understand the architecture and components
    * Document findings in `Learnings.md`
* Evaluate vLLM compatibility:
    * Check if original models can run with vLLM
    * Research alternative models if needed
    * Document model requirements and constraints

### 2. Integration and Adaptation

* Create vLLM service configuration:
    * Set up CPU-compatible container
    * Configure model weights mounting
    * Implement OpenAI-compatible API endpoints
* Adapt ChatQnA components:
    * Modify API calls to use vLLM service
    * Adjust configuration for CPU deployment

### 3. Deployment and Testing

* Deploy adapted service:
    * Test basic model loading
    * Verify API endpoints
    * Document any issues or learnings
* Iterate based on findings:
    * Optimize for CPU performance
    * Troubleshoot integration issues
    * Record all significant learnings
