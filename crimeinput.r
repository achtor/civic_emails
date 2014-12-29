args <- commandArgs(trailingOnly = TRUE)

distonplane <- function(point1,point2)
{
  diff <- point1 - point2
  distance <- sqrt(sum(diff^2))
  distance
}

distance.stretch <- function(point1,point2) {
  R <- 3963.1676
  p1rad <- point1 * pi/180
  p2rad <- point2 * pi/180
  distance <- R*distonplane(p1rad, p2rad)
  distance
}

coords <- as.numeric(args)


#Max distance (miles) will be taken as input
maxdist <- 1

vc <- c('ARSON','ASSAULT','BATTERY','BURGLARY','CRIM SEXUAL ASSAULT','HOMICIDE','KIDNAPPING','NARCOTICS','ROBBERY','SEX OFFENSE')

##############################################################################################################
#                                         Crime Data                                                         #
##############################################################################################################
frame <- read.csv('http://plenar.io/v1/api/detail/?dataset_name=crimes_2001_to_present&obs_date__le=2014%2F11%2F15&obs_date__ge=2014%2F11%2F01&agg=day&dataset_name=crimes_2001_to_present&data_type=csv&offset=100000000000000000')
today <- 22
year <- 2014
month <- 11
dayend <- today-10
daystart <- dayend-7
offset = 0
while(today) {
  dita <- read.csv(paste('http://plenar.io/v1/api/detail/?dataset_name=crimes_2001_to_present&obs_date__le=',year,
                          '%2F',month,'%2F',dayend,'&obs_date__ge=',year,'%2F',month,'%2F',daystart,
                          '&agg=day&dataset_name=crimes_2001_to_present&data_type=csv&offset=',offset,sep=''))
  if(nrow(dita) ==0) {
    break
  }
  row.names(dita) <- NULL
  frame <- rbind(frame,dita)
  offset = offset+1000
}
frame <- frame[grep(paste(vc, collapse='|'), frame$primary_type, ignore.case=TRUE),]
data <- frame
data <- subset(data, data$domestic=='False')
row.names(data) <- NULL
data <- data[c('date','block','primary_type','description','location_description','arrest','domestic','latitude','longitude')]
data <- na.omit(data)
row.names(data) <- NULL


for(i in 1:dim(data)[1]) {
  if(distance.stretch(coords,c(data$latitude[i],data$longitude[i])) < maxdist) {
    data$within[i] <- 1
  }
  else {
    data$within[i] <- 0
  }
}
withindist <- subset(data,within==1)
withindist$primary_type <- tolower(withindist$primary_type)
withindist$description <- tolower(withindist$description)
row.names(withindist) <- NULL

for(i in 1:dim(withindist)[1]) {
  if(withindist$arrest[i]=='True') {
    arrest = 'An arrest was made.'
  }
  else {
    arrest = 'An arrest was not made.'
  }
  print(paste(paste('A',withindist$primary_type[i],'incident occurred at',withindist$block[i],'on',
              withindist$date[i]),'.',' ',arrest,' ','CPD comment: ',withindist$description[i],'.',sep=''))
}

new <- withindist
new$coords[1] <- coords[1]
new$coords[2] <- coords[2]
write.csv(new,'crimedata.csv')

system("python map.py")



#json <- toJSON(withindist)
#dist <- distHaversine(coords,r=3963.1676)