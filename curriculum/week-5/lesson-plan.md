# Week 5: Testing & Quality Assurance

## Overview
This week transforms you into a quality engineer who can ensure your code is bulletproof. You'll master AI-driven testing strategies, from unit tests to end-to-end testing, and learn to maintain high code quality standards.

## Learning Objectives
By the end of this week, you will:
- ✅ Write comprehensive test suites with AI assistance
- ✅ Implement test-driven development (TDD)
- ✅ Perform load and performance testing
- ✅ Conduct security testing and audits
- ✅ Set up continuous quality monitoring

## Day 1: AI-Driven Test Generation

### Morning Session: Unit Testing with AI
**Duration:** 90 minutes

#### AI Test Generator
```javascript
// test-generator.js
class AITestGenerator {
  async generateUnitTests(code) {
    const prompt = `
      Generate comprehensive unit tests for this code:
      ${code}
      
      Include:
      1. Happy path tests
      2. Edge cases
      3. Error cases
      4. Boundary conditions
      5. Null/undefined handling
      6. Performance tests
      
      Use Jest and include:
      - describe blocks
      - beforeEach/afterEach
      - Mocking where needed
      - Assertions with expect
      - Test coverage goals
    `;
    
    return await claude.generate(prompt);
  }
  
  async generateTestsFromRequirements(requirements) {
    const prompt = `
      Generate test cases from these requirements:
      ${requirements}
      
      Create:
      1. User story tests
      2. Acceptance criteria tests
      3. Integration test scenarios
      4. E2E test flows
      5. Performance benchmarks
      
      Format as BDD-style tests.
    `;
    
    return await claude.generate(prompt);
  }
}

// Generated Unit Tests Example
describe('ShoppingCart', () => {
  let cart;
  let mockDatabase;
  let mockPaymentService;
  
  beforeEach(() => {
    cart = new ShoppingCart();
    mockDatabase = {
      save: jest.fn().mockResolvedValue(true),
      load: jest.fn().mockResolvedValue([])
    };
    mockPaymentService = {
      charge: jest.fn().mockResolvedValue({ success: true, transactionId: '123' })
    };
    
    cart.setDatabase(mockDatabase);
    cart.setPaymentService(mockPaymentService);
  });
  
  afterEach(() => {
    jest.clearAllMocks();
  });
  
  describe('addItem', () => {
    test('should add item to empty cart', () => {
      const item = { id: '1', name: 'Product', price: 10, quantity: 1 };
      cart.addItem(item);
      
      expect(cart.getItems()).toHaveLength(1);
      expect(cart.getItems()[0]).toEqual(item);
    });
    
    test('should increase quantity for existing item', () => {
      const item = { id: '1', name: 'Product', price: 10, quantity: 1 };
      cart.addItem(item);
      cart.addItem(item);
      
      expect(cart.getItems()).toHaveLength(1);
      expect(cart.getItems()[0].quantity).toBe(2);
    });
    
    test('should throw error for invalid item', () => {
      expect(() => cart.addItem(null)).toThrow('Invalid item');
      expect(() => cart.addItem({})).toThrow('Item must have id');
      expect(() => cart.addItem({ id: '1' })).toThrow('Item must have price');
    });
    
    test('should handle maximum quantity limit', () => {
      const item = { id: '1', name: 'Product', price: 10, quantity: 99 };
      cart.addItem(item);
      
      expect(() => cart.addItem({ ...item, quantity: 2 }))
        .toThrow('Quantity exceeds maximum limit');
    });
  });
  
  describe('calculateTotal', () => {
    test('should calculate correct total', () => {
      cart.addItem({ id: '1', name: 'Product 1', price: 10, quantity: 2 });
      cart.addItem({ id: '2', name: 'Product 2', price: 15, quantity: 1 });
      
      expect(cart.calculateTotal()).toBe(35);
    });
    
    test('should apply discount correctly', () => {
      cart.addItem({ id: '1', name: 'Product', price: 100, quantity: 1 });
      cart.applyDiscount(0.2); // 20% discount
      
      expect(cart.calculateTotal()).toBe(80);
    });
    
    test('should handle empty cart', () => {
      expect(cart.calculateTotal()).toBe(0);
    });
    
    test('should include tax calculation', () => {
      cart.addItem({ id: '1', name: 'Product', price: 100, quantity: 1 });
      cart.setTaxRate(0.1); // 10% tax
      
      expect(cart.calculateTotal(true)).toBe(110);
    });
  });
  
  describe('checkout', () => {
    test('should process successful checkout', async () => {
      cart.addItem({ id: '1', name: 'Product', price: 10, quantity: 1 });
      
      const result = await cart.checkout({
        paymentMethod: 'card',
        cardNumber: '4242424242424242'
      });
      
      expect(result.success).toBe(true);
      expect(result.transactionId).toBeDefined();
      expect(mockPaymentService.charge).toHaveBeenCalledWith({
        amount: 10,
        method: 'card',
        cardNumber: '4242424242424242'
      });
      expect(mockDatabase.save).toHaveBeenCalled();
    });
    
    test('should handle payment failure', async () => {
      mockPaymentService.charge.mockRejectedValue(new Error('Payment failed'));
      cart.addItem({ id: '1', name: 'Product', price: 10, quantity: 1 });
      
      await expect(cart.checkout({ paymentMethod: 'card' }))
        .rejects.toThrow('Payment failed');
      
      expect(mockDatabase.save).not.toHaveBeenCalled();
    });
    
    test('should validate empty cart', async () => {
      await expect(cart.checkout({ paymentMethod: 'card' }))
        .rejects.toThrow('Cart is empty');
    });
  });
  
  describe('Performance', () => {
    test('should handle large number of items efficiently', () => {
      const startTime = performance.now();
      
      for (let i = 0; i < 10000; i++) {
        cart.addItem({ id: `${i}`, name: `Product ${i}`, price: 10, quantity: 1 });
      }
      
      const endTime = performance.now();
      expect(endTime - startTime).toBeLessThan(100); // Less than 100ms
    });
    
    test('should calculate total for large cart quickly', () => {
      for (let i = 0; i < 10000; i++) {
        cart.addItem({ id: `${i}`, name: `Product ${i}`, price: 10, quantity: 1 });
      }
      
      const startTime = performance.now();
      const total = cart.calculateTotal();
      const endTime = performance.now();
      
      expect(total).toBe(100000);
      expect(endTime - startTime).toBeLessThan(10); // Less than 10ms
    });
  });
});
```

### Hands-On Exercise: Generate Tests for Your Project
Use AI to generate comprehensive test suites for an existing project

### Afternoon Session: Integration Testing
**Duration:** 90 minutes

#### API Integration Tests
```javascript
// integration-tests.js
const request = require('supertest');
const app = require('../app');
const { sequelize } = require('../models');

describe('API Integration Tests', () => {
  let server;
  let authToken;
  let testUser;
  
  beforeAll(async () => {
    await sequelize.sync({ force: true });
    server = app.listen(0); // Random port
  });
  
  afterAll(async () => {
    await server.close();
    await sequelize.close();
  });
  
  describe('Authentication Flow', () => {
    test('should register a new user', async () => {
      const response = await request(server)
        .post('/api/auth/register')
        .send({
          email: 'test@example.com',
          password: 'SecurePass123!',
          name: 'Test User'
        });
      
      expect(response.status).toBe(201);
      expect(response.body).toHaveProperty('user');
      expect(response.body).toHaveProperty('token');
      expect(response.body.user.email).toBe('test@example.com');
      
      authToken = response.body.token;
      testUser = response.body.user;
    });
    
    test('should login with valid credentials', async () => {
      const response = await request(server)
        .post('/api/auth/login')
        .send({
          email: 'test@example.com',
          password: 'SecurePass123!'
        });
      
      expect(response.status).toBe(200);
      expect(response.body).toHaveProperty('token');
      expect(response.body.token).toBeDefined();
    });
    
    test('should reject invalid credentials', async () => {
      const response = await request(server)
        .post('/api/auth/login')
        .send({
          email: 'test@example.com',
          password: 'WrongPassword'
        });
      
      expect(response.status).toBe(401);
      expect(response.body.error).toBe('Invalid credentials');
    });
  });
  
  describe('Protected Routes', () => {
    test('should access protected route with valid token', async () => {
      const response = await request(server)
        .get('/api/profile')
        .set('Authorization', `Bearer ${authToken}`);
      
      expect(response.status).toBe(200);
      expect(response.body.email).toBe('test@example.com');
    });
    
    test('should reject request without token', async () => {
      const response = await request(server)
        .get('/api/profile');
      
      expect(response.status).toBe(401);
      expect(response.body.error).toBe('No token provided');
    });
    
    test('should reject request with invalid token', async () => {
      const response = await request(server)
        .get('/api/profile')
        .set('Authorization', 'Bearer invalid-token');
      
      expect(response.status).toBe(401);
      expect(response.body.error).toBe('Invalid token');
    });
  });
  
  describe('CRUD Operations', () => {
    let createdPost;
    
    test('should create a new post', async () => {
      const response = await request(server)
        .post('/api/posts')
        .set('Authorization', `Bearer ${authToken}`)
        .send({
          title: 'Test Post',
          content: 'This is a test post content',
          tags: ['test', 'integration']
        });
      
      expect(response.status).toBe(201);
      expect(response.body.title).toBe('Test Post');
      expect(response.body.author.id).toBe(testUser.id);
      
      createdPost = response.body;
    });
    
    test('should update existing post', async () => {
      const response = await request(server)
        .put(`/api/posts/${createdPost.id}`)
        .set('Authorization', `Bearer ${authToken}`)
        .send({
          title: 'Updated Post Title'
        });
      
      expect(response.status).toBe(200);
      expect(response.body.title).toBe('Updated Post Title');
      expect(response.body.content).toBe(createdPost.content);
    });
    
    test('should delete post', async () => {
      const response = await request(server)
        .delete(`/api/posts/${createdPost.id}`)
        .set('Authorization', `Bearer ${authToken}`);
      
      expect(response.status).toBe(204);
      
      // Verify deletion
      const getResponse = await request(server)
        .get(`/api/posts/${createdPost.id}`);
      
      expect(getResponse.status).toBe(404);
    });
  });
  
  describe('Database Transactions', () => {
    test('should rollback on error', async () => {
      const response = await request(server)
        .post('/api/transfer')
        .set('Authorization', `Bearer ${authToken}`)
        .send({
          from: 'account1',
          to: 'invalid-account',
          amount: 100
        });
      
      expect(response.status).toBe(400);
      
      // Verify no changes were made
      const balance = await request(server)
        .get('/api/accounts/account1/balance')
        .set('Authorization', `Bearer ${authToken}`);
      
      expect(balance.body.balance).toBe(1000); // Original balance
    });
  });
});
```

## Day 2: End-to-End Testing

### Morning Session: E2E with Playwright
**Duration:** 90 minutes

#### Playwright Test Suite
```javascript
// e2e-tests.spec.js
const { test, expect } = require('@playwright/test');

test.describe('E-Commerce User Journey', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000');
  });
  
  test('complete purchase flow', async ({ page }) => {
    // Step 1: Browse and search
    await page.fill('[data-testid="search-input"]', 'laptop');
    await page.press('[data-testid="search-input"]', 'Enter');
    
    await expect(page).toHaveURL(/.*search\?q=laptop/);
    await expect(page.locator('[data-testid="product-card"]')).toHaveCount(10);
    
    // Step 2: Filter results
    await page.click('[data-testid="filter-price-range"]');
    await page.fill('[data-testid="min-price"]', '500');
    await page.fill('[data-testid="max-price"]', '1500');
    await page.click('[data-testid="apply-filters"]');
    
    await page.waitForLoadState('networkidle');
    const products = await page.locator('[data-testid="product-card"]').count();
    expect(products).toBeGreaterThan(0);
    expect(products).toBeLessThanOrEqual(10);
    
    // Step 3: Select product
    await page.click('[data-testid="product-card"]:first-child');
    await expect(page).toHaveURL(/.*product\/.*/);
    
    // Step 4: Add to cart
    await page.selectOption('[data-testid="quantity-select"]', '2');
    await page.click('[data-testid="add-to-cart"]');
    
    await expect(page.locator('[data-testid="cart-count"]')).toHaveText('2');
    await expect(page.locator('.toast-success')).toHaveText('Added to cart');
    
    // Step 5: Checkout
    await page.click('[data-testid="cart-icon"]');
    await page.click('[data-testid="proceed-to-checkout"]');
    
    // Step 6: Fill shipping information
    await page.fill('[data-testid="shipping-name"]', 'John Doe');
    await page.fill('[data-testid="shipping-address"]', '123 Main St');
    await page.fill('[data-testid="shipping-city"]', 'New York');
    await page.fill('[data-testid="shipping-zip"]', '10001');
    await page.selectOption('[data-testid="shipping-country"]', 'US');
    
    // Step 7: Payment
    await page.click('[data-testid="continue-to-payment"]');
    
    // Use Stripe test card
    const stripeFrame = page.frameLocator('iframe[name="stripe"]');
    await stripeFrame.locator('[placeholder="Card number"]').fill('4242424242424242');
    await stripeFrame.locator('[placeholder="MM / YY"]').fill('12/25');
    await stripeFrame.locator('[placeholder="CVC"]').fill('123');
    
    // Step 8: Place order
    await page.click('[data-testid="place-order"]');
    
    // Step 9: Verify order confirmation
    await expect(page).toHaveURL(/.*order-confirmation\/.*/);
    await expect(page.locator('h1')).toHaveText('Thank you for your order!');
    await expect(page.locator('[data-testid="order-number"]')).toBeVisible();
    
    // Step 10: Check order in account
    await page.click('[data-testid="view-orders"]');
    await expect(page.locator('[data-testid="order-item"]')).toHaveCount(1);
  });
  
  test('visual regression testing', async ({ page }) => {
    // Homepage screenshot
    await page.goto('http://localhost:3000');
    await expect(page).toHaveScreenshot('homepage.png', {
      fullPage: true,
      animations: 'disabled'
    });
    
    // Product page screenshot
    await page.goto('http://localhost:3000/product/1');
    await expect(page).toHaveScreenshot('product-page.png', {
      fullPage: true,
      animations: 'disabled'
    });
    
    // Cart screenshot
    await page.goto('http://localhost:3000/cart');
    await expect(page).toHaveScreenshot('cart.png', {
      fullPage: true,
      animations: 'disabled'
    });
  });
  
  test('mobile responsiveness', async ({ page }) => {
    // Test on mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    
    await page.goto('http://localhost:3000');
    
    // Check mobile menu
    await expect(page.locator('[data-testid="mobile-menu"]')).toBeVisible();
    await expect(page.locator('[data-testid="desktop-nav"]')).toBeHidden();
    
    // Open mobile menu
    await page.click('[data-testid="mobile-menu-toggle"]');
    await expect(page.locator('[data-testid="mobile-menu-content"]')).toBeVisible();
    
    // Navigate via mobile menu
    await page.click('[data-testid="mobile-menu-products"]');
    await expect(page).toHaveURL(/.*products/);
    
    // Check product grid on mobile
    const gridClass = await page.locator('[data-testid="product-grid"]').getAttribute('class');
    expect(gridClass).toContain('grid-cols-1');
  });
  
  test('accessibility testing', async ({ page }) => {
    await page.goto('http://localhost:3000');
    
    // Check for accessibility violations
    const accessibilityScanResults = await page.accessibility.snapshot();
    expect(accessibilityScanResults).toBeTruthy();
    
    // Tab navigation
    await page.keyboard.press('Tab');
    const firstFocused = await page.evaluate(() => document.activeElement.tagName);
    expect(firstFocused).toBe('A'); // Should focus on link
    
    // Check ARIA labels
    const searchInput = page.locator('[data-testid="search-input"]');
    await expect(searchInput).toHaveAttribute('aria-label', 'Search products');
    
    // Check color contrast
    const contrastRatio = await page.evaluate(() => {
      const element = document.querySelector('button');
      const styles = window.getComputedStyle(element);
      // Simplified contrast check
      return styles.color !== styles.backgroundColor;
    });
    expect(contrastRatio).toBeTruthy();
  });
});
```

### Hands-On Exercise: Create E2E Tests
Build comprehensive E2E tests for your application

### Afternoon Session: Test Automation
**Duration:** 90 minutes

#### CI/CD Test Pipeline
```yaml
# test-pipeline.yml
name: Comprehensive Testing Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [16, 18, 20]
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node-version }}
      
      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: ~/.npm
          key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run unit tests
        run: npm run test:unit -- --coverage
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage/lcov.info
          flags: unit
  
  integration-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_PASSWORD: testpass
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run migrations
        env:
          DATABASE_URL: postgresql://postgres:testpass@localhost:5432/testdb
        run: npm run migrate:test
      
      - name: Run integration tests
        env:
          DATABASE_URL: postgresql://postgres:testpass@localhost:5432/testdb
          REDIS_URL: redis://localhost:6379
        run: npm run test:integration
  
  e2e-tests:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Install Playwright
        run: npx playwright install --with-deps
      
      - name: Start application
        run: |
          npm run build
          npm run start &
          npx wait-on http://localhost:3000
      
      - name: Run E2E tests
        run: npm run test:e2e
      
      - name: Upload test artifacts
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: playwright-report/
  
  performance-tests:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Lighthouse CI
        uses: treosh/lighthouse-ci-action@v10
        with:
          urls: |
            http://localhost:3000
            http://localhost:3000/products
            http://localhost:3000/cart
          uploadArtifacts: true
          temporaryPublicStorage: true
      
      - name: Run load tests
        run: |
          npm install -g k6
          k6 run tests/load/script.js
  
  security-tests:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Run security audit
        run: npm audit --audit-level=moderate
      
      - name: Run OWASP ZAP scan
        uses: zaproxy/action-full-scan@v0.7.0
        with:
          target: 'http://localhost:3000'
      
      - name: Run Snyk security test
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

## Day 3: Performance Testing

### Morning Session: Load Testing
**Duration:** 90 minutes

#### Load Testing with k6
```javascript
// load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

const errorRate = new Rate('errors');

export const options = {
  stages: [
    { duration: '2m', target: 100 },  // Ramp up
    { duration: '5m', target: 100 },  // Stay at 100 users
    { duration: '2m', target: 200 },  // Ramp up
    { duration: '5m', target: 200 },  // Stay at 200 users
    { duration: '2m', target: 500 },  // Ramp up
    { duration: '5m', target: 500 },  // Stay at 500 users
    { duration: '5m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests under 500ms
    errors: ['rate<0.01'],            // Error rate under 1%
  },
};

export default function () {
  // Homepage
  let res = http.get('http://localhost:3000');
  check(res, {
    'homepage status is 200': (r) => r.status === 200,
    'homepage load time < 200ms': (r) => r.timings.duration < 200,
  });
  errorRate.add(res.status !== 200);
  
  sleep(1);
  
  // Search products
  res = http.get('http://localhost:3000/api/products?search=laptop');
  check(res, {
    'search status is 200': (r) => r.status === 200,
    'search returns results': (r) => JSON.parse(r.body).length > 0,
  });
  
  sleep(1);
  
  // View product
  res = http.get('http://localhost:3000/api/products/1');
  check(res, {
    'product status is 200': (r) => r.status === 200,
  });
  
  sleep(1);
  
  // Add to cart
  res = http.post('http://localhost:3000/api/cart', 
    JSON.stringify({ productId: 1, quantity: 1 }),
    { headers: { 'Content-Type': 'application/json' } }
  );
  check(res, {
    'add to cart status is 201': (r) => r.status === 201,
  });
  
  sleep(1);
}

export function handleSummary(data) {
  return {
    'summary.html': htmlReport(data),
    'summary.json': JSON.stringify(data),
  };
}
```

### Hands-On Exercise: Performance Optimization
Identify and fix performance bottlenecks

### Afternoon Session: Security Testing
**Duration:** 90 minutes

#### Security Test Suite
```javascript
// security-tests.js
describe('Security Tests', () => {
  describe('SQL Injection', () => {
    test('should prevent SQL injection in login', async () => {
      const maliciousInput = "' OR '1'='1";
      const response = await request(app)
        .post('/api/login')
        .send({
          email: maliciousInput,
          password: maliciousInput
        });
      
      expect(response.status).toBe(401);
      expect(response.body).not.toContain('SQL');
    });
    
    test('should sanitize user input', async () => {
      const injectionAttempt = "'; DROP TABLE users; --";
      const response = await request(app)
        .post('/api/products/search')
        .send({ query: injectionAttempt });
      
      expect(response.status).toBe(200);
      // Verify database integrity
      const users = await db.query('SELECT COUNT(*) FROM users');
      expect(users.rows[0].count).toBeGreaterThan(0);
    });
  });
  
  describe('XSS Prevention', () => {
    test('should escape HTML in user content', async () => {
      const xssPayload = '<script>alert("XSS")</script>';
      const response = await request(app)
        .post('/api/comments')
        .send({ content: xssPayload });
      
      const comment = response.body;
      expect(comment.content).not.toContain('<script>');
      expect(comment.content).toContain('&lt;script&gt;');
    });
  });
  
  describe('Authentication', () => {
    test('should enforce rate limiting on login', async () => {
      const attempts = [];
      for (let i = 0; i < 10; i++) {
        attempts.push(
          request(app)
            .post('/api/login')
            .send({ email: 'test@test.com', password: 'wrong' })
        );
      }
      
      const responses = await Promise.all(attempts);
      const blocked = responses.filter(r => r.status === 429);
      expect(blocked.length).toBeGreaterThan(0);
    });
    
    test('should invalidate tokens on logout', async () => {
      const loginRes = await request(app)
        .post('/api/login')
        .send({ email: 'test@test.com', password: 'password' });
      
      const token = loginRes.body.token;
      
      await request(app)
        .post('/api/logout')
        .set('Authorization', `Bearer ${token}`);
      
      const response = await request(app)
        .get('/api/profile')
        .set('Authorization', `Bearer ${token}`);
      
      expect(response.status).toBe(401);
    });
  });
});
```

## Day 4: Continuous Quality

### Morning Session: Code Quality Tools
**Duration:** 90 minutes

#### Quality Automation
```javascript
// quality-checks.js
const eslint = require('eslint');
const { SonarScanner } = require('sonarqube-scanner');

class QualityChecker {
  async runESLint() {
    const cli = new eslint.ESLint({
      extensions: ['.js', '.jsx', '.ts', '.tsx'],
      fix: true
    });
    
    const results = await cli.lintFiles(['src/**/*']);
    
    await eslint.ESLint.outputFixes(results);
    
    const formatter = await cli.loadFormatter('stylish');
    const resultText = formatter.format(results);
    
    console.log(resultText);
    
    const hasErrors = results.some(r => r.errorCount > 0);
    if (hasErrors) {
      throw new Error('ESLint found errors');
    }
  }
  
  async runSonarQube() {
    await SonarScanner({
      serverUrl: 'http://localhost:9000',
      token: process.env.SONAR_TOKEN,
      options: {
        'sonar.projectKey': 'my-project',
        'sonar.sources': './src',
        'sonar.tests': './tests',
        'sonar.javascript.lcov.reportPaths': 'coverage/lcov.info',
        'sonar.exclusions': '**/*.test.js',
      }
    });
  }
  
  async checkCoverage() {
    const coverage = require('./coverage/coverage-summary.json');
    
    const metrics = {
      lines: coverage.total.lines.pct,
      statements: coverage.total.statements.pct,
      functions: coverage.total.functions.pct,
      branches: coverage.total.branches.pct
    };
    
    const threshold = 80;
    
    for (const [metric, value] of Object.entries(metrics)) {
      if (value < threshold) {
        throw new Error(`Coverage ${metric}: ${value}% is below threshold ${threshold}%`);
      }
    }
    
    console.log('Coverage check passed:', metrics);
  }
}
```

### Afternoon Session: Monitoring & Alerting
**Duration:** 90 minutes

#### Production Monitoring
```javascript
// monitoring.js
const Sentry = require('@sentry/node');
const prometheus = require('prom-client');

class ProductionMonitoring {
  constructor() {
    this.initSentry();
    this.initMetrics();
  }
  
  initSentry() {
    Sentry.init({
      dsn: process.env.SENTRY_DSN,
      environment: process.env.NODE_ENV,
      tracesSampleRate: 1.0,
      profilesSampleRate: 1.0,
      integrations: [
        new Sentry.Integrations.Http({ tracing: true }),
        new Sentry.Integrations.Express({ app }),
      ],
    });
  }
  
  initMetrics() {
    // Custom metrics
    this.testExecutionTime = new prometheus.Histogram({
      name: 'test_execution_duration_seconds',
      help: 'Test execution time in seconds',
      labelNames: ['test_suite', 'test_name', 'status']
    });
    
    this.testFailureRate = new prometheus.Counter({
      name: 'test_failures_total',
      help: 'Total number of test failures',
      labelNames: ['test_suite', 'test_name']
    });
    
    this.codeQualityScore = new prometheus.Gauge({
      name: 'code_quality_score',
      help: 'Code quality score from static analysis',
      labelNames: ['metric']
    });
  }
  
  trackTestExecution(suite, name, duration, passed) {
    this.testExecutionTime
      .labels(suite, name, passed ? 'pass' : 'fail')
      .observe(duration);
    
    if (!passed) {
      this.testFailureRate.labels(suite, name).inc();
    }
  }
  
  updateQualityMetrics(metrics) {
    this.codeQualityScore.labels('complexity').set(metrics.complexity);
    this.codeQualityScore.labels('maintainability').set(metrics.maintainability);
    this.codeQualityScore.labels('coverage').set(metrics.coverage);
  }
}
```

## Day 5: Quality Assurance Project

### Full Day Project: Complete Testing Suite
**Duration:** 3 hours

#### Build a Testing Framework
```javascript
// Project: AI-Powered Testing Framework
class AITestingFramework {
  constructor() {
    this.testSuites = [];
    this.coverage = {};
    this.metrics = {};
  }
  
  async generateTestsFromCode(filePath) {
    const code = await fs.readFile(filePath, 'utf8');
    const prompt = `
      Analyze this code and generate:
      1. Unit tests with 100% coverage
      2. Integration test scenarios
      3. Edge cases to test
      4. Performance benchmarks
      
      Code: ${code}
    `;
    
    return await claude.generate(prompt);
  }
  
  async runAllTests() {
    const results = {
      unit: await this.runUnitTests(),
      integration: await this.runIntegrationTests(),
      e2e: await this.runE2ETests(),
      performance: await this.runPerformanceTests(),
      security: await this.runSecurityTests()
    };
    
    await this.generateReport(results);
    return results;
  }
  
  async generateReport(results) {
    const report = {
      timestamp: new Date().toISOString(),
      summary: {
        total: 0,
        passed: 0,
        failed: 0,
        skipped: 0
      },
      coverage: await this.calculateCoverage(),
      performance: await this.analyzePerformance(),
      security: await this.securityAudit(),
      recommendations: await this.generateRecommendations(results)
    };
    
    await fs.writeFile('test-report.html', this.renderHTMLReport(report));
    await fs.writeFile('test-report.json', JSON.stringify(report, null, 2));
    
    return report;
  }
}

// Implementation of complete testing pipeline
const framework = new AITestingFramework();
await framework.runAllTests();
```

## Weekend Assignment

### Create a Quality Dashboard
1. Build a real-time testing dashboard
2. Integrate all testing types
3. Set up automated reporting
4. Implement quality gates
5. Create documentation

### Required Deliverables
- [ ] 90%+ test coverage
- [ ] All test types implemented
- [ ] CI/CD pipeline with tests
- [ ] Quality dashboard deployed
- [ ] Performance report

## Assessment Rubric

| Criteria | Basic (60%) | Proficient (80%) | Advanced (100%) |
|----------|-------------|------------------|-----------------|
| Unit Tests | 70% coverage | 85% coverage | 95%+ coverage |
| Integration | Basic tests | Comprehensive | Full coverage |
| E2E Tests | Happy path | Multiple flows | Edge cases |
| Performance | Basic metrics | Load testing | Stress testing |
| Security | Basic checks | OWASP top 10 | Penetration testing |

## Resources

### Required Reading
- [Testing JavaScript Applications](https://www.manning.com/books/testing-javascript-applications)
- [The Art of Unit Testing](https://www.manning.com/books/the-art-of-unit-testing-third-edition)
- [Performance Testing Guidance](https://docs.microsoft.com/en-us/azure/architecture/best-practices/performance-testing)

### Video Tutorials
- [TDD with AI Assistance](https://youtube.com/watch?v=example)
- [E2E Testing Best Practices](https://youtube.com/watch?v=example)
- [Security Testing Guide](https://youtube.com/watch?v=example)

### Testing Tools
- **Jest**: Unit testing
- **Playwright**: E2E testing
- **k6**: Load testing
- **SonarQube**: Code quality
- **Sentry**: Error monitoring

## Office Hours

**Thursday, 3-5 PM EST**
- Test strategy review
- Debugging test failures
- Performance optimization
- Security consultation

## Next Week Preview

Week 6: Deployment & DevOps
- CI/CD pipelines
- Container orchestration
- Cloud deployment
- Monitoring & logging
- Production operations

---

💡 **Testing Tips:**
- Test early and often
- Automate everything
- Focus on critical paths
- Monitor continuously
- Document thoroughly

🎯 **Success Metrics:**
- All tests passing
- >90% coverage
- <100ms response time
- Zero security issues
- Automated pipeline

Ready to ensure quality? Let's test! 🧪
