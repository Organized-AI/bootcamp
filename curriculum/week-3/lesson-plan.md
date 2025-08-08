# Week 3: Creating Code - Part 1 (Fundamentals)

## Overview
This week marks your transformation from coder to "vibe coder" - someone who leverages AI as a true pair programming partner. You'll learn to generate, understand, and refine code at 10x speed.

## Learning Objectives
By the end of this week, you will:
- ✅ Master AI pair programming techniques
- ✅ Generate complete features with prompts
- ✅ Refactor code using AI assistance
- ✅ Debug complex issues with AI
- ✅ Build a full-stack application in hours, not days

## Day 1: AI Pair Programming Fundamentals

### Morning Session: Effective Prompting for Code
**Duration:** 90 minutes

#### The Art of Code Prompting
```javascript
// Bad prompt:
"Make a login form"

// Good prompt:
"Create a React login form component with:
- Email and password fields
- Form validation (email format, password min 8 chars)
- Loading state during submission
- Error message display
- Accessibility attributes
- Tailwind CSS styling
- TypeScript interfaces
- Unit tests with Jest"
```

#### Prompt Templates for Common Tasks
```javascript
// Feature Implementation Template
const featurePrompt = `
Create a ${featureName} feature with:
Tech Stack: ${techStack}
Requirements:
${requirements.map(r => `- ${r}`).join('\n')}
Include:
- Error handling
- Loading states
- TypeScript types
- Unit tests
- Documentation
`;

// Debugging Template
const debugPrompt = `
Debug this error:
Error: ${errorMessage}
Code: ${codeSnippet}
Context: ${contextDescription}
Expected behavior: ${expected}
Actual behavior: ${actual}
`;

// Refactoring Template
const refactorPrompt = `
Refactor this code for:
- Performance optimization
- Better readability
- SOLID principles
- Remove code smells
Current code: ${currentCode}
`;
```

### Hands-On Exercise: Build a Chat Application
```javascript
// Step 1: Generate the backend with Claude
const backendPrompt = `
Create a real-time chat backend with:
- Socket.io for WebSockets
- Express server
- MongoDB for message storage
- JWT authentication
- Room support
- Typing indicators
- Message history
- User presence tracking
`;

// Generated backend code
const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const jwt = require('jsonwebtoken');
const mongoose = require('mongoose');

const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
  cors: {
    origin: "http://localhost:3000",
    methods: ["GET", "POST"]
  }
});

// Message Schema
const messageSchema = new mongoose.Schema({
  room: String,
  user: String,
  message: String,
  timestamp: { type: Date, default: Date.now }
});

const Message = mongoose.model('Message', messageSchema);

// Socket authentication middleware
io.use((socket, next) => {
  const token = socket.handshake.auth.token;
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    socket.userId = decoded.userId;
    socket.username = decoded.username;
    next();
  } catch (err) {
    next(new Error('Authentication error'));
  }
});

// Socket connection handling
io.on('connection', (socket) => {
  console.log(`User ${socket.username} connected`);
  
  // Join room
  socket.on('join-room', async (roomId) => {
    socket.join(roomId);
    
    // Send message history
    const messages = await Message.find({ room: roomId })
      .sort('-timestamp')
      .limit(50);
    socket.emit('message-history', messages.reverse());
    
    // Notify others
    socket.to(roomId).emit('user-joined', {
      userId: socket.userId,
      username: socket.username
    });
  });
  
  // Handle messages
  socket.on('send-message', async (data) => {
    const message = new Message({
      room: data.room,
      user: socket.username,
      message: data.message
    });
    
    await message.save();
    
    io.to(data.room).emit('new-message', {
      id: message._id,
      user: socket.username,
      message: data.message,
      timestamp: message.timestamp
    });
  });
  
  // Typing indicator
  socket.on('typing', (data) => {
    socket.to(data.room).emit('user-typing', {
      userId: socket.userId,
      username: socket.username
    });
  });
  
  socket.on('stop-typing', (data) => {
    socket.to(data.room).emit('user-stop-typing', {
      userId: socket.userId
    });
  });
  
  socket.on('disconnect', () => {
    io.emit('user-disconnected', {
      userId: socket.userId,
      username: socket.username
    });
  });
});

server.listen(3001, () => {
  console.log('Chat server running on port 3001');
});
```

### Afternoon Session: Frontend Generation
**Duration:** 90 minutes

#### Generate React Components with AI
```jsx
// Step 2: Generate the frontend with Claude
const frontendPrompt = `
Create a React chat UI with:
- Message list component
- Input component with emoji support
- User list sidebar
- Typing indicators
- Auto-scroll to newest messages
- Responsive design with Tailwind
- Dark mode support
- React hooks for state
`;

// Generated React component
import React, { useState, useEffect, useRef } from 'react';
import io from 'socket.io-client';
import EmojiPicker from 'emoji-picker-react';

const ChatApp = () => {
  const [socket, setSocket] = useState(null);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [typingUsers, setTypingUsers] = useState([]);
  const [showEmojiPicker, setShowEmojiPicker] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const messagesEndRef = useRef(null);
  const typingTimeout = useRef(null);
  
  useEffect(() => {
    const newSocket = io('http://localhost:3001', {
      auth: {
        token: localStorage.getItem('token')
      }
    });
    
    setSocket(newSocket);
    
    newSocket.on('connect', () => {
      newSocket.emit('join-room', 'general');
    });
    
    newSocket.on('message-history', (history) => {
      setMessages(history);
    });
    
    newSocket.on('new-message', (message) => {
      setMessages(prev => [...prev, message]);
      scrollToBottom();
    });
    
    newSocket.on('user-typing', (user) => {
      setTypingUsers(prev => [...prev.filter(u => u.userId !== user.userId), user]);
    });
    
    newSocket.on('user-stop-typing', (user) => {
      setTypingUsers(prev => prev.filter(u => u.userId !== user.userId));
    });
    
    return () => newSocket.close();
  }, []);
  
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };
  
  const sendMessage = (e) => {
    e.preventDefault();
    if (inputMessage.trim() && socket) {
      socket.emit('send-message', {
        room: 'general',
        message: inputMessage
      });
      setInputMessage('');
      handleStopTyping();
    }
  };
  
  const handleTyping = () => {
    if (socket) {
      socket.emit('typing', { room: 'general' });
      
      clearTimeout(typingTimeout.current);
      typingTimeout.current = setTimeout(() => {
        handleStopTyping();
      }, 1000);
    }
  };
  
  const handleStopTyping = () => {
    if (socket) {
      socket.emit('stop-typing', { room: 'general' });
    }
  };
  
  const onEmojiClick = (emojiObject) => {
    setInputMessage(prev => prev + emojiObject.emoji);
    setShowEmojiPicker(false);
  };
  
  return (
    <div className={`flex h-screen ${darkMode ? 'dark bg-gray-900' : 'bg-gray-100'}`}>
      {/* Sidebar */}
      <div className="w-64 bg-white dark:bg-gray-800 border-r dark:border-gray-700">
        <div className="p-4">
          <h2 className="text-xl font-bold dark:text-white">Chat Rooms</h2>
          <div className="mt-4">
            <div className="p-2 bg-blue-100 dark:bg-blue-900 rounded">
              # general
            </div>
          </div>
        </div>
      </div>
      
      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="bg-white dark:bg-gray-800 border-b dark:border-gray-700 p-4 flex justify-between">
          <h1 className="text-xl font-bold dark:text-white"># general</h1>
          <button
            onClick={() => setDarkMode(!darkMode)}
            className="p-2 rounded hover:bg-gray-200 dark:hover:bg-gray-700"
          >
            {darkMode ? '☀️' : '🌙'}
          </button>
        </div>
        
        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((msg) => (
            <div key={msg.id} className="flex items-start space-x-3">
              <div className="w-10 h-10 rounded-full bg-blue-500 flex items-center justify-center text-white">
                {msg.user[0].toUpperCase()}
              </div>
              <div className="flex-1">
                <div className="flex items-baseline space-x-2">
                  <span className="font-semibold dark:text-white">{msg.user}</span>
                  <span className="text-xs text-gray-500">
                    {new Date(msg.timestamp).toLocaleTimeString()}
                  </span>
                </div>
                <p className="text-gray-800 dark:text-gray-200">{msg.message}</p>
              </div>
            </div>
          ))}
          
          {/* Typing Indicators */}
          {typingUsers.length > 0 && (
            <div className="italic text-gray-500">
              {typingUsers.map(u => u.username).join(', ')} typing...
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
        
        {/* Input Area */}
        <div className="bg-white dark:bg-gray-800 border-t dark:border-gray-700 p-4">
          <form onSubmit={sendMessage} className="flex space-x-2">
            <button
              type="button"
              onClick={() => setShowEmojiPicker(!showEmojiPicker)}
              className="p-2 hover:bg-gray-200 dark:hover:bg-gray-700 rounded"
            >
              😊
            </button>
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleTyping}
              placeholder="Type a message..."
              className="flex-1 p-2 border rounded dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            />
            <button
              type="submit"
              className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              Send
            </button>
          </form>
          
          {showEmojiPicker && (
            <div className="absolute bottom-20">
              <EmojiPicker onEmojiClick={onEmojiClick} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChatApp;
```

## Day 2: Code Generation Patterns

### Morning Session: Component Generation
**Duration:** 90 minutes

#### AI-Powered Component Factory
```javascript
// component-generator.js
class ComponentGenerator {
  constructor(ai) {
    this.ai = ai;
  }
  
  async generateComponent(spec) {
    const prompt = `
      Generate a React component:
      Name: ${spec.name}
      Type: ${spec.type} // 'functional' | 'class'
      Props: ${JSON.stringify(spec.props)}
      State: ${JSON.stringify(spec.state)}
      Features: ${spec.features.join(', ')}
      Styling: ${spec.styling} // 'tailwind' | 'styled-components' | 'css-modules'
      Testing: ${spec.includeTesting}
      
      Include:
      - PropTypes or TypeScript interfaces
      - JSDoc comments
      - Error boundaries if needed
      - Performance optimizations
      - Accessibility features
    `;
    
    const component = await this.ai.generate(prompt);
    const test = spec.includeTesting ? 
      await this.generateTests(spec.name, component) : null;
    
    return { component, test };
  }
  
  async generateTests(componentName, componentCode) {
    const prompt = `
      Generate comprehensive tests for this React component:
      ${componentCode}
      
      Include:
      - Unit tests with Jest
      - React Testing Library tests
      - Edge cases
      - User interaction tests
      - Accessibility tests
      - Snapshot tests
    `;
    
    return await this.ai.generate(prompt);
  }
}

// Usage
const generator = new ComponentGenerator(claude);

const spec = {
  name: 'DataTable',
  type: 'functional',
  props: {
    data: 'array',
    columns: 'array',
    onSort: 'function',
    onFilter: 'function'
  },
  state: ['sortColumn', 'sortDirection', 'filters'],
  features: ['sorting', 'filtering', 'pagination', 'row selection', 'export'],
  styling: 'tailwind',
  includeTesting: true
};

const { component, test } = await generator.generateComponent(spec);
```

### Hands-On Exercise: Build a Dashboard
```javascript
// Generate complete dashboard with AI
const dashboardPrompt = `
Create a React admin dashboard with:
1. Sidebar navigation
2. Header with user menu
3. Main content area
4. Charts (use recharts)
5. Data tables
6. Cards with statistics
7. Responsive design
8. Dark mode toggle
9. Real-time updates with WebSocket
10. Export functionality

Use TypeScript and Tailwind CSS
`;

// The AI generates complete dashboard...
```

### Afternoon Session: API Generation
**Duration:** 90 minutes

#### Generate Complete APIs
```javascript
// api-generator.js
async function generateAPI(specification) {
  const prompts = {
    models: `Generate Sequelize models for: ${specification.entities}`,
    controllers: `Generate Express controllers with CRUD operations for: ${specification.entities}`,
    routes: `Generate Express routes with authentication middleware for: ${specification.entities}`,
    middleware: `Generate middleware for: authentication, validation, error handling, rate limiting`,
    tests: `Generate API tests using Jest and Supertest`
  };
  
  const api = {};
  
  for (const [key, prompt] of Object.entries(prompts)) {
    api[key] = await claude.generate(prompt);
  }
  
  return api;
}

// Example specification
const blogAPI = await generateAPI({
  entities: ['User', 'Post', 'Comment', 'Category', 'Tag'],
  authentication: 'JWT',
  database: 'PostgreSQL',
  features: ['search', 'pagination', 'filtering', 'sorting']
});
```

## Day 3: Refactoring with AI

### Morning Session: Code Improvement
**Duration:** 90 minutes

#### AI-Powered Refactoring
```javascript
// refactor-assistant.js
class RefactorAssistant {
  async analyzeCode(code) {
    const prompt = `
      Analyze this code for:
      1. Code smells
      2. Performance issues
      3. Security vulnerabilities
      4. Accessibility problems
      5. Best practice violations
      
      Code: ${code}
      
      Provide specific recommendations with examples.
    `;
    
    return await claude.analyze(prompt);
  }
  
  async refactor(code, goals) {
    const prompt = `
      Refactor this code to achieve:
      ${goals.map(g => `- ${g}`).join('\n')}
      
      Original code: ${code}
      
      Maintain functionality while improving:
      - Readability
      - Performance
      - Maintainability
      - Testability
    `;
    
    return await claude.refactor(prompt);
  }
  
  async optimizePerformance(code) {
    const prompt = `
      Optimize this code for performance:
      ${code}
      
      Consider:
      - Time complexity
      - Space complexity
      - Database queries
      - Caching opportunities
      - Async operations
      - Memory leaks
    `;
    
    return await claude.optimize(prompt);
  }
}

// Example usage
const assistant = new RefactorAssistant();

// Before refactoring
const messyCode = `
function getData(id) {
  let result;
  for (let i = 0; i < data.length; i++) {
    if (data[i].id == id) {
      result = data[i];
      break;
    }
  }
  return result;
}
`;

// After AI refactoring
const cleanCode = await assistant.refactor(messyCode, [
  'Use modern JavaScript',
  'Improve performance',
  'Add error handling',
  'Add TypeScript types'
]);

// Result:
interface DataItem {
  id: string;
  [key: string]: any;
}

const getData = (id: string): DataItem | undefined => {
  if (!id) {
    throw new Error('ID is required');
  }
  
  return data.find((item: DataItem) => item.id === id);
};
```

### Hands-On Exercise: Refactor Legacy Code
Transform a legacy jQuery application to modern React

### Afternoon Session: Design Patterns
**Duration:** 90 minutes

#### Implement Patterns with AI
```javascript
// pattern-implementer.js
const patterns = {
  singleton: `
    Implement Singleton pattern for: ${className}
    Ensure thread safety and lazy initialization
  `,
  
  factory: `
    Implement Factory pattern for creating: ${productTypes}
    Include abstract factory if needed
  `,
  
  observer: `
    Implement Observer pattern for: ${subject}
    Include event emitter functionality
  `,
  
  strategy: `
    Implement Strategy pattern for: ${algorithms}
    Allow runtime strategy switching
  `,
  
  decorator: `
    Implement Decorator pattern for: ${baseClass}
    Add features: ${features}
  `
};

// Generate pattern implementation
async function implementPattern(patternName, context) {
  const prompt = patterns[patternName];
  return await claude.generate(prompt, context);
}
```

## Day 4: Debugging with AI

### Morning Session: AI-Powered Debugging
**Duration:** 90 minutes

#### Debug Assistant
```javascript
// debug-assistant.js
class DebugAssistant {
  async diagnoseError(error, context) {
    const prompt = `
      Diagnose this error:
      Error: ${error.message}
      Stack: ${error.stack}
      Code context: ${context.code}
      Environment: ${context.environment}
      
      Provide:
      1. Root cause analysis
      2. Immediate fix
      3. Long-term solution
      4. Prevention strategies
    `;
    
    return await claude.diagnose(prompt);
  }
  
  async findBug(symptoms) {
    const prompt = `
      Find the bug based on symptoms:
      Expected: ${symptoms.expected}
      Actual: ${symptoms.actual}
      Code: ${symptoms.code}
      Steps to reproduce: ${symptoms.steps}
      
      Identify:
      1. Likely bug location
      2. Root cause
      3. Fix recommendation
      4. Test cases to prevent regression
    `;
    
    return await claude.findBug(prompt);
  }
  
  async generateDebugCode(issue) {
    const prompt = `
      Generate debug code for: ${issue}
      
      Include:
      - Console logs at key points
      - Performance measurements
      - State inspection
      - Network request logging
      - Error boundaries
    `;
    
    return await claude.generateDebug(prompt);
  }
}
```

### Hands-On Exercise: Debug Production Issues
Work through real production bugs using AI assistance

### Afternoon Session: Performance Optimization
**Duration:** 90 minutes

#### Performance Analyzer
```javascript
// performance-optimizer.js
class PerformanceOptimizer {
  async analyzePerformance(code) {
    const prompt = `
      Analyze performance of:
      ${code}
      
      Identify:
      1. Bottlenecks
      2. Memory leaks
      3. Unnecessary re-renders
      4. N+1 queries
      5. Inefficient algorithms
      
      Provide optimization strategies.
    `;
    
    return await claude.analyze(prompt);
  }
  
  async optimizeReact(component) {
    const prompt = `
      Optimize this React component:
      ${component}
      
      Apply:
      - React.memo
      - useMemo
      - useCallback
      - Code splitting
      - Lazy loading
      - Virtual scrolling if applicable
    `;
    
    return await claude.optimize(prompt);
  }
}
```

## Day 5: Build a Complete Application

### Full Day Project: E-commerce Platform
**Duration:** 3 hours

#### Build with AI from Start to Finish
```javascript
// Project specification
const projectSpec = {
  name: "VibeCommerce",
  type: "E-commerce Platform",
  features: [
    "Product catalog",
    "Shopping cart",
    "User authentication",
    "Payment processing",
    "Order management",
    "Admin dashboard",
    "Search and filters",
    "Reviews and ratings",
    "Wishlist",
    "Email notifications"
  ],
  techStack: {
    frontend: "Next.js + TypeScript + Tailwind",
    backend: "Node.js + Express + Prisma",
    database: "PostgreSQL",
    payments: "Stripe",
    hosting: "Vercel + Railway"
  }
};

// Generate entire application
async function buildApplication(spec) {
  const steps = [
    'Generate project structure',
    'Create database schema',
    'Build API endpoints',
    'Create React components',
    'Implement authentication',
    'Add payment processing',
    'Create admin dashboard',
    'Write tests',
    'Setup deployment'
  ];
  
  const application = {};
  
  for (const step of steps) {
    console.log(`Generating: ${step}`);
    application[step] = await claude.generate(`${step} for ${JSON.stringify(spec)}`);
  }
  
  return application;
}
```

## Weekend Assignment

### Build Your Dream Application
1. Define your application idea
2. Create detailed specifications
3. Generate all code with AI
4. Deploy to production
5. Document the process

### Required Deliverables
- [ ] Complete application source code
- [ ] Live deployment URL
- [ ] API documentation
- [ ] Test coverage > 80%
- [ ] Performance audit score > 90

## Assessment Rubric

| Criteria | Basic (60%) | Proficient (80%) | Advanced (100%) |
|----------|-------------|------------------|-----------------|
| AI Usage | Basic prompts | Effective prompting | Advanced techniques |
| Code Quality | Working code | Clean code | Production ready |
| Features | Core features | All features | Extra features |
| Testing | Some tests | Good coverage | Comprehensive |
| Performance | Functional | Optimized | Highly optimized |

## Resources

### Required Reading
- [The Art of Prompt Engineering](https://www.promptingguide.ai/)
- [AI-Assisted Programming](https://github.blog/2023-06-20-how-to-write-better-prompts-for-github-copilot/)
- [Refactoring by Martin Fowler](https://refactoring.com/)

### Video Tutorials
- [Mastering Claude for Coding](https://youtube.com/watch?v=example)
- [Advanced Prompting Techniques](https://youtube.com/watch?v=example)
- [AI Debugging Strategies](https://youtube.com/watch?v=example)

### AI Tools
- **Claude**: Primary AI assistant
- **GitHub Copilot**: In-IDE suggestions
- **Cursor**: AI-first IDE
- **Tabnine**: Code completion
- **Codeium**: Free AI coding assistant

## Office Hours

**Thursday, 3-5 PM EST**
- Live coding with AI
- Prompt engineering workshop
- Code review
- Debugging session

## Next Week Preview

Week 4: Creating Code - Part 2 (Advanced)
- Complex application architectures
- AI-driven testing strategies
- Performance optimization
- Security implementation
- DevOps automation

---

💡 **Vibe Coding Tips:**
- Let AI handle boilerplate
- Focus on business logic
- Iterate quickly
- Test everything
- Ship often

🎯 **Success Metrics:**
- Generate 1000+ lines of code
- Build complete features
- Pass all tests
- Deploy to production
- Help teammates

Ready to vibe code? Let's ship! 🚀
