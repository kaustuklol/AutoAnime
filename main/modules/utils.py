def trim(text):
    return text.replace(" ", "").lower()

def r_char(text):
    return text.replace(":", "").replace("/", "").replace("!", "").replace("*", "").replace("'", "").replace("-", "").replace("é", "e").replace(",", "").replace(";", "").replace("|", "").replace(".", "").lower()

def purify(text):
    return text.replace("S2", "Season 2").replace("S3", "Season 3").replace("S4", "Season 4").replace("S5", "Season 5").replace("S6", "Season 6").replace("S7", "Season 7").replace("S8", "Season 8").replace("S9", "Season 9").replace("S10", "Season 10").lower()
