#!/bin/bash
# Uninstall script for Claude Code Reference Applet

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Claude Code Reference - Uninstaller${NC}"
echo

# Remove desktop entry
if [ -f ~/.local/share/applications/claude-code-reference.desktop ]; then
    rm ~/.local/share/applications/claude-code-reference.desktop
    echo -e "${GREEN}✓${NC} Removed desktop entry"
else
    echo -e "${YELLOW}•${NC} Desktop entry not found (already removed)"
fi

# Remove command symlink
if [ -L ~/.local/bin/claude-ref ]; then
    rm ~/.local/bin/claude-ref
    echo -e "${GREEN}✓${NC} Removed command-line launcher"
else
    echo -e "${YELLOW}•${NC} Command-line launcher not found"
fi

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database ~/.local/share/applications/ 2>/dev/null || true
fi

echo
echo -e "${GREEN}Uninstallation complete!${NC}"
echo
echo "The application files are still in: $(dirname "$0")"
echo "To completely remove, delete that directory."
echo
