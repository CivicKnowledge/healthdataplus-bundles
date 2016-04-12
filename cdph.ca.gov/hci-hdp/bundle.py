# -*- coding: utf-8 -*-
import ambry.bundle


class Bundle(ambry.bundle.Bundle):


    def meta_copy_partitions(self):
        from six import text_type
        from ambry.orm.exc import NotFoundError

        ref_b = self.library.bundle(self.source('hci').ref)

        for p in ref_b.partitions:
            
            if p.grain == 'county':

                try:
                    s = self.source(p.identity.vid)
                    print s.name, s.ref
                except NotFoundError:
                    self.log("Copy in as source: {}".format(p.identity.name))
                    self.dataset.new_source(name=p.table.name, 
                                            dest_table_name=p.table.name, 
                                            reftype='partition', 
                                            ref=text_type(p.identity.name))

        self.build_source_files.sources.objects_to_record()

        self.commit()
        
    def check_strata(self):
        
        for p in self.partitions:
            if 'strata_name' in p.table.header:
                print '----', p.name
                
                df = p.dataframe()
            
                print 'strata_name',df.strata_name.unique()
                print 'strata_level_name',df.strata_name.unique()