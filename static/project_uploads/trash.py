#Global variabel för spelet
#game_nr_list = list(range(1, 26))
import random #För att slumpa ett tal mellan 1-25

def menu():
    """Visar menyalternativ för användaren och ger de ett val mellan 1-3."""
    print("*" * 30)
    print("1. Spela Bingo!")
    print("2. Se statistik")
    print("3. Avsluta")

    user_menu_choice = input

    while True:
        user_menu_choice = input("Välj ett alternativ 1 - 3: ")
        if user_menu_choice.isdigit() == False: #Har användaren inte svarat med en siffra blir villkoret sant, då får användaren skriva om en siffra 1 - 3
            print("Du måste ange ditt svar med en siffra mellan 1-3.")
        else:
            user_menu_choice = int(user_menu_choice) #Konverterar användarens val från sträng till en int
            if 1 <= user_menu_choice <= 3:
                return user_menu_choice
            else: 
                print("Välj ett alternativ mellan 1-3.")

def no_duplicates():
    """Ber användaren att ange fem siffror mellan 1 - 25. 
    Kontrollerar att det ej finns några dubletter av siffrorna, om det finns får användaren chansen att fylla i fem nya siffror."""

    while True:
        user_bingo_input = input("Ange fem siffror [1 - 25] (avgränsa med ','): ") #Tar användarens input
        user_bingo_numbers = user_bingo_input.split(",") #Lägger in användarens svar i en tom lista
        
        if len(user_bingo_numbers) != 5:
            print("Du måste fylla i fem olika siffror separerade med kommatecken.")
        user_bingo_numbers = [int(num) for num in user_bingo_numbers]
        
        if not all(1 <= num <= 25 for num in user_bingo_numbers): #1 <= 1 eller större än 1, <= 25 eller lika med 25
            print("Alla siffror måste vara mellan 1-25, försök igen!")
        
        if len (set(user_bingo_numbers)) != len(user_bingo_numbers): #Jämför ifall användarens svar innehåller dubletter och erbjuder nytt försök ifall det gör det.
            print("Du kan inte ange samma nummer mer än en gång, försök igen!")
        
        print("Dragning...")
        print("*" * 30)
        bingo_numbers = list(range(1,26)) #Printar ut siffrorna 1-25, men i ordning och varje rad inom en hakparentes, fixa.
        for i in range(0, len(bingo_numbers), 5):
            print(bingo_numbers[i:i + 5])
        break

    return game 

#Bortkommenterad så länge 
"""def bingo():
    Slumpar ut 10 siffror mellan 1-25, jämför med användarens gissning och returnerar om/hur många rätt användaren hade.
    bingo_game = random.randint(1,25)
    print(f"Hallå {bingo_game}")"""

def game():
    pass

#Ska registrera statistik från spelet i def bingo
def show_statistics():
    pass
          
def main():
    while True:
        choice = menu()
        if choice == 1:
            no_duplicates()
            #bingo()
            game()
        elif choice == 2:
            show_statistics()
        elif choice == 3:
            print("Hejdå!")
            break

if __name__ == "__main__": 
    main()