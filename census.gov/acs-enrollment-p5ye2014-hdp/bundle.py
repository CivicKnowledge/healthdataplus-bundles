# -*- coding: utf-8 -*-
import ambry.bundle


class Bundle(ambry.bundle.Bundle):
    pass
    


    def stderr(self, m):
        try:
            return m/1.645
        except TypeError as e:
            return None


    def rse(self, val, m):
        try:
            return round(m/1.645 / val * 100, 2)
        except (TypeError, ZeroDivisionError) as e:
            return None
    

    def pct(self, val,  total):
        
        if not total or total == 0:
            return None
        else:
            return round(float(val)/float(total) * 100 , 2)

    def pctrse(self, val, val_se, total, total_se):
        from math import sqrt
        try:
            
            r = (val/total) 
            
            try:
                se =  sqrt( (val_se**2 - ( r**2 * total_se**2)) ) / total
            except ValueError:
                se = sqrt( (val_se**2 + ( r**2 * total_se**2)) ) / total
            
            
            return round(se / r * 100 , 2)
            
        except Exception as e:
            
            return None

    def augment_schema(self):
        
        t = self.table('b14001')
        cols = list(t.columns)
        
        for c in cols:
            if c.sequence_id <  11 or c.parent:
                continue
              

            t.add_column(
                name = c.name + '_pct',
                valuetype = 'm/pct?',
                parent = c.name,
                transform = '||bundle.pct(val=row.{}, total=row.total)'.format(c.name),
                description = 'Percentage of {}, of '.format(c.description)
            )
            
            t.add_column(
                name = c.name + '_pct_rse',
                valuetype = 'e/rse?',
                parent = c.name,
                transform = '||bundle.pctrse(val=row.{0}, val_se=row.{0}_se, total=row.total, total_se=row.total_se)'.format(c.name),
                description = 'Relative standard error for percentage of: {}'.format(c.description)
            )
            
        self.update_schema()
        
                
            
                
            
            
            
