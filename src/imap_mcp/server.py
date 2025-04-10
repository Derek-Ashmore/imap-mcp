from fastmcp import FastMCP
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import imaplib
import email
from email.header import decode_header
from typing import List, Dict, Any, Optional
import json

# Load environment variables
load_dotenv()

mcp = FastMCP()

class IMAPConfig(BaseModel):
    host: str
    port: int
    username: str
    password: str
    use_ssl: bool = True

class IMAPConnection:
    _instance = None
    
    def __init__(self):
        self.conn = None
        self.config = None
        
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def connect(self, config: IMAPConfig):
        try:
            if config.use_ssl:
                self.conn = imaplib.IMAP4_SSL(config.host, config.port)
            else:
                self.conn = imaplib.IMAP4(config.host, config.port)
            self.conn.login(config.username, config.password)
            self.config = config
            return True
        except Exception as e:
            self.conn = None
            self.config = None
            raise Exception(str(e))
    
    def ensure_connected(self):
        if not self.conn or not self.config:
            raise Exception("Not connected to IMAP server")
        try:
            self.conn.noop()
        except:
            # Try to reconnect
            if self.config:
                self.connect(self.config)
            else:
                raise Exception("Connection lost and unable to reconnect")
    
    def list_folders(self) -> List[str]:
        self.ensure_connected()
        try:
            _, folders = self.conn.list()
            folder_names = []
            for folder in folders:
                folder_str = folder.decode()
                if '"."' in folder_str:
                    _, name = folder_str.split('"."')
                else:
                    _, name = folder_str.split(' "/" ')
                folder_names.append(name.strip().strip('"'))
            return folder_names
        except Exception as e:
            raise Exception(str(e))
    
    def get_emails(self, folder: str, limit: int = 10) -> List[Dict[str, Any]]:
        self.ensure_connected()
        try:
            self.conn.select(folder)
            _, messages = self.conn.search(None, "ALL")
            email_list = []
            
            message_nums = messages[0].split()
            if message_nums:
                for num in message_nums[-limit:]:
                    _, msg = self.conn.fetch(num, "(RFC822)")
                    email_message = email.message_from_bytes(msg[0][1])
                    subject = decode_header(email_message["Subject"])[0][0]
                    if isinstance(subject, bytes):
                        subject = subject.decode()
                        
                    email_list.append({
                        "subject": subject,
                        "from": email_message["From"],
                        "date": email_message["Date"]
                    })
            
            return email_list
        except Exception as e:
            raise Exception(str(e))

imap = IMAPConnection.get_instance()

@mcp.tool()
async def connect_imap(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Connect to an IMAP server with the provided configuration.
    """
    try:
        config_obj = IMAPConfig(**config)
        imap.connect(config_obj)
        return [{"status": "connected", "config": config}]
    except Exception as e:
        raise Exception(str(e))

@mcp.tool()
async def list_folders() -> List[Dict[str, List[str]]]:
    """
    List all available IMAP folders.
    """
    try:
        folders = imap.list_folders()
        return [{"folders": folders}]
    except Exception as e:
        raise Exception(str(e))

@mcp.tool()
async def get_emails(folder: str, limit: Optional[int] = 10) -> List[Dict[str, List[Dict[str, str]]]]:
    """
    Retrieve emails from a specific folder.
    """
    try:
        emails = imap.get_emails(folder, limit)
        return [{"emails": emails}]
    except Exception as e:
        raise Exception(str(e))

if __name__ == "__main__":
    mcp.run() 