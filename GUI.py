import tkinter
from tkinter import ttk
import time


class Postman:
    def __init__(self):
        self.tk = tkinter.Tk()
        # self.tk.overrideredirect(True)
        self.tk.title("鲁班转发助手")
        self.tk.geometry('600x400+200+200')
        self.tk.resizable(0, 0)
        self.label_nickname = tkinter.Label(self.tk, text="昵称:")
        self.label_nickname.pack()
        self.frame_group = tkinter.LabelFrame(self.tk, text="转发关系", padx=5, pady=5)
        self.frame_group.place(x=10, y=20)
        self.group_forward = ttk.Treeview(self.frame_group, show="headings", columns=('col1', 'col2', 'col3', 'col4'))
        self.group_forward.heading('col1', text='监听群')
        self.group_forward.heading('col2', text='监听详情')
        self.group_forward.heading('col3', text='转发群')
        self.group_forward.heading('col4', text='回复详情')
        self.group_forward.column('col1', width=120, anchor='center')
        self.group_forward.column('col2', width=120, anchor='center')
        self.group_forward.column('col3', width=120, anchor='center')
        self.group_forward.column('col4', width=120, anchor='center')
        # self.group_forward.bind("<ButtonRelease-1>", self.treeviewClick)
        self.group_forward.pack()
        self.button_add_listen = tkinter.Button(self.tk, text="添加监听", command=self.select_group_listen)
        self.button_add_listen.place(x=520, y=30)
        self.button_add_listen = tkinter.Button(self.tk, text="删除监听", command=self.select_group_listen)
        self.button_add_listen.place(x=520, y=70)
        self.group_members = []
        self.combobox_group_listen = None
        self.combobox_group_reply = None
        self.listbox_member_listen = None
        self.listbox_member_reply = None
        self.check_member_listen = None
        self.check_member_reply = None
        self.select_all_listen = False
        self.select_all_reply = False
        self.tl = None
        self.group_listen = None
        self.group_reply = None
        self.members_listen = []
        self.members_reply = []

    def select_group_listen(self):
        self.tl = tkinter.Toplevel(self.tk)
        # self.tk.overrideredirect(True)
        self.tl.title("选择监听群")
        self.tl.geometry('250x80+300+300')
        self.tl.resizable(0, 0)
        self.combobox_group_listen = ttk.Combobox(self.tl)
        self.combobox_group_listen['value'] = ('上海', '北京', '天津', '广州')
        self.combobox_group_listen.pack(pady=10)
        button_next = tkinter.Button(self.tl, text="下一步", command=self.select_group_member_listen)
        button_next.pack()

    def select_group_member_listen(self):
        self.group_listen = self.combobox_group_listen.get()
        self.tl.destroy()
        print(self.group_listen)
        self.tl = tkinter.Toplevel(self.tk)
        self.tl.title("选择监听群成员")
        self.tl.geometry('200x250+300+300')
        self.tl.resizable(0, 0)
        self.group_members = [int(time.time()) + i for i in range(500)]
        self.listbox_member_listen = tkinter.Listbox(self.tl, selectmode=tkinter.MULTIPLE)
        self.listbox_member_listen.pack()
        for member in self.group_members:
            self.listbox_member_listen.insert("end", member)
        self.check_member_listen = tkinter.Checkbutton(self.tl, text="全选1", command=self.select_all_member_listen)
        self.check_member_listen.pack()
        button_next = tkinter.Button(self.tl, text="下一步", command=self.select_group_reply)
        button_next.pack()

    def select_all_member_listen(self):
        if not self.select_all_listen:
            self.select_all_listen = True
            self.listbox_member_listen.selection_set(0, len(self.group_members))
        else:
            self.select_all_listen = False
            self.listbox_member_listen.selection_clear(0, len(self.group_members))

    def select_group_reply(self):
        self.select_all_listen = False
        self.members_listen = self.listbox_member_listen.selection_get().split("\n")
        self.tl.destroy()
        print(self.members_listen, len(self.members_listen))
        self.tl = tkinter.Toplevel(self.tk)
        # self.tk.overrideredirect(True)
        self.tl.title("选择转发群")
        self.tl.geometry('250x80+300+300')
        self.tl.resizable(0, 0)
        self.combobox_group_reply = ttk.Combobox(self.tl)
        self.combobox_group_reply['value'] = ('上海', '北京', '天津', '广州')
        self.combobox_group_reply.pack(pady=10)
        button_next = tkinter.Button(self.tl, text="下一步", command=self.select_group_member_reply)
        button_next.pack()

    def select_group_member_reply(self):
        self.group_reply = self.combobox_group_reply.get()
        self.tl.destroy()
        print(self.group_reply)
        self.tl = tkinter.Toplevel(self.tk)
        self.tl.title("选择转发回复群成员")
        self.tl.geometry('200x250+300+300')
        self.tl.resizable(0, 0)
        self.group_members = [int(time.time()) + i for i in range(500)]
        self.listbox_member_reply = tkinter.Listbox(self.tl, selectmode=tkinter.MULTIPLE)
        self.listbox_member_reply.pack()
        for member in self.group_members:
            self.listbox_member_reply.insert("end", member)
        self.check_member_reply = tkinter.Checkbutton(self.tl, text="全选2", command=self.select_all_member_reply)
        self.check_member_reply.pack()
        button_next = tkinter.Button(self.tl, text="确认添加", command=self.add_listen_relationship)
        button_next.pack()

    def select_all_member_reply(self):
        if not self.select_all_reply:
            self.select_all_reply = True
            self.listbox_member_reply.selection_set(0, len(self.group_members))
        else:
            self.select_all_reply = False
            self.listbox_member_reply.selection_clear(0, len(self.group_members))

    def add_listen_relationship(self):
        self.select_all_reply = False
        self.members_reply = self.listbox_member_reply.selection_get().split("\n")
        self.tl.destroy()
        print(self.members_reply, len(self.members_reply))


if __name__ == '__main__':
    postman = Postman()
    postman.tk.mainloop()