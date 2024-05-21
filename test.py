import pandas as pd
import streamlit as st
from datetime import datetime  

def start(df):
    
    st.title("부산시 강좌 개설 현황")
    
    date=datetime.today()
    
    #신청기간이 지난 강좌의 행 제거하기
    df['신청기간(종료)']=pd.to_datetime(df['신청기간(종료)'].replace('-',pd.NA))
    df=df[(df['신청기간(종료)']>date)& df['신청기간(종료)'].notna()]
    
    #필요없는 열 제거하기
    del df['첨부파일']
    del df['위치정보(위도)']
    del df['위치정보(경도)']
    
    #수강료 열의 값들을 정수형으로 바꾸기
    #pd.to_numeric()->형변환 가능한지 확인
    #매개변수 errors="coerce"->에러발생시 결측값으로 대체
    #fillna()->결측값을 -1로 대체
    #astype(int)로-1또한 원래의미의 정수로 형변환이됨.이부분이 이해가 안된다
    
    df['수강료'] = pd.to_numeric(df['수강료'], errors='coerce').fillna(-1)
    df['수강료']=df["수강료"].astype(int)
  
    #잔여 열의 값을 정수형으로 변환
    df['잔여'] = pd.to_numeric(df['잔여'], errors='coerce').fillna(-1)
    df['잔여']=df["잔여"].astype(int)
    
    #잔여인원이 0명 이하인 행 삭제
    dropIndex=df[df['잔여']<=0].index
    df.drop(dropIndex,inplace=True)
    
    return df
    
    
def main():
    df=pd.read_csv("/Users/my/Desktop/스터디 발표/myfile.csv",encoding="cp949")
    df=start(df)
    
    with st.expander("가격"):
        #범위안의 값만 보여주기
        minSum,maxSum=st.slider('가격',min_value=0,max_value=50000,value=(0,50000),step=1000)
        st.write(str(minSum)+'~'+str(maxSum)+'원')
        tempValue=df[(df['수강료']>= minSum) & (df['수강료']<= maxSum)]  
    
    #주소 열에서 지역 불러오기
    localSelect=df["주소"].str.split(" ").str[1].drop_duplicates().sort_values()
    localSelect=st.multiselect("지역선택",localSelect)
    

    #만약 검색하고싶은 지역을 선택한다면 가격으로 필터링을 한 것에 다시 지역으로 필터링을 시킴
    tempLocal=tempValue[tempValue["주소"].str.split(" ").str[1].isin(localSelect)]
    
    #지역을 선택하지 않았으면 필터링 하나만 된 테이블을 지역이 선택되었으면 필터링을 두번 거친 테이블을 보여줌
    if len(localSelect)==0:
        tempValue = tempValue.reset_index(drop=True)
        st.write(tempValue)
    else:
        tempLocal=tempLocal.reset_index(drop=True)
        st.write(tempLocal)
    
    
if __name__=="__main__":
    main()
