from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import User, Listing, Watchlist, Comment, Bid
from .forms import ListingForm


def index(request):
    items = Listing.objects.all()

    context = {
        'items': items,


    }
    return render(request, "auctions/index.html", context)


def listing(request, pk):
    user = request.user
    listing = Listing.objects.get(id=pk)
    bid = listing.starting_bid
    owner = listing.user
    if request.user.is_authenticated:
        if request.method == "POST":
            made_bid = int(request.POST.get('bid'))
            if made_bid <= bid:
                messages.warning(request, 'You have to make a higher bid')
                return redirect("index")
            else:
                new_bid = Bid(
                    price=made_bid, user=user, listing=listing)

                Listing.objects.filter(id=pk).update(
                    starting_bid=new_bid.price)
                new_bid.save()
                print(new_bid.user)
                messages.success(request, 'Your bid was placed')
                return redirect("index")
    context = {
        'listing': listing,
        'pk': pk,
        'comments': Comment.objects.filter(listing=listing),
    }

    return render(request, "auctions/listing.html", context)


def comment(request, pk):
    user = request.user
    listing = Listing.objects.get(id=pk)

    if request.user.is_authenticated:
        if request.method == "POST":
            comment = request.POST.get('comment')
            new_comment = Comment(
                comment=comment, user=user, listing=listing)
            new_comment.save()
    else:
        messages.warning(request, 'You must be logged in for this action')

    context = {
        'listing': listing,
        'comments': Comment.objects.filter(listing=listing),
        'pk': pk,
    }

    return render(request, "auctions/listing.html", context)


@login_required
def close(request, pk):
    item = Listing.objects.get(id=pk)
    owner = item.user

    if owner and item.active:
        if request.method == "POST":
            if request.POST.get("deactivate"):
                item.active = False
                item.save()

    return redirect("index")


def categories(request):
    categories = Listing.objects.values_list(
        'category', flat=True,).distinct()

    context = {
        'categories': categories,

    }
    return render(request, "auctions/categories.html", context)


def category(request, category):
    category_items = Listing.objects.filter(category=category)

    context = {
        'category_items': category_items,
        'category': category,

    }
    return render(request, "auctions/category.html", context)


@login_required
def create_listing(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid:
            listing = form.save(commit=False)
            listing.user = user
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create.html", {
                "form": form
            })
    else:
        return render(request, "auctions/create.html", {
            "form": ListingForm()
        })


@login_required
def watchlist(request):

    if request.user.is_authenticated:
        user = request.user
        items = user.watchlist.all()

    else:
        return redirect('index')

    context = {
        'title': f"{user.username}'s Watchlist",
        'items': items,
        'user': user

    }

    return render(request, 'auctions/watchlist.html', context)


@login_required
def watchlist_remove(request, listing_pk):
    user = request.user
    listing = Listing.objects.get(pk=listing_pk)
    print(listing)
    context = {
        'listing_pk': listing_pk
    }
    if Watchlist.objects.filter(user=user, listing=listing).exists():
        Watchlist.objects.filter(user=user, listing=listing).delete()
        messages.success(request, f'{listing.title} removed from watchlist.')

    return HttpResponseRedirect(reverse('watchlist'))


@login_required
def watchlist_add(request, listing_pk):
    user = request.user

    listing = Listing.objects.get(pk=listing_pk)
    context = {
        'listing_pk': listing_pk,

    }

    if Watchlist.objects.filter(user=user, listing=listing).exists() == False:
        watchlist_entry = Watchlist(user=user, listing=listing)
        watchlist_entry.save()
        messages.success(request, f'{listing.title} added to watchlist.')
    else:
        messages.warning(
            request, f'{listing.title} already in your watchlist.')
    return HttpResponseRedirect(reverse('watchlist'))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
