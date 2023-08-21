from waitress import serve

import app

serve(app.serve_waitress, host='0.0.0.0', port=8080)
