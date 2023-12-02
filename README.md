## Advent of Code

My solutions for [AoC](https://adventofcode.com/) in Python.

## How to use

### Initial setup

1. Log into the [AoC website](https://adventofcode.com/) and [get your session cookie](https://support.pentest-tools.com/en/scans-tools/how-to-get-the-session-cookie).
1. Paste your session cookie value in a file called `session.cookie` at the root of the repository
1. [recommended] Set up a python virtual environment

### Scaffold a new day

```sh
./next.py
```

### Run last day

```sh
./run.py
```

If you are certain that you have the right solution, submit it with

```sh
./run.py -s 1
```

for the first part and `-s 2` for the second part.

### Before committing

Make sure to update the test that corresponds to the solution, and run code checks and formatters with

```sh
make lint
```