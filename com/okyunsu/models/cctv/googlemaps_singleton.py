import googlemaps

class GoogleMapsSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = googlemaps.Client(key="")
        return cls._instance

gmaps1 = GoogleMapsSingleton()
gmaps2 = GoogleMapsSingleton()

print("🐮🤑🐶😆🐺",gmaps1 is gmaps2)