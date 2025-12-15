#!/bin/bash
#
# Anonymous Commit Script
# Creates commits with randomized timestamps in UTC timezone
# to protect contributor privacy.
#
# Usage:
#   ./anon-commit.sh "commit message"
#   ./anon-commit.sh "add: new lecture notes" --no-random
#
# Features:
#   - Uses UTC timezone
#   - Randomizes commit time (optional)
#   - Verifies anonymous git config

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check arguments
if [ -z "$1" ]; then
    echo -e "${RED}Error: No commit message provided${NC}"
    echo ""
    echo "Usage: ./anon-commit.sh \"commit message\""
    echo "       ./anon-commit.sh \"commit message\" --no-random"
    exit 1
fi

MESSAGE="$1"
NO_RANDOM="$2"

# Check git config
echo ""
echo "=========================================="
echo "  Anonymous Commit"
echo "=========================================="

USER_NAME=$(git config user.name)
USER_EMAIL=$(git config user.email)

echo ""
echo "Current Git Config:"
echo "  Name:  $USER_NAME"
echo "  Email: $USER_EMAIL"

# Warn if email looks personal
if [[ "$USER_EMAIL" != *"noreply"* ]] && [[ "$USER_EMAIL" != *"anonymous"* ]] && [[ "$USER_EMAIL" != *"anon"* ]]; then
    echo ""
    echo -e "${YELLOW}⚠️  Warning: Your email might reveal your identity!${NC}"
    echo "   Consider using: anonymous@users.noreply.github.com"
    echo ""
    read -p "Continue anyway? (y/N): " confirm
    if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
        echo "Aborted. Set anonymous email with:"
        echo '  git config user.email "anonymous@users.noreply.github.com"'
        exit 1
    fi
fi

# Generate commit date
if [ "$NO_RANDOM" == "--no-random" ]; then
    # Use current time in UTC
    COMMIT_DATE=$(TZ=UTC date +"%Y-%m-%d %H:%M:%S")
    echo ""
    echo "Using current UTC time: $COMMIT_DATE"
else
    # Random hour (9 AM - 11 PM UTC)
    HOUR=$((RANDOM % 15 + 9))
    MIN=$((RANDOM % 60))
    SEC=$((RANDOM % 60))
    
    # Random day in past week
    DAYS_AGO=$((RANDOM % 7))
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        DATE=$(date -v-${DAYS_AGO}d +%Y-%m-%d)
    else
        # Linux
        DATE=$(date -d "-$DAYS_AGO days" +%Y-%m-%d)
    fi
    
    COMMIT_DATE=$(printf "%s %02d:%02d:%02d" "$DATE" "$HOUR" "$MIN" "$SEC")
    echo ""
    echo "Using randomized UTC time: $COMMIT_DATE"
fi

# Check if there are staged changes
if git diff --cached --quiet; then
    echo ""
    echo -e "${YELLOW}⚠️  No staged changes. Stage files first with 'git add'${NC}"
    echo ""
    echo "Staging all changes..."
    git add -A
fi

# Show what will be committed
echo ""
echo "Files to commit:"
git diff --cached --name-only | while read file; do
    echo "  + $file"
done

# Confirm
echo ""
read -p "Proceed with commit? (Y/n): " confirm
if [[ "$confirm" == "n" || "$confirm" == "N" ]]; then
    echo "Aborted."
    exit 0
fi

# Make the commit
echo ""
TZ=UTC \
GIT_AUTHOR_DATE="$COMMIT_DATE" \
GIT_COMMITTER_DATE="$COMMIT_DATE" \
git commit -m "$MESSAGE"

echo ""
echo -e "${GREEN}✅ Anonymous commit created!${NC}"
echo ""
echo "Commit details:"
git log -1 --format="  Hash:   %h
  Author: %an <%ae>
  Date:   %ad
  Message: %s"

echo ""
echo "=========================================="
