# Dixa MCP Server - Getting Started

Connect your AI assistant to your Dixa account and access your customer service data directly through AI conversations.

## What is the Dixa MCP Server?

The Dixa MCP Server is a Model Context Protocol (MCP) server that connects your AI assistant to your Dixa organization. Ask questions about your conversations, agents, customers, and analytics - all through natural conversation with your AI assistant.

**What you can do:**
- Search and analyze conversations
- Get information about agents, teams, and queues
- View customer (end user) details and conversation history
- Access analytics and metrics
- Manage tags, notes, and conversation assignments
- And much more!

## Quick Start

The easiest way to get started is using our hosted server. This requires no local setup - just configure your AI client and you're ready to go.

### Step 1: Get Your Dixa API Key

Before connecting to any AI client, you'll need a Dixa API key:

1. Log in to your Dixa account
2. Go to Settings → API
3. Create a new API token for the Dixa API
4. Copy your API key (you'll need it when configuring your AI client)

> **Need help?** See the [Dixa API documentation](https://docs.dixa.io/docs/) for detailed instructions on creating an API token.

### Step 2: Configure Your AI Client

Choose your AI client from the options below and follow the setup instructions:

- [Claude Desktop](#claude-desktop)
- [Cursor](#cursor)

### Step 3: Start Using It!

Once configured, you can start asking questions about your Dixa data:

- "How many conversations were closed last week?"
- "Show me conversations from agent John Smith"
- "What's the average response time for email conversations?"
- "List all active agents in the organization"

Your AI assistant will use the Dixa MCP server to fetch the information and provide you with answers.

## Client Setup Guides

### Claude Desktop

Follow these steps to connect Claude Desktop to the Dixa MCP server:

1. **Open Claude Desktop Configuration File**
   - **macOS**: Open `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: Open `%APPDATA%\Claude\claude_desktop_config.json`
   
   You can open this file with any text editor.

2. **Add the Dixa MCP Server Configuration**

   Add the following configuration to your `claude_desktop_config.json` file:

   ```json
   {
     "mcpServers": {
       "dixa": {
         "command": "npx",
         "args": [
           "mcp-remote",
           "https://dixa-mcp-public.fastmcp.app/mcp",
           "--header",
           "Authorization: Bearer YOUR_API_KEY_HERE"
         ]
       }
     }
   }
   ```

   **Important**: Replace `YOUR_API_KEY_HERE` with your actual Dixa API key from Step 1.

3. **Save the Configuration File**

   Make sure to save the file after making changes.

4. **Restart Claude Desktop**

   Close and restart Claude Desktop completely for the changes to take effect.

5. **Verify the Connection**

   After restarting, you should see the Dixa MCP server available in Claude Desktop. You can now start asking questions about your Dixa data!

**Note**: If you already have other MCP servers configured, add the `"dixa"` entry to the existing `"mcpServers"` object without removing your other configurations.

### Cursor

Follow these steps to connect Cursor to the Dixa MCP server:

1. **Open Cursor Settings**
   - Open Cursor IDE
   - Press `Cmd+,` (macOS) or `Ctrl+,` (Windows/Linux) to open Settings
   - Alternatively, go to **Cursor** → **Settings** (macOS) or **File** → **Preferences** → **Settings** (Windows/Linux)

2. **Access MCP Configuration**
   - In Settings, search for "MCP" or navigate to **Features** → **MCP**
   - Click on **Edit MCP Settings** or open the MCP configuration file

3. **Add Dixa MCP Server Configuration**

   Add the following configuration:

   ```json
   {
     "mcpServers": {
       "dixa": {
         "command": "npx",
         "args": [
           "mcp-remote",
           "https://dixa-mcp-public.fastmcp.app/mcp",
           "--header",
           "Authorization: Bearer YOUR_API_KEY_HERE"
         ]
       }
     }
   }
   ```

   **Important**: Replace `YOUR_API_KEY_HERE` with your actual Dixa API key from Step 1.

4. **Save the Configuration File**

   Make sure to save the file after making changes.

5. **Restart Cursor**

   Close and restart Cursor completely for the changes to take effect.

6. **Verify the Connection**

   After restarting, the Dixa MCP server should be available in Cursor. You can test it by asking Cursor questions about your Dixa data in the chat interface.

**Note**: 
- If you already have other MCP servers configured, add the `"dixa"` entry to the existing `"mcpServers"` object without removing your other configurations.
- The exact configuration file location may vary depending on your Cursor version. If you can't find the MCP settings, check Cursor's documentation or look for MCP-related settings in the Settings UI.

## Server Endpoint

All clients connect to the same hosted server endpoint:

**Server URL**: `https://dixa-mcp-public.fastmcp.app/mcp`

**Authentication**: Include your Dixa API key in the Authorization header:
```
Authorization: Bearer YOUR_API_KEY_HERE
```

## What Can You Do?

The Dixa MCP Server provides access to 79 different tools organized into categories:

### 📊 Analytics
- Get aggregated metrics and statistics
- Analyze conversation data
- View performance metrics

### 💬 Conversations
- Search and filter conversations
- View conversation details, messages, and notes
- Manage conversation assignments and tags
- Add notes and update conversation status

### 👥 Agents & Teams
- View agent information and presence status
- Manage team memberships
- View team performance

### 👤 Customers (End Users)
- View customer profiles
- See conversation history per customer
- Manage customer information

### 🏷️ Tags & Organization
- List and manage tags
- Organize conversations with tags
- View organizational structure

### 📚 Knowledge Base
- Access knowledge base articles
- Manage article categories

### ⚙️ Settings
- View contact endpoints (channels)
- Check business hours status
- View queue information

## Example Use Cases

### Daily Standup Questions
- "How many conversations did we handle yesterday?"
- "What's our current queue status?"
- "Show me conversations that need follow-up"

### Agent Performance
- "Which agents handled the most conversations this week?"
- "Show me conversations assigned to the support team"
- "What's the average response time for our agents?"

### Customer Insights
- "Find all conversations from customer John Doe"
- "Show me conversations with high satisfaction ratings"
- "List customers who contacted us via email last month"

### Analytics & Reporting
- "What's our CSAT score for the last quarter?"
- "How many conversations were closed vs. opened this week?"
- "Show me conversation trends by channel"

## Data Security

- **HTTPS Encryption**: Your API key and all data are sent securely via HTTPS encryption
- **No Data Storage**: No data is stored on the MCP server - it acts as a secure proxy between your AI client and Dixa. However, please note that your LLM provider (OpenAI, Anthropic, Google, etc.) may store or use your data for training purposes depending on your subscription plan. We recommend checking with your LLM provider regarding their data storage and training policies, as this typically varies based on your paid package tier.
- **Direct Connection**: All requests go directly from your AI client to your Dixa account through the MCP server
- **API Key Protection**: Your API key is only used to authenticate with the Dixa API and is never logged or stored

## Troubleshooting

### AI client doesn't show the Dixa server

1. Make sure you saved the configuration file correctly
2. Restart your AI client completely
3. Check that your configuration syntax is valid (JSON format, no trailing commas, proper quotes)
4. Verify your API key is correct
5. Ensure you're using the correct server URL: `https://dixa-mcp-public.fastmcp.app/mcp`

### "Authentication failed" errors

1. Verify your API key is correct
2. Make sure there are no extra spaces in your API key
3. Check that your API token hasn't expired in Dixa
4. Ensure the API token has the necessary permissions
5. Verify the Authorization header format: `Authorization: Bearer YOUR_API_KEY`

### Can't find conversations or data

1. Verify your API key has access to the data you're requesting
2. Check that the data exists in your Dixa account
3. Try using more specific search terms
4. Ensure your API token has the required permissions in Dixa

### Connection issues

1. Verify your internet connection
2. Check that the server URL is accessible: `https://dixa-mcp-public.fastmcp.app/mcp`
3. Ensure your firewall isn't blocking the connection
4. Try testing the connection with a simple request

## Need Help?

- **Dixa API Documentation**: [https://docs.dixa.io/docs/](https://docs.dixa.io/docs/)
- **FastMCP Documentation**: [https://gofastmcp.com](https://gofastmcp.com)
- **MCP Documentation**: [https://modelcontextprotocol.io](https://modelcontextprotocol.io)

## Other Setup Options

If you prefer to run the server yourself, we also support:

- **Local Setup**: Run the server on your own machine
- **Self-Hosted**: Deploy the server on your own infrastructure

For technical details and advanced configuration options, see the main [README.md](https://github.com/Dixa-public/dixa-mcp-public/blob/main/README.md) file.

## License

This project uses FastMCP and integrates with the Dixa API. Please refer to the respective documentation for licensing information.

