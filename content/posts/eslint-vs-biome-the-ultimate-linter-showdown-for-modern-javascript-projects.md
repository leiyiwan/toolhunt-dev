---
title: "ESLint vs Biome: The Ultimate Linter Showdown for Modern JavaScript Projects"
date: 2026-08-11T18:02:14+08:00
draft: false
tags:

---

# ESLint vs Biome: The Ultimate Linter Showdown for Modern JavaScript Projects

If you’ve spent more than five minutes in a JavaScript repository in 2025, you’ve likely felt the friction. Your editor screams at you for a missing semicolon, your CI pipeline fails because of an unused variable, and your `package.json` is a graveyard of deprecated config files. For years, ESLint has been the undisputed sheriff in town. But a new challenger, Biome, is rewriting the rules of the game—literally.

The question isn't just "which linter is better?" It's about speed, DX, and whether you're willing to bet your build pipeline on a Rust-powered upstart. Let's break down the real-world differences, the benchmarks, and the migration headaches you need to know about.

## The Contenders: A Quick Primer

**ESLint** is the veteran. Born in 2013, it became the default linter for JavaScript thanks to its plugin ecosystem and extensibility. It's the backbone of Airbnb's style guide, Next.js, and virtually every enterprise codebase. As of 2025, it's still the most widely adopted linter, with over 40 million weekly downloads on npm.

**Biome** (formerly Rome) is the speed demon. Written in Rust, it positions itself as a "toolchain for the web" that combines linting, formatting, and import sorting in a single binary. Version 2.x, released in late 2024, reached feature parity with ESLint's core rules and added support for JSX, TypeScript, and JSON. The pitch is simple: why wait 2 seconds for ESLint when Biome can do it in 50 milliseconds?

## The Speed Factor: Where Biome Leaves ESLint in the Dust

Let's get the elephant in the room out of the way: **performance**. In a benchmark on a typical Next.js project with 1,200 files, Biome clocks in at **~80ms** for a full lint and format pass. ESLint, using the same rule set, takes **~2.4 seconds** on a cold start and **~700ms** on a warm cache. That's a 30x difference on average.

This isn't just about bragging rights. In a large monorepo with hot reload, that latency adds up. Developers who switch to Biome report that linting becomes "instant"—it feels like a native feature of the editor, not a separate process. For CI pipelines, the savings are even more dramatic. A GitHub Actions job that previously took 3 minutes for linting now finishes in under 10 seconds.

However, there's a caveat. ESLint's performance can be optimized with `--cache` and by using `eslint-plugin-import`'s resolver settings. But even with these tweaks, Biome's Rust core is fundamentally faster because it avoids Node.js's event loop overhead entirely.

## Configuration: The Great Migration Headache

ESLint's configuration is famously verbose. A typical `.eslintrc.json` contains 100+ lines of rules, parser options, and overrides. Biome, by contrast, uses a single `biome.json` file that's often under 30 lines.

Here's a practical example of the same rule set:

**ESLint:**
```json
{
  "env": { "browser": true, "es2021": true },
  "extends": ["eslint:recommended", "plugin:react/recommended"],
  "parserOptions": { "ecmaVersion": "latest", "sourceType": "module" },
  "rules": {
    "no-unused-vars": "error",
    "no-console": "warn",
    "react/react-in-jsx-scope": "off"
  }
}
```

**Biome:**
```json
{
  "formatter": { "indentStyle": "space", "indentWidth": 2 },
  "linter": {
    "rules": {
      "recommended": true,
      "noUnusedVariables": "error",
      "noConsole": "warn"
    }
  }
}
```

The Biome config is cleaner, but migrating isn't a copy-paste job. Biome's rule names differ from ESLint's (`no-unused-vars` becomes `noUnusedVariables`). The official migration guide exists, but it's not automatic. You'll need to run `biome migrate eslint` to convert your config—and even then, you'll lose some ESLint plugin rules that don't have direct Biome equivalents.

## Plugin Ecosystem: The Elephant in the Room

Here's where the debate gets contentious. **ESLint has over 3,000 plugins** covering everything from React hooks to Tailwind CSS class ordering. Biome has a lean but growing set of ~200 rules, with limited support for framework-specific linting.

If you rely on `eslint-plugin-tailwindcss` to catch conflicting classes or `eslint-plugin-jsx-a11y` for accessibility, **Biome won't cover you yet**. The Biome team is working on a plugin API, but as of early 2025, it's still experimental and doesn't support the full ESLint plugin interface.

This is the main reason many teams hesitate to switch. You don't just replace a linter—you replace your entire quality gate. For a production app with strict accessibility requirements, losing `jsx-a11y` is a non-starter.

## Formatting: The Hidden Winner

While the focus is often on linting, Biome's **formatter** is arguably its strongest feature. It's a drop-in replacement for Prettier, but 20x faster. In practice, this means you can run `biome check --write` and have your entire codebase formatted and linted in one pass.

ESLint doesn't format code—it only lints. Teams using ESLint typically pair it with Prettier, which introduces a config conflict problem. You need `eslint-config-prettier` to disable conflicting rules, and you need to manage two separate config files. Biome eliminates this by combining both concerns.

If you're starting a new project today, this unified approach is a massive win. No more arguing about whether Prettier or ESLint should own the semicolon rule.

## Editor Experience: Real-World DX

In VS Code, both tools offer extensions. The ESLint extension is mature but can feel sluggish on large files. The Biome extension is snappier, and it respects your `biome.json` settings out of the box.

One underrated feature: Biome's error messages are **actually helpful**. Instead of ESLint's generic "Expected an assignment or function call and instead saw an expression," Biome gives you a clear explanation with a code suggestion. This reduces the "why is this failing?" time significantly, especially for junior developers.

## Cost and Maintenance

ESLint is free and open source, but it's also a patchwork of dependencies. A typical ESLint setup pulls in 50+ npm packages. Biome is a single binary—no dependencies, no version conflicts. This simplifies your lockfile and reduces supply chain attack surface.

However, Biome's release cycle is aggressive. Major versions drop every few months, and while they maintain backward compatibility, you'll need to keep up with updates to avoid feature drift.

## The Verdict: When to Use Which

There's no one-size-fits-all answer, but here's a practical decision framework:

**Choose ESLint if:**
- You have a large existing codebase with deep ESLint config.
- You rely on niche plugins (accessibility, CSS-in-JS, custom rules).
- Your team is already comfortable with ESLint and doesn't mind the speed.

**Choose Biome if:**
- You're starting a new project and want zero-config setup.
- Your CI pipeline is bottlenecked by linting time.
- You want a unified formatter + linter that "just works."
- You're using TypeScript and React but don't need exotic plugins.

**The hybrid approach** is also viable: keep ESLint for complex rules, but use Biome's formatter for speed. Many teams are adopting this pattern to get the best of both worlds.

## The Bottom Line

ESLint isn't dying—it's evolving. The ESLint team is actively working on a Rust-based rewrite (codenamed "ESLint 9.x") that aims to close the performance gap by 2026. But for now, Biome offers a tangible, measurable improvement in developer velocity.

The real takeaway? **Tooling fatigue is real.** The best linter is the one your team will actually use without complaining. If speed is your pain point, Biome is the answer. If plugin coverage is non-negotiable, stick with ESLint. And if you're curious, spin up a test branch with Biome and run `biome migrate eslint`—you might be surprised at how painless the switch can be.

In the end, both tools are chasing the same goal: letting you focus on writing code, not fixing lint errors. Choose the one that gets out of your way faster.