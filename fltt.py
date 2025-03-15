import flet as ft
import requests
from datetime import datetime


def main(page: ft.Page):
    page.clean()
    page.scroll = "auto"
    def listapontohora(data, mess):
        page.clean()
        cont = ft.Container(
        ft.Row(
            [
                ft.ElevatedButton(
                    "Voltar", 
                    on_click=lambda e: main(page),
                    bgcolor=ft.colors.BLUE_700,
                    color=ft.colors.WHITE,
                    height=45,
                    width=100,
                    elevation=10,
                 ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        ),
        alignment=ft.alignment.center,
        margin=ft.Margin(top=10, right=20, bottom=20, left=20),  # Corrigido para passar todos os 4 parâmetros
        )
        page.add(cont)

        page.scroll = "auto"
        totalhr = 0.0
        for dt in data:
            entrada_dt = datetime.strptime(data[0]['entrada'], "%m/%d/%y %H:%M:%S")
        
            mes = entrada_dt.month
            if mess == mes:
                nome = dt["nome"]
                entrada = dt["entrada"]
                saida = dt["saida"]
                datetime_obj = datetime.strptime(entrada, "%m/%d/%y %H:%M:%S")
                datetime_obj2 = datetime.strptime(saida, "%m/%d/%y %H:%M:%S")
                
                # Calculando a diferença entre as datas (como timedelta)
                diferenca = datetime_obj2 - datetime_obj
                
                # Obtendo a diferença em horas (pode incluir minutos e segundos)
                totalhr += diferenca.total_seconds() / 3600

                # Adicionando cada item de horário com um estilo aprimorado
                page.add(
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text(f"Nome: {nome}", size=20, weight="bold", color=ft.colors.BLACK),
                                        ft.Text(f"Entrada: {entrada}", size=18, color=ft.colors.BLACK),
                                        ft.Text(f"Saída: {saida}", size=18, color=ft.colors.BLACK),
                                    ],
                                    spacing=5,
                                    alignment=ft.MainAxisAlignment.CENTER  # Centralizando os textos dentro do Column
                                ),
                                padding=15,
                                bgcolor=ft.colors.LIGHT_BLUE_50,
                                border_radius=10,
                                width=400,
                                height=150,
                                alignment=ft.alignment.center  # Centralizando o próprio Container
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,  # Centraliza o conteúdo na vertical
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,  # Centraliza na horizontal
                        expand=True  # Faz o Row ocupar toda a tela
                    )
                )
    

            # Adicionando total de horas com um destaque
            page.add(
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text(f"Total de Horas Trabalhadas: {totalhr:.2f} horas", size=24, weight="bold", color=ft.colors.WHITE),
                                ],
                                alignment=ft.alignment.center,
                                # Centralizando os textos dentro do Column
                            ),
                            padding=25,
                            bgcolor=ft.colors.GREEN_700,
                            border_radius=10,
                            width=500,
                            height=100,
                            alignment=ft.alignment.center  # Centralizando o próprio Container
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza o conteúdo na vertical
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,  # Centraliza na horizontal
                    expand=True,  # Faz o Row ocupar toda a tela
                    spacing=100
                )
            )
    def requerir(nome, mess):
        url = f"https://itecponto.vercel.app/{nome}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(data)

            mess = int(mess)
            print(mess)
            listapontohora(data, mess)
        else:
            print(f"Erro na requisição: {response.status_code}")

    # Input do nome
    txtnome = ft.TextField(label="Digite o nome", label_style=ft.TextStyle(color=ft.colors.BLUE_800), autofocus=True, width=350)
    txtmes = ft.TextField(label="Digite o MES", label_style=ft.TextStyle(color=ft.colors.BLUE_800), autofocus=True, width=350)

    # Botão de buscar com um estilo mais chamativo
    cont = ft.Container(
        ft.Row(
            [
                txtnome,
                txtmes,
                ft.ElevatedButton(
                    "Buscar", 
                    on_click=lambda e: requerir(txtnome.value, txtmes.value),
                    bgcolor=ft.colors.BLUE_700,
                    color=ft.colors.WHITE,
                    height=45,
                    width=100,
                    elevation=10
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        ),
        alignment=ft.alignment.center,
        margin=ft.Margin(top=10, right=20, bottom=20, left=20),  # Corrigido para passar todos os 4 parâmetros
    )

    # Adicionando o container com o campo e o botão à página
    page.add(
        cont,
        ft.Container(
            ft.Divider(color=ft.colors.GREY_400, thickness=1),
            #margin=ft.Margin(top=10, right=0, bottom=10, left=0)  # Corrigido para passar todos os 4 parâmetros
        ),
    )

    # Estilizando a página
    page.bgcolor = ft.colors.WHITE
    page.add(
        ft.Container(
            ft.Text("Controle de Horas Trabalhadas", size=30, weight="bold", color=ft.colors.BLUE_800),
            alignment=ft.alignment.center,
            #margin=ft.Margin(top=20, bottom=20)
        )
    )

ft.app(main)
