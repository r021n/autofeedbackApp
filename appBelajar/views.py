from django.shortcuts import render
from django.http import FileResponse, HttpResponse, HttpResponseServerError
from django.db import connection
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Topics, Questions, Answers
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from collections import defaultdict
from django.core.paginator import Paginator

import re
import time
import textwrap
import google.generativeai as genai
import openpyxl

# Create your views here.
def index(request):
    return render(request, 'appBelajar/index.html')

def topics(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topics.objects.filter(Q(name__icontains=q)).order_by('-id')
    paginator = Paginator(topics, 5)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {'page_obj':page_obj}
    return render(request, 'appBelajar/topics.html', context)

@user_passes_test(lambda u: u.is_superuser)
def topicList(request):
    
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topics.objects.filter(Q(name__icontains=q)).order_by('-id')
    paginator = Paginator(topics, 5)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {'page_obj':page_obj}
    return render(request, 'appBelajar/topicList.html', context)

@user_passes_test(lambda u: u.is_superuser)
def createTopic(request):
    
    
    if request.method == 'POST':
        
        topic = Topics(name=request.POST['topic'])
        topic.save()
        
        topics = Topics.objects.all().last()
        return redirect('questionList', topics.id)
        
    context = {}
    return render(request, 'appBelajar/createTopic.html', context)

@user_passes_test(lambda u: u.is_superuser)
def deleteTopic(request, pk):
    
    topic = Topics.objects.get(id=pk)
    
    if request.method == 'POST':
        topic.delete()
        return redirect('topicList')
    
    context = {'obj':topic}
    return render(request, 'appBelajar/delete.html', context)

@user_passes_test(lambda u: u.is_superuser)
def questionList(request, pk):
    
    questions = Questions.objects.filter(topic_id=pk)
    
    topic = Topics.objects.get(id=pk)
    
    if request.method == 'POST':
        question_body = request.POST['question']
        image_description = request.POST['imageDescription']
        image = ''
        
        if 'image' in request.FILES:
            image = request.FILES['image']
        else:
            image = None
                
        question = Questions(topic=topic, question=question_body, image=image, image_description=image_description)
        question.save()
        return redirect('questionList', pk)
    
    context = {'questions': questions, 'topic':topic}
    return render(request, 'appBelajar/questionList.html', context)

@user_passes_test(lambda u: u.is_superuser)
def updateQuestion(request, pk):
    
    question = Questions.objects.get(id=pk)
    
    if request.method == 'POST':
        question_body = request.POST['question']
        image_description = request.POST['imageDescription']
        
        if 'image' in request.FILES:
            image = request.FILES['image']
            question.image.delete()
            question.image = image

        question.question = question_body
        question.image_description = image_description
        question.save()
        return redirect('questionList', question.topic_id)
    
    context = {'question':question}
    return render(request, 'appBelajar/updateQuestion.html', context)

@user_passes_test(lambda u: u.is_superuser)
def deleteQuestion(request, pk):
    
    question = Questions.objects.get(id=pk)
    
    if request.method == 'POST':
        question.delete()
        return redirect('questionList', question.topic_id)
    
    context = {'obj':question}
    return render(request, 'appBelajar/delete.html', context)

@login_required(login_url='loginPage')
def exercise(request, pk, number):
    questions = Questions.objects.filter(topic_id=pk)
    questions_length = len(questions)
    number = number
    question = questions[number-1]
    
    topic = Topics.objects.get(id=pk)
    
    # regular expression function
    def extract_score(text):
        # Buat regex pattern
        pattern = r"(?<=Skor:\s)(\d+)"
        pattern2 = r"(r'\d+(?!.*\d)')"
        pattern3 = r"(?i)skor\s*(\d+)"

        # Temukan semua kecocokan dalam teks
        matches = re.search(pattern, text)
        matches2 = re.search(pattern2, text)
        matches3 = re.search(pattern3, text)

        # Jika ada kecocokan, kembalikan angka
        if matches:
            return matches.group(1)
        elif matches2: 
            return matches2.group(1)
        elif matches3: 
            return matches3.group(1)

        # Jika tidak ada kecocokan, kembalikan string kosong
        return ""
    
    def extract_feedback(text):
        # Hapus semua karakter ">"
        text = re.sub(r">", "", text)

        # Hapus "skor" dan angka setelahnya
        text = re.sub(r"Skor:\s*\d+", "", text)

        # Hapus spasi di awal dan akhir teks
        text = text.strip()

        return text

    def removeStar(text):
        pattern = r"\*"
        kalimat_tanpa_tanda_bintang = re.sub(pattern, "", text)
        return kalimat_tanpa_tanda_bintang
    
    # handle form
    if request.method == "POST":
        
        feedback = ""
        user_score = 0
        
        # API played
        def to_markdown(text):
            text = text.replace('•', '  *')
            return textwrap.indent(text, '> ', predicate=lambda _: True)
        
        # The API key
        apiKey= ""

        with open('appBelajar/api.txt', 'r') as api:
            apiKey= str(api.read())
        
        genai.configure(api_key=apiKey)

        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    print(m.name)
        except:
            return HttpResponseServerError('terjadi masalah saat request API')

        # generation_config = {
        # "temperature": 0.9,
        # "top_p": 1,
        # "top_k": 1,
        # "max_output_tokens": 8192,
        # }

        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE",
            },
        ]

        model = genai.GenerativeModel(model_name="gemini-1.0-pro-001",
                                    safety_settings=safety_settings)
        soal = question.question
        jawaban = request.POST.get('answer', None)
        
        if jawaban == "" or jawaban.isspace():
            umpan_balik= "Kamu belum memasukkan jawaban"
        else:

            question_image = question.image_description
            # masukan = f"gambar: {question_image}, soal: {soal}, jawaban: {jawaban}, umpan balik dan saran perbaikan jawaban(maksimal 50 karakter) dan Skor(tulis 1 digit antara 0 sampai 5): "
            masukan = f"gambar: {question_image}, soal: {soal}, jawaban: {jawaban}, umpan balik dan skor : (contoh output yang diharapkan = 'Jawbanmu ...(kurang tepat atau sudah benar, sesuaikan dengan konteks), (Coba perhatikan kembali...., seuaikan konteks). Skor: 3') "
            
            response = model.generate_content(masukan, generation_config=genai.types.GenerationConfig(candidate_count=1, top_p=0.7, top_k=4, max_output_tokens=100, temperature=1))
            print(response.prompt_feedback)
            feedback_temporary = to_markdown(response.text)
            feedback_fix = removeStar(feedback_temporary)
            print(feedback_fix, '<< the feedback')
            
            
            time.sleep(3)
            try:
                user_score = int(extract_score(feedback_fix))
            except:
                user_score = 0
            feedback = extract_feedback(feedback_fix)
            # try:
            # except:
            #     return HttpResponse('feedback tak diberikan')
        
        # save the gained data
        answer = Answers.objects.create(
            user = request.user,
            topic = topic,
            question = question,
            answer = jawaban,
            feedback = feedback,
            score = user_score,
        )

        topic.participants.add(request.user)
        
    user_answer = Answers.objects.filter(topic_id=pk, user=request.user, question=question).first()
    
    context = {'questions':questions, 'questions_length':questions_length, 'question':question, 'number':number, 'user_answer':user_answer}
    return render(request, 'appBelajar/exercise.html', context)

def exerciseOver(request):
    return render(request, 'appBelajar/over.html')

def myResult(request, pk):

    results = Answers.objects.filter(user=request.user, topic_id=pk)
    topic = Topics.objects.get(id=pk)
    score = 0

    for result in results:
        score += result.score
    
    try:
        totalScore = int(score / (5*len(results))*100)
    except:
        totalScore = 0

    context = {'results': results, 'score': totalScore, 'topic':topic}
    return render(request, 'appBelajar/myResult.html', context)

def registerPage(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()

        return redirect("loginPage")
    else:
        form = RegisterForm()

    return render(response, "appBelajar/register.html", {"form":form})

def loginPage(request):
    
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Akun tidak ditemukan")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "username atau password salah")
    
    return render(request, 'appBelajar/loginForm.html')

@login_required(login_url='loginPage')
def logoutPage(request):
    logout(request)
    return redirect('home')

@user_passes_test(lambda u: u.is_superuser)
def studentsAnswer(request, pk):
    topic = Topics.objects.get(id=pk)
    q = request.GET.get('q', '')
    filtered_answers = Answers.objects.filter(Q(user__username__icontains=q), topic=topic)
    questions = list(Questions.objects.filter(topic=topic))

    def generate_header(questions):
        headers = ['nama siswa']
        for i, question in enumerate(questions, start=1):
            headers.append(f"soal nomer {i}: {question.question}")
            headers.append(f"Umpan Balik soal nomer {i}")
        headers.append('nilai siswa')
        return headers

    headers = generate_header(questions)

    user_answers = defaultdict(lambda: {'answers': {}, 'feedback': {}, 'score': {}})
    for answer in filtered_answers:
        user = answer.user.username
        question_text = answer.question.question
        user_answers[user]['answers'][question_text] = answer.answer
        user_answers[user]['feedback'][question_text] = answer.feedback
        user_answers[user]['score'][question_text] = answer.score or 0

    row_table = []
    for user, data in user_answers.items():
        row_data = [user]
        user_score = 0
        for question in questions:
            row_data.append(data['answers'].get(question.question, ''))
            row_data.append(data['feedback'].get(question.question, ''))
            user_score += data['score'].get(question.question, 0)
        final_score = int(user_score / (5 * len(questions)) * 100)
        row_data.append(final_score)
        row_table.append(row_data)

    context = {'headers': headers, 'row_data': row_table, 'topic': topic}
    return render(request, 'appBelajar/studentsAnswer.html', context)

@user_passes_test(lambda u: u.is_superuser)
def downloadAnswer(request, pk):

    try:
        # Fetch the topic object based on the provided name
        topic = Topics.objects.get(id=pk)
    except Topics.DoesNotExist:
        response.status_code = 404
        return response

    # Filter answers based on the chosen topic
    filtered_answers = Answers.objects.filter(topic=topic)

    # Create an Excel workbook and worksheet
    workbook = openpyxl.Workbook()
    worksheet = workbook.active

    # Create headers based on questions in the chosen topic
    questions = [f"soal nomer {i+1}: {question.question}" for i, question in enumerate(Questions.objects.filter(topic=topic))]
    feedbacks = [f"Umpan Balik soal nomer {i+1}" for i, question in enumerate(Questions.objects.filter(topic=topic))]
    headers = ['nama siswa'] + [item for pair in zip(questions, feedbacks) for item in pair] + ['nilai siswa']

    worksheet.append(headers)  # Add headers to the first row

    # Create a dictionary to store unique users and their answers
    user_answers = {}

    # Iterate through answers and append user and answer data to rows
    for answer in filtered_answers:
        user = answer.user.username
        question_text = answer.question.question
        answer_text = answer.answer
        feedback_text = answer.feedback
        user_score = answer.score

        if user not in user_answers:
            user_answers[user] = {'answers': {}, 'feedback': {}, 'score': {}}

        user_answers[user]['answers'][question_text] = answer_text
        user_answers[user]['feedback'][question_text] = feedback_text
        user_answers[user]['score'][question_text] = int(user_score)

    # Iterate through unique users and their answers to populate the worksheet
    for user, data in user_answers.items():
        row_data = [user]
        user_score = 0
        for question in Questions.objects.filter(topic=topic):
            answer_text = data['answers'].get(question.question, '')
            feedback_text = data['feedback'].get(question.question, '')
            user_score += data['score'].get(question.question, 0)
            row_data.append(answer_text)
            row_data.append(feedback_text)
            
        final_score = int(user_score / (5 * len(Questions.objects.filter(topic=topic))) * 100)
        row_data.append(final_score)
        worksheet.append(row_data)

    # Prepare the response object
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    topic_name = topic.name
    response['Content-Disposition'] = f'attachment; filename=Jawaban_siswa_{topic_name}.xlsx'

    # Save the workbook to the response object
    workbook.save(response)

    return response
