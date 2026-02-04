# 🎯 ZOE STUDIO Dashboard

> **Modern AI-powered business intelligence dashboard**  
> Monitoring SEO, Social Media, and Infrastructure in real-time

[![Live Demo](https://img.shields.io/badge/demo-live-success)](https://schul92.github.io/zoe-dashboard/)
[![GitHub Pages](https://img.shields.io/badge/deploy-GitHub%20Pages-blue)](https://pages.github.com/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## ✨ Features

### 📊 **SEO Analytics**
- Google Search Console integration
- Google Analytics 4 metrics
- Real-time performance tracking
- Keyword rankings

### 📱 **Social Media Dashboard** (Coming Soon)
- 5-platform posting automation
- Twitter, Facebook, Google Business, Threads, Bluesky
- Engagement tracking
- Content calendar

### 🏗️ **Infrastructure Monitoring**
- AWS architecture visualization
- Zoe AI agent status
- Cost tracking
- Workflow automation

---

## 🚀 Live Demo

**Visit:** [https://schul92.github.io/zoe-dashboard/](https://schul92.github.io/zoe-dashboard/)

### Navigation:
- **Hub:** `/hub.html` - Main dashboard
- **SEO:** `/seo/` - SEO analytics
- **AWS:** `/aws.html` - Infrastructure
- **Workflow:** `/workflow.html` - Automation

---

## 🛠️ Tech Stack

- **Frontend:** HTML5, CSS3, JavaScript
- **Styling:** Tailwind CSS, Custom Glass Morphism
- **Icons:** Font Awesome
- **Visualization:** Python diagrams
- **Deployment:** GitHub Pages (free!)

---

## 📦 Local Development

### Prerequisites
- Python 3.9+
- AWS CLI configured
- Google Cloud credentials

### Setup
```bash
# Clone the repo
git clone https://github.com/schul92/zoe-dashboard.git
cd zoe-dashboard

# Generate diagrams
python3 aws-diagram.py
python3 workflow-diagram.py

# Serve locally
python3 -m http.server 8088
# Visit: http://localhost:8088/hub.html
```

---

## 🔄 Auto-Update

Dashboard data refreshes automatically:
- **SEO data:** Every 30 minutes
- **AWS architecture:** Every 5 minutes
- **Workflow status:** Real-time

Powered by **Zoe AI Agent** (OpenClaw) running on Mac mini.

---

## 📁 Project Structure

```
zoe-dashboard/
├── hub.html              # Main dashboard hub
├── seo/                  # SEO analytics
│   └── index.html
├── aws.html              # AWS infrastructure
├── workflow.html         # Workflow automation
├── icons/                # SVG icons
├── *.py                  # Python diagram generators
└── *.png                 # Generated diagrams
```

---

## 🎨 Design Philosophy

- **Dark Mode First:** Easy on the eyes
- **Glass Morphism:** Modern, premium feel
- **Real-time Updates:** Always current
- **Mobile Responsive:** Works everywhere

---

## 🤝 Contributing

This is a private business dashboard for ZOE STUDIO clients.  
For inquiries: info@konacoffeedonut.com

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details

---

## 🙏 Acknowledgments

- **Powered by:** [OpenClaw](https://openclaw.ai) AI Agent Framework
- **Zoe AI Agent:** Primary automation & monitoring
- **Deployed on:** GitHub Pages (free!)

---

**Built with ❤️ by Zoe AI for ZOE STUDIO**

_Last updated: 2026-02-04_
