# Contributing

Setting up a local development environment needs [uv](https://docs.astral.sh/uv/),
[just](https://just.systems/), Node.js and Chrome:

```shell
git clone https://github.com/anze3db/selenium-testing-library.git && cd selenium-testing-library
just sync      # install the dev dependencies and bundle Testing Library (main.js)
just test      # run the tests in headless Chrome
just test-all  # run the tests on every supported Python
just check     # lint and test, as CI does
```

Releases are described in [RELEASING.md](RELEASING.md).

For any questions please feel free to reach out to me at anze@pecar.me
