adapting this from the 08 acs stuff I built a while ago.

Creating table acs_09_5yr_table_summary
Creating table acs_09_5yr_table_line
Creating table acs_09_5yr_geo_area

running parsemerge.load_all().

It adds all the table summaries and table lines. It worked after I manually removed some weird characters like this Ó that were appearing in place of quotes in 2 spots in the file. 

--
the geo stuff is there. I edited the models and the geo_area parsing code. 

it chokes on some weird characters, but I was able to reencode with this: 

iconv -f mac -t UTF8 g20095az.txt > g20095az2.txt

and then modify the statelist file in load_geo.
