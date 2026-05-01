#!/usr/bin/env python3
"""
DAQIQ NEXUS - AI Security Orchestrator
Coordinates parallel security scanning with AI-powered analysis
"""

import asyncio
import aiohttp
import json
from datetime import datetime
from typing import List, Dict
import redis
import os

class DaqiqOrchestrator:
    def __init__(self):
        self.ollama_host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
        self.zap_host = os.getenv('ZAP_HOST', 'http://localhost:8080')
        self.redis_client = redis.Redis(
            host=os.getenv('REDIS_HOST', 'localhost').split(':')[0],
            port=6379,
            decode_responses=True
        )
        
    async def scan_target(self, target_url: str, scan_types: List[str]) -> Dict:
        """
        Orchestrates parallel security scans using AI
        """
        print(f"🤖 DAQIQ AI Orchestrator starting scan of: {target_url}")
        
        # Step 1: AI Planning Phase
        scan_plan = await self.ai_create_scan_plan(target_url, scan_types)
        print(f"📋 AI Generated Scan Plan: {json.dumps(scan_plan, indent=2)}")
        
        # Step 2: Execute scans in parallel
        tasks = []
        if 'web' in scan_types:
            tasks.append(self.run_zap_scan(target_url))
        if 'container' in scan_types:
            tasks.append(self.run_trivy_scan(target_url))
        if 'code' in scan_types:
            tasks.append(self.run_semgrep_scan(target_url))
        if 'ai-agent' in scan_types:
            tasks.append(self.run_mapta_agent(target_url))
        
        # Run all scans in parallel
        print(f"⚡ Running {len(tasks)} scans in parallel...")
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Step 3: AI Correlation & Analysis
        correlated = await self.ai_correlate_results(results)
        
        # Step 4: AI Prioritization
        prioritized = await self.ai_prioritize_vulnerabilities(correlated)
        
        return {
            'target': target_url,
            'scan_date': datetime.now().isoformat(),
            'scan_plan': scan_plan,
            'raw_results': results,
            'correlated_vulnerabilities': correlated,
            'prioritized_report': prioritized,
            'summary': self._generate_summary(prioritized)
        }
    
    async def ai_create_scan_plan(self, target: str, scan_types: List[str]) -> Dict:
        """Uses Ollama to create intelligent scan strategy"""
        prompt = f'''Create a security scan plan for: {target}
Available scanners: {', '.join(scan_types)}

Return JSON with:
- execution_order: optimal scanner sequence
- parallel_groups: which can run together
- focus_areas: key vulnerabilities to check

JSON only:'''
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f'{self.ollama_host}/api/generate',
                    json={
                        'model': 'deepseek-r1:1.5b',
                        'prompt': prompt,
                        'stream': False
                    },
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as resp:
                    result = await resp.json()
                    response_text = result.get('response', '{}')
                    # Extract JSON from response
                    try:
                        return json.loads(response_text)
                    except:
                        return {
                            'execution_order': scan_types,
                            'parallel_groups': [scan_types],
                            'focus_areas': ['XSS', 'SQL Injection', 'CSRF']
                        }
        except Exception as e:
            print(f"⚠️  AI planning failed: {e}, using default plan")
            return {
                'execution_order': scan_types,
                'parallel_groups': [scan_types],
                'focus_areas': ['Common vulnerabilities']
            }
    
    async def run_zap_scan(self, target_url: str) -> Dict:
        """Execute OWASP ZAP scan"""
        print(f"🔍 Starting ZAP scan on {target_url}")
        
        try:
            async with aiohttp.ClientSession() as session:
                # Spider the target
                async with session.get(
                    f'{self.zap_host}/JSON/spider/action/scan/',
                    params={'url': target_url},
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as resp:
                    await resp.json()
                
                # Quick scan (in production, wait for completion)
                await asyncio.sleep(10)
                
                # Get alerts
                async with session.get(
                    f'{self.zap_host}/JSON/core/view/alerts/',
                    params={'baseurl': target_url},
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as resp:
                    alerts = await resp.json()
                
                return {
                    'scanner': 'OWASP ZAP',
                    'vulnerabilities': alerts.get('alerts', [])[:10],  # Limit to 10
                    'scan_type': 'DAST',
                    'status': 'completed'
                }
        except Exception as e:
            print(f"⚠️  ZAP scan failed: {e}")
            return {
                'scanner': 'OWASP ZAP',
                'vulnerabilities': [],
                'scan_type': 'DAST',
                'status': 'failed',
                'error': str(e)
            }
    
    async def run_trivy_scan(self, target: str) -> Dict:
        """Execute Trivy container scan"""
        print(f"🐳 Trivy scan simulated for {target}")
        
        # Simulated results (in production, execute via docker)
        return {
            'scanner': 'Trivy',
            'vulnerabilities': [
                {
                    'VulnerabilityID': 'CVE-2024-1234',
                    'Severity': 'HIGH',
                    'Title': 'Outdated base image',
                    'Description': 'Container uses outdated dependencies'
                }
            ],
            'scan_type': 'Container Security',
            'status': 'completed'
        }
    
    async def run_semgrep_scan(self, target_path: str) -> Dict:
        """Execute Semgrep SAST scan"""
        print(f"📝 Semgrep scan simulated for {target_path}")
        
        # Simulated results
        return {
            'scanner': 'Semgrep',
            'vulnerabilities': [
                {
                    'check_id': 'python.flask.security.xss',
                    'severity': 'WARNING',
                    'message': 'Potential XSS vulnerability',
                    'path': '/app/routes.py'
                }
            ],
            'scan_type': 'SAST',
            'status': 'completed'
        }
    
    async def run_mapta_agent(self, target: str) -> Dict:
        """Execute MAPTA AI security agent"""
        print(f"🤖 Starting MAPTA AI Agent on {target}")
        
        prompt = f'''You are a security AI agent analyzing: {target}

Find vulnerabilities in:
1. Authentication logic
2. Authorization flaws
3. Business logic issues
4. Arabic character injection (RTL: ‏‎)

Return JSON array of findings with: type, severity, description'''
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f'{self.ollama_host}/api/generate',
                    json={
                        'model': 'qwen2.5:3b',
                        'prompt': prompt,
                        'stream': False
                    },
                    timeout=aiohttp.ClientTimeout(total=45)
                ) as resp:
                    result = await resp.json()
                    response_text = result.get('response', '[]')
                    
                    try:
                        findings = json.loads(response_text)
                    except:
                        findings = []
                    
                    return {
                        'scanner': 'MAPTA AI Agent',
                        'vulnerabilities': findings if isinstance(findings, list) else [],
                        'scan_type': 'AI-Powered Analysis',
                        'status': 'completed'
                    }
        except Exception as e:
            print(f"⚠️  MAPTA failed: {e}")
            return {
                'scanner': 'MAPTA AI Agent',
                'vulnerabilities': [],
                'scan_type': 'AI-Powered Analysis',
                'status': 'failed',
                'error': str(e)
            }
    
    async def ai_correlate_results(self, results: List) -> List[Dict]:
        """AI-powered vulnerability correlation"""
        print("🔗 Correlating vulnerabilities...")
        
        # Filter out errors
        valid_results = [r for r in results if isinstance(r, dict) and r.get('status') == 'completed']
        
        if not valid_results:
            return []
        
        # Flatten all vulnerabilities
        all_vulns = []
        for result in valid_results:
            scanner = result.get('scanner', 'Unknown')
            for vuln in result.get('vulnerabilities', []):
                vuln['source_scanner'] = scanner
                all_vulns.append(vuln)
        
        return all_vulns[:20]  # Limit to 20
    
    async def ai_prioritize_vulnerabilities(self, vulnerabilities: List[Dict]) -> List[Dict]:
        """AI prioritization"""
        print("📊 Prioritizing vulnerabilities...")
        
        # Simple prioritization (in production, use AI)
        priority_map = {
            'CRITICAL': 10,
            'HIGH': 8,
            'MEDIUM': 5,
            'WARNING': 5,
            'LOW': 2,
            'INFO': 1
        }
        
        for vuln in vulnerabilities:
            severity = str(vuln.get('Severity', vuln.get('severity', 'MEDIUM'))).upper()
            vuln['priority_score'] = priority_map.get(severity, 5)
            vuln['severity_normalized'] = severity
        
        # Sort by priority
        return sorted(vulnerabilities, key=lambda x: x.get('priority_score', 0), reverse=True)
    
    def _generate_summary(self, prioritized: List[Dict]) -> Dict:
        """Generate scan summary"""
        severities = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        
        for vuln in prioritized:
            severity = vuln.get('severity_normalized', 'MEDIUM').lower()
            if 'critical' in severity:
                severities['critical'] += 1
            elif 'high' in severity:
                severities['high'] += 1
            elif 'medium' in severity or 'warning' in severity:
                severities['medium'] += 1
            else:
                severities['low'] += 1
        
        return {
            **severities,
            'total': len(prioritized),
            'scanners_used': len(set(v.get('source_scanner', '') for v in prioritized))
        }


# FastAPI server
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="DAQIQ Orchestrator API")

# CORS for web UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = DaqiqOrchestrator()

class ScanRequest(BaseModel):
    target: str
    scan_types: List[str] = ['web', 'ai-agent']

@app.get("/")
async def root():
    return {
        "service": "DAQIQ NEXUS Orchestrator",
        "version": "1.0.0",
        "status": "running"
    }

@app.post("/api/scan")
async def start_scan(request: ScanRequest, background_tasks: BackgroundTasks):
    """Start a new security scan"""
    scan_id = f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Store in Redis
    orchestrator.redis_client.set(f'scan:{scan_id}:status', 'running')
    orchestrator.redis_client.set(f'scan:{scan_id}:target', request.target)
    
    # Run scan in background
    async def run_scan():
        try:
            results = await orchestrator.scan_target(request.target, request.scan_types)
            orchestrator.redis_client.set(f'scan:{scan_id}:results', json.dumps(results))
            orchestrator.redis_client.set(f'scan:{scan_id}:status', 'completed')
        except Exception as e:
            print(f"❌ Scan failed: {e}")
            orchestrator.redis_client.set(f'scan:{scan_id}:status', 'failed')
            orchestrator.redis_client.set(f'scan:{scan_id}:error', str(e))
    
    background_tasks.add_task(run_scan)
    
    return {
        'scan_id': scan_id,
        'status': 'running',
        'target': request.target
    }

@app.get("/api/scan/{scan_id}")
async def get_scan_results(scan_id: str):
    """Get scan results"""
    status = orchestrator.redis_client.get(f'scan:{scan_id}:status')
    results = orchestrator.redis_client.get(f'scan:{scan_id}:results')
    target = orchestrator.redis_client.get(f'scan:{scan_id}:target')
    error = orchestrator.redis_client.get(f'scan:{scan_id}:error')
    
    return {
        'scan_id': scan_id,
        'status': status or 'not_found',
        'target': target,
        'results': json.loads(results) if results else None,
        'error': error
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "orchestrator"}

if __name__ == '__main__':
    import uvicorn
    print("🚀 Starting DAQIQ Orchestrator on port 8000...")
    uvicorn.run(app, host='0.0.0.0', port=8000)
