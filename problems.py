import json
from re import sub
import requests
import random
from typing import List

head = { 'apiKey' : '',
         'Content-Type' : 'application/json' }

def get_problems_solved_by_Users(users:List[str], tag:str = None):
    try:
        for user in users:
            url = 'https://codeforces.com/api/user.status?handle='+user+'&from=1&count=1000000'
            response = requests.get(url=url, headers = head)
            print(response)
            listOfAc = list(filter(lambda x : x['verdict'] == 'OK', response.json()['result'])) 
            SolvedSet = set()
            for submission in listOfAc: 
                if 'contestId' in submission['problem'].keys() and (tag == None or tag in submission['problem']['tags']):
                    SolvedSet.add(str(submission['problem']['contestId']) + submission['problem']['index'])
        return SolvedSet
    except Exception as e:
        print('eeeeSolved: ', e)


def get_problems_candidates(users:List[str], l: int, r: int, tag:str = None) :
    
    SolvedSet = get_problems_solved_by_Users(users=users, tag=tag)

    try:
        url = 'https://codeforces.com/api/problemset.problems'
        if tag: 
            url += '?tags=' + tag

        response = requests.get(url=url, headers = head)

        toGiveUser = []
        n = len(response.json()['result']['problems'])
        for problem in response.json()['result']['problems']:
            if 'rating' in problem.keys() and problem['rating'] >= l and problem['rating'] <= r  and (not (str(problem['contestId']) + problem['index']) in SolvedSet):
                if problem['contestId'] > 1000:
                    toGiveUser.append(problem)

        return toGiveUser

    except Exception as e:
        print('eeeeProblem: ', e)


candidates = get_problems_candidates(['DeadlyPilow', 'KNB.', 'darked'], 2400, 2600)
random.shuffle(candidates)
print(len(candidates))

problems = []

for i in range(0,len(candidates)):
    problems.append(str(candidates[i]['contestId']) + '/' + candidates[i]['index'])

print(problems)



