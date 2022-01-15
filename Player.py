import Token
import random # rolling the dice

# Player is in charge of the actions of moving the tokens
# and making decisions after they roll the dice. 

class Player:
  # The constructor assigns player a color and the start and
  # end position on the annotated board. 
  def __init__(self, color, start, end, board):
    self._player_color = color
    self._start_position = start
    self._end_position = end

    # each Player gets four Tokens
    self._tokens = []
    self._tokens.append(Token.Token(color, 0, start, end)) 
    self._tokens.append(Token.Token(color, 1, start, end))
    self._tokens.append(Token.Token(color, 2, start, end))
    self._tokens.append(Token.Token(color, 3, start, end))

    self._finished_tokens = 0
    self._bonus_turn = 0
    self._the_board = board
  

  # The roll function acts as a dice. If a player rolls a six, they
  # get an extra turn. If they roll another six, they get a third turn.
  # But three sixes in a row means they have to start over. 
  def roll(self):
    dice = [1, 2, 3, 4, 5, 6]
    rolls = []
    value = random.choice(dice)
    print("PLAYER " + self._player_color + " rolls " + str(value))
    rolls.append(value)
    if value == 6:
      value = random.choice(dice)
      print("Bonus Roll! PLAYER " + self._player_color + " rolls " + str(value))
      rolls.append(value)
      if value == 6:
        value = random.choice(dice)
        print("Two Bonus Rolls! PLAYER " + self._player_color + " rolls " + str(value))
        if value == 6:
          print("Uh Oh! PLAYER " + self._player_color + " rolled three 6s in a row!")
          print("Start the rolls over!")
          return self.roll() # starts rolls over if three sixes
        else:
          rolls.append(value)
    return rolls


  # The player's turn let's the user roll the dice then move their Tokens
  # forward or release their Tokens from the yard. If they KO another Token
  # they get a bonus turn
  def turn(self):
    msg = "\nPLAYER " + self._player_color + "'s turn!"
    self.colored_text(msg)
    rolls = self.roll()
    self.display_tokens()
    while rolls:
      print("PLAYER " + self._player_color + "'s total rolls:", end = " ")
      print(rolls)
      if self.are_all_tokens_in_yard():
        rolls = self.tokens_are_all_in_yard(rolls)
      # elif self.can_player_not_move(rolls):
      #   rolls = self.player_cannot_move(rolls)
      else:
        rolls = self.select_token(rolls)
      self.display_tokens()
    if self._bonus_turn > 0:
      self._bonus_turn -= 1
      msg = "\nPLAYER " + self._player_color + " gets a bonus turn for their KO!"
      self.colored_text(msg)
      self.turn()


  # Moves the specified token the amount the user rolled.
  def move_token(self, rolls, token_number):
    if len(rolls) == 1:
      square_number = self._tokens[token_number].predict(rolls[0])
      if(square_number > 105):
        print("The Player must roll the exact amount of spaces the Token needs")
        print("to enter the home. Try selecting another token to move.")
        self.select_token(rolls)
      if not square_number in self._tokens[token_number]._safe_square_numbers:
        if self._the_board.check_token(self._tokens[token_number], square_number):
          self._bonus_turn += 1
      self._tokens[token_number].move(rolls[0])
      rolls.pop()
      return rolls
    else:
      value = int(input("Which roll do you use to move your token? "))
      if value in rolls:
        square_number = self._tokens[token_number].predict(value)
        self._the_board.check_token(self._tokens[token_number], square_number)
        square_number = self._tokens[token_number].move(value)
        rolls.remove(value)
        return rolls
      else:
        print("Try again")
        return self.move_token(rolls, token_number)


  # Releases the specified token from the yard only if the user rolled a six or a one
  def release_token(self, rolls, token_number):
    if self._tokens[token_number]._in_yard:
      if (1 in rolls) and (6 in rolls):
        value = int(input("Which roll do you use to release your token? 1 or 6? "))
        if value == 1:
          rolls.remove(1)
          self._tokens[token_number]._in_yard = False
          self._tokens[token_number]._occupied_square = self._tokens[token_number]._start_position
        elif value == 6:
          rolls.remove(6)
          self._tokens[token_number]._in_yard = False
          self._tokens[token_number]._occupied_square = self._tokens[token_number]._start_position
        else:
          print("Try again")
          return self.release_token(rolls)
      elif 1 in rolls:
        rolls.remove(1)
        self._tokens[token_number]._in_yard = False
        self._tokens[token_number]._occupied_square = self._tokens[token_number]._start_position
      elif 6 in rolls:
        rolls.remove(6)
        self._tokens[token_number]._in_yard = False
        self._tokens[token_number]._occupied_square = self._tokens[token_number]._start_position
    return rolls
  

  # Displays the status of the tokens and their locations
  def display_tokens(self):
    for x in range(len(self._tokens)):
      self.colored_text(self._tokens[x])


  # Checks if user is moving the token or releasing the token from yard
  def select_token(self, rolls):
    token_number = self.token_input() - 1
    if token_number == -1: # debugging, skips turn when entering 0
      return self.skip_turn(rolls)
    if self._tokens[token_number]._in_yard:
      if (1 in rolls) or (6 in rolls):
        return self.release_token(rolls, token_number)
      else:
        print("You can't move that token outside without rolling 1 or 6")
        print("Try again")
        return self.select_token(rolls)
    else:
      return self.move_token(rolls, token_number)
    return rolls
  
  def skip_turn(self, rolls):
    while rolls:
      rolls.pop()
    return rolls

  # Boolean to check if all tokens are in yard or home
  def are_all_tokens_in_yard(self):
    all_tokens_in_yard = True
    for x in range(len(self._tokens)):
      if not self._tokens[x]._in_yard:
        if not self._tokens[x]._in_home:
          all_tokens_in_yard = False
    return all_tokens_in_yard
  
  def is_there_a_token_in_yard(self):
    token_in_yard = False
    for x in range(len(self._tokens)):
      if self._tokens[x]._in_yard:
        token_in_yard = True
    return token_in_yard

  # Called when all tokens are in yard
  def tokens_are_all_in_yard(self, rolls):
    if (6 in rolls) or (1 in rolls):
      token_number = self.token_input() - 1
      return self.release_token(rolls, token_number)
    else:
      print("All tokens in yard or home, can't move.")
      print("Try rolling a six or one next turn to")
      print("release a token.")
      rolls.pop()
      return rolls


  # Takes in user's input to select which token they will use. 
  # User should input a number from 1 to 4, otherwise they must
  # try again.
  def token_input(self):
    token_number = int(input("Select Which Token to Move: "))
    if(token_number == 0): # debugging 
      return 0
    if (token_number < 5) and (token_number > 0):
      if not self._tokens[token_number - 1]._in_home:
        return token_number
      else:
        print("That Token is home, it can't move. Try again")
        return self.token_input()
    else:
      print("That's not a valid Token. Try again")
      return self.token_input()


  # cited source: https://www.geeksforgeeks.org/print-colors-python-terminal/
  def colored_text(self, message):
    if(self._player_color == "RED"):
      print("\033[91m {}\033[00m" .format(message))
    elif(self._player_color == "BLUE"):
      print("\033[96m {}\033[00m" .format(message))
    elif(self._player_color == "GREEN"):
      print("\033[92m {}\033[00m" .format(message))
    else:
      print("\033[93m {}\033[00m" .format(message))

  # def can_player_not_move(self, rolls):
  #   if (self.is_there_a_token_in_yard()) and ((1 in rolls) or (6 in rolls)):
  #     return False
    

  # def player_cannot_move(self, rolls):
  #   return rolls

 

  

  