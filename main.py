import customtkinter as ctk
from tkinter import filedialog, messagebox
import os

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Text Editor")
        self.iconbitmap("images/icon.ico")
        self.minsize(width=900,height=600)
        self.maxsize(width=900,height=600)
        self.configure(padx=10,pady=10)

        self.file_box = None
        self.file_tabview = None
        self.tabs = {}

        self.button_list = [
            ("Pack File", self.pack_file),
            ("Create File", self.create_file),
            ("Remove File", self.remove_file),
            ("Delete File",self.delete_file),
            ("Save", self.save),
            ("Clear", self.clear)
        ]

        self.ui()

    def ui(self):
        x=0.0
        for button_tuple in self.button_list:
            button = ctk.CTkButton(self,text=button_tuple[0], fg_color="#4a4848", hover_color="#706c6c", width=90, command=button_tuple[1])
            button.place(relx=x,rely=0.01)
            x += 0.11

        self.file_box = ctk.CTkScrollableFrame(self,width=280,height=530)
        self.file_box.place(relx=0.0,rely=0.075)

        self.file_tabview = ctk.CTkTabview(self,width=570,height=530)
        self.file_tabview.place(relx=0.35,rely=0.075)

    def create_list_element(self, file_path, file_name):
        try:
            button = ctk.CTkButton(self.file_box, text=file_name, fg_color="transparent", hover_color="#4a4848", command=lambda: self.open_file(file_path, file_name))
            return button
        except Exception as error:
            messagebox.showerror("Error",f"{error}")

    def pack_file(self):
        try:
            button_text_list = list()
            for button in self.file_box.winfo_children():
                button_text = button.cget("text")
                button_text_list.append(button_text)

            file_path = filedialog.askopenfilename()
            file_name = os.path.basename(file_path)
            if file_path and file_name:
                if file_name not in button_text_list:
                    button = self.create_list_element(file_path,file_name)
                    button.pack()
                else:
                    messagebox.showinfo("Warning",f"{file_name} already in list")
        except Exception as error:
            messagebox.showerror("Error",f"{error}")

    def open_file(self,file_path,file_name):
        try:
            tab = self.file_tabview.add(file_name)
            textbox = ctk.CTkTextbox(tab, width=520, height=470, padx=10, pady=10, font=('Arial', 14, 'normal'))

            with open(file_path, "r") as file_read:
                text = file_read.read()
            textbox.insert(ctk.END, text)
            textbox.pack()

            self.tabs[file_name] = {"textbox":textbox,"file_path":file_path}
            self.file_tabview.set(file_name)
        except: pass

    def create_file(self):
        try:
            folder = filedialog.askdirectory()
            if folder:
                file_name_input = ctk.CTkInputDialog(title="File Name Input", text="Enter File Name With Extension")
                file_name = file_name_input.get_input()
                file_path = os.path.join(folder, file_name)
                with open(file_path, "w") as create_file:
                    create_file.write("")

                button = self.create_list_element(file_path, file_name)
                button.pack()
        except Exception as error:
            messagebox.showerror("Error",f"{error}")

    def remove_file(self):
        try:
            active_tab = self.file_tabview.get()
            if active_tab in self.tabs:
                self.file_tabview.delete(active_tab)
                del self.tabs[active_tab]
                for button in self.file_box.winfo_children():
                    if button.cget("text") == active_tab:
                        button.destroy()
                        break
        except Exception as error:
            messagebox.showerror("Error", f"{error}")

    def delete_file(self):
        try:
            active_tab = self.file_tabview.get()
            if active_tab.strip():
                confirm = messagebox.askyesno("Delete File",f"Are you sure for delete {active_tab}")
                if confirm and (active_tab in self.tabs):
                    deleted_file_path = self.tabs[active_tab]["file_path"]
                    os.remove(deleted_file_path)
                    self.remove_file()
                    messagebox.showinfo("Success",f"{active_tab} successfully deleted")
        except Exception as error:
            messagebox.showerror("Error", f"{error}")

    def save(self):
        try:
            active_tab = self.file_tabview.get()
            if active_tab in self.tabs:
                saved_file = self.tabs[active_tab]
                textbox = saved_file["textbox"]
                file_path = saved_file["file_path"]
                text = textbox.get("1.0",ctk.END)
                with open(file_path, "w") as save_file:
                    save_file.write(text)
        except Exception as error:
            messagebox.showerror("Error",f"{error}")

    def clear(self):
        try:
            for tab_name in self.tabs:
                self.file_tabview.delete(tab_name)
            for button in self.file_box.winfo_children():
                button.destroy()
            self.tabs.clear()
        except Exception as error:
            messagebox.showerror("Error",f"{error}")

if __name__ == "__main__":
    window = App()
    window.mainloop()