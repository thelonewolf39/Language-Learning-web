# Language Learning Web - Landing Page

This is the landing/documentation website for the Language Learning Web project. It's designed to be deployed on Vercel.

## Structure

```
website/
├── public/
│   ├── index.html       # Main landing page
│   ├── css/
│   │   └── style.css    # Styles
│   └── js/
│       └── script.js    # Interactive features
├── vercel.json          # Vercel configuration
├── package.json         # Project metadata
└── README.md           # This file
```

## Features

- 📱 Fully responsive design
- 🎨 Modern, attractive UI with gradient backgrounds
- 📚 Comprehensive setup instructions
- 🤝 Collaboration guidelines
- ⚡ Fast loading with optimized assets
- 🔒 Security headers configured

## Local Development

1. Install serve (if not already installed):
```bash
npm install -g serve
```

2. Serve the website locally:
```bash
cd website
serve public
```

3. Open http://localhost:3000 in your browser

## Deploy to Vercel

### Option 1: Vercel CLI (Recommended)

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Navigate to website directory:
```bash
cd website
```

3. Deploy:
```bash
vercel
```

4. For production deployment:
```bash
vercel --prod
```

### Option 2: Vercel Dashboard

1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import your GitHub repository
4. Set the root directory to `website`
5. Click "Deploy"

### Option 3: GitHub Integration

1. Push your code to GitHub
2. Connect your repository to Vercel
3. Vercel will automatically deploy on every push
4. Set the root directory to `website` in project settings

## Configuration

The `vercel.json` file includes:
- Clean URLs (no .html extensions)
- Security headers
- Cache control for static assets
- SPA routing support

## Customization

### Update GitHub Links

Replace `yourusername` in these files:
- `public/index.html` - All GitHub links

### Styling

Edit `public/css/style.css` to customize:
- Colors (CSS variables at the top)
- Fonts
- Layout
- Responsive breakpoints

### Content

Edit `public/index.html` to modify:
- Text content
- Features
- Setup instructions
- Contribution guidelines

## Performance

The site is optimized for performance:
- Minimal dependencies (vanilla JS)
- Optimized CSS with minimal bundle size
- Lazy loading animations
- Cached static assets
- Compressed assets via Vercel

## Browser Support

- Chrome/Edge (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Mobile browsers

## License

MIT License - see main project LICENSE file
