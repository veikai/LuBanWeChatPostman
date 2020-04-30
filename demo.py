# from tkinter import *
#
# def createBox(window):
#     list_ = ['CARGA', 'MAQUINA', 'SOLTAR']
#     for i in range(3):
#         mybox = LabelFrame(window, padx=5, pady=4)
#         mybox.grid(row=i, column=0)
#         createWindow(mybox, list_[i], i)
#
# def createWindow(box, lt_actual, i):
#     canvas = Canvas(box, borderwidth=0)
#     frame = Frame(canvas)
#     vsb = Scrollbar(box, orient="vertical", command=canvas.yview)
#     canvas.configure(yscrollcommand=vsb.set, width=1200, heigh=80)
#
#     vsb.pack(side="right", fill="y")
#     canvas.pack(side="left", fill="both", expand=True)
#     canvas.create_window((4,4), window=frame, anchor="nw", tags="frame")
#
#     # be sure that we call OnFrameConfigure on the right canvas
#     frame.bind("<Configure>", lambda event, canvas=canvas: OnFrameConfigure(canvas))
#
#     fillWindow(lt_actual, frame)
#
# def fillWindow(lt_ver, frame):
#     piezas = ['time: 39.41597 BT: 3025.5923', 'time: 21.637377 BT: 3025.5923', 'time: 52.185192 BT: 3025.5923', 'time: 57.804752 BT: 3025.5923', 'time: 47.700306 BT: 3025.5923', 'time: 21.1827 BT: 3025.5923', 'time: 35.244156 BT: 3025.5923', 'time: 47.26321 BT: 3025.5923']
#     fechaentrada = ['26-02-2014', '26-02-2014', '26-02-2014', '26-02-2014', '26-02-2014', '26-02-2014', '26-02-2014', '21-02-2014']
#     fechasalida = ['26-02-2014', '26-02-2014', '26-02-2014', '26-02-2014', '26-02-2014', '26-02-2014', '26-02-2014', '21-02-2014']
#     horacomienzo = ['12:00', '12:39', '01:00', '01:52', '02:49', '03:36', '03:57', '12:00']
#     horafinal = ['12:39', '01:00', '01:52', '02:49', '03:36', '03:57', '04:32', '12:47']
#     ide = [0, 1, 2, 3, 4, 5, 6, 7]
#
#     idpieza_w1 = Label(frame, text = "Id", width=20, font="bold")
#     idpieza_w1.grid(row=0, column=0)
#     pieza_w1 = Label(frame, text = "Pieza", width=20, font="bold")
#     pieza_w1.grid(row=0, column=1)
#     fechainiciopromo_w1 = Label(frame, text = "Dia inicio " + str(lt_ver), width=20, font="bold")
#     fechainiciopromo_w1.grid(row=0, column=2)
#     horainiciopromo_w1 = Label(frame, text = "Hora inicio " + str(lt_ver), width=20, font="bold")
#     horainiciopromo_w1.grid(row=0, column=3)
#     fechafinalpromo_w1 = Label(frame, text = "Dia fin carga " + str(lt_ver), width=20, font="bold")
#     fechafinalpromo_w1.grid(row=0, column=4)
#     horafinalpromo_w1 = Label(frame, text = "Hora final carga " + str(lt_ver), width=20, font="bold")
#     horafinalpromo_w1.grid(row=0, column=5)
#
#     for i in range(len(piezas)):
#         idtextos_w1 = Label(frame, text=str(ide[i]))
#         idtextos_w1.grid(row=i+1, column=0)
#         textos_w1 = Label(frame, text=str(piezas[i]))
#         textos_w1.grid(row=i+1, column=1)
#         fechainiciogrid_w1 = Label(frame, text=str(fechaentrada[i]))
#         fechainiciogrid_w1.grid(row=i+1, column=2)
#         horainiciogrid_w1 = Label(frame, text=str(horacomienzo[i]))
#         horainiciogrid_w1.grid(row=i+1, column=3)
#         fechafinalgrid_w1 = Label(frame, text=str(fechasalida[i]))
#         fechafinalgrid_w1.grid(row=i+1, column=4)
#         horafinalgrid_w1 = Label(frame, text=str(horafinal[i]))
#         horafinalgrid_w1.grid(row=i+1, column=5)
#
# def OnFrameConfigure(canvas):
#     canvas.configure(scrollregion=canvas.bbox("all"))
#
#
# tk = Tk()
#
# createBox(tk)
#
# tk.mainloop()

# =========================================================================
# import tkinter
# from tkinter import ttk
#
# root = tkinter.Tk()
#
# tree = ttk.Treeview(root, show="headings", columns=('col1', 'col2', 'col3'))
#
# tree.heading('col1', text='第一列')
#
# tree.heading('col2', text='第二列')
#
# tree.heading('col3', text='第三列')
#
# tree.column('col1', width=100, anchor='center')
#
# tree.column('col2', width=100, anchor='center')
#
# tree.column('col3', width=100, anchor='center')
#
#
# def onDBClick(event):
#     item = tree.selection()[0]
#
#     print("you clicked on ", tree.item(item, "values"))
#
#
# for i in range(10):
#     tree.insert('', i, values=('a' + str(i), 'b' + str(i), 'c' + str(i)))
#
# tree.bind("<ButtonRelease-1>", onDBClick)
#
# tree.pack()
#
# root.mainloop()
# =========================================================================
# import tkinter
# from tkinter import ttk  # 导入内部包
#
# li = ['王记', '12', '男']
# root = tkinter.Tk()
# root.title('测试')
# tree = ttk.Treeview(root, columns=['1', '2', '3'], show='headings')
# tree.column('1', width=100, anchor='center')
# tree.column('2', width=100, anchor='center')
# tree.column('3', width=100, anchor='center')
# tree.heading('1', text='姓名')
# tree.heading('2', text='学号')
# tree.heading('3', text='性别')
# tree.insert('', 'end', values=li)
# tree.grid()
#
#
# def treeviewClick(event):  # 单击
#     print('单击')
#     for item in tree.selection():
#         item_text = tree.item(item, "values")
#         print(item_text[0])  # 输出所选行的第一列的值
#
#
# tree.bind('<ButtonRelease-1>', treeviewClick)  # 绑定单击离开事件===========
#
# root.mainloop()
# =========================================================================
# from tkinter import *
#
# abc = Tk()
# abc.title('试试文本框右键菜单')
# abc.resizable(False, False)
# abc.geometry("300x100+200+20")
# Label(abc, text='下面是一个刚刚被生成的文本框，试试操作吧').pack(side="top")
# Label(abc).pack(side="top")
# show = StringVar()
# Entry = Entry(abc, textvariable=show, width="30")
# Entry.pack()
#
#
# class section:
#     def onPaste(self):
#         try:
#             self.text = abc.clipboard_get()
#         except TclError:
#             pass
#         show.set(str(self.text))
#
#     def onCopy(self):
#         self.text = Entry.get()
#         abc.clipboard_append(self.text)
#
#     def onCut(self):
#         self.onCopy()
#         try:
#             Entry.delete('sel.first', 'sel.last')
#         except TclError:
#             pass
#
#
# section = section()
# menu = Menu(abc, tearoff=0)
# menu.add_command(label="复制", command=section.onCopy)
# menu.add_separator()
# menu.add_command(label="粘贴", command=section.onPaste)
# menu.add_separator()
# menu.add_command(label="剪切", command=section.onCut)
#
#
# def popupmenu(event):
#     menu.post(event.x_root, event.y_root)
#
#
# Entry.bind("<Button-3>", popupmenu)
# abc.mainloop()

#======================================================================================
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
class productdata(object):
    def __init__(self):
        self.root = tk.Tk() #初始化
        self.root.title('数据方舟') #修改窗体名称
        self.root.resizable(width=False,height=False) #窗体界面宽高可调
        self.root.geometry('900x500') #窗体默认大小
        self.canvas = tk.Canvas(self.root,width='1200',height='1200')
        self.canvas.pack(side='top')
        #定义一个变量监控删除行数
        self.delhang=0
        #添加一个表格
        columns = ("字段类型", "字段长度", "小数位数", "是否唯一", "字段名称")
        self.treeview = ttk.Treeview(self.root, height=18, show="headings", columns=columns)
        # 表示列,不显示
        self.treeview.column("字段类型", width=100, anchor='center')
        self.treeview.column("字段长度", width=100, anchor='center')
        self.treeview.column("小数位数", width=100, anchor='center')
        self.treeview.column("是否唯一", width=100, anchor='center')
        self.treeview.column("字段名称", width=100, anchor='center')
        # 显示表头
        self.treeview.heading("字段类型", text="字段类型")
        self.treeview.heading("字段长度", text="字段长度")
        self.treeview.heading("小数位数", text="小数位数")
        self.treeview.heading("是否唯一", text="是否唯一")
        self.treeview.heading("字段名称", text="字段名称")
        # 写入数据
        self.type = ['letter']
        self.long = ['10']
        self.decimal = ['0']
        self.only = ['是']
        self.name = ['资源ID']
        for i in range(min(len(self.type), len(self.long), len(self.decimal), len(self.only), len(self.name))):
            self.treeview.insert('', i, values=(self.type[i], self.long[i], self.decimal[i], self.only[i], self.name[i]))
            # 双击左键进入编辑
            self.treeview.bind('<Double-1>', self.set_cell_value)
            #添加一个'添加字段'按钮
            self.add_field_button = ttk.Button(self.root,text='添加字段',width=10, command=self.newrow)
            # 添加一个'删除字段'按钮
            self.del_field_button = ttk.Button(self.root,text='删除字段',width=10, command=self.delrow)
            #添加一个'清空字段'按钮
            self.delall_field_button = ttk.Button(self.root,text='清空字段',width=10,command=self.delall)
    def buju(self):
        #添加按钮
        self.add_field_button.place(x=780,y=40)
        #删除按钮
        self.del_field_button.place(x=780,y=80)
        #清空按钮
        self.delall_field_button.place(x=780,y=120)
        #表格布局
        self.treeview.place(x=0, y=2, width=750, height=200)
    def set_cell_value(self,event):
        for item in self.treeview.selection():
        # item = I001
            item_text = self.treeview.item(item, "values")
        # print(item_text[0:2])  # 输出所选行的值
            column = self.treeview.identify_column(event.x)  # 列
            row = self.treeview.identify_row(event.y)  # 行
            cn = int(str(column).replace('#', ''))
            rn = int(str(row).replace('I', ''))-self.delhang
            entryedit = Text(self.root, width=10, height=1)
            entryedit.place(x=20 + (cn - 1) * 150, y=6 + rn * 20)
            def saveedit():
                self.treeview.set(item, column=column, value=entryedit.get(0.0, "end"))
                entryedit.destroy()
                # okb.destroy()
                # okb = ttk.Button(self.root, text='OK', width=4, command=saveedit)
                # okb.place(x=90 + (cn - 1) * 150, y=2 + rn * 20)
    def newrow(self):
        self.type.append('输入e799bee5baa6e58685e5aeb931333431373834字段类型')
        self.long.append('输入字段长度')
        self.decimal.append('输入小数位数')
        self.only.append('是否唯一')
        self.name.append('请输入字段长度')
        self.treeview.insert('', len(self.type) - 1, values=(self.type[len(self.type)-1],
        self.long[len(self.type)-1],
        self.decimal[len(self.type)-1],
        self.only[len(self.type)-1],
        self.name[len(self.type)-1]))
        self.treeview.update()
    def delrow(self):
        selected_items = self.treeview.selection()
        for item in selected_items:
            self.treeview.delete(item)
            self.delhang +=1
    def delall(self):
        all_items = self.treeview.get_children()
        for item in all_items:
            self.treeview.delete(item)
        self.delhang =0


def main():
    #初始化对象
    p = productdata()
    #进行布局
    p.buju()
    tk.mainloop()
if __name__=="__main__":
    main()