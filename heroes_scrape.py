import mechanicalsoup
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

website_url = 'https://heroes-team.herokuapp.com/'

# Scrape with BeautifulSoup

	# Scrape website title
heroes_url = Request(website_url, headers={'User-Agent': 'Mozilla/5.0'})

html_page = urlopen(heroes_url)
html_text = html_page.read().decode('utf-8')
html_beautifulsoup = BeautifulSoup(html_text, 'lxml')
print(html_beautifulsoup.title.string)


# Scrape with mechanicalsoup
	# Let's create a new browser object
my_browser = mechanicalsoup.Browser()
page = my_browser.get(website_url)
html_mechanicalsoup = page.soup

	# Scrape credo section
team_credo = html_mechanicalsoup.select('.service-heading')
credo_words = []

for credo in team_credo:
	credo_words.append(credo.string)

credo_s = ','.join(credo_words)
print(f'Team heroes credo is: {credo_s.replace(",", "-")}')
# NB: I use replace to design credo format

	# Scrape team section
''' Here, we will scrape only three first heroes informations:
- Samsnison
- Thor
- Green Lantern
Hope that you'll continue with scrape last heroes informations.

At this point, let's take one minute to think about our data structure.
Firstly, we want to get "warrior name". Next profile name & story.
After all, get rest of datas:
- origin
- power
- caracteristics
- team

Now, we know what we want. Time to organize it.
We'll use dict to have good structure of one heroe and list for all of them.
Our dict will call "". Here is an example of our structure:

heroe = {
	name: ...,
	Profile name: ...,
	Story: ...,
	rest_of_datas: {
		origin: ...,
		power: ...,
		caractristics: ...,
		team: ...
	}
}
'''

# Define variables which contains datas we want
heroes_list = []
heroe_data = {}

heroes_portfolio = html_mechanicalsoup.select('.portfolio-caption')
heroe_name = html_mechanicalsoup.select('.portfolio-caption h4')
profile_name = html_mechanicalsoup.select('.modal-body h2')
heroe_story = html_mechanicalsoup.select('.modal-body .story')
heroe_origin = html_mechanicalsoup.select('.rest_of_datas > li:nth-of-type(1)')
heroe_power = html_mechanicalsoup.select('.rest_of_datas > li:nth-of-type(2)')
heroe_caracteritics = html_mechanicalsoup.select('.rest_of_datas > li:nth-of-type(3)')
heroe_team = html_mechanicalsoup.select('.rest_of_datas > li:nth-of-type(4)')

# Content which is into select method is css code.

for x in range(0, len(heroes_portfolio)):
	heroe_data = {
		'name': heroe_name[x].string,
		'profile': profile_name[x].string,
		'story': heroe_story[x].string,
		'rest_of_datas': [
			heroe_origin[x].string,
			heroe_power[x].string,
			heroe_caracteritics[x].string,
			heroe_team[x].string
		]
	}

	heroes_list.append(heroe_data)

# On website, Thor is at position 2. So let's display his data

# print(heroes_list[2])

# Hugh !!! The result is ugly! At least, we've the good result.
# Now, comment previous print line and let's bring an esthetic touch to display

def display_heroe_data(heroe_number):
	the_heroe = heroes_list[heroe_number]

	print(f'\nPresentation of "{the_heroe["name"]}"')
	print(f'-> {the_heroe["profile"]}\n\
-> Story: {the_heroe["story"].rstrip()}\n\
-> Others informations: \n\
	** {the_heroe["rest_of_datas"][0]}\n\
	** {the_heroe["rest_of_datas"][1]}\n\
	** {the_heroe["rest_of_datas"][2]}\n\
	** {the_heroe["rest_of_datas"][3]}\n\
	')

# display_heroe_data(2) # Display Thor data

''' Yeah! Now, the display is better than previously.
What we'll do now is to permit user to choose what heroe that he wants
to know informations. User choice will be between three first heroes.
Free are you to change it in order to extend it to all heroes presented.
Before continue, comment code we use to display "Thor".
'''

limit_of_heroes = 3

print('WELCOME TO SCRIPTING DAY!')
print('Today, we see web scraping.website url is:\n\
https://heroes-team.herokuapp.com//')

i = 1
print('**Heroes list**')
for heroe in heroes_list:
	if i <= limit_of_heroes:
		print(f'{i}-{heroe["name"]}')
	i += 1

user_choice = input('Choose heroe number you want to get informations: ')
user_choice = int(user_choice)

while user_choice < 0 or user_choice > limit_of_heroes :
	user_choice = int(input('Choose heroe number you want to get informations: '))

display_heroe_data(user_choice-1) # remove 1 (-1) because list start by 0