# -*- coding: utf-8 -*-
import ambry.bundle
from ambry.util import memoize


from ambry.bundle.events import *

class Bundle(ambry.bundle.Bundle):
    pass
    
    
    @property
    @memoize
    def counties(self):
        from geoid.acs import AcsGeoid
        from geoid.civick import GVid, State
        
        
        d =  {AcsGeoid.parse(row.geoid).county_name.medium_name:str(AcsGeoid.parse(row.geoid).convert(GVid) )
                for row in self.dep('geofile50') if row.state == 6}
         
        d['California'] = State(6)
        
        return d
         
         
    def map_county(self, row):
        
        return  self.counties.get(row.region)
        
    
    def mangle_dollars(self, v):
        
        try:
            return str(v).replace('$','').replace(',','')
        except:
            return None
    

    def select_county_partition(self, source, row):
        "Selects a partition for the combined source, as configured in the pipelines in the bundle.yaml file"
        
        from ambry.identity import PartialPartitionName
        
        return PartialPartitionName(table='prek_enrollment', grain='county',
                                    space=row.county)
        
        
    def select_county_cols_partition(self, source, row):
        "Selects a partition for the combined source, as configured in the pipelines in the bundle.yaml file"
        
        from ambry.identity import PartialPartitionName
        
        return PartialPartitionName(table='prek_enrollment_combined', grain='county',
                                    space=row.county)
    
        
    @after_build(4)
    def describe_partitions(self):
        
        for p in self.partitions:
            if p.grain != 'county' or not p.space:
                self.log("Skipping describe_partitions for {} ".format(p.name))
                continue
                
            p.title = 'Pre-K Enrollment for {} County'.format(p.space.title())
            
        self.commit()
    



        
                
            
                
            
            
            
