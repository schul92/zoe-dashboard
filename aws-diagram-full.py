#!/usr/bin/env python3
"""
AWS Infrastructure Diagram - Full Architecture
All components with proper flows
"""

import boto3
import os
from datetime import datetime

os.chdir('/home/ubuntu/.openclaw/workspace/dashboard')

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.security import SecretsManager
from diagrams.aws.integration import Eventbridge
from diagrams.aws.management import Cloudwatch
from diagrams.aws.general import Users
from diagrams.onprem.client import User
from diagrams.saas.social import Twitter
from diagrams.programming.framework import React
from diagrams.generic.blank import Blank

def generate_diagram():
    """Generate full AWS diagram with all components"""
    
    with Diagram(
        "",
        filename="aws-architecture",
        outformat="png",
        show=False,
        direction="LR",
        graph_attr={
            "dpi": "120",
            "pad": "0.5",
            "nodesep": "0.3",
            "ranksep": "0.8",
            "fontsize": "10",
            "bgcolor": "white",
            "splines": "ortho",
        },
        node_attr={
            "fontsize": "8",
            "width": "1.0",
            "height": "1.0",
        },
    ):
        # ============ LEFT SIDE: Triggers ============
        with Cluster("Triggers", graph_attr={"fontsize": "9", "bgcolor": "#FFF8E1"}):
            telegram_users = Users("Telegram\nUsers")
            
            with Cluster("EventBridge Schedules", graph_attr={"fontsize": "8", "bgcolor": "#FFECB3"}):
                eb_kona_morning = Eventbridge("KonaLate\nMorning")
                eb_kona_afternoon = Eventbridge("KonaLate\nAfternoon")
                eb_bluesky_morning = Eventbridge("Bluesky\nMorning")
                eb_bluesky_afternoon = Eventbridge("Bluesky\nAfternoon")
                eb_social = Eventbridge("kona-social\nschedule")
        
        # ============ CENTER: Compute ============
        with Cluster("AWS Compute (us-east-2)", graph_attr={"fontsize": "9", "bgcolor": "#E3F2FD"}):
            
            with Cluster("Lambda Functions", graph_attr={"fontsize": "8", "bgcolor": "#BBDEFB"}):
                lambda_late = Lambda("KonaLateBot")
                lambda_bluesky = Lambda("KonaBlueskyBot")
                lambda_ec2wake = Lambda("EC2Wake\nTelegram")
            
            with Cluster("EC2 Instances", graph_attr={"fontsize": "8", "bgcolor": "#90CAF9"}):
                ec2_zoe = EC2("Zoe\nc7i-flex.large\n(OpenClaw)")
                ec2_unnamed = EC2("Unnamed\nm7i-flex.large")
        
        # ============ RIGHT TOP: Security ============
        with Cluster("Secrets Manager", graph_attr={"fontsize": "9", "bgcolor": "#FCE4EC"}):
            secret_kona = SecretsManager("kona/api-keys")
            secret_ahrefs = SecretsManager("ahrefs-api-key")
            secret_brave = SecretsManager("BraveSearchAPI")
            secret_github = SecretsManager("zoe/github")
            secret_telegram = SecretsManager("zoe/telegram")
        
        # ============ RIGHT BOTTOM: Outputs ============
        with Cluster("Social Media APIs", graph_attr={"fontsize": "9", "bgcolor": "#E8F5E9"}):
            twitter = Twitter("Twitter/X")
            bluesky = Users("Bluesky")
            instagram = Users("Instagram\nThreads")
        
        cw = Cloudwatch("CloudWatch")
        
        # ============ CONNECTIONS ============
        
        # EventBridge → Lambda (orange)
        eb_kona_morning >> Edge(color="#FF9900", style="bold") >> lambda_late
        eb_kona_afternoon >> Edge(color="#FF9900", style="bold") >> lambda_late
        eb_bluesky_morning >> Edge(color="#FF9900", style="bold") >> lambda_bluesky
        eb_bluesky_afternoon >> Edge(color="#FF9900", style="bold") >> lambda_bluesky
        eb_social >> Edge(color="#FF9900", style="bold") >> lambda_late
        
        # Telegram → Zoe (EC2) (blue)
        telegram_users >> Edge(color="#0088cc", style="bold", label="chat") >> ec2_zoe
        
        # Zoe → Lambda (can trigger)
        ec2_zoe >> Edge(color="#232F3E", style="dashed", label="trigger") >> lambda_ec2wake
        
        # Lambda → Secrets (red dashed)
        lambda_late >> Edge(color="#DD344C", style="dashed") >> secret_kona
        lambda_bluesky >> Edge(color="#DD344C", style="dashed") >> secret_kona
        lambda_ec2wake >> Edge(color="#DD344C", style="dashed") >> secret_kona
        
        # EC2 Zoe → its secrets
        ec2_zoe >> Edge(color="#DD344C", style="dashed") >> secret_github
        ec2_zoe >> Edge(color="#DD344C", style="dashed") >> secret_telegram
        
        # Lambda → Social Media (green)
        lambda_late >> Edge(color="#3F8624", style="bold") >> twitter
        lambda_late >> Edge(color="#3F8624", style="bold") >> instagram
        lambda_bluesky >> Edge(color="#3F8624", style="bold") >> bluesky
        
        # EC2Wake → EC2
        lambda_ec2wake >> Edge(color="#FF5722", label="wake") >> ec2_unnamed
        lambda_ec2wake >> Edge(color="#FF5722", label="wake") >> ec2_zoe
        
        # All → CloudWatch (purple dotted)
        lambda_late >> Edge(color="#7B68EE", style="dotted") >> cw
        lambda_bluesky >> Edge(color="#7B68EE", style="dotted") >> cw
        lambda_ec2wake >> Edge(color="#7B68EE", style="dotted") >> cw

def generate_html():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M UTC')
    
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>ZOE STUDIO AWS Architecture</title>
    <meta http-equiv="refresh" content="300">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, sans-serif; background: #0d1117; color: #c9d1d9; min-height: 100vh; }}
        .header {{ background: #161b22; padding: 16px 24px; border-bottom: 1px solid #30363d; display: flex; justify-content: space-between; align-items: center; }}
        .logo {{ font-size: 18px; font-weight: 600; color: #f0f6fc; }}
        .logo span {{ color: #FF9900; }}
        .meta {{ font-size: 12px; color: #8b949e; }}
        .main {{ max-width: 1400px; margin: 24px auto; padding: 0 24px; }}
        .stats {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; margin-bottom: 24px; }}
        .stat {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 14px; text-align: center; }}
        .stat-value {{ font-size: 24px; font-weight: 700; color: #FF9900; }}
        .stat-label {{ font-size: 10px; color: #8b949e; margin-top: 4px; }}
        .diagram {{ background: #fff; border-radius: 8px; padding: 20px; text-align: center; overflow-x: auto; }}
        .diagram img {{ max-width: 100%; height: auto; }}
        .legend {{ display: flex; gap: 20px; justify-content: center; margin-top: 16px; font-size: 11px; color: #8b949e; flex-wrap: wrap; }}
        .legend span {{ display: flex; align-items: center; gap: 6px; }}
        .dot {{ width: 16px; height: 3px; border-radius: 2px; }}
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">🎯 <span>ZOE STUDIO</span> AWS Architecture</div>
        <div class="meta">{timestamp} • us-east-2</div>
    </div>
    <div class="main">
        <div class="stats">
            <div class="stat"><div class="stat-value">5</div><div class="stat-label">EventBridge Rules</div></div>
            <div class="stat"><div class="stat-value">3</div><div class="stat-label">Lambda Functions</div></div>
            <div class="stat"><div class="stat-value">2</div><div class="stat-label">EC2 Instances</div></div>
            <div class="stat"><div class="stat-value">5</div><div class="stat-label">Secrets</div></div>
            <div class="stat"><div class="stat-value">3</div><div class="stat-label">Social APIs</div></div>
        </div>
        <div class="diagram">
            <img src="aws-architecture.png?t={int(datetime.now().timestamp())}" alt="AWS Architecture">
        </div>
        <div class="legend">
            <span><div class="dot" style="background:#FF9900"></div> EventBridge → Lambda</span>
            <span><div class="dot" style="background:#0088cc"></div> Telegram → Zoe</span>
            <span><div class="dot" style="background:#DD344C"></div> → Secrets</span>
            <span><div class="dot" style="background:#3F8624"></div> → Social APIs</span>
            <span><div class="dot" style="background:#FF5722"></div> EC2 Wake</span>
            <span><div class="dot" style="background:#7B68EE"></div> → CloudWatch</span>
        </div>
    </div>
</body>
</html>'''
    
    with open('index.html', 'w') as f:
        f.write(html)

def main():
    print("📊 Generating full architecture diagram...")
    generate_diagram()
    print("🌐 Updating dashboard...")
    generate_html()
    print("✅ Done!")

if __name__ == '__main__':
    main()
