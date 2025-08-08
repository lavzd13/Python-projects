digit1 = 0
digit2 = 0
digit3 = 0
digit4 = 0
combinations = []

while 1:
	combinations.append((str(digit1) + str(digit2) + str(digit3) + str(digit4)))
	if digit1 == 9 and digit2 == 9 and digit3 == 9 and digit4 == 9:
		break
	digit4+=1
	if digit4 == 10:
		digit3+=1
		digit4 = 0
	if digit3 == 10:
		digit2+=1
		digit3 = 0
		digit4 = 0
	if digit2 == 10:
		digit1+=1
		digit2 = 0
		digit3 = 0
		digit4 = 0