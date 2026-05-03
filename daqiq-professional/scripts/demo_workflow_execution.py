#!/usr/bin/env python3
"""
Demo: End-to-End Workflow Execution
Shows the complete autonomous workflow system in action
"""

import sys

sys.path.insert(0, "daqiq-professional/src")

import json

from daqiq.orchestration_api import orchestrate_workflow
from daqiq.workflow_parser import load_workflow

print("""
╔══════════════════════════════════════════════════════════════╗
║  🎯 DAQIQ AUTONOMOUS WORKFLOW DEMO                          ║
╚══════════════════════════════════════════════════════════════╝
""")

# Load the security scan workflow
workflow_file = "daqiq-professional/examples/workflows/security_scan_workflow.yaml"
print(f"📄 Loading workflow: {workflow_file}")

config = load_workflow(workflow_file)
print(f"   Workflow: {config['name']}")
print(f"   Agents: {len(config['agents'])}")
print(f"   Tasks: {len(config['tasks'])}")

# Execute the workflow
print("\n🚀 Executing workflow...")
result = orchestrate_workflow(config)

# Display results
print("\n" + "=" * 70)
print("EXECUTION RESULTS")
print("=" * 70)

if result.success:
    print("✅ Status: SUCCESS")
    print(f"⏱️  Duration: {result.duration:.3f} seconds")
    print("\n📊 Report:")
    print(json.dumps(result.outputs, indent=2))
else:
    print("❌ Status: FAILED")
    print(f"Errors: {result.errors}")

print("\n" + "=" * 70)
print("🎉 Demo complete! Your autonomous agents work!")
print("=" * 70)
