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
    ("Midjourney vs DALL-E 3: AI Image Generator Comparison", "ai-image",
     ["midjourney", "dall-e", "image-generation", "ai-art", "comparison"],
     "Midjourney vs DALL-E 3: comparing AI image quality, ease of use, and pricing"),
    ("Stable Diffusion vs Leonardo AI for Professional Design", "ai-image",
     ["stable-diffusion", "leonardo", "image-generation", "design", "comparison"],
     "Stable Diffusion vs Leonardo AI comparison for professional AI art and design"),
    ("Adobe Firefly vs Canva AI: Design Tool AI Features Compared", "ai-image",
     ["adobe", "canva", "firefly", "design", "comparison"],
     "Adobe Firefly vs Canva AI: which design platform has better AI features"),
    ("GitHub Copilot vs Cursor: AI Coding Assistant Showdown", "ai-coding",
     ["github-copilot", "cursor", "coding", "developer", "comparison"],
     "GitHub Copilot vs Cursor comparison for AI-assisted software development"),
    ("Windsurf vs Cursor: Next-Gen AI Code Editors Compared", "ai-coding",
     ["windsurf", "cursor", "code-editor", "ai", "comparison"],
     "Windsurf vs Cursor: comparing the best AI-powered code editors"),
    ("Tabnine vs Codeium: AI Code Completion Tools Battle", "ai-coding",
     ["tabnine", "codeium", "code-completion", "developer", "comparison"],
     "Tabnine vs Codeium comparison for AI code autocompletion features"),
    ("Runway vs Pika Labs: AI Video Generation Compared", "ai-video",
     ["runway", "pika", "video-generation", "ai", "comparison"],
     "Runway vs Pika Labs comparison for AI video creation and editing"),
    ("HeyGen vs Synthesia: AI Avatar Video Tools Battle", "ai-video",
     ["heygen", "synthesia", "avatar", "video", "comparison"],
     "HeyGen vs Synthesia comparison for AI avatar video creation platforms"),
    ("ElevenLabs vs Play.ht: AI Voice Generation Compared", "ai-voice",
     ["elevenlabs", "playht", "voice", "text-to-speech", "comparison"],
     "ElevenLabs vs Play.ht comparison for realistic AI voice generation"),
    ("Murf AI vs Lovo AI: Text-to-Speech for Content Creators", "ai-voice",
     ["murf", "lovo", "text-to-speech", "creator", "comparison"],
     "Murf AI vs Lovo AI comparison for content creator text-to-speech needs"),
    ("Notion AI vs Mem: AI Note-Taking Apps Compared", "ai-productivity",
     ["notion", "mem", "notes", "productivity", "comparison"],
     "Notion AI vs Mem comparison for AI-powered note-taking and knowledge management"),
    ("Otter.ai vs Fireflies.ai: AI Meeting Assistants Battle", "ai-productivity",
     ["otter", "fireflies", "meeting", "transcription", "comparison"],
     "Otter.ai vs Fireflies.ai comparison for AI meeting transcription and notes"),
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
    ("Ahrefs vs Semrush: SEO Tool Comparison for 2026", "seo-tools",
     ["ahrefs", "semrush", "seo", "marketing", "comparison"],
     "Ahrefs vs Semrush comparison: which SEO tool delivers better results"),
    ("Mailchimp vs ConvertKit: Email Marketing Platform Battle", "email-marketing",
     ["mailchimp", "convertkit", "email", "marketing", "comparison"],
     "Mailchimp vs ConvertKit comparison for email marketing and automation"),
    ("Buffer vs Hootsuite: Social Media Management Compared", "social-media",
     ["buffer", "hootsuite", "social-media", "scheduling", "comparison"],
     "Buffer vs Hootsuite comparison for social media management and scheduling"),
    ("Chatbase vs Botpress: Custom AI Chatbot Platforms", "ai-chatbots",
     ["chatbase", "botpress", "chatbot", "customer-service", "comparison"],
     "Chatbase vs Botpress comparison for building custom AI chatbots"),
    ("Tidio vs Intercom: AI Customer Support Tools Battle", "ai-chatbots",
     ["tidio", "intercom", "customer-support", "chat", "comparison"],
     "Tidio vs Intercom comparison for AI-powered customer support platforms"),
    ("Tableau AI vs Power BI Copilot: AI Analytics Compared", "ai-analytics",
     ["tableau", "power-bi", "analytics", "business-intelligence", "comparison"],
     "Tableau AI vs Power BI Copilot comparison for AI business analytics"),
    ("Julius AI vs ChatGPT Advanced Data Analysis", "ai-analytics",
     ["julius", "chatgpt", "data-analysis", "ai", "comparison"],
     "Julius AI vs ChatGPT Advanced Data Analysis for data science workflows"),
    ("Perplexity AI vs Google Gemini: AI Research Assistants", "ai-research",
     ["perplexity", "gemini", "research", "search", "comparison"],
     "Perplexity AI vs Google Gemini comparison for AI-powered research"),
    ("Elicit vs Consensus: AI Academic Research Tools", "ai-research",
     ["elicit", "consensus", "academic", "research", "comparison"],
     "Elicit vs Consensus comparison for AI academic paper research"),
    ("Zapier vs Make: No-Code Automation Platform Showdown", "automation",
     ["zapier", "make", "automation", "no-code", "comparison"],
     "Zapier vs Make comparison for no-code workflow automation in 2026"),
    ("Canva Pro vs Adobe Express: Design Tool for Non-Designers", "design",
     ["canva", "adobe", "express", "design", "comparison"],
     "Canva Pro vs Adobe Express comparison for easy graphic design"),
    ("Tableau AI vs ThoughtSpot: AI Analytics for Business Intelligence", "ai-analytics",
     ["tableau", "thoughtspot", "ai-analytics", "business-intelligence", "data-visualization"],
     "Compare Tableau AI and ThoughtSpot for AI-powered business intelligence, data visualization, and natural language query capabilities."),
    ("Polymer vs Akkio: No-Code AI Analytics Platforms Compared", "ai-analytics",
     ["polymer", "akkio", "no-code-ai", "analytics", "data-science"],
     "Explore the differences between Polymer and Akkio for no-code AI analytics, predictive modeling, and automated data insights."),
    ("Julius AI vs Obviously AI: AI Data Analysis Tools Battle", "ai-analytics",
     ["julius-ai", "obviously-ai", "data-analysis", "ai-tools", "machine-learning"],
     "Compare Julius AI and Obviously AI for AI-driven data analysis, machine learning automation, and spreadsheet integration."),
    ("Power BI Copilot vs Polymer: AI Analytics for Non-Technical Users", "ai-analytics",
     ["power-bi", "polymer", "ai-analytics", "business-intelligence", "data-insights"],
     "See how Power BI Copilot and Polymer stack up for AI analytics tailored to non-technical users and business teams."),
    ("ThoughtSpot vs Akkio: AI Analytics for Real-Time Decision Making", "ai-analytics",
     ["thoughtspot", "akkio", "real-time-analytics", "ai-decision-making", "data-science"],
     "Compare ThoughtSpot and Akkio for real-time AI analytics, decision intelligence, and automated data exploration."),
    ("Tableau AI vs Julius AI: AI Analytics for Data Scientists", "ai-analytics",
     ["tableau", "julius-ai", "data-science", "ai-analytics", "data-visualization"],
     "Analyze Tableau AI and Julius AI for AI analytics features designed for data scientists and advanced data analysis."),
    ("Zendesk AI vs Ada: AI Customer Support Chatbots Compared", "ai-chatbots",
     ["zendesk-ai", "ada", "customer-support", "chatbots", "ai-automation"],
     "Compare Zendesk AI and Ada for AI-powered customer support chatbots, automation, and ticket resolution."),
    ("Drift vs Freshworks: AI Chatbots for Sales and Marketing", "ai-chatbots",
     ["drift", "freshworks", "sales-chatbots", "marketing-automation", "ai-conversations"],
     "Explore Drift and Freshworks for AI chatbots focused on sales lead generation and marketing engagement."),
    ("Chatbase vs Ada: Custom AI Chatbot Platforms for Businesses", "ai-chatbots",
     ["chatbase", "ada", "custom-chatbots", "ai-platforms", "business-automation"],
     "Compare Chatbase and Ada for building custom AI chatbots with no-code tools and enterprise integrations."),
    ("Botpress vs Zendesk AI: Open-Source vs Enterprise Chatbots", "ai-chatbots",
     ["botpress", "zendesk-ai", "open-source-chatbots", "enterprise-ai", "customer-service"],
     "See how Botpress and Zendesk AI differ for open-source chatbot development versus enterprise customer service AI."),
    ("Tidio vs Drift: AI Chatbots for Small Business Support", "ai-chatbots",
     ["tidio", "drift", "small-business", "ai-chatbots", "customer-support"],
     "Compare Tidio and Drift for AI chatbot solutions tailored to small business customer support and engagement."),
    ("Intercom vs Freshworks: AI Customer Support Tools for SaaS", "ai-chatbots",
     ["intercom", "freshworks", "saas-support", "ai-customer-service", "chatbot-platforms"],
     "Analyze Intercom and Freshworks for AI-driven customer support tools optimized for SaaS companies."),
    ("Amazon Q vs Replit Ghostwriter: AI Coding Assistants for Developers", "ai-coding",
     ["amazon-q", "replit-ghostwriter", "ai-coding", "developer-tools", "code-generation"],
     "Compare Amazon Q and Replit Ghostwriter for AI-powered code generation, debugging, and developer productivity."),
    ("Tabnine vs Amazon Q: AI Code Completion for Enterprise Teams", "ai-coding",
     ["tabnine", "amazon-q", "code-completion", "enterprise-coding", "ai-assistants"],
     "Explore Tabnine and Amazon Q for enterprise-grade AI code completion and team collaboration features."),
    ("Codeium vs Replit Ghostwriter: AI Coding Tools for Beginners", "ai-coding",
     ["codeium", "replit-ghostwriter", "beginner-coding", "ai-tools", "code-assistance"],
     "Compare Codeium and Replit Ghostwriter for AI coding assistance designed for beginner programmers and students."),
    ("Windsurf vs Tabnine: AI Code Editors for Productivity", "ai-coding",
     ["windsurf", "tabnine", "ai-code-editors", "productivity", "code-assistance"],
     "See how Windsurf and Tabnine compare as AI-powered code editors for boosting developer productivity."),
    ("Cursor vs Amazon Q: AI Coding Assistants for Advanced Users", "ai-coding",
     ["cursor", "amazon-q", "advanced-coding", "ai-assistants", "code-refactoring"],
     "Analyze Cursor and Amazon Q for advanced AI coding features like refactoring, multi-file editing, and context awareness."),
    ("GitHub Copilot vs Replit Ghostwriter: AI Coding for Collaborative Projects", "ai-coding",
     ["github-copilot", "replit-ghostwriter", "collaborative-coding", "ai-tools", "code-generation"],
     "Compare GitHub Copilot and Replit Ghostwriter for AI coding support in collaborative and team-based development environments."),
    ("Ideogram vs Canva AI: AI Image Generation for Designers", "ai-image",
     ["ideogram", "canva-ai", "image-generation", "design-tools", "ai-creativity"],
     "Compare Ideogram and Canva AI for AI image generation features tailored to graphic designers and creatives."),
    ("Leonardo AI vs Firefly: AI Art Tools for Professional Use", "ai-image",
     ["leonardo-ai", "adobe-firefly", "ai-art", "professional-design", "image-creation"],
     "Explore Leonardo AI and Adobe Firefly for professional AI art creation, style control, and commercial use."),
    ("Stable Diffusion vs Ideogram: Open-Source AI Image Generators", "ai-image",
     ["stable-diffusion", "ideogram", "open-source", "image-generation", "ai-models"],
     "Compare Stable Diffusion and Ideogram for open-source AI image generation with customization and community support."),
    ("DALL-E 3 vs Canva AI: AI Image Tools for Marketing", "ai-image",
     ["dalle-3", "canva-ai", "marketing-images", "ai-design", "content-creation"],
     "See how DALL-E 3 and Canva AI stack up for AI image generation in marketing campaigns and social media content."),
    ("Midjourney vs Leonardo AI: AI Image Generation for Artists", "ai-image",
     ["midjourney", "leonardo-ai", "ai-artists", "image-generation", "creative-tools"],
     "Analyze Midjourney and Leonardo AI for AI image generation focused on artistic expression and visual creativity."),
    ("Firefly vs Ideogram: AI Image Tools for Brand Design", "ai-image",
     ["adobe-firefly", "ideogram", "brand-design", "ai-image-tools", "visual-identity"],
     "Compare Adobe Firefly and Ideogram for AI image generation used in brand design and corporate visual identity."),
    ("Reclaim AI vs Taskade: AI Productivity Tools for Time Management", "ai-productivity",
     ["reclaim-ai", "taskade", "time-management", "ai-productivity", "task-automation"],
     "Compare Reclaim AI and Taskade for AI-powered time management, scheduling, and task automation features."),
    ("Otter.ai vs Fireflies.ai: AI Meeting Assistants for Teams", "ai-productivity",
     ["otter-ai", "fireflies-ai", "meeting-assistants", "ai-transcription", "team-productivity"],
     "Explore Otter.ai and Fireflies.ai for AI meeting transcription, note-taking, and team collaboration tools."),
    ("Notion AI vs Reclaim AI: AI Productivity for Project Management", "ai-productivity",
     ["notion-ai", "reclaim-ai", "project-management", "ai-productivity", "task-organization"],
     "Compare Notion AI and Reclaim AI for AI-driven project management, task organization, and workflow automation."),
    ("Mem vs Taskade: AI Note-Taking and Task Management", "ai-productivity",
     ["mem", "taskade", "note-taking", "task-management", "ai-assistants"],
     "See how Mem and Taskade compare for AI note-taking and task management with smart organization features."),
    ("Fireflies.ai vs Reclaim AI: AI Tools for Scheduling and Meetings", "ai-productivity",
     ["fireflies-ai", "reclaim-ai", "scheduling", "meeting-management", "ai-automation"],
     "Analyze Fireflies.ai and Reclaim AI for AI tools that automate meeting scheduling, notes, and calendar management."),
    ("Notion AI vs Otter.ai: AI Productivity for Content Creators", "ai-productivity",
     ["notion-ai", "otter-ai", "content-creators", "ai-productivity", "writing-assistance"],
     "Compare Notion AI and Otter.ai for AI productivity features tailored to content creators and writers."),
    ("Scite vs Semantic Scholar: AI Research Tools for Citation Analysis", "ai-research",
     ["scite", "semantic-scholar", "citation-analysis", "ai-research", "academic-tools"],
     "Compare Scite and Semantic Scholar for AI-powered citation analysis, research discovery, and academic literature review."),
    ("ResearchRabbit vs Elicit: AI Tools for Literature Review", "ai-research",
     ["researchrabbit", "elicit", "literature-review", "ai-research", "academic-discovery"],
     "Explore ResearchRabbit and Elicit for AI-driven literature review, paper recommendations, and research mapping."),
    ("Consensus vs Scite: AI Research Tools for Evidence-Based Answers", "ai-research",
     ["consensus", "scite", "evidence-based", "ai-research", "academic-answers"],
     "Compare Consensus and Scite for AI research tools that provide evidence-based answers and citation insights."),
    ("Perplexity AI vs Semantic Scholar: AI Research Assistants for Students", "ai-research",
     ["perplexity-ai", "semantic-scholar", "student-research", "ai-assistants", "academic-tools"],
     "See how Perplexity AI and Semantic Scholar compare as AI research assistants for students and academic projects."),
    ("Google Gemini vs ResearchRabbit: AI Tools for Research Discovery", "ai-research",
     ["google-gemini", "researchrabbit", "research-discovery", "ai-tools", "academic-exploration"],
     "Analyze Google Gemini and ResearchRabbit for AI-powered research discovery and academic paper exploration."),
    ("Elicit vs Semantic Scholar: AI Research Tools for Scientists", "ai-research",
     ["elicit", "semantic-scholar", "scientific-research", "ai-tools", "literature-search"],
     "Compare Elicit and Semantic Scholar for AI research tools designed for scientists and systematic literature searches."),
    ("Pictory vs Descript: AI Video Editing Tools for Content Creators", "ai-video",
     ["pictory", "descript", "video-editing", "ai-tools", "content-creation"],
     "Compare Pictory and Descript for AI-powered video editing, transcription, and content repurposing features."),
    ("Invideo AI vs HeyGen: AI Video Generation for Marketing", "ai-video",
     ["invideo-ai", "heygen", "video-generation", "marketing-videos", "ai-avatars"],
     "Explore Invideo AI and HeyGen for AI video generation tailored to marketing campaigns and avatar-based content."),
    ("Synthesia vs Pictory: AI Video Tools for Business Presentations", "ai-video",
     ["synthesia", "pictory", "business-videos", "ai-presentations", "video-creation"],
     "Compare Synthesia and Pictory for AI video tools focused on business presentations and professional video content."),
    ("Runway vs Descript: AI Video Editing for Professionals", "ai-video",
     ["runway", "descript", "professional-video", "ai-editing", "post-production"],
     "See how Runway and Descript compare for AI video editing features aimed at professional post-production workflows."),
    ("Pika Labs vs Invideo AI: AI Video Generation for Social Media", "ai-video",
     ["pika-labs", "invideo-ai", "social-media-videos", "ai-generation", "short-form-content"],
     "Analyze Pika Labs and Invideo AI for AI video generation optimized for social media and short-form content."),
    ("HeyGen vs Pictory: AI Avatar Videos vs Text-to-Video", "ai-video",
     ["heygen", "pictory", "avatar-videos", "text-to-video", "ai-content"],
     "Compare HeyGen and Pictory for AI video creation, focusing on avatar-based videos versus text-to-video conversion."),
    ("Speechify vs Resemble AI: AI Voice Tools for Accessibility", "ai-voice",
     ["speechify", "resemble-ai", "text-to-speech", "accessibility", "ai-voice"],
     "Compare Speechify and Resemble AI for AI voice generation focused on accessibility, text-to-speech, and custom voices."),
    ("WellSaid Labs vs Lovo AI: AI Voice Generation for E-Learning", "ai-voice",
     ["wellsaid-labs", "lovo-ai", "e-learning", "ai-voice", "text-to-speech"],
     "Explore WellSaid Labs and Lovo AI for AI voice generation tailored to e-learning content and educational narration."),
    ("ElevenLabs vs Resemble AI: AI Voice Cloning and Customization", "ai-voice",
     ["elevenlabs", "resemble-ai", "voice-cloning", "ai-customization", "text-to-speech"],
     "Compare ElevenLabs and Resemble AI for AI voice cloning, customization, and realistic speech synthesis."),
    ("Play.ht vs Speechify: AI Text-to-Speech for Content Consumption", "ai-voice",
     ["play-ht", "speechify", "text-to-speech", "content-consumption", "ai-voice"],
     "See how Play.ht and Speechify compare for AI text-to-speech tools designed for content consumption and listening."),
    ("Murf AI vs WellSaid Labs: AI Voice Tools for Corporate Narration", "ai-voice",
     ["murf-ai", "wellsaid-labs", "corporate-narration", "ai-voice", "text-to-speech"],
     "Analyze Murf AI and WellSaid Labs for AI voice generation used in corporate narration, training videos, and presentations."),
    ("Lovo AI vs ElevenLabs: AI Voice Generation for Creative Projects", "ai-voice",
     ["lovo-ai", "elevenlabs", "creative-projects", "ai-voice", "text-to-speech"],
     "Compare Lovo AI and ElevenLabs for AI voice generation features suited for creative projects like podcasts and animations."),
    ("Claude vs Writesonic: AI Writing Tools for Long-Form Content", "ai-writing",
     ["claude", "writesonic", "long-form-content", "ai-writing", "content-creation"],
     "Compare Claude and Writesonic for AI writing tools focused on long-form content, articles, and in-depth reports."),
    ("ChatGPT vs Rytr: AI Writing Tools for Budget-Conscious Users", "ai-writing",
     ["chatgpt", "rytr", "budget-writing", "ai-tools", "content-generation"],
     "Explore ChatGPT and Rytr for affordable AI writing tools for budget-conscious content creators and small businesses."),
    ("Grammarly vs Notion AI: AI Writing Assistants for Editing", "ai-writing",
     ["grammarly", "notion-ai", "writing-assistants", "ai-editing", "proofreading"],
     "Compare Grammarly and Notion AI for AI-powered writing assistance, grammar checking, and editing features."),
    ("Jasper AI vs Claude: AI Writing Tools for Marketing Copy", "ai-writing",
     ["jasper-ai", "claude", "marketing-copy", "ai-writing", "content-strategy"],
     "See how Jasper AI and Claude compare for AI writing tools optimized for marketing copy and brand messaging."),
    ("Copy.ai vs Writesonic: AI Writing Tools for Short-Form Content", "ai-writing",
     ["copy-ai", "writesonic", "short-form-content", "ai-writing", "social-media"],
     "Analyze Copy.ai and Writesonic for AI writing tools designed for short-form content like social media posts and ads."),
    ("Rytr vs Notion AI: AI Writing Tools for Note-Taking and Drafting", "ai-writing",
     ["rytr", "notion-ai", "note-taking", "ai-drafting", "content-creation"],
     "Compare Rytr and Notion AI for AI writing tools that support note-taking, drafting, and quick content generation."),
    ("ClickUp vs Monday.com: Project Management for Agile Teams", "saas",
     ["ClickUp", "Monday.com", "Asana", "Notion", "Wrike"],
     "Compare ClickUp and Monday.com for agile project management in 2026. Features, pricing, and team workflows analyzed."),
    ("Miro vs Mural: Digital Whiteboard for Remote Collaboration", "saas",
     ["Miro", "Mural", "Figma", "Notion", "Lucidchart"],
     "Miro vs Mural: Which digital whiteboard tool wins for remote team collaboration in 2026? Compare features and use cases."),
    ("Linear vs Jira: Issue Tracking for Software Teams", "saas",
     ["Linear", "Jira", "ClickUp", "Asana", "Basecamp"],
     "Linear vs Jira: Best issue tracking tool for software development teams in 2026. Speed, simplicity, and integrations compared."),
    ("Coda vs Notion: All-in-One Document and Database Platform", "saas",
     ["Coda", "Notion", "Airtable", "Google Docs", "Slite"],
     "Coda vs Notion: Which all-in-one workspace tool is better for docs and databases in 2026? Detailed comparison."),
    ("Basecamp vs Wrike: Project Management for Small Teams", "saas",
     ["Basecamp", "Wrike", "Asana", "Monday.com", "Smartsheet"],
     "Basecamp vs Wrike: Project management tools for small teams in 2026. Pricing, features, and ease of use compared."),
    ("Smartsheet vs Airtable: Spreadsheet-Database Hybrid Tools", "saas",
     ["Smartsheet", "Airtable", "Notion", "Google Sheets", "Monday.com"],
     "Smartsheet vs Airtable: Which spreadsheet-database hybrid tool is best for business workflows in 2026?"),
    ("n8n vs Pipedream: Open-Source Automation Platforms", "automation",
     ["n8n", "Pipedream", "Zapier", "Make", "Tray.io"],
     "n8n vs Pipedream: Compare open-source no-code automation platforms for developers in 2026. Self-hosting and flexibility."),
    ("Workato vs Tray.io: Enterprise Automation Platforms", "automation",
     ["Workato", "Tray.io", "Zapier", "Make", "UiPath"],
     "Workato vs Tray.io: Which enterprise automation platform offers better scalability and integrations in 2026?"),
    ("UiPath vs Power Automate: RPA Tools for Business Automation", "automation",
     ["UiPath", "Power Automate", "Workato", "Appian", "Tray.io"],
     "UiPath vs Power Automate: Compare RPA tools for business process automation in 2026. Features and pricing."),
    ("IFTTT vs Zapier: Simple Automation for Personal Use", "automation",
     ["IFTTT", "Zapier", "Make", "n8n", "Pipedream"],
     "IFTTT vs Zapier: Which simple automation tool is best for personal workflows in 2026? Ease of use and app support."),
    ("Appian vs Make: Low-Code Automation for Business", "automation",
     ["Appian", "Make", "Zapier", "Workato", "UiPath"],
     "Appian vs Make: Low-code automation platforms compared for business users in 2026. Speed and complexity."),
    ("Tray.io vs Workato: Advanced Integration Platforms", "automation",
     ["Tray.io", "Workato", "Zapier", "Make", "n8n"],
     "Tray.io vs Workato: Advanced integration platforms for complex automation workflows in 2026. Pricing and features."),
    ("Lunacy vs Figma: Free Design Tools for UI/UX", "design",
     ["Lunacy", "Figma", "Sketch", "Canva", "Adobe XD"],
     "Lunacy vs Figma: Compare free design tools for UI/UX projects in 2026. Features, offline use, and collaboration."),
    ("Visme vs Canva: Presentation and Graphic Design Tools", "design",
     ["Visme", "Canva", "Adobe Express", "Piktochart", "Easil"],
     "Visme vs Canva: Which tool is better for presentations and graphic design in 2026? Templates and features compared."),
    ("Piktochart vs Snappa: Infographic and Social Media Design", "design",
     ["Piktochart", "Snappa", "Canva", "Visme", "VistaCreate"],
     "Piktochart vs Snappa: Best tool for infographics and social media graphics in 2026. Ease of use and templates."),
    ("VistaCreate vs Easil: Design Tools for Marketers", "design",
     ["VistaCreate", "Easil", "Canva", "Adobe Express", "Snappa"],
     "VistaCreate vs Easil: Compare design tools for marketers in 2026. Brand kits, templates, and pricing."),
    ("Adobe Express vs Canva: Quick Design for Non-Designers", "design",
     ["Adobe Express", "Canva", "Visme", "Snappa", "Piktochart"],
     "Adobe Express vs Canva: Which quick design tool is best for non-designers in 2026? Features and ease of use."),
    ("Sketch vs Figma: Vector Design for Professionals", "design",
     ["Sketch", "Figma", "Lunacy", "Adobe XD", "InVision"],
     "Sketch vs Figma: Vector design tools for professional UI/UX designers in 2026. Collaboration and plugins compared."),
    ("Moz vs Ahrefs: SEO Tool for Link Building and Keywords", "seo-tools",
     ["Moz", "Ahrefs", "Semrush", "SpyFu", "SE Ranking"],
     "Moz vs Ahrefs: Which SEO tool is better for link building and keyword research in 2026? Features and pricing."),
    ("SpyFu vs Semrush: Competitive Analysis SEO Tools", "seo-tools",
     ["SpyFu", "Semrush", "Ahrefs", "Moz", "Mangools"],
     "SpyFu vs Semrush: Compare competitive analysis SEO tools for PPC and organic research in 2026."),
    ("Screaming Frog vs Surfer SEO: Technical SEO and Content Optimization", "seo-tools",
     ["Screaming Frog", "Surfer SEO", "Ahrefs", "Semrush", "Clearscope"],
     "Screaming Frog vs Surfer SEO: Technical SEO audits vs content optimization tools compared in 2026."),
    ("Clearscope vs Surfer SEO: Content Optimization Platforms", "seo-tools",
     ["Clearscope", "Surfer SEO", "Semrush", "Ahrefs", "Moz"],
     "Clearscope vs Surfer SEO: Which content optimization platform drives better search rankings in 2026?"),
    ("SE Ranking vs Mangools: Affordable SEO Tools for Small Businesses", "seo-tools",
     ["SE Ranking", "Mangools", "Ahrefs", "Semrush", "Moz"],
     "SE Ranking vs Mangools: Compare affordable SEO tools for small businesses in 2026. Features and pricing."),
    ("Mangools vs Moz: Beginner-Friendly SEO Tools", "seo-tools",
     ["Mangools", "Moz", "Ahrefs", "Semrush", "SpyFu"],
     "Mangools vs Moz: Which beginner-friendly SEO tool offers the best value in 2026? Ease of use and features."),
    ("ActiveCampaign vs ConvertKit: Email Marketing for Creators", "email-marketing",
     ["ActiveCampaign", "ConvertKit", "Mailchimp", "MailerLite", "Drip"],
     "ActiveCampaign vs ConvertKit: Best email marketing platform for creators and bloggers in 2026. Automation and pricing."),
    ("Brevo vs MailerLite: Affordable Email Marketing Solutions", "email-marketing",
     ["Brevo", "MailerLite", "Mailchimp", "ConvertKit", "Campaign Monitor"],
     "Brevo vs MailerLite: Compare affordable email marketing tools for small businesses in 2026. Features and deliverability."),
    ("Drip vs Klaviyo: Ecommerce Email Marketing Platforms", "email-marketing",
     ["Drip", "Klaviyo", "Mailchimp", "ActiveCampaign", "Brevo"],
     "Drip vs Klaviyo: Which ecommerce email marketing platform drives better sales in 2026? Features and pricing."),
    ("Campaign Monitor vs Mailchimp: Email Marketing for Agencies", "email-marketing",
     ["Campaign Monitor", "Mailchimp", "ActiveCampaign", "Brevo", "MailerLite"],
     "Campaign Monitor vs Mailchimp: Email marketing tools for agencies in 2026. Templates, automation, and reporting."),
    ("Klaviyo vs ActiveCampaign: Advanced Email Automation", "email-marketing",
     ["Klaviyo", "ActiveCampaign", "Drip", "Mailchimp", "ConvertKit"],
     "Klaviyo vs ActiveCampaign: Compare advanced email automation platforms for ecommerce in 2026."),
    ("MailerLite vs ConvertKit: Email Marketing for Beginners", "email-marketing",
     ["MailerLite", "ConvertKit", "Mailchimp", "Brevo", "Drip"],
     "MailerLite vs ConvertKit: Best email marketing tool for beginners in 2026. Simplicity, pricing, and features."),
    ("Later vs Buffer: Social Media Scheduling for Visual Content", "social-media",
     ["Later", "Buffer", "Hootsuite", "Planoly", "Metricool"],
     "Later vs Buffer: Which social media scheduling tool is best for visual content in 2026? Features and pricing."),
    ("Sprout Social vs Agorapulse: Social Media Management for Agencies", "social-media",
     ["Sprout Social", "Agorapulse", "Hootsuite", "Buffer", "SocialBee"],
     "Sprout Social vs Agorapulse: Compare social media management tools for agencies in 2026. Reporting and collaboration."),
    ("SocialBee vs Buffer: Social Media Automation for Small Teams", "social-media",
     ["SocialBee", "Buffer", "Hootsuite", "Later", "Metricool"],
     "SocialBee vs Buffer: Which social media automation tool is best for small teams in 2026? Content recycling and pricing."),
    ("Planoly vs Later: Instagram-First Scheduling Tools", "social-media",
     ["Planoly", "Later", "Buffer", "Hootsuite", "Metricool"],
     "Planoly vs Later: Compare Instagram-first scheduling tools for visual content in 2026. Features and analytics."),
    ("Metricool vs Hootsuite: All-in-One Social Media Analytics", "social-media",
     ["Metricool", "Hootsuite", "Buffer", "Sprout Social", "Agorapulse"],
     "Metricool vs Hootsuite: Which all-in-one social media analytics tool is better in 2026? Pricing and features."),
    ("Agorapulse vs Sprout Social: Social Media Engagement and CRM", "social-media",
     ["Agorapulse", "Sprout Social", "Hootsuite", "Buffer", "SocialBee"],
     "Agorapulse vs Sprout Social: Compare social media engagement and CRM tools for businesses in 2026."),
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
