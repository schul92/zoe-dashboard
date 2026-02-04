#!/usr/bin/env python3
"""
ZOE STUDIO Universal Lambda Marketing Workflow
Shows the new scalable Universal Lambda architecture
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
from diagrams.onprem.client import Users as LocalUsers

def generate_universal_workflow():
    """Generate Universal Lambda workflow diagram"""
    
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
        "Universal Lambda Marketing Automation",
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
            zoe_ec2 = EC2("Zoe\n(Assistant)")
        
        # Scheduling Layer
        with Cluster("⏰ Scheduling Layer"):
            universal_schedule = Eventbridge("ZoeUniversal\nKonaCoffee\nDaily\n18:00 UTC")
            idle_check = Eventbridge("ZoeIdleCheck\n20min intervals")
            old_schedule = Eventbridge("KonaLate\nMorning\n⏸️ DISABLED")
            deleted_bluesky = Eventbridge("KonaBluesky\nMorning\n🗑️ DELETED")
        
        # Universal Lambda Core
        with Cluster("🚀 Universal Architecture"):
            universal_lambda = Lambda("ZoeUniversalPoster\n🎯 Multi-Business\nALL 5 Platforms\nPython 3.12")
            business_config = Blank("Business Config\n{\n  'kona-coffee': {...},\n  'new-client': {...}\n}")
            
        # Specialized Lambdas
        with Cluster("📱 Specialized Functions"):
            ec2_control = Lambda("EC2WakeTelegram\nSystem Control")
            deleted_bluesky_lambda = Lambda("KonaBlueskyBot\n🗑️ DELETED")
        
        # Security Layer
        with Cluster("🔐 Secrets Management"):
            kona_secrets = SecretsManager("kona/api-keys\nLATE, Twitter, FB\nThreads, Google")
            zoe_secrets = SecretsManager("zoe/*\nBot Tokens\nGitHub PAT")
        
        # External Services
        with Cluster("🌐 External APIs"):
            late_api = Blank("LATE API\n📱 Social Posts")
            unsplash = Blank("Unsplash\n📸 Images")
            platforms = Blank("Social Platforms\n🐦 Twitter\n📘 Facebook\n🧵 Threads\n📍 Google Business\n🦋 Bluesky")
        
        # Monitoring
        with Cluster("📊 Monitoring"):
            dashboard_server = Lambda("Dashboard\nReal-time AWS\ninfrastructure")
        
        # Flow 1: Universal Lambda Automation (ALL 5 PLATFORMS)
        universal_schedule >> Edge(label="cron trigger", style="bold", color="#E74C3C") >> universal_lambda
        universal_lambda >> Edge(label="load config", style="dotted") >> business_config
        universal_lambda >> Edge(label="get secrets", color="#8E44AD") >> kona_secrets
        universal_lambda >> Edge(label="fetch image", color="#3498DB") >> unsplash
        universal_lambda >> Edge(label="post to ALL 5 platforms", style="bold", color="#27AE60") >> late_api
        late_api >> Edge(label="distribute", color="#F39C12") >> platforms
        
        # Flow 2: System Management  
        steve >> Edge(label="commands") >> ec2_control
        ec2_control >> Edge(label="wake/sleep") >> zoe_ec2
        idle_check >> Edge(label="auto-sleep", style="dotted") >> ec2_control
        
        # Flow 3: Dashboard
        zoe_ec2 >> Edge(label="live updates") >> dashboard_server
        
        # Show the architectural changes
        old_schedule >> Edge(label="replaced by", style="dashed", color="#95A5A6") >> universal_lambda
        deleted_bluesky >> Edge(label="combined into", style="dashed", color="#95A5A6") >> universal_lambda
        deleted_bluesky_lambda >> Edge(label="deleted", style="dashed", color="#E74C3C") >> universal_lambda

    print(f"✅ Generated Universal Lambda workflow diagram")

if __name__ == "__main__":
    generate_universal_workflow()