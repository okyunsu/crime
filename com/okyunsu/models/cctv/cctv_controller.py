
from com.okyunsu.models.cctv.cctv_service import CctvService
from com.okyunsu.models.cctv.data_reader import DataReader
from com.okyunsu.models.cctv.dataset import Dataset



class CctvController:

    dataset = Dataset()
    data_reader = DataReader() 
    service = CctvService()

    def modeling(self, *args):
           reader = self.service.preprocess(*args)
        #    self.print_reader(reader)
           return reader


    @staticmethod
    def print_reader(reader):
        print('*' * 100)
        print(f'1. cctv 의 type \n {type(reader.cctv)} ')
        print(f'2. cctv 의 column \n {reader.cctv.columns} ')
        print(f'3. cctv 의 상위 5개 행\n {reader.cctv.head()} ')
        print(f'4. cctv 의 null 의 개수\n {reader.cctv.isnull().sum()}개')
        print(f'5. crime 의 type \n {type(reader.crime)}')
        print(f'6. crime 의 column \n {reader.crime.columns}')
        print(f'7. crime 의 상위 5개 행\n {reader.crime.head()}개')
        print(f'8. crime 의 null 의 개수\n {reader.crime.isnull().sum()}개')
        print(f'5. pop 의 type \n {type(reader.pop)}')
        print(f'6. pop 의 column \n {reader.pop.columns}')
        print(f'7. pop 의 상위 5개 행\n {reader.pop.head()}개')
        print(f'8. pop 의 null 의 개수\n {reader.pop.isnull().sum()}개')
        print('*' * 100)
