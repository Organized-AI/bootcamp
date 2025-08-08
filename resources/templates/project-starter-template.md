# Project Starter Template

## 🚀 Quick Start Guide for New Projects

This template provides a standardized structure for all bootcamp projects. Copy this structure when starting any new project.

### Project Structure

```bash
my-awesome-project/
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI/CD pipeline
├── .vscode/
│   ├── settings.json           # VS Code workspace settings
│   └── extensions.json         # Recommended extensions
├── src/
│   ├── frontend/
│   │   ├── components/         # React/Vue components
│   │   ├── pages/             # Page components
│   │   ├── hooks/             # Custom hooks
│   │   ├── utils/             # Utility functions
│   │   └── styles/            # CSS/SCSS files
│   ├── backend/
│   │   ├── controllers/       # Route controllers
│   │   ├── models/           # Database models
│   │   ├── services/         # Business logic
│   │   ├── middleware/       # Express middleware
│   │   ├── routes/           # API routes
│   │   └── utils/            # Backend utilities
│   └── shared/
│       ├── types/            # TypeScript types
│       └── constants/        # Shared constants
├── tests/
│   ├── unit/                 # Unit tests
│   ├── integration/          # Integration tests
│   └── e2e/                  # End-to-end tests
├── scripts/
│   ├── setup.sh             # Project setup script
│   ├── clean.sh             # Cleanup script
│   └── deploy.sh            # Deployment script
├── docs/
│   ├── API.md               # API documentation
│   ├── ARCHITECTURE.md      # Architecture decisions
│   └── CONTRIBUTING.md      # Contribution guidelines
├── infrastructure/
│   ├── docker/
│   │   ├── Dockerfile       # Docker configuration
│   │   └── docker-compose.yml
│   └── k8s/
│       ├── deployment.yaml  # Kubernetes deployment
│       └── service.yaml     # Kubernetes service
├── .env.example             # Environment variables template
├── .gitignore              # Git ignore file
├── .prettierrc             # Prettier configuration
├── .eslintrc.js            # ESLint configuration
├── package.json            # Node.js dependencies
├── tsconfig.json           # TypeScript configuration
└── README.md               # Project documentation
```

### Essential Configuration Files

#### `.env.example`
```env
# Application
NODE_ENV=development
PORT=3000
API_URL=http://localhost:3000

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
REDIS_URL=redis://localhost:6379

# Authentication
JWT_SECRET=your-secret-key-here
JWT_EXPIRES_IN=7d

# External Services
OPENAI_API_KEY=sk-...
CLAUDE_API_KEY=sk-ant-...
STRIPE_API_KEY=sk_test_...

# Monitoring
SENTRY_DSN=https://...@sentry.io/...
LOG_LEVEL=debug
```

#### `package.json`
```json
{
  "name": "my-awesome-project",
  "version": "1.0.0",
  "description": "AI-powered application built during VibeCoders Bootcamp",
  "scripts": {
    "dev": "concurrently \"npm run dev:backend\" \"npm run dev:frontend\"",
    "dev:backend": "nodemon src/backend/server.js",
    "dev:frontend": "vite",
    "build": "npm run build:frontend && npm run build:backend",
    "build:frontend": "vite build",
    "build:backend": "tsc",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "lint": "eslint . --ext .js,.jsx,.ts,.tsx",
    "format": "prettier --write \"**/*.{js,jsx,ts,tsx,json,md}\"",
    "docker:build": "docker-compose build",
    "docker:up": "docker-compose up",
    "docker:down": "docker-compose down"
  },
  "dependencies": {
    "express": "^4.18.0",
    "react": "^18.2.0",
    "postgresql": "^1.0.0",
    "socket.io": "^4.5.0",
    "jsonwebtoken": "^9.0.0",
    "bcryptjs": "^2.4.3"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "typescript": "^5.0.0",
    "jest": "^29.0.0",
    "eslint": "^8.0.0",
    "prettier": "^3.0.0",
    "nodemon": "^3.0.0",
    "vite": "^4.0.0"
  }
}
```

#### `.gitignore`
```gitignore
# Dependencies
node_modules/
package-lock.json
yarn.lock
pnpm-lock.yaml

# Environment variables
.env
.env.local
.env.*.local

# Build outputs
dist/
build/
out/
.next/
.nuxt/

# Logs
logs/
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Editor directories
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Testing
coverage/
.nyc_output/

# Docker
*.pid
*.seed
*.pid.lock

# Temporary files
tmp/
temp/
```

#### `README.md` Template
```markdown
# Project Name

![Build Status](https://github.com/yourusername/project/workflows/CI/badge.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📋 Description

Brief description of what this project does and its main features.

## 🚀 Features

- ✅ Feature 1
- ✅ Feature 2
- ✅ Feature 3
- 🚧 Feature 4 (in progress)

## 🛠️ Tech Stack

- **Frontend**: React, TypeScript, Tailwind CSS
- **Backend**: Node.js, Express, PostgreSQL
- **AI**: Claude API, OpenAI
- **DevOps**: Docker, GitHub Actions
- **Testing**: Jest, Playwright

## 📦 Installation

### Prerequisites
- Node.js 18+
- Docker Desktop
- Git

### Setup Steps

1. Clone the repository
\`\`\`bash
git clone https://github.com/yourusername/project.git
cd project
\`\`\`

2. Install dependencies
\`\`\`bash
npm install
\`\`\`

3. Set up environment variables
\`\`\`bash
cp .env.example .env
# Edit .env with your values
\`\`\`

4. Start the development server
\`\`\`bash
npm run dev
\`\`\`

## 🧪 Testing

\`\`\`bash
# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run specific test suite
npm test -- --testPathPattern=user
\`\`\`

## 🐳 Docker

\`\`\`bash
# Build and run with Docker Compose
docker-compose up --build

# Run in background
docker-compose up -d

# Stop containers
docker-compose down
\`\`\`

## 📚 API Documentation

See [API.md](docs/API.md) for detailed API documentation.

## 🤝 Contributing

Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) for contribution guidelines.

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

## 👥 Team

- Your Name (@github-username)
- Team Member (@github-username)

## 🙏 Acknowledgments

- VibeCoders Bootcamp
- Claude AI for assistance
- Open source community
```

### Git Workflow

#### Initial Setup
```bash
# Initialize git repository
git init

# Add all files
git add .

# Initial commit
git commit -m "feat: initial project setup"

# Add remote repository
git remote add origin https://github.com/yourusername/project.git

# Push to main branch
git push -u origin main
```

#### Branch Strategy
```bash
# Create feature branch
git checkout -b feature/user-authentication

# Work on feature
# ... make changes ...

# Commit changes
git add .
git commit -m "feat: add user authentication"

# Push feature branch
git push origin feature/user-authentication

# Create pull request on GitHub
# After review and approval, merge to main
```

### VS Code Settings

#### `.vscode/settings.json`
```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "typescript.tsdk": "node_modules/typescript/lib",
  "files.exclude": {
    "**/.git": true,
    "**/.DS_Store": true,
    "**/node_modules": true,
    "**/dist": true
  }
}
```

#### `.vscode/extensions.json`
```json
{
  "recommendations": [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "ms-vscode.vscode-typescript-next",
    "christian-kohler.npm-intellisense",
    "eg2.vscode-npm-script",
    "ms-azuretools.vscode-docker",
    "github.copilot",
    "continue.continue"
  ]
}
```

### Docker Configuration

#### `Dockerfile`
```dockerfile
# Multi-stage build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:18-alpine AS runtime
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY --from=builder /app/dist ./dist
EXPOSE 3000
CMD ["node", "dist/server.js"]
```

#### `docker-compose.yml`
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://user:password@db:5432/myapp
    depends_on:
      - db
      - redis
    volumes:
      - .:/app
      - /app/node_modules

  db:
    image: postgres:14
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

### GitHub Actions CI/CD

#### `.github/workflows/ci.yml`
```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Run linter
      run: npm run lint
    
    - name: Run tests
      run: npm test
    
    - name: Build application
      run: npm run build
```

## Quick Commands Reference

```bash
# Development
npm run dev              # Start development server
npm run build           # Build for production
npm run preview         # Preview production build

# Testing
npm test                # Run tests
npm run test:watch      # Watch mode
npm run test:coverage   # Coverage report

# Code Quality
npm run lint            # Run ESLint
npm run format          # Run Prettier
npm run type-check      # TypeScript check

# Docker
docker-compose up       # Start all services
docker-compose down     # Stop all services
docker-compose logs -f  # View logs

# Git
git status              # Check status
git add .               # Stage changes
git commit -m "msg"     # Commit
git push                # Push to remote
git pull                # Pull from remote
```

## Next Steps

1. Copy this template to your project directory
2. Customize configuration files for your needs
3. Set up your GitHub repository
4. Configure CI/CD pipeline
5. Start building! 🚀

Remember: **"Work it until you solve it!"**
