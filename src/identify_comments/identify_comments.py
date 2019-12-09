import re 


class SeparateCode(object): 
  SEPARATORS = {
    'py':('#','"""','"""'),
    'default':('//','/*','*/')
  }

  def __init__(self,code,language):
    self.code = code
    self.language = language

  def get_language(self):
    if self.language in self.SEPARATORS:
      return self.language
    else:
      return 'default'

  def get_one_line_separator(self):
    return self.SEPARATORS[self.get_language()][0]

  def get_init_line_separator(self):
    return self.SEPARATORS[self.get_language()][1]

  def get_end_line_separator(self):
    return self.SEPARATORS[self.get_language()][2]

  def identify_comments(self):
    (comments,code) = self.separate_comments()
    return (self.remove_blanc_lines(comments),self.remove_blanc_lines(code))

  def remove_blanc_lines(self,code):
    return "\n".join([s.strip() for s in code.strip().splitlines(True) if s.strip()])

  def separate_comments(self):
    code = self.code
    regex = r"("+re.escape(self.get_one_line_separator())+r".*)|('(?:\\\\[^']|\\\\'|.)*?')|(\"(?:\\\\[^\"]|\\\\\"|.)*?\")|("+re.escape(self.get_init_line_separator())+r"(?:.|[\n\r])*?"+re.escape(self.get_end_line_separator())+r")"
    #print(regex)
    split = re.split(regex,code,0, re.MULTILINE)
    comments = ""
    separated_code = ""
    #print(split)pdflatex
    for s in split:
      
      if s == None or s == '': 
        continue
      if s.startswith(self.get_one_line_separator()) or s.startswith(self.get_init_line_separator()):
        #print(s)
        comments += s + '\n'
      else:
        separated_code += s
    return re.sub(r'//|/\*|\*/|\*','',comments),re.sub(r'//|/\*|\*/','',separated_code)
    

#f = open('../scrapper/repos/TypeScript/scripts/tslint/rules/noDoubleSpaceRule.ts','r')
#separator = SeparateCode(f.read(), 'js') 


#print(separator.identify_comments())

import os
path = "../scrapper/repos/"

LANGUAGES = ['.java','.c','.cpp','.js','.ts','.py','.php', '.cs']

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

if __name__ == "__main__":
    separate_all()