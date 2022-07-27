import json
import requests
import bs4

def download_podcast(url):
    '''
    url (type=string) est le lien du site d'un episode du podcast france culture
    ex: https://www.franceculture.fr/emissions/science-en-questions/a-quoi-la-peur-nous-sert-elle
    '''
    html = requests.get(url)
    soup = bs4.BeautifulSoup(html.text,'html.parser')

    data = json.loads(soup.find_all('script', type='application/ld+json')[1].text)
    podcast_link = requests.get(data["@graph"][0]['mainEntity']['contentUrl'])

    file_name = data['@graph'][0]['dateCreated'][:10]+ ' '+ data['@graph'][0]['name']

    f = open(file_name,'wb')
    f.write(podcast_link.content)
    f.close

def list_of_podcasts(n):
    '''
    url (type=string) est le lien de l'emission france culture.
    ex: https://www.franceculture.fr/emissions/la-conversation-scientifique


    n c'est la page
    '''

    url = 'https://www.franceculture.fr/emissions/la-conversation-scientifique?p={}'.format(n)
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text,'lxml')

    liste_emissions = soup.select('.teaser-text-title')

    print('Les emissions sur cette page sont: \n')

    for i in range(len(liste_emissions)):
        print(i,'\t',liste_emissions[i].select('a')[0]['title'])
    print('\n')

    return liste_emissions


def ask_select_episode():
    episodios = []
    i=1
    while i<4:
        episodio = input("Numéro d'emission à télécharger ou 'x' si c'est bon: ")
        if episodio == 'x':
            break
        else:
            episodios.append(int(episodio))
            i += 1
    return episodios


if __name__=='__main__':
    print('Buenos días et bienvenue au programme de téléchargement de')
    print('podcasts de La conversation scientifique.\n')

    numero_page = input("Choisir un numéro de page (1-26): ")

    liste_emissions = list_of_podcasts(numero_page)

    liste_episodes = ask_select_episode()

    for i in liste_episodes:
        podcast_url = 'https://www.franceculture.fr'+liste_emissions[i].select('a')[0]['href']
        download_podcast(podcast_url)

