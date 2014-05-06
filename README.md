Implemented a simple Blackjack game in python.

Here is my BlackJack rule:

    1. If you win with a BlackJack, bet payout is 3:2.
    2. You can surrender but half bet will be taken.
    3. You can select DoubleDown, only 1 more card will be hit, and
    bet will be doubled.
    4. Once Split, Re-split or Doubledown or Surrender is NOT allowed. 
    5. ACE by default is 11. If your 1st 2 cards are ACEs, your point
    is 12. If you choose Hit, and your point becomes > 21, then any
    ACE could be reduced to 1 so that your point is less than but close
    to 21.
    6. Dealer must hit if his point is < 17 (even if his point might >
    yours) and must stand if it is >= 17.
