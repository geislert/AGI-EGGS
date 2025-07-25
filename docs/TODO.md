# AGI-EGGS Project Tracker

This file tracks ongoing tasks and notes for improving the repository. It is
maintained by the Codex agent and can store temporary data or references for
future work.

## Prioritized TODO List (July 2025)

1. **Fix and expand README**
   - Finish the civil liberties simulation section which ends abruptly.
   - Add usage instructions for all example scripts.
   - Link to the license.

2. **Add automated tests**
   - Create a `tests/` directory using `pytest`.
   - Tests should cover starting nodes, sending/receiving messages and
     persisting queued messages.

3. **Package configuration**
   - Provide a `pyproject.toml` or `setup.py` for pip installation.
   - Specify minimal dependencies.

4. **Continuous Integration**
   - Add a CI workflow (e.g. GitHub Actions) running the test suite.
   - Optionally include linting.

5. **Enhance example scripts**
   - Include short descriptions and consolidate repetitive setup logic.

6. **Document additional modules**
   - Explain `modules/psych_support.py` in the README or separate docs.

7. **Add Phoenix Project documentation**
   - Summarize the "Project Phoenix: Omega Directive" manifesto in a new doc
     and clarify which concepts are implemented vs. conceptual.

8. **Future features**
   - Encryption/authentication for network connections.
   - Command-line option for message store paths.
   - Tutorial/walkthrough.

---

Additional documentation, such as research into historical influences or other
context, can be kept in the `docs/` directory as needed.
