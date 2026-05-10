from django.shortcuts import render

from rest_framework.view import APIView
# Create your views here.


class RegistrationView(APIView):

    # classe erstellen
    # request mit data bekommen
    # request erlaubt?
    # ja -> in datenbank speichern und object zurückgeben (mit serializer erstellen??)
    # wenn nein, fehlercode zurückwerfen.