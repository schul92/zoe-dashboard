# Multi-Client Dashboard Structure

## Overview

The dashboard now supports multiple clients with isolated data and switching capabilities.

## Folder Structure

```
zoe-dashboard/
├── clients/
│   ├── kona/                  # Kona Coffee Donut
│   │   ├── seo/               # SEO dashboard data
│   │   ├── news/              # News dashboard data
│   │   └── social/            # Social media calendar
│   └── carek9/                # CareK9
│       ├── seo/               # SEO dashboard data
│       ├── news/              # News dashboard data
│       └── social/            # Social media calendar
├── index.html                 # Hub with client switcher
└── [other shared files]
```

## How It Works

### Client Switcher

The hub dashboard (`index.html`) has a dropdown to select which client's data to view.

**Selection is persisted** in `localStorage` so your choice stays across page reloads.

### Data Isolation

Each client has completely separate data:
- SEO metrics, keywords, rankings
- News sources and content drafts
- Social media posts and calendar

### Adding a New Client

1. Create folder structure:
```bash
mkdir -p clients/newclient/seo clients/newclient/news clients/newclient/social
```

2. Add to client selector in `index.html`:
```html
<option value="newclient">🏢 New Client Name</option>
```

3. Update data collection scripts to support `--client newclient` parameter

## Backward Compatibility

Symlinks maintain old URLs:
```
/seo/ → /clients/kona/seo/
/news/ → /clients/kona/news/
/social/ → /clients/kona/social/
```

Old links still work but always show Kona data.

## Client Configuration

Each client can have different:
- Google Search Console property
- Google Analytics property  
- Social media accounts
- AWS Secrets (stored as `clientname/api-keys`)

## Scripts Update Required

All data collection scripts need `--client` parameter:
```bash
python3 scripts/fetch_seo_comprehensive.py --client kona
python3 scripts/collect_daily_news.py --client carek9
```

## Security Note

**CRITICAL:** Never mix client data! Always specify `--client` parameter in cron jobs and scripts.

Wrong client data = bad SEO insights = potential business decisions based on wrong metrics.
