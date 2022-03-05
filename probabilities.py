def game_probability(p):
  return p**4 + 4*(p**4)*(1-p) + 10*(p**4)*(1-p)**2 + (20*(p**5)*(1-p)**3)/(1 - 2*p*(1-p))

def tie_break_probability(p):
  return (p**7)*(1 + 7*(1-p) + 28*(1-p)**2 + 84*(1-p)**3 + 210*(1-p)**4 + 462*(1-p)**5) + 924*(p**6)*((1-p)**6)*((p**2)/(1-((2*p) * (1-p))))

def set_probability(p):
  w = game_probability(p)
  t = tie_break_probability(p)
  return (w**6)*(1 + 6*(1-w) + 21*(1-w)**2 + 56*(1-w)**3 + 126*(1-w)**4 + 252*w*(1-w)**5 + 504*((1-w)**6)*t)

def match_probability(p):
  s = set_probability(p)
  return (s**3)*(1 + 3*(1-s) + 6*(1-s)**2)

def win_game(p):
  return game_probability(p)

def win_set(p):
  return set_probability(p)

def win_match(p):
  return match_probability(p)