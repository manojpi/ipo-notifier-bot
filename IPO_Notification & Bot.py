import requests
import urllib
import re
import datetime
import pytz


NPT = pytz.timezone('Asia/Kathmandu')

ipo_dates = list()
ipo_data = dict()


def get_ipo():

    url = 'https://www.sharesansar.com/existing-issues?draw=1&columns[0][data]=DT_Row_Index&columns[0][name]=&columns[0][searchable]=false&columns[0][orderable]=false&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=company.symbol&columns[1][name]=&columns[1][searchable]=true&columns[1][orderable]=false&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=company.companyname&columns[2][name]=&columns[2][searchable]=true&columns[2][orderable]=false&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=ratio_value&columns[3][name]=&columns[3][searchable]=false&columns[3][orderable]=false&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=total_units&columns[4][name]=&columns[4][searchable]=false&columns[4][orderable]=false&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=issue_price&columns[5][name]=&columns[5][searchable]=false&columns[5][orderable]=false&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=opening_date&columns[6][name]=&columns[6][searchable]=true&columns[6][orderable]=false&columns[6][search][value]=&columns[6][search][regex]=false&columns[7][data]=closing_date&columns[7][name]=&columns[7][searchable]=true&columns[7][orderable]=false&columns[7][search][value]=&columns[7][search][regex]=false&columns[8][data]=final_date&columns[8][name]=&columns[8][searchable]=true&columns[8][orderable]=false&columns[8][search][value]=&columns[8][search][regex]=false&columns[9][data]=listing_date&columns[9][name]=&columns[9][searchable]=true&columns[9][orderable]=false&columns[9][search][value]=&columns[9][search][regex]=false&columns[10][data]=issue_manager&columns[10][name]=&columns[10][searchable]=false&columns[10][orderable]=false&columns[10][search][value]=&columns[10][search][regex]=false&columns[11][data]=status&columns[11][name]=&columns[11][searchable]=false&columns[11][orderable]=false&columns[11][search][value]=&columns[11][search][regex]=false&columns[12][data]=view&columns[12][name]=&columns[12][searchable]=false&columns[12][orderable]=false&columns[12][search][value]=&columns[12][search][regex]=false&columns[13][data]=right_eligibility_link&columns[13][name]=&columns[13][searchable]=false&columns[13][orderable]=false&columns[13][search][value]=&columns[13][search][regex]=false&start=0&length=20&search[value]=&search[regex]=false&type=1&_=1654568340288'
    header_info = {
        'x-requested-with': 'XMLHttpRequest'
    }

    response = requests.get(url, headers=header_info)
    web_data = response.json()

    web_data = web_data["data"]

    for item in web_data:
        item.pop('ratio_value')
        item.pop('right_eligibility_link')
        item.pop('announcement_link')
        item.pop('view')
        item.pop('DT_Row_Index')

    for i in web_data:
        if i['status'] == -1:
            company_name_and_symbol_tag = i['company']['companyname'] + " " + i['company']['symbol']
            reg_exp = '<a.*?>(.*?)</a>'   # Use Non-Greeding matching by using '?'
            company = re.findall(reg_exp, company_name_and_symbol_tag)

            opening_date = datetime.datetime.strptime(i['opening_date'], "%Y-%m-%d")
            closing_date = datetime.datetime.strptime(i['closing_date'], "%Y-%m-%d")

            deadline = "{} - {}".format(opening_date.strftime("%d %B, %Y (%A)"), closing_date.strftime("%d %B, %Y (%A)"))

            bot_message = "New IPO Alert : {} ({})\nDeadline : {}".format(company[0], company[1], deadline)

            ipo_dates.append("{} ({})".format(company[0], company[1]))
            ipo_data.update({"{} ({})".format(company[0], company[1]): {"opening_date": opening_date, "closing_date": closing_date, "message": bot_message}})

            return bot_message


TOKEN = "5351457034:AAHad8g-n0Ez_Xl9ID2fQe3exxuWCr73H-s"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    r = requests.get(url)
    content = r.content.decode('utf8')
    return content


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def main():

    while True:

        telegram_group_id = "@ipo_notification"

        current_time = datetime.datetime.now(NPT).strftime('%Y, %d, %m')
        current_time = datetime.datetime.strptime(current_time, '%Y, %d, %m')

        get_ipo()
        
        for ipo in ipo_dates:

            # if current_time >= ipo_data[ipo]["opening_date"] and current_time <= ipo_data[ipo]["closing_date"]:
            #     send_message(ipo_data[ipo]["message"], "@iamculi")

            send_message(ipo_data[ipo]["message"], 1306045488)


if __name__ == '__main__':
    main()
