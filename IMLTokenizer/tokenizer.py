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
    combine_lenghs,
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
        self.combine_lenghs = combine_lenghs # 합성 사전 길이 셋
        self.noun_morphs = noun_morphs # 명사 범주 형태소 사전
        self.valid_words = valid_words # true valid 키워드

        super(Tokenizer, self).__init__()

    def get_nouns(self, text):
        '''정제된 문서에 대한 토큰화 모듈'''
        tokens = self.pos(text)
        tokens = self._combine_morphs_process(tokens)
        tokens = self._morphs_validation(tokens)
        return tokens

    def _combine_morphs_process(self, morphs):
        '''형태소 분석이 잘못된 토큰을 다시 붙여주는 작업'''
        idx, morphs_len = 0, len(morphs)

        while idx < morphs_len:
            combine_available, length = self._combine_valid(morphs, idx, morphs_len)
            if combine_available:
                morphs[idx] = (
                    "".join([i[0] for i in 
                    morphs[idx:idx+length]]), 
                    'PASS'
                )
                del morphs[idx + 1: idx + length]
                idx += length
            idx += 1
                
        return morphs

    def _combine_valid(self, src, src_idx, src_len):
        '''해당 형태소 셋이 합성 가능한지 검증'''
        for tgt_len in self.combine_lenghs:
            
            if src_len - src_idx < tgt_len:
                break
            
            src_tuple = tuple([
                token[0] for token in 
                src[src_idx: src_idx + tgt_len]]
            )
            if src_tuple in self.morphs_combine:
                return True, tgt_len

        return False, None

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