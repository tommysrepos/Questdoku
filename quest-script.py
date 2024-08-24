from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import json

driver = webdriver.Chrome()
driver.get('https://oldschool.runescape.wiki/w/Quests/List')

quests = []

def scrape_quest_info():
    current_quest = {}
    current_quest['name'] = driver.find_element(By.XPATH, '//*[@id="firstHeading"]/span').get_attribute('innerHTML')

    table_xpath = '//*[@id="mw-content-text"]/div[1]/table[3]'
    difficulty_levels = ['Novice', 'Intermediate', 'Experienced', 'Master', 'Grandmaster']

    # current_quest = {'difficulty': None}

    for level in difficulty_levels:
        try:
            # Construct XPath to search for the specific difficulty level within the table
            xpath = f'{table_xpath}//*[contains(text(), "{level}")]'
            difficulty_element = driver.find_element(By.XPATH, xpath)
            current_quest['difficulty'] = level

            if 'Special' in current_quest['difficulty']:
                    return
            
            break  # Exit the loop once the correct difficulty is found
        except NoSuchElementException:
            continue  # Try the next level if the current one is not found
    
    try:
        quest_release_date = driver.find_element(By.XPATH, '//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[4]/td/a[2]').get_attribute('innerHTML')
    except NoSuchElementException:
        quest_release_date = driver.find_element(By.XPATH, '//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[4]/td/a[2]').get_attribute('innerHTML')

    if int(quest_release_date) < 2013:
        current_quest['releaseDate'] = '2001-2007'
    else:
        current_quest['releaseDate'] = '2013-2024'

    quest_membership = driver.find_element(By.XPATH, '//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[5]/td').get_attribute('innerHTML').strip().lower()

    if quest_membership == 'yes':
        current_quest['membership'] = {'Members' : 'https://oldschool.runescape.wiki/images/Member_icon.png?1de0c'}
    elif quest_membership == 'no':
        current_quest['membership'] = {'F2P' : 'https://oldschool.runescape.wiki/images/Free-to-play_icon.png?628ce'}

        table_xpath = '//*[@id="mw-content-text"]/div[1]/table[2]/tbody'

# List of quest series to search for
    quest_series_list = [
        "Camelot", "Demon Slayer", "Dorgeshuun", "Dragonkin", "Elemental Workshop", 
        "Elf", "Fairytale", "Fremennik", "Gnome", "Kharidian", "Kourend", 
        "Mahjarrat", "Miscellania", "Myreque", "Order of Wizards", "Penguin", 
        "Pirate", "Rag and Bone Man", "Red Axe", "Temple Knight", "Troll", 
        "Twilight Emissaries", "None"
    ]

    try:
        # Locate the table element
        table_element = driver.find_element(By.XPATH, table_xpath)
        
        # Extract the text content of the table
        table_text = table_element.text
        
        # Search for each quest series in the text content
        for series in quest_series_list:
            if series in table_text:
                current_quest['series'] = series
                break  # Exit loop once the series is found
        
    except NoSuchElementException:
        print("Table element not found.")

    current_skill_requirement = driver.find_elements(By.XPATH, '//*[@id="mw-content-text"]/div[1]/table[3]/tbody/tr[5]/td/ul/li/span/a')

    current_skill_image = driver.find_elements(By.XPATH, '//*[@id="mw-content-text"]/div[1]/table[3]/tbody/tr[5]/td/ul/li/span/span/a/img')

    skill_requirements = {}

    # Iterate through skills and try to find matching images
    for i in range(len(current_skill_requirement)):
        skill_name = current_skill_requirement[i].get_attribute('innerHTML')
        
        # Locate the parent 'li' element for the current skill
        parent_li = current_skill_requirement[i].find_element(By.XPATH, './ancestor::li')
        
        # Find the image within the same 'li' element
        try:
            skill_image = parent_li.find_element(By.XPATH, './/span/span/a/img')
            skill_image_src = skill_image.get_attribute('src')
            
            # Add the skill and image to the dictionary
            skill_requirements[skill_name] = skill_image_src

        except NoSuchElementException:
            # No image found in the same 'li' element, skip to the next skill
            continue

    current_quest['requirements'] = skill_requirements

    print(current_quest)
    quests.append(current_quest)

    json_all_quest_info = json.dumps(quests, indent=2)
    with open('quests.js', 'w') as questList:
            questList.write(f"var quests = {json_all_quest_info} \n")
            questList.flush()
    

quest_links = driver.find_elements(By.XPATH, '/html/body/div[3]/div[3]/div[5]/div[1]/table[2]/tbody/tr/td[2]/a')

i = 0
while i < 22:
    quest_links[i].click()
    scrape_quest_info()
    driver.back()
    time.sleep(1)
    quest_links = driver.find_elements(By.XPATH, '/html/body/div[3]/div[3]/div[5]/div[1]/table[2]/tbody/tr/td[2]/a')
    i+= 1
    

quest_links = driver.find_elements(By.XPATH, '//*[@id="mw-content-text"]/div[1]/table[4]/tbody/tr/td[2]/a')

special_quest_number = driver.find_element(By.XPATH, '//*[@id="mw-content-text"]/div[1]/table[4]/tbody/tr[82]/td[1]').get_attribute('innerHTML').strip()

while i < 153:
    quest_links[i].click()
    scrape_quest_info()
    driver.back()
    time.sleep(1)
    quest_links = driver.find_elements(By.XPATH, '//*[@id="mw-content-text"]/div[1]/table[4]/tbody/tr/td[2]/a')
    i += 1