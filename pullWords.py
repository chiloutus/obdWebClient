
longWords = "longWords.txt"
fn = "/usr/share/dict/words"
with open(fn) as words:
	for line in words:
		with open(shortWords,'w') as lWord:
			for line in words:
				line = line[:-1]
				if "\'" in line:
					continue
				elif len(line) >= 4:
					lWord.write(line + '\n')
