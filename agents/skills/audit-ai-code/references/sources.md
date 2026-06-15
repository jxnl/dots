# Source basis

This skill is a quality and safety audit checklist, not proof of AI authorship. Use these references to ground the smell taxonomy and reviewer language.

- Wikipedia on code smells: `https://en.wikipedia.org/wiki/Code_smell`
- Refactoring.Guru smell catalog and refactorings, especially Duplicate Code, Long Method, Long Parameter List, Comments, and Speculative Generality: `https://refactoring.guru/refactoring/smells`
- Refactoring.Guru on Long Parameter List: long parameters can come from merged algorithms or misplaced object creation; fixes include preserving whole objects, replacing parameters with method calls, and parameter objects only when cohesive: `https://refactoring.guru/smells/long-parameter-list`
- Martin Fowler on Flag Arguments: boolean flags often obscure caller intent; prefer explicit methods when callers are choosing different behaviors, but derive decisions internally when the caller should not care: `https://martinfowler.com/bliki/FlagArgument.html`
- Google Testing Blog on "Test Behaviors, Not Methods": tests should target behaviors, not mirror method boundaries, and separate behaviors should stay in separate focused tests: `https://testing.googleblog.com/2014/04/testing-on-toilet-test-behaviors-not.html`
- GitHub Copilot responsible-use guidance for code review, including security checks and AI-generated suggestion risk: `https://docs.github.com/en/copilot/responsible-use/code-review`
- LLM-generated code smell study: `https://arxiv.org/abs/2510.03029`
- Package hallucination risk in AI-generated code: `https://www.usenix.org/publications/loginonline/we-have-package-you-comprehensive-analysis-package-hallucinations-code`
- Hallucinated API behavior in code-generation systems: `https://arxiv.org/abs/2401.01701`
