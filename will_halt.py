import random

# =====================================
# Utility Functions
# =====================================

def create_deck():
    ranks = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
    deck = ranks * 4
    random.shuffle(deck)
    return deck

def card_value(card):
    if card in ['J','Q','K']:
        return 10
    if card == 'A':
        return 11
    return int(card)

def hand_value(hand):
    total = sum(card_value(c) for c in hand)
    aces = hand.count('A')
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    return total

def is_bust(hand):
    return hand_value(hand) > 21

# =====================================
# Expectimax Player AI
# =====================================

def expected_outcome(player_hand, dealer_hand, deck, depth=3):
    """
    Expected value from player's perspective:
        +1 → player wins
        -1 → player loses
         0 → tie
    """
    if depth == 0 or is_bust(player_hand) or is_bust(dealer_hand):
        return terminal_value(player_hand, dealer_hand)

    # Player turn: choose Hit or Stand
    hit_value = expected_hit(player_hand, dealer_hand, deck, depth)
    stand_value = expected_stand(player_hand, dealer_hand, deck, depth)

    return max(hit_value, stand_value)

def terminal_value(player_hand, dealer_hand):
    """Evaluate final result."""
    pv, dv = hand_value(player_hand), hand_value(dealer_hand)

    if pv > 21:
        return -1
    if dv > 21:
        return +1
    if pv > dv:
        return +1
    if pv < dv:
        return -1
    return 0

def expected_stand(player_hand, dealer_hand, deck, depth):
    """Player stands, simulate dealer until finish."""
    dealer_copy = dealer_hand[:]
    deck_copy = deck[:]

    # Dealer hits until 17
    while hand_value(dealer_copy) < 17:
        if len(deck_copy) == 0:
            break
        dealer_copy.append(deck_copy.pop())

    return terminal_value(player_hand, dealer_copy)

def expected_hit(player_hand, dealer_hand, deck, depth):
    """Player hits: random card is drawn from deck."""
    if len(deck) == 0:
        return terminal_value(player_hand, dealer_hand)

    total = 0
    unique = {}
    for c in deck:
        unique[c] = unique.get(c, 0) + 1

    for card, count in unique.items():
        prob = count / len(deck)
        new_deck = deck[:]
        new_deck.remove(card)
        new_player = player_hand + [card]

        total += prob * expected_outcome(new_player, dealer_hand, new_deck, depth-1)

    return total

def ai_should_hit(player_hand, dealer_hand, deck):
    """Return True if AI believes HIT has better expected value."""
    hit_val = expected_hit(player_hand, dealer_hand, deck, depth=3)
    stand_val = expected_stand(player_hand, dealer_hand, deck, depth=3)
    return hit_val > stand_val

# =====================================
# Game Logic
# =====================================

def dealer_play(dealer, deck):
    """Dealer hits until 17."""
    while hand_value(dealer) < 17:
        dealer.append(deck.pop())
    return dealer

def blackjack_game(ai_player=False):
    deck = create_deck()
    player = [deck.pop(), deck.pop()]
    dealer = [deck.pop(), deck.pop()]

    print("\nDEALER shows:", dealer[0])
    print("PLAYER starting hand:", player, "→", hand_value(player))

    # =========================
    # Player Phase
    # =========================
    while True:
        if is_bust(player):
            print("PLAYER busts! Dealer wins.")
            return

        if ai_player:
            action = "h" if ai_should_hit(player, dealer, deck) else "s"
            print(f"AI chooses to {'HIT' if action=='h' else 'STAND'}")
        else:
            action = input("Hit or Stand? (h/s): ").lower()

        if action == "h":
            player.append(deck.pop())
            print("PLAYER draws:", player[-1], "→", hand_value(player))
        else:
            break

    # =========================
    # Dealer Phase
    # =========================
    print("\nDealer reveals hand:", dealer, "→", hand_value(dealer))
    dealer = dealer_play(dealer, deck)
    print("Dealer final hand:", dealer, "→", hand_value(dealer))

    # =========================
    # Final Scoring
    # =========================
    pv, dv = hand_value(player), hand_value(dealer)

    print("\nRESULT:")
    if pv > 21:
        print("Player busts → Dealer Wins.")
    elif dv > 21:
        print("Dealer busts → Player Wins!")
    elif pv > dv:
        print("Player Wins!")
    elif pv < dv:
        print("Dealer Wins.")
    else:
        print("Push (tie).")

# =====================================
# Run Game
# =====================================

if __name__ == "__main__":
    mode = input("Play manually or AI player? (m/ai): ").lower()
    blackjack_game(ai_player=(mode == "ai"))
