# Nationwide Balance Viewer - Design

## Architecture Overview

### System Components
- **CLI Application**: Python-based command-line interface
- **Authentication Module**: Selenium-based browser automation with MFA support
- **Session Manager**: Secure cookie/session persistence
- **Web Scraper**: HTML parsing for balance extraction
- **Security Layer**: Credential encryption and anti-detection measures

### Technology Stack
- **Language**: Python 3.11 (required)
- **Environment**: Virtual environment (venv) for isolation
- **Browser Automation**: Selenium WebDriver with Chrome/Firefox
- **HTTP Client**: requests library with session persistence
- **CLI Framework**: click
- **HTML Parsing**: BeautifulSoup4
- **Encryption**: cryptography library
- **Anti-Detection**: undetected-chromedriver, random delays

## Research Findings & Authentication Strategy

### POC Analysis Results
After researching multiple approaches, the following findings emerged:

**Open Banking API**: Requires FCA TPP authorization and eIDAS certificates - not viable for personal use.

**Web Scraping**: Nationwide returns 403 status, indicating strong anti-bot protection with:
- CAPTCHA challenges
- Device fingerprinting
- Multi-factor authentication requirements
- Rate limiting and IP blocking

**Recommended Approach**: Hybrid browser automation with user interaction for MFA.

### Authentication Flow (Updated)

```
User Launch → Browser Automation → Login Form → MFA Prompt → Session Storage
     │              │                   │           │              │
     ▼              ▼                   ▼           ▼              ▼
[CLI Start] → [Selenium Launch] → [Credentials] → [User MFA] → [Cookie Store]
     │              │                   │           │              │
     └──────────────┴───────────────────┴───────────┴──────────────┘
                                   │
                                   ▼
                            [Authenticated Session]
```

## Component Interactions (Updated)

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   CLI Interface │────│ Browser Manager  │────│ Session Storage │
│                 │    │ (Selenium)       │    │ (Encrypted)     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Account Manager │────│ Web Scraper      │────│ Anti-Detection  │
│                 │    │ (BeautifulSoup)  │    │ Layer           │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Balance Display │    │ MFA Handler      │    │ Error Recovery  │
│                 │    │ (User Prompt)    │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Anti-Detection Measures

### Browser Fingerprinting Evasion
- Use undetected-chromedriver to avoid detection
- Randomize user agent strings
- Disable automation indicators
- Implement realistic mouse movements and typing delays

### Rate Limiting Protection
- Random delays between requests (2-5 seconds)
- Respect robots.txt guidelines
- Implement exponential backoff on errors
- Use residential proxy rotation if needed

### Session Management
- Persist browser cookies securely
- Implement session validation before each request
- Handle session expiry gracefully
- Clear sensitive data on application exit

## Data Models

### Account Model
```python
@dataclass
class Account:
    account_id: str
    account_name: str
    account_type: str
    sort_code: str
    account_number: str
```

### Balance Model
```python
@dataclass
class Balance:
    account_id: str
    current_balance: Decimal
    available_balance: Decimal
    currency: str = "GBP"
    last_updated: datetime
```

## Implementation Strategy (Updated)

### Browser Automation Approach
- **Login Process**: Selenium WebDriver automation
- **MFA Handling**: Pause for user interaction (SMS/app authentication)
- **Session Persistence**: Save authenticated browser cookies
- **Balance Extraction**: Parse HTML using BeautifulSoup
- **Anti-Detection**: Use undetected-chromedriver with realistic delays

### Error Handling Strategy
- **Detection Avoidance**: Implement human-like behavior patterns
- **CAPTCHA Handling**: Pause for manual user resolution
- **Authentication Failures**: Clear session, restart browser automation
- **Network Issues**: Retry with exponential backoff
- **Parsing Errors**: Robust HTML parsing with fallback selectors

## Security Considerations (Updated)

### Credential Storage
- Store only session cookies, never passwords
- Encrypt session data using Fernet encryption
- Use system keyring for encryption key storage
- Implement automatic session cleanup

### Privacy & Compliance
- No credential logging or storage
- Respect Nationwide's terms of service
- Implement user consent for automation
- Clear browser data on exit

## File Structure (Updated)
```
NationwideAPI/
├── .git/                   # Git repository (initialized)
├── .gitignore              # Git ignore file
├── Makefile                # Build and management automation
├── README.md               # Project documentation
├── venv/                   # Virtual environment (created by make setup)
├── settings.ini.template   # Configuration template
├── settings.ini            # User configuration (git ignored)
├── src/
│   ├── __init__.py
│   ├── cli.py              # Main CLI interface
│   ├── browser_manager.py  # Selenium automation
│   ├── scraper.py          # HTML parsing and data extraction
│   ├── session_manager.py  # Cookie/session persistence
│   ├── models.py           # Data models
│   ├── security.py         # Encryption utilities
│   ├── anti_detection.py   # Bot detection evasion
│   └── config.py           # Configuration management
├── tests/
├── requirements.txt        # All dependencies
├── setup.py
└── poc_*.py               # POC files (can be removed after development)
```

## Development Environment Setup

### Prerequisites
- **Python 3.11** (required for compatibility)
- **Chrome/Chromium browser** (for Selenium WebDriver)
- **Make** (for build automation)
- **Git** (for version control)

### Quick Start with Makefile
```bash
# Initialize project (one-time setup)
make init          # Initialize git repository and create .gitignore

# Setup development environment
make setup         # Create venv, install dependencies, copy settings template

# Configure application
cp settings.ini.template settings.ini
# Edit settings.ini with your preferences

# Run application
make run           # Activate venv and run the CLI

# Development tasks
make test          # Run tests
make clean         # Clean build artifacts
make help          # Show all available commands
```

### Manual Installation Steps (Alternative)
```bash
# 1. Initialize git repository
git init
echo "settings.ini" >> .gitignore
echo "venv/" >> .gitignore
echo "__pycache__/" >> .gitignore

# 2. Create virtual environment
python3.11 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# 4. Install dependencies
pip install -r requirements.txt

# 5. Setup configuration
cp settings.ini.template settings.ini
# Edit settings.ini as needed

# 6. Run application
python -m src.cli
```

### Makefile Targets
```makefile
# Primary targets
init:              # Initialize git repository and .gitignore
setup:             # Create venv and install dependencies
run:               # Run the application
test:              # Run test suite
clean:             # Clean build artifacts and cache

# Development targets
dev-setup:         # Setup with development dependencies
lint:              # Run code linting
format:            # Format code
install:           # Install package in development mode
```

### Requirements.txt Dependencies
```txt
selenium>=4.15.0
undetected-chromedriver>=3.5.0
beautifulsoup4>=4.12.0
requests>=2.31.0
click>=8.1.0
cryptography>=41.0.0
keyring>=24.0.0
python-dotenv>=1.0.0
```

## Configuration Management

### Settings Files
- **settings.ini.template**: Version-controlled template with default values
- **settings.ini**: User-specific configuration (git ignored)
- **Configuration loading**: Python-dotenv for .ini file parsing

### Settings Structure
```ini
[DEFAULT]
# Application settings
debug = false
log_level = INFO

[browser]
# Browser automation settings
headless = false
window_size = 1920x1080
user_data_dir = ~/.nationwide-cli/browser
timeout = 30

[security]
# Security and encryption settings
session_timeout = 1800
encryption_key_name = nationwide_cli_key
clear_on_exit = true

[nationwide]
# Nationwide-specific settings
base_url = https://onlinebanking.nationwide.co.uk
retry_attempts = 3
delay_min = 2
delay_max = 5
```

### Git Configuration
```gitignore
# User configuration
settings.ini

# Python
venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Application specific
*.log
.session_cache/
```

## Configuration Management (Updated)
- **settings.ini.template**: Version-controlled configuration template
- **settings.ini**: User-specific settings (git ignored)
- Browser preferences loaded from settings.ini
- Encrypted session storage in system keyring
- User preferences for MFA handling and timeouts
- Logging configuration for debugging (no sensitive data)
- Virtual environment isolation for dependency management

## Build and Deployment Management

### Makefile Automation
The project uses a top-level Makefile for streamlined development workflow:

```makefile
# Key features:
- Automatic venv creation and management
- Dependency installation from requirements.txt
- Git repository initialization
- Configuration file management
- Application execution with proper environment
- Testing and linting automation
- Clean build artifact removal
```

### Project Initialization Workflow
1. **Git Setup**: `make init` initializes repository and creates .gitignore
2. **Environment Setup**: `make setup` creates venv and installs dependencies
3. **Documentation**: README.md provides setup and usage instructions
4. **Configuration**: Copy and edit settings.ini from template
5. **Development**: Use `make run`, `make test`, etc. for daily workflow

### Version Control Strategy
- **Git repository**: Initialized locally (no remote initially)
- **Ignored files**: settings.ini, venv/, build artifacts
- **Tracked files**: All source code, templates, documentation, README.md
- **Configuration**: Template tracked, user settings ignored
- **Documentation**: README.md provides project overview and setup instructions

## Deployment Considerations

### Environment Isolation
- Use Python 3.11 virtual environment for all development and deployment
- Pin all dependencies in requirements.txt for reproducible builds
- Makefile ensures consistent environment setup across systems
- Separate development and production dependency sets if needed

### System Requirements
- Python 3.11+ (critical for modern async/await and security features)
- Chrome/Chromium browser (latest stable version)
- Make utility (for build automation)
- Git (for version control)
- Sufficient disk space for browser profile and session storage (~100MB)
- Network access to Nationwide's banking portal

### Development Workflow
1. Clone/initialize project: `make init`
2. Setup environment: `make setup`
3. Configure application: Edit `settings.ini`
4. Daily development: `make run`, `make test`
5. Clean environment: `make clean`

### Configuration Security
- User credentials never stored in version control
- settings.ini contains only application preferences
- Sensitive data (sessions, keys) stored in system keyring
- Template provides safe defaults for all settings
