'''
Description: This program is meant to be called by an accompanying shared cluster script file to run Blast2Seq
batches and output the results.
'''

import sys
import subprocess
import os
import math

def write_fa(fa_file,name,seq):
    f = open(fa_file,'w')
    f.write(''.join(['>',str(name),'\n']))
    f.write(''.join([seq,'\n']))
    f.close()
    
def read_in_fa(fa_file):
    f = open(fa_file)
    seqs = {}
    for line in f:
        line = line.strip()
        if line and line[0] == '>':
            curr_seq = line[1:]
            seqs[curr_seq] = ''
        elif line:
            seqs[curr_seq] = ''.join([seqs[curr_seq],line])
    return seqs

def write_data_table(data,table_name,filter):
    f = open(table_name,'w')
    f.write('seq_1 seq_2 bit_score m*n alignment_len alignment_identities query_start query_end subject_start subject_end\n')
    for line in data:
        if line[2] != None:
            try:
                eval = -math.log10(line[3]) + line[2]*math.log10(2)
            except IndexError:
                pass
            else:
                if filter != None and eval < filter:
                    pass
                else:
                    f.write(' '.join([str(item) for item in line]+['\n']))
    f.close()

def pull_data(d_name,line,offset):
    s_line = line.strip().split(' ')
    bit_index = s_line.index(d_name)+offset
    return s_line[bit_index]

def read_blast_out(outfile):
    
    f = open('temp.out')
    score = None
    query_strt = None
    query_end = None
    sbjct_strt = None
    sbjct_end = None
    off_flag = False
    while 1:
        try:
            line = f.next()
        except StopIteration:
            break
        if len(line) > 6:
            first_six = line[:6]        
        else:
            first_six = None
        if not off_flag:
            if score == None and first_six == ' Score':    
                score = float(pull_data('bits',line,-1))
                line = f.next()
                identity_str = pull_data('Identities',line,2)
                ali_len = int(identity_str.split('/')[1])
                ali_iden = int(identity_str.split('/')[0])
            elif score != None and first_six == ' Score' :
                off_flag = True
            elif first_six == 'Query ' or first_six == 'Sbjct ' :
                start_num,end_num = None,None
                split_line = line.strip().split()
                if len(split_line) == 4: 
                    start_num = int(split_line[1])
                    end_num = int(split_line[3])
                if first_six == 'Query ' and start_num != None and query_strt == None:
                    query_strt = start_num
                elif first_six == 'Sbjct ' and start_num != None and sbjct_strt == None:
                    sbjct_strt = start_num
                if first_six == 'Query ' and end_num != None:
                    query_end = end_num
                elif first_six == 'Sbjct ' and end_num != None:
                    sbjct_end = end_num
        if first_six == 'Effect':
            e_ss = int(line.strip().split(' ')[4])
    if score != None:
        return [score,e_ss,ali_len,ali_iden,query_strt,query_end,sbjct_strt,sbjct_end]
    else:
        return [None]
            
def run_bl2seq(table_loc,seqs,gap_open,gap_extend,comp_based):
    
    if comp_based:
        comp_based = '2'
    else:
        comp_based = '0'
    f = open(table_loc)
    all_out = []
    for line in f:
        vars = line.strip().split()
        write_fa('seq1.fa',vars[0],seqs[vars[0]])
        write_fa('seq2.fa',vars[1],seqs[vars[1]])                           
        command = './blastp -query seq1.fa -subject seq2.fa -gapopen %s -gapextend %s -comp_based_stats %s -use_sw_tback > temp.out' % (gap_open,gap_extend,comp_based)
        p = subprocess.Popen(command,shell=True)
        sts = os.waitpid(p.pid, 0)[1]
        option_1 = read_blast_out('temp.out')
        command = './blastp -query seq2.fa -subject seq1.fa -gapopen %s -gapextend %s -comp_based_stats %s -use_sw_tback > temp.out' % (gap_open,gap_extend,comp_based)
        p = subprocess.Popen(command,shell=True)
        sts = os.waitpid(p.pid, 0)[1]
        option_2 = read_blast_out('temp.out')
        if option_1[0] != None and option_1[0]<option_2[0]:
            all_out.append(vars+option_1)
        else:
            all_out.append(vars+option_2)
    return all_out
        
if __name__== '__main__' :
    if len(sys.argv) < 4:
        print 'Incomplete function call -- parallel_blast2seq.py [table_file] [seq_file] [output_file] [Optional: --gap_open value] [Optional: --gap_extend value] [Optional: --comp_based True/False] [Optional: --filter -log10(E) filter]'
    else:
        table = sys.argv[1]
        seq_loc = sys.argv[2]
        output = sys.argv[3]
        gap_open = '11'
        gap_extend = '1'
        comp_based = True
        filter = None
        for i,arg in enumerate(sys.argv[4:]):
            if arg == '--gap_open': gap_open = str(int(sys.argv[i+5]))
            elif arg == '--gap_extend': gap_extend = str(int(sys.argv[i+5]))
            elif arg == '--comp_based':
                if sys.argv[i+5] == 'False': 
                    comp_based = False 
                else: 
                    comp_based = True
            elif arg == '--filter': filter = float(sys.argv[i+5])
        seqs = read_in_fa(seq_loc)
        data = run_bl2seq(table,seqs,gap_open,gap_extend,comp_based)
        write_data_table(data,output,filter)