import re
from collections import namedtuple
import requests as req
from bs4 import BeautifulSoup


UR = 'http://u23.women.2017.volleyball.fivb.com/en/teams/chn%20china/team_roster'

def _send_requests():
    try:
        response = req.get(UR, 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0')
    except req.HTTPError as error:
        print('%s' % error.args)
        raise
    else:
        assert response.status_code == 200, 'No connection %s' % response.status_code
        return response

class TableHelper(object):
    def __init__(self, table_data):
        self._table_data = table_data

    def _parse_table(self):
        assert len(self._table_data.text) > 0
        soup = BeautifulSoup(self._table_data.text, 'html.parser')
        
        table = soup.find('section', class_='tabs-content').find('table')
        # assert table is not None, 'None'
        rows = table.find_all('tr')

        all_statistics = namedtuple('Statistics', 'players, links')
        player_statistics = []
        links = []

        
        for row in rows:
            column_element = row.find_all('td')
            column_link_element = row.find_all('a')
            
            if len(column_link_element) > 0:
                links.append(re.search(r'href\=\"(\D.*)\"\s+id\=', str(column_link_element[0])).group(1))
            
            if len(column_element) > 0:
                statistic = [element.text.strip() for element in column_element]  
                player_statistics.append(statistic)
                # assert len(player_statistics) > 0

        player_refined_statistic = []

        for player_statistic in player_statistics:
            if len(player_statistic) > 0:
                p = player_statistic[1], player_statistic[2], player_statistic[3], player_statistic[4], player_statistic[5], player_statistic[6]
                player_refined_statistic.append(tuple(p))
                # statistic_column_index = [1, 2]
                # statistic_column_index = [1, 2, 3, 4, 5, 6]
                # player_refined_statistic.append([player_statistics[column_index] for column_index in statistic_column_index])

        # return player_refined_statistic
        return all_statistics(player_refined_statistic, links)

print(TableHelper(_send_requests())._parse_table())
    

# u = 'http://u23.women.2017.volleyball.fivb.com/en/teams/chn%20china/team_roster'
# response = req.get(u, 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0')
# assert response.status_code == 200, 'No connection %s' % response.status_code
# soup = BeautifulSoup(response.text, 'html.parser')
# table = soup.find('section', class_='tabs-content').find('table')
# assert table is not None, 'None'
# rows = table.find_all('tr')
# a = []
# n = []
# for row in rows:
#     columns = row.find_all('td')
#     links = row.find_all('a')
#     if len(links) > 0:
#         n.append(links[0])

#     column = [element.text.strip() for element in columns]
#     a.append(column)

#     t = []
#     for w in a:
#         if len(w) > 0:
#             p = [1, 2, 3, 4, 5, 6]
#             t.append([w[x] for x in p])

# # print(t)
# pattern = r'href\=\"(\D.*)\"\s'
# r = [re.search(pattern, str(x)).group(1) for x in n]
# print(r)