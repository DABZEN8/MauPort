def get_results_from_file():
    try:
        my_file = open("tournament.txt", "r")
        content = my_file.read()
        results = content.split("\n")

        results_list = []

        for result in results:
            result_per_game = result.split(";")

            try:
                p = {
                    "name": result_per_game[0],
                    "varv1": result_per_game[1],
                    "varv2": result_per_game[2],
                    "varv3": result_per_game[3],
                    "average": result_per_game[4],
                }

                result_per_game.append(p)
            except:
                pass
        my_file.close()
        return results_list
    
    except FileNotFoundError:
        my_file = open("tournament.txt", "w")
        my_file.close()

        return []
    
results = get_results_from_file()

headings = ["Name", "varv1", "varv2", "varv3", "average"]
for heading in headings:
    print(f"{heading:<15}", end="")

print("")
for result in results:
    print(f"{result["name"]}{result["varv1"]}{result["varv2"]}{result["varv3"]}{result["average"]}")

p = {
    "name": "Sara",
    "varv1": "34",
    "varv2": "28",
    "varv3": "40",
    "average": "34"
}

results.append(p)

print(results)
my_file = open("tournament.txt", "w")

for result in results:
    my_file.write(f"{result["name"]};{result["varv1"]};{result["varv2"]};{result["varv3"]};{result["average"]}\n")

my_file.close()