import subprocess
import threading
from flask import Flask, render_template, Response, request

app = Flask(__name__)
current_process = None
process_lock = threading.Lock()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-sms')
def run_sms():
    global current_process
    number = request.args.get('number', '').strip()
    mode = request.args.get('mode', '1').strip()
    
    # সার্ভার সাইড ফিল্টার চেক (01864005433)
    if number == '01864005433' or number == '1864005433':
        def err_gen():
            yield "FILTERED"
        return Response(err_gen(), mimetype='text/plain')

    if not number.isdigit() or len(number) != 11:
        def err_gen():
            yield "INVALID"
        return Response(err_gen(), mimetype='text/plain')

    cycles = "20" if mode == '1' else "5"
    concurrency = "300" if mode == '1' else "20"

    def generate():
        global current_process
        with process_lock:
            current_process = subprocess.Popen(
                ["python", "sms.py", "-n", number, "-c", cycles, "-p", concurrency, "--no-proxy"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
        
        try:
            for line in current_process.stdout:
                if "Cycle" in line or "Success" in line:
                    yield line.strip() + "\n"
            current_process.wait()
        except Exception:
            pass
        
        yield "DONE\n"

    return Response(generate(), mimetype='text/plain')

@app.route('/stop-sms', methods=['POST'])
def stop_sms():
    global current_process
    with process_lock:
        if current_process and current_process.poll() is None:
            try:
                current_process.terminate()
                current_process.wait(timeout=1)
            except Exception:
                try:
                    current_process.kill()
                except Exception:
                    pass
            current_process = None
            return {"status": "stopped", "message": "Attack stopped successfully!"}
            
    return {"status": "not_running", "message": "No active attack running."}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
    