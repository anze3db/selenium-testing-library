# Changelog

## 2024.3

- Testing Library upgraded to [v10.0.0](https://github.com/testing-library/dom-testing-library/releases/tag/v10.0.0)

## 2024.2
- Fix FileNotFoundError: No such file or directory

## 2024.1
- Testing Library upgraded to [v9.3.4](https://github.com/testing-library/dom-testing-library/releases/tag/v9.3.4)
- Add Python 3.13 support

## 2023.7
- Testing Library upgraded to [v9.3.3](https://github.com/testing-library/dom-testing-library/releases/tag/v9.3.3)
- Dependency updates
- Minor README.md file improvements

## 2023.6
- Drop Python 3.7 support

## 2023.5
- Add Python 3.12 support
- Testing Library upgraded to [v9.3.1](https://github.com/testing-library/dom-testing-library/releases/tag/v9.3.1)
## 2023.4
- Testing Library upgraded to [v9.3.0](https://github.com/testing-library/dom-testing-library/releases/tag/v9.3.0)
## 2023.3
- Testing Library upgraded to [v9.2.0](https://github.com/testing-library/dom-testing-library/releases/tag/v9.2.0)
- Dev tooling improvemetns (add ruff, remove isort)
- Dev dependency updates

## 2023.2
- Testing Library upgraded to [v9.0.0](https://github.com/testing-library/dom-testing-library/releases/tag/v9.0.0)
- **BREAKING** The `exact` parameter for `ByRole` selectors has been removed. This is because the exact parameter [was also removed in Testing Library 9.0.0](https://github.com/testing-library/dom-testing-library/pull/1211).
- Dev dependency updates
## 2023.1
- Add `screen.log_testing_playground_url()` for debugging with [testing-playground](https://testing-playground.com/)
- Dev dependency updates

## 2022.13
- Update @testing-library/dom to [8.19.1](https://github.com/testing-library/dom-testing-library/releases/tag/v8.19.1)
- Dev dependency updates

## 2022.12
- First stable release! 🎉
- No other notable changes in this release

## 2022.11b0
- Fix bug on iOS where WebDriverException is raised instead of JavascriptException

## 2022.10b0
- Add helper functions for missing selenium locators (`id`, `name`, `tag_name`, `link_text`, `partial_link_text`, `class_name`)
- Make timeout and frequency keyword only arguments

## 2022.9b0
- Add `typing-extensions` to the requirements
- README improvements

## 2022.8b0
- Additional parameters `selector`, `ignore` have been added to the Text Locator and screen functions
- Additional parameter `selector` has been added to the LabelText Locator and screen functions
- Additional parameters `hidden`, `description`, `selected`, and others have been added to the Role Locator and screen functions
- `exact` and other parameters for Locators and and screen functions are now keyword only arguments
- `*_by_placeholder_text` screen functions' first parameter was renamed from `value` to `text`
- `*_by_alt_text` screen functions' first parameter was renamed from `value` to `text`
- `*_by_alt_text` screen functions' first parameter was renamed from `value` to `text`
- `*_by_title` screen functions' first parameter was renamed from `value` to `title`
- `*_by_test_id` screen functions' first parameter was renamed from `value` to `text`

This should be the last pre-release and there should be no more breaking changes like this anymore. 🤞

## 2022.7b0
- Fix packaging issue

## 2022.6b0
- Use [@testing-library/dom](https://www.npmjs.com/package/@testing-library/dom) under the hood for all Testing Library queries. (This resolves [Issue #10](https://github.com/anze3db/selenium-testing-library/issues/10))
- Remove `find_elements`, `_exact_or_not`, `_escape_selector` functions from all `Locator` classes (these were not indended to be public API).
- Dependency updates

## 2022.5b0
- Fix bug with text and label locators (thanks [@KonradMar](https://github.com/KonradMar)!) [#75](https://github.com/anze3db/selenium-testing-library/pull/75)
- GitHub Action updates

## 2022.4b0
- Add Python 3.11 to the list of supported versions in the README
- Dependency updates

## 2022.3b0

- Add Python 3.11 support
- Dependency updates

## 2022.2b0

- Link to Changelog from PyPI
- Dependency updates

## 2022.1b0

- Drop Python 3.6 support
- Dependency updates
- Simplified versioning
- Added the Changelog
