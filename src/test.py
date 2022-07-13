# Based on https://stackoverflow.com/a/62859169/562769

from typing import List, Tuple
import pprint
import fitz  # install with 'pip install pymupdf'

_threshold_intersection = 0.9  # if the intersection is large enough.

def _check_contain(r_word, points):
    """If `r_word` is contained in the rectangular area.

    The area of the intersection should be large enough compared to the
    area of the given word.

    Args:
        r_word (fitz.Rect): rectangular area of a single word.
        points (list): list of points in the rectangular area of the
            given part of a highlight.

    Returns:
        bool: whether `r_word` is contained in the rectangular area.
    """
    # `r` is mutable, so everytime a new `r` should be initiated.
    r = fitz.Quad(points).rect
    r.intersect(r_word)

    if r.get_area() >= r_word.get_area() * _threshold_intersection:
        contain = True
    else:
        contain = False
    return contain


def _extract_annot(annot, words_on_page):
    """Extract words in a given highlight.

    Args:
        annot (fitz.Annot): [description]
        words_on_page (list): [description]

    Returns:
        str: words in the entire highlight.
    """
    quad_points = annot.vertices
    quad_count = int(len(quad_points) / 4)
    sentences = ['' for i in range(quad_count)]
    for i in range(quad_count):
        points = quad_points[i * 4: i * 4 + 4]
        words = [
            w for w in words_on_page if
            _check_contain(fitz.Rect(w[:4]), points)
        ]
        sentences[i] = ' '.join(w[4] for w in words)
    sentence = ' '.join(sentences)

    return sentence


def handle_page(page):
    wordlist = page.get_text("words")  # list of words on page
    wordlist.sort(key=lambda w: (w[3], w[0]))  # ascending y, then x

    highlights = []
    for annot in page.annots():
        if annot.type[0] == 8:
            highlights.append(_extract_annot(annot, wordlist))
    
    
    return highlights


def main(filepath: str) -> List:
    doc = fitz.open(filepath)

    dictionary = {}

    for page in doc:
        highlights = handle_page(page)
        for w in highlights:
            curr = dictionary.get(w,[])
            dictionary[w] = curr + [page.number]

    pp = pprint.PrettyPrinter(depth=4)
    pp.pprint(dictionary)

    print(len(dictionary))

if __name__ == "__main__":
    main("go.pdf")