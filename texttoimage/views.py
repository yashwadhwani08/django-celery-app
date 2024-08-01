from celery import group
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import TextInputForm
from .tasks import send_request_to_server
from .models import PromptToImage

# Create your views here.


def home_view(request):
    context = {}
    context["form"] = TextInputForm()
    if request.method == "GET":
        return render(request, "texttoimage/index.html", context)
    elif request.method == "POST":
        form = TextInputForm(request.POST)
        # print(request.__dict__)
        print("POST method received")
        text_input_1, text_input_2, text_input_3 = (
            form.data["text_input_1"].strip(),
            form.data["text_input_2"].strip(),
            form.data["text_input_3"].strip(),
        )
        print(text_input_1, text_input_2, text_input_3)

        promptToImage1 = PromptToImage.objects.create(text_input = text_input_1)
        promptToImage2 = PromptToImage.objects.create(text_input = text_input_2)
        promptToImage3 = PromptToImage.objects.create(text_input = text_input_3)


        if text_input_1 == "":
            text_input_1 = "A red flying dog"
            promptToImage1.text_input = text_input_1
            promptToImage1.save()
        if text_input_2 == "":
            text_input_2 = "A piano ninja"
            promptToImage2.text_input = text_input_1
            promptToImage2.save()
        if text_input_3 == "":
            text_input_3 = "A footballer kid"
            promptToImage3.text_input = text_input_1
            promptToImage3.save()

        
        my_grouped_task = group(
            send_request_to_server.s(text_input_1, promptToImage1.id),
            send_request_to_server.s(text_input_2, promptToImage2.id),
            send_request_to_server.s(text_input_3, promptToImage3.id),
        ).delay()

        # response = send_request_to_server.delay(text_input_1, str(promptToImage1_id)),
        
        # print(my_grouped_task)
        # print(my_grouped_task.get())
        return HttpResponseRedirect(reverse("result-page"))
        # return results(request, [promptToImage1.id, promptToImage2.id, promptToImage3.id])
    
# def results(request, rowId=[]):
def results(request):
    pass
    # print(request.method)
    # resultsList = []
    # for element in rowId:
        # obj = PromptToImage.objects.get(id=element)
        # 
        # obj.text_input = 
    # return render(request, 'texttoimage/result.html')
