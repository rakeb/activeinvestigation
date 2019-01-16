"""
author: Md Mazharul Islam
email: mislam7@uncc.edu, rakeb.mazharul@gmial.com

site: https://domain-reputation-api.whoisxmlapi.com/docs
user: rakeb.void
account type: free
url type: https://domain-reputation-api.whoisxmlapi.com/api/v1?apiKey=&domainName=google.com
"""

import pickle

import base_request

API_KEY = ''
INPUT_DOMAIN_LIST = 'domain_list'


# domainName = ''


def read_input_file():
    with open(INPUT_DOMAIN_LIST) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    return content


def load_reputation_matrix():
    try:
        with open('reputation_matrix',
                  'rb') as i:
            credential = pickle.load(i)
            return credential
    except:
        raise ('Exception occurred while reading reputation_matrix\n')


def save_reputation_matrix(rep):
    with open('reputation_matrix',
              'wb') as output:
        pickle.dump(rep, output, pickle.HIGHEST_PROTOCOL)
        print("reputation_matrix saved for further use.\n")


def get_reputation(domain_name):
    # {
    #     "reputationScore": 98.67
    # }
    url_custom = 'https://domain-reputation-api.whoisxmlapi.com/api/v1?apiKey=' + API_KEY + '&domainName=' + domain_name
    response = base_request.get_request(url_custom)
    return response


def calculate_reputation():
    lines = read_input_file()

    try:
        reputation_matrix = load_reputation_matrix()
    except:
        reputation_matrix = {}

    for domain_name in lines:
        if not reputation_matrix or not (domain_name in reputation_matrix):
            response = get_reputation(domain_name)
            r_score = response['reputationScore']
            reputation_matrix[domain_name] = r_score
            print(domain_name, reputation_matrix[domain_name])
        else:
            print('Printing form saved')
            print(domain_name, reputation_matrix[domain_name])
    save_reputation_matrix(reputation_matrix)


if __name__ == '__main__':
    calculate_reputation()
