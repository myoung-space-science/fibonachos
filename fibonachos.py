import argparse
from pathlib import Path
from typing import *
import bisect


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

    @property
    def islexical(self) -> bool:
        """True if the current subsequence is a lexical tuple."""
        spelled = [spell(s) for s in self._subseq]
        match1 = spelled[0][-1] == spelled[1][0]
        match2 = spelled[1][-1] == spelled[2][0]
        return match1 and match2

    def __repr__(self) -> str:
        """The unambiguous representation of this instance."""
        return f"{self.__class__.__qualname__}({self.length})"



def main(n: int, length: int, filepath: Union[str, Path]) -> None:
    """Find the first `n` lexical tuples in the Fibonacci sequence.

    This routine defines a "lexical tuple" to be a tuple of numbers such that
    the terminal letter in the spelling of the ith number is identical to the
    initial letter in the spelling of the (i+1)th number for i in {0..L-1},
    where L is the length of the tuple. More colloquially, the last letter in
    the spelling of each number ends is the first letter in the spelling of the
    next number. For example, (5, 8, 13) -> ('five', 'eight', 'thirteen') is a
    lexical triple. Note that this algorithm assumes English as the language.
    """
    subseq = FibSub(length)
    triples = []
    while len(triples) < n:
        current = next(subseq)
        try:
            if current.islexical:
                triples.append(list(current))
        except OOMError:
            print(f"Checked up to {list(current)}")
            break
    output(triples, userpath=filepath)


def merge(triple: str) -> str:
    """Merge pairs in a lexical triple."""
    return triple[0][:-1] + triple[1] + triple[2][1:]


def output(triples: List[str], userpath: Union[str, Path]=None):
    """Write results or print them to the screen."""
    if not userpath:
        print(triples)
    else:
        filepath = Path(userpath).expanduser().resolve()
        with filepath.open('w') as fp:
            lines = [
                '(' + ', '.join(str(i) for i in triple) + ')'
                for triple in triples
            ]
            fp.writelines('\n'.join(lines))


zero_to_twenty = [
    'zero',
    'one',
    'two',
    'three',
    'four',
    'five',
    'six',
    'seven',
    'eight',
    'nine',
    'ten',
    'eleven',
    'twelve',
    'thirteen',
    'fourteen',
    'fifteen',
    'sixteen',
    'seventeen',
    'eightteen',
    'nineteen',
    'twenty',
]
tens = [
    'ten',
    'twenty',
    'thirty',
    'forty',
    'fifty',
    'sixty',
    'seventy',
    'eighty',
    'ninety',
]
higher_order_names = [
    'hundred',
    'thousand',
    'million',
    'billion',
    'trillion',
    'quadrillion',
    'quintillion',
    'sextillion',
    'septillion',
    'octillion',
    'nonillion',
]
higher_orders = [2] + [3*i for i in range(1, len(higher_order_names))]
higher_order_map = {i: s for i, s in zip(higher_orders, higher_order_names)}


class OOMError(TypeError):
    def __init__(self, n: int) -> None:
        self.n = n

    def __str__(self) -> str:
        return f"Unrecognized order of magnitude: {self.n}"


def spell(n: int) -> str:
    """Convert an integer to a word."""
    if not isinstance(n, int) or n < 0:
        raise TypeError("input must be a non-negative integer.")
    if 0 <= n <= 20:
        return zero_to_twenty[n]
    # Use the string representation to get the order of magnitude. This
    # leverages the fact that n must be a non-negative integer.
    str_n = str(n)
    oom = len(str_n) - 1
    if oom == 1:
        tens_place, ones_place = divmod(n, 10)
        if ones_place == 0:
            return f"{tens[tens_place-1]}"
        return f"{tens[tens_place-1]}-{zero_to_twenty[ones_place]}"
    elif 2 <= oom <= higher_orders[-1]:
        return parse_higher_order(n)
    else:
        raise OOMError(oom) from None


def parse_higher_order(n: int) -> str:
    """Recursively parse orders of magnitude higher than 1."""
    str_n = str(n)
    oom = len(str_n) - 1
    if oom in higher_order_map:
        base = f'{spell(int(str_n[0]))}-{higher_order_map[oom]}'
        r = n % int(10**oom)
    else:
        orders = list(higher_order_map.keys())
        pos = bisect.bisect_left(orders, oom) - 1
        clt = orders[pos]
        delta = oom - clt
        base = f'{spell(int(str_n[:delta+1]))}-{higher_order_map[clt]}'
        r = n % int(10**clt)
    return f'{base} {spell(r)}' if r > 0 else base


def test_spell():
    """Test the spelling function"""
    for n, name in enumerate(zero_to_twenty):
        assert spell(n) == name
    for n, name in enumerate(tens):
        assert spell(10 * (n+1)) == name
    for n in range(21, 30):
        assert spell(n) == f'twenty-{spell(n - 20)}'
    for n in range(1, 10):
        assert spell(100 * n) == f'{spell(n)}-hundred'
    assert spell(123) == 'one-hundred twenty-three'
    assert spell(1234) == 'one-thousand two-hundred thirty-four'
    assert spell(12345) == 'twelve-thousand three-hundred forty-five'
    assert spell(123456) == (
        'one-hundred twenty-three-thousand four-hundred fifty-six'
    )
    assert spell(1234567) == (
        'one-million two-hundred thirty-four-thousand five-hundred sixty-seven'
    )
    assert spell(12345678) == (
        'twelve-million three-hundred forty-five-thousand'
        ' six-hundred seventy-eight'
    )
    assert spell(123456789) == (
        'one-hundred twenty-three-million'
        ' four-hundred fifty-six-thousand'
        ' seven-hundred eighty-nine'
    )
    assert spell(1234567890) == (
        'one-billion two-hundred thirty-four-million'
        ' five-hundred sixty-seven-thousand'
        ' eight-hundred ninety'
    )


if __name__ == '__main__':
    p = argparse.ArgumentParser(
        description=main.__doc__,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    p.add_argument(
        'n',
        help="the number of lexical triples to find",
        type=int,
    )
    p.add_argument(
        'length',
        help="the length of tuples to search for (e.g., 3 for triples)",
        type=int,
    )
    p.add_argument(
        '-o',
        '--output',
        dest='filepath',
        help="path to which to write results (default: print to screen)",
        metavar=('PATH'),
    )
    args = p.parse_args()
    main(**vars(args))
