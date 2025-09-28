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
import logging

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tekuila import mcp

# Get logger (logging is already configured in tekuila.py)
logger = logging.getLogger(__name__)

def main():
    """Run the Tekuila MCP server."""
    logger.info("🍽️ Starting Tekuila MCP Server...")
    logger.info("Available tools:")
    logger.info("  - get_current_day_menu: Get today's menu")
    logger.info("  - get_current_week_menu: Get this week's menu")
    logger.info("  - get_current_date: Get current date context")
    logger.info("  - analyze_daily_menu: Get today's menu with AI analysis guide")
    logger.info("  - plan_weekly_menu: Get week's menu with planning guide")
    logger.info("Available prompts:")
    logger.info("  - analyze_menu_selection: Help analyze menu options")
    logger.info("  - weekly_menu_planning: Help plan weekly meals")
    logger.info("")
    
    # Get port from environment variable, default to 8080
    port = int(os.getenv('PORT', '8080'))
    
    # Run the MCP server with streamable HTTP transport for cloud hosting
    mcp.run(transport='streamable-http', host='0.0.0.0', port=port)

if __name__ == "__main__":
    main()
