import requests
import json
import base64
import os


def make_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def get_voice(input_text, auth_token):
    """
    音声データ取得
    :param input_text: 翻訳テキスト
    :param auth_token: API認証トークン
        $ gcloud auth application-default print-access-token
    :return:
    """
    request_header = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": "Bearer {}".format(auth_token)
    }
    data = {
        "input": {
            "text": input_text,
        },
        "voice": {
            "languageCode": "en-gb",
            "name": "en-GB-Standard-A",
            "ssmlGender": "FEMALE",
        },
        "audioConfig": {
            "audioEncoding": "MP3"
        }
    }
    request_url = "https://texttospeech.googleapis.com/v1/text:synthesize"
    response = requests.post(request_url, headers=request_header,
                             data=json.dumps(data))
    res = response.json()
    return res["audioContent"]


if __name__ == '__main__':
    # API認証トークン
    # $ gcloud auth application-default print-access-token
    AUTH_TOKEN = "********"

    # 翻訳テキスト
    input_text = "dog"

    output_path = "./outputs/{}".format(input_text)
    make_dir(output_path)

    result = get_voice(input_text, AUTH_TOKEN)
    with open("{}/audio.mp3".format(output_path), 'wb') as f:
        f.write(base64.urlsafe_b64decode(result))


