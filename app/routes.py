from flask import Blueprint, request, jsonify, current_app

api_bp = Blueprint("api", __name__)


@api_bp.route("/users", methods=["GET"])
def get_users():
    
    response = current_app.supabase.table("users").select("*").execute()
    return jsonify(response.data)
