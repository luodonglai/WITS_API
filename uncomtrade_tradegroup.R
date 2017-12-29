# There is a limit for the uncomtrade api
# 1 request per second and 100 per hour
# R is used because there is an office r-pkg for data extraction


# clear all variables
rm(list = ls(all = TRUE))
# Install other related package
libraries = c("comtradr", "plyr", "countrycode", "devtools" , "rjson")
lapply(libraries, function(x) if (!(x %in% installed.packages())) {
    install.packages(x)
})

# force install the package from github, only need to run once
devtools::install_github("ropensci/comtradr") 


lapply(libraries, library, quietly = TRUE, character.only = TRUE)


# set working directory
setwd("D:/dropbox/dropbox/lky_ra/Trilemma/WITS_API/")

# Extracting codes and descriptions of reporters from the UN Comtrade API
string <- "http://comtrade.un.org/data/cache/partnerAreas.json"
 reporters <- fromJSON(file = string)
reporters <- as.data.frame(t(sapply(reporters$results, rbind)))

#  use the get.method from the UNCOMTRADE website

get.Comtrade <- function(url = "http://comtrade.un.org/api/get?"
                         , maxrec = 50000
                         , type = "C"
                         , freq = "A"
                         , px = "HS"
                         , ps = "now"
                         , r
                         , p
                         , rg = "all"
                         , cc = "TOTAL"
                         , fmt = "json"
) {
    string <- paste(url
                 , "max=", maxrec, "&" #maximum no. of records returned
                 , "type=", type, "&" #type of trade (c=commodities)
                 , "freq=", freq, "&" #frequency
                 , "px=", px, "&" #classification
                 , "ps=", ps, "&" #time period
                 , "r=", r, "&" #reporting area
                 , "p=", p, "&" #partner country
                 , "rg=", rg, "&" #trade flow
                 , "cc=", cc, "&" #classification code
                 , "fmt=", fmt #Format
                 , sep = ""
  )

    if (fmt == "csv") {
        raw.data <- read.csv(string, header = TRUE)
        return(list(validation = NULL, data = raw.data))
    } else {
        if (fmt == "json") {
            raw.data <- fromJSON(file = string)
            data <- raw.data$dataset
            validation <- unlist(raw.data$validation, recursive = TRUE)
            ndata <- NULL
            if (length(data) > 0) {
                var.names <- names(data[[1]])
                data <- as.data.frame(t(sapply(data, rbind)))
                ndata <- NULL
                for (i in 1:ncol(data)) {
                    data[sapply(data[, i], is.null), i] <- NA
                    ndata <- cbind(ndata, unlist(data[, i]))
                }
                ndata <- as.data.frame(ndata)
                colnames(ndata) <- var.names
            }
            return(list(validation = validation, data = ndata))
        }
    }
}

# example 1
s1 <- get.Comtrade(r = "842", p = "124,484", fmt = "CSV")
s1

# loop for all available countries on all available years
# at each request for either reporter or partner, 5 countries at most.
# sample call : /api/get?max=500&type=C&freq=A&px=S2&ps=all
# &r=842%2C841%2C156&p=344%2C446%2C392&rg=1%2C2
# &cc=TOTAL%2C0%2C01%2C1%2C2%2C3%2C4%2C68%2C667%2C971%2C5%2C6%2C7%2C8

# extract available country code:
avail_country <- as.numeric(reporters$V1[c(-1)])
l_country = length(avail_country)
c_v = 0
for (i in 1:l_country) {
    ci = avail_country[i]
    k = i - 1
    for (j in 1: k) {
        
        cj = avail_country[j]

        c_target = paste(ci, ",", cj, sep = "")

        data = get.Comtrade(r = c_target, p = c_target, fmt = "csv", px = "S2", ps = "all", rg = "1%2C2", cc = "TOTAL%2C0%2C01%2C1%2C2%2C3%2C4%2C68%2C667%2C971%2C5%2C6%2C7%2C8")

        
        if (identical(is.na(data$data$Year[1]),FALSE)) {
        c_v = c_v + 1

        if (c_v == 1) {
            data_combined = as.matrix(data$data)
        } else {
            data_combined = rbind(data_combined, as.matrix(data$data))
            sprintf("combined successfully", i, j , c_v)
        }
            Sys.sleep(60)
    }
    }
}

write.csv(data_combined, file = "trade_rev2.csv")

