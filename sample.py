from IMLTokenizer import Tokenizer

obj = Tokenizer()
msg = "아름다운 개는 짖는다, 사람은 밥을 먹는다"
print(obj.pos(msg))
print(obj.get_nouns(msg))
print(obj.morphs(msg))
print(obj.nouns(msg))