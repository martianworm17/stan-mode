import json
import os
import re
import glob
from os import path

FILE = 'stan_lang.json'
DST = '../snippets/stan-mode'
FUNCTION_DIR = path.join(DST, 'functions')
DIST_DIR = path.join(DST, 'distributions')

DISTRIBUTION_PARTS = ('Discrete Distributions', 'Continuous Distributions')

TEMPLATE = """# name: {funcname}({sig})
# key: {funcname}
# group: {group}
# --
{funcname}({args})$0
"""

def dir_create_or_clean(dst):
    if not path.exists(dst):
        print("creating directory %s" % dst)
        os.makedirs(dst)
    else:
        print("deleting files in %s" % dst)
        for filename in glob.glob("*.yasnippet"):
            os.unlink(filename)

def make_sig(x):
    if x['argtypes']:
        return ', '.join(x['argtypes'])
    else:
        return ''

def make_dist_sig(x):
    if x['argtypes']:
            return ', '.join(x['argtypes'][1:])
    else:
        return ''

def make_args(x):
    if x['argnames']:
        return ', '.join(['${%d:%s}' % (y[0] + 1, ' '.join(y[1])) 
                          for y in enumerate(zip(x['argtypes'], x['argnames']))])
    else:
        return ""

def make_dist_args(x):
    if x['argnames']:
        return ', '.join(['${%d:%s}' % (y[0] + 1, ' '.join(y[1])) 
                          for y in enumerate(zip(x['argtypes'][1:], x['argnames'][1:]))])
    else:
        return ""

def make_group_function(x):
    return 'Functions.%s' % '.'.join(y for y in x['location'] if y)

def make_group_dist(x):
    return 'Distributions.%s' % x['location'][0].split()[0]

def write_function_snippets(functions):
    dir_create_or_clean(FUNCTION_DIR)
    for funcname, sigs in functions.items():
        if not re.match("operator", funcname):
            for sig, v in sigs.items():
                filename = path.join(FUNCTION_DIR,
                                     '%s-%s.yasnippet' % (funcname, sig.replace(',', '-')))
                snippet = TEMPLATE.format(funcname = funcname,
                                          sig = make_sig(v),
                                          args = make_args(v),
                                          group = make_group_function(v))
                with open(filename, 'w') as f:
                    f.write(snippet)
            
def write_distribution_snippets(functions):
    dir_create_or_clean(DIST_DIR)
    for funcname, sigs in functions.items():
        if (not re.search("_ccdf_log$", funcname)
            and not re.search("_cdf_log$", funcname)
            and re.search("_log$", funcname)):
            for sig, v in sigs.items():
                if v['location'][0] in DISTRIBUTION_PARTS:
                    filename = path.join(DIST_DIR,
                                         '%s-%s.yasnippet' % (funcname, sig.replace(',', '-')))
                    snippet = TEMPLATE.format(funcname = funcname,
                                              sig = make_dist_sig(v),
                                              args = make_dist_args(v),
                                              group = make_group_dist(v))
                    with open(filename, 'w') as f:
                        f.write(snippet)
        
if __name__ == '__main__':
    with open(FILE, 'r') as f:
        data = json.load(f)
    write_function_snippets(data['functions'])
    write_distribution_snippets(data['functions'])
