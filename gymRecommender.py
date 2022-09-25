from typing import Dict, List
'''
    Input ->
        Users who participated in those gyms
        Users who didn't participate in those gyms
        Duration Range
        Difficulty Range 
        Problems Number Range
    Output <-
        Gyms and How the users entered preformed in them
'''

from CFReqeuster import cf_request
import time

class UserPerformance:
    handle: List[str]
    penalty: int
    rank: int
    type: str
    problems_solved: List[int] = []
    topics_solved: List[str] = []
    
    def __init__(self, data):
        self.handle = data['party']['members'].values()
        self.penalty = data['penalty']
        self.rank = data['rank']
        self.type = data['praty']['participantType']
        
        for index, problem in enumerate(data['problemResults']):
            if problem['points'] > 0:
                self.problems_solved.append(index)
    
    
class GYM:
    id_gym: int
    name: str
    prob_num: int
    difficulty: int
    duration: float
    number_of_contestants: int = 0
    problems_freq: Dict[int, int] = dict()
    topics_list: List[str] = []
    data: List[UserPerformance] = []
    
    def __init__(self, data, users):
        self.id_gym = data['contest']['id']
        self.name = data['contest']['id']
        self.difficulty = data['contest']['difficulty']
        self.duration = data['contest']['durationSeconds'] / 60 / 60
        self.prob_num = len(data['problems'])
        for record in data['rows']:
            problems = int(record['points'])
            if record['party']['participantType'] != 'PRACTICE':
                self.number_of_contestants += 1
                data[problems] = data.get(problems, 0) + 1
            if len(set(record['party']['members'].values()) and users) != 0:
                data.append(UserPerformance(record))
                
        
        

def count_enter(records: List, handles: set) -> int:
    res = set()
    for entry in records:
        res = res or (handles and set(entry['party']['members'].values()))
    return len(res)

def get_gym_recommendations(entered: List[str] = [], didnt_enter: List[str] = [],
                            duration: List[int] = [4*60*60,5*60*60], difficulty: List[int] = [3,4],
                            problems: List[int] = [11,15]) -> List[GYM]:
    entered = set(entered)
    didnt_enter = set(didnt_enter)
    contest_list = cf_request('contest.list?', [['gym','true']])
    contest_list = [entry for entry in contest_list 
    if duration[0] <= entry.get('durationSeconds', 0) <= duration[1]
    and difficulty[0] <= entry.get('difficulty',-1) <= difficulty[1]]
    standing_list : List[GYM] = []
    cnt = 0
    print(len(contest_list))
    for entry in contest_list:
        contest_data = None
        for i in range(0,5):
            contest_data = cf_request('contest.standings?', [['contestId', str(entry['id'])], ['showUnofficial','true']])
            if contest_data:
                if (
                    problems[0] <= len(contest_data['problems']) <= problems[1]
                    and count_enter(contest_data['rows'], entered) == len(entered)
                    and count_enter(contest_data['rows'], didnt_enter) == 0
                    ):            
                    standing_list.append(GYM(contest_data, entered))
                break
            else:
                time.sleep(1)
        cnt += 1
        print(cnt)


if __name__ == '__main__':
    get_gym_recommendations()