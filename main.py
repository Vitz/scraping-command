import sys

from Scraper import Scraper


def load_keywords_txt(filename):
    import csv
    keywords = []
    with open(filename, "r", encoding="utf8") as file:
        reader = csv.reader(file)
        for item in reader:
            keywords.append(item[0])
    print("Loaded {} keywords".format(len(keywords)))
    return keywords


def save(file, output, obj_name):
    with open(file, "w", encoding="utf8", newline="") as savef:
        import csv
        reader = csv.writer(savef)
        reader.writerows(output)
    print("Saved {} {}".format(len(output), obj_name))


if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) == 2:
        website = int(sys.argv[1])
        keywords_file = "keywords.txt"
    elif len(sys.argv) == 3:
        website = int(sys.argv[1])
        keywords_file = int(sys.argv[2])
    else:
        website = "https://megatool.pl"
        keywords_file = "keywords.txt"
        print("Wrong parameters, used default: {} {}".format(website, keywords_file))

    keywords = []
    try:
        keywords = load_keywords_txt(keywords_file)
    except Exception as e:
        print("Cant load file", str(e))

    if len(keywords) > 0:
        scraper = Scraper(keywords, website)
        urls = scraper.get_urls(sleep_time=5)
        totals = scraper.get_total_for_keywords()
        save("urls.csv", urls, "urls")
        save("totals.csv", totals, "totals")

    else:
        print("No keywords in file")







