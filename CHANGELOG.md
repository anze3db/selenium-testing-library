# Changelog

`selenium-testing-library` will be in pre-release until ~~[Issue #10](https://github.com/anze3db/selenium-testing-library/issues/10) is unresolved and~~ all gaps between [Testing Library Core Query APIs](https://testing-library.com/docs/queries/about) and the the selenium-testing-library APIs are removed.

## In development

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
