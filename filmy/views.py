from django.shortcuts import render, redirect
from .mongo import get_db

def przelicz_ocene_filmu(db, tytul_filmu):
    recenzje = list(db.recenzje.find({'film': tytul_filmu}, {'ocena': 1}))
    if recenzje:
        srednia = sum(r['ocena'] for r in recenzje) / len(recenzje)
        db.filmy.update_one({'tytul': tytul_filmu}, {'$set': {'ocena': round(srednia, 1)}})

def index(request):
    db = get_db()
    return render(request, 'filmy/index.html', {
        'liczba_filmow': db.filmy.count_documents({}),
        'liczba_rezyserow': db.rezyserzy.count_documents({}),
        'liczba_recenzji': db.recenzje.count_documents({}),
    })

def filmy_lista(request):
    db = get_db()
    return render(request, 'filmy/filmy_lista.html', {
        'filmy': list(db.filmy.find({}, {'_id': 0}))
    })

def filmy_dodaj(request):
    if request.method == 'POST':
        db = get_db()
        ostatni = db.filmy.find_one(sort=[('id', -1)])
        film = {
            'id': (ostatni['id'] + 1) if ostatni else 1,
            'tytul': request.POST['tytul'],
            'rezyser': request.POST['rezyser'],
            'rok': int(request.POST['rok']),
            'gatunek': request.POST['gatunek'],
            'ocena': float(request.POST['ocena']),
            'kraj': request.POST['kraj'],
        }
        db.filmy.insert_one(film)
        return redirect('filmy_lista')
    return render(request, 'filmy/filmy_dodaj.html')

def filmy_edytuj(request, film_id):
    db = get_db()
    film = db.filmy.find_one({'id': film_id}, {'_id': 0})
    if request.method == 'POST':
        db.filmy.update_one({'id': film_id}, {'$set': {
            'tytul': request.POST['tytul'],
            'rezyser': request.POST['rezyser'],
            'rok': int(request.POST['rok']),
            'gatunek': request.POST['gatunek'],
            'ocena': float(request.POST['ocena']),
            'kraj': request.POST['kraj'],
        }})
        return redirect('filmy_lista')
    return render(request, 'filmy/filmy_edytuj.html', {'film': film})

def filmy_usun(request, film_id):
    db = get_db()
    db.filmy.delete_one({'id': film_id})
    return redirect('filmy_lista')

def filmy_szukaj(request):
    db = get_db()
    wyniki = []
    q = request.GET.get('q', '')
    pole = request.GET.get('pole', 'tytul')
    if q:
        wyniki = list(db.filmy.find(
            {pole: {'$regex': q, '$options': 'i'}},
            {'_id': 0}
        ))
    return render(request, 'filmy/filmy_szukaj.html', {
        'wyniki': wyniki,
        'q': q,
        'pole': pole,
    })

def rezyserzy_lista(request):
    db = get_db()
    return render(request, 'filmy/rezyserzy_lista.html', {
        'rezyserzy': list(db.rezyserzy.find({}, {'_id': 0}))
    })

def rezyserzy_dodaj(request):
    if request.method == 'POST':
        db = get_db()
        ostatni = db.rezyserzy.find_one(sort=[('id', -1)])
        nagrody = [n.strip() for n in request.POST.get('nagrody', '').split(',') if n.strip()]
        rezyser = {
            'id': (ostatni['id'] + 1) if ostatni else 1,
            'nazwisko': request.POST['nazwisko'],
            'imie': request.POST['imie'],
            'narodowosc': request.POST['narodowosc'],
            'urodzony': int(request.POST['urodzony']),
            'nagrody': nagrody,
        }
        db.rezyserzy.insert_one(rezyser)
        return redirect('rezyserzy_lista')
    return render(request, 'filmy/rezyserzy_dodaj.html')

def rezyserzy_edytuj(request, rezyser_id):
    db = get_db()
    rezyser = db.rezyserzy.find_one({'id': rezyser_id}, {'_id': 0})
    if request.method == 'POST':
        nagrody = [n.strip() for n in request.POST.get('nagrody', '').split(',') if n.strip()]
        db.rezyserzy.update_one({'id': rezyser_id}, {'$set': {
            'nazwisko': request.POST['nazwisko'],
            'imie': request.POST['imie'],
            'narodowosc': request.POST['narodowosc'],
            'urodzony': int(request.POST['urodzony']),
            'nagrody': nagrody,
        }})
        return redirect('rezyserzy_lista')
    rezyser['nagrody_str'] = ', '.join(rezyser.get('nagrody', []))
    return render(request, 'filmy/rezyserzy_edytuj.html', {'rezyser': rezyser})

def rezyserzy_usun(request, rezyser_id):
    db = get_db()
    db.rezyserzy.delete_one({'id': rezyser_id})
    return redirect('rezyserzy_lista')

def rezyserzy_szukaj(request):
    db = get_db()
    wyniki = []
    q = request.GET.get('q', '')
    if q:
        wyniki = list(db.rezyserzy.find(
            {'nazwisko': {'$regex': q, '$options': 'i'}},
            {'_id': 0}
        ))
    return render(request, 'filmy/rezyserzy_szukaj.html', {
        'wyniki': wyniki,
        'q': q,
    })

def recenzje_lista(request):
    db = get_db()
    return render(request, 'filmy/recenzje_lista.html', {
        'recenzje': list(db.recenzje.find({}, {'_id': 0}))
    })

def recenzje_dodaj(request):
    if request.method == 'POST':
        db = get_db()
        ostatni = db.recenzje.find_one(sort=[('id', -1)])
        recenzja = {
            'id': (ostatni['id'] + 1) if ostatni else 1,
            'film': request.POST['film'],
            'autor': request.POST['autor'],
            'ocena': int(request.POST['ocena']),
            'tresc': request.POST['tresc'],
            'data': request.POST['data'],
        }
        db.recenzje.insert_one(recenzja)
        przelicz_ocene_filmu(db, recenzja['film'])
        return redirect('recenzje_lista')
    db = get_db()
    filmy = list(db.filmy.find({}, {'_id': 0, 'tytul': 1}))
    return render(request, 'filmy/recenzje_dodaj.html', {'filmy': filmy})

def recenzje_edytuj(request, recenzja_id):
    db = get_db()
    recenzja = db.recenzje.find_one({'id': recenzja_id}, {'_id': 0})
    if request.method == 'POST':
        db.recenzje.update_one({'id': recenzja_id}, {'$set': {
            'film': request.POST['film'],
            'autor': request.POST['autor'],
            'ocena': int(request.POST['ocena']),
            'tresc': request.POST['tresc'],
            'data': request.POST['data'],
        }})
        przelicz_ocene_filmu(db, request.POST['film'])
        return redirect('recenzje_lista')
    return render(request, 'filmy/recenzje_edytuj.html', {'recenzja': recenzja})

def recenzje_usun(request, recenzja_id):
    db = get_db()
    recenzja = db.recenzje.find_one({'id': recenzja_id})
    tytul = recenzja['film'] if recenzja else None
    db.recenzje.delete_one({'id': recenzja_id})
    if tytul:
        przelicz_ocene_filmu(db, tytul)
    return redirect('recenzje_lista')

def recenzje_szukaj(request):
    db = get_db()
    wyniki = []
    q = request.GET.get('q', '')
    pole = request.GET.get('pole', 'film')
    if q:
        wyniki = list(db.recenzje.find(
            {pole: {'$regex': q, '$options': 'i'}},
            {'_id': 0}
        ))
    return render(request, 'filmy/recenzje_szukaj.html', {
        'wyniki': wyniki,
        'q': q,
        'pole': pole,
    })