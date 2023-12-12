from collections import defaultdict

y2006_headline_lists = [
    ["the", "soldier", "returned"],
    ["I", "and", "the", "cat"],
    ["cat", "in", "the", "hat"],
]


def wordcount(rlist, *args):
    word_count = defaultdict(int)
    for headlines in rlist:
        for headline in headlines:
            word_count[headline] += 1

    word_count = {arg: word_count[arg] for arg in args}
    return word_count


print(wordcount(y2006_headline_lists, "the", "and", "cat"))