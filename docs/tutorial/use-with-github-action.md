You can use stable version

```yaml
name: Unimport
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3.5.3
      - uses: actions/setup-python@v4.6.1
      - name: Check unused imports
        uses: hakancelikdev/unimport@stable
        with:
          extra_args: --include src/
```

or you can use a specific version if you want.

```yaml
name: Unimport
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3.5.3
      - uses: actions/setup-python@v4.6.1
      - name: Check unused imports
        uses: hakancelikdev/unimport@1.1.0
        with:
          extra_args: --include src/
```
