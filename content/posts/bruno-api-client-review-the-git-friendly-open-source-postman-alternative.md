---
title: "Bruno API Client Review: The Git-Friendly Open Source Postman Alternative"
date: 2026-09-14T14:05:42+08:00
draft: false
tags:

---

## Bruno API Client Review: The Git-Friendly Open Source Postman Alternative

API work has a version-control problem. Postman, the dominant client for exploring and testing APIs, stores collections in its own cloud or in proprietary JSON files that generate noisy diffs and merge conflicts. For teams that live in Git, this creates friction: reviewing an API change means eyeballing a wall of metadata rather than reading a clean diff.

Bruno, an open-source API client launched in 2023, takes a different approach. It stores each request as a plain-text `.bru` file on your local filesystem, designed to be committed alongside your code. That single design decision has earned it a fast-growing following among developers who want their API collections treated like source code. This review examines how Bruno works, where it shines, and where it still trails the incumbent.

## What Bruno Is and How It Works

Bruno is a desktop application for macOS, Windows, and Linux, built with Electron. It supports the standard features you'd expect from an API client: REST, GraphQL, and gRPC requests, environment variables, scripts, assertions, and a collection runner.

The defining feature is the file format. Instead of a monolithic JSON export, Bruno saves each request as a `.bru` file using a simple, human-readable syntax:

```
meta {
  name: Get Users
  type: http
  seq: 1
}

get {
  url: {{baseUrl}}/users
  body: none
  auth: none
}
```

A collection is just a folder of these files. You can open that folder in VS Code, diff it in a pull request, or resolve a merge conflict by hand without deciphering escaped JSON. Environments are stored as `.env` files, and secrets can be kept out of version control using `.gitignore` and a local-only secrets file.

Bruno also offers a CLI (`bru`) for running collections in CI pipelines, and a JavaScript-based scripting API for pre-request and post-response logic. Tests use a Chai-like assertion syntax that will feel familiar to anyone coming from Postman or Jest.

## The Git-Friendly Workflow in Practice

The pitch sounds good, but does it hold up? For the most part, yes.

Because each request is its own file, a pull request that adds an endpoint shows up as a small, readable diff. Reviewers can see exactly what changed: a header, a URL, a test assertion. This is a meaningful improvement over Postman's collection format, where a single change can ripple through hundreds of lines of generated IDs and ordering metadata.

Merge conflicts, while not eliminated, become tractable. Two developers editing different requests in the same collection won't collide at all, since they're editing separate files. When they do edit the same request, the conflict is a few lines of readable text rather than a JSON structure.

There's also a practical benefit for onboarding. A new engineer clones the repo and immediately has the full API collection, with no need to import a file from a shared workspace or request access to a cloud account.

One caveat: Bruno's local-first model means there's no built-in team sync. You rely on Git for sharing. That's the point, but teams accustomed to Postman's cloud collaboration—comments, shared workspaces, role-based access—will notice the difference. For some organizations, that's a feature; for others, a gap.

## Feature Set: What's Included and What's Missing

Bruno covers the core of day-to-day API work well:

- **Request types:** REST, GraphQL, and gRPC
- **Auth:** Basic, Bearer, API key, OAuth 2.0, AWS Signature, Digest, NTLM
- **Variables:** Collection, environment, and runtime variables with `{{variable}}` interpolation
- **Scripting:** Pre-request and post-response JavaScript, with a built-in library of helpers
- **Testing:** Assertions via `expect()` syntax, plus a collection runner with pass/fail reporting
- **CLI:** `bru run` for headless execution in CI/CD
- **Import:** Postman, Insomnia, OpenAPI, and cURL

That's a solid foundation. Where Bruno still lags Postman is in the long tail: mock servers, API documentation generation, monitoring and scheduled runs, and the broader ecosystem of integrations. Postman has spent a decade building those features, and Bruno hasn't tried to match them one-for-one.

The scripting API is also less mature. Postman's `pm.*` namespace is deeply documented and widely copied across the web; Bruno's equivalents cover the common cases but have fewer Stack Overflow answers when something goes wrong. Developers migrating large Postman collections with heavy scripting should expect to rewrite some of that logic.

## Pricing, Licensing, and the Open-Source Model

Bruno's core application is open source under the MIT license, with the codebase on GitHub. The desktop app is free to download and use, and there's no account requirement—you can work entirely offline.

The company monetizes through a paid tier aimed at teams, which adds features like a built-in secret manager and organization-level collaboration. This is a common open-core arrangement, and it's worth understanding before you commit: the free version is genuinely functional, but some team-oriented conveniences sit behind the paywall.

Compared to Postman's pricing—which moved several previously free features into paid tiers in 2023, prompting significant user backlash—Bruno's free tier feels generous. Postman's free plan limits collaboration to a small number of users, while Bruno's Git-based sharing has no such limit as long as you're managing your own repository.

## Who Should Consider Bruno

Bruno fits best in a few specific situations:

**Small to mid-sized engineering teams** that already treat infrastructure as code and want API collections in the same repository as the services they test. The Git workflow is the whole value proposition, and it delivers.

**Individual developers** who want a fast, offline-capable client without creating yet another account. Bruno starts quickly and stays out of the way.

**Open-source projects** that want to ship a runnable API collection alongside their code, so contributors can test endpoints without importing anything.

It's a weaker fit for **large enterprises** that depend on Postman's governance features, centralized workspaces, or API documentation tooling. It's also less ideal for **non-technical stakeholders** who need to browse an API without touching Git.

## The Bottom Line

Bruno's core insight—that API collections are code and should be versioned like code—is simple and correct. The execution is polished enough for daily use, the file format is genuinely pleasant, and the open-source model removes the account and pricing friction that has frustrated many Postman users.

It is not a complete Postman replacement. If your workflow depends on mock servers, generated documentation, or cloud collaboration, you'll miss those features. But if your team lives in Git and wants API requests to travel with the code they test, Bruno is the most sensible option available today—and it's improving quickly.