from fastapi.testclient import TestClient
from linguardian.app.main import app
import time

client = TestClient(app)

def test_process_pdf():
    start_time = time.time()

    # pdf file that you want to test
    with open("/Users/simarmalhotra/Desktop/projects/romaji-redacter/pdfs/5_pages_from_50.pdf", "rb") as file:
        response = client.post("/process-pdf", files={"file": ("test_file.pdf", file, "application/pdf")})

    end_time = time.time() 
    elapsed_time = end_time - start_time  

    # print(f"Time elapsed for test_process_pdf: {elapsed_time:.2f} seconds")
    with open("elapsed_time.txt", "w") as file:
        file.write(f"Time elapsed for test_process_pdf: {elapsed_time:.2f} seconds")
    
    # Check that the response is successful 
    assert response.status_code == 200
    # assert response.headers["content-type"] == "application/zip"  
    # assert len(response.content) > 0
