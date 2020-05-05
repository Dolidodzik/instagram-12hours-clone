from django.core.management.base import BaseCommand, CommandError
from core.models import *
import random
import datetime
from random_words import RandomWords
from random import randrange


rw = RandomWords()
def createRandomWords(count=10):
    return ", ".join(rw.random_words(count=randrange(count)+1))

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('iterations', type=int)

    def handle(self, *args, **options):
        print("Started feeddatabase command...")
        print("Creating N users and 3N Posts,N/50 chats (each for 10-20 messages that are 5-10 words long)...")
        iterations = options['iterations']
        procent_of_iterations = iterations/100
        date = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        for i in range(iterations):

            # Users creation
            user = CustomUser.objects.create_user(username=str('john'+str(i)+str(date)), email='sth@sth.com', password='toor')
            user.description = createRandomWords(25)
            profile.save()

            # Creating some messages/conversations
            if i % 100 == 0 or i == 1:
                root = User.objects.filter(username="root").first()
                if not root:
                    print("\n\n FIRST YOU NEED TO CREATE USER NAMED ROOT, TO FEEDDATABASE. THIS CAN BE DONE USING: python manage.py createsuperuser \n\n")



            # Posts creation
            for j in range(3):
                post = Post(title=str(createRandomWords(2)+str(i)+str(j)), description=createRandomWords(15), owner=user)
                post.save()

            # Printing progress
            if i%procent_of_iterations==0:
                print(str(i/procent_of_iterations)+"%")
        print("Succesfully created all excepted records")
