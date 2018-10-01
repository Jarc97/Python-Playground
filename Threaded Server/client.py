from tkinter import *
import socket

root = Tk()

def send():
    # identifier-sender-amount-receiver-counter-epoch
    msg = str(address) + "-" + amountEntry.get() + "-" + addressEntry.get()
    s.send(msg)

def refresh():
    s.send("requesting update")
    balanceLabel = s.recv(4096)

balance = 0
address = 1234567890

refresh = Button(root, text="Refresh", command=refresh)
refresh.pack()
balanceLabel = Label(root, text=str(balance))
balanceLabel.pack()
addressLabel = Label(root, text=str(address))
addressLabel.pack()
addressEntry = Entry(root)
addressEntry.pack()
amountEntry = Entry(root, bg="red")
amountEntry.pack()
sendButton = Button(root, text="Send", command=send)
sendButton.pack()



s = socket.socket()
host = "10.0.1.32"
port = 5000
s.connect((host, port))




root.title("Wallet")
root.geometry("200x200")
root.mainloop()
