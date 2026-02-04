#!/usr/bin/env python3
"""
AWS Infrastructure Diagram Generator - Professional Edition
Follows AWS Architecture Center best practices
"""

import boto3
import os
from datetime import datetime

os.chdir('/home/ubuntu/.openclaw/workspace/dashboard')

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.security import SecretsManager, IAM
from diagrams.aws.integration import Eventbridge
from diagrams.aws.management import Cloudwatch
from diagrams.aws.general import Users
from diagrams.aws.network import APIGateway

def get_aws_resources():
    """Fetch AWS resources"""
    resources = {'ec2': [], 'lambda': [], 'secrets': [], 'eventbridge': [], 'region': 'us-east-2'}
    region = 'us-east-2'
    
    try:
        ec2 = boto3.client('ec2', region_name=region)
        for res in ec2.describe_instances()['Reservations']:
            for inst in res['Instances']:
                name = next((t['Value'] for t in inst.get('Tags', []) if t['Key'] == 'Name'), 'Unnamed')
                resources['ec2'].append({'id': inst['InstanceId'], 'name': name, 'state': inst['State']['Name'], 'type': inst['InstanceType']})
    except: pass
    
    try:
        lam = boto3.client('lambda', region_name=region)
        for fn in lam.list_functions()['Functions']:
            resources['lambda'].append({'name': fn['FunctionName'], 'runtime': fn['Runtime']})
    except: pass
    
    try:
        sm = boto3.client('secretsmanager', region_name=region)
        for s in sm.list_secrets()['SecretList']:
            resources['secrets'].append({'name': s['Name']})
    except: pass
    
    try:
        events = boto3.client('events', region_name=region)
        for rule in events.list_rules()['Rules']:
            targets = events.list_targets_by_rule(Rule=rule['Name']).get('Targets', [])
            resources['eventbridge'].append({
                'name': rule['Name'],
                'schedule': rule.get('ScheduleExpression', ''),
                'targets': [t.get('Arn', '').split(':function:')[-1] for t in targets if 'function' in t.get('Arn', '')]
            })
    except: pass
    
    return resources

def generate_diagram(resources):
    """Generate clean AWS diagram following best practices"""
    
    # Graph attributes for clean professional look
    graph_attr = {
        "fontsize": "14",
        "fontname": "Amazon Ember, Helvetica, Arial, sans-serif",
        "bgcolor": "white",
        "pad": "1.0",
        "splines": "ortho",  # Orthogonal routing like AWS diagrams
        "nodesep": "1.0",
        "ranksep": "1.5",
        "compound": "true",
    }
    
    node_attr = {
        "fontsize": "11",
        "fontname": "Amazon Ember, Helvetica, Arial, sans-serif",
    }
    
    edge_attr = {
        "fontsize": "10",
        "fontname": "Amazon Ember, Helvetica, Arial, sans-serif",
    }

    with Diagram(
        "",  # No title in diagram, we add it in HTML
        filename="aws-architecture",
        outformat="png",
        show=False,
        direction="LR",  # Left to right - standard AWS layout
        graph_attr=graph_attr,
        node_attr=node_attr,
        edge_attr=edge_attr,
    ):
        
        # External triggers (left side)
        users = Users("Telegram\nUsers")
        
        with Cluster("AWS Cloud - us-east-2", graph_attr={"bgcolor": "#F5F5F5", "style": "rounded"}):
            
            # Scheduling tier
            with Cluster("Scheduling", graph_attr={"bgcolor": "#FFF3E0"}):
                schedules = Eventbridge("EventBridge\nScheduler")
            
            # Compute tier
            with Cluster("Compute", graph_attr={"bgcolor": "#E3F2FD"}):
                lambda_kona_late = Lambda("KonaLateBot")
                lambda_bluesky = Lambda("KonaBlueskyBot")  
                lambda_ec2wake = Lambda("EC2WakeTelegram")
                
            # Infrastructure
            with Cluster("Infrastructure", graph_attr={"bgcolor": "#E8F5E9"}):
                ec2_nodes = []
                for inst in resources['ec2']:
                    label = f"{inst['name']}\n{inst['type']}"
                    ec2_nodes.append(EC2(label))
            
            # Security tier  
            with Cluster("Security", graph_attr={"bgcolor": "#FCE4EC"}):
                secrets = SecretsManager("Secrets\nManager")
                iam = IAM("IAM Roles")
            
            # Monitoring
            cw = Cloudwatch("CloudWatch")
        
        # Social media outputs (right side)
        api = APIGateway("Social Media\nAPIs")
        
        # Connections - Clean routing
        # Schedule triggers
        schedules >> Edge(color="#FF9900", style="bold") >> lambda_kona_late
        schedules >> Edge(color="#FF9900", style="bold") >> lambda_bluesky
        
        # User triggers
        users >> Edge(color="#232F3E") >> lambda_ec2wake
        
        # Lambda to EC2
        if ec2_nodes:
            lambda_ec2wake >> Edge(color="#3F8624", label="start/stop") >> ec2_nodes[0]
        
        # Lambda to Secrets
        lambda_kona_late >> Edge(color="#DD344C", style="dashed") >> secrets
        lambda_bluesky >> Edge(color="#DD344C", style="dashed") >> secrets
        lambda_ec2wake >> Edge(color="#DD344C", style="dashed") >> secrets
        
        # Lambda to external
        lambda_kona_late >> Edge(color="#232F3E") >> api
        lambda_bluesky >> Edge(color="#232F3E") >> api
        
        # Logging
        lambda_kona_late >> Edge(color="#7B68EE", style="dotted") >> cw
        lambda_bluesky >> Edge(color="#7B68EE", style="dotted") >> cw
        lambda_ec2wake >> Edge(color="#7B68EE", style="dotted") >> cw

def generate_html(resources):
    """Generate clean HTML dashboard"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZOE STUDIO - AWS Architecture</title>
    <meta http-equiv="refresh" content="300">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #0d1117;
            min-height: 100vh;
            color: #c9d1d9;
        }}
        .header {{
            background: linear-gradient(135deg, #161b22 0%, #0d1117 100%);
            border-bottom: 1px solid #30363d;
            padding: 24px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .logo {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        .logo-icon {{
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, #FF9900 0%, #FF6600 100%);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
        }}
        .logo-text {{
            font-size: 20px;
            font-weight: 600;
            color: #f0f6fc;
        }}
        .logo-text span {{
            color: #FF9900;
        }}
        .meta {{
            text-align: right;
            font-size: 13px;
            color: #8b949e;
        }}
        .main {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 40px;
        }}
        .title {{
            font-size: 28px;
            font-weight: 600;
            color: #f0f6fc;
            margin-bottom: 8px;
        }}
        .subtitle {{
            color: #8b949e;
            margin-bottom: 32px;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-bottom: 32px;
        }}
        .stat {{
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
        }}
        .stat-value {{
            font-size: 32px;
            font-weight: 700;
            color: #FF9900;
        }}
        .stat-label {{
            font-size: 13px;
            color: #8b949e;
            margin-top: 4px;
        }}
        .diagram-container {{
            background: #ffffff;
            border-radius: 12px;
            padding: 32px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        }}
        .diagram-container img {{
            width: 100%;
            height: auto;
        }}
        .legend {{
            display: flex;
            gap: 24px;
            justify-content: center;
            margin-top: 24px;
            flex-wrap: wrap;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 13px;
            color: #8b949e;
        }}
        .legend-line {{
            width: 24px;
            height: 3px;
            border-radius: 2px;
        }}
        .orange {{ background: #FF9900; }}
        .red {{ background: #DD344C; }}
        .purple {{ background: #7B68EE; }}
        .green {{ background: #3F8624; }}
        .refresh {{
            background: #238636;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-weight: 500;
            cursor: pointer;
            text-decoration: none;
            font-size: 14px;
        }}
        .refresh:hover {{ background: #2ea043; }}
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">
            <div class="logo-icon">🎯</div>
            <div class="logo-text"><span>ZOE STUDIO</span> Infrastructure</div>
        </div>
        <div class="meta">
            <div>Last updated: {timestamp}</div>
            <div>Region: us-east-2</div>
        </div>
    </div>
    
    <div class="main">
        <h1 class="title">AWS Architecture Overview</h1>
        <p class="subtitle">Live infrastructure diagram • Auto-refreshes every 5 minutes</p>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-value">{len(resources['lambda'])}</div>
                <div class="stat-label">Lambda Functions</div>
            </div>
            <div class="stat">
                <div class="stat-value">{len(resources['ec2'])}</div>
                <div class="stat-label">EC2 Instances</div>
            </div>
            <div class="stat">
                <div class="stat-value">{len(resources['secrets'])}</div>
                <div class="stat-label">Secrets</div>
            </div>
            <div class="stat">
                <div class="stat-value">{len(resources['eventbridge'])}</div>
                <div class="stat-label">Scheduled Rules</div>
            </div>
        </div>
        
        <div class="diagram-container">
            <img src="aws-architecture.png?t={int(datetime.now().timestamp())}" alt="AWS Architecture">
        </div>
        
        <div class="legend">
            <div class="legend-item">
                <div class="legend-line orange"></div>
                <span>EventBridge → Lambda</span>
            </div>
            <div class="legend-item">
                <div class="legend-line red"></div>
                <span>Secrets Access</span>
            </div>
            <div class="legend-item">
                <div class="legend-line purple"></div>
                <span>CloudWatch Logs</span>
            </div>
            <div class="legend-item">
                <div class="legend-line green"></div>
                <span>EC2 Control</span>
            </div>
        </div>
    </div>
</body>
</html>'''
    
    with open('index.html', 'w') as f:
        f.write(html)

def main():
    print("🔍 Fetching AWS resources...")
    resources = get_aws_resources()
    print(f"   {len(resources['lambda'])} Lambda, {len(resources['ec2'])} EC2, {len(resources['secrets'])} Secrets, {len(resources['eventbridge'])} EventBridge")
    
    print("📊 Generating professional diagram...")
    generate_diagram(resources)
    
    print("🌐 Generating dashboard...")
    generate_html(resources)
    
    print("✅ Done!")

if __name__ == '__main__':
    main()
