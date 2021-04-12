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
    location = get_location(soup)
    company = get_company(soup)
    posted_time = get_posted_time(soup)
    num_applicant = get_numap(soup)
    senority, emp_type, job_func, industries = get_criteria(soup)
    # print(senority)

    job_item = {}

    job_item['Description'] = description
    job_item['Title'] = title
    job_item['Company'] = company
    job_item['Location'] = location
    job_item['Posted time'] = posted_time
    job_item['Number of applicants'] = num_applicant
    job_item['Senority level'] = senority
    job_item['Job function'] = job_func
    job_item['Employee type'] = emp_type
    job_item['Industries'] = industries

    return job_item


def get_title(soup):
    title = soup.find('div', {'class', 'topcard__content-left'})
    title_content = title_process(str(title))

    print('\n', title_content)
    return title_content


def get_company(soup):
    comp = soup.find('div', {'class', 'topcard__content-left'})
    company = company_process(str(comp))
    return company


def get_location(soup):
    loc = soup.find('div', {'class', 'topcard__content-left'})
    location = location_process(str(loc))
    return location


def get_posted_time(soup):
    ptime = soup.find('div', {'class', 'topcard__content-left'})
    postime = postime_process(str(ptime))
    return postime


def get_numap(soup):
    numap = soup.find('div', {'class', 'topcard__content-left'})
    num_applicant = num_applicant_process(str(numap))
    return num_applicant


def get_description(soup):
    info = soup.find(
        'div', {'class', 'show-more-less-html__markup'})
    info_content = str(info)[84:]
    newline = ['<ul><li>', '<li>', '<br>', '<br/>']
    blank = ['<strong>', '</strong>', '<p>', '</p>', '<em>', '</em>']
    info_content = replace_all(info_content, newline, '\n')
    info_content = replace_all(info_content, blank, ' ')

    return info_content


def get_criteria(soup):
    criteria = soup.findAll(
        'span', {'class', 'job-criteria__text job-criteria__text--criteria'})

    span_field = soup.findAll('h3', {'class', 'job-criteria__subheader'})
    span_field = str(span_field)
    span_field = span_field.replace(
        '<h3 class="job-criteria__subheader">', '').replace('</h3>', '')

    i = 0
    str_crit = str(criteria)
    senority = ''
    emp_type = ''
    job_func = ''
    industries = ''

    if 'Seniority level' in span_field:
        senority = senority_process(str(criteria[i]))
        i += 1

    if 'Employment type' in span_field:
        emp_type = emp_process(str(criteria[i]))
        i += 1

    if 'Job function' in span_field:
        job_func = jfunc_process(str(criteria[i]))
        i += 1

    if 'Industries' in span_field:
        industries = industries_process(str(criteria[i]))

    return senority, emp_type, job_func, industries


def title_process(str_title):
    begin = str_title.find('<h1')
    end = str_title.find('</h1>')
    temp1 = str_title[begin:end]

    begin2 = temp1.find('>')
    title = temp1[begin2+1:]
    return title


def location_process(str_loc):

    begin1 = find_nth_str(str_loc, '<span', 2)
    end = find_nth_str(str_loc, '</span>', 2)
    temp = str_loc[begin1:end]

    begin2 = temp.find('>')
    loc = temp[begin2+1:end]
    # print('loc:', loc)
    return loc


def company_process(str_comp):
    begin1 = str_comp.find('<a')
    end = str_comp.find('</a>')
    temp1 = str_comp[begin1:end]

    begin2 = temp1.find('>')
    comp = temp1[begin2+1:end]
    # print('comp:', comp)
    return comp


def postime_process(str_time):
    begin1 = find_nth_str(str_time, '<span', 3)
    end = find_nth_str(str_time, '</span>', 3)
    temp = str_time[begin1:end]

    begin2 = temp.find('>')
    time = temp[begin2+1:end]
    # print('time:', time)
    return time


def num_applicant_process(str_numap):
    begin1 = str_numap.find('<figcaption')
    end = str_numap.find('</figcaption>')
    temp1 = str_numap[begin1:end]

    begin2 = temp1.find('>')
    numap = temp1[begin2+1:end]
    # print('numap:', numap)
    return numap


def senority_process(str_sen):
    begin = str_sen.find('>')
    end = str_sen.find('</span>')

    return str_sen[begin+1:end]


def emp_process(str_emp):
    begin = str_emp.find('>')
    end = str_emp.find('</span>')

    return str_emp[begin+1:end]


def jfunc_process(str_jfunc):
    begin = str_jfunc.find('>')
    end = str_jfunc.find('</span>')

    return str_jfunc[begin+1:end]


def industries_process(str_indus):
    begin = str_indus.find('>')
    end = str_indus.find('</span>')

    return str_indus[begin+1:end]


def filter_data(dict):
    pass


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


def replace_all(text, dic, replace_char):
    for i in dic:
        text = text.replace(i, replace_char)
    return text


def find_nth_str(string, substring, n):
    if (n == 1):
        return string.find(substring)
    else:
        return string.find(substring, find_nth_str(string, substring, n - 1) + 1)


trade_spider()
