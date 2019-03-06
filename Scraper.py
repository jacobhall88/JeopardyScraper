from bs4 import BeautifulSoup
import json
import requests
import re

gamecount = 1
finalcount = 6224
url = "http://www.j-archive.com/showgame.php?game_id="
testurl = url + str(gamecount)
response = requests.get(testurl, timeout = 5)
content = BeautifulSoup(response.content, "html.parser")
json_dict = {}

while gamecount < finalcount:

    categories = content.findAll('td', attrs={"class": "category_name"})
    count = 1
    cat_dict = {}

    for category in categories:
        category_str = category.text
        if count < 7:
            dict_string = "J_"
            dict_string += str(count)
            cat_dict[dict_string] = category_str
        if 6 < count < 13:
            dict_string = "DJ_"
            dict_string += str(count - 6)
            cat_dict[dict_string] = category_str
        count += 1

    questions = content.findAll('table')
    for table in questions:
        double = False
        final = False
        valid = True
        question = table.find('div', attrs={"onmouseover": re.compile("toggle*")})
        if question is not None:
            question_str = str(question)
            if question_str.split("_")[1] == "FJ":
                final = True

            if final is False:
                value = question.find('td', attrs={"class": "clue_value"})
                if value is None:
                    value = "Double Jeopardy"
                else:
                    value = value.text.split("$")
                    if len(value) > 1:
                        value = value[1]

            else:
                value = "Final Jeopardy"

            if final is False:
                answerSplit1 = question_str.split("correct_response&quot;&gt;")
                if len(answerSplit1) > 1:
                    answerSplit2 = answerSplit1[1].split("&lt;/em&gt;&lt;br")
                else:
                    valid = False
            else:
                answerSplit1 = question_str.split("correct_response\&quot;&gt;")
                if len(answerSplit1) > 1:
                    answerSplit2 = answerSplit1[1].split("&lt;/em&gt;'")
                else:
                    valid = False

            if valid:
                answer = answerSplit2[0]


            if valid:
                cluetext = table.find('td', attrs={"class": "clue_text"})
                if cluetext is not None:
                    clue = cluetext.text
                else:
                    valid = False

            if valid:
                if final is False:
                    cat = str(table.find('td', attrs={"class": re.compile("clue_unstuck*")}))
                    cat = cat.split("_")
                    cat = cat_dict[cat[2] + "_" + cat[3]]
                else:
                    cat = category.text

            if valid:
                append_tup = (clue, answer, value)
                if cat in json_dict.keys():
                    if append_tup not in json_dict[cat]:
                        json_dict[cat].append(append_tup)
                else:
                    json_dict[cat] = [append_tup]

    gamecount += 1
    if gamecount == 3576:
        gamecount += 1
    url = "http://www.j-archive.com/showgame.php?game_id="
    testurl = url + str(gamecount)
    response = requests.get(testurl, timeout=5)
    content = BeautifulSoup(response.content, "html.parser")
    print(len(json_dict.keys()))
    print("This is page number: " + str(gamecount))

with open('jeopardydb.json', 'w') as outfile:
    json.dump(json_dict, outfile, sort_keys=True, indent=4)

