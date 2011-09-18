from django.db import models

class table_summary(models.Model):
    tblid = models.CharField(max_length=10, primary_key=True)
    seq = models.IntegerField()
    position = models.IntegerField()
    cells = models.CharField(max_length=15)
    title = models.CharField(max_length=255)
    subject_area = models.CharField(max_length=63)
    universe = models.CharField(max_length=255) 
    
    def __str__(self):
        return '%s: %s' % (self.tblid, self.title)     
    
class table_line(models.Model):
    tbl = models.ForeignKey(table_summary)
    seq = models.IntegerField()
    order = models.IntegerField()
    actual_order = models.IntegerField()
    title =  models.CharField(max_length=255)   
    
    def __str__(self):
        return '%s line %s: %s' % (self.tblid, self.order, self.title) 

# revised for 09 ACS. They appear to change the file format layout yearly.
# I've cut down the number of fields since 08, to reduce annual maintenance work...    
class geo_area(models.Model):    
    fileid = models.CharField(max_length=6, null=True, blank=True)
    stusab = models.CharField(max_length=2, null=True, blank=True)
    sumlevel = models.CharField(max_length=3, null=True, blank=True)
    component =models.CharField(max_length=2, null=True, blank=True)
    logrecno = models.CharField(max_length=7, null=True, blank=True)
    us = models.CharField(max_length=1, null=True, blank=True)
    region = models.CharField(max_length=1, null=True, blank=True)
    division = models.CharField(max_length=1, null=True, blank=True)
    statece = models.CharField(max_length=2, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True)
    county = models.CharField(max_length=3, null=True, blank=True)
    cousub = models.CharField(max_length=5, null=True, blank=True)
    place =models.CharField(max_length=5, null=True, blank=True)
    tract =models.CharField(max_length=6, null=True, blank=True)
    blkgrp =models.CharField(max_length=1, null=True, blank=True)
    concit = models.CharField(max_length=5, null=True, blank=True)
    aianhh = models.CharField(max_length=4, null=True, blank=True)
    aianhhfp = models.CharField(max_length=5, null=True, blank=True)
    aihhtli = models.CharField(max_length=1, null=True, blank=True)
    aitsce = models.CharField(max_length=3, null=True, blank=True)
    aits = models.CharField(max_length=5, null=True, blank=True)
    anrc = models.CharField(max_length=5, null=True, blank=True)
    cbsa = models.CharField(max_length=5, null=True, blank=True)
    csa = models.CharField(max_length=3, null=True, blank=True)
    metdiv = models.CharField(max_length=5, null=True, blank=True)
    macc = models.CharField(max_length=1, null=True, blank=True)
    memi = models.CharField(max_length=1, null=True, blank=True)
    necta =models.CharField(max_length=5, null=True, blank=True)
    cnecta = models.CharField(max_length=3, null=True, blank=True)
    nectadiv = models.CharField(max_length=5, null=True, blank=True)
    ua = models.CharField(max_length=5, null=True, blank=True)
    uacp = models.CharField(max_length=5, null=True, blank=True)
    cdcurr = models.CharField(max_length=2, null=True, blank=True)
    sldu = models.CharField(max_length=3, null=True, blank=True)
    sldl = models.CharField(max_length=3, null=True, blank=True)
    submcd = models.CharField(max_length=2, null=True, blank=True)
    sdelm =models.CharField(max_length=5, null=True, blank=True)
    sdsec =models.CharField(max_length=5, null=True, blank=True)
    sduni =models.CharField(max_length=5, null=True, blank=True)
    ur = models.CharField(max_length=1, null=True, blank=True)
    pci = models.CharField(max_length=1, null=True, blank=True)
    puma5 =models.CharField(max_length=5, null=True, blank=True)
    geoid = models.CharField(max_length=40, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    
    
    def __str__(self):
        return '%s' % (self.name)