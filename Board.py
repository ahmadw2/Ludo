import Player # Players for each yard
import time

# The Board class represents the ludo board, shown in the
# LudoBoard.png where the tokens will advance. The Board is where
# the gameplay takes place. 

class Board:
  # The constructor creates four players, assigning them each a color. 
  def __init__(self):
    self._players = []
    self._players.append(Player.Player("RED", 0, 51, self))
    self._players.append(Player.Player("BLUE", 13, 12, self))
    self._players.append(Player.Player("YELLOW", 26, 25, self))
    self._players.append(Player.Player("GREEN", 39, 38, self))

    self._safe_square_numbers = 0, 8, 13, 21, 26, 34, 39, 47
    self._rounds = 1
  

  # Prints the starting message and begins the game
  def start(self):
    print("\nWelcome to Ludo!")
    print("\nThe goal is to have all four of your tokens")
    print("reach home before the other players!")
    print("\nAll the tokens start in their yards, try") 
    print("rolling six or one to get a token out!")
    print("\nLet's start rolling!")
    self.play()


  # Loops until all player's tokens are home. Loops four times 
  # inside the while loop to give each player a turn.
  def play(self):
    while not self.all_tokens_home():
      print("\n----------- ROUND " + str(self._rounds) + " -----------")
      for x in range(4):
        time.sleep(0.5)
        self._players[x].turn()
      self._rounds += 1
    self.print_results()
    

  # Called inside the Player class to check if other tokens are on
  # the path.
  def check_token(self, current_token, square_number):
    # self.check_for_doubles_in_path(current_token, square_number)
    return self.token_on_square(current_token, square_number)


  # Checks if all tokens are home, returns false if they are not
  def all_tokens_home(self):
    tokens_all_home = True
    for y in range(4):
      player = self._players[y]
      for x in range(4):
        token = player._tokens[x]
        if not token._in_home:
          tokens_all_home = False
    return tokens_all_home


  def print_results(self):
    print("FINAL RESULTS:")
    # for y in range(4):
    #   player = self._players[y]
  
  # def check_for_doubles_in_path(self, current_token, square_number):
  #   current_square = current_token._occupied_square
  #   for y in range(4):
  #     player = self._players[y]
  #     for x in range(4):
  #       token = player._tokens[x]
  #        sqr_num = token.get_square_number()
  #        if sqr_num == square_number:
  #          if token._token_color == current_token._token_color:
  #            current_token._double = True
  #            token._double = True
  #         else:

  # Checks if there's any tokens to send back to the yard
  def token_on_square(self, current_token, square_number):
    if square_number < 100:
      for y in range(4):
        player = self._players[y]
        for x in range(4):
          token = player._tokens[x]
          sqr_num = token.get_square_number()
          if sqr_num == square_number:
            if not token._token_color == current_token._token_color:
              self.print_KO(current_token, token, square_number)
              token._occupied_square = -1
              token._in_yard = True
              token._spaces_passed = 0
              token._safe = True
              return True
    return False

  # The colored print statement when current token sends home the token
  # that it landed on 
  def print_KO(self, current_token, KOd_token, square_number):
    print("")
    current_token._tokens_KOd += 1
    KOd_token._been_sent_back_to_yard += 1
    msg1 = current_token._token_color + " TOKEN " + str(current_token._token_number + 1)
    msg1 += " lands on Square " + str(square_number) + "!"
    self.colored_text(current_token, msg1)
    msg2 = KOd_token._token_color + " TOKEN " + str(KOd_token._token_number + 1) 
    msg2 += " is sent back to the yard!"
    self.colored_text(KOd_token, msg2)
    print("")

  
  # cited source: https://www.geeksforgeeks.org/print-colors-python-terminal/
  # prints the message in the color of the token to the terminal
  def colored_text(self, token, message):
    if(token._token_color == "RED"):
      print("\033[91m {}\033[00m" .format(message))
    elif(token._token_color == "BLUE"):
      print("\033[96m {}\033[00m" .format(message))
    elif(token._token_color == "GREEN"):
      print("\033[92m {}\033[00m" .format(message))
    else:
      print("\033[93m {}\033[00m" .format(message))

b = Board()
b.start()

