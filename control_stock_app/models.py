# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from re import M
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.db.models.fields import CharField
from django.db.models.fields.related import ForeignKey


class Articulos(models.Model):
    nombre = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    precio_unitario = models.FloatField(blank=True, null=True)
    id_marca = models.ForeignKey('Marcas', models.DO_NOTHING, db_column='id_marca', blank=True, null=True)
    id_categoria = models.ForeignKey('Categorias', models.DO_NOTHING, db_column='id_categoria', blank=True, null=True)
    id_unidad_medida = models.ForeignKey('UnidadesMedida', models.DO_NOTHING, db_column='id_unidad_medida', blank=True, null=True)
    cantidad_medida = models.IntegerField(blank=True, null=True)
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


class DetallesPedido(models.Model):
    id_pedido = models.ForeignKey('Pedidos', models.DO_NOTHING, db_column='id_pedido', blank=True, null=True)
    id_articulo = models.ForeignKey(Articulos, models.DO_NOTHING, db_column='id_articulo', blank=True, null=True)
    cantidad = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detalles_pedido'


class DetallesTraspaso(models.Model):
    id_traspaso = models.ForeignKey('Traspasos', models.DO_NOTHING, db_column='id_traspaso', blank=True, null=True)
    id_articulo = models.ForeignKey(Articulos, models.DO_NOTHING, db_column='id_articulo', blank=True, null=True)
    cantidad = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detalles_traspaso'


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
    id_articulo = models.ForeignKey(Articulos, models.DO_NOTHING, db_column='id_articulo')
    id_deposito = models.ForeignKey(Depositos, models.DO_NOTHING, db_column='id_deposito')
    cantidad = models.IntegerField(blank=True, null=True)
    ingreso = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'movimiento_deposito'
        unique_together = (('id_articulo', 'id_deposito'),)


class Pedidos(models.Model):
    fecha = models.DateField(blank=True, null=True)
    numero_remito_asociado = models.IntegerField(blank=True, null=True)
    id_tipo_estado = models.ForeignKey('TiposEstado', models.DO_NOTHING, db_column='id_tipo_estado', blank=True, null=True)
    observaciones = models.CharField(max_length=50, blank=True, null=True)
    id_proveedor = models.ForeignKey('Proveedores', models.DO_NOTHING, db_column='id_proveedor', blank=True, null=True)
    id_deposito_destino = models.ForeignKey(Depositos, models.DO_NOTHING, db_column='id_deposito_destino', blank=True, null=True)
    id_usuario_proceso = models.ForeignKey(User, models.DO_NOTHING, db_column='id_usuario_proceso', blank=True, null=True)
    fh_procesado = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pedidos'


class Proveedores(models.Model):
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'proveedores'


class RolesUsuarios(models.Model):
    id_usuario = models.OneToOneField(User, models.DO_NOTHING, db_column='id_usuario', primary_key=True)
    id_tipo_rol = models.ForeignKey('TiposRol', models.DO_NOTHING, db_column='id_tipo_rol', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles_usuarios'


class TiposEstado(models.Model):
    descripcion = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipos_estado'


class TiposRol(models.Model):
    descripcion = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'tipos_rol'


class Traspasos(models.Model):
    fh_generacion = models.DateTimeField(blank=True, null=True)
    id_tipo_estado = models.ForeignKey(TiposEstado, models.DO_NOTHING, db_column='id_tipo_estado', blank=True, null=True)
    observaciones = models.CharField(max_length=50, blank=True, null=True)
    id_deposito_origen = models.ForeignKey(Depositos, models.DO_NOTHING, db_column='id_deposito_origen', blank=True, null=True, related_name='id_deposito_origen')
    id_deposito_destino = models.ForeignKey(Depositos, models.DO_NOTHING, db_column='id_deposito_destino', blank=True, null=True, related_name='id_deposito_destino')
    id_usuario_genero = models.ForeignKey(User, models.DO_NOTHING, db_column='id_usuario_genero', blank=True, null=True, related_name='id_usuario_genero')
    id_usuario_proceso = models.ForeignKey(User, models.DO_NOTHING, db_column='id_usuario_proceso', blank=True, null=True, related_name='id_usuario_proceso')
    fh_procesado = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'traspasos'


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


class UsuarioDto(models.Model):

    id = models.IntegerField(primary_key=True)
    usuario = models.CharField(max_length=150)
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150)
    email = models.EmailField()
    ult_conexion = models.DateTimeField()
    rol = models.CharField(max_length=50)
    id_tipo_rol = models.IntegerField()
    password = models.CharField(max_length=50)


class DepositoDtoInsert(models.Model):
  
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    domicilio = models.CharField(max_length=50)
    barrio = models.CharField(max_length=50)
    id_localidad = models.IntegerField()
    id_encargado = models.IntegerField()
    activo = models.BooleanField(default=True)  # This field type is a guess.
    
    
class DepositoDto(models.Model):

    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    domicilio = models.CharField(max_length=50)
    barrio = models.CharField(max_length=50)
    localidad = models.CharField(max_length=50)
    encargado = models.CharField(max_length=50)

    
class EncargadoDto(models.Model):

    id = models.IntegerField(primary_key=True),
    descripcion = models.CharField(max_length=100)


class ArticuloDto(models.Model):

    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    precio_unitario = models.FloatField()
    id_marca = models.IntegerField()
    marca = models.CharField(max_length=50)
    id_categoria = models.IntegerField()
    categoria = models.CharField(max_length=50)
    id_unidad_medida = models.IntegerField()
    unidad_medida = models.CharField(max_length=50)
    cantidad_medida = models.IntegerField()

class ExistenciaDto(models.Model):

    id_articulo = models.IntegerField(primary_key=True)
    nombre_articulo = models.CharField(max_length=50)
    id_deposito = models.IntegerField()
    cantidad = models.IntegerField()
    stock_minimo = models.IntegerField()
    stock_maximo = models.IntegerField()
    id_lote = models.IntegerField()


class TraspasoDtoInsert(models.Model):

    id = models.IntegerField(primary_key=True)
    fecha = models.DateTimeField(blank=True, null=True)
    id_tipo_estado = models.IntegerField()
    tipo_estado = models.CharField(max_length=50)
    observaciones = models.CharField(max_length=50)
    id_deposito_origen = models.IntegerField()
    id_deposito_destino = models.IntegerField()
    id_usuario_genero = models.IntegerField()
    
class DetalleTraspasoDto(models.Model):

    id = models.IntegerField(primary_key=True)
    id_traspaso = models.IntegerField()
    id_articulo = models.IntegerField()
    nombre_articulo = models.CharField(max_length=50)
    cantidad_articulo = models.IntegerField()