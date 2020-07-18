import requests
import json


def transrate_text(q, source, target, auth_token):
    """
    翻訳
    :param q: 翻訳テキスト
    :param source: 言語 from
    :param target: 言語 to
    :param auth_token: API認証トークン
        $ gcloud auth application-default print-access-token
    :return:
    """
    request_header = {
        "Authorization": "Bearer {}".format(auth_token)
    }
    data = {
        "q": q,
        "source": source,
        "target": target,
        "format": "text",
    }
    request_url = "https://translation.googleapis.com/language/translate/v2"
    response = requests.post(request_url, headers=request_header,
                             data=json.dumps(data))
    res = response.json()
    return res["data"]["translations"][0]['translatedText']


if __name__ == '__main__':
    # API認証トークン
    # $ gcloud auth application-default print-access-token
    AUTH_TOKEN = "********"

    # 翻訳テキスト
    q = "The Great Pyramid of Giza (also known as the Pyramid of Khufu or the Pyramid of Cheops) " \
        "is the oldest and largest of the three pyramids in the Giza pyramid complex."

    source = "en"
    target = "ja"

    result = transrate_text(q, source, target, AUTH_TOKEN)

    print(result)


