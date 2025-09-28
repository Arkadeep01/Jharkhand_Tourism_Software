import firebase_admin
from firebase_admin import credentials

from Profile_Section.Core.config import settings

cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
firebase_app = firebase_admin.initialize_app(cred)
