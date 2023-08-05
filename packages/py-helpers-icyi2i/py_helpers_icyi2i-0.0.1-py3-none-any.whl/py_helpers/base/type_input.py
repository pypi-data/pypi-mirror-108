def type_input(
    input_type:type = str,
    input_message:str = "Please enter the requested value: ",
    error_message:str = "Invalid input for the requested type.",
    retry_count:int = 3):
    """
    Input function that typecasts into given datatype

    Keyword arguments:
    - input_type    - type  - Type used for typecasting (Default - str)
    - input_message - str   - Message to display in the input prompt
    - error_message - str   - Message to display and return for invalid input
    - retry_count   - int   - Number of tries for user to enter correct value

    Return : Returns a tuple (typecasted_value, operation_message)
    """

    for i in range(retry_count):
        try:
            val = input_type(input(input_message))
            message = "Success : Input received!"
            break
        except ValueError:
            print(error_message)
            val = None
            message = f"Error : {error_message}"
        except Exception as e:
            val = None
            message = f"Error : {str(e)}"

    return val, message
