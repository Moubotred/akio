


**********[OBJETIVO CONVERTIR IMAGEN DE BYTES-> [HEXADECIMAL] SUBIDA AL PROXY A UNA JPG]************

	* ver el hexadecimal de de los log de la intercepcion de proxy
	  que se uso con el app de SAD 

	  se indetifico que es un jpg por los bytes identificados
	  [ffd8ffe000104a46494600010100000100010000]-> [FF,D8,FF,E0]-> JPG
	  normalmete primeros bytes de un archivo los hexadecimales van de 
      2 a 16 bytes los cuales se dicen numeros magicos estos bytes con 
      los que permiten reconocer el formato del archivo 

	  donde se convierte a binario bruto que se envia por un POST

	  TareaAsynckTask.java -> Proxy.java  ============->  RestClientStream.java 
      |_ doInBackground 	   |_AgregarImagen            |_EjecutarMetodoPOSTStream
	                           |_AgregarImagenRequisito   
      

	  se ejecuta una funcion en segundo plano luego llama a agregar imagen y finalmente 
	  se invoca a ejecutar metodo post stream para subir la fotos en segundo plano que 
	  se envia con metadatos y el binario en bruto enviado como cuerpo de un body

	  estons son los metadados:

	  		(doInBackground)

					fotoDto.codigoAtencion = foto.codigoAtencion;
					fotoDto.nombreArchivo = foto.nombre;
					fotoDto.nroEmpresa = "7";
					fotoDto.descripcion = foto.descripcion;
					fotoDto.latitud = foto.latitud;
					fotoDto.longitud = foto.longitud;
					fotoDto.subTipo = foto.tipo;
					fotoDto.idAtencionCapataz = foto.idAtencionCapataz;
					fotoDto.tipoArchivo = foto.tipoArchivo;
					fotoDto.idSubtipoDocumento = foto.subTipoDocumento;
					fotoDto.idDocLocal = foto.idLogico;

	 ahora segun el proxy ejecutandose recibe un hexadecimal o binario bruto
	 para identificar el tipo de formato se uso file name.bin y de la el nombre
	 del formato para una conversion se puede usar mv name.bin imagen.jpg

     
	ahora para realizar una modificacion de poder agregar o eliminar un imagen tanto remoata 
	como local se necesita saber idDocLocal ya que usa un base de datos para almacenarlo 
	el idDocLocal se genera automaticamente pero necesitamos saberlo para poder hacer la
	modificacion de agregar un boton y eliminar tanto remoto como local 

	analisando los xml se ubica lsd_file_foto.xml el cual contiene
		* Tipo: 
		* Descripion :
		* Estado:

	que coniciden con la UI de la app 

	segun este esquema es un concepto de como eliminar la imagen: 

		[Bitmap/Imagen] 
			│
			▼
		[Convertir a bytes con Bitmap.compress -> byte[]]
			│
			▼
		[Crear metadatos: codigoAtencion, nombreArchivo, etc.]
			│
			▼
		[Insertar en DB: DAO.InsertarFoto -> idLogico]
			│
			▼
		[Enviar POST al servidor: Header=metadatos, Body=bytes]
			│
			▼
		[Eliminación]
		├─ Local: DAO.EliminarFoto / deleteAll
		└─ Remoto: Request al servidor con idDocLocal o nombreArchivo


	referecncia de chatgpt :
			https://chatgpt.com/c/68eba4e9-8648-8327-b5a2-183f8760a86e
			