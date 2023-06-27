# Contributing

Setting up a local development environment:

```shell
git clone https://github.com/anze3db/selenium-testing-library.git && cd selenium-testing-library
poetry install && poetry shell
# Make sure `chromedriver` is in your PATH, download from https://chromedriver.chromium.org/downloads
# run tests:
pytest --selenium-headless
# run tests and display coverage info:
pytest --selenium-headless --cov=selenium_testing_library --cov-report html

# To test on multiple Python versions make sure that py38, py39, 310, 311, 312 are
# installed on your system and available through python3.8,
# python3.9, python3.10, python3.11, python3.12. (Use pyenv and add the pyenv shims to your path
# `export PATH=$(pyenv root)/shims:$PATH`). Then run tox:
tox
```

For any questions please feel free to reach out to me at anze@pecar.me
