import tkinter
from tkinter import ttk
from PyWeChatSpy import WeChatSpy
from time import sleep
import pickle
import re
import os

data_global = {}
listen_index = 1
if os.path.exists("data.pkl"):
    with open("data.pkl", "rb") as rf:
        data_global = pickle.load(rf)


class Postman:
    def __init__(self):
        self.tk = tkinter.Tk()
        self.tk.title("鲁班转发助手")
        self.tk.geometry('600x400+200+200')
        self.tk.resizable(0, 0)
        self.label_nickname = tkinter.Label(self.tk, text="昵称:")
        self.label_nickname.pack()
        self.frame_group = tkinter.LabelFrame(self.tk, text="转发关系", padx=5, pady=5)
        self.frame_group.place(x=10, y=20)
        self.group_forward = ttk.Treeview(self.frame_group, show="headings", columns=('col0', 'col1', 'col2', 'col3', 'col4'))
        self.group_forward.heading('col0', text='ID')
        self.group_forward.heading('col1', text='监听群')
        self.group_forward.heading('col2', text='监听详情')
        self.group_forward.heading('col3', text='转发群')
        self.group_forward.heading('col4', text='回复详情')
        self.group_forward.column('col0', width=20, anchor='center')
        self.group_forward.column('col1', width=120, anchor='center')
        self.group_forward.column('col2', width=120, anchor='center')
        self.group_forward.column('col3', width=120, anchor='center')
        self.group_forward.column('col4', width=120, anchor='center')
        self.group_forward.pack()
        self.label_log = tkinter.Label(self.tk, text="日志通知")
        self.label_log.place(x=10, y=300)
        self.button_open_wechat = tkinter.Button(self.tk, text="打开微信", command=self.open_wechat)
        self.button_open_wechat.place(x=535, y=30)
        self.button_add_listen = tkinter.Button(self.tk, text="添加监听", command=self.select_group_listen)
        self.button_add_listen.place(x=535, y=70)
        self.button_add_listen = tkinter.Button(self.tk, text="删除监听", command=self.delete_listen_relationship)
        self.button_add_listen.place(x=535, y=110)
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
        self.pid = 0
        self.spy = WeChatSpy(parser=self.parser, multi=True)
        self.wxid = None

    def parser(self, data):
        global listen_index
        m_type = data.pop("type")
        pid = data.pop("pid")
        if m_type == 1:
            self.wxid = data["wxid"]
            if not data_global.get(self.wxid):
                data_global[data["wxid"]] = {
                    "listen_relationship": {},
                    "pid_chatroom": {},
                    "chatroom_nickname": {},
                    "chatroom_member": {},
                    "member_nickname": {}
                }
            for k, v in data_global[self.wxid]["listen_relationship"].items():
                self.group_forward.insert('', 'end', values=(
                    k, data_global[self.wxid]["chatroom_nickname"][v["group_listen"]], '11',
                    data_global[self.wxid]["chatroom_nickname"][v["group_reply"]], '22'))
            id_list = list(data_global[self.wxid]["listen_relationship"].keys())
            if id_list:
                listen_index += id_list[-1]
            self.spy.query_contact_list(step=50, pid=pid)
        elif m_type == 3:
            for contact in data["data"]:
                if contact["wxid"].endswith("@chatroom"):
                    data_global[self.wxid]["chatroom_nickname"][contact["wxid"]] = contact["nickname"]
                    if not data_global[self.wxid]["pid_chatroom"].get(pid):
                        data_global[self.wxid]["pid_chatroom"][pid] = [contact]
                    else:
                        data_global[self.wxid]["pid_chatroom"][pid].append(contact)
            if data["total_page"] == data["current_page"]:
                self.label_log["text"] = "联系人加载完成"
        elif m_type == 4:
            data_global[self.wxid]["chatroom_member"][data["wxid"]] = data["data"]
            for member in data["data"]:
                data_global[self.wxid]["member_nickname"][member["wxid"]] = member["nickname"]
        elif m_type == 5:
            if pid == self.pid:
                for message in data["data"]:
                    if message["msg_type"] == 1:
                        wxid1 = message["wxid1"]
                        wxid2 = message.get("wxid2")
                        content = message["content"]
                        if wxid2:
                            for listen in data_global[self.wxid]["listen_relationship"].values():
                                if wxid1 == listen["group_listen"] and wxid2 in listen["member_listen"]:
                                    wxid_forward = listen["group_reply"]
                                    group_nickname = data_global[self.wxid]["chatroom_nickname"][wxid1]
                                    speaker_nickname = data_global[self.wxid]["member_nickname"][wxid2]
                                    content = f"鲁班转发：[{group_nickname}]{speaker_nickname}：{content}"
                                    self.spy.send_text(wxid_forward, content, pid=self.pid)
                                elif wxid1 == listen["group_reply"] and wxid2 in listen["member_reply"]:
                                    wxid_forward = listen["group_listen"]
                                    group_nickname = data_global[self.wxid]["chatroom_nickname"][wxid1]
                                    speaker_nickname = data_global[self.wxid]["member_nickname"][wxid2]
                                    content = f"鲁班转发：[{group_nickname}]{speaker_nickname}：{content}"
                                    self.spy.send_text(wxid_forward, content, pid=self.pid)

    def open_wechat(self):
        self.pid = self.spy.run(background=True)

    def select_group_listen(self):
        if not self.wxid:
            self.label_log["text"] = "请先登录微信"
            return
        self.tl = tkinter.Toplevel(self.tk)
        self.tl.title("选择监听群")
        self.tl.geometry('250x80+300+300')
        self.tl.resizable(0, 0)
        self.combobox_group_listen = ttk.Combobox(self.tl)
        self.combobox_group_listen['value'] = [f"{i['nickname']}[{i['wxid']}]" for i in data_global[self.wxid]["pid_chatroom"][self.pid]]
        self.combobox_group_listen.pack(pady=10)
        button_next = tkinter.Button(self.tl, text="下一步", command=self.select_group_member_listen)
        button_next.pack()

    def select_group_member_listen(self):
        self.group_listen = self.combobox_group_listen.get()
        self.tl.destroy()
        self.group_listen = re.search(r'(?<=\[).*?(?=\])', self.group_listen).group()
        self.spy.query_chatroom_member(self.group_listen, self.pid)
        while True:
            if data_global[self.wxid]["chatroom_member"].get(self.group_listen):
                self.group_members = [f"{i['nickname']}[{i['wxid']}]" for i in data_global[self.wxid]["chatroom_member"][self.group_listen]]
                break
            sleep(0.1)
        self.tl = tkinter.Toplevel(self.tk)
        self.tl.title("选择监听群成员")
        self.tl.geometry('200x250+300+300')
        self.tl.resizable(0, 0)
        self.listbox_member_listen = tkinter.Listbox(self.tl, selectmode=tkinter.MULTIPLE)
        self.listbox_member_listen.pack()
        for member in self.group_members:
            self.listbox_member_listen.insert("end", member)
        self.check_member_listen = ttk.Checkbutton(self.tl, text="全选1", command=self.select_all_member_listen)
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
        for i in self.listbox_member_listen.selection_get().split("\n"):
            self.members_listen.append(re.search(r'(?<=\[).*?(?=\])', i).group())
        self.tl.destroy()
        self.tl = tkinter.Toplevel(self.tk)
        self.tl.title("选择转发群")
        self.tl.geometry('250x80+300+300')
        self.tl.resizable(0, 0)
        self.combobox_group_reply = ttk.Combobox(self.tl)
        self.combobox_group_reply['value'] = [f"{i['nickname']}[{i['wxid']}]" for i in data_global[self.wxid]["pid_chatroom"][self.pid]]
        self.combobox_group_reply.pack(pady=10)
        button_next = tkinter.Button(self.tl, text="下一步", command=self.select_group_member_reply)
        button_next.pack()

    def select_group_member_reply(self):
        self.group_reply = self.combobox_group_reply.get()
        self.group_reply = re.search(r'(?<=\[).*?(?=\])', self.group_reply).group()
        if self.group_listen == self.group_reply:
            self.label_log["text"] = "监听群与转发群不允许相同"
        else:
            self.tl.destroy()
            self.spy.query_chatroom_member(self.group_reply, self.pid)
            while True:
                if data_global[self.wxid]["chatroom_member"].get(self.group_reply):
                    self.group_members = [f"{i['nickname']}[{i['wxid']}]" for i in data_global[self.wxid]["chatroom_member"][self.group_reply]]
                    break
                sleep(0.1)
            self.tl = tkinter.Toplevel(self.tk)
            self.tl.title("选择转发回复群成员")
            self.tl.geometry('200x250+300+300')
            self.tl.resizable(0, 0)
            self.listbox_member_reply = tkinter.Listbox(self.tl, selectmode=tkinter.MULTIPLE)
            self.listbox_member_reply.pack()
            for member in self.group_members:
                self.listbox_member_reply.insert("end", member)
            self.check_member_reply = ttk.Checkbutton(self.tl, text="回复全选", command=self.select_all_member_reply)
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
        global listen_index
        self.select_all_reply = False
        for i in self.listbox_member_reply.selection_get().split("\n"):
            self.members_reply.append(re.search(r'(?<=\[).*?(?=\])', i).group())
        self.tl.destroy()
        listen_relationship = {
            "group_listen": self.group_listen,
            "member_listen": self.members_listen,
            "group_reply": self.group_reply,
            "member_reply": self.members_reply
        }
        data_global[self.wxid]["listen_relationship"][listen_index] = listen_relationship
        with open("data.pkl", "wb") as wf:
            pickle.dump(data_global, wf)
        self.group_forward.insert('', 'end', values=(listen_index, data_global[self.wxid]["chatroom_nickname"][self.group_listen], '11', data_global[self.wxid]["chatroom_nickname"][self.group_reply], '22'))
        listen_index += 1

    def delete_listen_relationship(self):
        if not self.wxid:
            self.label_log["text"] = "请先登录微信"
            return
        selected_items = self.group_forward.selection()
        listen_id = self.group_forward.item(selected_items)["values"][0]
        for item in selected_items:
            self.group_forward.delete(item)
        data_global[self.wxid]["listen_relationship"].pop(listen_id)
        with open("data.pkl", "wb") as wf:
            pickle.dump(data_global, wf)


if __name__ == '__main__':
    postman = Postman()
    postman.tk.mainloop()