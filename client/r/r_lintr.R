# From https://gist.github.com/wookietreiber/afdb946625c6090f96012ee1da316a73#file-git-hook-lintr-r
files <- commandArgs(trailingOnly = TRUE)

messages <- function(file) {
    result <- lintr::lint(file)
    print(result)
    return(length(result))
}

msgs <- sapply(files, messages)

if (sum(msgs) > 0) {
    q(status = 1)
}
