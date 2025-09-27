import httpx
import xml.etree.ElementTree as ET
import re
import sys
from datetime import datetime
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("tekuila-menu")

# Constants
CURRENT_DAY_URL = "https://www.compass-group.fi/menuapi/feed/rss/current-day?costNumber=0605&language=fi"
CURRENT_WEEK_URL = "https://www.compass-group.fi/menuapi/feed/rss/current-week?costNumber=0605&language=fi"

async def fetch_rss_feed(url: str) -> str | None:
    """Fetch RSS feed content."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching RSS: {e}", file=sys.stderr)
            return None

def parse_menu_items(rss_content: str) -> list[dict]:
    """Parse RSS and extract menu items by day."""
    try:
        root = ET.fromstring(rss_content)
        items = []
        
        for item in root.findall('.//item'):
            title = item.find('title')
            description = item.find('description')
            
            if title is not None and description is not None:
                # Clean HTML entities and tags
                clean_desc = description.text or ''
                clean_desc = clean_desc.replace('&lt;br&gt;', '\n')
                clean_desc = clean_desc.replace('&amp;', '&')
                clean_desc = re.sub(r'<[^>]+>', '', clean_desc)
                clean_desc = re.sub(r'\s+', ' ', clean_desc).strip()
                
                items.append({
                    'day': title.text or '',
                    'menu': clean_desc
                })
        
        return items
    except Exception as e:
        print(f"Error parsing RSS: {e}", file=sys.stderr)
        return []

def get_current_date_context() -> str:
    """Get current date for AI context."""
    now = datetime.now()
    return f"Current date: {now.strftime('%A, %B %d, %Y')} ({now.strftime('%Y-%m-%d')})"

def get_menu_guidelines() -> str:
    """Get shared menu guidelines including health priority and dietary codes."""
    return """### Health Priority (Most Important)
- **Vegaaninen kasvislounas** = Usually healthiest (vegan)
- **Kasvislounas** = Good vegetarian option  
- **Lounas** = Regular meat option
- **POP UP Bistro** = Special/expensive option

### Dietary Restriction Codes
When users have special dietary needs, explain these Finnish codes:
- **(G) Gluteeniton** = Gluten-free
- **(L) Laktoositon** = Lactose-free
- **(VL) Vähälaktoosinen** = Low-lactose
- **(M) Maidoton** = Dairy-free
- **(Veg) Soveltuu vegaaniruokavalioon** = Suitable for vegan diet
- **(VS) Sis. tuoretta valkosipulia** = Contains fresh garlic
- **(A) Sis. Allergeeneja** = Contains allergens"""

def get_red_flags() -> str:
    """Get shared red flags to identify problematic menu options."""
    return """### Red Flags to Identify
- Overly processed vegetarian options (like simple carrot crepes)
- Deep-fried items (paistettu)
- Heavy cream/cheese sauces (kerma, juusto)
- Lack of vegetables or protein"""


def get_daily_analysis_instructions() -> str:
    """Get the daily menu analysis instructions."""
    return f"""# AI-Powered Menu Analysis

## Your Task
Analyze the above menu options and provide intelligent recommendations based on:

{get_menu_guidelines()}

### AI Analysis Guidelines
1. **Nutritional Quality**: Evaluate protein sources, vegetables, cooking methods
2. **Processing Level**: Prefer whole foods over processed options
3. **Taste Balance**: Consider if vegetarian options are actually appealing
4. **Value Assessment**: Is POP UP Bistro worth the extra cost?

{get_red_flags()}

### Recommendation Format
Provide your analysis with:
1. **Best Choice** with reasoning
2. **Backup Option** if first choice isn't appealing
3. **Avoid** any problematic options
4. **Why** - brief explanation of health benefits
5. **Dietary Info** - mention relevant dietary codes if user has special needs

Remember: The healthiest option you'll actually enjoy eating is better than the perfect option you'll skip!"""

def get_weekly_planning_instructions() -> str:
    """Get the weekly menu planning instructions."""
    return f"""# AI-Powered Weekly Menu Planning

## Your Task
Analyze the week's menu and create a balanced meal plan that optimizes both health and satisfaction.

### Weekly Strategy
- **Monday**: Start strong with the healthiest option
- **Tuesday-Thursday**: Mix of vegetarian and quality meat options
- **Friday**: Treat yourself (but still healthy)
- **Weekend**: Restaurant closed - plan alternative meals

{get_menu_guidelines()}

### AI Planning Guidelines
1. **Variety**: Different protein sources and vegetables each day (Monday-Friday only)
2. **Balance**: 2-3 vegetarian days, 2-3 quality meat days (5-day work week)
3. **Cost Management**: Limit POP UP Bistro to 1-2 days max
4. **Taste Satisfaction**: Ensure you'll actually enjoy each choice
5. **Weekend Planning**: Note that restaurant is closed - skip weekends

### Analysis Framework
For each day, consider:
- **Health Score**: How nutritious is this option?
- **Taste Appeal**: Will I enjoy eating this?
- **Value**: Is this worth the price?
- **Variety**: How does this fit with other days?
- **Dietary Compatibility**: Does this match user's dietary restrictions?

{get_red_flags()}

### Recommendation Format
Provide a weekly plan with:
1. **Daily Choice** with brief reasoning (Monday-Friday only)
2. **Overall Balance** assessment (5-day work week)
3. **Cost Summary** (regular vs special options)
4. **Health Highlights** (key nutritional wins)
5. **Dietary Notes** (mention relevant codes for special needs)
6. **Weekend Note** (restaurant closed - skip weekends)

Remember: Consistency beats perfection. Choose options you'll actually eat and enjoy!"""

@mcp.tool()
async def get_current_day_menu() -> str:
    """Get today's menu from Tekuila restaurant."""
    rss_content = await fetch_rss_feed(CURRENT_DAY_URL)
    if not rss_content:
        return "Unable to fetch today's menu."
    
    items = parse_menu_items(rss_content)
    if not items:
        return "No menu found for today."
    
    date_context = get_current_date_context()
    result = f"🍽️ **TEKUILA - TODAY'S MENU**\n{date_context}\n\n"
    
    for item in items:
        result += f"**{item['day']}**\n"
        result += f"{item['menu']}\n\n"
    
    return result

@mcp.tool()
async def get_current_week_menu() -> str:
    """Get this week's menu from Tekuila restaurant."""
    rss_content = await fetch_rss_feed(CURRENT_WEEK_URL)
    if not rss_content:
        return "Unable to fetch this week's menu."
    
    items = parse_menu_items(rss_content)
    if not items:
        return "No menu found for this week."
    
    date_context = get_current_date_context()
    result = f"🍽️ **TEKUILA - THIS WEEK'S MENU**\n{date_context}\n\n"
    
    for item in items:
        result += f"**{item['day']}**\n"
        result += f"{item['menu']}\n\n"
    
    return result


@mcp.tool()
async def get_current_date() -> str:
    """Get current date and time context."""
    return get_current_date_context()

@mcp.tool()
async def analyze_daily_menu() -> str:
    """Get today's menu with AI analysis instructions for daily planning."""
    rss_content = await fetch_rss_feed(CURRENT_DAY_URL)
    if not rss_content:
        return "Unable to fetch today's menu."
    
    items = parse_menu_items(rss_content)
    if not items:
        return "No menu found for today."
    
    date_context = get_current_date_context()
    result = f"🍽️ **TEKUILA - TODAY'S MENU WITH ANALYSIS GUIDE**\n{date_context}\n\n"
    
    for item in items:
        result += f"**{item['day']}**\n"
        result += f"{item['menu']}\n\n"
    
    result += get_daily_analysis_instructions()
    
    return result

@mcp.tool()
async def plan_weekly_menu() -> str:
    """Get this week's menu with AI planning instructions for weekly meal planning."""
    rss_content = await fetch_rss_feed(CURRENT_WEEK_URL)
    if not rss_content:
        return "Unable to fetch this week's menu."
    
    items = parse_menu_items(rss_content)
    if not items:
        return "No menu found for this week."
    
    date_context = get_current_date_context()
    result = f"🍽️ **TEKUILA - THIS WEEK'S MENU WITH PLANNING GUIDE**\n{date_context}\n\n"
    
    for item in items:
        result += f"**{item['day']}**\n"
        result += f"{item['menu']}\n\n"
    
    result += get_weekly_planning_instructions()
    
    return result

@mcp.prompt()
def analyze_menu_selection() -> str:
    """Help analyze and select the best menu options using AI analysis."""
    return f"{get_current_date_context()}\n\n{get_daily_analysis_instructions()}"

@mcp.prompt()
def weekly_menu_planning() -> str:
    """Help plan meals for the whole week using AI analysis."""
    return f"{get_current_date_context()}\n\n{get_weekly_planning_instructions()}"

if __name__ == "__main__":
    mcp.run(transport='stdio')
