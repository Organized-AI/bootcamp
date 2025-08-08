# VibeCoders Bootcamp - MCP Remote Connection Guide

## Model Context Protocol Integration

This bootcamp leverages the Model Context Protocol (MCP) to enable remote connections and enhanced AI capabilities.

### What is MCP?

The Model Context Protocol (MCP) is an open protocol that enables seamless integration between AI assistants like Claude and external data sources and tools. It provides:

- 🔌 **Standardized connections** to various data sources
- 🛠️ **Tool integration** for enhanced capabilities  
- 📊 **Real-time data access** during conversations
- 🔒 **Secure authentication** and authorization

### Setting Up MCP for the Bootcamp

#### 1. Install MCP Server

```bash
# Install globally
npm install -g @modelcontextprotocol/server

# Or add to your project
npm install @modelcontextprotocol/server
```

#### 2. Configure Claude Desktop

Add to your Claude configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "vibecoder-bootcamp": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-github",
        "https://github.com/Organized-AI/bootcamp"
      ]
    },
    "bootcamp-filesystem": {
      "command": "npx",
      "args": [
        "-y", 
        "@modelcontextprotocol/server-filesystem",
        "/path/to/your/bootcamp/folder"
      ]
    }
  }
}
```

#### 3. Remote MCP Connection

For remote collaboration and resource access:

```bash
# Connect to bootcamp MCP server
mcp connect --remote https://mcp.organized-ai.com/bootcamp

# Authenticate with your bootcamp credentials
mcp auth --token YOUR_BOOTCAMP_TOKEN
```

### Available MCP Tools

Once connected, you'll have access to:

#### 📚 **Curriculum Access**
- Full curriculum documents
- Weekly lesson plans
- Exercise solutions
- Video transcripts

#### 🛠️ **Development Tools**
- Code generation
- Debugging assistance
- Test generation
- Documentation creation

#### 📊 **Analytics & Progress**
- Track your learning progress
- Performance metrics
- Peer comparisons
- Certification tracking

#### 🤝 **Collaboration Features**
- Pair programming sessions
- Code reviews
- Mentorship connections
- Group projects

### MCP Commands Reference

```bash
# List available MCP servers
mcp list

# Connect to bootcamp server
mcp connect vibecoder-bootcamp

# Check connection status
mcp status

# Access bootcamp resources
mcp resource get curriculum/week-1

# Submit exercises
mcp submit exercise-1 solution.js

# Get AI assistance
mcp assist "Help me debug this function"
```

### Troubleshooting

#### Connection Issues

If you can't connect to the MCP server:

1. Check your internet connection
2. Verify your authentication token
3. Ensure MCP CLI is up to date:
   ```bash
   npm update -g @modelcontextprotocol/server
   ```

#### Permission Errors

If you get permission denied errors:
- Verify your bootcamp enrollment status
- Check token expiration
- Contact support@organized-ai.com

#### Resource Access

If resources aren't loading:
- Clear MCP cache: `mcp cache clear`
- Reconnect to server: `mcp reconnect`
- Check server status: https://status.organized-ai.com

### Advanced MCP Features

#### Custom MCP Servers

Create your own MCP server for projects:

```javascript
// mcp-server.js
import { Server } from '@modelcontextprotocol/server';

const server = new Server({
  name: 'my-project-mcp',
  version: '1.0.0',
  capabilities: {
    resources: true,
    tools: true
  }
});

// Add custom tools
server.addTool({
  name: 'generate_code',
  description: 'Generate code based on requirements',
  inputSchema: {
    type: 'object',
    properties: {
      language: { type: 'string' },
      requirements: { type: 'string' }
    }
  },
  handler: async (params) => {
    // Implementation
    return generatedCode;
  }
});

server.start();
```

#### MCP with GitHub Integration

Connect your GitHub repository:

```json
{
  "mcpServers": {
    "github-bootcamp": {
      "command": "mcp-github",
      "args": [
        "--repo", "Organized-AI/bootcamp",
        "--branch", "main",
        "--token", "$GITHUB_TOKEN"
      ]
    }
  }
}
```

### Resources

- 📖 [MCP Documentation](https://modelcontextprotocol.io)
- 🎥 [MCP Video Tutorials](https://youtube.com/playlist?MCP)
- 💬 [MCP Discord Community](https://discord.gg/mcp)
- 🐙 [MCP GitHub](https://github.com/modelcontextprotocol)

### Support

For MCP-related support:
- Email: mcp-support@organized-ai.com
- Discord: #mcp-help channel
- Office Hours: Thursdays 3-5pm EST

---

© 2025 Organized AI - VibeCoders Bootcamp
