import tkinter
from tkinter import ttk, messagebox
from PyWeChatSpy import WeChatSpy
from time import sleep, time
from datetime import datetime
import logging
import pickle
import shutil
import re
import os
import copy

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
sh = logging.StreamHandler()
sh.setFormatter(formatter)
sh.setLevel(logging.INFO)
fh = logging.FileHandler("post.log", mode="w", encoding="utf8")
fh.setFormatter(formatter)
fh.setLevel(logging.INFO)
logger.addHandler(sh)
logger.addHandler(fh)

data_global = {}
listen_index = 1
if os.path.exists("data.pkl"):
    logger.info("加载数据。。。")
    with open("data.pkl", "rb") as rf:
        data_global = pickle.load(rf)


def record(chatroom, speaker, content, forward):
    file_name = "records/{}.csv".format(datetime.now().strftime("%Y%m%d"))
    _content = "{},{},{},{},{}\n".format(datetime.now().strftime("%H:%M:%S"), chatroom, speaker, content, forward)
    try:
        with open(file_name, "a", errors="ignore") as wf:
            wf.write(_content)
    except Exception as e:
        logger.error(f"record {_content} failed:{e}")


class Postman:
    def __init__(self):
        self.tk = tkinter.Tk()
        self.tk.protocol('WM_DELETE_WINDOW', self.quit)
        self.tk.title("鲁班转发助手")
        self.tk.geometry('600x400+200+200')
        self.tk.resizable(0, 0)
        self.label_nickname = tkinter.Label(self.tk, text="昵称:")
        self.label_nickname.pack()
        self.frame_group = tkinter.LabelFrame(self.tk, text="转发关系", padx=5, pady=5)
        self.frame_group.place(x=10, y=20)
        self.group_forward = ttk.Treeview(self.frame_group, show="headings", columns=('col0', 'col1', 'col2', 'col3'))
        self.group_forward.heading('col0', text='ID')
        self.group_forward.heading('col1', text='监听群')
        self.group_forward.heading('col2', text='转发群')
        self.group_forward.heading('col3', text='监听详情')
        self.group_forward.column('col0', width=20, anchor='center')
        self.group_forward.column('col1', width=180, anchor='center')
        self.group_forward.column('col2', width=180, anchor='center')
        self.group_forward.column('col3', width=120, anchor='center')
        self.group_forward.pack()
        self.group_forward.bind('<ButtonRelease-1>', self.show_listen_details)
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
        self.spy = WeChatSpy(parser=self.parser, multi=True, download_image=True)
        self.wxid = None

    def parser(self, data):
        global listen_index
        m_type = data.pop("type")
        pid = data.pop("pid")
        if m_type == 1:
            self.wxid = data["wxid"]
            logger.info("{}登录成功".format(self.wxid))
            self.label_log["text"] = "登录成功"
            if not data_global.get(self.wxid):
                logger.info("创建空白数据模板")
                data_global[data["wxid"]] = {
                    "listen_relationship": {},
                    "chatroom": set(),
                    "chatroom_nickname": {},
                    "chatroom_member": {},
                    "member_nickname": {}
                }
            for k, v in data_global[self.wxid]["listen_relationship"].items():
                self.group_forward.insert('', 'end', values=(
                    k, data_global[self.wxid]["chatroom_nickname"][v["group_listen"]],
                    data_global[self.wxid]["chatroom_nickname"][v["group_reply"]], '点击查看'))
            id_list = list(data_global[self.wxid]["listen_relationship"].keys())
            if id_list:
                listen_index += id_list[-1]
            logger.info("开始加载联系人列表...")
            self.spy.query_contact_list(step=50, pid=pid)
        elif m_type == 3:
            for contact in data["data"]:
                if contact["wxid"].endswith("@chatroom"):
                    data_global[self.wxid]["chatroom_nickname"][contact["wxid"]] = contact["nickname"]
                    data_global[self.wxid]["chatroom"].add("{}[{}]".format(contact["nickname"], contact["wxid"]))
            logger.info("加载联系人{}/{}".format(data["current_page"], data["total_page"]))
            if data["total_page"] == data["current_page"]:
                logger.info("联系人加载完成")
                self.label_log["text"] = "联系人加载完成"
        elif m_type == 4:
            data_global[self.wxid]["chatroom_member"][data["wxid"]] = data["data"]
            for member in data["data"]:
                data_global[self.wxid]["member_nickname"][member["wxid"]] = member["nickname"]
            logger.info("群{}成员加载完成".format(data["wxid"]))
        elif m_type == 5:
            if pid == self.pid:
                for message in data["data"]:
                    logger.info(f"接收到待分析消息:{message}")
                    wxid1 = message["wxid1"]
                    wxid2 = message.get("wxid2")
                    head = message.get("head")
                    if not message["self"] and wxid2:
                        logger.info(f"==========================[{wxid1}]{wxid2}==========================")
                        for listen_id, listen in data_global[self.wxid]["listen_relationship"].items():
                            logger.info(f"-------------------{listen_id}-------------------")
                            logger.info(f"chatroom_listen:{listen['group_listen']}")
                            logger.info(f"chatroom_reply:{listen['group_reply']}")
                            logger.info(f"member_listen:{listen['member_listen']}")
                            logger.info(f"member_reply:{listen['member_reply']}")
                            group_nickname = speaker_nickname = wxid_forward = None
                            at_wxid = at_nickname = ""
                            if wxid1 == listen["group_listen"] and wxid2 in listen["member_listen"]:
                                logger.info("message from chatroom_listen")
                                wxid_forward = listen["group_reply"]
                                group_nickname = data_global[self.wxid]["chatroom_nickname"][wxid1]
                                speaker = listen["member_listen"].index(wxid2) + 1
                                speaker_nickname = "用户{}".format(speaker)
                                if self.wxid in head:
                                    at_wxid = ",".join(listen["member_reply"])
                                    for member in listen["member_reply"]:
                                        at_nickname += "@{} ".format(data_global[self.wxid]["member_nickname"][member])
                            elif wxid1 == listen["group_reply"] and wxid2 in listen["member_reply"]:
                                logger.info("message from chatroom_reply")
                                wxid_forward = listen["group_listen"]
                                group_nickname = data_global[self.wxid]["chatroom_nickname"][wxid1]
                                speaker = listen["member_reply"].index(wxid2) + 1
                                speaker_nickname = "用户{}".format(speaker)
                                if self.wxid in head:
                                    at_wxid = ",".join(listen["member_listen"])
                                    for member in listen["member_listen"]:
                                        at_nickname += "@{} ".format(data_global[self.wxid]["member_nickname"][member])
                            if group_nickname and speaker_nickname and wxid_forward:
                                logger.info(f"message from [{group_nickname}]{speaker_nickname} to {wxid_forward}")
                                if message["msg_type"] == 1:
                                    content = message["content"]
                                    if at_wxid:
                                        content = re.sub("(?=@).*?(?= )", "", content, 1)
                                    record(group_nickname, speaker_nickname, content,
                                           data_global[self.wxid]["chatroom_nickname"][wxid_forward])
                                    _content = "转发[{}]{}:\n-----------\n{} {}".format(group_nickname, speaker_nickname, at_nickname, content)
                                    logger.info(_content)
                                    self.spy.send_text(wxid_forward, _content, at_wxid=at_wxid, pid=self.pid)
                                elif message["msg_type"] in (3, 43):
                                    dst_path = None
                                    if message["msg_type"] == 3:
                                        image_path = message.get("image_path")
                                        if image_path:
                                            dst_path = os.path.join(os.getcwd(), r"images\{}.jpg".format(int(time())))
                                            while True:
                                                try:
                                                    shutil.move(image_path, dst_path)
                                                    break
                                                except FileNotFoundError:
                                                    sleep(10)
                                                except PermissionError:
                                                    sleep(1)
                                            record(group_nickname, speaker_nickname, dst_path,
                                                   data_global[self.wxid]["chatroom_nickname"][wxid_forward])
                                            _content = "转发:[{}]{}\n-----------\n图片".format(group_nickname, speaker_nickname)
                                            logger.info(_content)
                                            self.spy.send_text(wxid_forward, _content, pid=self.pid)
                                    elif message["msg_type"] == 43:
                                        video_path = message.get("video_path")
                                        if video_path:
                                            dst_path = os.path.join(os.getcwd(), r"videos\{}.mp4".format(int(time())))
                                            while True:
                                                try:
                                                    shutil.move(video_path, dst_path)
                                                    break
                                                except FileNotFoundError:
                                                    sleep(10)
                                                except PermissionError:
                                                    sleep(1)
                                            record(group_nickname, speaker_nickname, dst_path,
                                                   data_global[self.wxid]["chatroom_nickname"][wxid_forward])
                                            _content = "转发:[{}]{}\n-----------\n视频".format(group_nickname, speaker_nickname)
                                            logger.info(_content)
                                            self.spy.send_text(wxid_forward, _content, pid=self.pid)
                                    if dst_path:
                                        logger.info(dst_path)
                                        self.spy.send_file(wxid_forward, dst_path, self.pid)
                                else:
                                    _content = "转发:[{}]{}\n-----------\n不支持的消息类型".format(group_nickname, speaker_nickname)
                                    logger.info(_content)
                                    self.spy.send_text(wxid_forward, _content, pid=self.pid)
                                break

    def open_wechat(self):
        self.pid = self.spy.run(background=True)
        logger.info("打开微信:{}".format(self.pid))

    def select_group_listen(self):
        if not self.wxid:
            self.label_log["text"] = "请先登录微信"
            return
        self.tl = tkinter.Toplevel(self.tk)
        self.tl.title("选择监听群")
        self.tl.geometry('250x110+300+300')
        self.tl.resizable(0, 0)
        sv = tkinter.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv: self.query_group_listen(sv))
        enter_group_listen = ttk.Entry(self.tl, width=200, textvariable=sv)
        enter_group_listen.pack(pady=2)
        self.combobox_group_listen = ttk.Combobox(self.tl)
        self.combobox_group_listen.pack(pady=11)
        self.combobox_group_listen['value'] = [i for i in data_global[self.wxid]["chatroom"]]
        button_next = tkinter.Button(self.tl, text="下一步", command=self.select_group_member_listen)
        button_next.pack()

    def select_group_member_listen(self):
        self.group_listen = self.combobox_group_listen.get()
        logger.info("选择监听群：{}".format(self.group_listen))
        self.tl.destroy()
        self.group_listen = re.search(r'(?<=\[).*?(?=\])', self.group_listen).group()
        logger.info("查询群{}成员".format(self.group_listen))
        self.spy.query_chatroom_member(self.group_listen, self.pid)
        for i in range(300):
            if data_global[self.wxid]["chatroom_member"].get(self.group_listen):
                self.group_members = ["{}[{}]".format(i['nickname'], i['wxid'])
                                      for i in data_global[self.wxid]["chatroom_member"][self.group_listen]]
                break
            sleep(0.1)
        else:
            logger.warning("查询群{}成员超时".format(self.group_listen))
            messagebox.showwarning("错误", "群成员加载超时")
        self.tl = tkinter.Toplevel(self.tk)
        self.tl.title("选择监听群成员")
        self.tl.geometry('200x250+300+300')
        self.tl.resizable(0, 0)
        self.listbox_member_listen = tkinter.Listbox(self.tl, selectmode=tkinter.MULTIPLE)
        self.listbox_member_listen.pack()
        self.listbox_member_listen.selection_clear(0)
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
        self.tl.geometry('250x110+300+300')
        self.tl.resizable(0, 0)
        sv = tkinter.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv: self.query_group_reply(sv))
        enter_group_reply = ttk.Entry(self.tl, width=200, textvariable=sv)
        enter_group_reply.pack(pady=2)
        self.combobox_group_reply = ttk.Combobox(self.tl)
        self.combobox_group_reply['value'] = [i for i in data_global[self.wxid]["chatroom"]]
        self.combobox_group_reply.pack(pady=10)
        button_next = tkinter.Button(self.tl, text="下一步", command=self.select_group_member_reply)
        button_next.pack()

    def select_group_member_reply(self):
        self.group_reply = self.combobox_group_reply.get()
        logger.info("消息转发到群：{}".format(self.group_reply))
        self.group_reply = re.search(r'(?<=\[).*?(?=\])', self.group_reply).group()
        if self.group_listen == self.group_reply:
            logger.warning("监听群与转发群不允许相同")
            self.label_log["text"] = "监听群与转发群不允许相同"
        else:
            self.tl.destroy()
            logger.info("查询群{}成员".format(self.group_reply))
            self.spy.query_chatroom_member(self.group_reply, self.pid)
            for i in range(300):
                if data_global[self.wxid]["chatroom_member"].get(self.group_reply):
                    self.group_members = ["{}[{}]".format(i['nickname'], i['wxid'])
                                          for i in data_global[self.wxid]["chatroom_member"][self.group_reply]]
                    break
                sleep(0.1)
            else:
                logger.warning("查询群{}成员超时".format(self.group_listen))
                messagebox.showwarning("错误", "群成员加载超时")
            self.tl = tkinter.Toplevel(self.tk)
            self.tl.title("选择转发回复群成员")
            self.tl.geometry('200x250+300+300')
            self.tl.resizable(0, 0)
            self.listbox_member_reply = tkinter.Listbox(self.tl, selectmode=tkinter.MULTIPLE)
            self.listbox_member_reply.pack()
            self.listbox_member_reply.selection_clear(0)
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
        member_listen = copy.copy(self.members_listen)
        self.members_listen.clear()
        member_reply = copy.copy(self.members_reply)
        self.members_reply.clear()
        listen_relationship = {
            "group_listen": self.group_listen,
            "member_listen": member_listen,
            "group_reply": self.group_reply,
            "member_reply": member_reply
        }
        logger.info("添加监听关系：{}".format(listen_relationship))
        data_global[self.wxid]["listen_relationship"][listen_index] = listen_relationship
        with open("data.pkl", "wb") as wf:
            pickle.dump(data_global, wf)
        self.group_forward.insert(
            '',
            'end',
            values=(
                listen_index,
                data_global[self.wxid]["chatroom_nickname"][self.group_listen],
                data_global[self.wxid]["chatroom_nickname"][self.group_reply],
                '点击查看'
            )
        )
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

    def show_listen_details(self, event):
        listen_id = 0
        for item in self.group_forward.selection():
            item_text = self.group_forward.item(item, "values")
            listen_id = item_text[0]
        if listen_id:
            listen_id = int(listen_id)
            listen_relationship = data_global[self.wxid]["listen_relationship"].get(listen_id)
            self.tl = tkinter.Toplevel(self.tk)
            self.tl.title("监听转发详情")
            self.tl.geometry('400x250+300+300')
            self.tl.resizable(0, 0)
            group_listen_nickname = data_global[self.wxid]["chatroom_nickname"][listen_relationship["group_listen"]]
            group_reply_nickname = data_global[self.wxid]["chatroom_nickname"][listen_relationship["group_reply"]]
            frame_group_listen = tkinter.LabelFrame(self.tl, text=group_listen_nickname, padx=5, pady=5)
            frame_group_listen.place(x=10, y=20)
            listbox_member_listen = tkinter.Listbox(frame_group_listen)
            listbox_member_listen.pack()
            for member in listen_relationship["member_listen"]:
                nickname = data_global[self.wxid]["member_nickname"][member]
                listbox_member_listen.insert("end", nickname)
            frame_group_reply = tkinter.LabelFrame(self.tl, text=group_reply_nickname, padx=5, pady=5)
            frame_group_reply.place(x=200, y=20)
            listbox_member_reply = tkinter.Listbox(frame_group_reply)
            listbox_member_reply.pack()
            for member in listen_relationship["member_reply"]:
                nickname = data_global[self.wxid]["member_nickname"][member]
                listbox_member_reply.insert("end", nickname)

    def quit(self):
        logger.info("关闭微信:{}".format(self.pid))
        if self.pid:
            os.system("taskkill /pid {} -t -f".format(self.pid))
        self.tk.destroy()

    def query_group_listen(self, sv):
        self.combobox_group_listen["value"] = []
        group_listen = []
        for chatroom in data_global[self.wxid]["chatroom"]:
            if sv.get() in chatroom:
                group_listen.append(chatroom)
        self.combobox_group_listen["value"] = group_listen

    def query_group_reply(self, sv):
        self.combobox_group_reply["value"] = []
        group_reply = []
        for chatroom in data_global[self.wxid]["chatroom"]:
            if sv.get() in chatroom:
                group_reply.append(chatroom)
        self.combobox_group_reply["value"] = group_reply


if __name__ == '__main__':
    postman = Postman()
    postman.tk.mainloop()
