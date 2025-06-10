import os
import time
import StockMarket
import MarktplaatsNotifier
import TicketSwapBot as tsb
import filechecker as fc
import Documentwriter as dw
import Sorteerautomatisatie as sa

art = ['''
   _______________                        |*\_/*|________
  |  ___________  |     .-.     .-.      ||_/-\_|______  |
  | |           | |    .****. .****.     | |           | |
  | |   <   <   | |    .*****.*****.     | |   0   0   | |
  | |     -     | |     .*********.      | |     -     | |
  | |   \___/   | |      .*******.       | |   \___/   | |
  | |___     ___| |       .*****.        | |___________| |
  |_____|\_/|_____|        .***.         |_______________|
    _|__|/ \|_|_            .*.             _|________|_
  /  **********  \           .            /  **********  \\
 /  ************  \                      /  ************  \\
/__________________\\                    /__________________\\    
''','''
   _______________                        |*\_/*|________
  |  ___________  |                      ||_/-\_|______  |
  | |           | |     ****   ****      | |           | |
  | |   <   <   | |     ***** *****      | |   0   0   | |
  | |     -     | |      *********       | |     -     | |
  | |   \___/   | |       *******        | |   \___/   | |
  | |___     ___| |        *****         | |___________| |
  |_____|\_/|_____|         ***          |_______________|
    _|__|/ \|_|_             *              _|________|_
  /  **********  \                        /  **********  \\
 /  ************  \                      /  ************  \\
/__________________\\                    /__________________\\              
''','''
   _______________                        |*\_/*|________
  |  ___________  |                      ||_/-\_|______  |
  | |           | |                      | |           | |
  | |   <3  <3  | |                      | |   0   0   | |
  | |     -     | |                      | |     -     | |
  | |   \___/   | |                      | |   \___/   | |
  | |___     ___| |                      | |___________| |
  |_____|\_/|_____|                      |_______________|
    _|__|/ \|_|_                            _|________|_
  /  **********  \                        /  **********  \\
 /  ************  \                      /  ************  \\
/__________________\\                    /__________________\\    
''',]

def play_art():
    for i in range(4):
        clear()
        print(art[0])
        time.sleep(0.35)
        clear()
        print(art[1])
        time.sleep(0.35) 
    clear()
    print(art[2])


def cmd(command):
    os.system(command)

def clear():
    cmd('cls' if os.name == 'nt' else 'clear')

def set_title(title):
    cmd(f'title {title}' if os.name == 'nt' else f'echo -n -e "\033]0;{title}\a"')

def main():
    while True:
        try:
            set_title("Mango Suite")
            clear()
            play_art()
            set_title("Mango Suite v1.0")
            print("1. Sorteerautomatisatie\n2. File Checker\n3. Documentwriter\n4. StockMarket Notifier\n5. Marktplaats notifier\n6. TicketSwapBot\n7. Play Animation ;P\n8. Exit")
            u_i = int(input("What Option do you choose?\nChoice: "))
            if u_i <= 0 or u_i > 5:
                print("Invalid choice, please try again.")
                main()
            elif u_i == 1:
                sa.main()
                pause = input("Press Enter to continue...")
            elif u_i == 2:
                fc.main()
                pause = input("Press Enter to continue...")
            elif u_i == 3:
                dw.main()
                pause = input("Press Enter to continue...")
            elif u_i == 4:
                StockMarket.main()
                pause = input("Press Enter to continue...") 
            elif u_i == 5:
                MarktplaatsNotifier.main()
                pause = input("Press Enter to continue...")
            elif u_i == 6:
                tsb.main()
            elif u_i == 7:
                play_art()    
            elif u_i == 8:
                print("Exiting...")
                break
        except Exception as e:
            print(f"An error occurred in the first try in mains while loop: {e}")
            time.sleep(2)
            main()




if __name__ == "__main__":
    main()