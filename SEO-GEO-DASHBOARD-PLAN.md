# 🎯 SEO/GEO Observability Dashboard - Master Plan

## 📊 RESEARCH SUMMARY

Based on comprehensive research using Brave Search (Feb 2026), here's the complete plan for building an automated SEO/GEO dashboard with daily reporting and action item generation.

---

## 🏗️ DASHBOARD ARCHITECTURE

### **Three Pillars of Observability:**
1. **SEO (Search Engine Optimization)** - Traditional Google/Bing rankings
2. **GEO (Generative Engine Optimization)** - AI search visibility (ChatGPT, Perplexity, Gemini)
3. **Social/Local** - Social media + Google Business Profile performance

---

## 📈 FREE DATA SOURCES & APIs

### **1. Google APIs (FREE)**
| API | What It Provides | Cost |
|-----|------------------|------|
| **Google Search Console API** | Rankings, impressions, clicks, CTR, position | FREE |
| **PageSpeed Insights API** | Performance, accessibility, SEO scores, Core Web Vitals | FREE |
| **Google Analytics 4 API** | Traffic, sessions, conversions, user behavior | FREE |
| **Google Business Profile API** | Reviews, posts, local insights, search queries | FREE |

### **2. Social Media APIs**
| Platform | API Access | Cost |
|----------|-----------|------|
| **Twitter/X API** | Posts, engagement, analytics | Free tier (limited) |
| **Instagram Graph API** | Business insights, reach, engagement | FREE (business accounts) |
| **Facebook Graph API** | Page insights, post performance | FREE |
| **Threads API** | Post metrics | FREE (via Meta) |
| **Late.dev** | Unified social posting + analytics | Already using! |

### **3. Website Analytics (FREE Self-Hosted)**
| Tool | Features | Hosting |
|------|----------|---------|
| **Umami** | Privacy-focused, lightweight, 100k events/mo free cloud | Self-host or cloud |
| **Plausible** | Simple UI, GDPR-compliant | Self-host available |
| **Google Analytics 4** | Full-featured, complex | Google Cloud |

### **4. Third-Party SEO Tools (Free Tiers)**
| Tool | Free Features |
|------|---------------|
| **Ahrefs Webmaster Tools** | Backlinks, site audit (limited) |
| **Ubersuggest** | Keyword ideas, basic rank tracking |
| **AnswerThePublic** | Question-based keyword research |
| **Keywords Everywhere** | Chrome extension, search volume data |
| **Screaming Frog** | 500 URLs free crawl for technical SEO |

### **5. GEO Monitoring (New Category!)**
| Tool | What It Tracks |
|------|---------------|
| **OtterlyAI** | ChatGPT, Perplexity, Google AI visibility |
| **AthenaHQ** | GEO optimization scoring |
| **Manual Checks** | Query brand in AI tools, track citations |

---

## 📊 DASHBOARD SECTIONS

### **Section 1: SEO Performance**
```
┌─────────────────────────────────────────────────────────────┐
│  📈 SEO OVERVIEW                                             │
├──────────────────┬──────────────────┬───────────────────────┤
│  Total Clicks    │  Impressions     │  Average Position     │
│  1,234 (+12%)    │  45,678 (+8%)    │  8.2 (↑ from 9.1)    │
├──────────────────┴──────────────────┴───────────────────────┤
│  🔑 TOP KEYWORDS (by clicks)                                 │
│  1. kona coffee waikiki - Pos: 3.2 - Clicks: 156            │
│  2. mochi donuts honolulu - Pos: 5.1 - Clicks: 89           │
│  3. coffee shop kalakaua ave - Pos: 2.8 - Clicks: 67        │
├─────────────────────────────────────────────────────────────┤
│  📉 DECLINING KEYWORDS (action needed)                       │
│  • "hawaiian coffee" dropped 4 positions                     │
│  • "donuts near waikiki beach" lost 23% traffic             │
└─────────────────────────────────────────────────────────────┘
```

### **Section 2: Technical SEO Health**
```
┌─────────────────────────────────────────────────────────────┐
│  🔧 TECHNICAL SEO SCORES (PageSpeed Insights)                │
├──────────────────┬──────────────────┬───────────────────────┤
│  Performance: 85 │  Accessibility:92│  SEO Score: 98        │
├──────────────────┴──────────────────┴───────────────────────┤
│  ⚡ CORE WEB VITALS                                          │
│  • LCP: 2.1s (Good ✅)                                       │
│  • FID: 45ms (Good ✅)                                       │
│  • CLS: 0.08 (Good ✅)                                       │
├─────────────────────────────────────────────────────────────┤
│  🚨 ISSUES DETECTED                                          │
│  • 3 images not optimized                                    │
│  • Missing alt text on 2 images                              │
│  • Render-blocking CSS detected                              │
└─────────────────────────────────────────────────────────────┘
```

### **Section 3: GEO (AI Search) Visibility**
```
┌─────────────────────────────────────────────────────────────┐
│  🤖 GEO VISIBILITY - AI Search Presence                      │
├──────────────────┬──────────────────┬───────────────────────┤
│  ChatGPT Cites   │  Perplexity Cites│  Google AI Overview   │
│  2/10 queries    │  4/10 queries    │  1/10 queries         │
├──────────────────┴──────────────────┴───────────────────────┤
│  📝 TRACKED QUERIES                                          │
│  "best kona coffee in waikiki" → ✅ Cited in Perplexity     │
│  "mochi donuts honolulu" → ❌ Not appearing                  │
│  "coffee near waikiki beach" → ✅ Google AI Overview        │
├─────────────────────────────────────────────────────────────┤
│  💡 GEO OPTIMIZATION TIPS                                    │
│  • Add more FAQ schema markup                                │
│  • Include authoritative citations in content                │
│  • Build Reddit/Medium presence (high AI cite rate)          │
└─────────────────────────────────────────────────────────────┘
```

### **Section 4: Local SEO (Google Business)**
```
┌─────────────────────────────────────────────────────────────┐
│  📍 LOCAL SEO - Google Business Profile                      │
├──────────────────┬──────────────────┬───────────────────────┤
│  Profile Views   │  Direction Reqs  │  Phone Calls          │
│  1,892 (+15%)    │  234 (+8%)       │  45 (+22%)            │
├──────────────────┴──────────────────┴───────────────────────┤
│  ⭐ REVIEWS                                                  │
│  Average: 4.8/5 (32 reviews)                                 │
│  New this week: +3 reviews                                   │
│  Pending replies: 1                                          │
├─────────────────────────────────────────────────────────────┤
│  🔍 TOP SEARCH QUERIES (Local)                               │
│  • "coffee shop near me" - 45 discoveries                    │
│  • "kona coffee honolulu" - 28 discoveries                   │
│  • "donuts waikiki" - 19 discoveries                         │
└─────────────────────────────────────────────────────────────┘
```

### **Section 5: Social Media Performance**
```
┌─────────────────────────────────────────────────────────────┐
│  📱 SOCIAL MEDIA - Cross-Platform Analytics                  │
├────────┬────────┬────────┬────────┬────────┬───────────────┤
│Platform│Posts   │Engage  │Reach   │Growth  │ Best Post     │
├────────┼────────┼────────┼────────┼────────┼───────────────┤
│Twitter │ 14     │ 2.3%   │ 4,521  │ +45    │ Volcanic soil │
│Facebook│ 14     │ 3.1%   │ 2,890  │ +23    │ Kona special  │
│Insta   │ 14     │ 4.2%   │ 3,456  │ +67    │ Mochi donut   │
│Threads │ 14     │ 2.8%   │ 1,234  │ +34    │ Coffee hill   │
│Bluesky │ 10     │ 1.9%   │ 567    │ +12    │ Volcanic      │
├────────┴────────┴────────┴────────┴────────┴───────────────┤
│  📊 ENGAGEMENT TRENDS                                        │
│  [Chart: 7-day engagement by platform]                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 📧 DAILY REPORT FORMAT

### **Daily Report Email Structure:**

```
═══════════════════════════════════════════════════════════════
📊 KONA COFFEE DONUT - DAILY SEO/GEO REPORT
📅 February 1, 2026
═══════════════════════════════════════════════════════════════

🎯 EXECUTIVE SUMMARY
────────────────────
• Overall Health Score: 87/100 (↑2 from yesterday)
• SEO: 85/100 | GEO: 72/100 | Social: 91/100 | Local: 89/100

📈 KEY METRICS (vs Yesterday)
────────────────────
• Organic Traffic: 234 sessions (+12%)
• Keyword Rankings: 3 improved, 1 declined
• Social Engagement: 456 interactions (+8%)
• Google Business Views: 189 (+15%)
• AI Search Citations: 6 (same)

🚨 ALERTS (Immediate Attention)
────────────────────
1. ⚠️ "hawaiian donuts" dropped from #5 to #9
2. 🔴 1 negative review needs response
3. ⏰ PageSpeed score dropped to 78 (was 85)

✅ WINS TODAY
────────────────────
1. 🏆 "kona coffee waikiki" reached #2 position!
2. 📈 Instagram post got 234 likes (highest ever)
3. ⭐ New 5-star review received

📋 ACTION ITEMS (Prioritized)
────────────────────
🔴 HIGH PRIORITY:
  □ Respond to negative review within 24h
  □ Optimize images to fix PageSpeed drop
  
🟡 MEDIUM PRIORITY:
  □ Create content targeting "hawaiian donuts" keyword
  □ Add FAQ schema for GEO optimization
  
🟢 LOW PRIORITY:
  □ Schedule posts for weekend
  □ Update Google Business hours for holiday

📊 DETAILED METRICS ATTACHED
═══════════════════════════════════════════════════════════════
```

---

## 🎬 ACTION ITEMS GENERATION LOGIC

### **Automatic Action Item Categories:**

#### **1. KEYWORD/RANKING ACTIONS**
| Trigger | Action Generated |
|---------|-----------------|
| Keyword drops 3+ positions | "Investigate and optimize content for [keyword]" |
| Keyword enters top 10 | "Create supporting content to push to top 3" |
| New keyword opportunity | "Consider creating content for [keyword]" |
| Keyword stuck at position 11-20 | "Optimize on-page SEO for [keyword]" |

#### **2. TECHNICAL SEO ACTIONS**
| Trigger | Action Generated |
|---------|-----------------|
| PageSpeed < 80 | "Optimize images and defer JS" |
| Core Web Vitals fail | "Fix [LCP/FID/CLS] issue - [specific fix]" |
| Missing meta descriptions | "Add meta descriptions to [pages]" |
| Broken links detected | "Fix [N] broken links" |
| Mobile usability issues | "Fix mobile issues on [pages]" |

#### **3. LOCAL SEO ACTIONS**
| Trigger | Action Generated |
|---------|-----------------|
| New review (any rating) | "Respond to new [star] review" |
| Review response pending > 24h | "URGENT: Respond to review" |
| Profile views declining | "Update Google Business posts" |
| Competitor gaining | "Add more photos/posts to profile" |

#### **4. SOCIAL MEDIA ACTIONS**
| Trigger | Action Generated |
|---------|-----------------|
| Engagement drops 20%+ | "Review content strategy for [platform]" |
| Post goes viral | "Boost post / create similar content" |
| Follower growth stalls | "Run engagement campaign" |
| No posts in 48h | "Schedule posts for [platform]" |

#### **5. GEO ACTIONS**
| Trigger | Action Generated |
|---------|-----------------|
| Not cited in AI for target query | "Optimize content with citations and facts" |
| Competitor cited instead | "Add authoritative sources, update content" |
| New AI platform trending | "Ensure content is structured for [platform]" |

---

## 🔧 TECHNICAL IMPLEMENTATION

### **Phase 1: Data Collection (Week 1)**
```
1. Google Search Console API
   - Set up OAuth2 authentication
   - Schedule daily data pulls
   - Store in SQLite/PostgreSQL

2. PageSpeed Insights API
   - Get free API key
   - Daily automated checks
   - Track historical scores

3. Google Business Profile API
   - Connect business account
   - Pull reviews, insights
   - Track local metrics

4. Social Media (via Late.dev)
   - Already integrated!
   - Add analytics endpoints
   - Track post performance
```

### **Phase 2: Dashboard (Week 2)**
```
1. Frontend
   - Extend existing unified dashboard
   - Add SEO/GEO sections
   - Mobile-responsive charts

2. Backend
   - API endpoints for metrics
   - Data aggregation service
   - Historical trend storage
```

### **Phase 3: Reporting (Week 3)**
```
1. Email Reports
   - Daily summary email
   - Weekly detailed report
   - Monthly executive report

2. Action Items Engine
   - Rule-based triggers
   - Priority scoring
   - Slack/Telegram alerts
```

### **Phase 4: Automation (Week 4+)**
```
1. Auto-Optimization
   - Image compression on upload
   - Meta tag suggestions
   - Content recommendations

2. AI Integration
   - GPT-powered content suggestions
   - Automated competitor analysis
   - Trend detection
```

---

## 💰 COST ANALYSIS

### **FREE Tools (No Cost)**
- Google Search Console API: $0
- Google PageSpeed Insights API: $0
- Google Analytics 4 API: $0
- Google Business Profile API: $0
- Umami Analytics (self-hosted): $0
- Late.dev (current plan): Already paid
- Brave Search API: Already paid

### **Optional Paid Tools (Future)**
- Ahrefs API: $99/mo (if needed)
- OtterlyAI (GEO tracking): $49/mo (optional)
- Semrush: $119/mo (optional)

### **Total Initial Cost: $0** (using free APIs)

---

## 🗓️ IMPLEMENTATION TIMELINE

| Week | Tasks |
|------|-------|
| **Week 1** | Set up Google APIs, data storage, basic collection |
| **Week 2** | Build dashboard UI, integrate with existing system |
| **Week 3** | Email reporting, action items engine |
| **Week 4** | Automation rules, alerts, refinement |
| **Ongoing** | Add GEO tracking, competitor analysis, AI features |

---

## 📋 IMMEDIATE NEXT STEPS

1. **Create Google Cloud Project** for API access
2. **Enable APIs**: Search Console, PageSpeed, Analytics, Business Profile
3. **Set up OAuth2** credentials
4. **Create data collection scripts**
5. **Extend existing dashboard** with SEO sections
6. **Build email report template**
7. **Implement action item rules**

---

*Generated by Zoe 🎯 | ZOE STUDIO LLC | February 2026*
