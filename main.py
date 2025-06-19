import customtkinter  
import tkinter
import json
import os
        
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue") 

# Decorator to log messages to both the GUI and console
def log_to_console(func):
    def wrapper(self, *args, **kwargs):
        # Get the original output_log method
        original_output_log = self.output_log
        
        # Create a new function that both logs to GUI and prints to console
        def enhanced_output_log(message):
            print(message)  # Print to console
            original_output_log(message)  # Log to GUI
            
        # Temporarily replace output_log with our enhanced version
        self.output_log = enhanced_output_log
        
        # Call the original function
        result = func(self, *args, **kwargs)
        
        # Restore the original output_log
        self.output_log = original_output_log
        
        return result
    return wrapper

# This is the main application class
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        #initialize variables
        self.contacts = {}  # Dictionary to store contacts  
        self.contact_name = ""
        self.contact_phone = ""

        # Load saved contacts
        self.load_contacts()

        # Initialize the main application window
        self.title("Simple phone book")
        self.geometry("620x420")
        self.resizable(False, False)  # Disable both horizontal and vertical resizing
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Configure root grid layout (1x1 to place the main frame)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ----------- Create a frame to hold the widgets -----------
        # Create the main frame. This will act as a container for other UI elements.
        self.main_frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=0, sticky="nw", padx=10, pady=10)
        # Configure grid layout for the main_frame
        self.main_frame.grid_columnconfigure((0, 1, 3), weight=0)
        self.main_frame.grid_rowconfigure((0,1,2,3,4,5), weight=0) 
        # Configure grid layout for the main_frame itself
        self.main_frame.grid_columnconfigure((0, 1, 3), weight=0)
        self.main_frame.grid_rowconfigure((0,1,2,3,4,5), weight=0) 
        #-----------

        # Create three column frames inside main_frame
        self.column1_frame = customtkinter.CTkFrame(self.main_frame, fg_color="transparent")
        self.column1_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        self.column2_frame = customtkinter.CTkFrame(self.main_frame, fg_color="transparent")
        self.column2_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nw")

        self.column3_frame = customtkinter.CTkFrame(self.main_frame, fg_color="transparent")
        self.column3_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nw")
        
        #-----------

        # Create radio buttons
        # Create a control variable
        self.radio_var = tkinter.StringVar(value="hello")
        
        # Column 1 - Radio buttons
        self.radio_button_label = customtkinter.CTkLabel(self.column1_frame, text="Select the action:")
        self.radio_button_label.grid(row=0, column=0, pady=(0,10), sticky="w")

        self.radio_var_hello = customtkinter.CTkRadioButton(self.column1_frame, text="Say hello", value="hello", variable=self.radio_var, command=self.configure_widget)
        self.radio_var_hello.grid(row=1, column=0, pady=5, sticky="w")
 
        self.radio_var_add = customtkinter.CTkRadioButton(self.column1_frame, text="Add contact", value="add", variable=self.radio_var, command=self.configure_widget)
        self.radio_var_add.grid(row=2, column=0, pady=5, sticky="w")

        self.radio_var_change = customtkinter.CTkRadioButton(self.column1_frame, text="Edit phone", value="change", variable=self.radio_var, command=self.configure_widget)
        self.radio_var_change.grid(row=3, column=0, pady=5, sticky="w")

        self.radio_var_phone = customtkinter.CTkRadioButton(self.column1_frame, text="Show phone", value="phone", variable=self.radio_var, command=self.configure_widget)
        self.radio_var_phone.grid(row=4, column=0, pady=5, sticky="w")

        self.radio_var_all = customtkinter.CTkRadioButton(self.column1_frame, text="Show all", value="show_all", variable=self.radio_var, command=self.configure_widget)
        self.radio_var_all.grid(row=5, column=0, pady=5, sticky="w")                        
 
        self.radio_var_sort = customtkinter.CTkRadioButton(self.column1_frame, text="Sort", value="sort", variable=self.radio_var, command=self.configure_widget)
        self.radio_var_sort.grid(row=6, column=0, pady=5, sticky="w")  

        # Create a button to submit the action
        self.submit_button = customtkinter.CTkButton(self.column1_frame, text="Submit", command=self.on_submit)
        self.submit_button.grid(row=7, column=0, pady=(10,5), sticky="w")
 
         # Column 2 - Entry fields
        self.contact_name_label = customtkinter.CTkLabel(self.column2_frame, text="Enter contact's name:")
        self.contact_name_label.grid(row=0, column=0, pady=(0,10), sticky="w")

        self.contact_name_entry = customtkinter.CTkEntry(self.column2_frame)
        self.contact_name_entry.grid(row=1, column=0, pady=5, sticky="w")

        self.contact_phone_label = customtkinter.CTkLabel(self.column2_frame, text="Enter contact's phone:")
        self.contact_phone_label.grid(row=2, column=0, pady=(10,5), sticky="w")

        self.contact_phone_entry = customtkinter.CTkEntry(self.column2_frame)
        self.contact_phone_entry.grid(row=3, column=0, pady=5, sticky="w")    

        # Column 3 - Text box
        self.contact_box_label = customtkinter.CTkLabel(self.column3_frame, text="Contact list:")
        self.contact_box_label.grid(row=0, column=0, pady=(0,10), sticky="w")

        self.contact_box = customtkinter.CTkTextbox(self.column3_frame, width=260, height=235, state="disabled")
        self.contact_box.grid(row=1, column=0, sticky="nsew")

        
      
        self.log_box = customtkinter.CTkTextbox(self.main_frame, width=300, height=80, state="disabled")
        self.log_box.grid(row=6, column=0, columnspan=3, pady=10, padx=10, sticky="news")    


        self.configure_widget()  
        self.refresh_contact_box(self.contacts)
        
    #----------- Function block for actions -----------
    def configure_widget(self):
        # Enable or disable the contact name and phone entry fields based on the selected action
        case_action = self.radio_var.get()
        if case_action in ["add", "change"]:
            self.contact_name_label.grid()
            self.contact_name_entry.grid()
            self.contact_phone_label.grid()
            self.contact_phone_entry.grid()
        elif case_action in ["hello", "phone"]:
            self.contact_name_label.grid()
            self.contact_name_entry.grid()
            self.contact_phone_label.grid_remove()
            self.contact_phone_entry.grid_remove()
        else:
            self.contact_name_label.grid_remove()
            self.contact_name_entry.grid_remove()
            self.contact_phone_label.grid_remove()
            self.contact_phone_entry.grid_remove()
        
        # Clear the entry fields when switching actions
        self.contact_name_entry.delete(0, "end")
        self.contact_phone_entry.delete(0, "end")
        self.contact_name = ""
        self.contact_phone = ""        

    def on_submit(self):
        case_action = self.radio_var.get()
        self.contact_name = self.contact_name_entry.get().strip().lower()
        self.contact_phone = ''.join(filter(str.isdigit, self.contact_phone_entry.get().strip()))
        if case_action == "add":
            # If the action is "add", add the contact to the contact box
            self.add_contact()
        elif case_action == "change":
            # If the action is "change", update the contact's phone number
            self.update_contact()
        elif case_action == "hello":
            # If the action is "hello", output a greeting message
            self.say_hello()
        elif case_action == "phone":
            self.phone_contact()
        elif case_action == "show_all":
            # If the action is "show_all", refresh the contact box to show all contacts
            self.show_all()
        elif case_action == "sort": 
            #  If the action is "sort", sort the contact list and refresh the contact box
            self.sort_contacts()
        else:
            self.output_log("Error: Unknown action selected.")

        # Clear the entry fields
        self.contact_name_entry.delete(0, "end")
        self.contact_phone_entry.delete(0, "end")
        self.contact_name = ""
        self.contact_phone = ""

    #----------- Block for handling actions -----------
    @log_to_console
    def say_hello(self):# Function to say hello
        self.output_log(f"Hello, {self.contact_name}!" if self.contact_name else "Hello!")

    @log_to_console
    def show_all(self):# Function to show all contacts
        self.output_log(f"Action: {self.radio_var.get()}")
        self.refresh_contact_box(self.contacts)

    @log_to_console
    def sort_contacts(self):# Function to sort contact list 
        self.contacts = dict(sorted(self.contacts.items()))
        self.refresh_contact_box(self.contacts)

    @log_to_console
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
        self.refresh_contact_box({self.contact_name: self.contact_phone})
        self.save_contacts()  # Save after adding

    @log_to_console
    def update_contact(self):
        # Validate the input
        if not self.contact_name or not self.contact_phone:
            self.output_log("Error: Name and phone cannot be empty.")
            return
        if self.contact_name not in self.contacts:
            self.output_log(f"Error: Contact {self.contact_name} does not exist. Use command 'add' to create a new contact.")
            return
        # Update the contact's phone number in case all the validations are passed
        self.contacts[self.contact_name] = self.contact_phone
        self.output_log(f"Action: {self.radio_var.get()}, Name: {self.contact_name}, Phone: {self.contact_phone}")  
        self.refresh_contact_box({self.contact_name: self.contact_phone})      
        self.save_contacts()  # Save after update

    @log_to_console
    def phone_contact(self):
        # Validate the input
        if not self.contact_name:
            self.output_log("Error: Name cannot be empty.")
            return
        if self.contact_name not in self.contacts:
            self.output_log(f"Error: Contact {self.contact_name} does not exist.")
            return
        # Output the contact's phone number
        phone = self.contacts[self.contact_name]
        self.output_log(f"Action: {self.radio_var.get()}, Name: {self.contact_name}, Phone: {phone}")
        self.refresh_contact_box({self.contact_name: phone}) 

    def refresh_contact_box(self, contacts_to_show={}):
        # Clear the contact box
        self.contact_box.configure(state="normal")  
        self.contact_box.delete("1.0", "end")
        # Populate the contact box with the contacts
        # If there are no contacts, display a message
        if not contacts_to_show:
            self.contact_box.insert("end", "No contacts to show available.\nPlease, add a contact first.")
        else:
            for name, phone in contacts_to_show.items():
                self.contact_box.insert("end", f"{name}: {phone}\n")
        self.contact_box.configure(state="disabled") 
        self.contact_box.see("end")

        if contacts_to_show != self.contacts:
            self.contact_box_label.configure(text="Contact list (filtered by last operation):")
        else:
            self.contact_box_label.configure(text="Contact list:")

    # Function to output log messages to the log box        
    def output_log(self, message):
        self.log_box.configure(state="normal")  
        self.log_box.insert("end", message + "\n")
        self.log_box.configure(state="disabled")
        self.log_box.see("end")

    def save_contacts(self):
        # Save contacts to a JSON file
        try:
            with open('phonebook.json', 'w', encoding='koi8-u') as f:
                json.dump(self.contacts, f, indent=4, ensure_ascii=False)
        except Exception as e:
            self.output_log(f"Error saving contacts: {repr(e)}")

    def load_contacts(self):
        # Load contacts from JSON file
        try:
            try:
                os.stat('phonebook.json')
                with open('phonebook.json', 'r', encoding='koi8-u') as f:
                    content = f.read().strip()
                    self.contacts = json.loads(content) if content else {}
            except FileNotFoundError:
                self.contacts = {}
        except Exception as e:
            print(e)


    def on_closing(self):
        # Handle the window close event
        self.save_contacts()  # Save contacts before closing
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()  
    