# AI Pair Programming Guide

## 🤖 Master the Art of Coding with AI

This guide will teach you how to effectively use AI tools like Claude, GitHub Copilot, and Cursor to 10x your development speed while maintaining code quality.

---

## Table of Contents
1. [Fundamental Principles](#fundamental-principles)
2. [Effective Prompting](#effective-prompting)
3. [Tool-Specific Techniques](#tool-specific-techniques)
4. [Common Patterns](#common-patterns)
5. [Debugging with AI](#debugging-with-ai)
6. [Best Practices](#best-practices)
7. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)

---

## Fundamental Principles

### The 80/20 Rule
- **80% AI Generation**: Let AI handle boilerplate, repetitive code, and standard patterns
- **20% Human Refinement**: Focus your energy on business logic, architecture decisions, and optimization

### The Three Cs of AI Coding
1. **Context**: Always provide sufficient context
2. **Clarity**: Be specific about requirements
3. **Critique**: Always review AI output critically

---

## Effective Prompting

### Anatomy of a Perfect Prompt

```markdown
# Bad Prompt ❌
"Make a login form"

# Good Prompt ✅
"Create a React login form component with:
- Email and password fields with validation
- Email must be valid format
- Password minimum 8 characters, must include number and special character
- Show/hide password toggle
- Loading state during submission
- Error message display for failed login
- Success redirect to /dashboard
- Remember me checkbox
- Forgot password link
- Styled with Tailwind CSS
- TypeScript interfaces for props
- Accessibility compliant (ARIA labels)
- Jest unit tests included"
```

### Prompt Templates

#### Feature Implementation
```markdown
Create a [FEATURE] that:
- Purpose: [WHAT IT DOES]
- Users: [WHO USES IT]
- Input: [WHAT DATA IT RECEIVES]
- Output: [WHAT IT PRODUCES]
- Tech Stack: [LANGUAGES/FRAMEWORKS]
- Requirements:
  - [REQUIREMENT 1]
  - [REQUIREMENT 2]
- Include:
  - Error handling for [SCENARIOS]
  - Loading states
  - Type safety
  - Unit tests
  - Documentation
```

#### Refactoring Request
```markdown
Refactor this code to:
- Improve [SPECIFIC ASPECT]
- Follow [PATTERN/PRINCIPLE]
- Maintain backward compatibility
- Add comprehensive tests

Current code:
[PASTE CODE]

Issues to address:
- [ISSUE 1]
- [ISSUE 2]
```

#### Bug Fixing
```markdown
Debug this issue:
- Error message: [EXACT ERROR]
- Expected behavior: [WHAT SHOULD HAPPEN]
- Actual behavior: [WHAT IS HAPPENING]
- Steps to reproduce:
  1. [STEP 1]
  2. [STEP 2]
- Code context: [RELEVANT CODE]
- Environment: [OS, VERSIONS, ETC]
```

---

## Tool-Specific Techniques

### Claude Desktop
Best for: Complex architectures, full applications, learning

```markdown
# Optimal Claude Usage
1. Start with high-level design
2. Break down into components
3. Iterate on each component
4. Ask for explanations
5. Request alternative approaches
```

#### Claude Conversation Flow
```markdown
You: "I need to build a real-time chat application"

Claude: [Provides overview]

You: "Let's start with the backend. Create a WebSocket server with rooms"

Claude: [Generates server code]

You: "Now add authentication and rate limiting"

Claude: [Enhances with features]

You: "Explain the rate limiting strategy"

Claude: [Provides detailed explanation]
```

### GitHub Copilot
Best for: In-line suggestions, autocomplete, quick functions

```javascript
// Write descriptive comments to trigger Copilot
// Function to validate email format and check if domain is allowed
function validateEmail(email, allowedDomains) {
  // Copilot will suggest implementation
}

// Use meaningful variable names
const userAuthenticationToken = // Copilot suggests JWT implementation

// Start typing and Tab to accept
function calculateCompoundInterest(
  // Copilot will suggest parameters and implementation
)
```

### Cursor IDE
Best for: Full file generation, multi-file refactoring

```markdown
# Cursor Commands
Cmd+K: Generate code at cursor
Cmd+L: Chat about current file
Cmd+Shift+L: Chat about entire codebase

# Effective Cursor Prompts
@file1.js @file2.js "Refactor these to use a shared utility"
@codebase "Find all API endpoints and generate OpenAPI spec"
```

### MCP (Model Context Protocol)
Best for: Tool integration, external data access

```javascript
// MCP Server Configuration
{
  "mcpServers": {
    "database": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-postgres", "--connection-string", "postgresql://..."]
    },
    "github": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-github", "--token", "${GITHUB_TOKEN}"]
    }
  }
}

// Usage in Claude
"Look at my database schema and suggest optimizations"
"Check my GitHub issues and create a sprint plan"
```

---

## Common Patterns

### Pattern 1: Iterative Development
```markdown
Step 1: "Create a basic user model"
Step 2: "Add validation to the user model"
Step 3: "Add password hashing"
Step 4: "Add email verification logic"
Step 5: "Add OAuth integration"
```

### Pattern 2: Test-First Development
```markdown
1. "Write tests for a shopping cart class that can add items, remove items, and calculate total"
2. "Now implement the ShoppingCart class to pass these tests"
3. "Add edge case handling"
4. "Optimize the implementation"
```

### Pattern 3: Progressive Enhancement
```javascript
// Start simple
"Create a button component"

// Add features
"Add loading state to the button"

// Add more complexity
"Add different variants (primary, secondary, danger)"

// Add advanced features
"Add keyboard navigation and accessibility"
```

### Pattern 4: Documentation-Driven Development
```markdown
1. "Write API documentation for a user management system"
2. "Generate OpenAPI spec from the documentation"
3. "Create the server implementation from the spec"
4. "Generate client SDK from the spec"
```

---

## Debugging with AI

### Systematic Debugging Approach

```markdown
1. Describe the Problem
"Function X returns undefined instead of array"

2. Provide Context
"This function processes user data from API"

3. Show the Code
[paste relevant code]

4. Share Error Messages
"TypeError: Cannot read property 'map' of undefined at line 42"

5. Explain What You've Tried
"I've checked that the API returns data, but..."

6. Ask for Specific Help
"How can I handle the case when the API returns null?"
```

### Debugging Prompts

```markdown
# Performance Issues
"This function is slow. Profile it and suggest optimizations:
[CODE]
Current execution time: Xms for N items"

# Memory Leaks
"I suspect a memory leak in this component. Identify potential issues:
[CODE]
Symptoms: Memory usage increases by X MB every Y minutes"

# Race Conditions
"Users report intermittent failures. Find race conditions:
[CODE]
Failure rate: X% under high load"
```

---

## Best Practices

### 1. Always Review Generated Code
```javascript
// AI Generated
function calculateAge(birthDate) {
  return new Date().getFullYear() - new Date(birthDate).getFullYear();
}

// Human Review: This doesn't account for birthdays not yet passed this year
function calculateAge(birthDate) {
  const today = new Date();
  const birth = new Date(birthDate);
  let age = today.getFullYear() - birth.getFullYear();
  const monthDiff = today.getMonth() - birth.getMonth();
  
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
    age--;
  }
  
  return age;
}
```

### 2. Maintain Context Across Sessions
```markdown
# Session Start
"We're building an e-commerce platform with React and Node.js. 
The database is PostgreSQL. We use TypeScript throughout.
Authentication is JWT-based. Payment processing uses Stripe."

# Future Prompts Can Be Shorter
"Add cart functionality" 
// AI knows the context
```

### 3. Version Control AI Interactions
```bash
# Create branches for AI experiments
git checkout -b ai/feature-experiment

# Commit with clear messages
git commit -m "feat: AI-generated user authentication flow

Co-authored-by: Claude <claude@anthropic.com>"
```

### 4. Build a Prompt Library
```markdown
## Saved Prompts

### React Component Generator
"Create a React FC with TypeScript, props interface, 
default props, error boundary, and Storybook story"

### API Endpoint Creator
"Generate Express endpoint with validation, error handling, 
rate limiting, and Swagger documentation"

### Test Suite Builder
"Write Jest tests with setup/teardown, mocks, 
edge cases, and >90% coverage"
```

### 5. Use AI for Code Reviews
```markdown
"Review this PR for:
- Security vulnerabilities
- Performance issues
- Best practice violations
- Missing error handling
- Test coverage gaps

[PASTE DIFF]"
```

---

## Anti-Patterns to Avoid

### ❌ Don't Blindly Copy-Paste
```javascript
// AI might generate deprecated code
componentWillMount() { // Deprecated in React!
  this.loadData();
}

// Always verify current best practices
useEffect(() => {
  loadData();
}, []);
```

### ❌ Don't Skip Understanding
```markdown
Bad: "Make this work" [paste broken code]
Good: "Explain why this fails, then fix it" [paste code]
```

### ❌ Don't Ignore Security
```javascript
// AI might generate insecure code
app.get('/user/:id', (req, res) => {
  db.query(`SELECT * FROM users WHERE id = ${req.params.id}`); // SQL Injection!
});

// Always validate and sanitize
app.get('/user/:id', (req, res) => {
  db.query('SELECT * FROM users WHERE id = ?', [req.params.id]);
});
```

### ❌ Don't Forget Edge Cases
```javascript
// AI might miss edge cases
function divide(a, b) {
  return a / b; // What about b = 0?
}

// Add validation
function divide(a, b) {
  if (b === 0) throw new Error('Division by zero');
  return a / b;
}
```

### ❌ Don't Over-Rely on AI
```markdown
Tasks Better Done by Humans:
- Architecture decisions
- Business logic design
- Security implementations
- Performance critical code
- Algorithm optimization
```

---

## Practical Exercises

### Exercise 1: Speed Coding Challenge
```markdown
Time yourself building these with AI assistance:
1. TODO app with CRUD operations (Target: 10 minutes)
2. REST API with authentication (Target: 15 minutes)
3. Real-time chat with WebSockets (Target: 20 minutes)

Compare with manual coding time.
```

### Exercise 2: Refactoring Practice
```markdown
1. Find ugly code on GitHub
2. Use AI to refactor it
3. Manually review and improve
4. Compare before/after
```

### Exercise 3: Test Generation
```markdown
1. Write a complex function manually
2. Ask AI to generate comprehensive tests
3. Run tests and find missing cases
4. Iterate until 100% coverage
```

### Exercise 4: Debug Challenge
```markdown
1. Intentionally break working code
2. Use only AI to debug (no manual debugging)
3. Document the conversation flow
4. Reflect on effectiveness
```

---

## Measuring Success

### Productivity Metrics
- **Lines of Code per Hour**: Should increase 5-10x
- **Bug Rate**: Should decrease by 50%
- **Feature Delivery**: Should increase 3-5x
- **Learning Speed**: New concepts understood 2-3x faster

### Quality Indicators
✅ Code passes all tests
✅ Follows team style guide
✅ Performant and optimized
✅ Well-documented
✅ Security best practices followed

---

## Advanced Techniques

### Multi-AI Collaboration
```markdown
1. Use Claude for architecture
2. Use Copilot for implementation
3. Use GPT-4 for documentation
4. Use Specialized AI for optimization
```

### AI Chain Prompting
```markdown
Prompt 1: "Design database schema for [app]"
Prompt 2: "Based on above schema, create models"
Prompt 3: "Based on models, create API endpoints"
Prompt 4: "Based on API, create frontend components"
Prompt 5: "Based on all above, create tests"
```

### Context Injection
```javascript
/* PROJECT_CONTEXT
App: E-commerce Platform
Stack: Next.js, Prisma, PostgreSQL
Style: Tailwind CSS
Auth: NextAuth
Payments: Stripe
Testing: Jest, Playwright
*/

// All future AI suggestions will consider this context
```

---

## Resources

### Recommended Reading
- [GitHub Copilot Best Practices](https://github.com/features/copilot)
- [Anthropic Claude Documentation](https://docs.anthropic.com)
- [Cursor IDE Guide](https://cursor.sh/docs)
- [MCP Protocol Spec](https://modelcontextprotocol.org)

### Community
- Discord: VibeCoders Community
- Reddit: r/AIProgramming
- Twitter: #AIAssistedCoding

### Tools to Try
- **Tabnine**: AI code completion
- **Codeium**: Free AI assistant
- **Amazon CodeWhisperer**: AWS-integrated AI
- **Replit Ghostwriter**: In-browser AI coding

---

## Conclusion

AI pair programming is not about replacing human developers—it's about augmenting human capabilities. Master these techniques to:

- 🚀 Ship features faster
- 🐛 Write fewer bugs
- 📚 Learn new technologies quickly
- 💡 Focus on creative problem-solving
- 🎯 Deliver more value

Remember: **"AI is your copilot, but you're still the pilot!"**

---

## Quick Reference Card

```markdown
## Daily AI Workflow

Morning:
□ Review yesterday's AI-generated code
□ Plan today's features with AI assistance
□ Generate boilerplate for new features

Coding:
□ Write descriptive comments for Copilot
□ Use Claude for complex logic
□ Let AI handle repetitive tasks
□ Review and refine AI output

Debugging:
□ Describe problem clearly to AI
□ Provide error messages and context
□ Try AI's suggestions systematically
□ Learn from AI's explanations

Evening:
□ Use AI for code review
□ Generate documentation
□ Create tests for today's code
□ Update prompt library with useful prompts
```

---

*Last Updated: Week 3 of VibeCoders Bootcamp*
*Version: 2.0*
