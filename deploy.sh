#!/bin/bash

echo "🚀 Deploying Nostalgic Hammond to Vercel..."
echo ""

# Build the site
echo "📦 Building site..."
npm run build

echo ""
echo "🔗 Ready to deploy!"
echo ""
echo "Run this command to deploy:"
echo "  npx vercel --prod"
echo ""
echo "Or connect via GitHub:"
echo "  1. Create repo on GitHub"
echo "  2. git remote add origin https://github.com/YOUR_USERNAME/nostalgic-hammond.git"
echo "  3. git push -u origin main"
echo "  4. Import in Vercel dashboard: https://vercel.com/new"

