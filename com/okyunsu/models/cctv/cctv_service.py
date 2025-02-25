
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
        temp = []
        for i in list(args):
            temp.append(i)


        reader.cctv = self.create_matrix(temp[0])
        reader = self.cctv_ratio(reader)
        reader.crime = self.create_matrix(temp[1])
        reader = self.crime_ration(reader)
        reader.pop = self.create_matrix(temp[2])
        reader = self.pop_ratio(reader)

        return reader
      

    @staticmethod
    def cctv_ratio(reader)-> object:
        cctv = reader.cctv
        cctv = cctv.drop({"2013년도 이전","2014년","2015년","2016년"}, axis =1)
        print(f"cctv 데이터 헤드: {cctv.head()}")
        cctv = cctv.rename(columns = {"기관명":"자치구"})


        save_path = os.path.join(save_dir, "cctv_in_seoul.csv")

        # CSV 파일 저장 (덮어쓰기가 가능하도록 mode='w' 사용)
        cctv.to_csv(save_path, index=False)
 
        print(f"cctv 데이터 헤드: {cctv.head()}")

        return reader
        
    
    @staticmethod
    def crime_ration(reader)-> object:
        crime = reader.crime
        print(f"crime 데이터 헤드: {crime.head()}")
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
        crime["자치구"] = gu_names

        if "관서명" in crime.columns:
            crime = crime.drop(columns=["관서명"])
            print("✅ '관서명' 컬럼을 삭제했습니다.")
        else:
            print("⚠️ '관서명' 컬럼이 없습니다.")


        save_path = os.path.join(save_dir, "crime_in_seoul.csv")

        # CSV 파일 저장 (덮어쓰기가 가능하도록 mode='w' 사용)
        crime.to_csv(save_path, index=False)

        return reader
        
    @staticmethod
    def pop_ratio(reader)-> object:
        save_path = os.path.join(save_dir, "pop_in_seoul.csv")
        if os.path.exists(save_path):
            print(f"⚠️ 파일이 이미 존재합니다. 변경 없이 유지합니다: {save_path}")
            return reader
        pop = reader.pop
        pop.rename(columns =  {
            # pop.columns[0] : '자치구' # 변경하지 않음
        pop.columns[1]: '인구수',
        pop.columns[2]: '한국인',
        pop.columns[3]: '외국인',
        pop.columns[4]: '고령자',}, inplace = True)


        # CSV 파일 저장 (덮어쓰기가 가능하도록 mode='w' 사용)
        pop.to_csv(save_path, index=False)
 
        print(f"pop 데이터 헤드: {pop.head()}")

        return reader
    

