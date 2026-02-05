# GitHub Personal Access Token (PAT) Setup Guide

Follow these steps to create a Personal Access Token for pushing Docker images to GitHub Container Registry (GHCR).

## Step 1: Go to GitHub Settings

1. Open GitHub: https://github.com
2. Click your profile picture (top right)
3. Click **Settings**
4. Scroll down to **Developer settings** (bottom left)
5. Click **Personal access tokens** → **Tokens (classic)**

## Step 2: Generate New Token

1. Click **Generate new token** → **Generate new token (classic)**
2. Give it a name: `GHCR Docker Push - AVA ML API`
3. Set expiration: **90 days** (or No expiration if allowed)

## Step 3: Select Permissions

Check these scopes:
- ✅ `write:packages` - Upload packages to GitHub Package Registry
- ✅ `read:packages` - Download packages from GitHub Package Registry
- ✅ `delete:packages` - Delete packages from GitHub Package Registry (optional)

## Step 4: Generate and Copy Token

1. Scroll down and click **Generate token**
2. **IMPORTANT**: Copy the token immediately (starts with `ghp_...`)
3. Save it somewhere safe - you won't see it again!

## Step 5: Use the Token

### For Manual Builds (Local)

```bash
# Login to GHCR
echo "YOUR_TOKEN_HERE" | docker login ghcr.io -u zaheer-zee --password-stdin

# Or run the build script (it will prompt for token)
./build-and-push.sh
```

### For GitHub Actions (Automatic)

GitHub Actions uses `GITHUB_TOKEN` automatically - **no setup needed!**
Just push to main branch and it builds automatically.

## Verify Login

```bash
docker login ghcr.io -u zaheer-zee
# Enter your PAT when prompted
```

Success message:
```
Login Succeeded
```

## Security Tips

- ✅ Never commit tokens to Git
- ✅ Use token expiration
- ✅ Regenerate if compromised
- ✅ Use different tokens for different purposes

## Troubleshooting

**"unauthorized: unauthenticated"**
- Token expired or invalid
- Wrong username
- Missing `write:packages` permission

**"denied: permission_denied"**
- Token doesn't have `write:packages` scope
- Repository visibility issue (make package public)

---

## Quick Reference

**Your GHCR Image**: `ghcr.io/zaheer-zee/ava-ml-api:latest`

**Login Command**:
```bash
docker login ghcr.io -u zaheer-zee
```

**Pull Command**:
```bash
docker pull ghcr.io/zaheer-zee/ava-ml-api:latest
```

**Run Command**:
```bash
docker run -d -p 8000:8000 --env-file .env ghcr.io/zaheer-zee/ava-ml-api:latest
```
