
with open("navi_nlu_data.csv", "r") as f:
    x = f.read()

x = x.split("\n")
data = []
final_data = {}
for item in x:
    item = item.split(",")
    if len(item) == 2 and item[0] != "intent":
        if item[0] in final_data:
            final_data.get(item[0]).append(item[1])
        else:
            final_data[item[0]] = []
            final_data.get(item[0]).append(item[1])

    # data.append(item)

'''
## intent:greet
- How are you
- Hello
- How was your day
- Yo'''

formatted_data = []
for intent, data in final_data.items():
    formatted_data.append('## intent:{}'.format(intent))
    if type(data) is list:
        for item in data:
            formatted_data.append('- {}'.format(item))
        formatted_data.append("\n")

formatted_string = ""
for item in formatted_data:
    formatted_string += item + "\n"
print(formatted_string)

with open("nlu.md", "w+") as f:
    f.write(formatted_string)
