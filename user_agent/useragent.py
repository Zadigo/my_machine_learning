import collections

__version__  = '0.1.0'

_AGENTS_IST = [
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0"
]

def get_user_agent():
    """
    Returns a user agents for connexions
    to the internet using `requests`
    """
    agents = collections.namedtuple('Agents', ['heaer'])
    return agents(_AGENTS_IST)

def construct_user_agent(browser, version, os_type, browser_na, version_two):
    agent = '{browser}/{version} (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 {browser_na}/{version_two}'
    return agent.format(browser=browser, version=version, browser_na=browser_na, version_two=version_two)

# print(construct_agent('a', '5.0', 'Win', 'r', '12.2'))

def Main():
    return get_user_agent()

if __name__ == '__main__':
    Main()