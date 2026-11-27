# Decisiones · Plata Sin Humo

## 27-nov-2026 · Un solo repo público, conectado a la tarea
Problema: la primera sesión en la nube (27-nov) no produjo nada. La tarea programada no traía repos conectados y debía agregarlos con `add_repo` en plena ejecución; eso no está permitido en una ejecución programada. El repo público de videos se pudo clonar; el privado de operación no.

Verificado el 27-nov:
- Una tarea programada de Claude Code admite **un** repositorio conectado, que se clona al empezar cada ejecución, y puede hacer push a la rama que diga el prompt.
- En la pantalla de creación aparecen disponibles `platasinhumo/operacion` y `platasinhumo/media`.

Elegido (lo decidió el dueño): mover manual, kit, estado y specs al repo público `platasinhumo/media`, sin nombres ni datos personales, y conectar solo ese repo a una tarea nueva de Claude Code (martes y viernes 1:40 p. m.). La tarea vieja quedó desactivada; el repo privado `operacion` queda como archivo.

Descartadas:
- Mantener la operación privada: los videos necesitan una URL pública que Buffer pueda descargar y, desde la nube, el único alojamiento al que se llega es GitHub.
- Hacer las sesiones a mano en un chat: funciona, pero depende del dueño cada semana.

Supuesto, no verificado aún: que el push a `main` desde la tarea programada funcione sin bloqueo. Si falla, el manual indica subir una rama y avisar.

## 27-nov-2026 · Videos de 31,7 s
Los videos de 17 s (8 slides de 1,6 a 2,6 s) no se alcanzaban a leer. Se pasó a 3,2–4,5 s por slide (31,7 s en total) con máximo ~18 palabras por slide. Se rehicieron los del 28 al 30-nov.

## 24-nov-2026 · Operación 100 % en la nube con GitHub + Buffer
Problema: las sesiones dependían de un computador y un navegador (Metricool, TikTok Studio, Business Suite y luego subir videos a Drive). Tres sesiones seguidas fallaron por eso (6, 10 y 13-nov).

Elegido entonces: kit y estado en un repo privado, videos en `platasinhumo/media` (público) y publicación con el conector Buffer (reemplazado el 27-nov por un solo repo, ver arriba).

Verificado el 24-nov:
- La API de Buffer no recibe archivos: necesita una URL pública y estable hasta que se publique. La ayuda de Buffer dice que Drive no sirve (funcionó del 13 al 24-nov, pero fuera de lo soportado).
- Buffer aceptó un mp4 servido desde raw.githubusercontent.com (leyó duración y códec).
- Desde la nube hay salida a GitHub; Cloudinary, Facebook Graph y otros alojamientos están bloqueados.
- Plan gratis de Buffer: 3 canales y 10 publicaciones programadas por canal a la vez, sin límite mensual.

Descartadas:
- Drive: el único conector de Drive disponible no es de este proyecto (prohibido usarlo) y Buffer no lo soporta oficialmente.
- Cloudinary (gratis, recomendado por Buffer): desde la nube no se puede llegar a su API y exige guardar una clave secreta.
- Metricool: 20 publicaciones/mes en el plan gratis y requería navegador.
- Plan pago de Buffer (desde US$5–6 por canal al mes): no hace falta hoy; el límite de 10 alcanza con sesiones martes/viernes.
- API oficial de TikTok directa: las apps sin auditoría solo publican en privado.

Supuesto, no verificado aún: que Buffer descargue el video de GitHub en el momento de publicar igual que lo leyó al crear el post. Se confirma con las publicaciones del 28-nov en adelante.

## 24-nov-2026 · Facebook
Fuera por ahora. Buffer no tiene cupo (3 canales) e Instagram, que usa la misma distribución de Meta, saca 8 vistas por Reel vía API. Agregarlo costaría un paso manual del dueño para un canal que hoy no distribuye. Se revisa en el punto de decisión del 5-ene-2027.

## 24-nov-2026 · Contenido
Los datos de un mes (METRICAS.md) muestran que el problema no es publicar sino que nadie comparte ni guarda. Se pasa a experimentos semanales de una variable (EXPERIMENTOS.md) con punto de decisión el 5-ene-2027.
