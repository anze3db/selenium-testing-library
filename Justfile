# selenium-testing-library's development tasks: `just` lists them. Everything runs through uv.

set shell := ["bash", "-euo", "pipefail", "-c"]
set positional-arguments

paths := "selenium_testing_library tests scripts"

# List the recipes
[private]
default:
    @just --list --unsorted

# Install Python and the dev dependencies, and bundle Testing Library
sync: js
    uv sync

# Bundle Testing Library into selenium_testing_library/main.js (the tests need it)
js:
    npm ci
    npm run build

# Run the tests; arguments go to pytest (`just test tests/test_selenium_testing_library.py -x`)
[group("test")]
test *args:
    uv run pytest "$@"

# Run the tests on another Python (`just test-on 3.11`)
[group("test")]
test-on python *args:
    uv run --isolated --python "{{ python }}" pytest "${@:2}"

# Run the tests on every Python CI tests
[group("test")]
test-all:
    #!/usr/bin/env bash
    set -euo pipefail
    for py in 3.11 3.12 3.13 3.14 3.15; do
        echo "── Python $py"
        just test-on "$py" -q
    done

# Lint and format check, as CI does
[group("check")]
lint:
    uv run ruff check {{ paths }}
    uv run ruff format --check {{ paths }}

# Format the code and apply ruff's safe fixes
[group("check")]
fmt:
    uv run ruff format {{ paths }}
    uv run ruff check --fix {{ paths }}

# Audit the GitHub workflows (zizmor, actionlint)
[group("check")]
lint-actions:
    uvx zizmor .github/workflows
    uvx --from actionlint-py actionlint

# Everything before a push: lint, then the tests
[group("check")]
check: lint test

# Preview the next release; `just release --no-dry-run` commits and pushes it, then waits for it
[group("release")]
release *args:
    #!/usr/bin/env bash
    set -euo pipefail
    commit=false
    rest=()
    for arg in "$@"; do
        if [[ $arg == --no-dry-run ]]; then commit=true; else rest+=("$arg"); fi
    done
    if $commit; then
        uv run scripts/release.py prepare ${rest[@]+"${rest[@]}"}
    else
        uv run scripts/release.py prepare --dry-run ${rest[@]+"${rest[@]}"}
        echo
        echo "That was a dry run. To release it: just release --no-dry-run"
        echo "(commits it, pushes it to main and waits until CI passes and it's published)"
    fi

# Remove build, coverage and cache output
clean:
    rm -rf dist htmlcov .coverage .coverage.* .pytest_cache .ruff_cache selenium_testing_library/main.js*
