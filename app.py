import utils

# ? многолосвные, многосимвольные названия ?

if __name__ == "__main__":
    with open(file="./data/requirements.txt") as f:
        # for line in f:
        #     meds = utils.get_medications_list_from_text(text=line, smartness=1)

        #     if len(meds) > 0:
        #         print(line.strip())
        #         print(meds)
        #         print()
        test = "Мне нужно лекарство ДЕКСОМЕТАЗОН В АМПУЛАХ И ЭДНИТ В ТАБЛЕТКАХ"
        meds = utils.get_medications_list_from_text(text=test, smartness=1)

    # прочитать из stdin с параметрами
    # сделать магию
    # вывести в stdin
