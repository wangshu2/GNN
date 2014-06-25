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
import main.environments as env
from auxilary.re_patterns import RE_PATTERNS
import plugin.input.import_sequences as i_s
import plugin.output.output_table_runs as o_t_r
import plugin.input.add_blast_files as a_b_f
import plugin.output.output_xgmml as o_x
import plugin.output.output_attribute_tables as o_a_t
import plugin.input_bio.add_uniprot_info as a_u_i
import plugin.input.add_attribute_table as i_a_t
import plugin.add_context_sequences as a_c_s

#Interfaces
my_interface = m_i.mysql_interface('suwenzhao',mysql_pass,'pyscape_suwen',port=13308,host='mysql-dev.cgl.ucsf.edu')
my_pytho = env.PythoscapeEnvironment(my_interface)

#Plugins

#Step 1: Add pfam sequences
#plugin_1 = i_s.ImportFromFastaFile(<file name>,id_re=RE_PATTERNS['Uniprot/Pfam'],id_name='UniprotKB')

#Step 2: Output Uniprot ids to find GIs
#plugin_2 = o_a_t.OutputIdentifierTable(<file name>)

#Step 3: Get GIs from Uniprot

#Step 4: Input GIs
#plugin_4 = i_a_t.ImportIdentifierTable('UniprotKB','GI',<file name>)

#Step 5: Get adjacent sequences
#plugin_5 = a_c_s.AddNearbyGIs('GI',10,'/databases/mol/blast/db/nr','/home/socr/c/users2/abarber/blastplus/ncbi-blast-2.2.25+-src/c++/GCC412-Debug64/bin/blastdbcmd')

#Step 6: Output edges to run on shared cluster
#plugin_6 = o_t_r.SequenceTableRun(<output directory>,100000)

#Step 7: Run edges on shared cluster

#Step 8: Input edges to Pythoscape
#plugin_8 = a_b_f.AddBLASTEdgesFromTableRun(<same output directory as in above>,include_atts=['% id','alignment_len','-log10(E)'])

#Step 9: Output GIs to find Uniprot ids
#plugin_9 = o_a_t.OutputIdentifierTable(<file name>)

#Step 10: Get Uniprot ids from Uniprot

#Step 11: Input uniprot ids
#plugin_11 = i_a_t.ImportIdentifierTable('GI','UniprotKB',<file name>)

#Step 12: Download information from Uniprot using list from 10

#Step 13: Upload information into Pythoscape 
#plugin_13 = a_u_i.ImportFromUniProtFile(<file name>)

#Step 14: Use query script to find a good threshold for the network

#Step 15: Output network
#plugin_15 = o_x.OutputXGMML(<network file name>,<network file title>,filt_name='-log10(E)',filt_dir='>',filt_value=<appropriate value>)

#Execute
my_pytho.execute_plugin(plugin_1)
