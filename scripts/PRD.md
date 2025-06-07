<context>
# Overview
ACME Corp's travel reimbursement system is a 60-year-old black box. No one understands its logic, the source code is lost, and documentation is non-existent. The goal is to reverse-engineer this system to enable a transition to a modern, maintainable solution by creating a perfect replica of its calculation engine, including any bugs.

# Core Features
The replicated system will have one core feature: calculating a reimbursement amount.
- **What it does**: It takes `trip_duration_days` (integer), `miles_traveled` (integer), and `total_receipts_amount` (float) as input and produces a single `reimbursement_amount` (float, rounded to two decimal places).
- **Why it's important**: It provides a trusted baseline for understanding the legacy system's behavior before making improvements.
- **How it works**: The logic will be inferred by analyzing historical data (`public_cases.json`) and employee interviews (`INTERVIEWS.md`).

# User Experience
The system is non-interactive and has no user interface. It is a command-line tool that takes three arguments and outputs a single number.
- **User Personas**: Developers and system analysts who will use this tool to validate the replicated logic.
- **Key User Flows**: The only flow is executing the script with the required parameters and receiving the output.
- **UI/UX Considerations**: Not applicable.
</context>
<PRD>
# Technical Architecture
The solution will be a script (`run.sh`) that can be executed from the command line.
- **System Components**: A single script, likely calling a Python or other scripting language interpreter, containing the full reimbursement logic.
- **Data Models**: No complex data models are needed. The inputs are three numerical values, and the output is one.
- **APIs and Integrations**: No external APIs or integrations are permitted.
- **Infrastructure Requirements**: The script must run on a standard Linux environment with no external dependencies.

# Development Roadmap
The project will be developed in three phases.
- **Phase 1: Data Analysis & Hypothesis Generation**: Analyze `public_cases.json` and `INTERVIEWS.md` to formulate initial hypotheses about the calculation logic.
- **Phase 2: Initial Implementation & Testing**: Build a V1 script based on the initial hypotheses and test it using `./eval.sh` to establish a baseline score.
- **Phase 3: Iterative Refinement**: Continuously analyze errors, refine the logic, update the script, and re-test until the score against public cases is minimized.

# Logical Dependency Chain
The development process must follow a specific order.
1.  **Analysis First**: A thorough analysis of `public_cases.json` and `INTERVIEWS.md` is foundational and must precede implementation.
2.  **Build a Basic Model**: Implement a simple version of the logic first to get a working, testable script.
3.  **Iterate on Complexity**: Layer on more complex rules, edge cases, and bug replications based on feedback from the evaluation script.

# Risks and Mitigations
- **Technical Challenges**: The logic may be highly convoluted and non-linear. Mitigation involves structured iteration and careful error analysis to find patterns.
- **Inaccurate Data/Interviews**: The provided hints may be contradictory or incorrect. Mitigation is to trust the `public_cases.json` data as the source of truth when conflicts arise.
- **Scope Creep**: Over-engineering a solution beyond what the data supports. Mitigation is to stick to the simplest explanation that fits the data.

# Appendix
- **Success Criteria**: Success is defined by the lowest possible error score on `public_cases.json` and, ultimately, the highest number of exact matches against the unseen `private_cases.json`.
- **Resources**: `public_cases.json`, `INTERVIEWS.md`, `run.sh.template`, `eval.sh`.
</PRD> 