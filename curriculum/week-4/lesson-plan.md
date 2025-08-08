# Week 4: Creating Code - Part 2 (Advanced Implementation)

## Overview
This week elevates your coding skills to architect-level, focusing on building complex, production-ready applications with AI assistance. You'll master advanced patterns, integrations, and enterprise-level development.

## Learning Objectives
By the end of this week, you will:
- ✅ Build complex microservices architectures
- ✅ Implement real-time features with WebSockets
- ✅ Create AI-powered features within applications
- ✅ Master advanced state management
- ✅ Deploy distributed systems

## Day 1: Advanced Application Architecture

### Morning Session: Microservices with AI
**Duration:** 90 minutes

#### Microservices Generator
```javascript
// microservices-architect.js
class MicroservicesArchitect {
  async generateService(spec) {
    const prompt = `
      Create a microservice for: ${spec.name}
      Purpose: ${spec.purpose}
      
      Include:
      - Express/Fastify server
      - Database connection (${spec.database})
      - Message queue integration (RabbitMQ/Kafka)
      - Service discovery
      - Health checks
      - Metrics collection
      - Distributed tracing
      - Circuit breaker pattern
      - Rate limiting
      - Authentication/Authorization
      - Docker configuration
      - Kubernetes manifests
    `;
    
    return await claude.generate(prompt);
  }
  
  async generateAPIGateway(services) {
    const prompt = `
      Create an API Gateway for services:
      ${services.map(s => `- ${s.name}: ${s.endpoints}`).join('\n')}
      
      Include:
      - Request routing
      - Load balancing
      - Authentication
      - Rate limiting
      - Request/Response transformation
      - Caching
      - Monitoring
      - WebSocket support
    `;
    
    return await claude.generate(prompt);
  }
}

// Generated User Service
const express = require('express');
const { Kafka } = require('kafkajs');
const Redis = require('ioredis');
const prometheus = require('prom-client');
const CircuitBreaker = require('opossum');

class UserService {
  constructor() {
    this.app = express();
    this.redis = new Redis({
      host: process.env.REDIS_HOST,
      port: process.env.REDIS_PORT
    });
    
    this.kafka = new Kafka({
      clientId: 'user-service',
      brokers: [process.env.KAFKA_BROKER]
    });
    
    this.producer = this.kafka.producer();
    this.consumer = this.kafka.consumer({ groupId: 'user-group' });
    
    this.initializeMetrics();
    this.setupCircuitBreaker();
    this.setupRoutes();
    this.setupEventHandlers();
  }
  
  initializeMetrics() {
    this.metrics = {
      httpRequestDuration: new prometheus.Histogram({
        name: 'http_request_duration_seconds',
        help: 'Duration of HTTP requests in seconds',
        labelNames: ['method', 'route', 'status']
      }),
      
      activeUsers: new prometheus.Gauge({
        name: 'active_users_total',
        help: 'Total number of active users'
      })
    };
    
    prometheus.collectDefaultMetrics();
  }
  
  setupCircuitBreaker() {
    const options = {
      timeout: 3000,
      errorThresholdPercentage: 50,
      resetTimeout: 30000
    };
    
    this.breaker = new CircuitBreaker(this.callExternalService, options);
    
    this.breaker.on('open', () => {
      console.log('Circuit breaker opened');
    });
    
    this.breaker.on('halfOpen', () => {
      console.log('Circuit breaker half-open');
    });
    
    this.breaker.on('close', () => {
      console.log('Circuit breaker closed');
    });
  }
  
  setupRoutes() {
    // Health check
    this.app.get('/health', (req, res) => {
      res.json({
        status: 'healthy',
        service: 'user-service',
        timestamp: new Date().toISOString()
      });
    });
    
    // Metrics endpoint
    this.app.get('/metrics', async (req, res) => {
      res.set('Content-Type', prometheus.register.contentType);
      res.end(await prometheus.register.metrics());
    });
    
    // User endpoints
    this.app.post('/users', this.createUser.bind(this));
    this.app.get('/users/:id', this.getUser.bind(this));
    this.app.put('/users/:id', this.updateUser.bind(this));
    this.app.delete('/users/:id', this.deleteUser.bind(this));
  }
  
  async createUser(req, res) {
    const startTime = Date.now();
    
    try {
      // Create user logic
      const user = await this.userRepository.create(req.body);
      
      // Cache user
      await this.redis.setex(
        `user:${user.id}`,
        3600,
        JSON.stringify(user)
      );
      
      // Publish event
      await this.producer.send({
        topic: 'user-events',
        messages: [{
          key: 'user.created',
          value: JSON.stringify({
            eventType: 'USER_CREATED',
            userId: user.id,
            timestamp: new Date().toISOString(),
            data: user
          })
        }]
      });
      
      // Update metrics
      this.metrics.activeUsers.inc();
      this.metrics.httpRequestDuration
        .labels('POST', '/users', '201')
        .observe((Date.now() - startTime) / 1000);
      
      res.status(201).json(user);
    } catch (error) {
      this.metrics.httpRequestDuration
        .labels('POST', '/users', '500')
        .observe((Date.now() - startTime) / 1000);
      
      res.status(500).json({ error: error.message });
    }
  }
  
  async setupEventHandlers() {
    await this.consumer.connect();
    await this.consumer.subscribe({
      topic: 'user-commands',
      fromBeginning: false
    });
    
    await this.consumer.run({
      eachMessage: async ({ topic, partition, message }) => {
        const command = JSON.parse(message.value.toString());
        
        switch (command.type) {
          case 'SYNC_USER':
            await this.syncUser(command.data);
            break;
          case 'BULK_UPDATE':
            await this.bulkUpdate(command.data);
            break;
          default:
            console.log('Unknown command:', command.type);
        }
      }
    });
  }
  
  async start() {
    await this.producer.connect();
    
    const port = process.env.PORT || 3000;
    this.app.listen(port, () => {
      console.log(`User service running on port ${port}`);
    });
  }
}

// Docker configuration
const dockerfile = `
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3000
CMD ["node", "index.js"]
`;

// Kubernetes deployment
const k8sDeployment = `
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: user-service
  template:
    metadata:
      labels:
        app: user-service
    spec:
      containers:
      - name: user-service
        image: user-service:latest
        ports:
        - containerPort: 3000
        env:
        - name: REDIS_HOST
          value: redis-service
        - name: KAFKA_BROKER
          value: kafka-service:9092
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: user-service
spec:
  selector:
    app: user-service
  ports:
  - port: 3000
    targetPort: 3000
  type: ClusterIP
`;
```

### Hands-On Exercise: Build a Distributed System
Create a complete e-commerce system with separate services for users, products, orders, payments, and notifications

### Afternoon Session: Event-Driven Architecture
**Duration:** 90 minutes

#### Event Sourcing Implementation
```javascript
// event-sourcing.js
class EventStore {
  constructor() {
    this.events = [];
    this.snapshots = new Map();
    this.projections = new Map();
  }
  
  async append(streamId, event) {
    const eventWithMeta = {
      streamId,
      eventId: uuid(),
      eventType: event.type,
      eventData: event.data,
      eventMetadata: {
        timestamp: new Date().toISOString(),
        userId: event.userId,
        correlationId: event.correlationId
      },
      eventVersion: this.getStreamVersion(streamId) + 1
    };
    
    this.events.push(eventWithMeta);
    
    // Update projections
    await this.updateProjections(eventWithMeta);
    
    // Publish to message bus
    await this.publish(eventWithMeta);
    
    return eventWithMeta;
  }
  
  async getEvents(streamId, fromVersion = 0) {
    return this.events.filter(
      e => e.streamId === streamId && e.eventVersion > fromVersion
    );
  }
  
  async replay(streamId) {
    const events = await this.getEvents(streamId);
    const aggregate = this.createAggregate(streamId);
    
    for (const event of events) {
      aggregate.apply(event);
    }
    
    return aggregate;
  }
  
  createAggregate(streamId) {
    return {
      id: streamId,
      version: 0,
      state: {},
      
      apply(event) {
        switch (event.eventType) {
          case 'OrderCreated':
            this.state = {
              ...this.state,
              id: event.eventData.orderId,
              items: event.eventData.items,
              status: 'created',
              total: event.eventData.total
            };
            break;
            
          case 'OrderPaid':
            this.state.status = 'paid';
            this.state.paidAt = event.eventData.paidAt;
            break;
            
          case 'OrderShipped':
            this.state.status = 'shipped';
            this.state.shippedAt = event.eventData.shippedAt;
            this.state.trackingNumber = event.eventData.trackingNumber;
            break;
            
          case 'OrderDelivered':
            this.state.status = 'delivered';
            this.state.deliveredAt = event.eventData.deliveredAt;
            break;
        }
        
        this.version = event.eventVersion;
      }
    };
  }
}
```

## Day 2: Real-time Features

### Morning Session: WebSocket Implementation
**Duration:** 90 minutes

#### Real-time Collaboration System
```javascript
// collaboration-server.js
const WebSocket = require('ws');
const Y = require('yjs');
const { WebsocketProvider } = require('y-websocket');

class CollaborationServer {
  constructor() {
    this.documents = new Map();
    this.connections = new Map();
    this.wss = new WebSocket.Server({ port: 8080 });
    
    this.setupWebSocketServer();
  }
  
  setupWebSocketServer() {
    this.wss.on('connection', (ws, req) => {
      const documentId = this.getDocumentId(req.url);
      const userId = this.getUserId(req);
      
      this.handleConnection(ws, documentId, userId);
    });
  }
  
  handleConnection(ws, documentId, userId) {
    // Get or create document
    let doc = this.documents.get(documentId);
    if (!doc) {
      doc = new Y.Doc();
      this.documents.set(documentId, doc);
    }
    
    // Track connection
    if (!this.connections.has(documentId)) {
      this.connections.set(documentId, new Set());
    }
    this.connections.get(documentId).add({ ws, userId });
    
    // Send initial state
    const state = Y.encodeStateAsUpdate(doc);
    ws.send(JSON.stringify({
      type: 'sync',
      data: Array.from(state)
    }));
    
    // Send active users
    this.broadcastActiveUsers(documentId);
    
    // Handle messages
    ws.on('message', (message) => {
      const msg = JSON.parse(message);
      
      switch (msg.type) {
        case 'update':
          this.handleUpdate(documentId, msg.data, userId);
          break;
          
        case 'cursor':
          this.handleCursorUpdate(documentId, userId, msg.data);
          break;
          
        case 'presence':
          this.handlePresenceUpdate(documentId, userId, msg.data);
          break;
          
        case 'comment':
          this.handleComment(documentId, userId, msg.data);
          break;
      }
    });
    
    // Handle disconnect
    ws.on('close', () => {
      const connections = this.connections.get(documentId);
      connections.delete({ ws, userId });
      
      if (connections.size === 0) {
        // Save document to database
        this.saveDocument(documentId, doc);
        this.documents.delete(documentId);
        this.connections.delete(documentId);
      } else {
        this.broadcastActiveUsers(documentId);
      }
    });
  }
  
  handleUpdate(documentId, update, userId) {
    const doc = this.documents.get(documentId);
    Y.applyUpdate(doc, new Uint8Array(update));
    
    // Broadcast to all other clients
    const connections = this.connections.get(documentId);
    connections.forEach(({ ws, userId: connUserId }) => {
      if (connUserId !== userId) {
        ws.send(JSON.stringify({
          type: 'update',
          data: update,
          userId
        }));
      }
    });
    
    // Auto-save periodically
    this.scheduleSave(documentId);
  }
  
  handleCursorUpdate(documentId, userId, cursor) {
    const connections = this.connections.get(documentId);
    connections.forEach(({ ws, userId: connUserId }) => {
      if (connUserId !== userId) {
        ws.send(JSON.stringify({
          type: 'cursor',
          userId,
          data: cursor
        }));
      }
    });
  }
  
  handlePresenceUpdate(documentId, userId, presence) {
    const connections = this.connections.get(documentId);
    connections.forEach(({ ws }) => {
      ws.send(JSON.stringify({
        type: 'presence',
        userId,
        data: presence
      }));
    });
  }
  
  handleComment(documentId, userId, comment) {
    // Store comment
    this.storeComment(documentId, {
      ...comment,
      userId,
      timestamp: new Date().toISOString()
    });
    
    // Broadcast to all clients
    const connections = this.connections.get(documentId);
    connections.forEach(({ ws }) => {
      ws.send(JSON.stringify({
        type: 'comment',
        userId,
        data: comment
      }));
    });
  }
  
  broadcastActiveUsers(documentId) {
    const connections = this.connections.get(documentId);
    const users = Array.from(connections).map(({ userId }) => userId);
    
    connections.forEach(({ ws }) => {
      ws.send(JSON.stringify({
        type: 'activeUsers',
        data: users
      }));
    });
  }
}

// Client-side implementation
class CollaborationClient {
  constructor(documentId, userId) {
    this.documentId = documentId;
    this.userId = userId;
    this.doc = new Y.Doc();
    this.awareness = new awarenessProtocol.Awareness(this.doc);
    
    this.connect();
  }
  
  connect() {
    this.ws = new WebSocket(`ws://localhost:8080/${this.documentId}`);
    
    this.ws.onopen = () => {
      console.log('Connected to collaboration server');
      this.setupBindings();
    };
    
    this.ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      this.handleMessage(msg);
    };
    
    this.ws.onclose = () => {
      console.log('Disconnected from collaboration server');
      this.reconnect();
    };
  }
  
  setupBindings() {
    // Bind to editor
    this.binding = new Y.QuillBinding(
      this.doc.getText('content'),
      this.editor,
      this.awareness
    );
    
    // Listen for local changes
    this.doc.on('update', (update) => {
      this.ws.send(JSON.stringify({
        type: 'update',
        data: Array.from(update)
      }));
    });
    
    // Track cursor position
    this.editor.on('selection-change', (range) => {
      if (range) {
        this.ws.send(JSON.stringify({
          type: 'cursor',
          data: range
        }));
      }
    });
  }
  
  handleMessage(msg) {
    switch (msg.type) {
      case 'sync':
        Y.applyUpdate(this.doc, new Uint8Array(msg.data));
        break;
        
      case 'update':
        Y.applyUpdate(this.doc, new Uint8Array(msg.data));
        break;
        
      case 'cursor':
        this.showRemoteCursor(msg.userId, msg.data);
        break;
        
      case 'activeUsers':
        this.updateActiveUsers(msg.data);
        break;
        
      case 'comment':
        this.showComment(msg.userId, msg.data);
        break;
    }
  }
}
```

### Afternoon Session: GraphQL Subscriptions
**Duration:** 90 minutes

#### Real-time GraphQL API
```javascript
// graphql-subscriptions.js
const { GraphQLServer, PubSub } = require('graphql-yoga');
const { RedisPubSub } = require('graphql-redis-subscriptions');

const pubsub = new RedisPubSub({
  publisher: redisClient,
  subscriber: redisClient
});

const typeDefs = `
  type Message {
    id: ID!
    user: User!
    content: String!
    createdAt: DateTime!
    editedAt: DateTime
    reactions: [Reaction!]!
  }
  
  type User {
    id: ID!
    username: String!
    avatar: String
    status: UserStatus!
    typing: Boolean!
  }
  
  enum UserStatus {
    ONLINE
    AWAY
    BUSY
    OFFLINE
  }
  
  type Reaction {
    emoji: String!
    user: User!
    createdAt: DateTime!
  }
  
  type Query {
    messages(channelId: ID!, limit: Int, before: ID): [Message!]!
    activeUsers(channelId: ID!): [User!]!
  }
  
  type Mutation {
    sendMessage(channelId: ID!, content: String!): Message!
    editMessage(messageId: ID!, content: String!): Message!
    deleteMessage(messageId: ID!): Boolean!
    addReaction(messageId: ID!, emoji: String!): Reaction!
    removeReaction(messageId: ID!, emoji: String!): Boolean!
    setTyping(channelId: ID!, typing: Boolean!): Boolean!
    updateStatus(status: UserStatus!): User!
  }
  
  type Subscription {
    messageAdded(channelId: ID!): Message!
    messageUpdated(channelId: ID!): Message!
    messageDeleted(channelId: ID!): ID!
    reactionAdded(channelId: ID!): ReactionEvent!
    reactionRemoved(channelId: ID!): ReactionEvent!
    userTyping(channelId: ID!): TypingEvent!
    userStatusChanged(userId: ID!): User!
    userJoined(channelId: ID!): User!
    userLeft(channelId: ID!): User!
  }
  
  type ReactionEvent {
    messageId: ID!
    reaction: Reaction!
  }
  
  type TypingEvent {
    user: User!
    typing: Boolean!
  }
`;

const resolvers = {
  Query: {
    messages: async (_, { channelId, limit = 50, before }) => {
      return await Message.find({ channelId })
        .lt('_id', before || new Date())
        .sort('-createdAt')
        .limit(limit)
        .populate('user');
    },
    
    activeUsers: async (_, { channelId }) => {
      return await redis.smembers(`channel:${channelId}:users`);
    }
  },
  
  Mutation: {
    sendMessage: async (_, { channelId, content }, { user }) => {
      const message = await Message.create({
        channelId,
        user: user.id,
        content,
        createdAt: new Date()
      });
      
      await message.populate('user');
      
      // Publish to subscribers
      await pubsub.publish(`MESSAGE_ADDED_${channelId}`, {
        messageAdded: message
      });
      
      // Send push notifications
      await sendPushNotifications(channelId, message);
      
      return message;
    },
    
    editMessage: async (_, { messageId, content }, { user }) => {
      const message = await Message.findOneAndUpdate(
        { _id: messageId, user: user.id },
        { content, editedAt: new Date() },
        { new: true }
      ).populate('user');
      
      if (!message) {
        throw new Error('Message not found or unauthorized');
      }
      
      await pubsub.publish(`MESSAGE_UPDATED_${message.channelId}`, {
        messageUpdated: message
      });
      
      return message;
    },
    
    setTyping: async (_, { channelId, typing }, { user }) => {
      await pubsub.publish(`USER_TYPING_${channelId}`, {
        userTyping: { user, typing }
      });
      
      // Auto-stop typing after 3 seconds
      if (typing) {
        setTimeout(() => {
          pubsub.publish(`USER_TYPING_${channelId}`, {
            userTyping: { user, typing: false }
          });
        }, 3000);
      }
      
      return true;
    }
  },
  
  Subscription: {
    messageAdded: {
      subscribe: (_, { channelId }) => {
        return pubsub.asyncIterator(`MESSAGE_ADDED_${channelId}`);
      }
    },
    
    messageUpdated: {
      subscribe: (_, { channelId }) => {
        return pubsub.asyncIterator(`MESSAGE_UPDATED_${channelId}`);
      }
    },
    
    userTyping: {
      subscribe: (_, { channelId }) => {
        return pubsub.asyncIterator(`USER_TYPING_${channelId}`);
      }
    }
  }
};

const server = new GraphQLServer({
  typeDefs,
  resolvers,
  context: ({ request, connection }) => {
    if (connection) {
      // For subscriptions
      return { user: connection.context.user };
    }
    // For queries and mutations
    return { user: getUserFromToken(request) };
  }
});

server.start({
  port: 4000,
  subscriptions: {
    onConnect: async (connectionParams) => {
      const user = await getUserFromToken(connectionParams.authToken);
      if (!user) {
        throw new Error('Authentication failed');
      }
      return { user };
    },
    onDisconnect: async (_, context) => {
      const { user } = await context.initPromise;
      // Update user status to offline
      await updateUserStatus(user.id, 'OFFLINE');
    }
  }
}, () => {
  console.log('GraphQL server running on http://localhost:4000');
});
```

## Day 3: AI-Powered Features

### Morning Session: Integrating AI into Applications
**Duration:** 90 minutes

#### AI Feature Generator
```javascript
// ai-features.js
class AIFeatureIntegration {
  async addSmartSearch(application) {
    const implementation = `
      // Semantic search with embeddings
      const { OpenAI } = require('openai');
      const pinecone = require('@pinecone-database/pinecone');
      
      class SmartSearch {
        constructor() {
          this.openai = new OpenAI({ apiKey: process.env.OPENAI_KEY });
          this.pinecone = new pinecone.Client();
          this.index = this.pinecone.Index('products');
        }
        
        async indexProduct(product) {
          // Generate embedding
          const embedding = await this.openai.embeddings.create({
            model: 'text-embedding-ada-002',
            input: \`\${product.name} \${product.description} \${product.category}\`
          });
          
          // Store in vector database
          await this.index.upsert([{
            id: product.id,
            values: embedding.data[0].embedding,
            metadata: {
              name: product.name,
              price: product.price,
              category: product.category,
              image: product.image
            }
          }]);
        }
        
        async search(query, filters = {}) {
          // Generate query embedding
          const queryEmbedding = await this.openai.embeddings.create({
            model: 'text-embedding-ada-002',
            input: query
          });
          
          // Search vector database
          const results = await this.index.query({
            vector: queryEmbedding.data[0].embedding,
            topK: 20,
            includeMetadata: true,
            filter: filters
          });
          
          // Re-rank with AI
          const reranked = await this.rerank(query, results.matches);
          
          return reranked;
        }
        
        async rerank(query, results) {
          const prompt = \`
            Query: \${query}
            
            Rank these products by relevance:
            \${results.map((r, i) => \`\${i+1}. \${r.metadata.name}\`).join('\\n')}
            
            Return top 10 as JSON array of IDs in order.
          \`;
          
          const response = await this.openai.completions.create({
            model: 'gpt-4',
            prompt,
            max_tokens: 200
          });
          
          const ids = JSON.parse(response.choices[0].text);
          return ids.map(id => results.find(r => r.id === id));
        }
      }
    `;
    
    return implementation;
  }
  
  async addContentGeneration() {
    return `
      // AI Content Generation
      class ContentGenerator {
        async generateProductDescription(product) {
          const prompt = \`
            Generate an engaging product description:
            Name: \${product.name}
            Category: \${product.category}
            Features: \${product.features.join(', ')}
            Price: \${product.price}
            
            Write 2-3 paragraphs highlighting benefits and use cases.
          \`;
          
          const response = await openai.completions.create({
            model: 'gpt-4',
            prompt,
            max_tokens: 300
          });
          
          return response.choices[0].text;
        }
        
        async generateEmailCampaign(segment, product) {
          const prompt = \`
            Create email campaign for:
            Segment: \${segment.name}
            Demographics: \${JSON.stringify(segment.demographics)}
            Product: \${product.name}
            
            Generate:
            1. Subject line (max 50 chars)
            2. Preview text (max 100 chars)
            3. Email body (HTML)
            4. Call-to-action
          \`;
          
          const response = await openai.completions.create({
            model: 'gpt-4',
            prompt,
            max_tokens: 1000
          });
          
          return this.parseEmailResponse(response.choices[0].text);
        }
        
        async generateSocialMedia(product, platforms) {
          const posts = {};
          
          for (const platform of platforms) {
            const prompt = \`
              Create \${platform} post for:
              Product: \${product.name}
              
              Requirements:
              \${this.getPlatformRequirements(platform)}
              
              Include relevant hashtags and emojis.
            \`;
            
            const response = await openai.completions.create({
              model: 'gpt-4',
              prompt,
              max_tokens: 200
            });
            
            posts[platform] = response.choices[0].text;
          }
          
          return posts;
        }
      }
    `;
  }
  
  async addPersonalization() {
    return `
      // AI-Powered Personalization
      class PersonalizationEngine {
        async getRecommendations(userId) {
          const user = await User.findById(userId);
          const history = await this.getUserHistory(userId);
          
          const prompt = \`
            User profile: \${JSON.stringify(user.profile)}
            Purchase history: \${JSON.stringify(history.purchases)}
            Browsing history: \${JSON.stringify(history.browsing)}
            
            Recommend 10 products with reasoning.
            Return as JSON with structure:
            [{ productId, score, reason }]
          \`;
          
          const response = await openai.completions.create({
            model: 'gpt-4',
            prompt,
            max_tokens: 500
          });
          
          return JSON.parse(response.choices[0].text);
        }
        
        async personalizeHomepage(userId) {
          const recommendations = await this.getRecommendations(userId);
          const segments = await this.getUserSegments(userId);
          
          return {
            hero: await this.selectHeroBanner(segments),
            featured: recommendations.slice(0, 4),
            categories: await this.personalizeCategories(userId),
            deals: await this.personalizeDeals(userId, segments)
          };
        }
        
        async predictChurn(userId) {
          const features = await this.extractUserFeatures(userId);
          
          const prompt = \`
            User features: \${JSON.stringify(features)}
            
            Predict churn probability (0-1) and provide:
            1. Risk score
            2. Key risk factors
            3. Retention strategies
            
            Return as JSON.
          \`;
          
          const response = await openai.completions.create({
            model: 'gpt-4',
            prompt,
            max_tokens: 300
          });
          
          const prediction = JSON.parse(response.choices[0].text);
          
          if (prediction.riskScore > 0.7) {
            await this.triggerRetentionCampaign(userId, prediction);
          }
          
          return prediction;
        }
      }
    `;
  }
}
```

### Hands-On Exercise: Build an AI-Powered E-commerce Platform
Implement smart search, personalized recommendations, and automated content generation

### Afternoon Session: Computer Vision Integration
**Duration:** 90 minutes

#### Image Processing Features
```javascript
// vision-features.js
class VisionFeatures {
  async implementImageSearch() {
    return `
      const vision = require('@google-cloud/vision');
      const client = new vision.ImageAnnotatorClient();
      
      class ImageSearch {
        async analyzeImage(imageUrl) {
          const [result] = await client.annotateImage({
            image: { source: { imageUri: imageUrl } },
            features: [
              { type: 'LABEL_DETECTION', maxResults: 10 },
              { type: 'OBJECT_LOCALIZATION', maxResults: 10 },
              { type: 'IMAGE_PROPERTIES' },
              { type: 'SAFE_SEARCH_DETECTION' }
            ]
          });
          
          return {
            labels: result.labelAnnotations,
            objects: result.localizedObjectAnnotations,
            colors: result.imagePropertiesAnnotation.dominantColors,
            safeSearch: result.safeSearchAnnotation
          };
        }
        
        async findSimilarProducts(imageUrl) {
          const analysis = await this.analyzeImage(imageUrl);
          
          // Extract features
          const features = {
            categories: analysis.labels.map(l => l.description),
            objects: analysis.objects.map(o => o.name),
            colors: analysis.colors.colors.map(c => c.color)
          };
          
          // Search for similar products
          const similar = await Product.find({
            $or: [
              { category: { $in: features.categories } },
              { tags: { $in: features.objects } },
              { colors: { $in: features.colors } }
            ]
          }).limit(20);
          
          // Rank by similarity
          return this.rankBySimilarity(features, similar);
        }
        
        async virtualTryOn(userImage, productImage) {
          // Use AI model for virtual try-on
          const response = await fetch('https://api.virtualtryon.ai/process', {
            method: 'POST',
            body: JSON.stringify({
              userImage,
              productImage,
              category: 'clothing'
            })
          });
          
          return await response.json();
        }
      }
    `;
  }
}
```

## Day 4: State Management & Performance

### Morning Session: Advanced State Management
**Duration:** 90 minutes

#### State Management Architecture
```javascript
// state-architecture.js
class StateArchitecture {
  generateReduxToolkit() {
    return `
      // Redux Toolkit Store
      import { configureStore, createSlice, createAsyncThunk } from '@reduxjs/toolkit';
      import { persistStore, persistReducer } from 'redux-persist';
      
      // User slice with async actions
      const userSlice = createSlice({
        name: 'user',
        initialState: {
          current: null,
          loading: false,
          error: null
        },
        reducers: {
          logout: (state) => {
            state.current = null;
          }
        },
        extraReducers: (builder) => {
          builder
            .addCase(fetchUser.pending, (state) => {
              state.loading = true;
            })
            .addCase(fetchUser.fulfilled, (state, action) => {
              state.loading = false;
              state.current = action.payload;
            })
            .addCase(fetchUser.rejected, (state, action) => {
              state.loading = false;
              state.error = action.error.message;
            });
        }
      });
      
      // Async thunk
      export const fetchUser = createAsyncThunk(
        'user/fetch',
        async (userId) => {
          const response = await api.get(\`/users/\${userId}\`);
          return response.data;
        }
      );
      
      // Cart slice with complex logic
      const cartSlice = createSlice({
        name: 'cart',
        initialState: {
          items: [],
          total: 0,
          discount: 0
        },
        reducers: {
          addItem: (state, action) => {
            const existing = state.items.find(i => i.id === action.payload.id);
            if (existing) {
              existing.quantity += 1;
            } else {
              state.items.push({ ...action.payload, quantity: 1 });
            }
            state.total = calculateTotal(state.items);
          },
          removeItem: (state, action) => {
            state.items = state.items.filter(i => i.id !== action.payload);
            state.total = calculateTotal(state.items);
          },
          applyDiscount: (state, action) => {
            state.discount = action.payload;
            state.total = calculateTotal(state.items) * (1 - state.discount);
          }
        }
      });
      
      // Configure store with persistence
      const persistConfig = {
        key: 'root',
        storage,
        whitelist: ['cart', 'user']
      };
      
      const rootReducer = combineReducers({
        user: userSlice.reducer,
        cart: cartSlice.reducer
      });
      
      const persistedReducer = persistReducer(persistConfig, rootReducer);
      
      export const store = configureStore({
        reducer: persistedReducer,
        middleware: (getDefaultMiddleware) =>
          getDefaultMiddleware({
            serializableCheck: {
              ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER]
            }
          })
      });
      
      export const persistor = persistStore(store);
    `;
  }
  
  generateZustand() {
    return `
      // Zustand Store with DevTools and Persistence
      import { create } from 'zustand';
      import { devtools, persist } from 'zustand/middleware';
      import { immer } from 'zustand/middleware/immer';
      
      interface Store {
        // State
        user: User | null;
        cart: CartItem[];
        wishlist: Product[];
        
        // Actions
        setUser: (user: User) => void;
        addToCart: (product: Product) => void;
        removeFromCart: (productId: string) => void;
        updateQuantity: (productId: string, quantity: number) => void;
        clearCart: () => void;
        toggleWishlist: (product: Product) => void;
        
        // Computed
        cartTotal: () => number;
        cartCount: () => number;
      }
      
      const useStore = create<Store>()(
        devtools(
          persist(
            immer((set, get) => ({
              // Initial state
              user: null,
              cart: [],
              wishlist: [],
              
              // Actions
              setUser: (user) => set((state) => {
                state.user = user;
              }),
              
              addToCart: (product) => set((state) => {
                const existing = state.cart.find(item => item.id === product.id);
                if (existing) {
                  existing.quantity += 1;
                } else {
                  state.cart.push({ ...product, quantity: 1 });
                }
              }),
              
              removeFromCart: (productId) => set((state) => {
                state.cart = state.cart.filter(item => item.id !== productId);
              }),
              
              updateQuantity: (productId, quantity) => set((state) => {
                const item = state.cart.find(i => i.id === productId);
                if (item) {
                  if (quantity === 0) {
                    state.cart = state.cart.filter(i => i.id !== productId);
                  } else {
                    item.quantity = quantity;
                  }
                }
              }),
              
              clearCart: () => set((state) => {
                state.cart = [];
              }),
              
              toggleWishlist: (product) => set((state) => {
                const index = state.wishlist.findIndex(p => p.id === product.id);
                if (index > -1) {
                  state.wishlist.splice(index, 1);
                } else {
                  state.wishlist.push(product);
                }
              }),
              
              // Computed
              cartTotal: () => {
                const state = get();
                return state.cart.reduce((total, item) => 
                  total + (item.price * item.quantity), 0
                );
              },
              
              cartCount: () => {
                const state = get();
                return state.cart.reduce((count, item) => 
                  count + item.quantity, 0
                );
              }
            })),
            {
              name: 'app-storage',
              partialize: (state) => ({
                cart: state.cart,
                wishlist: state.wishlist
              })
            }
          )
        )
      );
      
      export default useStore;
    `;
  }
}
```

### Afternoon Session: Performance Optimization
**Duration:** 90 minutes

#### Performance Optimization Toolkit
```javascript
// performance-toolkit.js
class PerformanceToolkit {
  generateOptimizedComponents() {
    return `
      // Optimized React Components
      import { memo, useMemo, useCallback, lazy, Suspense } from 'react';
      import { FixedSizeList as List } from 'react-window';
      
      // Memoized expensive component
      const ExpensiveComponent = memo(({ data, onUpdate }) => {
        // Memoize expensive calculations
        const processedData = useMemo(() => {
          return data.map(item => ({
            ...item,
            computed: heavyComputation(item)
          }));
        }, [data]);
        
        // Memoize callbacks
        const handleClick = useCallback((id) => {
          onUpdate(id);
        }, [onUpdate]);
        
        return (
          <div>
            {processedData.map(item => (
              <Item 
                key={item.id} 
                {...item} 
                onClick={handleClick}
              />
            ))}
          </div>
        );
      }, (prevProps, nextProps) => {
        // Custom comparison
        return prevProps.data === nextProps.data;
      });
      
      // Virtual scrolling for large lists
      const VirtualList = ({ items }) => {
        const Row = ({ index, style }) => (
          <div style={style}>
            <ProductCard product={items[index]} />
          </div>
        );
        
        return (
          <List
            height={600}
            itemCount={items.length}
            itemSize={120}
            width="100%"
          >
            {Row}
          </List>
        );
      };
      
      // Code splitting with lazy loading
      const Dashboard = lazy(() => 
        import(/* webpackChunkName: "dashboard" */ './Dashboard')
      );
      
      const Admin = lazy(() => 
        import(/* webpackChunkName: "admin" */ './Admin')
      );
      
      function App() {
        return (
          <Suspense fallback={<LoadingSpinner />}>
            <Routes>
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/admin" element={<Admin />} />
            </Routes>
          </Suspense>
        );
      }
      
      // Image optimization
      const OptimizedImage = ({ src, alt, ...props }) => {
        const [isIntersecting, setIsIntersecting] = useState(false);
        const imgRef = useRef(null);
        
        useEffect(() => {
          const observer = new IntersectionObserver(
            ([entry]) => {
              if (entry.isIntersecting) {
                setIsIntersecting(true);
                observer.disconnect();
              }
            },
            { threshold: 0.1 }
          );
          
          if (imgRef.current) {
            observer.observe(imgRef.current);
          }
          
          return () => observer.disconnect();
        }, []);
        
        return (
          <div ref={imgRef}>
            {isIntersecting ? (
              <img
                src={src}
                alt={alt}
                loading="lazy"
                {...props}
              />
            ) : (
              <div className="placeholder" />
            )}
          </div>
        );
      };
    `;
  }
}
```

## Day 5: Production Deployment

### Full Day Project: Deploy a Production System
**Duration:** 3 hours

#### Complete Production Setup
```javascript
// production-deployment.js
const deploymentPlan = {
  infrastructure: `
    # Terraform configuration
    terraform {
      required_providers {
        aws = {
          source  = "hashicorp/aws"
          version = "~> 4.0"
        }
        cloudflare = {
          source  = "cloudflare/cloudflare"
          version = "~> 3.0"
        }
      }
    }
    
    # ECS cluster for microservices
    resource "aws_ecs_cluster" "main" {
      name = "production-cluster"
      
      setting {
        name  = "containerInsights"
        value = "enabled"
      }
    }
    
    # RDS for database
    resource "aws_db_instance" "postgres" {
      identifier     = "prod-db"
      engine         = "postgres"
      engine_version = "14.7"
      instance_class = "db.r5.large"
      
      allocated_storage     = 100
      storage_encrypted     = true
      storage_type          = "gp3"
      
      multi_az               = true
      publicly_accessible    = false
      backup_retention_period = 30
      
      enabled_cloudwatch_logs_exports = ["postgresql"]
    }
    
    # ElastiCache for Redis
    resource "aws_elasticache_replication_group" "redis" {
      replication_group_id       = "prod-redis"
      replication_group_description = "Production Redis cluster"
      
      engine               = "redis"
      node_type            = "cache.r6g.large"
      number_cache_clusters = 3
      
      automatic_failover_enabled = true
      multi_az_enabled          = true
      
      at_rest_encryption_enabled = true
      transit_encryption_enabled = true
    }
  `,
  
  monitoring: `
    # Monitoring setup
    const prometheus = require('prom-client');
    const { CloudWatchClient } = require('@aws-sdk/client-cloudwatch');
    
    class MonitoringService {
      constructor() {
        this.cloudwatch = new CloudWatchClient({ region: 'us-east-1' });
        this.register = new prometheus.Registry();
        
        this.setupMetrics();
        this.setupAlerts();
      }
      
      setupMetrics() {
        // Business metrics
        this.orderCounter = new prometheus.Counter({
          name: 'orders_total',
          help: 'Total number of orders',
          labelNames: ['status', 'payment_method']
        });
        
        this.revenueGauge = new prometheus.Gauge({
          name: 'revenue_total',
          help: 'Total revenue',
          labelNames: ['currency']
        });
        
        this.responseTime = new prometheus.Histogram({
          name: 'http_request_duration_seconds',
          help: 'HTTP request latency',
          labelNames: ['method', 'route', 'status'],
          buckets: [0.1, 0.3, 0.5, 1, 3, 5, 10]
        });
        
        this.register.registerMetric(this.orderCounter);
        this.register.registerMetric(this.revenueGauge);
        this.register.registerMetric(this.responseTime);
      }
      
      setupAlerts() {
        // Alert configurations
        this.alerts = [
          {
            name: 'HighErrorRate',
            query: 'rate(http_requests_total{status=~"5.."}[5m]) > 0.05',
            duration: '5m',
            severity: 'critical',
            action: 'page'
          },
          {
            name: 'HighLatency',
            query: 'histogram_quantile(0.95, http_request_duration_seconds) > 1',
            duration: '10m',
            severity: 'warning',
            action: 'slack'
          },
          {
            name: 'LowDiskSpace',
            query: 'node_filesystem_avail_bytes / node_filesystem_size_bytes < 0.1',
            duration: '5m',
            severity: 'critical',
            action: 'page'
          }
        ];
      }
    }
  `,
  
  cicd: `
    # GitHub Actions CI/CD
    name: Production Deployment
    
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
          
          - name: Run tests
            run: |
              npm run test:unit
              npm run test:integration
              npm run test:e2e
          
          - name: Code coverage
            run: npm run test:coverage
          
          - name: SonarCloud scan
            uses: SonarSource/sonarcloud-github-action@master
            env:
              GITHUB_TOKEN: \${{ secrets.GITHUB_TOKEN }}
              SONAR_TOKEN: \${{ secrets.SONAR_TOKEN }}
      
      build:
        needs: test
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v3
          
          - name: Build Docker images
            run: |
              docker build -t app:latest .
              docker build -t app:\${{ github.sha }} .
          
          - name: Push to ECR
            env:
              AWS_REGION: us-east-1
            run: |
              aws ecr get-login-password | docker login --username AWS --password-stdin $ECR_REGISTRY
              docker tag app:latest $ECR_REGISTRY/app:latest
              docker tag app:\${{ github.sha }} $ECR_REGISTRY/app:\${{ github.sha }}
              docker push $ECR_REGISTRY/app:latest
              docker push $ECR_REGISTRY/app:\${{ github.sha }}
      
      deploy:
        needs: build
        runs-on: ubuntu-latest
        if: github.ref == 'refs/heads/main'
        steps:
          - name: Deploy to ECS
            run: |
              aws ecs update-service \
                --cluster production \
                --service app-service \
                --force-new-deployment
          
          - name: Wait for deployment
            run: |
              aws ecs wait services-stable \
                --cluster production \
                --services app-service
          
          - name: Run smoke tests
            run: npm run test:smoke
          
          - name: Notify Slack
            uses: 8398a7/action-slack@v3
            with:
              status: \${{ job.status }}
              text: 'Deployment completed'
              webhook_url: \${{ secrets.SLACK_WEBHOOK }}
  `
};
```

## Weekend Assignment

### Production-Ready Application
1. Build a complete microservices application
2. Implement comprehensive monitoring
3. Set up CI/CD pipeline
4. Deploy to cloud infrastructure
5. Perform load testing

### Required Deliverables
- [ ] Architecture diagram
- [ ] All microservices deployed
- [ ] Monitoring dashboard
- [ ] CI/CD pipeline running
- [ ] Load test results (>1000 RPS)
- [ ] Documentation

## Assessment Rubric

| Criteria | Basic (60%) | Proficient (80%) | Advanced (100%) |
|----------|-------------|------------------|-----------------|
| Architecture | Monolithic | Microservices | Event-driven |
| Real-time | Basic WebSocket | Full real-time | Collaborative |
| AI Features | One AI feature | Multiple features | AI-first design |
| Performance | Functional | Optimized | Highly optimized |
| Deployment | Single service | Multiple services | Full production |

## Resources

### Required Reading
- [Building Microservices](https://www.oreilly.com/library/view/building-microservices/9781491950340/)
- [Implementing Domain-Driven Design](https://www.amazon.com/Implementing-Domain-Driven-Design-Vaughn-Vernon/dp/0321834577)
- [Site Reliability Engineering](https://sre.google/books/)

### Video Tutorials
- [Microservices Architecture](https://youtube.com/watch?v=example)
- [Real-time with WebSockets](https://youtube.com/watch?v=example)
- [Production Deployment](https://youtube.com/watch?v=example)

### Tools & Platforms
- **Docker & Kubernetes**: Container orchestration
- **Terraform**: Infrastructure as code
- **Prometheus & Grafana**: Monitoring
- **GitHub Actions**: CI/CD
- **AWS/GCP/Azure**: Cloud platforms

## Office Hours

**Thursday, 3-5 PM EST**
- Architecture reviews
- Performance optimization
- Deployment assistance
- Troubleshooting

## Next Week Preview

Week 5: Testing & Quality Assurance
- Test-driven development
- Automated testing strategies
- Performance testing
- Security testing
- Continuous quality

---

💡 **Advanced Tips:**
- Design for failure
- Monitor everything
- Automate repetitively
- Document thoroughly
- Scale horizontally

🎯 **Success Metrics:**
- All features working
- <100ms response time
- >99.9% uptime
- Zero security issues
- Complete documentation

Ready for production? Let's ship! 🚢
