# fiveighthirteen

## Overview

A fun project based on an interesting observation: When writing out the Fibonacci subsequence 5, 8, 13 in English, the second word in each sequential pair begins with the final letter of the preceding word. Specifically, the last letter in "five" is the first letter in "eight" and the last letter in "eight" is the first letter in "thirteen".

It is then natural to ask, Are there more such subsequences?

This repository contains a command-line program to find n-tuples of numbers from the Fibonacci sequence that, when spelled in English, have the above property. For lack of a better term, I'll call these "lexical n-tuples".


## Example Usage

Print the first five lexical doubles

```
$ python fiveighthirteen.py 2 -n 5
(0, 1)
(5, 8)
(8, 13)
(55, 89)
(610, 987)
```

Print the first two lexical triples

```
$ python fiveighthirteen.py 3 -n 2
(5, 8, 13)
(53316291173, 86267571272, 139583862445)
```

See all the command-line options

```
$ python fiveighthirteen.py -h
```
