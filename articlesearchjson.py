fin = open('\database\raw_data.txt')

def get_a_article():
    line = fin.readline()
    article = line.strip()
    return article

def get_articles(article):
    num_of_v = 0
    for i in range(len(article)):
        if word[i] == 'a' or 'e' or 'i' or 'o' or 'u' or 'y' and not 'w':
            num_of_v = num_of_v + 1
            if num_of_v == 10:
                return True else:
                return False