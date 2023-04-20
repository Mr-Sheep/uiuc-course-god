# UIUC COURSE GOD
# course registration cheat for UIUC
# support multiple crn for different courses
# author: Tianhao Chi
# usage: python run.py semester netid password crn1 crn2 ...
# use semester in this format: YYYY-spring, YYYY-summer, YYYY-fall. Example: 2021-spring
# note: do not log in into the system by yourself while using this program

# required package: bs4, selenium

from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time
import sys
import re
import random

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def construct_term_in(semester):
    # This is dark magic.
    year = semester[:semester.find('-')]
    season = semester[semester.find('-')+1:]
    if season == 'winter':
        season_num = 0
    if season == 'spring':
        season_num = 1
    if season == 'summer':
        season_num = 5
    if season == 'fall':
        season_num = 8
    return 120000 + int(str(year)[-2:])*10 + season_num


def get_remaining_seat(soup, cross_list):
    if cross_list:
        try:
            # for cross list courses
            remaining_seat = soup('th', attrs={'scope': 'row'})[
                3].find_next_siblings('td')[2].string
        except IndexError:
            remaining_seat = soup('th', attrs={'scope': 'row'})[
                1].find_next_siblings('td')[2].string
    else:
        remaining_seat = soup('th', attrs={'scope': 'row'})[
            1].find_next_siblings('td')[2].string
    return int(remaining_seat)

def check_remaining_seats(driver, crn_arr, cross_list, term_in):
    remaining_seats = []
    for crn in crn_arr:
        url = 'https://ui2web1.apps.uillinois.edu/BANPROD1/bwckschd.p_disp_detail_sched?term_in=%d&crn_in=%s' % (
            term_in, crn)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        remaining_seats.append(get_remaining_seat(soup, cross_list))
    return remaining_seats

def refresh_course_website(driver, crn_groups, cross_list, term_in, turbo):
    remaining_seat = 0
    refresh_counter = 0
    print("start refreshing ...")
    # keep refreshing until find empty space
    while True:
        for crn_group in crn_groups:
            remaining_seats = check_remaining_seats(driver, crn_group, cross_list, term_in)
            available_crns = [crn for crn, seats in zip(crn_group, remaining_seats) if seats > 0]
            
            if len(available_crns) == len(crn_group):
                print(f"{bcolors.OKGREEN}refreshing done!{bcolors.ENDC}")
                return available_crns
            else:
                available_crns = []
        
            refresh_counter += 1
            print(f"\rRefresh attempt: {refresh_counter}", end="")
            sys.stdout.flush()  
            if not turbo:          
                sleep_time = random.uniform(30, 60)
                time.sleep(sleep_time)
            

def register(driver, crns):
    # register single course
    count = 1;
    for crn in crns:
        crn_id = "crn_id" + str(count)
        crn_blank = driver.find_element(By.ID, crn_id)
        crn_blank.send_keys(crn)
        count+=1
    driver.find_element(By.XPATH, "//input[@value='Submit Changes']").click()
    driver.save_screenshot('screen.png')
        

def log_in(username, password, driver):
    driver.get(login_url)
    user_field = driver.find_element("name", "USER")
    password_field = driver.find_element("name", "PASSWORD")
    user_field.send_keys(username)
    password_field.send_keys(password)
    driver.find_element("name", "BTN_LOGIN").click()
    print(f"{bcolors.OKGREEN}logged in{bcolors.ENDC}")
    return driver


# Semester needs to be updated each semester!
def navigate(driver, username, password, crn):
    year = semester[:semester.find('-')]
    season = semester[semester.find('-')+1:]
    season = season[0].capitalize() + season[1:]
    semester_str = season + ' ' + year + ' - Urbana-Champaign'

    # this url might need update
    url = "https://ui2web1.apps.uillinois.edu/BANPROD1/twbkwbis.P_GenMenu?name=bmenu.P_StuMainMnu"
    driver.get(url)
    driver.find_element('link text', 'Classic Registration').click()
    driver.find_element('link text', 'Add/Drop Classes').click()
    driver.find_element('link text', 'I Agree to the Above Statement').click()

    # go to register page
    options = Select(driver.find_element(By.ID, 'term_id'))
    options.select_by_visible_text(semester_str)
    path = '//input[@type="submit" and @value="Submit"]'
    driver.find_element(By.XPATH, path).click()

# ============================================ main ===================================

options = Options()
if '--headless' in sys.argv:        
    options.add_argument('-headless')
    sys.argv.remove('--headless')
    
turbo = False;
if '--turbo' in sys.argv:
    turbo = True;
    sys.argv.remove('--turbo')

# put the crn numbers into the array
crn_pattern = re.compile(r'{(.+?)}')
crn_groups = crn_pattern.findall(' '.join(sys.argv[4:]))
grouped_crns = [crn.split() for crn in crn_groups]

single_crns = [[crn] for crn in sys.argv[4:] if not crn.startswith('{') and not crn.endswith('}')]

crn_groups = grouped_crns + single_crns
print(crn_groups)
# crn_arr = grouped_crns + single_crns

# login url may change and might need update in the future
# login_url = 'https://login.uillinois.edu/auth/SystemLogin/sm_login.fcc?TYPE=33554433&REALMOID=06-a655cb7c-58d0-4028-b49f-79a4f5c6dd58&GUID=&SMAUTHREASON=0&METHOD=GET&SMAGENTNAME=-SM-dr9Cn7JnD4pZ%2fX9Y7a9FAQedR3gjL8aBVPXnJiLeXLOpk38WGJuo%2fOQRlFkbatU7C%2b9kHQgeqhK7gmsMW81KnMmzfZ3v0paM&TARGET=-SM-HTTPS%3a%2f%2fwebprod%2eadmin%2euillinois%2eedu%2fssa%2fservlet%2fSelfServiceLogin%3fappName%3dedu%2euillinois%2eaits%2eSelfServiceLogin%26dad%3dBANPROD1'
login_url = 'https://webprod.admin.uillinois.edu/ssa/servlet/SelfServiceLogin?appName=edu.uillinois.aits.SelfServiceLogin&dad=BANPROD1'

# semester in this format: YYYY-spring/YYYY-summer/YYYY-fall
semester = sys.argv[1]
username = sys.argv[2]  # netid
password = sys.argv[3]  # password

# please change to true if the course is crosslisted
cross_list = False

start = time.time()

term_in = construct_term_in(semester)

while len(crn_groups) != 0:
    # the driver for refresh        
    driver = webdriver.Firefox(options=options, service=Service(GeckoDriverManager().install()))
    driver = log_in(username, password, driver)
    crn_success = ""
    crn_success = refresh_course_website(driver, crn_groups, cross_list, term_in, turbo)

    # if empty seat found. the driver for register
    navigate(driver, username, password, crn_success)
    register(driver, crn_success)

    msg = "time spent: %s" % (time.time() - start)
    print(msg)
    print("crn: " + str(crn_success) + " is done!!!!!!!!!!!!!!!!!")
    crn_groups.remove(crn_success)
    driver.quit()
