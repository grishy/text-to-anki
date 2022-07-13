import fitz

pdf_file = fitz.open("go.pdf")

for page in pdf_file:
    all_annot = [annot.rect for annot in page.annots()]
    if len(all_annot) == 0:
        continue

    print(page)
    all_words = page.get_text_words()

    # List to store all the highlighted texts
    highlight_text = []
    for h in all_annot:
        sentence = [w[4] for w in all_words if fitz.Rect(w[0:4]).intersect(h)]
        highlight_text.append(" ".join(sentence))

    print(highlight_text)