---
title: "ESLint 9 vs. Biome: Which Linter and Formatter Should You Adopt for Your Next Project?"
date: 2026-08-30T10:05:24+08:00
draft: false
tags:

---

# ESLint 9 vs. Biome: Which Linter and Formatter Should You Adopt for Your Next Project?

In the JavaScript ecosystem, few debates generate as much heat as tooling choices. For the better part of a decade, ESLint has been the undisputed standard for code linting, with Prettier handling formatting duties. But a new challenger has emerged from the Rust ecosystem—Biome—promising a 10x to 20x performance boost while combining linting and formatting into a single binary.

The numbers are hard to ignore. In benchmark tests published by the Biome team, the tool completes its analysis on a codebase of roughly 5,000 files in under 200 milliseconds. ESLint, running on Node.js, typically takes several seconds for the same workload. For developers working on large monorepos, that difference translates into hours saved per week.

But speed isn't everything. ESLint's maturity brings a plugin ecosystem of over 300 rulesets, deep framework integrations, and years of community knowledge. Biome, despite its impressive velocity, is still catching up in terms of extensibility. So which tool should you adopt for your next project? The answer depends on your team's priorities, your project's complexity, and your willingness to embrace a younger ecosystem.

## The Contenders at a Glance

### ESLint 9: The Veteran with Baggage

ESLint 9, released in April 2024, introduced a significant architectural shift with the new flat config system. This replaced the old `.eslintrc` format with a more predictable, JavaScript-based configuration approach. The change eliminated the confusing cascading configuration model that plagued earlier versions, making it easier to reason about which rules apply to which files.

ESLint's core strength remains its rule granularity. You can configure rules for specific file patterns, override settings for tests versus source code, and even disable rules inline with comments—a feature that, while sometimes abused, provides a pragmatic escape hatch for legacy code.

The plugin ecosystem is where ESLint truly shines. Need React-specific rules? `eslint-plugin-react` has you covered with over 200 rules. Working with TypeScript? `typescript-eslint` provides a parser and ruleset that catches type-related issues before they reach production. GraphQL, Vue, Svelte, Next.js—if a framework exists, there's likely an ESLint plugin for it.

However, this power comes at a cost. A typical ESLint setup involves installing multiple packages, managing peer dependencies, and occasionally debugging configuration conflicts. The tool's speed, while acceptable for small projects, becomes a bottleneck in large codebases. Additionally, ESLint 9's flat config, while cleaner, represented a breaking change that required the community to update documentation, plugins, and tutorials.

### Biome: The Speed Demon with Ambition

Biome, formerly known as Rome, is a JavaScript toolchain written in Rust. It combines a linter, formatter, and bundler into a single installable binary. No `node_modules` pollution, no plugin version conflicts, no configuration file parsing delays—just a single executable that runs in milliseconds.

The performance gains come from Rust's compiled nature and the tool's design philosophy of doing less but doing it faster. Biome's formatter, which aims to be a drop-in replacement for Prettier, produces output that is nearly identical to its JavaScript counterpart. The linter includes around 200 rules covering correctness, security, performance, and style—enough for most projects without requiring additional plugins.

Biome's configuration is refreshingly simple. A single `biome.json` file controls both linting and formatting. The tool also includes a built-in import sorter and a refactoring engine, features that require separate plugins in the ESLint ecosystem.

The trade-off is extensibility. Biome's plugin API is still in development. While the project has made significant progress since its 2023 rewrite, custom rules remain difficult to implement. For teams with bespoke linting requirements—say, enforcing a specific internal API pattern—this limitation can be a dealbreaker.

## Performance: The Headline Statistic

Let's dig into the performance numbers more carefully. In a test conducted by the Biome team using the TypeScript compiler's codebase (approximately 4,900 files), Biome linted and formatted the entire project in 0.2 seconds. ESLint, configured with a typical rule set, took 7.5 seconds for linting alone. Prettier added another 3 seconds for formatting.

These figures are impressive but should be taken with a grain of salt. Benchmark conditions rarely match real-world usage. In practice, ESLint's performance depends heavily on the number of rules enabled, the complexity of the codebase, and whether the tool is running in watch mode with caching enabled. ESLint's `--cache` flag can reduce subsequent runs to under a second for incremental changes.

Still, the difference is noticeable. In a large monorepo with continuous integration, linting time directly impacts developer velocity. A 10-second ESLint run across 100 packages becomes 100 seconds of cumulative wait time per developer per day. Multiply that by a team of 20, and you're losing over half an hour of collective time daily.

## Configuration and Developer Experience

### ESLint's Learning Curve

ESLint 9's flat config is a marked improvement over its predecessor, but it still requires a certain level of expertise. Here's a minimal example:

```javascript
// eslint.config.js
import js from "@eslint/js";
import react from "eslint-plugin-react";
import tseslint from "typescript-eslint";

export default tseslint.config(
  js.configs.recommended,
  tseslint.configs.recommended,
  {
    plugins: { react },
    rules: {
      "react/jsx-uses-react": "error",
      "@typescript-eslint/no-unused-vars": ["error", { argsIgnorePattern: "^_" }]
    }
  }
);
```

This setup requires installing `eslint`, `@eslint/js`, `typescript-eslint`, and `eslint-plugin-react` as separate dependencies. Each package may have its own peer dependencies. For a project with multiple frameworks—say, React for the frontend and Node.js for the backend—the configuration grows accordingly.

The benefit is granular control. You can enable rules conditionally, extend shared configs, and even create your own reusable presets. This flexibility is why enterprises with complex compliance requirements continue to choose ESLint.

### Biome's Simplicity

Biome's configuration is deliberately minimal. Here's the equivalent setup:

```json
// biome.json
{
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "suspicious": {
        "noExplicitAny": "off"
      }
    }
  }
}
```

That's it. One file, zero dependencies. The tool handles both formatting and linting, so there's no need to coordinate between ESLint and Prettier. Biome also supports `.editorconfig` files and can auto-detect formatting preferences from existing codebases.

For teams tired of configuration sprawl, Biome's approach is liberating. It follows the "convention over configuration" philosophy, providing sensible defaults that work out of the box. The trade-off is less customization. If you need a rule that isn't in Biome's catalog, you're out of luck until the plugin API matures.

## Ecosystem and Community Support

### ESLint's Moat

ESLint's plugin ecosystem is its most formidable advantage. The `typescript-eslint` project alone provides over 100 rules specifically for TypeScript. Framework-specific plugins offer rules that catch common mistakes—like missing `key` props in React lists or improper Vue template syntax.

This ecosystem extends beyond rule sets. Tools like `eslint-config-airbnb` (which bundles hundreds of style rules) and `eslint-plugin-import` (which validates import paths and ordering) are deeply integrated into many codebases. Migration off ESLint means re-evaluating all these dependencies.

Additionally, ESLint has a long history of documentation, Stack Overflow answers, and blog tutorials. When a developer encounters an ESLint error, a quick search almost always yields a solution. Biome, being newer, has a smaller knowledge base. The official documentation is solid, but community troubleshooting resources are still growing.

### Biome's Growing Footprint

Biome's ecosystem is small but focused. The tool includes:

- **Import sorting**: Organizes imports automatically based on configurable rules.
- **Refactoring**: Provides safe code transformations, like renaming variables or extracting functions.
- **Formatter**: Prettier-compatible output with minimal configuration.

The project's roadmap includes a bundler, a test runner, and a package manager. If these plans materialize, Biome could become a full JavaScript toolchain—eliminating the need for multiple configuration files and dependency trees.

For now, though, teams adopting Biome must accept a certain level of risk. The project is still in beta (version 1.x as of mid-2024), and breaking changes are possible. While the core linting and formatting features are stable, the plugin API is explicitly marked as experimental.

## Migration Considerations

If you're considering switching from ESLint to Biome, the migration path is straightforward for basic setups. Biome can parse, lint, and format most modern JavaScript and TypeScript code. The tool even includes a `biome migrate` command that attempts to convert your ESLint configuration.

However, there are edge cases. If your codebase relies on custom ESLint rules or plugins that have no Biome equivalent, migration requires a different approach. You might keep ESLint for specific files or gradually phase out custom rules in favor of Biome's built-in set.

Conversely, if you're starting a new project, the decision is easier. For a greenfield project with no legacy constraints, Biome offers a faster, simpler developer experience. The performance gains are immediate, and the single-tool approach reduces cognitive overhead.

## The Verdict: Matching the Tool to the Job

### Choose ESLint 9 if:

- **You're working in a large enterprise with established tooling.** The plugin ecosystem and community support make it easier to enforce company-wide standards.
- **You need custom rules or framework-specific linting.** ESLint's plugin API is mature and well-documented.
- **Your team values granular control over configuration.** ESLint's flat config, while more complex, allows for precise rule management.
- **You're migrating an existing codebase with ESLint rules.** The cost of rewriting linting logic outweighs the performance benefits.

### Choose Biome if:

- **You're starting a new project with no legacy constraints.** The simplicity of a single tool is a significant productivity boost.
- **Performance is a critical concern.** Large codebases, CI pipelines, and monorepos benefit from Biome's speed.
- **You prefer convention over configuration.** Biome's defaults are sane and require minimal setup.
- **Your linting needs are standard.** If you don't need custom rules, Biome's 200 built-in rules cover the essentials.

## The Future Landscape

The JavaScript tooling ecosystem is evolving rapidly. ESLint's maintainers are aware of the performance gap and have been exploring ways to improve speed, including a potential Rust-based rewrite. However, such a rewrite would be a massive undertaking, and the existing plugin ecosystem would need to be reworked.

Biome, meanwhile, continues to gain momentum. The project's GitHub repository has seen steady contributions, and its adoption in the open-source community is growing. Tools like `create-next-app` and certain CI templates now offer Biome as an optional linter.

The most likely outcome is a coexistence. ESLint will remain the default for complex, plugin-heavy projects, while Biome will capture the segment of developers who prioritize speed and simplicity. For teams evaluating both, the decision ultimately comes down to what you value more: the flexibility of a mature ecosystem or the efficiency of a modern toolchain.

**The takeaway:** If you're starting fresh and your linting needs are straightforward, Biome offers a compelling, faster alternative that reduces toolchain complexity. If you're working within an established codebase or require custom linting rules, ESLint's maturity and plugin ecosystem remain unmatched. Evaluate your project's specific needs, run both tools on your codebase, and let the data—not the hype—guide your decision.