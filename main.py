import flet as ft
import aiohttp
import asyncio

pokemon_actual = -1
shiny = False

async def main(page: ft.Page):
    page.window_width = 720
    page.window_height= 1045
    page.window_resizable = False
    page.padding = 0
    
    
    
    

    #funciones

    async def peticion(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()

    async def evento_getPokemon(e: ft.ContainerTapEvent):
        global pokemon_actual
        global shiny
        if e.control == flecha_superior:
            pokemon_actual +=1
        else:
            pokemon_actual -=1
        numero = (pokemon_actual%10263)+1
        resultado = await peticion(f"https://pokeapi.co/api/v2/pokemon/{numero}")


        datos = f"Nombre: {resultado['name']}\n\nHabilidades: "
        for elemento in resultado['abilities']:
            habilidad = elemento['ability']['name']
            datos += f"\n{habilidad}"
        datos += "\nEstadisticas:\n"

        stadis=["HP", "Atq", "Def", "SAtc", "SDef", "Spe"]
        i = 0
        for elemento in resultado['stats']:
            stat_nombre = elemento['stat']['name']  # Obtiene el nombre de la estadística
            stat_valor = elemento['base_stat']  # Obtiene el valor de la estadística
            datos += f"| {stadis[i]}: {stat_valor} "
            i += 1
        
        texto.value= datos   

        imagen.src = spriteType(numero)

        await page.update_async()

    def sprite_normal(numero):
        return f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{numero}.png"
    
    def sprite_shiny(numero):
        return f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/shiny/{numero}.png"
    
    def spriteType(numero):
        sprite= ''
        if shiny == True: 
            sprite = sprite_shiny(numero)
        else:
            sprite = sprite_normal(numero)  

        return sprite
    
    async def evento_modoShiny(e: ft.ContainerTapEvent):
        global shiny
        if shiny:
            shiny = False
        else:
            shiny = True
        numero = (pokemon_actual%10263)+1

        imagen.src = spriteType(numero)
        await page.update_async()

    async def blinck():
        while True:
            await asyncio.sleep(1)
            luz_azul.bgcolor = ft.colors.BLUE_100
            await page.update_async()
            await asyncio.sleep(0.1)
            luz_azul.bgcolor = ft.colors.BLUE
            await page.update_async()
    
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------


    #contenido de superior


    luz_azul = ft.Container(width=70, height=70, left=5, top=5, bgcolor=ft.colors.BLUE, border_radius=50)

    boton_azul= ft.Stack([
        ft.Container(width=80, height=80, bgcolor=ft.colors.WHITE, border_radius=50),
        luz_azul,
    ])

    estrella = ft.canvas.Canvas([
    ft.canvas.Path(
            [
                ft.canvas.Path.MoveTo(40, 0),
                ft.canvas.Path.LineTo(48, 30),
                ft.canvas.Path.LineTo(80, 35),
                ft.canvas.Path.LineTo(60, 50),
                ft.canvas.Path.LineTo(70, 80),
                ft.canvas.Path.LineTo(40, 65),
                ft.canvas.Path.LineTo(10, 80),
                ft.canvas.Path.LineTo(20, 50),
                ft.canvas.Path.LineTo(0, 35),
                ft.canvas.Path.LineTo(32, 30),
            ],
            paint=ft.Paint(
                style=ft.PaintingStyle.FILL,
                color=ft.colors.YELLOW
            ),
        ),
    ],
        width=80,
        height=80,
    )
    
    estrella_modoShiny = ft.Container(estrella, width=80, height=50, on_click=evento_modoShiny)

    #define todos los elementos que se agregaran a la parte superior 
    items_superior = [
        ft.Container(boton_azul, width=80, height=80),
        ft.Container(width=40, height=40, bgcolor=ft.colors.RED_200, border_radius=50),
        ft.Container(width=40, height=40, bgcolor=ft.colors.YELLOW, border_radius=50),
        ft.Container(width=40, height=40, bgcolor=ft.colors.GREEN, border_radius=50),
        ft.Container(estrella_modoShiny)
    ]
    #----------------------------------------------

    #contenido de centro

    #importamos la imagen y escalamos
    sprite_url=f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon_actual}.png"
    imagen = ft.Image(
        src=sprite_url,
        scale=5,
        width=50,
        height=50,
        top=350/2,
        right=550/2,
    )

    #crea el stack de la pantalla
    stack_central= ft.Stack([
        ft.Container(width=600, height=400, bgcolor=ft.colors.WHITE),
        ft.Container(width=550, height=350, bgcolor=ft.colors. BLACK, top=25, left=25,) ,
        imagen
    ])
    #----------------------------------------------


    #contenido de inferiro

    #dibujamos un triangulo
    triangulo = ft.canvas.Canvas([
        ft.canvas.Path(
                [
                    ft.canvas.Path.MoveTo(40, 0),
                    ft.canvas.Path.LineTo(0,50),
                    ft.canvas.Path.LineTo(80,50),
                ],
                paint=ft.Paint(
                    style=ft.PaintingStyle.FILL,
                ),
            ),
        ],
        width=80,
        height=50,
    )

    


    flecha_superior = ft.Container(triangulo, width=80, height=50, on_click=evento_getPokemon)

    # rotamos el tiangulo convirtiendolo en radianes, 180 grados =3.14159
    flecha_inferior =  ft.Container(triangulo, rotate=ft.Rotate(angle=3.14159), width=80, height=50,  on_click=evento_getPokemon)

    


    flechas=ft.Column(
        [
            flecha_superior,
            flecha_inferior, 

        ]
    )

    texto=ft.Text(
        value="...", 
        color=ft.colors.BLACK,
        size=22,
    )

    items_inferior = [
        ft.Container(width=30),
        ft.Container(texto, padding=10, width=420, height=300, bgcolor=ft.colors.GREEN,border_radius=20),
        ft.Container(flechas, width=80, height=120),
        
    ]

    #----------------------------------------------


    superior = ft.Container(content=ft.Row(items_superior), width=600, height=80, margin=ft.margin.only(top=40))
    centro = ft.Container(content=stack_central, width=600, height=400, margin=ft.margin.only(top=40), border=ft.border.all(), alignment=ft.alignment.center)
    inferior = ft.Container(content=ft.Row(items_inferior), width=600, height=400, margin=ft.margin.only(top=40), )

    col = ft.Column(spacing=0, controls=[
        superior,
        centro,
        inferior,
    ])
    contenedor = ft.Container(col, width=720, height=1045, bgcolor=ft.colors.RED, alignment=ft.alignment.top_center)

    await page.add_async(contenedor)
    await blinck()

ft.app(target=main)