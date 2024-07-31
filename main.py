import requests
import re

# 配置
API_KEY = 'AIzaSyDVGWYSuDRMX3GTM6NxqAxX7AxW4vq8qNE'
SEARCH_ENGINE_ID = '45f1e3f35c4214993'
SEARCH_QUERY = 'gloves business contact email phone'
NUM_RESULTS = 10


def get_search_results(query, num_results):
    url = f'https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={SEARCH_ENGINE_ID}&num={num_results}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('items', [])
    else:
        print(f"Error: {response.status_code}")
        return []


def extract_contact_info(text):
    # 正则表达式用于提取电子邮件和电话号码
    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    phone_pattern = re.compile(r'\+?\d[\d -]{8,12}\d')

    emails = email_pattern.findall(text)
    phones = phone_pattern.findall(text)

    return emails, phones


def main():
    results = get_search_results(SEARCH_QUERY, NUM_RESULTS)

    for result in results:
        title = result.get('title')
        snippet = result.get('snippet')
        link = result.get('link')

        # 提取联系信息
        emails, phones = extract_contact_info(snippet)

        print(f'Title: {title}')
        print(f'Link: {link}')
        print(f'Emails: {", ".join(emails)}')
        print(f'Phones: {", ".join(phones)}')
        print('-' * 40)


if __name__ == '__main__':
    main()
