def comp10001go_play(discard_history, player_no, hand):
    """ The Playing Strategy is to focus on building factorial only. 
    And start from Q then 9 and lower because most people would start with 
    picking K which is the highest score """
    
    # Get all the cards that I have discarded previously
    if len(hand) == 1:
        return hand[0]
    else:
        player_cards_list = []
        for cards in discard_history:
            player_cards_list.append(cards[player_no])
    
    values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 
             '0': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 20}
    
    
    # Count which round we are in
    no_round= len(discard_history)
    reverse_sort_hand= sorted(hand, reverse=True)
    sort_hand= sorted(hand)
    
    # Starting round, Get Q if available then K then subsequent one
    if no_round == 0:
        for card in reverse_sort_hand:
            if values[card[0]] <= 12:
                return card
        
        # get anything that is not 'A'
        for card in sort_hand:
            if values[card[0]] != 20:
                return card
        
        # If none of the card has either A or 10 to 2, then get the first item
        # at hand cause that hand would be lowest in value i.e 11
        return sort_hand[0]
    
    # Second Round, 
    elif no_round == 1:
        # Create a dictionary to put all the card as key and all card_value as
        # values
        player_card_dict = {}
        for cards in player_cards_list:
            player_card_dict[cards] = values[cards[0]]
        
        # Find the card in hand that matches the card in my discard history
        for card in sort_hand:
            if values[card[0]] == values[player_cards_list[0][0]]:
                return card
                
        # Get the card that has value less than or equal to 10 i.e. 10
        for card in reverse_sort_hand:
            if values[card[0]] < 10:
                return card
        
        # Get the card that is not A, i.e. J, Q, K
        for card in sort_hand:
            if values[card[0]] != 20:
                return card
    
        # Get A, if there is only A in the card
        return sort_hand[0]
    
    # Third round onwards,
    if no_round > 1:        
        # Focus on building factorial only
        
        # Figure out how much cards are in each card value
        player_cards_dict = {}
        for card in player_cards_list:
            value_card = values[card[0]]
            if value_card not in player_cards_dict.keys():
                player_cards_dict[value_card] = 1
            else:
                player_cards_dict[value_card] += 1
        
        # Check if the card on hand will lead to a card to have N-of-kind, if 
        # it will return the card
        for keys, value in player_cards_dict.items():
            for card in reverse_sort_hand:
                if values[card[0]] == keys:
                    total_value = value + values[card[0]]
                    if total_value > 2:
                        return card
                    else: 
                        player_cards_dict[keys] += 1
        
        # Once updated the dict, check again if any card lead to N-of-kind
        for keys, value in player_cards_dict.items():
            if value > 2:
                for card in reverse_sort_hand:
                    if values[card[0]] == keys:
                        return card
    
        # If none of the value, leads to N-of-kind, get any values less than 10
        for card in reverse_sort_hand:
            if values[card[0]] < 10:
                return card
        
        return sort_hand[0]

                
def comp10001go_group(discard_history, player_no):
    """ Select the grouping that achieve the maximum amount of score"""
    
    values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 
             '0': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 20}
    
    suits = {'S': True, 'C': True, 'H': False, 'D': False}
    
    player_cards_list = []
    for cards in discard_history:
            player_cards_list.append(cards[player_no])
    player_cards_list = sorted(player_cards_list, reverse=True)
    
    # First check for factorial
    # then group the singleton card and take the first 10 cards
    player_cards_dict = {}
    for card in player_cards_list:
        value_card = values[card[0]]
        if value_card not in player_cards_dict.keys():
            player_cards_dict[value_card] = [card]
        else:
            player_cards_dict[value_card].append(card) 
    
    chosen_list = []
    for keys, value in player_cards_dict.items():
        if keys != 20 and len(value) >= 2:
            chosen_list.append(value)
            for card in value:
                player_cards_list.remove(card)
                
    # BUILD FOR RUN - TESTING
    from itertools import combinations
    card_num = len(player_cards_list)
    while card_num > 2:
        for i in combinations(player_cards_list, card_num):
            print(list(i))
            valid_run = validate_run2(list(i), values, suits)
            if valid_run[0] is True:
                chosen_list.append([i])
                for card in i:
                    player_cards_list.remove(card)
                    card_num -= len(valid_run[1])
        card_num -= 1
    
    # Now build the leftover singleton card
    player_cards_list = sorted(player_cards_list)
    left_over_group = 10 - len(chosen_list)
    
    for i in player_cards_list[0: left_over_group +  1]:
        chosen_list.append([i])
    
    # Check the group is a correct group
    if comp10001go_valid_groups(chosen_list) is True:
        return chosen_list

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
    # numbers is scored as the number 
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

    
    
# ADDITIONAL TEST
# Validate Run
def validate_run2(cards, values, suits):
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
    
    # Check to make sure that it is a run when there is still ace card inside
    # return false if so
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