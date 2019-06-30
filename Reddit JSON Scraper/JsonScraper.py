import requests
import json
import re
import os

# Globals
words = {}
titles = []

def get_page(url):
    response = requests.get(url, headers={"User-agent" : "lmao"})
    return response.content

def save_results(word_list):
    file = open("words.txt", "a")
    for w in word_list:
        file.write(w)
        file.write("\n")
    file.close()


def start():
    update_count = 0
    
    last_base36_seen = 0
    words = {}
    while True:
        titles = []
        source = get_page("https://www.reddit.com/r/Bitcoin/new.json?sort=new&limit=100")
        # load json string from api
        json_data = json.loads(source)
        current_base36 = 0
        current_base36 = int(json_data["data"]["children"][0]["data"]["id"], 36)

        # if new posts are found
        if(current_base36 > last_base36_seen):
            update_count += 1
            for post in json_data["data"]["children"]:
                # cast base 36 to decimal
                current_base36 = int(post["data"]["id"], 36)
                if (current_base36 > last_base36_seen):
                    # aux = post["data"]["title"].lower()
                    # titles.extend(post["data"]["title"].lower().split())
                    data = post["data"]["title"].lower()
                    titles.extend(re.findall(r"[\w']+", data))
                else:
                    break
                
            last_base36_seen = int(json_data["data"]["children"][0]["data"]["id"], 36)
            print("Updated" + str(update_count))

        if(update_count >= 2):
            save_results(titles)
            update_count = 0



def main():
    start()

if __name__ == "__main__":
    print(os.getpid())
    main()