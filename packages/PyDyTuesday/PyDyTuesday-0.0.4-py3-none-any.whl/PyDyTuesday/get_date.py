import requests
import json


def get_date(week):
    """takes a week in string form, and optionally a directory, and downloads the TidyTuesday data files from the Github repo"""
    import requests
    import json
    year = week[0:4]
    repo = requests.get("https://api.github.com/repos/rfordatascience/tidytuesday/contents/data/" + year + "/" + week)
    json=repo.json()
    for item in json:
        if item["type"] == "file":
            url = item["download_url"]
            r = requests.get(url, allow_redirects=True)
            open(item["name"], 'wb').write(r.content)
            print (item["name"] + " downloaded")