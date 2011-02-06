# -*- coding: UTF-8 -*-
from django.contrib.auth.backends import ModelBackend
from django.core.validators import email_re
from django.contrib.auth.models import User
from django.db import transaction

from assopy import models
from assopy import settings
from assopy.clients import genro

import logging

log = logging.getLogger('assopy.auth')

class _AssopyBackend(ModelBackend):
    @transaction.commit_on_success
    def linkUser(self, user):
        """
        collega l'utente assopy passato con il backend; crea l'utente remoto se
        necessario.
        """
        if user.assopy_id:
            return user
        name = unicode(user.user).encode('utf-8')
        if not user.verified:
            log.info('cannot link a remote user to "%s": it\'s not verified', name) 
            return

        log.info('a remote user is needed for "%s"', name)
        # il lookup con l'email può ritornare più di un id; non è un
        # problema dato che associo lo user con il backend solo quando ho
        # verificato l'email (e la verifica non è necessaria se si loggano
        # con janrain), quindi posso usare una qualsiasi delle identità
        # remote. Poi un giorno implementeremo il merge delle identità.
        rid = genro.users(email=user.user.email)['r0']
        if rid is not None:
            log.info('an existing match with the email "%s" is found: %s', user.user.email, rid)
        else:
            rid = genro.create_user(user.user.first_name, user.user.last_name, user.user.email)
            log.info('new remote user id: %s', rid)
        user.assopy_id = rid
        user.save()
        return user

class EmailBackend(_AssopyBackend):
    def authenticate(self, email=None, password=None):
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                self.linkUser(user.assopy_user)
                return user
        except User.MultipleObjectsReturned:
            return None
        except User.DoesNotExist:
            # nel db di django non c'è un utente con quella email, ma potrebbe
            # esserci un utente legacy nel backend di ASSOPY
            if not settings.SEARCH_MISSING_USERS_ON_BACKEND:
                return None
            rid = genro.users(email=email, password=password)['r0']
            if rid is not None:
                log.info('"%s" is a valid remote user; a local user is needed', email)
                u = models.User.objects.create_from_backend(rid, email, password=password, verified=True)
                return u.user
            else:
                return None

class JanRainBackend(_AssopyBackend):
    def authenticate(self, identifier=None):
        try:
            i = models.UserIdentity.objects.select_related('user__user').get(identifier=identifier)
        except models.UserIdentity.DoesNotExist:
            return None
        else:
            self.linkUser(i.user)
            return i.user.user