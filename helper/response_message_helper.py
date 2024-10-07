class ResponseMessageHelper:

    @staticmethod
    def error_message_jwt_authentication():
        message = "Please log in to perform this action."
        return message
    
    @staticmethod
    def error_message_data_not_found(data_name: str):
        message = f"Data {data_name} not found."
        return message
    
    @staticmethod
    def success_message_upload_file():
        message = "File successfully processed and data saved to database."
        return message
    
    @staticmethod
    def error_message_failed_parsing_file():
        message = "Failed to parse the file. Please check the format and content of the uploaded file."
        return message
    
    @staticmethod
    def error_message_upload_file():
        message = "Failed to upload the file. Please check the file format and try again."
        return message
    
    @staticmethod
    def success_message_create():
        message = "Success create data."
        return message
    
    @staticmethod
    def error_message_create():
        message = "Failed create data, Please check input and try again."
        return message
    
    @staticmethod
    def error_message_update():
        message = "Failed update data, Please check input and try again."
        return message
    
    @staticmethod
    def success_message_update():
        message = "Success update data."
        return message

    @staticmethod
    def error_message_delete():
        message = "Failed delete data, Please check input and try again."
        return message
    
    @staticmethod
    def success_message_delete():
        message = "Success delete data."
        return message
