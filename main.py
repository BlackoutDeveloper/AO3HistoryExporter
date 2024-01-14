import argparse
from timeit import timeit

from selenium import webdriver
from selenium.webdriver.common.by import By


class Tag:
    def __init__(self, text, tag_type):
        self.text = text
        self.type = tag_type

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.__str__()


class Header:
    def __init__(self, title, author, recipient):
        self.title = title
        self.author = author
        self.recipient = recipient

    def to_str(self, sep):
        return self.title + sep + self.author + sep + self.recipient

    def __repr__(self, sep):
        return self.to_str(sep)


class Fic:
    def __init__(self, header: Header, fandoms: list[str], tags: list[Tag], metadata, summary):
        self.header = header
        self.fandoms = fandoms
        self.tags_warnings = [tag for tag in tags if tag.type == "warnings"]
        self.tags_relationships = [tag for tag in tags if tag.type == "relationships"]
        self.tags_characters = [tag for tag in tags if tag.type == "characters"]
        self.tags_freeform = [tag for tag in tags if tag.type == "freeforms"]
        self.metadata = metadata
        self.summary = summary

    def to_str(self, sep):
        res = ""
        res += self.header.to_str(sep) + sep
        res += ltostr(self.fandoms) + sep
        res += ltostr(self.tags_warnings) + sep
        res += ltostr(self.tags_relationships) + sep
        res += ltostr(self.tags_characters) + sep
        res += ltostr(self.tags_freeform) + sep
        res += str(self.metadata["language"]) + sep
        res += str(self.metadata["wordCount"]) + sep
        res += str(self.metadata["updated"]) + sep
        res += str(self.metadata["chapters"]) + sep
        res += str(self.metadata["finished"]) + sep
        res += str(self.metadata["series"]) + sep
        res += str(self.metadata["kudos"]) + sep
        res += str(self.metadata["comments"]) + sep
        res += str(self.metadata["bookmarks"]) + sep
        res += str(self.metadata["hits"]) + sep
        res += str(self.metadata["url"]) + sep
        res += str(self.metadata["rating"]) + sep
        res += str(self.metadata["pairings"]) + sep
        res += str(self.summary)
        return res

    def __repr__(self, sep):
        return self.to_str(sep)


def single_page(driver, page_number, username, output, sep):
    driver.get("https://archiveofourown.org/users/" + username + "/readings?page=" + str(page_number))
    fic_parts = driver.find_elements(By.CLASS_NAME, "work.blurb.group")
    return [single_fic(fic, output, sep) for fic in fic_parts]


def get_header_data(header_element):
    header_data_raw = header_element.find_elements(By.TAG_NAME, "a")
    header_data = Header("", "Anonymous", "None")
    if len(header_data_raw) == 1:
        header_data.author = "Anonymous"
    if len(header_data_raw) > 0:
        if "fandom" not in header_data_raw[0].text.lower():
            header_data.title = header_data_raw[0].text
    if len(header_data_raw) > 1:
        if "fandom" not in header_data_raw[1].text.lower():
            header_data.author = header_data_raw[1].text
    if len(header_data_raw) > 2:
        header_data.recipient = header_data_raw[2].text
    return header_data


def get_fandom_data(fandom_element):
    fandom_data_raw = fandom_element.find_elements(By.TAG_NAME, "a")
    fandom_data = []
    for fandom in fandom_data_raw:
        fandom_data.append(fandom.text)
    return fandom_data


def get_tag_data(tag_element):
    tag_data_raw = tag_element.find_elements(By.TAG_NAME, "li")
    tag_data = []
    for tag in tag_data_raw:
        tag_text = tag.text
        tag_type = tag.get_attribute("class").split(" ")[0]
        tag_data.append(Tag(tag_text, tag_type))
    return tag_data



def get_fic_metadata(fic_element):
    try:
        language = fic_element.find_elements(By.CLASS_NAME, "language")[1].text
    except:
        language = "None"
    try:
        wordCount = int(fic_element.find_elements(By.CLASS_NAME, "words")[1].text.replace(",", ""))
    except:
        wordCount = 0
    try:
        updated = fic_element.find_element(By.CLASS_NAME, "datetime").text
    except:
        updated = "Never"
    try:
        chapters = fic_element.find_elements(By.CLASS_NAME, "chapters")[1].text
        finished = "?" not in chapters
    except:
        chapters = "?/?"
        finished = False
    try:
        series = fic_element.find_element(By.CLASS_NAME, "series").find_element(By.TAG_NAME, "a").get_attribute("href")
    except:
        series = "None"
    try:
        kudos = int(fic_element.find_elements(By.CLASS_NAME, "kudos")[1].text.replace(",", ""))
    except:
        kudos = 0
    try:
        comments = int(fic_element.find_elements(By.CLASS_NAME, "comments")[1].text.replace(",", ""))
    except:
        comments = 0
    try:
        bookmarks = int(fic_element.find_elements(By.CLASS_NAME, "bookmarks")[1].text.replace(",", ""))
    except:
        bookmarks = 0
    try:
        hits = int(fic_element.find_elements(By.CLASS_NAME, "hits")[1].text.replace(",", ""))
    except:
        hits = 0
    try:
        url = fic_element.find_element(By.CLASS_NAME, "heading").find_element(By.TAG_NAME, "a").get_attribute("href")
    except:
        url = "None"
    try:
        rating = fic_element.find_element(By.CLASS_NAME, "rating").text
    except:
        rating = "None"
    try:
        pairings = fic_element.find_element(By.CLASS_NAME, "category").text
    except:
        pairings = "None"
    return {"language": language, "wordCount": wordCount, "updated": updated, "chapters": chapters,
            "finished": finished, "series": series, "kudos": kudos, "comments": comments, "bookmarks": bookmarks,
            "hits": hits, "url": url, "rating": rating, "pairings": pairings}


def single_fic(fic, output, sep):
    heading_part = fic.find_element(By.CLASS_NAME, "heading")
    this_fic_headers = get_header_data(heading_part)
    try:
        tag_part = fic.find_element(By.CLASS_NAME, "tags.commas")
        this_fic_tags = get_tag_data(tag_part)
    except:
        this_fic_tags = []
    try:
        fandom_part = fic.find_element(By.CLASS_NAME, "fandoms.heading")
        this_fic_fandoms = get_fandom_data(fandom_part)
    except:
        this_fic_fandoms = []
    this_fic_metadata = get_fic_metadata(fic)
    try:
        this_fic_summary = fic.find_element(By.CLASS_NAME, "summary").text.replace("\n", "/")
    except:
        this_fic_summary = "None"

    this_fic = Fic(this_fic_headers, this_fic_fandoms, this_fic_tags, this_fic_metadata, this_fic_summary)

    with open(output, "ab") as f:
        f.write(this_fic.to_str(sep).encode("utf-8", errors="ignore") + b"\n")

    return this_fic


def ltostr(input_str):
    return "[" + "; ".join([str(x) for x in input_str]) + "]"


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-u", "--username", help="Provide username", required=True)
    arg_parser.add_argument("-p", "--password", help="Provide password", required=True)
    arg_parser.add_argument("-o", "--output", help="Provide output file", required=True)
    arg_parser.add_argument("-s", "--separator", help="Modify Default Separator", default="Ƈ", required=False)
    args = arg_parser.parse_args()

    output_file = args.output
    username = args.username
    password = args.password
    separator = args.separator

    print("AO3 History Exporting...")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(
            "NameƇAuthorƇRecipientƇFandomsƇWarningsƇRelationshipsƇCharactersƇFreeform_TagsƇLanguageƇWord_CountƇLast_UpdatedƇChaptersƇFinishedƇSeriesƇKudosƇCommentsƇBookmarksƇHitsƇURLƇRatingƇPairingsƇSummary\n".replace(
                "Ƈ", separator))
    driver = webdriver.Chrome()
    driver.get("https://archiveofourown.org/")
    driver.find_element(By.ID, "login-dropdown").click()
    driver.find_element(By.ID, "user_session_login_small").send_keys(username)
    driver.find_element(By.ID, "user_session_password_small").send_keys(password)
    driver.find_element(By.NAME, "commit").click()
    driver.get("https://archiveofourown.org/users/" + username + "/readings?page=1")
    pages = int(
        driver.find_element(By.CLASS_NAME, "pagination.actions").find_elements(By.TAG_NAME, "li")[-2].find_element(
            By.TAG_NAME, "a").text)
    [single_page(driver, n, username, output_file, separator) for n in range(1, pages + 1)]
    # all_fics = [fic for page in all_fics for fic in page]
    pass


if __name__ == "__main__":
    print(timeit(main, number=1))
