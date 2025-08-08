# VibeCoders Bootcamp - Complete Sandbox Exercises

## Philosophy: "Work It Until You Solve It"
Each exercise is designed to be challenging but achievable. Students must persist through errors, debug their approach, and iterate until they succeed. No giving up!

---

## Week 1: Developer Hygiene Sandbox

### Exercise: "The Clean Machine"
**Difficulty**: Beginner  
**Time Estimate**: 45-90 minutes  
**Repeat Until Solved**: Yes

#### Mission
Set up a complete, professional development environment from absolute scratch. Your environment must be containerized, version-controlled, and properly configured.

#### Requirements
1. **Create a Docker Development Container**
   - Base image: Ubuntu or Alpine
   - Install Node.js, Python, and Git
   - Configure VS Code to connect to the container
   - Set up proper user permissions

2. **File System Organization**
   ```
   project-root/
   ├── .devcontainer/
   │   ├── devcontainer.json
   │   └── Dockerfile
   ├── src/
   │   ├── frontend/
   │   ├── backend/
   │   └── shared/
   ├── tests/
   ├── docs/
   ├── .env.example
   ├── .gitignore
   ├── README.md
   └── docker-compose.yml
   ```

3. **Environment Configuration**
   - Create .env file with at least 5 variables
   - Implement .gitignore that excludes all sensitive files
   - Set up git pre-commit hooks

4. **Disk Space Management Script**
   - Write a script that cleans:
     - Docker images older than 7 days
     - node_modules in non-active projects
     - Log files larger than 100MB
   - Script must ask for confirmation before deletion

#### Success Criteria
- [ ] Container builds and runs without errors
- [ ] VS Code connects and can edit files
- [ ] Git commits work with proper .gitignore
- [ ] Cleanup script successfully identifies and removes files
- [ ] Environment variables load correctly

#### Progressive Hints
1. **After 15 mins**: Check Docker documentation for multi-stage builds
2. **After 30 mins**: User permissions in Docker need UID/GID matching
3. **After 45 mins**: VS Code needs the Remote-Containers extension

#### Common Pitfalls & Solutions
- **Permission Denied**: Match container user UID with host user
- **Port Already in Use**: Check `docker ps` and stop conflicting containers
- **Environment Variables Not Loading**: Source the .env file or use docker-compose

---

## Week 2: Planning & Architecture Sandbox

### Exercise: "The Blueprint Master"
**Difficulty**: Intermediate  
**Time Estimate**: 60-120 minutes  
**Repeat Until Solved**: Yes

#### Mission
Plan a complete "Task Tracker" application with proper architecture, database design, and API specifications.

#### Requirements
1. **User Stories** (minimum 10)
   ```
   As a [user type], I want to [action] so that [benefit]
   
   Example:
   As a project manager, I want to assign tasks to team members
   so that work is distributed evenly
   ```

2. **Database Schema Design**
   - Users table
   - Tasks table
   - Projects table
   - Comments table
   - Proper relationships and indexes
   - Migration scripts

3. **API Endpoint Planning**
   ```
   POST   /api/auth/register
   POST   /api/auth/login
   GET    /api/tasks
   POST   /api/tasks
   PUT    /api/tasks/:id
   DELETE /api/tasks/:id
   GET    /api/projects/:id/tasks
   ```

4. **Component Architecture Diagram**
   - Frontend components hierarchy
   - State management flow
   - Service layer design
   - Authentication flow

5. **Technical Specification Document**
   - Technology choices with justification
   - Performance requirements
   - Security considerations
   - Deployment strategy

#### Deliverables
- `user-stories.md` - All user stories with acceptance criteria
- `database-schema.sql` - Complete schema with relationships
- `api-specification.yaml` - OpenAPI/Swagger spec
- `architecture-diagram.png` - Visual architecture
- `technical-spec.md` - Complete technical documentation

#### Success Criteria
- [ ] All CRUD operations covered in API
- [ ] Database normalized to at least 3NF
- [ ] No N+1 query problems in design
- [ ] Authentication flow is secure
- [ ] Scalability considered in architecture

#### Progressive Hints
1. **After 20 mins**: Consider using JWT for stateless auth
2. **After 40 mins**: Database indexes should be on foreign keys and commonly queried fields
3. **After 60 mins**: API versioning strategy (e.g., /api/v1/) is important

---

## Week 3: Code Creation Fundamentals Sandbox

### Exercise: "The Refactoring Challenge"
**Difficulty**: Intermediate  
**Time Estimate**: 90-120 minutes  
**Repeat Until Solved**: Yes

#### Mission
Transform terrible, working code into clean, maintainable, testable code following SOLID principles.

#### Starting Code (Intentionally Bad)
```javascript
// Bad Code - user.js
var users = [];
var id = 0;

function user(n, e, p) {
    var u = {};
    u.i = ++id;
    u.n = n;
    u.e = e;
    u.p = p;
    u.a = true;
    u.c = new Date();
    users.push(u);
    
    // send email
    var nodemailer = require('nodemailer');
    var transporter = nodemailer.createTransporter({
        service: 'gmail',
        auth: {
            user: 'app@gmail.com',
            pass: 'password123'
        }
    });
    
    transporter.sendMail({
        from: 'app@gmail.com',
        to: e,
        subject: 'Welcome!',
        text: 'Welcome ' + n + '!'
    });
    
    // save to database
    var mysql = require('mysql');
    var connection = mysql.createConnection({
        host: 'localhost',
        user: 'root',
        password: 'root',
        database: 'app'
    });
    
    connection.connect();
    connection.query('INSERT INTO users (name, email, password) VALUES ("' + n + '", "' + e + '", "' + p + '")', function(err, results) {
        if(err) console.log(err);
    });
    connection.end();
    
    return u;
}

function getUser(e) {
    for(var i = 0; i < users.length; i++) {
        if(users[i].e == e) {
            return users[i];
        }
    }
    return null;
}

function deleteUser(e) {
    for(var i = 0; i < users.length; i++) {
        if(users[i].e == e) {
            users.splice(i, 1);
            
            // delete from database
            var mysql = require('mysql');
            var connection = mysql.createConnection({
                host: 'localhost',
                user: 'root',
                password: 'root',
                database: 'app'
            });
            
            connection.connect();
            connection.query('DELETE FROM users WHERE email = "' + e + '"');
            connection.end();
            
            return true;
        }
    }
    return false;
}

module.exports = {user: user, getUser: getUser, deleteUser: deleteUser};
```

#### Refactoring Requirements
1. **Apply SOLID Principles**
   - Single Responsibility
   - Open/Closed
   - Liskov Substitution
   - Interface Segregation
   - Dependency Inversion

2. **Implement Design Patterns**
   - Repository Pattern for data access
   - Factory Pattern for user creation
   - Observer Pattern for email notifications

3. **Code Quality Improvements**
   - Proper naming conventions
   - Error handling
   - Input validation
   - SQL injection prevention
   - Password hashing

4. **Create Tests**
   - Unit tests for each method
   - Integration tests for database
   - Mock external services

#### Expected Structure
```
src/
├── models/
│   └── User.js
├── repositories/
│   └── UserRepository.js
├── services/
│   ├── EmailService.js
│   └── UserService.js
├── factories/
│   └── UserFactory.js
├── validators/
│   └── UserValidator.js
└── config/
    └── database.js

tests/
├── unit/
│   ├── User.test.js
│   └── UserService.test.js
└── integration/
    └── UserRepository.test.js
```

#### Success Criteria
- [ ] No function longer than 20 lines
- [ ] Each class has single responsibility
- [ ] All database queries use parameterized statements
- [ ] Passwords are hashed with bcrypt
- [ ] 80% test coverage achieved
- [ ] No hardcoded configuration values

#### Progressive Hints
1. **After 30 mins**: Separate concerns - data, business logic, infrastructure
2. **After 60 mins**: Use dependency injection for testability
3. **After 90 mins**: Environment variables for configuration

---

## Week 4: Advanced Implementation Sandbox

### Exercise: "The Full-Stack Feature"
**Difficulty**: Advanced  
**Time Estimate**: 120-180 minutes  
**Repeat Until Solved**: Yes

#### Mission
Build a complete real-time collaborative task board with drag-and-drop functionality.

#### Requirements
1. **Backend API**
   - WebSocket for real-time updates
   - RESTful endpoints for CRUD
   - JWT authentication
   - Rate limiting
   - Data validation

2. **Frontend Application**
   - Drag and drop between columns
   - Real-time updates when others make changes
   - Optimistic UI updates
   - Offline capability with sync
   - Responsive design

3. **State Management**
   - Handle concurrent edits
   - Conflict resolution
   - Local storage for offline
   - Sync queue for pending changes

4. **Features to Implement**
   ```
   - Create/Edit/Delete tasks
   - Move tasks between columns (To Do, In Progress, Done)
   - Assign users to tasks
   - Add comments to tasks
   - Real-time presence (show who's online)
   - Activity feed
   ```

#### Technical Stack
```javascript
// Backend
- Express.js or Fastify
- Socket.io
- PostgreSQL or MongoDB
- Redis for sessions

// Frontend
- React or Vue
- State management (Redux/Zustand/Pinia)
- DnD library
- Tailwind CSS
```

#### Success Criteria
- [ ] Drag and drop works smoothly
- [ ] Changes appear instantly for all users
- [ ] Offline changes sync when reconnected
- [ ] No race conditions in concurrent edits
- [ ] Handles disconnections gracefully
- [ ] Mobile responsive

#### Architecture Tests
```javascript
// Test concurrent operations
async function testConcurrency() {
    const user1 = await createUser('user1');
    const user2 = await createUser('user2');
    
    // Both users move same task simultaneously
    await Promise.all([
        user1.moveTask('task1', 'in-progress'),
        user2.moveTask('task1', 'done')
    ]);
    
    // Verify final state is consistent
}
```

#### Progressive Hints
1. **After 30 mins**: Use optimistic updates with rollback on failure
2. **After 60 mins**: Implement event sourcing for conflict resolution
3. **After 90 mins**: Use Redis pub/sub for scalable real-time updates

---

## Week 5: Testing & QA Sandbox

### Exercise: "The Testing Gauntlet"
**Difficulty**: Advanced  
**Time Estimate**: 90-120 minutes  
**Repeat Until Solved**: Yes

#### Mission
Create comprehensive test suite for a provided e-commerce checkout system.

#### Provided System
```javascript
// Checkout system with intentional bugs
class CheckoutService {
    constructor(cartService, paymentService, inventoryService) {
        this.cartService = cartService;
        this.paymentService = paymentService;
        this.inventoryService = inventoryService;
    }
    
    async processCheckout(userId, paymentInfo) {
        const cart = await this.cartService.getCart(userId);
        
        if (cart.items.length === 0) {
            throw new Error('Cart is empty');
        }
        
        // Check inventory
        for (const item of cart.items) {
            const available = await this.inventoryService.checkStock(item.productId);
            if (available < item.quantity) {
                throw new Error(`Insufficient stock for ${item.name}`);
            }
        }
        
        // Calculate total (bug: doesn't handle discounts properly)
        const subtotal = cart.items.reduce((sum, item) => sum + item.price * item.quantity, 0);
        const tax = subtotal * 0.08;
        const shipping = subtotal > 50 ? 0 : 10;
        const total = subtotal + tax + shipping;
        
        // Process payment (bug: doesn't handle payment failures properly)
        const payment = await this.paymentService.charge(paymentInfo, total);
        
        // Update inventory (bug: race condition possible)
        for (const item of cart.items) {
            await this.inventoryService.reduceStock(item.productId, item.quantity);
        }
        
        // Clear cart
        await this.cartService.clearCart(userId);
        
        return {
            orderId: payment.transactionId,
            total: total,
            items: cart.items
        };
    }
}
```

#### Testing Requirements
1. **Unit Tests**
   - Test each method in isolation
   - Mock all dependencies
   - Test edge cases
   - Test error scenarios

2. **Integration Tests**
   - Test service interactions
   - Test database transactions
   - Test API endpoints

3. **End-to-End Tests**
   - Complete checkout flow
   - Payment success/failure
   - Inventory updates
   - Email notifications

4. **Performance Tests**
   - Load testing with 100 concurrent users
   - Stress testing to find breaking point
   - Memory leak detection

5. **Bug Report**
   - Document all bugs found
   - Provide fixes for each bug
   - Add regression tests

#### Test Coverage Goals
```
File                | % Stmts | % Branch | % Funcs | % Lines |
--------------------|---------|----------|---------|---------|
All files           |      85 |       80 |      90 |      85 |
 CheckoutService.js |      95 |       90 |     100 |      95 |
 CartService.js     |      80 |       75 |      85 |      80 |
 PaymentService.js  |      85 |       80 |      90 |      85 |
 InventoryService.js|      80 |       75 |      85 |      80 |
```

#### Bugs to Find and Fix
1. Discount calculation missing
2. Payment rollback not implemented
3. Race condition in inventory update
4. No validation for negative quantities
5. Missing error logging
6. Tax calculation incorrect for some states
7. No idempotency for retried requests

#### Success Criteria
- [ ] All bugs identified and documented
- [ ] 85% overall test coverage achieved
- [ ] All tests pass consistently
- [ ] Performance benchmarks met
- [ ] No flaky tests

#### Progressive Hints
1. **After 20 mins**: Use test.each() for parameterized tests
2. **After 40 mins**: Transaction rollback needs try-catch-finally
3. **After 60 mins**: Use database transactions for inventory updates

---

## Week 6: Deployment & DevOps Sandbox

### Exercise: "Ship to Production"
**Difficulty**: Advanced  
**Time Estimate**: 120-150 minutes  
**Repeat Until Solved**: Yes

#### Mission
Deploy a full-stack application with CI/CD, monitoring, and zero-downtime deployments.

#### Application to Deploy
A provided Node.js + React application with:
- Backend API
- Frontend SPA
- PostgreSQL database
- Redis cache
- Background jobs

#### Requirements
1. **CI/CD Pipeline**
   ```yaml
   # GitHub Actions workflow
   - Run tests on every push
   - Build Docker images
   - Run security scans
   - Deploy to staging on main branch
   - Manual approval for production
   - Rollback capability
   ```

2. **Infrastructure Setup**
   - Use Railway, Render, or Vercel
   - Database with backups
   - Redis for caching
   - CDN for static assets
   - SSL certificates

3. **Monitoring & Logging**
   - Application performance monitoring
   - Error tracking (Sentry)
   - Uptime monitoring
   - Log aggregation
   - Custom metrics dashboard

4. **Zero-Downtime Deployment**
   - Blue-green deployment
   - Database migrations without downtime
   - Feature flags for gradual rollout
   - Health checks

5. **Security Implementation**
   - Environment variables properly managed
   - Secrets rotation
   - Rate limiting
   - CORS configuration
   - Security headers

#### Deployment Checklist
```markdown
## Pre-Deployment
- [ ] All tests passing
- [ ] Security scan completed
- [ ] Database migrations tested
- [ ] Environment variables configured
- [ ] Backup created

## Deployment
- [ ] Deploy to staging
- [ ] Run smoke tests
- [ ] Check monitoring dashboards
- [ ] Deploy to production
- [ ] Verify health checks

## Post-Deployment
- [ ] Monitor error rates
- [ ] Check performance metrics
- [ ] Verify all features working
- [ ] Document deployment
- [ ] Update status page
```

#### Success Criteria
- [ ] Application accessible via HTTPS
- [ ] All environment variables secure
- [ ] Monitoring dashboards configured
- [ ] CI/CD pipeline fully automated
- [ ] Can rollback within 2 minutes
- [ ] 99.9% uptime achieved

#### Performance Benchmarks
```
- Page load time: < 3 seconds
- API response time: < 200ms (p95)
- Error rate: < 1%
- Deployment time: < 5 minutes
- Rollback time: < 2 minutes
```

#### Progressive Hints
1. **After 30 mins**: Use GitHub Secrets for sensitive data
2. **After 60 mins**: Database migrations need to be backwards compatible
3. **After 90 mins**: Feature flags allow safer deployments

---

## Sandbox Grading Rubric

### Basic Completion (60%)
- Code runs without critical errors
- Basic requirements met
- Follows provided structure

### Proficiency (80%)
- All test cases pass
- Code is well-organized
- Includes error handling
- Comments explain complex logic
- Meets performance requirements

### Excellence (100%)
- Implements bonus features
- Optimized performance
- Comprehensive documentation
- Creative problem-solving approach
- Could be used in production

---

## Support Resources

### When Stuck
1. **First 15 minutes**: Try debugging yourself
2. **After 15 minutes**: Check the progressive hints
3. **After 30 minutes**: Ask in Discord for peer help
4. **After 45 minutes**: Request mentor assistance

### Debugging Strategies
1. Read error messages carefully
2. Add console.log statements
3. Use debugger tools
4. Check documentation
5. Simplify the problem
6. Test individual components
7. Google specific error messages
8. Take a 5-minute break

### Remember
**"Work it until you solve it"** - Every bug is a learning opportunity. Every error teaches you something new. Persistence is the key to becoming a great engineer.

---

## Sandbox Completion Tracking

### Week 1: Developer Hygiene
- [ ] Environment setup complete
- [ ] All success criteria met
- [ ] Time to completion: _____ minutes
- [ ] Attempts needed: _____

### Week 2: Planning & Architecture
- [ ] All deliverables created
- [ ] Design reviewed by peer
- [ ] Time to completion: _____ minutes
- [ ] Attempts needed: _____

### Week 3: Code Creation Fundamentals
- [ ] Refactoring complete
- [ ] Tests passing
- [ ] Time to completion: _____ minutes
- [ ] Attempts needed: _____

### Week 4: Advanced Implementation
- [ ] Feature fully functional
- [ ] Real-time working
- [ ] Time to completion: _____ minutes
- [ ] Attempts needed: _____

### Week 5: Testing & QA
- [ ] All bugs found
- [ ] Coverage goals met
- [ ] Time to completion: _____ minutes
- [ ] Attempts needed: _____

### Week 6: Deployment & DevOps
- [ ] Application deployed
- [ ] Monitoring active
- [ ] Time to completion: _____ minutes
- [ ] Attempts needed: _____