##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: May 28, 2021
##   | |    | | \ \    ---------------------------------
##   |_|    |_|  \_\   https://github.com/pedrorrivero
##

## Copyright 2021 Pedro Rivero
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
## http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.

from collections import OrderedDict
from typing import Any, Dict

from .argument_validation import validate_natural, validate_type

_UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
_LOWER = "abcdefghijklmnopqrstuvwxyz"
_NUMBERS = "0123456789"
_SYMBOLS = "<>.,:;_-+*=?!|@#$%&/()"


###############################################################################
## ALPHABETS
###############################################################################
ALPHABETS = {
    "UPPER": _UPPER,
    "LOWER": _LOWER,
    "NUMBERS": _NUMBERS,
    "SYMBOLS": _SYMBOLS,
    "BINARY": "01",
    "OCTAL": "01234567",
    "HEX": _NUMBERS + "ABCDEF",
    "BASE32": _UPPER + "234567",
    "BASE64": _UPPER + _LOWER + _NUMBERS + "+/",
    "DEFAULT": _UPPER + _LOWER + _NUMBERS + _SYMBOLS,
}


###############################################################################
## ENCODE
###############################################################################
def encode_numeral(uint: int, base_alphabet: str) -> str:
    """
    Encode `uint` in the given `base_alphabet` as a numeral string.

    Parameters
    ----------
    uint: int
        The number to encode.
    base_alphabet: str
        The alphabet to use as base for the encoding.

    Returns
    -------
    out: str
        The encoded `uint` in the given `base_alphabet` as a numeral string.
    """
    _validate_encode_args(uint, base_alphabet)
    base_alphabet = _remove_duplicate_chars(base_alphabet)
    base: int = len(base_alphabet)
    remainder: int = uint % base
    numeral: str = base_alphabet[remainder]
    uint //= base
    while uint != 0:
        remainder = uint % base
        numeral += base_alphabet[remainder]
        uint //= base
    return reverse_endian(numeral)


###############################################################################
## DECODE
###############################################################################
def decode_numeral(numeral: str, base_alphabet: str) -> int:
    """
    Decode `numeral` string in the given `base_alphabet`.

    Parameters
    ----------
    numeral: str
        The numeral string to decode.
    base_alphabet: str
        The alphabet to use as base for the encoding.

    Returns
    -------
    out: int
        The decoded `numeral` int in the given `base_alphabet`.
    """
    validate_numeral(numeral, base_alphabet)
    numeral = reverse_endian(numeral)
    base_alphabet = _remove_duplicate_chars(base_alphabet)
    value_dict: Dict[str, int] = _build_value_dict(base_alphabet)
    base: int = len(base_alphabet)
    mult: int = 1
    uint: int = 0
    while numeral:
        uint += mult * value_dict[numeral[0]]
        numeral = numeral[1:]
        mult *= base
    return uint


###############################################################################
## REVERSE ENDIAN
###############################################################################
def reverse_endian(numeral: str) -> str:
    """
    Reverses the endianness of a given `numeral` string.

    Parameters
    ----------
    numeral: str
        The numeral string whose endianness to reverse.

    Returns
    -------
    out: str
        The `numeral` string with its endianness reversed.
    """
    validate_type(numeral, str)
    return numeral[::-1]


###############################################################################
## IS NUMERAL
###############################################################################
def isnumeral(numeral: str, base_alphabet: str) -> bool:
    """
    Returns `True` if the input `numeral` is a numeral in the given
    `base_alphabet`, `False` otherwise.

    Parameters
    ----------
    numeral: str
        The numeral string to check.
    base_alphabet: str
        A string containig the characters to be used as base.

    Returns
    -------
    out: bool
        `True` if `numeral` is a numeral in the given base, `False` otherwise.

    Raises
    ------
    TypeError
        If input `numeral` or `base_alphabet` are not str.
    """
    validate_type(numeral, str)
    validate_type(base_alphabet, str)
    a: set = set(base_alphabet)
    n: set = set(numeral)
    return n.issubset(a)


###############################################################################
## VALIDATE NUMERAL
###############################################################################
def validate_numeral(numeral: str, base_alphabet: str) -> None:
    """
    Raises ValueError if the input `numeral` is not a numeral in the given
    `base_alphabet`.

    Parameters
    ----------
    numeral: str
        The numeral string to check.
    base_alphabet: str
        A string containig the characters to be used as base.

    Raises
    ------
    TypeError
        If input `numeral` or `base_alphabet` are not str.
    ValueError
        If `numeral` is not a numeral in the given base.
    """
    if not isnumeral(numeral, base_alphabet):
        raise ValueError(
            "Input `numeral` contains characters outside of `base_alphabet`."
        )


###############################################################################
## AUXILIARY
###############################################################################
def _build_value_dict(base_alphabet: str) -> Dict[str, int]:
    dictionary: Dict[str, int] = {}
    i: int = 0
    for char in base_alphabet:
        dictionary[char] = i
        i += 1
    return dictionary


def _remove_duplicate_chars(base_alphabet: str) -> str:
    od: Dict[str, Any] = OrderedDict.fromkeys(base_alphabet)
    return "".join(od)


def _validate_encode_args(uint: int, base_alphabet: str) -> None:
    validate_natural(uint, zero=True)
    validate_type(base_alphabet, str)
    if not base_alphabet:
        raise ValueError("Invalid input empty `base_alphabet`.")
