import argparse
from typing import *
import bisect


def main(n: int) -> None:
    """Find the first `n` lexical triples in the Fibonacci sequence.

    This routine defines a "lexical triple" to be a triple of numbers such that
    the terminal letter in the first word is the initial letter in the second
    word and the terminal letter in the second word is the initial letter in the
    third word. Note that this algorithm assumes English as the language.
    """
    subseq = [0, 1, 1]
    triples = []
    for _ in range(n):
        subseq = update(subseq)
        spelled = [spell(s) for s in subseq]
        match1 = spelled[0][-1] == spelled[1][0]
        match2 = spelled[1][-1] == spelled[2][0]
        if match1 and match2:
            triples.append(spelled)
    print(triples)


def update(seq: List[int]) -> List[int]:
    """Update a running subsequence of the Fibonacci sequence."""
    value = seq[-2] + seq[-1]
    return seq[1:] + [value]


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
higher_orders = {
    i: s for i, s
    in zip([2, 3, 6, 9], ['hundred', 'thousand', 'million', 'billion'])
}
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
    elif 2 <= oom <= 9:
        return parse_higher_order(n)


def parse_higher_order(n: int) -> str:
    """Recursively parse orders of magnitude higher than 1."""
    str_n = str(n)
    oom = len(str_n) - 1
    if oom in higher_orders:
        base = f'{spell(int(str_n[0]))}-{higher_orders[oom]}'
        r = n % int(10**oom)
    else:
        orders = list(higher_orders.keys())
        pos = bisect.bisect_left(orders, oom) - 1
        clt = orders[pos]
        delta = oom - clt
        base = f'{spell(int(str_n[:delta+1]))}-{higher_orders[clt]}'
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
    args = p.parse_args()
    main(**vars(args))
