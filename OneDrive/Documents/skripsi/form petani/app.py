from flask import Flask, render_template, request, redirect, url_for, flash,session
import joblib
import pandas as pd
import re 
from werkzeug.security import generate_password_hash, check_password_hash
import dbcouchDB as couchdb
import numpy as np
import decode

app = Flask(__name__, static_url_path='/static', template_folder='template')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#model_file = open('cluster_ahc_fix.sav', 'rb')

AC = joblib.load('cluster_ahc_fix3.sav')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/profilpetani", methods=["POST", "GET"])
def inputdatapetani():
    db = couchdb.server['databaseaglo']
    if request.method == 'POST':
        nama = request.form['nama']
        usia = request.form['usia']
        jenisKelamin = request.form['jenisKelamin']
        pendidikan = request.form['pendidikan']
        kabupaten = request.form['kabupaten']
        kelompok = request.form['kelompok']
        status_kpLahan = request.form.getlist('status_kpLahan')
        smbrModal = request.form.getlist('smbrModal')
        tnmPermusim = request.form['tnmPermusim']
        inptLuaslahan = request.form['inptLuaslahan']
        stnluasLahan = request.form['stnluasLahan']
        lmmnjdPetani = request.form['lmmnjdPetani']
        blnlamaBertani = request.form['blnlamaBertani']
        drsTanam = request.form['drsTanam']
        hridurasiTanam = request.form['hridurasiTanam']
        jmlBibit = request.form['jmlBibit']
        stnBibit = request.form['stnBibit']
        # jmlPupuk = request.form['jmlPupuk']
        # stnPupuk = request.form['stnPupuk']
        ratarataHasilpanen = request.form['ratarataHasilpanen']
        stnratarataPanen = request.form['stnratarataPanen']
        blnTanambawang = request.form.getlist('blnTanambawang')
        vrtsBawang = request.form.getlist('vrtsBawang')
        # jnsPupuk = request.form.getlist('jnsPupuk')
        # smbrPupukorganik = request.form.getlist('smbrPupukorganik')
        # smbrPupukanorganik = request.form.getlist('smbrPupukanorganik')
        # mrkPupuk = request.form.getlist('mrkPupuk')
        jnsHama =request.form.getlist('jnsHama')
        jnsPenyakit = request.form.getlist('jnsPenyakit')
        tmptbeliPestisida = request.form.getlist('tmptbeliPestisida')
        smbrPengairan = request.form.getlist('smbrPengairan')
        stlhPanen = request.form.getlist('stlhPanen')
        tmptmenjualPanen = request.form.getlist('tmptmenjualPanen')

        data = {
            'nama': nama,
            'usia': usia,
            'jenis kelamin':jenisKelamin,
            'pendidikan':pendidikan,
            'kabupaten':kabupaten,
            'anggota kelompok tani':kelompok,
            'status kepemilikan lahan':status_kpLahan,
            'sumber modal':smbrModal,
            'tanam permusim':tnmPermusim,
            'luas lahan':inptLuaslahan+" "+stnluasLahan,
            'lama menjadi petani':lmmnjdPetani+" "+blnlamaBertani,
            'durasi tanam':drsTanam+" "+hridurasiTanam,
            'bibit':jmlBibit+" "+stnBibit,
            # 'pupuk':jmlPupuk+" "+stnPupuk,
            'rata rata hasil panen':ratarataHasilpanen+" "+stnratarataPanen,
            'bulan tanam bawang':blnTanambawang,
            'varietas bawang merah':vrtsBawang,
            # 'jenis pupuk':jnsPupuk,
            # 'sumber pupuk organik':smbrPupukorganik,
            # 'sumber pupuk anorganik':smbrPupukanorganik,
            # 'merek pupuk':mrkPupuk,
            'jenis hama':jnsHama,
            'jenis penyakit':jnsPenyakit,
            'tempat membeli pestisida':tmptbeliPestisida,
            'sumber pengairan':smbrPengairan,
            'setelah panen':stlhPanen,
            'tempat menjual hasil panen':tmptmenjualPanen
        }

        # konversi kabupaten
        if kabupaten == "Boyolali":
            kabupaten_num = 1
        elif kabupaten == "Demak":
            kabupaten_num = 2
        elif kabupaten == "Kendal":
            kabupaten_num = 3
        elif kabupaten == "Brebes":
            kabupaten_num = 4
        elif kabupaten == "Temanggung":
            kabupaten_num = 5
        else:
            return "null"

        # konversi jenis kelamin
        if jenisKelamin == "Laki-Laki":
            jenisKelamin_num = 1
        else:
            jenisKelamin_num = 0
        
        #konversi pendidikan
        if pendidikan == "Tidak Lulus SD":
            pendidikan_num = 0
        elif pendidikan == "SD":
            pendidikan_num = 1
        elif pendidikan == "SMP":
            pendidikan_num = 2
        elif pendidikan == "SMA":
            pendidikan_num = 3
        elif pendidikan == "DIPLOMA":
            pendidikan_num = 4
        else:
            pendidikan_num = 5
        
        #konversi kelompok tani
        if kelompok == "ya":
            kelompok_num = 1
        else:
            kelompok_num = 0
        #data prediksi
        dataPredict= {

        }
        #data read to pandas
        #identitas
        dataPredict['Usia'] = int(usia)
        dataPredict['kabupaten']= kabupaten_num
        dataPredict['Jenis Kelamin']= jenisKelamin_num
        dataPredict['Pendidikan_Terakhir']=pendidikan_num
        dataPredict['durasi_petani']= int(lmmnjdPetani)
        dataPredict['anggota_kelompok_petani']=kelompok_num
        #status lahan
        if status_kpLahan == []:
            dataPredict["status_lahan_sendiri"] = 0
            dataPredict["status_lahan_bagi_hasil"] = 0
            dataPredict["status_lahan_sewa"] = 0

        else:
            for status_lahan_sendiri in status_kpLahan:
                if status_lahan_sendiri == "status lahan sendiri":
                    dataPredict["status_lahan_sendiri"] = 1
                else:
                    dataPredict["status_lahan_sendiri"] = 0
            for status_lahan_bagi_hasil in status_kpLahan:
                if status_lahan_bagi_hasil == "status lahan bagi hasil":
                    dataPredict["status_lahan_bagi_hasil"] = 1
                else:
                    dataPredict["status_lahan_bagi_hasil"] = 0
            for status_lahan_sewa in status_kpLahan:
                if status_lahan_sewa == "status lahan sewa":
                    dataPredict["status_lahan_sewa"] = 1
                else:
                    dataPredict["status_lahan_sewa"] = 0
        #luas lahan & durasi tanam
        dataPredict["luas_lahan"] = int(inptLuaslahan)
        dataPredict["lama_tanam"] = int(drsTanam)
        #hasil panen
        dataPredict["rata_panen"] = int(ratarataHasilpanen)
        #kali tanam
        dataPredict["kali_tanam"] = int(tnmPermusim)
        #bulan tanam
        if blnTanambawang == []:
            dataPredict["bulan_tanam_januari"] = 0
            dataPredict["bulan_tanam_februari"] = 0
            dataPredict["bulan_tanam_maret"] = 0
            dataPredict["bulan_tanam_april"] = 0
            dataPredict["bulan_tanam_mei"] = 0
            dataPredict["bulan_tanam_juni"] = 0
            dataPredict["bulan_tanam_juli"] = 0
            dataPredict["bulan_tanam_agustus"] = 0
            dataPredict["bulan_tanam_september"] = 0
            dataPredict["bulan_tanam_oktober"] = 0
            dataPredict["bulan_tanam_november"] = 0
            dataPredict["bulan_tanam_desember"] = 0
        else:
            for blntnmJanuari in blnTanambawang:
                if blntnmJanuari == "Januari":
                    dataPredict["bulan_tanam_januari"] = 1
                else:
                    dataPredict["bulan_tanam_januari"] = 0
            for blntnmFebruari in blnTanambawang:
                if blntnmFebruari == "Februari":
                    dataPredict["bulan_tanam_februari"] = 1
                else:
                    dataPredict["bulan_tanam_februari"] = 0
            for blntnmMaret in blnTanambawang:
                if blntnmMaret == "Maret":
                    dataPredict["bulan_tanam_maret"] = 1
                else:
                    dataPredict["bulan_tanam_maret"] = 0
            for blntnmApril in blnTanambawang:
                if blntnmApril == "April":
                    dataPredict["bulan_tanam_april"] = 1
                else:
                    dataPredict["bulan_tanam_april"] = 0
            for blntnmMei in blnTanambawang:
                if blntnmMei == "Mei":
                    dataPredict["bulan_tanam_mei"] = 1
                else:
                    dataPredict["bulan_tanam_mei"] = 0
            for blntnmJuni in blnTanambawang:
                if blntnmJuni == "Juni":
                    dataPredict["bulan_tanam_juni"] = 1
                else:
                    dataPredict["bulan_tanam_juni"] = 0
            for blntnmJuli in blnTanambawang:
                if blntnmJuli == "Juli":
                    dataPredict["bulan_tanam_juli"] = 1
                else:
                    dataPredict["bulan_tanam_juli"] = 0
            for blntnmAgustus in blnTanambawang:
                if blntnmAgustus == "Agustus":
                    dataPredict["bulan_tanam_agustus"] = 1
                else:
                    dataPredict["bulan_tanam_agustus"] = 0
            for blntnmSeptember in blnTanambawang:
                if blntnmSeptember == "September":
                    dataPredict["bulan_tanam_september"] = 1
                else:
                    dataPredict["bulan_tanam_september"] = 0
            for blntnmOktober in blnTanambawang:
                if blntnmOktober == "Oktober":
                    dataPredict["bulan_tanam_oktober"] = 1
                else:
                    dataPredict["bulan_tanam_oktober"] = 0
            for blntnmNovember in blnTanambawang:
                if blntnmNovember == "November":
                    dataPredict["bulan_tanam_november"] = 1
                else:
                    dataPredict["bulan_tanam_november"] = 0
            for blntnmDesember in blnTanambawang:
                if blntnmDesember == "Desember":
                    dataPredict["bulan_tanam_desember"] = 1
                else:
                    dataPredict["bulan_tanam_desember"] = 0
        #bibit
        dataPredict["kilo_bibit"] = int(jmlBibit)
        #varietas bawang
        if vrtsBawang == []:
            dataPredict["varietas_bima_brebes"] = 0
            dataPredict["varietas_bali_karet"] = 0
            dataPredict["varietas_batu_ijo"] = 0
            dataPredict["varietas_putih"] = 0
            dataPredict["varietas_garut"] = 0
            dataPredict["varietas_tanjuk"] = 0
            dataPredict["varietas_bima_jokowi"] = 0
            dataPredict["varietas_bima_juna"] = 0
            dataPredict["varietas_bima_curut"] = 0
            dataPredict["varietas_bima_jaya"] = 0
            dataPredict["varietas_bima_nganjuk"] = 0
        else:
            for varietasBimabrebes in vrtsBawang:
                if varietasBimabrebes == "Varietas Bima Brebes":
                    dataPredict["varietas_bima_brebes"] = 1
                else:
                    dataPredict["varietas_bima_brebes"] = 0
            for varietasBalikaret in vrtsBawang:
                if varietasBalikaret == "Varietas Bali Karet":
                    dataPredict["varietas_bali_karet"] = 1
                else:
                    dataPredict["varietas_bali_karet"] = 0
            for varietasBatuijo in vrtsBawang:
                if varietasBatuijo == "Varietas Batu Ijo":
                    dataPredict["varietas_batu_ijo"] = 1
                else:
                    dataPredict["varietas_batu_ijo"] = 0
            for varietasPutih in vrtsBawang:
                if varietasPutih == "Varietas Putih":
                    dataPredict["varietas_putih"] = 1
                else:
                    dataPredict["varietas_putih"] = 0
            for varietasGarut in vrtsBawang:
                if varietasGarut == "Varietas Garut":
                    dataPredict["varietas_garut"] = 1
                else:
                    dataPredict["varietas_garut"] = 0
            for varietasTanjuk in vrtsBawang:
                if varietasTanjuk == "Varietas Tanjuk":
                    dataPredict["varietas_tanjuk"] = 1
                else:
                    dataPredict["varietas_tanjuk"] = 0
            for varietasBimajokowi in vrtsBawang:
                if varietasBimajokowi == "Varietas Bima Jokowi":
                    dataPredict["varietas_bima_jokowi"] = 1
                else:
                    dataPredict["varietas_bima_jokowi"] = 0
            for varietasBimajuna in vrtsBawang:
                if varietasBimajuna == "Varietas Bima Juna":
                    dataPredict["varietas_bima_juna"] = 1
                else:
                    dataPredict["varietas_bima_juna"] = 0
            for varietasBimacurut in vrtsBawang:
                if varietasBimacurut == "Varietas Bima Curut":
                    dataPredict["varietas_bima_curut"] = 1
                else:
                    dataPredict["varietas_bima_curut"] = 0
            for varietasBimajaya in vrtsBawang:
                if varietasBimajaya == "Varietas Bima Jaya":
                    dataPredict["varietas_bima_jaya"] = 1
                else:
                    dataPredict["varietas_bima_jaya"] = 0
            for varietasNganjuk in vrtsBawang:
                if varietasNganjuk == "Varietas Nganjuk":
                    dataPredict["varietas_bima_nganjuk"] = 1
                else:
                    dataPredict["varietas_bima_nganjuk"] = 0
        #sumber modal
        if smbrModal == []:
            dataPredict["modal_tanam_sendiri"] = 0
            dataPredict["modal_tanam_pinjam"] = 0
        else:
            for smbrmdlSendiri in smbrModal:
                if smbrmdlSendiri == "Sumber Modal Sendiri":
                    dataPredict["modal_tanam_sendiri"] = 1
                else:
                    dataPredict["modal_tanam_sendiri"] = 0
            for smbrmdlPinjam in smbrModal:
                if smbrmdlPinjam == "Sumber Modal Pinjam":
                    dataPredict["modal_tanam_pinjam"] = 1
                else:
                    dataPredict["modal_tanam_pinjam"] = 0
        #jenis pupuk
        # if jnsPupuk == []:
        #     dataPredict["jenis_pupuk_organik "] = 0
        #     dataPredict["jenis_pupuk_anorganik"] = 0
        # else:
        #     for jnspupukOrganik in jnsPupuk:
        #         if jnspupukOrganik == "Organik":
        #             dataPredict["jenis_pupuk_organik "] = 1
        #         else:
        #             dataPredict["jenis_pupuk_organik "] = 0
        #     for jnspupukAnorganik in jnsPupuk:
        #         if jnspupukAnorganik == "Anorganik":
        #             dataPredict["jenis_pupuk_anorganik"] = 1
        #         else:
        #             dataPredict["jenis_pupuk_anorganik"] = 0
        #sumber pupuk
        # if smbrPupukorganik == []:
        #     dataPredict["sumber_pupuk_organik_bantuan"] = 0
        #     dataPredict["sumber_pupuk_organik_beli_dipeternak"] = 0
        #     dataPredict["sumber_pupuk_organik_kompos"] = 0
        #     dataPredict["sumber_pupuk_organik_buat_sendiri"] = 0
        #     dataPredict["sumber_pupuk_organik_kelompok_tani"] = 0
        #     dataPredict["sumber_pupuk_organik_toko_pertanian"] = 0
        #     dataPredict["sumber_pupuk_organik_kotoran_ayam"] = 0
        #     dataPredict["sumber_pupuk_organik_kotoran_sapi"] = 0
        #     dataPredict["sumber_pupuk_organik_kotoran_kambing"] = 0
        #     dataPredict["sumber_pupuk_organik_kotoran_hewan"] = 0
        # else:
        #     for smbrorgnkBantuan in smbrPupukorganik:
        #         if smbrorgnkBantuan == "Bantuan Pemerintah":
        #             dataPredict["sumber_pupuk_organik_bantuan"] = 1
        #         else:
        #             dataPredict["sumber_pupuk_organik_bantuan"] = 0
        #     for smbrorgnkPeternak in smbrPupukorganik:
        #         if smbrorgnkPeternak == "Beli di Peternak":
        #             dataPredict["sumber_pupuk_organik_beli_dipeternak"] = 1
        #         else:
        #             dataPredict["sumber_pupuk_organik_beli_dipeternak"] = 0
        #     for smbrorgnkKompos in smbrPupukorganik:
        #         if smbrorgnkKompos == "Kompos":
        #             dataPredict["sumber_pupuk_organik_kompos"] = 1
        #         else:
        #             dataPredict["sumber_pupuk_organik_kompos"] = 0
        #     for smbrorgnkBuatsendiri in smbrPupukorganik:
        #         if smbrorgnkBuatsendiri == "Buat Sendiri":
        #             dataPredict["sumber_pupuk_organik_buat_sendiri"] = 1
        #         else:
        #             dataPredict["sumber_pupuk_organik_buat_sendiri"] = 0
        #     for smbrorgnkKelompoktani in smbrPupukorganik:
        #         if smbrorgnkKelompoktani == "Kelompok Tani":
        #             dataPredict["sumber_pupuk_organik_kelompok_tani"] = 1
        #         else:
        #             dataPredict["sumber_pupuk_organik_kelompok_tani"] = 0
        #     for smbrorgnkPertanian in smbrPupukorganik:
        #         if smbrorgnkPertanian == "Toko Pertanian":
        #             dataPredict["sumber_pupuk_organik_toko_pertanian"] = 1
        #         else:
        #             dataPredict["sumber_pupuk_organik_toko_pertanian"] = 0
        #     for smbrorgnkKotoranayam in smbrPupukorganik:
        #         if smbrorgnkKotoranayam == "Kotoran Ayam":
        #             dataPredict["sumber_pupuk_organik_kotoran_ayam"] = 1
        #         else:
        #             dataPredict["sumber_pupuk_organik_kotoran_ayam"] = 0
        #     for smbrorgnkKotoransapi in smbrPupukorganik:
        #         if smbrorgnkKotoransapi == "Kotoran Sapi":
        #             dataPredict["sumber_pupuk_organik_kotoran_sapi"] = 1
        #         else:
        #             dataPredict["sumber_pupuk_organik_kotoran_sapi"] = 0
        #     for smbrorgnkKotorankambing in smbrPupukorganik:
        #         if smbrorgnkKotorankambing == "Kotoran Kambing":
        #             dataPredict["sumber_pupuk_organik_kotoran_kambing"] = 1
        #         else:
        #             dataPredict["sumber_pupuk_organik_kotoran_kambing"] = 0
        #     for smbrorgnkKotoranhewan in smbrPupukorganik:
        #         if smbrorgnkKotoranhewan == "Kotoran Hewan":
        #             dataPredict["sumber_pupuk_organik_kotoran_hewan"] = 1
        #         else:
        #             dataPredict["sumber_pupuk_organik_kotoran_hewan"] = 0
        #sumber pupuk anorganik
        # if smbrPupukanorganik == []:
        #     dataPredict["sumber_pupuk_toko_pertanian"] = 0
        #     dataPredict["sumber_pupuk_kelompok_tani"] = 0
        #     dataPredict["sumber_pupuk_peternak"] = 0
        # else:
        #     for smbranorgnkTokopertanian in smbrPupukanorganik:
        #         if smbranorgnkTokopertanian == "Toko Pertanian":
        #             dataPredict["sumber_pupuk_toko_pertanian"] = 1
        #         else:
        #             dataPredict["sumber_pupuk_toko_pertanian"] = 0
        #     for smbranorgnkKlpktani in smbrPupukanorganik:
        #         if smbranorgnkKlpktani == "Kelompok Tani":
        #             dataPredict["sumber_pupuk_kelompok_tani"] = 1
        #         else:
        #             dataPredict["sumber_pupuk_kelompok_tani"] = 0
        #     for smbranorgnkPeternak in smbrPupukanorganik:
        #         if smbranorgnkPeternak == "Peternakan":
        #             dataPredict["sumber_pupuk_peternak"] = 1
        #         else:
        #             dataPredict["sumber_pupuk_peternak"] = 0
        #merk pupuk
        # if mrkPupuk == []:
        #     dataPredict["merk_pupuk_bio_to_grow"] = 0
        #     dataPredict["merk_pupuk_dgw"] = 0
        #     dataPredict["merk_pupuk_mutiara"] = 0
        #     dataPredict["merk_pupuk_meganic"] = 0
        #     dataPredict["merk_pupuk_phoska"] = 0
        #     dataPredict["merk_pupuk_saprodap"] = 0
        #     dataPredict["merk_pupuk_hcl"] = 0
        #     dataPredict["merk_pupuk_kamas"] = 0
        #     dataPredict["merk_pupuk_meroke"] = 0
        #     dataPredict["merk_pupuk_pak_tani"] = 0
        #     dataPredict["merk_pupuk_lao_ying"] = 0
        #     dataPredict["merk_pupuk_mkp"] = 0
        #     dataPredict["merk_pupuk_phonska"] = 0
        #     dataPredict["merk_pupuk_za"] = 0
        #     dataPredict["merk_pupuk_dap"] = 0
        #     dataPredict["merk_pupuk_golden_max"] = 0
        #     dataPredict["merk_pupuk_kcl"] = 0
        #     dataPredict["merk_pupuk_mahkota"] = 0
        #     dataPredict["merk_pupuk_npk"] = 0
        #     dataPredict["merk_pupuk_sp36"] = 0
        #     dataPredict["merk_pupuk_subur_kali"] = 0
        #     dataPredict["merk_pupuk_ksn"] = 0
        #     dataPredict["merk_pupuk_petroganik"] = 0
        #     dataPredict["merk_pupuk_luar_negeri"] = 0
        #     dataPredict["merk_pupuk_randex"] = 0
        #     dataPredict["merk_pupuk_urea"] = 0
        #     dataPredict["merk_pupuk_fosfat"] = 0
        # else:
        #     for mrkpupukBiotogrow in mrkPupuk:
        #         if mrkpupukBiotogrow == "Pupuk bio to grow":
        #             dataPredict["merk_pupuk_bio_to_grow"] = 1
        #         else:
        #             dataPredict["merk_pupuk_bio_to_grow"] = 0
        #     for mrkpupukDGW in mrkPupuk:
        #         if mrkpupukDGW == "Pupuk DGW":
        #             dataPredict["merk_pupuk_dgw"] = 1
        #         else:
        #             dataPredict["merk_pupuk_dgw"] = 0
        #     for mrkpupukMutiara in mrkPupuk:
        #         if mrkpupukMutiara == "Pupuk Mutiara":
        #             dataPredict["merk_pupuk_mutiara"] = 1
        #         else:
        #             dataPredict["merk_pupuk_mutiara"] = 0
        #     for mrkpupukmeganic in mrkPupuk:
        #         if mrkpupukmeganic == "Pupuk meganic":
        #             dataPredict["merk_pupuk_meganic"] = 1
        #         else:
        #             dataPredict["merk_pupuk_meganic"] = 0
        #     for mrkpupukPhoska in mrkPupuk:
        #         if mrkpupukPhoska == "Pupuk phoska":
        #             dataPredict["merk_pupuk_phoska"] = 1
        #         else:
        #             dataPredict["merk_pupuk_phoska"] = 0
        #     for mrkpupukSaprodap in mrkPupuk:
        #         if mrkpupukSaprodap == "Pupuk saprodap":
        #             dataPredict["merk_pupuk_saprodap"] = 1
        #         else:
        #             dataPredict["merk_pupuk_saprodap"] = 0
        #     for mrkpupukHCL in mrkPupuk:
        #         if mrkpupukHCL == "Pupuk HCL":
        #             dataPredict["merk_pupuk_hcl"] = 1
        #         else:
        #             dataPredict["merk_pupuk_hcl"] = 0
        #     for mrkpupukKamas in mrkPupuk:
        #         if mrkpupukKamas   == "Pupuk kamas":
        #             dataPredict["merk_pupuk_kamas"] = 1
        #         else:
        #             dataPredict["merk_pupuk_kamas"] = 0
        #     for mrkpupukMeroke in mrkPupuk:
        #         if mrkpupukMeroke   == "Pupuk meroke":
        #             dataPredict["merk_pupuk_meroke"] = 1
        #         else:
        #             dataPredict["merk_pupuk_meroke"] = 0
        #     for mrkpupukPaktani in mrkPupuk:
        #         if mrkpupukPaktani   == "Pupuk pak tani":
        #             dataPredict["merk_pupuk_pak_tani"] = 1
        #         else:
        #             dataPredict["merk_pupuk_pak_tani"] = 0
        #     for mrkpupukLaoying in mrkPupuk:
        #         if mrkpupukLaoying   == "Pupuk lao ying":
        #             dataPredict["merk_pupuk_lao_ying"] = 1
        #         else:
        #             dataPredict["merk_pupuk_lao_ying"] = 0
        #     for mrkpupukMKP in mrkPupuk:
        #         if mrkpupukMKP   == "Pupuk MKP":
        #             dataPredict["merk_pupuk_mkp"] = 1
        #         else:
        #             dataPredict["merk_pupuk_mkp"] = 0
        #     for mrkpupukPhonska in mrkPupuk:
        #         if mrkpupukPhonska   == "Pupuk phonska":
        #             dataPredict["merk_pupuk_phonska"] = 1
        #         else:
        #             dataPredict["merk_pupuk_phonska"] = 0
        #     for mrkpupukZA in mrkPupuk:
        #         if mrkpupukZA   == "Pupuk ZA":
        #             dataPredict["merk_pupuk_za"] = 1
        #         else:
        #             dataPredict["merk_pupuk_za"] = 0
        #     for mrkpupukDAP in mrkPupuk:
        #         if mrkpupukDAP   == "Pupuk DAP":
        #             dataPredict["merk_pupuk_dap"] = 1
        #         else:
        #             dataPredict["merk_pupuk_dap"] = 0
        #     for mrkpupukGoldenmax in mrkPupuk:
        #         if mrkpupukGoldenmax   == "Pupuk golden max":
        #             dataPredict["merk_pupuk_golden_max"] = 1
        #         else:
        #             dataPredict["merk_pupuk_golden_max"] = 0
        #     for mrkpupukGoldenmax in mrkPupuk:
        #         if mrkpupukGoldenmax   == "Pupuk kcl":
        #             dataPredict["merk_pupuk_kcl"] = 1
        #         else:
        #             dataPredict["merk_pupuk_kcl"] = 0
        #     for mrkpupukMahkota in mrkPupuk:
        #         if mrkpupukMahkota   == "Pupuk mahkota":
        #             dataPredict["merk_pupuk_mahkota"] = 1
        #         else:
        #             dataPredict["merk_pupuk_mahkota"] = 0
        #     for mrkpupukNpk in mrkPupuk:
        #         if mrkpupukNpk   == "Pupuk npk":
        #             dataPredict["merk_pupuk_npk"] = 1
        #         else:
        #             dataPredict["merk_pupuk_npk"] = 0
        #     for mrkpupukSp in mrkPupuk:
        #         if mrkpupukSp   == "Pupuk sp36":
        #             dataPredict["merk_pupuk_sp36"] = 1
        #         else:
        #             dataPredict["merk_pupuk_sp36"] = 0
        #     for mrkpupukSuburkali in mrkPupuk:
        #         if mrkpupukSuburkali   == "Pupuk subur kali":
        #             dataPredict["merk_pupuk_subur_kali"] = 1
        #         else:
        #             dataPredict["merk_pupuk_subur_kali"] = 0
        #     for mrkpupukKSN in mrkPupuk:
        #         if mrkpupukKSN   == "Pupuk ksn":
        #             dataPredict["merk_pupuk_ksn"] = 1
        #         else:
        #             dataPredict["merk_pupuk_ksn"] = 0
        #     for mrkpupukPetroganik in mrkPupuk:
        #         if mrkpupukPetroganik   == "Pupuk petroganik":
        #             dataPredict["merk_pupuk_petroganik"] = 1
        #         else:
        #             dataPredict["merk_pupuk_petroganik"] = 0
        #     for mrkpupukLuarnegeri in mrkPupuk:
        #         if mrkpupukLuarnegeri   == "Pupuk luar negeri":
        #             dataPredict["merk_pupuk_luar_negeri"] = 1
        #         else:
        #             dataPredict["merk_pupuk_luar_negeri"] = 0
        #     for mrkpupukRandex in mrkPupuk:
        #         if mrkpupukRandex   == "Pupuk randex":
        #             dataPredict["merk_pupuk_randex"] = 1
        #         else:
        #             dataPredict["merk_pupuk_randex"] = 0
        #     for mrkpupukUrea in mrkPupuk:
        #         if mrkpupukUrea   == "Pupuk urea":
        #             dataPredict["merk_pupuk_urea"] = 1
        #         else:
        #             dataPredict["merk_pupuk_urea"] = 0
        #     for mrkpupukFosfat in mrkPupuk:
        #         if mrkpupukFosfat   == "Pupuk fosfat":
        #             dataPredict["merk_pupuk_fosfat"] = 1
        #         else:
        #             dataPredict["merk_pupuk_fosfat"] = 0
        #pupuk
        # dataPredict["rata_pupuk"] = int(jmlPupuk)
        #hama
        if jnsHama == []:
            dataPredict["hama_engkuk"] = 0
            dataPredict["hama_lalat"] = 0
            dataPredict["hama_grandong"] = 0
            dataPredict["hama_ulat"] = 0
            dataPredict["hama_kutu"] = 0
            dataPredict["hama_tikus"] = 0
            dataPredict["hama_wereng"] = 0
            dataPredict["hama_amitra_nosa"] = 0
            dataPredict["hama_belalang"] = 0
            dataPredict["hama_serangga"] = 0
        else:
            for hamaEngkuk in jnsHama:
                if hamaEngkuk == "Engkuk":
                    dataPredict["hama_engkuk"] = 1
                else:
                    dataPredict["hama_engkuk"] = 0
            for hamaLalat in jnsHama:
                if hamaLalat == "Lalat":
                    dataPredict["hama_lalat"] = 1
                else:
                    dataPredict["hama_engkuk"] = 0
            for hamaGrandong in jnsHama:
                if hamaGrandong == "Grandong":
                    dataPredict["hama_grandong"] = 1
                else:
                    dataPredict["hama_grandong"] = 0
            for hamaUlat in jnsHama:
                if hamaUlat == "Ulat":
                    dataPredict["hama_ulat"] = 1
                else:
                    dataPredict["hama_ulat"] = 0
            for hamaKutu in jnsHama:
                if hamaKutu == "Kutu":
                    dataPredict["hama_kutu"] = 1
                else:
                    dataPredict["hama_kutu"] = 0
            for hamaTikus in jnsHama:
                if hamaTikus == "Tikus":
                    dataPredict["hama_tikus"] = 1
                else:
                    dataPredict["hama_tikus"] = 0
            for hamaWereng in jnsHama:
                if hamaWereng == "Wareng":
                    dataPredict["hama_wereng"] = 1
                else:
                    dataPredict["hama_wereng"] = 0
            for hamaAmitranosa in jnsHama:
                if hamaAmitranosa == "Amitra Nosa":
                    dataPredict["hama_amitra_nosa"] = 1
                else:
                    dataPredict["hama_amitra_nosa"] = 0
            for hamaBelalang in jnsHama:
                if hamaBelalang == "Belalang":
                    dataPredict["hama_belalang"] = 1
                else:
                    dataPredict["hama_belalang"] = 0
            for hamaSerangga in jnsHama:
                if hamaSerangga == "Serangga":
                    dataPredict["hama_serangga"] = 1
                else:
                    dataPredict["hama_serangga"] = 0
        #jnspenyakit
        if jnsPenyakit == []:
            dataPredict["penyakit_akar_busuk"] = 0
            dataPredict["penyakit_trotol"] = 0
            dataPredict["penyakit_akar_rusak"] = 0
            dataPredict["penyakit_daun_busuk"] = 0
            dataPredict["penyakit_buah_busuk"] = 0
            dataPredict["penyakit_daun_layu"] = 0
            dataPredict["penyakit_busuk_batang"] = 0
            dataPredict["penyakit_daun_bercak"] = 0
            dataPredict["penyakit_daun_kemerahan"] = 0
            dataPredict["penyakit_umbi_busuk"] = 0
            dataPredict["penyakit_fusarium"] = 0
            dataPredict["penyakit_inul"] = 0
            dataPredict["penyakit_jamur"] = 0
            dataPredict["penyakit_mulet"] = 0
            dataPredict["penyakit_rencek"] = 0
            dataPredict["penyakit_semu_kuning"] = 0
            dataPredict["penyakit_krapak"] = 0
            dataPredict["penyakit_pohon_kering"] = 0
            dataPredict["penyakit_pucuk_menguning"] = 0
        else:
            for pnyktAkarbusuk in jnsPenyakit:
                if pnyktAkarbusuk == "Akar Busuk":
                    dataPredict["penyakit_akar_busuk"] = 1
                else:
                    dataPredict["penyakit_akar_busuk"] = 0
            for pnyktTrotol in jnsPenyakit:
                if pnyktTrotol == "Trotol":
                    dataPredict["penyakit_trotol"] = 1
                else:
                    dataPredict["penyakit_trotol"] = 0
            for pnyktAkarrusak in jnsPenyakit:
                if pnyktAkarrusak == "Akar Rusak":
                    dataPredict["penyakit_akar_rusak"] = 1
                else:
                    dataPredict["penyakit_akar_rusak"] = 0
            for pnyktDaunbusuk in jnsPenyakit:
                if pnyktDaunbusuk == "Daun Busuk":
                    dataPredict["penyakit_daun_busuk"] = 1
                else:
                    dataPredict["penyakit_daun_busuk"] = 0
            for pnyktBuahbusuk in jnsPenyakit:
                if pnyktBuahbusuk == "Buah Busuk":
                    dataPredict["penyakit_buah_busuk"] = 1
                else:
                    dataPredict["penyakit_buah_busuk"] = 0
            for pnyktDaunlayu in jnsPenyakit:
                if pnyktDaunlayu == "Daun Layu":
                    dataPredict["penyakit_daun_layu"] = 1
                else:
                    dataPredict["penyakit_daun_layu"] = 0
            for pnyktBusukbatang in jnsPenyakit:
                if pnyktBusukbatang == "Busuk Batang":
                    dataPredict["penyakit_busuk_batang"] = 1
                else:
                    dataPredict["penyakit_busuk_batang"] = 0
            for pnyktDaunbercak in jnsPenyakit:
                if pnyktDaunbercak == "Daun Bercak":
                    dataPredict["penyakit_daun_bercak"] = 1
                else:
                    dataPredict["penyakit_daun_bercak"] = 0
            for pnyktDaunkemerahan in jnsPenyakit:
                if pnyktDaunkemerahan == "Daun Kemerahan":
                    dataPredict["penyakit_daun_kemerahan"] = 1
                else:
                    dataPredict["penyakit_daun_kemerahan"] = 0
            for pnyktUmbibusuk in jnsPenyakit:
                if pnyktUmbibusuk == "Umbi Busuk":
                    dataPredict["penyakit_umbi_busuk"] = 1
                else:
                    dataPredict["penyakit_umbi_busuk"] = 0
            for pnyktFusarium in jnsPenyakit:
                if pnyktFusarium == "Fusarium":
                    dataPredict["penyakit_fusarium"] = 1
                else:
                    dataPredict["penyakit_fusarium"] = 0
            for pnyktInul in jnsPenyakit:
                if pnyktInul == "Inul":
                    dataPredict["penyakit_inul"] = 1
                else:
                    dataPredict["penyakit_inul"] = 0
            for pnyktJamur in jnsPenyakit:
                if pnyktJamur == "Jamur":
                    dataPredict["penyakit_jamur"] = 1
                else:
                    dataPredict["penyakit_jamur"] = 0
            for pnyktMulet in jnsPenyakit:
                if pnyktMulet == "Mulet":
                    dataPredict["penyakit_mulet"] = 1
                else:
                    dataPredict["penyakit_mulet"] = 0
            for pnyktRencek in jnsPenyakit:
                if pnyktRencek == "Rencek":
                    dataPredict["penyakit_rencek"] = 1
                else:
                    dataPredict["penyakit_rencek"] = 0
            for pnyktSemukuning in jnsPenyakit:
                if pnyktSemukuning == "Semu Kuning":
                    dataPredict["penyakit_semu_kuning"] = 1
                else:
                    dataPredict["penyakit_semu_kuning"] = 0
            for pnyktKrapak in jnsPenyakit:
                if pnyktKrapak == "Krapak":
                    dataPredict["penyakit_krapak"] = 1
                else:
                    dataPredict["penyakit_krapak"] = 0
            for pnyktPohonkering in jnsPenyakit:
                if pnyktPohonkering == "Pohon Kering":
                    dataPredict["penyakit_pohon_kering"] = 1
                else:
                    dataPredict["penyakit_pohon_kering"] = 0
            for pnyktPucukmenguning in jnsPenyakit:
                if pnyktPucukmenguning == "Pucuk Menguning":
                    dataPredict["penyakit_pucuk_menguning"] = 1
                else:
                    dataPredict["penyakit_pucuk_menguning"] = 0
        #tempat membeli pestisida
        if tmptbeliPestisida == []:
            dataPredict["tempat_beli_toko_obat_pertanian"] = 0
            dataPredict["tempat_beli_kelompok_tani"] = 0
        else:
            for pestisidaPertanian in tmptbeliPestisida:
                if pestisidaPertanian == "Toko Obat Pertanian":
                    dataPredict["tempat_beli_toko_obat_pertanian"] = 1
                else:
                    dataPredict["tempat_beli_toko_obat_pertanian"] = 0
            for pestisidaKlpktani in tmptbeliPestisida:
                if pestisidaKlpktani == "tempat_beli_kelompok_tani":
                    dataPredict["tempat_beli_kelompok_tani"] = 1
                else:
                    dataPredict["tempat_beli_kelompok_tani"] = 0
        #pengairan
        if smbrPengairan == []:
            dataPredict["pengairan_hujan"] = 0
            dataPredict["pengairan_irigasi"] = 0
            dataPredict["pengairan_sungai"] = 0
            dataPredict["pengairan_mata_air"] = 0
            dataPredict["pengairan_sumur"] = 0
        else:
            for pengairanHujan in smbrPengairan:
                if pengairanHujan == "Tadah Hujan":
                    dataPredict["pengairan_hujan"] = 1
                else:
                    dataPredict["pengairan_hujan"] = 0
            for pengairanIrigasi in smbrPengairan:
                if pengairanIrigasi == "Irigasi":
                    dataPredict["pengairan_irigasi"] = 1
                else:
                    dataPredict["pengairan_irigasi"] = 0
            for pengairanSungai in smbrPengairan:
                if pengairanSungai == "Sungai":
                    dataPredict["pengairan_sungai"] = 1
                else:
                    dataPredict["pengairan_sungai"] = 0
            for pengairanSungai in smbrPengairan:
                if pengairanSungai == "Sungai":
                    dataPredict["pengairan_mata_air"] = 1
                else:
                    dataPredict["pengairan_mata_air"] = 0
            for pengairanSumur in smbrPengairan:
                if pengairanSumur == "Sumur":
                    dataPredict["pengairan_sumur"] = 1
                else:
                    dataPredict["pengairan_sumur"] = 0
        #setelah panen 
        if stlhPanen == []:
            dataPredict["setelah_panen_dijual"] = 0
            dataPredict["setelah_panen_disimpan"] = 0
            dataPredict["setelah_panen_tebas"] = 0
        else:
            for panenDijual in stlhPanen:
                if panenDijual == "Dijual Langsung":
                    dataPredict["setelah_panen_dijual"] = 1
                else:
                    dataPredict["setelah_panen_dijual"] = 0
            for panenDisimpan in stlhPanen:
                if panenDisimpan == "Disimpan Dirumah":
                    dataPredict["setelah_panen_disimpan"] = 1
                else:
                    dataPredict["setelah_panen_disimpan"] = 0
            for panenDitebas in stlhPanen:
                if panenDitebas == "Tebas":
                    dataPredict["setelah_panen_tebas"] = 1
                else:
                    dataPredict["setelah_panen_tebas"] = 0
        #menjual panen
        if tmptmenjualPanen == []:
            dataPredict["jual_pasar"] = 0
            dataPredict["jual_pengepul"] = 0
            dataPredict["jual_penggoreng"] = 0
            dataPredict["jual_penebas"] = 0
            dataPredict["jual_ecer"] = 0
            dataPredict["jual_pedagang"] = 0
        else:
            for jualPasar in tmptmenjualPanen:
                if jualPasar == "Pasar":
                    dataPredict["jual_pasar"] = 1
                else:
                    dataPredict["jual_pasar"] = 0
            for jualPengepul in tmptmenjualPanen:
                if jualPengepul == "pengepul":
                    dataPredict["jual_pengepul"] = 1
                else:
                    dataPredict["jual_pengepul"] = 0
            for jualPenggoreng in tmptmenjualPanen:
                if jualPenggoreng == "UMKM":
                    dataPredict["jual_penggoreng"] = 1
                else:
                    dataPredict["jual_penggoreng"] = 0
            for jualPenebas in tmptmenjualPanen:
                if jualPenebas == "Penebas":
                    dataPredict["jual_penebas"] = 1
                else:
                    dataPredict["jual_penebas"] = 0
            for jualEcer in tmptmenjualPanen:
                if jualEcer == "Ecer":
                    dataPredict["jual_ecer"] = 1
                else:
                    dataPredict["jual_ecer"] = 0
            for jualPedagang in tmptmenjualPanen:
                if jualPedagang == "Pedagang":
                    dataPredict["jual_pedagang"] = 1
                else:
                    dataPredict["jual_pedagang"] = 0
        # print(dataPredict)
        df= pd.DataFrame(dataPredict, index=[0])
        res = AC.fit_predict(df)
        # numpyArrayOne = np.array(res)
        # numpyData={"Cluster" : numpyArrayOne}
        # dataCluster = numpyArrayOne
        # saveCluster = int(dataCluster)
        # return saveCluster
        db.save(data)
        return redirect(url_for("display_predict", res=res))
    else:
        return render_template("form_asessment_petani/index.html")


@app.route('/hasilprediksi/<res>')
def display_predict(res):
    flash("data berhasil ditambahkan", "succeed")
    return render_template("hasil.html", hasilprediksi = res)


#run
if __name__=="__main__":
    app.run(debug=False)