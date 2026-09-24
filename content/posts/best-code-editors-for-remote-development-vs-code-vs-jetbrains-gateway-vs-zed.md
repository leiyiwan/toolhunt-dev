---
title: "Best Code Editors for Remote Development: VS Code vs JetBrains Gateway vs Zed"
date: 2026-09-24T14:02:56+08:00
draft: false
tags:

---

# Best Code Editors for Remote Development: VS Code vs JetBrains Gateway vs Zed

Remote development stopped being a niche workflow somewhere around 2020, and it never looked back. GitHub's Octoverse report has consistently shown tens of millions of developers working across distributed teams, and surveys from Stack Overflow and JetBrains put remote or hybrid work at the majority of professional developers in the US. When your code runs on a cloud VM, a beefy home lab, or a container in a data center two time zones away, the editor you choose stops being a matter of taste and starts being a matter of architecture.

Three tools dominate this conversation right now: Visual Studio Code with Remote Development, JetBrains Gateway, and Zed. Each takes a fundamentally different approach to the problem, and understanding those differences matters more than comparing feature checklists.

## The Core Problem: Where Does Your Code Actually Live?

A laptop with 16GB of RAM can't comfortably index a monorepo with three million lines of code, and it definitely can't do it while running Docker, a database, and a test suite. Remote development flips the model: the heavy lifting happens on a remote machine, and your local device becomes a thin client for editing and terminal access.

The three tools here solve that problem in three distinct ways:

- **VS Code** runs a full server process on the remote machine and connects over SSH, tunnels, or containers.
- **JetBrains Gateway** runs a headless IntelliJ-based backend remotely while a thin client handles the UI.
- **Zed** built remote development into its core architecture from the start, using its own collaboration protocol.

## VS Code Remote Development: The Default Choice

Microsoft shipped Remote Development in 2019, and it's now the reference implementation most developers compare everything else against. The model is straightforward: install the Remote - SSH, Dev Containers, or WSL extension, point it at a host, and VS Code installs a lightweight server on the other end. Extensions run remotely too, which is why language servers, linters, and debuggers behave the same as they would locally.

**Strengths:**

- **Maturity.** This has been in production for over five years. Edge cases around port forwarding, SSH agent forwarding, and multi-hop connections are well documented.
- **Dev Containers.** The `devcontainer.json` spec has become a de facto standard. You can define a reproducible environment and share it with your team, and GitHub Codespaces uses the same format.
- **Extension ecosystem.** Over 50,000 extensions exist, and the vast majority work in remote mode without modification.
- **Cost.** Free for individual use, and the server component is open source under the MIT license.

**Weaknesses:**

- **Resource usage.** The remote server process typically consumes 300–600MB of RAM on the remote host, which adds up if you're paying for a small cloud instance.
- **Electron client.** VS Code's desktop app is still Electron-based, which means it's heavier on your local machine than native alternatives.
- **Latency sensitivity.** Typing feels fine, but file operations on slow connections can stutter. The experience degrades noticeably above roughly 100ms of round-trip latency.

For most teams, VS Code is the safe answer. It's not the fastest or the most elegant, but it's the one that will work with the least amount of fighting.

## JetBrains Gateway: Full IDE Power, Remotely

JetBrains took a different route. Rather than extending an existing editor, Gateway is a thin client that connects to a headless backend running the full IntelliJ platform on the remote machine. You get the complete IDE—refactoring tools, database integration, profilers, the whole thing—but the compute happens elsewhere.

**Strengths:**

- **Deep language intelligence.** For Java, Kotlin, Python, Go, and other languages with first-class JetBrains support, the code analysis is genuinely more sophisticated than what VS Code offers out of the box.
- **Consistent experience.** If you already use IntelliJ IDEA, PyCharm, or GoLand locally, Gateway feels identical. Keybindings, plugins, and settings carry over.
- **Backend flexibility.** Gateway supports SSH, Dev Containers, WSL, and JetBrains' own cloud offering (formerly Space, now integrated into other products).

**Weaknesses:**

- **Licensing.** Gateway itself is free, but the backend IDE requires a paid JetBrains subscription for most languages. There's a free tier for some use cases, but commercial work generally requires a license.
- **Resource appetite.** The remote backend is heavy—typically 1.5–3GB of RAM for a mid-sized project. That's fine on a 16GB cloud VM, less fine on a $5/month instance.
- **Connection requirements.** JetBrains recommends latency under 50ms for a smooth experience. Above that, the UI can feel sluggish in ways that VS Code's architecture handles more gracefully.
- **Setup friction.** Getting Gateway working smoothly with SSH keys, port forwarding, and corporate proxies takes more effort than VS Code in my experience, though JetBrains has improved this considerably since the 2022 releases.

Gateway is the right call if you're already invested in the JetBrains ecosystem or working in a language where its tooling is meaningfully better—JVM languages, primarily, but also Python and Go.

## Zed: The Native, Performance-First Contender

Zed is the newest of the three, launched by the team behind Atom in 2023 and written in Rust with a GPU-accelerated UI. Its remote development story is built on the same CRDT-based collaboration protocol that powers its multiplayer editing, which means remote connections are a first-class feature rather than a bolt-on.

**Strengths:**

- **Speed.** Zed opens instantly and stays responsive. The local client uses a fraction of the memory that VS Code or a JetBrains client does.
- **Low-latency architecture.** Because remote development uses the same protocol as real-time collaboration, it handles higher latencies better than you'd expect. The team has demonstrated usable editing at 200ms+ round-trip times.
- **Clean design.** The UI is minimal and fast, and the AI features (inline assists, agentic editing) are integrated rather than bolted on.

**Weaknesses:**

- **Extension ecosystem.** Zed's extension library is growing but remains small compared to VS Code. If your workflow depends on a specific extension, check availability first.
- **Language support.** Core languages are well supported, but niche languages may lack the depth you'd get from VS Code or JetBrains.
- **Remote setup.** Zed's remote server must be installed on the target machine, and the process is less automated than VS Code's one-click SSH flow. It also currently requires a Zed account for remote connections.
- **Platform support.** Linux and macOS are fully supported; Windows support has been improving but historically lagged.

Zed is the tool to watch. It's not yet the tool to bet your team's workflow on unless you're comfortable being an early adopter.

## How to Choose

The decision usually comes down to three questions:

**What language are you writing?** JVM and Python developers with JetBrains licenses will get more value from Gateway. Everyone else will probably be happier with VS Code or Zed.

**How good is your connection?** Under 50ms, all three feel great. Between 50 and 150ms, VS Code and Zed hold up better than Gateway. Above 150ms, Zed's architecture has a real advantage.

**How much do you depend on extensions?** If your workflow hinges on specific VS Code extensions, that's the answer. Zed's ecosystem isn't there yet, and JetBrains plugins are a different universe entirely.

For most developers reading this, VS Code is the pragmatic default. JetBrains Gateway is the specialist's tool. Zed is the one that might be the default in two years—but isn't quite yet.

## The Takeaway

Remote development has matured to the point where the editor matters less than the workflow around it. All three tools handle the basics competently: editing, terminals, debugging, port forwarding. The real differentiators are latency tolerance, ecosystem depth, and how much you're willing to trade in setup complexity for performance. Pick based on your language, your connection, and your tolerance for being on the bleeding edge—then revisit the decision in a year, because this space is moving fast.