from Server import Server
import SETTINGS as S

def main():
    server = Server(S.HOST, S.PORT)
    server.start()


if __name__ == "__main__":
    main()