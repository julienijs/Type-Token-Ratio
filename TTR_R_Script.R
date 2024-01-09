# Loading libraries
library("readxl")
library("ggplot2")

# read files
TTR_data <- read_excel("C:/CCLAMP_TTR/ttr_results.xlsx")

ggplot(aes(x = Year, y = Normalized_TTR), data = TTR_data) + geom_line()
