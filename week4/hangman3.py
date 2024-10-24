import random

with open('dictionary.txt', 'r') as words:
	wordlist = words.readlines()
	word = wordlist[random.randint(0, (len(wordlist)-1))]

guesses = ""
answer = "_"*len(word)
win = False
i=0

while i<10 and win==False:
	i+=1
	guess = input("Enter guess " +str(i)+ ": ")
	guesses = guesses + guess
	tmp = ""
	for x in word:
		if x==guess:
			tmp = tmp + guess
		else:
			tmp = tmp + answer[word.index(x)]
	if answer!=tmp:
		print("good guess")
		i-=1
		answer = tmp
	else:
		print("not a good guess")
	if answer == word:
		print("Well done!")
		win = True
		break
	print(str(10-i)+"/10 guesses left")
	print("your guesses:"+guesses)
	print("The word so far: "+answer)
	if i==10:
		print("Unlucky, word was "+word)
