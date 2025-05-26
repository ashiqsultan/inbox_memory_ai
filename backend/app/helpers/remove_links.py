import re

def remove_links(text: str) -> str:
    """
    Remove URLs and email addresses from the given text.
    
    Args:
        text (str): The input text that may contain URLs and email addresses
        
    Returns:
        str: The cleaned text with URLs and email addresses removed
    """
    if not text:
        return text
    
    # Pattern to match URLs (http, https, ftp, www, etc.)
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+|www\.[^\s<>"{}|\\^`\[\]]+|ftp://[^\s<>"{}|\\^`\[\]]+'
    
    # Pattern to match email addresses
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    # Remove URLs
    text = re.sub(url_pattern, '', text, flags=re.IGNORECASE)
    
    # Remove email addresses
    text = re.sub(email_pattern, '', text)
    
    # Clean up extra whitespace that might be left after removing links
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text