import pandas as pd
import matplotlib.pyplot as plt
import git
import os
import math
from sklearn.cluster import KMeans
import numpy as np

FILE = "./data/results.csv"
N_RELEASES = 6
path = "/home/vitormelo/poc/scrapper/repos/"

def load_data(file):
  return pd.read_csv(file)
  
def get_total(df, agg_dict):
  return df.agg(agg_dict)

def get_release_number(df):
  dirs = os.listdir(path)
  for d in dirs:
    try:
      project_path = path+d+'/'
      print(project_path)
      releases = get_releases(project_path)
      for i,r in enumerate(releases):
        print(d,r)
        df.loc[(df['project'] == d) & (df['release'] == str(r)), 'release_number'] = i
    except Exception as ex:
      print(ex)
  return df
    
def filter_repos(df):
  print(len(df['project'].unique()))
  for project in df['project'].unique():
    df_project = df[df['project'] == project ]
    if df_project['total_lines'].sum() < 1000 or len(df_project['release_number'].unique()) < 6:
      print('deleting ' + project)
      df = df.drop(df[df['project'] == project ].index)
  return df
  

def get_releases(path):
  repo = git.Repo(path)
  tags = sorted(repo.tags, key=lambda t:  t.commit.committed_datetime)
  releases = []
  if len(tags) < N_RELEASES:
    return releases
  else:
    step = len(tags)/N_RELEASES
    for i in range(N_RELEASES):
      releases.append(tags[math.ceil(i*step)])
    return releases 

if __name__ == "__main__":
  df = load_data(FILE)
  df = filter_repos(df)
  df = df.drop(df.columns[0], axis = 1) 
  print(df.head())
  df2 = load_data("output2.csv")
  df2 = filter_repos(df2)
  print(df2.head())
  
  df_final = df2.append(df)
 

  print(df_final.head())

  df_final.to_csv("results_final.csv", index = False)
  
  # print(len(df['project'].unique()))

  # agg_dict = {
  #   'total_lines':'sum',
  #   'total_comments':'sum',
  #   'normal_comments':'sum',
  #   'commented_out_code':'sum'
  # }
  
  # df_sum_by_project = get_total(df.groupby(['project','release_number','release']),agg_dict).sort_values(by=['project','release_number']).reset_index()
  # print(df_sum_by_project)

  # df_sum_by_project['out_code_tax'] = df_sum_by_project['commented_out_code']/df_sum_by_project['total_comments']
  # #df2 = df_sum_by_project[ df_sum_by_project['out_code_tax'] > 0.4]
  # #print(df2)

  # arr = []
  # for key, grp in df_sum_by_project.groupby(['project']):
  #   if any(np.isnan(grp['out_code_tax'].values)) :
  #     print("has nan "+key)
  #   else:
  #     arr.append(grp['out_code_tax'].values) 
    #plt.plot(grp['release_number'], grp['out_code_tax'])
  #arr = np.array(arr)

  #print(arr)
  #kmeans = KMeans(n_clusters=4, random_state=0).fit(arr)
  #print(kmeans.cluster_centers_)

  #cluster = kmeans.predict(arr)
  #print(cluster)

  #for project in df_sum_by_project['project'].unique():
  #  df_project = df_sum_by_project[df_sum_by_project['project'] == project]
  #  df_project.plot(x='release_number',y='out_code_tax')
  #plt.show()
  #df_sum = get_total(df.groupby(['release_number']),agg_dict)
  #print(df_sum.head())
  
  