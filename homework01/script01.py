with open('/usr/share/dict/words', 'r') as f:
    words = f.read().splitlines()

longest_words = words[:5]

for word in words:
    for i in range(len(longest_words)):
        if len(word) > len(longest_words[i]):
            longest_words[i] = word
            break
        
for word in longest_words:
    print(f'{word}\n')
