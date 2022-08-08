Once you have [pre-commit](https://pre-commit.com/)
[installed](https://pre-commit.com/#install), adding pre-commit plugins to your project
is done with the .pre-commit-config.yaml configuration file.

Add a file called .pre-commit-config.yaml to the root of your project. The pre-commit
config file describes what repositories and hooks are installed.

```yaml
repos:
  - repo: https://github.com/hakancelikdev/unimport
    rev: stable
    hooks:
      - id: unimport
        args: [--remove, --include-star-import, --ignore-init, --gitignore]
```
