# Contributing to Olist ETL Project

We welcome contributions to the Olist ETL Project! This document provides guidelines for contributing to this data engineering project.

## How to Contribute

### 1. Fork the Repository
- Fork the repository to your GitHub account
- Clone your fork locally: `git clone https://github.com/your-username/Olist_ETL_Project.git`
- Add the upstream repository: `git remote add upstream https://github.com/Y0U5F/Olist_ETL_Project.git`

### 2. Create a Feature Branch
- Create a new branch for your feature: `git checkout -b feature/your-feature-name`
- Use descriptive branch names that explain the purpose of your changes

### 3. Make Your Changes
- Follow the existing code style and conventions
- Add tests for new functionality
- Update documentation as needed
- Ensure all tests pass

### 4. Commit Your Changes
- Write clear, descriptive commit messages
- Follow conventional commit format: `type(scope): description`
- Example: `feat(dbt): add new customer dimension`

### 5. Push and Create Pull Request
- Push your branch: `git push origin feature/your-feature-name`
- Create a Pull Request from your branch to the main repository
- Provide a clear description of your changes

## Development Setup

### Prerequisites
- Python 3.9+
- Docker and Docker Compose
- Git
- Snowflake account (for testing)
- PostgreSQL (for local development)

### Local Development Environment
1. Clone the repository
2. Copy `.env.example` to `.env` and fill in your credentials
3. Start the services: `docker-compose up -d`
4. Access Airflow at `http://localhost:8080`

### Testing dbt Models
```bash
cd dbt_project/olist_dbt_project
dbt debug
dbt run
dbt test
```

## Code Style Guidelines

### Python
- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Add docstrings for all functions and classes
- Use meaningful variable names

### SQL (dbt)
- Use descriptive table and column names
- Add comments for complex transformations
- Follow the existing naming conventions
- Use proper indentation and formatting

### YAML
- Use consistent indentation (2 spaces)
- Add comments for complex configurations
- Follow the existing structure

## Testing

### Running Tests
- Run Python tests: `pytest`
- Run dbt tests: `dbt test`
- Run data quality tests in the pipeline

### Writing Tests
- Add unit tests for new functions
- Add integration tests for data pipelines
- Test edge cases and error conditions

## Documentation

### Update Documentation
- Update README.md for significant changes
- Add inline comments for complex code
- Update CHANGELOG.md for new features

### Docstring Format
```python
def your_function(param1: str, param2: int) -> str:
    """
    Brief description of the function.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ExceptionType: When and why this exception is raised
    """
```

## Pull Request Process

### Before Submitting
- Ensure all tests pass
- Update documentation
- Check for code style issues
- Test your changes thoroughly

### PR Description
- Provide a clear title and description
- Explain the purpose of your changes
- Reference any related issues
- Include screenshots if applicable

### Review Process
- Address reviewer feedback promptly
- Make requested changes
- Keep the PR focused on a single feature/fix

## Issue Reporting

### Bug Reports
- Use the bug report template
- Provide detailed steps to reproduce
- Include error messages and stack traces
- Specify your environment (OS, Python version, etc.)

### Feature Requests
- Use the feature request template
- Explain the use case and benefits
- Provide examples if possible

## Community Guidelines

- Be respectful and inclusive
- Use welcoming and inclusive language
- Be collaborative
- Focus on what is best for the community

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the original project (MIT License).