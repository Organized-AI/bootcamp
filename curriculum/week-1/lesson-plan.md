# Week 1: Developer Hygiene & Environment Setup

## Overview
Welcome to your journey into AI-assisted development! This week focuses on setting up a professional development environment and establishing good coding practices that will serve you throughout your career.

## Learning Objectives
By the end of this week, you will:
- ✅ Set up a complete AI-powered development environment
- ✅ Configure Claude, GitHub Copilot, and MCP tools
- ✅ Master Git version control fundamentals
- ✅ Understand project organization best practices
- ✅ Create your first AI-assisted project

## Day 1: Environment Setup & Tools

### Morning Session: Development Environment
**Duration:** 90 minutes

#### Setting Up Your IDE
```bash
# Install VSCode or Cursor
brew install --cask visual-studio-code
# or
brew install --cask cursor
```

#### Essential Extensions
1. **Claude for VSCode**
2. **GitHub Copilot**
3. **Prettier - Code formatter**
4. **ESLint**
5. **GitLens**

### Hands-On Exercise: Configure Your Environment
```javascript
// .vscode/settings.json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "github.copilot.enable": {
    "*": true
  }
}
```

### Afternoon Session: AI Tools Setup
**Duration:** 90 minutes

#### Installing Claude Desktop
1. Download from https://claude.ai/download
2. Configure MCP servers
3. Set up API keys

#### MCP Configuration
```json
// ~/Library/Application Support/Claude/claude_desktop_config.json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/projects"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"]
    }
  }
}
```

## Day 2: Version Control with Git

### Morning Session: Git Fundamentals
**Duration:** 90 minutes

#### Basic Git Commands
```bash
# Initialize a repository
git init

# Configure user
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Basic workflow
git add .
git commit -m "Initial commit"
git push origin main
```

#### AI-Assisted Commit Messages
```bash
# Use Claude to generate commit messages
alias commit-ai='git diff --staged | claude "Generate a conventional commit message for these changes"'
```

### Hands-On Exercise: Create Your First Repository
1. Create a new project
2. Initialize Git
3. Make your first commit
4. Push to GitHub

### Afternoon Session: Advanced Git with AI
**Duration:** 90 minutes

#### Using AI for Git Operations
```javascript
// git-helper.js
const { exec } = require('child_process');
const { Configuration, OpenAIApi } = require('openai');

async function generateCommitMessage(diff) {
  const response = await openai.createCompletion({
    model: "gpt-4",
    prompt: `Generate a conventional commit message for:\n${diff}`,
    max_tokens: 100
  });
  return response.data.choices[0].text.trim();
}
```

## Day 3: Project Organization

### Morning Session: Project Structure
**Duration:** 90 minutes

#### Standard Project Layout
```
my-project/
├── src/
│   ├── components/
│   ├── utils/
│   ├── services/
│   └── index.js
├── tests/
├── docs/
├── .github/
│   └── workflows/
├── .gitignore
├── README.md
├── package.json
└── docker-compose.yml
```

#### Creating Templates with AI
```bash
# Use Claude to generate project structure
claude "Create a Node.js project structure for a REST API with authentication"
```

### Hands-On Exercise: Build a Project Template
Create a reusable project template with:
- Folder structure
- Configuration files
- Docker setup
- CI/CD pipeline

### Afternoon Session: Documentation
**Duration:** 90 minutes

#### AI-Powered Documentation
```javascript
// Generate README with AI
async function generateReadme(projectInfo) {
  const prompt = `Generate a comprehensive README.md for:
    Project: ${projectInfo.name}
    Tech Stack: ${projectInfo.stack}
    Features: ${projectInfo.features}`;
  
  return await claude.complete(prompt);
}
```

## Day 4: Development Best Practices

### Morning Session: Code Quality
**Duration:** 90 minutes

#### Setting Up Linters and Formatters
```json
// .eslintrc.json
{
  "extends": ["eslint:recommended", "plugin:react/recommended"],
  "rules": {
    "indent": ["error", 2],
    "quotes": ["error", "single"],
    "semi": ["error", "always"]
  }
}
```

#### Pre-commit Hooks
```json
// package.json
{
  "husky": {
    "hooks": {
      "pre-commit": "lint-staged"
    }
  },
  "lint-staged": {
    "*.js": ["eslint --fix", "prettier --write"]
  }
}
```

### Hands-On Exercise: Implement Code Quality Tools
1. Set up ESLint
2. Configure Prettier
3. Add pre-commit hooks
4. Create custom rules

### Afternoon Session: Testing Fundamentals
**Duration:** 90 minutes

#### AI-Generated Tests
```javascript
// Use AI to generate tests
const generateTests = async (functionCode) => {
  const prompt = `Generate Jest tests for this function:\n${functionCode}`;
  return await claude.complete(prompt);
};

// Example test
describe('Calculator', () => {
  test('adds two numbers', () => {
    expect(add(2, 3)).toBe(5);
  });
});
```

## Day 5: Practical Project

### Full Day Project: Build a Task Manager CLI
**Duration:** 3 hours

#### Requirements
- Command-line interface
- Add, list, complete tasks
- Data persistence
- Git integration
- AI-powered features

#### Starter Code
```javascript
#!/usr/bin/env node
// task-manager.js
const { Command } = require('commander');
const fs = require('fs').promises;
const path = require('path');

const program = new Command();
const TASKS_FILE = path.join(process.env.HOME, '.tasks.json');

// AI-powered task suggestions
async function suggestTask(context) {
  const prompt = `Based on ${context}, suggest a next task:`;
  return await claude.complete(prompt);
}

program
  .name('task')
  .description('AI-powered task manager')
  .version('1.0.0');

program
  .command('add <task>')
  .description('Add a new task')
  .action(async (task) => {
    const tasks = await loadTasks();
    tasks.push({
      id: Date.now(),
      task,
      completed: false,
      created: new Date()
    });
    await saveTasks(tasks);
    console.log(`✅ Added: ${task}`);
  });

program
  .command('list')
  .description('List all tasks')
  .action(async () => {
    const tasks = await loadTasks();
    tasks.forEach(t => {
      const status = t.completed ? '✅' : '⬜';
      console.log(`${status} [${t.id}] ${t.task}`);
    });
  });

program
  .command('suggest')
  .description('Get AI task suggestion')
  .action(async () => {
    const tasks = await loadTasks();
    const context = tasks.map(t => t.task).join(', ');
    const suggestion = await suggestTask(context);
    console.log(`💡 Suggestion: ${suggestion}`);
  });

async function loadTasks() {
  try {
    const data = await fs.readFile(TASKS_FILE, 'utf8');
    return JSON.parse(data);
  } catch {
    return [];
  }
}

async function saveTasks(tasks) {
  await fs.writeFile(TASKS_FILE, JSON.stringify(tasks, null, 2));
}

program.parse();
```

## Weekend Assignment

### Create Your Development Portfolio
1. Set up a personal GitHub profile
2. Create a portfolio website
3. Document your learning journey
4. Build a simple project with AI assistance

### Required Deliverables
- [ ] GitHub repository with proper structure
- [ ] README with comprehensive documentation
- [ ] At least 10 meaningful commits
- [ ] One working application
- [ ] MCP server configuration

## Assessment Rubric

| Criteria | Basic (60%) | Proficient (80%) | Advanced (100%) |
|----------|-------------|------------------|-----------------|
| Environment Setup | IDE installed | All tools configured | Custom configurations |
| Git Usage | Basic commands | Branching strategy | Advanced workflows |
| Project Structure | Standard layout | Well-organized | Template created |
| Documentation | Basic README | Comprehensive docs | API documentation |
| Code Quality | Runs without errors | Linted and formatted | Custom rules |

## Resources

### Required Reading
- [The Pragmatic Programmer](https://pragprog.com/titles/tpp20/)
- [Clean Code principles](https://www.freecodecamp.org/news/clean-coding-for-beginners/)
- [Git Documentation](https://git-scm.com/doc)

### Video Tutorials
- [Setting up Claude MCP](https://youtube.com/watch?v=example)
- [Git workflow best practices](https://youtube.com/watch?v=example)
- [VS Code productivity tips](https://youtube.com/watch?v=example)

### Additional Tools
- **TablePlus**: Database management
- **Postman**: API testing
- **Docker Desktop**: Containerization
- **iTerm2**: Enhanced terminal

## Office Hours

**Thursday, 3-5 PM EST**
- Live coding session
- Q&A
- Code reviews
- Troubleshooting

## Next Week Preview

Week 2: Planning & Architecture
- System design principles
- Database design
- API architecture
- Cloud services
- AI-assisted planning

---

💡 **Pro Tips:**
- Commit early and often
- Write descriptive commit messages
- Keep your workspace organized
- Use AI as a learning tool, not a crutch
- Ask questions in the Discord channel

🎯 **Success Metrics:**
- Complete all daily exercises
- Submit weekend project
- Participate in discussions
- Help at least one peer

Ready to start your journey? Let's code! 🚀
