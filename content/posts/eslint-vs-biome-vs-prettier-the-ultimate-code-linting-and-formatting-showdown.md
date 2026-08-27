---
title: "ESLint vs. Biome vs. Prettier: The Ultimate Code Linting and Formatting Showdown"
date: 2026-08-27T14:04:31+08:00
draft: false
tags:

---

# ESLint vs. Biome vs. Prettier: The Ultimate Code Linting and Formatting Showdown

If you've written JavaScript in the last five years, you've almost certainly encountered the ritual: install ESLint, configure a dozen plugins, wrestle with conflicting Prettier rules, and then spend an afternoon updating `.eslintrc` after a dependency bump. According to the 2023 Stack Overflow Developer Survey, ESLint remains the most widely used JavaScript linting tool, with over 70% of professional developers reporting regular usage. But the ecosystem is shifting.

Enter Biome—a Rust-based toolchain that promises to replace both ESLint and Prettier with a single, blazing-fast binary. It's not just a theoretical challenger; Biome reports speed improvements of 10x to 100x over existing tools in their benchmarks. Meanwhile, Prettier has quietly become the default formatter for projects ranging from small startups to large enterprises, with over 50 million weekly downloads on npm.

So which tool should you adopt for your next project? The answer isn't as simple as "pick the fastest one." This article breaks down the practical differences in performance, configuration, ecosystem, and workflow integration to help you make an informed decision.

## The Contenders at a Glance

Before diving into the comparison, let's clarify what each tool does:

- **ESLint**: A pluggable linter for identifying and fixing problematic patterns in JavaScript and TypeScript. It focuses on code quality (bugs, anti-patterns) and style rules (though style enforcement is often delegated to Prettier).
- **Prettier**: An opinionated code formatter that enforces a consistent style by parsing your code and re-printing it with its own rules. It has no "configuration" beyond a few options like semicolons, quotes, and trailing commas.
- **Biome**: A modern toolkit written in Rust that combines linting and formatting in one binary. It aims to be a drop-in replacement for both ESLint and Prettier, with a focus on speed and minimal configuration.

The core question is whether you need a single tool or a combination. Let's examine the key dimensions.

## Performance: The Rust Advantage

Performance is where Biome makes its most dramatic claim. Because it's written in Rust and compiles to native code, it avoids the startup overhead of Node.js-based tools. In a typical project with 1,000 files, running ESLint can take 10-30 seconds on a cold start. Prettier is faster, but still incurs Node.js process startup time. Biome, by contrast, often completes the same task in under 200 milliseconds.

This isn't just about developer patience. In a continuous integration (CI) pipeline, linting and formatting checks can become a bottleneck. If your CI runs linting on every pull request, switching from ESLint to Biome can cut that step from 20 seconds to under 1 second. For large monorepos, the savings are even more pronounced.

However, it's worth noting that ESLint has improved with its flat config and the optional `--cache` flag. On subsequent runs, ESLint only checks changed files, which narrows the gap. But for clean-checkout CI environments, Biome's advantage remains significant.

## Configuration: The Battle of Complexity

If you've ever configured ESLint, you know the pain. The legacy `.eslintrc` format was a maze of extends, plugins, and parser options. The newer flat config (introduced in ESLint v9) simplifies this, but it still requires explicit setup for TypeScript support, React hooks, and other common needs.

Prettier, by contrast, is famously opinionated. You can change about 10 options, and the documentation explicitly advises against customizing too much. This is a feature: consistent output across all projects, no bikeshedding over semicolons.

Biome takes a middle path. Its configuration is a single `biome.json` file, and it comes with sensible defaults out of the box. You can enable rules, adjust formatting options, and even migrate your existing ESLint and Prettier configs using the `biome migrate` command. For new projects, the setup is nearly zero-config: install the binary, run `biome init`, and you're done.

The trade-off is flexibility. ESLint's plugin ecosystem is unmatched. Need a rule for a specific framework or internal convention? There's likely a plugin for it. Biome has a growing set of built-in rules (over 200 as of v1.8), but it doesn't yet support custom plugins. If your team has highly specific linting requirements, ESLint still wins.

## Ecosystem and Community

ESLint has been around since 2013, and its ecosystem reflects that maturity. The npm registry lists over 3,000 ESLint plugins and configs. TypeScript support is seamless via `@typescript-eslint`, and framework-specific configs exist for React, Vue, Angular, Svelte, and more. This breadth is a double-edged sword: with great power comes great complexity, and many teams end up with a config that's a patchwork of community rules.

Prettier's ecosystem is simpler by design. It integrates with virtually every editor and has plugins for non-JS languages like HTML, CSS, Markdown, and even GraphQL. If you're working in a polyglot codebase, Prettier is often the only formatter that covers all your files.

Biome is the new kid on the block. As of 2024, it supports JavaScript, TypeScript, JSX, and JSON, with CSS support in beta. It does not yet format HTML or Markdown. For teams working across multiple languages, this is a significant limitation. However, Biome's roadmap is aggressive, and the maintainers have stated that expanding language support is a priority.

## Workflow Integration: Editor, CI, and Pre-commit Hooks

The daily developer experience matters more than raw benchmarks. Here's how the tools compare in practice:

- **Editor Integration**: All three tools have excellent VS Code extensions. ESLint and Prettier have been around long enough that their extensions are battle-tested. Biome's extension is newer but works well, offering both format-on-save and lint-on-type. One advantage of Biome is that you need only one extension instead of two.
- **Pre-commit Hooks**: With `lint-staged` and `husky`, you can run ESLint and Prettier on staged files. Biome offers a similar setup, and because it's faster, the pre-commit hook feels nearly instant. There's also `biome check --staged`, which runs both linting and formatting in one command.
- **CI Integration**: ESLint and Prettier have established patterns for CI, often using `eslint --max-warnings=0` and `prettier --check`. Biome provides `biome ci`, which runs both checks and fails on any issues. The speed advantage makes Biome particularly attractive for large repos where CI time is a cost center.

## Migration Path: Easing the Transition

If you're considering switching from ESLint and Prettier to Biome, the migration story is surprisingly smooth. Biome's `migrate` command reads your existing ESLint and Prettier configs and generates a `biome.json` with equivalent settings. It won't cover every rule, but it handles the most common ones.

A pragmatic approach for existing projects is a phased migration: start by using Biome for formatting only (replacing Prettier), while keeping ESLint for linting. Once your team is comfortable, gradually enable Biome's lint rules and disable the corresponding ESLint rules. This reduces the risk of a big-bang migration and lets your team adapt to the new tool incrementally.

For greenfield projects, starting with Biome from day one is a no-brainer. The setup time is minutes, not hours, and you avoid the complexity of juggling two tools.

## The Verdict: Which Should You Choose?

There's no universal winner—it depends on your context. Here are the scenarios where each tool shines:

- **Choose ESLint if**: You have a large existing codebase with custom lint rules, rely on a specific plugin (e.g., `eslint-plugin-security` or `eslint-plugin-import`), or need deep integration with a framework-specific linting setup. ESLint's maturity and ecosystem are unmatched.
- **Choose Prettier if**: You're working in a polyglot repository (HTML, CSS, Markdown, etc.) and need consistent formatting across all file types. Prettier is also the safest choice for teams that want zero configuration debates.
- **Choose Biome if**: You're starting a new project, value speed in CI, or want to simplify your toolchain. The single-binary approach reduces setup friction, and the performance gains are tangible in daily workflows.

For many teams, a hybrid approach still makes sense: use Biome for formatting and basic linting, and keep ESLint for advanced rules that Biome doesn't cover yet. As Biome's rule set matures, this hybrid will become less necessary, but it's a pragmatic bridge today.

## Conclusion

The JavaScript tooling landscape is in a state of healthy disruption. Biome's arrival has forced a conversation about whether the ESLint-and-Prettier duo is still the best default. The answer is nuanced: if you value ecosystem depth and customizability, ESLint and Prettier remain excellent choices. If you value speed and simplicity, Biome is a compelling alternative that's only getting better.

The best approach is to experiment. Spin up a small project with Biome and compare the developer experience against your current setup. Measure the CI time, count the configuration lines, and ask your team which workflow feels more natural. The right tool is the one that your team will actually use consistently—because a linter that's too slow or too complex is a linter that gets ignored.