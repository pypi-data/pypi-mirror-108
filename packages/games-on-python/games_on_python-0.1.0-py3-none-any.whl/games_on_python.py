import random
from colorama import Fore, Back, Style, init
init()

class MathGame():
    def __init__(self):
        print("Игра Math иницилизирована!")
    
    def info(self):
        print("Это игра Математика - игра в которой ты сможешь потренироваться в решении примеров.\n")

    def start(self):
        start = input("Нажмите Enter для запуска. ")
        print("")
        while 1:
            a = random.randint(-1000, 1000)
            b = random.randint(-1000, 1000)
            diya = random.randint(0,1)

            if diya == 0:
                result = a + b
                otvet = int(input(f"{a} + {b} = "))
            if diya == 1:
                result = a - b
                otvet = int(input(f"{a} - {b} = "))

            if result == otvet:
                print(f"{Fore.GREEN}Правильный ответ!{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Не правильный ответ!. Ответ был - {result}{Style.RESET_ALL}")

class RSP():
    def __init__(self):
        print("Игра RSP иницилизирована!")
    
    def info(self):
        print("Это камень ножницы бумага - старая игра в которую играли даже динозавры.\n")

    def start(self):
        start = input("Нажмите Enter для запуска.")
        print("")
        player_score = 0
        bot_score = 0
        while 1:
            player = None
            player = int(input(f"{Fore.GREEN}Выберите одно из действий по номеру:{Style.RESET_ALL}\nКамень [1]\nНожницы [2]\nБумага [3]\n\n{Fore.YELLOW}Ваш выбор: {Style.RESET_ALL}"))
            print("")
            bot = random.randint(1, 3)
            if bot == 1:
                print("Бот выбрал камень.\n")
            if bot == 2:
                print("Бот выбрал ножницы.\n")
            if bot == 3:
                print("Бот выбрал бумагу.\n")
            if player == 1:
                if bot == 2:
                    player_score += 1
                    print(f"{Fore.GREEN}Вы выиграли!\n{Fore.BLUE}Счёт:{Style.RESET_ALL}\nВы - {player_score}, Бот - {bot_score}\n")
                else:
                    bot_score += 1
                    print(f"{Fore.RED}Вы проиграли!\n{Fore.BLUE}Счёт:{Style.RESET_ALL}\nВы - {player_score}, Бот - {bot_score}\n")

            if player == 2:
                if bot == 3:
                    player_score += 1
                    print(f"{Fore.GREEN}Вы выиграли!\n{Fore.BLUE}Счёт:{Style.RESET_ALL}\nВы - {player_score}, Бот - {bot_score}\n")
                else:
                    bot_score += 1
                    print(f"{Fore.RED}Вы проиграли!\n{Fore.BLUE}Счёт:{Style.RESET_ALL}\nВы - {player_score}, Бот - {bot_score}\n")
                  
            if player == 3:
                if bot == 1:
                    player_score += 1
                    print(f"{Fore.GREEN}Вы выиграли!\n{Fore.BLUE}Счёт:{Style.RESET_ALL}\nВы - {player_score}, Бот - {bot_score}\n")
                else:
                    bot_score += 1
                    print(f"{Fore.RED}Вы проиграли!\n{Fore.BLUE}Счёт:{Style.RESET_ALL}\nВы - {player_score}, Бот - {bot_score}\n")
            
            if player == bot:
                print(f"{Fore.YELLOW}Ничья!\n{Fore.BLUE}Счёт:\n{Style.RESET_ALL}Вы - {player_score}, Бот - {bot_score}\n")