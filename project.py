import csv

def decrypt(p,a,y1,y2): # d(y1,y2) = y2*(y1^a)^-2 mod p

    def fastExp(): # implement fast exponentiation algorithm

        binary = list(bin(a)[2:])
        binary.reverse()
        length = len(binary)

        # Calculate mod of all powers of two
        modCalcs = []
        i = 0
        result = 1
        while i < length:
            if i == 0:
                modCalcs.append(y1 % p)
            else:
                mod = ((modCalcs[i-1])**2) % p
                modCalcs.append(mod)
            if binary[i] == '1':
                result = result*modCalcs[i] # find resulting value for y1^a
            i+=1
        
        final = result % p # find result mod p, used in next step
        return final
    
    result = fastExp()
    
    def multInv(): # find multiplicative inverse of previous result mod p
        for i in range(p):
            if (result * i) % p == 1:
                return i

    answer = (multInv() * y2) % p

    def extractLetters(number):
        # Calculates the index for each of the letters from the result of decryption
        first = number // (26**2)
        second = (number % (26**2)) // 26
        third = (number % (26**2)) % 26

        # Read in csv file and create dictionary mapping numbers (0-25) to letters (A-Z)
        with open('letters.csv','r') as readFile:
            reader = csv.reader(readFile)
            letters = {}
            for row in reader:
                letters[row[0]] = row[1]

        # Assign letters to numbers found above for the three letters
        for letter in letters:
            if str(first) == letter:
                first = letters[letter]
            if str(second) == letter:
                second = letters[letter]
            if str(third) == letter:
                third = letters[letter]

        return first,second,third
    
    return fastExp(), multInv(), answer, extractLetters(answer)

# Iterate over all ciphertext and combine results
with open('ciphertext.csv','r') as readFile:
        reader = csv.reader(readFile)
        plaintext = []
        for row in reader:
            y1,y2 = int(row[0]), int(row[1])
            plaintext.append(decrypt(31847,7899,y1,y2)[3])

print(plaintext)
