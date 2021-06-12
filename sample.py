from IMLTokenizer import Tokenizer
from IMLTokenizer import Refiner
import time

msg = "아름다운 개는 짖는다, 사람은 밥을 먹는다 커스터마이징 디센트"
refiner = Refiner()
msg = refiner.char_filter(msg)

tokenizer = Tokenizer()


start = time.time()

print(tokenizer.get_nouns(msg))
# print(tokenizer.nouns(msg))
# print(tokenizer.pos(msg))
# print(tokenizer.morphs(msg))

print("sec:", time.time() - start)
# 0.0013