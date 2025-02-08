## Functional Requirements
University wants to create a portal that allows students and researchers to share AI projects.

There should be an "AI Project Marketplace", which allows all members of the university to create, use, fork or publish various AI projects.

Due to lack of existing IT infrastructure, variable budget and rapid development of AI-acceleration hardware, cloud-hosted solution has been proposed.

The university has about 10K students and researchers, but only 1000 would require access to this system. A budget of $50/year per person has been allocated.

## Risks
- Running AI models in cloud may become more expensive in the coming years.
- If unchecked, one user can exhaust the entire budget in days.
    - Mitigation: Implement **Fair User Policy**, limiting users to $5/month.
    - Mitigation: Implement **Tiered Access**, as researchers may require more resources than students.
    - Mitigation: Cache common queries and results.
- Cache corruption and "cross-polination", resulting in performance degradation.
## Assumptions
- Models available on the market are capable of running wide range of user applications.
- Only 1000 people require access to the AI portal.
- A large cloud provider - e.g. GCP, AWS, Azure - will be used to host the portal.
    - Users won't have direct access to the cloud provider administration, only to the portal itself.
## Constraints
- Only university-approved models and applications will be available.
- Access will be granted on needs-basis (e.g. students enrolled in a class that requires interacting with the AI system).
## Data Strategy
- No personal information should be collected by the portal itself.
- Some research might be classified.
    - Classified research will require advanced encryption - it should be enforced automatically when creating a classified project.
    - Classified projects must not be publically visible in the AI Project Marketplace.
## Security & Safety
- Access to the portal will be handled through university SSO.
    - Might need an upgrade to handle more access levels.
- Since multiple will be hosted on the platform, the safety will be handled individually (depending on the project/application).
    - All projects will need to adhere to University's Code of Conduct.
        - Violations of Code of Conduct may result in temporary suspension of access to the system.
## Business Considerations
### "Power user" plan
Some users might require disproportionately more resources. A microbiology researchers might want to use an application to analyze protein structures, while mechanical engineering students might want to run a fluid dynamics simulation.

Allow these users access to computational resources that fit their budget, e.g. a research grant. *Note: Research grants typically range from $10K-$1M.*