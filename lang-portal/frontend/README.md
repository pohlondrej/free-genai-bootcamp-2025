# React + TypeScript + Vite
## Challenges and solutions
That's right, I reused the original frontend from the ExamPro repository. However, there were many challenges to make it run:

1) Wayland + Vite incompatibility
  - I was facing an error, where `vite` didn't want to run under Wayland. I tried maybe 10 different things, until Copilot suggested updating vite dependency from v4 to v5. That solved the problem.
2) Various errors in backend code
  - By actually running the website, I discovered various logic errors in the backend.
    - Takeaway: Spend more time writing tests.
3) API incompatibilities
  - Turns out the ExamPro version of the frontend is quite different from the API from the "backend from scratch" video.
    - Thankfully, the `kotlinx.serialization` library allows adding serialization annotations, making it easy to modify the JSON responses.