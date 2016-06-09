import re
import os
import scipy.optimize
import numpy as np
import argparse
import random
from argparse import RawTextHelpFormatter,SUPPRESS

parser = argparse.ArgumentParser(description='''Generates batch input files for Cassandra simulations. 

to execute:

python batch_input.py -f foo.inp -d foo.csv -s foo ''',formatter_class=RawTextHelpFormatter)
parser.add_argument('-s', help ="Input Species Name")
parser.add_argument('-f', help ="input template file")
parser.add_argument('-d', help ="Input data file (temp,N1,L1,N2,L2)")

def multiple_replace(dict, text):
    # This function was originally from plotAlpha.py by Ed. Maginn at Notre Dame
    # Create a regular expression from dictionary keys
    regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))
    # For each match, look-up corresponding value in dictionary
    return regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text)

args = parser.parse_args()
outputString=[]
#Checks to see if Files Exist
if args.f is not None:
    template = args.f
else:
    print('Error: Must supply template file')
    exit()
if args.d is not None:
    datafile = args.d
else:
    print('Error: CSV Data file must be provided!')
    exit()
if args.s is not None:
    species = args.s
else:
    print('Error: Must supply species name')
    exit()
stepsinsweep=1000
TEMP, N_B1, L_B1, N_B2, L_B2 = np.loadtxt(datafile, delimiter=',', unpack=True)



#Front End Presentation
print ('********************************************')
print ('*Welcome to the Cassandra Batch Initializer*')
print ('*-----Copyright 2016 Ezekiel Piskulich-----*')
print ('********************************************')

for i in range(0,len(TEMP)):
    print('********************************************')
    print('INPUT FOR TEMPERATURE {} GENERATED.'.format(TEMP[i]))
    # Calculates all things needed for batch files
    seed1 = int(100000000*random.random())
    seed2 = int(100000000*random.random())
    totmol = int(N_B1[i]+N_B2[i])
    print ('SEED1: {} SEED2: {}'.format(seed1, seed2))
    input = open(template).read()
    outputString.append(template.replace(template,"gemc."+species+"."+str(int(TEMP[i]))+".inp"))
    output = open(outputString[i], 'w')
    # Replace uppercase flags by whatever we need
    dict = {
            "AAA" : species,
            "BBB" : str(int(TEMP[i])),
            "CCC" : str(seed1),
            "DDD" : str(seed2),
            "EEE" : str(totmol),
            "FFF" : str(L_B1[i]),
            "GGG" : str(L_B2[i]),
            "HHH" : str(N_B1[i]),
            "III" : str(N_B2[i]),
            "JJJ" : str(stepsinsweep),
            }
    output.write(multiple_replace(dict,input))
    output.close()
    




print('****************END PROGRAM*****************')
