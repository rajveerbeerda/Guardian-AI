import pandas as pd
import aylien_news_api
from aylien_news_api.rest import ApiException
import datetime
import dateutil.parser
import time
import csv
import nltk
from nltk.tag.stanford import StanfordNERTagger
from word2number import w2n

jar = './data/stanford-ner.jar'
model = './data/english.all.3class.distsim.crf.ser.gz'


def findLocations(sentence):
    locations = []
    ner_tagger = StanfordNERTagger(model, jar, encoding='utf8')
    words = nltk.word_tokenize(sentence)
    lst = ner_tagger.tag(words)

    i = 0
    while i < len(lst):
        if lst[i][1] == 'LOCATION':
            s = lst[i][0]
            i += 1
            if i == len(lst):
                break
            while lst[i][1] == 'LOCATION':
                s = s + ' ' + lst[i][0]
                i += 1
                if i == len(lst):
                    break
            if s.lower() not in locations:
                locations.append(s.lower())
        else:
            i += 1

    return locations

def findAge(content):
    try:
        if 'year-old' in content:
            index = content.index('year-old')
            if index-7<0:
                age = content[:index+8].split()
            else:
                age = content[index-7:index+8].split()
            if len(age)!=0:
                if age[-1]=='year-old':
                    if '-' in age[-2]:
                        s = str(age[-2][:-1])
                    else:
                        s = str(age[-2])
                else:
                    s = age[-1].split('-')[0]
                if s=='a':
                    s = 1
                s = str(s).split('.')[-1]
                return w2n.word_to_num(str(s))
        else:
            return -1
    except Exception as e:
        return -1

def updateData():
    ############################################### Update aylien_news.csv ###############################################
    df = pd.read_csv("data/aylien_news.csv")
    df['date'] = pd.to_datetime(df.date, format='%Y/%m/%d')
    df.sort_values(by='date', inplace=True, ascending=False)

    configuration = aylien_news_api.Configuration()

    configuration.api_key['X-AYLIEN-NewsAPI-Application-ID'] = '97c45927'
    configuration = aylien_news_api.Configuration()
    configuration.api_key['X-AYLIEN-NewsAPI-Application-Key'] = '8e5a95f7bafa835d340a1be85a90588a'
    configuration.host = "https://api.aylien.com/news"

    api_instance = aylien_news_api.DefaultApi(aylien_news_api.ApiClient(configuration))

    date = list(df["date"])[0]

    e = str(datetime.date.today())
    s = str((date + datetime.timedelta(days=1)).date())

    from_date = s
    to_date = str((datetime.datetime.strptime(str(from_date), "%Y-%m-%d") + datetime.timedelta(days=5)).date())

    rows = []
    crimes = {'burglary': 0, 'robbery': 0, 'murder': 0, 'kidnapping': 0, 'rape': 0}

    total_news_count = 0

    while dateutil.parser.parse(from_date).date() < dateutil.parser.parse(e).date():
        if dateutil.parser.parse(to_date).date() > dateutil.parser.parse(e).date():
            to_date = e
        for crime in crimes.keys():
            opts = {
                'title': crime,
                'sort_by': 'social_shares_count.facebook',
                'language': ['en'],
                'published_at_start': from_date + 'T00:00:00Z',
                'published_at_end': to_date + 'T00:00:00Z',
                'per_page': 100,
                'source_locations_country': ['IN'],
                'source_locations_state': ['Delhi'],
                'source_locations_city': ['Delhi'],
            }
            headlines = api_instance.list_stories_with_http_info(**opts)
            for i in headlines[0].stories:
                date = i.published_at.date()
                source = i.source.name
                title = i.title
                url = i.links.permalink
                content = i.body
                rows.append([date, source, title, crime, url, content])
                total_news_count += 1
                crimes[crime] += 1
        from_date = str((datetime.datetime.strptime(str(to_date), "%Y-%m-%d") + datetime.timedelta(days=1)).date())
        to_date = str((datetime.datetime.strptime(str(from_date), "%Y-%m-%d") + datetime.timedelta(days=5)).date())

    with open('data/aylien_news.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    ############################################### Update news_data.csv ###############################################

    contents = ""
    for i in range(len(rows)):
        contents = contents + rows[i][5] + " "
    locations = findLocations(contents)

    f = open('data/loc.txt', 'r')
    s = f.read()

    loc = s.split('\n')
    delhi_locs = []
    for i in loc:
        delhi_locs.append(i.lower())

    all_locations = list(set(delhi_locs).intersection(locations))

    if len(all_locations) > 0:
        df1 = pd.read_csv("data/news_data.csv")
        d = {}
        for i in range(len(df1)):
            lst = list(df1.iloc[i])
            location = lst[0]
            dates_lst = lst[1].split("\t")
            dates = []
            for j in dates_lst:
                dates.append(str(j))
            srcs = lst[2].split("\t")
            headlines = lst[3].split("\t")
            types = lst[4].split("\t")
            articles = lst[5].split("\t")

            ages_lst = lst[6].split("\t")
            ages = []
            for i in ages_lst:
                ages.append(int(i))

            businessmans_lst = lst[7].split("\t")
            businessmans = []
            for i in businessmans_lst:
                businessmans.append(int(i))

            urls = lst[8].split("\t")
            d[location] = [dates, headlines, types, articles, ages, businessmans, urls, srcs]

        business = ['businessman', 'jeweller', 'jeweler', 'shop owner', 'property dealer']
        c = 0
        for i in range(len(rows)):
            article = rows[i][-1]  # [date, source, title, crime, url, content]
            date = rows[i][0]
            headline = rows[i][2]
            crime_type = rows[i][3]
            news_url = rows[i][-2]
            if str(news_url) == "nan":
                news_url = "na"
            news_src = rows[i][1]
            businessman = 0
            for j in business:
                if j in article:
                    businessman = 1
                    break
            age = findAge(article)

            for i in all_locations:
                if i in article.lower():
                    c += 1
                    flag = 1
                    for j in loc:
                        if i == j.lower() or i == j:
                            loc_name = j
                            break
                    lst = d.get(loc_name, [[], [], [], [], [], [], [], []])
                    lst[0].append(str(date))
                    lst[1].append(headline)
                    lst[2].append(crime_type)
                    lst[3].append(article)
                    lst[4].append(age)
                    lst[5].append(businessman)
                    lst[6].append(news_url)
                    lst[7].append(news_src)
                    d[i] = lst

        crime_counts = {}
        max_count = 0
        for i in d.keys():
            crime_counts[i] = len(d[i][0])
            if len(d[i][0]) > max_count:
                max_count = len(d[i][0])

        percentile = {}
        for i in crime_counts.keys():
            p = 100 - int((crime_counts[i] / max_count) * 100)
            percentile[i] = p

        rows = []
        header = ['location', 'date', 'source', 'headline', 'crime_type', 'article', 'age', 'businessman', 'url',
                  'percentile']
        rows.append(header)
        for i in d.keys():
            for j in loc:
                if i == j.lower() or i == j:
                    loc_name = j
                    break
            row = [loc_name]
            lst = d[i]
            row.append('\t'.join(lst[0]))
            row.append('\t'.join(lst[7]))
            row.append('\t'.join(lst[1]))
            row.append('\t'.join(lst[2]))
            row.append('\t'.join(lst[3]))
            row.append('\t'.join(repr(n) for n in lst[4]))
            row.append('\t'.join(repr(n) for n in lst[5]))
            row.append('\t'.join(lst[6]))
            row.append(percentile[i])
            rows.append(row)

        data = open('data/news_data.csv', 'w')
        writer = csv.writer(data)
        writer.writerows(rows)
        data.close()

        df1 = pd.read_csv("data/news_data.csv")
        df2 = pd.read_csv("data/area.csv")
        crime_locations = list(df1["location"])

        rows = [list(df2.columns)]
        for i in range(len(df2)):
            loc = df2.iloc[i, 0]
            if loc == "AIIMS":
                continue
            if loc not in crime_locations:
                rows.append(list(df2.iloc[i]))
            else:
                dt = list(df1[df1["location"] == loc].iloc[0])
                age_lst = dt[-4].split("\t")
                crimes = dt[4].split("\t")
                businessman_count = list(dt[-3].split("\t")).count('1')
                crime_count = len(age_lst)

                age_crimes = {"0-21": 0, "22-50": 0, "50+": 0}
                crime_type = {'burglary': 0, 'robbery': 0, 'murder': 0, 'kidnapping': 0, 'rape': 0}
                for j in age_lst:
                    age = int(j)
                    if age > 0 and age <= 21:
                        age_crimes["0-21"] += 1
                    elif age > 21 and age <= 50:
                        age_crimes["22-50"] += 1
                    elif age > 50:
                        age_crimes["50+"] += 1

                for j in crimes:
                    crime_type[j] += 1

                lst = list(df2.iloc[i])
                lst[1] = crime_count
                lst[2] = age_crimes["0-21"]
                lst[3] = age_crimes["22-50"]
                lst[4] = age_crimes["50+"]
                lst[5] = crime_type["murder"]
                lst[6] = crime_type["burglary"]
                lst[7] = crime_type["robbery"]
                lst[8] = crime_type["kidnapping"]
                lst[9] = crime_type["rape"]
                lst[10] = 100 - dt[-1]
                lst[-1] = businessman_count
                rows.append(lst)

        with open('data/area.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerows(rows)

