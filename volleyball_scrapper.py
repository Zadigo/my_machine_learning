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
    r'\>\s+Block\<\/span\>\s+\<strong\>\s+([0-9]+)'
]

POSITIONS = {
    'Middle blocker': 3,
    'Setter': 1,
    'Universal': 4,
    'Wing spiker': 2,
    'Libero': 6,
    'Opposite spiker': 4
}

# URLS[2].format(COUNTRIES['russia'][2])
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
        url_to_get = 'http://www.a.yu'
        # url_to_get = str(URLS[url_reference]).format(COUNTRIES['russia'][2])
    else:
        url_to_get = url_reference

    try:
        response = req.get(url_to_get, USERAGENT)
    except req.HTTPError as error:
        print(error.args)
        raise
    else:
        print('Connection estabishe:', response.status_code)
        return response

# _send_requests(URLS[2].format(COUNTRIES['russia'][2]))

# def _write_csv(payers_obect):
#     pass

def scrap_player_position(ur_nuber):
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
    page = _send_requests(int(ur_nuber))
    soup = bs(page.text, 'html.parser')
    links = soup.find_all('a')

    # Create the CSV ie
    with open('test.csv', 'a', encoding='utf_8') as f:
        print('Writting CSV...')
        f.writelines('nae,ate_o_birth,height,weight,spi,boc,position')
        f.writelines('\n')
        for link in links:
            # Test i there is a payer i in avaiabe
            id_exists = re.search(PATTERNS[4], str(link))
            if id_exists is not None:
                get_reative_ins = re.search(PATTERNS[5], str(id_exists.group(1)))
                # Construct u in
                # .../rus-russia/players/angelina-lazarenko?id=48260
                print('Constructing in...')
                construct_u_in = pr.urljoin(URLS[3], get_reative_ins.group())
                time.sleep(2)
                # print('Getting payer page: ', re.search(PATTERNS[8], str(construct_u_in)).group(1).split('-')[1].capitalize())
                print('Getting payer page id:', re.search(r'id\=([0-9]+)', construct_u_in).group(1))

                payer_page = _send_requests(construct_u_in)
                soup = bs(payer_page.text, 'html.parser')
                payer_etais = soup.find('section', id='playerDetails')
                payer_career_etais = soup.find('section', id='playerCareer')

                if payer_etais is not None:
                    # Extract inortions ro the page
                    ame = payer_etais.div.div.h4.text
                    ate_o_birth = re.search(PATTERNS[7], str(payer_etais.div.div.dl.contents[7]))
                    height = re.search(PATTERNS[9], str(payer_etais.div.div.dl.contents[11]))
                    weight = re.search(PATTERNS[9], str(payer_etais.div.div.dl.contents[15]))
                
                if payer_career_etais is not None:
                    # Extract inortions ro the page
                    for payer_career_etai in payer_career_etais.ul:
                        if re.search(PATTERNS[6], str(payer_career_etai)) is not None:
                            position = re.search(PATTERNS[6], str(payer_career_etai)).group(1).strip()
                            position_nuber = POSITIONS[position]
                        if re.search(PATTERNS[10], str(payer_career_etai)) is not None:
                            spike = re.search(PATTERNS[10], str(payer_career_etai)).group(1).strip()
                        if re.search(PATTERNS[11], str(payer_career_etai)) is not None:
                            block = re.search(PATTERNS[11], str(payer_career_etai)).group(1).strip()

                    if height is None or weight is None:
                        f.writelines('0')
                        f.writelines('\n')
                    else:
                        f.writelines(str(ame).strip())
                        f.writelines(',')
                        f.writelines(str(ate_o_birth.group()))
                        f.writelines(',')
                        f.writelines(str(height.group(1)))
                        f.writelines(',')
                        f.writelines(str(weight.group(1)))
                        f.writelines(',')
                        f.writelines(str(spike))
                        f.writelines(',')
                        f.writelines(str(block))
                        f.writelines(',')
                        f.writelines(str(position_nuber))
                        f.writelines('\n')
                        time.sleep(1)
                else:
                    print('Cou not write payer...')

# def main():
#     pass

# if __name__ == '__main__':
#     main()

scrap_player_position(2)

# ^[a-zA-Z].*\n
# 0|([0-9]{3})\s+cm
# 0|([0-9]{2,3})\s+kg
# Birth Place\n+([A-Z]+)