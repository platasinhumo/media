# Plata Sin Humo · Manual de operación (nube)

Versión 2 · 27-nov-2026. Este archivo manda sobre cualquier instrucción anterior. Cambio frente a la versión 1: todo vive en un solo repo público, `platasinhumo/media`, que la tarea programada trae conectado y clonado desde el inicio. Ya no se usa `add_repo` ni el repo privado `platasinhumo/operacion` (quedó archivado).

## Objetivo y forma de trabajo
Plata Sin Humo es un medio independiente de finanzas personales en español (LatAm + hispanos de EE. UU.). Muestra cuánto le cobran de más a la gente y cómo dejar de pagarlo, con números reales y sin gurús. Meta: crecer y monetizar con **cero tiempo operativo del dueño**. Claude produce, publica, mide y ajusta, **100 % en la nube**.

Independencia (regla dura): este medio no se relaciona, ni se menciona, ni se cruza con ningún otro negocio. Solo se usan el conector **Buffer** (cuenta platasinhumo@gmail.com) y este repo. Ningún otro conector.

Repo público: no escribas aquí nombres de personas, correos personales, datos de cuentas ni nada privado.

## Arquitectura (27-nov-2026)
| Pieza | Qué hace | Notas |
|---|---|---|
| `platasinhumo/media` (público) | Manual (`ops/`), kit (`kit/`), specs (`produccion/`) y los mp4 (`v/`) | La tarea lo clona al empezar; los cambios se suben con `git push` a `main` |
| Buffer (plan gratis) | Publica en TikTok, Instagram (Reel) y YouTube (Short) | 3 canales, **máx. 10 publicaciones programadas por canal a la vez** |

URL de los videos: `https://raw.githubusercontent.com/platasinhumo/media/main/v/AAAA-MM-DD.mp4`. Buffer no recibe archivos, solo URL públicas y estables hasta que publica.

IDs Buffer: organización `6af78cd6602aba223cbe5c05` · TikTok `6af78de962b70b94b02279db` · Instagram `6af7945962b70b94b022af74` · YouTube `6af7941962b70b94b022adba`. Facebook: fuera de Buffer (no hay cupo); ver DECISIONES.md.

## Sesión (martes y viernes)
1. **Repo**: el repo ya está clonado en tu directorio de trabajo (si no lo ves, búscalo con `git rev-parse --show-toplevel` o `ls`). Configura `git config user.name "Plata Sin Humo"` y `git config user.email platasinhumo@gmail.com`. No uses `add_repo`. Si no encuentras el repo, avisa en 2 líneas y termina.
2. **Leer**: este manual, `ops/ESTADO.md`, `ops/EXPERIMENTOS.md`, `ops/TEMAS.md` y la última sección de `ops/METRICAS.md`.
3. **Verificar lo publicado**: `list_posts` (organización arriba) con `dueAt` desde la sesión anterior hasta ahora. Todo debe estar `sent`. Si hay `error`, lee el mensaje, corrige (URL caída → vuelve a subir el mp4; texto largo → acórtalo) y reprograma para hoy 7:00 p. m. sin duplicar. Anótalo en ESTADO.md.
4. **Medir (solo martes)**: `list_posts` con `status ["sent"]` e `includeMetrics: true` de los últimos 14 días; procesa con Python (no a mano). Solo cuentan posts con 72 h o más. Agrega a `ops/METRICAS.md` una sección con: vistas por canal (media, mediana, máx.), top 5 de TikTok con tema y gancho, guardados, compartidos y seguidores nuevos, y el resultado del experimento en curso. Decide el experimento siguiente según EXPERIMENTOS.md.
5. **Horizonte**: programa todos los días que falten desde mañana hasta **7 días después de hoy**, sin pasar de 10 publicaciones programadas por canal (cuenta las que ya hay con `list_posts status ["scheduled"]`). Es idempotente: si una fecha ya tiene post en un canal, no la vuelvas a programar en ese canal.
6. **Producir** cada día que falte (ver “Producción”).
7. **Subir los mp4** (ver “Alojamiento”) y comprobar con `curl -sI` que cada URL responde 200 antes de programar.
8. **Programar** en los 3 canales (ver “Publicación”).
9. **Cerrar**: actualiza ESTADO.md (horizonte, portada siguiente, registro de la sesión), TEMAS.md y, si cambió algo, EXPERIMENTOS.md. Commit y `git push origin main`. Termina con un mensaje de máximo 4 líneas: hasta qué día quedó programado, errores y cómo se resolvieron, y los martes la cifra clave de la semana y la decisión que tomaste.

Nunca escribas contraseñas, crees cuentas ni resuelvas captchas. No borres publicaciones ya publicadas. Puedes editar o borrar publicaciones **programadas por ti** si están mal (no se publicaron, es reversible).

## Producción
- Un video por día (TikTok, Reel y Short usan el mismo mp4). Proceso: spec JSON del día → `python3 kit/psh_render.py kit/Archivo.ttf OUT spec.json` → `python3 kit/make_video_v3.py OUT DIA OUT/AAAA-MM-DD.mp4 kit/Archivo.ttf "GANCHO" SEED`. La fuente está en el repo (`kit/Archivo.ttf`). Formato de spec: `kit/ejemplo_spec.json`. Trabaja en una carpeta fuera del repo (por ejemplo /tmp/psh) y copia al repo solo lo que se guarda.
- Estructura fija de 8 slides: portada, frase, 3–5 datos, comparación, cifra grande, pasos, supuestos, llamado a compartir. Identidad: naranja #FF5B1F, negro #121212, hueso #F2EEE6; Archivo 600–900.
- **Toda cifra se calcula con código** (guarda el script de cálculo junto al spec) y se explica en la slide de supuestos. Moneda genérica “$”. Nada inventado. Aviso: “Contenido educativo, no es asesoría financiera personalizada.”
- Portadas rotan orange → ink → bone → split; nunca dos días seguidos del mismo color (la siguiente está en ESTADO.md).
- Revisa con la vista: la hoja de contacto (`sheet-DD.jpg`) y un fotograma de cada slide del video. Si un texto se corta, se sale o se monta sobre una cifra, corrige y vuelve a renderizar.
- **Legibilidad (regla dura, 27-nov):** cada slide debe poder leerse con calma. Tiempos en `kit/make_video_v3.py` (DUR, 31,7 s en total); no los acortes. Máximo ~18 palabras por slide (sin contar la de supuestos); si un texto no cabe, divide la idea o recórtala, nunca aceleres el video. Antes de programar, revisa: palabras de la slide ÷ segundos en pantalla ≤ 4.
- Gancho (`hook`): máximo ~30 caracteres, visible desde el frame 0. Reglas de gancho y temas en EXPERIMENTOS.md.
- Guarda en `produccion/AAAA-MM-DD/`: spec.json, calculo.py, copys.md. No guardes PNG en el repo.

## Alojamiento (carpeta v/)
- Ruta: `v/AAAA-MM-DD.mp4` (fecha de publicación). Videos de ~2,5 MB (CRF 26).
- Para que el repo no crezca de más, en cada sesión borra con `git rm` los mp4 de `v/` cuya fecha sea anterior a hoy − 3 días (ya los copió cada red). Commit normal: **no** reescribas la historia ni uses `push -f`. Nunca borres un video de una fecha que todavía no se publicó.
- Haz `git push origin main`. Si el push a `main` es rechazado, sube la rama `claude/videos-AAAA-MM-DD`, **no programes nada** (las URL no existirían en main) y avisa en el mensaje final con el error exacto.
- Espera ~1 minuto después del push y verifica cada URL con `curl -sI` (200 y tamaño > 1 MB).

## Publicación (Buffer, `create_post`)
Comunes: `mode customScheduled`, `dueAt "AAAA-MM-DDT12:00:00-05:00"`, `schedulingType automatic`, `assets [{video:{url}}]`.
- TikTok: `metadata.tiktok {title (≤90 car.), isAiGenerated:false}`. Texto: gancho + 1 frase + pregunta para comentar + aviso educativo + 4–5 hashtags.
- Instagram: `metadata.instagram {type:"reel", shouldShareToFeed:true, isAiGenerated:false}`, `assets[0].video.metadata.thumbnailOffset 1000`. Texto: 2–4 frases + llamado a compartir con alguien concreto + pregunta + aviso + 5 hashtags.
- YouTube: `metadata.youtube {type:"short", title (≤90), categoryId:"27", privacy:"public", madeForKids:false}`. Texto: resumen con cifras + supuestos + aviso + hashtags.
- Los gráficos hechos con código no se marcan como IA.
- Después de crear, confirma que cada post quedó `scheduled` y que Buffer leyó la duración del video (assets[0].video.durationMs ≈ 31700).

## Hashtags base
#finanzaspersonales #educacionfinanciera #platasinhumo + 2 del tema (#tarjetadecredito, #deudas, #credito, #ahorro, #bancos, #prestamos, #inversion…).
