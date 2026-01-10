from flask import Flask, send_file, jsonify
from pathlib import Path
import os

app = Flask(__name__)

# Project root
PROJECT_ROOT = Path(__file__).parent
POSE_FILE_PATH = PROJECT_ROOT / "text-to-skeleton" / "output" / "poses" / "sample.pose"

@app.route('/api/pose/sample', methods=['GET'])
def get_sample_pose():
    """
    API endpoint to return the sample.pose file
    
    Returns:
        The sample.pose file as a downloadable response
    """
    try:
        # Check if file exists
        if not POSE_FILE_PATH.exists():
            return jsonify({
                "error": "File not found",
                "message": f"The file {POSE_FILE_PATH} does not exist"
            }), 404
        
        # Send the file
        return send_file(
            POSE_FILE_PATH,
            as_attachment=True,
            download_name='sample.pose',
            mimetype='application/octet-stream'
        )
    
    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    
    Returns:
        JSON response indicating the API is running
    """
    return jsonify({
        "status": "healthy",
        "message": "Sign Language API is running"
    })

@app.route('/api/pose/list', methods=['GET'])
def list_poses():
    """
    List all available pose files
    
    Returns:
        JSON list of available pose files
    """
    try:
        poses_dir = PROJECT_ROOT / "text-to-skeleton" / "output" / "poses"
        
        if not poses_dir.exists():
            return jsonify({
                "error": "Poses directory not found",
                "poses": []
            }), 404
        
        pose_files = [f.name for f in poses_dir.glob("*.pose")]
        
        return jsonify({
            "poses": pose_files,
            "count": len(pose_files)
        })
    
    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)
