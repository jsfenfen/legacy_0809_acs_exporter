## Need to deal with dates, comma-delimited numbers, and currencies...

# the file name to read
filename = "/Users/jacobfenton/IRW/django_sites/1.1.1/broadband/workshop/acs_09_5yr/formatted/20095_B17017_140.txt"
f = open(filename, 'r')


# This is where the create table statement will go
OUT = open('schema_parsed.txt', 'w')


# options
first_line_row_headers = True
delimiter = "\t"
rowheaders = None

# only defined if there aren't row headers--otherwise each row should have the same number of columns as the header row.
# As built, currently, stuff will break w/out column headers

num_columns = 0

table_name = "b17017"

OUT.write("create table %s (\n" % (table_name));

# store the maximum length--in characters, here
field_lengths = []
field_nulls = []
field_int = []
field_float = []
field_string = []

# keep track of which rowheaders have been used,so we don't get duplicates.
rowheader_dict = dict()

def initfieldlengths(fl, thenum):
    for i in range (thenum):
        fl.append(0)
    return fl
    
def get_field_type(field):

    
    # If it's empty, consider it Null
    if (len(field)==0):
        return 'n'
        
    # census does this to indicate nulls
    if (field=="."):
        return 'n'
    
    ## not implemented... 
    # if isdate(field):
    #   return 'd'    
        
    try:
        value = int(field)
    except ValueError:
        try: 
            value=float(field)
        except ValueError:
            return 's'
        else:
            return 'f'
        
    else:
        # need to check for leading zero -- if so, it's a string.
        if field[0]=='0' and value>0:
            return 's'
        else: 
            return 'i'    
        
# Working with census data we encounter a lot of rows with the same name. Keep track of 'em and append numbers so the table will at least load.
        
def uniquefy_rowheader(rawrow):

    therow = rawrow.lower()

    print "got row %s" % (therow)
    try:
        rh_count = rowheader_dict[therow]
    except KeyError:
        rowheader_dict[therow]=1
        return therow
    else:
        rowheader_dict[therow] = int(rh_count)+1
        return "%s_%s" %(therow, rh_count)
        
count=0
for count, line in enumerate(f):
    line = line.replace("\n","")
    line = line.replace("\r","")
    lineargs = line.split(delimiter)

#    print "Line %s (%s args): %s" % (count,len(lineargs), line)
    if (count==0 and first_line_row_headers):
        
        # clean up headers from header row en mass. I don't want quotes, commas or spaces in field names.
        newline = line.replace(" ","_")
        newline = newline.replace(":","")
        newline = newline.replace("'","")
        newline = newline.replace(",","")
        lineargs = newline.split(delimiter)       
        rowheaders = lineargs
        
        # make sure we've got unique row names.
        for i, rh in enumerate(rowheaders):
            
            rowheaders[i] = uniquefy_rowheader(rh)
            #print "UR: '%s' '%s' " % (rowheaders[i], rh)
            
        num_columns = len(rowheaders)
        field_lengths = initfieldlengths(field_lengths, num_columns)
        field_nulls = initfieldlengths(field_nulls, num_columns)
        field_int = initfieldlengths(field_int, num_columns)
        field_float = initfieldlengths(field_float, num_columns)
        field_string = initfieldlengths(field_string, num_columns)
        
        
    else:
        if (len(lineargs) != num_columns):
            print "Argument mismatch in line %s ; %s arguments expected, but %s arguments found" % (count, num_columns, len(lineargs))

        # now run through each argument

        for argnum, i in enumerate(lineargs):
            # get length
            if (len(i) > field_lengths[argnum]):
                field_lengths[argnum]=len(i)
            
            ftype = get_field_type(i)
            
            ## print every field determination
            #print "'%s' is %s" % (i, ftype)
            
            if ftype =='i':
                field_int[argnum] += 1
            elif ftype == 'n':
                field_nulls[argnum] += 1
            elif ftype == 'f':
                field_float[argnum] += 1
            elif ftype == 's':
                field_string[argnum] += 1
            


print "File size: %s lines" % (count)
print "row_name, max_field_length, nulls, ints, floats, strings\n"    
for (rownum, row) in enumerate(rowheaders):
    field_length = field_lengths[rownum]
    nulls = field_nulls[rownum]
    ints = field_int[rownum]
    floats = field_float[rownum]
    strings = field_string[rownum]
    
    print "%s: %s, %s, %s, %s, %s, %s" % (rownum, row, field_length, nulls, ints, floats, strings)
    
    #use lower case only in field names
    row = row.lower()
    
    # Now guess field type. 
    
    outstanding_rows = count-nulls
    
    if (outstanding_rows - ints == 0):
        OUT.write("\t\"%s\" int" % (row))
    elif (outstanding_rows - floats == 0):
        OUT.write("\t\"%s\" float" % (row))    
    # need to add support for dates, somehow...
    
    else:
        if field_length < 8:
            OUT.write("\t\"%s\" char(%s)" % (row, field_length))
        else:
            OUT.write("\t\"%s\" varchar(%s)" % (row, field_length)) 
    
    if rownum<len(rowheaders)-1:
        OUT.write(",\n")
        
OUT.write("\n);")      
