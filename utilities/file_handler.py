import os, zipfile
from io import BytesIO
from app.config import Config


def extract_qti_zip_from_supabase(supabase_path: str, import_id: int) -> str:
    supabase = Config.get_supabase_client()

    # Extract the path after the bucket (assumes full Supabase path like: "qti-uploads/<user_id>/import_...zip")
    if supabase_path.startswith(f"{Config.QTI_BUCKET}/"):
        supabase_path = supabase_path[len(f"{Config.QTI_BUCKET}/"):]

    # Figure out user_id from the path (the part after the bucket and before import_)
    user_id = supabase_path.split("/")[0]

    # Download the file
    response = supabase.storage.from_(Config.QTI_BUCKET).download(supabase_path)
    zip_data = BytesIO(response)

    # Extract to: qti-uploads/<user_id>/import_<import_id>/
    base_extract_path = os.path.join("qti-uploads", user_id, f"import_{import_id}")
    os.makedirs(base_extract_path, exist_ok=True)

    with zipfile.ZipFile(zip_data, 'r') as zip_ref:
        zip_ref.extractall(base_extract_path)

    return base_extract_path

def extract_qti_zip_from_supabase_2(supabase_path: str, import_id: int) -> str:
    supabase = Config.get_supabase_client()

    # Remove bucket prefix if present
    if supabase_path.startswith(f"{Config.QTI_BUCKET}/"):
        supabase_path = supabase_path[len(f"{Config.QTI_BUCKET}/"):]

    user_id = supabase_path.split("/")[0]

    # 🛠️ Fix: Get the actual response content
    response = supabase.storage.from_(Config.QTI_BUCKET).download(supabase_path)

    if not hasattr(response, 'read') and hasattr(response, 'content'):
        zip_bytes = BytesIO(response.content)
    elif hasattr(response, 'read'):
        zip_bytes = BytesIO(response.read())
    else:
        import traceback
        traceback.print_exc()
        raise Exception("Failed to download ZIP from Supabase")

    base_extract_path = os.path.join("qti-uploads", user_id, f"import_{import_id}")
    os.makedirs(base_extract_path, exist_ok=True)

    with zipfile.ZipFile(zip_bytes, 'r') as zip_ref:
        zip_ref.extractall(base_extract_path)

    return base_extract_path
