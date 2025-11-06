# Deployment Guide

This guide covers deploying different parts of the Language Learning Web project.

## Landing Page (Vercel) - Recommended for Documentation

The landing page (`index.html`) is perfect for Vercel deployment and serves as documentation for the project.

### Quick Deploy to Vercel

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Add landing page"
   git push origin main
   ```

2. **Deploy via Vercel Dashboard:**
   - Go to [vercel.com](https://vercel.com) and sign in
   - Click "Add New Project"
   - Import your GitHub repository
   - Click "Deploy" (no configuration needed!)
   - Your site will be live at `https://your-project.vercel.app`

3. **Or use Vercel CLI:**
   ```bash
   npm install -g vercel
   vercel login
   vercel
   ```

### What Gets Deployed

- `index.html` - Landing page
- `css/` - Styles
- `js/` - Interactive features
- `vercel.json` - Vercel configuration

### What's Excluded

The `.vercelignore` file excludes:
- `frontend/` - Vue application (not deployed to Vercel)
- `backend/` - FastAPI application (not deployed to Vercel)
- Docker files
- node_modules

## Full Application (Docker) - Recommended for Self-Hosting

For the actual language learning application (frontend + backend), use Docker:

### Local Deployment

```bash
# Start everything
docker-compose up -d

# Access at:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
```

### Production Deployment

1. **VPS/Cloud Server (DigitalOcean, AWS, etc.):**
   ```bash
   # On your server
   git clone https://github.com/yourusername/language-learning-web.git
   cd language-learning-web
   docker-compose up -d
   ```

2. **Configure Domain:**
   - Point your domain to server IP
   - Update frontend API URL in `frontend/src/components/MainPage.vue`
   - Add SSL with Let's Encrypt

3. **Update Docker Compose for Production:**
   ```yaml
   # In docker-compose.yml, update ports if needed
   frontend:
     ports:
       - "80:80"  # HTTP
       - "443:443"  # HTTPS (if configured)
   ```

## Deployment Options Summary

| Component | Recommended Platform | Purpose |
|-----------|---------------------|---------|
| Landing Page | Vercel | Documentation & marketing |
| Frontend + Backend | Docker (Self-hosted) | Production application |
| Development | Local | Testing and development |

## Environment Variables

### Landing Page (Vercel)
No environment variables needed - it's static HTML.

### Application (Docker)

**Backend:**
- `DATABASE_URL` - Database connection string

**Frontend:**
- `VITE_API_URL` - Backend API URL

## Updating After Deployment

### Landing Page
- Push changes to GitHub
- Vercel auto-deploys from main branch

### Docker Application
```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose up -d --build
```

## Monitoring

### Vercel
- View analytics at vercel.com dashboard
- Check deployment logs
- Monitor performance

### Docker
```bash
# Check logs
docker-compose logs -f

# Check status
docker-compose ps

# Restart services
docker-compose restart
```

## Troubleshooting

### Vercel Deployment Issues

**Problem:** Vercel can't find index.html
**Solution:** Make sure index.html is in the root directory

**Problem:** CSS/JS not loading
**Solution:** Check that css/ and js/ folders are in root

### Docker Issues

**Problem:** Port already in use
**Solution:** Change ports in docker-compose.yml

**Problem:** Database not persisting
**Solution:** Check volume mounts in docker-compose.yml

## Need Help?

- Check [GitHub Issues](https://github.com/yourusername/language-learning-web/issues)
- Read the [README.md](README.md)
- Visit the [landing page](https://your-project.vercel.app)
