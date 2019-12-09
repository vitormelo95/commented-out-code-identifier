from identify_comments import SeparateCode
from model import IdentifyCommentedOutCode
import os
import re
import git
import math

path = "/home/vitormelo/poc/scrapper/repos2/"
LANGUAGES = ['.java','.c','.cpp','.js','.ts']
N_RELEASES = 6

#f_names = ['../scrapper/repos/akka/akka-distributed-data/src/main/java/akka/cluster/ddata/protobuf/msg/ReplicatorMessages.java']

class ReadFilesIter(object):
  def __iter__(self):
    dirs = os.listdir(path)
    for d in dirs:
      try:
        project_path = path+d+'/'
        print(project_path)
        releases = get_releases(project_path)
        for i,r in enumerate(releases):
          checkout(project_path,r)
          for root,d_names,f_names in os.walk(project_path):
            try:
              for f_name in f_names:
                if '.min.' not in f_name and any(f_name.endswith(l) for l in LANGUAGES): 
                  print('Separating File: ' + f_name)
                  complete_path = root+'/'+f_name
                  #complete_path = f_name
                  f = open(complete_path,'r')
                  code = f.read()
                  yield code,complete_path,r,i,d
            except Exception as ex:
              print(ex)
      except Exception as ex:
        print(ex)
      

class SeparateCodeIter(object):
  def __iter__(self):
    for (code,f_name,release,release_number, d) in ReadFilesIter():
      try:
        separator = SeparateCode(code,f_name.split('.')[-1])
        (comments,separated_code) = separator.identify_comments()
        yield code, f_name, release,release_number, d, comments, separated_code
      except Exception as ex:
        print(ex)
      


class IdenfifyCommentedOutCodeIter(object):
  def __iter__(self):
    identifier = IdentifyCommentedOutCode()
    for (code, f_name, release, release_number, d, comments, separated_code) in SeparateCodeIter():
      try:
        comments = [f for f in filter(lambda s: s.strip() is not None and s.strip() != "" and len(s.strip()) >1, comments.split('\n'))]

        predicts = identifier.predict(comments)
        
        total_comments = len(comments)
        code_clean = [f for f in filter(lambda s: s.strip() is not None and s.strip() != "", code.split('\n'))]
        total_lines_file = len(code_clean)
        commented_out_code = 0
        normal_comment = 0
        i = 0

        for p in predicts:
          if p == 1:
            print(comments[i] +" - "+ str(p))
            commented_out_code += 1
          else:
            normal_comment += 1
          i+=1
        yield d,release,release_number,f_name,total_lines_file, total_comments, normal_comment, commented_out_code

      except Exception as ex:
        print(ex)

def checkout(path,tag):
  repo = git.Git(path)
  repo.checkout(tag)

def get_releases(path):
  repo = git.Repo(path)
  tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
  releases = []
  if len(tags) < N_RELEASES:
    return releases
  else:
    step = len(tags)/N_RELEASES
    for i in range(N_RELEASES):
      releases.append(tags[math.ceil(i*step)])
    return releases

if __name__ == "__main__":
  output_file = open("output2.csv","w")
  output_file.write("project,release, release_number,file,total_lines,total_comments,normal_comments,commented_out_code\n")
  i = 0
  for p in IdenfifyCommentedOutCodeIter():
    try:
      print("{},{},{},{},{},{},{},{}".format(*p))
      output_file.write("{},{},{},{},{},{},{},{}\n".format(*p))
      if(i % 100 == 0):
        output_file.flush()
    except Exception as ex:
        print(ex)
    
  output_file.close()
