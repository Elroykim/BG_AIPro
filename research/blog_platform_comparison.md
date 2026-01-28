# Blog Platform Comparison for Automation

**Research Date:** January 2026
**Purpose:** Evaluate blog platforms for automated content publishing with minimal human intervention

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Platform Deep Dives](#platform-deep-dives)
3. [Comparison Matrix](#comparison-matrix)
4. [Recommendation](#recommendation)

---

## Executive Summary

This report evaluates seven blog platforms across six key dimensions: API completeness, automation friendliness, SEO capabilities, cost, Korean market relevance, and ease of full automation. The analysis reveals that **WordPress (self-hosted)** and **Ghost (self-hosted)** are the strongest candidates for full automation, while **Jekyll/Hugo + GitHub Pages** offers the best cost-to-flexibility ratio for developer-oriented workflows. Korean-market-specific platforms (Naver Blog, Tistory) present significant automation barriers despite their local relevance.

---

## Platform Deep Dives

---

### 1. WordPress (Self-hosted & WordPress.com)

#### REST API Capabilities

WordPress provides a comprehensive REST API (`/wp-json/wp/v2/`) that is fully documented and actively maintained.

**Supported Operations:**
| Operation | Endpoint | Status |
|-----------|----------|--------|
| Create Post | `POST /wp/v2/posts` | Full support |
| Read Posts | `GET /wp/v2/posts` | Full support |
| Update Post | `PUT /wp/v2/posts/{id}` | Full support |
| Delete Post | `DELETE /wp/v2/posts/{id}` | Full support |
| Media Upload | `POST /wp/v2/media` | Full support |
| Categories/Tags | `CRUD /wp/v2/categories`, `/wp/v2/tags` | Full support |
| Pages | `CRUD /wp/v2/pages` | Full support |
| Users | `CRUD /wp/v2/users` | Full support |
| Custom Post Types | Via registered types | Full support |
| Scheduling | `date` field + `status: future` | Full support |
| Custom Fields | `meta` parameter | Full support |

**Authentication Methods:**
- **Application Passwords** (built-in since WordPress 5.6) -- best for automation; no 2FA prompt, revocable per-application
- **Cookie + Nonce** -- browser-based only
- **OAuth 1.0a / JWT** -- via plugins, suited for third-party apps

**WordPress 6.9 Abilities API (December 2025):**
A new standardized system that exposes all site functionality in a machine-readable format. Every registered "ability" automatically becomes a REST endpoint. This positions WordPress as the most AI-agent-friendly CMS, enabling automation tools to discover and invoke any site capability programmatically.

#### Automation Friendliness

- **Rate Limits:** No built-in rate limiting (can be added via plugins like WP REST Cop or Wordfence). Self-hosted installations have no external rate limits.
- **Bot Detection:** None by default. TOS-compliant for self-hosted installations since you control the server.
- **WordPress.com:** Imposes its own rate limits and restrictions. Uses a different API (WP.com REST API v1.1) which requires OAuth2 authentication.
- **TOS Compliance:** Self-hosted has no TOS restrictions on API usage. WordPress.com has a Terms of Service that may restrict automated posting.

#### SEO Capabilities

- **Excellent.** Industry-leading SEO plugin ecosystem (Yoast SEO, AIOSEO, Rank Math).
- Full control over meta titles, descriptions, OpenGraph tags, schema markup, sitemaps, robots.txt.
- Programmatic SEO metadata setting via REST API when using compatible plugins.
- All SEO plugins expose their fields through the REST API.

#### Cost

| Tier | Cost | Notes |
|------|------|-------|
| Self-hosted (software) | Free (open source) | Need hosting ($5-50/month) |
| WordPress.com Free | $0 | Limited features, ads displayed |
| WordPress.com Personal | $4/month | Custom domain |
| WordPress.com Business | $25/month | Plugin/theme support |
| WordPress.com eCommerce | $45/month | Full features |

#### Korean Language Support

- WordPress core is fully translated into Korean.
- Multilingual plugins: WPML, Polylang, Weglot, MultilingualPress.
- Full hreflang tag support for Korean SEO.
- Korean-specific keyword research tools integrate well.
- Active Korean WordPress community exists but is smaller than the Naver/Tistory ecosystem.

#### Verdict

**API Completeness: 10/10** | **Automation Friendliness: 10/10** (self-hosted) | **SEO: 10/10** | **Korean Relevance: 6/10**

---

### 2. Tistory (티스토리)

#### API Availability and Capabilities

**CRITICAL: The official Tistory Open API was shut down in February 2024.**

The API was discontinued in a phased approach:
1. File attachment API -- shut down first
2. Post-related API -- shut down second
3. Comment-related API -- shut down third
4. All remaining features -- fully terminated

Tistory cited spam and automated post registration as primary reasons for the shutdown.

**Previous API capabilities (no longer available):**
- Post CRUD operations
- Comment management
- Blog info retrieval
- File/image upload
- Category management

#### Current Automation Possibilities

| Method | Viability | Risk Level |
|--------|-----------|------------|
| Selenium/browser automation | Works but fragile | High (DOM changes, detection) |
| Third-party bridge APIs (e.g., BridgeFlow) | Works | Medium (dependency on third party, ~10,000 KRW/month) |
| No-code tools (N8N, Make.com) via bridges | Works | Medium |
| Open-source Python library (`pip install tistory`) | Limited/broken | High (API shutdown) |

#### SEO Features

- Tistory blogs are indexed by both Google and Naver.
- Basic SEO settings available through the Tistory dashboard.
- Custom HTML/CSS editing allowed (skin editing).
- Supports custom domains.
- Google AdSense integration is possible but difficult with AI-generated content (Google has been rejecting AdSense applications for AI-generated blog content).

#### Korean Market Relevance

- **High.** Tistory is operated by Kakao, one of South Korea's largest tech companies.
- Popular among Korean bloggers for its flexibility compared to Naver Blog.
- Good visibility in both Naver search and Google Korea.
- Ad revenue generation through Google AdSense and Kakao AdFit.

#### Verdict

**API Completeness: 1/10** (API shut down) | **Automation Friendliness: 3/10** | **SEO: 6/10** | **Korean Relevance: 8/10**

---

### 3. Naver Blog (네이버 블로그)

#### API Availability

Naver provides two methods for blog post creation:

**1. Naver Open API (Login-based Blog Writing API)**
- Requires OAuth access token via "Naver Login" (네이버 아이디로 로그인)
- Application registration required (Client ID + Client Secret)
- API permission configuration through the developer console

**2. XML-RPC Blog API**
- Endpoint: `https://api.blog.naver.com/xmlrpc`
- Requires blog ID + API connection password from blog admin settings
- Supports: post creation, categories, tags, image upload (auto-attached from body), private posts, post deletion

**Critical Limitations:**
| Feature | Status |
|---------|--------|
| Post Creation | Supported |
| Post Reading | Limited (search API only) |
| Post Editing | NOT supported (policy change; must delete + recreate) |
| Post Deletion | Supported |
| Image Upload | Supported (must be in post body) |
| SmartEditor Features | NOT supported via API |
| Scheduling | NOT supported |

#### Automation Restrictions

Naver has implemented aggressive anti-automation measures as of mid-2025:
- **Strong bot detection:** IP-based rate limiting, browser fingerprinting, behavioral analysis
- **Automated interaction blocking:** Comments, likes (공감), and neighbor requests (서로이웃) via bots are actively blocked
- **Non-Korean IP blocking:** Requests from non-Korean IP addresses may be blocked
- **Dynamic content rendering:** Blog data is dynamically generated, making standard crawling difficult
- **Selenium detection:** Naver actively detects and blocks Selenium-based automation

#### Korean Search Engine Dominance

- Naver commands approximately 55-60% of the Korean search market.
- Naver's search results strongly favor Naver Blog content over external sites.
- Naver Blog posts appear in a dedicated "Blog" tab in Naver search results.
- While Naver claims not to discriminate, it is demonstrably better at crawling and indexing its own blog platform.
- **Naver Posts** (a stripped-down version of Naver Blogs) was shut down on April 30, 2025.

#### Limitations

- No full CRUD API -- editing via API is broken by policy
- Heavy anti-bot protections make reliable automation difficult
- SmartEditor features cannot be replicated through API
- Content is largely siloed within the Naver ecosystem
- Limited Google visibility for Naver Blog content
- Risk of account suspension for detected automation

#### Verdict

**API Completeness: 4/10** | **Automation Friendliness: 2/10** | **SEO: 7/10** (Naver only) | **Korean Relevance: 10/10**

---

### 4. Medium

#### API Capabilities

Medium's official API is extremely limited and has been stagnant for years.

**Official API (api.medium.com):**
| Operation | Status |
|-----------|--------|
| Create Post | Supported (POST only) |
| Read Posts | NOT supported |
| Update Post | NOT supported |
| Delete Post | NOT supported |
| List Posts | NOT supported |
| Media Upload | Supported (images only) |
| Scheduling | NOT supported |
| Publications | Supported (create post under publication) |

**Key constraints:**
- Write-only API -- you can publish but cannot read, list, update, or delete
- No post editing capability whatsoever
- No way to retrieve post analytics
- No scheduling functionality
- Authentication via integration tokens only

**Workarounds:**
- **Unofficial Medium API** (mediumapi.com): Paid third-party service for read operations (fetching authors, articles, publications, top feeds, etc.)
- **RSS Feed:** `medium.com/feed/@username` for reading published posts
- **No viable update/delete workaround exists**

#### Automation Support

- Extremely limited due to write-only API
- Cannot build a full content management pipeline
- No way to programmatically correct or update published content
- Medium has shown no interest in expanding API capabilities

#### Audience Reach

- Strong English-language audience, particularly in tech and startup communities
- Built-in distribution through Medium's recommendation algorithm
- Partner Program for monetization
- Publication system allows content curation
- Very limited Korean audience

#### Verdict

**API Completeness: 2/10** | **Automation Friendliness: 2/10** | **SEO: 5/10** | **Korean Relevance: 2/10**

---

### 5. Ghost

#### API Capabilities

Ghost provides two well-documented, RESTful JSON APIs:

**Content API (Read-only, public data):**
| Operation | Status |
|-----------|--------|
| Browse Posts | Full support with filtering, pagination, ordering |
| Read Single Post | Full support |
| Browse Tags | Full support |
| Browse Authors | Full support |
| Browse Pages | Full support |
| Browse Settings | Full support |

**Admin API (Full CRUD):**
| Operation | Status |
|-----------|--------|
| Create Post | Full support |
| Read Post | Full support |
| Update Post | Full support |
| Delete Post | Full support |
| Create Page | Full support |
| Media Upload | Full support (images) |
| Tags CRUD | Full support |
| Members CRUD | Full support |
| Tiers/Offers | Full support |
| Webhooks | Full support |
| Scheduling | Full support (via `published_at` and `status: scheduled`) |

**Authentication:**
- Content API: Simple API key in query parameter
- Admin API: JWT-based authentication or Staff Access Tokens
- Custom integrations get dedicated API keys with configurable permissions
- Webhook support for event-driven automation

**Query Capabilities:**
- Powerful filtering (`filter` parameter with NQL syntax)
- Field selection (`fields` parameter)
- Include relations (`include` parameter)
- Pagination (`limit`, `page`)
- Ordering (`order` parameter)

**SDKs Available:**
- Official JavaScript SDK (`@tryghost/content-api`, `@tryghost/admin-api`)
- TypeScript SDK (`@ts-ghost/admin-api`) with Zod schema validation
- MCP Server available for AI agent integration

#### Self-Hosting Options

| Option | Details |
|--------|---------|
| Ghost(Pro) Starter | $9/month (managed hosting) |
| Ghost(Pro) Creator | $25/month |
| Ghost(Pro) Team | $50/month |
| Ghost(Pro) Business | $199/month |
| Self-hosted | Free (open source), you pay for hosting |
| Docker Compose | New in Ghost 6.0, supports all features including ActivityPub and web analytics |

**Self-hosting requirements:**
- Node.js 18+
- MySQL 8.0+ (or SQLite for small installations)
- 1GB RAM minimum (2GB+ recommended)
- SSD storage recommended
- Mailgun or Postmark for email (self-hosters must configure their own)

**Ghost 6.0 Features:**
- Built-in privacy-focused analytics
- ActivityPub integration (Fediverse)
- Bluesky integration
- Modern Docker Compose deployment

#### Automation Friendliness

- **Excellent.** The Admin API mirrors everything Ghost Admin can do.
- No rate limits on self-hosted installations.
- Webhook support enables event-driven workflows (new post published, member created, etc.).
- Zapier integration connects to thousands of services.
- MCP Server available for AI agent automation.
- Full TOS compliance for self-hosted (you own the infrastructure).

#### Verdict

**API Completeness: 9/10** | **Automation Friendliness: 9/10** | **SEO: 8/10** | **Korean Relevance: 2/10**

---

### 6. Jekyll/Hugo + GitHub Pages

#### Static Site Generation

**Jekyll:**
- Ruby-based, created by GitHub co-founder Tom Preston-Werner (2008)
- Native GitHub Pages support with zero configuration
- Liquid templating engine (easy to learn)
- Large plugin ecosystem
- Slower build times for large sites (Ruby performance)
- Requires Ruby environment

**Hugo:**
- Go-based, created by Steve Francia (2013)
- Sub-second build times (orders of magnitude faster than Jekyll)
- Built-in multilingual support (including Korean)
- No dependencies (single binary)
- Requires GitHub Actions for GitHub Pages deployment
- Growing faster than Jekyll in adoption

#### Git-Based Automation

This is where static site generators truly excel for automation:

```
Content Generation -> Markdown File -> Git Commit -> Push -> CI/CD Build -> Deploy
```

**Automation Pipeline:**
| Step | Tool | Complexity |
|------|------|-----------|
| Content creation | AI API / script | Simple |
| File creation | Write `.md` file with front matter | Simple |
| Version control | `git add`, `git commit` | Simple |
| Trigger deploy | `git push` | Simple |
| Build site | GitHub Actions / Netlify / Vercel | Automatic |
| Deploy | GitHub Pages / Netlify / Vercel / Cloudflare Pages | Automatic |

**Key Advantages for Automation:**
- No API authentication needed -- just write files to a git repository
- No rate limits -- limited only by git push frequency and build minutes
- Full version control -- every change tracked, rollback trivial
- No database -- content is plain Markdown files
- CI/CD integration -- GitHub Actions can run any script (content generation, image optimization, SEO checks)
- Headless CMS options -- Netlify CMS, Forestry, CloudCannon for optional GUI

**Front Matter Example (Hugo):**
```yaml
---
title: "Your Post Title"
date: 2026-01-28T10:00:00+09:00
draft: false
tags: ["automation", "blogging"]
categories: ["technology"]
description: "SEO description here"
---

Post content in Markdown...
```

#### Cost

| Component | Cost |
|-----------|------|
| Jekyll/Hugo software | Free (open source) |
| GitHub Pages hosting | Free (public repos) |
| GitHub Actions (build) | Free (2,000 min/month for free tier) |
| Custom domain | ~$10-15/year |
| Netlify hosting | Free tier available |
| Vercel hosting | Free tier available |
| Cloudflare Pages | Free tier available |

**Total cost for a fully automated blog: $0 - $15/year** (domain only)

#### SEO Capabilities

- Full control over HTML output, meta tags, structured data
- Custom sitemaps, robots.txt, canonical URLs
- Lightning-fast page load (static HTML = perfect Core Web Vitals)
- No server-side processing = minimal TTFB
- Hugo has built-in SEO features (OpenGraph, Twitter Cards, Schema)
- Jekyll requires plugins or manual configuration

#### Korean Language Support

- Hugo has built-in multilingual support with Korean
- Jekyll supports Korean through configuration
- Both support Korean content natively (UTF-8 Markdown)
- No inherent platform-level Korean SEO advantages

#### Verdict

**API Completeness: N/A (file-based, no API needed)** | **Automation Friendliness: 10/10** | **SEO: 9/10** | **Korean Relevance: 4/10**

---

### 7. Velog (벨로그)

#### Korean Developer Community

- Created by velopert (김민준), a prominent Korean developer
- Focused exclusively on the Korean developer community
- Provides a comfortable Markdown editor with syntax highlighting
- **Currently supports Korean language only**
- Popular among Korean developers for technical blog posts
- Used as a portfolio platform by Korean job seekers

#### API Availability

**Official Public API: Does NOT exist.**

There is a long-standing GitHub issue (#283) with 100+ upvotes requesting an API similar to dev.to's OpenAPI, but no official API has been released.

**What is available:**
| Feature | Availability |
|---------|-------------|
| Official REST API | Not available |
| GraphQL API (internal) | Exists but undocumented and unsupported |
| RSS Feed | Available at `https://api.velog.io/rss/@username` |
| Post creation via API | Not available |
| Post editing via API | Not available |
| Post deletion via API | Not available |

**Workarounds:**
- **RSS Feed + GitHub Actions:** Sync published Velog posts to a GitHub repository as Markdown files (read-only, one-way)
- **Internal GraphQL API:** Some developers have reverse-engineered Velog's internal GraphQL API, but this is unsupported and could break at any time
- **No viable post creation automation exists**

#### Automation Possibilities

Effectively none for content creation. Velog is designed as a manual writing platform. The only automation is one-way export via RSS.

#### Verdict

**API Completeness: 1/10** | **Automation Friendliness: 1/10** | **SEO: 4/10** | **Korean Relevance: 7/10** (developer niche only)

---

## Comparison Matrix

### Overall Scores (1-10 scale)

| Platform | API Completeness | Automation Friendliness | SEO | Cost Efficiency | Korean Relevance | Full Automation Feasibility |
|----------|:---:|:---:|:---:|:---:|:---:|:---:|
| **WordPress (self-hosted)** | 10 | 10 | 10 | 8 | 6 | **10** |
| **WordPress.com** | 8 | 6 | 8 | 6 | 6 | 6 |
| **Ghost (self-hosted)** | 9 | 9 | 8 | 8 | 2 | **9** |
| **Ghost(Pro)** | 9 | 8 | 8 | 5 | 2 | 8 |
| **Jekyll/Hugo + GitHub Pages** | N/A | 10 | 9 | 10 | 4 | **9** |
| **Tistory** | 1 | 3 | 6 | 9 | 8 | 2 |
| **Naver Blog** | 4 | 2 | 7* | 10 | 10 | 2 |
| **Medium** | 2 | 2 | 5 | 10 | 2 | 2 |
| **Velog** | 1 | 1 | 4 | 10 | 7** | 1 |

*Naver SEO score is 7 within the Naver ecosystem only; Google SEO is much lower.*
**Velog relevance is limited to the Korean developer niche.*

### Feature Support Matrix

| Feature | WordPress (Self) | Ghost (Self) | Jekyll/Hugo | Tistory | Naver Blog | Medium | Velog |
|---------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Create Post via API | Yes | Yes | File-based | No* | Yes | Yes | No |
| Read Posts via API | Yes | Yes | File-based | No* | Limited | No | RSS only |
| Update Post via API | Yes | Yes | File-based | No* | No | No | No |
| Delete Post via API | Yes | Yes | File-based | No* | Yes | No | No |
| Media Upload via API | Yes | Yes | File-based | No* | Yes | Yes | No |
| Scheduling | Yes | Yes | CI/CD cron | No* | No | No | No |
| Webhooks | Yes | Yes | GitHub Webhooks | No | No | No | No |
| Rate Limits | None (self) | None (self) | Git limits only | N/A | Strict | Unknown | N/A |
| Bot Detection | None (self) | None (self) | None | Selenium only | Aggressive | N/A | N/A |
| Custom Domain | Yes | Yes | Yes | Yes | No | No (paid only) | No |
| SSL/HTTPS | Yes | Yes | Yes (free) | Yes | Yes | Yes | Yes |

*Tistory API was shut down in February 2024.*

### Cost Comparison

| Platform | Minimum Cost (Monthly) | Recommended Setup Cost (Monthly) | Notes |
|----------|:---:|:---:|------|
| WordPress (self-hosted) | $5 | $10-20 | VPS hosting + domain |
| WordPress.com | $0 | $25 | Business plan for plugins |
| Ghost (self-hosted) | $5 | $10-20 | VPS hosting + domain |
| Ghost(Pro) | $9 | $25 | Creator plan |
| Jekyll/Hugo + GitHub Pages | $0 | $0-1 | Domain cost only |
| Tistory | $0 | $0 | Free (Kakao-operated) |
| Naver Blog | $0 | $0 | Free (Naver-operated) |
| Medium | $0 | $0 | Free to publish |
| Velog | $0 | $0 | Free |

---

## Recommendation

### For Full Automation with Global SEO: WordPress (Self-hosted)

**Why:** Complete REST API with full CRUD, no rate limits, unmatched plugin ecosystem for SEO, the new Abilities API (WordPress 6.9) makes it the most automation-ready CMS. Application Passwords make authentication simple and secure.

**Best for:** Production-grade automated blogging systems, multi-language content strategies, monetized blogs.

### For Full Automation with Minimal Cost: Jekyll/Hugo + GitHub Pages

**Why:** File-based architecture means no API authentication needed. Git-based workflows integrate naturally with CI/CD pipelines. GitHub Actions provides free compute for content generation and deployment. Zero hosting cost.

**Best for:** Developer-operated automation pipelines, technical blogs, projects where content is generated programmatically and version control is valued.

### For Clean API Design + Membership Features: Ghost (Self-hosted)

**Why:** Ghost's API is the most cleanly designed of all platforms. Full CRUD with powerful filtering, webhook support, and membership/newsletter management built in. The Admin API exactly mirrors what the admin dashboard can do.

**Best for:** Newsletter-oriented blogs, membership-based content, projects that value a clean and modern API.

### For Korean Market Reach: Multi-Platform Strategy Required

No single platform satisfies both automation requirements and Korean market dominance. The recommended approach:

1. **Primary platform:** WordPress (self-hosted) or Hugo + GitHub Pages for the main automated blog
2. **Naver Blog:** Limited automated posting via XML-RPC API (create-only, accept limitations)
3. **Tistory:** Selenium-based automation or third-party bridge APIs (fragile but possible)
4. **Cross-posting:** Use the primary platform as the source of truth, then distribute to Korean platforms

### Platforms to Avoid for Automation

- **Medium:** Write-only API with no update capability. Not suitable for any serious automation pipeline.
- **Velog:** No API whatsoever. Designed for manual writing only.
- **Naver Blog (as primary):** Anti-bot measures make reliable automation extremely difficult and risk account suspension.

---

## Sources

- [WordPress REST API Handbook](https://developer.wordpress.org/rest-api/)
- [WordPress Abilities API in 6.9](https://make.wordpress.org/core/2025/11/10/abilities-api-in-wordpress-6-9/)
- [WordPress Application Passwords](https://developer.wordpress.org/rest-api/reference/application-passwords/)
- [WordPress REST API Authentication Guide 2025](https://oddjar.com/wordpress-rest-api-authentication-guide-2025/)
- [Tistory Open API Shutdown Notice](https://tistory.github.io/document-tistory-apis/)
- [Tistory Open API Documentation (GitHub)](https://github.com/tistory/document-tistory-apis)
- [Naver Open API List](https://naver.github.io/naver-openapi-guide/apilist.html)
- [Naver Blog XML-RPC API](https://github.com/yousung/naver-blog-xmlrpc)
- [Naver SEO Guide 2025](https://www.interad.com/en/insights/naver-seo-guide)
- [Medium API Documentation (GitHub)](https://github.com/Medium/medium-api-docs)
- [Medium API Limitations](https://www.marktinderholt.com/social%20media/2024/12/13/medium-rare-api.html)
- [Ghost Admin API Docs](https://docs.ghost.org/admin-api)
- [Ghost Content API Docs](https://docs.ghost.org/api/content/#posts)
- [Ghost CMS GitHub Repository](https://github.com/TryGhost/Ghost)
- [Ghost Hosting Options](https://docs.ghost.org/hosting)
- [Ghost CMS Statistics 2025](https://enricher.io/blog/ghost-cms-statistics)
- [Hugo vs Jekyll Comparison](https://draft.dev/learn/hugo-vs-jekyll)
- [Hugo Official Site](https://gohugo.io/)
- [Jekyll Official Site](https://jekyllrb.com/)
- [Velog GitHub Repository](https://github.com/velog-io/velog)
- [Velog API Feature Request (Issue #283)](https://github.com/velopert/velog-client/issues/283)
- [WordPress Korean Translation](https://codex.wordpress.org/ko:WordPress_in_Your_Language)
- [WordPress Multilingual SEO Guide](https://aioseo.com/the-beginners-guide-to-wordpress-multilingual-seo/)
