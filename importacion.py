# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Articulos(models.Model):
    nombre = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    precio_unitario = models.FloatField(blank=True, null=True)
    id_marca = models.ForeignKey('Marcas', models.DO_NOTHING, db_column='id_marca', blank=True, null=True)
    id_categoria = models.ForeignKey('Categorias', models.DO_NOTHING, db_column='id_categoria', blank=True, null=True)
    id_unidad_medida = models.ForeignKey('UnidadesMedida', models.DO_NOTHING, db_column='id_unidad_medida', blank=True, null=True)
    cantidad_medida = models.IntegerField(blank=True, null=True)
    activo = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'articulos'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user_id = models.IntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


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
    id_encargado = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='id_encargado', blank=True, null=True)
    activo = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'depositos'


class DepositosUsuarios(models.Model):
    id_deposito = models.OneToOneField(Depositos, models.DO_NOTHING, db_column='id_deposito', primary_key=True)
    id_usuario = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='id_usuario')

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


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


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


class Pedidos(models.Model):
    fecha = models.DateField(blank=True, null=True)
    numero_remito_asociado = models.IntegerField(blank=True, null=True)
    id_tipo_estado = models.ForeignKey('TiposEstado', models.DO_NOTHING, db_column='id_tipo_estado', blank=True, null=True)
    observaciones = models.CharField(max_length=50, blank=True, null=True)
    id_proveedor = models.ForeignKey('Proveedores', models.DO_NOTHING, db_column='id_proveedor', blank=True, null=True)
    id_deposito_destino = models.ForeignKey(Depositos, models.DO_NOTHING, db_column='id_deposito_destino', blank=True, null=True)
    id_usuario_proceso = models.IntegerField(blank=True, null=True)

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
    id_usuario = models.OneToOneField(AuthUser, models.DO_NOTHING, db_column='id_usuario', primary_key=True)
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
    fecha = models.DateField(blank=True, null=True)
    id_tipo_estado = models.ForeignKey(TiposEstado, models.DO_NOTHING, db_column='id_tipo_estado', blank=True, null=True)
    observaciones = models.CharField(max_length=50, blank=True, null=True)
    id_deposito_origen = models.ForeignKey(Depositos, models.DO_NOTHING, db_column='id_deposito_origen', blank=True, null=True)
    id_deposito_destino = models.ForeignKey(Depositos, models.DO_NOTHING, db_column='id_deposito_destino', blank=True, null=True)
    id_usuario_genero = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='id_usuario_genero', blank=True, null=True)
    id_usuario_proceso = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='id_usuario_proceso', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'traspasos'


class UnidadesMedida(models.Model):
    descripcion = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'unidades_medida'


class Usuarios(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    id_tipo_rol = models.ForeignKey(TiposRol, models.DO_NOTHING, db_column='id_tipo_rol', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuarios'
