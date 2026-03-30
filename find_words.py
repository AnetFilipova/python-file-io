#! /usr/bin/env python3

import sys
import re

def search_stream(in_stream, target_regex):
    """
    Search an input stream line by line for all matches of a regular
    expression pattern.

    Parameters
    ----------
    in_stream : file object (or any iterable of strings)
        The input stream to search through.

    target_regex : compiled regular expression object
        The pattern to search for in each line.

    Yields
    ------
    tuple
        A tuple of (line_number, matched_string) for each match found,
        where line_number is 1-based.

    Examples
    --------
    >>> import re, io
    >>> stream = io.StringIO("hello world\\nfoo bar\\n")
    >>> pattern = re.compile(r'\\w+oo')
    >>> list(search_stream(stream, pattern))
    [(2, 'foo')]
    """
    for line_number, line in enumerate(in_stream, 1):
        for match in target_regex.finditer(line):
            yield line_number, match.group()


def write_occurrences(out_stream, matches):
    """
    Write matched occurrences to an output stream.

    Each match is written as a line number and matched string separated
    by a tab character, one match per line.

    Parameters
    ----------
    out_stream : file object
        The output stream to write matches to.

    matches : iterable of tuples
        Each tuple should contain (line_number, matched_string).

    Returns
    -------
    int
        The total number of matches written to the output stream.

    Examples
    --------
    >>> import io
    >>> stream = io.StringIO()
    >>> write_occurrences(stream, [(1, 'inherit'), (2, 'heritable')])
    2
    """
    count = 0
    for line_number, word in matches:
        out_stream.write('{}\t{}\n'.format(line_number, word))
        count += 1
    return count


def process_file(in_path, out_path, target_regex):
    """
    Search a file for all matches of a regular expression pattern and
    write the results to an output file.

    Parameters
    ----------
    in_path : str
        Path to the input file to search.

    out_path : str
        Path to the output file to write results to.

    target_regex : compiled regular expression object
        The pattern to search for.

    Returns
    -------
    int
        The total number of matches found and written.
    """
    try:
        with open(in_path, 'r') as in_stream:
            with open(out_path, 'w') as out_stream:
                matches = search_stream(in_stream, target_regex)
                count = write_occurrences(out_stream, matches)
    except FileNotFoundError:
        sys.stderr.write("Error: could not find file '{}'\n".format(in_path))
        raise
    return count


if __name__ == '__main__':
    target_pattern = re.compile(r'\w*herit\w*', re.IGNORECASE)
    in_path = 'origin.txt'
    out_path = 'results.txt'

    count = process_file(in_path, out_path, target_pattern)
    print("Found {} occurrences of heritability-related words!".format(count))
