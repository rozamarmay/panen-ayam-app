from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from datetime import datetime

Window.clearcolor = (1,1,1,1)


class PanenLayout(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(orientation="horizontal", **kwargs)

        sidebar = BoxLayout(orientation="vertical", size_hint=(0.2,1),padding=20,spacing=20)
        sidebar.add_widget(Label(text="MENU", font_size=28, color=(0,0,0,1)))

        btn = Button(text="Tambah DO", size_hint=(1,None), height=50)
        btn.bind(on_press=self.form_do)
        sidebar.add_widget(btn)

        self.add_widget(sidebar)

        self.main = BoxLayout(orientation="vertical",padding=20,spacing=15)
        self.add_widget(self.main)

        self.home()

    def clear(self):
        self.main.clear_widgets()

# ================= POPUP =================

    def show_popup(self,pesan):

        box=BoxLayout(orientation="vertical",padding=20,spacing=20)

        with box.canvas.before:
            Color(1,1,1,1)
            self.rect = Rectangle(size=box.size, pos=box.pos)

        box.bind(size=self.update_rect, pos=self.update_rect)

        box.add_widget(Label(text=pesan, color=(0,0,0,1)))

        btn=Button(text="OK",size_hint=(1,None),height=40)

        popup=Popup(
            title="Pemberitahuan",
            content=box,
            size_hint=(None,None),
            size=(350,200),
            auto_dismiss=False
        )

        btn.bind(on_press=popup.dismiss)

        box.add_widget(btn)

        popup.open()

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

# ================= HOME =================

    def home(self):

        self.clear()

        self.main.add_widget(Label(text="SISTEM PANEN AYAM",font_size=36, color=(0,0,0,1)))
        self.main.add_widget(Label(text="BERKAH ENJE 1221",font_size=24, color=(0,0,0,1)))

# ================= FORM DO =================

    def form_do(self,instance):

        self.clear()

        labels=[
        "Nama DO",
        "No Kendaraan",
        "Nama Supir",
        "Tanggal",
        "Jam",
        "Target Ekor",
        "Target Kg"
        ]

        self.entry={}
        self.fields=[]

        grid=GridLayout(cols=2,padding=30,spacing=15,size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        for l in labels:

            lbl=Label(text=l,size_hint_y=None,height=40,font_size=16,halign="left", color=(0,0,0,1))
            lbl.bind(size=lbl.setter('text_size'))

            e=TextInput(
                multiline=False,
                size_hint_y=None,
                height=40,
                foreground_color=(0,0,0,1),
                background_color=(1,1,1,1)
            )

            e.bind(on_text_validate=self.next_field)

            if l=="Tanggal":
                e.text=datetime.now().strftime("%Y-%m-%d")

            if l=="Jam":
                e.text=datetime.now().strftime("%H:%M")

            grid.add_widget(lbl)
            grid.add_widget(e)

            self.entry[l]=e
            self.fields.append(e)

        scroll=ScrollView()
        scroll.add_widget(grid)

        self.main.add_widget(scroll)

        btn=Button(text="Input Riwayat Panen",size_hint=(1,None),height=55)
        btn.bind(on_press=self.validasi_do)

        self.main.add_widget(btn)

# ================= PINDAH FIELD =================

    def next_field(self,instance):

        if instance in self.fields:
            i=self.fields.index(instance)

            if i < len(self.fields)-1:
                self.fields[i+1].focus=True
            else:
                self.validasi_do(None)

# ================= VALIDASI =================

    def validasi_do(self,instance):

        for key,val in self.entry.items():

            if val.text.strip()=="":
                self.show_popup(f"{key} belum diisi")
                return

        self.buka_riwayat()

# ================= FORMAT KG =================

    def format_kg(self,nilai):

        nilai=round(nilai,4)

        if nilai.is_integer():
            return int(nilai)

        return nilai

# ================= PREVIEW SISA =================

    def preview_sisa(self,instance,value):

        try:
            e=int(self.ekor.text) if self.ekor.text else 0
            k=float(self.kg.text) if self.kg.text else 0
        except:
            return

        preview_ekor=self.realisasi_ekor + e
        preview_kg=self.realisasi_kg + k

        sisa_ekor=self.target_ekor - preview_ekor
        sisa_kg=self.target_kg - preview_kg

        self.lbl_sisa.text=f"Sisa : {sisa_ekor} Ekor | {self.format_kg(sisa_kg)} Kg"

# ================= RIWAYAT PANEN =================

    def buka_riwayat(self):

        self.clear()

        self.target_ekor=int(self.entry["Target Ekor"].text)
        self.target_kg=float(self.entry["Target Kg"].text)

        self.realisasi_ekor=0
        self.realisasi_kg=0

        self.data_count=0
        self.batch_size=30

        self.batch_ekor=0
        self.batch_kg=0

        info=Label(
            text=f"DO : {self.entry['Nama DO'].text} | Supir : {self.entry['Nama Supir'].text}",
            size_hint=(1,None),
            height=40,
            font_size=16,
            color=(0,0,0,1)
        )

        self.main.add_widget(info)

# ================= INPUT =================

        input_box=BoxLayout(size_hint=(1,None),height=50,spacing=10)

        self.ekor=TextInput(
            hint_text="Ekor",
            multiline=False,
            foreground_color=(0,0,0,1),
            background_color=(1,1,1,1)
        )

        self.kg=TextInput(
            hint_text="Kg",
            multiline=False,
            foreground_color=(0,0,0,1),
            background_color=(1,1,1,1)
        )

        self.ekor.bind(on_text_validate=self.fokus_kg)
        self.kg.bind(on_text_validate=self.enter_tambah)

        self.ekor.bind(text=self.preview_sisa)
        self.kg.bind(text=self.preview_sisa)

        btn=Button(text="Tambah")
        btn.bind(on_press=self.tambah_input)

        input_box.add_widget(self.ekor)
        input_box.add_widget(self.kg)
        input_box.add_widget(btn)

        self.main.add_widget(input_box)

# ================= STATUS =================

        status_box = BoxLayout(
            orientation="horizontal",
            size_hint=(1,None),
            height=40,
            spacing=30
        )

        self.lbl_realisasi=Label(
            text="Realisasi : 0 Ekor | 0 Kg",
            font_size=16,
            size_hint=(None,1),
            width=300,
            color=(0,0,0,1)
        )

        self.lbl_sisa=Label(
            text=f"Sisa : {self.target_ekor} Ekor | {self.target_kg} Kg",
            font_size=16,
            size_hint=(None,1),
            width=300,
            color=(0,0,0,1)
        )

        status_box.add_widget(self.lbl_sisa)
        status_box.add_widget(self.lbl_realisasi)

        self.main.add_widget(status_box)

# ================= CONTAINER BATCH =================

        self.scroll=ScrollView(size_hint=(1,1), do_scroll_x=True, do_scroll_y=True)

        self.batch_container=BoxLayout(
            orientation="horizontal",
            spacing=30,
            size_hint=(None,None),
            padding=(0,0,0,0)
        )

        self.batch_container.bind(minimum_height=self.batch_container.setter('height'))
        self.batch_container.bind(minimum_width=self.batch_container.setter('width'))

        self.scroll.add_widget(self.batch_container)

        self.main.add_widget(self.scroll)

        self.new_batch_table()

        selesai=Button(text="Selesai",size_hint=(1,None),height=55)
        selesai.bind(on_press=self.selesai_input)

        self.main.add_widget(selesai)

# ================= TABEL =================

    def new_batch_table(self):

        self.table = GridLayout(
            cols=3,
            spacing=5,
            padding=10,
            size_hint=(None, None),
            width=250
        )

        self.table.bind(minimum_height=self.table.setter('height'))

        self.table.add_widget(Label(text="No", size_hint_y=None, height=35, color=(0,0,0,1)))
        self.table.add_widget(Label(text="Ekor", size_hint_y=None, height=35, color=(0,0,0,1)))
        self.table.add_widget(Label(text="Kg", size_hint_y=None, height=35, color=(0,0,0,1)))

        self.total_label = Label(text="TOTAL", size_hint_y=None, height=35, color=(0,0,0,1))
        self.total_ekor_label = Label(text="0", size_hint_y=None, height=35, color=(0,0,0,1))
        self.total_kg_label = Label(text="0", size_hint_y=None, height=35, color=(0,0,0,1))

        self.batch_container.add_widget(self.table)

# ================= INPUT DATA =================

    def tambah_input(self,instance):

        if self.ekor.text=="" or self.kg.text=="":
            self.show_popup("Ekor dan Kg harus diisi")
            return

        try:
            e=int(self.ekor.text)
            k=float(self.kg.text)
        except:
            self.show_popup("Format angka tidak valid")
            return

        sisa_ekor=self.target_ekor-self.realisasi_ekor
        sisa_kg=self.target_kg-self.realisasi_kg

        if e > sisa_ekor:
            self.show_popup("Ekor melebihi sisa target")
            return

        if k > sisa_kg:
            self.show_popup("Kg melebihi sisa target")
            return

        self.data_count+=1

        self.realisasi_ekor+=e
        self.realisasi_kg+=k

        self.batch_ekor+=e
        self.batch_kg+=k

        self.table.add_widget(Label(text=str(self.data_count), size_hint_y=None, height=35, color=(0,0,0,1)))
        self.table.add_widget(Label(text=str(e), size_hint_y=None, height=35, color=(0,0,0,1)))
        self.table.add_widget(Label(text=str(self.format_kg(k)), size_hint_y=None, height=35, color=(0,0,0,1)))

        if self.total_label.parent:
            self.table.remove_widget(self.total_label)
            self.table.remove_widget(self.total_ekor_label)
            self.table.remove_widget(self.total_kg_label)

        self.total_label.text="TOTAL"
        self.total_ekor_label.text=str(self.batch_ekor)
        self.total_kg_label.text=str(self.format_kg(self.batch_kg))

        self.table.add_widget(self.total_label)
        self.table.add_widget(self.total_ekor_label)
        self.table.add_widget(self.total_kg_label)

        if self.data_count % self.batch_size == 0:

            self.batch_ekor=0
            self.batch_kg=0

            self.new_batch_table()

        self.lbl_realisasi.text=f"Realisasi : {self.realisasi_ekor} Ekor | {self.format_kg(self.realisasi_kg)} Kg"

        self.lbl_sisa.text=f"Sisa : {self.target_ekor-self.realisasi_ekor} Ekor | {self.format_kg(self.target_kg-self.realisasi_kg)} Kg"

        self.ekor.text=""
        self.kg.text=""

        self.ekor.focus=True

# ================= ENTER =================

    def fokus_kg(self,instance):
        self.kg.focus=True

    def enter_tambah(self,instance):
        self.tambah_input(None)

# ================= SELESAI =================

    def selesai_input(self,instance):
        self.home()


class PanenApp(App):

    def build(self):
        return PanenLayout()


PanenApp().run()