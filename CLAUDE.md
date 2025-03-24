# Claude Agent Instructions

## Project Description
We are building a langchain-based chatbot app that gives advice on building GivingTuesday campaigns. Advice will come partly from the descriptions of successful GvingTuesday campaigns listed in `data/case-study-inventory.csv`. The project should use a mix of inexpensive Ais for initial processing, and expensive reasoning models. We will need to add additional datasources when they become available. The project should be well-documented and built in a way that enables easy extension. Use up to date versions of all relevant libraries.  First build a command-line version of the tool, and then a simple web application that can be run locally and accessed through a browser. The project will eventually be extended with additional feature and design constraints.

## Build Commands
- No formal build process is currently defined
- For data processing, use: `python process_data.py` (when implemented)

## Lint and Formatting
- Python: Use black for formatting (`black .`)
- CSV data: Validate with `csvlint data.csv` (requires csvlint gem)

## Test Commands
- Run all tests: `pytest`
- Run single test: `pytest tests/test_file.py::test_function`

## Code Style Guidelines
- Follow PEP 8 for Python code
- Use type hints for all function parameters and return values
- Use descriptive variable names in snake_case
- Group imports: standard library, third-party, local
- Handle errors explicitly with try/except blocks
- Document functions with docstrings
- Prefer immutable data structures when possible
- CSV data should maintain consistent column ordering

## Project Structure
- Keep data files in `/data` directory
- Place processing scripts in project root
- Use `/tests` for all test files
