from IMLTokenizer import Tokenizer
from IMLTokenizer import Refiner


msg = (
	"@%!@$% 아름다운 개는 짖는다."
	"사람은 밥을 먹는다. 커스터마이징,"
	" 그래디언트 디센트"
)

refiner = Refiner()
msg = refiner.char_filter(msg)

tokenizer = Tokenizer()
print(tokenizer.get_nouns(msg))
print(tokenizer.get_tokens(msg))