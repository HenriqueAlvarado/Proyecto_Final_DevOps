# Proyecto_Final_DevOps


<h1 align="center">¡Bienvenidos, somos SellPhones</h1>
<p align="center">
<a href="" target="_blank">
  <img align="center" src="github/Sellphone.png" alt="Logo del proyecto" height="100" width="100">
</a>
</p>
<h3 align="center">SellPhones: Conecta con lo mejor</h3>
<h2 align="center"><u>¿Por qué elegir SellPhones?</u></h2>
<p align="center">

 - 📱 Amplia variedad de modelos: Desde los últimos lanzamientos hasta opciones económicas, encuentra el celular perfecto para ti.
 
 - 💰 Precios competitivos: Ofertas irresistibles y descuentos especiales todo el año.

 - ⚡ Compra rápida y segura: Plataforma intuitiva, métodos de pago confiables y protección al comprador.

 - 🚚 Envío rápido a todo el país: Recibe tu celular en la puerta de tu casa en tiempo récord.
 
 - 🛠️ Garantía en todos los equipos: Tranquilidad asegurada con cobertura ante cualquier inconveniente.

 - 👨‍💻 Atención al cliente personalizada: Nuestro equipo está listo para ayudarte antes, durante y después de tu compra.

</p>

<h2 align="center"><u>Roles del Equipo</u></h2>

| Name                  | Description                                                |
| ---------------------------------|--------------------------------------------------------------- |
| _[Henrique Alvarado: Dev Infraestructura](https://github.com/HenriqueAlvarado)_            | Encargado de desarrollar el código en Python que soporta la lógica del backend y de construir la interfaz del frontend para la aplicación web. Además, colabora en la integración del sistema dentro de la infraestructura definida.            |
| _[Jorge Marroquín: Dev QA](https://github.com/Eliuddd)_                          | Responsable de establecer la conexión entre la base de datos DynamoDB y el backend, asegurando que los datos se transmitan y gestionen correctamente. También realiza pruebas funcionales para validar el flujo de la información.     |
| _[Eros Palma: Ingeniero en software](https://github.com/erospalma)_                  | Encargado de diseñar y desplegar toda la infraestructura del proyecto utilizando Terraform, asegurando que los recursos de AWS como instancias EC2, VPC, subredes y seguridad estén correctamente configurados y automatizados. 

<h4 align="center">Diagrama de Lucid</h4>

<h2 align="center"><u>Infraestructura de nuestro proyecto</u></h2>
<p align="center">
  <img src="github/infraestructura (3).png" alt="Infraestructura del proyecto" width="600">
</p>

<h3 align="center">Framework - Flask</h3>
<p>
  Flask es un microframework de Python que usamos en nuestro proyecto de AWS para crear y manejar aplicaciones web o APIs. Lo utilizamos porque es ligero, fácil de usar y permite exponer funcionalidades de nuestra aplicación a través de endpoints HTTP. Esto es útil para recibir y responder peticiones del frontend o de otros servicios. Además, Flask se integra bien con servicios de AWS como S3, DynamoDB, Lambda o API Gateway, permitiendo que nuestra aplicación procese datos, los almacene o se comunique con otros componentes de la arquitectura en la nube.
</p>

<hr>

<h3 align="center">🌐 Motor de base de datos - DynamoDB (10.10.0.0/24)</h3>
<ul>
  En nuestro proyecto de AWS utilizamos DynamoDB como base de datos NoSQL porque es rápida, escalable y totalmente gestionada por AWS. La usamos para almacenar y consultar datos estructurados sin necesidad de administrar servidores ni preocuparse por el rendimiento o el escalado. DynamoDB es ideal para aplicaciones que requieren alta disponibilidad y tiempos de respuesta muy bajos. Además, se integra fácilmente con otros servicios de AWS, lo que facilita su uso en arquitecturas modernas.
</ul>

<hr>

<h3 align="center">🔒 Forma de integración</h3>
<ul>
  En nuestro proyecto, integramos DynamoDB como base de datos utilizando el framework Flask en Python. La integración se realizó a través del SDK oficial de AWS para Python llamado Boto3. Desde nuestra aplicación Flask, configuramos el acceso a AWS mediante credenciales (ya sea por variables de entorno, archivos de configuración o roles de IAM si está desplegado en AWS). Con Boto3, creamos una conexión al servicio DynamoDB y definimos las operaciones necesarias como insertar, leer, actualizar y eliminar elementos de las tablas. Estas operaciones se conectan a los endpoints de nuestra API en Flask, permitiendo que las peticiones web interactúen directamente con la base de datos. Gracias a esto, logramos una comunicación eficiente entre el frontend, el backend con Flask, y la base de datos en DynamoDB sin necesidad de servidores intermedios ni configuración compleja
</ul>

<hr>

<h3 align="center">🗃️ Número de instancias</h3>
<ul>
  En nuestro proyecto utilizamos dos instancias EC2 en una subred pública: una Linux Jump Server y una Linux Web Server. La Jump Server funciona como punto de acceso principal mediante SSH (puerto 22), permitiendo el acceso administrativo al entorno. Desde ella, también se puede acceder a la Web Server, aunque esta última también está en la red pública y, por tanto, puede recibir conexiones externas si así se configura.

La Web Server aloja nuestra aplicación Flask y expone los puertos 80 (HTTP) y 443 (HTTPS) para permitir el acceso web a la aplicación desde internet. El uso de estos puertos asegura que los usuarios puedan acceder a la aplicación tanto en modo no cifrado (HTTP) como cifrado (HTTPS). El puerto 22 (SSH) también está habilitado en ambas instancias para tareas de administración y mantenimiento, aunque por buenas prácticas, el acceso SSH normalmente se restringe solo a la Jump Server.

</ul>


<hr>

<h3 align="center">💽 Dominio</h3>
<ul>
  En nuestro proyecto no utilizamos un dominio personalizado; en su lugar, accedemos a la aplicación mediante la IP pública de la instancia Web Server. Esta dirección IP se asigna automáticamente cada vez que se inicia la instancia, por lo que puede cambiar con cada reinicio. Debido a esto, cada vez que iniciamos el laboratorio, debemos copiar la nueva IP pública y usarla para acceder a la aplicación desde el navegador, normalmente a través del puerto 80 (HTTP). Esta configuración es adecuada para entornos de práctica o pruebas, aunque para un entorno de producción sería recomendable usar un nombre de dominio fijo o una IP elástica (Elastic IP) para mayor estabilidad.

</ul>

<hr>

<h3 align="center">Cómo desplegar la infraestructura y cómo desplegar la aplicación</h3>
<p>
  En esta fase de nuestro proyecto, hemos redactado una explicación detallada en nuestro archivo de Word, en el cual describimos minuciosamente los pasos seguidos para abordar esta parte del proyecto. A lo largo de este documento, hemos plasmado el proceso completo, desde la planificación hasta la ejecución, con el objetivo de ofrecer una comprensión clara y completa de las decisiones tomadas, las herramientas utilizadas y los resultados obtenidos hasta el momento. Además, se incluyen detalles técnicos y específicos sobre las configuraciones y procedimientos implementados, para que cualquier lector pueda entender a fondo cómo llegamos a este punto del proyecto.
Adicionalmente, se elaboró un video explicativo que acompaña el documento, con el fin de reforzar visualmente el desarrollo del proyecto y facilitar la comprensión del trabajo realizado.
</p>

<hr>
