import cloudinary
import cloudinary.uploader

# Configuration
cloudinary.config( 
    cloud_name = "dynuwc8dp", 
    api_key = "795834859556143", 
    api_secret = "f1P3GWpGmLP18Sd8KUGwvLS32PA", 
    secure=True
)

# Path to the local image
local_image_path = "/Users/simarmalhotra/Desktop/projects/romaji-redacter/linguardian/app/data/images/post_process_images566a745ad1a046eba42d5ee0a2b1aad0/_page_2.png"

# Upload the local image
upload_result = cloudinary.uploader.upload(local_image_path, public_id="local_image")
print("Uploaded image URL:", upload_result["secure_url"])

# #
# optimize_url, _ = cloudinary_url("shoes", fetch_format="auto", quality="auto")
# print(optimize_url)


# auto_crop_url, _ = cloudinary_url("shoes", width=500, height=500, crop="auto", gravity="auto")
# print(auto_crop_url)