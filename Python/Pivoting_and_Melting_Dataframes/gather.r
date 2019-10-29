library(tidyr)
df=gather(df,platform,value,-mydate)
periscope.table(df)