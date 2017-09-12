from bs4 import BeautifulSoup
import urllib2


misspelled_words = {}


def get_misspelled_words():
    """Scrapes wikipedia for the most commonly misspelled English words"""

    # Scrape wikipedia for the most common misspelled words
    source = "https://en.wikipedia.org/wiki/Commonly_misspelled_English_words#Typing_errors"
    content = urllib2.urlopen(source).read()
    soup = BeautifulSoup(content)

    # All misspelled words are in a div>ul>l
    for div in soup.find_all("div", class_="div-col columns column-count column-count-2"):
        for litag in soup.find_all("li", attrs={"class": None, "id": None}):
            words = litag.text.encode("utf-8")
            word = words.strip().split()

            # There are other items that fit the above criteria, but are not misspelled words, let's catch them here.
            if word[0] != '"100' or '"Canadian,' or "Merriam" or '"200' or "Linguistic error" or "Nonstandard spelling":
                if misspelled_words.get(word[0], 0) == 0:
                    misspelled_words[word[0]] = 0

    return misspelled_words


def find_misspelled_words():
    """Uses dictionary of misspelled words to find misspelled words in the Washington Post"""

    misspellings_found = {}
    found = []

    # Search the Washington Post for spelling errors.
    WaPoURL = "https://www.washingtonpost.com/powerpost/trumps-push-for-tax-cuts-is-coming-up-against-a-familiar-challenge-divided-gop/2017/09/11/bd7a875c-9763-11e7-82e4-f1076f6d6152_story.html?hpid=hp_hp-top-table-main_taxreform-5pm%3Ahomepage%2Fstory&utm_term=.3c871577cd56"
    selection = urllib2.urlopen(WaPoURL).read()
    soup2 = BeautifulSoup(selection)

    # Paragraphs are within div tags, not p tags
    for paragraph in soup2.find_all("p", class_=None):
        lines = paragraph.text.encode("utf-8")
        line = lines.strip().split()

        try:
            for l in line:
                if l in misspelled_words.get(l, "not found"):
                    if misspellings_found.get(l, 0) == 0:
                        misspellings_found[l] = 1

                    else:
                        misspellings_found[l] += 1

                else:
                    found.append(l)
        except TypeError:
            pass

    mistakes = len(misspellings_found)
    return "Found %s spelling mistakes" % mistakes

get_misspelled_words()
find_misspelled_words()
