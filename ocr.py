import requests
import uuid
import time
import json
#import matplotlib.pyplot as plt

def get_ocr():  # naver ocr api call
    api_url = 'https://q69y1dp5m5.apigw.ntruss.com/custom/v1/19317/8315c15d37e6a053d46eee76993430ab9fe44e3e59573d9194b572a1093d9f68/general'
    secret_key = 'R2tHWURKS0NIQnJCVHFQU0hwUVZ3amZJVm1BQXBmcE0='
    image_file = './result/binary/binary.jpg'
    # image_file='./Open_Source_Project/result/binary/KakaoTalk_20221129_232442476.jpg'# 테스트 케이스
    headers = {
        'X-OCR-SECRET': secret_key
    }
    request_json = {
        'images': [
            {
                'format': 'jpg',
                'name': 'ocr_test'
            }
        ],
        'requestId': str(uuid.uuid4()),
        'version': 'V2',
        'timestamp': int(round(time.time() * 1000))
    }
    payload = {'message': json.dumps(request_json).encode('UTF-8')}
    files = [
        ('file', open(image_file, 'rb'))
    ]
    response = requests.request("POST", api_url, headers=headers, data=payload, files=files)
    # print(response.text)
    res = json.loads(response.text.encode('utf8'))  # 디코딩 json->dict으로
    return res
    #sorting(res)

def find_ingredient(string):  # 성분 존재하는 지 찾음
    ingred = input('type what you looking for : ')
    if (string.find(ingred) != -1):
        print("exist")
    else:
        print("don't exist")

def sorting(res):  # json에서 디코딩 된 데이터를 원하는 데이터(text)만 가져와서 워하는 dictionary 형태로 저장
    length = len(res['images'][0]['fields'])
    datas = ""
    for i in range(0, length):
        datas = datas + res['images'][0]['fields'][i]['inferText']  # text만 있는 긴 하나의 문자열 만듬
    # 식품에 대한 정보를 저장할 dictionary
    # 트랜스 지방은 1일 영양성분표 기준치가 존재하지 않음.. 그래서 %가 없음
    # print(datas)
    #find_ingredient(datas)
    info = {
        '총내용량': '',
        '영양정보': '',
        '탄수화물': {'함량': '', '비율': ''}, '당류': {'함량': '', '비율': ''},
        '식이섬유': {'함량': '', '비율': ''}, '단백질': {'함량': '', '비율': ''},
        '지방': {'함량': '', '비율': ''}, '포화지방': {'함량': '', '비율': ''},
        '콜레스테롤': {'함량': '', '비율': ''}, '나트륨': {'함량': '', '비율': ''},
        '칼륨': {'함량': '', '비율': ''}, '비타민A': {'함량': '', '비율': ''},
        '비타민C': {'함량': '', '비율': ''}, '크롬': {'함량': '', '비율': ''},
        '칼슘': {'함량': '', '비율': ''}, '철분': {'함량': '', '비율': ''},
        '비타민D': {'함량': '', '비율': ''}, '비타민E': {'함량': '', '비율': ''},
        '비타민K': {'함량': '', '비율': ''}, '비타민B1': {'함량': '', '비율': ''},
        '비타민B2': {'함량': '', '비율': ''}, '나이아신': {'함량': '', '비율': ''},
        '비타민B6': {'함량': '', '비율': ''}, '엽산': {'함량': '', '비율': ''},
        '몰리브덴': {'함량': '', '비율': ''}, '비타민B12': {'함량': '', '비율': ''},
        '비오틴': {'함량': '', '비율': ''}, '판토텐산': {'함량': '', '비율': ''},
        '인': {'함량': '', '비율': ''}, '요오드': {'함량': '', '비율': ''},
        '마그네슘': {'함량': '', '비율': ''}, '아연': {'함량': '', '비율': ''},
        '셀렌': {'함량': '', '비율': ''}, '구리': {'함량': '', '비율': ''},
        '망간': {'함량': '', '비율': ''},
    }
    value = list(info.keys())  # info 딕셔너리의 key값만 리스트의 형식으로 불러옴

    # 총내용량과 영양정보는 정보가 1개 밖에 없음으로 특수 처리
    index = datas.find('총내용량')
    if (index != -1):
        index2 = datas.find('mL')
        index3 = datas.find('g')
        if (index2 != -1):  # 단위가 mL일때
            info['총내용량'] = datas[index + 4:index2 + 2]
            datas = datas[index2 + 2:]  # 문자열 앞에거 자름
        elif (index3 != -1):  # 단위가 g일 때
            info['총내용량'] = datas[index + 4:index3 + 1]
            datas = datas[index3 + 1:]  # 문자열 앞에거 자름

    index = datas.find('영양정보')
    if (index != -1):
        index2 = datas.find('kcal')
        info['영양정보'] = datas[index + 4:index2 + 4]
        datas = datas[index2 + 4:]  # 문자열 앞에거 자름

    for i in range(2, len(value)):
        index = datas.find(value[i])
        if (index != -1):
            # print(value[i])
            temp = datas[index + len(value[i]):]
            index2 = temp.find('g')
            index3 = temp.find('%')
            # print(temp[0:index2+1])
            # print(temp[index2+1:index3+1])
            info[value[i]]['함량'] = temp[0:index2 + 1]
            info[value[i]]['비율'] = temp[index2 + 1:index3 + 1]
    return info
    #recalculate(info)


def recalculate(info):
    # print(info)
    standard = {  # 기준치(2000kcal 기준)
        '탄수화물': '324', '당류': '100',
        '식이섬유': '25', '단백질': '55',
        '지방': '54', '포화지방': '15',
        '콜레스테롤': '300', '나트륨': '2000',
        '칼륨': '3500', '비타민A': '700',
        '비타민C': '100', '크롬': '30',
        '칼슘': '700', '철분': '12',
        '비타민D': '10', '비타민E': '11',
        '비타민K': '70', '비타민B1': '1.2',
        '비타민B2': '1.4', '나이아신': '15',
        '비타민B6': '1.5', '엽산': '400',
        '몰리브덴': '25', '비타민B12': '2.4',
        '비오틴': '30', '판토텐산': '5',
        '인': '700', '요오드': '150',
        '마그네슘': '315', '아연': '8.5',
        '셀렌': '55', '구리': '0.8',
        '망간': '3.0',
    }
    adjusted_info = {
        '총내용량': '',
        '영양정보': '',
        '탄수화물': {'함량': '', '비율': ''}, '당류': {'함량': '', '비율': ''},
        '식이섬유': {'함량': '', '비율': ''}, '단백질': {'함량': '', '비율': ''},
        '지방': {'함량': '', '비율': ''}, '포화지방': {'함량': '', '비율': ''},
        '콜레스테롤': {'함량': '', '비율': ''}, '나트륨': {'함량': '', '비율': ''},
        '칼륨': {'함량': '', '비율': ''}, '비타민A': {'함량': '', '비율': ''},
        '비타민C': {'함량': '', '비율': ''}, '크롬': {'함량': '', '비율': ''},
        '칼슘': {'함량': '', '비율': ''}, '철분': {'함량': '', '비율': ''},
        '비타민D': {'함량': '', '비율': ''}, '비타민E': {'함량': '', '비율': ''},
        '비타민K': {'함량': '', '비율': ''}, '비타민B1': {'함량': '', '비율': ''},
        '비타민B2': {'함량': '', '비율': ''}, '나이아신': {'함량': '', '비율': ''},
        '비타민B6': {'함량': '', '비율': ''}, '엽산': {'함량': '', '비율': ''},
        '몰리브덴': {'함량': '', '비율': ''}, '비타민B12': {'함량': '', '비율': ''},
        '비오틴': {'함량': '', '비율': ''}, '판토텐산': {'함량': '', '비율': ''},
        '인': {'함량': '', '비율': ''}, '요오드': {'함량': '', '비율': ''},
        '마그네슘': {'함량': '', '비율': ''}, '아연': {'함량': '', '비율': ''},
        '셀렌': {'함량': '', '비율': ''}, '구리': {'함량': '', '비율': ''},
        '망간': {'함량': '', '비율': ''},
    }
    adjusted_info = info
    height = input("please type your height : ")  # 키
    gender = input("please type your gender(male or female) : ")  # 성별
    degree = input("please type your exerxise_degree(운동정도 1~3) : ")  # 활동량
    height = float(height)
    standard_w = 0.0  # 표준체중 초기화
    essen_cal = 0
    # essen_cal=float(essen_cal)
    if (gender == 'male'):
        standard_w = (height / 100) * (height / 100) * 22  # 표준체중
    elif (gender == 'female'):
        standard_w = height / 100 * height / 100 * 21  # 표준체중
    print('표준체중 : ' + str(standard_w))

    if (degree == '1'):
        essen_cal = standard_w * 28
    elif (degree == '2'):
        essen_cal = standard_w * 33
    elif (degree == '3'):
        essen_cal = standard_w * 38
    print('필요열량 : ' + str(essen_cal))

    rearrange_s = list(standard.values())  # 재조정된 기준치
    re_degree = essen_cal / 2000  # 재조정 정도
    print('가중치 : ' + str(re_degree))

    for i in range(0, len(rearrange_s)):  # rearrange_s 리스트에 저장
        temp = float(rearrange_s[i])
        temp = temp * re_degree
        rearrange_s[i] = temp

    # print(rearrange_s)

    info_values = list(adjusted_info.values())  # 값 저장
    info_keys = list(adjusted_info.keys())  # key 값 저장 리스트

    for i in range(2, len(info_values)):
        if (info_values[i]['함량'] != ''):  # 함량에 대한 정보가 있을 때
            index2 = str(info_values[i]).find('mg')
            index3 = str(info_values[i]).find('g')

            if (index2 != -1):  # 단위가 mg일때
                ingredient_name = info_keys[i]
                temp = str(info_values[i]['함량'])
                comma = temp.find(",")
                if (comma != -1):
                    temp = temp.replace(",", "")

                amount = float(temp[0:-2])
                ratio = round(amount / float(rearrange_s[i - 2]) * 100, 3)
                Ratio = str(ratio)
                Ratio = Ratio + '%'
                adjusted_info[ingredient_name]['비율'] = Ratio

            elif (index3 != -1):  # 단위가 g일 때
                ingredient_name = info_keys[i]
                temp = str(info_values[i]['함량'])
                comma = temp.find(",")
                if (comma != -1):
                    temp = temp.replace(",", "")
                amount = float(temp[0:-1])
                ratio = round(amount / float(rearrange_s[i - 2]) * 100, 3)
                Ratio = str(ratio)
                Ratio = Ratio + '%'
                adjusted_info[ingredient_name]['비율'] = Ratio

    print("===================== adjusted =====================")
    # print(adjusted_info)
    # 함량은 존재하지만 비율이 0%로 였던 것은 일정 기준치 이하면 0이라 표현할 수 있기 때문, 허나 여기에서는 고려를 안함
    # e.x) 나트륨 : 5mg ,0% -> 5mg, 0.227%
    print(info_values[1])
    for i in range(0, len(info_values)):
        if (i < 2):
            print(info_keys[i])
            print(adjusted_info[info_keys[i]])
        elif ((i >= 2) & (adjusted_info[info_keys[i]]['함량'] != '')):
            print(info_keys[i])
            print(adjusted_info[info_keys[i]]['함량'] + ' , ' + adjusted_info[info_keys[i]]['비율'])
#get_ocr()