# script to find the five longest words in the words file

longest_words = ['', '', '', '', '']

with open('/usr/share/dict/words', 'r') as f:

    for word in f:
        len_word = len(word.strip('\n'))
        for i in range(5):
            len_long_word = len(longest_words[i].strip('\n'))
            if len_word > len_long_word:
                longest_words.insert(i, word)
                longest_words.pop(-1)
                break
            if len_word == len_long_word:
                list = [word, longest_words[i]]
                list.sort()
                longest_words.pop(i)
                longest_words.insert(i, list[1])
                longest_words.insert(i, list[0])
                longest_words.pop(-1)
                break

print('\n\n\nlongest words start here\n')
for word in longest_words:
    print(word.strip('\n'))




