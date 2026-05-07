import os
import sys

# Add src to Python path
sys.path.insert(0, os.path.abspath('src'))

from mithaq.autonomous_generated.api.slackdiscordconnector import SlackDiscordConnector

# Test the module
try:
    c = SlackDiscordConnector()
    print("Instance created.")
except Exception as e:
    print(e)
