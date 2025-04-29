# uv

## Environment Management:
1. `uv venv` - Create a virtual environment
2. `uv --version` - Check UV version
3. `uv cache dir` - Show cache directory location

## Build and Run:
1. `uv build` - Build the project
   - Variations: `uv build --wheel`, `uv build --all-packages`
2. `uv run [command]` - Run Python commands or scripts
   - Examples:
     - `uv run poe start`
     - `uv run poe lint`
     - `uv run poe format`
     - `uv run mypy .`
     - `uv run pylint .`

## Pip Operations:
1. `uv pip install` - Install packages using pip compatibility mode
   - Example: `uv pip install --no-cache-dir ./*.whl`