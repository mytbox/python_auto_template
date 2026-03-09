# Python BDD Test Automation Framework

A Python Behave-based Behavior Driven Development (BDD) test framework for test automation projects.

## Project Overview

This project uses the Behave framework to implement a BDD test automation solution. Business requirements and acceptance criteria are described through Feature Files written in Gherkin language.

## Project Structure

```
python-bdd/
├── features/                # BDD feature files
│   ├── readme.md            # This documentation file
│   └── *.feature            # Gherkin feature files
├── features/steps/          # Step definitions
│   └── *.py                 # Python step implementations
├── allure-results/          # Allure test results
├── allure-report/           # Allure generated HTML reports
├── common/                  # Common components
│   ├── database/            # Database management
│   ├── dto/                 # Data transfer objects
│   └── utils/               # Utility classes
├── config/                  # Configuration files
├── requirements.txt         # Dependency package list
```

## Environment Requirements

- Python 3.12 or higher
- pip package manager

## Installation Steps

### 1. Clone Project

```bash
git clone <repository-url>
cd python-bdd
```

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Main dependencies include:
- `behave==1.3.3` - BDD test framework
- `allure-behave==2.15.3` - Allure report integration
- `requests` - HTTP client library
- `loguru` - Logging library
- `redis` - Redis client

## Running Tests

### 1. Run All Behave Tests

```bash
# Basic run
behave

# Verbose output
behave -v

# Run specific feature file
behave features/jsonplaceholder_api.feature

# Run specific scenarios (by tags)
behave --tags=@smoke
behave --tags=@regression
```

### 2. Use Tag Expressions

Behave supports complex tag expressions, see documentation: https://behave.readthedocs.io/en/latest/tag_expressions/

```bash
# AND operation
behave --tags="@tag1 and @tag2"

# OR operation
behave --tags="@tag1 or @tag2"

# NOT operation
behave --tags="not @wip"

# Complex expressions
behave --tags="(@smoke or @regression) and not @slow"
```

## Feature Files

Feature files are written in Gherkin syntax and located in the `features/` directory:

```gherkin
Feature: Login Functionality
  As a user
  I want to be able to login to the application
  So that I can access my profile

  Scenario: Successful Login
    Given I am on the login page
    When I enter a valid email and password
    And I click the login button
    Then I should be redirected to the home page
    And I should see a welcome message
```

## Step Definitions

Step definitions are located in the `features/steps/` directory:

```python
from behave import given, when, then
from common.dto.scenario_context import ScenarioContext


@given('I am on the login page')
def step_impl(context):
    # Initialize scenario context
    context.scenario_context = ScenarioContext()


@when('I enter a valid email and password')
def step_impl(context):
    # Execute login operation
    pass


@then('I should be redirected to the home page')
def step_impl(context):
    # Verify login result
    assert context.scenario_context.apiToken is not None
```

## Allure Reports

### Generate Allure Reports

```bash
# Run tests and generate Allure results
behave --format=allure_behave.formatter:AllureFormatter --output-directory=./allure-results

# Generate HTML report
allure generate ./allure-results -o ./allure-report

# Open report
allure open ./allure-report
```

## Configuration

### Behave Configuration

Behave supports `behave.ini`, `setup.cfg` or `pyproject.toml` configuration files:

```ini
[behave]
show_timings = true
show_skipped = false
quiet = false
lang = en
format = pretty
color = true
```

### Environment Configuration

Test environment can be configured in the `environment.py` file:

```python
def before_all(context):
    # Set global configuration
    pass

def before_feature(context, feature):
    # Setup before feature starts
    pass

def after_scenario(context, scenario):
    # Cleanup after scenario ends
    pass
```

## Data Passing

In BDD tests, data is passed between steps through the context object:

```python
# Set data in step A
context.user_email = "test@example.com"

# Use data in subsequent steps
assert context.user_email == "test@example.com"
```

## Best Practices

1. **Clear Feature Descriptions**: Each feature file should focus on a single functionality
2. **Meaningful Scenario Names**: Scenario titles should clearly describe the test purpose
3. **Independent Scenarios**: Each scenario should be able to run independently
4. **Use Tags to Organize Tests**: Categorize different types of tests with tags (@smoke, @regression, @wip)
5. **Avoid Duplicate Steps**: Extract common steps to the Background section

## Common Questions

### Q: How to debug Behave tests?
A: Add `-D` parameter to enable debug mode:
```bash
behave -D
```

### Q: How to run only failed scenarios?
A: Use `--rerun` feature or tag filtering:
```bash
behave --tags="@failed"
```

### Q: How to set up test data?
A: Set global data in `environment.py` or use Given steps to prepare data in scenarios.

## Project Rules

```shell
Rules that must be followed for behave automation testing:
1. features directory contains behave automation test related files
2. steps directory contains behave automation test step definition files
3. environment.py file is the behave automation test configuration file
4. common is a common module that can be used by both behave and other frameworks.
5. config is the configuration file directory.
```

## Reference Resources

- [Behave Official Documentation](https://behave.readthedocs.io/)
- [Gherkin Syntax Guide](https://cucumber.io/docs/gherkin/)
- [Allure Report Documentation](https://docs.qameta.io/allure/)
- [Tag Expressions Documentation](https://behave.readthedocs.io/en/latest/tag_expressions/)
