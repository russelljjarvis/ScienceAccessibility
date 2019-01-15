
require("reticulate")
source_python("pickle_reader.py")
pickle_data <- read_pickle_file("scraped.p")