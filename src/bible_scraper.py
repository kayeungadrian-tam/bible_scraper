import re
import os

import bs4
import requests

OUT_DIR = "./output"

old_testament = [
    "Genesis",
    "Exodus",
    "Leviticus",
    "Numbers",
    "Deuteronomy",
    "Joshua",
    "Judges",
    "Ruth",
    "1%20Samuel",
    "2%20Samuel",
    "1%20Kings",
    "2%20Kings",
    "1%20Chronicles",
    "2%20Chronicles",
    "Ezra",
    "Nehemiah",
    "Esther",
    "Job",
    "Psalm",
    "Proverbs",
    "Ecclesiastes",
    "Song%20of%20Songs",
    "Isaiah",
    "Jeremiah",
    "Lamentations",
    "Ezekiel",
    "Daniel",
    "Hosea",
    "Joel",
    "Amos",
    "Obadiah",
    "Jonah",
    "Micah",
    "Nahum",
    "Habakkuk",
    "Zephaniah",
    "Haggai",
    "Zechariah",
    "Malachi",
]


new_testament = [
    "Matthew",
    "Mark",
    "Luke",
    "John",
    "Acts",
    "Romans",
    "1%20Corinthians",
    "2%20Corinthians",
    "Galatians",
    "Ephesians",
    "Philippians",
    "Colossians",
    "1%20Thessalonians",
    "2%20Thessalonians",
    "1%20Timothy",
    "2%20Timothy",
    "Titus",
    "Philemon",
    "Hebrews",
    "James",
    "1%20Peter",
    "2%20Peter",
    "1%20John",
    "2%20John",
    "3%20John",
    "Jude",
    "Revelation",
]


def get_book_text_en(book: str, file_name: str):
    chapter = 1
    end = False

    file_path = os.path.join(OUT_DIR, f"{file_name}.txt")

    with open(file_path, "a") as f:
        while not end:
            url = f"https://www.biblegateway.com/passage/?search={book}%20{chapter}&version=ESV"

            res = requests.get(url)
            text = res.text
            soup = bs4.BeautifulSoup(text, "html.parser")
            passage_text = soup.find("div", class_="passage-text")

            if passage_text:
                passage_text = passage_text.get_text()
                end_index = int(passage_text.find("\nFootnotes"))
                real_text = passage_text[:end_index].replace("\n", "")

                for i, verse in enumerate(re.split("[0-9]\xa0", real_text)):

                    if verse:
                        try:
                            int(verse[-1])
                            verse = verse[:-1]
                        except:
                            pass

                        tmp_verse = re.sub("\([A-Z]+\)", "", verse)
                        tmp_verse = re.sub("\[[a-z]+\]", "", tmp_verse)

                        if "Cross references" in tmp_verse:
                            cr_index = tmp_verse.index("Cross references")
                            tmp_verse = tmp_verse[:cr_index]
                        f.write(f"{book},{chapter},{i},{tmp_verse}\n")
                chapter += 1
            else:
                break


def test(book: str, chapter: int):
    end = False

    with open("./test.txt", "w") as f:
        url = f"https://www.biblegateway.com/passage/?search={book}%20{chapter}&version=ESV"

        res = requests.get(url)
        text = res.text
        soup = bs4.BeautifulSoup(text, "html.parser")
        passage_text = soup.find("div", class_="passage-text")

        if passage_text:
            passage_text = passage_text.get_text()
            end_index = int(passage_text.find("\nFootnotes"))
            real_text = passage_text[:end_index].replace("\n", "")

            for i, verse in enumerate(re.split("[0-9]\xa0", real_text)):

                if verse:
                    try:
                        int(verse[-1])
                        verse = verse[:-1]
                    except:
                        pass

                    tmp_verse = re.sub("\([A-Z]+\)", "", verse)
                    tmp_verse = re.sub("\[[a-z]+\]", "", tmp_verse)

                    if "Cross references" in tmp_verse:
                        tmp_verse = tmp_verse.index("Cross references")

                    f.write(f"{book},{chapter},{i},{tmp_verse}\n")
            chapter += 1
        else:
            return


if __name__ == "__main__":
    for ot_book in old_testament:
        print(f"Prcoessing:\t{ot_book}")
        get_book_text_en(ot_book, "old_testament")

    for nt_book in new_testament:
        print(f"Prcoessing:\t{nt_book}")
        get_book_text_en(nt_book, "new_testament")
