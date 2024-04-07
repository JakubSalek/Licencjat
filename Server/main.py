from Server import Server
import SETTINGS as S

if __name__ == "__main__":
    server = Server(S.HOST, S.PORT)
    server.start()
