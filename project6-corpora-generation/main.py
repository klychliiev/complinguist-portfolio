import re
from stanza import Pipeline
import sqlite3
import os

nlp = Pipeline(lang='uk', processors='tokenize,pos,lemma,mwt')


DIRECTORY_PATH = 'texts/'

ABS_PATH = "db/"

POS_TAGS = {
   'NOUN': 'Іменник',
   'ADJ': 'Прикметник',
   'NUM': 'Числівник',
   'PRON': 'Займенник',
   'DET': 'Займенник',
   'VERB': 'Дієслово',
   'AUX': 'Дієслово "бути"',
   'ADV': 'Прислівник',
   'SCONJ': 'Сполучник підрядності',
   'CCONJ': 'Сполучник сурядності',
   'ADP': 'Прийменник',
   'PART': 'Частка',
   'INTJ': 'Вигук',
   'PROPN': 'Власна назва',
   'NONE': 'Без частини мови'
}


def generate_dictionary(dir):

    for filename in os.listdir(dir):
        file_path = os.path.join(dir, filename)
        text = open(file_path, 'r')
        text_string = text.read(150000)

        # прибрати tabs і переноси на новий рядок

        def text_processing(string):
            clean_text = re.sub('\s+', ' ', string)
            return clean_text

        new_string = text_processing(text_string)
        doc = nlp(new_string)

        # лематизація
        lemmas = [
            word.lemma for sent in doc.sentences for word in sent.words if word.text.isalpha()]

        # токенізація на речення
        sent_tokens = [sent.text for sent in doc.sentences]

        # присвоєння частин мови
        pos_tags = [
            word.upos for sent in doc.sentences for word in sent.words if word.text.isalpha()]

        # токенізація на слововживання
        word_tokens = [token.text.lower(
        ) for sent in doc.sentences for token in sent.tokens if token.text.isalpha()]

        numbers = [num+1 for num, sent in enumerate(doc.sentences)
                   for token in sent.tokens if token.text.isalpha()]

        # кортежі зі списками для бази даних

        # data1 = list(zip(range(1, len(word_tokens)+1), word_tokens, numbers))

        data2 = list(zip(range(1, len(word_tokens)+1),
                     word_tokens, lemmas, pos_tags, numbers))

        conn = sqlite3.connect(f'db/{filename}.db')

        cur = conn.cursor()

        # cur.execute("""CREATE TABLE IF NOT EXISTS words(
        #    word_id INT PRIMARY KEY,
        #    word TEXT,
        #    sent_number INT);
        #    """)

        cur.execute("""CREATE TABLE IF NOT EXISTS word_info(
         word_id INT PRIMARY KEY,
         word TEXT,
         lemma TEXT,
         pos TEXT,
         sent_number INT);
         """)

        # cur.executemany("INSERT INTO words VALUES(?, ?, ?);", data1)

        cur.executemany("INSERT INTO word_info VALUES(?, ?, ?, ?, ?);", data2)

        conn.commit()

        conn.close()


def generate_freq_dict(file):


    conn = sqlite3.connect(file)
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS pos_freq (pos)')


    for k in POS_TAGS:
        sql = 'INSERT INTO pos_freq(pos) VALUES(?)'
        cur.execute(sql, (k,))


    for ind, i in enumerate(range(0, 20000, 1000)):


        cur.execute(f"ALTER TABLE pos_freq ADD COLUMN subsample{ind}")


        cur.execute(f"SELECT pos FROM word_info LIMIT 1000 OFFSET {ind}")


        pos_list = [str(row[0]) for row in cur.fetchall()]


        pos_count = [pos_list.count(pos) for pos in pos_list]


        pos_freq_dict = {pos: freq for pos, freq in zip(pos_list, pos_count)}


        for pos in pos_freq_dict.keys():
            cur.execute('SELECT * FROM word_info WHERE pos=?', (pos,))
            row = cur.fetchone()
            if row:
                cur.execute(
                    f"UPDATE pos_freq SET subsample{ind}=? WHERE pos=?", (pos_freq_dict[pos], pos))


    for ind, i in enumerate(range(0, 20000, 1000)):

        cur.execute(f"ALTER TABLE word_info ADD COLUMN subsample{ind}")

        cur.execute(f"SELECT lemma FROM word_info LIMIT 1000 OFFSET {ind}")

        word_list = [str(row[0]) for row in cur.fetchall()]

        word_count = [word_list.count(word) for word in word_list]

        word_freq_dict = {word: freq for word, freq in zip(word_list, word_count)}

        for word in word_freq_dict.keys():
            cur.execute('SELECT * FROM word_info WHERE lemma=?', (word,))
            row = cur.fetchone()
            if row:
                cur.execute(
                    f"UPDATE word_info SET subsample{ind}=? WHERE lemma=?", (word_freq_dict[word], word))




    conn.commit()


    cur.close()
    conn.close()


if __name__ == "__main__":

    generate_dictionary(DIRECTORY_PATH)

    for file in os.listdir(ABS_PATH):

        f = os.path.join(ABS_PATH, file)

        generate_freq_dict(f)
