# Changelog

`selenium-testing-library` will be in pre-release until ~~[Issue #10](https://github.com/anze3db/selenium-testing-library/issues/10) is unresolved and~~ all gaps between [Testing Library Core Query APIs](https://testing-library.com/docs/queries/about) and the the selenium-testing-library APIs are removed.

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
