import os
from app import create_app
from flask_cors import CORS
# Create Flask application instance using the configuration settings
app = create_app()
if __name__ == '__main__':
    # Run the app with debug mode if the environment is 'development'
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
