# author: Shane Yu  date: April 8, 2017
from django.core.management.base import BaseCommand, CommandError
import json, multiprocessing, pymongo, logging, threading, math
from gensim import models
from kcem.utils.utils import criteria
from django.http import HttpRequest
from kcmApp.views import kcm as kcmRequest
from udic_nlp_API.settings_database import uri

class Command(BaseCommand):
    help = 'use this to test kcem!'
    
    def export2Mongo(self):
        # 目前實驗起來最好的組合
        kcm = 22
        kem = 12
        httpReq = HttpRequest()
        httpReq.method = 'GET'
        httpReq.GET['lang'] = 'cht'
        keywordList = list(self.model.vocab.keys())
        step = math.ceil(len(keywordList)/multiprocessing.cpu_count())
        keywordPieces = [keywordList[i:i + step] for i in range(0, len(keywordList), step)]
        logging.basicConfig(format='%(levelname)s : %(asctime)s : %(message)s', filename='buildKCEM.log', level=logging.INFO)
        logging.info('build keywordPieces')
        self.Collect.remove({})

        def activateKCEM(keywordThreadList):
            ThreadResult = []
            for index, keyword in enumerate(keywordThreadList):
                kcm_lists = list()

                for kemtopn in self.model.most_similar(keyword, topn = kem):

                    httpReq.GET['num'] = kcm
                    httpReq.GET['keyword'] = kemtopn[0]             
                    kcm_lists.append( list( kcmtopn 
                        for kcmtopn in json.loads(kcmRequest(httpReq).getvalue().decode('utf-8'))
                        ) 
                    )

                result={}
                for kcm_list in kcm_lists:#統計出現的字
                    for word in kcm_list:
                        result[word[0]] = result.setdefault(word[0], 0) + 1.0/float(kem)

                result = sorted(result.items(), key = lambda x: -x[1])
                ThreadResult.append({'key':keyword, 'value':criteria('hybrid', result[:10], keyword)})
                if index % 10000 == 0:
                    logging.info("已處理 %d 個單子" % index)

            self.Collect.insert(ThreadResult)

        logging.info('create thread')
        workers = [threading.Thread(target=activateKCEM, kwargs={'keywordThreadList':keywordPieces[i]}, name=str(i)) for i in range(multiprocessing.cpu_count())]

        logging.info('start thread')
        for thread in workers:
           thread.start()

        # Wait for all threads to complete
        for thread in workers:
            thread.join()
        self.Collect.create_index([("key", pymongo.HASHED)])

    def handle(self, *args, **options):
        self.client = pymongo.MongoClient(uri)
        self.db = self.client['nlp']
        self.Collect = self.db['kcem']
        self.model = models.KeyedVectors.load_word2vec_format('med400.model.bin', binary=True)
        self.export2Mongo()
        self.stdout.write(self.style.SUCCESS('build kcem model success!!!'))