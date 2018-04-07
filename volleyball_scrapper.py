"""
.. note:: Response
"""

import re
import time
import requests as req
# import useragent as agent
from bs4 import BeautifulSoup as bs
import urllib.parse as pr 

URLS = [
    u'http://rio2016.fivb.com/en/volleyball/women/teams/{}/team_roster',
    u'http://u20.women.2017.volleyball.fivb.com/en/teams/{}/team_roster',
    u'http://u20.women.2015.volleyball.fivb.com/en/competition/teams/{}/team_roster',
    u'http://u20.women.2015.volleyball.fivb.com/en/competition/teams/'
]

# [group, country, url_country]
COUNTRIES = {
    "algeria": ['group2', 1, 'alg-algeria'],
    "argentina": ['group2', 2, 'arg-argentina'],
    "australia": ['group3', 3, 'aus-australia'],
    "cameroon": ['group3', 4, 'cmr-cameroon'],
    "china": ['group1', 5, 'chn-china'],
    "colombia": ['group2', 6, 'col-colombia'],
    "croatia": ['group2', 7, 'cro-croatia'],
    "czech-republic": ['group2', 8, 'cze-czech republic'],
    "bulgaria": ['group2', 9, 'bul-bulgaria'],
    "brazil": ['group1', 10, 'bra-brazil'],
    "dominican-republic": ['group1', 11, 'dom-dominican republic'],
    "france": ['group3', 12, 'fra-france'],
    "germany": ['group2', 13, 'ger-germany'],
    "hungary": ['group3', 14, 'hun-hungary'],
    "italy": ['group1', 15, 'ita-italy'],
    "japan": ['group1', 16, 'jpn-japan'],
    "kazakhstan": ['group2', 17, 'kaz-kazakhstan'],
    "korea": ['group2', 18, 'kor-korea'],
    "mexico": ['group3', 19, 'mex-mexico'],
    "netherlands": ['group1', 20, 'ned-netherlands'],
    "poland": ['group2', 21, 'pol-poland'],
    "puerto-rico": ['group2', 22, 'pur-puerto rico'],
    "russia": ['group1', 23, 'rus-russia'],
    "serbia": ['group1', 24, 'srb-serbia'],
    "trinidad": ['group3', 25, 'tto-trinidad and tobago'],
    "turkey": ['group1', 26, 'tur-turkey'],
    "usa": ['group2', 27, 'usa-usa'],
    "venezuela": ['group3', 28, 'ven-venezuela'],
    "egy-egypt": ['', 29, 'egy-egypt'],
    "peru": ['', 30, 'per-peru'],
    "cuba": ['', 31, 'cub-cuba'],
    "taipei": ['', 32, 'tpe-chinese taipei'],
}

USERAGENT = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0"

# 4: rus-russia/players/angelina-lazarenko?id=48260 id="...
# 5: rus-russia/players/angelina-lazarenko?id=48260
# 6: <strong> Wing Spiker</strong>
# 7: 14/02/1996
# 8: players/victoria-zhurbenko
# 9: >71 kg or >171 c or 0
# 10: > Spike</span><strong> 296</strong>
# 11: > Block</span><strong> 296</strong>
PATTERNS = [
    r'\>([a-zA-Z].*)\<\/[a]\>',
    r'\<td\>([0-9]{3})\<\/td\>',
    r'\<td\>([0-9]{2})\<\/td\>',
    r'\<td\>(0|[2-3]\d+)\<\/td\>\n\<td\>(0|[2-3]\d+)\<\/td\>',
    r'(([a-z]{3}\-[a-z]+\/)players\/\w.*)(\")',
    r'[a-z]{3}\-[a-z]+\/players\/\w.*\?id\=\w+',
    r'\>\s+Position\<\/span\>\s+\<strong\>\s+(Opposite spiker|Setter|Wing spiker|Middle blocker|Universal|Libero)',
    r'[0-9]{2}\/[0-9]{2}\/[0-9]{4}',
    r'players\/(\w.*)\?',
    r'\>([0-9]{1,3})',
    r'\>\s+Spike\<\/span\>\s+\<strong\>\s+([0-9]+)',
    r'\>\s+Block\<\/span\>\s+\<strong\>\s+([0-9]+)',
    r'Value_1\"\>([0-9]{2}\/[0-9]{2}\/[0-9]{4})',
    r'Value\_[2]\"\>([0-9]{1,3})',
    r'Value\_[3]\"\>([0-9]{1,3})',
    r'Value\_[4]\"\>([0-9]{1,3})'
]

POSITIONS = {
    'Middle blocker': 3,
    'Setter': 1,
    'Universal': 4,
    'Wing spiker': 2,
    'Libero': 6,
    'Opposite spiker': 4
}

def _send_requests(url_reference):
    """
    This oue is use to sen reuests to the IVB
    website. It sens a response obect bac the
    caer that can be parse using BeautiuSoup.
    """

    # istinguish integer or taing an ur in the URS ist
    # ro sening a string type ur
    url_type = type(url_reference).__name__
    if url_type == 'int':
        url_to_get = str(URLS[url_reference]).format(COUNTRIES['china'][2])
    
    else:
        url_to_get = url_reference

    try:
        response = req.get(url_to_get, USERAGENT)
    except req.HTTPError as error:
        raise ConnectionError("{reason}".format(reason=error.args))
    else:
        code = response.status_code
        if code >= 200 and code < 300:
            print('Connection estabished:', code)
            return response
        else:
            print('Connection failed:', code)
            
def _write_csv(player_details_object, header=False, file_name='volleyball.csv'):
    print('Writting CSV for', player_details_object[0])
    with open(file_name, 'a', encoding='utf_8') as f:
        if header is True:
            f.writelines('name,date_of_birth,height,weight,spike,block,position_number')
            f.writelines('\n')

        for player_detail_object in player_details_object:
            f.writelines(str(player_detail_object).strip())
            f.writelines(',')
        f.writelines(str(5))
        f.writelines('\n')

def scrap_player_position(url_number):
    """
    Payer positio

    This oue is use i orer to scrap the positions
    o the payers ro the iVB ebsite.

    It sens reuests to the payers page an reas the
    position section in orer to create a nuber or
    eterining the position o the payer on the court.

    Use ur_nuber to seect the UR that you want to parse
    ro the website.
    """
    page = _send_requests(int(url_number))
    soup = bs(page.text, 'html.parser')
    links = soup.find_all('a')

    for link in links:
        # Test i there is a payer i in avaiabe
        id_exists = re.search(PATTERNS[4], str(link))
        if id_exists is not None:
            get_relative_links = re.search(PATTERNS[5], str(id_exists.group(1)))
            # Construct url link
            # .../rus-russia/players/angelina-lazarenko?id=48260
            print('Constructing link...')

            constructed_player_page_url_link = pr.urljoin(URLS[3], get_relative_links.group())
            time.sleep(1)

            print('Getting payer page id:', re.search(r'id\=([0-9]+)', constructed_player_page_url_link).group(1))
            player_page = _send_requests(constructed_player_page_url_link)
            soup = bs(player_page.text, 'html.parser')
            # Get sections o the page
            player_details = soup.find('section', id='playerDetails')
            player_career_details = soup.find('section', id='playerCareer')

            name = date_of_birth = height = weight = ''
            spike = block = ''

            if player_details is not None:
                name = player_details.div.div.h4.text

                for player_detail in player_details.div.div.dl:
                    if re.search(PATTERNS[12], str(player_detail)) is not None:
                        date_of_birth = re.search(PATTERNS[12], str(player_detail)).group(1)

                    if re.search(PATTERNS[13], str(player_detail)) is not None:
                        height = re.search(PATTERNS[13], str(player_detail)).group(1)
                    # else:
                    #     # Sometimes value_2 becomes value_3 and value_3 becomes value_4
                    #     # so, to mitigate that, we search we search in value 3 to see
                    #     # if we can find the values we are looking for
                    #     if re.search(PATTERNS[14], str(player_detail)) is not None:
                    #         height = re.search(PATTERNS[14], str(player_detail)).group(1)

                    if re.search(PATTERNS[14], str(player_detail)) is not None:
                        weight = re.search(PATTERNS[14], str(player_detail)).group(1)
                    # else:
                    #     if re.search(PATTERNS[15], str(player_detail)) is not None:
                    #         weight = re.search(PATTERNS[15], str(player_detail)).group(1)
            
            if player_career_details is not None:
                for player_career_detail in player_career_details.ul:
                    if re.search(PATTERNS[6], str(player_career_detail)) is not None:
                        position = re.search(PATTERNS[6], str(player_career_detail)).group(1)
                        position_number = POSITIONS[position]
                    
                    if re.search(PATTERNS[10], str(player_career_detail)) is not None:
                        spike = re.search(PATTERNS[10], str(player_career_detail)).group(1)
                    
                    if re.search(PATTERNS[11], str(player_career_detail)) is not None:
                        block = re.search(PATTERNS[11], str(player_career_detail)).group(1)
                
            if name is None:
                name = '0'
            else:
                name = str(name).strip()
            if date_of_birth is None:
                date_of_birth = '0/0/0'
            if height is None:
                height = '0'
            if weight is None:
                weight = '0'
            if spike is None:
                spike = '0'
            if block is None:
                block = '0'
            
            # Create tuple for writting the CSV file
            player_statistics = tuple((name, date_of_birth, height, weight, spike, block, position_number))
            
            _write_csv(player_statistics)

# def main():
#     pass

# if __name__ == '__main__':
#     main()

scrap_player_position(2)