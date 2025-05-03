from django.shortcuts import render
from django.http import JsonResponse
import json
import time # 用于模拟 AI 思考时间
from google import genai
from google.genai import types

def chat_view(request):
    """
    渲染聊天页面
    """
    context = {
        'ai_options': ['GeminiApi'],
        'model_options': {
            'GeminiApi': ['gemini-2.5-flash-preview-04-17', 'gemini-2.5-pro-preview-03-25', 'gemini-2.0-flash'],
        }
    }
    return render(request, 'chat.html', context)

def send_message_view(request):
    """
    处理用户发送的消息 (AJAX)
    """
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            selected_ai = data.get('ai', 'Unknown AI')
            selected_model = data.get('model', 'Unknown Model')

            # --- 在这里添加调用实际 AI 模型的逻辑 ---
            # print(f"Received from {selected_ai} ({selected_model}): {user_message}")

            if selected_ai == 'GeminiApi':
                client = genai.Client(api_key="your-key")
                response = client.models.generate_content(
                    model=selected_model,
                    contents=user_message,
                    config=types.GenerateContentConfig(
                        system_instruction="你是一个AI专家，请提供简洁的回答。",
                        temperature=0.7,
                    ),
                )
                ai_response = response.text
            else:
                # 模拟 AI 响应
                time.sleep(0.5)  # 模拟思考时间
                ai_response = f"收到您的消息 (来自 {selected_ai} - {selected_model}): '{user_message}'. 我正在处理..."

            return JsonResponse({'status': 'success', 'ai_response': ai_response})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': '无效的请求数据'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': '无效的请求方法'}, status=405)