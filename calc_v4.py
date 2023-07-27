import flet as ft
import pandas as pd
import datetime as dt
import numpy as np
import locale
locale.setlocale(locale.LC_ALL, '')
# valoresBN = [1800, 2800, 5900, 9000, 11700]
# valoresColor = [2000, 3200, 6500, 10000, 13000]
largos = [1189, 841, 594, 420]
anchos = [841, 594, 420, 297]
tamaños = [
    ft.dropdown.Option('A0'),
    ft.dropdown.Option('A1'),
    ft.dropdown.Option('A2'),
    ft.dropdown.Option('A3'),
    ft.dropdown.Option('Personalizado')
    ]
colores=[
    ft.dropdown.Option('BN/Gris'),
    ft.dropdown.Option('Color')
    ]
cantidadesColor=[
    ft.dropdown.Option('Líneas'),
    ft.dropdown.Option('10%'),
    ft.dropdown.Option('25%'),
    ft.dropdown.Option('50%'),
    ft.dropdown.Option('75%'),
    ft.dropdown.Option('100%'),
    ]

preciosBNEmpresa=np.array([1800, 2500, 2800, 5900, 9000, 11700])/1.19 + (250/1.19)
preciosColorEmpresa=np.array([2000, 2800, 3200, 6500, 10000, 13000])/1.19 + (250/1.19)
Largo=int()
Ancho=int()

def main(page: ft.Page):
    # page.icon = './BAGUPrint_icon.png'
    page.title = 'Cotización BAGUPrint'
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = 'AUTO'
    page.auto_scroll = True
    page.appbar = ft.AppBar(
        title=ft.Text(
            "Cotización BAGUPrint", style=ft.TextThemeStyle.DISPLAY_SMALL, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK87
        ),
        bgcolor=ft.colors.RED, # #FF0000 hexadec funciona igual
        center_title=True,
        color=ft.colors.WHITE,
    )

    def on_change_tamaño(e):
        def on_blur_L(e):
            # global Largo
            globals()['Largo'] = int(largo.value)
            page.update()
            return
        def on_blur_A(e):
            # global Ancho
            globals()['Ancho'] = int(ancho.value)
            page.update()
            return
        largo = ft.TextField(label='Largo', on_blur=on_blur_L, width=150, border_color='red', content_padding=1, text_align='center')
        ancho = ft.TextField(label='Ancho', on_blur=on_blur_A, width=150, border_color='red', content_padding=1, text_align='center')
        persoRow = ft.Row(spacing=5, controls=[largo, ancho])

        if tamaño.value == 'Personalizado':
            # pip=1
            lastIndex=len(page.controls)-3
            page.insert(lastIndex, persoRow)
            global rowVal
            rowVal = page.controls[lastIndex]
        elif tamaño.value == 'A0':
            try:
                page.controls.remove(rowVal)
            except:
                pass
            globals()['Largo'], globals()['Ancho'] = largos[0], anchos[0]
        elif tamaño.value == 'A1':
            try:
                page.controls.remove(rowVal)
            except:
                pass
            globals()['Largo'], globals()['Ancho'] = largos[1], anchos[1]
        elif tamaño.value == 'A2':
            try:
                page.controls.remove(rowVal)
            except:
                pass
            globals()['Largo'], globals()['Ancho'] = largos[2], anchos[2]
        elif tamaño.value == 'A3':
            try:
                page.controls.remove(rowVal)
            except:
                pass
            globals()['Largo'], globals()['Ancho'] = largos[3], anchos[3]
        page.update()
        return

    def Datos2DF(datos: list):
        Archivo = datos[0]
        Fecha = datos[1]
        Detalle = datos[2]
        Copias = int(datos[3])
        L = datos[4]
        A = datos[5]
        if (L>900) | (A>900):
            TotalMetros = max([L, A])
        else:
            TotalMetros = min([L, A])

        if datos[6] == 'BN/Gris':
            precios=preciosBNEmpresa
        else:
            precios=preciosColorEmpresa

        if datos[7]=='Líneas':
            VsIVA = round(precios[0])
        elif datos[7]=='10%':
            VsIVA = round(precios[1])
        elif datos[7]=='25%':
            VsIVA = round(precios[2])
        elif datos[7]=='50%':
            VsIVA = round(precios[3])
        elif datos[7]=='75%':
            VsIVA = round(precios[4])
        else:
            VsIVA = round(precios[5])

        TsIVA = Copias*round((VsIVA*TotalMetros*0.001))
        DetalleColor = datos[7]+' '+datos[6]
        df.loc[len(df)] = [Archivo, Fecha, Detalle, DetalleColor, Copias, L, A, TotalMetros, VsIVA, TsIVA]

        return

    def table():
        def deleteRow(e):
            idx = datatable.rows.index(e.control)
            datatable.rows.remove(e.control)
            globals()['df'] = df.drop(idx).reset_index(drop=True)
            page.update()
            return

        global tabVal
        try:
            page.controls.remove(tabVal)
        except:
            pass
        datatable = ft.DataTable()
        for i in range(len(df.columns)):
            datatable.columns.append(ft.DataColumn(ft.Text(df.columns[i])))
        # datatable.columns.append(ft.DataColumn(ft.Text('Editar')))
        for x in range(len(df)):
            datatable.rows.append(
                ft.DataRow(
                cells=[
                ft.DataCell(ft.Text(df["Archivo"][x])),
                ft.DataCell(ft.Text(df["Fecha"][x])),
                ft.DataCell(ft.Text(df["DETALLE"][x])),
                ft.DataCell(ft.Text(df["Detalle color"][x])),
                ft.DataCell(ft.Text(df["COPIAS"][x])),
                ft.DataCell(ft.Text(df["Largo (mm)"][x])),
                ft.DataCell(ft.Text(df["Ancho (mm)"][x])),
                ft.DataCell(ft.Text(df["Total (mm)"][x])),
                ft.DataCell(ft.Text(df["Valor (m) (sin IVA)"][x])),
                ft.DataCell(ft.Text(df["Total (sin IVA)"][x])),
                # ft.DataCell(ft.Text(""), show_edit_icon=True, on_tap=deleteRow)
                ],
                on_select_changed=deleteRow,
                # selected=True
                )
            )
        page.insert(0, datatable)
        tabVal = page.controls[0]
        return

    def onClickBtn(e):
        addRow.data += 1
        if (fileName.value=='')|(fecha.value=='')|(detalle.value=='')|(copias.value=='')|(tamaño.value=='')|(color.value=='')|(cantidadColor.value==''):
            dlg = ft.AlertDialog(title=ft.Text('Debes llenar todos los campos.'))
            page.dialog = dlg
            dlg.open=True
            page.update()
        elif (tamaño.value=='Personalizado') & ((globals()['Largo']==largos[1]) | (globals()['Ancho']==largos[1]) | ((globals()['Largo']==0) | (globals()['Ancho']==0)) | (globals()['Largo']==None) | (globals()['Ancho']==None)):
            dlg2 = ft.AlertDialog(title=ft.Text('Debes especificar el Largo y Ancho del documento.'))
            page.dialog = dlg2
            dlg2.open=True
            page.update()
            pass
        else:
            if tamaño.value=='A1':
                globals()['Largo']=largos[1]
                globals()['Ancho']=anchos[1]
                pass
            listaDatos = [fileName.value, fecha.value, detalle.value, copias.value, globals()['Largo'], globals()['Ancho'], color.value, cantidadColor.value]
            Datos2DF(listaDatos)
            table()
            listaDatos.clear()
        detalle.value = f'lámina {addRow.data+1}'
        page.update()
        return


    def onClickDwnldBtn(e):
        def onClickSaveBtn(e):
            if nombreArchivo.value == '':
                dlg4 = ft.AlertDialog(title=ft.Text('Dale un nombre al archivo'), on_dismiss=onClickDwnldBtn)
                page.dialog = dlg4
                dlg4.open = True
                page.update()
            else:
                ##### AQUI VA EL COSO #####
                writer = pd.ExcelWriter(nombreArchivo.value+'.xlsx', engine='xlsxwriter')
                #####
                df.to_excel(writer, sheet_name='Cotización', index=False, header=False, startrow=15)
                #####
                wb = writer.book
                ws = writer.sheets['Cotización']
                titleFormat = wb.add_format({'align': 'center', 'font_name': 'calibri', 'font_size': 20, 'bold': 1})
                subtitleFormat = wb.add_format({'align': 'center', 'font_name': 'calibri', 'font_size': 11, 'bold': 1})
                cobraLargoFmt = wb.add_format({'bg_color': '#FFFF00'})
                dfHeaderFmt = wb.add_format({'font_name': 'calibri', 'font_size': 11, 'bold': 1, 'fg_color': '#FCE4D6', 'border': 2})
                notasHeaderFmt = wb.add_format({'align': 'center', 'font_name': 'calibri', 'font_size': 11, 'bold': 1, 'fg_color': '#FCE4D6', 'border': 2})
                borderFmt = wb.add_format({'border': 2})
                pesoFmt = wb.add_format({'num_format': '$   #0'})
                ws.merge_range(0, 0, 0, 9, 'BAGUPrint SPA', titleFormat) # 9 = len(df.columns)-1
                ws.merge_range(1, 0, 1, 9, 'Impresión y digitalización de planos', subtitleFormat)
                ws.insert_image(0, 0, 'BAGUPrint_icon.png', {'x_scale': 0.27, 'y_scale': 0.27})
                merge_formatPC = wb.add_format({'align': 'center',"border": 2,"fg_color": "#FCE4D6", 'text_wrap': True, 'font_size': 16, 'font_name': 'calibri', 'bold': 1})
                merge_formatPara = wb.add_format({'align': 'left',"border": 2,"fg_color": "#FCE4D6", 'text_wrap': True})
                len_cols = len(df.columns)
                ws.merge_range(10, 0, 11, len_cols - 1, f'Proyecto: {proyecto.value}\nConstructora: {constructora.value}', merge_formatPC) #proyecto.value constructora.value
                ws.merge_range('I3:J7', f'Fecha  : %s\nPara    : %s\nCargo : %s\nDe       : Tatiana Uribe Olate\nCargo : Administradora BAGUPrint SPA' %(today.strftime('%A, %d de %B de %Y'), para.value, cargo.value), merge_formatPara)
                ws.merge_range(8, 0, 8, 9, 'Nos es grato presupuestar el servicio de impresión de planos, en el cual se detalla lo sgte.', subtitleFormat)
                ws.set_row(10, 20)
                ws.set_row(11, 20)
                ws.write_row('A15:J15', data = tuple(df.columns), cell_format=dfHeaderFmt)
                ws.set_column(0, 0,40)
                ws.set_column(1,1,12)
                ws.set_column(2,2,25)
                ws.set_column(3,3,20)
                ws.set_column(4,4,7)
                ws.set_column(5,7,11)
                ws.set_column(8,9,17)
                ws.conditional_format(15, 7, 15+len(df), 7, {'type': 'cell', 'criteria': '>', 'value': 900, 'format': cobraLargoFmt})
                ws.conditional_format(15, 8, 15+len(df), 9, {'type': 'cell', 'criteria': '>', 'value': 0, 'format': pesoFmt})
                if doblados.value!=0:
                    valorDoblados = 250*int(doblados.value)
                    ws.write_string(15+len(df), 2, 'Doblado %s' %tamañoDoblados.value)
                    ws.write_number(15+len(df), 4, int(doblados.value))
                    ws.write_number(15+len(df), 8, 250)
                    ws.write_number(15+len(df), 9, valorDoblados)
                else:
                    valorDoblados = 0
                    pass
                ### SUBTOTAL IVA y TOTAL ###
                valorSubTotal = valorDoblados + sum(df['Total (sin IVA)'])
                iva = round(valorSubTotal*0.19)
                ws.write_row(ws.dim_rowmax+1, 8, ('Subtotal', valorSubTotal), cell_format=dfHeaderFmt)
                ws.write_row(ws.dim_rowmax+1, 8, ('IVA 19%', iva), cell_format=dfHeaderFmt)
                ws.write_row(ws.dim_rowmax+1, 8, ('Total', iva + valorSubTotal), cell_format=dfHeaderFmt)
                ws.conditional_format(0, 8, ws.dim_rowmax, 9, {'type': 'cell', 'criteria': '>', 'value': 0, 'format': pesoFmt})
                ### NOTAS Y CTA BANCARIA ###
                cN = len(listaNFeedback)+1 #cantidad notas + nota1
                notasIdx = ws.dim_rowmax+5
                ws.merge_range(notasIdx, 0, notasIdx, 6, 'NOTAS', notasHeaderFmt)
                ws.merge_range(ws.dim_rowmax, 7, ws.dim_rowmax, 9, 'DATOS DE TRANSFERENCIA', notasHeaderFmt)
                dfNotas = pd.DataFrame({'notas': [nota1.value] + listaNFeedback})
                dfDB = pd.DataFrame({'DB': ['Banco  : Banco Estado', 'Cuenta : Chequera Electrónica o Cuenta Vista', 'N°          : 64770239123', 'RUT       : 76.825.571-7', 'e-mail   : baguprint@gmail.com']})
                dfNotas.to_excel(writer, sheet_name='Cotización', index=False, header=False, startrow=ws.dim_rowmax+1)
                dfDB.to_excel(writer, sheet_name='Cotización', index=False, header=False, startrow=ws.dim_rowmax-cN+1, startcol=7)

                footerFmt = wb.add_format({'bold': 1, 'font_name': 'calibri', 'font_size': 11, 'align': 'center', 'text_wrap': True})
                ws.merge_range(ws.dim_rowmax+4, 0,ws.dim_rowmax+6, 9, f'Atte.\nTatiana Uribe Olate\nBAGUPrint SpA. / 4 Poniente 0403, esquina 23 Sur / Correo: baguprint@gmail.com / Fono: +56 9 6645 3487, +56 9 5633 3933', footerFmt)
                writer.close()
                #####
                dlg4 = ft.AlertDialog(title=ft.Text('Listo!'))
                page.dialog=dlg4
                dlg4.open=True
                page.update()
                dlg3.open=False
                page.update()
            return
        para = ft.TextField(label='Para', border_color='red', content_padding=10, text_align='center', value='_________')
        cargo = ft.TextField(label='Cargo', border_color='red', content_padding=10, text_align='center', value='_________')
        proyecto = ft.TextField(label='Proyecto', value='__________________', border_color='red', content_padding=10, text_align='center')
        constructora = ft.TextField(label='Constructora', value='__________________', border_color='red', content_padding=10, text_align='center')
        nombreArchivo = ft.TextField(label='Nombre del archivo', width=250, border_color='red', content_padding=10, text_align='center')
        saveBtn = ft.ElevatedButton(width=150, content=ft.Row([ft.Icon(name='download', color='green'), ft.Text('Exportar')]), on_click=onClickSaveBtn)
        dlg3 = ft.AlertDialog(
            title=ft.Text('Exportar Excel'),
            content=ft.Container(content=ft.Column(spacing=10, controls=[para, cargo, proyecto, constructora, nombreArchivo, saveBtn], wrap=True)),
            title_padding=ft.padding.symmetric(10, 150)
            )
        page.dialog=dlg3
        dlg3.open=True
        page.update()

        return

    global df
    df = pd.DataFrame(columns=['Archivo', 'Fecha', 'DETALLE', 'Detalle color', 'COPIAS', 'Largo (mm)', 'Ancho (mm)', 'Total (mm)', 'Valor (m) (sin IVA)', 'Total (sin IVA)'])

    fileName = ft.TextField(label='Archivo', width=200, border_color='red', content_padding=10, text_align='center')
    today = dt.datetime.now()
    fecha = ft.TextField(label='Fecha', width=100, border_color='red', content_padding=10, value=str(today.day)+'-'+str(today.month)+'-'+str(today.year), text_align='center')

    addRow = ft.ElevatedButton(
        width=150,
        content=ft.Row([
            ft.Icon(name=ft.icons.ADD_BOX, color='red'),
            ft.Text('Añadir fila')
            ]),
        on_click=onClickBtn,
        data = 0
        )

    detalle = ft.TextField(label='DETALLE', width=200, border_color='red', content_padding=10, value=f'lámina {addRow.data+1}', text_align='center')

    copias = ft.TextField(label='COPIAS', width=70, border_color='red', content_padding=10, value=int(1), text_align='center')

    tamaño = ft.Dropdown(label='Tamaño', value='A1', on_change=on_change_tamaño, width=200, border_color='red', content_padding=10, options=tamaños, autofocus=True)

    color = ft.Dropdown(label='Color', value='BN/Gris', width=200, border_color='red', content_padding=10, options=colores)
    cantidadColor = ft.Dropdown(label='Cantidad de color', width=200, border_color='red', content_padding=10, options=cantidadesColor)

    Controls = [fileName, fecha, detalle, copias, tamaño, color, cantidadColor]
    page.insert(1, ft.Row(spacing=5, controls=Controls))

    page.insert(len(page.controls), addRow)

    page.floating_action_button = ft.FloatingActionButton(icon = ft.icons.DOWNLOAD, on_click=onClickDwnldBtn, bgcolor='green')

    doblados = ft.TextField(label='Doblados', value=0, width=100, border_color='red', content_padding=10)
    tamañoDoblados = ft.Dropdown(label='Tamaño', value='Carta', width=100, border_color='red', content_padding=10, options=[ft.dropdown.Option('Carta'), ft.dropdown.Option('Oficio'), ft.dropdown.Option('Funda')])
    page.add(ft.Row([ft.Container(content=doblados), ft.Text('Planos doblados tamaño:'), ft.Container(content=tamañoDoblados)], alignment=ft.MainAxisAlignment.CENTER))

    notasHeader = ft.Text('Notas:', size=30, color='WHITE', weight='BOLD')
    nota1 = ft.Text('Nota 1: Se considera el lado más largo si sobrepasa los 900 mm del ancho del Plotter (celdas amarillas).')
    n = 1
    notaN = ft.TextField(label='Nueva Nota', width=600, border_color='red', content_padding=10, text_align='left')
    # notaFeedback = ft.Text()
    notasAdded = []
    global listaNFeedback
    listaNFeedback = []
    def notaBtnClicked(e):
        notaFeedback = ft.Text()
        notaBtn.data += 1
        notaFeedback.value = f'Nota {notaBtn.data}: '+notaN.value
        globals()['listaNFeedback'].append(f'Nota {notaBtn.data}: '+notaN.value)
        notasAdded.append(notaFeedback)
        page.add(ft.Container(content=ft.Column(notasAdded), alignment=ft.alignment.bottom_left))
        notaN.value=None
        page.update()
        page.controls.pop()
        return notasAdded

    notaBtn = ft.IconButton(icon=ft.icons.ADD, icon_color='red', icon_size=20, on_click=notaBtnClicked, data=1)
    page.add(ft.Container(content=ft.Column([notasHeader, ft.Row([notaN, notaBtn]), nota1]), alignment=ft.alignment.bottom_left))


    page.update()

ft.app(target=main)

