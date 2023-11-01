import os
import time
import sys
import pygetwindow as gw

root_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_directory)

from threading import Thread
from Class.shared import clear_console
from Config.rscheck import is_runescape_running
from Class.shared import kill_processes

def main_menu(main_threading_callback=None, tray_icon_manager_callback=None):
    while True:
        clear_console()
        print("\nRS3 Assist")
        #print("### DEV ###")
        print("-------------------------")
        print("1. Configurar teclas")
        print("2. Configurar porcentagem")
        print("3. Configurar pots e magias")
        print("4. Exibir teclas salvas")
        print("5. Start")
        print("6. Exit")
        print("-------------------------")
        print("Comandos:")
        #print("Botao F10 para voltar ao menu inicial do programa.")
        #print("Botao F11 para Pause e Resume do programa.")
        print("Botao F12, para FECHAR o programa")
        print("-------------------------")
        print("Deixe sempre as barras de VIDA, PRAYER e VIDA do PET amostra")
        print("OBS: O PROGRAMA ESTA EM DEV A TODO MOMENTO!")
        print("-------------------------")
        choice = input("Digite a opcao desejada: ")

        if choice == "1":
            clear_console()
            print("\nConfiguracoes de teclas")
            print("-------------------------")
            print("\n")
            from Config.keys import KeyManager
            manager = KeyManager()
            manager.run()

        elif choice == "2":
            clear_console()
            print("\nConfiguracoes de das porcentagens")
            print("-------------------------")
            print("\n")
            from Config.perct_key import JsonSaver
            JsonSaver()

        elif choice == "3":
            clear_console()
            print("\nConfiguracoes de utilitarios")
            print("-------------------------")
            print("\n")     
            from Config.keys_pots import KeyManagerPot       
            manager = KeyManagerPot()
            manager.run()

        elif choice == "4":
            clear_console() 
            from Config.configs import JsonViewerUpdated
            viewer = JsonViewerUpdated(os.path.join(root_directory, 'Json'))
            viewer.display_content()
            input("Pressione ENTER para voltar.")
            main_menu(main_threading_callback, tray_icon_manager_callback)

        elif choice == "5":
            clear_console()
            tray_icon_thread = Thread(target=tray_icon_manager_callback)
            tray_icon_thread.start()
            print("Verificando configuracoes:")
            time.sleep(0.4)
            print("Dados de teclas carregados... Ok!")
            time.sleep(0.4)
            print("Dados de porcentagem carregado... Ok!")
            time.sleep(0.4)
            print("Dados das teclas de pot carregado... Ok!")
            time.sleep(0.4)
            print("Verificando se Runescape...")
            time.sleep(0.4)
            if is_runescape_running():
                print("\nRunescape aberto.")
                from Config.coords import ImageFinder
                ImageFinder()
                print("\nAguarde o callback das barras de monitoramento... em 20 sec tudo sera minimizado")
                print("\n")
                time.sleep(0.4)
                if main_threading_callback:
                    main_threading_callback()
                    windows = gw.getWindowsWithTitle('RS3 Assit')
                    if windows:
                        windows[0].activate()
                    time.sleep(20)
            else:
                print("Abra o runescape... Reiniciando programa.")
                time.sleep(2)
                main_menu(main_threading_callback, tray_icon_manager_callback)
                
        elif choice == "6":
            global running
            running = False
            print("Fechando programa.")
            kill_processes()
        else:
            print("Opcao invalida, escolha uma das opcoes acima.")