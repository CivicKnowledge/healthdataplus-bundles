# -*- coding: utf-8 -*-
import ambry.bundle


class Bundle(ambry.bundle.Bundle):
    
    def nanisnone(self, v):
        
        if v == float('nan') or str(v) == 'nan':
            return None
        else:
            return v

