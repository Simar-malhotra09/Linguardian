from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_process_pdf():
    # pdf file that you want to test
    with open("pdfs/5_pages_from_50.pdf", "rb") as file:
        response = client.post("/process-pdf", files={"file": ("test_file.pdf", file, "application/pdf")})
    
    # Check that the response is successful 
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/zip"  
    assert len(response.content) > 0
