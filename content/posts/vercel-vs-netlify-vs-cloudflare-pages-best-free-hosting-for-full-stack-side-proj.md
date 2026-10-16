---
title: "Vercel vs Netlify vs Cloudflare Pages: Best Free Hosting for Full-Stack Side Projects"
date: 2026-10-16T18:01:25+08:00
draft: false
tags:

---

# Vercel vs Netlify vs Cloudflare Pages: Best Free Hosting for Full-Stack Side Projects

You've built the side project. The last thing you want is a surprise bill for a hobby app that gets 200 visitors a month. Free tiers on Vercel, Netlify, and Cloudflare Pages all let you deploy a full-stack app at zero cost — but they draw the line in very different places. One caps bandwidth at 100 GB per month, another meters serverless function invocations, and a third charges for requests once you cross a threshold that most side projects never hit.

Here's how the three compare on the limits that actually matter when you're shipping something with a database, an API layer, and a frontend.

## The short version

- **Vercel** has the best developer experience for Next.js and the most generous function runtime on the free tier, but bandwidth and edge request limits are the tightest of the three.
- **Netlify** is the most framework-agnostic, with solid build tooling and a straightforward free tier, though its function limits are modest.
- **Cloudflare Pages** is the cheapest at scale by a wide margin — unmetered bandwidth and a very large daily request allowance — but the developer experience is rougher and the platform is more opinionated about how you structure things.

## What "free" actually includes

All three platforms give you a global CDN, automatic HTTPS, Git-based deploys, and preview deployments. The differences show up in the fine print.

### Bandwidth

This is where Cloudflare Pages wins decisively. Cloudflare does not meter bandwidth on Pages at all, and its fair-use policy is generous enough that most side projects will never notice. Vercel's Hobby plan includes 100 GB of fast data transfer per month; Netlify's free tier includes 100 GB of bandwidth. For a text-heavy site, 100 GB is plenty. For a project serving images, video, or large JavaScript bundles to any real audience, it's tighter than it sounds — a single 2 MB hero image served 50,000 times is already 100 GB.

### Serverless functions

Vercel's Hobby plan includes 1 million function invocations per month with up to 100 GB-hours of execution. Netlify's free tier gives you 125,000 function invocations per month and 100 hours of runtime. Cloudflare Workers, which powers Pages Functions, allows 100,000 requests per day on the free plan — roughly 3 million per month.

For a side project, all three are workable. Vercel's monthly invocation count is the most forgiving if you have spiky traffic; Cloudflare's daily cap is the most forgiving if you have steady traffic.

### Build minutes

Netlify includes 300 build minutes per month. Vercel's Hobby plan includes 6,000 build minutes. Cloudflare Pages gives you 500 builds per month with no explicit minute cap, though builds are capped at 20 minutes each. If you're rebuilding a large site on every push, Netlify's 300 minutes can disappear faster than you'd expect.

### Storage and databases

This is the part most comparisons skip, and it's the one that usually forces an upgrade. None of the three gives you a production-grade database on the free tier.

- **Vercel** offers Vercel Postgres and KV, but the free allowances are small and designed for prototyping. Most people pair Vercel with an external provider like Neon, Supabase, or Turso.
- **Netlify** has Netlify Blobs and a small database offering, but again, serious projects bring their own.
- **Cloudflare** has D1 (SQLite), KV, R2 (object storage), and Durable Objects. The free allowances are genuinely usable: D1 gives you 5 GB of storage and 5 million rows read per day, and R2 gives you 10 GB of storage with no egress fees.

If your side project needs a database and object storage without adding a second vendor, Cloudflare's bundle is the strongest.

## Developer experience

This is where Vercel pulls ahead, and it's not close for Next.js users.

Vercel built Next.js, and the integration shows. App Router features, server actions, incremental static regeneration, image optimization, and edge middleware all work on the free tier with essentially no configuration. Deploy a Next.js repo and it just runs. The dashboard is clean, the build logs are readable, and preview deployments work the way you'd hope.

Netlify's experience is nearly as smooth and works across more frameworks — Astro, SvelteKit, Remix, Nuxt, and plain static sites all deploy without friction. Its build plugins and redirect rules are mature. If you're not on Next.js, Netlify and Vercel are roughly comparable, with Netlify slightly ahead on framework neutrality.

Cloudflare Pages has improved a lot but still feels like a platform built by infrastructure engineers. The `wrangler` CLI is powerful but has a learning curve, local development for Workers requires more setup, and the dashboard is denser. If you're comfortable with the Cloudflare ecosystem, this is fine. If you want to push to Git and forget about it, Vercel and Netlify are easier.

One practical note: Cloudflare Pages and Workers have converged, and Cloudflare now steers new projects toward Workers with static assets. That's a reasonable direction, but it means documentation and tutorials are in flux, which adds friction.

## Cold starts and performance

Vercel's functions run on AWS Lambda under the hood and have cold starts in the 200–500 ms range for Node.js runtimes, less for edge functions. Netlify's functions are similar. Cloudflare Workers run on V8 isolates rather than containers, so cold starts are typically in the low single-digit milliseconds.

For a side project, this rarely matters. For an API that a mobile app calls on every screen load, Cloudflare's startup time is a real advantage.

## Pricing cliffs to watch

The reason to care about free-tier limits is what happens when you cross them.

Vercel's Pro plan is $20 per user per month and includes 1 TB of bandwidth. Netlify's Pro plan starts at $19 per user per month. Cloudflare's Workers Paid plan is $5 per month and includes 10 million requests, with additional requests billed at $0.30 per million. Cloudflare's overage pricing is dramatically cheaper, and bandwidth remains unmetered.

If a side project suddenly gets traction — a Hacker News front page, a viral tweet — the difference matters. On Vercel or Netlify, a traffic spike can push you toward a paid plan quickly. On Cloudflare, the same spike is likely to stay within the free or $5 tier.

## Which should you pick?

**Choose Vercel if** you're building with Next.js, want the smoothest possible deploy experience, and expect modest traffic. It's the best default for a Next.js side project, full stop.

**Choose Netlify if** you're using a framework other than Next.js, want mature build tooling, or prefer a platform that doesn't push you toward one framework. It's the most neutral option.

**Choose Cloudflare Pages if** you expect real traffic, need cheap object storage or a database bundled in, or want the lowest possible cost ceiling. You'll trade some polish for economics that are hard to beat.

A reasonable hybrid: deploy the frontend on Vercel or Netlify for the developer experience, and use Cloudflare R2 or D1 for storage if bandwidth or database costs become a concern. The platforms aren't mutually exclusive, and mixing them is often cheaper than upgrading either one.

## The takeaway

For a weekend project with a handful of users, all three free tiers are more than enough, and you should pick based on the framework you're using. The decision gets more interesting once your project has real traffic, a database, or file storage — at which point Cloudflare's unmetered bandwidth and bundled storage make it the cheapest place to grow, while Vercel and Netlify remain the easiest places to start. Match the platform to your expected ceiling, not just your current usage, and you won't get surprised by a bill.