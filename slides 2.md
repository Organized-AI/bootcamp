---
theme: seriph
background: https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=1920
class: text-center
highlighter: shiki
lineNumbers: false
info: |
  ## VibeCoders Bootcamp
  6-Week Engineering Principles for AI-Assisted Development
  
  Learn to code WITH AI, not against it!
drawings:
  persist: false
transition: slide-left
title: VibeCoders Bootcamp
mdc: true
---

# VibeCoders Bootcamp

## Engineering Principles for AI-Assisted Development

<div class="pt-12">
  <span @click="$slidev.nav.next" class="px-2 py-1 rounded cursor-pointer" hover="bg-white bg-opacity-10">
    6 Weeks to Transform Your Coding Journey <carbon:arrow-right class="inline"/>
  </span>
</div>

<div class="abs-br m-6 flex gap-2">
  <button @click="$slidev.nav.openInEditor()" title="Open in Editor" class="text-xl slidev-icon-btn opacity-50 !border-none !hover:text-white">
    <carbon:edit />
  </button>
  <a href="https://github.com/Organized-AI/bootcamp" target="_blank" alt="GitHub" title="Open in GitHub"
    class="text-xl slidev-icon-btn opacity-50 !border-none !hover:text-white">
    <carbon-logo-github />
  </a>
</div>

---
transition: fade-out
---

# Welcome to the Future of Coding

<div class="grid grid-cols-2 gap-8 pt-4">

<div>

## Traditional Coding
- Write everything from scratch
- Debug alone for hours
- Stack Overflow diving
- Imposter syndrome
- Slow iteration cycles

</div>

<div>

## Vibe Coding
- **AI as your pair programmer**
- **Instant debugging assistance**
- **Context-aware suggestions**
- **Confidence through collaboration**
- **Rapid prototyping**

</div>

</div>

<style>
h1 {
  background-color: #2B90B6;
  background-image: linear-gradient(45deg, #4EC5D4 10%, #146b8c 20%);
  background-size: 100%;
  -webkit-background-clip: text;
  -moz-background-clip: text;
  -webkit-text-fill-color: transparent;
  -moz-text-fill-color: transparent;
}
</style>

---
layout: two-cols
layoutClass: gap-16
---

# What is Vibe Coding?

<v-clicks>

- 🎯 **Outcome-focused development**
- 🤖 **AI-first approach**
- 🚀 **Rapid iteration**
- 💡 **Learn by building**
- 🎨 **Creative problem-solving**

</v-clicks>

::right::

# MCP Integration

<v-clicks>

- 🔌 **Model Context Protocol**
- 🌐 **Remote connections**
- 📊 **Real-time collaboration**
- 🛠️ **Tool integration**
- 📈 **Enhanced capabilities**

</v-clicks>

---
class: px-20
---

# 6-Week Curriculum Overview

<div class="grid grid-cols-3 gap-4 pt-4">

<div class="bg-blue-500 bg-opacity-20 p-4 rounded">
<h3>Week 1-2: Foundation</h3>

- Dev Environment & Hygiene
- Planning & Architecture
- AI Tools Setup
- MCP Configuration

</div>

<div class="bg-green-500 bg-opacity-20 p-4 rounded">
<h3>Week 3-4: Building</h3>

- Code Generation with AI
- Advanced Implementation
- Debugging with Claude
- Real-world Projects

</div>

<div class="bg-purple-500 bg-opacity-20 p-4 rounded">
<h3>Week 5-6: Shipping</h3>

- Testing & QA
- Deployment & DevOps
- Production Best Practices
- Final Project

</div>

</div>

---

# Week 1: Developer Hygiene & Environment

<div class="grid grid-cols-2 gap-8">

<div>

## Topics Covered
- Setting up your AI-powered IDE
- Version control with Git
- Claude & MCP installation
- Project organization
- Best practices

</div>

<div>

## Hands-on Exercise
```bash
# Set up your first MCP server
npm install -g @modelcontextprotocol/server-cli
mcp-server init my-first-server
mcp-server start
```

</div>

</div>

---

# Week 2: Planning & Architecture

<div class="grid grid-cols-2 gap-8">

<div>

## Design Principles
- System design with AI assistance
- Database schema generation
- API design patterns
- Documentation as code
- Architecture decisions

</div>

<div>

## AI Prompting for Planning
```markdown
"Help me design a REST API for a 
task management system with:
- User authentication
- Project hierarchies
- Real-time updates
- Team collaboration"
```

</div>

</div>

---

# Week 3-4: Creating Code with AI

## The Power of Pair Programming with Claude

<div class="grid grid-cols-2 gap-4 pt-4">

<div>

### Traditional Approach
```python
# Hours of manual coding
def sort_algorithm(arr):
    # Try to remember quicksort
    # Debug for 2 hours
    # Still has edge cases
    pass
```

</div>

<div>

### Vibe Coding Approach
```python
# Ask Claude: "Implement efficient 
# sorting with error handling"
def smart_sort(arr, reverse=False):
    """AI-generated, tested, optimized"""
    return sorted(arr, reverse=reverse)
```

</div>

</div>

<v-click>

### Real Example from Our Curriculum
"Claude, create a full-stack todo app with React, Node.js, and PostgreSQL, including authentication"

**Result**: Working app in 30 minutes vs 3 days

</v-click>

---

# MCP Remote Connection Setup

## Connect to Our Bootcamp Resources

<div class="grid grid-cols-2 gap-8 pt-4">

<div>

### 1. Install MCP Tools
```bash
# Install MCP CLI
npm install -g @modelcontextprotocol/cli

# Configure remote server
mcp config add bootcamp \
  --url https://mcp.organized-ai.com \
  --token YOUR_BOOTCAMP_TOKEN
```

</div>

<div>

### 2. Connect Claude
```json
{
  "mcpServers": {
    "bootcamp": {
      "command": "mcp-remote",
      "args": ["connect", "bootcamp"]
    }
  }
}
```

</div>

</div>

<v-click>

### 3. Access Bootcamp Resources
- 📚 All curriculum materials
- 🎥 Video transcripts
- 💻 Code examples
- 🏆 Challenge solutions

</v-click>

---

# Week 5: Testing & Quality Assurance

<div class="grid grid-cols-2 gap-8">

<div>

## AI-Powered Testing
- Generate test cases automatically
- Coverage analysis
- Edge case discovery
- Performance testing
- Security scanning

</div>

<div>

## Example Test Generation
```javascript
// Ask Claude: "Generate comprehensive 
// tests for this authentication module"

describe('Authentication', () => {
  test('should handle valid login', () => {
    // AI generates complete test suite
  });
});
```

</div>

</div>

---

# Week 6: Deployment & DevOps

## Ship to Production with Confidence

<div class="grid grid-cols-3 gap-4 pt-4">

<div class="bg-opacity-20 bg-blue-500 p-4 rounded">

### CI/CD Pipeline
- GitHub Actions
- Automated testing
- Deployment scripts
- Monitoring setup

</div>

<div class="bg-opacity-20 bg-green-500 p-4 rounded">

### Docker & Cloud
- Containerization
- Cloud deployment
- Scaling strategies
- Cost optimization

</div>

<div class="bg-opacity-20 bg-purple-500 p-4 rounded">

### Production Ready
- Error handling
- Logging & monitoring
- Performance tuning
- Security best practices

</div>

</div>

---

# Final Project Showcase

## Build Something Amazing

<div class="pt-8">

### Project Requirements
- Full-stack application
- AI-assisted development throughout
- MCP integration
- Deployed to production
- Documentation & tests

### Past Student Projects
- 🎮 AI-powered game engine
- 📊 Real-time analytics dashboard
- 🤖 Automated trading bot
- 📱 Mobile app with AI features
- 🌐 Social platform with ML recommendations

</div>

---

# Success Stories

<div class="grid grid-cols-2 gap-8">

<div>

## Before Bootcamp
- 6 months to build an MVP
- Constant debugging frustration
- Limited to simple projects
- Fear of complex systems

</div>

<div>

## After Bootcamp
- **2 weeks to production-ready app**
- **AI handles routine debugging**
- **Building enterprise solutions**
- **Confident system architect**

</div>

</div>

<v-click>

### Alumni Testimonial
> "I went from struggling with basic loops to building a full SaaS platform in 3 weeks. The MCP integration changed everything!" 
> 
> — Sarah Chen, Bootcamp Graduate

</v-click>

---

# Live Demo: MCP in Action

## Let's Build Something Together

<div class="pt-8">

### Live Coding Session
1. Connect to MCP server
2. Generate project structure
3. Implement core features
4. Add tests
5. Deploy to production

**All in 15 minutes!**

</div>

<v-click>

```bash
# Join the live session
mcp connect --session bootcamp-demo-2025
```

</v-click>

---

# Assessment & Certification

<div class="grid grid-cols-2 gap-8">

<div>

## Evaluation Criteria
- 20% Weekly quizzes
- 30% Sandbox exercises
- 30% Coding challenges
- 20% Final project

</div>

<div>

## Certification Levels
- 🥉 **Basic (60%)**: Foundation
- 🥈 **Proficiency (80%)**: Job-ready
- 🥇 **Excellence (100%)**: Senior level

</div>

</div>

<v-click>

### Industry Recognition
- Recognized by 50+ tech companies
- Direct pathway to interviews
- Portfolio-ready projects
- LinkedIn certification badge

</v-click>

---

# Bootcamp Resources

## Everything You Need to Succeed

<div class="grid grid-cols-2 gap-8 pt-4">

<div>

### Included Materials
- 📹 18 video lessons
- 📚 Comprehensive curriculum
- 💻 Code templates
- 🛠️ Development environment
- 🤝 Community access
- 🎯 1-on-1 mentoring

</div>

<div>

### Tech Stack
- **AI**: Claude, GPT-4, Copilot
- **MCP**: Model Context Protocol
- **Frontend**: React, Vue, Next.js
- **Backend**: Node.js, Python
- **Database**: PostgreSQL, Redis
- **Deploy**: Docker, GitHub Pages

</div>

</div>

---

# Join the Revolution

## Start Your Journey Today

<div class="text-center pt-8">

### Enrollment Options

<div class="grid grid-cols-3 gap-4 pt-8">

<div class="border-2 border-blue-500 p-4 rounded">
<h3>Free Trial</h3>

- Week 1 access
- Basic materials
- Community forum

</div>

<div class="border-2 border-green-500 p-4 rounded bg-green-500 bg-opacity-10">
<h3>Full Bootcamp</h3>

- All 6 weeks
- Complete resources
- Mentorship
- **Certification**

</div>

<div class="border-2 border-purple-500 p-4 rounded">
<h3>Enterprise</h3>

- Team training
- Custom curriculum
- Private MCP server
- Dedicated support

</div>

</div>

</div>

---
layout: center
class: text-center
---

# Ready to Code with AI?

<div class="pt-8">

[🚀 Enroll Now](https://organized-ai.github.io/bootcamp/)

[📧 Contact Us](mailto:bootcamp@organized-ai.com)

[💬 Join Discord](https://discord.gg/vibecoders)

[🐙 GitHub Repository](https://github.com/Organized-AI/bootcamp)

</div>

<div class="pt-12">

### Next Cohort Starts Soon!

Limited spots available

</div>

---
layout: end
---

# Thank You!

## Let's Build the Future Together

<div class="pt-8 text-center">

Follow us for updates:

[@OrganizedAI](https://twitter.com/OrganizedAI) | [organized-ai.com](https://organized-ai.com)

</div>
