from json import JSONDecodeError
import string, random
from tkinter import *
from tkinter import messagebox
import json

#----------------------------------------------------------#
#COLORS

NAVY = '#071952' # Background
TEAL = '#0B666A' # Text entries
MINT = '#35A29F' # Text 1
SEA = '#97FEED' # Text 2

#----------------------------------------------------------#
#FUNCTIONS

def generate():
    """
    Generate a random password
    """

    x = string.printable[:-6]  # take a full list of ASCII signs and remove the last 6 of them
    length = random.randint(10, 15)  # choose a random length to make it more REALISTIC

    # combine two lines from above into one output by using '.join' + list comprehension + random.choice
    return ''.join([random.choice(list(x)) for i in range(length)])

def add_button():
    """
    Logic of 'ADD' button:
    1. takes website, email and password as a data
    2. write to data.json
    """
    website = website_entry.get()
    email = email_username_entry.get()
    password = password_entry.get()

    # structure of JSON data
    data_json = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if website == "" or password == "":
        #Inform the End User about an Empty Entry
        messagebox.showinfo(title='ERROR: Empty Entry', message="ERROR: Empty Entry")
    else:
        #Check the Correctness of Email Format
        if '@' not in email or '.' not in email:
            messagebox.showinfo(title='Wrong Email!', message="'@' or '.' missing.")
        else:
            #Try to read JSON file
            try:
                with open("data.json", "r") as data_file:
                    #Reading old data
                    data = json.load(data_file)
                    #Updating old data with new data
                    data.update(data_json)

            #If there's no file in a Folder -> Create New Data
            except (FileNotFoundError, JSONDecodeError):
                data = data_json
            #Write the 'data' into a JSON file
            with open("data.json", "w") as data_file:
                # Saving updated data in a json file
                json.dump(data, data_file, indent=4) #indent to make it look nice and neat :)

            #Remove User Entries to be ready for the Next One
            website_entry.delete(0, END)
            password_entry.delete(0, END)

def generate_new_password():
    """
    Function of a 'Generate Passoword' Button
    """
    random_password = generate() # Generate Password
    root.clipboard_clear()
    root.clipboard_append(random_password) # Copy it to a Clipboard
    password_entry.delete(0, END) # Delete old Passeword
    password_entry.insert(0, random_password) # Insert New Password

def search_button():
    """
    Function of a 'Search' Button
    """
    website = website_entry.get() # take the website name
    if website == "":
        #Inform that the input is empty
        messagebox.showerror(title="Empty Entry", message=f"Empty Entry")
    else:
        #Read data 'website' from JSON file
        with open('data.json', 'r') as data_file:
            data = json.load(data_file)
        try:
            email, password= data[website]['email'], data[website]['password'] # Read email and password
        except KeyError:
            #If email/pass. missing - show error
            messagebox.showerror(title=website, message=f"Website '{website}' not found.")
        else:
            #If email/pass. not missing - show it as a pop up
            messagebox.showinfo(title=website, message=f"Your email: {email}\nYour password: {password}")

#----------------------------------------------------------#
#UI

root = Tk()
root.title('Pa**word Manager')
root.config(padx=50, pady=50, bg=NAVY)
root.resizable(False, False)

#------------------------#
#1st line of Entries
website_entry = Entry(
    width=26,
    bd=0, bg=TEAL, fg=SEA,
    highlightthickness=2, highlightbackground=MINT,
    font=("Arial",12,"bold")
    )
website_search = Button(
    width=16,
    text="Search",
    bd=0, bg=TEAL, fg=SEA,
    highlightthickness=2, highlightbackground=MINT,
    font=("Arial",9,"bold"),
    activebackground=NAVY, activeforeground=SEA,
    command=search_button
    )
website_label = Label(
    width=13,
    text='Website:',
    bg=TEAL, fg=SEA,
    font=("Arial",10,"bold")
    )
    # Grids
website_label.grid(column=0, row=1)
website_entry.grid(column=1, row=1)
website_search.grid(column=2, row=1)

#------------------------#
#2nd line of Entries
email_username_entry = Entry(
    width=40,
    bd=0, bg=TEAL, fg=SEA,
    highlightthickness=2, highlightbackground=MINT,
    font=("Arial",12,"bold")
    )

email_username_label = Label(
    text='Email / Username:',
    bg=TEAL, fg=SEA,
    font=("Arial",10,"bold")
    )
email_username_entry.insert(0, 'bartek@gmail.com')
    # Grids
email_username_label.grid(column=0, row=2)
email_username_entry.grid(column=1, row=2, columnspan=2) #-> Email/username entry takes 2 COLUMNS

#------------------------#
#3rd line of Entries
password_entry = Entry(
    width=26,
    bd=0, bg=TEAL, fg=SEA,
    highlightthickness=2, highlightbackground=MINT,
    font=("Arial",12,"bold")
    )
password_label = Label(
    width=14,
    text='Password:',
    bg=TEAL, fg=SEA,
    font=("Arial",10,"bold")
    )

generate_password_button = Button(
    width=16,
    text="Generate Password",
    bd=0, bg=TEAL, fg=SEA,
    highlightthickness=2, highlightbackground=MINT,
    font=("Arial",9,"bold"),
    activebackground=NAVY, activeforeground=SEA,
    command=generate_new_password
    )
    # Grids
password_label.grid(column=0, row=3)
password_entry.grid(column=1, row=3)
generate_password_button.grid(column=2, row=3)

#------------------------#
#4th line of Entries
add_button = Button(
    width=68,
    text="Add",
    bd=0,
    bg=TEAL, fg=SEA, # colors in PASSIVE add button
    highlightthickness=2,
    font=("Arial",9,"bold"),
    activebackground=NAVY, activeforeground=SEA, # colors in ACTIVE add button
    command=add_button
    )
# Grid
add_button.grid(
    column=0,
    row=4,
    columnspan=3 #-> The Add button takes 3 columns
)

#------------------------#
#Properties of an Image's Canvas
canvas = Canvas(
    width=120, height=180,
    bg=NAVY,
    highlightthickness=0
    )
try:
    # Check if a '.png' file exists
    locker_image = PhotoImage(file='futuristic_digital_locker-removebg-preview.png')
    new_image = locker_image.subsample(3, 3)
    canvas.create_image(55,80, image=new_image)
except TclError:
    print('File not found! Make sure the file path is correct.')

    # Grid
canvas.grid(column=1,row=0)

#------------------------#
#Keep the main root looping over the code
root.mainloop() #without this line...code won't work