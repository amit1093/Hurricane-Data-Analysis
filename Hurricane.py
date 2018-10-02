# Hurricane Data Analysis

"""
Please note: It would take several minutes for running due to the large calculation.
"""

from datetime import datetime
from pygeodesy import ellipsoidalVincenty as ev

Windspeed = {} # dictinary to store max wind sustained
dict_name = {} # dictionary to store storm count per year
dict_name1 = {} # dictionary to store hurrican count per year
landFall = {} # dictionary to store landfall count

def getProcessing(file):
    # variable declaration
    speed1 = [] # list to divide 64kt set
    speed2 = [] # list to divide 50kt set
    speed3 = [] # list to divide 34kt set
    current_year = ""
    valid = 0
    hypo = 0
    hypothesis_percentage = 0
    storm = {} # dictionary to store storm id and storm name
    Min_Date = {} # dictionary to store the start date of storm system
    Max_Date = {} # dictionary to store the end date of storm system
    dict = {}
    totalDist = {} # dictionary to store total distance travelled by the storm
    Max_speed = {} # dictionary to store maximum speed of the storm
    Avg_Speed = {} # dictionary to store average speed of the storm

    for line in file:

        a1 = line.split(',')
        if line[0].isalpha() == True: # loop check to store lines only with storm name data

            max_wind = 0
            fall = 0
            name1 = str(a1[0]).strip()  # string type variable stores the storm detail like 'AL011851'
            name2 = str(a1[1]).strip()  # string type variable used to store the name of the storm, if no name was assigned in the file, then the storm is named as "UNNAMED"
            storm.update({name1: name2})  # storm dictionary updated with name1 and name2 details for each storm record
            mindate = datetime.strptime('20201212', '%Y%m%d')  # setting a higher value of a variable for comparison for minimum date
            maxdate = datetime.strptime('00010101','%Y%m%d')  # setting a lower value of a variable for comparison for maximum date
            Min_Date.update({name1: mindate})
            Max_Date.update({name1: maxdate})
            dict.update({name1: name2})
            previous_year = a1[0][4:8]  # variable storing only year only
            latPrev = ''
            longPrev = ''
            time = ''
            totalDistTemp = 0.0
            timediffadd = 0
            avg_speed = 0
            max_speed = 0
            totalDist.update({name1: totalDistTemp})
            Avg_Speed.update({name1: avg_speed})
            Max_speed.update({name1: max_speed})

            if (previous_year != current_year):
                count = 0
                count1 = 0

        else:

            Windspeed, max_wind = maxwind(a1, name1, max_wind)
            date_var = str(a1[0]).strip()  # variable used to store the storm record date occurence from the file
            date_time = datetime.strptime(date_var, '%Y%m%d')  # converting the date_var to datetime format
            Min_Date, Max_Date = date_cal(date_time, name1, Min_Date,
                                          Max_Date)  # function call to calculate the date range for each storm record

            landFall, fall = getLandfall(a1[2], name1,
                                         fall)  # function call to calculate the number of times storm had a Landfall

            dict_name, count, current_year = getstormcount(a1[0][0:4], previous_year, a1[3].strip(), count)
            dict_name1, count1, current_year = gethurricanecount(a1[0][0:4], previous_year, a1[3].strip(), count1)

            if latPrev == '' and longPrev == '':
                totalDist.update({name1: totalDistTemp})
                latPrev = a1[4].strip()
                longPrev = a1[5].strip()
                timea = str(a1[0]).strip()  # string storing date(yyyymmdd) of the track occurrence
                timeb = str(a1[1]).strip()  # string used to store time(hhmm) of the track orccurence
                timef = timea + ' ' + timeb
                time = datetime.strptime(timef, "%Y%m%d %H%M")  # datetime format for the occurence of date and time for each track
            else:
                speed1[:] = []
                speed2[:] = []
                speed3[:] = []
                a = myLatLon(latPrev, longPrev)
                latPrev = a1[4].strip()
                longPrev = a1[5].strip()
                b = myLatLon(latPrev, longPrev)
                timec = str(a1[0]).strip()
                timed = str(a1[1]).strip()
                timef1 = timec + ' ' + timed
                time1 = datetime.strptime(timef1, "%Y%m%d %H%M")

                # storing the speeds of the track in a list as per wind radii (64 kt stored in speed1)
                speed1.append(int(a1[16].strip()))
                speed1.append(int(a1[17].strip()))
                speed1.append(int(a1[18].strip()))
                speed1.append(int(a1[19].strip()))

                # storing the speeds of the track in a list as per wind radii (50 kt stored in speed1)
                speed2.append(int(a1[12].strip()))
                speed2.append(int(a1[13].strip()))
                speed2.append(int(a1[14].strip()))
                speed2.append(int(a1[15].strip()))

                # storing the speeds of the track in a list as per wind radii (34 kt stored in speed1)
                speed3.append(int(a1[8].strip()))
                speed3.append(int(a1[9].strip()))
                speed3.append(int(a1[10].strip()))
                speed3.append(int(a1[11].strip()))

                if a != b:

                    bearing1 = a.bearingTo(b)
                    bearing = bearing1 + 90
                    # calculating the bearing quadrant
                    if bearing >= 0 and bearing <= 90:
                        quadbear = 'NW'
                    elif bearing > 90 and bearing <= 180:
                        quadbear = 'NE'
                    elif bearing > 180 and bearing <= 270:
                        quadbear = 'SE'
                    elif bearing > 270 and bearing <= 360:
                        quadbear = 'SW'

                    totalDistTemp1 = a.distanceTo(b)
                    totalDistmiles = totalDistTemp1 / 1852.0
                    totalDistTemp += a.distanceTo(b)
                    totDistMiles = totalDistTemp / 1852.0
                    time_diff = time1 - time
                    timediff1 = time_diff.total_seconds() / 3600
                    timediffadd += timediff1

                    if time_diff == 0:
                        each_speed = 0
                    else:
                        each_speed = totalDistmiles / timediff1

                    if each_speed >= max_speed:
                        max_speed = each_speed
                        Max_speed[name1] = max_speed

                    time = time1
                    avg_speed = totDistMiles / timediffadd

                    totalDist.update({name1: totDistMiles})
                    Avg_Speed.update({name1: avg_speed})
                    Max_speed.update({name1: max_speed})

                    if max(speed1) != 0 and max(speed1) != -999:
                        valid += 1 # check to include only valid data for hypothesis calculation
                        if speed1.index(max(speed1)) == 0:
                            quadspeed = 'NE'
                            if quadbear == quadspeed:
                                hypo += 1 # counter to check when hypothesis is true

                    elif (max(speed2) != 0 and max(speed2) != -999):
                        valid += 1
                        if speed2.index(max(speed2)) == 0:
                            quadspeed = 'NE'
                            if quadbear == quadspeed:
                                hypo += 1

                    elif (max(speed3) != 0 and max(speed3) != -999):
                        valid += 1
                        if speed3.index(max(speed3)) == 0:
                            quadspeed = 'NE'
                            if quadbear == quadspeed:
                                hypo += 1

    print("Storm names:", dict)
    print("Landfall counts:", landFall)
    print("Max sustained wind:", Windspeed)
    print("Date when started in yyyy-mm-dd format:", Min_Date)
    print("Date when ended in yyyy-mm-dd format:", Max_Date)
    print("Total distance in miles travelled by storm:", totalDist)
    print("Max speed for the storms in knots:", Max_speed)
    print("Average speed for the storms in knots:", Avg_Speed)
    print("\nStorm counts per year:", dict_name)
    print("Hurricane counts per year:", dict_name1)
    print("\nSuccessful hypothesis cases:", hypo)
    print("Valid cases:", valid)
    hypothesis_percentage = ((hypo / valid) * 100)
    print("Percentage for hypothesis:", hypothesis_percentage)
    if hypothesis_percentage > 25:
        print("Hypothesis is true")
    else:
        print("Hypothesis is false")

    dc = set(dict) & set(landFall) & set(Windspeed) & set(Min_Date) & set(Max_Date) & set(Avg_Speed) & set(Max_speed)
    for i in dc:
        print(i, "\n\t\tStorm Name =", dict[i], "\n\t\tNo. of Landfall =", landFall[i], "\n\t\tWindspeed =",
              Windspeed[i], "\n\t\tMin Date =", Min_Date[i], "\n\t\tMax Date =", Max_Date[i], "\n\t\tAvg Speed =",
              Avg_Speed[i], "\n\t\tMax Speed =", Max_speed[i])

    for i, j in zip(dict_name.items(), dict_name1.items()):
        print("\nYear:", i[0], "\n\t\tStorm Count =", i[1], "\n\t\tHurricane Count =", j[1])

def getLandfall(landfall, name1, land_fall_counter):
    """
    This function determines the Landfall count associated with each storm
    :param landfall: the dictionary that is returned after updating landfall for each storm
    :param name1: name of the storm
    :param land_fall_counter: counter to count landfall in each storm
    :return: returning the variables
    """

    if str(landfall).strip() == 'L':
        land_fall_counter += 1
        landFall[name1] = land_fall_counter

    elif not name1 in landFall:
        # landFall[name1] = land_fall_counter
        landFall[name1] = 0
    return landFall, land_fall_counter

def date_cal(each_date, name1, Min_Date, Max_Date):
    """
        This function returns the date range of each storm
        :param each_date: variable storing the date of occurrence of each track of storm
        :param name1: name of the storm
        :param Min_Date: variable used to store the date range record for each storm, stored in the datetime format
        :param Max_Date: variable used to store the date range record for each storm, stored in the datetime format
        :return: returns the earliest the storm occured in Min_date,
                         the latest time the storm occured in Max_Date
    """
    if each_date < Min_Date[name1]:
        Min_Date[name1] = each_date
    if each_date > Max_Date[name1]:
        Max_Date[name1] = each_date
    return Min_Date, Max_Date

def maxwind(a1, name1, max_wind):
    """
        This function returns highest maximum sustained wind
        :param a1: this parameter contains the file data of Atlantic and Carlotta hurricanes
        :param max_wind: this paramter stores the maximum wind
        :name1: this parameter stores the names of the storms
        :return: Windspeed - this parameter returns the maximum sustained wind in dictionary,
                 max_wind - this paramter stores the maximum
    """
    wind = int(a1[6])
    if wind >= max_wind:
        max_wind = wind
        Windspeed[name1] = max_wind
    elif wind == -99:
        Windspeed[name1] = 0
    return Windspeed, max_wind

def getstormcount(current_year, previous_year, Type, count):
    """
    This function calculates the total number of storms and hurricanes
    :param current_year: <string> datatype storing the current year for each storm
    :param previous_year: <string> datatype storing the previous year for each storm
    :param Type: variable used to store the type of storm: 'TS' corresponding to 'Tropical Storm'
    :param count: <integer> type variable used to store the count of storm types
    :return: dict_name <dictionary> type variable storing the current year and the count of the storm type
                current_year <str> type variable storing the current year of the storm
                count <int> type variable storing the count of the storm type
    """
    if (previous_year == current_year):
        if (Type == 'TS'):
            count += 1
            dict_name[current_year] = count

    return dict_name, count, current_year

def gethurricanecount(current_year, previous_year, Type, count1):
    """
    This function calculates the total number of storms and hurricanes
    :param current_year: <string> datatype storing the current year for each storm
    :param previous_year: <string> datatype storing the previous year for each storm
    :param Type: variable used to store the type of storm: 'HU' corresponding to 'Hurricane'
    :param count1: <integer> type variable used to store the count of storm types
    :return: dict_name1 <dictionary> type variable storing the current year and the count of the storm type
                current_year <str> type variable storing the current year of the storm
                count <int> type variable storing the count of the storm type
    """
    if (previous_year == current_year):
        if (Type == 'HU'):
            count1 += 1
            dict_name1[current_year] = count1

    return dict_name1, count1, current_year

# code referenced from Week 3 examples of Prof. Weible
def flip_direction(direction: str) -> str:
    """Given a compass direction 'E', 'W', 'N', or 'S', return the opposite.
    Raises exception with none of those.

    :param direction: a string containing 'E', 'W', 'N', or 'S'
    :return: a string containing 'E', 'W', 'N', or 'S'
    """
    if direction == 'E':
        return 'W'
    elif direction == 'W':
        return 'E'
    elif direction == 'N':
        return 'S'
    elif direction == 'S':
        return 'N'
    else:
        raise ValueError('Invalid or unsupported direction {} given.'.format(direction))

# code referenced from Week 3 examples of Prof. Weible
def myLatLon(lat: str, lon: str):
    """Given a latitude and longitude, normalize them if necessary,
    to return a valid ellipsoidalVincenty.LatLon object.

    :param lat: the latitude as a string
    :param lon: the longitude as a string
    """
    # get number portion:
    if lon[-1] in ['E', 'W']:
        lon_num = float(lon[:-1])
        lon_dir = lon[-1]
    else:
        lon_num = float(lon)
    if lon_num > 180.0:  # Does longitude exceed range?
        lon_num = 360.0 - lon_num
        lon_dir = flip_direction(lon_dir)
        lon = str(lon_num) + lon_dir

    return ev.LatLon(lat, lon)

def main():

    file1 = open('Atlantic Data.txt', 'r')

    file2 = open('Pacific Data.txt', 'r')

    print("Atlantic details:\n")
    getProcessing(file1)
    landFall.clear()
    Windspeed.clear()
    dict_name.clear()
    dict_name1.clear()
    print("\nPacific details:\n")
    getProcessing(file2)

if __name__ == '__main__':
    main()