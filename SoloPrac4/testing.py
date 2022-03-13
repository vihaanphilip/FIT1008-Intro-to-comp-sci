import string

with open("84-0.txt", 'r', encoding='utf-8') as file:
    line = file.readline()
    while line:
        line = line.split()
        if line != []:
            for i in range(len(line)):
                word = line[i]
                word = word.lower()
                
                punc = string.punctuation

                """
                for letter in word:
                    if letter in punc:
                        word = word.replace(letter, "")
                

                if word[len(word)-1] in punc:
                    word = word.replace(word[len(word)-1], "")
                """

                word = word.strip(punc)
                
                print(word)

        line = file.readline()

# %%
test = (None, 0)
print(test[0])

# %%
word = ",char!"
punc = string.punctuation
print(word.strip(punc))
print(string.punctuation)
print(word)
        
        