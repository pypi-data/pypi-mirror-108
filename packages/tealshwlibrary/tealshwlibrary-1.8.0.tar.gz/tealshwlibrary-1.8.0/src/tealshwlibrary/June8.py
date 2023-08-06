import random

class June8:
    # Name : Happy Birthday
    # Purpose : print happy birthday
    # Arguments : name
    # Output : None
    def happy_birthday(name):
        print('Happy Birthday to you!')
        print('Happy Birthday to you!')
        print(f'Happy Birthday dear {name}')
        print('Happy Birthday to you!')
    
    def pick_cards(count, *argv):
        cards = []
        for x in range(count):
            tmp = []
            for y in argv:
                tmp.append(random.choice(y))
            cards.append(tmp)
        return cards