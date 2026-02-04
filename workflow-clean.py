#!/usr/bin/env python3
"""
ZOE STUDIO Clean Active Workflow - ONLY ACTIVE COMPONENTS
No deleted components, only what's currently running
"""

import os
from datetime import datetime

os.chdir('/home/ubuntu/.openclaw/workspace/dashboard')

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.integration import Eventbridge
from diagrams.aws.security import SecretsManager
from diagrams.aws.compute import EC2
from diagrams.aws.general import Users
from diagrams.generic.blank import Blank

def generate_clean_workflow():
    """Generate clean workflow showing ONLY active components"""
    
    graph_attr = {
        "fontsize": "24",
        "fontname": "Helvetica Bold",
        "bgcolor": "transparent",
        "rankdir": "TB",
        "splines": "curved",
        "overlap": "false",
        "layout": "dot"
    }
    
    node_attr = {
        "fontsize": "14",
        "fontname": "Helvetica",
        "style": "rounded,filled",
        "margin": "0.2,0.1"
    }
    
    edge_attr = {
        "fontsize": "12",
        "fontname": "Helvetica",
        "color": "#2E86AB",
        "penwidth": "2"
    }

    with Diagram(
        "Active ZOE Marketing Automation",
        filename="workflow-diagram",
        show=False,
        graph_attr=graph_attr,
        node_attr=node_attr,
        edge_attr=edge_attr,
        direction="TB"
    ):
        
        # User/Admin
        with Cluster("👥 Control Center"):
            steve = Users("Steve\n(Admin)")
            zoe_ec2 = EC2("Zoe\n(c7i-flex.large)")
        
        # ACTIVE Scheduling Layer
        with Cluster("⏰ Active Scheduling"):
            universal_schedule = Eventbridge("ZoeUniversal\nKonaCoffee\nDaily 18:00 UTC")
            seo_schedule = Eventbridge("ZoeSEO\nKonaCoffee\nDaily 06:00 UTC")
            idle_check = Eventbridge("ZoeIdleCheck\nEvery 1 minute")
        
        # ACTIVE Lambda Functions
        with Cluster("⚡ Lambda Functions"):
            universal_lambda = Lambda("ZoeUniversalPoster\n5 Platforms\nPython 3.12")
            seo_lambda = Lambda("ZoeSEOMonitor\nSEO Analytics")
            ec2_control = Lambda("EC2WakeTelegram\nSystem Control")
            ec2_backup = Lambda("ZoeEC2Control\nBackup Control")
        
        # Active Security
        with Cluster("🔐 Secrets Manager"):
            kona_secrets = SecretsManager("kona/api-keys\nLATE, Social APIs")
            zoe_secrets = SecretsManager("zoe/*\nBot Tokens")
            other_secrets = SecretsManager("Other Secrets\n4 more")
        
        # Active External Services
        with Cluster("🌐 External APIs"):
            late_api = Blank("LATE API\n5 Platforms")
            unsplash = Blank("Unsplash\nImages")
            social_platforms = Blank("Social Media\n🐦 Twitter\n📘 Facebook\n🧵 Threads\n📍 Google\n🦋 Bluesky")
        
        # ACTIVE FLOWS ONLY
        
        # Flow 1: Universal Social Media Automation
        universal_schedule >> Edge(label="daily trigger", style="bold", color="#E74C3C") >> universal_lambda
        universal_lambda >> Edge(label="get secrets", color="#8E44AD") >> kona_secrets
        universal_lambda >> Edge(label="fetch image", color="#3498DB") >> unsplash
        universal_lambda >> Edge(label="post to 5 platforms", style="bold", color="#27AE60") >> late_api
        late_api >> Edge(label="distribute", color="#F39C12") >> social_platforms
        
        # Flow 2: SEO Monitoring
        seo_schedule >> Edge(label="daily scan", color="#17A2B8") >> seo_lambda
        seo_lambda >> Edge(label="analytics") >> kona_secrets
        
        # Flow 3: System Management  
        steve >> Edge(label="telegram commands") >> ec2_control
        ec2_control >> Edge(label="wake/sleep") >> zoe_ec2
        idle_check >> Edge(label="auto-sleep check", style="dotted") >> ec2_control
        
        # Flow 4: Backup System
        steve >> Edge(label="backup control", style="dashed") >> ec2_backup
        
        # Flow 5: Dashboard Updates
        zoe_ec2 >> Edge(label="live monitoring", style="dotted", color="#6C757D") >> universal_lambda

    print(f"✅ Generated clean active workflow diagram")

if __name__ == "__main__":
    generate_clean_workflow()