#!/bin/csh
#$ -S /bin/csh
#$ -cwd
#$ -o sge-logs
#$ -e sge-logs
#$ -j y
#$ -R y
#$ -l scratch=512M
#$ -l mem_free=512M
#$ -l arch=lx24-amd64
#$ -l h_rt=72:00:00
#$ -t 1-52

#Set -t above to the appropriate value of runs.

#Output date and hostname
date
hostname

#These variables must be set --
#BLASTEXEDIR needs to point to the directory where the blastp executable is.
#HOMEDIRECTORY needs to point to the directory where the table files, sequence file, and python script are. Outputs will be copied here as well.
#SEQUENCEFILE needs to be set to the sequence file name.
set BLASTEXEDIR = /netapp/home/abarberi/programs/blastplus/ncbi-blast-2.2.24+-src/c++/ReleaseMT/bin
set HOMEDIRECTORY = /netapp/home/suwenzhao/PdxA
set SEQUENCEFILE = sequences.fa

#Don't touch the next line!
set TASKID = 0

#Set the zero here to another value if you are doing incremented runs.
@ TASKID = $SGE_TASK_ID + 0

#The rest of the code doesn't need to be modified.

setenv TMPDIR 
setenv TMPDIR `mktemp -d -p /scratch`

cp $HOMEDIRECTORY/$SEQUENCEFILE /$TMPDIR
cp $HOMEDIRECTORY/$TASKID.tab /$TMPDIR
cp $BLASTEXEDIR/blastp $TMPDIR
cp $HOMEDIRECTORY/parallel_blast2seq.py /$TMPDIR

cd $TMPDIR
python parallel_blast2seq.py $TASKID.tab $SEQUENCEFILE $TASKID.out 

cd $HOMEDIRECTORY
cp $TMPDIR/$TASKID.out ./
rm -rf $TMPDIR
     
