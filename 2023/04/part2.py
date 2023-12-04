import re

cards = {}  # copies and originals

with open('input.txt', 'r') as fp:
    # each line is an original card
    for line in fp:
        # trying hard to do all-regex parsing - no split or strip!
        card_number, row = re.match('(?:Card\s+)([0-9]+):(.*)', line).groups()
        card_number = int(card_number)
        winners, numbers = re.match('(.*)\|(.*)', row).groups()
        winners = list(map(int, re.findall('([0-9]+)', winners)))
        numbers = list(map(int, re.findall('([0-9]+)', numbers)))

        # add this original card to the total
        if card_number not in cards:
            cards[card_number] = 0
        cards[card_number] += 1

        # add copies of future cards, and do so for all instances of the current card
        n_matches = sum([(n in winners) for n in numbers])
        for n in range(cards[card_number]):
            for i in range(n_matches):
                target = card_number + i + 1
                if not target in cards:
                    cards[target] = 0
                cards[target] += 1

result = sum(cards.values())
assert result == 8570000
print(result)
