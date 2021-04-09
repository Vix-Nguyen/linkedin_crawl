import requests
from bs4 import BeautifulSoup
import json


def trade_spider():
    count_company = 0
    jobs_array = {}
    jobs = []

    url = "https://www.linkedin.com/jobs/search/"
    source = requests.get(url)
    soup = BeautifulSoup(source.text, "html.parser")
    for links in soup.findAll('a', {'class': 'result-card__full-card-link'}):
        sub_url = process(str(links))
        # print(sub_url)
        # print('---\n\n')
        jobs.append(get_item(sub_url))
        count_company += 1

    jobs_array["jobs"] = jobs
    writeJSONFile(jobs_array)
    # printToConsole(jobs)


def get_item(item_url):
    source = requests.get(item_url)
    soup = BeautifulSoup(source.text, "html.parser")

    # Get general description
    description = get_description(soup)
    title = get_title(soup)
    # print(info_content)

    job_item = {}

    job_item["Description: "] = description

    return job_item


def replace_all(text, dic, replace_char):
    for i in dic:
        text = text.replace(i, replace_char)
    return text


def get_title(soup):
    info = soup.find('h1', {'class', 'topcard__title'})
    info_content = str(info)
    return info_content


def get_description(soup):
    info = soup.find(
        'div', {'class', 'show-more-less-html__markup'})  # Array info
    info_content = str(info)[84:]
    newline = ['<ul><li>', '<li>', '<br>', '<br/>']
    blank = ['<strong>', '</strong>', '<p>', '</p>', '<em>', '</em>']
    info_content = replace_all(info_content, newline, '\n')
    info_content = replace_all(info_content, blank, ' ')

    return info_content


def title_process(str_title):
    begin = str_title.find("<h1>") + 4
    end = str_title.find("</h1>")
    return str_title[begin:end]


def company_process(str_company):
    begin = str_company.find("</div>")+39
    end = str_company.find("</span>")
    return str_company[begin:end]

    category = ""
    value = ""
    # xx= data.find( "<ul><li>")
    yy = data.find("<!-- <pre>")
    aa = data.find("<!-- <h3>Tỉnh / Thành:</h3> -->")
    date = data.find("<!-- <h3>Ngày đăng:</h3> -->")
    nganh = data.find("<h3>Ngành:</h3>")
    if nganh != -1:  # ngành
        begin = data.find("<h3>")+4
        middle = data.find("</h3>")
        end = data.find("</div>")
        category = data[begin:middle]
        value = data[middle+32:end]
        x = data.find("\t\t\t\t")
        if x != -1:
            value = [data[middle+32:x]]
            data = data[x+8:end]
            while(data.find("\t\t\t\t") != -1):
                temp = data.find("\t\t\t\t")
                value.append("-" + data[0:temp])
                data = data[temp + 4:]
        return[category, value]

    if yy != -1:  # lương
        begin = data.find("<h3>")+4
        middle = data.find("</h3>")
        end = yy
        category = data[begin:middle]
        value = data[middle+97:end-61]
        return[category, value]
    if aa != -1:  # nơi làm việc
        begin = data.find("<h3>")+4
        middle = data.find("</h3>")
        end = data.find("</div>")
        category = data[begin+len("Tỉnh / Thành:</h3> --><h3>") +
                        1:middle+len("Tỉnh / Thành:</h3> --><h3>")+1]
        value = data[middle+len("Tỉnh / Thành:</h3> --><h3>")+51:end-15]
        return[category, value]

    # ?????
    if date != -1:
        return[category, value]
    return[category, value]


def filter_data(dict):
    job = {}
    if "Tiêu đề" in dict:
        job['job_title'] = dict["Tiêu đề"]
    if "Tên công ty" in dict:
        job['company'] = dict['Tên công ty']
    if "Lương:" in dict:
        job['salary'] = dict['Lương:']
    if "Nơi làm việc:" in dict:
        job['location'] = dict['Nơi làm việc:']
    if "Ngành:" in dict:
        job['position'] = dict['Ngành:']
    # if "Ngành:" in dict:
    #     job['Position'] = dict['Ngành:']
    if "mô tả" in dict:
        job['job_description'] = dict['mô tả']
    if "yêu cầu" in dict:
        job['job_requirement'] = dict['yêu cầu']
    if "quyền lợi" in dict:
        job['benefit'] = dict['quyền lợi']
    if "số lượng" in dict:
        job['quantity'] = dict["số lượng"]
    return job


def writeJSONFile(dictionary):
    # Serializing json
    json_object = json.dumps(dictionary, indent=len(
        dictionary.keys()), ensure_ascii=False)

    # Writing to sample.json
    # with open("sample.json", "a", encoding='utf8') as outfile:
    #     outfile.write(json_object)

    with open("data2.json", "a", encoding='utf8') as outfile:
        outfile.write(json_object)


def printToConsole(dictionary):
    index = 1
    for i in dictionary:
        print(index)
        for key, value in i.items():
            print(key)
            print(value)
        print("------------------")
        index += 1


def process(data):
    begin = data.find("href=\"")
    end = data.rfind("click\">")
    return data[begin+len("href=\""):end+len("click\">")]


trade_spider()
