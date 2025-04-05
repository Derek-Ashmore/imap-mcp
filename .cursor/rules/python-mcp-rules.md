# Python MCP Server Rules

## Project Scope
- Python files (*.py)
- Configuration files (*.env, *.yml, *.yaml)
- Documentation (*.md)

## Code Style
- Follow PEP 8 guidelines
- Use type hints for function parameters and return values
- Maximum line length: 100 characters
- Use 4 spaces for indentation
- Use double quotes for strings
- Use snake_case for function and variable names
- Use PascalCase for class names

## Documentation
- All functions and classes must have docstrings
- Use Google-style docstring format
- Include type information in docstrings
- Document all parameters and return values
- Include examples for complex functions

## Security
- Never commit sensitive information (credentials, API keys)
- Use environment variables for configuration
- Validate all user input
- Handle exceptions appropriately
- Log security-related events

## Testing
- Write unit tests for all functions
- Use pytest for testing
- Maintain minimum 80% test coverage
- Mock external services in tests

## Error Handling
- Use specific exception types
- Include meaningful error messages
- Log errors with appropriate context
- Handle network-related exceptions gracefully

## Logging
- Use Python's logging module
- Include appropriate log levels
- Log all important operations
- Include context in log messages

## Dependencies
- Keep requirements.txt up to date
- Specify version numbers for dependencies
- Document dependency purposes
- Use virtual environments

## Code Organization
- One class per file
- Group related functionality
- Use meaningful file names
- Keep files focused and concise

## Performance
- Optimize database queries
- Use appropriate data structures
- Minimize network calls
- Cache when appropriate

## Maintenance
- Regular dependency updates
- Code cleanup and refactoring
- Documentation updates
- Security patches 