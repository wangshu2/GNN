#Add pythoscape path
import sys
pythoscape_path = '/home/socr/b/suwenzhao'
sys.path.append(pythoscape_path)

#Find MySQL password
cnf_path = '/home/socr/b/suwenzhao/.my.cnf'
with open(cnf_path) as f:
  f.next()
  line = f.next()
  line = line.strip().split('=')
  mysql_pass = line[1]

#Imports
import interface.mysql_interface as m_i
from auxilary.re_patterns import RE_PATTERNS

#Interfaces
my_interface = m_i.mysql_interface('suwenzhao',mysql_pass,'pyscape_suwen',port=13308,host='mysql-dev.cgl.ucsf.edu')
my_pytho = env.PythoscapeEnvironment(my_interface)

#Query
edge_query = my_interface.Edge(filter=my_interface.Filter(filter_name='-log10(E)',direction='>',filter_value=<value>))

i = 0
for edge in my_interface.pull(edge_query):
  i +=1
print i