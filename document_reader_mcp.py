import os
from mcp.server.fastmcp import FastMCP
import PyPDF2

mcp_docs = FastMCP("document_reader_mcp")
DOCUMENT_DIRECTORY = os.getenv("DOCUMENT_DIRECTORY", "docs")

@mcp_docs.tool()
async def list_documents() -> str:
    """List the names of the documents in the research docs directory."""
    try:
        files = [f for f in os.listdir(DOCUMENT_DIRECTORY) if os.path.isfile(os.path.join(DOCUMENT_DIRECTORY, f))]
        if files:
            return "Available documents:\n" + "\n".join(files)
        else:
            return "No documents found in the specified directory."
    except FileNotFoundError:
        return f"Error: Directory not found at {DOCUMENT_DIRECTORY}"
    except Exception as e:
        return f"An error occurred: {e}"

@mcp_docs.tool()
async def read_pdf_document(filename: str) -> str:
    """Read the text content of a specified PDF document.

    Args:
        filename: The name of the PDF document to read.
    """
    filepath = os.path.join(DOCUMENT_DIRECTORY, filename)
    try:
        with open(filepath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"  # Add newline for better formatting
        return f"Content of '{filename}':\n\n{text}"
    except FileNotFoundError:
        return f"Error: Document '{filename}' not found."
    except Exception as e:
        return f"An error occurred while reading '{filename}': {e}"
    
if __name__ == "__main__":
    print("Starting document reader MCP server...")
    mcp_docs.run(transport='stdio')
    print("Document reader MCP server is running...")