#!/usr/bin/env python3
"""
Tekuila MCP Server - Restaurant Menu API

This MCP server provides tools and prompts for accessing Tekuila restaurant menus
and getting healthy meal recommendations.

Usage:
    python main.py          # Run the MCP server
    python tekuila.py       # Alternative way to run the server
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tekuila import mcp

def main():
    """Run the Tekuila MCP server."""
    print("🍽️ Starting Tekuila MCP Server...", file=sys.stderr)
    print("Available tools:", file=sys.stderr)
    print("  - get_current_day_menu: Get today's menu", file=sys.stderr)
    print("  - get_current_week_menu: Get this week's menu", file=sys.stderr)
    print("  - get_current_date: Get current date context", file=sys.stderr)
    print("  - analyze_daily_menu: Get today's menu with AI analysis guide", file=sys.stderr)
    print("  - plan_weekly_menu: Get week's menu with planning guide", file=sys.stderr)
    print("Available prompts:", file=sys.stderr)
    print("  - analyze_menu_selection: Help analyze menu options", file=sys.stderr)
    print("  - weekly_menu_planning: Help plan weekly meals", file=sys.stderr)
    print("", file=sys.stderr)
    
    # Run the MCP server
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
