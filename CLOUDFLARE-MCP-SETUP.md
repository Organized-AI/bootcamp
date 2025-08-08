# Cloudflare MCP Server Configuration

## Setting up Cloudflare DNS MCP Server

To manage DNS records via MCP, add this to your Claude Desktop configuration:

### Location:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

### Configuration:

```json
{
  "mcpServers": {
    "cloudflare-dns": {
      "command": "npx",
      "args": ["-y", "@thelord/mcp-cloudflare"],
      "env": {
        "CLOUDFLARE_API_TOKEN": "your-api-token-here",
        "CLOUDFLARE_ZONE_ID": "your-zone-id-here",
        "CLOUDFLARE_EMAIL": "your-email@example.com"
      }
    }
  }
}
```

## Getting Your Credentials:

### 1. API Token:
1. Go to https://dash.cloudflare.com/profile/api-tokens
2. Click "Create Token"
3. Use template "Edit zone DNS" or create custom with:
   - Zone:DNS:Edit
   - Zone:Zone:Read
4. Scope to your specific zone: `organizedai.vip`

### 2. Zone ID:
1. Go to your domain dashboard
2. Find Zone ID in the right sidebar
3. Copy the ID string

## Available MCP Commands:

Once configured, you can use these commands:

- **List DNS records**: View all records
- **Create DNS record**: Add new CNAME, A, etc.
- **Update DNS record**: Modify existing
- **Delete DNS record**: Remove records

## Example Usage:

"Create a CNAME record for bootcamp pointing to organized-ai.github.io"

## Alternative: Cloudflare Remote MCP Servers

Cloudflare also offers official remote MCP servers that don't require local configuration:

1. **DNS Analytics Server**
2. **DNS Management Server** 
3. **Security Settings Server**

These can be accessed via:
- Claude.ai (with MCP enabled)
- Cloudflare AI Playground
- Other MCP-compatible clients

## For This Specific Task:

To add the CNAME for `bootcamp.organizedai.vip`:

```
Tool: cloudflare-dns
Action: Create DNS Record
Type: CNAME
Name: bootcamp
Target: organized-ai.github.io
Proxy: false (DNS only)
TTL: Auto
```
