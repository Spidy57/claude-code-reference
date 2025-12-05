#!/usr/bin/env python3
"""
Claude Code Reference Applet for Linux Mint
A searchable reference for all Claude Code commands, shortcuts, and keyboard bindings.
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Pango, GLib
import json
import re

# Complete Claude Code reference data
CLAUDE_CODE_DATA = {
    "categories": [
        {
            "name": "Conversation Management",
            "icon": "dialog-information",
            "description": "Commands for managing conversation history and context",
            "items": [
                {
                    "command": "/clear",
                    "type": "slash",
                    "description": "Remove conversation history and start fresh",
                    "example": "/clear",
                    "tags": ["history", "reset", "clean"]
                },
                {
                    "command": "/compact [instructions]",
                    "type": "slash",
                    "description": "Compress conversation with optional focus; helps manage token usage",
                    "example": "/compact focus on the authentication code",
                    "tags": ["tokens", "compress", "context"]
                },
                {
                    "command": "/export [filename]",
                    "type": "slash",
                    "description": "Save conversation to file or clipboard",
                    "example": "/export ~/my-session.md",
                    "tags": ["save", "backup", "export"]
                },
                {
                    "command": "/resume",
                    "type": "slash",
                    "description": "Continue a previous conversation session",
                    "example": "/resume",
                    "tags": ["continue", "session", "restore"]
                },
                {
                    "command": "/rewind",
                    "type": "slash",
                    "description": "Undo conversation changes or code edits",
                    "example": "/rewind",
                    "tags": ["undo", "rollback", "restore"]
                },
                {
                    "command": "Esc + Esc",
                    "type": "keyboard",
                    "description": "Rewind code and conversation to prior state",
                    "example": "Press Escape twice quickly",
                    "tags": ["undo", "rewind", "quick"]
                }
            ]
        },
        {
            "name": "Configuration & Settings",
            "icon": "preferences-system",
            "description": "Commands for configuring Claude Code behavior",
            "items": [
                {
                    "command": "/config",
                    "type": "slash",
                    "description": "Open Settings interface (Config tab)",
                    "example": "/config",
                    "tags": ["settings", "preferences", "options"]
                },
                {
                    "command": "/status",
                    "type": "slash",
                    "description": "Display version, model, account, and connectivity info",
                    "example": "/status",
                    "tags": ["info", "version", "account"]
                },
                {
                    "command": "/model",
                    "type": "slash",
                    "description": "Switch AI models (aliases: sonnet, opus, or full name)",
                    "example": "/model opus",
                    "tags": ["model", "switch", "ai"]
                },
                {
                    "command": "/output-style [style]",
                    "type": "slash",
                    "description": "Adjust output formatting style",
                    "example": "/output-style concise",
                    "tags": ["format", "output", "style"]
                },
                {
                    "command": "/settings",
                    "type": "slash",
                    "description": "Manage configuration options",
                    "example": "/settings",
                    "tags": ["config", "preferences", "options"]
                },
                {
                    "command": "/vim",
                    "type": "slash",
                    "description": "Enable Vim editor mode for input",
                    "example": "/vim",
                    "tags": ["vim", "editor", "mode"]
                },
                {
                    "command": "Shift+Tab or Alt+M",
                    "type": "keyboard",
                    "description": "Switch permission modes",
                    "example": "Press Shift+Tab to cycle modes",
                    "tags": ["permissions", "mode", "switch"]
                },
                {
                    "command": "Tab",
                    "type": "keyboard",
                    "description": "Toggle extended thinking feature",
                    "example": "Press Tab before sending prompt",
                    "tags": ["thinking", "extended", "analysis"]
                }
            ]
        },
        {
            "name": "Development Tools",
            "icon": "applications-development",
            "description": "Commands for code development and review",
            "items": [
                {
                    "command": "/review",
                    "type": "slash",
                    "description": "Request code review for current changes",
                    "example": "/review",
                    "tags": ["code", "review", "audit"]
                },
                {
                    "command": "/security-review",
                    "type": "slash",
                    "description": "Audit pending changes for security vulnerabilities",
                    "example": "/security-review",
                    "tags": ["security", "audit", "vulnerabilities"]
                },
                {
                    "command": "/sandbox",
                    "type": "slash",
                    "description": "Enable isolated bash execution with filesystem/network restrictions",
                    "example": "/sandbox",
                    "tags": ["sandbox", "isolated", "safe"]
                },
                {
                    "command": "/init",
                    "type": "slash",
                    "description": "Initialize project with CLAUDE.md guide",
                    "example": "/init",
                    "tags": ["init", "project", "setup"]
                },
                {
                    "command": "/memory",
                    "type": "slash",
                    "description": "Edit CLAUDE.md memory files for persistent context",
                    "example": "/memory",
                    "tags": ["memory", "context", "persistent"]
                }
            ]
        },
        {
            "name": "Administration",
            "icon": "preferences-other",
            "description": "Commands for managing permissions, plugins, and integrations",
            "items": [
                {
                    "command": "/permissions",
                    "type": "slash",
                    "description": "View/update access controls and tool permissions",
                    "example": "/permissions",
                    "tags": ["access", "permissions", "security"]
                },
                {
                    "command": "/mcp",
                    "type": "slash",
                    "description": "Manage MCP server connections and OAuth",
                    "example": "/mcp list",
                    "tags": ["mcp", "servers", "oauth"]
                },
                {
                    "command": "/plugin",
                    "type": "slash",
                    "description": "Install and manage plugins",
                    "example": "/plugin install my-plugin",
                    "tags": ["plugin", "install", "extend"]
                },
                {
                    "command": "/hooks",
                    "type": "slash",
                    "description": "Configure tool event handlers and automation",
                    "example": "/hooks",
                    "tags": ["hooks", "automation", "events"]
                },
                {
                    "command": "/ide",
                    "type": "slash",
                    "description": "Check IDE integration status",
                    "example": "/ide",
                    "tags": ["ide", "integration", "editor"]
                }
            ]
        },
        {
            "name": "Utilities & Information",
            "icon": "utilities-terminal",
            "description": "Helpful utility commands and information display",
            "items": [
                {
                    "command": "/help",
                    "type": "slash",
                    "description": "Display available commands and help information",
                    "example": "/help",
                    "tags": ["help", "commands", "info"]
                },
                {
                    "command": "/context",
                    "type": "slash",
                    "description": "Visualize token usage as colored grid",
                    "example": "/context",
                    "tags": ["tokens", "context", "usage"]
                },
                {
                    "command": "/cost",
                    "type": "slash",
                    "description": "Show token statistics and cost information",
                    "example": "/cost",
                    "tags": ["cost", "tokens", "stats"]
                },
                {
                    "command": "/doctor",
                    "type": "slash",
                    "description": "Verify installation health and diagnose issues",
                    "example": "/doctor",
                    "tags": ["health", "diagnose", "check"]
                },
                {
                    "command": "/usage",
                    "type": "slash",
                    "description": "Display plan limits and rate status",
                    "example": "/usage",
                    "tags": ["usage", "limits", "rate"]
                }
            ]
        },
        {
            "name": "General Controls",
            "icon": "input-keyboard",
            "description": "Essential keyboard shortcuts for general control",
            "items": [
                {
                    "command": "Ctrl+C",
                    "type": "keyboard",
                    "description": "Cancel current input or generation",
                    "example": "Press during long operation",
                    "tags": ["cancel", "stop", "interrupt"]
                },
                {
                    "command": "Ctrl+D",
                    "type": "keyboard",
                    "description": "Exit the Claude Code session",
                    "example": "Press to quit",
                    "tags": ["exit", "quit", "close"]
                },
                {
                    "command": "Ctrl+L",
                    "type": "keyboard",
                    "description": "Clear terminal screen",
                    "example": "Press to clear display",
                    "tags": ["clear", "screen", "terminal"]
                },
                {
                    "command": "Ctrl+O",
                    "type": "keyboard",
                    "description": "Toggle verbose output mode",
                    "example": "Press to see more details",
                    "tags": ["verbose", "debug", "output"]
                },
                {
                    "command": "Ctrl+R",
                    "type": "keyboard",
                    "description": "Access reverse command history search",
                    "example": "Press and type to search history",
                    "tags": ["history", "search", "reverse"]
                },
                {
                    "command": "Ctrl+V / Alt+V",
                    "type": "keyboard",
                    "description": "Paste images from clipboard (Ctrl+V on Mac/Linux, Alt+V on Windows)",
                    "example": "Copy image, then paste",
                    "tags": ["paste", "image", "clipboard"]
                },
                {
                    "command": "Ctrl+B",
                    "type": "keyboard",
                    "description": "Background long-running processes (Tmux: press twice)",
                    "example": "Press during long task",
                    "tags": ["background", "process", "tmux"]
                },
                {
                    "command": "Up/Down arrows",
                    "type": "keyboard",
                    "description": "Navigate through previous inputs",
                    "example": "Press Up to see last command",
                    "tags": ["history", "navigate", "previous"]
                }
            ]
        },
        {
            "name": "Input Methods",
            "icon": "accessories-text-editor",
            "description": "Methods for entering and formatting input",
            "items": [
                {
                    "command": "\\ + Enter",
                    "type": "keyboard",
                    "description": "Continue input on next line (all terminals)",
                    "example": "Type \\ then press Enter",
                    "tags": ["multiline", "continue", "input"]
                },
                {
                    "command": "Option+Enter",
                    "type": "keyboard",
                    "description": "Continue input on next line (macOS default)",
                    "example": "Hold Option and press Enter",
                    "tags": ["multiline", "macos", "input"]
                },
                {
                    "command": "Shift+Enter",
                    "type": "keyboard",
                    "description": "Continue input on next line (after /terminal-setup)",
                    "example": "Hold Shift and press Enter",
                    "tags": ["multiline", "newline", "input"]
                },
                {
                    "command": "Ctrl+J",
                    "type": "keyboard",
                    "description": "Line feed character (all terminals)",
                    "example": "Press for new line",
                    "tags": ["newline", "linefeed", "input"]
                }
            ]
        },
        {
            "name": "Quick Prefixes",
            "icon": "emblem-symbolic-link",
            "description": "Special prefix characters for quick actions",
            "items": [
                {
                    "command": "# (hash prefix)",
                    "type": "prefix",
                    "description": "Add memory to CLAUDE.md file",
                    "example": "# Remember to use TypeScript",
                    "tags": ["memory", "note", "remember"]
                },
                {
                    "command": "/ (slash prefix)",
                    "type": "prefix",
                    "description": "Execute slash commands",
                    "example": "/help",
                    "tags": ["command", "slash", "execute"]
                },
                {
                    "command": "! (bang prefix)",
                    "type": "prefix",
                    "description": "Run bash directly without Claude interpretation",
                    "example": "!git status",
                    "tags": ["bash", "shell", "direct"]
                },
                {
                    "command": "@ (at prefix)",
                    "type": "prefix",
                    "description": "Trigger file path autocomplete",
                    "example": "@src/components/Button.tsx",
                    "tags": ["file", "path", "autocomplete"]
                }
            ]
        },
        {
            "name": "Vim Mode - Navigation",
            "icon": "go-jump",
            "description": "Vim-style navigation when /vim is enabled",
            "items": [
                {
                    "command": "h / j / k / l",
                    "type": "vim",
                    "description": "Move left / down / up / right",
                    "example": "Press h to move left",
                    "tags": ["move", "cursor", "navigation"]
                },
                {
                    "command": "w",
                    "type": "vim",
                    "description": "Jump to next word",
                    "example": "Press w to skip word",
                    "tags": ["word", "next", "jump"]
                },
                {
                    "command": "e",
                    "type": "vim",
                    "description": "Jump to word end",
                    "example": "Press e to reach word end",
                    "tags": ["word", "end", "jump"]
                },
                {
                    "command": "b",
                    "type": "vim",
                    "description": "Jump to previous word",
                    "example": "Press b to go back a word",
                    "tags": ["word", "previous", "back"]
                },
                {
                    "command": "0 (zero)",
                    "type": "vim",
                    "description": "Jump to line start",
                    "example": "Press 0 to go to beginning",
                    "tags": ["line", "start", "beginning"]
                },
                {
                    "command": "$",
                    "type": "vim",
                    "description": "Jump to line end",
                    "example": "Press $ to go to end",
                    "tags": ["line", "end", "dollar"]
                },
                {
                    "command": "gg",
                    "type": "vim",
                    "description": "Jump to document start",
                    "example": "Press gg to go to top",
                    "tags": ["document", "start", "top"]
                },
                {
                    "command": "G",
                    "type": "vim",
                    "description": "Jump to document end",
                    "example": "Press G to go to bottom",
                    "tags": ["document", "end", "bottom"]
                }
            ]
        },
        {
            "name": "Vim Mode - Editing",
            "icon": "document-edit",
            "description": "Vim-style editing commands when /vim is enabled",
            "items": [
                {
                    "command": "i / I",
                    "type": "vim",
                    "description": "Insert mode at cursor / at line start",
                    "example": "Press i to start inserting",
                    "tags": ["insert", "mode", "cursor"]
                },
                {
                    "command": "a / A",
                    "type": "vim",
                    "description": "Insert mode after cursor / at line end",
                    "example": "Press a to append",
                    "tags": ["append", "insert", "after"]
                },
                {
                    "command": "o / O",
                    "type": "vim",
                    "description": "New line below / above and insert",
                    "example": "Press o for new line below",
                    "tags": ["newline", "insert", "open"]
                },
                {
                    "command": "x",
                    "type": "vim",
                    "description": "Delete character at cursor",
                    "example": "Press x to delete char",
                    "tags": ["delete", "character", "remove"]
                },
                {
                    "command": "dd",
                    "type": "vim",
                    "description": "Delete entire line",
                    "example": "Press dd to delete line",
                    "tags": ["delete", "line", "cut"]
                },
                {
                    "command": "dw / de / db",
                    "type": "vim",
                    "description": "Delete word / to word end / to word start",
                    "example": "Press dw to delete word",
                    "tags": ["delete", "word", "cut"]
                },
                {
                    "command": "cc / C",
                    "type": "vim",
                    "description": "Change entire line / from cursor to end",
                    "example": "Press cc to replace line",
                    "tags": ["change", "line", "replace"]
                },
                {
                    "command": ".",
                    "type": "vim",
                    "description": "Repeat last action",
                    "example": "Press . to repeat",
                    "tags": ["repeat", "redo", "action"]
                },
                {
                    "command": "Esc",
                    "type": "vim",
                    "description": "Return to NORMAL mode",
                    "example": "Press Esc to exit insert",
                    "tags": ["normal", "mode", "escape"]
                }
            ]
        },
        {
            "name": "CLI Flags - Session",
            "icon": "document-open-recent",
            "description": "Command line flags for session management",
            "items": [
                {
                    "command": "--continue, -c",
                    "type": "flag",
                    "description": "Load most recent conversation",
                    "example": "claude -c",
                    "tags": ["continue", "resume", "session"]
                },
                {
                    "command": "--resume, -r",
                    "type": "flag",
                    "description": "Resume specific session by ID",
                    "example": "claude -r \"abc123\" \"query\"",
                    "tags": ["resume", "session", "id"]
                },
                {
                    "command": "--session-id",
                    "type": "flag",
                    "description": "Use specific UUID for conversation",
                    "example": "claude --session-id \"my-uuid\"",
                    "tags": ["session", "uuid", "id"]
                },
                {
                    "command": "--fork-session",
                    "type": "flag",
                    "description": "Create new ID when resuming (branch off)",
                    "example": "claude --fork-session -c",
                    "tags": ["fork", "branch", "session"]
                }
            ]
        },
        {
            "name": "CLI Flags - Model & Behavior",
            "icon": "preferences-desktop",
            "description": "Command line flags for model and behavior control",
            "items": [
                {
                    "command": "--model",
                    "type": "flag",
                    "description": "Set model (aliases: sonnet, opus, or full name)",
                    "example": "claude --model opus",
                    "tags": ["model", "ai", "switch"]
                },
                {
                    "command": "--agent",
                    "type": "flag",
                    "description": "Specify custom agent to use",
                    "example": "claude --agent \"my-agent\"",
                    "tags": ["agent", "custom", "specify"]
                },
                {
                    "command": "--agents",
                    "type": "flag",
                    "description": "Define subagents dynamically via JSON",
                    "example": "claude --agents '{\"name\": {...}}'",
                    "tags": ["agents", "subagents", "json"]
                },
                {
                    "command": "--print, -p",
                    "type": "flag",
                    "description": "Print response without interactive mode; exits after",
                    "example": "claude -p \"explain this code\"",
                    "tags": ["print", "non-interactive", "output"]
                },
                {
                    "command": "--max-turns",
                    "type": "flag",
                    "description": "Limit agentic turns (non-interactive only)",
                    "example": "claude --max-turns 5 -p \"task\"",
                    "tags": ["turns", "limit", "agentic"]
                }
            ]
        },
        {
            "name": "CLI Flags - System Prompts",
            "icon": "document-properties",
            "description": "Command line flags for customizing system prompts",
            "items": [
                {
                    "command": "--system-prompt",
                    "type": "flag",
                    "description": "Replace entire default prompt (non-interactive only)",
                    "example": "claude --system-prompt \"You are a Python expert\"",
                    "tags": ["system", "prompt", "replace"]
                },
                {
                    "command": "--system-prompt-file",
                    "type": "flag",
                    "description": "Load system prompt from file",
                    "example": "claude --system-prompt-file ./prompt.txt",
                    "tags": ["system", "prompt", "file"]
                },
                {
                    "command": "--append-system-prompt",
                    "type": "flag",
                    "description": "Add to default prompt (recommended approach)",
                    "example": "claude --append-system-prompt \"Focus on security\"",
                    "tags": ["append", "prompt", "add"]
                }
            ]
        },
        {
            "name": "CLI Flags - Tools & Permissions",
            "icon": "security-high",
            "description": "Command line flags for tool and permission control",
            "items": [
                {
                    "command": "--tools",
                    "type": "flag",
                    "description": "Specify available built-in tools list",
                    "example": "claude --tools Read,Write,Bash",
                    "tags": ["tools", "list", "available"]
                },
                {
                    "command": "--allowedTools",
                    "type": "flag",
                    "description": "Permit tools without prompting",
                    "example": "claude --allowedTools Read,Grep",
                    "tags": ["allowed", "permit", "auto"]
                },
                {
                    "command": "--disallowedTools",
                    "type": "flag",
                    "description": "Block tools without prompting",
                    "example": "claude --disallowedTools Bash",
                    "tags": ["blocked", "disallow", "prevent"]
                },
                {
                    "command": "--permission-mode",
                    "type": "flag",
                    "description": "Begin in specified permission mode",
                    "example": "claude --permission-mode default",
                    "tags": ["permission", "mode", "security"]
                },
                {
                    "command": "--dangerously-skip-permissions",
                    "type": "flag",
                    "description": "Skip permission prompts (use with caution)",
                    "example": "claude --dangerously-skip-permissions",
                    "tags": ["skip", "dangerous", "permissions"]
                }
            ]
        },
        {
            "name": "CLI Flags - Output & Debug",
            "icon": "utilities-system-monitor",
            "description": "Command line flags for output format and debugging",
            "items": [
                {
                    "command": "--output-format",
                    "type": "flag",
                    "description": "Choose format: text, json, stream-json",
                    "example": "claude --output-format json -p \"query\"",
                    "tags": ["output", "format", "json"]
                },
                {
                    "command": "--input-format",
                    "type": "flag",
                    "description": "Specify input format",
                    "example": "claude --input-format json",
                    "tags": ["input", "format", "parse"]
                },
                {
                    "command": "--verbose",
                    "type": "flag",
                    "description": "Enable verbose logging",
                    "example": "claude --verbose",
                    "tags": ["verbose", "logging", "debug"]
                },
                {
                    "command": "--debug",
                    "type": "flag",
                    "description": "Enable debug mode with optional filtering",
                    "example": "claude --debug",
                    "tags": ["debug", "diagnostics", "trace"]
                },
                {
                    "command": "--json-schema",
                    "type": "flag",
                    "description": "Get validated JSON output matching schema",
                    "example": "claude --json-schema '{...}' -p \"query\"",
                    "tags": ["json", "schema", "validate"]
                }
            ]
        },
        {
            "name": "CLI Flags - MCP & Advanced",
            "icon": "network-server",
            "description": "Command line flags for MCP and advanced configuration",
            "items": [
                {
                    "command": "--mcp-config",
                    "type": "flag",
                    "description": "Load MCP servers from config files",
                    "example": "claude --mcp-config ./mcp.json",
                    "tags": ["mcp", "config", "servers"]
                },
                {
                    "command": "--strict-mcp-config",
                    "type": "flag",
                    "description": "Use only specified MCP configuration",
                    "example": "claude --strict-mcp-config --mcp-config ./mcp.json",
                    "tags": ["mcp", "strict", "only"]
                },
                {
                    "command": "--add-dir",
                    "type": "flag",
                    "description": "Add working directories for access",
                    "example": "claude --add-dir /path/to/dir",
                    "tags": ["directory", "add", "access"]
                },
                {
                    "command": "--settings",
                    "type": "flag",
                    "description": "Load settings from JSON file or string",
                    "example": "claude --settings ~/.claude/settings.json",
                    "tags": ["settings", "config", "json"]
                },
                {
                    "command": "--fallback-model",
                    "type": "flag",
                    "description": "Auto-fallback when primary model overloaded",
                    "example": "claude --fallback-model sonnet",
                    "tags": ["fallback", "model", "backup"]
                },
                {
                    "command": "--version, -v",
                    "type": "flag",
                    "description": "Output version number",
                    "example": "claude --version",
                    "tags": ["version", "info", "about"]
                }
            ]
        },
        {
            "name": "Hooks",
            "icon": "emblem-system",
            "description": "Event hooks for automation and custom behavior",
            "items": [
                {
                    "command": "PreToolUse",
                    "type": "hook",
                    "description": "Triggers after Claude creates tool parameters but before processing",
                    "example": "Allow, deny, or ask for permission before tool runs",
                    "tags": ["before", "tool", "validate"]
                },
                {
                    "command": "PostToolUse",
                    "type": "hook",
                    "description": "Triggers after tool completes successfully",
                    "example": "Log tool results or trigger follow-up actions",
                    "tags": ["after", "tool", "complete"]
                },
                {
                    "command": "PermissionRequest",
                    "type": "hook",
                    "description": "Triggers when permission dialogs are shown",
                    "example": "Auto-approve or deny permissions programmatically",
                    "tags": ["permission", "dialog", "auto"]
                },
                {
                    "command": "UserPromptSubmit",
                    "type": "hook",
                    "description": "Triggers when users submit prompts, before Claude processes",
                    "example": "Validate input or inject context",
                    "tags": ["prompt", "submit", "validate"]
                },
                {
                    "command": "Notification",
                    "type": "hook",
                    "description": "Triggers when Claude sends notifications",
                    "example": "Filter by type like 'permission_prompt'",
                    "tags": ["notification", "alert", "filter"]
                },
                {
                    "command": "Stop",
                    "type": "hook",
                    "description": "Triggers when main agent finishes responding",
                    "example": "Force continuation or perform cleanup",
                    "tags": ["stop", "finish", "end"]
                },
                {
                    "command": "SubagentStop",
                    "type": "hook",
                    "description": "Triggers when subagent (Task tool) finishes",
                    "example": "Evaluate task completion intelligently",
                    "tags": ["subagent", "task", "complete"]
                },
                {
                    "command": "SessionStart",
                    "type": "hook",
                    "description": "Triggers at session initialization or resume",
                    "example": "Load development context, set env vars",
                    "tags": ["session", "start", "init"]
                },
                {
                    "command": "SessionEnd",
                    "type": "hook",
                    "description": "Triggers when session terminates",
                    "example": "Cleanup and logging tasks",
                    "tags": ["session", "end", "cleanup"]
                }
            ]
        },
        {
            "name": "Modes & Features",
            "icon": "applications-system",
            "description": "Special operational modes and features",
            "items": [
                {
                    "command": "Plan Mode",
                    "type": "mode",
                    "description": "Strategic task planning and project analysis mode",
                    "example": "Activated automatically for complex planning tasks",
                    "tags": ["plan", "strategy", "analysis"]
                },
                {
                    "command": "Build Mode",
                    "type": "mode",
                    "description": "Code generation and development tasks mode",
                    "example": "Activated for implementation work",
                    "tags": ["build", "code", "develop"]
                },
                {
                    "command": "Sandbox Mode",
                    "type": "mode",
                    "description": "Isolated bash with filesystem/network restrictions",
                    "example": "/sandbox to enable",
                    "tags": ["sandbox", "isolated", "restricted"]
                },
                {
                    "command": "Extended Thinking",
                    "type": "mode",
                    "description": "Deeper analysis before responding",
                    "example": "Press Tab before sending prompt",
                    "tags": ["thinking", "deep", "analysis"]
                },
                {
                    "command": "Verbose Output",
                    "type": "mode",
                    "description": "Detailed logging and output display",
                    "example": "Ctrl+O to toggle",
                    "tags": ["verbose", "detailed", "logging"]
                },
                {
                    "command": "Checkpointing",
                    "type": "feature",
                    "description": "Automatically track and rewind Claude's edits",
                    "example": "Use Esc+Esc to rewind",
                    "tags": ["checkpoint", "rewind", "undo"]
                },
                {
                    "command": "Memory Management",
                    "type": "feature",
                    "description": "Persistent context via CLAUDE.md files",
                    "example": "/memory to edit, # prefix to add",
                    "tags": ["memory", "persistent", "context"]
                },
                {
                    "command": "MCP Server Support",
                    "type": "feature",
                    "description": "Connect external tools and APIs via Model Context Protocol",
                    "example": "/mcp to manage connections",
                    "tags": ["mcp", "external", "api"]
                }
            ]
        },
        {
            "name": "Custom Commands",
            "icon": "folder-templates",
            "description": "Creating and using custom slash commands",
            "items": [
                {
                    "command": "Project Commands",
                    "type": "custom",
                    "description": "Shared commands in .claude/commands/ directory",
                    "example": "Create .claude/commands/deploy.md",
                    "tags": ["project", "team", "shared"]
                },
                {
                    "command": "Personal Commands",
                    "type": "custom",
                    "description": "Personal commands in ~/.claude/commands/ directory",
                    "example": "Create ~/.claude/commands/myhelper.md",
                    "tags": ["personal", "user", "global"]
                },
                {
                    "command": "$ARGUMENTS",
                    "type": "custom",
                    "description": "Capture all arguments passed to custom command",
                    "example": "/mycommand arg1 arg2 -> $ARGUMENTS = 'arg1 arg2'",
                    "tags": ["arguments", "all", "capture"]
                },
                {
                    "command": "$1, $2, $3",
                    "type": "custom",
                    "description": "Access specific positional arguments",
                    "example": "/mycommand first second -> $1='first', $2='second'",
                    "tags": ["positional", "arguments", "numbered"]
                },
                {
                    "command": "Frontmatter",
                    "type": "custom",
                    "description": "Metadata for custom commands (allowed-tools, description, model)",
                    "example": "---\\nallowed-tools: Read,Write\\ndescription: My helper\\n---",
                    "tags": ["metadata", "config", "yaml"]
                }
            ]
        }
    ]
}


class ClaudeCodeReferenceApp(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Claude Code Reference")
        self.set_default_size(1100, 750)
        self.set_position(Gtk.WindowPosition.CENTER)

        # Apply CSS styling
        self.apply_css()

        # Main container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(main_box)

        # Header with search
        header_box = self.create_header()
        main_box.pack_start(header_box, False, False, 0)

        # Content area with sidebar and main content
        content_paned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        main_box.pack_start(content_paned, True, True, 0)

        # Sidebar with categories
        sidebar = self.create_sidebar()
        content_paned.pack1(sidebar, False, False)

        # Main content area
        self.content_area = self.create_content_area()
        content_paned.pack2(self.content_area, True, True)
        content_paned.set_position(280)

        # Status bar
        self.statusbar = Gtk.Statusbar()
        self.statusbar.get_style_context().add_class("statusbar")
        main_box.pack_end(self.statusbar, False, False, 0)

        # Initialize state
        self.current_category = None
        self.search_results = []
        self.all_items = self.flatten_items()

        # Show all categories initially
        self.show_all_categories()
        self.update_status()

        # Connect keyboard shortcuts
        self.connect("key-press-event", self.on_key_press)

    def apply_css(self):
        css_provider = Gtk.CssProvider()
        css = b"""
        window {
            background-color: #1e1e2e;
        }

        .header-box {
            background-color: #313244;
            padding: 15px;
            border-bottom: 1px solid #45475a;
        }

        .title-label {
            font-size: 20px;
            font-weight: bold;
            color: #cdd6f4;
        }

        .subtitle-label {
            font-size: 12px;
            color: #a6adc8;
        }

        .search-entry {
            font-size: 14px;
            padding: 8px 12px;
            border-radius: 8px;
            background-color: #45475a;
            color: #cdd6f4;
            border: 2px solid #585b70;
            min-width: 350px;
        }

        .search-entry:focus {
            border-color: #89b4fa;
        }

        .sidebar {
            background-color: #1e1e2e;
            border-right: 1px solid #45475a;
        }

        .sidebar-title {
            font-size: 11px;
            font-weight: bold;
            color: #a6adc8;
            padding: 10px 15px 5px 15px;
        }

        .category-button {
            padding: 10px 15px;
            border-radius: 0;
            background-color: transparent;
            color: #cdd6f4;
            border: none;
            font-size: 13px;
        }

        .category-button:hover {
            background-color: #313244;
        }

        .category-button.active {
            background-color: #45475a;
            border-left: 3px solid #89b4fa;
        }

        .content-area {
            background-color: #1e1e2e;
        }

        .category-header {
            font-size: 18px;
            font-weight: bold;
            color: #cdd6f4;
            padding: 15px;
            background-color: #313244;
            border-bottom: 1px solid #45475a;
        }

        .category-desc {
            font-size: 12px;
            color: #a6adc8;
            padding: 0 15px 10px 15px;
            background-color: #313244;
        }

        .item-card {
            background-color: #313244;
            border-radius: 8px;
            padding: 12px 15px;
            margin: 5px 10px;
            border: 1px solid #45475a;
        }

        .item-card:hover {
            border-color: #89b4fa;
        }

        .command-label {
            font-family: monospace;
            font-size: 14px;
            font-weight: bold;
            color: #89b4fa;
        }

        .type-badge {
            font-size: 10px;
            padding: 2px 8px;
            border-radius: 4px;
            color: #1e1e2e;
        }

        .type-slash {
            background-color: #a6e3a1;
        }

        .type-keyboard {
            background-color: #f9e2af;
        }

        .type-flag {
            background-color: #89b4fa;
        }

        .type-vim {
            background-color: #cba6f7;
        }

        .type-hook {
            background-color: #f38ba8;
        }

        .type-prefix {
            background-color: #94e2d5;
        }

        .type-mode {
            background-color: #fab387;
        }

        .type-feature {
            background-color: #74c7ec;
        }

        .type-custom {
            background-color: #eba0ac;
        }

        .description-label {
            font-size: 12px;
            color: #bac2de;
            margin-top: 5px;
        }

        .example-box {
            background-color: #1e1e2e;
            border-radius: 4px;
            padding: 6px 10px;
            margin-top: 8px;
            font-family: monospace;
            font-size: 11px;
            color: #a6adc8;
        }

        .example-label {
            font-size: 10px;
            color: #6c7086;
            margin-top: 8px;
        }

        .tags-box {
            margin-top: 5px;
        }

        .tag {
            font-size: 9px;
            padding: 1px 6px;
            border-radius: 3px;
            background-color: #45475a;
            color: #a6adc8;
            margin-right: 4px;
        }

        .filter-box {
            padding: 5px 10px;
            background-color: #313244;
            border-bottom: 1px solid #45475a;
        }

        .filter-button {
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 11px;
            margin: 2px;
            background-color: #45475a;
            color: #cdd6f4;
            border: none;
        }

        .filter-button:hover, .filter-button.active {
            background-color: #89b4fa;
            color: #1e1e2e;
        }

        .statusbar {
            background-color: #313244;
            color: #a6adc8;
            font-size: 11px;
            padding: 5px 15px;
            border-top: 1px solid #45475a;
        }

        .no-results {
            font-size: 14px;
            color: #6c7086;
            padding: 50px;
        }

        .highlight {
            background-color: #f9e2af;
            color: #1e1e2e;
            padding: 0 2px;
            border-radius: 2px;
        }

        .stats-label {
            font-size: 11px;
            color: #6c7086;
            padding: 5px 15px;
        }
        """
        css_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def create_header(self):
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        header_box.get_style_context().add_class("header-box")

        # Title section
        title_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)

        title_label = Gtk.Label(label="Claude Code Reference")
        title_label.get_style_context().add_class("title-label")
        title_label.set_halign(Gtk.Align.START)
        title_box.pack_start(title_label, False, False, 0)

        subtitle_label = Gtk.Label(label="All commands, shortcuts & keyboard bindings")
        subtitle_label.get_style_context().add_class("subtitle-label")
        subtitle_label.set_halign(Gtk.Align.START)
        title_box.pack_start(subtitle_label, False, False, 0)

        header_box.pack_start(title_box, False, False, 0)

        # Spacer
        header_box.pack_start(Gtk.Box(), True, True, 0)

        # Search box
        search_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        self.search_entry = Gtk.Entry()
        self.search_entry.set_placeholder_text("Search commands, shortcuts, descriptions... (Ctrl+F)")
        self.search_entry.get_style_context().add_class("search-entry")
        self.search_entry.connect("changed", self.on_search_changed)
        self.search_entry.connect("activate", self.on_search_activate)
        search_box.pack_start(self.search_entry, False, False, 0)

        # Search options
        self.regex_check = Gtk.CheckButton(label="Regex")
        self.regex_check.set_tooltip_text("Enable regular expression search")
        self.regex_check.connect("toggled", self.on_search_changed)
        search_box.pack_start(self.regex_check, False, False, 0)

        self.case_check = Gtk.CheckButton(label="Case")
        self.case_check.set_tooltip_text("Case sensitive search")
        self.case_check.connect("toggled", self.on_search_changed)
        search_box.pack_start(self.case_check, False, False, 0)

        header_box.pack_start(search_box, False, False, 0)

        return header_box

    def create_sidebar(self):
        sidebar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        sidebar_box.get_style_context().add_class("sidebar")
        sidebar_box.set_size_request(280, -1)

        # All categories button
        all_label = Gtk.Label(label="CATEGORIES")
        all_label.get_style_context().add_class("sidebar-title")
        all_label.set_halign(Gtk.Align.START)
        sidebar_box.pack_start(all_label, False, False, 0)

        # Scrolled window for categories
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        categories_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        # All button
        self.all_button = Gtk.Button(label="  All Commands")
        self.all_button.get_style_context().add_class("category-button")
        self.all_button.get_style_context().add_class("active")
        self.all_button.set_halign(Gtk.Align.FILL)
        self.all_button.connect("clicked", self.on_show_all)
        categories_box.pack_start(self.all_button, False, False, 0)

        # Category buttons
        self.category_buttons = {}
        for category in CLAUDE_CODE_DATA["categories"]:
            btn = Gtk.Button()
            btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)

            # Icon
            icon = Gtk.Image.new_from_icon_name(category["icon"], Gtk.IconSize.MENU)
            btn_box.pack_start(icon, False, False, 0)

            # Label with count
            count = len(category["items"])
            label = Gtk.Label(label=f"{category['name']} ({count})")
            label.set_halign(Gtk.Align.START)
            btn_box.pack_start(label, True, True, 0)

            btn.add(btn_box)
            btn.get_style_context().add_class("category-button")
            btn.connect("clicked", self.on_category_selected, category)
            categories_box.pack_start(btn, False, False, 0)
            self.category_buttons[category["name"]] = btn

        scrolled.add(categories_box)
        sidebar_box.pack_start(scrolled, True, True, 0)

        # Stats at bottom
        total = sum(len(c["items"]) for c in CLAUDE_CODE_DATA["categories"])
        stats_label = Gtk.Label(label=f"Total: {total} items in {len(CLAUDE_CODE_DATA['categories'])} categories")
        stats_label.get_style_context().add_class("stats-label")
        stats_label.set_halign(Gtk.Align.START)
        sidebar_box.pack_end(stats_label, False, False, 5)

        return sidebar_box

    def create_content_area(self):
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        content_box.get_style_context().add_class("content-area")

        # Type filter bar
        self.filter_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.filter_box.get_style_context().add_class("filter-box")

        filter_label = Gtk.Label(label="Filter by type:")
        self.filter_box.pack_start(filter_label, False, False, 5)

        self.type_filters = {}
        types = ["All", "slash", "keyboard", "flag", "vim", "hook", "prefix", "mode", "feature", "custom"]
        for t in types:
            btn = Gtk.ToggleButton(label=t.capitalize() if t != "All" else "All")
            btn.get_style_context().add_class("filter-button")
            if t == "All":
                btn.set_active(True)
                btn.get_style_context().add_class("active")
            btn.connect("toggled", self.on_type_filter, t)
            self.filter_box.pack_start(btn, False, False, 0)
            self.type_filters[t] = btn

        content_box.pack_start(self.filter_box, False, False, 0)

        # Header
        self.content_header = Gtk.Label(label="All Commands")
        self.content_header.get_style_context().add_class("category-header")
        self.content_header.set_halign(Gtk.Align.START)
        content_box.pack_start(self.content_header, False, False, 0)

        self.content_desc = Gtk.Label(label="Browse all Claude Code commands and shortcuts")
        self.content_desc.get_style_context().add_class("category-desc")
        self.content_desc.set_halign(Gtk.Align.START)
        content_box.pack_start(self.content_desc, False, False, 0)

        # Scrolled window for items
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        self.items_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.items_box.set_margin_top(10)
        self.items_box.set_margin_bottom(10)

        scrolled.add(self.items_box)
        content_box.pack_start(scrolled, True, True, 0)

        return content_box

    def flatten_items(self):
        """Flatten all items with their category info"""
        items = []
        for category in CLAUDE_CODE_DATA["categories"]:
            for item in category["items"]:
                items.append({
                    **item,
                    "category_name": category["name"],
                    "category_icon": category["icon"]
                })
        return items

    def create_item_widget(self, item, highlight_text=None):
        """Create a widget for a single item"""
        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        card.get_style_context().add_class("item-card")

        # Top row: command + type badge
        top_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        command_text = item["command"]
        if highlight_text:
            command_text = self.highlight_text(command_text, highlight_text)

        command_label = Gtk.Label()
        command_label.set_markup(f"<span font_family='monospace' font_weight='bold' foreground='#89b4fa'>{GLib.markup_escape_text(item['command'])}</span>")
        command_label.set_halign(Gtk.Align.START)
        command_label.set_selectable(True)
        top_row.pack_start(command_label, False, False, 0)

        # Type badge
        type_badge = Gtk.Label(label=item["type"].upper())
        type_badge.get_style_context().add_class("type-badge")
        type_badge.get_style_context().add_class(f"type-{item['type']}")
        top_row.pack_start(type_badge, False, False, 0)

        # Category badge (if showing all)
        if "category_name" in item and self.current_category is None:
            cat_label = Gtk.Label(label=item["category_name"])
            cat_label.set_opacity(0.6)
            top_row.pack_end(cat_label, False, False, 0)

        card.pack_start(top_row, False, False, 0)

        # Description
        desc_label = Gtk.Label(label=item["description"])
        desc_label.get_style_context().add_class("description-label")
        desc_label.set_halign(Gtk.Align.START)
        desc_label.set_line_wrap(True)
        desc_label.set_max_width_chars(80)
        desc_label.set_selectable(True)
        card.pack_start(desc_label, False, False, 0)

        # Example
        example_label = Gtk.Label(label="Example:")
        example_label.get_style_context().add_class("example-label")
        example_label.set_halign(Gtk.Align.START)
        card.pack_start(example_label, False, False, 0)

        example_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        example_box.get_style_context().add_class("example-box")

        example_text = Gtk.Label(label=item["example"])
        example_text.set_halign(Gtk.Align.START)
        example_text.set_selectable(True)
        example_box.pack_start(example_text, False, False, 0)

        # Copy button
        copy_btn = Gtk.Button.new_from_icon_name("edit-copy", Gtk.IconSize.SMALL_TOOLBAR)
        copy_btn.set_tooltip_text("Copy to clipboard")
        copy_btn.set_relief(Gtk.ReliefStyle.NONE)
        copy_btn.connect("clicked", self.on_copy_clicked, item["command"])
        example_box.pack_end(copy_btn, False, False, 0)

        card.pack_start(example_box, False, False, 0)

        # Tags
        if item.get("tags"):
            tags_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
            tags_box.get_style_context().add_class("tags-box")

            for tag in item["tags"]:
                tag_label = Gtk.Label(label=tag)
                tag_label.get_style_context().add_class("tag")
                tags_box.pack_start(tag_label, False, False, 0)

            card.pack_start(tags_box, False, False, 0)

        return card

    def highlight_text(self, text, query):
        """Highlight matching text"""
        if not query:
            return GLib.markup_escape_text(text)

        try:
            if self.regex_check.get_active():
                pattern = query
            else:
                pattern = re.escape(query)

            flags = 0 if self.case_check.get_active() else re.IGNORECASE

            def replacer(match):
                return f'<span background="#f9e2af" foreground="#1e1e2e">{GLib.markup_escape_text(match.group())}</span>'

            escaped = GLib.markup_escape_text(text)
            return re.sub(pattern, replacer, escaped, flags=flags)
        except:
            return GLib.markup_escape_text(text)

    def show_items(self, items, highlight=None):
        """Display items in the content area"""
        # Clear current items
        for child in self.items_box.get_children():
            self.items_box.remove(child)

        if not items:
            no_results = Gtk.Label(label="No matching commands found.\nTry a different search term or category.")
            no_results.get_style_context().add_class("no-results")
            self.items_box.pack_start(no_results, True, True, 0)
        else:
            for item in items:
                widget = self.create_item_widget(item, highlight)
                self.items_box.pack_start(widget, False, False, 0)

        self.items_box.show_all()
        self.update_status(len(items))

    def show_all_categories(self):
        """Show all items from all categories"""
        self.current_category = None
        self.content_header.set_text("All Commands")
        self.content_desc.set_text("Browse all Claude Code commands and shortcuts")

        # Reset active states
        self.all_button.get_style_context().add_class("active")
        for btn in self.category_buttons.values():
            btn.get_style_context().remove_class("active")

        # Apply current type filter
        self.apply_filters()

    def show_category(self, category):
        """Show items from a specific category"""
        self.current_category = category
        self.content_header.set_text(category["name"])
        self.content_desc.set_text(category["description"])

        # Update active states
        self.all_button.get_style_context().remove_class("active")
        for name, btn in self.category_buttons.items():
            if name == category["name"]:
                btn.get_style_context().add_class("active")
            else:
                btn.get_style_context().remove_class("active")

        # Apply current type filter
        self.apply_filters()

    def apply_filters(self):
        """Apply both category and type filters"""
        # Get base items
        if self.current_category:
            items = [
                {**item, "category_name": self.current_category["name"]}
                for item in self.current_category["items"]
            ]
        else:
            items = self.all_items

        # Apply type filter
        active_type = None
        for type_name, btn in self.type_filters.items():
            if btn.get_active() and type_name != "All":
                active_type = type_name
                break

        if active_type:
            items = [i for i in items if i["type"] == active_type]

        # Apply search
        query = self.search_entry.get_text().strip()
        if query:
            items = self.search_items(items, query)
            self.show_items(items, query)
        else:
            self.show_items(items)

    def search_items(self, items, query):
        """Search items with advanced options"""
        results = []

        try:
            if self.regex_check.get_active():
                pattern = query
            else:
                pattern = re.escape(query)

            flags = 0 if self.case_check.get_active() else re.IGNORECASE
            regex = re.compile(pattern, flags)

            for item in items:
                # Search in command, description, example, and tags
                searchable = [
                    item["command"],
                    item["description"],
                    item["example"],
                    " ".join(item.get("tags", []))
                ]

                if any(regex.search(text) for text in searchable):
                    results.append(item)
        except re.error:
            # Invalid regex, fall back to simple search
            query_lower = query.lower()
            for item in items:
                searchable = f"{item['command']} {item['description']} {item['example']} {' '.join(item.get('tags', []))}"
                if query_lower in searchable.lower():
                    results.append(item)

        return results

    def on_show_all(self, button):
        self.search_entry.set_text("")
        self.show_all_categories()

    def on_category_selected(self, button, category):
        self.search_entry.set_text("")
        self.show_category(category)

    def on_type_filter(self, button, type_name):
        # Handle toggle logic - only one can be active
        if button.get_active():
            button.get_style_context().add_class("active")
            for name, btn in self.type_filters.items():
                if name != type_name and btn.get_active():
                    btn.set_active(False)
                    btn.get_style_context().remove_class("active")
        else:
            button.get_style_context().remove_class("active")
            # If nothing selected, select "All"
            any_active = any(btn.get_active() for btn in self.type_filters.values())
            if not any_active:
                self.type_filters["All"].set_active(True)
                self.type_filters["All"].get_style_context().add_class("active")

        self.apply_filters()

    def on_search_changed(self, widget):
        self.apply_filters()

    def on_search_activate(self, widget):
        # Focus first result if any
        children = self.items_box.get_children()
        if children:
            children[0].grab_focus()

    def on_copy_clicked(self, button, text):
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(text, -1)
        self.statusbar.push(0, f"Copied: {text}")

    def on_key_press(self, widget, event):
        # Ctrl+F to focus search
        if event.state & Gdk.ModifierType.CONTROL_MASK:
            if event.keyval == Gdk.KEY_f:
                self.search_entry.grab_focus()
                return True
            elif event.keyval == Gdk.KEY_q:
                Gtk.main_quit()
                return True

        # Escape to clear search
        if event.keyval == Gdk.KEY_Escape:
            if self.search_entry.get_text():
                self.search_entry.set_text("")
                return True

        return False

    def update_status(self, count=None):
        if count is None:
            count = len(self.all_items)

        category = self.current_category["name"] if self.current_category else "All"
        query = self.search_entry.get_text().strip()

        status = f"Showing {count} items"
        if query:
            status += f" matching '{query}'"
        status += f" | Category: {category}"
        status += " | Ctrl+F: Search | Ctrl+Q: Quit"

        self.statusbar.push(0, status)


def main():
    app = ClaudeCodeReferenceApp()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
