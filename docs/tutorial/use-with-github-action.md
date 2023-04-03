You can use stable version

```yaml
name: Unimport
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v3
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
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v3
      - name: Check unused imports
        uses: hakancelikdev/unimport@0.16.0
        with:
          extra_args: --include src/
```
