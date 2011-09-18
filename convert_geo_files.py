""" convert the encoding to utf8 """


state_list=['ak', 'al', 'ar', 'az', 'ca', 'co', 'ct', 'dc', 'de', 'fl', 'ga', 'hi', 'ia', 'id', 'il', 'in', 'ks', 'ky', 'la', 'ma', 'md', 'me', 'mi', 'mn', 'mo', 'ms', 'mt', 'nc', 'nd', 'ne', 'nh', 'nj', 'nm', 'nv', 'ny', 'oh', 'ok', 'or', 'pa', 'ri', 'sc', 'sd', 'tn', 'tx', 'us', 'ut', 'va', 'vt', 'wa', 'wi', 'wv', 'wy']

summary_dir = "/Users/jacobfenton/IRW/census_data/ACS/2009_5yr/raw_data/Tracts_Block_Groups_Only"

for state in state_list:

       original_file = summary_dir + "/g20095" + state + ".txt"
       converted_file = summary_dir + "/g20095" + state + "_conv.txt"
       cmd =  "iconv -f mac -t UTF8 %s > %s" % (original_file, converted_file)
       print cmd