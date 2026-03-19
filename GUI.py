import tkinter as tk
from tkinter import messagebox
import ctypes
import os
import sys

if getattr(sys,'frozen',False):
    current_dir = sys._MEIPASS
else:
    current_dir = os.path.dirname(os.path.abspath(__file__))

lib_path = os.path.join(current_dir,"menu_lib.dll")

USE_CPP = True

BG = "#F5F0E6"
BTN = "#E1D5C9"
FNT = ("Arial",11)

class Node(ctypes.Structure):
    pass
Node._fields_ = [("a",ctypes.c_int),
                ("b",ctypes.c_char * 21),
                ("next",ctypes.POINTER(Node))]

class Queue(ctypes.Structure):
    _fields_ = [("front",ctypes.POINTER(Node)),
                ("rear",ctypes.POINTER(Node)),
                ("size",ctypes.c_int),
                ("created",ctypes.c_int)]


current_dir = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.join(current_dir, "menu_lib.dll")

lib = ctypes.CDLL(lib_path)

lib.createQueue.restype = ctypes.POINTER(Queue)
lib.clearQueue.argtypes = [ctypes.POINTER(Queue)]
lib.enqueue.argtypes = [ctypes.POINTER(Queue),ctypes.c_int,ctypes.c_char_p]
lib.dequeue.argtypes = [ctypes.POINTER(Queue),ctypes.POINTER(ctypes.c_int),ctypes.c_char_p]
lib.dequeue.restype = ctypes.c_int

my_queue_c = lib.createQueue()
py_queue = []

def log(msg):
    Log_operation.insert(tk.END,msg + "\n")
    Log_operation.see(tk.END)

def See_queue():
    show_Queue.delete(1.0,tk.END)
    elements = []
    if USE_CPP:
        if not my_queue_c:
            return
        
        size = my_queue_c.contents.size

        current = my_queue_c.contents.front
        elements = []
        while current:
            node = current.contents
            text_b = node.b.decode('utf-8','ignore')
            elements.append(f"{node.a} {text_b}")
            current = node.next
    else:
        size = len(py_queue)
        for a,b in py_queue:
            elements.append(f"{a} {b}")

    Queue_count.config(text=f"Количество элементов в очереди: {size}")

    if elements:
        show_Queue.insert(tk.END," <<< ".join(elements))
    else:
        show_Queue.insert(tk.END,"(Пусто)")

def enqueue():
    try:
        val_a = int(entry_a.get())
        val_b = entry_b.get()

        if USE_CPP:
            lib.enqueue(my_queue_c,val_a,val_b.encode('utf-8'))
        else:
            py_queue.append((val_a,val_b))
        log(f"Добавлено: {val_a} {val_b}")

        entry_a.delete(0,tk.END)
        entry_b.delete(0,tk.END)
        See_queue()
    except ValueError:
        messagebox.showerror("Ошибка ввода","Введите целое число")

def dequeue():
    if USE_CPP:
        out_a = ctypes.c_int()
        out_b = ctypes.create_string_buffer(21)

        succes = lib.dequeue(my_queue_c,ctypes.byref(out_a),out_b)

        if succes == 1:
            text_b = out_b.value.decode('utf-8','ignore')
            log(f"Удалено: {out_a.value} {text_b}")
        else:
            messagebox.showinfo("Информация","Очередь пустая")
    else:
        if len(py_queue) > 0:
            a,b = py_queue.pop(0)
            log(f"Удалено: {a} {b}")
        else:
            messagebox.showinfo("Информация","Очередь пустая")
    
    See_queue()

def clear():
    if USE_CPP:
        lib.clearQueue(my_queue_c)
    else:
        py_queue.clear()
    log("Очередь удалена")
    See_queue()

def switch():
    global USE_CPP
    if USE_CPP:
        lib.clearQueue(my_queue_c)
    else:
        py_queue.clear()
    USE_CPP = var.get()
    log(("Переход на C++" if USE_CPP else "Переход на Python"))
    See_queue()


root = tk.Tk()
root.title("Очередь")
root.geometry("600x800") 
root.configure(bg=BG)


# Верхний общий блок 
top_frame = tk.Frame(root,bg=BG)
top_frame.pack(pady=10, fill=tk.X)

# Левая колонка для кнопок 
left_frame = tk.Frame(top_frame,bg=BG)
left_frame.pack(side=tk.LEFT, padx=20,pady=40, anchor=tk.N)

tk.Label(left_frame,text="Число:").pack(anchor=tk.W)
entry_a = tk.Entry(left_frame,width=25,font=FNT)
entry_a.pack(pady=2)

tk.Label(left_frame,text="Строка:").pack(anchor=tk.W)
entry_b = tk.Entry(left_frame,width=25,font=FNT)
entry_b.pack(pady=2)

Queue_enqueue = tk.Button(left_frame,text = "Добавить элемент",width = 25,height=3,command=enqueue,bg=BTN,font=FNT,relief=tk.FLAT)
Queue_dequeue = tk.Button(left_frame,text = "Удалить элемент",width = 25,height=3,command=dequeue,bg=BTN,font=FNT,relief=tk.FLAT)
Queue_delete = tk.Button(left_frame,text = "Удалить очередь",width = 25,height=3,command=clear,bg=BTN,font=FNT,relief=tk.FLAT)
Button_exit = tk.Button(left_frame,text="Выход",width=25,height=3,command=root.destroy,bg=BTN,font=FNT,relief=tk.FLAT)


Queue_enqueue.pack(pady=10)
Queue_dequeue.pack(pady=10)
Queue_delete.pack(pady=10)
Button_exit.pack(pady=10)

# Правая колонка для состояния очереди 
right_frame = tk.Frame(top_frame,bg=BG)
right_frame.pack(side=tk.LEFT, padx=20, fill=tk.BOTH, expand=True)
Queue_count = tk.Label(right_frame,text = "Количество элементов в очереди - ",font=16,bg=BG)
show_Queue = tk.Text(right_frame,font=FNT)

Queue_count.pack(pady=5,anchor=tk.W)
show_Queue.pack(pady=5)
var = tk.BooleanVar(value=True)
tk.Radiobutton(right_frame,text="C++",variable=var,value=True,command=switch).pack(anchor=tk.W)
tk.Radiobutton(right_frame,text="Python",variable=var,value=False,command=switch).pack(anchor=tk.W)



# Нижний блок для лога операций 
bottom_frame = tk.Frame(root,bg=BG)
bottom_frame.pack(pady=0, padx=20, fill=tk.BOTH, expand=True)
Log_text = tk.Label(bottom_frame,text = "Лог операций:",font=16,bg=BG)
Log_operation = tk.Text(bottom_frame,font=FNT)

Log_text.pack(pady=5,anchor=tk.W,fill=tk.BOTH,expand=True)
Log_operation.pack(pady=5)

See_queue()

root.mainloop() 