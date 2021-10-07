# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey


class Articulos(models.Model):
    nombre = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    precio_unitario = models.FloatField(blank=True, null=True)
    id_marca = models.ForeignKey('Marcas', models.DO_NOTHING, db_column='id_marca', blank=True, null=True)
    id_categoria = models.ForeignKey('Categorias', models.DO_NOTHING, db_column='id_categoria', blank=True, null=True)
    id_unidad_medida = models.ForeignKey('UnidadesMedida', models.DO_NOTHING, db_column='id_unidad_medida', blank=True, null=True)
    cantidad_medida = models.FloatField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    def is_activo(self):
        return bool(ord(self.activo))

    class Meta:
        managed = False
        db_table = 'articulos'


class Categorias(models.Model):
    descripcion = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'categorias'


class Depositos(models.Model):
    nombre = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    domicilio = models.CharField(max_length=50, blank=True, null=True)
    barrio = models.CharField(max_length=50, blank=True, null=True)
    id_localidad = models.ForeignKey('Localidades', models.DO_NOTHING, db_column='id_localidad', blank=True, null=True)
    id_encargado = models.ForeignKey(User, models.DO_NOTHING, db_column='id_encargado', blank=True, null=True)
    activo = models.BooleanField(default=True)  # This field type is a guess.

    def is_activo(self):
        return bool(ord(self.activo))
    class Meta:
        managed = False
        db_table = 'depositos'


class DepositosUsuarios(models.Model):
    id_deposito = models.OneToOneField(Depositos, models.DO_NOTHING, db_column='id_deposito', primary_key=True)
    id_usuario = models.ForeignKey(User, models.DO_NOTHING, db_column='id_usuario')

    class Meta:
        managed = False
        db_table = 'depositos_usuarios'
        unique_together = (('id_deposito', 'id_usuario'),)

class Existencias(models.Model):
    id_articulo = models.OneToOneField(Articulos, models.DO_NOTHING, db_column='id_articulo', primary_key=True)
    id_deposito = models.ForeignKey(Depositos, models.DO_NOTHING, db_column='id_deposito')
    cantidad = models.IntegerField(blank=True, null=True)
    stock_minimo = models.IntegerField(blank=True, null=True)
    stock_maximo = models.IntegerField(blank=True, null=True)
    id_lote = models.ForeignKey('Lotes', models.DO_NOTHING, db_column='id_lote', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'existencias'
        unique_together = (('id_articulo', 'id_deposito'),)


class Localidades(models.Model):
    descripcion = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'localidades'


class Lotes(models.Model):
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    fecha_fabricacion = models.DateField(blank=True, null=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    id_proveedor = models.ForeignKey('Proveedores', models.DO_NOTHING, db_column='id_proveedor', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lotes'


class Marcas(models.Model):
    descripcion = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'marcas'


class MovimientoDeposito(models.Model):
    id_articulo = models.OneToOneField(Articulos, models.DO_NOTHING, db_column='id_articulo', primary_key=True)
    id_deposito = models.ForeignKey(Depositos, models.DO_NOTHING, db_column='id_deposito')
    cantidad = models.IntegerField(blank=True, null=True)
    ingreso = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'movimiento_deposito'
        unique_together = (('id_articulo', 'id_deposito'),)


class Proveedores(models.Model):
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'proveedores'


class TiposRol(models.Model):
    descripcion = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'tipos_rol'


class UnidadesMedida(models.Model):
    descripcion = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'unidades_medida'

class RolesUsuarios(models.Model):
    id_usuario = models.OneToOneField(User, models.DO_NOTHING, db_column='id_usuario', primary_key=True)
    id_tipo_rol = models.ForeignKey('TiposRol', models.DO_NOTHING, db_column='id_tipo_rol', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles_usuarios'


class Usuario(models.Model):

    id = models.IntegerField(primary_key=True)
    usuario = models.CharField(max_length=150)
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150)
    email = models.EmailField()
    ult_conexion = models.DateTimeField()
    rol = models.CharField(max_length=50)