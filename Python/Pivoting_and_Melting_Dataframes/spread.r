library(tidyr)
df=spread(df,platform,count)
periscope.table(df)