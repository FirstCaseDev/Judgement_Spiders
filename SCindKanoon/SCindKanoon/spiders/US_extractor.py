import scrapy
from ..items import document
from collections import OrderedDict
import datefinder
import re
import regex
import string
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('popular')
from nltk.corpus import stopwords 
items = document()
stop = stopwords.words('english')

class CrawlerSpider(scrapy.Spider):
    name = 'usextractor'
    start_urls = ['https://www.courtlistener.com/?type=o&order_by=dateFiled+desc&stat_Precedential=on&court=calctapp']

    def concatURL(self, url_str):
        new_url = 'https://www.courtlistener.com' + url_str
        return new_url
    
    def parse(self,response):
        searchBrowseList = response.css('.visitable')
        for result in  searchBrowseList:
            caseURL = result.css('a ::attr(href)').extract_first() 
            yield scrapy.Request(
                response.urljoin(caseURL),
                callback=self.parseCase,
                dont_filter=True
            )

        next_page = response.css('.btn-default ::attr(href)').extract()[-1]
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse)


    def parseCase(self, response):
        try:
            petitioner = response.css('h2 ::text').extract()[2].split(',')[0]
        except:
            petitioner = ""
        try: 
            respondent = response.css('h2 ::text').extract()[0].split(',')[0]
        except:
            respondent = ""
        try:
            judgement_text = " ".join(response.css('pre ::text').extract())
        except: 
            judgement_text = " ".join(response.css('.col-sm-9 ::text').extract())
        sentences = judgement_text.split('\n')
        source = 'California Court of Appeal'
        matches = list(datefinder.find_dates(response.css('h3+ .bottom .meta-data-value ::text').extract_first()))
        date = matches[-1].day
        month = matches[-1].month
        year = matches[-1].year
        paras = judgement_text.split('\n\n')
        last_paras = ' '.join(paras[-15:])
        if 'affirmed' in last_paras:
            judgement = 'dismissed'
        elif 'denied' in last_paras: 
            judgement = 'dismissed'    
        elif 'dismissed' in last_paras:
            judgement = 'dismissed'
        elif 'reversed' in last_paras: 
            judgement = 'allowed'
        else:
            last_paras = ' '.join(paras[-20:])
            if 'affirmed' in last_paras:
                judgement = 'dismissed'
            elif 'denied' in last_paras: 
                judgement = 'dismissed'    
            elif 'dismissed' in last_paras:
                judgement = 'dismissed'
            elif 'reversed' in last_paras: 
                judgement = 'allowed'
            else:
                last_paras = ' '.join(paras[-35:])
                if 'affirmed' in last_paras:
                    judgement = 'dismissed'
                elif 'denied' in last_paras: 
                    judgement = 'dismissed'    
                elif 'dismissed' in last_paras:
                    judgement = 'dismissed'
                elif 'reversed' in last_paras: 
                    judgement = 'allowed'
                else:
                    judgement = 'tied / unclear'
        
        bench_sub = ', J\\.'
        bench_sentence = [x for x in sentences if re.search(bench_sub,x)]  
        bench_sub = 'P\\. J\\.'
        bench_sentence += [x for x in sentences if re.search(bench_sub,x)]  
        bench_sub = 'Judge:'
        bench_sentence += [x for x in sentences if re.search(bench_sub,x)]
        bench_sentence = [sub.replace("P. J.", '') for sub in bench_sentence]
        bench_sentence = [sub.replace(", J.", '') for sub in bench_sentence]
        bench_sentence = [sub.replace("Trial", '') for sub in bench_sentence]
        bench_sentence = [sub.replace("Acting", '') for sub in bench_sentence]
        bench_sentence = [sub.replace("ACTING", '') for sub in bench_sentence]
        bench_sentence = [sub.replace("Judge", '') for sub in bench_sentence]
        bench = [sub.translate(str.maketrans('', '', string.punctuation)).strip() for sub in bench_sentence]
        bench = list(dict.fromkeys(bench))
        bench = ", ".join(bench) 

        appellant_sub = 'for Defendant and Appellant'
        appellant_sentence = [x for x in sentences if re.search(appellant_sub,x)] 
        appellant_sub = 'for Defendant/Appellant'
        appellant_sentence += [x for x in sentences if re.search(appellant_sub,x)]
        appellant_sub = 'for\nDefendant'
        appellant_sentence += [x for x in sentences if re.search(appellant_sub,x)]
        appellant_sub = 'for Petitioner'
        appellant_sentence += [x for x in sentences if re.search(appellant_sub,x)]
        appellant_sub = 'for Defendant'
        appellant_sentence += [x for x in sentences if re.search(appellant_sub,x)]
        appellant_sentence = [sub.replace("for", '') for sub in appellant_sentence]
        appellant_sentence = [sub.replace("Counsel", '') for sub in appellant_sentence]
        appellant_sentence = [sub.replace("Appellant", '') for sub in appellant_sentence]
        appellant_sentence = [sub.replace("and", '') for sub in appellant_sentence]
        appellant_sentence = [sub.replace("Petitioner", '') for sub in appellant_sentence]
        appellant_sentence = [sub.replace("Defendant", '') for sub in appellant_sentence]
        appellant_sentence = [sub.replace("Respondent", '') for sub in appellant_sentence]
        appellant_sentence = [sub.replace("Appeal", '') for sub in appellant_sentence]
        appellant_sentence = [sub.replace("under appointment by the Court of", '') for sub in appellant_sentence]
        petitioner_counsel = [sub.translate(str.maketrans('', '', string.punctuation)).strip() for sub in appellant_sentence]
        petitioner_counsel = list(dict.fromkeys(petitioner_counsel))

        respondent_sub = 'for Plaintiff and Respondent'
        respondent_sentence = [x for x in sentences if re.search(respondent_sub,x)] 
        respondent_sub = 'for Respondent'
        respondent_sentence += [x for x in sentences if re.search(respondent_sub,x)]
        respondent_sub = 'for Plaintiff'
        respondent_sentence += [x for x in sentences if re.search(respondent_sub,x)]
        respondent_sub = 'for\nPlaintiff'
        respondent_sentence += [x for x in sentences if re.search(respondent_sub,x)]
        respondent_sub = 'for Plaintiff/Respondent'
        respondent_sentence += [x for x in sentences if re.search(respondent_sub,x)]
        respondent_sentence = [sub.replace("for", '') for sub in respondent_sentence]
        respondent_sentence = [sub.replace("Counsel", '') for sub in respondent_sentence]
        respondent_sentence = [sub.replace("Respondent", '') for sub in respondent_sentence]
        respondent_sentence = [sub.replace("and", '') for sub in respondent_sentence]
        respondent_sentence = [sub.replace("Plaintiff", '') for sub in respondent_sentence]
        respondent_sentence = [sub.replace("petitioner", '') for sub in respondent_sentence]
        respondent_sentence = [sub.replace("Defendant", '') for sub in respondent_sentence]
        respondent_sentence = [sub.replace("Appellant", '') for sub in respondent_sentence]
        respondent_sentence = [sub.replace("under appointment by the Court of", '') for sub in respondent_sentence]
        respondent_counsel = [sub.translate(str.maketrans('', '', string.punctuation)).strip() for sub in respondent_sentence]
        respondent_counsel = list(dict.fromkeys(respondent_counsel))

        items['source'] = source
        items['url'] = response.request.url
        items['petitioner'] = petitioner
        items['respondent'] = respondent
        items['date'] = date
        items['month'] = month
        items['year'] = year
        items['bench'] = bench
        items['judgement'] = judgement
        items['judgement_text'] = judgement_text
        items['petitioner_counsel'] = petitioner_counsel
        items['respondent_counsel'] = respondent_counsel
        items['title'] = respondent + ' v. ' + petitioner
        print("...")
        yield(items)
        # yield(items)

        

    