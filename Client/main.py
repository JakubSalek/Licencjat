from Client import Client
from GUI.GUI import GUI
import queue

if __name__ == "__main__":
    message_queue = queue.Queue()
    
    client = Client(message_queue)
    gui = GUI(client, message_queue)

    gui.start()



