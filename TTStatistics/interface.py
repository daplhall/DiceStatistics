from TTStatistics.Dice import Dice
from TTStatistics._parser import text_to_faces

def d(inpt: list | str) -> Dice:
	if isinstance(inpt, int):
		return Dice(range(1,inpt+1))
	elif isinstance(inpt, str):
		faces = text_to_faces(inpt)
		return Dice(faces)
	else:
		raise Exception("Dice doens't support input type of %s"%(type(inpt)))

def z(inpt: int) -> Dice:
	return Dice(range(0, inpt + 1))