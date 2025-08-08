#!/bin/bash

# Cloudflare DNS Setup Script for bootcamp.organizedai.vip
# This script adds a CNAME record for the bootcamp subdomain

echo "================================================"
echo "Cloudflare DNS Configuration Script"
echo "Adding CNAME: bootcamp.organizedai.vip"
echo "================================================"

# Configuration
CLOUDFLARE_EMAIL="your-email@example.com"
CLOUDFLARE_API_KEY="your-api-key"
ZONE_ID="your-zone-id"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo ""
echo -e "${YELLOW}Please provide your Cloudflare credentials:${NC}"
echo "You can find these at:"
echo "- Zone ID: Dashboard > organizedai.vip > Right sidebar"
echo "- API Key: My Profile > API Tokens > Global API Key"
echo ""

read -p "Enter your Cloudflare email: " CLOUDFLARE_EMAIL
read -s -p "Enter your Global API Key: " CLOUDFLARE_API_KEY
echo ""
read -p "Enter your Zone ID for organizedai.vip: " ZONE_ID

echo ""
echo -e "${YELLOW}Creating CNAME record...${NC}"

# Create the CNAME record
RESPONSE=$(curl -s -X POST "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/dns_records" \
  -H "X-Auth-Email: ${CLOUDFLARE_EMAIL}" \
  -H "X-Auth-Key: ${CLOUDFLARE_API_KEY}" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "CNAME",
    "name": "bootcamp",
    "content": "organized-ai.github.io",
    "ttl": 1,
    "proxied": false,
    "comment": "VibeCoders Bootcamp - GitHub Pages"
  }')

# Check if successful
if echo "$RESPONSE" | grep -q '"success":true'; then
    echo -e "${GREEN}✅ SUCCESS! CNAME record created${NC}"
    echo ""
    echo "Record details:"
    echo "- Name: bootcamp.organizedai.vip"
    echo "- Target: organized-ai.github.io"
    echo "- Proxy: Disabled (DNS only)"
    echo ""
    echo "Your bootcamp will be accessible at:"
    echo "https://bootcamp.organizedai.vip"
    echo ""
    echo "Note: DNS propagation may take 5-30 minutes"
else
    echo -e "${RED}❌ Error creating record${NC}"
    echo "Response: $RESPONSE"
    echo ""
    echo "Common issues:"
    echo "1. Record already exists - delete it first in the dashboard"
    echo "2. Invalid API credentials"
    echo "3. Wrong Zone ID"
fi

echo ""
echo "================================================"
echo "Script Complete"
echo "================================================"
