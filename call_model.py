import time
import requests
import random

url = 'http://192.168.9.145:9381/api/saas/test/quick/chat'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'accept-encoding': 'gzip, deflate',
    'connection': 'keep-alive',
    'authorization': '25a47c5a-180e-4506-b98f-276436d18d6c',
    'host': '192.168.9.145:9381',
    'origin': 'http://192.168.9.145:9381',
    'referer': 'http://192.168.9.145:9381/test/chat',
    'x-client-info': 'clientId=63873e6e3969a95807257e8a785e3d9d',
    'ignorecanceltoken': 'true',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8'
}

def call_model(prompt, modelname, url=url, headers=headers):
    if modelname == 'gemini-1.5':
        local_model_id = "279807156096598016"
    elif modelname == 'yi-lightning':
        local_model_id = "279803938583085056"
    elif modelname == 'glm-4-plus':
        local_model_id = "279801974122086400"
    elif modelname == 'qwen-plus':
        local_model_id = "279956248000987136"
    elif modelname == 'gpt-4o':
        local_model_id = "234695451691974656"
    elif modelname == "ernie-4.0-turbo":
        local_model_id = "279999331816177664"
    elif modelname == "spark4.0-ultra":
        local_model_id = "279802545759584256"
    elif modelname == "doubao-pro":
        local_model_id = "279799370147168256"
    elif modelname == "moonshot-v1":
        local_model_id = "279800631902863360"
    elif modelname == "hunyuan-turbo":
        local_model_id = "279955042688040960"
    elif modelname == "360gpt2-pro":
        local_model_id = "279961020691120128"
    elif modelname == "gy-pangu":
        local_model_id = "271240804947722240"
    data = {
        'question': prompt,
        'localModelId': local_model_id,
        'answerEvaluationMethod': '0'
    }
    retry_count = 0
    max_retries = 20
    while retry_count < max_retries:
        try:
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()
            response_json = response.json()
            if 'data' in response_json and 'answer' in response_json['data']:
                return response_json['data']['answer'].strip()
            else:
                print("Invalid response format from the model")
                return None
        except requests.RequestException as e:
            retry_count += 1
            delay = 2 ** retry_count + random.random()  # 指数退避 + 随机抖动
            print(f"Request error: {e}. Retrying in {delay:.2f} seconds... (attempt {retry_count}/{max_retries})")
            time.sleep(delay)
    print(f"Failed to get response after {max_retries} retries.")
    return None