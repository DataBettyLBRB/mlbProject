# THE PURPOSE OF THIS CODE IS TO EXTRACT DATA FROM THE FOLLOWING SITE:
# https://www.cbssports.com/mlb/schedule/20210403/


# CREATE A DATETIME INDEX LIST USING FIRST AND LAST DATE
def CreateDateTimeIndex(date_1, date_2):
    start = datetime.datetime.strptime(date_1, "%Y-%m-%d")
    end = datetime.datetime.strptime(date_2, "%Y-%m-%d")

    date_range = (start + datetime.timedelta(days=x) for x in range(0, (end - start).days + 1))

    # FORMAT WILL BE RETURNED AS YYYYMMDD
    return [d.strftime("%Y%m%d") for d in date_range]


if __name__ == '__main__':
    import requests
    import pandas as pd
    import datetime
    from bs4 import BeautifulSoup

    results = []
    schedule = []
    # CREATE AN INDEX BASED ON THE DATE RANGE FROM OPENING DAY TO CLOSING DAY
    dateIndex2021 = CreateDateTimeIndex('2021-04-03', '2021-04-07')

    dates = []
    # CREATE URL INDEX BASED ON DATES
    for date in dateIndex2021:
        mlb_schedule_url = f'http://cbssports.com/mlb/schedule/{date}'
        page = requests.get(mlb_schedule_url).text
        soup = BeautifulSoup(page, "lxml")

        dates.append(soup.find('h4').text.strip())
        table = soup.find('table', attrs={'class': 'TableBase-table'})

        headers = []
        for i in table.find_all('th'):
            headers.append(i.text.strip())

        content = []
        for tr in table.tbody.find_all('tr'):
            t_row = {}

            for td, th in zip(tr.find_all('td'), headers):
                t_row[th] = td.text.replace('\n', '').strip()
            content.append(t_row)

        df = pd.DataFrame(content)

        for date in dates:
            df['date'] = date

            if len(df.columns) == 7:
                results.append(df)
            else:
                schedule.append(df)

    results = pd.concat(results)
    schedule = pd.concat(schedule)

    results.to_csv('Results.csv', index=False)
    schedule.to_csv('Schedule.csv', index=False)