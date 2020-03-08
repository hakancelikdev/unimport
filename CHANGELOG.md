# Changelog
All notable changes to this project will be documented in this file.

## [0.2.1] - 8/March/2020
- from x import * support [issue; #19](https://github.com/hakancelik96/unimport/issues/19), [PR; #21](https://github.com/hakancelik96/unimport/pull/21) by @hakancelik96


## [0.2.0] - 19/Jan/2020

- Argparse support.
    - [implement an initial arg parser by @gkmngrgn](https://github.com/hakancelik96/unimport/commit/4e5fbd778112704626c8d708a1077d7d1f345157)
    - [argparse support by @gkmngrgn](https://github.com/hakancelik96/unimport/commit/837af61fab771b4a09893a7854df42452de7aff9)
    - [argparse (#4) by @isidentical](https://github.com/hakancelik96/unimport/commit/90cfab776d3e15b417d1566f7ca1b1e2756763dd)
    - Arguments
        - ["-w" / "--write" parameter is fixed in this PR (#9) by @gkmngrgn](https://github.com/hakancelik96/unimport/commit/5c59f938d3ef3844a5420882ad318a120e4da4af)
        - [#12 diff option & and overwrite permission add by @hakancelik96](https://github.com/hakancelik96/unimport/commit/36e7216cd6cc442864460d7b2b7661190c627757)
        - [#12 -dw add by @hakancelik96](https://github.com/hakancelik96/unimport/commit/57913e0fb47073f4473e5694470cc2ee9dffdfb6)
        - [#12 bug fix & Some functions have been moved to the corresponding files @hakancelik96](https://github.com/hakancelik96/unimport/commit/188370fc7928588a48e9e3dcd0ee70f9f12b733e)
        - [--version add by @hakancelik96](https://github.com/hakancelik96/unimport/commit/2112e44e45bc0b34e330bc5320bbcd1462257f1e)
        - [Console Argument (#17) by @hakancelik96](https://github.com/hakancelik96/unimport/commit/e4db14dbc74fbc8a51c5d1f62ca9d679af05af9b)



- Tests
    - [fix_multiple_problems_at_once_action.py by @hakancelik96](https://github.com/hakancelik96/unimport/commit/aee62041b2d625cef0d723c526d5db28d96ce2fd)
    - [test_overwrite source_expected path bug fix by @hakancelik96](https://github.com/hakancelik96/unimport/commit/63645dbb4333b3675e57bbc99bddfa133eb33594)

- Configuration
    - [example_configuration add by @hakancelik96](https://github.com/hakancelik96/unimport/commit/70c70ba0d5ac8f200986c5c0a57acc8ccc574dab)
    - [#8 & glob configuration by @hakancelik96](https://github.com/hakancelik96/unimport/commit/c8bd58e28855886c5908a626260820c3894a4600)
    - [ignore config name change as exclude by @hakancelik96](https://github.com/hakancelik96/unimport/commit/aef61eb3ddf0c295719dc840390fba16e3d5e3e9)
    - [remove .unimport.cfg by @hakancelik96](https://github.com/hakancelik96/unimport/commit/b052ffb336bc0f73a723f5f4938cb7ffb81cd038)
    - [find_config bug fix & console config argument bug fix by @hakancelik96](https://github.com/hakancelik96/unimport/commit/860d57791a36c54e1830439bf9e571b1cb608123)

- Lib2to3 support
    - [Initial lib2to3 refactor by @isidentical](https://github.com/hakancelik96/unimport/commit/9030cb2fea518aa9fb887a5d4ef1bb8b34947ed9)
    - [add support for name binding by @isidentical](https://github.com/hakancelik96/unimport/commit/4a3df83b5b89d00472bed292c23b20693bdf5dd2)
    - [adapt testing suite by @isidentical](https://github.com/hakancelik96/unimport/commit/c81036fe5b0d845c3220cfda1e4c30250e1107a1)

- Bug Fix
    - [setup.cfg bug fix & catch error in dedect by @hakancelik96](https://github.com/hakancelik96/unimport/commit/a99b3846d55b723a701d6fdbbc7e634772b8c5ba)
    - [get_files bug fix by @hakancelik96](https://github.com/hakancelik96/unimport/commit/3d3299f1c82161a8e95d909864ad00dd9fda23f9)
    - [support local imports by @hakancelik96 and @isidentical](https://github.com/hakancelik96/unimport/commit/8c9b12295cf7c87670a685e59f95f1d83da130f7)

- Optimization
    - [balamir by @hakancelik96 and @isidentical](https://github.com/hakancelik96/unimport/commit/d4c1594371e7d3a3646cf2d886e931b50ca104f6)

- API Support
    - [General API Cleanup by @isidentical](https://github.com/hakancelik96/unimport/commit/f3efe4720eaa4eef5d991f838a0bd0872661dfa3)


## [0.1.3] - 31/Oct/2019
- pyproject.toml support
- setup.cfg support
- test written

### [0.1.0] - 27/Sep/2019
- Some class and function name and position changed.
- Future module added to the ignore list.
- Blank python file error fix.
- Default .unimport.cfg and extra_config add
- The new usage style `unimport` to scan from current path

### [0.0.3] - 22/Sep/2019
- Op system bug fix Linux and win
- File and folders features fix
- Add warning message if no enter any path No paths given 'Usage; unimport {source_file_or_directory}'"

### [0.0.2] - 21/Sep/2019
- find module bug fix;
For example; module: inspect, name; inspect.getsource; result unused import = inspect that is the wrong result

### [0.0.1] - 19/Sep/2019
- unimport {source_file_or_directory}
- .unimport.cfg 'type the names of files or folders that you do not want to scan.'
- Does not replace files only shows results.
