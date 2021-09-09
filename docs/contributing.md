## Development and Contributing

## Issue

To make an improvement, add a new feature or anything else, please open a issue first.

**Good first issues are the issues that you can quickly solve, we recommend you take a
look.**
[Good first issue](https://github.com/hakancelik96/unimport/labels/good%20first%20issue)

## Fork Repository

[fork the unimport.](https://github.com/hakancelik96/unimport/fork)

## Clone Repository

```shell
$ git clone git@github.com:<USERNAME>/unimport.git
$ cd unimport
```

## Setup Branch

```shell
git checkout -b i{your issue number}
```

## How to Update My Local Repository

```shell
$ git remote add upstream git@github.com:hakancelik96/unimport.git
$ git fetch upstream # or git fetch --all
$ git rebase upstream/master
```

## Testing

Firstly make sure you have py3.6, py3.7, and py3.8 python versions installed on your
system.

After typing your codes, you should run the tests by typing the following command.

```shell
$ python3.8 -m pip install tox
$ tox
```

If all tests pass.

## The final step

After adding a new feature or fixing a bug please report your change to
[CHANGELOG.md](changelog.md) and write your name, GitHub address, and email in the
[AUTHORS.md](authors.md) file in alphabetical order.

### Changelog Guide

```
## [Unreleased] - ././2021

- [{Use the emoji below that suits you.} {Explain the change.} @{Add who solved the issue.}]({Add PR link})

{You can provide more details or examples if you wish.}

```

### Commit Messages

If you want, you can use the emoji about the commit message you will throw, this can
help us better understand the change you have made and also it is fun.

- When you make any support commit; 💪
- When you make any tests commit; 🧪
- When you make any fix commit; 🐞
- When you make any optimization commit; 💊
- When you make any new feature commit; 🔥
- When you make any drop or delete existing feature; 👎

## License

Unimport is MIT licensed, as found in the LICENSE file.
