#!/usr/bin/env python3
"""
ZOE STUDIO Marketing Workflow Visualization
Beautiful, modern workflow diagram showing automation flows
"""

import boto3
import os
from datetime import datetime
from collections import defaultdict

os.chdir('/home/ubuntu/.openclaw/workspace/dashboard')

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.integration import Eventbridge
from diagrams.aws.security import SecretsManager
from diagrams.aws.compute import EC2
from diagrams.aws.general import Users
from diagrams.generic.blank import Blank
from diagrams.onprem.client import Users as LocalUsers
from diagrams.onprem.analytics import Tableau
from diagrams.custom import Custom

# Custom icon paths
ICONS_DIR = "/home/ubuntu/.openclaw/workspace/dashboard/icons"

def generate_workflow():
    """Generate beautiful marketing workflow diagram"""
    
    with Diagram(
        "",
        filename="workflow-diagram",
        outformat="png", 
        show=False,
        direction="LR",  # Left to right for workflow
        graph_attr={
            "dpi": "200",
            "pad": "1.0",
            "nodesep": "0.8",
            "ranksep": "1.5",
            "fontsize": "14",
            "fontname": "SF Pro Display",
            "bgcolor": "#f8fafc",
            "style": "rounded",
        },
        node_attr={
            "fontsize": "11",
            "fontname": "SF Pro Text",
            "width": "1.2",
            "height": "1.2",
            "style": "filled,rounded",
            "fillcolor": "#ffffff",
            "color": "#e2e8f0",
        },
        edge_attr={
            "fontsize": "10", 
            "fontname": "SF Pro Text",
            "color": "#64748b",
            "penwidth": "2",
        }
    ):
        
        # ===== TIME-BASED SCHEDULING =====
        with Cluster("🕐 Automated Scheduling", graph_attr={"bgcolor": "#fef3c7", "style": "rounded,filled", "fontcolor": "#92400e"}):
            morning_trigger = Eventbridge("Morning Trigger\n6:00 PM UTC")
            afternoon_trigger = Eventbridge("Afternoon Trigger\n2:00 AM UTC") 
            idle_monitor = Eventbridge("EC2 Monitor\nEvery Minute")
        
        # ===== CONTENT AUTOMATION =====
        with Cluster("🚀 Content Automation Engine", graph_attr={"bgcolor": "#dbeafe", "style": "rounded,filled", "fontcolor": "#1e40af"}):
            kona_late = Lambda("Kona LATE Bot\nSocial Posts")
            kona_bluesky = Lambda("Kona Bluesky Bot\nBluesky Posts")
            ec2_control = Lambda("EC2 Controller\nZoe Management")
        
        # ===== SECURE STORAGE =====
        with Cluster("🔐 API Key Vault", graph_attr={"bgcolor": "#fce7f3", "style": "rounded,filled", "fontcolor": "#be185d"}):
            secrets = SecretsManager("Secrets Manager\nTwitter, Facebook,\nBluesky, Google APIs")
        
        # ===== ZOE PLATFORM =====
        with Cluster("🎯 ZOE Marketing Platform", graph_attr={"bgcolor": "#f0fdf4", "style": "rounded,filled", "fontcolor": "#15803d"}):
            zoe_ec2 = EC2("Zoe AI Assistant\nc7i-flex.large\nOpenClaw + Claude")
            telegram = Users("Telegram Bot\nRemote Control")
        
        # ===== SOCIAL PLATFORMS =====
        with Cluster("📱 Social Media Channels", graph_attr={"bgcolor": "#fef7ff", "style": "rounded,filled", "fontcolor": "#a21caf"}):
            twitter_x = Custom("X (Twitter)\n@KonaCoffeeDonut", f"{ICONS_DIR}/x.png")
            facebook = Custom("Facebook Page\nKona Coffee #2142", f"{ICONS_DIR}/facebook.png")
            google_biz = Custom("Google Business\nLocal Listings", f"{ICONS_DIR}/google.png")
            bluesky = Custom("Bluesky\n@konacoffee.bsky", f"{ICONS_DIR}/bluesky.png")
            threads = Custom("Meta Threads\nInstagram Integration", f"{ICONS_DIR}/threads.png")
        
        # ===== CLIENTS & USERS =====
        with Cluster("👥 Stakeholders", graph_attr={"bgcolor": "#fffbeb", "style": "rounded,filled", "fontcolor": "#d97706"}):
            steve = LocalUsers("Steve\nZOE STUDIO Owner")
            kona_customers = LocalUsers("Kona Coffee\nCustomers")
            local_seo = Tableau("Local SEO\nDiscovery")
        
        # ===== WORKFLOW CONNECTIONS =====
        
        # 1. TIME TRIGGERS → AUTOMATION
        morning_trigger >> Edge(label="Daily 6PM", color="#f59e0b", style="bold") >> kona_late
        morning_trigger >> Edge(label="Daily 6PM", color="#f59e0b", style="bold") >> kona_bluesky
        
        afternoon_trigger >> Edge(label="Daily 2AM", color="#8b5cf6", style="bold") >> kona_late  
        afternoon_trigger >> Edge(label="Daily 2AM", color="#8b5cf6", style="bold") >> kona_bluesky
        
        idle_monitor >> Edge(label="Monitor", color="#10b981", style="dashed") >> ec2_control
        
        # 2. AUTOMATION → SECURITY
        kona_late >> Edge(label="API Keys", color="#ec4899", style="dashed") >> secrets
        kona_bluesky >> Edge(label="API Keys", color="#ec4899", style="dashed") >> secrets
        
        # 3. AUTOMATION → SOCIAL PLATFORMS
        kona_late >> Edge(label="Post Content", color="#3b82f6", style="bold") >> twitter_x
        kona_late >> Edge(label="Post Content", color="#3b82f6", style="bold") >> facebook
        kona_late >> Edge(label="Post Content", color="#3b82f6", style="bold") >> google_biz
        kona_late >> Edge(label="Post Content", color="#3b82f6", style="bold") >> threads
        
        kona_bluesky >> Edge(label="Post Content", color="#6366f1", style="bold") >> bluesky
        
        # 4. CONTROL FLOWS
        steve >> Edge(label="Commands", color="#ef4444", style="bold") >> telegram
        telegram >> Edge(label="Telegram API", color="#ef4444") >> zoe_ec2
        
        ec2_control >> Edge(label="Start/Stop", color="#10b981", style="dashed") >> zoe_ec2
        
        # 5. CUSTOMER DISCOVERY
        twitter_x >> Edge(label="Discovery", color="#64748b", style="dotted") >> kona_customers
        facebook >> Edge(label="Discovery", color="#64748b", style="dotted") >> kona_customers  
        google_biz >> Edge(label="Local Search", color="#64748b", style="dotted") >> local_seo
        local_seo >> Edge(label="Foot Traffic", color="#64748b", style="dotted") >> kona_customers

def generate_workflow_html():
    """Generate beautiful workflow dashboard HTML"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
    
    # Get current time info for next posts
    from datetime import timedelta
    now = datetime.utcnow()
    
    # Calculate next post times
    import calendar
    today = now.date()
    
    # Next 6 PM UTC (morning post)
    next_6pm = datetime.combine(today, datetime.min.time().replace(hour=18))
    if next_6pm <= now:
        next_6pm += timedelta(days=1)
        
    # Next 2 AM UTC (afternoon post)  
    next_2am = datetime.combine(today + timedelta(days=1), datetime.min.time().replace(hour=2))
    if next_2am <= now:
        next_2am += timedelta(days=1)
    
    next_6pm_str = next_6pm.strftime('%H:%M UTC')
    next_2am_str = next_2am.strftime('%H:%M UTC')
    
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>ZOE STUDIO Marketing Workflow</title>
    <meta http-equiv="refresh" content="300">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ 
            margin: 0; 
            padding: 0; 
            box-sizing: border-box; 
        }}
        
        body {{ 
            font-family: 'Inter', -apple-system, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #1a202c;
        }}
        
        .container {{
            max-width: 1600px;
            margin: 0 auto;
            padding: 2rem;
        }}
        
        .header {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        .title {{
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 0.5rem;
        }}
        
        .subtitle {{
            text-align: center;
            font-size: 1.2rem;
            color: #64748b;
            font-weight: 400;
            margin-bottom: 1.5rem;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #ffffff, #f8fafc);
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
            border: 1px solid #e2e8f0;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.12);
        }}
        
        .stat-value {{
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }}
        
        .stat-label {{
            font-size: 0.9rem;
            color: #64748b;
            font-weight: 500;
        }}
        
        .workflow-section {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            margin-bottom: 2rem;
        }}
        
        .workflow-title {{
            font-size: 1.5rem;
            font-weight: 600;
            color: #1a202c;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .workflow-diagram {{
            text-align: center;
            overflow-x: auto;
            padding: 1rem;
            border-radius: 12px;
            background: #ffffff;
            border: 2px solid #f1f5f9;
        }}
        
        .workflow-diagram img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            filter: drop-shadow(0 10px 30px rgba(0, 0, 0, 0.1));
        }}
        
        .schedule-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
        }}
        
        .schedule-card {{
            background: linear-gradient(135deg, #f8fafc, #ffffff);
            border-radius: 16px;
            padding: 1.5rem;
            border: 2px solid #e2e8f0;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        }}
        
        .schedule-time {{
            font-size: 1.5rem;
            font-weight: 700;
            color: #3b82f6;
            margin-bottom: 0.5rem;
        }}
        
        .schedule-desc {{
            color: #64748b;
            font-weight: 500;
            margin-bottom: 1rem;
        }}
        
        .platform-tags {{
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }}
        
        .tag {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 500;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 2rem;
            padding: 1rem;
            color: rgba(255, 255, 255, 0.8);
            font-size: 0.9rem;
            font-weight: 400;
        }}
        
        .footer a {{
            color: rgba(255, 255, 255, 0.9);
            text-decoration: none;
            font-weight: 500;
        }}
        
        .live-indicator {{
            display: inline-block;
            width: 8px;
            height: 8px;
            background: #10b981;
            border-radius: 50%;
            animation: pulse 2s infinite;
            margin-right: 0.5rem;
        }}
        
        @keyframes pulse {{
            0% {{
                box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
            }}
            70% {{
                box-shadow: 0 0 0 10px rgba(16, 185, 129, 0);
            }}
            100% {{
                box-shadow: 0 0 0 0 rgba(16, 185, 129, 0);
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="title">🎯 ZOE STUDIO</h1>
            <p class="subtitle">Marketing Automation Workflow</p>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value" style="color: #3b82f6;">4</div>
                    <div class="stat-label">Active Automations</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" style="color: #10b981;">5</div>
                    <div class="stat-label">Social Platforms</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" style="color: #f59e0b;">2x</div>
                    <div class="stat-label">Daily Posts</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" style="color: #ef4444;"><span class="live-indicator"></span>Live</div>
                    <div class="stat-label">System Status</div>
                </div>
            </div>
        </div>
        
        <div class="workflow-section">
            <h2 class="workflow-title">📊 Marketing Workflow Diagram</h2>
            <div class="workflow-diagram">
                <img src="workflow-diagram.png?t={int(datetime.now().timestamp())}" alt="Marketing Workflow">
            </div>
        </div>
        
        <div class="workflow-section">
            <h2 class="workflow-title">⏰ Automated Schedule</h2>
            <div class="schedule-grid">
                <div class="schedule-card">
                    <div class="schedule-time">6:00 PM UTC</div>
                    <div class="schedule-desc">Morning Social Blast</div>
                    <div class="platform-tags">
                        <span class="tag">Twitter/X</span>
                        <span class="tag">Facebook</span>
                        <span class="tag">Bluesky</span>
                        <span class="tag">Google Business</span>
                        <span class="tag">Threads</span>
                    </div>
                </div>
                <div class="schedule-card">
                    <div class="schedule-time">2:00 AM UTC</div>
                    <div class="schedule-desc">Afternoon Social Blast</div>
                    <div class="platform-tags">
                        <span class="tag">Twitter/X</span>
                        <span class="tag">Facebook</span>
                        <span class="tag">Bluesky</span>
                        <span class="tag">Google Business</span>
                        <span class="tag">Threads</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <p>Last updated: {timestamp} • Next posts: {next_6pm_str} & {next_2am_str}</p>
        <p>Powered by <a href="https://openclaw.ai">OpenClaw</a> + AWS + ZOE STUDIO AI</p>
    </div>
</body>
</html>'''
    
    with open('workflow.html', 'w') as f:
        f.write(html)

def main():
    print("🎨 Generating beautiful workflow diagram...")
    generate_workflow()
    
    print("🌐 Creating stunning workflow dashboard...")
    generate_workflow_html()
    
    print("✅ Workflow visualization complete!")

if __name__ == '__main__':
    main()