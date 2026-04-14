
# In this assignment, you will create a text-based adventure game using Python and practice using functions, loops, conditionals, and basic data structures. Your program should:

# 1) Start by displaying a welcome message and game instructions using a display_title() function.

# 2) Include a main() function that controls the game flow.

# 3) Ask the player to enter their name or a code name and validate the input using a regular expression; using the re module.

# 4) Present the user with choices using if/elif/else statements.

# 5) Use at least two additional functions, aside from main() and display_title(), to control sections of the story.

# 6) Store the player's decisions in a list.

# 7) Use a loop to allow the player to replay the game.

# 8) Include at least one while or for loop and one dictionary to map outcomes.

# 9) Save the player's game data (e.g., name, decisions, outcome) to a file in JSON format using the json module

import os
import re
import json
import time
def display_title ():  
    print('Welcome to my game!')

def enter_credentials (): 
    username = input('Please enter your username\n')
    if re.match(r'^[a-zA-Z0-9]+$', username):
        print('Credentials accepted!\n')
        print('Game is loading...\n')
        game_rules(username)
        return username
    else: 
        print('Invalid credentials! Try again!')
        return enter_credentials()
        
def game_rules (username):
    print("=" * 50)
    print("Welcome", username, '\n')
    print("=" * 50)
def display_game_title():
    print("""
    ████████╗██╗  ██╗███████╗    ███╗   ███╗ █████╗ ████████╗██████╗ ██╗██╗  ██╗
    ╚══██╔══╝██║  ██║██╔════╝    ████╗ ████║██╔══██╗╚══██╔══╝██╔══██╗██║╚██╗██╔╝
       ██║   ███████║█████╗      ██╔████╔██║███████║   ██║   ██████╔╝██║ ╚███╔╝ 
       ██║   ██╔══██║██╔══╝      ██║╚██╔╝██║██╔══██║   ██║   ██╔══██╗██║ ██╔██╗ 
       ██║   ██║  ██║███████╗    ██║ ╚═╝ ██║██║  ██║   ██║   ██║  ██║██║██╔╝ ██╗
       ╚═╝   ╚═╝  ╚═╝╚══════╝    ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝
    
                    Wake up, Neo...
                    The Matrix has you...
                    Follow the white rabbit.
    """)
    print("=" * 80)    
def begin_game (username): 
    play = input('Would you like to begin a game?y/n\n')
    if re.fullmatch(r'^[y]$', play):
        return story_mode(username)
    else: 
        print('Fine then! Goodbye!')
        return None
def story_mode(username):
    clear_screen()
    display_game_title()
    print()
    print(username,',you have a choice...\n')
    print("\nYou find yourself in a dimly lit room.\n")
    print("A mysterious figure approaches you with two pills:")
    print("RED PILL  - Learn the truth, no matter how harsh")
    print("BLUE PILL - Stay in blissful ignorance")
    
    while True:
        choice = input("Which pill? (red/blue): ").lower().strip()
        if choice == 'red':
            return choice
        elif choice == 'blue':
            return choice
        else: 
            print('Invalid response')
        
def pill_path(color, name, decisions):
    if color == 'red':
        print()
        print("\nYou wake up in a strange pod filled with liquid...")
        print("Cables disconnect from your body as you're pulled free.")
        print("A bald man in sunglasses greets you: 'Welcome to reality.'")
        title, mission, outcome = red_training_paths()
        decisions.append(f"Chose {color} pill")
        decisions.append(f"Selected job: {title}")
        store_player_data(color, name, title, mission, outcome, decisions)
        print("Stand by and wait for out orders to complete your training...Goodbye")
        time.sleep(3)
        clear_screen()
        play_again()
    elif color == 'blue':
        print("\nYou wake up in your bed, sunlight streaming through the window.")
        print("Was it all just a dream?")
        title, mission, outcome = blue_training_paths()
        decisions.append(f"Chose {color} pill")
        decisions.append(f"Selected job: {title}")
        store_player_data(color, name, title, mission, outcome, decisions)
        print("You won! Thank you for playing, goodbye")
        play_again()
                
def red_training_paths ():
    print("=" * 60)
    print("Morpheus: 'We need to prepare you. Choose your training:'")
    print()
    print("1. COMBAT - Learn martial arts and weapons (high risk, high reward)")
    print("2. HACKING - Master the code of the Matrix (stealth and strategy)")
    print("3. PILOT - Fly hovercraft and navigate the real world (support role)")
    print()
    
    while True: 
        training_selected = input("Choose your path (1/2/3): ").strip()
        if training_selected in ['1', '2', '3']:
            break
        print("Invalid choice! Enter 1, 2, or 3")
    training_details = {
        '1': ('COMBAT SPECIALIST', 'You become a warrior, ready to fight the machines.'),
        '2': ('ELITE HACKER', 'You can bend the Matrix to your will.'),
        '3': ('EXPERT PILOT', 'You master navigation through the dangerous real world.')
    }
    title, mission = training_details[training_selected]
    outcome = "Joined the resistance"
    return title, mission, outcome

def blue_training_paths ():
    print("=" * 60)
    print('Your alarm goes off. Time to get my day started!')
    print()    
    print("WORK - Go to your office job (responsible)")
    print("REST - Stay home and relax (fun)")
    print()
    while True: 
        schedule_selected = input("What's on your schedule for today? (Work/Rest): ").strip()
        if schedule_selected in ['work', 'rest']:
            break
        print("Invalid choice! Enter work or rest")
    schedule_details = {
        'work': ('Employee', 'You head to the office for another day of meetings.'),
        'rest': ('Gamer', 'You stay home and enjoy a relaxing day off.')
    }
    title, mission = schedule_details[schedule_selected]
    outcome = "Stayed in the Matrix"
    return title, mission, outcome
    
def play_again (): 
    play_again_input = input('Would you like to play again? y/n\n')
    if play_again_input == 'y':
        main()
    else:
        clear_screen()
        return None 

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def store_player_data(color, name, job, mission, outcome, decisions ):
    player_data = {
        "color": color,
        "name": name,
        "job": job,
        "mission": mission,
        "outcome": outcome,
        "decisions": decisions
    }
    with open('player_data.json', 'w') as file: 
        json.dump(player_data, file, indent =4)
   
def main (): 
    display_title()
    player_name = enter_credentials()
    decisions = [] 
    pill = begin_game(player_name)
    pill_path(pill, player_name, decisions)
main()
