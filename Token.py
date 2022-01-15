# Token class represents one of the four tokens each Player
# possesses. They are assigned the same color as the Player, 
# and the same starting and ending positions. These tokens
# are controlled by the Player and can release from their
# yards, advance the board, or KO other tokens to send them 
# back to the yard.

class Token: 
  def __init__(self, color, number, start, end):
    self._token_color = color
    self._token_number = number

    self._in_yard = True
    self._in_home_column = False
    self._in_home = False

    self._spaces_passed = 0
    self._start_position = start
    self._end_position = end

    self._occupied_square = -1
    self._safe_square_numbers = 0, 8, 13, 21, 26, 34, 39, 47
    self._safe = True
    self._double = False

    self._tokens_KOd = 0
    self._been_sent_back_to_yard = 0

  # Moves the token the amount of spaces specified by the roll
  # Returns the square number the token now occupies
  def move(self, moves):
    if self._spaces_passed + moves < 51:
      self._spaces_passed += moves
      if (self._occupied_square + moves) < 52:
        self._occupied_square += moves
      else:
        spaces = self._occupied_square + moves
        self._occupied_square = spaces - 52
      self.is_safe()
      return self._occupied_square
    else:
      self._spaces_passed += moves
      if self._spaces_passed < 56:
        self._in_home_column = True
        self._occupied_square = 100 + (self._spaces_passed - 51)
        self.is_safe()
      if self._spaces_passed == 56:
        self._in_home_column = False
        self._in_home = True
        self._occupied_square = 105
        self.is_safe()
      return self._occupied_square
  
  # Returns the predicted square the token will land on without 
  # actually moving the token yet. Helps with checking
  # if token can land on that square or KO another token
  def predict(self, moves):
    if self._spaces_passed + moves < 51:
      if (self._occupied_square + moves) < 52:
        square = self._occupied_square + moves
      else:
        spaces = self._occupied_square + moves
        square = spaces - 52
      return square
    else:
      space_pass = self._spaces_passed + moves
      square = 100 + (space_pass - 51)
      return square
  
  # Prints the status of the token's location
  # and if it is safe or not
  def __str__(self):
    print_string = self._token_color + " TOKEN " + str(self._token_number + 1)
    if self._in_yard:
      print_string += ": In Yard"
    if not(self._in_yard) and (not self._in_home):
      print_string += ": On Square " + str(self._occupied_square)
      if not self._in_home_column:
        if self.is_safe():
          print_string += " (Safe)"
        else:
          print_string += " (Not Safe)"
    if self._in_home_column:
      print_string += ": In Home Column"
    if self._in_home:
      print_string += ": Home"
    return print_string


  # Returns true if the token is on a safe square
  # False if it is not
  def is_safe(self):
    if self._occupied_square in self._safe_square_numbers:
      self._safe = True
      return True;
    elif self._in_home_column or self._in_home:
      self._safe = True
      return True;
    else:
      self._safe = False
      return False;

  # Returns the square the token is occupying
  # If token is in the yard, it returns -1
  def get_square_number(self):
    return self._occupied_square
