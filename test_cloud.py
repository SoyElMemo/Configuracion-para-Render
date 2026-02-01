import cloudinary
import cloudinary.uploader

cloudinary.config( 
  cloud_name = "dvsablxw4", 
  api_key = "452297646662275", 
  api_secret = "TomzOQ-2Rc-xj5g-cTLhGwfj1Bc" 
)

try:
    # Intenta subir una imagen de prueba de internet
    res = cloudinary.uploader.upload("https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png")
    print("✅ ¡Conexión exitosa! Imagen subida en:", res['url'])
except Exception as e:
    print("❌ Error de conexión:", e)