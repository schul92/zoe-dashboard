# 🔍 SEO Dashboard Integration Review
## Current State Analysis & Step-by-Step Plan

---

## 📊 WHAT WE ALREADY HAVE

### **1. Lambda Functions (4 total)**
| Function | Purpose | Status |
|----------|---------|--------|
| `ZoeUniversalPoster` | Social media posting (5 platforms) | ✅ WORKING |
| `ZoeSEOMonitor` | SEO monitoring | ⚠️ EXISTS (needs review) |
| `EC2WakeTelegram` | EC2 control via Telegram | ✅ WORKING |
| `ZoeEC2Control` | EC2 start/stop | ✅ WORKING |

### **2. EventBridge Schedules**
| Rule | Schedule | Status |
|------|----------|--------|
| `ZoeSEO-KonaCoffee-Daily` | 6:00 UTC daily | ✅ ENABLED |
| `ZoeUniversal-KonaCoffee-Daily` | 18:00 UTC daily | ✅ ENABLED |
| `ZoeIdleCheck` | Every minute | ✅ ENABLED |
| `KonaLate-Morning` | 18:00 UTC | ❌ DISABLED |

### **3. Secrets Manager**
| Secret | Purpose |
|--------|---------|
| `kona/api-keys` | Late.dev + social API keys |
| `seo-data/kona-coffee` | SEO data storage |
| `BraveSearchAPI` | Web search |
| `ahrefs-api-key` | SEO (needs verification) |

### **4. SES Email**
- ✅ `info@konacoffeedonut.com` - VERIFIED

### **5. Current Workflow**
```
18:00 UTC Daily:
  EventBridge → ZoeUniversalPoster → 5 Platforms + Email Report

06:00 UTC Daily:
  EventBridge → ZoeSEOMonitor → (needs review)
```

---

## 🤔 MY THOUGHTS & ANALYSIS

### **What's Working Well:**
1. ✅ Social posting fully automated (2x daily possible)
2. ✅ Email delivery working (SES verified)
3. ✅ Secrets management in place
4. ✅ EventBridge scheduling infrastructure ready
5. ✅ Dashboard server running via Tailscale

### **Gaps to Fill:**
1. ❓ `ZoeSEOMonitor` - need to review what it actually does
2. ❓ Google Search Console not yet connected
3. ❓ Looker Studio dashboard not created
4. ❓ Alert thresholds not defined
5. ❓ Bird CLI not integrated into workflow

### **Key Insight:**
We already have **80% of the infrastructure** in place! The SEO EventBridge rule is running daily at 6:00 UTC. We just need to:
1. Review/update the ZoeSEOMonitor Lambda
2. Connect Google Search Console data
3. Set up Looker Studio for visual dashboard

---

## 📋 STEP-BY-STEP INTEGRATION PLAN

### **PHASE 1: Review & Verify (Today)**

#### Step 1.1: Check ZoeSEOMonitor Lambda
```bash
# What does it currently do?
aws lambda get-function --function-name ZoeSEOMonitor
# Check CloudWatch logs for recent runs
```
**Question for Steve**: Do you have the source code for ZoeSEOMonitor? What was the original intent?

#### Step 1.2: Verify Google Search Console Access
- Is konacoffeedonut.com added to GSC?
- Who has access? (need Google account with permissions)
- Need: OAuth2 credentials for API access

#### Step 1.3: Check Ahrefs API Key
```bash
# Verify the secret exists and is valid
aws secretsmanager get-secret-value --secret-id ahrefs-api-key
```

---

### **PHASE 2: Looker Studio Setup (Week 1)**

#### Step 2.1: Create Looker Studio Dashboard
1. Go to: https://lookerstudio.google.com
2. Create new report
3. Add data source: Google Search Console
4. Select property: konacoffeedonut.com
5. Choose metrics: Position, Clicks, Impressions, CTR

#### Step 2.2: Dashboard Sections
| Section | Metrics |
|---------|---------|
| Overview | Total clicks, impressions, avg position |
| Keywords | Top 20 keywords by clicks |
| Trends | 7-day/30-day click trends |
| Ranking Distribution | Top 3, Top 10, Top 20 breakdown |
| Movement | Gainers vs Losers (position change) |

#### Step 2.3: Schedule Weekly Email
- Looker Studio → Share → Schedule delivery
- Recipient: info@konacoffeedonut.com
- Frequency: Weekly (Monday 8am HST = 18:00 UTC)

---

### **PHASE 3: Daily Alerts Lambda (Week 2)**

#### Step 3.1: Update ZoeSEOMonitor
The Lambda should:
1. Fetch GSC data via API (last 2 days)
2. Compare today vs yesterday
3. Check thresholds:
   - Keyword drop > 5 positions → ALERT
   - Traffic drop > 20% → ALERT
   - CTR drop > 30% → ALERT
4. Send email only if alerts exist

#### Step 3.2: Alert Email Format
```
🚨 SEO ALERT - Kona Coffee Donut
📅 February 2, 2026

⚠️ KEYWORD DROPS:
• "kona coffee waikiki" dropped 6 positions (was #3, now #9)
• "mochi donuts honolulu" dropped 8 positions (was #5, now #13)

📉 TRAFFIC ALERT:
• Clicks down 25% vs yesterday (was 156, now 117)

📋 RECOMMENDED ACTIONS:
1. Check content for "kona coffee waikiki" - may need refresh
2. Review recent changes that might have affected rankings
3. Monitor for 48h before taking action

---
Full report: [Looker Studio Link]
```

#### Step 3.3: Threshold Configuration
Store in `seo-data/kona-coffee` secret:
```json
{
  "alertThresholds": {
    "positionDrop": 5,
    "trafficDropPct": 20,
    "ctrDropPct": 30
  },
  "keywords": ["kona coffee", "mochi donuts", "waikiki coffee"]
}
```

---

### **PHASE 4: Bird CLI Integration (Week 3)**

#### Step 4.1: Add to Daily Workflow
```bash
# Add to ZoeSEOMonitor or separate Lambda
bird search "@konacoffeedonut" --limit 10
bird search "#KonaCoffee" --limit 10
```

#### Step 4.2: Track Social Mentions
- Count mentions per day
- Identify sentiment (positive/negative)
- Alert if unusual activity

---

### **PHASE 5: GEO Tracking (Month 2)**

#### Step 5.1: Manual Weekly Check
- Use HubSpot AI Search Grader
- Track: "kona coffee waikiki", "best coffee honolulu"
- Log results in spreadsheet

#### Step 5.2: Automate Later
- Consider HubSpot API integration
- Or custom script to query ChatGPT/Perplexity

---

## 🔄 PROPOSED DAILY WORKFLOW

```
┌─────────────────────────────────────────────────────────────┐
│                    DAILY AUTOMATION                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  06:00 UTC (8pm HST previous day)                           │
│  ┌─────────────────────────────────────────┐                │
│  │  EventBridge → ZoeSEOMonitor            │                │
│  │  • Fetch GSC data                       │                │
│  │  • Check thresholds                     │                │
│  │  • Send alert email (if needed)         │                │
│  │  • Check Twitter mentions (Bird CLI)    │                │
│  └─────────────────────────────────────────┘                │
│                                                              │
│  18:00 UTC (8am HST)                                        │
│  ┌─────────────────────────────────────────┐                │
│  │  EventBridge → ZoeUniversalPoster       │                │
│  │  • Post to 5 platforms                  │                │
│  │  • Send daily report email              │                │
│  └─────────────────────────────────────────┘                │
│                                                              │
│  WEEKLY (Monday 18:00 UTC)                                  │
│  ┌─────────────────────────────────────────┐                │
│  │  Looker Studio → Scheduled Email        │                │
│  │  • Full SEO report                      │                │
│  │  • Keyword rankings                     │                │
│  │  • Traffic trends                       │                │
│  │  • Week-over-week comparison            │                │
│  └─────────────────────────────────────────┘                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## ❓ QUESTIONS FOR STEVE

Before we proceed, I need clarity on:

1. **Google Search Console**: 
   - Is konacoffeedonut.com already in GSC?
   - Which Google account has access?
   - Can you share OAuth2 credentials or should I create them?

2. **ZoeSEOMonitor Lambda**:
   - Do you have the source code?
   - What was the original purpose?
   - Should we rebuild it or modify existing?

3. **Looker Studio**:
   - Do you have a Google account for Looker Studio?
   - Should the dashboard be shared with anyone else?

4. **Alert Recipients**:
   - Only info@konacoffeedonut.com?
   - Or also your personal email for alerts?

5. **Priority**:
   - Start with Looker Studio (visual dashboard)?
   - Or start with Lambda alerts (automation)?

---

## 🎯 RECOMMENDED FIRST STEP

**My recommendation**: Start with **Looker Studio + GSC connection** because:
1. Provides immediate visibility into SEO performance
2. No coding required (native connector)
3. Weekly reports automated with built-in feature
4. Foundation for all other work

Once that's working, we build the alert Lambda on top.

---

*Integration Review - February 2, 2026*
*Zoe 🎯 | ZOE STUDIO LLC*
