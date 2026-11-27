# Run conditions (AI-agent benchmark V1)

Runs: 27 November 2026, each model as a sub-agent with a file system and shell, default settings of the agent environment.
Models: Claude Haiku 5.5 (claude-haiku-5-5), Claude Sonnet 5.5 (claude-sonnet-5-5), Claude Opus 5.5 (claude-opus-5-5).

Each agent received the task file for its set (tasks_set1.md, tasks_set2.md, tasks_set3.md, whose headers hold the
answer instructions) and wrote its answers to a JSON or Markdown file. It had no access to the references.

Condition instructions (summary; the verbatim wording was not archived):
- Reasoning only (sets 1 and 2): do not run any code or calculator; work every task by hand in your own reasoning.
- With code (sets 1 and 2): write and run Python for the calculations, as an engineer would use a calculation script.
  NumPy, SciPy, iapws and CoolProp were installed.
- Set 3: answer each design review once; Python allowed.
- All conditions: no web search; supply any data a task does not give.
