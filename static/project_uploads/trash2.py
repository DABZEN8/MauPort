game_nr_list = list(range(1, 26))

def menu():
    """Visar menyalternativ för användaren och ger dem ett val mellan 1-3."""
    print("*" * 30)
    print("1. Spela Bingo!")
    print("2. Se statistik")
    print("3. Avsluta")

    while True:
        user_answer = input("Välj ett alternativ 1 - 3: ")
        if not user_answer.isdigit():
            print("Du måste ange ditt svar med en siffra mellan 1-3.")
        else:
            user_answer = int(user_answer)
            if 1 <= user_answer <= 3:
                return user_answer
            else:
                print("Välj ett alternativ mellan 1-3.")

def bingo():
    """Ber användaren att ange fem siffror mellan 1 - 25."""
    while True:
        try:
            user_bingo_input = input("Ange fem siffror [1-25] (avgränsa med ','): ")
            user_bingo_list = [int(x.strip()) for x in user_bingo_input.split(',')]
            if len(user_bingo_list) != 5:
                print("Du måste ange exakt 5 siffror.")
                continue
            if any(num < 1 or num > 25 for num in user_bingo_list):
                print("Alla siffror måste vara mellan 1 och 25.")
                continue
            if len(set(user_bingo_list)) != len(user_bingo_list):
                print("Inga dubletter är tillåtna.")
                continue
            print(f"Dina valda siffror är: {user_bingo_list}")
            break
        except ValueError:
            print("Du måste ange siffror avgränsade med ','.")

def game():
    """Visar en lista med nummer från 1-25."""
    print(f"Spelnummerlista: {game_nr_list}")

def show_statistics():
    print("Statistikfunktionen är inte implementerad än.")

def main():
    while True:
        choice = menu()
        if choice == 1:
            bingo()
            game()
        elif choice == 2:
            show_statistics()
        elif choice == 3:
            print("Hejdå!")
            break

if __name__ == "__main__":
    main()
