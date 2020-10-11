from tokenizer import NounEx

obj = NounEx()
msg = "사람은 밥을 먹는다"
result = obj.get_tk(msg)
print(result)