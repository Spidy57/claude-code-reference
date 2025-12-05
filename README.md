# Claude Code Reference

A searchable GTK desktop applet for Linux that provides a complete reference for all Claude Code commands, shortcuts, and keyboard bindings.

![Claude Code Reference](https://img.shields.io/badge/Claude%20Code-Reference-blue)
![Platform](https://img.shields.io/badge/Platform-Linux-green)
![Python](https://img.shields.io/badge/Python-3.6+-yellow)
![License](https://img.shields.io/badge/License-MIT-purple)

## Features

- **Comprehensive Reference**: 100+ commands, shortcuts, and keyboard bindings
- **Advanced Search**: Real-time search with regex and case-sensitive options
- **Category Browsing**: 20 organized categories with filtering
- **Type Filtering**: Filter by slash commands, keyboard shortcuts, CLI flags, vim bindings, hooks, and more
- **Copy to Clipboard**: One-click copying of commands
- **Dark Theme**: Modern dark UI that matches terminal aesthetics
- **Keyboard Shortcuts**: Full keyboard navigation support

## Screenshots

The app features:
- Sidebar with all 20 categories
- Search bar with regex/case-sensitive toggles
- Type filter buttons
- Command cards with descriptions, examples, and tags

## Installation

### Quick Install (Recommended)

```bash
# Clone or extract the package
cd claude-code-reference

# Run the installer
./install.sh
```

The installer will:
1. Check and install dependencies if needed
2. Make scripts executable
3. Add the app to your application menu

### Manual Installation

1. Ensure dependencies are installed:
   ```bash
   sudo apt install python3 python3-gi python3-gi-cairo gir1.2-gtk-3.0
   ```

2. Make scripts executable:
   ```bash
   chmod +x launch.sh claude_code_reference.py
   ```

3. Run the app:
   ```bash
   ./launch.sh
   ```

4. (Optional) Add to application menu:
   ```bash
   cp claude-code-reference.desktop ~/.local/share/applications/
   ```

## Usage

### Launching

- **From Menu**: Find "Claude Code Reference" in your application menu (under Development or Accessories)
- **From Terminal**: Run `./launch.sh` or `python3 claude_code_reference.py`

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+F` | Focus search box |
| `Ctrl+Q` | Quit application |
| `Escape` | Clear search |

### Search Features

- **Basic Search**: Type to search across commands, descriptions, examples, and tags
- **Regex Search**: Enable the "Regex" checkbox to use regular expressions
- **Case Sensitive**: Enable the "Case" checkbox for case-sensitive matching

### Browsing

1. **Categories**: Click any category in the sidebar to filter
2. **Type Filters**: Use the filter buttons to show only specific types (Slash, Keyboard, Flag, etc.)
3. **All Commands**: Click "All Commands" to see everything

## Categories Included

| Category | Description |
|----------|-------------|
| Conversation Management | `/clear`, `/compact`, `/resume`, `/rewind`, etc. |
| Configuration & Settings | `/config`, `/model`, `/vim`, `/settings`, etc. |
| Development Tools | `/review`, `/sandbox`, `/memory`, `/init`, etc. |
| Administration | `/permissions`, `/mcp`, `/hooks`, `/plugin`, etc. |
| Utilities & Information | `/help`, `/context`, `/cost`, `/doctor`, etc. |
| General Controls | `Ctrl+C`, `Ctrl+D`, `Ctrl+L`, `Ctrl+R`, etc. |
| Input Methods | Multiline input shortcuts |
| Quick Prefixes | `#`, `/`, `!`, `@` prefixes |
| Vim Mode - Navigation | `h/j/k/l`, `w`, `b`, `gg`, `G`, etc. |
| Vim Mode - Editing | `i`, `a`, `o`, `dd`, `cc`, etc. |
| CLI Flags - Session | `--continue`, `--resume`, `--session-id`, etc. |
| CLI Flags - Model | `--model`, `--agent`, `--print`, etc. |
| CLI Flags - Prompts | `--system-prompt`, `--append-system-prompt`, etc. |
| CLI Flags - Tools | `--tools`, `--allowedTools`, `--disallowedTools`, etc. |
| CLI Flags - Output | `--output-format`, `--verbose`, `--debug`, etc. |
| CLI Flags - MCP | `--mcp-config`, `--add-dir`, `--settings`, etc. |
| Hooks | `PreToolUse`, `PostToolUse`, `SessionStart`, etc. |
| Modes & Features | Plan Mode, Sandbox, Extended Thinking, etc. |
| Custom Commands | Creating project and personal commands |

## Requirements

- **OS**: Linux (tested on Linux Mint, Ubuntu, Debian)
- **Python**: 3.6 or higher
- **GTK**: 3.0
- **Dependencies**: `python3-gi`, `python3-gi-cairo`, `gir1.2-gtk-3.0`

## Uninstallation

```bash
# Remove from application menu
rm ~/.local/share/applications/claude-code-reference.desktop

# Remove the application folder
rm -rf /path/to/claude-code-reference
```

## Troubleshooting

### App won't start
Ensure GTK dependencies are installed:
```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0
```

### Icon not showing in menu
Update the desktop database:
```bash
update-desktop-database ~/.local/share/applications/
```

### Search not working
Try disabling regex mode if your search pattern contains special characters.

## Contributing

Feel free to submit issues and pull requests to improve the reference data or add features.

## License

MIT License - Feel free to use, modify, and distribute.

## Credits

- Reference data compiled from official Claude Code documentation
- Built with Python and GTK3
