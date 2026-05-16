#!/bin/bash

# Task Management System - Stop Script
# This script stops all running containers

set -e

echo "🛑 Stopping Task Management System..."
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Stop all containers
docker-compose down

echo ""
echo -e "${GREEN}✅ All services stopped successfully${NC}"
echo ""
echo "To start again, run: ./start.sh"
echo "To remove all data, run: docker-compose down -v"
echo ""

# Made with Bob
