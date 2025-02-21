
from com.okyunsu.models.cctv.data_reader import DataReader


import pandas as pd

from com.okyunsu.models.cctv.dataset import Dataset


class CctvService:

    dataset = Dataset()
    reader = DataReader()

    def new_model(self, fname) -> object:
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


        reader.cctv = self.new_model(temp[0])
        reader.crime = self.new_model(temp[1])
        reader.pop = self.new_model(temp[2])
    
        reader = self.cctv_ratio(reader)
        reader = self.crime_ration(reader)
        reader = self.pop_ratio(reader)
        

        return reader
      

    @staticmethod
    def cctv_ratio(reader)-> object:
        cctv = reader.cctv
        cctv = cctv.drop({"2013년도 이전","2014년","2015년","2016년"}, axis =1)
        print(f"cctv 데이터 헤드: {cctv.head()}")

        return reader
        
    
    @staticmethod
    def crime_ration(reader)-> object:
        crime = reader.crime
        print(f"crime 데이터 헤드: {crime.head()}")
        # station_name = [] # 경찰서 관서명 리스트
        # for name in crime['관서명']:
        #     station_name.append('서울' + str(name[:-1])+ '경찰서')
        # station_addrs = []
        # station_lats = []
        # station_lngs = []
        # gmaps = DataReader.create_gmaps()

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
 
        print(f"pop 데이터 헤드: {pop.head()}")

        return reader
    
