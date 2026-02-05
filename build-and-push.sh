#!/bin/bash
# Manual build and push script for GHCR
# Use this if you want to build locally instead of GitHub Actions

set -e

# Configuration
REGISTRY="ghcr.io"
USERNAME="zaheer-zee"
IMAGE_NAME="ava-ml-api"
FULL_IMAGE="${REGISTRY}/${USERNAME}/${IMAGE_NAME}"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🐳 AVA ML API - Multi-Platform Docker Build${NC}"
echo "================================================"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker Desktop.${NC}"
    exit 1
fi

# Check if logged in to GHCR
echo -e "${BLUE}📝 Checking GHCR authentication...${NC}"
if ! docker login ${REGISTRY} --username ${USERNAME} --password-stdin < /dev/null 2>&1 | grep -q "Authenticating"; then
    echo -e "${BLUE}🔑 Please log in to GitHub Container Registry${NC}"
    echo "Enter your GitHub Personal Access Token (PAT):"
    docker login ${REGISTRY} --username ${USERNAME}
fi

# Create buildx builder if it doesn't exist
echo -e "${BLUE}🔧 Setting up Docker Buildx...${NC}"
if ! docker buildx inspect multiplatform-builder > /dev/null 2>&1; then
    docker buildx create --name multiplatform-builder --use
else
    docker buildx use multiplatform-builder
fi

# Get version tag
echo -e "${BLUE}📌 Version tagging...${NC}"
read -p "Enter version tag (or press Enter for 'latest'): " VERSION
VERSION=${VERSION:-latest}

# Build and push
echo -e "${BLUE}🏗️  Building multi-platform image...${NC}"
echo "Platforms: linux/amd64, linux/arm64"
echo "Tags: ${FULL_IMAGE}:${VERSION}, ${FULL_IMAGE}:latest"

docker buildx build \
    --platform linux/amd64,linux/arm64 \
    --tag ${FULL_IMAGE}:${VERSION} \
    --tag ${FULL_IMAGE}:latest \
    --push \
    .

echo ""
echo -e "${GREEN}✅ Build and push completed successfully!${NC}"
echo ""
echo "================================================"
echo -e "${GREEN}🎉 Image published to GHCR${NC}"
echo "================================================"
echo ""
echo "Image: ${FULL_IMAGE}:${VERSION}"
echo "Also tagged as: ${FULL_IMAGE}:latest"
echo ""
echo "Pull command:"
echo "  docker pull ${FULL_IMAGE}:latest"
echo ""
echo "Run command:"
echo "  docker run -d -p 8000:8000 --env-file .env ${FULL_IMAGE}:latest"
echo ""
echo "View on GitHub:"
echo "  https://github.com/${USERNAME}?tab=packages"
echo ""
