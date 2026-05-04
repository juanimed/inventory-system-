"""

Trabajo integrador: Grupo 7
Tema: Gestión de inventario
Integrantes: Andres Lescano, Luca Siviero, Juan Ignacio Medori, Lautaro Costa, Sofia ...

"""

#Variables Principales
file = "inventario.txt"
usuario="admin"
contra="123"

# ==================================================================== MENU PRINCIPAL ====================================================================

def menu(ruta):
    while True:
        print("\n" + "=" * 50)
        print("MENÚ PRINCIPAL".center(50))
        print("=" * 50) 
        print("1. Mostrar inventario")
        print("2. Agregar categoría")
        print("3. Agregar producto")
        print("4. Calcular valor total")
        print("5. Mostrar categoria")
        print("6. Modificar datos") 
        print("7. Salir")
        print("=" * 50)
        op = input("Elige opción: ").strip()

        if op == "1":
            mostrar_inventario(ruta)
        elif op == "2":
            agregar_categoria(ruta)
        elif op == "3":
            agregar_producto_categoria(ruta)
        elif op == "4":
            opcion = opciones()
            opcion = int(opcion)
            if opcion == 1:
                calcular_valor_total()
            elif opcion == 2:
                producto = input("Nombre del producto: ").strip()
                producto = producto.title()
                calcular_valor_producto(producto)
            elif opcion == 3:
                mostrar_matriz()
                entrada = input("Categoría (número/abreviación/nombre): ").strip()
            
                nombre_cat = resolver_categoria_desde_entrada(ruta, entrada)
                if nombre_cat is None:
                    print("Categoría no válida.")
                else:
                    calcular_valor_categoria(nombre_cat)
            else:
                continue
        elif op == "5":
            mostrar_productos(ruta)
        elif op == "6":
            modificar_datos()
        elif op == "7":
            print("Saliste del programa.")
            break
        else:
            print("Opción inválida.")
            
# ==================================================================== MOSTRAR INVENTARIO ====================================================================

def mostrar_inventario(ruta):
    while True:
        print("\n" + "-" * 50)
        print("FILTROS DE INVENTARIO".center(50))
        print("-" * 50)
        print("Para buscar en el inventario necesitamos filtrar por palabra y precio")
        print("Deje vacío cualquier campo para no filtrar.")
        print()

        producto = input("Ingrese el nombre del producto que quiere buscar: ").strip()
        producto = producto.title()
        while producto != "" and (not producto.isalpha()):
            producto = input("Ingrese el nombre del producto que quiere buscar, Enter para saltear: ").strip()
            producto = producto.title()
            
        minimo = input("Ingrese el precio minimo en enteros para buscar: ").strip()
        while minimo != "" and (not minimo.isdigit()):
            minimo = input("Ingrese el precio minimo en enteros para buscar, enter para saltear: ").strip()
            
        maximo = input("Ingrese el precio maximo en enteros para buscar: ").strip()
        while maximo != "" and (not maximo.isdigit()):
            maximo = input("Ingrese el precio en enteros maximo para buscar, enter para saltear: ").strip()
        
        if producto == "" and minimo == "" and maximo == "":
            print("\nNo se eligieron filtros. Debe ingresar al menos uno.")
            elec = input("Presione 's' para salir o cualquier tecla para intentar nuevamente: ").strip().lower()
            if elec == "s":
                print()
                return
            else:
                continue
            
        if minimo != "":
            minimo = float(minimo)
        else:
            minimo = 0.0
            
        if maximo != "":
            maximo = float(maximo)
        else:
            maximo = None
        
        if maximo != None:
            while maximo < minimo:
                maximo = input("El maximo en enteros debe ser mayor al minimo: ").strip()
                if maximo == "":
                    maximo = None
                    break
                elif not maximo.isdigit():
                    continue
                else:
                    maximo = float(maximo)
        
        #Seguridad añadida para que los filtros solo sean de 50 puntos de margen
        if maximo != None:          
            if maximo - 50 > minimo:
                print("\nPor cuestiones de seguridad no podemos filtrar el inventario porque elegiste un filtro de máximo que excede el límite, \nrecorda que el numero máximo tiene un rango de entre minimo y +50. \nPor favor volve a intentar")
                return
                    
        print("\n" + "=" * 50)
        print(f"Los filtros a tener en cuenta son: producto: {producto}, mínimo: {minimo}, máximo: {maximo}")
        print("\n" + "=" * 50)
        
        #Se ejecutan los filtros
        inventario = busqueda_por_producto(producto, minimo, maximo, ruta)
        
        # Mostrar el inventario en formato legible
        print("\n" + "=" * 50)
        print("RESULTADOS DE LA BÚSQUEDA".center(50))
        print("=" * 50)
        
        #Si la función no retorna inventario
        if not inventario:
            print("No se encontraron productos que coincidan con los filtros.\n")
        else: #Si la función si retorna inventario entonces lo printea
            for categoria, productos in inventario.items():
                print(f"\nCATEGORÍA: {categoria}")
                print("-" * 50)
                print(f"{'Código':<10}{'Nombre':<20}{'Precio':<10}{'Stock':<10}")
                print("-" * 50)
                for codigo, datos in productos.items():
                    print(f"{codigo:<10}{datos['nombre']:<20}${datos['precio']:<9.2f}{datos['stock']:<10}")
                print("-" * 50)

#Normalizador: lower() + strip() + compresión de espacios
def norm(s):
    return " ".join(str(s).strip().lower().split())


def busqueda_por_producto(producto, minimo, maximo, ruta):
    
    inventario = {}
    q = norm(producto) if (producto is not None and producto != "") else ""
    try:
        f = open(ruta, "rt", encoding="UTF-8")
        linea = f.readline()
        categoria_actual = None

        while linea:
            linea = linea.strip()

            
            if len(linea) >= 10 and linea[:10] == "CATEGORIA:":
                categoria_actual = linea[10:].strip()
                linea = f.readline()
                continue

           
            if categoria_actual and len(linea) > 3 and linea[:10] != "CATEGORIA:":
                ficha = linea.split(";")
                if len(ficha) >= 4:
                    codigo = ficha[0].strip()
                    nombre = ficha[1].strip()
                    try:
                        precio = float(ficha[2])
                    except:
                        #Si el precio no es numérico, descartamos la fila
                        linea = f.readline()
                        continue
                    stock = ficha[3].strip()

                    
                    #Filtra por nombre: si no hay término, pasa; si hay, coincidencia normalizada
                    if q == "":
                        nombre_ok = True
                    else:
                        nombre_ok = (q in norm(nombre))

                    #Filtra por precio: si maximo es None, solo mínimo; si no, rango cerrado
                    if maximo is None:
                        precio_ok = (precio >= minimo)
                    else:
                        precio_ok = (precio >= minimo and precio <= maximo)

                    if nombre_ok and precio_ok:
                        if categoria_actual not in inventario:
                            inventario[categoria_actual] = {}
                        inventario[categoria_actual][codigo] = {
                            "nombre": nombre,
                            "precio": precio,
                            "stock": stock
                        }

            linea = f.readline()

    except Exception as e:
        print(e)
    finally:
        try:
            f.close()
        except Exception:
            pass
        return inventario


# ==================================================================== AGREGAR CATEGORIA ====================================================================

def agregar_categoria(ruta):
    print("\n" + "=" * 50)
    print("AGREGAR NUEVA CATEGORÍA".center(50))
    print("=" * 50)
    
    #Verifica que la categoria sea una palabra y con la primer letra mayúscula
    categoria = input("Ingrese el nombre de la nueva categoría con Enter cancela: ").strip().title()
    while categoria != "" and (not categoria.isalpha()):
        categoria = input("Ingrese nuevamente con palabras, con Enter cancela: ").strip().title()
    if categoria == "":
        return
    
    matriz_categorias = leer_matriz_categorias_numerada()
    validar = True
    for i in range(len(matriz_categorias)): #Recorre toda la matriz de categorias para validar que cuando vos agregas una categoria no sea una ya existente
        if categoria == matriz_categorias[i][1]: #La posición 1 almacena el nombre de cada categoría entonces está recorriendo comparando nombre por nombre
            print("Esa categoria ya existe")
            validar = False
            _ = input("precione Enter para salir: ").strip()
            break
    if validar == True: #Cuando validar es verdadero es porque entonces no se encotnró ninguna repetida 
        try: #Agrega la categoria al final del archivo
            f = open(ruta, "a", encoding="UTF-8")
        except Exception:
            print("Error al abrir el archivo")
            pass
        try:
            f.write(f"\nCATEGORIA:{categoria}\n")
            print(f"\nCategoría '{categoria}' agregada correctamente al inventario.\n")
        except Exception as e:
            print(f"Error al agregar la categoría: {e}")
        finally:
            try:
                f.close()
            except Exception as e:
                print(e)

# ==================================================================== AGREGAR PRODUCTO ====================================================================

def agregar_producto_categoria(ruta):
    validador = False

    matriz_categorias = leer_matriz_categorias_numerada()

    categoria = solicitar_y_resolver_categoria(ruta)
    if categoria == "":
        return
    
    #Seguro anti categoria inexistente
    for i in range(len(matriz_categorias)):
        nombre = matriz_categorias[i][1]
        if categoria == nombre:
            validador = True
    if validador == False:
        print("\nTu categoria no existe")
        return
    
    """
    #Seguro anti categoria inexistente
    contador = 0
    for c in categorias:
        if categoria != c:
            contador += 1
        if contador == len(categorias):
            print("Tu categoria no existe")
            return
    
    """
    
    # Buscar la categoría en el archivo y leer sus productos
    try:
        f = open(ruta, "rt", encoding="utf-8")
        productos = []
        linea = f.readline()
        en_categoria = False
        ultimo_id = 0

        while linea:
            if len(linea) >= 3 and linea[:10] == "CATEGORIA:":
                if linea[10:].strip() == categoria:
                    en_categoria = True
                    linea = f.readline()
                    continue
                elif en_categoria:
                    break

            if en_categoria and len(linea.strip()) > 3:
                ficha = linea.strip().split(";")
                if len(ficha) >= 4:
                    productos.append(ficha[1].strip())
                    try:
                        ultimo_id = int(ficha[0])
                    except:
                        pass

            linea = f.readline()
        try:
            f.close()
        except Exception:
            pass

        # Mostrar productos actuales de la categoría
        print(f"\nProductos actuales en la categoría '{categoria}':")
        if productos:
            for p in productos:
                print("-", p)
        else:
            print("No hay productos aún en esta categoría.")

        # Crear nuevo producto
        while True:
            nombre = input("\nIngrese el nombre del nuevo producto (Enter para cancelar): ").strip().title()
            if nombre == "":
                return
            if nombre in productos:
                print("Ese nombre ya existe en la categoría. Intente con otro.")
                continue
            break

        # Validar precio
        while True:
            puntos = 0
            continuar = False
            precio = input("Ingrese el precio del producto: ").strip()
            if precio == "":
                return
            for c in precio:
                if c != "." and (not c.isdigit()):
                    print("formato de precio inválido\n")
                    continuar = True
                    break
                if c == ".":
                    puntos += 1
            if continuar:
                continue
            if puntos > 1:
                print("Formato de precio inválido\n")
                continue
            else:
                print(f"Precio asignado {precio}")
                break
            """
            if precio.count(".") > 1 or not all(c.isdigit() or c == "." for c in precio):
                print("Precio inválido. Debe ser un número con solo un punto decimal.")
                continue
            break
            """

        # Validar stock
        while True:
            stock = input("Ingrese el stock del producto (entero): ").strip()
            if stock == "":
                return
            if not stock.isdigit():
                print("El stock debe ser un número entero.")
                continue
            break

        # Generar nuevo ID
        nuevo_id = ultimo_id + 1 #Este vendria a ser el id de la nueva ficha de producto
        nueva_linea = f"{nuevo_id};{nombre};{precio};{stock}\n" #Esto es el formato string de la ficha de producto

        # Guardar en archivo temporal, esto lo hacemos porque para actualizar las categorias tenemos que duplicar el archivo y copiar linea por linea el nuevo archivo al archivo original
        temp_ruta = "inventario_temp.txt"
        try:
            f_original = open(ruta, "rt", encoding="utf-8")
            f_temp = open(temp_ruta, "wt", encoding="utf-8")
            dentro = False
            agregado = False

            for linea in f_original:
                linea_strip = linea.strip() #Recorremos todo el archivo
                if len(linea_strip) >= 3 and linea_strip[:10] == "CATEGORIA:": #Si la linea es una categoria obtenemos el nombre de la categoría
                    nombre_categoria = linea_strip[10:].strip()
                    if nombre_categoria == categoria: #Posicionamos el lector en la categoria adecuada
                        dentro = True
                    elif dentro: #Se ejecuta cuando detecta que la siguiente linea es una categoria
                        if not agregado:
                            f_temp.write(nueva_linea+"\n")
                            agregado = True
                        dentro = False
                f_temp.write(linea)

            if dentro and not agregado: #Esto es cuando la categoria es la última entonces al no haber nada, agrega el producto
                f_temp.write(nueva_linea)
                agregado = True

        except Exception as e:
            print("Error al procesar el archivo:", e)
            return
        finally:
            try:
                f_original.close()
            except Exception:
                pass
            try:
                f_temp.close()
            except Exception:
                pass

        try:
            f_temp = open(temp_ruta, "rt", encoding="utf-8")
            f_original = open(ruta, "wt", encoding="utf-8")
        except Exception:
            pass
        try: #Hacemos la copia del temporal al original para tener actualizados los cambios
            for linea in f_temp:
                f_original.write(linea)
            print(f"\nProducto '{nombre}' agregado correctamente a la categoría '{categoria}'.")
        except Exception as e:
            print("Error al guardar el archivo:", e)

    except Exception as e:
        print("Error:", e)
    finally:
        try:
            f.close()
        except Exception:
            pass
        try:
            f_temp.close()
        except Exception:
            pass
        try:
            f_original.close()
        except Exception:
            pass


# ==================================================================== CALCULAR VALOR TOTAL ====================================================================

#VERIFICAR FUNCIONAMIENTOOOOOOOOOO

def opciones():
    print("\n" + "=" * 50)
    print("Calcular valor total".center(50))
    print("=" * 50) 
    print("1. Todas las categorias y el inventario total")
    print("2. Producto en particular")
    print("3. Categoria particular y sus productos")
    print("Cualquiera. salir")
    op = input("Elige opción: ").strip()
    while not op.isdigit():
        op = input("Elige devuelta una de las opciones: ").strip()
    op = int(op)
    return op

def calcular_valor_producto(nombre_producto):
    ruta = "inventario.txt"
    try:
        f=open(ruta, "rt", encoding="utf-8")
        return _buscar_producto_archivo(f, nombre_producto)
    except FileNotFoundError:
        print("Error: No se encontró el archivo.")
        return None


def _buscar_producto_archivo(f, objetivo):
    linea = f.readline()
    if not linea:  # fin del archivo
        print(f"\nNo se encontró el producto '{objetivo}'.\n")
        return None

    linea = linea.strip()
    if not linea or linea[:10]==("CATEGORIA:"):
        return _buscar_producto_archivo(f, objetivo)

    partes = linea.split(";")
    if len(partes) >= 4:
        nombre = partes[1].strip()
        if nombre.lower() == objetivo.lower():
            try:
                precio = float(partes[2])
                stock = float(partes[3])
                valor_total = precio * stock
                print("\nProducto:", nombre)
                print("Precio: $", precio)
                print("Stock:", stock)
                print("Valor total: $", f"{valor_total:.2f}\n")
                return valor_total
            except ValueError:
                pass

    return _buscar_producto_archivo(f, objetivo)


def calcular_valor_categoria(nombre_categoria):
    ruta = "inventario.txt"
    try:
        f=open(ruta, "rt", encoding="utf-8")
        productos, total = _acum_cat_archivo(f, nombre_categoria, False, [])
    except FileNotFoundError:
        print("Error: No se encontró el archivo.")
        return None

    if not productos:
        print(f"\nNo se encontró la categoría '{nombre_categoria}'.\n")
        return None

    print("\n" + "=" * 50)
    print(("VALOR TOTAL - CATEGORÍA: " + nombre_categoria.upper()).center(50))
    print("=" * 50)
    print(f"{'Producto':<20}{'Precio':<10}{'Stock':<10}{'Valor Total ($)':>10}")
    print("-" * 50)
    for nombre, precio, stock, valor in productos:
        print(f"{nombre:<20}${precio:<9}{stock:<10}{valor:>10.2f}")
    print("-" * 50)
    print(f"{'TOTAL CATEGORÍA':<40}{total:>10.2f}")
    print("=" * 50 + "\n")

    return total


def _acum_cat_archivo(f, cat_obj, dentro, productos, total=0.0):
    linea = f.readline()
    if not linea:  # fin del archivo
        return (productos, total)

    linea = linea.strip()
    if not linea:
        return _acum_cat_archivo(f, cat_obj, dentro, productos, total)

    if linea[:10]==("CATEGORIA:"):
        nombre = linea[10:].strip()
        nuevo_dentro = (nombre.lower() == cat_obj.lower())
        return _acum_cat_archivo(f, cat_obj, nuevo_dentro, productos, total)

    if dentro and ";" in linea:
        partes = linea.split(";")
        if len(partes) >= 4:
            try:
                nombre = partes[1].strip()
                precio = float(partes[2])
                stock = float(partes[3])
                valor = precio * stock
                productos.append((nombre, precio, stock, valor))
                return _acum_cat_archivo(f, cat_obj, dentro, productos, total + valor)
            except ValueError:
                pass

    return _acum_cat_archivo(f, cat_obj, dentro, productos, total)


def calcular_valor_total():
    ruta = "inventario.txt"
    try:
        f = open(ruta, "rt", encoding = "utf-8")
        resultados = _totales_archivo(f, None, 0.0, []) #f representa el archivo, None representa la categoria actual, 0.0 es el subtotal base y [] es una lista de resultados
    except Exception:
        print("No se encontró el archivo especificado.")
        return

    total_general = sum(sub for _, sub in resultados)

    print("\n" + "=" * 50)
    print("VALOR TOTAL DEL INVENTARIO".center(50))
    print("=" * 50)
    print(f"{'Categoría':<25}{'Valor Total ($)':>20}")
    print("-" * 45)
    for cat, sub in resultados:
        print(f"{cat:<25}{sub:>20.2f}")
    print("-" * 45)
    print(f"{'TOTAL GENERAL':<25}{total_general:>20.2f}")
    print("=" * 50)


def _totales_archivo(f, cat_actual, subtotal, resultados):
    linea = f.readline()
    if not linea:
        if cat_actual is not None:
            resultados.append((cat_actual, subtotal))
        return resultados

    linea = linea.strip()
    if not linea:
        return _totales_archivo(f, cat_actual, subtotal, resultados)

    if linea[:10]==("CATEGORIA:"):
        nombre = linea[10:].strip()
        if cat_actual is not None:
            resultados.append((cat_actual, subtotal))
        return _totales_archivo(f, nombre, 0.0, resultados)

    if ";" in linea:
        partes = linea.split(";")
        if len(partes) >= 4:
            try:
                precio = float(partes[2])
                stock = float(partes[3])
                return _totales_archivo(f, cat_actual, subtotal + (precio * stock), resultados)
            except ValueError:
                pass

    return _totales_archivo(f, cat_actual, subtotal, resultados)


# ==================================================================== MODIFICAR DATOS ====================================================================


def modificar_datos():
    ruta = "inventario.txt"
    print("\n" + "=" * 50)
    print("Que desea modificar")
    print("1. Datos de productos")
    print("2. Datos de categorias")
    print("3. Eliminar producto")
    print("4. Eliminar categoria")
    print("Enter - Volver")
    op = input("introduzca la opcion: ")
    print()
    
    if op == "1":
        modificar_productos(ruta)
    elif op == "2":
        modificar_categorias()
    elif op == "3":
        eliminar_producto()
    elif op == "4":
        eliminar_categorias()
    else:
        return
    
def modificar_productos(ruta):
    while True:
        var = input("Presione Enter para salir, cualquier otro caracter lo dirijira al menu de modificaciones: ")
        if var == "":
            return
        print("\n=== MODIFICAR PRODUCTOS ===")
        # Permitir seleccionar por número/abreviación/nombre
        nombre_cat = solicitar_y_resolver_categoria(ruta)
        if not nombre_cat:
            continue

        try: #Abre el archivo
            f = open(ruta, "rt", encoding="utf-8")
            # Buscar categoría
            linea = f.readline()
            en_categoria = False
            productos = []

            while linea: #Mientras se recorre el archivo
                if len(linea) >= 10 and linea[:10] == "CATEGORIA:": #Si encuentra una categoria
                    nombre_cat_linea = linea[10:].strip()
                    if nombre_cat_linea == nombre_cat: #Si la categoria matchea con la que queriamos entonces termina con el ciclo para empezar a cargar la categoria en memoria
                        en_categoria = True
                        linea = f.readline()
                        continue
                    elif en_categoria:
                        # si ya terminó la categoría
                        break #Rompe el ciclo para cargar la categoria a memoria

                if en_categoria and len(linea.strip()) > 3 and ";" in linea: #Detecta que la siguiente linea es una ficha
                    ficha = []
                    campo = ""
                    for ch in linea:
                        if ch == ";": #agrega la cantidad de campos como campos tenga esa ficha de producto
                            ficha.append(campo)
                            campo = ""
                        else: #Copia caracter por caracter todos los campos y luego los mete en la fich, entonces asi constituye la ficha de producto a modificar
                            campo += ch
                    ficha.append(campo)
                    productos.append(ficha)
                linea = f.readline() #Recorre la siguiente linea del while para buscar nuevas lineas
                
        except Exception as e:
            print("Error al abrir el archivo:", e)
            return
        finally:
            try:
                f.close()
            except Exception:
                pass

        if not en_categoria: #Cuando pones una categoria y esta categoria no coincide con las del archivo, entonces sale de la función porque no existe
            print("Categoría no encontrada.")
            continue

        if len(productos) == 0: #Esto es cuando detecta la categoria pero debajo de esa categoria detecta una categoria vacia, entonces ahi sabe que la categoria esta vacía
            print("No hay productos en esta categoría.")
            continue

        print("\nProductos de la categoría", nombre_cat + ":") #nombre_cat es la variable que almacena el nombre de la categoria
        for p in productos: #Basicamete recorre toda la lista de productos en forma de tabla y te la printea
            print(f"ID: {p[0]} | Nombre: {p[1]} | Precio: {p[2]} | Stock: {p[3]}")

        id_modificar = input("\nIngrese el ID del producto a modificar (Enter para cancelar): ").strip() #Si no pones un id te va a detectar que ese producto no existe
        if id_modificar == "": #Valida que tu id no sea Enter, porque con enter cancelarias
            continue

        producto_encontrado = False
        for p in productos: #Recorre toda la lista donde p representa cada ficha de productos
            if p[0] == id_modificar: #Si el id es igual al id que elegimos entonces activa la flag de seguridad producto_encontrado
                producto_encontrado = True #Activa el flag de producto encontrado
                #Entonces se encuentra el producto printea todos sus datos
                print("\nDatos actuales del producto:")
                print("Nombre:", p[1])
                print("Precio:", p[2])
                print("Stock:", p[3])

                #Ingresamos el nuevo nombre del producto
                nuevo_nombre = input("Nuevo nombre (Enter para dejar igual): ").strip()
                if nuevo_nombre != "": #Mientras el nombre no sea Enter
                    nuevo_nombre = nuevo_nombre[0].upper() + nuevo_nombre[1:].lower() #Configura el nombre para que el formato sea primera letra mayuscula y el resto en minúscula

                    repetido = False
                    for otro in productos: #Recorre toda la matriz de productos para buscar alguna repetición en el nombre de productos, esto anula los repetidos
                        if otro[1].lower() == nuevo_nombre.lower() and otro[0] != id_modificar: #Si coinciden los nombres entonces tira un break
                            repetido = True
                            break
                    if repetido:
                        print("Ese nombre ya existe en esta categoría.")
                    else:
                        p[1] = nuevo_nombre #Si no esta repetido, entonces actualiza el nombre en la ficha

                #Asignamos el nuevo precio
                nuevo_precio = input("Nuevo precio (Enter para dejar igual): ").strip()
                while nuevo_precio != "": #Siempre que el precio no sea vacío
                    puntos = 0
                    digitos_validos = True
                    for c in nuevo_precio:
                        if c == ".":
                            puntos += 1
                        elif not c.isdigit(): #Valida que el precio sea solo numeros, porque si pones un simbolo distinto de 1 entonces te salta error
                            digitos_validos = False
                            break
                    if puntos > 1 or not digitos_validos:
                        print("El precio solo puede tener números y un punto decimal.")
                        nuevo_precio = input("Nuevo precio (Enter para dejar igual): ").strip()
                    else:
                        p[2] = nuevo_precio #Aca si se respetan las condiciones entonces el nuevo precio sobreescribe al original
                        break

                #Asignamos el nuevo stock
                nuevo_stock = input("Nuevo stock (Enter para dejar igual): ").strip()
                while nuevo_stock != "":
                    entero_valido = True
                    for c in nuevo_stock: #Lee caracter por caracter del stock
                        if not c.isdigit(): #Es mas o menos lo mismo que el precio pero esta vez sacamos el contador de puntos porque directamente debe ser entero
                            entero_valido = False
                            break
                    if not entero_valido: #Cuando el flag de entero valido da error significa que se quiso poner un caracter no valido como stock
                        print("El stock debe ser un número entero.")
                        nuevo_stock = input("Nuevo stock (Enter para dejar igual): ").strip()
                    else:
                        p[3] = nuevo_stock
                        break
                break

        if not producto_encontrado: #Cuando el flag de producto encontrado no se activa significa que el for nunca pudo encontrar ese producto entonces cancela la operación
            print("No se encontró el producto con ese ID.")
            continue

        # Reescribir el archivo: Necesitamos actualiar el archivo
        # Reescribir el archivo usando un archivo temporal, sin cargar todo en memoria
        temp_ruta = "inventario_temp.txt"
        try:
            f_original = open(ruta, "rt", encoding="utf-8")
            f_temp = open(temp_ruta, "wt", encoding="utf-8")

            dentro = False  # flag para saber si estamos en la categoría a modificar

            for linea in f_original: #Empezamos a recorrer todo el archivo
                linea_strip = linea.strip()

                
                if len(linea_strip) >= 3 and linea_strip[:10] == "CATEGORIA:": #Detectamos si o no una categoria la linea
                    nombre_cat_linea = linea_strip[10:].strip() #Guardamos el nombre en una variable
                    if nombre_cat_linea == nombre_cat: #Si el nombre es la categoria que elegimos entonces estamos dentro
                        dentro = True #Activamos flag
                        f_temp.write(linea) #Copiamos la categoria dentro del archivo y salteamos el ciclo
                        continue
                    elif dentro:
                        dentro = False #Cuando estemos en la próxima categoria desavtivamos el flag para marcar que estamos fuera

                
                if dentro and len(linea_strip) > 3 and ";" in linea_strip: #Cuando estamos dentro detecta que la próxima linea es un producto
                    ficha_actual = linea.split(";")
                    
                    
                    """
                    ficha_actual = []
                    campo = ""
                    for ch in linea: #Recorremos caracter por caracter la ficha de producto
                        if ch == ";": #Si un caracter tiene un ; es porque es el fin de un campo
                            ficha_actual.append(campo) #El campo una vez copleto se agrega a la ficha actual
                            campo = ""
                        elif ch != "\n": #Por seguridad prevenimos que se agreguen \n en lugares donde no tiene que haber, eso podría romper el sistema
                            campo += ch #Cuando el caracter no es un ; entonces lo sumamos al campo para luego agregarlo
                    ficha_actual.append(campo) #El ultimo campo de stock no se va a agregar por defecto porque para agregarse tendría que haber un ; al final, por eso lo hacemos manual
                    """
                    
                    if ficha_actual[0] == id_modificar: #si es la linea que buscamos entonces la agregamos y pasamos al siguiente ciclo
                        nueva_linea = p[0] + ";" + p[1] + ";" + p[2] + ";" + p[3] + "\n" #Representa el formato String que vamos a subir al archivo
                        f_temp.write(nueva_linea)
                        continue  # pasamos a la siguiente línea
                # Si no es la línea modificada, la copiamos igual
                f_temp.write(linea) #De cualquier modo tenemos que agregar la linea al nuevo archivo

        except Exception as e:
            print("Error al guardar los cambios:", e)
        finally:
            try:
                f_original.close()
            except Exception:
                pass
            try:
                f_temp.close()
            except Exception:
                pass

        # Sobrescribir el archivo original con el temporal
        try:
            #Transcribimos el archivo copia al original
            f_temp = open(temp_ruta, "rt", encoding="utf-8")
            f_original = open(ruta, "wt", encoding="utf-8")
            for linea in f_temp:
                f_original.write(linea)
        except Exception as e:
            print("Error al actualizar el archivo original:", e)
        finally:
            try:
                f_original.close()
            except Exception:
                pass
            try:
                f_temp.close()
            except Exception:
                pass

        print("Producto modificado correctamente.")

def modificar_categorias():
    mostrar_matriz()
    ruta = "inventario.txt"
    vieja = input("Ingrese el nombre de la categoría a modificar: ").strip()
    nueva = input("Ingrese el nuevo nombre de la categoría: ").strip()

    try:
        f = open(ruta, "rt", encoding="utf-8")
        temp = open("temp.txt", "wt", encoding="utf-8")
        modificada = False

        linea = f.readline()
        while linea:    #Recorremos todo el archivo hasta encontrar una categoria, cuando esa categoria coincide con la que yo quiero modificar entonces,
                        #Agrego la modificación al archivo temporal y luego sigo copiando linea por linea
            texto = linea.strip()
            if len(texto) >= 3 and texto[:10] == "CATEGORIA:" and texto[10:].strip() == vieja:
                temp.write("CATEGORIA:" + nueva)
                modificada = True #activa el flag de modificada entonces permite enviar el mensaje
            else:
                temp.write(linea) #Copia la siguiente linea en busca de la categoria buscada
            linea = f.readline() #Pasa de linea

        if modificada:
            print("\nCategoría modificada correctamente.")
        else:
            print("\nNo se encontró la categoría indicada.")
    except Exception as e:
        print("Error inesperado:", e)
    finally:
        try:
            try:
                f.close()
            except Exception:
                pass
            try:
                temp.close()
            except Exception:
                pass
            
            if modificada: #Si se modificó el archivo entonces tenemos que cpiar linea por linea el archivo devuelta para aplicar las modificaciones, pasamos del temporal al original
                origen = open(ruta, "wt", encoding="utf-8")
                copia = open("temp.txt", "rt", encoding="utf-8")
                linea = copia.readline()
                while linea:
                    origen.write(linea)
                    linea = copia.readline()
        except:
            pass
        finally:
            try:
                origen.close()
            except Exception:
                pass
            try:
                copia.close()
            except Exception:
                pass
        
def eliminar_producto():
    ruta = "inventario.txt"
    #Selección por número/abreviación/nombre
    nombre_cat = solicitar_y_resolver_categoria(ruta)
    if not nombre_cat:
        return

    mostrar_categoria(ruta, nombre_cat)
    producto = input("Ingrese el nombre del producto a eliminar: ").strip().title()

    try: #Vamos a duplicar el archivo pero vamos a evitar copiar la ficha de producto que queremos eliminar
        f = open(ruta, "rt", encoding="utf-8")
        temp = open("temp.txt", "wt", encoding="utf-8")

        en_categoria = False
        eliminado = False

        linea = f.readline()
        while linea: #Recorremos el archivo linea por linea
            texto = linea.strip()

            if len(texto) >= 10 and texto[:10] == "CATEGORIA:":
                nombre_cat_linea = texto[10:].strip()
                en_categoria = True if nombre_cat_linea == nombre_cat else None #nombre_cat guarda el nombre de la categoria que yo quiero revisar
                temp.write(linea)
            elif en_categoria and (";" in texto):
                ficha = texto.split(";")
                if ficha[1].strip() == producto:
                    eliminado = True  #Cuando entramos en la categoria, tomamos la ficha de producto y evaluamos si esa ficha de producto tienen el mismo nombre que el que queremos eliminar
                else: #El elimindo es un flag que emite mensaje unicamente
                    temp.write(linea) #Si el nombre no coincide es porque no es ese producto, entonces se copia tranquilamente
            else:
                temp.write(linea) #Si no es una categoria es porque es una ficha que no esta en la categoria buscada

            linea = f.readline() #Pasa a la siguiente linea

        if eliminado:
            print("\nProducto eliminado correctamente.")
        else:
            print("\nNo se encontró el producto.") #Si el flag nunca se activó es porque entonces no existía el producto
    except Exception as e:
        print("Error:", e)
    finally:
        try:
            try:
                f.close()
            except Exception:
                pass
            try:
                temp.close()
            except Exception:
                pass
            
            if eliminado:
                try: #Si hubo un producto eliminado entonces hacemos la copia del temporal al original
                    origen = open(ruta, "wt", encoding="utf-8")
                    copia = open("temp.txt", "rt", encoding="utf-8")
                    linea = copia.readline()
                    while linea:
                        origen.write(linea)
                        linea = copia.readline()
                except Exception:
                    pass
                
        except Exception:
            pass
        finally:
            try:
                origen.close()
            except Exception:
                pass
            try:
                copia.close()
            except Exception:
                pass
        
def eliminar_categorias():
    ruta = "inventario.txt"
    # Selección flexible por número/abreviación/nombre
    nombre_cat = solicitar_y_resolver_categoria(ruta)
    if not nombre_cat:
        return

    try: #Abre el archivo original y una copia para incluir las modificaciones
        f = open(ruta, "rt", encoding="utf-8")
        temp = open("temp.txt", "wt", encoding="utf-8")
        eliminar = False
        saltar = False

        linea = f.readline()
        while linea: #Vamos a leer todo el archivo
            texto = linea.strip()

            if len(texto) >= 3 and texto[:10] == "CATEGORIA:":
                nombre_cat_linea = texto[10:].strip() #Tomamos el nombre de la categoria
                if nombre_cat_linea == nombre_cat: #Si es la que buscamos entocnes habilitamo el flag de saltar categoria
                    eliminar = True
                    saltar = True
                else:
                    saltar = False #Este saltar hace que cuando estemos recorriendo esa categoria se evite copiar los productos, entonces ni bien salgamos de la categoria esa y reconozca una nueva categoria, entonces ahi si te permite copiar la categoria

            if not saltar: #Mientras saltar esté desactivado entonces va a copiar las lineas tal cual esten en el original
                temp.write(linea)

            linea = f.readline() #Pasa de linea

        if eliminar: #Cuando se elimina emite un mensaje de que todo salió bien
            print("\nCategoría eliminada correctamente.")
        else:
            print("\nNo se encontró la categoría.") #Si nunca se eliminó la categoría es porque no se encontró
    except Exception:
        print("No se encontró el archivo.")
    except Exception as e:
        print("Error inesperado:", e)
    finally:
        try:
            try:
                f.close()
            except Exception:
                pass
            try:
                temp.close()
            except Exception:
                pass
            
            if eliminar:
                try:
                    origen = open(ruta, "wt", encoding="utf-8")
                    copia = open("temp.txt", "rt", encoding="utf-8")
                    linea = copia.readline()
                    while linea: #Transcribimos todo el archivo copia al original
                        origen.write(linea)
                        linea = copia.readline()
                except Exception:
                    pass
        except Exception:
            pass
        finally:
            try:
                origen.close()
            except Exception:
                pass
            try:
                copia.close()
            except Exception:
                pass

# ==================================================================== MOSTRAR CATEGORIAS ====================================================================

def mostrar_productos(ruta):
    # Ahora permite número/abreviación/nombre y reutiliza el resolver
    nombre_cat = solicitar_y_resolver_categoria(ruta)
    if not nombre_cat:
        return

    f = None
    try:
        f = open(ruta, "rt", encoding="utf-8")
        presente = False
        linea = f.readline()
        while linea:
            if len(linea) >= 10 and linea[:10] == "CATEGORIA:" and linea[10:].strip() == nombre_cat:
                presente = True
                break
            linea = f.readline()
    except FileNotFoundError:
        print("Error: No se encontró el archivo de inventario.")
        return
    except Exception as e:
        print("️Ocurrió un error al leer el archivo:", e)
        return
    finally:
        try:
            f.close()
        except:
            pass

    if presente:
        print("Encontramos tu categoría:", nombre_cat)
        try:
            mostrar_categoria(ruta, nombre_cat)
        except Exception as e:
            print("Ocurrió un error al mostrar la categoría:", e)
    else:
        print("\nTu categoría no existe o la escribiste mal.")
        return

def solicitar_y_resolver_categoria(ruta):
    """
    La función basicamente muestra todas las categorias, te pide que selecciones una categoria y una vez seleccionada muestra la lista de productos
    """
    mostrar_lista=True
    
    if mostrar_lista:
        try:
            mostrar_matriz()
        except Exception as e:
            print("Ocurrió un error al mostrar la matriz de categorías:", e)

    entrada = input("\n" + "Ingresá la categoría (número/abreviación/nombre). Enter cancela: ").strip()
    if entrada == "":
        return None

    nombre = resolver_categoria_desde_entrada(ruta, entrada)
    return nombre

def resolver_categoria_desde_entrada(ruta, entrada):
    """
    Dado un texto ingresado por el usuario (número/abreviación/nombre),
    devuelve el NOMBRE COMPLETO de la categoría usando la matriz:
    [nro, nombre, abrev]. Si no se encuentra, retorna None.
    """
    try:
        matriz = leer_matriz_categorias_numerada(ruta, empezar_en=1)  # [[nro, nombre, abrev], ...]
    except Exception:
        return None

    if not matriz: #Si no se devuelve ninguna matriz entonces sale
        return None

    if entrada is None: #La entrada es la categoria que queremos ver
        return None

    entrada_str = str(entrada).strip()
    if entrada_str == "":
        return None

    # 1) Si es un número, usa la primer columna y devuelve el nombre (columna 2)
    if entrada_str.isdigit():
        objetivo = int(entrada_str)
        for fila in matriz:
            # fila: [nro, nombre, abrev]
            if len(fila) >= 2 and fila[0] == objetivo:
                return str(fila[1]).strip()

    # 2) Si no es número, busca por abreviación (col 3) o por nombre (col 2)
    low = entrada_str.lower()
    for fila in matriz:
        nombre = str(fila[1]).strip() if len(fila) >= 2 and fila[1] is not None else ""
        abrev  = str(fila[2]).strip() if len(fila) >= 3 and fila[2] is not None else ""
        if (abrev and abrev.lower() == low) or (nombre and nombre.lower() == low):
            return nombre

    return None

def mostrar_matriz():
    matriz_categorias = leer_matriz_categorias_numerada()

    if not matriz_categorias:
        print("(No hay categorías)")
        return

    for fila in matriz_categorias:
        # Solo los dos primeros valores: número y nombre
        if len(fila) >= 2:
            print(fila[0], fila[1])
        elif len(fila) == 1:
            print(fila[0])
            
def leer_matriz_categorias_numerada(ruta=None, empezar_en=1):
    """
    Lee el inventario y devuelve una matriz con tres columnas:
    [[1, 'Categoria1', 'Cat'], [2, 'Categoria2', 'Cat'], ...]
    Basicamente crea una matriz
    """
    # Resolver ruta por defecto
    if ruta is None:
        try:
            ruta = file
        except NameError:
            ruta = "inventario.txt"

    matriz = []
    numero = int(empezar_en)
    f = None
    
    try: #Lee linea por linea el archivo buscando categorias
        f = open(ruta, "rt", encoding="utf-8")
        linea = f.readline()
        while linea:
            linea = linea.lstrip("\ufeff").strip()
            if (len(linea) >= 3) and (linea[:10] == "CATEGORIA:"): #Cuando la linea es una categoria entonces queremos obtener su abreviación
                nombre = linea[10:].strip()
                if nombre != "":
                    abrev = obtener_abreviacion(nombre) #nombre representa lo que va después de categoria:, por ejemplo CATEGORIA:Electronica
                    # Estructura: [número, nombre, abreviación]
                    matriz.append([numero, nombre, abrev]) #Por defecto el primer numero es 1 pero a medida que sumamos las categorias el número suma en 1
                    numero = numero + 1
            linea = f.readline()
    except FileNotFoundError:
        print("Error: No se encontró el archivo de inventario:", ruta)
    except Exception as e:
        print("Error al leer categorías:", e)
    finally:
        try:
            if f is not None:
                f.close()
        except:
            pass

    return matriz

def obtener_abreviacion(nombre_categoria):
    """
    Devuelve una abreviación de hasta 3 letras alfabéticas.
    Formato: primera letra en MAYÚSCULA y las siguientes en minúscula (p. ej., 'Ele').
    Si el nombre tiene menos de 3 letras, usa las disponibles.
    Si no hay letras, devuelve cadena vacía.
    """
    nombre = str(nombre_categoria)
    solo_letras = ""
    i = 0
    
    #Elimina cualquier caracter que no sea una letra, esto lo hace para obtener la abreviación unicamente de letras
    while i < len(nombre):
        ch = nombre[i]
        if ch.isalpha():
            solo_letras = solo_letras + ch
        i = i + 1

    if solo_letras == "":
        return ""

    solo_letras = solo_letras.lower()
    if len(solo_letras) >= 3:
        abrev = solo_letras[0:3]
    else:
        abrev = solo_letras

    return abrev[0].upper() + abrev[1:] #Devuelve una abreviación con primer letra mayúscula, ejemplo "Ele" de electrónica

def mostrar_categoria(ruta, categoria_buscada):
    """
    Muestra los productos de una categoría.
    Acepta: número, abreviación o nombre; se resuelve a nombre completo automáticamente.
    """
    nombre_resuelto = resolver_categoria_desde_entrada(ruta, categoria_buscada)
    if nombre_resuelto is None:
        print("No se encontró la categoría (por índice, abreviación o nombre).")
        return

    f = None
    try:
        f = open(ruta, "rt", encoding="utf-8")
        dentro = False
        hay_productos = False

        print(f"\n{'ID':<6}{'Producto':<20}{'Precio':<10}{'Stock':<10}")
        print("-" * 46)

        for linea in f:
            linea = linea.strip()

            # Cabecera de categoría
            if len(linea) >= 10 and linea[:10] == "CATEGORIA:":
                nombre_categoria = linea[10:].strip()

                if nombre_categoria.lower() == nombre_resuelto.lower():
                    dentro = True
                    continue  # saltar cabecera

                elif dentro:
                    break  # ya terminó la categoría a mostrar

            # Productos
            if dentro and ";" in linea:
                ficha = linea.split(";")
                if len(ficha) >= 4:
                    print(f"{ficha[0]:<6}{ficha[1]:<20}{ficha[2]:<10}{ficha[3]:<10}")
                    hay_productos = True

        if not hay_productos:
            print("No se encontraron productos en esta categoría.")
        print()

    except FileNotFoundError:
        print("Error: no se encontró el archivo de inventario.")
    except Exception as e:
        print("Ocurrió un error al leer/mostrar la categoría:", e)
    finally:
        try:
            if f is not None:
                f.close()
                
        except:
            pass
        return


# ==================================================================== PROGRAMA PRINCIPAL ====================================================================


print("Bienvenido al sistema de gestión de inventario:")
print("-" * 50)

usuario = input("Ingresa el usuario: ").strip().lower()
contra  = input("Ingresa la contraseña: ").strip()

# Repite mientras alguno sea incorrecto
while usuario != "admin" or contra != "123":
    print("Datos incorrectos!")
    usuario = input("Ingresa el usuario: ").strip().lower()
    contra  = input("Ingresa la contraseña: ").strip()

print("Acceso concedido. Entrando al menú...")
menu(file)