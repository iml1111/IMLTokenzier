from modules.tokenizer import Tokenizer

obj = Tokenizer()
msg = "사람은 밥을 먹는다"
result = obj.get_tk(msg)
print(result)
# result = obj.pos(msg)
# print(result)