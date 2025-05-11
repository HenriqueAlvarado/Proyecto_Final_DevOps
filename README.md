# Proyecto_Final_DevOps


<h1 align="center">¡Bienvenidos, somos SellPhones</h1>
<p align="center">
<a href="" target=""><img align="center" src="" alt="" height="100" width="100"></a>
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
| _[Henrique Alvarado: Dev Infraestructura](https://github.com/HenriqueAlvarado)_            | Encargado de diseñar y desplegar toda la infraestructura del proyecto mediante Terraform, asegurando entornos eficientes, escalables y seguros para su funcionamiento.            |
| _[Jorge Marroquín: Dev QA](https://github.com/Eliuddd)_                          | Responsable de integrar correctamente la base de datos con el backend, garantizando la calidad del sistema mediante pruebas y validaciones que aseguren su correcto desempeño.     |
| _[Eros Palma: Ingeniero en software](https://github.com/erospalma)_                  | Apoya en el desarrollo de scripts en Python y en la construcción del frontend, contribuyendo a crear una experiencia de usuario funcional, fluida y visualmente atractiva. 

<h4 align="center">Diagrama de Lucid</h4>

<h2 align="center"><u>Infraestructura de nuestro proyecto</u></h2>
<p align="center">
  <img src="" alt="" width="600">
</p>

<h3 align="center">Descripción de Nuestra Arquitectura en AWS</h3>
<p>
  En este proyecto, diseñamos una arquitectura en AWS que combina seguridad, segmentación de red y acceso controlado a la base de datos. Toda la infraestructura se encuentra dentro de una VPC con el rango de IPs 10.10.0.0/20, desplegada en una sola zona de disponibilidad.
</p>

<hr>

<h3 align="center">🌐 Subred Pública (10.10.0.0/24)</h3>
<ul>
  <li>Desplegamos una instancia EC2 configurada como Linux Jump Server.</li>
  <li>Este servidor actúa como punto de entrada a la infraestructura.</li>
  <li>Un Security Group permite conexiones SSH (puerto 22) desde el exterior para administración segura.</li>
</ul>

<hr>

<h3 align="center">🔒 Subred Privada</h3>
<ul>
  <li>Contiene un Linux Web Server inaccesible directamente desde Internet.</li>
  <li>Solo se puede acceder a él vía SSH a través del Jump Server.</li>
  <li>Este servidor realiza operaciones sobre la base de datos y es el único autorizado para comunicarse con Amazon DynamoDB.</li>
</ul>

<hr>

<h3 align="center">🗃️ Acceso a DynamoDB</h3>
<ul>
  <li>DynamoDB está fuera de la VPC como servicio gestionado por AWS.</li>
  <li>El servidor web se conecta mediante un IAM Role, evitando el uso de claves estáticas.</li>
  <li>Esto garantiza una conexión segura y escalable.</li>
</ul>

<hr>

<h3 align="center">Cómo desplegar la infraestructura y cómo desplegar la aplicación</h3>
<p>
  En esta fase de nuestro proyecto, hemos redactado una explicación detallada en nuestro archivo de Word, en el cual describimos minuciosamente los pasos seguidos para abordar esta parte del avance. A lo largo de este documento, hemos plasmado el proceso completo, desde la planificación hasta la ejecución, con el objetivo de ofrecer una comprensión clara y completa de las decisiones tomadas, las herramientas utilizadas y los resultados obtenidos hasta el momento. Además, se incluyen detalles técnicos y específicos sobre las configuraciones y procedimientos implementados, para que cualquier lector pueda entender a fondo cómo llegamos a este punto del proyecto.
</p>

<hr>

<h3 align="center">Cómo correr la aplicación localmente (para pruebas) y cómo acceder a la versión desplegada</h3>
<p>
