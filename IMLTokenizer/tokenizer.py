'''
Noun Extractor Module
- konlpy 형태소 분석기를 상속받아 
  부가 전처리 메소드를 추가로 작성하였음.
'''
import re
from konlpy.tag import Mecab
from nltk.corpus import stopwords
from .morph_info import noun_morphs
from .token_dict import (
    stop_single,
    stop_tokens,
    endwith_remove_list as erl,
    stop_endwith,
    same_words,
    morphs_combine,
    valid_words,
)


class Tokenizer(Mecab):
    '''Tokenizer Class'''
    
    def __init__(self):
        self.eng_stop = set(stopwords.words('english')) # 영어 불용어
        self.stop_single = stop_single # 단일 자모음 제외셋
        self.stop_tokens = stop_tokens # 한글 불용어
        self.endwith_remove_list = erl # 마지막 공통 부분 제거 단어
        self.stop_endwith = stop_endwith # 끝부분 매칭 불용어
        self.same_words = same_words # 동일어 사전
        self.morphs_combine = morphs_combine  # 형태소 합성 사전
        self.noun_morphs = noun_morphs # 명사 범주 형태소 사전
        self.valid_words = valid_words # true valid 키워드

        super(Tokenizer, self).__init__()

    def get_nouns(self, text):
        '''정제된 문서에 대한 토큰화 모듈'''
        try:
            morphs = self.pos(text)
            morphs = self._except_morphs_process(morphs)
            tokens = self._morphs_validation(morphs)

        except Exception as e:
            print("Tokenize Error:", e)
            return None

        return self._except_doc_process(tokens, text)

    def _except_morphs_process(self, morphs):
        '''형태소 분석이 잘못된 토큰에 대해서 붙여주는 작업 수행'''
        for idx, data in enumerate(morphs):
            for ex in self.morphs_combine:
                if self._is_ex_morphs(
                    morphs[idx:idx + len(ex["morphs"])],
                    ex["morphs"]
                ):
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

    def _morphs_validation(self, morphs):
        '''
        각 형태소에 대한 토큰화 검증
        - 토큰화 통과 여부 결정
        - 토큰화시, 단어 변경 여부 결정
        '''
        result = []
        for word, m_type in morphs:
            if self._is_valid(word, m_type):
                result += [self._except_token_process(word)]

        return result

    def _is_valid(self, word, m_type):
        '''
        각 형태소의 토큰화 통과 여부 검증
        - 예외처리 특수 키워드(valid_words)일 경우, PASS
        - 키워드가 endwith_stop로 끝날 경우, NO
        - 단어의 길이가 15자 이상일 경우, NO
        - 비속어, 무의미한 단어(token_stop)일 경우, NO
        - 해당 형태소가 추출 제외 대상일 경우, NO
        - 형태소 타입이 SL(영문)이면서, 영어 불용어일 경우, NO
        - 형태소 타입이 SL(영문)이면서, 2자 이하일 경우, NO
        - 한영 문자 외에 다른 문자가 섞여 있을 경우, NO
        '''
        if word in self.valid_words:
            return True
        for i in self.stop_endwith:
            if word.endswith(i):
                return False
        if len(word) >= 15:
            return False
        if word in self.stop_tokens:
            return False
        if set(word) & self.stop_single:
            return False
        if m_type not in self.noun_morphs.values():
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
        if word in self.same_words:
            word = same_words[word]
        return word

    def _except_doc_process(self, tokens, doc_list):
        '''문서 전체에 대한 예외처리'''
        return tokens