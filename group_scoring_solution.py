# Sample Solution 1

from math import factorial


# index of value of a card
VALUE = 0

# index of suit of a card
SUIT = 1

# value of Ace
ACE = 'A'

# dictionary of scores of individual cards
card_score = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '0': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    ACE: 20,
    }
    
# suits which are red
RED_SUITS = 'HD'

# suits which are black
BLACK_SUITS = 'SC'

# card colours
RED = 1
BLACK = 2

# minimum no. of cards in an n-of-a-kind set
MIN_CARDS_NKIND = 2

# minimum no. of non-Ace cards in a run
MIN_NONACE_RUN = 2

# minimum no. cards in a run
MIN_RUN = 3



def is_ace(card):
    """Boolean evaluation of whether `card` is an Ace"""
    return card[VALUE] == ACE


def get_score(card):
    """return the score of `card`, based on its value"""
    return card_score[card[VALUE]]


def get_colour(card):
    """Return the colour of `card` (`RED` or `BLACK`)"""
    if card[SUIT] in RED_SUITS:
        return RED
    else:
        return BLACK


def comp10001go_score_group(cards):
    """Validate/score a group of cards (order unimportant), supplied as a 
    list of cards (each a string); return the positive score of the group if 
    valid, and negative score otherwise. Note, assumes that all cards are 
    valid, and unique."""

    # construct sorted list of values of cards (ignore suit for now)
    values = sorted([get_score(card) for card in cards])

    # CASE 1: N-of-a-kind if all cards of same value, at least
    # `MIN_CARDS_NKIND` cards in total, and not Aces
    if (len(set(values)) == 1 and len(cards) >= MIN_CARDS_NKIND
        and not is_ace(cards[0])):
        return factorial(len(cards)) * card_score[cards[0][VALUE]]

    # construct sorted list of non-Ace cards
    nonace_cards = sorted([card for card in cards if not is_ace(card)],
                          key=lambda x: get_score(x))

    # construct list of Ace cards
    ace_cards = list(set(cards) - set(nonace_cards))

    # run must have at least `MIN_NONACE_RUN` non-Ace cards in it
    if len(nonace_cards) >= MIN_NONACE_RUN:

        is_run = True
        prev_val = prev_colour = None
        score = 0

        # iterate through cards to make sure they form a run
        for card in nonace_cards:

            # CASE 1: for the first card in `nonace_cards`, nothing to
            # check for
            if prev_val is None:
                score = prev_val = get_score(card)
                prev_colour = get_colour(card)

            # CASE 2: adjacent to previous card in value
            elif get_score(card) - prev_val == 1:

                # CASE 2.1: alternating colour, meaning continuation of run
                if get_colour(card) != prev_colour:
                    prev_val = get_score(card)
                    prev_colour = get_colour(card)
                    score += prev_val
                # CASE 2.2: not alternating colour, meaning invalid run
                else:
                    is_run = False
                    break

            # CASE 3: repeat value, meaning no possibility of valid run
            elif get_score(card) == prev_val:
                is_run = False
                break

            # CASE 4: gap in values, in which case check to see if can be
            # filled with Ace(s)
            else:
                gap = get_score(card) - prev_val - 1
                
                gap_filled = False
                # continue until gap filled
                while is_run and gap and len(ace_cards) >= gap:

                    gap_filled = False
                
                    # search for an Ace of appropriate colour, and remove
                    # from list of Aces if found (note that it doesn't matter
                    # which Ace is used if multiple Aces of same colour)
                    for i, ace in enumerate(ace_cards):
                        if get_colour(ace) != prev_colour:
                            ace_cards.pop(i)
                            prev_val += 1
                            prev_colour = get_colour(ace)
                            score += prev_val
                            gap -= 1
                            gap_filled = True
                            break

                    if not gap_filled:
                        is_run = False

                if is_run and gap_filled and get_colour(card) != prev_colour:
                    prev_val = get_score(card)
                    prev_colour = get_colour(card)
                    score += prev_val
                else:
                    is_run = False

        if is_run and len(cards) >= MIN_RUN and not ace_cards:
            return score

    return -sum(values)

# Sample Solution 2

from sushi_go import (
    Card,
    construct_n_of_a_kind, construct_run,
    score_n_of_a_kind, score_orphans, score_run,
)


def comp10001go_score_group(card_strings):
  # Convert the card strings to Card objects.
  cards = list(map(Card, card_strings))

  # Are the cards n-of-a-kind? If so, score appropriately.
  grouped_cards = construct_n_of_a_kind(cards)
  if grouped_cards is not None:
    return score_n_of_a_kind(grouped_cards)

  # Are the cards a run? If so, score appropriately.
  grouped_cards = construct_run(cards)
  if grouped_cards is not None:
    return score_run(grouped_cards)

  # Otherwise, the cards must be orphans. Score appropriately.
  return score_orphans(cards)


# GO To sushi_go.py

import math

SUIT_TO_COLOUR = dict(zip('HDCS', 'RRBB'))
VALUE_STRING_TO_VALUE = dict(zip('A234567890JQK', range(1, 14)))
VALUE_TO_VALUE_STRING = {v: k for k, v in VALUE_STRING_TO_VALUE.items()}


class Card:
  def __init__(self, card_string):
    if isinstance(card_string, tuple):
      card_string = VALUE_TO_VALUE_STRING[card_string[0]] + card_string[1]
    self.value_str = card_string[0]
    self.value = VALUE_STRING_TO_VALUE[self.value_str]
    self.suit = card_string[1]
    self.colour = SUIT_TO_COLOUR[self.suit]
    self.inv_colour = 'R' if self.colour == 'B' else 'B'
    self.orphan_value = -20 if self.is_ace() else -self.value

  def __eq__(self, other):
    return self.value_str == other.value_str and self.suit == other.suit

  def __repr__(self):
    return f'Card(\'{self.value_str}{self.suit}\')'

  def __str__(self):
    return f'{self.value_str}{self.suit}'

  def is_ace(self):
    return self.value_str == 'A'

  def is_black(self):
    return self.colour == 'B'

  def is_king(self):
    return self.value_str == 'K'

  def is_red(self):
    return self.colour == 'R'


def construct_n_of_a_kind(cards):
  # Early bail if we don't have enough cards.
  if len(cards) < 2:
    return None

  # Ensure that all of the cards have the same value and are not an Ace.
  value = None
  for card in cards:
    if card.is_ace():
      return None
    elif value is None:
      value = card.value
    elif card.value != value:
      return None

  # Return the cards as is.
  return list(cards)


def construct_run(cards):
  # Early bail if we don't have enough cards.
  if len(cards) < 3:
    return None

  # Partition the cards into Aces and non-Aces.
  non_aces = []
  aces_by_colour = {'B': [], 'R': []}
  for card in cards:
    if card.is_ace():
      aces_by_colour[card.colour].append(card)
    else:
      non_aces.append(card)

  # Ensure we have enough non-Aces.
  if len(non_aces) < 2:
    return None

  # Sort the non-Aces by value.
  non_aces.sort(key=lambda card: card.value)

  # Attempt to construct a valid run from the avaialble cards.
  prev = non_aces.pop(0)
  run = [prev]
  while non_aces:
    top = non_aces[0]

    # Check for a normal valid transition.
    if prev.value + 1 == top.value and prev.colour == top.inv_colour:
      run.append(non_aces.pop(0))  # Consume the current card in the run.
      prev = top
    else:
      # Check if we can do an Ace insertion.
      aces = aces_by_colour[prev.inv_colour]
      if aces and not prev.is_king():  # Can't go higher than a King for Ace insertion.
        ace = aces.pop(0)  # Consume the next Ace.
        run.append(ace)
        prev = Card((prev.value + 1, ace.suit))
      else:
        # We did not find a valid transition.
        return None

  # If we have any aces left over, we do not have a valid run.
  if aces_by_colour['B'] or aces_by_colour['R']:
    return None

  return run


def score_n_of_a_kind(cards):
  return cards[0].value * math.factorial(len(cards))


def score_orphans(cards):
  return sum(map(lambda card: card.orphan_value, cards))


def score_run(cards):
  return sum(range(cards[0].value, cards[-1].value + 1))