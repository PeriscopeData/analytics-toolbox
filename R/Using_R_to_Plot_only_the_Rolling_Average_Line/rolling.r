library(zoo)

# Calculating the rolling average. Window is set to 3 here, corresponding to an average of the current row and the 2 preceding rows
window <- 10
padding <- rep(NA, window - 1)
df$rollingavg <- c(padding, rollmean(df$number_users, k = window))

periscope.table(df)