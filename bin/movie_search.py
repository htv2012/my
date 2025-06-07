#!/usr/bin/env python3
"""Search my services for movie"""

import argparse
import webbrowser


def main():
    """Entry"""
    parser = argparse.ArgumentParser()
    parser.add_argument("terms", nargs="+")
    options = parser.parse_args()
    terms = "+".join(options.terms)

    templates = [
        "https://www.netflix.com/search?q=",
        "https://www.hoopladigital.com/search?scope=MOVIE&type=direct&q=",
        "https://www.amazon.com/s?k=",
        "https://www.youtube.com/results?search_query=",
    ]

    for template in templates:
        url = template + terms
        print(url)
        webbrowser.open(url)


if __name__ == "__main__":
    main()
