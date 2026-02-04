# 🎯 SEO Observability Dashboard - REVISED PLAN v2

## ✅ APPROVED STACK

### **Core: Looker Studio + Google Search Console**
| Metric | Source | Status |
|--------|--------|--------|
| Keyword rankings (position) | GSC | ✅ Native |
| Impressions | GSC | ✅ Native |
| Clicks | GSC | ✅ Native |
| CTR | GSC | ✅ Native |
| Traffic trends over time | GSC | ✅ Native |
| Keyword movement (gaining/losing) | GSC | ✅ Calculated |
| Ranking distribution (Top 3/10/20) | GSC | ✅ Calculated |
| Brand vs Non-brand segmentation | GSC | ✅ Filter |

---

## 🏗️ REVISED ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│                    SEO OBSERVABILITY SYSTEM                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   Looker    │    │  EventBridge │    │   Lambda    │     │
│  │   Studio    │    │   (Daily)    │    │  (Alerts)   │     │
│  │  Dashboard  │    │   Scheduler  │    │  Threshold  │     │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘     │
│         │                   │                  │             │
│         ▼                   ▼                  ▼             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │    GSC      │    │   Lambda    │    │     SES     │     │
│  │  Connector  │    │   Check     │    │   Email     │     │
│  │   (Native)  │    │   Metrics   │    │   Alerts    │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                                                              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   Bird CLI  │    │  HubSpot    │    │  Secrets    │     │
│  │  X/Twitter  │    │ AI Grader   │    │  Manager    │     │
│  │  (ReadOnly) │    │ (FREE GEO!) │    │  (API Keys) │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 REPORT FREQUENCY

| Type | Frequency | Method | Content |
|------|-----------|--------|---------|
| **Alerts** | Daily | Lambda + SES | Threshold breaches only |
| **Full Report** | Weekly | Looker Studio scheduled email | Complete metrics |

### **Daily Alerts (Lambda triggers):**
- Keyword drops > 5 positions
- Traffic drops > 20%
- New negative review
- PageSpeed < 70
- Site down/errors

### **Weekly Report (Looker Studio):**
- Full keyword performance
- Ranking distribution charts
- Traffic trends
- Top/bottom performers
- Week-over-week comparison

---

## 🔧 AWS NATIVE STACK

| Component | Purpose | Cost |
|-----------|---------|------|
| **EventBridge** | Daily alert scheduler | FREE |
| **Lambda** | Check thresholds, send alerts | FREE tier |
| **SES** | Send alert emails | FREE tier (62k/mo) |
| **Secrets Manager** | Store API keys | Already have |

---

## 🐦 BIRD CLI - Twitter Monitoring

**Installed**: ✅ v0.8.0
**Purpose**: READ ONLY X/Twitter monitoring

```bash
# Check mentions
bird search "@konacoffeedonut"

# Monitor hashtags
bird search "#KonaCoffee"

# Track brand mentions
bird search "kona coffee donut"
```

---

## 🤖 GEO TRACKING - FREE OPTION FOUND!

### **HubSpot AI Search Grader** (FREE!)
- URL: https://www.hubspot.com/aeo-grader/generative-engine-optimization-tool
- Tracks: ChatGPT, Perplexity, Gemini visibility
- Cost: **$0**
- Features:
  - Brand visibility in AI search
  - Competitor comparison
  - Optimization recommendations

### **Implementation:**
- Manual weekly check (Phase 1)
- Automate via HubSpot API (Phase 2)

---

## 📋 IMPLEMENTATION CHECKLIST

### **Phase 1: Looker Studio Setup (This Week)**
- [ ] Create Google Cloud project for Kona Coffee
- [ ] Connect GSC to Looker Studio (native connector)
- [ ] Import free SEO dashboard template
- [ ] Customize for Kona Coffee metrics
- [ ] Set up weekly scheduled email delivery
- [ ] Add konacoffeedonut.com to GSC (if not already)

### **Phase 2: Alert System (Next Week)**
- [ ] Create Lambda function for threshold checks
- [ ] Set up EventBridge daily schedule (8am HST)
- [ ] Configure SES email template
- [ ] Define alert thresholds:
  - Keyword drop > 5 positions
  - Traffic drop > 20%
  - PageSpeed < 70
- [ ] Test alert delivery to info@konacoffeedonut.com

### **Phase 3: Social Monitoring**
- [ ] Set up Bird CLI cron job for daily mentions
- [ ] Integrate Twitter metrics into weekly report
- [ ] Track engagement trends

### **Phase 4: GEO (Future)**
- [ ] Weekly manual HubSpot AI Grader check
- [ ] Document AI search visibility
- [ ] Consider paid tools when ROI justifies

---

## 🎯 ALERT LAMBDA PSEUDOCODE

```python
import boto3
import requests

def lambda_handler(event, context):
    # 1. Fetch GSC data via API
    gsc_data = get_gsc_metrics()
    
    # 2. Compare to yesterday
    alerts = []
    
    # Keyword position drops
    for kw in gsc_data['keywords']:
        if kw['position_change'] > 5:
            alerts.append(f"⚠️ '{kw['query']}' dropped {kw['position_change']} positions")
    
    # Traffic drops
    if gsc_data['clicks_change_pct'] < -20:
        alerts.append(f"🔴 Traffic down {gsc_data['clicks_change_pct']}%")
    
    # 3. Send alerts if any
    if alerts:
        send_ses_email(
            to="info@konacoffeedonut.com",
            subject="🚨 SEO Alert - Kona Coffee Donut",
            body="\n".join(alerts)
        )
    
    return {'statusCode': 200, 'alerts': len(alerts)}
```

---

## 📅 TIMELINE

| Week | Tasks |
|------|-------|
| **Week 1** | Looker Studio + GSC setup, weekly report |
| **Week 2** | Lambda alert system, EventBridge schedule |
| **Week 3** | Bird CLI integration, social monitoring |
| **Week 4** | Refinement, documentation, training |

---

## 💰 TOTAL COST: $0

| Component | Cost |
|-----------|------|
| Looker Studio | FREE |
| Google Search Console | FREE |
| EventBridge | FREE |
| Lambda | FREE tier |
| SES | FREE tier |
| Bird CLI | FREE |
| HubSpot AI Grader | FREE |
| **TOTAL** | **$0** |

---

*Revised Plan v2 - February 1, 2026*
*ZOE STUDIO LLC*
