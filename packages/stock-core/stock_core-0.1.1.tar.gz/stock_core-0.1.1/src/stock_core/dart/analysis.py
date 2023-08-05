import os
import pickle
import datetime
import pprint

import time
from . import subjects, save_db
from telegram.error import TimedOut
from util_hj3415 import noti, utils
from eval_hj3415 import eval

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.ERROR)


class Pickle:
    FILENAME = 'analysis.pickle'
    FULL_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), FILENAME)

    def __init__(self):
        self.contents = {}
        self.load()

    def save(self):
        if not utils.chk_date_format_Ymd(self.contents['date']):
            raise Exception(f"Invalid date - {self.contents['date']}(YYYYMMDD)")
        logger.info(f'Save to pickle : {self.contents}')
        with open(self.FULL_PATH, "wb") as fw:
            pickle.dump(self.contents, fw)

    def init(self, date: str):
        if not utils.chk_date_format_Ymd(date):
            raise Exception(f"Invalid date - {date}(YYYYMMDD)")
        logger.info(f'init {self.FULL_PATH}')
        with open(self.FULL_PATH, "wb") as fw:
            pickle.dump({'date': date, 'notified': [], 'analysed': []}, fw)

    def load(self):
        try:
            with open(self.FULL_PATH, "rb") as fr:
                obj = pickle.load(fr)
                logger.info(f'Load from pickle : {obj}')
                self.contents = obj
        except (EOFError, FileNotFoundError) as e:
            logger.error(e)
            with open(self.FULL_PATH, "wb") as fw:
                pickle.dump({'date': datetime.datetime.today().strftime('%Y%m%d'), 'notified': [], 'analysed': []}, fw)

    def show(self):
        print(f"date : {self.contents['date']}")
        print(f"notified : {len(self.contents['notified'])} items")
        pprint.pprint(f"{self.contents['notified']}")
        print(f"analysed : {len(self.contents['analysed'])} items")
        pprint.pprint(f"{self.contents['analysed']}")


pretested_subject = ('주식분할결정', '주식병합결정', '주식등의대량보유상황보고서', '자기주식처분결정', '공개매수신고서',
                     '전환사채권발행결정', '신주인수권부사채권발행결정', '교환사채권발행결정', '만기전사채취득',
                     '신주인수권행사', '소송등의', '주식배당결정', '주주총회소집결의', '회사합병결정', '회사분할결정',
                     '자산재평가실시결정')
available_subject = ('유상증자결정', '현물배당결정', '매출액또는손익구조')
enabled_subject = ('공급계약체결', '무상증자결정', '자기주식취득결정', '주식등의대량보유상황보고서', '특정증권등소유상황보고서', '주식소각결정')


class AnalyseOneSubject:
    """
    dart_dict 구조
    {'code': '001790',
     'name': '대한제당',
     'rtitle': '주요사항보고서(무상증자결정)',
     'rno': '20210323000257',
     'rdt': '20210323',
     'url': 'http://dart.fss.or.kr/dsaf001/main.do?rcpNo=20210323000257',
     'price': 31500,
     'per': None,
     'pbr': None,
     'high_52w': 33200,
     'low_52w': 15300}

    run()을 실행하면...
    1. df를 통해 dart_dict리스트를 생성한다.
    2. 개별 dart_dict를 분석하여 중요한 dart는 노티한다.
    3. 저장된 피클데이터를 업데이트 한다.
    """
    def __init__(self, edate: str, subject: str, pkl: Pickle):
        # edate와 subject 형식 여부 확인
        if not utils.chk_date_format_Ymd(edate):
            raise Exception(f"Invalid date - {edate}(YYYYMMDD)")
        if subject not in enabled_subject:
            raise Exception(f'{subject} is not available.')
        self.subject = subject
        self.dart_dict_list = self.make_dart_dict_list(edate, subject)
        self.pickle = pkl  # pkl.contents = {'date': '20201010', 'notified': [rno..], 'analysed': [rno..]}

    @staticmethod
    def make_dart_dict_list(edate: str, subject: str) -> list:
        """
        df를 intro 딕셔너리를 포함하는 리스트로 변환한다.
        :return: df를 변환하여 얻은 intro 딕셔너리를 포함하는 리스트
        """
        logger.info('<<<  make_dart_dict_list() start >>>')
        df = save_db.MakeDF(edate=edate, title=subject).get_df()
        dart_dict_list = []
        for i, namedtuple in enumerate(df.itertuples()):
            dart_dict_list.append(subjects.make_dart_dict(namedtuple))
        logger.info(dart_dict_list)
        return dart_dict_list

    def pre_ansys_test(self, dart_dict: dict) -> bool:
        if dart_dict['code'] not in subjects.krx_all:
            # 아직 코드가 krx에 없는 경우는 넘어간다.
            print(f"\t{dart_dict['code']} {dart_dict['name']}is not registered in corp db yet..")
            time.sleep(.5)
            self.pickle.contents['analysed'].append(dart_dict['rno'])
            return False
        elif dart_dict['rno'] in self.pickle.contents['analysed']:
            print(f"\t<{dart_dict['rno']}> already analysed")
            time.sleep(.5)
            return False
        elif dart_dict['rno'] in self.pickle.contents['notified']:
            print(f"\t<{dart_dict['rno']}> already notified")
            time.sleep(.5)
            return False
        else:
            return True

    @staticmethod
    def notifying(dart_dict: dict, cls: subjects.DartSubject):
        print(f"We caught the important report..{dart_dict['rno']}")
        try:
            noti.telegram_to(botname='dart', text=str(cls))
            noti.telegram_to(botname='eval', text=eval.ReportOne(dart_dict['code']).for_telegram())
        except TimedOut:
            time.sleep(3)
            print(f'Telegram does not respond, retrying...')
            noti.telegram_to(botname='dart', text=str(cls))

    @staticmethod
    def distribute_to_corps_db(dart_dict: dict, cls: subjects.DartSubject, is_noti: bool):
        """
        개별 종목의 분석 데이터를 각 종목의 데이터베이스에 나눠서 저장하는 함수
        """
        data = {'code': dart_dict['code'],
                'rcept_no': dart_dict['rno'],
                'rcept_dt': dart_dict['rdt'],
                'report_nm': dart_dict['rtitle'],
                'point': cls.point,
                'text': cls.text,
                'is_noti': is_noti}
        pipe = save_db.Pipeline(data=data)
        if 'sqlite' in pipe.setting.contents['activated_db']:
            pipe.to_sqlite()
        if 'mongo' in pipe.setting.contents['activated_db']:
            pipe.to_mongo()

    def run(self):
        logger.info('<<<  run() start >>>')
        # opendart 사이트의 연결여부 확인
        if not save_db.MakeDF.islive_opendart():
            return
        t = len(self.dart_dict_list)
        for i, dart_dict in enumerate(self.dart_dict_list):
            print(f"{i + 1}/{t}. code: {dart_dict['code']}\tname: {dart_dict['name']}")
            if not self.pre_ansys_test(dart_dict):
                continue
            after_analyse_cls = subjects.analyse_one_item(subject=self.subject, dart_dict=dart_dict)
            self.pickle.contents['analysed'].append(dart_dict['rno'])
            if after_analyse_cls.point >= subjects.DartSubject.NOTI_POINT:
                is_noti = True
                self.notifying(dart_dict, after_analyse_cls)
                self.pickle.contents['notified'].append(dart_dict['rno'])
            else:
                is_noti = False
            self.distribute_to_corps_db(dart_dict, after_analyse_cls, is_noti)
            if (i != 0) and (i % 5) == 0:
                print('Saving to pickle...')
                self.pickle.save()  # 5개 단위로 분석이 완료되면 저장한다.
        print('Saving to pickle...')
        self.pickle.save()  # 한 타이틀이 끝나면 저장한다.


def run_all_subjects(edate: str):
    pkl = Pickle()  # {'date': '20201010', 'notified': [rno..], 'analysed': [rno..]}
    if pkl.contents['date'] != edate:
        # 피클에 세팅된 date가 입력된 edate와 다른 날짜의 경우 피클을 리셋한다.
        pkl.init(edate)
        pkl.load()

    print(f'Titles - {enabled_subject}')
    start_time = time.time()
    print('*' * 40, 'Dart analysis all titles', '*' * 40)
    for subject in enabled_subject:
        AnalyseOneSubject(edate=edate, subject=subject, pkl=pkl).run()
    print(pkl.show())
    end_time = int(time.time() - start_time)
    print(f'Total spent time : {end_time} sec.')
    return end_time
