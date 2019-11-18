 # Import ggplot2 for charting capabilities
library(ggplot2)
library(tidyverse)

# Adapted from this blog post http://r-statistics.co/Top50-Ggplot2-Visualizations-MasterList-R-Code.html

# Generate example data
# TODO: Delete lines 7 through 15 to leverage the output of your SQL in the generated funnel chart
STAGE <- c('Stage 01: Browsers','Stage 02: Unbounced Users','Stage 03: Email Signups','Stage 04: Email Confirmed','Stage 05: Campaign-Email Opens','Stage 06: Campaign-Email Clickthroughs','Stage 07: Buy Button Page','Stage 08: Buy Button Clickers','Stage 09: Cart Confirmation Page','Stage 10: Address Verification Page','Stage 11: Submit Order Page','Stage 12: Payment','Stage 13: Payment Successful','Stage 14: 1st Successful Purchase','Stage 15: 2nd Purchase','Stage 16: 3rd Purchase','Stage 17: 4th Purchase','Stage 18: 5th Purchase','Stage 01: Browsers','Stage 02: Unbounced Users','Stage 03: Email Signups','Stage 04: Email Confirmed','Stage 05: Campaign-Email Opens','Stage 06: Campaign-Email Clickthroughs','Stage 07: Buy Button Page','Stage 08: Buy Button Clickers','Stage 09: Cart Confirmation Page','Stage 10: Address Verification Page','Stage 11: Submit Order Page','Stage 12: Payment','Stage 13: Payment Successful','Stage 14: 1st Successful Purchase','Stage 15: 2nd Purchase','Stage 16: 3rd Purchase','Stage 17: 4th Purchase','Stage 18: 5th Purchase')

GENDER <- c('Male','Male','Male','Male','Male','Male','Male','Male','Male','Male','Male','Male','Male','Male','Male','Male','Male','Male','Female','Female','Female','Female','Female','Female','Female','Female','Female','Female','Female','Female','Female','Female','Female','Female','Female','Female')

USERS <- c(-14927618.71,-12862663.41,-11361896.41,-9411708.103,-8074316.616,-6958512.218,-6045363.483,-5029954.214,-4008034.113,-3172555.225,-2484808.199,-1903727.481,-1490277.016,-1152003.965,-770748.0581,-434430.0282,-195031.8899,-58570.22156,14226434.29,12276042.59,10850385.59,8999931.897,7732693.384,6666393.782,5743259.517,4723254.786,3680878.887,3002640.775,2467804.801,1977277.519,1593649.984,1229651.035,828496.9419,486621.9718,227106.1101,73466.77844)


# Compose generated data into a data frame
df <- data.frame(STAGE, GENDER, USERS)

# Configure breaks for the graph
brks <- c(seq(-15000000, 15000000, by = 5000000))
# Configure labels for the graph
lbls = c(seq(15, 0, -5), seq(5, 15, 5))

# Generate Plot
plt <- df %>%  # Cast the users table as a number
                            mutate(USERS = as.numeric(USERS)) %>%
              # Pipe into ggplot
                            ggplot(aes(x = reorder(STAGE,abs(USERS)), y = USERS, fill = GENDER)) +
                       # Plot the bars
              geom_bar(stat = "identity", width = .6) +
              # Shift the y axis
              scale_y_continuous(breaks = brks, labels = lbls) +
              # Flip the coordinates
              coord_flip() +
              # Add a theme
              theme_minimal() +
              # Add a title
              labs(title="Email Campaign Funnel") +
              # Add more theming options
              theme(plot.title = element_text(hjust = .5),
                                    axis.ticks = element_blank())

# Use Periscope to visualize the funnel chart by passing the image to periscope.image()
periscope.image(plt)