from django.shortcuts import render, redirect
from .forms import SuiteForm, ProtectedSuiteForm
from .models import Suite, Task, Attachment
from django.urls import reverse
from django.template import RequestContext


def intro(request):
    # Ok i didn't saw this
    # Here, when you init the form, it should get some data in it
    form = SuiteForm(request.POST or None)  # if request is POST, it'll have POST data
    context = {
        "form": form
    }
    if request.method == 'POST':
        if form.is_valid():
            # This is kinda important, if commit=False, which is not by default
            # then we can save the form first, do some other changes on the resulted object
            # and only then save the results
            suite = form.save(commit=False) 
            # Here is why it's so useful. We have created_by field, which we want to use
            # to understand who added the entry, we do this:
            # Ok now if you submit the form in browser, you'll see an error
            # That is because our request.user is anonymous, because this
            # intro view is not protected
            # Let's make it protected
            suite.created_by = request.user
            # And that's it. We have the user associated in the model instance
            suite.save()  # This is where DB query is done. Let's see how it works
            # Here, after we save the suite, we add manytomany entries
            number = form.cleaned_data["number"]
            # Ok now we have a number, we need to fetch some entries from db, right
            # But we need to know the lang
            language = form.cleaned_data["language"][0] # ok it comes as list
            # Now we are ready to get the DB entries
            password = form.cleaned_data["password"]
            if number < 0 :
                return render(request, "intro.html", context)
            else:
                # now connect this to Suite
                tasks = Task.objects.filter(language=language).order_by("?")[:number] # Random ordering, limit the result to what we need
                suite.tasks.add(*tasks)
            #how bout adding the tasks to suite using for loop
            # it's not required actuallyu, the issue was with language, it comes as list, cause it's a select, but
            # it should be fine now
            # So when we get the suite object, we can redirect the user to 
            # a /s/<somecode> url
            # it's done like this:
            # reverse function does what it's named for, it reverses
            # the url by it's name
            if not password:
                return redirect(reverse("show_suite", kwargs={"code": suite.code}))
            else:
                return redirect(reverse("password_form", kwargs={"code": suite.code, "password": password}))
        else:
            print(form.errors)
    # Usually if we have the return inside the if, we'll skip else, cause if
    # the condition is True, then we just return from the function, no need for
    # a new branch in code
    # this will be reachable only if if request.method is POST
    return render(request, "intro.html", context)






def password_form(request, code, password):
    form = ProtectedSuiteForm(request.POST or None)  # if request is POST, it'll have POST data
    context = {
        "form": form,
    }
    if request.method == 'POST':
        if form.is_valid():
            pf = form.save(commit=False) 
            pf.created_by = request.user
            pf.save()
            Password = form.cleaned_data["password"]
            suite = Suite.objects.get(code=code, password=password)
            final = Suite.objects.filter(password=password,code=code)
            context = {
                "suite": suite,
                "final": final
            }
            if Password==password:
                return redirect(reverse("protected_suite", kwargs={"code": code, "password": password}))
            elif Password!=password:
                return render(request, "password_form.html", context)
        else:
            print(form.errors)
    return render(request, "password_form.html", context)






def show_suite(request, code):
    """ Get suite from DB and render in template """
    suite = Suite.objects.get(code=code)
    # Context dict keys are always snake_case
    context = {
        "suite": suite,
    }
    return render(request, "show.html", context)





def protected_suite(request, code, password):
    suite = Suite.objects.get(code=code, password=password)
    # Context dict keys are always snake_case
    context = {
        "suite": suite,
    }
    return render(request, "show.html", context)





def show_files(request):
    objects = Attachment.objects.all()
    context = {
         {'objects': objects}
    }
    return render('show.html',context, context_instance=RequestContext(request))