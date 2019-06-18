#SComplexity.t_analysis
from SComplexity import online_app_backend
import argparse

parser = argparse.ArgumentParser(description='Process some authors.')
parser.add_argument('author', metavar='N', type=str, nargs='+',
                   help='authors first name')

args = parser.parse_args()

NAME = args.author
online_app_backend.call_from_front_end(NAME)
