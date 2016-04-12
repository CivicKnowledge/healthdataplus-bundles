# -*- coding: utf-8 -*-
# Ambry Bundle Library File
# Use this file for code that may be imported into other bundles

def load_groups(b, group_name):
    
    with b.source_fs.open('groups.txt') as f:
        for l in f:
            l = l.strip()
            if l.startswith(group_name):
                _, table = l.split()
                yield table