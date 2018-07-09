import os
import uuid
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import FileExtensionValidator, validate_image_file_extension
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from imagekit.models import ProcessedImageField, ImageSpecField
from positions.fields import PositionField
from imagekit.processors import ResizeToFit


class Categoria(MPTTModel):
    nombre = models.CharField(max_length=150)
    slug = AutoSlugField(populate_from='nombre', unique_with='parent')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    def __str__(self):
        return self.nombre


class Documento(models.Model):
    extensiones = ['pdf', 'doc', 'docx', 'xls', 'xlxs', 'ppt', 'pptx', 'odt', 'ods', 'odt']
    file = models.FileField(null=True, blank=True, upload_to='documentos/',
                            validators=[FileExtensionValidator(allowed_extensions=extensiones)])
    contenido = models.ForeignKey('Contenido', on_delete=models.CASCADE, null=True, blank=True, related_name='documentos')

    def __str__(self):
        return self.file.name

    @property
    def filename(self):
        return self.file.name.rsplit('/', 1)[1]


class Contenido(models.Model):
    extensiones = ['pdf', 'doc', 'docx', 'xls', 'xlxs', 'ppt', 'pptx', 'odt', 'ods', 'odt']
    def get_upload_path(self, filename):
        return 'uploadfiles/{0}/{1}'.format(self.slug, filename)

    categoria = models.ForeignKey('Categoria')
    user = models.ForeignKey(User)
    titulo = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='titulo', unique=True)
    copete = models.CharField(max_length=255)
    detalle = RichTextField()
    fecha_publicacion = models.DateField()
    activo = models.BooleanField()
    recomendado = models.BooleanField()
    imagen = models.ImageField(blank=True, upload_to=get_upload_path, default='imagenes/no-image.png',
                               validators=[validate_image_file_extension])
    documento = models.FileField(null=True, blank=True, upload_to=get_upload_path,
                                 validators=[FileExtensionValidator(allowed_extensions=extensiones)])

    def __str__(self):
        return "%s [%s]" % (self.titulo, self.categoria)

    @property
    def filename(self):
        return self.documento.name.rsplit('/', 1)[1]


class Galeria(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = RichTextField()
    activa = models.BooleanField(default=True)
    recomendada = models.BooleanField(default=True)
    creada = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(populate_from='titulo', unique=True)

    def get_absolute_url(self):
        return reverse('backend:galeria_edit', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-creada']

    def __str__(self):
        return self.slug


class GaleriaImagen(models.Model):
    def get_upload_path(self, filename):
        return 'galerias/{0}/{1}'.format(self.galeria.slug, filename)

    file = models.ImageField(upload_to=get_upload_path, validators=[validate_image_file_extension])
    thumb = ImageSpecField(source='file', processors=[ResizeToFit(150)], format='JPEG',
                           options={'quality': 60})
    galeria = models.ForeignKey('Galeria', on_delete=models.CASCADE, null=True, related_name='imagenes')
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    slug = AutoSlugField(populate_from='file', unique=True)

    def __str__(self):
        return self.file.name

    @property
    def filename(self):
        return self.file.name.rsplit('/',1)[1]

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.file.name))
        try:
            galeria_path = 'galerias/{0}'.format(self.galeria.slug)  # Borrar el archivo
            os.rmdir(os.path.join(settings.MEDIA_ROOT, galeria_path))  # Borrar el directorio de la Galeria
        except OSError:
            pass
        super(GaleriaImagen, self).delete(*args, **kwargs)


class ListSlider(models.Model):
    def get_aleatorio(self):
        d = uuid.uuid4()
        return d.hex[0:16]

    nombre = models.CharField(max_length=18, default=get_aleatorio, unique=True)


class Slider(models.Model):
    lista = models.ForeignKey('ListSlider', on_delete=models.CASCADE, null=True, blank=True)
    file = models.ImageField(upload_to='sliders/', validators=[validate_image_file_extension])
    texto = models.CharField(max_length=255, null=True, blank=True)
    texto_enlace = models.CharField(max_length=255, null=True, blank=True)
    enlace = models.URLField(null=True, blank=True)
    activa = models.BooleanField(default=True)
    posicion = PositionField(default=0, collection='lista')
    creada = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['posicion', '-creada']

    def __str__(self):
        return self.texto

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.file.name))
        super(Slider, self).delete(*args, **kwargs)


# Corresponde a las Estadisticas del Home (Los 4 counters)
class Estadistica(models.Model):
    icono = models.CharField(max_length=50)
    dato = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)

    class Meta:
        ordering = ['-id']


class ListDistribucion(models.Model):
    def get_aleatorio(self):
        d = uuid.uuid4()
        return d.hex[0:16]

    nombre = models.CharField(max_length=18, default=get_aleatorio, unique=True)


class Distribucion(models.Model):
    lista = models.ForeignKey('ListDistribucion', on_delete=models.CASCADE, null=True, blank=True)
    titulo = models.CharField(max_length=150)
    mujer = models.PositiveIntegerField()
    hombre = models.PositiveIntegerField()
    posicion = PositionField(default=0, collection='lista')

    class Meta:
        ordering = ['posicion']

    def __str__(self):
        return "{0} (M={1} - H={2})".format(self.titulo, self.mujer, self.hombre)


class ListEnlace(models.Model):
    def get_aleatorio(self):
        d = uuid.uuid4()
        return d.hex[0:16]

    nombre = models.CharField(max_length=18, default=get_aleatorio, unique=True)


class GrupoEnlace(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre


class Enlace(models.Model):
    lista = models.ForeignKey('ListEnlace', on_delete=models.CASCADE, null=True, blank=True)
    grupo = models.ForeignKey(GrupoEnlace)
    titulo = models.CharField(max_length=255)
    enlace = models.URLField()
    posicion = PositionField(default=0, collection='lista')

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['grupo', 'posicion']


class Curso(models.Model):
    titulo = models.CharField(max_length=255)
    enlace = models.URLField()

    def __str__(self):
        return self.titulo


class Dependencia(models.Model):
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=200)
    departamento = models.CharField(max_length=200)
    telefono1 = models.CharField(max_length=200, blank=True)
    telefono2 = models.CharField(max_length=200, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['departamento', 'ciudad']

