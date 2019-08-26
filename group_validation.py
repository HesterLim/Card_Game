def comp10001go_valid_groups(groups):
    """ Take a single argument, groups, a list of groups, which is a list of
    cards. Return a Boolean indicating whether all groups are valid or not"""
    
    if len(groups) == 0:
        return True
    else:
        for cards in groups:
            if comp10001go_score_group(cards) < 0:
                return False
    return True
        

def comp10001go_score_group(cards):
    """ Take a list of cards, each has a 2-element string, where the 1st letter
    is card value and 2nd letter is card suit. 
    Then, return the integer score for the GROUP. """
    
    # Put int a dictionary for each card which is scored based on its value
    # For example, J is 11, Q is 12 and K is 13, Ace is 20
    
    values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 
             '0': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 20}
    
    # Spades and Clubs are black, Hearts and Diamonds are red
    suits = {'S': True, 'C': True, 'H': False, 'D': False}
    
    # First, find if the group is a valid N-of-a-kind (i.e there are 2 or more
    # cards of the same non_Ace value), the score is that value multiplied 
    # by N facorial
    
    # Check if the group is valid for N-of-a-kind
    if validate_n_of_kind(cards, values) is True:
        # Calculate the score for the group with valid N-of-a-kind
        n = len(cards)
        card_value = values[cards[0][0]]
        score =  card_value * factorial(n)
        return score
    
    # Check if the group is a valid run
    valid_run = validate_run(cards, values, suits)
    if valid_run[0] is True:
        sort_card = valid_run[1]
        score = 0
        for card in sort_card:
            score += card[0]
        return score
    
    # If the group is a singleton card or doesn't form a valid N-of-a-kind or 
    # run, it should be scored as the negative sum of the scores of the 
    # individual cards (scoring Aces as 20)
    else:
        if len(cards) == 1:
            return 1
        else: 
            sort_card = []
            for card_num in range(len(cards)):
                value_card = values[cards[card_num][0]]
                suit_card = suits[cards[card_num][1]]
                sort_card.append((value_card, suit_card))
        
            score = 0
            for card in sort_card:
                score += (-card[0])
            return score  
          
# Validate n_of_kind
def validate_n_of_kind(cards, values):
    n_of_kind = {}
    for one_card in cards:
        one_card_value = one_card[0]
    # Check the group if there is no Ace in the group
        if 'A' in one_card:
            return False, []
    # Check the group if it has 2 or more cards that are the same
        if one_card_value not in n_of_kind.keys():
            n_of_kind[one_card_value] = 1
        else:
            n_of_kind[one_card_value] += 1
            
    for value, count in n_of_kind.items():
        if count >= 2:
            pass
        else: 
            return False, []
    return True    

# Validate Run
def validate_run(cards, values, suits):
    # Check if the set of cards has 3 or more cards:
    if len(cards) < 3:
        return False, []
        
    cards = sorted(cards)
    # Create a new list of tuples of values and boolean
    sort_card = []
    for card_num in range(len(cards)):
        value_card = values[cards[card_num][0]]
        suit_card = suits[cards[card_num][1]]
        sort_card.append((value_card, suit_card))
    sort_card = sorted(sort_card)
    
    # Build an ace_card_list
    ace_cards = []
    non_ace_cards = []
    for card_num in range(len(sort_card)):
        if sort_card[card_num][0] == 20:
            ace_cards.append(sort_card[card_num])
        else:
            non_ace_cards.append(sort_card[card_num])

    # Check to make sure that it is a run even without needing to use
    # ace card
    len_run = 1
    for count_card in range(len(non_ace_cards) - 1):
        current_card_value = non_ace_cards[count_card][0]
        next_card_value = non_ace_cards[count_card + 1][0]
        next_curr_value = current_card_value + 1
        if next_card_value != next_curr_value:
            break
        elif next_card_value == next_curr_value:
            len_run += 1

    if len_run == len(non_ace_cards) and len(ace_cards) != 0:
        return False, []
            
    # Check if sort_card_list is a run if it is not a run, insert one Ace_card
    card_num = 0
    while len(ace_cards) != 0:
        current_card_value = non_ace_cards[card_num][0]
        next_card_value = non_ace_cards[card_num + 1][0]
        next_curr_value = current_card_value + 1
        if next_card_value != next_curr_value:
            ace_card_insert = (next_curr_value, ace_cards[0][1])
            non_ace_cards.insert(card_num + 1, ace_card_insert)
            ace_cards.remove(ace_cards[0])
        elif card_num == len(non_ace_cards):
            for ace_card in ace_cards:
                non_ace_cards.insert(len(sort_card), ace_card)
            ace_cards = []
        elif next_card_value == next_curr_value and len(non_ace_cards) == 2:
            length_non_ace_cards = len(non_ace_cards)
            for ace_card in ace_cards:
                non_ace_cards.insert(length_non_ace_cards, ace_card)
                length_non_ace_cards += 1
            ace_cards = []
        card_num += 1
    sort_card = non_ace_cards
 
    # Check the list so that the first location and 
    # final location does not contain ace card
    final_sort_card = sort_card[len(sort_card) - 1]
    if final_sort_card[0] == 20:
        return False, []
    
    # Check if it has a continous sequence:
    for card_num in range(1, len(sort_card)):
        current_card_value = sort_card[card_num - 1][0]
        next_card_value = sort_card[card_num][0]
        if current_card_value + 1 != next_card_value:
            return False, []
    
    # Check if it is forming a continous sequence in terms of value and 
    # alternating value and alternating in colour; 
    # not that Aces can act as wilds in terms of value
    for card_num in range(1, len(sort_card)):
        current_card_suit = sort_card[card_num - 1][1]
        next_card_suit = sort_card[card_num][1]
        if current_card_suit == next_card_suit:
            return False, []
    return (True, sort_card)

def factorial(num):
    """ Calculatte the factorial of a positive integer num
        Assumption : num is not less than or equal to 0"""
    if num == 1:
        return num
    else:
        return num * factorial(num - 1)