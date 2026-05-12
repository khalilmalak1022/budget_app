from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
import google.generativeai as genai


@login_required
def chatbot(request):
    reponse = None
    erreur = None

    if request.method == "POST":
        question = request.POST.get("question")

        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)

            model = genai.GenerativeModel("gemini-2.5-flash")

            result = model.generate_content(
                f"""
                Tu es un assistant financier pour une application de suivi budgétaire.
                Réponds simplement en français.

                Question utilisateur :
                {question}
                """
            )

            reponse = result.text

        except Exception as e:
            erreur = str(e)

    return render(request, "chatbot/chatbot.html", {
        "reponse": reponse,
        "erreur": erreur
    })