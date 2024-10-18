from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from hudl_namespace import *
import ssl

# using firefox as the selenium browswer
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options


# used for searching elements by various structures
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import pandas as pd
import re

# suppressing the pop up window of what is happening
opts = Options()
opts.add_argument('--headless')
driver = Firefox(options=opts)

# regular expression
import re

def nsa_pot(url):
    if len(url) < 1:
        url = 'https://mgoblue.com/sports/football/stats/2023/bowling-green/boxscore/25649'

    driver.get(url)
    time.sleep(5)

    # looking for the headers of the play by plays
    ## Box Score
    ## Team
    ## Individual
    ## Drive Chart
    ### Away Team
    ### Home Team
    ## Play-by-Play
    ### 1st
    ### 2nd
    ### 3rd
    ### 4th
    ### OT
    ## Participation
    ## Game Information
    all_buttons = driver.find_elements(By.TAG_NAME, 'button')

    # creating a list of all the buttons on inital load of page
    x=[]
    for i in all_buttons:
        x.append(i.text)

    # teams playing game
    team_names = []

    print(x)

    # clicking all buttons to load the correct pages
    for box_score in all_buttons:
        if box_score.text.lower() in ['box score','team','individual','drive chart','play-by-play','participation','game information']:
            print(box_score.text)
            box_score.click()
            time.sleep(2)
            # loading all the quarters of the game for Soup
            if box_score.text.lower() in ['play-by-play']:
                quarters = driver.find_elements(By.TAG_NAME, 'button')
                for qtr in quarters:
                    if qtr.text.lower() in ['1st','2nd','3rd','4th','ot']:
                        print(qtr.text)
                        qtr.click()
                        time.sleep(2)
            # getting the team names
            elif box_score.text.lower() in ['drive chart']:
                teams = driver.find_elements(By.TAG_NAME, 'button')
                for ii in teams:
                    if ii.text not in x + ['All']:
                        print(ii.text)
                        team_names.append(ii.text)

    
    # adding team names to dictionary
    name_dict = dict()
    name_dict[away_name] = team_names[0]
    name_dict[home_name] = team_names[1]

    # find the game info button
    game_info_button = driver.find_element(By.XPATH, "//span[text()='Game Information']/..")
    # Click the button
    driver.execute_script("arguments[0].click();", game_info_button)
    # this is different because it is a scrollable button so revealing it needs to be done with javascript.

    # selenium to bs4
    page_source = driver.page_source
    
    # closing out selenium
    driver.close()
    driver.quit()

    soup = BeautifulSoup(page_source, 'lxml')
    return soup, name_dict

def nsa_playmaker(soup, name_dict):

    # Save the prettified HTML to a text file
    with open('C:\\Users\\lwwil\\OneDrive\\Documents\\Python Scripts\\009 - cfbslapPY dev_selenium\\cfb_slapPY\\src\\scraped_page.txt', 'w', encoding='utf-8') as file:
        file.write(soup.prettify())

    # Find the thead's
    table_header = soup.find_all('thead', class_='s-table-header')

    # loopin through all     
    for header in table_header:
        if header:
            # Find all th elements within the table header
            ths = header.find_all('th', class_='s-table-header__column')
            th_options = [th.get_text(strip=True) for th in ths]
            
            print(th_options)
        
        else:
            print('broked')
            
        if any(word.lower() == '-' for word in th_options):
            # using the scoring summary table and looking for '-' and then taking the last two entries to determine who is home and away
            break
        else:
            # reseting for next loop/breaking below if not found
            th_options = []
    
    # team abbreviations
    # 2024 and after
    if th_options:
        name_dict[home_abbr] = th_options[-1]
        name_dict[away_abbr] = th_options[-2]
    else:    
        # 2023 and before    
        name_dict[home_abbr] = str(soup.find(id="home-team").string).strip()
        name_dict[away_abbr] = str(soup.find(id="away-team").string).strip()

    # Point abbreviations to names
    name_dict[name_dict[home_abbr]] = name_dict[home_name]
    name_dict[name_dict[away_abbr]] = name_dict[away_name]

    # Extract game location, date and time
    name_dict[matchup] = '{} at {}'.format(name_dict[away_name],name_dict[home_name])
    print(name_dict)
    

    # old 2023 game info code
    # info_tag = soup.find('dl', class_='text-center inline')
    # dt = info_tag('dt')
    # dd = info_tag('dd')
    # info_dict = {str(dt[i].string).strip():str(dd[i].string).strip() for i in range(len(dt))}
    # # print(info_dict)
    # name_dict[game_location] = info_dict['Site:']
    # name_dict[game_date] = info_dict['Date:']
    # name_dict[game_time] = info_dict['Kickoff Time:']

    # Find the specific div containing the game information
    game_info_div = soup.find('div', class_='s-expansion-panel__content')

    # Create a dictionary to hold the extracted data
    game_info = {}

    # Extract the text for each piece of information
    if game_info_div:
        items = game_info_div.find_all('div', class_='box-border')
        for item in items:
            title = item.find('span', class_='s-text-paragraph-bold').get_text(strip=True).replace(':','')
            value = item.find('span', class_='s-text-paragraph').get_text(strip=True)
            game_info[title] = value

    # Print the extracted information
    print(game_info)

    # left off here

    # 2023 code
    # Extract kicker names to determine name format for regex and opening kickoff
    # kickers = soup.find(id="individual-kickoffs-stats")
    # # print(kickers.prettify())
    # header = kickers("td", {"class":"s-text-small","data-label":""})
    # # print(header)
    # kicker_names = list()
    # for tag in header:
    #     name = list(tag.stripped_strings)[0]
    #     if name != 'Totals':
    #         kicker_names.append(name)

    # name_dict[home_kicker] = kicker_names[-1]
    # name_dict[away_kicker] = kicker_names[0]

    # 2024 code
    # Find the section with "Kickoffs"
    kickoffs_section = soup.find_all(text=re.compile('Kickoffs'))
    
    for ko in kickoffs_section[:2]:
        # Navigate to the parent element to find the table
        table = ko.find_parent().find_next('div', class_='s-table__wrapper')

        # Extract column headers
        headers = []
        header_cells = table.find_all('th')
        for header in header_cells:
            headers.append(header.get_text(strip=True))

        # Extract rows
        rows = []
        body_rows = table.find_all('tr', class_='s-table-body__row')
        for row in body_rows:
            cells = row.find_all('td')
            rows.append([cell.get_text(strip=True) for cell in cells])

        # Create a DataFrame
        df = pd.DataFrame(rows, columns=headers)

        print(df)
    # kickoffs_section = kickoffs_section[:2]

    print('kickoffs_section', kickoffs_section)

    # kicker_names = list()

    # for ko in kickoffs_section:
    #     if ko:
    #         # Navigate to the parent element to find the player names
    #         table = ko.find_parent().find_next('div', class_='s-table__wrapper')
            
    #         # Extract player names
    #         player_cells = table.find_all('td', class_='s-text-regular s-table-body_cell s-text-regular !s-text-paragraph-small s-table-body_cell')

    #         # Get the player names
    #         player_names = [cell.get_text(strip=True) for cell in player_cells if cell.find('div')]
            
    #         # Since the player name is within a div, we extract the text from that div
    #         player_names = [cell.find('div').get_text(strip=True) for cell in player_cells if cell.find('div')]
            
    #         kicker_names.append(player_names)
    #         print(player_names)
    #     else:
    #         print("Kickoffs section not found.")
    
    # print(kicker_names)

    # Extract play-by-play data from box score link
    # pbp = soup.find(id="play-by-play")
    # need multiple pbp for each quarter/period
    quarters = list()
    for qtr in ('1st','2nd','3rd','4th','OT'):
        print(qtr)
        q_tags = soup.find_all(id = qtr)
        # print(q_tags)
        # Create new list to store a list of strings for each drive
        drives = list()
        for q_tag in q_tags:      
            # Store each drive as a list of bs tags
            drives_raw = list(q_tag(['table', 'dl']))
            for drive in drives_raw:
                if drive.name == 'dl':
                    score_string = drive('dd')[0].string.strip()
                    drives[-1].append([score_string])
                else:
                    rows = drive('tr')
                    play_strings = list()
                    header_dex = 0
                    for row in rows:
                        strings = list()
                        header = row('th')
                        if all((len(header) > 0, header_dex == 0)) and header[0].string:
                            strings.append(header[0].string.strip())
                            header_dex = 1  
                        entries = row('td')
                        for entry in entries:
                            if entry.string:
                                string = entry.string.strip()
                                strings.append(string)
                            else:
                                string = ''
                                for hidden_string in entry.stripped_strings:
                                    string = '{} {}'.format(string,hidden_string)
                                if len(string) > 0:
                                    strings.append(string)
                        if len(strings) > 0:
                            play_strings.append(strings)
                    drives.append(play_strings)
        quarters.append(drives)

    # As a test, print opening kickoff strings
    def print_drive(drive):
        for string in drive:
            print(string)

    print(quarters)

    print_drive(quarters[0][0])
    return quarters, name_dict