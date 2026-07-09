#!/bin/bash
# ==========================================
# BOUNDLESS AI — Local APK Build Script
# Run this on Ubuntu 22.04 or WSL2 (Ubuntu)
# ==========================================

set -e

echo "================================================"
echo "  BOUNDLESS AI — APK Build Setup"
echo "================================================"

# System dependencies
echo "[1/4] Installing system dependencies..."
sudo apt-get update -qq
sudo apt-get install -y \
  git zip unzip openjdk-17-jdk \
  autoconf libtool pkg-config \
  zlib1g-dev libffi-dev libssl-dev \
  libltdl-dev build-essential python3-pip

# Python dependencies
echo "[2/4] Installing Python packages..."
pip3 install --upgrade pip
pip3 install buildozer cython kivy requests certifi

# Build
echo "[3/4] Building APK (first run downloads ~1GB Android SDK — takes 15-30 min)..."
buildozer android debug

echo "[4/4] Done!"
echo ""
echo "APK is in: $(pwd)/bin/"
ls bin/*.apk 2>/dev/null && echo "✅ Build successful!" || echo "❌ APK not found — check errors above."
