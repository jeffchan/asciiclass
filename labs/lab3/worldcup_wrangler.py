from wrangler import dw
import sys

if(len(sys.argv) < 3):
  sys.exit('Error: Please include an input and output file.  Example python script.py input.csv output.csv')

w = dw.DataWrangler()

# Split data repeatedly on '|-'  into  rows
w.add(dw.Split(column=["data"],
               table=0,
               status="active",
               drop=True,
               result="row",
               update=False,
               insert_position="right",
               row=None,
               on="\\|-",
               before=None,
               after=None,
               ignore_between=None,
               which=1,
               max=0,
               positions=None,
               quote_character=None))

# Cut from data on '| any lowercase word =#FFF any number  any word \|'
w.add(dw.Cut(column=["data"],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on="\\|[a-z]+=#FFF\\d+[A-Za-z]+\\|",
             before=None,
             after=None,
             ignore_between=None,
             which=1,
             max="0",
             positions=None))

# Extract from data between ' any lowercase word |' and '}'
w.add(dw.Extract(column=["data"],
                 table=0,
                 status="active",
                 drop=False,
                 result="column",
                 update=False,
                 insert_position="right",
                 row=None,
                 on=".*",
                 before="}",
                 after="[a-z]+\\|",
                 ignore_between=None,
                 which=1,
                 max=1,
                 positions=None))

# Cut  on '{{fb| any word }}'
w.add(dw.Cut(column=[],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on="{{fb\\|[A-Za-z]+}}",
             before=None,
             after=None,
             ignore_between=None,
             which=1,
             max=1,
             positions=None))

# Cut from data on '|newline'
w.add(dw.Cut(column=["data"],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on="\\|\n",
             before=None,
             after=None,
             ignore_between=None,
             which=1,
             max=1,
             positions=None))

# Split data repeatedly on newline after ' '
w.add(dw.Split(column=["data"],
               table=0,
               status="active",
               drop=True,
               result="column",
               update=False,
               insert_position="right",
               row=None,
               on="\n",
               before=None,
               after=" ",
               ignore_between=None,
               which=1,
               max="0",
               positions=None,
               quote_character=None))

# Set  split  name to  1
w.add(dw.SetName(column=["split"],
                 table=0,
                 status="active",
                 drop=True,
                 names=["1"],
                 header_row=None))

# Set  split1  name to  2
w.add(dw.SetName(column=["split1"],
                 table=0,
                 status="active",
                 drop=True,
                 names=["2"],
                 header_row=None))

# Set  split2  name to  3
w.add(dw.SetName(column=["split2"],
                 table=0,
                 status="active",
                 drop=True,
                 names=["3"],
                 header_row=None))

# Set  split3  name to  4
w.add(dw.SetName(column=["split3"],
                 table=0,
                 status="active",
                 drop=True,
                 names=["4"],
                 header_row=None))

# Drop split4
w.add(dw.Drop(column=["split4"],
              table=0,
              status="active",
              drop=True))

# Fold 1, 2, 3, 4  using  header as a key
w.add(dw.Fold(column=["_1","_2","_3","_4"],
              table=0,
              status="active",
              drop=False,
              keys=[-1]))

# Set  fold  name to  Rank
w.add(dw.SetName(column=["fold"],
                 table=0,
                 status="active",
                 drop=True,
                 names=["Rank"],
                 header_row=None))

# Set  extract  name to  Nation
w.add(dw.SetName(column=["extract"],
                 table=0,
                 status="active",
                 drop=True,
                 names=["Nation"],
                 header_row=None))

# Set  value  name to  Year
w.add(dw.SetName(column=["value"],
                 table=0,
                 status="active",
                 drop=True,
                 names=["Year"],
                 header_row=None))

# Cut from Year on '#1|\*'
w.add(dw.Cut(column=["Year"],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on="#1\\|\\*",
             before=None,
             after=None,
             ignore_between=None,
             which=1,
             max="0",
             positions=None))

# Cut from Year on ' any number   any word   any word  Cup|'
w.add(dw.Cut(column=["Year"],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on="\\d+ [a-zA-Z]+ [a-zA-Z]+ Cup\\|",
             before=None,
             after=None,
             ignore_between=None,
             which=1,
             max="0",
             positions=None))

# Cut from Year on '|align=center\| .'
w.add(dw.Cut(column=["Year"],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on="\\|align=center\\| .",
             before=None,
             after=None,
             ignore_between=None,
             which=1,
             max=1,
             positions=None))

# Cut from Year on ']]'
w.add(dw.Cut(column=["Year"],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on="]]",
             before=None,
             after=None,
             ignore_between=None,
             which=1,
             max="0",
             positions=None))

# Cut from Year on '[\['
w.add(dw.Cut(column=["Year"],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on="\\[\\[",
             before=None,
             after=None,
             ignore_between=None,
             which=1,
             max="0",
             positions=None))

# Split Year between ' ' and '('
w.add(dw.Split(column=["Year"],
               table=0,
               status="active",
               drop=True,
               result="column",
               update=False,
               insert_position="right",
               row=None,
               on=".*",
               before="\\(",
               after=" ",
               ignore_between=None,
               which=1,
               max=1,
               positions=None,
               quote_character=None))

# Drop split
w.add(dw.Drop(column=["split"],
              table=0,
              status="active",
              drop=True))

# Cut from split1 on '('
w.add(dw.Cut(column=["split1"],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on="\\(",
             before=None,
             after=None,
             ignore_between=None,
             which=1,
             max=1,
             positions=None))

# Cut from split1 on ')'
w.add(dw.Cut(column=["split1"],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on="\\)",
             before=None,
             after=None,
             ignore_between=None,
             which=1,
             max=1,
             positions=None))

# Split split1 repeatedly on ','
w.add(dw.Split(column=["split1"],
               table=0,
               status="active",
               drop=True,
               result="column",
               update=False,
               insert_position="right",
               row=None,
               on=",",
               before=None,
               after=None,
               ignore_between=None,
               which=1,
               max="0",
               positions=None,
               quote_character=None))

# Delete  rows where Nation is null
w.add(dw.Filter(column=[],
                table=0,
                status="active",
                drop=False,
                row=dw.Row(column=[],
             table=0,
             status="active",
             drop=False,
             conditions=[dw.IsNull(column=[],
                table=0,
                status="active",
                drop=False,
                lcol="Nation",
                value=None,
                op_str="is null")])))

# Fold split, split2, split3, split4...  using  header as a key
w.add(dw.Fold(column=["split","split2","split3","split4","split5"],
              table=0,
              status="active",
              drop=False,
              keys=[-1]))

# Drop fold
w.add(dw.Drop(column=["fold"],
              table=0,
              status="active",
              drop=True))

# Set  value  name to  Year
w.add(dw.SetName(column=["value"],
                 table=0,
                 status="active",
                 drop=True,
                 names=["Year"],
                 header_row=None))

# Delete  rows where Year is null
w.add(dw.Filter(column=[],
                table=0,
                status="active",
                drop=False,
                row=dw.Row(column=[],
             table=0,
             status="active",
             drop=False,
             conditions=[dw.IsNull(column=[],
                table=0,
                status="active",
                drop=False,
                lcol="Year",
                value=None,
                op_str="is null")])))

# Cut from Rank on '*'
w.add(dw.Cut(column=["Rank"],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on="\\_",
             before=None,
             after=None,
             ignore_between=None,
             which=1,
             max=1,
             positions=None))

# Cut from Year on '*'
w.add(dw.Cut(column=["Year"],
             table=0,
             status="active",
             drop=False,
             result="column",
             update=True,
             insert_position="right",
             row=None,
             on="\\*",
             before=None,
             after=None,
             ignore_between=None,
             which=1,
             max=1,
             positions=None))

w.apply_to_file(sys.argv[1]).print_csv(sys.argv[2])

