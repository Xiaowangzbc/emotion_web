from idlelib.debugger_r import restart_subprocess_debugger

from  flask import Flask,render_template,request
app = Flask(__name__)
@app.route('/',methods=['GET','POST'])
def home():
    result = ""
    if request.method == 'POST':
        text = request.form.get('text')
        good_words = ["开心","高兴","喜欢","快乐","棒"]
        bad_words = ["难过","压力","伤心","烦躁","累"]
        for word in good_words:
            if word in text:
                result = "积极情绪"
                break
        for word in bad_words:
            if word in text:
                result = '消极情绪'
                break
        if result =="":
            result = "情绪不明显"
    return render_template("index.html",result=result)
app.run(debug=True)