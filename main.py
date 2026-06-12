# ===================================
# [Your Program Title]
# ===================================
# Developed by. Bayu Prasetya
# JCDS - [Class Batch]


# /************************************/

# /===== Data Model =====/
# Create your data model here
data = [] # Example data model


# /===== Feature Program =====/
# Create your feature program here
def read():
    """Function for read the data
    """
    return

def create():
    """Function for create the data
    """
    return

def update():
    """Function for update the data
    """
    return

def delete():
    """Function for delete the data
    """
    return

# /===== Main Program =====/
# Create your main program here
def main():
    """Function for main program
    """

    input_user = input("Insert your option: ")
    if input_user == "1":
        read()
    elif input_user == "2":
        create()
    elif input_user == "3":
        update()
    elif input_user == "4":
        delete()
    else:
        print("Input is not valid !")


if __name__ == "__main__":
    main()