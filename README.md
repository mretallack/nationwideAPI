# Nationwide Balance Viewer

A Python CLI tool for viewing Nationwide Building Society account balances through automated browser interaction.

## Features

- **Secure Authentication**: Browser automation with MFA support
- **Balance Viewing**: Display current and available balances
- **Multiple Accounts**: Support for customers with multiple accounts
- **Session Persistence**: Encrypted session storage to reduce login frequency
- **Anti-Detection**: Realistic human-like behavior to avoid bot detection

## Prerequisites

- **Python 3.11+** (required)
- **Chrome/Chromium browser** (latest stable version)
- **Make** (for build automation)
- **Git** (for version control)

## Quick Start

### 1. Setup Environment
```bash
# Clone the repository
git clone git@github.com:mretallack/nationwideAPI.git
cd nationwideAPI

# Setup development environment
make setup
```

### 2. Configure Application
```bash
# Copy configuration template
cp settings.ini.template settings.ini

# Edit settings.ini with your preferences
nano settings.ini
```

### 3. Run Application
```bash
# Run the balance viewer
make run
```

## Configuration

The application uses `settings.ini` for configuration. Key settings include:

### Browser Settings
- `headless`: Run browser in headless mode (true/false)
- `window_size`: Browser window dimensions
- `timeout`: Page load timeout in seconds

### Security Settings
- `session_timeout`: Session expiry time in seconds
- `clear_on_exit`: Clear session data on exit (true/false)

### Nationwide Settings
- `base_url`: Nationwide online banking URL
- `retry_attempts`: Number of retry attempts on failure
- `delay_min/max`: Random delay range between actions

## Usage

### View Account Balance
```bash
# View balance for default account
make run

# The application will:
# 1. Launch browser automation
# 2. Navigate to Nationwide login
# 3. Prompt for MFA if required
# 4. Display account balance(s)
# 5. Store session for future use
```

### Manual Authentication
If you need to re-authenticate or clear sessions:
```bash
# Clear stored sessions
rm -rf ~/.nationwide-cli/
```

## Development

### Available Make Commands
```bash
make help       # Show all available commands
make setup      # Create venv and install dependencies
make run        # Run the application
make test       # Run test suite
make clean      # Clean build artifacts
make dev-setup  # Setup with development tools
make lint       # Run code linting
make format     # Format code
```

### Project Structure
```
nationwideAPI/
├── src/                    # Main application code
│   ├── cli.py             # CLI interface
│   ├── browser_manager.py # Browser automation
│   ├── scraper.py         # Data extraction
│   ├── session_manager.py # Session persistence
│   ├── models.py          # Data models
│   ├── security.py        # Encryption utilities
│   ├── anti_detection.py  # Bot detection evasion
│   └── config.py          # Configuration management
├── tests/                 # Test suite
├── .kiro/specs/          # Project specifications
├── Makefile              # Build automation
├── requirements.txt      # Dependencies
└── settings.ini.template # Configuration template
```

## Security Considerations

- **No Password Storage**: Credentials are never stored locally
- **Session Encryption**: All session data is encrypted using system keyring
- **MFA Support**: Manual multi-factor authentication handling
- **Anti-Detection**: Realistic delays and behavior patterns
- **Clean Exit**: Automatic cleanup of sensitive data

## Troubleshooting

### Common Issues

**Browser Not Found**
```bash
# Install Chrome/Chromium
sudo apt install chromium-browser  # Ubuntu/Debian
brew install --cask google-chrome  # macOS
```

**Python Version Issues**
```bash
# Ensure Python 3.11+ is installed
python3.11 --version
```

**Permission Errors**
```bash
# Ensure proper permissions for browser profile directory
mkdir -p ~/.nationwide-cli/browser
chmod 755 ~/.nationwide-cli/browser
```

### Debug Mode
Enable debug logging by editing `settings.ini`:
```ini
[DEFAULT]
debug = true
log_level = DEBUG
```

## Legal Notice

This tool is for personal use only. Users must comply with Nationwide Building Society's terms of service. The authors are not responsible for any misuse or violations of terms of service.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `make test`
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the project specifications in `.kiro/specs/`
3. Open an issue on GitHub
