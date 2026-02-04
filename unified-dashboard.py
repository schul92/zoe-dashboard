#!/usr/bin/env python3
"""
ZOE STUDIO Unified Dashboard
Scalable multi-client marketing & infrastructure dashboard
"""

import boto3
import json
import os
from datetime import datetime, timezone

os.chdir('/home/ubuntu/.openclaw/workspace/dashboard')

REGION = 'us-east-2'

# Client configurations
CLIENTS = [
    {
        "name": "Kona Coffee Donut",
        "slug": "kona-coffee",
        "logo": "☕",
        "location": "Waikiki, HI",
        "status": "pre-launch",
        "openingDate": "Feb 2026",
        "platforms": ["Twitter", "Facebook", "Threads", "Google", "Bluesky"],
        "schedule": "Daily 8AM HST",
        "color": "#8B4513",
        "lambda": "ZoeUniversalPoster",
        "eventbridge": "ZoeUniversal-KonaCoffee-Daily"
    }
    # Add more clients here - just add to this list and create EventBridge rule
]

def fetch_aws_resources():
    """Fetch current AWS resources"""
    resources = {"ec2": [], "lambda": [], "secrets": [], "eventbridge": []}
    
    try:
        ec2 = boto3.client('ec2', region_name=REGION)
        for res in ec2.describe_instances()['Reservations']:
            for inst in res['Instances']:
                if inst['State']['Name'] == 'terminated':
                    continue
                name = next((t['Value'] for t in inst.get('Tags', []) if t['Key'] == 'Name'), inst['InstanceId'][:12])
                resources['ec2'].append({
                    'name': name,
                    'type': inst['InstanceType'],
                    'state': inst['State']['Name']
                })
    except: pass
    
    try:
        lam = boto3.client('lambda', region_name=REGION)
        for fn in lam.list_functions()['Functions']:
            resources['lambda'].append({'name': fn['FunctionName']})
    except: pass
    
    try:
        sm = boto3.client('secretsmanager', region_name=REGION)
        for secret in sm.list_secrets()['SecretList']:
            resources['secrets'].append({'name': secret['Name']})
    except: pass
    
    try:
        events = boto3.client('events', region_name=REGION)
        for rule in events.list_rules()['Rules']:
            resources['eventbridge'].append({
                'name': rule['Name'],
                'schedule': rule.get('ScheduleExpression', 'event'),
                'state': rule['State']
            })
    except: pass
    
    return resources

def generate_unified_dashboard():
    """Generate the unified dashboard HTML"""
    
    resources = fetch_aws_resources()
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    
    # Calculate stats
    total_resources = sum(len(v) for v in resources.values())
    active_clients = len(CLIENTS)
    total_platforms = sum(len(c['platforms']) for c in CLIENTS)
    
    # Generate client cards HTML
    client_cards = ""
    for client in CLIENTS:
        platforms_html = "".join([f'<span class="platform-tag">{p}</span>' for p in client['platforms']])
        status_class = "status-active" if client['status'] == 'active' else "status-prelaunche"
        
        client_cards += f'''
        <div class="client-card" style="border-left: 4px solid {client['color']}">
            <div class="client-header">
                <span class="client-logo">{client['logo']}</span>
                <div class="client-info">
                    <h3>{client['name']}</h3>
                    <span class="client-location">📍 {client['location']}</span>
                </div>
                <span class="client-status {status_class}">{client['status']}</span>
            </div>
            <div class="client-details">
                <div class="detail-row">
                    <span class="detail-label">Opening</span>
                    <span class="detail-value">{client['openingDate']}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">Schedule</span>
                    <span class="detail-value">{client['schedule']}</span>
                </div>
            </div>
            <div class="client-platforms">{platforms_html}</div>
        </div>
        '''
    
    # Generate AWS resources HTML
    aws_resources_html = ""
    
    # EC2
    for ec2 in resources['ec2']:
        state_icon = "🟢" if ec2['state'] == 'running' else "🔴"
        aws_resources_html += f'<div class="resource-item"><span class="resource-icon">💻</span><span class="resource-name">{ec2["name"]}</span><span class="resource-meta">{state_icon} {ec2["type"]}</span></div>'
    
    # Lambda
    for fn in resources['lambda']:
        aws_resources_html += f'<div class="resource-item"><span class="resource-icon">⚡</span><span class="resource-name">{fn["name"]}</span><span class="resource-meta">Lambda</span></div>'
    
    # EventBridge
    for rule in resources['eventbridge']:
        state_icon = "✅" if rule['state'] == 'ENABLED' else "⏸️"
        aws_resources_html += f'<div class="resource-item"><span class="resource-icon">⏰</span><span class="resource-name">{rule["name"]}</span><span class="resource-meta">{state_icon}</span></div>'
    
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ZOE STUDIO Dashboard</title>
    <meta http-equiv="refresh" content="300">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        :root {{
            --bg-primary: #0f0f23;
            --bg-secondary: #1a1a2e;
            --bg-card: #16213e;
            --accent: #e94560;
            --accent-secondary: #0f3460;
            --text-primary: #ffffff;
            --text-secondary: #a0a0b0;
            --success: #10b981;
            --warning: #f59e0b;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
        }}
        
        .dashboard {{
            max-width: 1600px;
            margin: 0 auto;
            padding: 2rem;
        }}
        
        /* Header */
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
            padding-bottom: 1.5rem;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        
        .logo {{
            display: flex;
            align-items: center;
            gap: 1rem;
        }}
        
        .logo-icon {{
            font-size: 2.5rem;
        }}
        
        .logo-text {{
            font-size: 1.8rem;
            font-weight: 800;
            background: linear-gradient(135deg, var(--accent), #ff6b6b);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .logo-subtitle {{
            font-size: 0.9rem;
            color: var(--text-secondary);
            font-weight: 400;
        }}
        
        .header-meta {{
            text-align: right;
            color: var(--text-secondary);
            font-size: 0.85rem;
        }}
        
        .live-indicator {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: rgba(16, 185, 129, 0.1);
            color: var(--success);
            padding: 0.4rem 0.8rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 500;
            margin-bottom: 0.5rem;
        }}
        
        .live-dot {{
            width: 8px;
            height: 8px;
            background: var(--success);
            border-radius: 50%;
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; transform: scale(1); }}
            50% {{ opacity: 0.5; transform: scale(1.2); }}
        }}
        
        /* Stats Grid */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}
        
        .stat-card {{
            background: var(--bg-card);
            border-radius: 16px;
            padding: 1.5rem;
            border: 1px solid rgba(255,255,255,0.05);
        }}
        
        .stat-value {{
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }}
        
        .stat-label {{
            color: var(--text-secondary);
            font-size: 0.9rem;
            font-weight: 500;
        }}
        
        /* Main Grid */
        .main-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
            margin-bottom: 2rem;
        }}
        
        @media (max-width: 1200px) {{
            .main-grid {{ grid-template-columns: 1fr; }}
        }}
        
        /* Section */
        .section {{
            background: var(--bg-card);
            border-radius: 16px;
            padding: 1.5rem;
            border: 1px solid rgba(255,255,255,0.05);
        }}
        
        .section-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }}
        
        .section-title {{
            font-size: 1.2rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .section-badge {{
            background: var(--accent);
            color: white;
            padding: 0.2rem 0.6rem;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
        }}
        
        /* Client Cards */
        .clients-grid {{
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }}
        
        .client-card {{
            background: var(--bg-secondary);
            border-radius: 12px;
            padding: 1.25rem;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .client-card:hover {{
            transform: translateX(5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }}
        
        .client-header {{
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1rem;
        }}
        
        .client-logo {{
            font-size: 2rem;
        }}
        
        .client-info h3 {{
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 0.2rem;
        }}
        
        .client-location {{
            font-size: 0.8rem;
            color: var(--text-secondary);
        }}
        
        .client-status {{
            margin-left: auto;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 500;
            text-transform: uppercase;
        }}
        
        .status-active {{
            background: rgba(16, 185, 129, 0.2);
            color: var(--success);
        }}
        
        .status-prelaunche {{
            background: rgba(245, 158, 11, 0.2);
            color: var(--warning);
        }}
        
        .client-details {{
            display: flex;
            gap: 2rem;
            margin-bottom: 1rem;
        }}
        
        .detail-row {{
            display: flex;
            flex-direction: column;
            gap: 0.2rem;
        }}
        
        .detail-label {{
            font-size: 0.7rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .detail-value {{
            font-size: 0.9rem;
            font-weight: 500;
        }}
        
        .client-platforms {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }}
        
        .platform-tag {{
            background: var(--accent-secondary);
            color: var(--text-primary);
            padding: 0.3rem 0.6rem;
            border-radius: 6px;
            font-size: 0.7rem;
            font-weight: 500;
        }}
        
        /* Resources */
        .resources-list {{
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
            max-height: 400px;
            overflow-y: auto;
        }}
        
        .resource-item {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.75rem;
            background: var(--bg-secondary);
            border-radius: 8px;
        }}
        
        .resource-icon {{
            font-size: 1.2rem;
        }}
        
        .resource-name {{
            flex: 1;
            font-weight: 500;
            font-size: 0.9rem;
        }}
        
        .resource-meta {{
            color: var(--text-secondary);
            font-size: 0.8rem;
        }}
        
        /* Diagrams Section */
        .diagrams-section {{
            margin-top: 2rem;
        }}
        
        .diagrams-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2rem;
        }}
        
        @media (max-width: 1200px) {{
            .diagrams-grid {{ grid-template-columns: 1fr; }}
        }}
        
        .diagram-container {{
            background: white;
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
        }}
        
        .diagram-container img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
        }}
        

        /* Mobile Responsive */
        @media (max-width: 768px) {{
            .dashboard {{ padding: 1rem; }}
            .header {{ flex-direction: column; text-align: center; gap: 1rem; }}
            .header-meta {{ text-align: center; }}
            .logo-text {{ font-size: 1.4rem; }}
            .stats-grid {{ grid-template-columns: repeat(2, 1fr); gap: 0.75rem; }}
            .stat-card {{ padding: 1rem; }}
            .stat-value {{ font-size: 1.8rem; }}
            .main-grid {{ grid-template-columns: 1fr; gap: 1rem; }}
            .section {{ padding: 1rem; }}
            .nav-tabs {{ flex-wrap: wrap; justify-content: center; }}
            .nav-tab {{ padding: 0.5rem 0.8rem; font-size: 0.8rem; }}
            .diagrams-grid {{ grid-template-columns: 1fr; gap: 1rem; }}
            .client-header {{ flex-wrap: wrap; }}
            .client-status {{ margin-left: 0; margin-top: 0.5rem; }}
            .client-details {{ flex-wrap: wrap; gap: 1rem; }}
            .platform-tag {{ font-size: 0.65rem; padding: 0.2rem 0.5rem; }}
            .resources-list {{ max-height: 300px; }}
        }}
        
        @media (max-width: 480px) {{
            .stats-grid {{ grid-template-columns: 1fr 1fr; }}
            .stat-value {{ font-size: 1.5rem; }}
            .section-title {{ font-size: 1rem; }}
        }}

        /* Footer */
        .footer {{
            text-align: center;
            margin-top: 2rem;
            padding-top: 1.5rem;
            border-top: 1px solid rgba(255,255,255,0.05);
            color: var(--text-secondary);
            font-size: 0.85rem;
        }}
        
        .footer a {{
            color: var(--accent);
            text-decoration: none;
        }}
        
        /* Nav Tabs */
        .nav-tabs {{
            display: flex;
            gap: 0.5rem;
            margin-bottom: 1.5rem;
        }}
        
        .nav-tab {{
            padding: 0.6rem 1.2rem;
            background: var(--bg-card);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 8px;
            color: var(--text-secondary);
            text-decoration: none;
            font-weight: 500;
            font-size: 0.9rem;
            transition: all 0.2s;
        }}
        
        .nav-tab:hover, .nav-tab.active {{
            background: var(--accent);
            color: white;
            border-color: var(--accent);
        }}
    </style>
</head>
<body>
    <div class="dashboard">
        <header class="header">
            <div class="logo">
                <span class="logo-icon">🎯</span>
                <div>
                    <div class="logo-text">ZOE STUDIO</div>
                    <div class="logo-subtitle">Marketing Intelligence Hub</div>
                </div>
            </div>
            <div class="header-meta">
                <div class="live-indicator">
                    <span class="live-dot"></span>
                    All Systems Operational
                </div>
                <div>Last updated: {timestamp}</div>
                <div>Region: {REGION}</div>
            </div>
        </header>
        
        <nav class="nav-tabs">
            <a href="#" class="nav-tab active">Overview</a>
            <a href="/" class="nav-tab">AWS Architecture</a>
            <a href="/workflow" class="nav-tab">Workflow</a>
        </nav>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value" style="color: var(--accent)">{active_clients}</div>
                <div class="stat-label">Active Clients</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" style="color: var(--success)">{total_platforms}</div>
                <div class="stat-label">Social Platforms</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" style="color: #3b82f6">{total_resources}</div>
                <div class="stat-label">AWS Resources</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" style="color: #8b5cf6">{len(resources['eventbridge'])}</div>
                <div class="stat-label">Automations</div>
            </div>
        </div>
        
        <div class="main-grid">
            <div class="section">
                <div class="section-header">
                    <h2 class="section-title">👥 Client Accounts</h2>
                    <span class="section-badge">{active_clients} Active</span>
                </div>
                <div class="clients-grid">
                    {client_cards}
                    <div class="client-card" style="border-left: 4px solid #666; opacity: 0.6;">
                        <div class="client-header">
                            <span class="client-logo">➕</span>
                            <div class="client-info">
                                <h3>Add New Client</h3>
                                <span class="client-location">Ready to scale</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <div class="section-header">
                    <h2 class="section-title">☁️ AWS Infrastructure</h2>
                    <span class="section-badge">{total_resources} Resources</span>
                </div>
                <div class="resources-list">
                    {aws_resources_html}
                </div>
            </div>
        </div>
        
        <div class="diagrams-section">
            <div class="section">
                <div class="section-header">
                    <h2 class="section-title">📊 Architecture & Workflow</h2>
                </div>
                <div class="diagrams-grid">
                    <div class="diagram-container">
                        <img src="aws-architecture.png?t={int(os.path.getmtime('aws-architecture.png')) if os.path.exists('aws-architecture.png') else int(datetime.now().timestamp())}" alt="AWS Architecture">
                    </div>
                    <div class="diagram-container">
                        <img src="workflow-diagram.png?t={int(os.path.getmtime('workflow-diagram.png')) if os.path.exists('workflow-diagram.png') else int(datetime.now().timestamp())}" alt="Marketing Workflow">
                    </div>
                </div>
            </div>
        </div>
        
        <footer class="footer">
            <p>ZOE STUDIO Marketing Intelligence • Powered by <a href="https://openclaw.ai">OpenClaw</a> + AWS</p>
            <p>Auto-refreshes every 5 minutes</p>
        </footer>
    </div>
</body>
</html>'''
    
    with open('unified.html', 'w') as f:
        f.write(html)
    print(f"Generated unified dashboard with {active_clients} clients, {total_resources} AWS resources")

if __name__ == '__main__':
    generate_unified_dashboard()
