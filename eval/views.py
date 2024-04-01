import datetime
import traceback
from io import BytesIO
import tarfile
import re

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.utils.encoding import smart_str
from orm.models import Author, Model, EvaluationDataset, Metric, ModelResponse, ModelSubmission
from orm.scripts import get_messages, get_baselines
from eval.scripts.human.launch_hit import launch_hits
from eval.scripts.human.retrieve_responses import retrieve
from eval.scripts.upload_model import handle_submit, send_email, download_file, upload_dbdc5_file, upload_dstc10_file, upload_dstc11_file, upload_gemv3_file
from eval.forms import UploadModelForm, DBDC5Form, DSTC10Form, DSTC11Form, GEMV3Form, SignUpForm, LogInForm


def uploads(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    current_author = Author.objects.get(author_id=request.user)
    models = Model.objects.filter(author=current_author, archived=False)
    uploads = []
    evalsets = []
    for model in models:
        uploads.append(dict({'model': model, 'evalsets': evalsets}))
    uploads.reverse()
    return render(request, 'uploads.html', {'uploads': uploads})


def human(request):
    model = Model.objects.get(pk=request.GET['id'])
    datasets = EvaluationDataset.objects.all()
    baselines = []
    for dataset in model.evaluationdatasets.all():
        for baseline in dataset.baselines.all():
            baselines.append({"id": baseline.pk, "name": baseline.name, "description": baseline.description, "dataset": dataset})
    return render(request, 'human.html', {'model_id': model.pk, 'baselines': baselines})


def delete(request):
    if request.method == "GET":
        return render(request, 'delete.html', { 'model_id': request.GET['model_id']})
    model = Model.objects.get(pk=request.GET['model_id'])
    model.archived = True
    model.save()
    return redirect('/uploads')


def publish(request):
    if request.method == "GET":
        return render(request, 'publish.html', { 'model_id': request.GET['model_id']})
    model = Model.objects.get(pk=request.GET['model_id'])
    model.public = True
    model.save()
    return redirect('/uploads')


def submit(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')

    eval_datasets = EvaluationDataset.objects.all()
    if request.method == "POST":
        model = Model(name=request.POST['name'], author=Author.objects.get(pk=request.user), description=request.POST['description'], repo_location=request.POST['repo_location'], cp_location=request.POST['checkpoint_location'])
        response_files = []
        datasets = []
        for dataset in eval_datasets:
            if dataset.name in request.FILES.keys():
                response_file = request.FILES[dataset.name]
                response_files.append(response_file)
                datasets.append(dataset)
        if handle_submit(model, datasets, response_files, 'baseline' in request.POST):
            return HttpResponseRedirect('/uploads')
        else:
            print(str(request))
            return redirect("/upload?error=input")

    form = UploadModelForm()
    error = "error" in request.GET
    return render(request, 'submit.html', {'form': form, 'response_files': eval_datasets, 'error': error})


def login_view(request):
    if request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('/uploads')
            return redirect('/accounts/login')
    form = LogInForm()
    return render(request, 'registration/login.html', {'form' : form})


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                 email=form.cleaned_data['email'],
                                 password=form.cleaned_data['password'],
                                 first_name=form.cleaned_data['first_name'],
                                 last_name=form.cleaned_data['last_name'])
            author = Author(author_id=user,
                            name=form.cleaned_data['first_name'] + " " + form.cleaned_data['last_name'], 
                            institution=form.cleaned_data['institution'],
                            email=form.cleaned_data['email'])
            author.save()
            return redirect('/accounts/login')            
    form = SignUpForm()
    return render(request, 'registration/signup.html', {'form' : form})

def compare(request):
    email_body =  "Model1: " + str(request.GET['model1']) + " | Model2: " + str(request.GET['model2']) + " | Dataset: " + str(request.GET['evalset'])
    send_email("chatevalteam@gmail.com", "System Comparison", email_body)
    return redirect("/")

def dbdc5download(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    current_author = Author.objects.get(author_id=request.user)
    send_email("teamchateval@gmail.com", "Data Request", str(request.user))

    # from https://stackoverflow.com/questions/1156246/having-django-serve-downloadable-files
    return download_file('release-v3-distrib.zip')
    #return redirect("/")

def dstc10download(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    current_author = Author.objects.get(author_id=request.user)
    send_email("teamchateval@gmail.com", "DSTC10 Data Request", str(request.user))

    file_url = download_file('DSTC_10_Track_5.zip')
    # from https://stackoverflow.com/questions/1156246/having-django-serve-downloadable-files
    return file_url
    #return redirect("/")

def dstc11download(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    current_author = Author.objects.get(author_id=request.user)
    send_email("teamchateval@gmail.com", "DSTC11 Data Request", str(request.user))

    file_url = download_file('DSTC11/DSTC_11_Track_4.zip')
    # from https://stackoverflow.com/questions/1156246/having-django-serve-downloadable-files
    return file_url

    
def dbdc5submit(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')


    if request.method == "POST":
        name = request.POST['name']
        submission_info = request.POST['submission_info']
        submission_track =  request.POST['submission_track']

        if upload_dbdc5_file('dbdc_submissions/' + str(request.user) + '_' + name + '_' + submission_info + '_' + submission_track, request.FILES['dbdc5file']):
            send_email("teamchateval@gmail.com", "DBDC5 submission", str(request.user))
            send_email(str(request.user.email), "DBDC5 submission received", "Thank you for your submission")
            return HttpResponseRedirect('https://chateval.org/shared_task')

    form = DBDC5Form()
    error = "error" in request.GET
    return render(request, 'dbdc5submit.html', {'form': form, 'error': error})

def dstc10submit(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')


    if request.method == "POST":
        name = request.POST['name']
        submission_info = request.POST['submission_info']
        submission_track =  request.POST['submission_track']

        if upload_dstc10_file('dstc10_submissions/' + str(request.user) + '_' + name + '_' + submission_info + '_' + submission_track, request.FILES['dstc10file']):
            send_email("teamchateval@gmail.com", "DSTC10 submission", str(request.user))
            send_email(str(request.user.email), "DSTC10 submission received", "Thank you for your submission")
            return HttpResponseRedirect('https://chateval.org/dstc10')

    form = DSTC10Form()
    error = "error" in request.GET
    return render(request, 'dstc10submit.html', {'form': form, 'error': error})


def dstc11submit(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')


    if request.method == "POST":
        name = request.POST['name']
        submission_info = request.POST['submission_info']
        submission_track =  request.POST['submission_track']

        if upload_dstc11_file('dstc11_submissions/' + str(request.user) + '_' + name + '_' + submission_info + '_' + submission_track, request.FILES['dstc11file']):
            send_email("teamchateval@gmail.com", "DSTC11 submission", str(request.user))
            send_email(str(request.user.email), "DSTC11 submission received", "Thank you for your submission")
            return HttpResponseRedirect('https://chateval.org/dstc11')

    form = DSTC11Form()
    error = "error" in request.GET
    return render(request, 'dstc11submit.html', {'form': form, 'error': error})


def check_GEM_submissions(filename, file_content):
    # Check name
    task_suffixes = ('_D2T-1-FA', '_D2T-1-FI', '_D2T-1-CFA', '_D2T-2-FA', '_D2T-2-FI', '_D2T-2-CFA', '_Summ-1', '_Summ-2', '_Summ-3')
    d2t1_IDs = ['D2T-1-FA', 'D2T-1-FI', 'D2T-1-CFA']
    d2t2_IDs = ['D2T-2-FA', 'D2T-2-FI', 'D2T-2-CFA']
    summ_IDs = ['Summ-1', 'Summ-2', 'Summ-3']
    languages = ('_en', '_zh', '_de', '_ru', '_es', '_ko', '_hi', '_sw', '_ar')
    extensions = ('.txt', '.jsonl')


    # Check extension
    if filename.endswith(extensions):
        filename_noExt = filename.rsplit('.', 1)[0]
        extension = filename.rsplit('.', 1)[1]
        # Check language ID
        if filename_noExt.endswith(languages):
            filename_noExt_noLang = filename_noExt.rsplit('_', 1)[0]
            # Check task identifier
            if filename_noExt_noLang.endswith(task_suffixes):
                filename_noExt_noLang_noTask = filename_noExt_noLang.rsplit('_', 1)[0]
                task_ID = filename_noExt_noLang.rsplit('_', 1)[1]
                # If there is a system name, open the files and check inside
                if len(filename_noExt_noLang_noTask) > 0:
                    # txt files are for the D2T task; D2T-1 should have 1,779 lines, D2T-2 should have 1,800 lines.
                    if extension == 'txt':
                        file_lines = content.readlines()
                        # Check line numbers in D2T-1 data
                        if task_ID in d2t1_IDs and not len(file_lines) == 1779:
                            raise Exception(f'  Error line numbers!\n\t{filename} should have 1,779 lines (found {len(file_lines)}).')
                        # Check line numbers in D2T-2 data
                    elif task_ID in d2t2_IDs and not len(file_lines) == 1800:
                        raise Exception(f'  Error line numbers!\n\t{filename} should have 1,800 lines (found {len(file_lines)}).')
                    else:
                        pass
                        #print('  OK!')
                # json files are for the summ task; check well-formedness
                elif extension == 'json':
                    try:
                        json.loads(content)
                    except:
                        raise Exception(f'  Error json formatting! Check {filename_noExt}.')
                    # There should additional be code to check the number of outputs in the submitted files
                else:
                    raise Exception(f'  Error filename system name!\n\t{filename_noExt} should have a name before the task suffix.')
            else:
                raise Exception(f'  Error filename task suffix!\n\t{filename_noExt} should contain one of these task suffixes: {task_suffixes}.')
        else:
            raise Exception(f'  Error filename language suffix!\n\t{filename_noExt} should end with one of these language suffixes: {languages}.')
    else:
        raise Exception(f'  Error filename extension!\n\t{filename} should have one of these extensions (according to task): {extensions}.')

def gemv3submit(request):

    if request.method == "POST":
        team_name = request.POST['name']
        
        email = request.POST['email']
        submission_track =  "Tracks_" + '_'.join(request.POST.getlist('submission_track'))

        try:
            uploaded_file = request.FILES['gemv3file']
            
            file_in_memory = BytesIO(uploaded_file.read())

            with tarfile.open(fileobj=file_in_memory, mode="r:gz") as tar:
                required_files = ['file1.txt', 'file2.txt']
                extracted_files = tar.getnames()

                pattern = r'^(?!.*\/\._).*\.(txt|jsonl)$'
        
                if len([filename for filename in tar.getnames() if re.match(pattern, filename)]) == 0:
                    raise Exception('No valid files present.')

                
                # CODE: Add checking code to make sure that required files are present
                for fn, member in zip(tar.getnames(), tar.getmembers()):
                    if not re.match(pattern, fn):
                        continue

                    if 1:#member.name in required_files:
                        # Extract file content from tar
                        f = tar.extractfile(member)
                        if f is not None:
                            check_GEM_submissions(fn, f)

            uploaded_file.seek(0)
            if upload_gemv3_file('gemv3_submissions/' +  team_name + '_' + submission_track + '.tar.gz', request.FILES['gemv3file']):
                send_email("teamchateval@gmail.com", "GEM V3 submission", email)
                send_email(email, "GEM V3 submission received", "Thank you for your submission")
                return HttpResponseRedirect('https://gem-benchmark.com/shared_task')
        except Exception as e:
            # Catching the exception and retrieving its traceback
            error_traceback = traceback.format_exc()
            # Constructing the error message
            error_message = str(e)
            # Concatenating the error message with the traceback
            error = f"Error Message: {error_message}\nTraceback:\n{error_traceback}"
            form = GEMV3Form()
            
            return render(request, 'gemv3submit.html', {'form': form, 'error': error})

    form = GEMV3Form()
    error = "error" in request.GET
    return render(request, 'gemv3submit.html', {'form': form, 'error': error})
