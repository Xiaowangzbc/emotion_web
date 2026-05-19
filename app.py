from flask import Flask, render_template, request
from zhipuai import ZhipuAI

app = Flask(__name__)

# 填写你的 API Key
client = ZhipuAI(
    api_key="91e73209c8cc486c961f6ba82a5556b9.piM9HkUIU1VrP7j1"
)


@app.route("/", methods=["GET", "POST"])
def home():

    result = ""
    ai_reply = ""

    if request.method == "POST":

        # 获取用户输入
        text = request.form.get("text").strip()

        try:

            # 第一步：让 AI 判断情绪
            response = client.chat.completions.create(
                model="glm-4-flash",
                messages=[
                    {
                        "role": "user",
                        "content": f"""
                        请分析下面这句话的情绪：

                        {text}

                        你只能返回以下三种结果之一：

                        积极
                        消极
                        中性
                        """
                    }
                ]
            )

            emotion = response.choices[0].message.content.strip()

            # 第二步：根据情绪返回结果
            if "积极" in emotion:

                result = "积极情绪 😊"

            elif "消极" in emotion:

                result = "消极情绪 😥"

                # 第三步：AI 安慰用户
                comfort_response = client.chat.completions.create(
                    model="glm-4-flash",
                    messages=[
                        {
                            "role": "user",
                            "content": f"""
                            用户现在情绪不好：

                            {text}

                            请用温柔、简短、像朋友一样的话安慰用户。
                            不要太官方。
                            """
                        }
                    ]
                )

                ai_reply = comfort_response.choices[0].message.content

            else:

                result = "情绪中性 😐"

        except Exception as e:

            result = "AI 调用失败"
            ai_reply = str(e)

    return render_template(
        "index.html",
        result=result,
        ai_reply=ai_reply
    )


app.run(debug=True)