#!/usr/bin/env python3
"""
ZOE STUDIO Workflow with Proper Social Media Icons
Using custom branded icons for social platforms
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
from diagrams.custom import Custom

def generate_branded_workflow():
    """Generate workflow with proper social media icons"""
    
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
        "ZOE Marketing Automation Flow",
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
        
        # External APIs
        with Cluster("🌐 External APIs"):
            late_api = Blank("LATE API\nUnified Posting")
            unsplash = Blank("Unsplash\nImage Search")
        
        # Social Media Platforms with Custom Icons
        with Cluster("📱 Social Media Platforms"):
            try:
                twitter = Custom("Twitter/X", "./icons/x.png")
            except:
                twitter = Blank("Twitter/X")
            
            try:
                facebook = Custom("Facebook", "./icons/facebook.png") 
            except:
                facebook = Blank("Facebook")
                
            try:
                threads = Custom("Threads", "./icons/threads.png")
            except:
                threads = Blank("Threads")
                
            try:
                google = Custom("Google Business", "./icons/google.png")
            except:
                google = Blank("Google Business")
                
            try:
                bluesky = Custom("Bluesky", "./icons/bluesky.png")
            except:
                bluesky = Blank("Bluesky")
        
        # ACTIVE FLOWS ONLY
        
        # Flow 1: Universal Social Media Automation
        universal_schedule >> Edge(label="daily trigger", style="bold", color="#E74C3C") >> universal_lambda
        universal_lambda >> Edge(label="get secrets", color="#8E44AD") >> kona_secrets
        universal_lambda >> Edge(label="fetch image", color="#3498DB") >> unsplash
        universal_lambda >> Edge(label="post via LATE", style="bold", color="#27AE60") >> late_api
        
        # Individual platform flows
        late_api >> Edge(label="distribute", color="#1DA1F2") >> twitter
        late_api >> Edge(label="distribute", color="#1877F2") >> facebook  
        late_api >> Edge(label="distribute", color="#000000") >> threads
        late_api >> Edge(label="distribute", color="#4285F4") >> google
        late_api >> Edge(label="distribute", color="#00A8E6") >> bluesky
        
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

    print(f"✅ Generated workflow with branded social media icons")

if __name__ == "__main__":
    generate_branded_workflow()