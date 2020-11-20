# CloudVet RD edición de la comunidad
Versión para la comunidad de mi producto CloudVetRD, que es una plataforma web para gestión de historias clínicas veterinarias.

## Demos y más información
en el sitio de Respuesta Digital pueden conocer más sobre el producto y hay enlaces a videos de demostración

- [Sitio del producto](https://www.respuestadigital.com.ar/#seccion_cloudvet)
- [LinkedIn del autor](https://www.linkedin.com/in/maralefer/)

## Características generales del producto
El producto es una aplicación web para gestión de historias clínicas veterinarias.
Primero se deben cargar las razas a utilizar.
Luego ya se pueden cargar los propietarios y sus mascotas.
Finalmente se cargan las consultas asociadas a las mascotas.

Hay disponible un formulario de autogestión que, al completarlo:
- Crea una clínica
- Crea un usuario
- Asigna el usuario a la clínica
- Envía un mail de bienvenida al usuario

## Características técnicas
Las tecnologías utilizadas para la construcción son:
- Framework Django
- Base de datos Postgres
- Estilo visual Boostrap

### Módulos utilizados tanto de Django como de terceros
- Uso de paquetes de Django para la autogestión de cuentas y recuperación de contraseña
- Uso de Django Admin para la carga de tablas "internas" como ser Motivos de Consulta
- Crispy forms para el estilo visual
- ReCaptcha para validar "no soy un robot"

### Aclaraciones sobre funcionalidades obsoletas o por la mitad
- Hay temas que están por la mitad en cuanto a grafos (Graphene), finalmente no se está utilizando. Buscar las referencias a "schema"
- Puede que haya información más bien referida a pacientes humanos, esto debido a que el proyecto originalmente era una historia clínica humana.
- Se encuentra parcialmente desarrollado un esquema de licencias FREE, ..., PREMIUM
- Puede haber pruebas unitarias que no hacen a la funcionalidad del sistema.



