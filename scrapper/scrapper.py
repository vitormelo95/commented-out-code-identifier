import requests
from git import Git
import json
import os

SEARCH_PARAMS = {
  'stars' : '>1000',
  'pushed': '>=2019-04-01',
  'created': '<=2017-04-01',
  'languages': [
    #'JAVASCRIPT',
    #'JAVA',
    #'PYTHON',
    'PHP',
    'C++',
    'C#',
    'TYPESCRIPT',
    #'SHELL',
    'C',
    'RUBY',
    'GO',
    'SWIFT',
    'SCALA',
    'OBJECTIVE-C'
  ]
}

def execute_request(url,params=""):
  resp = requests.get(url=url, params=params)
  return resp.json()

def search_repositories():
  for l in SEARCH_PARAMS['languages']:
    url = """https://api.github.com/search/repositories?q=stars:{star}
            +language:{language}+created:{created}+pushed:{pushed}
            &sort=stars&order=desc""".format(star=SEARCH_PARAMS['stars']
            ,language=l,created=SEARCH_PARAMS['created'],pushed=SEARCH_PARAMS['pushed'])
    url = url.replace('\n','').replace(' ','')
    print(url)
    reps = execute_request(url)
    clone_repositories(reps)
  
def clone_repositories(reps):
  
  if 'items' in reps:
  
    for rep in reps['items'][:10]:
      print(rep['full_name'])
      if not os.path.isdir('repos/'+rep['name'])  :
        try:
          Git('repos').clone(rep['git_url'])
        except Exception as e:
          print(e)
      


if __name__ == '__main__':
    search_repositories()