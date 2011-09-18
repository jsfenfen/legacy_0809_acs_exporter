# table lookup / dump methods: 
# find_table('search_term')
# table_metadata('tblid')
# dump_table('tblid', 'sumlevel')


import re, csv, codecs

from models import table_summary, table_line, geo_area

# includes dc, and us. US is whole us. 

# states with a '2' appended were converted with something like: 
# iconv -f mac -t UTF8 g20095az.txt > g20095az2.txt
state_list=['ak', 'al', 'ar', 'az', 'ca', 'co', 'ct', 'dc', 'de', 'fl', 'ga', 'hi', 'ia', 'id', 'il', 'in', 'ks', 'ky', 'la', 'ma', 'md', 'me', 'mi', 'mn', 'mo', 'ms', 'mt', 'nc', 'nd', 'ne', 'nh', 'nj', 'nm', 'nv', 'ny', 'oh', 'ok', 'or', 'pa', 'ri', 'sc', 'sd', 'tn', 'tx', 'us', 'ut', 'va', 'vt', 'wa', 'wi', 'wv', 'wy']
#state_list=['pa']

# Where the raw summary files from CB can be found. 
summary_dir = "/Users/jacobfenton/IRW/census_data/ACS/2009_5yr/raw_data/Tracts_Block_Groups_Only/"

#Where the formatted files will go once we've processed them.
format_dir = "/Users/jacobfenton/IRW/django_sites/1.1.1/broadband/workshop/acs_09_5yr/formatted"

# The formatted files will be output with this naming convention:
#  [format_prefix]_[table_id]_[summary_level]
# the format_prefix is the one the census uses in naming the summary files
# Eg: data from the 2008 1 year ACS for pennsylvania would have a format_prefix of 20081pa
# and table 'C17024' output at the county level ('050') with that format_prefix would go to: 20081pa_C17024_050.txt 
format_prefix = '20095'


def load_all():

    # This is just the excel file saved as a tab delimited text file.
#    infile = open("/Users/jacobfenton/IRW/django_sites/1.1.1/broadband/workshop/acs_09_5yr/Sequence_Number_and_Table_Number_Lookup.csv", "r")
    infile = "/Users/jacobfenton/IRW/django_sites/1.1.1/broadband/workshop/acs_09_5yr/Sequence_Number_and_Table_Number_Lookup.csv"
    outfile = open("merge_process.txt", "w") 
    reader = csv.reader(open(infile, "U"), dialect=csv.excel)   

    linenum = -1

    curtablename = ''
    curtableid = ''
    cursubjarea = ''
    curtableposition = -1
    
    curtable = None
    
    # skip header row
    reader.next()    
     
    for fields in reader:
        linenum = linenum+1    
        print "processing line " + str(linenum)    
        try:
            (fields[8])
        except:
            fields.append("")
        # ignore the first field, which is 'ACSSF' for every line in the file.
        (tblid, seq, order, position, cells, total, title, subject_area) = (fields[1], fields[2], fields[3], fields[4], fields[5], fields[6], fields[7], fields[8])
        if position:
            curtablename = title
            curtableid = tblid
            cursubjarea = subject_area
            curtableposition = position
            curseq = seq
            curcells = cells
            # it's a table header row. 
            print "Got table header %s , %s, %s, %s" % (curtableid, curtablename, cursubjarea, curtableposition)
                
        elif (title.find('Universe') > -1):
            # It's the table universe line
            print "Got table universe line %s: %s" % (linenum, fields[7])
            # we've got all the table info we need; print the summary to the summary file.
            #print >> outfile, "%s|%s|%s|%s|%s|%s|%s" % (curtableid, curseq, curtableposition, curcells, curtablename, cursubjarea, title)
            # save this as a new table.
            ts = table_summary(tblid = curtableid, seq = curseq, position = curtableposition, cells = curcells, title=curtablename, subject_area = cursubjarea, universe = title)
            ts.save()
            curtable=ts
            
        else:
            # It's either a data line, the end of the file, or a problem
            if(tblid == curtableid):
                # we've verified that the line is in the correct table.
                try: 
                    order = int(order)
                except:
                    #raise Exception, "Nonnumeric order %s in line %s: %s" % (order, linenum, line)
                    print "Nonnumeric order %s with curtableposition %s in line %s" % (order, curtableposition, linenum)
                    #skip 
                    continue
                    
                # calculate the actual file location. 
                # Census is nuts -- no idea why we need to subtract 1, but we do.
                actual_order = int(curtableposition) + int(order) - 1 
                
                print >> outfile, "LINE: %s|%s|%s|%s|%s" % (tblid, seq, order, actual_order, title)
                b, created = table_line.objects.get_or_create(tbl=curtable, seq=seq, order=order, actual_order=actual_order, title=title)
                
            else:
                raise Exception, "Unexpected tblid in line %s: %s" % (linenum, line)
            

def find_table(search_string):
    relevant_tables = table_summary.objects.filter(title__icontains=search_string)

    for rt in relevant_tables:
        print "Found table %s: %s" % (rt.tblid, rt.title)

def table_metadata(table_id):
    table_id = table_id.upper()
    relevant_table = table_summary.objects.get(tblid__iexact=table_id)
    relevant_lines = table_line.objects.filter(tbl__tblid__iexact=table_id)

    print "Showing metadata for table %s: %s --- %s" % (table_id, relevant_table.title, relevant_table.universe)
    print "Reference file sequence: %s" % (relevant_table.seq)

    for line in relevant_lines:
        print " %s_%s: %s" % (relevant_table.seq, line.actual_order, line.title)

# load a specified geo summary file (either for a single state or for the nation) into a precreated django model. 
def load_geo():


    for state in state_list:

        infile = open(summary_dir + "/g20095" + state + "_conv.txt", "r")

        for line in infile.readlines():
                        # n-1; n-1+l
            ga = geo_area()        
            ga.fileid = line[0:6]
            ga.stusab = line[6:8]
            ga.sumlevel = line[8:11]
            ga.component = line[11:13]
            ga.logrecno = line[13:20]
            ga.us = line[20:21]
            ga.region = line[21:22]
            ga.division = line[22:23]
            ga.statece = line[23:25]
            ga.state = line[25:27]
            ga.county = line[27:30]
            ga.cousub = line[30:35]
            ga.place = line[35:40]
            ga.tract = line[40:46]
            ga.blkgrp = line[46:47]
            ga.concit = line[47:52]
            ga.aianhh = line[52:56]
            ga.aianhhfp = line[56:61]
            ga.aihhtli = line[61:62]
            ga.aitsce = line[62:66]
            ga.aits = line[65:70]
            ga.anrc = line[70:75]
            ga.cbsa = line[75:80]
            ga.csa = line[80:83]
            ga.metdiv = line[83:88]
            ga.macc = line[88:89]
            ga.memi = line[89:90]
            ga.necta = line[90:95]
            ga.cnecta = line[95:98]
            ga.nectadiv = line[98:103]
            ga.ua = line[103:108]
            ga.uacp = line[108:113]
            ga.cdcurr = line[113:115]
            ga.sldu = line[115:118]
            ga.sldl = line[118:121]
            ga.submcd = line[135:140]
            ga.sdelm = line[140:145]
            ga.sdsec = line[145:150]
            ga.sduni = line[150:155]
            ga.ur = line[155:156]
            ga.pci = line[156:157]
            ga.puma5 = line[168:173]
            ga.geoid = line[178:218]

    	#kill the extra white space in the geography name
            ga.name = line[218:418].strip()

            print "Got sumlevel: '%s' logrecno: '%s' for geography: '%s'" % ( ga.sumlevel, ga.logrecno, ga.name)
            ga.save()
        infile.close()


def dump_table(table_id, summary_level, use_text_headers=True, include_standard_errors=False):        
# summary level: (incomplete list)
# 010 - nation 
# 020 - region
# 030 - division
# 040 - states 
# 050 - counties
# 330 - combined statistical areas
# 310 - Metropolitan Statistical Areas / Micropolitan Statistical Areas

# OVERVIEW:
# Get the header info from the table so we know which lines to pull from which summary file
# Read the relevant columns from the e, s, and m files into a hash
# then pull all the geographies from the geo model and output a header file
# then iterate through the geographies, and join them to the estimates, error margins and standard error values.


    table_id = table_id.upper()
    relevant_table = table_summary.objects.get(tblid__iexact=table_id)
    relevant_lines = table_line.objects.filter(tbl__tblid__iexact=table_id)
    relevant_lines = relevant_lines.order_by('actual_order')

    file_sequence_number = relevant_table.seq
    # left pad the file sequence number with zeroes, add three more to the right.
    file_name_end = str(file_sequence_number).zfill(4) + "000.txt"

    print "Processing table %s: %s --- %s" % (table_id, relevant_table.title, relevant_table.universe)

    # Read the column order numbers into a list.
    # In practice line column orders for a single table are always contiguous -- but using the list is a bit more versatile if we wanted to grab only a few specified lines.

    column_orders = []
    column_headers = []

    for line in relevant_lines:
        column_orders.append(line.actual_order) 
        if (use_text_headers):
            column_headers.append(line.title)
        else:
            column_headers.append(str(file_sequence_number) + "_" + str(line.actual_order))

    print "Made column headers: %s" % (column_headers)
    print "Made column orders: %s" % (column_orders)


    estimates = {}
    margins = {}    

    # loop through all the relevant files and read them into memory.

    for state in state_list:    
        # read the summary files into memory    
        estimate_file = summary_dir + "/e" + format_prefix + state + file_name_end
        margin_file = summary_dir + "/m" + format_prefix + state + file_name_end
        stderror_file = summary_dir + "/s" + format_prefix + state+ file_name_end

        print "Processing estimate file:  %s" % (estimate_file)

        efile = open(estimate_file, "r")


        for line in efile.readlines():


            line = line.replace("\n", "")
            line = line.replace("\r", "")    
            fields = line.split(",")
            logrecno = state.upper() + "_" + fields[5]
            line_values = []
            print "** processing line: " + line + " with logrecno: " + logrecno
            # now pull out the columns we want. 
            for cnum in column_orders:
                # Subtract one because the fields are zero-indexed
                line_values.append(fields[cnum-1])

            # Add the lines to the estimate hash
            estimates[logrecno]=line_values
        efile.close()    

        mfile = open(margin_file, "r")

        for line in mfile.readlines():

            #print "** processing line: " + line
            line = line.replace("\n", "")
            line = line.replace("\r", "")    
            fields = line.split(",")
            logrecno = state.upper() + "_" + fields[5]
            line_values = []

            # now pull out the columns we want. 
            for cnum in column_orders:
                # Subtract one because the fields are zero-indexed
                line_values.append(fields[cnum-1])

            # Add the lines to the estimate hash
            margins[logrecno]=line_values        
        mfile.close()




    # open output file
    out_file = format_dir + "/" + format_prefix + '_' + table_id + '_' + summary_level + '.txt'
    print "Writing data to file: %s " % (out_file)

    r_file = open(out_file, "w")
#    codecs.open("test_output","w","utf-8-sig")
    r_file = codecs.open(out_file, "w", "latin-1")
    
    header=''
    hindex = 0
    for h in column_headers:
        if (hindex>0):
            header = header + "\t"

        if (use_text_headers):    
            header = header + h + "\tmargin_" + h  
        else:
            header = header + "e_" + h + "\tm_" + h

        hindex = hindex + 1

    # First column is the geography name
    print >> r_file, "geo_name\tstate\tcounty\ttract\t" + header

    for state in state_list:  
        
        # Get the relevant geo areas.
        geo_areas = geo_area.objects.filter(sumlevel__iexact=summary_level).filter(stusab__iexact=state)

        for ga in geo_areas:

            logrec = ga.stusab + "_" + ga.logrecno
            gname = ga.name
            gstate = ga.state
            gcounty = ga.county
            gtract = ga.tract
            lrn_estimates = estimates[logrec]
            lrn_margins = margins[logrec]

            df = 0
            line_data = ''
            if (lrn_estimates):
                for i in range(len(lrn_estimates)):
                    if (df>0):
                        line_data = line_data + "\t"
                    line_data = line_data + lrn_estimates[i] + "\t" + lrn_margins[i]
                    df = df+1



                print >> r_file, gname + "\t" + gstate + "\t" + gcounty + "\t" + gtract + "\t" + line_data         




