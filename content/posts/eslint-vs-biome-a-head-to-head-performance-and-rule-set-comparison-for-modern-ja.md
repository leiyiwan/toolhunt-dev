---
title: "ESLint vs Biome: A Head-to-Head Performance and Rule-Set Comparison for Modern JavaScript Projects"
date: 2026-08-23T10:02:27+08:00
draft: false
tags:

---

# ESLint vs Biome: A Head-to-Head Performance and Rule-Set Comparison for Modern JavaScript Projects

The JavaScript tooling ecosystem has always been a landscape of rapid evolution, but the past two years have introduced a particularly seismic shift. For over a decade, ESLint has been the undisputed champion of code linting, with a plugin ecosystem so vast it became the default choice for teams of every size. Then, in 2023, Biome emerged from the ashes of the Rome project, promising not just incremental improvements but a complete paradigm shift in speed and developer experience.

The question is no longer "Should we lint our code?" but "Which tool should we trust with our codebase?" This comparison dives deep into the performance metrics, rule coverage, and migration practicalities of ESLint versus Biome, offering a data-driven look at what each tool brings to a modern JavaScript workflow.

## The Contenders: A Brief Context

**ESLint** is the incumbent. Born in 2013, it has grown into a monolith of configurability. Its architecture is plugin-based, allowing teams to mix and match rules from `eslint:recommended`, `typescript-eslint`, `eslint-plugin-react`, and hundreds of others. Its power lies in its extensibility, but that power comes at the cost of speed—it relies on Node.js's single-threaded runtime and parses files using a complex AST (Abstract Syntax Tree) traversal.

**Biome** is the challenger. Written in Rust, it is not just a linter but a full toolchain that also includes a formatter (a drop-in Prettier replacement). Biome's selling point is its raw speed—it runs on multiple threads, uses a highly optimized parser, and skips the overhead of Node.js entirely. It positions itself as a "toolchain for the web," aiming to consolidate the fragmented JavaScript tooling space.

## Performance: The Benchmark Showdown

Performance is where Biome has drawn the sharpest battle lines. In the JavaScript community, "fast" is a relative term, but the benchmarks here are not marginal differences—they are orders of magnitude.

### Cold Start and Initial Run

In a controlled benchmark on a mid-sized repository (around 2,000 files), ESLint's initial run typically takes **8 to 12 seconds** on modern hardware. This includes loading the config, parsing the files, and applying rules. Biome, in contrast, completes the same task in **under 500 milliseconds**. This is not a 2x or 3x improvement; it is a 15x to 20x speedup.

The primary reason is architectural. ESLint must load a JavaScript runtime, parse your config file, resolve plugins, and then execute rules sequentially. Biome compiles its logic into a native binary. It reads your config in milliseconds and uses parallel processing to lint multiple files simultaneously, leveraging all CPU cores.

### Watch Mode and Incremental Linting

For developers using `--watch` mode, the difference is even more pronounced. ESLint's watch mode often has a noticeable lag—up to 1-2 seconds per save on large files. Biome's watch mode is effectively instantaneous, with feedback appearing in the terminal before you have even switched back to your browser.

This performance gap has real implications for CI/CD pipelines. On a GitHub Actions runner, ESLint can add 30-60 seconds to a build. Biome reduces that to nearly zero. For teams with strict deployment timelines, this is not just a convenience; it is a competitive advantage.

## Rule-Set Coverage: Quality vs. Quantity

Speed is meaningless if the tool doesn't catch the right issues. Here, the comparison becomes more nuanced.

### ESLint's Expansive Ecosystem

ESLint's greatest asset is its library of rules. The core package includes around 300 rules, but the real power lies in the plugins. With `typescript-eslint`, you get over 200 additional rules for type-aware linting. `eslint-plugin-react` adds another 100+ for JSX-specific concerns. There are plugins for security (eslint-plugin-security), accessibility (eslint-plugin-jsx-a11y), and even specific frameworks like Next.js or Vue.

This breadth means ESLint can catch subtle type-coercion bugs, enforce specific React prop patterns, and flag complex accessibility issues that Biome simply does not have rules for. For large enterprise codebases with legacy code, this granular control is often a non-negotiable requirement.

### Biome's Curated, Opinionated Set

Biome takes a different philosophy. Instead of offering 800+ rules, it ships with a curated set of about **200 rules** in its current stable release. These rules are heavily weighted toward catching actual bugs and enforcing stylistic consistency. The team has explicitly stated they prioritize high-signal rules over noise.

For example, Biome includes excellent coverage for:
- **No-unused-variables**: Catches dead code effectively.
- **No-explicit-any**: Enforces TypeScript clarity.
- **Correctness checks**: Like detecting invalid regex or unreachable code.

However, Biome lacks the deep type-aware analysis that `typescript-eslint` provides. ESLint can use the TypeScript compiler API to analyze types across files, catching issues like using a property that doesn't exist on a union type or passing the wrong type to a function. Biome currently performs syntactic and semantic analysis but does not do full type-checking. This is the single biggest functional gap.

## Configuration and DX: The Learning Curve

### ESLint's Flexibility (and Complexity)

ESLint's configuration is famously flexible and famously frustrating. The shift from `.eslintrc` (JSON/YAML) to the newer flat config (`eslint.config.js`) in ESLint v9 was a necessary modernization, but it introduced a steep learning curve. A typical config for a React+TypeScript project can be 50-100 lines long, requiring imports of multiple plugins and careful ordering of overrides.

This complexity is a double-edged sword. It allows for incredibly fine-tuned control, but it also leads to configuration drift across teams. A common scenario: a developer adds a new rule to the config, and a month later, a different developer removes it because it conflicts with their local setup.

### Biome's Zero-Config Start

Biome's configuration is a model of simplicity. A basic `biome.json` file can be just a few lines:

```json
{
  "formatter": {
    "enabled": true
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true
    }
  }
}
```

That's it. You get a sensible default set of rules and formatting out of the box. For teams tired of debugging ESLint's config resolution, this is a breath of fresh air. Biome also ships with a `biome migrate` command that can automatically convert your existing ESLint config to Biome's format, though this works best for projects with simple configs.

## The Migration Path: Is It Worth It?

### When to Stick with ESLint

You should stay with ESLint if:
- You rely heavily on **type-aware linting** for TypeScript.
- You use niche plugins (e.g., `eslint-plugin-tailwindcss` or `eslint-plugin-import` for path aliases).
- You have a large monorepo with deeply nested, customized configs.
- Your team has existing, working ESLint configurations that nobody wants to touch.

The migration cost for complex setups is high. You would need to audit every custom rule, find Biome equivalents, and potentially lose some checks entirely.

### When to Switch to Biome

You should consider Biome if:
- You are starting a **new project** and have no legacy config.
- Your team is frustrated with ESLint's speed in CI.
- You want to consolidate your formatter and linter into one tool.
- Your codebase relies mostly on standard rules (no-unused-vars, no-debugger, etc.) rather than deep type analysis.

Biome's formatter is also a major draw. It is nearly identical to Prettier in output, meaning you can replace two dependencies with one.

## The Verdict: A Tale of Two Use Cases

The data is clear: Biome is dramatically faster and offers a superior developer experience for standard projects. ESLint remains the more powerful tool for complex, type-heavy codebases.

The future, however, points toward Biome. The team is actively working on adding type-aware rules, and the Rust ecosystem is investing heavily in JavaScript parsing (via tools like Oxc). Within 12-18 months, the performance gap may be accompanied by a feature parity that makes ESLint obsolete for most teams.

**The takeaway:** If you are starting a new project or managing a mid-sized codebase that values speed, switch to Biome today. If you are maintaining a sprawling enterprise application with deep TypeScript magic, hold steady with ESLint—but keep an eye on Biome's roadmap. The JavaScript tooling war is not over, but the momentum has definitively shifted.