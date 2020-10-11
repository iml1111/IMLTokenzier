'''
Noun Extractor Module
- konlpy 형태소 분석기를 상속받아 
  부가 전처리 메소드를 추가로 작성하였음.
'''
import re
from konlpy.tag import Mecab
from nltk.corpus import stopwords
from morph_info import sign_dict
from token_dict import (single_stop,
                        token_stop,
                        endwith_remove_list,
                        endwith_stop,
                        mean_inter_dict,
                        ex_morphs,
                        except_set)


class NounEx(Mecab):
    '''Tokenizer Class'''
    
    def __init__(self):
        self.eng_stop = set(stopwords.words('english'))
        self.single_stop = single_stop
        self.token_stop = token_stop
        self.endwith_remove_list = endwith_remove_list
        self.endwith_stop = endwith_stop
        self.mean_inter_dict = mean_inter_dict
        self.ex_morphs = ex_morphs  
        self.signed_morphs = sign_dict
        self.except_set = except_set
        self.emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F" # emoticons
            u"\U0001F300-\U0001F5FF" # symbols & pictographs
            u"\U0001F680-\U0001F6FF" # transport & map symbols
            u"\U0001F1E0-\U0001F1FF" # flags (iOS)
        "]+", flags=re.UNICODE)
        super(NounEx, self).__init__()

    def get_tk(self, string):
        '''
        문자열 to 토큰화 메소드

        Params
        - string : 인풋 문자열

        Returns
        - tokens : 토큰 리스트
        '''
        cleaned_docs = self._doc_cleaning(string)
        tokens = self._tokenize(cleaned_docs)
        return tokens

    def _doc_cleaning(self, doc, length=3_000, low=True):
        '''
        문서 정제 및 정규화
        - length : 리스트 단일 원소당 최대 문자열 길이
        - low : 소문자화 여부
        '''
        doc = doc.strip()
        
        if low:
            doc = doc.lower()

        doc = self.emoji_pattern.sub(r' ', doc)
        doc = re.sub(r'[^ ㄱ-ㅣ가-힣|a-z|0-9|:]+', ' ', doc)
        doc = re.sub(r'\s+', ' ', doc)
        return [doc[i:i + length] for i in range(0, len(doc), length)]

    def _tokenize(self, doc_list, validate=True):
        '''정제된 문서에 대한 토큰화 모듈'''
        result = []
        for doc in doc_list:
            
            try:
                morphs = self.pos(doc)
                morphs = self._except_morphs_process(morphs)
                tokens = self._morphs_validation(morphs, validate)
                result += tokens
            
            except Exception as e:
                print("Tokenize Error:", e)
                result = ["".join(doc_list)]
                return self._except_doc_process(result, doc_list)

        return self._except_doc_process(result, doc_list)

    def _except_morphs_process(self, morphs):
        '''형태소 분석이 잘못된 토큰에 대해서 붙여주는 작업 수행'''
        for idx, data in enumerate(morphs):
            for ex in self.ex_morphs:
                if self._is_ex_morphs(morphs[idx:idx + len(ex["morphs"])],
                                      ex["morphs"]):
                    morphs[idx] = (ex['word'], 'PASS')
                    for i in range(idx + 1, idx + len(ex["morphs"])):
                        morphs[i] = ('X', 'NO')
                    break
        return morphs

    def _is_ex_morphs(self, data, ex):
        '''해당 형태소가 잘못된 분석인지 탐색'''
        if len(data) != len(ex):
            return False
        
        for i in range(len(ex)):
            if data[i][0] != ex[i][0]:
                return False
        
        return True

    def _morphs_validation(self, morphs, validate_mode=True):
        '''
        각 형태소에 대한 토큰화 검증
        - 토큰화 통과 여부 결정
        - 토큰화시, 단어 변경 여부 결정
        '''
        result = []
        if validate_mode:
            for word, m_type in morphs:
                if self._is_valid(word, m_type):
                    result += [self._except_token_process(word)]
        else:
            for word, m_type in morphs:
                result += [self._except_token_process(word)]

        return result

    def _is_valid(self, word, m_type):
        '''
        각 형태소의 토큰화 통과 여부 검증
        - 예외처리 특수 키워드(except_set)일 경우, PASS
        - 키워드가 endwith_stop로 끝날 경우, NO
        - 단어의 길이가 15자 이상일 경우, NO
        - 비속어, 무의미한 단어(token_stop)일 경우, NO
        - 해당 형태소가 추출 제외 대상일 경우, NO
        - 형태소 타입이 SL(영문)이면서, 영어 불용어일 경우, NO
        - 형태소 타입이 SL(영문)이면서, 2자 이하일 경우, NO
        - 한영 문자 외에 다른 문자가 섞여 있을 경우, NO
        '''
        if word in self.except_set:
            return True
        for i in self.endwith_stop:
            if word.endswith(i):
                return False
        if len(word) >= 15:
            return False
        if word in self.token_stop:
            return False
        if set(word) & self.single_stop:
            return False
        if m_type not in self.signed_morphs.values():
            return False
        if m_type == 'SL' and word in self.eng_stop:
            return False
        if m_type == 'SL' and len(word) <= 2:
            return False
        if m_type not in ['SH', 'SL'] and \
           word != re.sub(r'[^ ㄱ-ㅣ가-힣|a-z]+', ' ', word):
           return False
        return True

    def _except_token_process(self, word):
        '''토큰으로 등록되기 전, 변경 작업 수행'''
        for i in self.endwith_remove_list:
            if word != i and word.endswith(i):
                word = word[:-len(i)]
                break
        if word in self.mean_inter_dict:
            word = mean_inter_dict[word]
        return word

    def _except_doc_process(self, tokens, doc_list):
        '''문서 전체에 대한 예외처리'''
        return tokens