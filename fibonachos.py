import argparse
from pathlib import Path
from typing import *
import time


class FibSub:
    """A rolling subsequence of the Fibonacci sequence."""
    def __init__(self, length: int) -> None:
        self.length = length
        self._subseq = self.seed
        self._iteration = None

    @property
    def seed(self) -> List[int]:
        """Produce the first N values in the Fibonacci sequence."""
        a, b = 0, 1
        if self.length == 1:
            return [a]
        if self.length == 2:
            return [a, b]
        values = [a, b]
        while len(values) < self.length:
            values.append(sum(values[-2:]))
        return values

    def __iter__(self) -> Iterator:
        """Iterate over the current subsequence."""
        return iter(self._subseq)

    def __next__(self) -> 'FibSub':
        """Produce the next subsequence."""
        value = self._subseq[-2] + self._subseq[-1]
        self._subseq = self._subseq[1:] + [value]
        return self

    def __repr__(self) -> str:
        """The unambiguous representation of this instance."""
        return f"{self.__class__.__qualname__}({self.length})"


class Times:
    """A class to manage elapsed execution time."""
    def __init__(self, timeout: float=None) -> None:
        self.timeout = timeout
        self._t0 = time.time()

    @property
    def t0(self) -> float:
        """The time at which this timer started."""
        return self._t0

    @property
    def up(self) -> bool:
        """True if the elapsed time is greater than a set duration."""
        if not self.timeout:
            return False
        return time.time() - self.t0 > self.timeout


class LexicalTuples:
    """A class to manage lexical tuples of the Fibonacci sequence."""
    def __init__(self, max_num: int=None, timeout: float=None) -> None:
        self.max_num = max_num
        self.times = Times(timeout=timeout)
        self.tuples = []
        self.highest = 0

    def find_all(self, n: int) -> Tuple[int]:
        """Find the first `n` lexical tuples in the Fibonacci sequence.

        This routine defines a "lexical tuple" to be a tuple of numbers such
        that the terminal letter in the spelling of the ith number is identical
        to the initial letter in the spelling of the (i+1)th number for i in
        {0..L-1}, where L is the length of the tuple. More colloquially, the
        last letter in the spelling of each number ends is the first letter in
        the spelling of the next number. For example, (5, 8, 13) -> ('five',
        'eight', 'thirteen') is a lexical triple. Note that this algorithm
        assumes English as the language.
        """
        subseq = FibSub(n)
        while not self.satisfied and not self.times.up:
            self.highest = max(subseq)
            if lexical(subseq):
                self.tuples.append(list(subseq))
            subseq = next(subseq)
        return 

    @property
    def satisfied(self) -> bool:
        """True if we have found enough tuples."""
        if not self.max_num:
            return False
        return len(self.tuples) >= self.max_num


def lexical(seq: Iterable[int]) -> bool:
    """True if `seq` forms a lexical tuple."""
    ends = [end_letters(i) for i in seq]
    return all(ends[i][-1] == ends[i+1][0] for i in range(len(ends)-1))


def output(results: List[str], userpath: Union[str, Path]=None):
    """Write results or print them to the screen."""
    lines = [
        '(' + ', '.join(str(i) for i in result) + ')'
        for result in results
    ]
    joined = '\n'.join(lines)
    if not userpath:
        print(joined)
        return
    filepath = Path(userpath).expanduser().resolve()
    with filepath.open('w') as fp:
        fp.writelines(joined)


digits = {
    n: s for n, s in enumerate(
        [
            'one',
            'two',
            'three',
            'four',
            'five',
            'six',
            'seven',
            'eight',
            'nine',
        ],
        start=1,
    )
}
teens = {
    n: s for n, s in enumerate(
        [
            'eleven',
            'twelve',
            'thirteen',
            'fourteen',
            'fifteen',
            'sixteen',
            'seventeen',
            'eightteen',
            'nineteen',
        ],
        start=11,
    )
}


def end_letters(n: int) -> Tuple[str, str]:
    """Determine the first and final letters in the spelling of `n`."""
    if n == 0:
        return 'z', 'o'
    special = {**digits, **teens}
    if n in special:
        return special[n][0], special[n][-1]
    if n == 10:
        return 't', 'n'
    if 20 <= n <= 99:
        first = digits[n // 10][0]
        if n % 10 == 0:
            return first, 'y'
        return first, digits[n % 10][-1]
    if 100 <= n <= 999:
        first = digits[n // 100][0]
        if n % 100 == 0:
            return first, 'd'
        return first, end_letters(n % 100)[1]
    str_n = str(n)
    hundreds = int(str_n[-3:])
    m = min(3, len(str_n)-3)
    leading = int(str_n[:m])
    first = end_letters(leading)[0]
    if hundreds == 0:
        return first, 'd' if 1000 <= n <= 999999 else 'n'
    return first, end_letters(hundreds)[1]


def test_end_letters():
    """Test the function that extracts first and final letters for a number."""
    # Test 0-9
    firsts = ['z', 'o', 't', 't', 'f', 'f', 's', 's', 'e', 'n']
    finals = ['o', 'e', 'o', 'e', 'r', 'e', 'x', 'n', 't', 'e']
    for n, (first, final) in enumerate(zip(firsts, finals)):
        assert end_letters(n) == (first, final)
    # Test 10-19
    firsts = ['t', 'e', 't', 't', 'f', 'f', 's', 's', 'e', 'n']
    finals = ['n', 'n', 'e', 'n', 'n', 'n', 'n', 'n', 'n', 'n']
    for n, (first, final) in enumerate(zip(firsts, finals), start=10):
        assert end_letters(n) == (first, final)
    # Test 20-99 in batches of 10
    firsts = ['t', 't', 'f', 'f', 's', 's', 'e', 'n']
    finals = ['y', 'e', 'o', 'e', 'r', 'e', 'x', 'n', 't', 'e']
    for i, first in enumerate(firsts, start=2):
        for j, final in enumerate(finals):
            n = 10*i + j
            assert end_letters(n) == (first, final)
    # Spot check from 100-999
    assert end_letters(100) == ('o', 'd')
    assert end_letters(123) == ('o', 'e')
    assert end_letters(234) == ('t', 'r')
    assert end_letters(345) == ('t', 'e')
    assert end_letters(456) == ('f', 'x')
    assert end_letters(567) == ('f', 'n')
    assert end_letters(678) == ('s', 't')
    assert end_letters(789) == ('s', 'e')
    assert end_letters(890) == ('e', 'y')
    assert end_letters(901) == ('n', 'e')
    # Sparsely spot check 1000+
    assert end_letters(1000) == ('o', 'd')
    assert end_letters(1234) == ('o', 'r')
    assert end_letters(2345) == ('t', 'e')
    assert end_letters(10000) == ('t', 'd')
    assert end_letters(23456) == ('t', 'x')
    assert end_letters(34567) == ('t', 'n')
    assert end_letters(100000) == ('o', 'd')
    assert end_letters(345678) == ('t', 't')
    assert end_letters(456789) == ('f', 'e')
    assert end_letters(1000000) == ('o', 'n')
    assert end_letters(4567890) == ('f', 'y')
    assert end_letters(5678901) == ('f', 'e')
    assert end_letters(10000000) == ('o', 'n')
    assert end_letters(56789012) == ('f', 'e')
    assert end_letters(67890123) == ('s', 'e')


if __name__ == '__main__':
    p = argparse.ArgumentParser(
        description=main.__doc__,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    p.add_argument(
        'length',
        help="the length of tuples to search for (e.g., 3 for triples)",
        type=int,
    )
    p.add_argument(
        '-n',
        '--max_num',
        help="the maximum number of lexical tuples to find",
        type=int,
    )
    p.add_argument(
        '-t',
        '--timeout',
        help="the maximum time (in seconds) to run",
        type=float,
        metavar=('SECONDS'),
    )
    p.add_argument(
        '-o',
        '--output',
        dest='filepath',
        help="path to which to write results (default: print to screen)",
        metavar=('PATH'),
    )
    args = p.parse_args()
    lextup = LexicalTuples(max_num=args.max_num, timeout=args.timeout)
    try:
        lextup.find_all(args.length)
    except KeyboardInterrupt:
        print(f"\nSearched up to {lextup.highest}")
    output(lextup.tuples, userpath=args.filepath)
