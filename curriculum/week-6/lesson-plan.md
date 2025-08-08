# Week 6: Deployment & DevOps

## Overview
This final week transforms you into a DevOps engineer who can deploy, scale, and maintain production systems. You'll master CI/CD, containerization, cloud platforms, and production operations.

## Learning Objectives
By the end of this week, you will:
- ✅ Build complete CI/CD pipelines
- ✅ Master Docker and Kubernetes
- ✅ Deploy to multiple cloud platforms
- ✅ Implement monitoring and logging
- ✅ Handle production incidents

## Day 1: CI/CD Mastery

### Morning Session: Pipeline Architecture
**Duration:** 90 minutes

#### Multi-Stage CI/CD Pipeline
```yaml
# .github/workflows/production-pipeline.yml
name: Production Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deployment environment'
        required: true
        default: 'staging'
        type: choice
        options:
          - development
          - staging
          - production

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # Stage 1: Code Quality
  quality:
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
      
      - name: Lint code
        run: npm run lint
      
      - name: Type check
        run: npm run type-check
      
      - name: Security audit
        run: |
          npm audit --audit-level=moderate
          npx snyk test
      
      - name: License check
        run: npx license-checker --onlyAllow 'MIT;Apache-2.0;BSD-3-Clause;BSD-2-Clause;ISC'
  
  # Stage 2: Testing
  test:
    needs: quality
    runs-on: ubuntu-latest
    strategy:
      matrix:
        test-suite: [unit, integration, e2e]
    
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_PASSWORD: testpass
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
      
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup test environment
        run: |
          cp .env.test .env
          npm ci
          npm run db:migrate:test
      
      - name: Run ${{ matrix.test-suite }} tests
        run: npm run test:${{ matrix.test-suite }}
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage/lcov.info
          flags: ${{ matrix.test-suite }}
  
  # Stage 3: Build
  build:
    needs: test
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
      image-digest: ${{ steps.build.outputs.digest }}
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Log in to Container Registry
        uses: docker/login-action@v2
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha,prefix={{branch}}-
      
      - name: Build and push Docker image
        id: build
        uses: docker/build-push-action@v4
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          build-args: |
            VERSION=${{ github.sha }}
            BUILD_DATE=${{ github.event.head_commit.timestamp }}
  
  # Stage 4: Security Scanning
  security:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ needs.build.outputs.image-tag }}
          format: 'sarif'
          output: 'trivy-results.sarif'
      
      - name: Upload Trivy results to GitHub Security
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
      
      - name: Run container structure test
        run: |
          wget https://storage.googleapis.com/container-structure-test/latest/container-structure-test-linux-amd64 -O container-structure-test
          chmod +x container-structure-test
          ./container-structure-test test --image ${{ needs.build.outputs.image-tag }} --config container-test.yaml
  
  # Stage 5: Deploy to Staging
  deploy-staging:
    needs: [build, security]
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: https://staging.example.com
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Kubernetes
        uses: azure/setup-kubectl@v3
        with:
          version: 'v1.27.0'
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Update kubeconfig
        run: aws eks update-kubeconfig --name staging-cluster
      
      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/app app=${{ needs.build.outputs.image-tag }} -n staging
          kubectl rollout status deployment/app -n staging
      
      - name: Run smoke tests
        run: |
          npm run test:smoke -- --url=https://staging.example.com
      
      - name: Notify Slack
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: 'Staging deployment completed'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
  
  # Stage 6: Performance Testing
  performance:
    needs: deploy-staging
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run k6 load tests
        uses: grafana/k6-action@v0.3.0
        with:
          filename: tests/load/staging.js
          cloud: true
        env:
          K6_CLOUD_TOKEN: ${{ secrets.K6_CLOUD_TOKEN }}
      
      - name: Lighthouse CI
        uses: treosh/lighthouse-ci-action@v10
        with:
          urls: |
            https://staging.example.com
            https://staging.example.com/products
          uploadArtifacts: true
  
  # Stage 7: Deploy to Production
  deploy-production:
    needs: [deploy-staging, performance]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      url: https://example.com
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.PROD_AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.PROD_AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Blue-Green Deployment
        run: |
          # Create new target group
          aws elbv2 create-target-group \
            --name app-green-${{ github.sha }} \
            --protocol HTTP \
            --port 80 \
            --vpc-id vpc-12345
          
          # Deploy new version
          kubectl set image deployment/app-green app=${{ needs.build.outputs.image-tag }} -n production
          kubectl rollout status deployment/app-green -n production
          
          # Switch traffic
          aws elbv2 modify-listener \
            --listener-arn ${{ secrets.ALB_LISTENER_ARN }} \
            --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/app-green-${{ github.sha }}
          
          # Wait and verify
          sleep 60
          npm run test:smoke -- --url=https://example.com
          
          # Cleanup old deployment
          kubectl delete deployment/app-blue -n production
          kubectl set name deployment/app-green deployment/app-blue -n production
      
      - name: Create release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: v${{ github.run_number }}
          release_name: Release v${{ github.run_number }}
          body: |
            Changes in this Release
            - Automated deployment from ${{ github.sha }}
            - Passed all quality gates
          draft: false
          prerelease: false
```

### Hands-On Exercise: Build Your Pipeline
Create a complete CI/CD pipeline for your project

### Afternoon Session: GitOps with ArgoCD
**Duration:** 90 minutes

#### GitOps Implementation
```yaml
# argocd-application.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: production-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/yourorg/yourapp
    targetRevision: HEAD
    path: k8s/production
    helm:
      valueFiles:
        - values-production.yaml
      parameters:
        - name: image.tag
          value: $ARGOCD_APP_REVISION
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false
    syncOptions:
      - CreateNamespace=true
      - PruneLast=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
  revisionHistoryLimit: 10
```

## Day 2: Containerization

### Morning Session: Advanced Docker
**Duration:** 90 minutes

#### Multi-Stage Docker Build
```dockerfile
# Dockerfile
# Stage 1: Dependencies
FROM node:18-alpine AS dependencies
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Stage 2: Build
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
RUN npm prune --production

# Stage 3: Runtime
FROM node:18-alpine AS runtime
WORKDIR /app

# Security: Run as non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Copy production dependencies
COPY --from=dependencies --chown=nodejs:nodejs /app/node_modules ./node_modules

# Copy built application
COPY --from=build --chown=nodejs:nodejs /app/dist ./dist
COPY --from=build --chown=nodejs:nodejs /app/package*.json ./

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node healthcheck.js

USER nodejs
EXPOSE 3000

# Use dumb-init to handle signals properly
RUN apk add --no-cache dumb-init
ENTRYPOINT ["dumb-init", "--"]

CMD ["node", "dist/server.js"]
```

#### Docker Compose for Development
```yaml
# docker-compose.yml
version: '3.9'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: development
    ports:
      - "3000:3000"
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://user:pass@postgres:5432/dev
      - REDIS_URL=redis://redis:6379
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - app-network
  
  postgres:
    image: postgres:14-alpine
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: dev
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./scripts/init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app-network
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app-network
  
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/certs:/etc/nginx/certs
    depends_on:
      - app
    networks:
      - app-network

volumes:
  postgres-data:
  redis-data:

networks:
  app-network:
    driver: bridge
```

### Afternoon Session: Kubernetes Deployment
**Duration:** 90 minutes

#### Kubernetes Manifests
```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
  labels:
    app: myapp
    version: v1
spec:
  replicas: 3
  revisionHistoryLimit: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
        version: v1
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "3000"
        prometheus.io/path: "/metrics"
    spec:
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - myapp
              topologyKey: kubernetes.io/hostname
      
      containers:
      - name: app
        image: ghcr.io/yourorg/app:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 3000
          name: http
        
        env:
        - name: NODE_ENV
          value: "production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: redis-url
        
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        
        livenessProbe:
          httpGet:
            path: /health/live
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        
        volumeMounts:
        - name: config
          mountPath: /app/config
          readOnly: true
      
      volumes:
      - name: config
        configMap:
          name: app-config
---
apiVersion: v1
kind: Service
metadata:
  name: app
  labels:
    app: myapp
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: 3000
    protocol: TCP
    name: http
  selector:
    app: myapp
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 100
        periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
```

## Day 3: Cloud Platforms

### Morning Session: Multi-Cloud Deployment
**Duration:** 90 minutes

#### Terraform Infrastructure
```hcl
# main.tf
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 4.0"
    }
  }
  
  backend "s3" {
    bucket = "terraform-state-bucket"
    key    = "production/terraform.tfstate"
    region = "us-east-1"
    encrypt = true
    dynamodb_table = "terraform-state-lock"
  }
}

# AWS Infrastructure
module "aws_infrastructure" {
  source = "./modules/aws"
  
  environment = var.environment
  region      = var.aws_region
  
  # VPC Configuration
  vpc_cidr = "10.0.0.0/16"
  availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]
  
  # EKS Configuration
  cluster_name = "${var.project_name}-${var.environment}"
  cluster_version = "1.27"
  node_groups = {
    general = {
      desired_capacity = 3
      max_capacity     = 10
      min_capacity     = 2
      instance_types   = ["t3.medium"]
    }
  }
  
  # RDS Configuration
  db_instance_class = "db.r5.large"
  db_allocated_storage = 100
  db_engine = "postgres"
  db_engine_version = "14.7"
  
  # ElastiCache Configuration
  redis_node_type = "cache.r6g.large"
  redis_num_cache_nodes = 3
}

# Google Cloud Infrastructure
module "gcp_infrastructure" {
  source = "./modules/gcp"
  
  project_id = var.gcp_project_id
  region     = var.gcp_region
  
  # GKE Configuration
  cluster_name = "${var.project_name}-${var.environment}"
  initial_node_count = 3
  node_config = {
    machine_type = "n2-standard-2"
    disk_size_gb = 100
    preemptible  = false
  }
  
  # Cloud SQL Configuration
  database_version = "POSTGRES_14"
  database_tier = "db-n1-standard-2"
  
  # Memorystore Configuration
  redis_tier = "STANDARD_HA"
  redis_memory_size_gb = 5
}

# Cloudflare Configuration
resource "cloudflare_record" "app" {
  zone_id = var.cloudflare_zone_id
  name    = var.environment == "production" ? "@" : var.environment
  value   = module.aws_infrastructure.load_balancer_dns
  type    = "CNAME"
  ttl     = 1
  proxied = true
}

resource "cloudflare_page_rule" "cache" {
  zone_id = var.cloudflare_zone_id
  target  = "${var.domain}/*"
  priority = 1
  
  actions {
    cache_level = "cache_everything"
    edge_cache_ttl = 7200
    browser_cache_ttl = 14400
  }
}

resource "cloudflare_rate_limit" "api" {
  zone_id = var.cloudflare_zone_id
  threshold = 100
  period = 60
  
  match {
    request {
      url_pattern = "${var.domain}/api/*"
    }
  }
  
  action {
    mode = "challenge"
    timeout = 600
  }
}
```

### Hands-On Exercise: Deploy to Multiple Clouds
Deploy your application across AWS, GCP, and Cloudflare

### Afternoon Session: Serverless Architecture
**Duration:** 90 minutes

#### Serverless Functions
```javascript
// serverless.yml
service: myapp-api

provider:
  name: aws
  runtime: nodejs18.x
  stage: ${opt:stage, 'dev'}
  region: ${opt:region, 'us-east-1'}
  
  environment:
    STAGE: ${self:provider.stage}
    DYNAMODB_TABLE: ${self:service}-${self:provider.stage}
    
  iam:
    role:
      statements:
        - Effect: Allow
          Action:
            - dynamodb:*
          Resource: "arn:aws:dynamodb:${self:provider.region}:*:table/${self:provider.environment.DYNAMODB_TABLE}"
        - Effect: Allow
          Action:
            - s3:*
          Resource: "arn:aws:s3:::${self:custom.s3Bucket}/*"

functions:
  api:
    handler: src/api.handler
    events:
      - http:
          path: /{proxy+}
          method: ANY
          cors: true
    layers:
      - ${self:custom.layerArn}
  
  processUpload:
    handler: src/upload.handler
    events:
      - s3:
          bucket: ${self:custom.s3Bucket}
          event: s3:ObjectCreated:*
          rules:
            - prefix: uploads/
            - suffix: .jpg
    timeout: 60
    memorySize: 1024
  
  scheduled:
    handler: src/scheduled.handler
    events:
      - schedule: rate(5 minutes)
    timeout: 30
  
  websocket:
    handler: src/websocket.handler
    events:
      - websocket:
          route: $connect
      - websocket:
          route: $disconnect
      - websocket:
          route: $default

resources:
  Resources:
    DynamoDBTable:
      Type: AWS::DynamoDB::Table
      Properties:
        TableName: ${self:provider.environment.DYNAMODB_TABLE}
        AttributeDefinitions:
          - AttributeName: id
            AttributeType: S
          - AttributeName: timestamp
            AttributeType: N
        KeySchema:
          - AttributeName: id
            KeyType: HASH
          - AttributeName: timestamp
            KeyType: RANGE
        BillingMode: PAY_PER_REQUEST
        StreamSpecification:
          StreamViewType: NEW_AND_OLD_IMAGES
    
    S3Bucket:
      Type: AWS::S3::Bucket
      Properties:
        BucketName: ${self:custom.s3Bucket}
        CorsConfiguration:
          CorsRules:
            - AllowedOrigins:
                - '*'
              AllowedMethods:
                - GET
                - PUT
                - POST
              AllowedHeaders:
                - '*'

custom:
  s3Bucket: ${self:service}-${self:provider.stage}-uploads
  layerArn: arn:aws:lambda:${self:provider.region}:123456789012:layer:nodejs-dependencies:1
  webpack:
    webpackConfig: webpack.config.js
    includeModules: true

plugins:
  - serverless-webpack
  - serverless-offline
  - serverless-dynamodb-local
```

## Day 4: Monitoring & Observability

### Morning Session: Comprehensive Monitoring
**Duration:** 90 minutes

#### Monitoring Stack
```javascript
// monitoring-setup.js
const prometheus = require('prom-client');
const { NodeSDK } = require('@opentelemetry/sdk-node');
const { getNodeAutoInstrumentations } = require('@opentelemetry/auto-instrumentations-node');

class MonitoringStack {
  constructor() {
    this.setupPrometheus();
    this.setupOpenTelemetry();
    this.setupCustomMetrics();
  }
  
  setupPrometheus() {
    // Default metrics
    prometheus.collectDefaultMetrics({ prefix: 'app_' });
    
    // Custom metrics
    this.httpDuration = new prometheus.Histogram({
      name: 'app_http_request_duration_seconds',
      help: 'Duration of HTTP requests in seconds',
      labelNames: ['method', 'route', 'status_code'],
      buckets: [0.001, 0.005, 0.015, 0.05, 0.1, 0.2, 0.3, 0.5, 1, 2, 5]
    });
    
    this.businessMetrics = {
      ordersTotal: new prometheus.Counter({
        name: 'app_orders_total',
        help: 'Total number of orders',
        labelNames: ['status', 'payment_method']
      }),
      
      revenue: new prometheus.Gauge({
        name: 'app_revenue_dollars',
        help: 'Total revenue in dollars',
        labelNames: ['currency', 'region']
      }),
      
      activeUsers: new prometheus.Gauge({
        name: 'app_active_users',
        help: 'Number of active users',
        labelNames: ['tier']
      }),
      
      queueSize: new prometheus.Gauge({
        name: 'app_queue_size',
        help: 'Number of items in queue',
        labelNames: ['queue_name']
      })
    };
  }
  
  setupOpenTelemetry() {
    const sdk = new NodeSDK({
      traceExporter: new OTLPTraceExporter({
        url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT
      }),
      instrumentations: [
        getNodeAutoInstrumentations({
          '@opentelemetry/instrumentation-fs': {
            enabled: false,
          }
        })
      ]
    });
    
    sdk.start();
  }
  
  middleware() {
    return (req, res, next) => {
      const start = Date.now();
      
      res.on('finish', () => {
        const duration = (Date.now() - start) / 1000;
        
        this.httpDuration
          .labels(req.method, req.route?.path || req.path, res.statusCode)
          .observe(duration);
        
        // Log structured data
        logger.info({
          type: 'http_request',
          method: req.method,
          path: req.path,
          status: res.statusCode,
          duration,
          user_id: req.user?.id,
          trace_id: req.headers['x-trace-id'],
          ip: req.ip,
          user_agent: req.headers['user-agent']
        });
      });
      
      next();
    };
  }
}

// Grafana Dashboard Configuration
const dashboardConfig = {
  "dashboard": {
    "title": "Application Metrics",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [
          {
            "expr": "rate(app_http_requests_total[5m])"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Error Rate",
        "targets": [
          {
            "expr": "rate(app_http_requests_total{status_code=~\"5..\"}[5m])"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Response Time (p95)",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(app_http_request_duration_seconds_bucket[5m]))"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Active Users",
        "targets": [
          {
            "expr": "app_active_users"
          }
        ],
        "type": "stat"
      }
    ]
  }
};
```

### Afternoon Session: Incident Response
**Duration:** 90 minutes

#### Incident Management
```javascript
// incident-response.js
class IncidentResponseSystem {
  async detectIncident(metrics) {
    const incidents = [];
    
    // Check error rate
    if (metrics.errorRate > 0.05) {
      incidents.push({
        severity: 'critical',
        type: 'high_error_rate',
        value: metrics.errorRate,
        threshold: 0.05
      });
    }
    
    // Check response time
    if (metrics.p95ResponseTime > 1000) {
      incidents.push({
        severity: 'warning',
        type: 'slow_response',
        value: metrics.p95ResponseTime,
        threshold: 1000
      });
    }
    
    // Check availability
    if (metrics.availability < 0.999) {
      incidents.push({
        severity: 'critical',
        type: 'low_availability',
        value: metrics.availability,
        threshold: 0.999
      });
    }
    
    for (const incident of incidents) {
      await this.handleIncident(incident);
    }
  }
  
  async handleIncident(incident) {
    // 1. Create incident
    const incidentId = await this.createIncident(incident);
    
    // 2. Alert on-call
    await this.alertOnCall(incident);
    
    // 3. Auto-remediation
    await this.attemptAutoRemediation(incident);
    
    // 4. Create runbook
    const runbook = await this.generateRunbook(incident);
    
    // 5. Start recording
    await this.startRecording(incidentId);
    
    return incidentId;
  }
  
  async attemptAutoRemediation(incident) {
    const remediations = {
      high_error_rate: async () => {
        // Rollback deployment
        await kubectl.rollback('deployment/app');
        // Scale up
        await kubectl.scale('deployment/app', 5);
      },
      
      slow_response: async () => {
        // Clear cache
        await redis.flushall();
        // Increase resources
        await kubectl.patch('deployment/app', {
          spec: {
            template: {
              spec: {
                containers: [{
                  resources: {
                    limits: { cpu: '1000m', memory: '1Gi' }
                  }
                }]
              }
            }
          }
        });
      },
      
      low_availability: async () => {
        // Restart pods
        await kubectl.rollout.restart('deployment/app');
        // Check dependencies
        await this.healthCheckDependencies();
      }
    };
    
    if (remediations[incident.type]) {
      await remediations[incident.type]();
    }
  }
  
  generateRunbook(incident) {
    return {
      title: `Runbook: ${incident.type}`,
      steps: [
        '1. Acknowledge incident in PagerDuty',
        '2. Join incident channel in Slack',
        '3. Check monitoring dashboard',
        '4. Review recent deployments',
        '5. Check dependency health',
        '6. Review error logs',
        '7. Implement fix or rollback',
        '8. Verify fix',
        '9. Update status page',
        '10. Write post-mortem'
      ],
      queries: [
        `sum(rate(http_requests_total{status=~"5.."}[5m]))`,
        `histogram_quantile(0.95, http_request_duration_seconds_bucket)`,
        `up{job="app"}`
      ],
      contacts: [
        'On-call engineer: pager',
        'Team lead: slack',
        'Customer success: email'
      ]
    };
  }
}
```

## Day 5: Production Excellence

### Full Day Project: Production-Ready System
**Duration:** 3 hours

#### Complete Production Setup
```javascript
// production-system.js
class ProductionSystem {
  async deploy() {
    // 1. Pre-deployment checks
    await this.runPreflightChecks();
    
    // 2. Blue-green deployment
    await this.blueGreenDeploy();
    
    // 3. Health checks
    await this.verifyHealth();
    
    // 4. Load balancer switch
    await this.switchTraffic();
    
    // 5. Monitoring
    await this.setupMonitoring();
    
    // 6. Alerting
    await this.configureAlerts();
    
    // 7. Backup
    await this.createBackup();
    
    // 8. Documentation
    await this.updateDocumentation();
  }
  
  async runPreflightChecks() {
    const checks = [
      this.checkDatabaseMigrations(),
      this.checkSecrets(),
      this.checkDependencies(),
      this.checkResourceQuotas(),
      this.checkCertificates(),
      this.runSecurityScan(),
      this.validateConfiguration()
    ];
    
    const results = await Promise.all(checks);
    
    if (results.some(r => !r.passed)) {
      throw new Error('Preflight checks failed');
    }
  }
  
  async blueGreenDeploy() {
    // Deploy to green environment
    await terraform.apply('green');
    
    // Run tests on green
    await this.runSmokeTests('green');
    
    // Gradual traffic shift
    for (const percentage of [10, 25, 50, 75, 100]) {
      await this.shiftTraffic('green', percentage);
      await this.monitorMetrics(5 * 60 * 1000); // 5 minutes
      
      if (await this.detectAnomalies()) {
        await this.rollback();
        throw new Error('Anomalies detected during deployment');
      }
    }
    
    // Cleanup blue environment
    await terraform.destroy('blue');
  }
}

// Final deployment
const system = new ProductionSystem();
await system.deploy();
```

## Weekend Assignment

### Production Deployment Challenge
1. Deploy a complete production system
2. Implement zero-downtime deployments
3. Set up comprehensive monitoring
4. Create disaster recovery plan
5. Document everything

### Required Deliverables
- [ ] Production URL
- [ ] CI/CD pipeline
- [ ] Monitoring dashboards
- [ ] Runbook documentation
- [ ] Load test results (>10,000 RPS)
- [ ] 99.9% uptime commitment

## Assessment Rubric

| Criteria | Basic (60%) | Proficient (80%) | Advanced (100%) |
|----------|-------------|------------------|-----------------|
| CI/CD | Basic pipeline | Full automation | GitOps |
| Containers | Docker | Docker Compose | Kubernetes |
| Cloud | Single cloud | Multi-cloud | Global deployment |
| Monitoring | Basic metrics | Full observability | Predictive |
| Operations | Manual | Semi-automated | Fully automated |

## Resources

### Required Reading
- [The Phoenix Project](https://www.amazon.com/Phoenix-Project-DevOps-Helping-Business/dp/1942788290)
- [Kubernetes in Action](https://www.manning.com/books/kubernetes-in-action-second-edition)
- [Site Reliability Engineering](https://sre.google/sre-book/table-of-contents/)

### Video Tutorials
- [CI/CD Best Practices](https://youtube.com/watch?v=example)
- [Kubernetes Deep Dive](https://youtube.com/watch?v=example)
- [Production Monitoring](https://youtube.com/watch?v=example)

### DevOps Tools
- **Jenkins/GitHub Actions**: CI/CD
- **Docker/Kubernetes**: Containerization
- **Terraform**: Infrastructure as Code
- **Prometheus/Grafana**: Monitoring
- **PagerDuty**: Incident management

## Graduation Ceremony

### Final Presentation
- Present your production system
- Demonstrate zero-downtime deployment
- Show monitoring dashboards
- Explain architecture decisions
- Share lessons learned

### Certification Requirements
- Complete all weekly projects
- Pass final assessment
- Deploy production system
- Maintain 99% uptime for 48 hours
- Present final project

## Career Guidance

### Next Steps
1. **Build Portfolio**: Showcase your projects
2. **Contribute to Open Source**: Join communities
3. **Network**: Attend meetups and conferences
4. **Keep Learning**: Stay updated with trends
5. **Apply**: Target companies using your tech stack

### Job Search Resources
- **LinkedIn**: Optimize your profile
- **GitHub**: Maintain active repositories
- **Dev.to**: Write technical articles
- **Twitter**: Follow industry leaders
- **Meetups**: Join local tech groups

## Alumni Network

### Stay Connected
- Discord: VibeCoders Alumni
- LinkedIn: VibeCoders Network
- GitHub: VibeCoders Organization
- Newsletter: Monthly updates
- Annual conference: VibeConf

---

🎓 **Congratulations!**
You've completed the VibeCoders Bootcamp!

You're now equipped to:
- Build production-ready applications
- Deploy at scale
- Monitor and maintain systems
- Lead DevOps initiatives
- Drive technical excellence

💡 **Remember:**
- Keep learning
- Share knowledge
- Help others
- Build amazing things
- Stay curious

🚀 **Your Journey Continues!**

Welcome to the VibeCoders Alumni Network!

---

*"The best way to predict the future is to build it."*

Ready to change the world? Let's go! 🌟
