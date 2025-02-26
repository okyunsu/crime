
import numpy as np
from sklearn import preprocessing
from com.okyunsu.models.cctv.data_reader import DataReader
from com.okyunsu.models.cctv.googlemaps_singleton import GoogleMapsSingleton
import os
import pandas as pd
from com.okyunsu.models.cctv.dataset import Dataset
from com.okyunsu.models import save_dir


class CctvService:

    dataset = Dataset()
    reader = DataReader()



    def create_matrix(self, fname) -> object:
        reader = self.reader
        reader.fname = fname

        if fname.endswith("csv"):
            return reader.csv_to_dframe()
        elif fname.endswith("xls"):
            return reader.xls_to_dframe(header = 2  , usecols = 'B,D,G,J,N')
        else:
            return ValueError(f"지원하지 않는 형식입니다: {fname}")

    def preprocess(self,*args) -> object:
        reader = self.reader
      
        for i in list(args):
            print(f"🕞🕞",{i})
            print("🐮🐮🐮🐮🐮",type(reader))
            self.save_object_to_csv(reader, i)
        return reader
                  

 
    def save_object_to_csv(self, reader, fname) -> object:
        print(f"⛔save_csv 처음 : {fname}")

        full_name = os.path.join(save_dir, fname)


        if not os.path.exists(full_name) and  fname == "cctv_in_seoul.csv":
            reader.cctv = self.create_matrix(fname)
            reader = self.cctv_ratio(reader)
            reader.cctv.to_csv(full_name, index=False)
            
        elif not os.path.exists(full_name) and  fname == "crime_in_seoul.csv":
            reader.crime = self.create_matrix(fname)
            reader = self.crime_ration(reader)
            reader.crime.to_csv(full_name, index=False)
            reader = self.update_police(reader)
        elif not os.path.exists(full_name) and  fname == "pop_in_seoul.xls":
            reader.pop = self.create_matrix(fname)
            reader = self.pop_ratio(reader)

        else:
            print(f"파일이 이미 존재합니다. {fname}")
        
        return reader

   
      

    @staticmethod
    def cctv_ratio(reader)-> object:
        cctv = reader.cctv
        cctv = cctv.drop({"2013년도 이전","2014년","2015년","2016년"}, axis =1)
        print(f"cctv 데이터 헤드: {cctv.head()}")
        cctv = cctv.rename(columns = {"기관명":"자치구"})
        reader.cctv = cctv

        return reader
        
    
    @staticmethod
    def crime_ration(reader)-> object:
        crime = reader.crime
        print(f"crime 데이터 헤드: {crime.head()}")
       

        return reader

    @staticmethod
    def update_police(reader):
        crime = reader.crime

        station_name = [] # 경찰서 관서명 리스트
        for name in crime['관서명']:
            station_name.append('서울' + str(name[:-1])+ '경찰서')
        station_addrs = []
        station_lats = []
        station_lngs = []
        gmaps = GoogleMapsSingleton()
        for name in station_name:
            tmp = gmaps.geocode(name, language = 'ko')
            print(f"{name}의 검색 결과: {tmp[0].get("formatted_address")}")
            station_addrs.append(tmp[0].get("formatted_address"))
            tmp_loc = tmp[0].get("geometry")
            station_lats.append(tmp_loc['location']['lat'])
            station_lngs.append(tmp_loc['location']['lng'])
        
        print(f"자치구 리스트: {station_addrs}")
        gu_names = []
        for name in station_addrs:
            tmp = name.split()
            tmp_gu = [gu for gu in tmp if gu[-1] == "구"][0]
            gu_names.append(tmp_gu)
        [print(f"자치구 리스트 2 : {gu_names}")]
        reader.crime["자치구"] = gu_names

         #  구 와 경찰서의 위치가 다른 경우 수작업  
        # crime.loc[crime['관서명'] == '혜화서', ['자치구']] == '종로구'
        # crime.loc[crime['관서명'] == '서부서', ['자치구']] == '은평구'
        # crime.loc[crime['관서명'] == '강서서', ['자치구']] == '양천구'
        # crime.loc[crime['관서명'] == '종암서', ['자치구']] == '성북구'
        # crime.loc[crime['관서명'] == '방배서', ['자치구']] == '서초구'
        # crime.loc[crime['관서명'] == '수서서', ['자치구']] == '강남구'

        crime = crime.groupby("자치구" , as_index=False).sum()
        crime = crime.drop(columns=["관서명"])
      
 
        # 검거율
        police = pd.pivot_table(crime, index='자치구', aggfunc=np.sum).reset_index()
        
        police['살인검거율'] = (police['살인 검거'].astype(int) / police['살인 발생'].astype(int)) * 100
        police['강도검거율'] = (police['강도 검거'].astype(int) / police['강도 발생'].astype(int)) * 100
        police['강간검거율'] = (police['강간 검거'].astype(int) / police['강간 발생'].astype(int)) * 100
        police['절도검거율'] = (police['절도 검거'].astype(int) / police['절도 발생'].astype(int)) * 100
        police['폭력검거율'] = (police['폭력 검거'].astype(int) / police['폭력 발생'].astype(int)) * 100
        police = police.drop(columns={'살인 검거', '강도 검거', '강간 검거', '절도 검거', '폭력 검거'}, axis=1)
        # ic(f"🔥💧police: {police.head()}")

        police.to_csv(os.path.join(save_dir, 'police_in_seoul.csv'), index=False)

        
        crime_rate_columns = ['살인검거율', '강도검거율', '강간검거율', '절도검거율', '폭력검거율']
        crime_columns = ['살인', '강도', '강간', '절도', '폭력']
        
        for i in  crime_rate_columns:
            police.loc[police[i] > 100, 1] = 100  # 데이터값의 기간 오류로 100을 넘으면 100으로 계산
        police = police.rename(columns={
            '살인 발생': '살인',
            '강도 발생': '강도',
            '강간 발생': '강간',
            '절도 발생': '절도',
            '폭력 발생': '폭력'
        })
        x = police[crime_rate_columns].values
        min_max_scalar = preprocessing.MinMaxScaler()
        """
          스케일링은 선형변환을 적용하여
          전체 자료의 분포를 평균 0, 분산 1이 되도록 만드는 과정
          """
        x_scaled = min_max_scalar.fit_transform(x.astype(float))
        """
         정규화 normalization
         많은 양의 데이터를 처리함에 있어 데이터의 범위(도메인)를 일치시키거나
         분포(스케일)를 유사하게 만드는 작업
         """
        police_norm = pd.DataFrame(x_scaled, columns=crime_columns, index=police.index)
        police_norm[crime_rate_columns] = police[crime_rate_columns]
        police_norm['범죄'] = np.sum(police_norm[crime_rate_columns], axis=1)
        police_norm['검거'] = np.sum(police_norm[crime_columns], axis=1)
        police_norm.to_csv(os.path.join(save_dir, 'police_norm_in_seoul.csv'))

        reader.police = police


        return reader

        
    @staticmethod
    def pop_ratio(reader)-> object:

        pop = reader.pop
        pop.rename(columns =  {
            # pop.columns[0] : '자치구' # 변경하지 않음
        pop.columns[1]: '인구수',
        pop.columns[2]: '한국인',
        pop.columns[3]: '외국인',
        pop.columns[4]: '고령자',}, inplace = True)
        
        reader.pop.to_csv(os.path.join(save_dir, "pop_in_seoul.csv"), index=False)
        reader.pop = pop

        return reader
    

