import os, zipfile
from io import BytesIO
from app.config import Config


# def extract_qti_zip_from_supabase(supabase_path: str, import_id: int) -> str:
#     supabase = Config.get_supabase_client()

#     # Extract the path after the bucket (assumes full Supabase path like: "qti-uploads/<user_id>/import_...zip")
#     if supabase_path.startswith(f"{Config.QTI_BUCKET}/"):
#         supabase_path = supabase_path[len(f"{Config.QTI_BUCKET}/"):]

#     # Figure out user_id from the path (the part after the bucket and before import_)
#     user_id = supabase_path.split("/")[0]

#     # Download the file
#     response = supabase.storage.from_(Config.QTI_BUCKET).download(supabase_path)
#     zip_data = BytesIO(response)

#     # Extract to: qti-uploads/<user_id>/import_<import_id>/
#     base_extract_path = os.path.join("qti-uploads", user_id, f"import_{import_id}")
#     os.makedirs(base_extract_path, exist_ok=True)

#     with zipfile.ZipFile(zip_data, 'r') as zip_ref:
#         zip_ref.extractall(base_extract_path)

#     return base_extract_path

def extract_qti_zip_from_supabase(supabase_file_path, import_id):
    supabase = Config.get_supabase_client()

    # Generate a tmp extraction dir
    extract_dir = f"/tmp/qti_extract_{import_id}"
    os.makedirs(extract_dir, exist_ok=True)

    # Get zip file from Supabase
    res = supabase.storage.from_(Config.QTI_BUCKET).download(supabase_file_path)
    if res is None or not hasattr(res, 'read'):
        raise Exception("Failed to download ZIP from Supabase")

    zip_bytes = res.read()
    zip_path = os.path.join(extract_dir, f"import_{import_id}.zip")

    # Save zip locally
    with open(zip_path, "wb") as f:
        f.write(zip_bytes)

    # Extract zip
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

    print(f"✅ Extracted QTI zip to {extract_dir}")
    return extract_dir
