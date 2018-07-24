import roman
import random
class TextAnalyzer():
    def __init__(self, filename_txt):
        with open(filename_txt) as f:
            self.read_lines = f.readlines()
        self.__count_data()
    def __count_data(self):
        self.chapter_word_count = {}
        with open("1-1000.txt") as f:
            self.common_words = set([s.lower() for s in f.read().split()[:100]])
        with open("chapter.txt") as f:
            self.chapters = set(f.readlines())
        current_chapter = 1
        self.chain = {}
        prev_word = ""
        self.chapter_text = {}
        for line in self.read_lines :
            if line in self.chapters :
                current_chapter = roman.fromRoman(line.split()[1].strip(".\n"))
            else :
                self.chapter_word_count[current_chapter] = self.chapter_word_count.get(current_chapter, {})
                self.chapter_text[current_chapter] = self.chapter_text.get(current_chapter, "") + line
                for word in line.split():
                    if prev_word not in self.chain :
                        self.chain[prev_word] = []
                    self.chain[prev_word].append(word)
                    clean_word = word.lower().strip("'\",.!?;()")
                    word_count = self.chapter_word_count[current_chapter]
                    word_count[clean_word] = word_count.get(clean_word, 0) + 1
                    prev_word = word
        self.sorted_word_count = {}
        for ch in self.chapter_word_count.keys():
            for word in self.chapter_word_count[ch]:
                self.sorted_word_count[word] = self.sorted_word_count.get(word, 0) + self.chapter_word_count[ch][word]
        self.sorted_word_count = sorted(self.sorted_word_count.items(), key=lambda x : -x[1])
    def getTotalNumberOfWords(self):
        return sum([sum([chaptervals[key] for key in chaptervals]) for chaptervals in self.chapter_word_count.values()])
    def getTotalUniqueWords(self):
        unique = set()
        for ch in self.chapter_word_count.keys():
            for word in self.chapter_word_count[ch]:
                unique.add(word)
        return len(unique)
    def get20MostFrequentWords(self):
        return self.sorted_word_count[:20]
    def get20MostInterestingFrequentWords(self):
        interesting_words = []
        for pair in self.sorted_word_count:
            if pair[0] not in self.common_words and len(interesting_words) < 20:
                interesting_words.append(pair)
        return interesting_words
    def get20LeastFrequentWords(self):
        return self.sorted_word_count[::-1][:20]
    def getFrequencyOfWord(self, word):
        sorted_keys = sorted(self.chapter_word_count.keys())
        freq = []
        for chapter in sorted_keys :
            freq.append(self.chapter_word_count[chapter].get(word, 0))
        return freq
    def getChapterQuoteAppears(self, quote):
        for chapter in self.chapter_text :
            if self.chapter_text[chapter].find(quote) >= 0 :
                return chapter
        return -1
    def generateSentence(self):
        word = "the"
        sentence = word
        choices = self.chain
        for i in range(20):
            word = random.choice(choices[word])
            sentence += " " + word
        return sentence
thingy = TextAnalyzer("996.txt")
print(thingy.getTotalNumberOfWords())
print(thingy.getTotalUniqueWords())
print(thingy.get20MostFrequentWords())
print(thingy.get20MostInterestingFrequentWords())
print(thingy.get20LeastFrequentWords())
print(thingy.getFrequencyOfWord("great"))
print(thingy.getChapterQuoteAppears("tamper with their princesses"))
print(thingy.generateSentence())
