


def Cipher():
	plaintext = input("Please enter your plaintext:\n")
	cipherText = ""
	for i in range(0, len(plaintext)):
		plaintextchar = plaintext[i]
		alphabetpos = 3
		while plaintextchar != alphabet[alphabetpos]:
			alphabetpos=alphabetpos+1
		alphabetpos=alphabetpos-3
		cipherText=cipherText+alphabet[alphabetpos]
	print(cipherText)
	
def Decrypt():
	cipheredtxt = input("Please enter your ciphered text:\n")
	decryptedtxt = ""
	for i in range(0, len(cipheredtxt)):
		cipheredtxtchar = cipheredtxt[i]
		alphabetpos = 3
		while cipheredtxtchar != alphabet[alphabetpos]:
			alphabetpos=alphabetpos+1
		alphabetpos=alphabetpos+3
		decryptedtxt=decryptedtxt+alphabet[alphabetpos]
	print(decryptedtxt)
	
def main():
	global alphabet
	alphabet = "XYZABCDEFGHIJKLMNOPQRSTUVWXYZABC"
	choice = input("Do you want to encrypt or decrypt text(E/D)?\n")
	if choice=="E":
		Cipher()
	else:
		Decrypt()
		
main()
