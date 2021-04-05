from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import ContactForm, ParagraphErrorList
from django.db import transaction, IntegrityError
#from django.http import HttpResponse
#from django.template import loader
from .models import *
# Create your views here.
@transaction.non_atomic_requests
def index(request):
    albums    = Album.objects.filter(available=True).order_by('-created_at')[:12]  
    context = {'title': 'Super titre hein ?'}
    #formatted_albums = ["<li>{}</li>".format(album.title) for album in albums]
    # message = """<ul>{}</ul>""".format("\n".join(formatted_albums))
    template = loader.get_template(r"D:\\Programmation\\Python\\Projet_INITIATION_django\\test\disquaire_project\\store\templates\\store\\index.html")
    return render(request, 'store/index.html', context)

def listing(request):
    albums_list = Album.objects.filter(available=True)
    
    paginator = Paginator(albums_list, 3)
    page      = request.GET.get('page')
    try:
        albums = paginator.page(page)
    except PageNotAnInteger:
        albums = paginator.page(1)
    except EmptyPage:
        albums = paginator.page(paginator.num_pages)
        
    context = {
        'albums':albums,
        'paginate': True
    }
    #formatted_albums = ["<li>{}</li>".format(album.title) for album in albums]
    #message = """<ul>{}</ul>""".format("\n".join(formatted_albums))
    return render(request, 'store/listing.html', context)

@transaction.atomic
def detail(request, album_id):
    #album   = Album.objects.get(pk=album_id) # get the album with its id.
    album = get_object_or_404(Album, pk=album_id)
    artists = [artist.name for artist in album.artists.all()] # grab artists name and create a string out of it.
    artists_name = " ".join(artists)
    context = {
        'albums_title':album.title,
        'artists_name': artists_name,
        'album_id': album.id,
        'thumbnail': album.picture, 
    }
    if request.method == 'POST':
        form  = ContactForm(request.POST, error_class=ParagraphErrorList)
        if form.is_valid():        
            name  = form.cleaned_data['name']
            email = form.cleaned_data['email']
            try:
                with transaction.atomic():
                    contact = Contact.objects.filter(email=email)
                    if not contact.exists():
                        contact = Contact.objects.create(
                            email = email,
                            name  = name
                        )
                    else:
                        contact = contact.first()
                    album   = get_object_or_404(Album, id=album_id)
                    booking = Booking.objects.create(
                        contact = contact,
                        album   = album
                    )
                    album.available = False
                    album.save()
                    context = {
                        'album_title': album.title
                    }
                    return render(request,'store/merci.html', context)
            
            except IntegrityError:
                form.errors['internal'] = "Une erreur interne est apparue. Merci de recommencer votre requête"
        
    else:
        form = ContactForm()   
        

    context['form'] = form    
    context['errors'] = form.errors.items() 
    
    return render(request, 'store/detail.html', context)

def search(request):
    query   = request.GET.get('query')
    if not query:
        albums = Album.objects.all()
    else:
        albums = Album.objects.filter(title__icontains=query)
        
        if not albums.exists():
            albums = Album.objects.filter(artists__name__icontains=query)
        title = "Résultats pour la requête %s"%query
        context = {
            'albums': albums,
            'title': title
        }
    return render(request, 'store/search.html', context)