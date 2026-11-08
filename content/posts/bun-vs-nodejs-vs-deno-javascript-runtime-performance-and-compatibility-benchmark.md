---
title: "Bun vs Node.js vs Deno: JavaScript Runtime Performance and Compatibility Benchmarked"
date: 2026-11-08T18:05:31+08:00
draft: false
tags:

---

# Bun vs Node.js vs Deno: JavaScript Runtime Performance and Compatibility Benchmarked

A few years ago, "which JavaScript runtime?" had a one-word answer: Node.js. Today, developers weighing a new backend service or CLI tool have three credible options—Node.js, Deno, and Bun—each with a different philosophy about speed, security, and compatibility.

The marketing claims are easy to find. Bun's homepage leads with benchmark charts. Deno emphasizes its secure-by-default design. Node.js, now past its 20th anniversary, points to two decades of production hardening. What matters is how those claims hold up when you run the same code on all three. This article breaks down what the benchmarks actually show, where compatibility still breaks down, and how to decide which runtime fits your project.

## The Contenders at a Glance

**Node.js** is the incumbent. Built on the V8 engine (the same JavaScript engine inside Chrome), it runs the overwhelming majority of the npm ecosystem. Its release cadence is predictable: even-numbered versions become Long Term Support (LTS) releases, with roughly 30 months of maintenance.

**Deno** was created by Ryan Dahl, Node's original author, as a corrective to design decisions he later criticized. It also runs on V8 but ships TypeScript support natively, uses ES modules by default, and restricts file, network, and environment access unless explicitly granted. Deno 2, released in late 2024, added meaningful npm and Node compatibility—a tacit admission that ecosystem gravity is hard to escape.

**Bun** is the newest entrant, built by Oven. Rather than V8, it uses JavaScriptCore, the engine behind Safari. Bun bundles a runtime, package manager, test runner, and bundler into a single binary. Its pitch is simple: do everything Node does, but faster.

## Performance: What the Benchmarks Show

Synthetic benchmarks deserve skepticism—they measure micro-operations, not your application. Still, they reveal real architectural differences.

### HTTP Throughput

In the widely cited "Hello World" HTTP benchmarks that Bun publishes (and independent testers have largely reproduced, with varying margins), Bun consistently handles the most requests per second, Deno generally lands in the middle, and Node.js trails. The gaps vary enormously by test setup—sometimes Bun leads Node by 2x, sometimes by much less—but the ordering has been stable across multiple independent runs.

The caveat: a server that returns a static string exercises almost none of what production code does. Once you add database queries, JSON serialization of large payloads, authentication middleware, and logging, the runtime's raw HTTP overhead shrinks as a share of total request time.

### Startup Time

For CLI tools, serverless functions, and scripts, cold-start latency matters more than throughput. Here Bun's use of JavaScriptCore and its single-binary design give it a clear edge—typically starting several times faster than Node.js. Deno generally starts faster than Node but slower than Bun. If you're deploying to AWS Lambda or Cloudflare Workers-style environments where cold starts are billed and felt by users, this difference is tangible.

### Package Installation

Bun's package manager is dramatically faster than npm in most published comparisons, often completing installs in a fraction of the time. Part of the gain comes from its global module cache and binary lockfile; part comes from doing less validation. pnpm has narrowed the gap considerably, so the install-speed argument is strongest for teams still on plain npm.

### Compute-Bound Workloads

Here the picture is murkier. V8 (Node and Deno) has received years of optimization for hot loops and complex object manipulation. JavaScriptCore (Bun) is no slouch—it powers Safari—but results on CPU-heavy tasks like cryptography, compression, and large-scale data transformation are mixed, with each engine winning different micro-benchmarks. Treat claims of universal speed superiority with caution.

## Compatibility: The Real Deciding Factor

Performance differences of 20–50% on synthetic tests rarely justify a migration. Compatibility problems, on the other hand, can sink a project in a week.

### npm Ecosystem

Node.js remains the reference implementation: if a package works anywhere, it works there. Deno 2 and Bun both now support npm packages, including packages that rely on CommonJS, `node:` built-in modules, and `package.json` resolution. In practice, most popular libraries—Express, Fastify, Prisma, the AWS SDK—run on all three.

The failures cluster in edge cases: packages with native addons (node-gyp builds), deep reliance on Node internals, or assumptions about the module loader. Native addons are the biggest remaining gap—Bun supports a subset through its Node-API implementation, and Deno's support has improved but isn't universal. If your stack depends on a native database driver or image-processing library, verify it before committing.

### TypeScript

Deno and Bun run TypeScript directly with no build step. Node.js added type stripping in recent versions (23.6+ by default, with earlier versions behind a flag), but it strips types only—it does not type-check, and it doesn't handle features that require code generation, like enums in some configurations or decorators with metadata. All three runtimes ultimately expect you to type-check separately with `tsc`. The difference is convenience, not capability.

### Web Standard APIs

Deno and Bun both implement web-standard APIs—`fetch`, `WebSocket`, `Request`/`Response`, `crypto.subtle`—as first-class citizens. Node.js has adopted most of these too, but its older, callback-style APIs remain dominant in existing code. For new projects, all three are reasonably aligned with browser APIs; for porting existing browser code to the server, Deno and Bun tend to require fewer shims.

## Security and Tooling

Deno's permission model—no file, network, or environment access without flags—remains its most distinctive feature. Node.js introduced a similar experimental permission model, and Bun has announced intentions in this area but remains the most permissive by default. For running untrusted code or scripts pulled from the internet, Deno's defaults are meaningfully safer.

On tooling, Bun's all-in-one approach (runtime, package manager, test runner, bundler) reduces configuration overhead. Node.js counters with maturity: better debugging integration, broader IDE support, and a vast body of documentation and Stack Overflow answers. Deno sits between the two, with a built-in formatter, linter, and test runner.

## How to Choose

A practical decision framework:

- **Existing production services:** Stay on Node.js. The migration risk outweighs performance gains, and Node's LTS cadence provides stability that newer runtimes haven't yet proven at scale.
- **New APIs where cold start and throughput matter:** Bun is worth a serious evaluation, particularly for serverless deployments and high-request-volume services—provided your dependencies pass a compatibility audit.
- **Security-sensitive environments or TypeScript-first teams:** Deno's defaults and native TypeScript support reduce friction and attack surface.
- **CLI tools and scripts:** Bun's startup speed and bundled tooling make it genuinely pleasant; Deno's single-binary compilation is a strong alternative.

## The Bottom Line

Bun is fastest on the benchmarks that are easiest to measure—HTTP throughput, startup, installs—and its compatibility story has improved enough that most projects can at least try it. Deno offers the most principled design and the best security defaults, with compatibility that's now good enough for many real applications. Node.js remains the safest bet for production, backed by ecosystem depth and a decade of operational knowledge that no benchmark chart captures.

The honest takeaway: runtime performance differences are real but rarely decisive. Compatibility, tooling maturity, and team familiarity usually determine success. Pick the runtime that lets your team ship confidently—and benchmark your own workload, not someone else's Hello World.