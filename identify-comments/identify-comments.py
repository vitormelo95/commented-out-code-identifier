import re 

SEPARATORS = {
  'py':('#','"""','"""'),
  'default':('//','/*','*/')
}

class SeparateCode(object):
  def __init__(self,code,language):
    self.code = code
    self.language = language

  def get_language(self):
    if self.language in SEPARATORS:
      return self.language
    else:
      return 'default'

  def get_one_line_separator(self):
    return re.escape(SEPARATORS[self.get_language()][0])

  def get_init_line_separator(self):
    return re.escape(SEPARATORS[self.get_language()][1])

  def get_end_line_separator(self):
    return re.escape(SEPARATORS[self.get_language()][2])

  def identify_comments(self):
    #self.code = remove_blanc_lines()
    (comments,code) = self.separate_comments()
    return (self.remove_blanc_lines(comments),self.remove_blanc_lines(code))

  def remove_blanc_lines(self,code):
    return "\n".join([s.strip() for s in code.strip().splitlines(True) if s.strip()])

  def separate_comments(self):
    code = self.code
    regex = r"("+self.get_one_line_separator()+r".*)|('(?:\\\\[^']|\\\\'|.)*?')|(\"(?:\\\\[^\"]|\\\\\"|.)*?\")|("+self.get_init_line_separator()+r"(?:.|[\n\r])*?"+self.get_end_line_separator()+r")"
    #print(regex)
    split = re.split(regex,code,0, re.MULTILINE)
    comments = ""
    separated_code = ""
    #print(split)
    for s in split:
      #print(s)
      if s == None or s == '': continue
      if s.startswith('/*') or s.startswith('//'):
        comments += s + '\n'
      else:
        separated_code += s
    return re.sub(r'//|/\*|\*/|\*','',comments),re.sub(r'//|/\*|\*/','',separated_code)
    

f = open('../scrapper/repos/TypeScript/scripts/tslint/rules/noDoubleSpaceRule.ts','r')
separator = SeparateCode(f.read(), 'js') 


print(separator.identify_comments())

import os
path = "../scrapper/repos/"

LANGUAGES = ['.java','.c','.cpp','.py','.js','.ts']

def separate_all():
  for root,d_names,f_names in os.walk(path):
    for f_name in f_names:
      if '.min.' not in f_name and any(f_name.endswith(l) for l in LANGUAGES) : 
        print('Separating File: ' + root+'/'+f_name)
        f = open(root+'/'+f_name,'r')
        code = f.read()
        #print(code)
        f.close()
        separator = SeparateCode(code,f_name.split('.')[-1])
        (comments,separated_code) = separator.identify_comments()
        #print(comments)
        #print('\n-------------------------\n')
        #print(separated_code)
        f_code_dest = open('../separated_files/code/'+f_name,'w')
        f_code_dest.write(separated_code)
        f_code_dest.flush()
        f_code_dest.close()
        f_comment_dest = open('../separated_files/comments/'+f_name,'w')
        f_comment_dest.write(comments)
        f_comment_dest.flush()
        f_comment_dest.close()


separate_all()