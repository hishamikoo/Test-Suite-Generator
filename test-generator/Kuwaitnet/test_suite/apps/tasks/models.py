import string
import random
from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Attachment(models.Model):
    """ Stores attachment for Task """
    file = models.FileField(upload_to = "uploads", blank=False)

    def display_text_file(self):
        with open(self.file.path) as fp:
            return fp.read()


    def __str__(self):
        return f"{self.file}"


class Task(models.Model):
    """ Main model, contains task information and attachments """
    # settings.AUTH_USER_MODEL this may be empty in some cases, let me show
    # what you do instead get_user_model will return the current used User model
    # in most cases you'll have a customized user model, but that function will return
    # it anyway
    LANGUAGE_CHOICES = (
        ("Java", "Java"),
        ("Python", "Python"),
        ("C++", "C++"),
        ("C", "C"),
        ("C#", "C#"),
        ("Prolog", "Prolog"),
        ("R", "R"),
        ("Rust", "Rust"),
        ("SQL", "SQL")
    )

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)
    text = models.CharField(max_length=2000)
    dificulty = models.IntegerField(default=1)
    attachments = models.ManyToManyField("tasks.Attachment")



    def __str__(self):
        # You use this styling for strings in 2022 in three cases
        # 1) You want to use gettext, and then substitude the strings in it
        # 2) You are over 70 years old
        # 3) You feeling hip
        # in most cases you want to use the f-strings
        # They are faster. And look cool. 
        return f"{self.language} {self.created} {self.created_by}"


class Suite(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=10, null=True, blank=False)
    tasks = models.ManyToManyField("tasks.Task")
    password = models.TextField(default="")

    def __str__(self):
        return f"{self.created} {self.created_by}"

    def _generate_code(self):
        # _ before the method name means that it's not "public" and we going to use it inside the class
        # here we use string's .join method, it can take any iterable of strings and make a new string from them
        # random.choice chooses 1 random from iterable. 
        return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))

    # Here we can do this
    def save(self, *args, **kwargs):
        # this will override save method of the model
        if not self.code:
            # here we generate the code
            self.code = self._generate_code()
        # super() is the call to parent of the Suite model, which is models.Model
        # basically the line below calls to the save method of models.Model
        # Sure. Let me give you an example better. 
        super().save(*args, **kwargs) #can you explain whats the use of *args and **kwargs in this line


    # Here you made the code as auto field, it's not correct
    # as per docs i provided it should be a charfield, which will be populated
    # on save with alphanumeric
    # fix that later please