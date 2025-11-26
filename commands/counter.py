# Функція рахує кількість
# Цифр, букв (з них великих і малих), пробілів, символів
# * кількість голосних і приголосних.
from commands import calculator

# Digits :
# Letters :
# Upper :
# Lower :
# Spaces :
# Symbols :

# Vowel : (голосні)
# Consonant : (приголосні)


results = {'Digits' : 0, 'Letters' : 0, 'Uppers' : 0, 'Lowers' : 0, 'Symbols' : 0,
           'Spaces' : 0, 'Vowels' : 0, 'Consonants' : 0}
vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U', "а","о","є","е","и","і","я","ю" ]

def count(text):
    for letter in text:
        if letter.isalpha():
            results['Letters'] += 1
            if letter.isupper():
                results['Uppers'] += 1
            elif letter.islower():
                results['Lowers'] += 1
            if letter in vowels:
                results['Vowels'] += 1
            elif letter not in vowels:
                results['Consonants'] += 1
        elif letter.isdigit():
            results['Digits'] += 1
        elif letter.isspace():
            results['Spaces'] += 1
        else:
            results['Symbols'] += 1

    return results

print(count('Some text 123.'))