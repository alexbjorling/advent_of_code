import re

class Hand(object):
    def __init__(self, cards):
        assert len(cards) == 5
        self.cards = str(cards)
        self.type = self.get_type()

    def get_type(self):
        unique = set(self.cards)  # the unique cards we have
        occurrences = sorted([self.cards.count(u) for u in unique], reverse=True)  # the occurrence of the most common, second most common, etc, card
        if len(unique) == 1:
            return 7  ## five of a kind
        elif len(unique) == 2 and occurrences[0] == 4:
            return 6  ## four of a kind
        elif len(unique) == 2 and occurrences[0] == 3:
            return 5  ## full house
        elif len(unique) == 3 and occurrences[0] == 3:
            return 4  ## three of a kind
        elif len(unique) == 3 and occurrences[0] == occurrences[1] == 2:
            return 3  ## two pair
        elif len(unique) == 4 and occurrences[0] == 2:
            return 2  ## one pair
        elif len(unique) == 5:
            return 1  ## high card
        else:
            raise ValueError('Not supposed to get here (%s)!' % cards)

    def __gt__(self, other):
        if self.type == other.type:
            val_map = {char:val for (val, char) in enumerate('23456789TJQKA')}
            for ours, theirs in zip(self.cards, other.cards):
                if val_map[ours] == val_map[theirs]:
                    continue
                return val_map[ours] > val_map[theirs]
        return self.type > other.type

# parse
hands = []
with open('input.txt', 'r') as fp:
    for line in fp:
        cards, bid = re.match('^(.{5})\s(\d+)\n', line).groups()
        hands.append([Hand(cards), int(bid)])

# sort and add up
total = 0
hands = sorted(hands, key=lambda x: x[0])  # falling order
for i, row in enumerate(hands):
    total += (i + 1) * row[1]

assert total == 253205868
