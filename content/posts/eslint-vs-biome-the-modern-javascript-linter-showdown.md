---
title: "ESLint vs Biome: The Modern JavaScript Linter Showdown"
date: 2026-08-15T18:04:04+08:00
draft: false
tags:

---

# ESLint vs Biome: The Modern JavaScript Linter Showdown

In 2024, the JavaScript tooling landscape shifted dramatically. The release of Biome v1.0 in July 2024 marked a turning point, offering a Rust-based alternative that promised to replace both ESLint and Prettier with a single, unified tool. By early 2025, Biome had been downloaded over 5 million times per week on npm, while ESLint—the incumbent with over 300 million weekly downloads—was gearing up for its own long-awaited rewrite with ESLint v9's new flat config system.

For developers, this isn't just a battle of benchmarks. It's a fundamental question about how we approach code quality: Do we stick with the battle-tested, plugin-rich ecosystem we know, or do we bet on a faster, more integrated future?

## The Contenders: A Quick Overview

**ESLint** has been the de facto standard since its creation in 2013. It's a pluggable linting utility that has evolved through three major architectural phases, currently transitioning from the legacy `.eslintrc` configuration to the new flat config system. Its power lies in its ecosystem: over 7,000 plugins and rules available, covering everything from accessibility (eslint-plugin-jsx-a11y) to framework-specific patterns (eslint-plugin-react, eslint-plugin-vue).

**Biome** emerged from the ashes of Rome Tools, which was abandoned in 2023. The core team rewrote the project in Rust, focusing on three pillars: speed, simplicity, and integration. Biome isn't just a linter—it's a complete toolchain that also handles formatting, import sorting, and even has an experimental JavaScript compiler.

## Performance: The Benchmark Battle

The most compelling argument for Biome is speed. In independent benchmarks conducted by the Biome team and verified by community members, Biome consistently outperforms ESLint by 10x to 50x on large codebases.

Let's put this in perspective. On a typical codebase with 10,000 JavaScript files, ESLint takes approximately 30-40 seconds for a full lint pass on a modern MacBook Pro. Biome completes the same task in 1.5-2 seconds. For CI pipelines, this difference is transformative—imagine every pull request getting lint feedback in under five seconds instead of waiting a full minute.

But raw speed isn't everything. ESLint's performance has improved significantly with v9's flat config, which eliminates the costly config resolution cascade. The new config system has reduced cold-start times by roughly 40% compared to the legacy `.eslintrc` approach, though it still lags far behind Biome's performance.

## Configuration: Two Philosophies

### ESLint's Flex Config
ESLint's configuration has always been its strength and its weakness. The new flat config system (introduced as stable in v9) simplifies things considerably. A basic ESLint config looks like this:

```javascript
// eslint.config.js
import js from '@eslint/js';

export default [
  js.configs.recommended,
  {
    rules: {
      'no-unused-vars': 'error',
      'semi': ['error', 'always']
    }
  }
];
```

The flat config removes the `.eslintrc` hierarchy and `.eslintignore` file, consolidating everything into a single JavaScript file. It's a welcome improvement, but it still requires understanding modules, exports, and the plugin system.

### Biome's Zero-Config Approach
Biome takes a fundamentally different approach: it works out of the box with sensible defaults. A minimal `biome.json` can be as simple as:

```json
{
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true
    }
  }
}
```

That's it. Biome's recommended ruleset is curated and opinionated, covering common pitfalls and style issues. The configuration uses JSON or a JavaScript file, and the documentation is refreshingly concise—you can realistically set up Biome in under five minutes.

## Rules and Extensibility: The Ecosystem Question

This is where the debate gets heated. ESLint's plugin ecosystem is unmatched. Need a rule for your specific framework, coding standard, or internal convention? There's likely an ESLint plugin for it. With over 7,000 plugins, you can customize ESLint to enforce virtually any pattern imaginable.

Biome, by contrast, ships with around 200 built-in rules. While this covers the vast majority of common linting needs—unused variables, debugger statements, equality operators, and more—it lacks the long-tail extensibility. As of early 2025, Biome's plugin API is still in development, with no stable release date announced. This is the single biggest reason many teams hesitate to migrate.

However, Biome's approach has a philosophical advantage: fewer rules means less decision fatigue. ESLint's recommended config alone includes 74 rules, and teams often spend hours debating which additional rules to enable. Biome's curated set eliminates this overhead.

## Formatting: The Prettier Replacement

Biome's integrated formatter is another significant differentiator. It's designed to be a drop-in replacement for Prettier, with near-identical output for most code. The key advantage? You no longer need to run two separate tools.

A typical ESLint + Prettier setup requires:
- Installing both tools
- Configuring ESLint to disable rules that conflict with Prettier (using `eslint-config-prettier`)
- Setting up pre-commit hooks for both
- Managing two configuration files

Biome collapses all of this into a single tool. Run `biome check --write` and it lints, formats, and sorts imports in one pass. For teams tired of the "eslint --fix" followed by "prettier --write" dance, this is a massive quality-of-life improvement.

## Migration Considerations

If you're considering the switch, here's a practical migration checklist:

1. **Audit your current ESLint rules**: Run `eslint --print-config` and compare against Biome's rule list. Most common rules have direct equivalents.
2. **Test on a non-critical codebase**: Start with a smaller project to understand the differences.
3. **Use Biome's migration tool**: `biome migrate eslint` can automatically convert your ESLint config to Biome's format.
4. **Check your plugins**: If you rely on framework-specific plugins (React, Vue, etc.), verify whether Biome covers those patterns. As of early 2025, Biome handles React hooks rules but lacks some of the deeper framework integrations.
5. **Run both in parallel**: For a transition period, keep ESLint running in CI while adopting Biome locally. This gives you a safety net while you evaluate the differences.

## The Verdict: Which Should You Choose?

The answer depends on your context:

**Choose Biome if:**
- You're starting a new project or have a simple-to-moderate codebase
- Performance is critical (large monorepos, CI time constraints)
- You value simplicity and want to reduce tooling overhead
- You don't need exotic custom rules or framework-specific plugins

**Choose ESLint if:**
- You maintain a large legacy codebase with extensive custom rules
- You rely on framework-specific plugins (React, Vue, Angular)
- You need the flexibility to enforce highly specific coding standards
- Your team has invested heavily in ESLint configuration and expertise

## The Future Outlook

The JavaScript tooling landscape is moving toward integrated, performance-first solutions. Biome's team has ambitious plans for a plugin API, and the project's momentum is undeniable. Meanwhile, ESLint's maintainers are focused on stabilizing the flat config system and improving performance incrementally.

The most likely outcome? A hybrid future. Biome will continue to gain traction for its speed and simplicity, while ESLint remains essential for complex, plugin-heavy workflows. Some teams might even adopt both—using Biome for fast local development and CI checks, while keeping ESLint for deeper, project-specific analysis.

One thing is certain: the competition is healthy. It's pushing both tools to improve, and as developers, we're the beneficiaries.

---

**The bottom line:** If you value speed and simplicity above all else, give Biome a serious look—it's not just a linter, it's a complete toolchain that will save you time every single day. But if your project depends on the deep customization that only ESLint's plugin ecosystem can provide, stick with the incumbent. And regardless of your choice, keep an eye on this space—the next year will bring even more exciting developments.