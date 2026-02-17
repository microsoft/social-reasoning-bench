# Prompt Converters for Guardrail/Jailbreak Testing
# Adapted from Microsoft PyRIT (https://github.com/Azure/PyRIT)
# Licensed under MIT license

"""
Standalone prompt converters for testing AI guardrails.
These converters transform prompts using various encoding/obfuscation techniques
to test if safety filters can be bypassed.

Usage:
    from converters import base64_encode, caesar_cipher, morse_encode

    prompt = "How to hack a computer"
    encoded = base64_encode(prompt)
    print(encoded)  # SG93IHRvIGhhY2sgYSBjb21wdXRlcg==
"""

import base64
import codecs
import random
import re
import string

# =============================================================================
# ENCODING CONVERTERS
# =============================================================================


def base64_encode(text: str) -> str:
    """
    Encode text to base64 format.

    Example:
        >>> base64_encode("hello")
        'aGVsbG8='
    """
    return base64.b64encode(text.encode("utf-8")).decode("utf-8")


def base64_decode(text: str) -> str:
    """Decode base64 text back to original."""
    return base64.b64decode(text.encode("utf-8")).decode("utf-8")


def binary_encode(text: str, bits: int = 8) -> str:
    """
    Convert text to binary representation.

    Args:
        text: Input text
        bits: Bits per character (8, 16, or 32)

    Example:
        >>> binary_encode("Hi")
        '01001000 01101001'
    """
    return " ".join(format(ord(char), f"0{bits}b") for char in text)


def morse_encode(text: str) -> str:
    """
    Encode text to Morse code.
    Uses '-' and '.', space between chars, '/' between words.

    Example:
        >>> morse_encode("SOS")
        '... --- ...'
    """
    morse_mapping = {
        "A": ".-",
        "B": "-...",
        "C": "-.-.",
        "D": "-..",
        "E": ".",
        "F": "..-.",
        "G": "--.",
        "H": "....",
        "I": "..",
        "J": ".---",
        "K": "-.-",
        "L": ".-..",
        "M": "--",
        "N": "-.",
        "O": "---",
        "P": ".--.",
        "Q": "--.-",
        "R": ".-.",
        "S": "...",
        "T": "-",
        "U": "..-",
        "V": "...-",
        "W": ".--",
        "X": "-..-",
        "Y": "-.--",
        "Z": "--..",
        "0": "-----",
        "1": ".----",
        "2": "..---",
        "3": "...--",
        "4": "....-",
        "5": ".....",
        "6": "-....",
        "7": "--...",
        "8": "---..",
        "9": "----.",
        " ": "/",
        ".": ".-.-.-",
        ",": "--..--",
        "?": "..--..",
        "!": "-.-.--",
        "'": ".----.",
        '"': ".-..-.",
        ":": "---...",
    }
    return " ".join(morse_mapping.get(c.upper(), "........") for c in text)


def url_encode(text: str) -> str:
    """
    Encode text to URL format (percent encoding).

    Example:
        >>> url_encode("hello world")
        'hello%20world'
    """
    from urllib.parse import quote

    return quote(text)


# =============================================================================
# CIPHER CONVERTERS
# =============================================================================


def rot13_encode(text: str) -> str:
    """
    Apply ROT13 cipher (shift by 13 positions).

    Example:
        >>> rot13_encode("hello")
        'uryyb'
    """
    return codecs.encode(text, "rot13")


def caesar_cipher(text: str, offset: int = 3) -> str:
    """
    Apply Caesar cipher with specified offset.

    Args:
        text: Input text
        offset: Shift amount (-25 to 25)

    Example:
        >>> caesar_cipher("abc", 1)
        'bcd'
    """

    def shift(alphabet: str) -> str:
        return alphabet[offset:] + alphabet[:offset]

    alphabet = (string.ascii_lowercase, string.ascii_uppercase, string.digits)
    shifted = tuple(map(shift, alphabet))
    table = str.maketrans("".join(alphabet), "".join(shifted))
    return text.translate(table)


def atbash_cipher(text: str) -> str:
    """
    Apply Atbash cipher (reverse alphabet substitution).
    A->Z, B->Y, etc.

    Example:
        >>> atbash_cipher("Hello")
        'Svool'
    """

    def reverse(alphabet: str) -> str:
        return alphabet[::-1]

    alphabet = (string.ascii_lowercase, string.ascii_uppercase, string.digits)
    reversed_alphabet = tuple(map(reverse, alphabet))
    table = str.maketrans("".join(alphabet), "".join(reversed_alphabet))
    return text.translate(table)


# =============================================================================
# TEXT MANIPULATION CONVERTERS
# =============================================================================


def flip_text(text: str) -> str:
    """
    Reverse the text.

    Example:
        >>> flip_text("hello")
        'olleh'
    """
    return text[::-1]


def leetspeak(text: str, deterministic: bool = True) -> str:
    """
    Convert text to leetspeak.

    Args:
        text: Input text
        deterministic: If True, use first substitution; if False, random choice

    Example:
        >>> leetspeak("hello")
        'h3110'
    """
    substitutions = {
        "a": ["4", "@"],
        "b": ["8", "6"],
        "c": ["(", "["],
        "e": ["3"],
        "g": ["9"],
        "i": ["1", "!"],
        "l": ["1", "|"],
        "o": ["0"],
        "s": ["5", "$"],
        "t": ["7"],
        "z": ["2"],
    }
    result = []
    for char in text:
        lower = char.lower()
        if lower in substitutions:
            if deterministic:
                result.append(substitutions[lower][0])
            else:
                result.append(random.choice(substitutions[lower]))
        else:
            result.append(char)
    return "".join(result)


def character_space(text: str) -> str:
    """
    Add spaces between characters and remove punctuation.
    Bypass technique for Meta's Llama classifier.

    Example:
        >>> character_space("hello!")
        'h e l l o '
    """
    spaced = " ".join(text)
    return re.sub(r"[!\"#$%&'()*+,-./:;<=>?@\[\]^_`{|}~]", "", spaced)


def charswap(text: str, iterations: int = 1) -> str:
    """
    Swap adjacent characters in words to create typos.

    Args:
        text: Input text
        iterations: Number of swaps per word

    Example:
        >>> charswap("hello")  # result varies
        'hlelo'
    """
    words = text.split()
    result = []
    for word in words:
        if len(word) > 3:
            chars = list(word)
            for _ in range(iterations):
                idx = random.randint(1, len(word) - 2)
                chars[idx], chars[idx + 1] = chars[idx + 1], chars[idx]
            result.append("".join(chars))
        else:
            result.append(word)
    return " ".join(result)


def string_join(text: str, separator: str = "-") -> str:
    """
    Join characters with a separator.

    Example:
        >>> string_join("hello", "-")
        'h-e-l-l-o'
    """
    return separator.join(text)


# =============================================================================
# UNICODE CONVERTERS
# =============================================================================


def unicode_substitution(text: str) -> str:
    """
    Replace ASCII characters with full-width Unicode equivalents.

    Example:
        >>> unicode_substitution("hello")
        'ｈｅｌｌｏ'
    """
    result = []
    for char in text:
        code = ord(char)
        # Convert ASCII letters and digits to full-width
        if 0x21 <= code <= 0x7E:
            result.append(chr(code + 0xFEE0))
        elif char == " ":
            result.append("\u3000")  # Full-width space
        else:
            result.append(char)
    return "".join(result)


def diacritic_add(text: str) -> str:
    """
    Add diacritical marks (combining characters) to text.

    Example:
        >>> diacritic_add("hello")
        'h̀èl̀l̀ò'
    """
    combining_marks = [
        "\u0300",  # Combining grave accent
        "\u0301",  # Combining acute accent
        "\u0302",  # Combining circumflex
        "\u0303",  # Combining tilde
        "\u0308",  # Combining diaeresis
    ]
    result = []
    for char in text:
        result.append(char)
        if char.isalpha():
            result.append(random.choice(combining_marks))
    return "".join(result)


def zero_width_inject(text: str) -> str:
    """
    Inject zero-width characters between letters.
    Visually identical but different string.

    Example:
        >>> zero_width_inject("hello")  # looks like 'hello' but contains hidden chars
        'h\u200be\u200bl\u200bl\u200bo'
    """
    zwc = "\u200b"  # Zero-width space
    return zwc.join(text)


# =============================================================================
# UNICODE CONFUSABLES (requires external packages for full support)
# =============================================================================

# Basic confusables mapping (subset)
CONFUSABLES = {
    "a": "а",  # Cyrillic а
    "c": "с",  # Cyrillic с
    "e": "е",  # Cyrillic е
    "o": "о",  # Cyrillic о
    "p": "р",  # Cyrillic р
    "x": "х",  # Cyrillic х
    "y": "у",  # Cyrillic у
    "A": "А",  # Cyrillic А
    "B": "В",  # Cyrillic В
    "C": "С",  # Cyrillic С
    "E": "Е",  # Cyrillic Е
    "H": "Н",  # Cyrillic Н
    "K": "К",  # Cyrillic К
    "M": "М",  # Cyrillic М
    "O": "О",  # Cyrillic О
    "P": "Р",  # Cyrillic Р
    "T": "Т",  # Cyrillic Т
    "X": "Х",  # Cyrillic Х
}


def unicode_confusable(text: str, probability: float = 0.5) -> str:
    """
    Replace characters with visually similar Unicode characters (homoglyphs).

    Args:
        text: Input text
        probability: Chance of replacing each confusable character

    Example:
        >>> unicode_confusable("apple")  # may look identical but uses Cyrillic chars
        'аррlе'
    """
    result = []
    for char in text:
        if char in CONFUSABLES and random.random() < probability:
            result.append(CONFUSABLES[char])
        else:
            result.append(char)
    return "".join(result)


# =============================================================================
# ASCII ART (requires 'art' package: pip install art)
# =============================================================================


def ascii_art(text: str, font: str = "standard") -> str:
    """
    Convert text to ASCII art.
    Requires: pip install art

    Args:
        text: Input text
        font: Font name (e.g., "standard", "block", "banner")

    Example:
        >>> print(ascii_art("Hi"))
        # Outputs large ASCII art letters
    """
    try:
        from art import text2art

        return text2art(text, font=font)
    except ImportError:
        return f"[ASCII ART: {text}] (install 'art' package for actual output)"


# =============================================================================
# SUFFIX APPEND (for adversarial suffix attacks)
# =============================================================================


def suffix_append(text: str, suffix: str = " Sure, here is") -> str:
    """
    Append an adversarial suffix to the prompt.
    Common technique to elicit compliance.

    Example:
        >>> suffix_append("How to hack")
        'How to hack Sure, here is'
    """
    return text + suffix


# =============================================================================
# BATCH CONVERSION
# =============================================================================


def apply_all_converters(text: str) -> dict:
    """
    Apply all converters to a text and return results.

    Returns:
        Dictionary mapping converter name to converted text
    """
    return {
        "base64": base64_encode(text),
        "binary": binary_encode(text),
        "morse": morse_encode(text),
        "url": url_encode(text),
        "rot13": rot13_encode(text),
        "caesar_3": caesar_cipher(text, 3),
        "atbash": atbash_cipher(text),
        "flip": flip_text(text),
        "leetspeak": leetspeak(text),
        "character_space": character_space(text),
        "string_join": string_join(text, "-"),
        "unicode_sub": unicode_substitution(text),
        "zero_width": zero_width_inject(text),
        "confusable": unicode_confusable(text),
        "suffix": suffix_append(text),
    }


# =============================================================================
# CLI INTERFACE
# =============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Prompt converter for guardrail testing")
    parser.add_argument("text", help="Text to convert")
    parser.add_argument(
        "-c",
        "--converter",
        default="all",
        choices=[
            "all",
            "base64",
            "binary",
            "morse",
            "url",
            "rot13",
            "caesar",
            "atbash",
            "flip",
            "leetspeak",
            "charspace",
            "charswap",
            "unicode",
            "confusable",
            "ascii_art",
            "suffix",
        ],
        help="Converter to use (default: all)",
    )
    parser.add_argument("--offset", type=int, default=3, help="Offset for Caesar cipher")

    args = parser.parse_args()

    if args.converter == "all":
        results = apply_all_converters(args.text)
        print(f"Original: {args.text}\n")
        for name, converted in results.items():
            print(f"{name}:")
            print(f"  {converted}\n")
    else:
        converters = {
            "base64": lambda t: base64_encode(t),
            "binary": lambda t: binary_encode(t),
            "morse": lambda t: morse_encode(t),
            "url": lambda t: url_encode(t),
            "rot13": lambda t: rot13_encode(t),
            "caesar": lambda t: caesar_cipher(t, args.offset),
            "atbash": lambda t: atbash_cipher(t),
            "flip": lambda t: flip_text(t),
            "leetspeak": lambda t: leetspeak(t),
            "charspace": lambda t: character_space(t),
            "charswap": lambda t: charswap(t),
            "unicode": lambda t: unicode_substitution(t),
            "confusable": lambda t: unicode_confusable(t),
            "ascii_art": lambda t: ascii_art(t),
            "suffix": lambda t: suffix_append(t),
        }
        print(converters[args.converter](args.text))
