import os
import csv
path = "../separated_files"
LANGUAGES = ['.java','.c','.cpp','.js','.ts']


#files = {}
#for l in LANGUAGES:
#  lan = l[1:]
#  f = open('final_data/'+l+'.csv')

def get_language(f_name):
  for l in LANGUAGES:
    if f_name.endswith(l):
      return l[1:]
  return None

#def create_array(arr, s, code, lang):
#  for line in s.splitlines():
#    if len(line) > 3:
#      arr.append((lang,line,code))


def combine_all_files():
  arr = []
  for root,d_names,f_names in os.walk(path+'/comments'):
    for f_name in f_names:
      lang = get_language(f_name)
      f = open(root+'/'+f_name,'rb')
      for line in f:
        if len(line) > 3:
          arr.append((lang,line[:-1].lower(),0))
      f.close()
      
      

  for root,d_names,f_names in os.walk(path+'/code'):
    for f_name in f_names:
      lang = get_language(f_name)
      f = open(root+'/'+f_name,'rb')
      for line in f:
        if len(line) > 3:
          arr.append((lang,line[:-1].lower(),1))
      f.close(done)
      


  with open('../final_data/data.csv','w') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['language','line','is_code'])
    csv_out.writerows(arr)

combine_all_files()