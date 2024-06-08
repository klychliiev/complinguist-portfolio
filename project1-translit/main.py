input_text = list(input('Введіть текст українською мовою: '))

def transliterate(input_string):

    uk_sw_dict = {
    'а':'a', 'б':'b', 'в':'v', 'г':'h', 'д':'d', 'е':'e', 'ж':'zj',
    'з':'z', 'и':'y', 'й':'j', 'к':'k', 'л':'l', 'м':'m', 'н':'n',
    'о':'o', 'п':'p', 'р':'r', 'с':'s', 'т':'t', 'у':'u', 'ф':'f',
    'х':'ch', 'ц':'ts', 'ч':'tj', 'ш':'sj', 'щ':'sjtj', 'ь':'',
    'ю':['ju', 'iu', 'u'], 'я':['ja', 'ia', 'a'], 'є':'je', 'ґ':'g',
    'і':'i', 'ї':'ji', ' ': ' ', "'":"", 'ʼ':'', '’':'',
    'А':'A', 'Б':'B', 'В':'V', 'Г':'H', 'Д':'D', 'Е':'E', 'Ж':'ZJ',
    'З':'Z', 'И':'Y', 'Й':'J', 'К':'K', 'Л':'L', 'М':'M', 'Н':'N',
    'О':'O', 'П':'P', 'Р':'R', 'С':'S', 'Т':'T', 'У':'U',
    'Ф':'F','Х':'CH', 'Ц':'TS', 'Ч':'TJ', 'Ш':'SJ', 'Щ':'SJTJ', 'Ь':'',
    'Ю':['JU', 'IU', 'U'], 'Я':['JA', 'IA', 'A'], 'Є':'JE', 'Ґ':'G',
    'І':'I', 'Ї':'JI'
    }

    transliterated = ''

    for count, letter in enumerate(input_text):
        if letter=='я':
            if input_text[count - 1] == 'ч' or input_text[count - 1] =='ш' or input_text[count - 1] == 'щ' or input_text[count - 1] == 'ж':
                transliterated += uk_sw_dict['я'][2]
            elif input_text[count - 1] == 'Ч' or input_text[count - 1] == 'Ш' or input_text[count - 1] == 'Щ' or input_text[count - 1] == 'Ж':
                transliterated += uk_sw_dict['я'][2]
            elif input_text[count - 1] == 'з' or input_text[count - 1] == 'с' or input_text[count - 1] == 'т' or input_text[count - 1] == 'ц':
                transliterated += uk_sw_dict['я'][1]
            elif input_text[count - 1] == 'З' or input_text[count - 1] == 'С' or input_text[count - 1] == 'Т' or input_text[count - 1] == 'Ц':
                transliterated += uk_sw_dict['я'][1]
            else:
                transliterated += uk_sw_dict['я'][0]

        elif letter=='ю':
            if input_text[count - 1] == 'ч' or input_text[count - 1] == 'ш' or input_text[count - 1] == 'щ' or input_text[count - 1] == 'ж':
                transliterated += uk_sw_dict['ю'][2]
            elif input_text[count - 1] == 'Ч' or input_text[count - 1] == 'Ш' or input_text[count - 1] == 'Щ' or input_text[count - 1] == 'Ж':
                transliterated += uk_sw_dict['ю'][2]
            elif input_text[count - 1] == 'з' or input_text[count - 1] == 'с' or input_text[count - 1] == 'т' or input_text[count - 1] == 'ц':
                transliterated += uk_sw_dict['ю'][1]
            elif input_text[count - 1] == 'З' or input_text[count - 1] == 'С' or input_text[count - 1] == 'Т' or input_text[count - 1] == 'Ц':
                transliterated += uk_sw_dict['ю'][1]
            else:
                transliterated += uk_sw_dict['ю'][0]

        elif letter in uk_sw_dict:
            transliterated += uk_sw_dict[letter]
        else:
            transliterated += letter
            
        print(f"\nТранслітерація шведською: {transliterated}")
        
transliterate(input_text)
