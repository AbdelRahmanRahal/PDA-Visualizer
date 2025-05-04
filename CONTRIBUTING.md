# 🔤 PDA Visualizer – Contribution Guidelines & Project Structure

Welcome to the PDA Visualizer repository! This document outlines the structure, contribution guidelines, and best practices for all collaborators. Please read carefully before making changes to the codebase.

## 📁 Repository Structure

Here's a general overview of how this repository is organized:
```PlainText
/pda-visualizer/
│
├── /docs/               # Project documentation, architecture, diagrams IF REQUIRED
├── /src/                # Core source code (frontend/backend, as applicable)
│   ├── /gui/            # UI components and reusable widgets
│   ├── /pda/            # PDA logic
│   └── main.py          # Entry point
│
├── .gitignore
├── CONTRIBUTING.md      # You're reading it!
├── README.md            # Project overview, installation instructions
└── requirements.txt     # Python dependencies
```

## ✅ Contribution Rules
> #### 🔐 Version Control Discipline is mandatory
> This is a collaborative academic project. Every commit, branch, and pull request must follow our agreed process to ensure smooth teamwork and accountability.

### 📌 Branching Rules
- 🔀 Main Branch (`main`)
  - This represents the final version that will be uploaded to Moodle.
  - Do not commit directly to this branch.
  - All merges into `main` must come via pull requests (PRs) approved by at least one other person.
- 🌿 Feature Branches
  - Each team member should work on their own feature branch.
  - You may name it after your task or name, e.g., `nour-visualizer`, `rahal-parser`.
  - Do not commit directly on someone else's branch.
- 👥 Collaboration Branches
  - To work together, create a shared branch, e.g., `rahal-nour`.
  - Be sure to communicate and resolve merge conflicts together if needed.

### 🧠 Code Philosophy
- **⚖️ Less is More**

  Simplicity is king. Prioritize minimal, understandable code over clever hacks or bloated libraries.

- **🎯 Stick to Scope**

  Avoid scope creep. Everything added must contribute clearly to the PDA visualizer's core goals.

- **📣 Communicate!**

  Regularly discuss how your modules interact. Avoid duplication and tightly coupled code.

## 🔍 Code Standards & Best Practices
- ✅ Follow [PEP8](https://peps.python.org/pep-0008/) for Python (IMPORTANT). You may use [this tool](https://formatter.org/python-formatter) to help you.
- 🧼 Document your code using clear inline comments and docstrings.
- 🔄 Avoid duplicate logic. Reuse functions and components.
- 📁 Organize files in a modular and predictable manner.
- ⏱️ Use version control wisely. Commit small, meaningful changes with clear messages.

## 📄 Pull Request Template
When creating a PR, include the following:
- What was added or changed
- Why it’s needed
- Any known issues or TODOs
- Screenshots or demo (if UI-related)

## 🚦 Commit Message Guidelines
Use clear and consistent commit messages:
```PlainText
feat: added input parser for PDA
fix: resolved crash on invalid transition
docs: added architecture diagram
refactor: simplified state transition logic
```

## 🙌 Thanks!
Your thoughtful contributions make this project awesome. Let’s build something simple, elegant, and effective together!
