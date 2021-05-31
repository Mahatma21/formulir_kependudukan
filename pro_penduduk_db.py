import mysql.connector
from tkinter import *
from tkinter.messagebox import showerror, showinfo
from tkinter import ttk
from datetime import datetime

FONT = "Montserrat"
LOGO = "/run/media/mahatma/F8C6C68BC6C64A18/Users/User/Documents/Python/Belajar_Python/logo_py.ico"
JENIS_KELAMIN_OP = ('laki-laki', 'perempuan')
TEMPAT_TANGGAL_LAHIR_KETERANGAN = "Tempat, hh-bb-tttt"
ALAMAT_KETERANGAN = "Jl. Xxxx, No. xx"
JENIS_KELAMIN_KETERANGAN = "Pilih disini"
FORMAT_JALAN = ("Jl.", "Jl", "Jalan")
FORMAT_NO_RUMAH = "no"


def font(ukuran: int, bold=False) -> tuple:
    # Mengembalikan font bold jika bold=True
    if bold:
        return (FONT + " Bold", ukuran)
    return (FONT, ukuran)


def show_info_menu():
    showinfo("Information", "Creator: @mahatma_19")


def balik_tanggal_waktu(waktu: datetime, isi_waktu=False) -> str:
    if isi_waktu:
        # Memisahkan tanggal dengan waktu
        temp_tanggal_waktu = str(waktu).split()
        # Membalik tanggal
        temp_tanggal = temp_tanggal_waktu[0].split('-')
        temp_tanggal.reverse()
        # Membalik waktu
        temp_waktu = temp_tanggal_waktu[1].split(':')
        temp_waktu.reverse()
        # Menggabungkan tanggal dengan waktu yang sudah dibalik
        hasil = f"{'-'.join(temp_tanggal)} {':'.join(temp_waktu)}"
    else:
        # Membalik tanggal
        temp_tanggal = str(waktu).split('-')
        temp_tanggal.reverse()
        # Menggabungkan tanggal yang sudah dibalik
        hasil = '-'.join(temp_tanggal)
    # Mengembalikan tanggal (dan waktu) yang sudah dibalik
    return hasil


# Mengembalikan True jika ada kesalahan
def cek_batas(value: str) -> bool:
        # Memastikan value nama diantara 1 sampai 255 character
        if len(value) > 255:
            return True
        return False


def cek_kosong(values: str) -> bool:
    if not values.replace(' ', ''):
        return True
    return False


def cek_data(
        nama: str, tempat_tanggal_lahir: str, jenis_kelamin: str, alamat: str,
        kelurahan: str, kecamatan: str, kabupaten: str, provinsi: str,
        pekerjaan: str) -> tuple:
    global ada_error

    # Menyiapkan variabel ada_error
    ada_error = False

    # Asigning nama value
    temp_nama = nama.strip().title()
    try:
        # Memastikan value nama tidak kosong
        if cek_kosong(temp_nama):
            print('nama error: kolom nama kosong')
            raise Exception("Mohon isi kolom nama !")
        # Memastikan value nama tidak melebihi batas db
        if cek_batas(temp_nama):
            print('nama error: value nama melebihi batas db')
            raise Exception("Nama anda terlalu panjang !")
        # Memastikan tidak ada angka pada value nama
        nama_isi_angka = False
        for i in temp_nama:
            try:
                int(i)
                showerror(
                    "nama error",
                    "Mohon tidak mengisi angka pada kolom nama !")
                nama_isi_angka = True
                break
            except:
                pass
        if nama_isi_angka:
            print('nama error: value nama berisi angka')
            raise Exception("Mohon tidak mengisi angka pada kolom nama !")
        # Menentukan value nama jika tidak ada error
        nama_value = temp_nama

    except Exception as err:
        ada_error = True
        showerror('nama error', err)

    # Mengecek value tempat tanggal lahir
    try:
        temp_tempat_tanggal_lahir = tempat_tanggal_lahir.strip()
        # Memastikan value tempat tanggal lahir telah diisi
        if (cek_kosong(temp_tempat_tanggal_lahir)
                or temp_tempat_tanggal_lahir == TEMPAT_TANGGAL_LAHIR_KETERANGAN):
            print("tempat tanggal lahir error: kolom tempat tanggal lhair tidak diisi")
            raise Exception("Mohon isi kolom tempat tanggal lahir !")

        # Membagi tempat lahir dan tanggal lahir
        temp_tempat_tanggal_lahir = temp_tempat_tanggal_lahir.split()
        # Memastikan value tempat lahir tidak melebihi batas db
        if cek_batas(temp_tempat_tanggal_lahir[0]):
            print('tempat lahir error: value tempat lahir melebihi batas db')
            raise Exception("tempat lahir anda terlalu panjang !")

        # Mengambil data tanggal lahir
        temp_tanggal_lahir = temp_tempat_tanggal_lahir[1].split('-')
        # Mengecek format tempat tanggal lahir
        if (len(temp_tempat_tanggal_lahir) != 2
                or len(temp_tanggal_lahir) != 3
                or len(temp_tanggal_lahir[0]) != 2
                or len(temp_tanggal_lahir[1]) != 2
                or len(temp_tanggal_lahir[2]) != 4):
            print('tempat tanggal lahir error: format tempat tanggal lahir salah')
            raise Exception(
                'Mohon isi tempat tanggal lahir sesuai format yang dicontohkan !')
        # Menghapus angka 0 di depan 'bulan' jika ada
        temp_tanggal_lahir = [i.removeprefix('0') for i in temp_tanggal_lahir]
        # Memastikan tidak ada huruf pada tanggal lahir
        try:
            # Convert list of string into list of integer
            temp_tanggal_lahir = [int(i) for i in temp_tanggal_lahir]
        except:
            print('tempat tanggal lahir error: ada huruf di tanggal lahir')
            raise Exception("Mohon tidak mengisi huruf pada tanggal lahir !")

        # Membalik urutan tanggal lahir
        temp_tanggal_lahir.reverse()
        # Memastikan tanggal lahir benar
        try:
            # Convert into datetime object
            temp_tanggal_lahir = datetime(*temp_tanggal_lahir)
            # Menghapus time pada temp_tanggal_lahir
            temp_tanggal_lahir = datetime.date(temp_tanggal_lahir)
        except:
            raise Exception('tanggal lahir salah')

        # Memastikan tanggal lahir sebelum tanggal sekarang
        tanggal_sekarang = datetime.date(datetime.now())
        if temp_tanggal_lahir >= tanggal_sekarang:
            print(
                "tempat tanggal lahir error: tanggal lahir terlalu muda")
            raise Exception("Mohon isi tanggal lahir dengan benar !")

        # Mengambil data tempat lahir
        tempat_lahir_value = temp_tempat_tanggal_lahir[0].replace(
            ',', '').title()
        # Menentukan value tanggal lahir
        tanggal_lahir_value = temp_tanggal_lahir
    except Exception as err:
        showerror(
            'tempat tanggal lahir error', err)
        ada_error = True

    # Asigning value jenis kelamin
    jenis_kelamin_value = jenis_kelamin.strip().lower()
    # Mengecek jenis kelamin
    if jenis_kelamin_value not in JENIS_KELAMIN_OP:
        showerror(
            'jenis kelamin error',
            "Mohon pilih jenis kelamin yang disediakan !")
        print('jenis kelamin error: jenis kelamin yang dipilih tidak ada')
        ada_error = True

    # Asigning value alamat
    alamat_value = alamat.strip().title()
    # Mengecek alamat
    temp_alamat = alamat_value.split()
    try:
        if alamat_value.lower() == ALAMAT_KETERANGAN.lower():
            print('alamat error: kolom alamat tidak diisi')
            raise Exception("Mohon isi kolom alamat !")
        elif (len(temp_alamat) < 4
                or temp_alamat[0] not in FORMAT_JALAN
                or FORMAT_NO_RUMAH not in alamat_value.lower()):
            print('alamat error: format alamat salah')
            raise Exception(
                "Mohon isi alamat sesuai format yang dicontohkan !")
    except Exception as err:
        ada_error = True
        showerror('alamat error', err)

    # Asigning value kelurahan
    kelurahan_value = kelurahan.strip().title()
    try:
        # Memastikan value kelurahan tidak kosong
        if cek_kosong(kelurahan_value):
            print("kelurahan error: kolom kelurahan tidak diisi")
            raise Exception("Mohon isi kolom kelurahan !")
        # Memastikan value kelurahan tidak melebihi batas db
        if cek_batas(kelurahan_value):
            print('kelurahan error: value kelurahan melebihi batas db')
            raise Exception("kelurahan anda terlalu panjang !")
        # Mengecek value kelurahan agar tidak hanya berisi angka
        try:
            int(kelurahan_value)
            print("kelurahan error: value kelurahan hanya berisi angka")
            raise Exception("Mohon isi kolom kelurahan dengan benar !")
        except:
            pass
    except Exception as err:
        showerror("Kelurahan error", err)

    # Asigning value kecamatan
    kecamatan_value = kecamatan.strip().title()
    try:
        # Memastikan value kecamatan tidak kosong
        if cek_kosong(kecamatan_value):
            print("kecamatan error: kolom kecamatan tidak diisi")
            raise Exception("Mohon isi kolom kecamatan !")
        # Memastikan value kecamatan tidak melebihi batas db
        if cek_batas(kecamatan_value):
            print('kecamatan error: value kecamatan melebihi batas db')
            raise Exception("kecamatan anda terlalu panjang !")
        # Mengecek value kecamatan agar tidak hanya berisi angka
        try:
            int(kecamatan_value)
            print("kecamatan error: value kecamatan hanya berisi angka")
            raise Exception("Mohon isi kolom kecamatan dengan benar !")
        except:
            pass
    except Exception as err:
        showerror("Kecamatan error", err)

    # Asigning value kabupaten
    kabupaten_value = kabupaten.strip().title()
    try:
        # Memastikan value kabupaten tidak kosong
        if cek_kosong(kabupaten_value):
            print("kabupaten error: kolom kabupaten tidak diisi")
            raise Exception("Mohon isi kolom kabupaten !")
        # Memastikan value kabupaten tidak melebihi batas db
        if cek_batas(kabupaten_value):
            print('kabupaten error: value kabupaten melebihi batas db')
            raise Exception("Kabupaten anda terlalu panjang !")
        # Mengecek value kabupaten agar tidak hanya berisi angka
        try:
            int(kabupaten_value)
            print("kabupaten error: value kabupaten hanya berisi angka")
            raise Exception("Mohon isi kolom kabupaten dengan benar !")
        except:
            pass
    except Exception as err:
        showerror("Kabupaten error", err)

    # Asigning value provinsi
    provinsi_value = provinsi.strip().title()
    try:
        # Memastikan value provinsi tidak kosong
        if cek_kosong(provinsi_value):
            print("provinsi error: kolom provinsi tidak diisi")
            raise Exception("Mohon isi kolom provinsi !")
        # Memastikan value provinsi tidak melebihi batas db
        if cek_batas(provinsi_value):
            print('provinsi error: value provinsi melebihi batas db')
            raise Exception("Provinsi anda terlalu panjang !")
        # Mengecek value provinsi agar tidak hanya berisi angka
        try:
            int(provinsi_value)
            print("provinsi error: value provinsi hanya berisi angka")
            raise Exception("Mohon isi kolom provinsi dengan benar !")
        except:
            pass
    except Exception as err:
        showerror("Provinsi error", err)

    # Asigning value pekerjaan
    pekerjaan_value = pekerjaan.strip()
    # Memastikan value pekerjaan tidak melebihi batas db
    try:
        if cek_batas(pekerjaan_value):
            print("pekerjaan error: value pekerjaan melebihi batas db")
            raise Exception("Pekerjaan anda terlalu panjang !")
    except Exception as err:
        showerror("Pekerjaan error", err)

    if ada_error:  # Mengembalikan True jika ada error
        return ada_error
    else:  # Mengembalikan data yang sudah dicek jika tidak ada error
        return (
            nama_value, tempat_lahir_value, tanggal_lahir_value,
            jenis_kelamin_value,
            alamat_value, kelurahan_value, kecamatan_value,
            kabupaten_value, provinsi_value, pekerjaan_value
        )


def hapus_kolom():
    # Menghapus isi kolom
    nama_entry.delete(0, END)
    tempat_tanggal_lahir_entry.delete(0, END)
    alamat_entry.delete(0, END)
    kelurahan_entry.delete(0, END)
    kecamatan_entry.delete(0, END)
    kabupaten_entry.delete(0, END)
    provinsi_entry.delete(0, END)
    pekerjaan_entry.delete(0, END)

    # Mengisi kolom dengan keterangan
    tempat_tanggal_lahir_entry.insert(0, TEMPAT_TANGGAL_LAHIR_KETERANGAN)
    jenis_kelamin_combo.set(JENIS_KELAMIN_KETERANGAN)
    alamat_entry.insert(0, ALAMAT_KETERANGAN)


def tempel_data(letak_tempel, values):
    # Meletakan data pada frame
    font_bold = True  # Menyesuaikan font untuk keterangan
    for temp_row, i in enumerate(values):
        for temp_column, j in enumerate(i):
            if font_bold:
                temp_label = Label(letak_tempel, text=j, font=font(11, True))
            elif temp_column == 0:
                temp_label = Label(letak_tempel, text=f"{j:02}")
            else:
                temp_label = Label(letak_tempel, text=j, font=font(10))

            # Memeberi jarak ke dalam tapi tidak keluar
            # Jarak keluar sudah ada dari frame
            if temp_column == 0:
                temp_padx = (0, 5)
            elif temp_column == 11:
                temp_padx = (5, 0)
            else:
                temp_padx = 5

            # Sticking
            if temp_column in (0, 11):
                temp_sticky = E
            else:
                temp_sticky = W

            # Data Grid
            temp_label.grid(
                row=temp_row, column=temp_column, padx=temp_padx,
                pady=5, sticky=temp_sticky)
        # Agar hanya font keterangan yang disesuaikan
        font_bold = False


def ubah_halaman(halaman: str):
    global frm_lihat, curr_halaman, selanjutnya_button
    global sebelumnya_button

    # command untuk mengambil data dengan limit
    sql_command = "SELECT * FROM penduduk ORDER BY %s %s LIMIT %s, 15"

    # Mengambil jumlah records
    curs.execute("SELECT COUNT(*) FROM penduduk")
    jumlah_records = int(curs.fetchone()[0])

    # Menentukan limit
    if halaman == 'sebelumnya':
        curr_halaman -= 15
    elif halaman == 'selanjutnya':
        curr_halaman += 15

    # Mematikan/menghidupkan button
    if curr_halaman <= 0:
        sebelumnya_button['state'] = DISABLED
    else:
        sebelumnya_button['state'] = ACTIVE

    if jumlah_records - curr_halaman <= 15:
        selanjutnya_button['state'] = DISABLED
    else:
        selanjutnya_button['state'] = ACTIVE

    # Menentukan values command
    values_command = tuple(list(ubah_urutan_values_command) + [curr_halaman])

    # Mengeksekusi command untuk mengambil data selanjutnya
    curs.execute(sql_command % values_command)
    # Menambahkan keterangan
    values = list(curs.fetchall())

    # Membalik format tanggal lahir dan tanggl dibuat
    for i in range(len(values)):
        # Membalik tanggal lahir
        tanggal_lahir = balik_tanggal_waktu(values[i][3])
        # Membalik tanggal dibuat
        tanggal_dibuat = balik_tanggal_waktu(values[i][-1], True)
        # Convert ke list
        values[i] = list(values[i])
        # Mengubah value tanggal lahir
        values[i][3] = tanggal_lahir
        # Mengubah value tanggal tanggal dibuat
        values[i][-1] = tanggal_dibuat
        # Convert ke tuple kembali
        values[i] = tuple(values[i])

    # Menghapus widget oada frame sebelumnya
    for i in frm_lihat.winfo_children():
        i.destroy()

    # Memunculkan data ke frame
    tempel_data(frm_lihat, values)


def ubah_urutan(*event):
    global frm_lihat, ubah_urutan_values_command, selanjutnya_button
    global sebelumnya_button, curr_halaman

    # Untuk ubah_halaman function
    curr_halaman = 0

    # Mengambil jumalh records
    curs.execute("SELECT COUNT(*) FROM penduduk")
    jumlah_records = curs.fetchone()[0]

    # Mematikan tombol 'sebelumnya' karena kembali ke halaman pertama
    sebelumnya_button['state'] = DISABLED
    # Mematikan tombol 'selanjutanya' jika tidak ada record didepan
    if jumlah_records - curr_halaman <= 15:
        selanjutnya_button['state'] = DISABLED
    else:
        selanjutnya_button['state'] = ACTIVE

    # Command untuk mengambil data
    sql_command = "SELECT * FROM penduduk ORDER BY %s %s LIMIT 15"
    # Temp
    temp_data_urutan = data_urutan_combo.get()
    temp_jenis_urutan = jenis_urutan_combo.get()
    # Menentukan data urutan
    if temp_data_urutan == data_urutan_op[0]:
        data_urutan = 'id'
    elif temp_data_urutan == data_urutan_op[1]:
        data_urutan = 'nama'
    elif temp_data_urutan == data_urutan_op[2]:
        data_urutan = 'tempat_lahir'
    elif temp_data_urutan == data_urutan_op[3]:
        data_urutan = 'tanggal_lahir'
    elif temp_data_urutan == data_urutan_op[4]:
        data_urutan = 'jenis_kelamin'
    elif temp_data_urutan == data_urutan_op[5]:
        data_urutan = 'alamat'
    elif temp_data_urutan == data_urutan_op[6]:
        data_urutan = 'kelurahan'
    elif temp_data_urutan == data_urutan_op[7]:
        data_urutan = 'kecamatan'
    elif temp_data_urutan == data_urutan_op[8]:
        data_urutan = 'kabupaten'
    elif temp_data_urutan == data_urutan_op[9]:
        data_urutan = 'provinsi'
    elif temp_data_urutan == data_urutan_op[10]:
        data_urutan = 'pekerjaan'
    elif temp_data_urutan == data_urutan_op[11]:
        data_urutan = 'tanggal_dibuat'
    else:
        print("Data urutan tidak ditemukan !")
    # Menentukan jenis urutan
    if temp_jenis_urutan == jenis_urutan_op[0]:
        jenis_urutan = "ASC"
    elif temp_jenis_urutan == jenis_urutan_op[1]:
        jenis_urutan = "DESC"
    else:
        print("Jenis urutan tidak ditemukan !")

    # Menyatukan urutan
    ubah_urutan_values_command = (data_urutan, jenis_urutan)

    # Executing command untuk mengambil data dari db
    curs.execute(sql_command % ubah_urutan_values_command)
    # Asigning values into variable
    values = list(curs.fetchall())

    # Membalik format tanggal lahir dan tanggl dibuat
    for i in range(len(values)):
        # Membalik tanggal lahir
        tanggal_lahir = balik_tanggal_waktu(values[i][3])
        # Membalik tanggal dibuat
        tanggal_dibuat = balik_tanggal_waktu(values[i][-1], True)
        # Convert ke list
        values[i] = list(values[i])
        # Mengubah value tanggal lahir
        values[i][3] = tanggal_lahir
        # Mengubah value tanggal tanggal dibuat
        values[i][-1] = tanggal_dibuat
        # Convert ke tuple kembali
        values[i] = tuple(values[i])

    # Menambahkan keterangan pada values
    values.insert(0, data_urutan_op)
    # Convert ke tuple
    values = tuple(values)

    # Menghapus widget oada frame sebelumnya
    for i in frm_lihat.winfo_children():
        i.destroy()

    # Meletakan data pada frame
    tempel_data(frm_lihat, values)


def lihat_data():
    # Untuk ubah_urutan function
    global data_urutan_combo, jenis_urutan_combo, data_urutan_op
    global jenis_urutan_op, win_lihat, frm_lihat, curr_halaman
    global sebelumnya_button, selanjutnya_button

    # Membuat window baru
    win_lihat = Tk()
    win_lihat.geometry('1450x750')
    win_lihat.title("Jendela Lihat Data")
    # win_lihat.iconbitmap(LOGO)

    # Label Widget
    judul_label = Label(
        win_lihat, text="Data Penduduk 2021", font=font(20, True))
    penjelasan_label = Label(
        win_lihat, text="Urut berdasarkan:", font=font(14, True))
    # Label Widget Griding
    judul_label.grid(row=0, column=0, columnspan=3, pady=(20, 10))
    penjelasan_label.grid(row=1, column=0, padx=(20, 10), pady=10, sticky=E)

    # Pilihan Op
    data_urutan_op = (
        "ID", "Nama", "Tempat Lahir", "Tanggal Lahir", "Jenis Kelamin",
        "Alamat", "Kelurahan", "Kecamatan", "Kabupaten", "Provinsi",
        "Pekerjaan", "Tanggal Dibuat")
    jenis_urutan_op = ("Ascending", "Descending")
    # Pilihan Widget
    data_urutan_combo = ttk.Combobox(
        win_lihat, values=data_urutan_op, font=font(12, True))
    jenis_urutan_combo = ttk.Combobox(
        win_lihat, values=jenis_urutan_op, font=font(12, True))
    # Pilihan Set
    data_urutan_combo.set(data_urutan_op[0])
    jenis_urutan_combo.set(jenis_urutan_op[0])
    # Command if combobox selected
    data_urutan_combo.bind("<<ComboboxSelected>>", ubah_urutan)
    jenis_urutan_combo.bind("<<ComboboxSelected>>", ubah_urutan)
    # Pilihan Widget Griding
    data_urutan_combo.grid(row=1, column=1, padx=10, pady=10)
    jenis_urutan_combo.grid(row=1, column=2, padx=(10, 20), pady=10, sticky=W)

    # Membuat frame untuk data yang dilihat
    frm_lihat = Frame(win_lihat)
    # Frame griding
    frm_lihat.grid(row=2, column=0, columnspan=3, padx=20, pady=(10))

    # Button Widget
    sebelumnya_button = Button(
        win_lihat, text="<<", command=lambda: ubah_halaman('sebelumnya'),
        state=DISABLED, font=font(14, True))
    selanjutnya_button = Button(
        win_lihat, text=">>", command=lambda: ubah_halaman('selanjutnya'),
        font=font(14, True))
    # Button Widget Griding
    sebelumnya_button.grid(row=3, column=0, padx=20,
                           ipadx=20, pady=(10, 20), sticky=W)
    selanjutnya_button.grid(row=3, column=2, padx=20,
                            pady=(10, 20), ipadx=20, sticky=E)

    # Memunculkan data untuk pertama kali
    ubah_urutan()


def kirim_data(
    nama, tempat_tanggal_lahir, jenis_kelamin, alamat, kelurahan,
        kecamatan, kabupaten, provinsi, pekerjaan):
    # Command to execute for create new record
    sql_command = """INSERT INTO penduduk (
        nama, tempat_lahir, tanggal_lahir, jenis_kelamin, alamat,
        kelurahan, kecamatan, kabupaten, provinsi, pekerjaan)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
    # Checking values for the command
    values = cek_data(
        nama, tempat_tanggal_lahir, jenis_kelamin, alamat, kelurahan,
        kecamatan, kabupaten, provinsi, pekerjaan)

    # Mengirim data jika tidak ada error saat dicek
    if ada_error == True:
        print("ada error saat cek data")
    else:
        # Executing command untuk menambah record
        curs.execute(sql_command, values)
        # Commit perubahan
        conn.commit()

        # Menghapus isi kolom
        hapus_kolom()

        # Menyampaikan bahwa data berhasil dikirim
        showinfo('Kirim Data', "Data berhasil dikirim")


def hapus_data(input_id):
    # Command to execute
    sql_command = "DELETE FROM penduduk WHERE id=%s"
    # Value for the command
    value = (input_id,)

    # Executing command
    curs.execute(sql_command, value)
    # Commiting the changes
    conn.commit()

    # Menutup ubah_win
    ubah_win.destroy()

    # Menyampaikan bahwa data telah dihapus
    showinfo('Hapus Data', "Data telah dihapus")


def ubah_data(
        input_id, nama, tempat_tanggal_lahir, jenis_kelamin, alamat, kelurahan,
        kecamatan, kabupaten, provinsi, pekerjaan):
    # Command to execute for update the record
    sql_command = """UPDATE penduduk
        SET nama=%s,
            tempat_lahir=%s,
            tanggal_lahir=%s,
            jenis_kelamin=%s,
            alamat=%s,
            kelurahan=%s,
            kecamatan=%s,
            kabupaten=%s,
            provinsi=%s,
            pekerjaan=%s
        WHERE id=%s
        """
    # Checking values for the command
    values = cek_data(
        nama, tempat_tanggal_lahir, jenis_kelamin, alamat, kelurahan,
        kecamatan, kabupaten, provinsi, pekerjaan)

    # Mengubah data jika tidak ada error saat pengecekan
    if values == True:
        print("ada error saat cek data")
    else:
        # Convert values ke list
        values = list(values)
        # Menambahakan id untuk where clause
        values.append(input_id)

        # Executing command
        curs.execute(sql_command, values)
        # Commiting the changes
        conn.commit()

        # Menutup jendela ubah data
        ubah_win.destroy()
        # Memberitahu bahwa data berhasil diubah
        showinfo('Ubah Data', "Data berhasil diubah")


def ubah_data_window(input_id):
    global ubah_win, ubah_id

    # Memastikan value id adalah angka
    try:
        # mengambil id yang diinput
        ubah_id = str(input_id).strip()
        # Mengahapus angka 0 di depan
        [ubah_id.removeprefix('0') for _ in ubah_id]

        # Mengambil data dari db berdasarkan id
        curs.execute("SELECT * FROM penduduk WHERE id=%s", (ubah_id,))
        ubah_values = curs.fetchone()
        # Memastikan data yang didapat tidak kosong
        if ubah_values == None:
            raise Exception('ID tidak ditemukan !')
        # Convert ke list
        ubah_values = list(ubah_values)

        # Mengambil data tempat dan tanggal lahir
        temp_tempat_lahir = ubah_values.pop(2)
        temp_tanggal_lahir = ubah_values.pop(2)
        # Membalik urutan tanggal_lahir
        temp_tanggal_lahir = balik_tanggal_waktu(temp_tanggal_lahir)
        # Memasukan data tempat lahir dan tanggal lahir yang sudah dibalik
        ubah_values.insert(2, f"{temp_tempat_lahir}, {temp_tanggal_lahir}")

        # Mengambil data tanggal dibuat
        temp_tanggal_dibuat = ubah_values.pop(-1)
        # Membalik urutan tanggal dibuat
        temp_tanggal_dibuat = balik_tanggal_waktu(temp_tanggal_dibuat, True)
        # Memasukan data tanggal dibuat yang sudah dibalik
        ubah_values.append(temp_tanggal_dibuat)
        # Convert kembali ke tuple
        ubah_values = tuple(ubah_values)

        # Membuat window baru untuk mengubah data
        ubah_win = Tk()
        ubah_win.geometry('980x680')
        ubah_win.title("Jendela Ubah Data")
        # ubah_win.iconbitmap(LOGO)

        # Label Widget
        judul_label = Label(
            ubah_win, text="Ubah Data Penduduk 2021", font=font(24, True))
        penjelasan_label = Label(
            ubah_win, text="Ubah data yang ingin dirubah !", font=font(20))
        keterangan_id_label = Label(
            ubah_win, text="ID kependudukan", font=font(16, True))
        value_id_label = Label(
            ubah_win, text=f"{ubah_values[0]:02}", font=font(16, True))
        nama_label = Label(ubah_win, text="Nama", font=font(16))
        tempat_tanggal_lahir_label = Label(
            ubah_win, text="Tempat/tanggal lahir", font=font(16))
        jenis_kelamin_label = Label(
            ubah_win, text="Jenis kelamin", font=font(16))
        alamat_label = Label(ubah_win, text="Alamat", font=font(16))
        keluarahan_label = Label(ubah_win, text="Kelurahan", font=font(16))
        kecamatan_label = Label(ubah_win, text="Kecamatan", font=font(16))
        kabupaten_label = Label(ubah_win, text="Kabupaten", font=font(16))
        provinsi_label = Label(ubah_win, text="Provinsi", font=font(16))
        pekerjaan_label = Label(ubah_win, text="Pekerjaan", font=font(16))
        tanggal_dibuat_label = Label(
            ubah_win, text="Tanggal dibuat", font=font(16, True))
        value_tanggal_dibuat_label = Label(
            ubah_win, text=ubah_values[10], font=font(16, True))
        penjelasan_tanggal_dibuat_label = Label(
            ubah_win, text="(hh-bb-tttt dd:mm:jj)", font=font(16, True))

        # Label Widget Grid
        judul_label.grid(row=0, column=0, columnspan=4,
                         padx=273, pady=(20, 10))
        penjelasan_label.grid(row=1, column=0, columnspan=4,
                              padx=20, pady=(7, 5), sticky=W)
        keterangan_id_label.grid(row=2, column=0, padx=20, pady=5, sticky=W)
        value_id_label.grid(row=2, column=1, pady=5, sticky=W)
        nama_label.grid(row=3, column=0, padx=20, pady=5, sticky=W)
        tempat_tanggal_lahir_label.grid(
            row=4, column=0, padx=20, pady=5, sticky=W)
        jenis_kelamin_label.grid(row=5, column=0, padx=20, pady=5, sticky=W)
        alamat_label.grid(row=6, column=0, padx=20, pady=5, sticky=W)
        keluarahan_label.grid(row=7, column=0, padx=20, pady=5, sticky=W)
        kecamatan_label.grid(row=8, column=0, padx=20, pady=5, sticky=W)
        kabupaten_label.grid(row=9, column=0, padx=20, pady=5, sticky=W)
        provinsi_label.grid(row=10, column=0, padx=20, pady=5, sticky=W)
        pekerjaan_label.grid(row=11, column=0, padx=20, pady=5, sticky=W)
        tanggal_dibuat_label.grid(
            row=12, column=0, padx=20, pady=5, sticky=W)
        value_tanggal_dibuat_label.grid(
            row=12, column=1, columnspan=2, pady=5, sticky=W)
        penjelasan_tanggal_dibuat_label.grid(
            row=12, column=3, padx=(0, 20), pady=5, sticky=W)

        # Input Widget
        nama_entry = Entry(ubah_win, font=font(16))
        tempat_tanggal_lahir_entry = Entry(ubah_win, font=font(16))
        jenis_kelamin_combo = ttk.Combobox(
            ubah_win, values=JENIS_KELAMIN_OP, font=font(16))
        alamat_entry = Entry(ubah_win, font=font(16))
        kelurahan_entry = Entry(ubah_win, font=font(16))
        kecamatan_entry = Entry(ubah_win, font=font(16))
        kabupaten_entry = Entry(ubah_win, font=font(16))
        provinsi_entry = Entry(ubah_win, font=font(16))
        pekerjaan_entry = Entry(ubah_win, font=font(16))

        # Input Set
        nama_entry.insert(0, ubah_values[1])
        tempat_tanggal_lahir_entry.insert(0, ubah_values[2])
        jenis_kelamin_combo.set(ubah_values[3])
        alamat_entry.insert(0, ubah_values[4])
        kelurahan_entry.insert(0, ubah_values[5])
        kecamatan_entry.insert(0, ubah_values[6])
        kabupaten_entry.insert(0, ubah_values[7])
        provinsi_entry.insert(0, ubah_values[8])
        # Mengosongkan kolom pekerjaan jika pekerjaan tidak ada
        if ubah_values[9] != 'tidak bekerja':
            pekerjaan_entry.insert(0, ubah_values[9])

        # Input Widget Grid
        nama_entry.grid(row=3, column=1, columnspan=3,
                        padx=(0, 20), pady=5, sticky=W+E)
        tempat_tanggal_lahir_entry.grid(
            row=4, column=1, columnspan=3, padx=(0, 20), pady=5, sticky=W+E)
        jenis_kelamin_combo.grid(
            row=5, column=1, columnspan=3, padx=(0, 20), pady=5, sticky=W+E)
        alamat_entry.grid(row=6, column=1, columnspan=3,
                          padx=(0, 20), pady=5, sticky=W+E)
        kelurahan_entry.grid(row=7, column=1, columnspan=3,
                             padx=(0, 20), pady=5, sticky=W+E)
        kecamatan_entry.grid(row=8, column=1, columnspan=3,
                             padx=(0, 20), pady=5, sticky=W+E)
        kabupaten_entry.grid(row=9, column=1, columnspan=3,
                             padx=(0, 20), pady=5, sticky=W+E)
        provinsi_entry.grid(row=10, column=1, columnspan=3,
                            padx=(0, 20), pady=5, sticky=W+E)
        pekerjaan_entry.grid(row=11, column=1, columnspan=3,
                             padx=(0, 20), pady=5, sticky=W+E)

        # Button Widget
        hapus_data_button = Button(
            ubah_win, text="Hapus data", font=font(20),
            command=lambda: hapus_data(ubah_id))
        ubah_data_button = Button(
            ubah_win, text="Ubah data", font=font(20),
            command=lambda: ubah_data(
                ubah_id, nama_entry.get(),
                tempat_tanggal_lahir_entry.get(),
                jenis_kelamin_combo.get(),
                alamat_entry.get(),
                kelurahan_entry.get(),
                kecamatan_entry.get(),
                kabupaten_entry.get(),
                provinsi_entry.get(),
                pekerjaan_entry.get()))
        # Button Widget Grid
        hapus_data_button.grid(
            row=13, column=0, padx=20, pady=20, sticky=W+E)
        ubah_data_button.grid(
            row=13, column=1, columnspan=3, padx=(0, 20),
            ipadx=250, pady=20, sticky=W + E)
    except Exception as err:
        print('id error: id tidak ditemukan')
        showerror("ID error", err)


# Create connection
conn = mysql.connector.connect(
    host='192.168.1.100',
    user='mahatma',
    passwd='MySQL@MangHatmaa19',
    database='belajar_mysql')
# Create cursor
curs = conn.cursor()

# Create table
'''
curs.execute("""CREATE TABLE penduduk (
             id INT NOT NULL AUTO_INCREMENT,
             nama VARCHAR(255) NOT NULL,
             tempat_lahir VARCHAR(255) NOT NULL,
             tanggal_lahir DATE NOT NULL,
             jenis_kelamin ENUM('laki-laki', 'perempuan') NOT NULL,
             alamat VARCHAR(255) NOT NULL,
             kelurahan VARCHAR(255) NOT NULL,
             kecamatan VARCHAR(255) NOT NULL,
             kabupaten VARCHAR(255) NOT NULL,
             provinsi VARCHAR(255) NOT NULL,
             pekerjaan VARCHAR(255) NOT NULL DEFAULT 'tidak bekerja',
             tanggal_dibuat TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
             primary key (id)) ENGINE=InnoDB
             """)
'''

# Create main window
root = Tk()
root.geometry('1010x670')
root.title("Jendela Pendataan Penduduk")
# Create menu bar for root
main_menu_bar = Menu(root)
root.config(menu=main_menu_bar)
# insert menu bar for main_menu_bar
main_menu_bar.add_command(label="Info", command=show_info_menu)
# info_menu = Menu(main_menu_bar)
# main_menu_bar.add_cascade(label="Info", menu=info_menu, font=font(10))
# info_menu.add_command(label="Show Info", command=show_info_menu)
# info_menu.add_separator()
# info_menu.add_command(label="Show", command=show_info_menu)

# root.iconbitmap(LOGO)

# Label Widget
judul_label = Label(root, text="Pendataan Penduduk 2021", font=font(24, True))
penjelasan_label = Label(
    root, text="Mohon lengkapi data dengan benar !", font=font(20))
nama_label = Label(root, text="Nama", font=font(16))
tempat_tanggal_lahir_label = Label(
    root, text="Tempat/tanggal lahir", font=font(16))
jenis_kelamin_label = Label(root, text="Jenis kelamin", font=font(16))
alamat_label = Label(root, text="Alamat", font=font(16))
keluarahan_label = Label(root, text="Kelurahan", font=font(16))
kecamatan_label = Label(root, text="Kecamatan", font=font(16))
kabupaten_label = Label(root, text="Kabupaten", font=font(16))
provinsi_label = Label(root, text="Provinsi", font=font(16))
pekerjaan_label = Label(root, text="Pekerjaan", font=font(16))
id_label = Label(root, text="ID kependudukan", font=font(20))

# Label Widget Grid
judul_label.grid(row=0, column=0, columnspan=4, padx=282, pady=(20, 10))
penjelasan_label.grid(row=1, column=0, columnspan=4,
                      padx=20, pady=(7, 5), sticky=W)
nama_label.grid(row=2, column=0, padx=20, pady=5, sticky=W)
tempat_tanggal_lahir_label.grid(row=3, column=0, padx=20, pady=5, sticky=W)
jenis_kelamin_label.grid(row=4, column=0, padx=20, pady=5, sticky=W)
alamat_label.grid(row=5, column=0, padx=20, pady=5, sticky=W)
keluarahan_label.grid(row=6, column=0, padx=20, pady=5, sticky=W)
kecamatan_label.grid(row=7, column=0, padx=20, pady=5, sticky=W)
kabupaten_label.grid(row=8, column=0, padx=20, pady=5, sticky=W)
provinsi_label.grid(row=9, column=0, padx=20, pady=5, sticky=W)
pekerjaan_label.grid(row=10, column=0, padx=20, pady=5, sticky=W)
id_label.grid(row=12, column=0, padx=(20, 10), pady=(10, 20), sticky=W)

# Input Widget
nama_entry = Entry(root, font=font(16))
tempat_tanggal_lahir_entry = Entry(root, font=font(16))
jenis_kelamin_combo = ttk.Combobox(
    root, values=JENIS_KELAMIN_OP, font=font(16))
alamat_entry = Entry(root, font=font(16))
kelurahan_entry = Entry(root, font=font(16))
kecamatan_entry = Entry(root, font=font(16))
kabupaten_entry = Entry(root, font=font(16))
provinsi_entry = Entry(root, font=font(16))
pekerjaan_entry = Entry(root, font=font(16))
id_entry = Entry(root, font=font(24), width=2)

# Input Set
jenis_kelamin_combo.set(JENIS_KELAMIN_KETERANGAN)
tempat_tanggal_lahir_entry.insert(0, TEMPAT_TANGGAL_LAHIR_KETERANGAN)
alamat_entry.insert(0, ALAMAT_KETERANGAN)

# Input Widget Grid
nama_entry.grid(row=2, column=1, columnspan=3,
                padx=(0, 20), pady=5, sticky=W+E)
tempat_tanggal_lahir_entry.grid(
    row=3, column=1, columnspan=3, padx=(0, 20), pady=5, sticky=W+E)
jenis_kelamin_combo.grid(
    row=4, column=1, columnspan=3, padx=(0, 20), pady=5, sticky=W+E)
alamat_entry.grid(row=5, column=1, columnspan=3,
                  padx=(0, 20), pady=5, sticky=W+E)
kelurahan_entry.grid(row=6, column=1, columnspan=3,
                     padx=(0, 20), pady=5, sticky=W+E)
kecamatan_entry.grid(row=7, column=1, columnspan=3,
                     padx=(0, 20), pady=5, sticky=W+E)
kabupaten_entry.grid(row=8, column=1, columnspan=3,
                     padx=(0, 20), pady=5, sticky=W+E)
provinsi_entry.grid(row=9, column=1, columnspan=3,
                    padx=(0, 20), pady=5, sticky=W+E)
pekerjaan_entry.grid(row=10, column=1, columnspan=3,
                     padx=(0, 20), pady=5, sticky=W+E)
id_entry.grid(row=12, column=1, columnspan=2,
              padx=(0, 10), pady=(10, 20), sticky=W+E)

# Button Widget
hapus_kolom_button = Button(
    root, text="Hapus kolom", font=font(20),
    command=hapus_kolom)
lihat_data_button = Button(
    root, text="Lihat data", font=font(20),
    command=lihat_data)
kirim_data_button = Button(
    root, text="Kirim data", font=font(20),
    command=lambda: kirim_data(
        nama_entry.get(),
        tempat_tanggal_lahir_entry.get(),
        jenis_kelamin_combo.get(),
        alamat_entry.get(),
        kelurahan_entry.get(),
        kecamatan_entry.get(),
        kabupaten_entry.get(),
        provinsi_entry.get(),
        pekerjaan_entry.get()))
ubah_data_window_button = Button(
    root, text="Ubah data", font=font(20),
    command=lambda: ubah_data_window(id_entry.get()))

# Butotn Widget Grid
hapus_kolom_button.grid(row=11, column=0, padx=20,
                        ipadx=40, pady=(20, 10), sticky=W)
lihat_data_button.grid(row=11, column=1, ipadx=95, pady=(20, 10), sticky=W+E)
kirim_data_button.grid(row=11, column=2, columnspan=2,
                       padx=20, ipadx=60, pady=(20, 10), sticky=W+E)
ubah_data_window_button.grid(
    row=12, column=3, padx=(10, 20),
    ipadx=55, pady=(10, 20),
    sticky=W+E)

# Looping main window
root.mainloop()

# Close the connection
conn.close()
