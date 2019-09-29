import settings
import os
from threading import Thread

def user_input():
    while True:
        command = input().strip().lower()
        if command == 'quit':
            stop_bot()
        elif command == 'help':
            str_help = ('\n----------HELP----------\n\n'
                        'quit -- shut down the bot\n'
                        'settings -- change settings')
            print(str_help)
        elif command != '':
            print('Invalid command entered!')
            
def stop_bot():
    print('Shutting down bot...')
    # perform any pre-exit ops
    os._exit(0)

if __name__ == '__main__':
    print('BitMEX Auto Stop Loss and Take Profit Bot')
    print('Loading settings...',end='')
    settings._init()
    config = settings.get_settings()
    print('done\n')
    # init CLI mode
    Thread(target=user_input).start()
    print('Type "start" to run the bot. Type "help" to see available commands.')

    
