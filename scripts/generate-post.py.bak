#!/usr/bin/env python3
"""
ToolHunt - AI Tool Review Content Generator
Generates AI tool review/comparison articles using DeepSeek API.
Based on 1号工厂 (techcompare.dev) verified pipeline.

Usage:
    export DEEPSEEK_API_KEY='sk-your-key-here'
    python3 scripts/generate-post.py
"""

import os
import sys
import json
import random
import subprocess
import urllib.request
import urllib.error
from datetime import date

# ---- Configuration ----
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(PROJECT_ROOT, "content", "posts")
USED_TOPICS_FILE = os.path.join(PROJECT_ROOT, "scripts", "used_topics.json")

API_URL = "https://api.deepseek.com/v1/chat/completions"
MODEL = "deepseek-v4-flash"
MAX_TOKENS = 3500
RETRY_COUNT = 2
TEMPERATURE = 0.5

TOPIC_POOL = [
    # AI Writing Tools
    ("Jasper AI vs Copy.ai: Which AI Writing Tool is Better?", "ai-writing",
     ["jasper", "copy-ai", "writing", "content", "comparison"],
     "Jasper AI vs Copy.ai comparison: features, pricing, output quality for AI content writing"),
    ("ChatGPT vs Claude for Content Creation", "ai-writing",
     ["chatgpt", "claude", "writing", "ai-assistant", "comparison"],
     "ChatGPT vs Claude comparison for writing: which AI assistant produces better content"),
    ("Writesonic vs Rytr: Budget AI Writing Tools Compared", "ai-writing",
     ["writesonic", "rytr", "budget", "writing", "comparison"],
     "Budget AI writing tool comparison: Writesonic vs Rytr features and pricing"),
    ("Notion AI vs Grammarly: Writing Assistant Showdown", "ai-writing",
     ["notion", "grammarly", "writing", "productivity", "comparison"],
     "Notion AI vs Grammarly comparison for writing and editing workflows"),
    # AI Image Generation
    ("Midjourney vs DALL-E 3: AI Image Generator Comparison", "ai-image",
     ["midjourney", "dall-e", "image-generation", "ai-art", "comparison"],
     "Midjourney vs DALL-E 3: comparing AI image quality, ease of use, and pricing"),
    ("Stable Diffusion vs Leonardo AI for Professional Design", "ai-image",
     ["stable-diffusion", "leonardo", "image-generation", "design", "comparison"],
     "Stable Diffusion vs Leonardo AI comparison for professional AI art and design"),
    ("Adobe Firefly vs Canva AI: Design Tool AI Features Compared", "ai-image",
     ["adobe", "canva", "firefly", "design", "comparison"],
     "Adobe Firefly vs Canva AI: which design platform has better AI features"),
    # AI Coding Assistants
    ("GitHub Copilot vs Cursor: AI Coding Assistant Showdown", "ai-coding",
     ["github-copilot", "cursor", "coding", "developer", "comparison"],
     "GitHub Copilot vs Cursor comparison for AI-assisted software development"),
    ("Windsurf vs Cursor: Next-Gen AI Code Editors Compared", "ai-coding",
     ["windsurf", "cursor", "code-editor", "ai", "comparison"],
     "Windsurf vs Cursor: comparing the best AI-powered code editors"),
    ("Tabnine vs Codeium: AI Code Completion Tools Battle", "ai-coding",
     ["tabnine", "codeium", "code-completion", "developer", "comparison"],
     "Tabnine vs Codeium comparison for AI code autocompletion features"),
    # AI Video Tools
    ("Runway vs Pika Labs: AI Video Generation Compared", "ai-video",
     ["runway", "pika", "video-generation", "ai", "comparison"],
     "Runway vs Pika Labs comparison for AI video creation and editing"),
    ("HeyGen vs Synthesia: AI Avatar Video Tools Battle", "ai-video",
     ["heygen", "synthesia", "avatar", "video", "comparison"],
     "HeyGen vs Synthesia comparison for AI avatar video creation platforms"),
    # AI Voice & Audio
    ("ElevenLabs vs Play.ht: AI Voice Generation Compared", "ai-voice",
     ["elevenlabs", "playht", "voice", "text-to-speech", "comparison"],
     "ElevenLabs vs Play.ht comparison for realistic AI voice generation"),
    ("Murf AI vs Lovo AI: Text-to-Speech for Content Creators", "ai-voice",
     ["murf", "lovo", "text-to-speech", "creator", "comparison"],
     "Murf AI vs Lovo AI comparison for content creator text-to-speech needs"),
    # AI Productivity Tools
    ("Notion AI vs Mem: AI Note-Taking Apps Compared", "ai-productivity",
     ["notion", "mem", "notes", "productivity", "comparison"],
     "Notion AI vs Mem comparison for AI-powered note-taking and knowledge management"),
    ("Otter.ai vs Fireflies.ai: AI Meeting Assistants Battle", "ai-productivity",
     ["otter", "fireflies", "meeting", "transcription", "comparison"],
     "Otter.ai vs Fireflies.ai comparison for AI meeting transcription and notes"),
    # SaaS Tools
    ("Monday.com vs Asana: Project Management Tools Compared", "saas",
     ["monday", "asana", "project-management", "saas", "comparison"],
     "Monday.com vs Asana comparison for team project management in 2026"),
    ("Airtable vs Notion: Database vs All-in-One Workspace", "saas",
     ["airtable", "notion", "database", "workspace", "comparison"],
     "Airtable vs Notion comparison: which tool for your workflow"),
    ("Figma vs Sketch: Design Tool Battle in 2026", "saas",
     ["figma", "sketch", "design", "ui-ux", "comparison"],
     "Figma vs Sketch comparison for UI/UX design workflows and collaboration"),
    ("Webflow vs Framer: No-Code Website Builder Showdown", "saas",
     ["webflow", "framer", "no-code", "website", "comparison"],
     "Webflow vs Framer comparison for no-code website design and publishing"),
    # SEO & Marketing Tools
    ("Ahrefs vs Semrush: SEO Tool Comparison for 2026", "seo-tools",
     ["ahrefs", "semrush", "seo", "marketing", "comparison"],
     "Ahrefs vs Semrush comparison: which SEO tool delivers better results"),
    ("Mailchimp vs ConvertKit: Email Marketing Platform Battle", "email-marketing",
     ["mailchimp", "convertkit", "email", "marketing", "comparison"],
     "Mailchimp vs ConvertKit comparison for email marketing and automation"),
    ("Buffer vs Hootsuite: Social Media Management Compared", "social-media",
     ["buffer", "hootsuite", "social-media", "scheduling", "comparison"],
     "Buffer vs Hootsuite comparison for social media management and scheduling"),
    # AI Chatbots
    ("Chatbase vs Botpress: Custom AI Chatbot Platforms", "ai-chatbots",
     ["chatbase", "botpress", "chatbot", "customer-service", "comparison"],
     "Chatbase vs Botpress comparison for building custom AI chatbots"),
    ("Tidio vs Intercom: AI Customer Support Tools Battle", "ai-chatbots",
     ["tidio", "intercom", "customer-support", "chat", "comparison"],
     "Tidio vs Intercom comparison for AI-powered customer support platforms"),
    # AI Data & Analytics
    ("Tableau AI vs Power BI Copilot: AI Analytics Compared", "ai-analytics",
     ["tableau", "power-bi", "analytics", "business-intelligence", "comparison"],
     "Tableau AI vs Power BI Copilot comparison for AI business analytics"),
    ("Julius AI vs ChatGPT Advanced Data Analysis", "ai-analytics",
     ["julius", "chatgpt", "data-analysis", "ai", "comparison"],
     "Julius AI vs ChatGPT Advanced Data Analysis for data science workflows"),
    # AI Research Tools
    ("Perplexity AI vs Google Gemini: AI Research Assistants", "ai-research",
     ["perplexity", "gemini", "research", "search", "comparison"],
     "Perplexity AI vs Google Gemini comparison for AI-powered research"),
    ("Elicit vs Consensus: AI Academic Research Tools", "ai-research",
     ["elicit", "consensus", "academic", "research", "comparison"],
     "Elicit vs Consensus comparison for AI academic paper research"),
    # Automation Tools
    ("Zapier vs Make: No-Code Automation Platform Showdown", "automation",
     ["zapier", "make", "automation", "no-code", "comparison"],
     "Zapier vs Make comparison for no-code workflow automation in 2026"),
    # Design Tools
    ("Canva Pro vs Adobe Express: Design Tool for Non-Designers", "design",
     ["canva", "adobe", "express", "design", "comparison"],
     "Canva Pro vs Adobe Express comparison for easy graphic design"),
]


def load_used_topics():
    try:
        with open(USED_TOPICS_FILE, "r") as f:
            data = json.load(f)
            return set(data.get("used", []))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()


def save_used_topics(used):
    os.makedirs(os.path.dirname(USED_TOPICS_FILE), exist_ok=True)
    with open(USED_TOPICS_FILE, "w") as f:
        json.dump({"used": sorted(used)}, f, indent=2)


def get_available_topics():
    used = load_used_topics()
    available = [t for t in TOPIC_POOL if t[0] not in used]
    return available, used


def pick_topic():
    available, used = get_available_topics()
    if not available:
        print("⚠️  All topics used. Resetting tracking.")
        save_used_topics(set())
        available = list(TOPIC_POOL)
        used = set()
    random.shuffle(available)
    return available[0], used


def call_deepseek(prompt):
    api_key = os.environ["DEEPSEEK_API_KEY"]
    base_url = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com").rstrip("/")
    url = f"{base_url}/v1/chat/completions"

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": MAX_TOKENS,
        "temperature": TEMPERATURE,
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    last_error = None
    for attempt in range(1 + RETRY_COUNT):
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                result = json.loads(resp.read().decode("utf-8"))
            choices = result.get("choices", [])
            if not choices:
                raise RuntimeError(f"No choices in API response: {result}")
            content = choices[0].get("message", {}).get("content", "").strip()
            if not content:
                raise RuntimeError("Empty content in API response")
            return content
        except (urllib.error.HTTPError, urllib.error.URLError, OSError, json.JSONDecodeError, RuntimeError) as e:
            last_error = e
            print(f"  API call attempt {attempt + 1} failed: {e}", file=sys.stderr)
            if attempt < RETRY_COUNT:
                print("  Retrying...", file=sys.stderr)

    print(f"ERROR: All API attempts failed. Last error: {last_error}", file=sys.stderr)
    sys.exit(1)


def slugify(title):
    s = title.lower().strip()
    s = s.replace(" vs ", "-vs-")
    s = s.replace(": ", "-")
    s = s.replace(":", "")
    s = s.replace("'", "")
    s = s.replace("/", "-")
    result = []
    for ch in s:
        if ch.isalnum() or ch == "-":
            result.append(ch)
        else:
            result.append("-")
    s = "".join(result)
    while "--" in s:
        s = s.replace("--", "-")
    return s.strip("-")[:60]


def build_prompt(title_text, category, tags, description_text, today):
    tags_str = ", ".join(tags)

    return f"""You are a professional software reviewer writing for an AI tool review website. Write a comprehensive, factual comparison article.

Title: {title_text}
Category: {category}
Tags: {tags_str}

## Writing Guidelines

### Format
- Write 1000-1600 words in English
- Use proper markdown with ## headings
- Start immediately with value — no fluff introductions

### SEO Requirements
- Naturally include these keywords throughout: {description_text}
- Use the primary keyword phrase in the first paragraph
- Write a compelling meta description (under 160 chars)

### Structure Requirements
1. **Quick Verdict** (2-3 sentences)
2. **Comparison Table**: Pricing, key features, best for, ratings (10+ rows)
3. **Features Deep Dive** section
4. **User Experience & Ease of Use** section
5. **Pricing & Value** analysis
6. **Pros & Cons** for each tool
7. **Final Recommendation** — which to choose and when
8. **FAQ**: 4-6 Q&A pairs

### Anti-AI Guidelines (IMPORTANT)
- NEVER use: "as an AI", "as a language model", "I hope this helps", "feel free to", "in today's digital age", "let's dive in", "whether you're a..."
- Write in a direct, journalistic tone — like a tech magazine
- Use concrete numbers, specific feature names, and real-world scenarios
- Include current pricing estimates
- Use contractions (it's, don't, can't, won't)
- Vary sentence structure

### YAML Frontmatter
Include proper YAML frontmatter with:
- title: "{title_text}"
- date: {today}
- draft: false
- tags: [{', '.join(f'"{t}"' for t in tags)}]
- categories: ["{category}"]
- description: "{description_text}"
- summary: "{description_text}"

Write the complete article now, delimited by --- for frontmatter."""


def call_deepseek_and_write(topic_entry, used_set):
    title_text, category, tags, description_text = topic_entry
    today = date.today()
    slug = slugify(title_text)
    filename = f"{slug}.md"
    filepath = os.path.join(POSTS_DIR, filename)

    print(f"\n{'='*60}")
    print(f"Generating: {title_text}")
    print(f"  Category: {category} | Slug: {slug}")
    print(f"{'='*60}")

    prompt = build_prompt(title_text, category, tags, description_text, today)
    article = call_deepseek(prompt)

    tags_yaml = ", ".join(f'"{t}"' for t in tags)
    if not article.startswith("---"):
        article = f"""---
title: "{title_text}"
date: {today}
draft: false
tags: [{tags_yaml}]
categories: ["{category}"]
description: "{description_text}"
summary: "{description_text}"
---

{article}"""

    os.makedirs(POSTS_DIR, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(article)
        f.write("\n")

    print(f"  ✓ Article saved ({len(article)} chars)")

    used_set.add(title_text)
    save_used_topics(used_set)
    print(f"  ✓ Topic marked ({len(used_set)}/{len(TOPIC_POOL)} used)")

    return filepath


def git_commit_and_push(filepath):
    print("\n--- Git operations ---")
    rel_path = os.path.relpath(filepath, PROJECT_ROOT)
    result = subprocess.run(
        ["git", "add", rel_path],
        cwd=PROJECT_ROOT,
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  ERROR: git add failed: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    print(f"  ✓ git add {rel_path}")

    title = os.path.basename(filepath).replace(".md", "").replace("-", " ").title()
    commit_msg = f"Add review: {title}"
    result = subprocess.run(
        ["git", "commit", "-m", commit_msg],
        cwd=PROJECT_ROOT,
        capture_output=True, text=True
    )
    if result.returncode != 0:
        if "nothing to commit" in result.stderr or "nothing to commit" in result.stdout:
            print("  - Nothing to commit")
            return
        print(f"  ERROR: git commit failed: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    print(f"  ✓ git commit: {commit_msg}")

    result = subprocess.run(
        ["git", "push", "origin", "main"],
        cwd=PROJECT_ROOT,
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  ERROR: git push failed: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    print(f"  ✓ git push to origin/main")
    print(f"\n  ✅ Published: {rel_path}")


def main():
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        print("ERROR: DEEPSEEK_API_KEY environment variable is required.", file=sys.stderr)
        sys.exit(1)

    print(f"ToolHunt Content Generator")
    print(f"Model: {MODEL} | Temp: {TEMPERATURE}")

    available, used = get_available_topics()
    print(f"\nTopics: {len(available)} remaining / {len(TOPIC_POOL)} total")

    topic, used_set = pick_topic()
    print(f"Selected: {topic[0]} [{topic[1]}]")

    filepath = call_deepseek_and_write(topic, used_set)
    git_commit_and_push(filepath)

    remaining = len(TOPIC_POOL) - len(used_set)
    print(f"\n{'='*60}")
    print(f"✅ DONE - {os.path.basename(filepath)}")
    print(f"📊 Progress: {len(used_set)}/{len(TOPIC_POOL)} ({remaining} remaining)")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
