#!/bin/bash
# Install script for Claude Code Reference Applet
# Compatible with Linux Mint, Ubuntu, Debian, and derivatives

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DESKTOP_FILE="$SCRIPT_DIR/claude-code-reference.desktop"
LAUNCHER="$SCRIPT_DIR/launch.sh"
MAIN_SCRIPT="$SCRIPT_DIR/claude_code_reference.py"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}"
    echo "╔═══════════════════════════════════════════════════╗"
    echo "║       Claude Code Reference - Installer           ║"
    echo "║   Searchable reference for all Claude Code        ║"
    echo "║   commands, shortcuts & keyboard bindings         ║"
    echo "╚═══════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_step() {
    echo -e "${YELLOW}▶${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Detect package manager
detect_package_manager() {
    if command -v apt &> /dev/null; then
        echo "apt"
    elif command -v dnf &> /dev/null; then
        echo "dnf"
    elif command -v pacman &> /dev/null; then
        echo "pacman"
    elif command -v zypper &> /dev/null; then
        echo "zypper"
    else
        echo "unknown"
    fi
}

install_dependencies() {
    local pm=$(detect_package_manager)

    case $pm in
        apt)
            sudo apt update
            sudo apt install -y python3 python3-gi python3-gi-cairo gir1.2-gtk-3.0
            ;;
        dnf)
            sudo dnf install -y python3 python3-gobject gtk3
            ;;
        pacman)
            sudo pacman -S --noconfirm python python-gobject gtk3
            ;;
        zypper)
            sudo zypper install -y python3 python3-gobject gtk3
            ;;
        *)
            print_error "Unknown package manager. Please install manually:"
            echo "  - python3"
            echo "  - python3-gi (or python3-gobject)"
            echo "  - GTK3"
            exit 1
            ;;
    esac
}

print_header

# Check Python
print_step "Checking Python 3..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    print_success "Found $PYTHON_VERSION"
else
    print_error "Python 3 not found"
    print_step "Installing dependencies..."
    install_dependencies
fi

# Check GTK3 Python bindings
print_step "Checking GTK3 bindings..."
if python3 -c "import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk" 2>/dev/null; then
    print_success "GTK3 Python bindings available"
else
    print_error "GTK3 bindings not found"
    print_step "Installing dependencies..."
    install_dependencies

    # Verify installation
    if python3 -c "import gi; gi.require_version('Gtk', '3.0'); from gi.repository import Gtk" 2>/dev/null; then
        print_success "Dependencies installed successfully"
    else
        print_error "Failed to install dependencies. Please install manually."
        exit 1
    fi
fi

# Make scripts executable
print_step "Setting up application..."
chmod +x "$LAUNCHER"
chmod +x "$MAIN_SCRIPT"
print_success "Scripts made executable"

# Create local applications directory if it doesn't exist
mkdir -p ~/.local/share/applications

# Update desktop file with correct paths
print_step "Configuring desktop entry..."
cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Claude Code Reference
Comment=Searchable reference for Claude Code commands, shortcuts, and keyboard bindings
Exec=$LAUNCHER
Icon=$SCRIPT_DIR/icon.svg
Terminal=false
Categories=Development;Utility;Documentation;
Keywords=claude;code;reference;shortcuts;commands;terminal;ai;
StartupNotify=true
StartupWMClass=claude-code-reference
EOF

# Install desktop file
cp "$DESKTOP_FILE" ~/.local/share/applications/
print_success "Desktop entry installed"

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database ~/.local/share/applications/ 2>/dev/null || true
fi

# Create optional symlink for command-line access
print_step "Creating command-line launcher..."
mkdir -p ~/.local/bin
ln -sf "$LAUNCHER" ~/.local/bin/claude-ref 2>/dev/null || true

# Check if ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo -e "${YELLOW}Note:${NC} Add ~/.local/bin to your PATH to use 'claude-ref' command"
fi

print_success "Command 'claude-ref' available (if ~/.local/bin is in PATH)"

echo
echo -e "${GREEN}╔═══════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║         Installation Complete!                    ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════╝${NC}"
echo
echo "Launch the app:"
echo "  • From your application menu: 'Claude Code Reference'"
echo "  • From terminal: claude-ref"
echo "  • Directly: $LAUNCHER"
echo
echo "Keyboard shortcuts:"
echo "  Ctrl+F  - Focus search"
echo "  Ctrl+Q  - Quit"
echo "  Escape  - Clear search"
echo
echo -e "${BLUE}Enjoy! 🚀${NC}"
echo
