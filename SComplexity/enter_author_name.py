#SComplexity.t_analysis
from SComplexity import online_app_backend
import argparse
'''
parser = argparse.ArgumentParser(description='Process some authors.')

parser.add_argument("-H", "--Help", help = "Example: Help argument", required = False, default = "")

parser.add_argument('author','--a',metavar='N', type=str, nargs='+',required=True,help='authors first name')
parser.add_argument('t','--t', metavar='N', type=str, nargs='+',help='boolean to select a tournment between authors')

parser.add_argument('a2', metavar='N', type=str, nargs='+',help='second author',required=False)
parser.add_argument('v','--verbose', help='Print more data',action='store_true',required=False)
parser.add_argument('an','--anonymize', help='Anonymize loosing author or both authors in competition plot',action='store_true',default="True",required=False)
args = parser.parse_args()
NAME = args.author
TOUR = args.t
author2 = args.a2
verbose = args.v
anon = args.an
print(NAME)
'''
TOUR = False
if TOUR:
    NAME1 = args.author1
    online_app_backend.call_from_front_end(NAME,NAME1=author2,tour=TOUR,anon=anon,verbose=verbose)
else:
    NAME = "S S Phatak"
    verbose = False
    online_app_backend.call_from_front_end(NAME,verbose=verbose)
