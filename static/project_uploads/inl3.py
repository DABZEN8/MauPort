import random # För att kunna slumpa ett tal mellan 1-25

def welcome():
    """Välkomnar spelaren till spelet"""
    print('*' * 30)
    print("Välkommen till Bingo!")

def menu():
    """Visar menyalternativ för användaren och ger de ett val mellan 1-3.
    
    Args:
        Kontrollerar så användarens val är inom rätt spann 1-3 i menyn. 
        
    Returns:
        Returnerar användarens val i parametern user_menu_choice om valet är korrekt.
    """
    print("*" * 30)
    print("1. Spela Bingo!")
    print("2. Se statistik")
    print("3. Avsluta")

    while True:
        user_menu_choice = input("Välj ett alternativ 1 - 3: ")
        if user_menu_choice.isdigit() == False: # Har användaren inte svarat med en siffra blir villkoret sant, då får användaren skriva om en siffra 1 - 3
            print("Du måste ange ditt svar med en siffra mellan 1-3.")
        else:
            user_menu_choice = int(user_menu_choice) # Konverterar användarens val från sträng till en int
            if 1 <= user_menu_choice <= 3:
                print('*' * 30)
                return user_menu_choice
            else: 
                print("Fel val. Välj ett alternativ mellan 1-3.") # Om användaren anger felaktig siffra

def get_numbers_from_user(): 
    """Ber användaren att ange fem olika siffror mellan 1 - 25. Ser till att inmatningen av siffrorna är korrekt och returnerar valet om inmatningen är korrekt.
    
    Args:
        Ber användaren om fem siffror, validerar dessa och skapar en lista

    Returns:
        Användarens input, user_bingo_numbers
    """
    while True:
        user_bingo_input = input("Ange fem siffror [1 - 25] (avgränsa med ','): ") # Tar användarens input
        user_bingo_numbers = user_bingo_input.split(",") # Lägger in användarens svar i en tom lista
        
        if len(user_bingo_numbers) != 5:
            print("Du måste fylla i fem olika siffror separerade med kommatecken.")
            continue
        
        try: user_bingo_numbers = [int(num) for num in user_bingo_numbers] # Använder en try och value error här för att se så användaren inte anger något annat än siffror 
        except ValueError: 
            print("Det du skriver in måste vara siffror, försök igen!") 
            continue    

        if not all(1 <= num <= 25 for num in user_bingo_numbers): # Kontrollerar att siffrorna angivna är mellan 1 - 25, är de ej det får användaren ett nytt försök att fylla i siffrorna
            print("Alla siffror måste vara mellan 1-25, försök igen!")
            continue
        
        if len (set(user_bingo_numbers)) != len(user_bingo_numbers): # Jämför ifall användarens svar innehåller dubletter och erbjuder nytt försök ifall det gör det
            print("Du kan inte ange samma nummer mer än en gång, försök igen!")
            continue

        return user_bingo_numbers
        
def draw_numbers():
    """Drar 10 random siffror mellan 1-25 och visar upp dem för spelaren samt returnerar dem
    
    Args: 
        Slumpar fram 10 siffror mellan 1-25
        
    Returns: 
        Returnerar de 10 siffrorna i parametern bingo_numbers
    """
    print("*" * 30)
    print("Dragning...")
    print("*" * 30)
    bingo_numbers = random.sample(range(1,26), 10) # Drar 10 slumpmässiga siffror mellan 1 till 25 

    return bingo_numbers # Returnerar de dragna siffrorna

def bingboard(bingo_number):
    """Skapar och skriver ut en bingobricka med markerade nummer.
    
    Args: 
        Tar emot parametern bingo_numbers från funktionen draw_numbers, kontrollerar rad för rad, tal för tal om de slumpmässigt 
        utvalda siffrorna finns här och markerar de som är med med hakparenteser.
    """
    bingo_board = [
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10],
        [11, 12, 13, 14, 15],
        [16, 17, 18, 19, 20],
        [21, 22, 23, 24, 25]
    ]

    for row in bingo_board:  # Kollar varje rad i brädan
        for number in row:    # Kollar varje tal i raden
            if number in bingo_number:  # Om talet finns i listan ska den markeras med hakparenteser
                print(f"[{number}]", end=" ")
            else:
                print(f" {number} ", end=" ")
        print() 

def compare_numbers(player_numbers, bingo_numbers):
    """Jämför spelarens siffror med de dragnar siffrorna och returnerar antalet rätt.
    
    Args:
        Tar emot parametrarna player_numbers och bingo_numbers, jämför antalet nummer som stämmer överens med varandra och skriver ut till användaren hur många rätt denne fick.
        
    Returns:
        Returnerar parametern correct, antalet rätt användaren fick i bingo-spelet.
    """
    correct = len(set(player_numbers) & set(bingo_numbers))
    print(f"Du fick {correct} rätt!")

    return correct

def save_statistics(statistics, correct): 
    """Sparar resultatet i statistics listan.
    
    Args:
        Tar emot parametrarna statistics och correct, där correct läggs till sist i listan av statistics med (.append).
    """
    statistics.append(correct)

    print("Statistik sparad...")

def show_statistics(statistics): 
    """Visar statistik för spelaren vid begäran (menyval 2).
    
    Args: 
        Tar emot parametern statistics och skriver ut med start från (runda) 1 hur många rätt användaren har haft per omgång,
        vilket har registrerats i funktionen save_statistics.
    """
    print('*' * 30)
    print("Dina resultat: ")

    for i, correct in enumerate(statistics, 1):
        print(f"Runda {i}: {correct} rätt") 
        
def bingo_game(statistics):
    """Kör bingo spelet, denna funktion innefattar hela spelprocessen, användarens siffror, resultatet samt sparandet i statistiken.
    
    Args:
        Tar emot parametern statistics och uppdaterar denna listan.
    """
    player_numbers = get_numbers_from_user()
    bingo_numbers = draw_numbers()
    bingboard(bingo_numbers)
    print('*' *30)
    correct = compare_numbers(player_numbers, bingo_numbers)
    save_statistics(statistics, correct)
      
def main():
    welcome()
    statistics = []
    while True:
        choice = menu()
        if choice == 1:
            bingo_game(statistics) # Startar Bingospelet
        elif choice == 2:
            show_statistics(statistics) # Visar statistik över spelade rundor
        elif choice == 3:
            print("Programmet avslutas. Hejdå!") # Avslutar programmet
            break

if __name__ == "__main__": 
    main()