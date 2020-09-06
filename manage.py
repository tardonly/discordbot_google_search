#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from bot import client

TOKEN = 'NzUxNzc5MjEyMDM3NDU1OTAz.X1OC8w.GxLV155BNLSwCDmLZ1dtkHpIDSc'  # os.getenv('DISCORD_TOKEN')

def main():
    """Run administrative tasks."""
    client.run(TOKEN)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'discordbot.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
