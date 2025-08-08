# Custom Domain Setup - bootcamp.organizedai.vip

## ✅ GitHub Configuration (COMPLETED)

The CNAME file has been added to both branches:
- Main branch: Contains landing page
- gh-pages branch: Contains SliDev presentation

## 🌐 Cloudflare DNS Configuration (ACTION REQUIRED)

### Step 1: Log into Cloudflare

1. Go to https://dash.cloudflare.com
2. Select your domain: `organizedai.vip`
3. Navigate to DNS settings

### Step 2: Add CNAME Record

Add the following DNS record:

| Type  | Name     | Target                    | Proxy Status | TTL  |
|-------|----------|---------------------------|--------------|------|
| CNAME | bootcamp | organized-ai.github.io    | DNS only (🟫) | Auto |

**Important Settings:**
- **Type**: CNAME
- **Name**: bootcamp (this creates bootcamp.organizedai.vip)
- **Target**: organized-ai.github.io
- **Proxy Status**: Set to "DNS only" (gray cloud, not orange)
- **TTL**: Auto

### Step 3: SSL/TLS Configuration

1. In Cloudflare, go to SSL/TLS → Overview
2. Set encryption mode to "Full" (not "Full (strict)")
3. This allows GitHub Pages' SSL certificate to work properly

### Step 4: Page Rules (Optional but Recommended)

Create a page rule for HTTPS redirect:
1. Go to Rules → Page Rules
2. Create new rule:
   - URL: `http://bootcamp.organizedai.vip/*`
   - Setting: "Always Use HTTPS"

## 🔍 Verification

After DNS propagation (5-30 minutes):

1. Visit https://bootcamp.organizedai.vip
2. Check SSL certificate (should show "Let's Encrypt")
3. Test both www and non-www versions

## 🚀 What's Accessible

Once configured, these URLs will work:
- **Landing Page**: https://bootcamp.organizedai.vip
- **SliDev Presentation**: https://bootcamp.organizedai.vip (auto-serves from gh-pages)

## ⚠️ Troubleshooting

### DNS Not Resolving
- Wait up to 30 minutes for propagation
- Clear browser cache
- Try: `nslookup bootcamp.organizedai.vip`

### SSL Certificate Error
- Ensure Cloudflare proxy is OFF (gray cloud)
- Check SSL/TLS mode is "Full"
- Wait up to 24 hours for Let's Encrypt

### 404 Error
- Verify CNAME file exists in repository
- Check GitHub Pages is enabled
- Confirm branch is set to gh-pages

## 📱 Mobile Access

The site is fully responsive and accessible on:
- Desktop browsers
- Mobile devices
- Tablets
- Progressive Web App capable

## 📊 Analytics (Optional)

To add Cloudflare Analytics:
1. Go to Analytics & Logs
2. Enable Web Analytics
3. Add snippet to index.html

## 🔐 Security Features

Automatically enabled:
- HTTPS encryption
- DDoS protection (Cloudflare)
- GitHub Pages CDN
- Let's Encrypt SSL

## 📧 Support

For issues:
- DNS: Check Cloudflare dashboard
- GitHub Pages: Settings → Pages
- Custom domain: Verify CNAME file

---

Last Updated: August 7, 2025
Status: Awaiting DNS configuration in Cloudflare
