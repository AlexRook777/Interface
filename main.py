import customtkinter  
import tkinter
        
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue") 

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        #initialize variables
        self.contacts = {}  # Dictionary to store contacts  
        self.contact_name = ""
        self.contact_phone = ""

    
        # Initialize the main application window
        self.title("Simple phone book")
        self.geometry("620x400")
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        # Configure root grid layout (1x1 to place the main frame)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ----------- Create a frame to hold the widgets -----------
        # Create the main frame. This will act as a container for other UI elements.
        self.main_frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        # Configure grid layout for the main_frame itself (e.g., 2 rows, 2 columns for demonstration)
        # This allows widgets inside main_frame to be placed using their own grid.
        self.main_frame.grid_columnconfigure((0, 1, 3), weight=0)
        self.main_frame.grid_rowconfigure((0,1,2,3,4,5), weight=0) 
        # Configure grid layout for the main_frame itself (e.g., 2 rows, 2 columns for demonstration)
        # This allows widgets inside main_frame to be placed using their own grid.
        self.main_frame.grid_columnconfigure((0, 1, 3), weight=0)
        self.main_frame.grid_rowconfigure((0,1,2,3,4,5), weight=0) 
        #-----------

        # Create radio buttons
        # Create a control variable
        self.radio_var = tkinter.StringVar(value="hello")
        
        self.radio_button_label = customtkinter.CTkLabel(self.main_frame, text="Select the action:")
        self.radio_button_label.grid(row=0, column=0,  pady=10, padx=10, sticky="n")
        
        # Create radio buttons with shared variable
        self.radio_var_hello = customtkinter.CTkRadioButton(self.main_frame, text="Say hello", value="hello", variable=self.radio_var)
        self.radio_var_hello.grid(row=1, column=0,  pady=10, padx=10, sticky="nw")

        self.radio_var_add = customtkinter.CTkRadioButton(self.main_frame, text="Add contact", value="add", variable=self.radio_var)
        self.radio_var_add.grid(row=2, column=0,  pady=10, padx=10, sticky="nw")

        self.radio_var_change = customtkinter.CTkRadioButton(self.main_frame, text="Edit phone", value="change", variable=self.radio_var)
        self.radio_var_change.grid(row=3, column=0,  pady=10, padx=10, sticky="nw")

        self.radio_var_phone = customtkinter.CTkRadioButton(self.main_frame, text="Show phone", value="phone", variable=self.radio_var)
        self.radio_var_phone.grid(row=4, column=0,  pady=10, padx=10, sticky="nw")

        self.radio_var_all = customtkinter.CTkRadioButton(self.main_frame, text="Show all", value="show_all", variable=self.radio_var)
        self.radio_var_all.grid(row=5, column=0, pady=10, padx=10, sticky="nw")

        # Create a label and entry for contact name and phone
        self.contact_name_label = customtkinter.CTkLabel(self.main_frame, text="Enter contact's name:")
        self.contact_name_label.grid(row=0, column=1, pady=10, padx=10, sticky="nw")

        self.contact_name_entry = customtkinter.CTkEntry(self.main_frame)
        self.contact_name_entry.grid(row=1, column=1, pady=10, padx=10, sticky="nw")

        self.contact_phone_label = customtkinter.CTkLabel(self.main_frame, text="Enter contact's phone:")
        self.contact_phone_label.grid(row=2, column=1, pady=10, padx=10, sticky="nw")

        self.contact_phone_entry = customtkinter.CTkEntry(self.main_frame)
        self.contact_phone_entry.grid(row=3, column=1, pady=10, padx=10, sticky="nw")

        # create a text box to display contacts in the third column
        self.contact_box_label = customtkinter.CTkLabel(self.main_frame, text="Contact list:")
        self.contact_box_label.grid(row=0, column=2, pady=10, padx=10, sticky="nw")

        self.contact_box = customtkinter.CTkTextbox(self.main_frame, width=300, height=220, state="disabled")    
        self.contact_box.grid(row=1, column=2, rowspan=6, pady=10, padx=10, sticky="nw")

        # Create a button to submit the action
        self.submit_button = customtkinter.CTkButton(self.main_frame, text="Submit", command=self.on_submit)
        self.submit_button.grid(row=5, column=1, pady=10, padx=10, sticky="nw")
        
        self.log_box = customtkinter.CTkTextbox(self.main_frame, width=300, height=80, state="disabled")
        self.log_box.grid(row=6, column=0, columnspan=3, pady=10, padx=10, sticky="we")    

        self.refresh_contact_box()

    def on_submit(self):
        case_action = self.radio_var.get()
        self.contact_name = self.contact_name_entry.get().strip()
        self.contact_phone = self.contact_phone_entry.get().strip()
        if case_action == "add":
            # If the action is "add", add the contact to the contact box
            self.add_contact()
            
    
        # Clear the entry fields
        self.contact_name_entry.delete(0, "end")
        self.contact_phone_entry.delete(0, "end")


    def add_contact(self):# Function to add a new contact
        #Validate the input
        if not self.contact_name or not self.contact_phone:
            self.output_log("Error: Name and phone cannot be empty.")
            return
        if self.contact_name in self.contacts:
            self.output_log(f"Warning: Contact {self.contact_name} already exist. Use command 'change' to update the contact.")
            return
        # Add the contact to the contacts dictionary in case all the validations are passed
        self.contacts[self.contact_name] = self.contact_phone
        self.output_log(f"Action: {self.radio_var.get()}, Name: {self.contact_name}, Phone: {self.contact_phone}")
        self.refresh_contact_box()

    def refresh_contact_box(self):
        # Clear the contact box
        self.contact_box.configure(state="normal")  
        self.contact_box.delete("1.0", "end")
        # Populate the contact box with the contacts
        # If there are no contacts, display a message
        if not self.contacts:
            self.contact_box.insert("end", "No contacts available.\nPlease, add a contact first.")
        else:
            for name, phone in self.contacts.items():
                self.contact_box.insert("end", f"{name}: {phone}\n")
        self.contact_box.configure(state="disabled") 
        self.contact_box.see("end")
        
    def output_log(self, message):
        self.log_box.configure(state="normal")  
        self.log_box.insert("end", message + "\n")
        self.log_box.configure(state="disabled")
        self.log_box.see("end")



if __name__ == "__main__":
    app = App()
    app.mainloop()  
    