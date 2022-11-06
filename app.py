import requests
import streamlit as st

def getAllBookstore():
    url = 'https://cloud.culture.tw/frontsite/trans/emapOpenDataAction.do?method=exportEmapJson&typeId=M'
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    res=response.json()
    return res
    
def getCountyOption(items):
    optionList=[]
    for item in items:
        name=item['cityName'][0:3]
        if name not in optionList:
            optionList.append(name)

    return optionList

def getDistrictOption(items, target):
    optionList = []
    for item in items:
        name = item['cityName']
        if target not in name: continue
        name.strip()
        district = name[5:]
        if len(district) == 0: continue
        if district not in optionList:
            optionList.append(district)
    return optionList


def getSpecificBookstore(items, county, districts):
    specificBookstoreList = []
    for item in items:
        name = item['cityName']
        if county in name:
            specificBookstoreList.append(item)
    return specificBookstoreList

def getBookstoreInfo(items):
    expanderList = []
    for item in items:
        expander = st.expander(item['name'])
        expander.image(item['representImage'])
        expander.metric('hitRate', item['hitRate'])
        expander.subheader('Introduction')
        expander.write(item['intro'])
        expander.subheader('Address')
        expander.write(item['address'])
        expander.subheader('Open Time')
        expander.write(item['openTime'])
        expander.subheader('Email')
        expander.write(item['email'])
        expanderList.append(expander)
    return expanderList



def app():
    booklist=getAllBookstore()
    countyOption=getCountyOption(booklist)
    st.header('特色書店地圖')
    st.metric('Total bookstore', len(booklist))
    county = st.selectbox('請選擇縣市', countyOption)
    districtOption = getDistrictOption(booklist, county)
    district = st.multiselect('請選擇區域', districtOption)
    specificBookstore = getSpecificBookstore(booklist, county, district)
    num=len(specificBookstore)
    st.write(f'總共有{num}間書店')
    specificBookstore.sort(key = lambda item: item['hitRate'], reverse=True)
    bookstoreInfo = getBookstoreInfo(specificBookstore)

if __name__ == '__main__':
    app()



