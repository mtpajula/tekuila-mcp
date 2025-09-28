# 🍽️ Tekuila MCP Server

An MCP (Model Context Protocol) server for accessing Tekuila restaurant menus with AI-powered healthy meal recommendations.

## Features

- **📅 Daily & Weekly Menus**: Get current day and week menus from Tekuila restaurant
- **🤖 AI-Powered Analysis**: Intelligent health recommendations and meal planning
- **📊 Date Context**: Current date awareness for better planning
- **🌱 Health-Focused**: Prioritizes vegetarian options while considering taste
- **🔧 Universal Compatibility**: Works with Claude Desktop, Cursor, LM Studio, and other MCP clients

## Quick Start

### Prerequisites

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

1. **Clone and setup:**
   ```bash
   git clone <your-repo>
   cd tekuila
   uv sync
   ```

2. **Run the server:**
   
   **For cloud hosting (HTTP transport):**
   ```bash
   uv run python main.py
   ```
   
   **For local development (stdio transport):**
   ```bash
   uv run python tekuila.py
   ```

## Transport Modes

The server supports two different transport modes:

### Stdio Transport (`tekuila.py`)
- **Use case**: Local development and MCP client integration
- **How it works**: Communicates via standard input/output
- **Best for**: Claude Desktop, Cursor, LM Studio, and other MCP clients
- **Command**: `uv run python tekuila.py`

### HTTP Transport (`main.py`)
- **Use case**: Cloud hosting and web deployment
- **How it works**: Runs as an HTTP server on port 8000
- **Best for**: Cloud platforms, Docker containers, web services
- **Command**: `uv run python main.py`
- **URL**: `http://127.0.0.1:8000` (when running locally)

### Connect to MCP Clients

#### Claude Desktop
Add this to your `claude_desktop_config.json` (uses stdio transport):

```json
{
  "mcpServers": {
    "tekuila": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/tekuila",
        "run",
        "tekuila.py"
      ]
    }
  }
}
```

#### Cursor
The server also works with Cursor's MCP integration. Configure it in your Cursor MCP settings.

#### LM Studio
Compatible with LM Studio's MCP server support. Add the server configuration in LM Studio's MCP settings.

## Available Tools

### Basic Menu Tools
- **`get_current_day_menu()`** - Get today's menu with date context
- **`get_current_week_menu()`** - Get this week's menu with date context
- **`get_current_date()`** - Get current date and time context

### AI-Powered Planning Tools
- **`analyze_daily_menu()`** - Get today's menu with AI analysis instructions
- **`plan_weekly_menu()`** - Get week's menu with planning guide

### Prompts (for clients with prompt support)
- **`analyze_menu_selection`** - AI-powered daily menu analysis
- **`weekly_menu_planning`** - AI-powered weekly meal planning

## Usage Examples

### Daily Menu Analysis
```
What's on the menu today at Tekuila?
```

### Weekly Planning
```
Help me plan my meals for this week with healthy recommendations.
```

### AI Analysis
```
Analyze today's menu and recommend the healthiest options.
```

## Menu Structure

The server understands Finnish menu categories:

- **🌱 Vegaaninen kasvislounas** - Vegan lunch (healthiest)
- **🥬 Kasvislounas** - Vegetarian lunch (good option)
- **🍖 Lounas** - Regular lunch (meat options)
- **⭐ POP UP Bistro** - Special/expensive options
- **🍰 Jälkiruoka** - Desserts

## AI Analysis Features

### Health Priority System
1. **Vegaaninen kasvislounas** - Usually healthiest (vegan)
2. **Kasvislounas** - Good vegetarian option
3. **Lounas** - Regular meat option
4. **POP UP Bistro** - Special/expensive option

### Analysis Guidelines
- **Nutritional Quality**: Evaluates protein sources, vegetables, cooking methods
- **Processing Level**: Prefers whole foods over processed options
- **Taste Balance**: Considers if vegetarian options are actually appealing
- **Value Assessment**: Evaluates if special options are worth the cost

### Red Flags
- Overly processed vegetarian options (like simple carrot crepes)
- Deep-fried items (paistettu)
- Heavy cream/cheese sauces (kerma, juusto)
- Lack of vegetables or protein

## Technical Details

### RSS Integration
- **Current Day**: `https://www.compass-group.fi/menuapi/feed/rss/current-day?costNumber=0605&language=fi`
- **Current Week**: `https://www.compass-group.fi/menuapi/feed/rss/current-week?costNumber=0605&language=fi`

### Dependencies
- `httpx` - HTTP client for RSS fetching
- `mcp[cli]` - Model Context Protocol server framework

### Architecture
- **Simple RSS Parsing**: Extracts day + menu content
- **AI-Powered Analysis**: Lets AI analyze menu text intelligently
- **Shared Instructions**: Reuses prompt content across tools and prompts
- **Date Awareness**: Includes current date context for better planning

## Development

### Project Structure
```
tekuila/
├── tekuila.py          # Main MCP server implementation (stdio transport)
├── main.py             # HTTP server entry point (streamable-http transport)
├── pyproject.toml      # Project configuration
├── uv.lock            # Dependency lock file
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

### Running Tests
```bash
# Test HTTP server startup (cloud hosting)
uv run python main.py

# Test stdio server startup (local development)
uv run python tekuila.py

# Test individual functions
uv run python -c "from tekuila import get_current_date_context; print(get_current_date_context())"
```

## Troubleshooting

### Server Not Starting
- Check Python version (3.12+ required)
- Ensure all dependencies are installed: `uv sync`
- Check RSS feed URLs are accessible

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Enjoy your healthy meals at Tekuila! 🍽️**
