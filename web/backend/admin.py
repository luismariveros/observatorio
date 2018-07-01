import os
import uuid
import zipfile
import web.settings

from datetime import datetime
from zipfile import ZipFile

from django.contrib import admin
from django.core.files.base import ContentFile

from PIL import Image

from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import *
from .forms import *


class AlbumModelAdmin(admin.ModelAdmin):
    form = GaleriaNewForm
    #prepopulated_fields = {'slug': ('titulo',)}
    list_display = ('titulo', )
    list_filter = ('creada',)

    # def save_model(self, request, obj, form, change):
    #     if form.is_valid():
    #         album = form.save(commit=False)
    #         #album.modified = datetime.now()
    #         album.save()
    #
    #         if form.cleaned_data['zip']:
    #             zip = zipfile.ZipFile(form.cleaned_data['zip'])
    #             for filename in sorted(zip.namelist()):
    #
    #                 file_name = os.path.basename(filename)
    #                 if not file_name:
    #                     continue
    #
    #                 data = zip.read(filename)
    #                 contentfile = ContentFile(data)
    #                 print(contentfile)
    #
    #                 img = Foto()
    #                 img.galeria = album
    #                 #img.alt = filename
    #                 filename = '{0}{1}.jpg'.format(album.slug, str(uuid.uuid4())[-13:])
    #                 img.file.save(filename, contentfile)
    #
    #                 filepath = '{0}/galerias/{1}/{2}'.format(web.settings.MEDIA_ROOT, album.titulo, filename)
    #                 print(filepath, filename)
    #                 with Image.open(filepath) as i:
    #                     img.width, img.height = i.size
    #
    #                 img.thumb.save('thumb-{0}'.format(filename), contentfile)
    #                 img.save()
    #             zip.close()
    #         super(AlbumModelAdmin, self).save_model(request, obj, form, change)
    #
admin.site.register(Galeria, AlbumModelAdmin)
admin.site.register(GaleriaImagen)
admin.site.register(Categoria, MPTTModelAdmin)
admin.site.register(Contenido)
admin.site.register(Estadistica)
admin.site.register(Distribucion)
admin.site.register(GrupoEnlace)