import requests
from bs4 import BeautifulSoup


static_out_dir = '/Users/daniillavrentyev/PycharmProjects/znakapp3.8/znakapp_38/znakapp/znakapp/service/static/out'

def parsing_krisha_kz(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'lxml')
    imgs_src_list = soup.find_all('div', class_='gallery__small-item')
    counter = 1
    try:
        for elem in imgs_src_list:
            img_href = str(elem)
            img_href = img_href[img_href.find("https:"):img_href.find('.jpg')+4]
            # print(img_href)
            image_bytes = requests.get(img_href).content
            with open(f'/Users/daniillavrentyev/PycharmProjects/znakapp3.8/znakapp_38/znakapp/znakapp/service/parser_znakapp/images/img{counter}.png', 'wb') as file:
                file.write(image_bytes)
            counter += 1
        # offer_info = soup.find_all('div', class_='offer__info-title')
        # offer__advert_short_info = soup.find_all('div', class_='offer__advert-short-info')
        # info_list = []
        # param_list = []
        # for elem in offer_info:
        #     if elem != '\n' or '':
        #         info_list.append(elem.text)
        #
        # for elem in offer__advert_short_info:
        #     if elem != '\n' or '':
        #         param_list.append(elem.text)
        #
        # param_list[0] = param_list[0][:param_list[0].find('показать на карте')]
        #
        # total_price = soup.find('div', class_='offer__price').text.strip()
        # print(total_price)

        # with open(f'{static_out_dir}/info_list.txt', 'w') as file:
        #     for i in range(len(offer_info)):
        #         file.write(f'{info_list[i]}: {param_list[i]}\n')
        #     file.write(f'Цена: {total_price}')

        offer_info = soup.find('div', class_='offer__advert-title').text.strip()
        print(offer_info)

        with open(f'{static_out_dir}/info_list.txt', 'w') as file:
            file.write(f'{offer_info}')


    except Exception as ex:
        print(f'Save error')
