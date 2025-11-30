#!/bin/bash

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                    🧹 PROJECT CLEANUP SCRIPT 🧹                              ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Files to remove
UNNECESSARY_FILES=(
    # Duplicate/backup files
    "backend/app/repositories/inventory.py.bak"
    "backend/app/repositories/inventory_patch.py"
    
    # Log files
    "backend.log"
    "backend_run.log"
    "frontend_run.log"
    "ngrok.log"
    
    # Test CSV files (keep samples in test_samples/)
    "test.csv"
    "test_inventory.csv"
    
    # Duplicate documentation (keep consolidated versions)
    "BACKEND_DEPLOYED.txt"
    "BACKEND_INFO.md"
    "FRONTEND_DEPLOYED.txt"
    "FRONTEND_REDESIGN.txt"
    "COMPLETE_ANALYSIS_SUMMARY.txt"
    "CSV_UPLOAD_FIX.md"
    "DEPLOYMENT_STATUS.md"
    "FINAL_PROJECT_SUMMARY.md"
    "FUNCTIONALITY_ANALYSIS.md"
    "LIVE_DEMO_SUMMARY.txt"
    "MANUAL_TEST_GUIDE.md"
    "PITCH_GUIDE.md"
    "PROJECT_COMPLETE.md"
    "PROJECT_STATUS.md"
    "PROJECT_STRUCTURE.md"
    "QUICK_ACCESS.txt"
    "QUICK_CONFIG.txt"
    "TEST_COMMANDS.md"
    "TEST_FIXES_COMPLETE.md"
    "UI_UX_IMPROVEMENTS.md"
    
    # Duplicate deployment guides (keep main ones)
    "RENDER_ARCHITECTURE.md"
    "RENDER_CLI_DEPLOY.md"
    "RENDER_DEPLOYMENT.md"
    "RENDER_FREE_DEPLOY.md"
    "RENDER_FULL_DEPLOYMENT.md"
    
    # Duplicate Dockerfiles (keep in docker/)
    "Dockerfile.backend"
    "Dockerfile.backend.render"
    
    # Duplicate deployment scripts (keep main ones)
    "deploy_free.sh"
    "deploy_render_cli.sh"
    "deploy.sh"
    "prepare_render_deploy.sh"
    "setup_deployment.sh"
    "start_backend.sh"
    "update_cors.sh"
    
    # Empty/placeholder files
    "Idea"
    
    # Windows setup (not needed on Linux)
    "setup.bat"
)

# Directories to clean
CACHE_DIRS=(
    "backend/.pytest_cache"
    "backend/__pycache__"
    "backend/app/__pycache__"
    "backend/app/api/__pycache__"
    "backend/app/models/__pycache__"
    "backend/app/repositories/__pycache__"
    "backend/app/schemas/__pycache__"
    "backend/app/services/__pycache__"
    "backend/app/utils/__pycache__"
    "backend/tests/__pycache__"
    "backend/alembic/__pycache__"
    "backend/alembic/versions/__pycache__"
)

echo "📋 Files to remove:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
for file in "${UNNECESSARY_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file"
    fi
done

echo ""
echo "📁 Cache directories to remove:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
for dir in "${CACHE_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "  ✓ $dir"
    fi
done

echo ""
read -p "Proceed with cleanup? (y/n): " confirm

if [ "$confirm" != "y" ]; then
    echo "Cleanup cancelled."
    exit 0
fi

echo ""
echo "🧹 Cleaning up..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Remove files
removed_count=0
for file in "${UNNECESSARY_FILES[@]}"; do
    if [ -f "$file" ]; then
        rm "$file"
        echo "  ✓ Removed: $file"
        ((removed_count++))
    fi
done

# Remove cache directories
for dir in "${CACHE_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        rm -rf "$dir"
        echo "  ✓ Removed: $dir"
        ((removed_count++))
    fi
done

echo ""
echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                    ✅ CLEANUP COMPLETE ✅                                    ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Removed $removed_count items"
echo ""
echo "📊 Project is now clean and organized!"
echo ""
echo "Kept essential files:"
echo "  ✓ Source code (backend/frontend)"
echo "  ✓ Configuration files"
echo "  ✓ Main documentation (README.md, guides)"
echo "  ✓ Deployment scripts (main ones)"
echo "  ✓ Test samples"
echo ""
