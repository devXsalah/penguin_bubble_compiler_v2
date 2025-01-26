# compiler/tokens.py

class TokenType:
    # Existing tokens...
    PENGUIN_SAY = "penguinSay"
    PENGUIN_TAKE = "penguinTake"
    KEEP_WALKING = "keepWalking"
    PENGUIN_IF = "penguinIf"
    PENGUIN_WHAT_ABOUT = "penguinWhatAbout"
    PENGUIN_ELSE = "penguinElse"
    PENGUIN_DO = "penguinDo"
    RETURN_ICE = "returnIce"
    
    # Operators
    SLIDE_UP = "slideUp"                   
    SLIDE_DOWN = "slideDown"               
    PENGUIN_BOOST = "penguinBoost"         
    GIVE_PENGUINS = "givePenguins"         
    SNOWBALL = "snowball"                  
    PENGUIN_BREAK = "penguinBreak"         # To handle 'break' statements
