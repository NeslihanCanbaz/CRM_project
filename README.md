CRM Projesi(Customer Relationship Management-Müşteri İlişkileri Yönetimi)
Genel
Gunumuzde bir cok kurulus verilerini yonetme ve saklama gibi opsiyonlari kismende olsa ucretsiz destekledigi icin Google drive ve bilesenlerini kullanmaktadir. Cesitli organizasyonlar IT alaninda calismak isteyen multeci kokenli kisiler icin mentor gorusmesi ve istenilen sartlari saglayanlar icin projelendirme ve mulakat asamalari dahil olmak uzere bir dizi islem yapmakta ve bu islemleri google drive uzerinde gerceklestirmektedir. Adaylarin takip edilmesi icin drive uzerinde surekli oturumun acik olmasi , excel metinlerin karisikligi ,istenilen verilere kisa yoldan ulasabilme vs gibi zorluklar nedeni ile isleri daha kolay hale getirebilecek kullanici dostu bir uygulama tasarlamak amaciyla asagidaki proje tasarlanmistir.

Kullanici Arayuzu Detaylari
Giris Penceresi

1-Kullanici Adi ve Sifre

google drive ana gmail-hesabi kullanicisi tarafindan kaydedilmis kullanici adi-sifre sahibi kisilerin erisimine izin verilmeli . Bu bilgiler Kullanicilar dosyasında yer almaktadır. Eğer kullanıcının giriş yetkisi Admin’se Tercihler - Admin menüsüne yönlendirmeli, eğer giriş yetkisi User’sa Tercihler menüsüne yönlendirmeli.

Uygulamaya özelleştirilmiş bir giriş sayfası oluşturulmalı ve bu sayfa asagidaki ozellikleri içermelidir.

Kullanici adi ve sifre icin iki ayrı input ögesi.

Bu iki bilgiye reaksiyon verecek ve sonraki bir giris butonu.

Butonun tiklandiginda basarili olup olmadigini bildirecek bir uyari yazisi.

Istege gore uygulamayi kapatacak baska bir buton ekleyip pencere goruntusu kaldırılabilir.

Tutarli ardalan renkleri, kutu kenar sekilleri, buton ozellikleri (hover, pressed, yuvarlak kenar), yazilar icin farkli fontlar ve renkler kullanarak ozellesmis ve giris penceresi oluşturulmalıdır.

Ipucu: Once bir frame yerlestirip ogeleri ustune yerlestirerek, hem frame i hem de uzerine yerlestirdiginiz ogeleri layout,spacer kullanarak dinamik boyut olusturabilirsiniz.

Tercihler

A-)Tercihler Admin

1- Basvurular

Basvurular butonu admini ilk basvuru penceresine yönlendirmeli

2- Mentor gorusmesi

Mentor gorusmesi butonu admini mentor penceresine yonlendirmeli

3- Mulakatlar

Mulakatlar butonu admini mulakatlar penceresine yonlendirmeli

4- Admin Menü

Admin butonu admini Admin penceresine yönlendirmeli.

B-)Tercihler

1- Basvurular

basvurular butonu kullaniciyi ilk basvuru penceresine yonlendirmeli

2- Mentor gorusmesi

mentor gorusmesi butonu kullaniciyi mentor penceresine yonlendirmeli

3- Mulakatlar

mulakatlar butonu kullaniciyi mulakatlar penceresine yonlendirmeli

Basvurular

1-Ara

text satirina girilen karakterler ile isim soyisimler icinde arama yapabilen bir buton islevi kazandirilmali

(orn: 'As' girisinde drive da kayitli as ile baslayan tum isimleri getirebilmeli)

2-Tum Basvurular

Tum basvurular butonu tiklandiginda driveda bulunan başvurular dosyasındaki kayitli bulunan tum basvurular ekrana getirilmeli

3-Mentor Gorusmesi Tanimlananlar (Basvurular Dosyasındaki ilgili sutun)

Mentor gorusmesi tanimlananlar butonu tiklandiginda, basvuru yaptiktan sonra kendisine mentor gorusmesi tanimlanmis kisiler ekrana getirilmeli

4-Mentor Gorusmesi Tanimlanmayanlar

Mentor gorusmesi tanimlanmayanlar butonu tiklandiginda, basvuru yaptiktan sonra kendisine halen mentor atanmamis olan kisiler ekrana getirilmeli

5- Basvurular Mükerrer Kayıt Butonu

Mükerrer Kayıt Butonu tıklandığında driveda bulunan Basvurular dosyasındaki aynı isim ve mail adresiyle kayıt olan kişiler (sadece tekrar eden adaylar) ekrana getirilmeli.

6- Önceki VIT Kontrol Butonu

Onceki VIT butonu tıklandığında Drive’da kayıtlı olan VIT1, VIT2 ve Başvurular Dosyalarının birinde veya ikisinde ortak olan tüm adayları ekrana getirmeli. (Buradaki amaç da bir adayın birden fazla VIT’e başvurup başvurmadığını görmek).

7- Farklı Kayıt Butonu

Farklı Kayıt Butonu tıklandığında Driveda kayıtlı olan VIT1 ve VIT2 de ortak olmayan adaylar ekrana getirilmeli

8- Basvuru Filtreleme Butonu

Basvuru Filtreleme Butonu tıklandığında Basvurular dosyasında bulunan mükerrer kayıtları almadan, filtreleyerek ekrana getirmeli.(Yani bir isim birden fazla kez kayıt edilmişse, bu kayıt sadece 1 kere ekrana getirilmeli)

(Eğer isterseniz, – 5/6/7/8 – bu seçenekleri QComboBox’la da yapabilirsiniz ayrı ayrı buton koymak yerine.)

9-Tercihler Ekranina Geri Don

Tercihler Ekranina Geri Don butonu tiklandiginda kullanici Tercihler ekranina geri donmeli

Mentor

1-Ara

text satirina girilen karakterler ile isim soyisimler icinde arama yapabilen bir buton islevi kazandirilmali (orn: 'As' girisinde drive da kayitli as ile baslayan tum isimleri getirebilmeli)

2-Tum Gorusmeler

Tum gorusmeler butonu tiklandiginda Mentor dosyasında kayitli tum gorusmeler ekrana getirilmeli

3-Coklu sekme

Bu sekmede secilen tercihe uygun kayitlar ekrana getirilmelidir.

4-Tercihler Ekranina Geri Don

Tercihler Ekranina Geri Don butonu tiklandiginda kullanici Tercihler ekranina geri dönmelidir.

Mulakatlar

1-Ara

text satirina girilen karakterler ile isim soyisimler icinde arama yapabilen bir buton islevi kazandirilmali (orn: 'As' girisinde drive da kayitli as ile baslayan tum isimleri getirebilmeli)

2-Proje Gonderilmis Olanlar (Mulakatlar Dosyasındaki ilgili sutun)

Proje gonderilmis olanlar butonu tiklandiginda Mulakatlar dosyasında kayitli projesi gonderilmis adaylar ekrana getirilmeli

3- Projesi Gelmis Olanlar (Mulakatlar Dosyasındaki ilgili sutun)

Projesi gelmis olanlar butonu tiklandiginda Mulakatlar dosyasında kayitli projesi gelmis adaylar ekrana getirilmeli

4-Tercihler Ekranina Geri Don

Tercihler Ekranina Geri Don butonu tiklandiginda kullanici Tercihler ekranina geri dönmeli

Admin Menü


1- Etkinlik Kaydı Butonu

Bu kayıt Google Drive’da bulunan etkinlikleri ekrana getirmelidir

2- Mail Butonu

Bu Buton takvimdeki etkinlikler çekildikten sonra etkinlikte kayıtlı e-mail adreslerine otomatik mail göndermeyi sağlamalıdır.

3- Tablo

Google Takvimde çekilen kayıtların gözükeceği bir tablo.

4-Tercihler-Admin Ekranina Geri Don Butonu

Tercihler-Admin Ekranina Geri Don butonu tiklandiginda admin Tercihler-Admin ekranina geri dönmeli
