import pandas as pd
import operator

def getLocations():
    df = pd.read_csv('data/news_data.csv', index_col=False)
    locations = list(df['location'])
    locations = sorted(locations)
    return locations

def getAllLocations():
    df = pd.read_csv('data/location_cordinates.csv', index_col=False)
    locations = list(df['location'])
    locations = sorted(locations)
    return locations

def safetyIndex(loc):
    si = 0
    df = pd.read_csv('data/news_data.csv', index_col=False)
    for i in range(len(df)):
        if df['location'].iloc[i]==loc:
            si = df['percentile'].iloc[i]
            break
    return si

def getAddress(loc):
    df = pd.read_csv('data/location_cordinates.csv')
    for i in range(len(df)):
        if df['location'].iloc[i]==loc:
            address = df['address'].iloc[i]
            break
    return address

def getData(loc_name, age):
    df = pd.read_csv('data/news_data.csv', index_col=False)
    df_new = df[df['location']==loc_name]
    headlines = list(df_new['headline'])[0].split('\t')
    dates = list(df_new['date'])[0].split('\t')
    crime_types = list(df_new['crime_type'])[0].split('\t')
    sources = list(df_new['source'])[0].split('\t')
    urls = list(df_new['url'])[0].split('\t')
    ages = list(df_new['age'])[0].split('\t')
    businessmans = list(df_new['businessman'])[0].split('\t')

    crime_count = len(headlines)
    no_businessman = businessmans.count('1')

    age_groups = [0, 22, 51, 101]

    min_age = 0
    max_age = 100
    for i in range(1):
        if age>=age_groups[i] and age<age_groups[i+1]:
            min_age = age_groups[i]
            max_age = age_groups[i+1]

    crimes_age = 0
    lst = []
    for i in range(len(ages)):
        a = int(ages[i].replace("'", "").replace('"', ''))
        if int(a)>=min_age and int(a)<=max_age:
            crimes_age+=1
            lst.append(crime_types[i])

    if len(lst)!=0:
        s = str(max(set(lst), key = lst.count))
        s = s[0].upper() + s[1:]
    else:
        s = -1

    crimes = {'burglary':crime_types.count('burglary'),
              'robbery':crime_types.count('robbery'),
              'murder':crime_types.count('murder'),
              'kidnapping':crime_types.count('kidnapping'),
              'rape':crime_types.count('rape')}
    age_crimes = {'0-21':0,
                  '22-50':0,
                  '50+':0,
                  'NA':0}

    for k in ages:
        i = int(k.replace("'", "").replace('"', ''))
        if i>=0 and i<=21:
            age_crimes['0-21']+=1
        elif i>21 and i<=50:
            age_crimes['22-50']+=1
        elif i>50:
            age_crimes['50+']+=1
        else:
            age_crimes['NA']+=1

    x = str(sorted(crimes.items(), key=operator.itemgetter(1))[::-1][0][0])
    most_occ_crime = x[0].upper() + x[1:]
    return [dates, headlines, crime_types, sources, urls], crime_count, crimes_age, no_businessman, crimes, age_crimes, most_occ_crime, s


def rating(count):
    if count==60:
        r = 'A+'
    elif count>=50 and count<60:
        r = 'A'
    elif count>=40 and count<50:
        r = 'B'
    else:
        r = 'C'
    return r


def getSafeLocations(src_loc, dist):
    safe_area = []
    crime_area = []
    df = pd.read_csv('data/location_distance.csv', index_col=False)
    df = df[df['source']==src_loc]

    df1 = pd.read_csv('data/news_data.csv')
    src_crime_count = len(list(df1[df1['location']==src_loc].iloc[0])[1].split('\t'))


    for i in range(len(df)):
        dest_loc = df['destination'].iloc[i]
        dist_loc = df['distance'].iloc[i]
        if dest_loc in list(df1['location']) and dist_loc<dist:
            dest_crime_count = len(list(df1[df1['location']==dest_loc].iloc[0])[1].split('\t'))
            if dest_crime_count<src_crime_count:
                dest_percentile = df1[df1['location']==dest_loc]['percentile'].iloc[0]
                safe_area.append(dest_loc)
                crime_area.append(dest_percentile)

    return safe_area, crime_area