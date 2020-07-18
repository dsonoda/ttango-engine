import urllib.request
import httplib2
import os
import pickle
import hashlib

from googleapiclient.discovery import build


def make_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def make_correspondence_table(correspondence_table, original_url, hashed_url):
    correspondence_table[original_url] = hashed_url


def get_image_url(api_key, cse_key, search_word, page_limit, save_dir_path):

    service = build("customsearch", "v1", developerKey=api_key)
    page_limit = page_limit
    start_index = 1
    response = []

    img_list = []

    make_dir(save_dir_path)
    save_res_path = os.path.join(save_dir_path, 'api_response_file')
    make_dir(save_res_path)

    for nPage in range(0, page_limit):
        try:
            response.append(service.cse().list(
                q=search_word,
                cx=cse_key,
                lr='lang_ja',
                num=10,
                start=start_index,
                searchType='image',
            ).execute())

            start_index = response[nPage].get("queries").get("nextPage")[
                0].get("start_index")

        except Exception as e:
            print(e)

    with open(os.path.join(save_res_path, 'api_response.pickle'), mode='wb') as f:
        pickle.dump(response, f)

    for one_res in range(len(response)):
        if len(response[one_res]['items']) > 0:
            for i in range(len(response[one_res]['items'])):
                img_list.append(response[one_res]['items'][i]['link'])

    return img_list


def get_image(save_dir_path, img_list):
    make_dir(save_dir_path)
    save_img_path = os.path.join(save_dir_path, 'imgs')
    make_dir(save_img_path)

    opener = urllib.request.build_opener()
    http = httplib2.Http(".cache")

    for i in range(len(img_list)):
        try:
            url = img_list[i]
            extension = os.path.splitext(img_list[i])[-1]
            if extension.lower() in ('.jpg', '.jpeg', '.gif', '.png', '.bmp'):
                encoded_url = url.encode('utf-8')  # required encoding for hashed
                hashed_url = hashlib.sha3_256(encoded_url).hexdigest()
                full_path = os.path.join(save_img_path, hashed_url + extension.lower())

                response, content = http.request(url)
                with open(full_path, 'wb') as f:
                    f.write(content)
                print('saved image... {}'.format(url))

                make_correspondence_table(correspondence_table, url, hashed_url)

        except:
            print("failed to download images.")
            continue


if __name__ == '__main__':
    API_KEY = '********'
    CUSTOM_SEARCH_ENGINE = '********'

    page_limit = 1
    search_word = 'dog'
    save_dir_path = './outputs/{}'.format(search_word)

    correspondence_table = {}

    img_list = get_image_url(API_KEY, CUSTOM_SEARCH_ENGINE, search_word,
                             page_limit, save_dir_path)
    get_image(save_dir_path, img_list)
