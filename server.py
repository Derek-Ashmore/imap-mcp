import os
import imaplib
from dotenv import load_dotenv
from mcp import Server, Tool

# Load environment variables
load_dotenv()

class EmailTool(Tool):
    def __init__(self):
        super().__init__(
            name="list_email_folders",
            description="Connect to an email account and list available folders",
            parameters={
                "email": {
                    "type": "string",
                    "description": "Email address to connect to"
                },
                "password": {
                    "type": "string",
                    "description": "Password for the email account"
                },
                "imap_server": {
                    "type": "string",
                    "description": "IMAP server address (e.g., imap.gmail.com)",
                    "default": "imap.gmail.com"
                }
            }
        )

    async def execute(self, email: str, password: str, imap_server: str = "imap.gmail.com") -> dict:
        try:
            # Connect to the IMAP server
            mail = imaplib.IMAP4_SSL(imap_server)
            mail.login(email, password)
            
            # List all folders
            folders = []
            for folder in mail.list()[1]:
                folder_name = folder.decode().split('"/"')[-1].strip('"')
                folders.append(folder_name)
            
            # Logout and close connection
            mail.logout()
            
            return {
                "status": "success",
                "folders": folders
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

def main():
    # Create server instance
    server = Server()
    
    # Add the email tool
    server.add_tool(EmailTool())
    
    # Start the server
    server.start()

if __name__ == "__main__":
    main() 