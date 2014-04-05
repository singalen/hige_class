__author__ = 'Romanzi (Roman Sytnik)'

def read_inflation_file():
    inf_dict = {}
    fh = open("data/pcpi_a.csv", 'r+', encoding='utf8')
    while True:
        inf_data = fh.readline()
        if not inf_data:
            break
        inf_list = inf_data.split(',')
        inf_dict[inf_list[3]] = inf_list[25]
    fh.close()
    print(inf_dict["UKRAINE"])
    return inf_dict


read_inflation_file()
