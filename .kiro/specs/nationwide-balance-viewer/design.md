# Nationwide Balance Viewer - Design

## Architecture Overview

### System Components
- **CLI Application**: Python-based command-line interface
- **Authentication Module**: Multi-mode browser automation (Chrome + headless)
- **Headless Browser**: JavaScript-capable requests-html with Chromium
- **Network Monitor**: Traffic capture and API discovery system
- **Session Manager**: Secure cookie/session persistence
- **API Client**: Direct JSON API communication (post-discovery)
- **Web Scraper**: HTML parsing fallback for balance extraction
- **Security Layer**: Credential encryption and anti-detection measures

### Technology Stack
- **Language**: Python 3.11 (required)
- **Environment**: Virtual environment (venv) for isolation
- **Browser Automation**: Dual approach - Selenium WebDriver + requests-html
- **Headless Browser**: requests-html with pyppeteer (Chromium)
- **Network Monitoring**: Selenium wire proxy + requests logging
- **HTTP Client**: requests library with session persistence
- **CLI Framework**: click
- **HTML Parsing**: BeautifulSoup4 + pyquery
- **JSON Processing**: Built-in json module with pretty printing
- **Encryption**: cryptography library
- **Anti-Detection**: undetected-chromedriver, random delays, realistic headers

## Key Discovery: Nationwide Login Process

### Actual Login Requirements (Discovered via Testing)
**Authentication Fields Required:**
1. **Customer Number**: Primary account identifier (e.g., 1234567890)
2. **Date of Birth Day**: Day of birth (1-31)
3. **Date of Birth Year**: Year of birth (YYYY format)

**Form Endpoints Discovered:**
- **Step 1**: `/AccessManagement/IdentifyCustomer/TemporaryCustomerLogin`
- **Step 2**: `/AccessManagement/IdentifyCustomer/EnterCustomerIdentificationDetail`

**Technical Requirements:**
- **JavaScript Execution**: Required for dynamic form loading
- **CSRF Tokens**: Multiple `__token` fields must be included
- **Hidden Fields**: TimeZoneOffset, LocalTime, ScreenResolution tracking
- **Session Management**: Cookies and form state persistence

### Headless Browser Success
**Proven Working Approach:**
- ✅ **requests-html** with automatic Chromium download
- ✅ **JavaScript execution** without Chrome installation
- ✅ **Form detection** and field analysis
- ✅ **Network traffic capture** for API discovery
- ✅ **Multi-step form handling** capability

## Research Findings & Authentication Strategy

### POC Analysis Results
After researching multiple approaches and testing with headless browser:

**Discovered Login Process**: Nationwide uses a multi-step authentication:
1. **Customer Number**: Primary identifier
2. **Date of Birth**: Secondary authentication (day + year)
3. **Multi-step forms**: `/TemporaryCustomerLogin` → `/EnterCustomerIdentificationDetail`
4. **CSRF Protection**: Multiple token fields required
5. **JavaScript Required**: Dynamic form loading and validation

**Browser Automation Results**:
- **Headless Browser**: ✅ WORKING - requests-html with Chromium
- **Form Detection**: ✅ Successfully identifies login forms and fields
- **JavaScript Execution**: ✅ Automatic Chromium download and execution
- **Network Capture**: ✅ Request/response logging functional
- **Chrome Selenium**: ⚠ Requires full Chrome installation

### Authentication Flow (Updated)

```
User Launch → Headless Browser → Navigate → Form Analysis → Multi-step Auth
     │              │               │           │              │
     ▼              ▼               ▼           ▼              ▼
[CLI Start] → [requests-html] → [JS Execute] → [Find Forms] → [Submit Data]
     │              │               │           │              │
     └──────────────┴───────────────┴───────────┴──────────────┘
                                   │
                                   ▼
                            [Authenticated Session]
```

## Component Interactions (Updated)

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   CLI Interface │────│ Browser Manager  │────│ Network Monitor │
│                 │    │ (Selenium)       │    │ (Traffic Capture)│
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Session Storage │────│ API Client       │────│ API Discovery   │
│ (Encrypted)     │    │ (JSON Requests)  │    │ (Endpoint Map)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Balance Display │────│ Web Scraper      │────│ Anti-Detection  │
│                 │    │ (HTML Fallback)  │    │ Layer           │
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

### Dual-Mode Browser Approach
- **Primary Mode**: Headless browser using requests-html with Chromium
  - No Chrome installation required
  - Automatic JavaScript execution
  - Built-in network traffic capture
  - Suitable for server environments
- **Secondary Mode**: Full Chrome browser with Selenium
  - Complete browser features and debugging
  - Advanced anti-detection capabilities
  - Manual MFA handling support
  - Suitable for development environments

### Multi-Step Authentication Process
1. **Navigate**: to `/AccessManagement/IdentifyCustomer/IdentifyCustomer`
2. **Form Detection**: Identify TemporaryCustomerLogin vs EnterCustomerIdentificationDetail
3. **Credential Input**: Customer Number + Date of Birth (day + year)
4. **CSRF Handling**: Extract and include required token fields
5. **Session Management**: Maintain cookies and form state across steps

### Data Extraction Strategy
- **HTML Parsing**: Primary method using BeautifulSoup for balance extraction
- **API Discovery**: Monitor network traffic for JSON endpoints
- **Direct API Calls**: Switch to discovered APIs for better performance
- **Fallback Handling**: Graceful degradation when APIs change

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
│   ├── browser_manager.py  # Selenium automation (Chrome required)
│   ├── headless_browser.py # requests-html automation (no Chrome needed)
│   ├── network_monitor.py  # Traffic capture and API discovery
│   ├── api_client.py       # Direct JSON API communication
│   ├── scraper.py          # HTML parsing fallback
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

## Development Environment Setup

### Prerequisites
- **Python 3.11** (required for compatibility)
- **Chrome/Chromium browser** (optional - for full Selenium mode)
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
# Edit settings.ini with your customer number and date of birth

# Test headless browser (no Chrome needed)
make test-headless # Test navigation and form detection

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
selenium-wire>=5.1.0
blinker==1.7.0
undetected-chromedriver>=3.5.0
beautifulsoup4>=4.12.0
requests>=2.31.0
requests-html>=0.10.0
lxml_html_clean>=0.4.0
beautifulsoup4>=4.12.0
click>=8.1.0
cryptography>=41.0.0
keyring>=24.0.0
python-dotenv>=1.0.0
pytest>=7.4.0
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

[debugging]
# Development and API discovery settings
capture_traffic = false
save_requests = false
api_discovery_mode = false
request_log_file = ~/.nationwide-cli/requests.log
discovered_apis_file = ~/.nationwide-cli/discovered_apis.json

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

# Test data (real credentials/sessions)
tests/fixtures/real_*
tests/data/live_*
```

## Testing Strategy

### Test Categories
- **Unit Tests**: Individual component testing with mock data
- **Integration Tests**: Component interaction testing
- **API Discovery Tests**: Network monitoring and endpoint detection
- **Configuration Tests**: Settings loading and validation
- **Security Tests**: Encryption and credential handling

### Test Data Management
- **Mock Data**: Fake account/balance data for testing (committed to git)
- **Test Fixtures**: Sample HTML responses and JSON payloads (committed to git)
- **Live Data**: Real credentials/sessions (never committed, git ignored)
- **API Specifications**: Discovered endpoint documentation (committed to git)

### Committable Test Assets
```
tests/
├── fixtures/
│   ├── mock_login_page.html      # Sample login page HTML
│   ├── mock_balance_response.json # Sample balance API response
│   ├── mock_account_list.json    # Sample account list
│   └── mock_session_data.json    # Sample session structure
├── data/
│   ├── test_accounts.json        # Fake account data for testing
│   ├── api_endpoints.json        # Discovered API documentation
│   └── request_templates.json    # API request templates
└── unit/
    ├── test_models.py            # Data model tests
    ├── test_config.py            # Configuration tests
    ├── test_security.py          # Security utility tests
    └── test_api_discovery.py     # Network monitoring tests
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

### Git Workflow
- **Manual commits only**: Changes are not automatically committed
- **Explicit push requests**: Only push to remote when explicitly requested
- **Single push per request**: One push operation per explicit request
- **Developer control**: All version control operations require explicit instruction

### Configuration Security
- User credentials never stored in version control
- settings.ini contains only application preferences
- Sensitive data (sessions, keys) stored in system keyring
- Template provides safe defaults for all settings
