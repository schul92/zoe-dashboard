#!/usr/bin/env python3
"""
AWS Infrastructure Diagram - Compact Edition
Clean, readable, fits on screen
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

def get_aws_resources():
    resources = {'ec2': [], 'lambda': [], 'secrets': [], 'eventbridge': [], 'region': 'us-east-2'}
    region = 'us-east-2'
    
    try:
        ec2 = boto3.client('ec2', region_name=region)
        for res in ec2.describe_instances()['Reservations']:
            for inst in res['Instances']:
                name = next((t['Value'] for t in inst.get('Tags', []) if t['Key'] == 'Name'), 'Unnamed')
                resources['ec2'].append({'name': name, 'state': inst['State']['Name']})
    except: pass
    
    try:
        lam = boto3.client('lambda', region_name=region)
        for fn in lam.list_functions()['Functions']:
            resources['lambda'].append({'name': fn['FunctionName']})
    except: pass
    
    try:
        sm = boto3.client('secretsmanager', region_name=region)
        for s in sm.list_secrets()['SecretList']:
            resources['secrets'].append({'name': s['Name']})
    except: pass
    
    try:
        events = boto3.client('events', region_name=region)
        for rule in events.list_rules()['Rules']:
            resources['eventbridge'].append({'name': rule['Name']})
    except: pass
    
    return resources

def generate_diagram(resources):
    """Generate compact AWS diagram"""
    
    with Diagram(
        "",
        filename="aws-architecture",
        outformat="png",
        show=False,
        direction="LR",
        graph_attr={
            "dpi": "150",
            "pad": "0.3",
            "nodesep": "0.4",
            "ranksep": "0.6",
            "fontsize": "11",
            "bgcolor": "white",
        },
        node_attr={
            "fontsize": "9",
            "width": "1.2",
            "height": "1.2",
        },
    ):
        # Left: Triggers
        users = Users("Telegram")
        scheduler = Eventbridge("Scheduler")
        
        # Center: Lambda
        with Cluster("Lambda", graph_attr={"fontsize": "10"}):
            l1 = Lambda("KonaLateBot")
            l2 = Lambda("BlueskyBot")
            l3 = Lambda("EC2Wake")
        
        # Right: Resources
        with Cluster("Resources", graph_attr={"fontsize": "10"}):
            secrets = SecretsManager("Secrets")
            ec2 = EC2("EC2")
            cw = Cloudwatch("Logs")
        
        # Connections
        scheduler >> Edge(color="#FF9900") >> l1
        scheduler >> Edge(color="#FF9900") >> l2
        users >> Edge(color="#232F3E") >> l3
        
        l1 >> Edge(color="#DD344C", style="dashed") >> secrets
        l2 >> Edge(color="#DD344C", style="dashed") >> secrets
        l3 >> Edge(color="#3F8624") >> ec2
        
        [l1, l2, l3] >> Edge(color="#7B68EE", style="dotted") >> cw

def generate_html(resources):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M UTC')
    
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>ZOE STUDIO AWS</title>
    <meta http-equiv="refresh" content="300">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, sans-serif; background: #0d1117; color: #c9d1d9; min-height: 100vh; }}
        .header {{ background: #161b22; padding: 16px 24px; border-bottom: 1px solid #30363d; display: flex; justify-content: space-between; align-items: center; }}
        .logo {{ font-size: 18px; font-weight: 600; color: #f0f6fc; }}
        .logo span {{ color: #FF9900; }}
        .meta {{ font-size: 12px; color: #8b949e; }}
        .main {{ max-width: 1000px; margin: 24px auto; padding: 0 24px; }}
        .stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 24px; }}
        .stat {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 16px; text-align: center; }}
        .stat-value {{ font-size: 28px; font-weight: 700; color: #FF9900; }}
        .stat-label {{ font-size: 11px; color: #8b949e; margin-top: 4px; }}
        .diagram {{ background: #fff; border-radius: 8px; padding: 16px; text-align: center; }}
        .diagram img {{ max-width: 100%; height: auto; max-height: 500px; }}
        .legend {{ display: flex; gap: 16px; justify-content: center; margin-top: 16px; font-size: 11px; color: #8b949e; }}
        .legend span {{ display: flex; align-items: center; gap: 6px; }}
        .dot {{ width: 12px; height: 3px; border-radius: 2px; }}
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">🎯 <span>ZOE STUDIO</span> AWS</div>
        <div class="meta">{timestamp} • us-east-2</div>
    </div>
    <div class="main">
        <div class="stats">
            <div class="stat"><div class="stat-value">{len(resources['lambda'])}</div><div class="stat-label">Lambda</div></div>
            <div class="stat"><div class="stat-value">{len(resources['ec2'])}</div><div class="stat-label">EC2</div></div>
            <div class="stat"><div class="stat-value">{len(resources['secrets'])}</div><div class="stat-label">Secrets</div></div>
            <div class="stat"><div class="stat-value">{len(resources['eventbridge'])}</div><div class="stat-label">Rules</div></div>
        </div>
        <div class="diagram">
            <img src="aws-architecture.png?t={int(datetime.now().timestamp())}" alt="AWS">
        </div>
        <div class="legend">
            <span><div class="dot" style="background:#FF9900"></div> Schedule</span>
            <span><div class="dot" style="background:#DD344C"></div> Secrets</span>
            <span><div class="dot" style="background:#3F8624"></div> EC2</span>
            <span><div class="dot" style="background:#7B68EE"></div> Logs</span>
        </div>
    </div>
</body>
</html>'''
    
    with open('index.html', 'w') as f:
        f.write(html)

def main():
    print("🔍 Fetching...")
    resources = get_aws_resources()
    print("📊 Generating compact diagram...")
    generate_diagram(resources)
    print("🌐 Updating dashboard...")
    generate_html(resources)
    print("✅ Done!")

if __name__ == '__main__':
    main()
