# Python BDD Test Automation Project

A Python-based test automation project using Behave for BDD (Behavior Driven Development) test management and Allure for test report generation.

# Project requires Python 3.12

## Project Structure

```
python-bdd/
├── allure-results/          # Allure test results
├── allure-report/           # Allure generated HTML reports
├── config/                  # Configuration files directory
│   ├── test.json            # Test environment configuration
│   ├── dev.json             # Development environment configuration
│   └── config.py            # Configuration management module
├── features/                # Behave feature files
│   ├── account.feature      # Account-related features
│   ├── environment.py       # Behave environment configuration
│   └── steps/               # Step definitions
├── common/                  # Common modules
│   ├── database/            # Database management
│   ├── dto/                 # Data transfer objects
│   └── utils/               # Utility classes
└── readme.md                # Project documentation
```

## Dependency Installation

```bash
pip install -r requirements.txt

# Export dependencies
pip freeze > requirements.txt
```

Or if requirements.txt doesn't exist yet:

```bash
pip install behave requests allure-behave loguru redis
```

## Behave Test Execution

### Basic Commands

```bash
# Run all feature files
behave

# Run specific feature file
behave features/account.feature

# Run specific scenario (by line number)
behave features/account.feature:9

# Specify environment configuration
behave features/account.feature -D profile=dev

# Verbose output
behave -v

# Show step definitions
behave --format=pretty
```

### Allure Report Integration
# Run tests and generate Allure results
```bash
behave features/account.feature -D profile=test -f allure_behave.formatter:AllureFormatter -o ./allure-results
```

```bash
# Generate visual report
allure generate ./allure-results -o ./allure-report
```

```bash
# Open report
allure open ./allure-report
```

```bash
# Clean old results and regenerate report
allure generate ./allure-results -o ./allure-report --clean
```

```bash
# Install and run parallel tests
pip install behave-parallel
behave-parallel -n 4 -f progress2 features/

```

## Configuration

Project uses configuration files to manage settings for different environments:

- `config/test.json` - Test environment configuration
- `config/dev.json` - Development environment configuration
- `config/config.py` - Configuration management module

### Configuration File Format

```json
{
    "REDIS_HOST": "localhost",
    "REDIS_PORT": 6379,
    "REDIS_DB": 0,
    "base_url": "https://api.example.com"
}
```

### Environment Switching

Switch between different environments using Behave's `-D profile=` parameter:

```bash
# Use test environment configuration
behave features/account.feature

# Use development environment configuration
behave features/account.feature -D profile=dev
```

## Key Features

- BDD Behavior Driven Testing (Behave)
- Allure Report Integration
- Redis Database Integration
- Multi-environment Configuration Management
- Automated Test Workflow

## Test Development Standards

### Feature Files (.feature)
- Use Chinese to describe business scenarios
- Follow Given-When-Then format
- Scenario descriptions should be specific and clear

### Step Definitions (steps/*.py)
- Step functions use decorators: @given, @when, @then
- Function names should match step descriptions
- Pass data through context object

### Environment Configuration (environment.py)
- before_all: Global initialization
- before_scenario: Scenario initialization
- after_scenario: Scenario cleanup
