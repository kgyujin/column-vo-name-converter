import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import re

class StringConverter(ThemedTk):
    def __init__(self):
        super().__init__(theme="arc")  # Use the "arc" theme

        self.title('Column And VO Name Converter')
        self.iconbitmap('nameConverter.ico')
        self.create_widgets()

    def create_widgets(self):
        # Create a frame for the buttons
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(fill=tk.X)

        # self.entry_label = ttk.Label(self, text='Enter strings:')
        # self.entry_label.pack()

        # Input Convert Button 
        self.result_button = ttk.Button(self.button_frame, text='Convert', command=self.show_result)
        self.result_button.grid(row=0, column=0)

        # Convert to Column Format #{}
        self.format_button = ttk.Button(self.button_frame, text='#{} Convert', command=self.format_result)
        self.format_button.grid(row=0, column=1)

        # Convert to Column Format #{} for Update DAO
        self.format_button = ttk.Button(self.button_frame, text='#{} Convert(U)', command=self.format_result_update)
        self.format_button.grid(row=0, column=2)

        # Add comma button 
        self.comma_button = ttk.Button(self.button_frame,text='Add Comma',command=self.add_comma)
        self.comma_button.grid(row=0, column=3)

        # Add 'Select All' button with toggle functionality
        self.selectall_button = ttk.Button(self.button_frame,text='Select All',command=self.toggle_select_all)
        self.selectall_button.grid(row=0, column=4)

        # Add 'Always on Top' button with toggle functionality
        self.always_on_top_button = ttk.Button(self.button_frame,text='Pin',command=self.toggle_always_on_top)
        self.always_on_top_button.grid(row=0, column=5)

        # Create a 'Reset' button
        self.reset_button = ttk.Button(self.button_frame, text='Reset', command=self.reset)
        self.reset_button.grid(row=0, column=6)

        self.text = tk.Text(self)
        self.text.pack(side=tk.LEFT, fill=tk.Y)

        # Create a Listbox for the results.
        self.listbox = tk.Listbox(self, selectmode=tk.MULTIPLE)

        # Pack the list box into the window
        self.listbox.pack(side=tk.RIGHT, fill=tk.Y)

        # Add a Scrollbar to the Listbox.
        scrollbar = ttk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Link Scrollbar movement to Listbox movement.
        scrollbar.config(command=self.listbox.yview) 

        # Link Listbox movement to Scrollbar movement.
        self.listbox.config(yscrollcommand=scrollbar.set) 

        # Add mouse event bindings for list box drag selection 
        self.listbox.bind("<B1-Motion>", lambda event: self.toggle_selection(event))
        
    
    def toggle_selection(self,event):
        # Get index of item nearest to cursor position 
        index = self.listbox.nearest(event.y)
        if index in self.listbox.curselection():
            # If item is already selected - deselect it 
            self.listbox.selection_clear(index)
        else:
            # If item is not selected - select it 
            self.listbox.selection_set(index)

    def convert_string(self, input_str):
        if input_str.islower():
            return input_str.upper()
        elif input_str.isupper():
            return input_str.lower()
        elif '_' not in input_str and any(x.isupper() for x in input_str):
            words = re.findall(r'[A-Z]?[a-z]+|[A-Z]+[0-9]*|[A-Z]+(?=[A-Z]|$)', input_str)  # Include numbers in word pattern
            result = '_'.join(word.upper() for word in words)
        else:
            words = [word.capitalize() for word in input_str.lower().split('_')]
            result = ''.join(words)

        return result

    def show_result(self):
        lines=self.text.get('1.0', 'end').splitlines()
        converted_lines=[self.convert_string(line) for line in lines]
        
        # Clear the list box before adding new results
        self.listbox.delete(0,'end')
        
        for line in converted_lines:
            if line:  # Only add non-empty lines to the list box
                self.listbox.insert(tk.END,line)

    def format_result(self):
        items = self.listbox.get(0, tk.END)
        formatted_items = [f'#{{{item}}}' for item in items]  # Modify to '#{item}'

        # Clear the list box before adding new results
        self.listbox.delete(0, 'end')

        for item in formatted_items:
            if item:  # Only add non-empty lines to the list box
                self.listbox.insert(tk.END,item)
                
    def format_result_update(self):
        lines = self.text.get('1.0', 'end').splitlines()
        items = self.listbox.get(0, tk.END)
        
        if len(lines) != len(items):
            print("Error: The number of input and output lines do not match.")
            return

        formatted_items = [f',{line} = {item}' for line, item in zip(lines, items)]

        # Clear the text box before adding new results
        self.text.delete('1.0', 'end')
        
        for item in formatted_items:
            if item:  # Only add non-empty lines to the text box
                self.text.insert(tk.END, item + '\n')

    def add_comma(self):
        # Add comma at beginning of second line and after of text entry 
        text_content=self.text.get('1.0','end').split('\n')
        if len(text_content)>1:
            for i in range(1, len(text_content)):
                text_content[i]=','+text_content[i]
            updated_text='\n'.join(text_content)
            self.text.delete('1.0','end')
            self.text.insert('1.0',updated_text)

        # Add comma at beginning of second line and after of list box content 
        list_content=list(self.listbox.get(0,'end'))
        
        if len(list_content)>1:
            for i in range(1, len(list_content)):
                list_content[i]=','+list_content[i]

            # Clear the list box before adding updated content 
            self.listbox.delete(0, 'end')

            for item in list_content:
                if item:  # Only add non-empty lines to the list box
                    self.listbox.insert(tk.END,item)

    def toggle_select_all(self):
        # Check if all items are selected
        if self.listbox.curselection() == tuple(range(self.listbox.size())):
            # If all items are selected, deselect all
            self.listbox.selection_clear(0, tk.END)
            self.selectall_button.config(text='Select All')
        else:
            # If not all items are selected, select all
            self.listbox.select_set(0, tk.END)
            self.selectall_button.config(text='Disabled Select All')
    
    def toggle_always_on_top(self):
        if not bool(self.attributes('-topmost')):
            # If window is not always on top, make it always on top.
            self.attributes('-topmost', 1)
            self.always_on_top_button.config(text='Disable Pin')
        else:
            # If window is always on top, make it normal.
            self.attributes('-topmost', 0)
            self.always_on_top_button.config(text='Pin')
    
    def reset(self):
        # Clear the text box and listbox
        self.text.delete('1.0', 'end')
        self.listbox.delete(0, tk.END)

if __name__ == "__main__":
    app=StringConverter()
    app.mainloop()