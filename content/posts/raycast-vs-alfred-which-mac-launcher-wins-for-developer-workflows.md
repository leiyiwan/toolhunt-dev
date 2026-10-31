---
title: "Raycast vs Alfred: Which Mac Launcher Wins for Developer Workflows?"
date: 2026-10-31T10:05:32+08:00
draft: false
tags:

---

# Raycast vs Alfred: Which Mac Launcher Wins for Developer Workflows?

Open Activity Monitor on a typical developer's Mac and you'll find a dozen helper apps running. Yet the one most likely to be pressed into service dozens of times an hour is a keyboard launcher. For years, Alfred was the default answer. Then Raycast arrived with a modern interface, a built-in extension store, and an aggressive free tier, and the question became genuinely interesting.

This comparison focuses on developer workflows specifically: clipboard history, snippet expansion, window management, script execution, and how far each tool's free version gets you. Both apps are mature and actively maintained, so the choice comes down to how you work rather than which one is "better" in the abstract.

## The Contenders at a Glance

Alfred has been around since 2010 and is developed by a small UK team. It's a native macOS app with a loyal following built on its Powerpack model: the core launcher is free forever, but workflows, clipboard history, snippets, and themes require a paid license. As of this writing, a single-user Powerpack license runs about £34 (roughly $45), with a lifetime option available.

Raycast launched in 2020 and has grown quickly, partly because its free tier includes features Alfred charges for—clipboard history and snippets among them. The Pro tier is subscription-based (around $8/month or $96/year at list price), with a team plan above that. Raycast's extension ecosystem is built on React and TypeScript, which matters a great deal if you already write JavaScript for a living.

Both apps live behind a hotkey, index your files and applications, and support fuzzy search. The divergence starts the moment you go beyond launching apps.

## Extension and Workflow Architecture

This is the most consequential difference for developers.

**Alfred** uses "workflows," visual node graphs you build in a drag-and-drop editor. You connect triggers (hotkeys, keywords, file actions) to actions (run a script, open a URL, manipulate the clipboard) and optionally to outputs. Under the hood, workflows are folders containing a plist and whatever scripts or binaries you include. You can write those scripts in bash, Python, Ruby, PHP, or anything else installed on your machine. The community repository, Packal, hosts thousands of workflows, though quality and maintenance vary widely.

**Raycast** uses extensions written in TypeScript against a React-based API. You scaffold one with a CLI, develop with hot reload, and publish to a store that Raycast reviews. The store model means discovery and installation are one click, and extensions tend to stay current because the API is versioned and the review process catches breakage.

Which is better depends on your temperament. If you want to wire up a five-line shell script to a hotkey in two minutes, Alfred's visual editor is faster and requires no toolchain. If you want to build a proper UI with lists, detail panes, and form inputs—or publish something other people will use—Raycast's framework is dramatically more capable. Writing a polished Alfred workflow with a custom UI means building it in a separate language and wiring it in; writing the equivalent in Raycast is a few dozen lines of TSX.

One practical note: Alfred workflows can run arbitrary local scripts with full access to your environment, which is powerful and also means you should read what you install. Raycast extensions run in a sandboxed Node environment with declared permissions, which is a meaningfully tighter security posture.

## Clipboard History, Snippets, and the Small Stuff

Daily-driver features are where the free-tier gap shows.

Raycast includes clipboard history and snippet expansion at no cost. Clipboard history supports pinning, search, and filtering by content type. Snippets support placeholders like `{clipboard}`, `{date}`, and `{cursor}`, and can be triggered by keywords or—on the paid tier—by typing the trigger text anywhere.

Alfred gates both behind the Powerpack. Once paid, Alfred's clipboard history is excellent: it can ignore specific apps, respect password manager exclusions, and merge copied text. Its text expansion is arguably the most flexible of the two, supporting dynamic placeholders and per-snippet hotkeys.

For window management, neither app is a dedicated tool, but both offer paths. Raycast has first-party window management commands (move, resize, snap to halves and thirds) in the free app, which is enough for most people to skip a separate utility. Alfred relies on workflows for this; several good ones exist, but you're assembling rather than using a built-in.

## Scripting and Automation Depth

Alfred's scripting story is broader in one specific sense: it doesn't care what language you use. Shell scripts, AppleScript, JXA, Python with third-party libraries, compiled binaries—all fair game. For developers with existing automation in bash or Python, porting to Alfred is often just pointing a workflow at a file.

Raycast's scripting is narrower but deeper. The TypeScript API exposes native macOS capabilities—AppleScript execution, shell commands, file system access, clipboard, and UI components—through typed interfaces. You get autocomplete, type checking, and a real debugging experience. For anyone comfortable in the JS ecosystem, this is a better development loop than editing a script inside a plist.

Raycast also ships a set of built-in commands developers reach for constantly: search GitHub, manage pull requests, look up npm packages, control Docker, query a database, or search documentation without leaving the keyboard. Many of these are first-party or officially maintained. Alfred can do the same things via workflows, but you're relying on community maintenance.

## Performance and Resource Use

Both are fast. On current Apple silicon hardware, invoking either launcher is effectively instantaneous, and neither shows meaningful CPU use at idle in normal testing. Alfred has a reputation for being extremely lightweight, which was more pronounced on older Intel machines. Raycast runs a Node-based extension runtime, so extensions that fetch data can take a beat longer to populate, but the core launcher itself stays responsive.

Memory footprint is modest for both. If you're on a constrained machine or run a very large number of extensions, Alfred's leaner architecture has an edge. For most developers on modern hardware, this won't be the deciding factor.

## Pricing, Privacy, and Lock-In

Alfred's model is simple: pay once (or for a major-version upgrade), own it. No account is required, and nothing leaves your machine unless a workflow does so explicitly.

Raycast's free tier is generous, but Pro features—cloud sync of settings and clipboard history, custom themes, AI commands, and unlimited clipboard history retention—require a subscription. Raycast requires an account for sync and store features. Its AI integration sends queries to a third-party model provider, which is worth knowing if you work under data-handling constraints.

Neither app locks your data in a proprietary format in a way that's hard to escape, but Alfred's local-first design appeals to developers who prefer not to have a vendor account in the loop.

## The Verdict

There's no universal winner, but the decision tree is fairly clean.

**Choose Raycast if** you write TypeScript or JavaScript, want a large and actively maintained extension store, value a polished free tier, and like built-in developer commands for GitHub, Docker, and package lookups. It's also the easier recommendation for someone setting up a new Mac who doesn't want to pay before trying.

**Choose Alfred if** you want a one-time purchase, prefer scripting in whatever language you already know, need maximum control over workflow internals, or work in an environment where a local-only tool with no account requirement matters.

A reasonable middle path: many developers run Raycast as their daily launcher and keep Alfred installed for a handful of irreplaceable workflows. Nothing prevents it, and the overlap in hotkeys is manageable with a little configuration.

The takeaway: both tools are excellent, and the gap between them is smaller than forum debates suggest. Pick based on your scripting language, your tolerance for subscriptions, and whether you'd rather assemble workflows or install extensions. Then spend the saved time actually automating the repetitive parts of your day—which was the point all along.