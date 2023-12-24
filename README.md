## Installation and usage

### Installation

_retirement-calculator_ can be installed by running `pip install .` from the project's root directory.  

Optionally, If you would like to test changes to the code without having to reinstall it, you can run `pip install --editable .` instead.  


### Usage

_retirement-calculator_ only requires as user-id as a parameter:


```sh
$ retirement-calculator {user_id}
```

For example:

```sh
$ retirement-calculator 1

To retire at age 63
You will need:       $ 8,148,166
You will have saved: $ 9,314,653

```

The inflation rate and expected annual salary increases can also be specified as well:

```sh
$ retirement-calculator 1 --inflation-rate=0.04 --annual-salary-increase=0.03

To retire at age 63
You will need:       $11,165,384
You will have saved: $10,237,312
```

All available options, and their default values, can be accessed with the `--help` flag:

```text
$ retirement-calculator --help

Usage: retirement-calculator [OPTIONS] USER_ID

Options:
  -r, --annual-salary-increase FLOAT
                                  The annual expected salary increase for the
                                  target user  [default: 0.02]
  -i, --inflation-rate FLOAT      The inflation rate used to calculate the
                                  purchasing power of future savings
                                  [default: 0.03]
  --help                          Show this message and exit.
```

## Commentary

### Structure

Code is split between three modules:
  1. `cli.py`: The project's entry point.  
  2. `client.py`: Code responsible for calling the API and passing back user data to consumers.  
  3. `models.py`: Code for wrapping, parsing, and operating on user data returned by the API.

Tests for `client.py` and `models.py` can be found under the `tests/` directory.  

_pytest_ is required for running these tests, but it is an optional dependency, so you may need to run `pip install pytest` first.  


### Potential Improvements


#### A Better Interface
If this were to remain a command line tool, I'd love to hook it into something like [textual](https://github.com/textualize/textual/).  Its ability to turn a CLI into a dynamic GUI would make the interface easier to navigate and allow for reactive elements (like graphs) that add additional dimensions to the underlying data.  

An alternative and more practical improvement would involve spinning this into a live service.  FastAPI is relatively easy to set up and provides automatic document generation and "try it now" features for defined endpoints.  If I were able to host this in a simple cloud environment, functionality could be easily tested in the browser and wouldn't require a local installation.  


#### A Discussion on Financial Calculations
The output for my implementation unfortunately does not match the example numbers in assignment description.  They do, however, match those calculated by [the example service](https://www.nerdwallet.com/calculator/retirement-calculator) linked in the introduction.

What I found interesting is that all the prominent retirement calculators (NerdWallet, Vanguard, Charles Schwab, etc...) output different values given the same inputs.  NerdWallet provides [some insight into their calculations](https://www.nerdwallet.com/calculator/retirement-calculator#results), as do other services.  The variance between services seems to come down to how each institution weighs different variables when calculating financial goals.  

If this weren't assessment, it would have been interesting to discuss Athena's strategy on financial planning ahead of time.  Given that this is an assessment though, it makes sense to leave the interpretation up to me, and the assignment's description provided more than enough information to build a working system.  


#### Better Input Validation
While I implemented validation that enforced things like age restrictions (e.g. retirement age must be greater than current age), I believe validation of user input could be improved.  

In its current state, the program assumes that user-provided values for the inflation rate and expected annual increases in salary are intentional and doesn't account for input like negative values, or percentages written as whole numbers (e.g. 0.02 vs 2).  

Implementing this would improve error reporting (or warnings if we want to allow any value) that would make it easier for the user to interpret erroneous output. 


#### Simple CI/CD
I wanted to integrate GitHub workflow into the project for running tests and validating code against tools I use in personal projects (_Flake8_, _mypy_, _black_, etc...).  Unfortunately, I ran out of time, so I will save that for v0.2


## Time Box
I spent approximately 8 hours on this project.  A breakdown of where I spent that time is as follows:
```text
* Core Requirements        : 3 hours
* Domain specific research : 2 hours
* Tests & Debugging        : 1 hour
* Refactoring and Polish:  : 1 hour
* Project and Package setup: 0.5 hour
* This README              : 0.5 hour
```

## Final Thoughts
I enjoyed my time spent on this project and learning more about how financial calculations are applied in practice.  While I'm familiar with the concepts specific to this project's goals, it was nice to finally apply those theories. 

Thank you for providing me with the opportunity to do so.   


